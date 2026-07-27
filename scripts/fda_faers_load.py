"""Load FDA FAERS/LAERS quarterly adverse-event files.

Mission packet item #3 (Gap Acquisition Campaign).
  FED_FDA_FAERS_DEMO / _DRUG / _REAC / _OUTC / _INDI

Quarterly ASCII zips ($-delimited) from fis.fda.gov, 2004Q1..present.
Legacy LAERS (pre-2012Q4) and FAERS columns are unioned: new columns are
added to the landing table via ALTER TABLE ADD COLUMN, legacy rows keep NULLs.
Raw landing only -- no dedup, no rename. Checkpointed per quarter for resume.

Parallel mode: downloads up to N quarters concurrently while uploading
completed downloads to Snowflake. Checkpoint is still per-quarter (safe to
kill and resume at any time).

    python scripts/fda_faers_load.py --run [--start 2004q1] [--end 2026q1] [--workers 4]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
import time
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

USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
CHECKPOINT = _REPO / "logs" / "faers_checkpoint.json"
FILE_TYPES = ["DEMO", "DRUG", "REAC", "OUTC", "INDI"]
CHUNK_ROWS = 500_000
DEFAULT_WORKERS = 4


def quarters(start: str, end: str) -> list[str]:
    sy, sq = int(start[:4]), int(start[5])
    ey, eq = int(end[:4]), int(end[5])
    out = []
    y, q = sy, sq
    while (y, q) <= (ey, eq):
        out.append(f"{y}q{q}")
        q += 1
        if q == 5:
            y, q = y + 1, 1
    return out


def url_for(quarter: str) -> str:
    y, q = int(quarter[:4]), int(quarter[5])
    prefix = "aers" if (y, q) < (2012, 4) else "faers"
    return f"https://fis.fda.gov/content/Exports/{prefix}_ascii_{quarter}.zip"


def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())
    return {}


def save_checkpoint(cp: dict):
    CHECKPOINT.parent.mkdir(exist_ok=True)
    CHECKPOINT.write_text(json.dumps(cp, indent=1))


def download_quarter(quarter: str) -> tuple[str, bytes, str]:
    """Download a quarter's zip. Returns (quarter, content_bytes, sha256)."""
    url = url_for(quarter)
    resp = None
    for attempt in range(5):
        try:
            resp = requests.get(url, timeout=1800, headers=USER_AGENT)
            break
        except requests.exceptions.RequestException as e:
            print(f"[{quarter}] download attempt {attempt+1} failed: {str(e)[:100]}")
            time.sleep(30 * (attempt + 1))
    if resp is None:
        raise RuntimeError(f"download failed after retries: {url}")
    resp.raise_for_status()
    sha = hashlib.sha256(resp.content).hexdigest()
    print(f"[{quarter}] downloaded {len(resp.content):,} bytes  sha={sha[:12]}")
    return quarter, resp.content, sha


def ensure_columns(conn, tbl: str, cols: list[str], existing: dict[str, set]) -> None:
    cur = conn.cursor()
    if tbl not in existing:
        cur.execute(f"SELECT COLUMN_NAME FROM {bulk.LANDING_DB}.INFORMATION_SCHEMA.COLUMNS "
                    f"WHERE TABLE_SCHEMA='{bulk.LANDING_SCHEMA}' AND TABLE_NAME='{tbl}'")
        existing[tbl] = {r[0] for r in cur.fetchall()}
    if not existing[tbl]:
        meta = (f", {bulk.META_INGESTED_AT} TIMESTAMP_NTZ, "
                f"{bulk.META_SOURCE_RUN_ID} VARCHAR, {bulk.META_SRC_SHA256} VARCHAR, "
                f"_SRC_QUARTER VARCHAR")
        cur.execute(f'CREATE TABLE {bulk.LANDING_FQS}."{tbl}" '
                    f'({", ".join(c + " VARCHAR" for c in cols)}{meta})')
        existing[tbl] = set(cols) | {bulk.META_INGESTED_AT, bulk.META_SOURCE_RUN_ID,
                                     bulk.META_SRC_SHA256, "_SRC_QUARTER"}
    else:
        missing = [c for c in cols if c not in existing[tbl]]
        for c in missing:
            cur.execute(f'ALTER TABLE {bulk.LANDING_FQS}."{tbl}" ADD COLUMN {c} VARCHAR')
            existing[tbl].add(c)


