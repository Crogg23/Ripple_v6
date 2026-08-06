"""Load GLEIF Level 2 relationship records + reporting exceptions.

Mission packet item #1 (Gap Acquisition Campaign).
  INTL_GLEIF_RELATIONSHIPS  -- rr golden copy (~482K relationships)
  INTL_GLEIF_REPEX          -- reporting exceptions (~6.3M rows)

Source: https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest
Raw landing only: all original columns preserved, chunked append,
standard provenance stamps.

    python scripts/gleif_relationships_load.py --run
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
import uuid
import zipfile
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

API = "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
CHUNK_ROWS = 250_000

TARGETS = [
    ("rr", "INTL_GLEIF_RELATIONSHIPS"),
    ("repex", "INTL_GLEIF_REPEX"),
]


def load_file(conn, url: str, tbl: str) -> int:
    from snowflake.connector.pandas_tools import write_pandas

    print(f"  Downloading {url}")
    resp = requests.get(url, timeout=1800, headers=USER_AGENT)
    resp.raise_for_status()
    sha = hashlib.sha256(resp.content).hexdigest()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    print(f"  Downloaded {len(resp.content):,} bytes  sha256={sha[:16]}...")

    total = 0
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        for name in names:
            with zf.open(name) as f:
                reader = pd.read_csv(f, dtype=str, chunksize=CHUNK_ROWS,
                                     low_memory=False, encoding_errors="replace")
                first = total == 0
                for df in reader:
                    df.columns = [bulk.sf_col(c) for c in df.columns]
                    if first:
                        cols_sql = ", ".join(f'{c} VARCHAR' for c in df.columns)
                        cur = conn.cursor()
                        cur.execute(
                            f'CREATE OR REPLACE TABLE {bulk.LANDING_FQS}."{tbl}" '
                            f'({cols_sql}, {bulk.META_INGESTED_AT} TIMESTAMP_NTZ, '
                            f'{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR)')
                    df = df.astype(object).where(df.notna(), None)
                    df[bulk.META_INGESTED_AT] = started
                    df[bulk.META_SOURCE_RUN_ID] = run_id
                    df[bulk.META_SRC_SHA256] = sha
                    ok, _c, _n, _ = write_pandas(
                        conn, df, table_name=tbl,
                        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
                        auto_create_table=False, overwrite=False,
                        quote_identifiers=False,
                    )
                    if not ok:
                        raise RuntimeError(f"write_pandas failed for {tbl}")
                    first = False
                    total += len(df)
                    print(f"    {tbl}: {total:,} rows loaded")
    print(f"  SOURCE_URL={url}")
    print(f"  SHA256={sha}  ROWS={total}")
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()

    meta = requests.get(API, timeout=60, headers=USER_AGENT).json()["data"]
    plan = []
    for key, tbl in TARGETS:
        c = meta[key]["full_file"]["csv"]
        plan.append((tbl, c["url"], c["record_count"]))
        print(f"{tbl}: {c['record_count']:,} records  {c['size_human_readable']}  {c['url']}")

    if not args.run:
        print("\nPreview only. Re-run with --run to load.")
        return

    conn = snow.connect()
    shortfalls = []
    try:
        for tbl, url, expected in plan:
            n = load_file(conn, url, tbl)
            print(f"  EXPECTED={expected:,}  LOADED={n:,}")
            # Quality gate (audit 2026-08-05/06 finding: this loader had none at
            # all -- it prints EXPECTED vs LOADED but never acted on the gap.
            # GLEIF's own API response gives an authoritative expected count, so
            # use it directly rather than a generic density check.
            if expected and n < expected * 0.98:
                print(f"  QUALITY GATE FAILED {tbl}: loaded {n:,} < 98% of "
                      f"source-declared {expected:,}")
                shortfalls.append(tbl)
    finally:
        conn.close()
    if shortfalls:
        raise RuntimeError(f"QUALITY GATE FAILED for: {', '.join(shortfalls)}")


if __name__ == "__main__":
    main()
