"""Shared bulk-load utilities -- parallel download + fast Snowflake landing.

All agency discovery loaders (SEC, EPA, DOL, IRS) import this to avoid
duplicating the download/load/stamp machinery.  Optimized for throughput:
  - ThreadPoolExecutor for parallel downloads + loads
  - PUT + COPY INTO for files > SMALL_THRESHOLD (bypasses write_pandas overhead)
  - ZipFile over BytesIO (no temp extraction directory)

    from _bulk_load_utils import fast_load, load_zip_csvs, parallel_load, ...
"""
from __future__ import annotations

import concurrent.futures
import datetime as dt
import hashlib
import io
import re
import tempfile
import time
import uuid
import zipfile
from pathlib import Path
from typing import Callable

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
import sys
sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass

import ingest  # noqa: E402
import snow    # noqa: E402
from config import settings  # noqa: E402

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
LANDING_DB = settings.raw_database      # LIBRARY_RAW
LANDING_SCHEMA = settings.raw_schema    # LANDING
LANDING_FQS = f'"{LANDING_DB}"."{LANDING_SCHEMA}"'

MAX_WORKERS = 6
SMALL_THRESHOLD = 20_000_000  # 20 MB -- above this, use PUT+COPY path
DEFAULT_MAX_ROWS = 500_000
DEFAULT_TIMEOUT = 300

# Provenance columns
META_INGESTED_AT = ingest.META_INGESTED_AT
META_SOURCE_RUN_ID = ingest.META_SOURCE_RUN_ID
META_SRC_SHA256 = ingest.META_SRC_SHA256


# ---------------------------------------------------------------------------
# Table naming
# ---------------------------------------------------------------------------
def table_name(prefix: str, title: str, max_len: int = 60) -> str:
    """Convert a dataset title to FED_{AGENCY}_{TITLE} table name."""
    name = re.sub(r'[^a-zA-Z0-9]+', '_', title).strip('_').upper()
    name = re.sub(r'_+', '_', name)
    full = f"{prefix}_{name}"
    if len(full) > max_len:
        full = full[:max_len].rstrip('_')
    return full


def sf_col(name: str) -> str:
    """Sanitize column name for Snowflake (delegates to ingest._sf_col)."""
    return ingest._sf_col(name)


# ---------------------------------------------------------------------------
# Already-loaded check
# ---------------------------------------------------------------------------
def get_loaded_tables(conn) -> set[str]:
    """Return the set of table names already in LANDING."""
    cur = conn.cursor()
    cur.execute(f"SELECT TABLE_NAME FROM {LANDING_DB}.INFORMATION_SCHEMA.TABLES "
                f"WHERE TABLE_SCHEMA='{LANDING_SCHEMA}'")
    return {r[0] for r in cur.fetchall()}


# ---------------------------------------------------------------------------
# Header check (fast -- just first 4KB)
# ---------------------------------------------------------------------------
def check_header(url: str, user_agent: dict | None = None, timeout: int = 20) -> list[str] | None:
    """Fetch just the first 4KB to read CSV column headers. Returns col names or None."""
    try:
        headers = {"Range": "bytes=0-4096"}
        if user_agent:
            headers.update(user_agent)
        resp = requests.get(url, stream=True, timeout=timeout, headers=headers)
        if resp.status_code not in (200, 206):
            return None
        chunk = resp.content.decode("utf-8", errors="ignore")
        first_line = chunk.split("\n")[0].strip()
        if not first_line or len(first_line) < 5:
            return None
        cols = [c.strip().strip('"').upper() for c in first_line.split(",")]
        return cols
    except Exception:
        return None


def has_entity_key(cols: list[str], key_set: set[str]) -> list[str]:
    """Return which entity keys are present in a column list."""
    return [c for c in cols if c in key_set]


# ---------------------------------------------------------------------------
# Loading paths
# ---------------------------------------------------------------------------
def fast_load(conn, url: str, tbl: str, *,
              user_agent: dict | None = None,
              max_rows: int = DEFAULT_MAX_ROWS,
              timeout: int = DEFAULT_TIMEOUT) -> int:
    """Download CSV and load to Snowflake. Auto-picks the fastest path."""
    headers = user_agent or {}
    resp = requests.get(url, timeout=timeout, headers=headers)
    resp.raise_for_status()
    return _load_bytes(conn, resp.content, tbl, max_rows=max_rows)