def upload_quarter(conn, quarter: str, content: bytes, sha: str,
                   existing: dict[str, set]) -> dict[str, int]:
    """Parse and upload a downloaded quarter to Snowflake. Returns file-type counts."""
    from snowflake.connector.pandas_tools import write_pandas

    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    counts: dict[str, int] = {}

    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        names = {n.upper(): n for n in zf.namelist()}
        for ft in FILE_TYPES:
            match = [orig for up, orig in names.items()
                     if up.endswith(".TXT") and Path(up).name.startswith(ft)]
            if not match:
                print(f"[{quarter}] WARNING no {ft} file found")
                continue
            tbl = f"FED_FDA_FAERS_{ft}"
            total = 0
            with zf.open(match[0]) as f:
                reader = pd.read_csv(f, sep="$", dtype=str, chunksize=CHUNK_ROWS,
                                     low_memory=False, encoding_errors="replace",
                                     on_bad_lines="skip")
                for df in reader:
                    df.columns = [bulk.sf_col(c) for c in df.columns]
                    ensure_columns(conn, tbl, list(df.columns), existing)
                    df = df.astype(object).where(df.notna(), None)
                    df[bulk.META_INGESTED_AT] = started
                    df[bulk.META_SOURCE_RUN_ID] = run_id
                    df[bulk.META_SRC_SHA256] = sha
                    df["_SRC_QUARTER"] = quarter
                    ok, _c, _n, _ = write_pandas(
                        conn, df, table_name=tbl,
                        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
                        auto_create_table=False, overwrite=False,
                        quote_identifiers=False)
                    if not ok:
                        raise RuntimeError(f"write_pandas failed {tbl} {quarter}")
                    total += len(df)
            counts[ft] = total
    print(f"[{quarter}] loaded: " + ", ".join(f"{k}={v:,}" for k, v in counts.items()))
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--start", default="2004q1")
    ap.add_argument("--end", default="2026q1")
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS,
                    help="Number of parallel download threads (default 4)")
    args = ap.parse_args()

    qs = quarters(args.start, args.end)
    cp = load_checkpoint()
    todo = [q for q in qs if q not in cp]
    print(f"{len(qs)} quarters in range, {len(todo)} to load, {args.workers} workers")
    if not args.run:
        return

    conn = snow.connect()
    existing: dict[str, set] = {}
    cp_lock = Lock()

    try:
        # Pipeline: download in parallel, upload sequentially (Snowflake conn is not
        # thread-safe for writes, and ensure_columns/ALTER TABLE needs serialization).
        # Downloads are the bottleneck (slow gov servers), so overlapping them is the win.
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(download_quarter, q): q for q in todo}

            for future in as_completed(futures):
                quarter = futures[future]
                try:
                    _, content, sha = future.result()
                except requests.HTTPError as e:
                    print(f"[{quarter}] HTTP error: {e} -- skipping")
                    with cp_lock:
                        cp[quarter] = {"error": str(e)}
                        save_checkpoint(cp)
                    continue
                except Exception as e:
                    print(f"[{quarter}] download failed: {e} -- skipping")
                    with cp_lock:
                        cp[quarter] = {"error": str(e)}
                        save_checkpoint(cp)
                    continue

                # Upload sequentially (safe)
                try:
                    counts = upload_quarter(conn, quarter, content, sha, existing)
                except Exception as e:
                    print(f"[{quarter}] upload failed: {e}")
                    raise

                with cp_lock:
                    cp[quarter] = counts
                    save_checkpoint(cp)

        run_id = str(uuid.uuid4())
        for ft in FILE_TYPES:
            tbl = f"FED_FDA_FAERS_{ft}"
            bulk.run_quality_gate(conn, f"fed_fda_faers_{ft.lower()}", tbl, run_id)
    finally:
        conn.close()
    print("DONE")


if __name__ == "__main__":
    main()
