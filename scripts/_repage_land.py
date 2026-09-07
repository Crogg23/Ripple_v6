"""Shared lander for the *_FULL repage loaders (2026-09-07).

Three landing tables stopped at a page cap because the onboarding pipeline's
generated fetch_data read one page and quit. Each repage loader walks every
page and lands into a NEW table named <old>_FULL. The old table is never read,
written or dropped.

Landing is chunked: pages are buffered up to CHUNK_ROWS, then appended, so a
200K-row pull with big polygon strings never sits in memory all at once. The
table is created on the first chunk with every data column VARCHAR plus the
audit columns _INGESTED_AT (TIMESTAMP_NTZ), _SOURCE_RUN_ID, _SRC_SHA256.
CREATE TABLE IF NOT EXISTS then append; a table that already holds rows stops
the loader unless --append is passed, because a second full pull would double
every row.
"""
from __future__ import annotations

import hashlib
import sys
import uuid
from pathlib import Path
from typing import Callable, Iterable

import pandas as pd

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

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
CHUNK_ROWS = 25_000


def existing_rows(conn, table: str) -> int | None:
    try:
        return conn.cursor().execute(
            f'select count(*) from {bulk.LANDING_FQS}."{table}"').fetchone()[0]
    except Exception:
        return None  # table does not exist


def _create_if_missing(conn, table: str, columns: list[str]) -> None:
    cols = list(columns) + [bulk.META_INGESTED_AT, bulk.META_SOURCE_RUN_ID, bulk.META_SRC_SHA256]
    defs = ", ".join(
        f'"{c}" TIMESTAMP_NTZ' if c == bulk.META_INGESTED_AT else f'"{c}" VARCHAR'
        for c in cols)
    cur = conn.cursor()
    try:
        cur.execute(f'CREATE TABLE IF NOT EXISTS {bulk.LANDING_FQS}."{table}" ({defs})')
    finally:
        cur.close()


def _append(conn, table: str, df: pd.DataFrame, run_id: str, sha: str) -> int:
    from snowflake.connector.pandas_tools import write_pandas
    df = df.astype(str).replace({"None": None, "nan": None, "NaT": None, "<NA>": None})
    df[bulk.META_INGESTED_AT] = pd.Timestamp.utcnow().tz_localize(None)
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha
    ok, _c, nrows, _ = write_pandas(conn, df, table, database=bulk.LANDING_DB,
                                    schema=bulk.LANDING_SCHEMA,
                                    quote_identifiers=False, auto_create_table=False)
    if not ok:
        raise RuntimeError("write_pandas reported failure")
    return nrows


def land_pages(*, source_id: str, table: str, source_url: str, columns: list[str],
               pages: Callable[[], Iterable[pd.DataFrame]], run: bool, append: bool,
               expected_total: int | None = None, resume_run_id: str | None = None,
               key_col: str | None = None) -> int:
    """Walk pages(); dry run counts rows and lands nothing; --run lands in chunks.

    columns is the fixed column order every page is reindexed to, so a page
    missing a field still lands with the same shape.
    resume_run_id continues an interrupted run under ITS run id: rows whose
    key_col value already sits in the table under that run id are skipped, so
    the finished run holds each key once and "newest run id" still means the
    complete set. Returns rows landed (or rows counted on a dry run).
    """
    conn = None
    run_id = resume_run_id or str(uuid.uuid4())
    hasher = hashlib.sha256()
    seen: set = set()
    if run:
        conn = snow.connect()
        have = existing_rows(conn, table)
        if resume_run_id:
            if not key_col:
                raise ValueError("resume needs key_col")
            cur = conn.cursor()
            try:
                cur.execute(f'select "{key_col}" from {bulk.LANDING_FQS}."{table}" '
                            f'where "{bulk.META_SOURCE_RUN_ID}" = %s', (resume_run_id,))
                seen = {r[0] for r in cur.fetchall()}
            finally:
                cur.close()
            print(f"resuming run {resume_run_id}: {len(seen):,} keys already landed, will skip them")
        elif have:
            print(f"{table} already holds {have:,} rows.")
            if not append:
                print("Stopping: a second full pull would double every row. "
                      "Pass --append if that is what you want.")
                conn.close()
                sys.exit(2)
        _create_if_missing(conn, table, columns)
        print(f"run id {run_id}")

    total = 0
    buf: list[pd.DataFrame] = []
    buffered = 0

    def flush():
        nonlocal buf, buffered, total
        if not buf:
            return
        df = pd.concat(buf, ignore_index=True).reindex(columns=columns)
        if run:
            n = _append(conn, table, df, run_id, "streamed")
        else:
            n = len(df)
        total += n
        print(f"  {'landed' if run else 'counted'} {total:,} rows so far"
              + (f" of {expected_total:,}" if expected_total else ""))
        buf, buffered = [], 0

    skipped = 0
    for page in pages():
        if page is None or page.empty:
            continue
        if seen:
            before = len(page)
            page = page[~page[key_col].isin(seen)]
            skipped += before - len(page)
            if page.empty:
                continue
        hasher.update(page.to_csv(index=False).encode("utf-8", "replace"))
        buf.append(page)
        buffered += len(page)
        if buffered >= CHUNK_ROWS:
            flush()
    flush()
    sha = hasher.hexdigest()
    if seen:
        print(f"skipped {skipped:,} rows already landed under {run_id}")

    if not run:
        print(f"\n(dry run) {total:,} rows fetched, sha256 {sha[:12]}, nothing landed. "
              f"Add --run to land into {bulk.LANDING_FQS}.{table}")
        return total

    cur = conn.cursor()
    try:
        cur.execute(f'update {bulk.LANDING_FQS}."{table}" set "{bulk.META_SRC_SHA256}" = %s '
                    f'where "{bulk.META_SOURCE_RUN_ID}" = %s', (sha, run_id))
    finally:
        cur.close()
    print(f"landed {total:,} rows into {bulk.LANDING_FQS}.{table}  run {run_id}  sha256 {sha[:12]}")
    passed, report = bulk.run_quality_gate(conn, source_id, table, run_id, sha256=sha,
                                           row_count=total, source_url=source_url)
    conn.close()
    if not passed:
        print(f"QUALITY GATE FAILED: {report}")
        sys.exit(1)
    print("DONE")
    return total
