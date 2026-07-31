"""Load the DEA ARCOS litigation release (Washington Post, 2006-2014).

Mission packet item #8 (Gap Acquisition Campaign).
  FED_DEA_ARCOS_FULL  (existing small FED_DEA_ARCOS left untouched)

Single ~6.9GB tsv.gz with ~380M distributor->buyer transactions.
Path: stream-download, PUT to stage (gzip native), COPY INTO all-VARCHAR
table created from the file's header row.

    python scripts/dea_arcos_full_load.py --run
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
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

URL = "https://d2ty8gaf6rmowa.cloudfront.net/dea-pain-pill-database/bulk/arcos_all_washpost.tsv.gz"
TBL = "FED_DEA_ARCOS_FULL"
# Stable, project-relative -- NOT a Claude-Code session scratchpad (those are
# tied to one session UUID and vanish/change every session, so the resume
# logic below would silently miss a prior partial/full download).
CACHE_DIR = _REPO / "outputs" / "_bulk_cache"
LOCAL = CACHE_DIR / "arcos_all_washpost.tsv.gz"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}


FULL_SIZE = 6886701113


def download() -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    have = LOCAL.stat().st_size if LOCAL.exists() else 0
    if have < FULL_SIZE:
        hdrs = dict(USER_AGENT)
        mode = "wb"
        if 0 < have:
            hdrs["Range"] = f"bytes={have}-"
            mode = "ab"
            print(f"  resuming at {have/1e9:.1f} GB")
        else:
            print(f"  downloading {URL}")
        with requests.get(URL, stream=True, timeout=14400, headers=hdrs) as r:
            r.raise_for_status()
            if mode == "ab" and r.status_code != 206:
                mode = "wb"
                have = 0
                print("  server ignored Range; restarting")
            done = have
            with open(LOCAL, mode) as f:
                for chunk in r.iter_content(1 << 22):
                    f.write(chunk)
                    done += len(chunk)
                    if done % (1 << 30) < (1 << 22):
                        print(f"    {done/1e9:.1f} GB")
    h = hashlib.sha256()
    with open(LOCAL, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def header_cols() -> list[str]:
    with gzip.open(LOCAL, "rt", encoding="utf-8", errors="replace") as f:
        line = f.readline().rstrip("\n")
    return [bulk.sf_col(c) for c in line.split("\t")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if not args.run:
        print(URL)
        return

    sha = download()
    print(f"  sha256={sha}")
    cols = header_cols()
    print(f"  {len(cols)} columns: {cols[:8]}...")
    run_id = str(uuid.uuid4())

    conn = snow.connect()
    cur = conn.cursor()
    try:
        cur.execute(f'CREATE OR REPLACE TABLE {bulk.LANDING_FQS}."{TBL}" '
                    f'({", ".join(c + " VARCHAR" for c in cols)}, '
                    f"{bulk.META_INGESTED_AT} TIMESTAMP_NTZ, "
                    f"{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR)")
        cur.execute(f'CREATE OR REPLACE STAGE {bulk.LANDING_FQS}."STG_ARCOS"')
        print("  PUT (~6.9GB upload)...")
        cur.execute(f"PUT 'file://{LOCAL.as_posix()}' @{bulk.LANDING_FQS}.\"STG_ARCOS\" "
                    f"AUTO_COMPRESS=FALSE PARALLEL=8")
        sel = ", ".join(f"${i+1}" for i in range(len(cols)))
        print("  COPY INTO...")
        cur.execute(f"""
COPY INTO {bulk.LANDING_FQS}."{TBL}"
FROM (SELECT {sel}, '{dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat()}'::TIMESTAMP_NTZ,
             '{run_id}', '{sha}'
      FROM @{bulk.LANDING_FQS}."STG_ARCOS")
FILE_FORMAT=(TYPE=CSV COMPRESSION=GZIP FIELD_DELIMITER='\\t' SKIP_HEADER=1
             FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE
             ENCODING='UTF8')
ON_ERROR=ABORT_STATEMENT
""")
        for row in cur.fetchall():
            print("  COPY:", row[:4])
        cur.execute(f'SELECT COUNT(*) FROM {bulk.LANDING_FQS}."{TBL}"')
        rows = cur.fetchone()[0]
        print(f"  ROWS={rows:,}  SOURCE_URL={URL}  SHA256={sha}")
        cur.execute(f'DROP STAGE {bulk.LANDING_FQS}."STG_ARCOS"')

        passed, report = bulk.run_quality_gate(
            conn, "fed_dea_arcos_full", TBL, run_id,
            sha256=sha, row_count=rows, source_url=URL)
        if not passed:
            sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
