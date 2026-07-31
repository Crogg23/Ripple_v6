"""Load CourtListener dockets bulk export into FED_COURTLISTENER_DOCKETS.

Mission packet item #5 (Gap Acquisition Campaign).
Parties/attorneys have NO bulk export (API-only) -- flagged separately.

Path: download the ~5GB csv.bz2, PUT to a Snowflake stage (as-is, bz2 is
natively supported), COPY INTO a pre-created all-VARCHAR table with the
column order taken from CourtListener's own load-bulk-data script, stamping
provenance columns in the COPY transformation.

    python scripts/courtlistener_dockets_load.py --run
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
import sys
import uuid
from pathlib import Path

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

DATE = "2026-06-30"
S3 = "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data"
DOCKETS_URL = f"{S3}/dockets-{DATE}.csv.bz2"
LOADSH_URL = f"{S3}/load-bulk-data-{DATE}.sh"
TBL = "FED_COURTLISTENER_DOCKETS"
# Stable, project-relative -- NOT a Claude-Code session scratchpad (those are
# tied to one session UUID and vanish/change every session, so the re-use
# check below would silently miss a prior 5GB download and re-fetch from
# scratch, or fail outright if the temp dir was already cleaned up).
CACHE_DIR = _REPO / "outputs" / "_bulk_cache"
LOCAL = CACHE_DIR / f"dockets-{DATE}.csv.bz2"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}


def get_columns() -> list[str]:
    s = requests.get(LOADSH_URL, timeout=120, headers=USER_AGENT).text
    m = re.search(r"COPY public\.search_docket \((.*?)\) FROM", s, re.S)
    return [c.strip().upper() for c in m.group(1).replace("\n", " ").split(",")]


def download() -> str:
    """Stream-download the bz2; returns sha256."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256()
    if LOCAL.exists() and LOCAL.stat().st_size > 5_000_000_000:
        print(f"  Using existing {LOCAL}")
        with open(LOCAL, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 22), b""):
                h.update(chunk)
        return h.hexdigest()
    print(f"  Downloading {DOCKETS_URL}")
    with requests.get(DOCKETS_URL, stream=True, timeout=7200, headers=USER_AGENT) as r:
        r.raise_for_status()
        done = 0
        with open(LOCAL, "wb") as f:
            for chunk in r.iter_content(1 << 22):
                f.write(chunk)
                h.update(chunk)
                done += len(chunk)
                if done % (1 << 30) < (1 << 22):
                    print(f"    {done/1e9:.1f} GB")
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()

    cols = get_columns()
    print(f"{len(cols)} columns: {cols[:6]}...")
    if not args.run:
        return

    sha = download()
    run_id = str(uuid.uuid4())
    print(f"  sha256={sha}")

    conn = snow.connect()
    cur = conn.cursor()
    try:
        cols_sql = ", ".join(f"{c} VARCHAR" for c in cols)
        cur.execute(f'CREATE OR REPLACE TABLE {bulk.LANDING_FQS}."{TBL}" ({cols_sql}, '
                    f"{bulk.META_INGESTED_AT} TIMESTAMP_NTZ, "
                    f"{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR)")
        cur.execute(f'CREATE OR REPLACE STAGE {bulk.LANDING_FQS}."STG_CL_DOCKETS"')
        print("  PUT (uploading ~5GB, this takes a while)...")
        cur.execute(f"PUT 'file://{LOCAL.as_posix()}' @{bulk.LANDING_FQS}.\"STG_CL_DOCKETS\" "
                    f"AUTO_COMPRESS=FALSE PARALLEL=8")
        sel = ", ".join(f"${i+1}" for i in range(len(cols)))
        print("  COPY INTO...")
        cur.execute(f"""
COPY INTO {bulk.LANDING_FQS}."{TBL}"
FROM (SELECT {sel}, '{dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat()}'::TIMESTAMP_NTZ,
             '{run_id}', '{sha}'
      FROM @{bulk.LANDING_FQS}."STG_CL_DOCKETS")
FILE_FORMAT=(TYPE=CSV COMPRESSION=BZ2 SKIP_HEADER=1
             FIELD_OPTIONALLY_ENCLOSED_BY='"' ESCAPE='\\\\'
             NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE ENCODING='UTF8'
             ERROR_ON_COLUMN_COUNT_MISMATCH=TRUE)
ON_ERROR=ABORT_STATEMENT
""")
        for row in cur.fetchall():
            print("  COPY:", row[:4])
        cur.execute(f'SELECT COUNT(*) FROM {bulk.LANDING_FQS}."{TBL}"')
        rows = cur.fetchone()[0]
        print(f"  ROWS={rows:,}  SOURCE_URL={DOCKETS_URL}  SHA256={sha}")
        cur.execute(f'DROP STAGE {bulk.LANDING_FQS}."STG_CL_DOCKETS"')

        passed, report = bulk.run_quality_gate(
            conn, "fed_courtlistener_dockets", TBL, run_id,
            sha256=sha, row_count=rows, source_url=DOCKETS_URL)
        if not passed:
            sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
