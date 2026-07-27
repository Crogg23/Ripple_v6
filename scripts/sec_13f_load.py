"""Load SEC Form 13F structured data sets (2013Q2+).

Mission packet item #6 (Gap Acquisition Campaign).
  FED_SEC_13F_HOLDINGS     -- INFOTABLE.tsv  (one row per holding)
  FED_SEC_13F_FILERS       -- COVERPAGE.tsv  (one row per filing)
  FED_SEC_13F_SUBMISSIONS  -- SUBMISSION.tsv (accession -> cik/period)

Quarterly zips from sec.gov structured data sets (cleaner than parsing
EDGAR SGML). Amendments (13F-HR/A) are kept, not deduplicated -- raw landing.
Checkpointed per zip for resume.

Parallel mode: downloads up to N zips concurrently, uploads sequentially.

    python scripts/sec_13f_load.py --run [--workers 4]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import re
import sys
import uuid
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

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

INDEX_URL = "https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
CHECKPOINT = _REPO / "logs" / "sec13f_checkpoint.json"
CHUNK_ROWS = 500_000
DEFAULT_WORKERS = 4

FILE_MAP = {
    "INFOTABLE": "FED_SEC_13F_HOLDINGS",
    "COVERPAGE": "FED_SEC_13F_FILERS",
    "SUBMISSION": "FED_SEC_13F_SUBMISSIONS",
}


def list_zips() -> list[str]:
    html = requests.get(INDEX_URL, timeout=120, headers=USER_AGENT).text
    urls = sorted(set(re.findall(
        r'href="(/files/structureddata/data/form-13f-data-sets/[^"]+\.zip)"', html)))
    return ["https://www.sec.gov" + u for u in urls]


def ensure_columns(conn, tbl: str, cols: list[str], existing: dict[str, set]) -> None:
    cur = conn.cursor()
    if tbl not in existing:
        cur.execute(f"SELECT COLUMN_NAME FROM {bulk.LANDING_DB}.INFORMATION_SCHEMA.COLUMNS "
                    f"WHERE TABLE_SCHEMA='{bulk.LANDING_SCHEMA}' AND TABLE_NAME='{tbl}'")
        existing[tbl] = {r[0] for r in cur.fetchall()}
    if not existing[tbl]:
        meta = (f", {bulk.META_INGESTED_AT} TIMESTAMP_NTZ, "
                f"{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR, "
                f"_SRC_FILE VARCHAR")
        cur.execute(f'CREATE TABLE {bulk.LANDING_FQS}."{tbl}" '
                    f'({", ".join(c + " VARCHAR" for c in cols)}{meta})')
        existing[tbl] = set(cols) | {bulk.META_INGESTED_AT, bulk.META_SOURCE_RUN_ID,
                                     bulk.META_SRC_SHA256, "_SRC_FILE"}
    else:
        for c in [c for c in cols if c not in existing[tbl]]:
            cur.execute(f'ALTER TABLE {bulk.LANDING_FQS}."{tbl}" ADD COLUMN {c} VARCHAR')
            existing[tbl].add(c)


def download_zip(url: str) -> tuple[str, bytes, str]:
    """Download a zip file. Returns (label, content_bytes, sha256)."""
    label = url.rsplit("/", 1)[-1]
    resp = None
    for attempt in range(5):
        try:
            resp = requests.get(url, timeout=3600, headers=USER_AGENT)
            break
        except requests.exceptions.RequestException as e:
            print(f"[{label}] download attempt {attempt+1} failed: {str(e)[:100]}")
            import time
            time.sleep(30 * (attempt + 1))
    if resp is None:
        raise RuntimeError(f"download failed after retries: {url}")
    resp.raise_for_status()
    sha = hashlib.sha256(resp.content).hexdigest()
    print(f"[{label}] downloaded {len(resp.content):,} bytes sha={sha[:12]}")
    return label, resp.content, sha


def upload_zip(conn, label: str, content: bytes, sha: str,
               existing: dict[str, set]) -> dict[str, int]:
    """Parse and upload a downloaded zip to Snowflake."""
    from snowflake.connector.pandas_tools import write_pandas

    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    counts: dict[str, int] = {}

    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        for name in zf.namelist():
            stem = Path(name).stem.upper()
            if stem not in FILE_MAP:
                continue
            tbl = FILE_MAP[stem]
            total = 0
            with zf.open(name) as f:
                reader = pd.read_csv(f, sep="\t", dtype=str, chunksize=CHUNK_ROWS,
                                     low_memory=False, encoding_errors="replace",
                                     on_bad_lines="skip", quoting=3)
                for df in reader:
                    df.columns = [bulk.sf_col(c) for c in df.columns]
                    ensure_columns(conn, tbl, list(df.columns), existing)
                    df = df.astype(object).where(df.notna(), None)
                    df[bulk.META_INGESTED_AT] = started
                    df[bulk.META_SOURCE_RUN_ID] = run_id
                    df[bulk.META_SRC_SHA256] = sha
                    df["_SRC_FILE"] = label
                    ok, _c, _n, _ = write_pandas(
                        conn, df, table_name=tbl,
                        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
                        auto_create_table=False, overwrite=False,
                        quote_identifiers=False)
                    if not ok:
                        raise RuntimeError(f"write_pandas failed {tbl} {label}")
                    total += len(df)
            counts[stem] = total
    print(f"[{label}] loaded: " + ", ".join(f"{k}={v:,}" for k, v in counts.items()))
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS,
                    help="Number of parallel download threads (default 4)")
    args = ap.parse_args()

    zips = list_zips()
    cp = json.loads(CHECKPOINT.read_text()) if CHECKPOINT.exists() else {}
    todo = [u for u in zips if u.rsplit("/", 1)[-1] not in cp]
    print(f"{len(zips)} zips, {len(todo)} to load, {args.workers} workers")
    if not args.run:
        return

    conn = snow.connect()
    existing: dict[str, set] = {}
    cp_lock = Lock()

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(download_zip, u): u for u in todo}

            for future in as_completed(futures):
                url = futures[future]
                label = url.rsplit("/", 1)[-1]
                try:
                    _, content, sha = future.result()
                except requests.HTTPError as e:
                    print(f"[{label}] HTTP error {e} -- skipping")
                    with cp_lock:
                        cp[label] = {"error": str(e)}
                        CHECKPOINT.parent.mkdir(exist_ok=True)
                        CHECKPOINT.write_text(json.dumps(cp, indent=1))
                    continue
                except Exception as e:
                    print(f"[{label}] download failed: {e} -- skipping")
                    with cp_lock:
                        cp[label] = {"error": str(e)}
                        CHECKPOINT.parent.mkdir(exist_ok=True)
                        CHECKPOINT.write_text(json.dumps(cp, indent=1))
                    continue

                try:
                    counts = upload_zip(conn, label, content, sha, existing)
                except Exception as e:
                    print(f"[{label}] upload failed: {e}")
                    raise

                with cp_lock:
                    cp[label] = counts
                    CHECKPOINT.parent.mkdir(exist_ok=True)
                    CHECKPOINT.write_text(json.dumps(cp, indent=1))

        run_id = str(uuid.uuid4())
        for tbl in ("FED_SEC_13F_HOLDINGS", "FED_SEC_13F_FILERS", "FED_SEC_13F_SUBMISSIONS"):
            bulk.run_quality_gate(conn, "fed_sec_13f", tbl, run_id)
    finally:
        conn.close()
    print("DONE")


if __name__ == "__main__":
    main()
