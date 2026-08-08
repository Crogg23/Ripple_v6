"""Shared bulk-load utilities -- parallel download + fast Snowflake landing.

All agency discovery loaders (SEC, EPA, DOL, IRS) import this to avoid
duplicating the download/load/stamp machinery.  Optimized for throughput:
  - ThreadPoolExecutor for parallel downloads + loads
  - PUT + COPY INTO for files > SMALL_THRESHOLD (bypasses write_pandas overhead)
  - ZipFile over BytesIO (no temp extraction directory)

    from _bulk_load_utils import fast_load, load_zip_csvs, parallel_load, ...
    from _bulk_load_utils import assess_bulk_load, bulk_log_run
"""
from __future__ import annotations

import concurrent.futures
import datetime as dt
import hashlib
import io
import json
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
DEFAULT_MAX_ROWS = 5_000_000
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

    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{tbl}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
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

    # Quality gate (audit 2026-08-05/06 finding: fast_load/_load_bytes had none
    # beyond an empty-frame check -- a row count > 0 with every column blank, the
    # platform's own recurring failure mode, sailed through as a normal load).
    # Runs post-write like every other caller of assess_bulk_load in this file;
    # raising here is deliberate so a caller that doesn't check fast_load's
    # return value still finds out, instead of silently logging a bad load as fine.
    passed, report = assess_bulk_load(conn, tbl)
    if not passed:
        raise RuntimeError(f"QUALITY GATE FAILED for {tbl}: {report}")
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


# ---------------------------------------------------------------------------
# Data Quality Gate
# ---------------------------------------------------------------------------
META_COLS = {"INGESTED_AT", "SOURCE_RUN_ID", "SRC_SHA256", "LOADED_AT",
             "SRC_YEAR", "SRC_QUARTER", "SRC_FILE"}
# 2026-08-07 fix: these used to carry a leading underscore (matching the raw
# DataFrame column names in ingest.py), but sf_col()/_sf_col() strips leading
# underscores before a column ever lands in Snowflake -- the old names never
# matched a real column, so this filter silently excluded nothing. Provenance
# columns have always been included in the density check below (harmless
# since they're never degenerate, but wasted scan cost on every table).

DQ_FAILURES_PATH = _REPO / "outputs" / "_dq_failures.jsonl"


def _data_columns(conn, table: str) -> list[str]:
    """Non-meta columns in a landing table."""
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME=%s ORDER BY ORDINAL_POSITION",
            (table.upper(),))
        cols = [r[0] for r in cur.fetchall()]
    finally:
        cur.close()
    return [c for c in cols if c.upper() not in META_COLS]


def _density_check(conn, table: str, data_cols: list[str],
                   sample: int = 5000, threshold: float = 0.85) -> tuple[float, bool]:
    """Check for degenerate columns (dead-scrape signature).

    Returns (degenerate_frac, passed). Passed means < threshold fraction degenerate.
    """
    if not data_cols:
        return 1.0, False
    # 2026-08-07 fix: exact COUNT(DISTINCT ...) per column scales roughly
    # quadratically with column count (confirmed: 100 cols=3.6s, 300
    # cols=28.1s, 800 cols timed out at 150s) -- a wide table (thousands of
    # columns) can blow past Snowflake's statement timeout and never get a
    # verdict. APPROX_COUNT_DISTINCT (HyperLogLog) is far cheaper per column
    # and plenty accurate for a near-1-distinct threshold check.
    sel = ["COUNT(*) AS _n"] + [
        f'APPROX_COUNT_DISTINCT(NULLIF(TRIM("{c}"),\'\')) AS "d_{i}"'
        for i, c in enumerate(data_cols)]
    sql = (f"SELECT {', '.join(sel)} FROM "
           f'(SELECT * FROM {LANDING_FQS}."{table}" LIMIT {int(sample)})')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        row = cur.fetchone()
    finally:
        cur.close()
    if not row or row[0] == 0:
        return 1.0, False
    distincts = list(row[1:])
    degenerate_count = sum(1 for d in distincts if (d or 0) <= 1)
    frac = degenerate_count / len(data_cols)
    return frac, frac < threshold


