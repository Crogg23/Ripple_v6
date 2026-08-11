#!/usr/bin/env python3
"""FDIC Summary of Deposits (SOD) full-history loader.

Branch-level deposits, one row = one branch-year, 1994-present
(~2.82M rows per API metadata). Replaces the 10,000-row proof slice.

Mirrors scripts/fema_ia_load.py: paginates offset/limit, appends in batches,
checkpoints the offset to disk so a kill/restart resumes. On a FRESH run
(no checkpoint) it drops and recreates the landing table with an all-VARCHAR
schema (same guard as the FEMA loader).

    python scripts/fdic_sod_load.py
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


BASE = "https://api.fdic.gov/banks/sod"
TABLE = "FED_FDIC_SOD_BRANCH_DEPOSITS"
SID = "fed_fdic_sod_branch_deposits"
TOP = 10000
CKPT = _REPO / "outputs" / "_fdic_sod_checkpoint.json"
LOG = _REPO / "outputs" / "_fdic_sod_progress.log"


def log(msg):
    line = f"{dt.datetime.now().isoformat()} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def fetch_page(offset: int, year: int | None = None) -> list[dict]:
    # NOTE: sort_by=ID is rejected (400), and the API 400s past offset 2M
    # (max_result_window). So we partition by YEAR (each ~85k rows) and
    # paginate within the year — offsets never approach the cap.
    params = {"limit": TOP, "offset": offset, "sort_by": "UNINUMBR", "sort_order": "ASC"}
    if year is not None:
        params["filters"] = f"YEAR:{year}"
    for attempt in range(6):
        try:
            r = requests.get(BASE, params=params, timeout=120,
                             headers={"User-Agent": "ripple-research/1.0"})
            if r.status_code == 200:
                return [rec.get("data", rec) for rec in r.json().get("data", [])]
            time.sleep(3 * (attempt + 1))
        except Exception:
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"failed page offset={offset}")


YEARS = list(range(1994, 2027))


def main():
    conn = snow.connect()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    total_loaded = 0
    done_years: list[int] = []

    if CKPT.exists():
        ck = json.loads(CKPT.read_text())
        done_years = ck.get("done_years", [])
        total_loaded = ck["total_loaded"]
        if "done_years" not in ck:
            # old offset-based checkpoint from the pre-partition loader:
            # its rows are an unordered mix — start over clean.
            done_years, total_loaded = [], 0
            CKPT.unlink()
        else:
            log(f"resuming: {len(done_years)} years done, total_loaded={total_loaded}")

    if not done_years:
        sample = fetch_page(0, YEARS[0])
        if not sample:
            log("no data on probe page -- aborting")
            sys.exit(1)
        cols = sorted({k for rec in sample for k in rec.keys()})
        sf_cols = [ingest._sf_col(c) for c in cols]
        cur = conn.cursor()
        # fresh full run replaces the proof slice / any partial pre-partition run
        cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{TABLE}")
        ddl_cols = ", ".join(f'"{c}" VARCHAR' for c in sf_cols)
        ddl_cols += ', "_INGESTED_AT" VARCHAR, "_SOURCE_RUN_ID" VARCHAR, "_SRC_SHA256" VARCHAR'
        cur.execute(f'CREATE TABLE LIBRARY_RAW.LANDING.{TABLE} ({ddl_cols})')
        cur.close()
        log(f"created {TABLE} with {len(sf_cols)} VARCHAR columns")

    from snowflake.connector.pandas_tools import write_pandas

    for year in YEARS:
        if year in done_years:
            continue
        offset = 0
        year_rows = 0
        while True:
            batch = fetch_page(offset, year)
            if not batch:
                break
            df = pd.DataFrame(batch)
            df.columns = [ingest._sf_col(c) for c in df.columns]
            for c in df.columns:
                df[c] = df[c].apply(_as_text)
            sha = hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()[:16]
            df["_INGESTED_AT"] = started.isoformat()
            df["_SOURCE_RUN_ID"] = run_id
            df["_SRC_SHA256"] = sha
            ok, _c, nrows, _ = write_pandas(conn, df, table_name=TABLE,
                                            database="LIBRARY_RAW", schema="LANDING",
                                            quote_identifiers=False)
            if not ok:
                raise RuntimeError(f"write failed year={year} offset={offset}")
            offset += len(batch)
            year_rows += len(batch)
        total_loaded += year_rows
        done_years.append(year)
        CKPT.write_text(json.dumps({"done_years": done_years, "total_loaded": total_loaded}))
        log(f"year={year} rows={year_rows} total_loaded={total_loaded}")

    ended = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    ingest._log_run(conn, SID, run_id, "success", total_loaded, None, run_id[:16], BASE,
                    started, ended,
                    f"{SID}; full SOD history via api.fdic.gov; {total_loaded:,} rows this run")
    log(f"DONE total_loaded={total_loaded}")
    CKPT.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
