"""Load CPSC NEISS archived annual injury data.

Mission packet item #7, NEISS half (Gap Acquisition Campaign).
  FED_CPSC_NEISS        -- one row per sampled ER visit, statistical Weight kept
  FED_CPSC_NEISS_CODES  -- parsed neiss_fmt.txt lookup (product/diagnosis/etc codes)

Files: https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/{Y}/neiss{Y}.tsv
NOTE: cpsc.gov blocks curl/PowerShell TLS fingerprints and HEAD requests;
python-requests GET works. Checkpointed per year.

    python scripts/cpsc_neiss_load.py --run
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
BASE = "https://www.cpsc.gov/cgibin/NEISSQuery/Data"
FMT_URL = f"{BASE}/Info%20Docs/neiss_fmt.txt"
CHECKPOINT = _REPO / "logs" / "neiss_checkpoint.json"
TBL = "FED_CPSC_NEISS"
CHUNK_ROWS = 500_000
YEARS = range(1999, 2027)


def ensure_columns(conn, tbl: str, cols: list[str], existing: dict[str, set]) -> None:
    cur = conn.cursor()
    if tbl not in existing:
        cur.execute(f"SELECT COLUMN_NAME FROM {bulk.LANDING_DB}.INFORMATION_SCHEMA.COLUMNS "
                    f"WHERE TABLE_SCHEMA='{bulk.LANDING_SCHEMA}' AND TABLE_NAME='{tbl}'")
        existing[tbl] = {r[0] for r in cur.fetchall()}
    if not existing[tbl]:
        meta = (f", {bulk.META_INGESTED_AT} TIMESTAMP_NTZ, "
                f"{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR, "
                f"_SRC_YEAR VARCHAR")
        cur.execute(f'CREATE TABLE {bulk.LANDING_FQS}."{tbl}" '
                    f'({", ".join(c + " VARCHAR" for c in cols)}{meta})')
        existing[tbl] = set(cols) | {bulk.META_INGESTED_AT, bulk.META_SOURCE_RUN_ID,
                                     bulk.META_SRC_SHA256, "_SRC_YEAR"}
    else:
        for c in [c for c in cols if c not in existing[tbl]]:
            cur.execute(f'ALTER TABLE {bulk.LANDING_FQS}."{tbl}" ADD COLUMN {c} VARCHAR')
            existing[tbl].add(c)


def load_year(conn, year: int, existing: dict[str, set]) -> int:
    from snowflake.connector.pandas_tools import write_pandas

    url = f"{BASE}/Archived%20Data/{year}/neiss{year}.tsv"
    r = None
    for attempt in range(5):
        try:
            r = requests.get(url, headers=USER_AGENT, timeout=1800)
            break
        except requests.exceptions.RequestException as e:
            print(f"[{year}] download attempt {attempt+1} failed: {str(e)[:100]}")
            import time
            time.sleep(30 * (attempt + 1))
    if r is None:
        raise RuntimeError(f"download failed after retries: {url}")
    if r.status_code != 200:
        print(f"[{year}] HTTP {r.status_code} -- not available")
        return -1
    sha = hashlib.sha256(r.content).hexdigest()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    total = 0
    reader = pd.read_csv(io.BytesIO(r.content), sep="\t", dtype=str,
                         chunksize=CHUNK_ROWS, low_memory=False,
                         encoding_errors="replace", on_bad_lines="skip")
    for df in reader:
        df.columns = [bulk.sf_col(c) for c in df.columns]
        ensure_columns(conn, TBL, list(df.columns), existing)
        df = df.astype(object).where(df.notna(), None)
        df[bulk.META_INGESTED_AT] = started
        df[bulk.META_SOURCE_RUN_ID] = run_id
        df[bulk.META_SRC_SHA256] = sha
        df["_SRC_YEAR"] = str(year)
        ok, _c, _n, _ = write_pandas(
            conn, df, table_name=TBL,
            database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
            auto_create_table=False, overwrite=False, quote_identifiers=False)
        if not ok:
            raise RuntimeError(f"write_pandas failed {year}")
        total += len(df)
    print(f"[{year}] {total:,} rows  sha={sha[:12]}")
    return total


def load_codes(conn):
    """neiss_fmt.txt: SAS-format lookup 'Format name;Starting value;Ending value;Label'."""
    from snowflake.connector.pandas_tools import write_pandas
    r = requests.get(FMT_URL, headers=USER_AGENT, timeout=300)
    r.raise_for_status()
    sha = hashlib.sha256(r.content).hexdigest()
    df = pd.read_csv(io.BytesIO(r.content), sep="\t", dtype=str,
                     encoding_errors="replace", on_bad_lines="skip")
    df.columns = [bulk.sf_col(c) for c in df.columns]
    df = df.astype(object).where(df.notna(), None)
    df[bulk.META_INGESTED_AT] = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    df[bulk.META_SOURCE_RUN_ID] = str(uuid.uuid4())
    df[bulk.META_SRC_SHA256] = sha
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {bulk.LANDING_FQS}."FED_CPSC_NEISS_CODES"')
    ok, _c, _n, _ = write_pandas(conn, df, table_name="FED_CPSC_NEISS_CODES",
                                 database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
                                 auto_create_table=True, overwrite=True,
                                 quote_identifiers=False)
    print(f"[codes] {len(df):,} rows cols={list(df.columns)[:6]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if not args.run:
        print("preview: years", list(YEARS))
        return
    cp = json.loads(CHECKPOINT.read_text()) if CHECKPOINT.exists() else {}
    conn = snow.connect()
    existing: dict[str, set] = {}
    try:
        load_codes(conn)
        for y in YEARS:
            if str(y) in cp:
                continue
            n = load_year(conn, y, existing)
            cp[str(y)] = n
            CHECKPOINT.parent.mkdir(exist_ok=True)
            CHECKPOINT.write_text(json.dumps(cp, indent=1))
    finally:
        conn.close()
    print("DONE")


if __name__ == "__main__":
    main()
