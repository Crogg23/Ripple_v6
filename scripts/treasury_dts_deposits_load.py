#!/usr/bin/env python3
"""Treasury Daily Statement — operating-cash deposits and withdrawals, full history.

One row = one line of the Daily Treasury Statement's deposits/withdrawals table
(~478,149 records per the API's own total-count). Replaces the 10,000-row slice
that sat on an exact page boundary.

This is the federal government's daily cash ledger: what came in, what went out,
by category, every business day. Useful precisely because it is daily -- annual
budget tables cannot show a payment stopping mid-month.

Paginates page[number]/page[size], appends in batches, checkpoints the page
number so a kill/restart resumes. A fresh run drops and recreates the landing
table as all-VARCHAR, the same guard the other loaders use.

    python scripts/treasury_dts_deposits_load.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import time
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import ingest  # noqa: E402


def _as_text(v):
    """Stringify for an all-VARCHAR landing table WITHOUT inventing the text 'nan'.

    THE BUG THIS FIXES (2026-08-11). Every loader here did
    `None if v is None else str(v)`. pandas does not keep a JSON null as None --
    it becomes float NaN as soon as the column is built -- so `v is None` was
    False and str(NaN) wrote the four characters n-a-n into the warehouse. The
    column then reads as populated: FDIC's LEI showed 6,260 non-null values, of
    which 4,008 were the string 'nan'. That is exactly the sentinel-masked-blank
    trap that has already fooled this platform on two other join keys, and it is
    worse for a KEY column, because 'nan' joins to 'nan'.

    Also catches pandas' NA/NaT and the whitespace-only strings that some of
    these APIs return in place of a null.
    """
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass  # arrays/lists raise here; they are real values, fall through
    s = str(v)
    return None if s.strip() == "" else s


BASE = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
        "/v1/accounting/dts/deposits_withdrawals_operating_cash")
TABLE = "FED_TREASURY_DTS_DEPOSITS"
SID = "fed_treasury_dts_deposits"
PAGE_SIZE = 10000
ATTEMPTS = 8
CKPT = _REPO / "outputs" / "_treasury_dts_checkpoint.json"
LOG = _REPO / "outputs" / "_treasury_dts_progress.log"


def log(msg):
    line = f"{dt.datetime.now().isoformat()} {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def fetch_page(page: int):
    # Sorted by record_date so the page walk is stable; an unsorted offset walk
    # can repeat and skip rows across page boundaries.
    params = {"page[size]": PAGE_SIZE, "page[number]": page, "sort": "record_date"}
    last = None
    for attempt in range(ATTEMPTS):
        try:
            r = requests.get(BASE, params=params, timeout=min(60 + 30 * attempt, 240))
            if r.status_code == 200:
                d = r.json()
                return d.get("data", []), d.get("meta", {}).get("total-count")
            last = f"HTTP {r.status_code}"
        except Exception as e:
            last = repr(e)[:120]
        wait = min(5 * (2 ** attempt), 120)
        log(f"  retry page={page} attempt={attempt + 1}/{ATTEMPTS} ({last}) -- sleeping {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"failed page={page} ({last})")


def main():
    conn = snow.connect()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    page, total_loaded = 1, 0

    if CKPT.exists():
        ck = json.loads(CKPT.read_text())
        page, total_loaded = ck["page"], ck["total_loaded"]
        log(f"resuming at page={page}, total_loaded={total_loaded}")
    else:
        sample, expected = fetch_page(1)
        if not sample:
            log("no data on probe page -- aborting")
            sys.exit(1)
        log(f"source advertises {expected:,} records" if expected else "total unknown")
        cols = sorted({k for rec in sample for k in rec.keys()})
        sf_cols = [ingest._sf_col(c) for c in cols]
        cur = conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{TABLE}")
        ddl = ", ".join(f'"{c}" VARCHAR' for c in sf_cols)
        ddl += ', "_INGESTED_AT" VARCHAR, "_SOURCE_RUN_ID" VARCHAR, "_SRC_SHA256" VARCHAR'
        cur.execute(f"CREATE TABLE LIBRARY_RAW.LANDING.{TABLE} ({ddl})")
        cur.close()
        log(f"created {TABLE} with {len(sf_cols)} VARCHAR columns")

    from snowflake.connector.pandas_tools import write_pandas

    def existing_cols():
        c = conn.cursor()
        c.execute("SELECT COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS"
                  f" WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME='{TABLE}'")
        out = {r[0].upper() for r in c.fetchall()}
        c.close()
        return out

    known = existing_cols()

    def widen(df_cols):
        """Add any field a later page introduces. Same guard as the BankFind
        loader, where a field that only appears past page one (PRIORNAME9) broke
        the insert with 'invalid identifier'."""
        nonlocal known
        missing = [c for c in df_cols if c.upper() not in known]
        if not missing:
            return
        c = conn.cursor()
        for col in missing:
            c.execute(f'ALTER TABLE LIBRARY_RAW.LANDING.{TABLE} ADD COLUMN "{col}" VARCHAR')
        c.close()
        known |= {m.upper() for m in missing}
        log(f"  widened table with {len(missing)} new column(s): {', '.join(missing[:8])}")

    expected_total = None
    while True:
        batch, expected = fetch_page(page)
        expected_total = expected_total or expected
        if not batch:
            log(f"empty page at page={page} -- done")
            break
        df = pd.DataFrame(batch)
        df.columns = [ingest._sf_col(c) for c in df.columns]
        for c in df.columns:
            df[c] = df[c].apply(_as_text)
        widen(list(df.columns))
        sha = hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()[:16]
        df = df.copy()
        df["_INGESTED_AT"] = started.isoformat()
        df["_SOURCE_RUN_ID"] = run_id
        df["_SRC_SHA256"] = sha
        ok, _c, n, _ = write_pandas(conn, df, table_name=TABLE,
                                    database="LIBRARY_RAW", schema="LANDING",
                                    auto_create_table=False, overwrite=False,
                                    quote_identifiers=False)
        if not ok:
            raise RuntimeError(f"write failed at page={page}")
        total_loaded += n
        page += 1
        CKPT.write_text(json.dumps({"page": page, "total_loaded": total_loaded}))
        if page % 5 == 0 or len(batch) < PAGE_SIZE:
            log(f"page={page - 1} total_loaded={total_loaded}")
        if len(batch) < PAGE_SIZE:
            log(f"final short page ({len(batch)}) -- done")
            break

    ended = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    note = f"{SID}; full Daily Treasury Statement cash history; {total_loaded:,} rows this run"
    if expected_total:
        note += f" (source advertised {expected_total:,})"
    ingest._log_run(conn, SID, run_id, "success", total_loaded, None, run_id[:16], BASE,
                    started, ended, note)
    log(f"DONE total_loaded={total_loaded}")
    CKPT.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
