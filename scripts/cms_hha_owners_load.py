"""Load the CMS Home Health Agency All Owners file (data.cms.gov).

Dataset: fc009b2d-7846-44b1-b4a1-692f0c143879, quarterly (R/P3M).
One row per (enrollment, owner, role). 38 columns, all landed as text.
Joins to FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS on ENROLLMENT_ID to get the CCN.

Written 2026-09-07 for docket E74 (who is the new owner of a home health agency).
See reports/dead_ends_scope_C_refetch_2026-09-07.md for why this file was never
landed before: only a TYPE_OF_OWNERSHIP category existed in the warehouse.

    python scripts/cms_hha_owners_load.py            # dry run: header + row count
    python scripts/cms_hha_owners_load.py --run      # land it

Append-only: write_pandas with no overwrite. The table is created if missing
with every column VARCHAR. A rerun on the same day doubles the rows, so --run
refuses when the table already holds rows unless --append is passed.
The load stops if the column count is not 38 or the row count moves more than
20% from EXPECTED_ROWS; pass --expect-rows to reset the baseline.
"""
from __future__ import annotations

import argparse
import hashlib
import io
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

DATASET_ID = "fc009b2d-7846-44b1-b4a1-692f0c143879"
CSV_URL = ("https://data.cms.gov/sites/default/files/2026-07/"
           "e3c50419-ff93-4b7a-964c-f8b1d622d817/HHA_All_Owners_2026.07.17.csv")
SOURCE_ID = "fed_cms_home_health_owners"
TABLE = "FED_CMS_HOME_HEALTH_OWNERS"
EXPECTED_COLS = 38
EXPECTED_ROWS = 101_188   # data-api stats endpoint, read 2026-09-07
USER_AGENT = "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"


def fetch_csv(url: str) -> bytes:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=300)
    r.raise_for_status()
    return r.content


def read_frame(content: bytes) -> pd.DataFrame:
    # CMS ships this as Windows-1252 (a 0x96 en-dash sits at byte 46,777 of the
    # 2026-07-17 file). Try utf-8 first so a future clean file still reads.
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("cp1252")
    df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False)
    df.columns = [bulk.sf_col(c) for c in df.columns]
    # blank string -> NULL, so count(x) means "has a value"
    df = df.replace({"": None})
    return df


def landed_rows(conn) -> int | None:
    cur = conn.cursor()
    try:
        return cur.execute(f'select count(*) from {bulk.LANDING_FQS}."{TABLE}"').fetchone()[0]
    except Exception:
        return None   # table does not exist yet
    finally:
        cur.close()


def upload(conn, df: pd.DataFrame, run_id: str):
    from snowflake.connector.pandas_tools import write_pandas
    df = df.copy()
    df["INGESTED_AT"] = pd.Timestamp.utcnow().isoformat()
    df["_SOURCE_RUN_ID"] = run_id
    cols_sql = ", ".join(f'"{c}" VARCHAR' for c in df.columns)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {bulk.LANDING_FQS}."{TABLE}" ({cols_sql})')
    cur.close()
    write_pandas(conn, df, TABLE, database=bulk.LANDING_DB,
                 schema=bulk.LANDING_SCHEMA, quote_identifiers=False,
                 auto_create_table=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="land the file (default: dry run)")
    ap.add_argument("--append", action="store_true",
                    help="allow --run when the table already holds rows")
    ap.add_argument("--url", default=CSV_URL)
    ap.add_argument("--expect-rows", type=int, default=EXPECTED_ROWS,
                    help="row-count baseline; the load stops if the file is off by more than 20%%")
    args = ap.parse_args()

    print(f"fetching {args.url}")
    content = fetch_csv(args.url)
    sha = hashlib.sha256(content).hexdigest()
    df = read_frame(content)
    print(f"  {len(content):,} bytes, sha256 {sha[:12]}")
    print(f"  {len(df.columns)} columns, {len(df):,} rows (expected {EXPECTED_COLS} / {EXPECTED_ROWS:,})")
    print("  header:")
    for c in df.columns:
        print(f"    {c}")

    if len(df.columns) != EXPECTED_COLS:
        print(f"STOP: column count {len(df.columns)} != {EXPECTED_COLS}; the file changed shape")
        sys.exit(1)
    if abs(len(df) - args.expect_rows) > 0.2 * args.expect_rows:
        print(f"STOP: row count {len(df):,} is more than 20% off the baseline {args.expect_rows:,}; "
              "a truncated or mis-served file. Pass --expect-rows if the source really moved.")
        sys.exit(1)

    if not args.run:
        print("\n(dry run -- add --run to land)")
        return

    run_id = str(uuid.uuid4())
    conn = snow.connect()
    have = landed_rows(conn)
    if have:
        print(f"  {TABLE} already holds {have:,} rows")
        if not args.append:
            print("STOP: refusing to append on top of an existing load; pass --append if that is wanted")
            conn.close()
            sys.exit(1)

    upload(conn, df, run_id)
    n = landed_rows(conn)
    print(f"  landed -> {bulk.LANDING_FQS}.{TABLE}: {n:,} rows")

    passed, report = bulk.run_quality_gate(
        conn, SOURCE_ID, TABLE, run_id, sha256=sha, row_count=len(df),
        source_url=args.url, file_bytes=len(content))
    conn.close()
    if not passed:
        print(f"QUALITY GATE FAILED {TABLE}: {report}")
        sys.exit(1)
    print("DONE")


if __name__ == "__main__":
    main()