def _load_bytes(conn, content: bytes, tbl: str, *, max_rows: int = DEFAULT_MAX_ROWS) -> int:
    """Load CSV bytes into a Snowflake table with provenance stamps."""
    from snowflake.connector.pandas_tools import write_pandas

    sha = hashlib.sha256(content).hexdigest()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc)

    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows,
                     low_memory=False, encoding_errors="replace")
    if df.empty:
        return 0

    # Normalize column names
    df.columns = [sf_col(c) for c in df.columns]
    # Provenance stamps
    df[META_INGESTED_AT] = started.replace(tzinfo=None)
    df[META_SOURCE_RUN_ID] = run_id
    df[META_SRC_SHA256] = sha

    ok, _c, _n, _ = write_pandas(
        conn, df, table_name=tbl,
        database=LANDING_DB, schema=LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas failed for {tbl}")
    return len(df)


def load_zip_csvs(conn, url: str, prefix: str, key_set: set[str], *,
                  user_agent: dict | None = None,
                  max_rows: int = DEFAULT_MAX_ROWS,
                  timeout: int = 600) -> list[tuple[str, int, list[str]]]:
    """Download a ZIP, iterate CSVs inside, load each that has entity keys.

    Returns list of (table_name, row_count, keys_found) for each loaded CSV.
    """
    headers = user_agent or {}
    resp = requests.get(url, timeout=timeout, headers=headers)
    resp.raise_for_status()

    results = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(('.csv', '.txt')):
                continue
            with zf.open(name) as f:
                header_line = f.readline().decode("utf-8", errors="ignore")
            cols = [c.strip().strip('"').upper() for c in header_line.split(",")]
            keys_found = has_entity_key(cols, key_set)
            if not keys_found:
                continue
            tbl = table_name(prefix, Path(name).stem)
            try:
                with zf.open(name) as f:
                    n = _load_bytes(conn, f.read(), tbl, max_rows=max_rows)
                if n > 0:
                    results.append((tbl, n, keys_found))
                    print(f"    -> {tbl}: {n:,} rows (keys: {keys_found})")
            except Exception as e:
                print(f"    FAILED {tbl}: {str(e)[:120]}")
    return results


# ---------------------------------------------------------------------------
# Parallel executor
# ---------------------------------------------------------------------------
def parallel_load(tasks: list[dict], max_workers: int = MAX_WORKERS,
                  label: str = "load") -> list[dict]:
    """Run multiple load jobs in parallel.

    Each task dict: {"fn": callable, "args": tuple, "kwargs": dict, "name": str}
    Returns list of {"name", "result"|"error"} dicts.
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {}
        for t in tasks:
            fut = ex.submit(t["fn"], *t.get("args", ()), **t.get("kwargs", {}))
            futures[fut] = t.get("name", "?")
        for fut in concurrent.futures.as_completed(futures):
            name = futures[fut]
            try:
                r = fut.result()
                results.append({"name": name, "result": r})
                print(f"  [{label}] {name}: OK")
            except Exception as e:
                results.append({"name": name, "error": str(e)[:200]})
                print(f"  [{label}] {name}: FAILED - {str(e)[:100]}")
    return results


def parallel_header_check(urls: list[tuple[str, str]], key_set: set[str],
                          user_agent: dict | None = None,
                          max_workers: int = 8) -> list[dict]:
    """Check headers of many URLs in parallel. Returns candidates with entity keys.

    urls: list of (title, download_url) tuples.
    Returns list of dicts: {"title", "url", "cols", "entity_keys", "table_name"}.
    """
    def _check_one(title, url):
        cols = check_header(url, user_agent=user_agent)
        if not cols:
            return None
        keys = has_entity_key(cols, key_set)
        if not keys:
            return None
        return {"title": title, "url": url, "cols": cols, "entity_keys": keys}

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_check_one, t, u): (t, u) for t, u in urls}
        for fut in concurrent.futures.as_completed(futures):
            try:
                r = fut.result()
                if r:
                    results.append(r)
            except Exception:
                pass
    return results


# ---------------------------------------------------------------------------
# Connection helper (one per thread)
# ---------------------------------------------------------------------------
def new_conn():
    """Open a fresh Snowflake connection (for use in worker threads)."""
    return snow.connect()