def assess_bulk_load(conn, table: str, *,
                     expected_min_rows: int = 1,
                     prev_row_count: int | None = None,
                     density_sample: int = 5000,
                     density_threshold: float = 0.85) -> tuple[bool, dict]:
    """Post-load quality gate. Returns (passed, report).

    Checks:
      1. Row count > expected_min_rows
      2. No >50% row regression vs prev_row_count (if provided)
      3. Density gate -- not a dead-scrape (degenerate columns < threshold)
    """
    report: dict = {}
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT COUNT(*) FROM {LANDING_FQS}."{table}"')
        actual = cur.fetchone()[0]
    finally:
        cur.close()

    report["row_count"] = actual
    report["row_check"] = actual > expected_min_rows

    if prev_row_count and actual < prev_row_count * 0.5:
        report["regression"] = True
        report["regression_detail"] = f"{actual} vs prev {prev_row_count} (>50% drop)"
    else:
        report["regression"] = False

    data_cols = _data_columns(conn, table)
    if actual > 0 and data_cols:
        degen_frac, density_ok = _density_check(
            conn, table, data_cols, sample=density_sample, threshold=density_threshold)
        report["degenerate_frac"] = round(degen_frac, 4)
        report["density_check"] = density_ok
    else:
        report["degenerate_frac"] = None
        report["density_check"] = actual > 0

    passed = (report["row_check"] and not report["regression"] and report["density_check"])
    report["passed"] = passed
    return passed, report


def bulk_log_run(conn, source_id: str, run_id: str, *,
                 sha256: str = "",
                 row_count: int = 0,
                 status: str = "success",
                 message: str = "",
                 source_url: str = "",
                 file_bytes: int | None = None,
                 dq_report: dict | None = None):
    """Write to INGEST_RUNS -- same schema as ingest._log_run()."""
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    msg = message
    if dq_report:
        msg = (message + " | DQ: " + json.dumps(dq_report, default=str))[:16_000]
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO LIBRARY_META.INGEST_LOGS.INGEST_RUNS "
            "(SOURCE_ID, RUN_ID, STARTED_AT, ENDED_AT, STATUS, ROW_COUNT, "
            " FILE_BYTES, SHA256, SOURCE_URL, MESSAGE) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (source_id, run_id, now, now, status, row_count,
             file_bytes, sha256 or None, source_url or None, msg or None))
    finally:
        cur.close()


def _append_dq_failure(source_id: str, table: str, report: dict):
    """Local fallback: append failure to JSONL so it's visible even if SF is dead."""
    entry = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_id": source_id,
        "table": table,
        **report,
    }
    DQ_FAILURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DQ_FAILURES_PATH, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


def run_quality_gate(conn, source_id: str, table: str, run_id: str, *,
                     sha256: str = "",
                     row_count: int | None = None,
                     source_url: str = "",
                     file_bytes: int | None = None,
                     prev_row_count: int | None = None,
                     expected_min_rows: int = 1) -> tuple[bool, dict]:
    """Full quality gate + logging in one call.

    Call this at the end of any bulk loader:
        passed, report = run_quality_gate(conn, SOURCE_ID, TABLE, run_id, sha256=sha)
        if not passed:
            sys.exit(1)

    prev_row_count defaults to the last SUCCESSFUL run's row count from
    INGEST_RUNS, so the >50% regression guard is live for every caller
    without each loader having to thread it through.
    """
    if prev_row_count is None:
        try:
            prev_row_count = ingest._latest_success_rows(conn, source_id)
        except Exception:
            prev_row_count = None
    passed, report = assess_bulk_load(
        conn, table,
        expected_min_rows=expected_min_rows,
        prev_row_count=prev_row_count)

    actual_rows = report.get("row_count", row_count or 0)
    status = "success" if passed else "dq_failed"

    bulk_log_run(conn, source_id, run_id,
                 sha256=sha256, row_count=actual_rows,
                 status=status, source_url=source_url,
                 file_bytes=file_bytes, dq_report=report)

    if not passed:
        _append_dq_failure(source_id, table, report)
        print(f"  [DQ FAILED] {source_id}/{table}: {report}")
    else:
        print(f"  [DQ OK] {source_id}/{table}: {actual_rows:,} rows, "
              f"density {report.get('degenerate_frac', 'n/a')}")

    return passed, report
