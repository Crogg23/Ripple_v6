#!/usr/bin/env python3
"""FDIC BankFind full insured-institution directory loader.

One row = one FDIC-insured institution, active and historical (~27,836 per the
API's own total). Replaces the 10,000-row API slice that the mart was built on
and that was labelled SAMPLE ONLY.

Also WIDENS the table: the slice kept 24 fields, the API returns 95 (regulator,
charter class, holding company, CBSA geography, closure/merger dates, the
CFPB supervision flags). Every column the old slice had is still present, so
anything selecting from it keeps working.

Mirrors scripts/fdic_sod_load.py: offset/limit paging, batched appends,
checkpointed to disk so a kill/restart resumes. A fresh run (no checkpoint)
drops and recreates the landing table with an all-VARCHAR schema, the same
guard the other loaders use so a page with an all-null column can never get
type-inferred as NUMBER and break a later text batch.

    python scripts/fdic_institutions_load.py
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


BASE = "https://banks.data.fdic.gov/api/institutions"
TABLE = "FED_FDIC_BANK_DATA"
SID = "fed_fdic_bank_data"
TOP = 5000
ATTEMPTS = 8
CKPT = _REPO / "outputs" / "_fdic_institutions_checkpoint.json"
LOG = _REPO / "outputs" / "_fdic_institutions_progress.log"


def log(msg):
    line = f"{dt.datetime.now().isoformat()} {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def fetch_page(offset: int) -> list[dict]:
    # sort_by is required for a stable offset walk -- without it the API is free
    # to return rows in a different order per request, which silently duplicates
    # some institutions and drops others across page boundaries.
    params = {"limit": TOP, "offset": offset, "format": "json",
              "sort_by": "CERT", "sort_order": "ASC"}
    last = None
    for attempt in range(ATTEMPTS):
        try:
            r = requests.get(BASE, params=params, timeout=min(60 + 30 * attempt, 240),
                             headers={"User-Agent": "ripple-research/1.0"})
            if r.status_code == 200:
                return [rec.get("data", rec) for rec in r.json().get("data", [])]
            last = f"HTTP {r.status_code}"
        except Exception as e:
            last = repr(e)[:120]
        wait = min(5 * (2 ** attempt), 120)
        log(f"  retry offset={offset} attempt={attempt + 1}/{ATTEMPTS} ({last}) -- sleeping {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"failed page offset={offset} ({last})")


def total_count() -> int | None:
    try:
        r = requests.get(BASE, params={"limit": 1, "format": "json"}, timeout=60,
                         headers={"User-Agent": "ripple-research/1.0"})
        return r.json().get("meta", {}).get("total")
    except Exception:
        return None


def main():
    conn = snow.connect()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    offset, total_loaded = 0, 0

    expected = total_count()
    log(f"source advertises {expected:,} institutions" if expected else "source total unknown")

    if CKPT.exists():
        ck = json.loads(CKPT.read_text())
        offset, total_loaded = ck["offset"], ck["total_loaded"]
        log(f"resuming at offset={offset}, total_loaded={total_loaded}")
    else:
        sample = fetch_page(0)
        if not sample:
            log("no data on probe page -- aborting")
            sys.exit(1)
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
        """Add any column this page has that the table does not.

        The first page does NOT contain every field. BankFind returns an
        institution's former names as PRIORNAME1..PRIORNAME10, and an
        institution with nine previous names appears well past page one -- so a
        schema inferred from the first 5,000 rows is missing PRIORNAME9 and the
        insert fails with 'invalid identifier'. Widening on demand makes the
        loader independent of which fields happen to show up early.
        """
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

    while True:
        batch = fetch_page(offset)
        if not batch:
            log(f"empty page at offset={offset} -- done")
            break
        df = pd.DataFrame(batch)
        df.columns = [ingest._sf_col(c) for c in df.columns]
        for c in df.columns:
            df[c] = df[c].apply(_as_text)
        widen(list(df.columns))
        sha = hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()[:16]
        df = df.copy()  # de-fragment before the three provenance columns go on
        df["_INGESTED_AT"] = started.isoformat()
        df["_SOURCE_RUN_ID"] = run_id
        df["_SRC_SHA256"] = sha
        ok, _c, n, _ = write_pandas(conn, df, table_name=TABLE,
                                    database="LIBRARY_RAW", schema="LANDING",
                                    auto_create_table=False, overwrite=False,
                                    quote_identifiers=False)
        if not ok:
            raise RuntimeError(f"write failed at offset={offset}")
        total_loaded += n
        offset += len(batch)
        CKPT.write_text(json.dumps({"offset": offset, "total_loaded": total_loaded}))
        log(f"offset={offset} total_loaded={total_loaded}")
        if len(batch) < TOP:
            log(f"final short page ({len(batch)}) -- done")
            break

    ended = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    note = f"{SID}; full BankFind institution directory; {total_loaded:,} rows this run"
    if expected:
        note += f" (source advertised {expected:,})"
    ingest._log_run(conn, SID, run_id, "success", total_loaded, None, run_id[:16], BASE,
                    started, ended, note)
    log(f"DONE total_loaded={total_loaded}")
    CKPT.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
