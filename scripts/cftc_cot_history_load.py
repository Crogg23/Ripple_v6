"""Backfill CFTC Commitments of Traders history into the landing tables.

Defect class 4 (SHORT), warehouse verification 2026-08-11:
  - LIBRARY_RAW.LANDING.FED_CFTC_COT_FUTURES held only 2024 (16,764 rows);
    publisher full futures-only history is ~287k rows back to 1986.
  - LIBRARY_RAW.LANDING.FED_CFTC_COT_FINANCIAL held only 2024 (3,163 rows);
    the Traders-in-Financial-Futures series starts mid-2006.

This loader APPENDS the missing years to the existing tables (constitution:
no DROP/TRUNCATE/OVERWRITE of existing warehouse tables; the 2024 rows there
are valid and are deliberately NOT re-loaded).

Sources (yearly zips, one text file per zip):
  futures:   https://www.cftc.gov/files/dea/history/deacotYYYY.zip   1986-2025
  financial: https://www.cftc.gov/files/dea/history/fut_fin_txt_YYYY.zip  2010-2025
  financial 2006-2009: only published inside fin_fut_txt_2006_2016.zip --
    that bundle overlaps the yearly files, so it is sliced to report dates
    before 2010-01-01 (a deliberate year slice, not a truncation).

Safety:
  - Columns of every downloaded year are compared to the existing table's
    data columns after sf_col() normalization. A mismatched year is NEVER
    forced in -- it is appended to <TABLE>_HIST instead (auto-created), and
    reported. (Probe 2026-08-11: 1986/1995/2010/2025 futures and 2025 TFF all
    match the live layouts, so _HIST is expected to stay empty.)
  - Checkpoint file logs/cftc_cot_history_checkpoint.json records every
    completed (table, year) so a rerun skips finished work. Restart-safe.
  - 2024 is excluded for both tables (already loaded). A post-load dedupe
    check counts exact-duplicate rows via HASH(*).

    python scripts/cftc_cot_history_load.py            # preview plan
    python scripts/cftc_cot_history_load.py --run      # load
    python scripts/cftc_cot_history_load.py --verify   # counts + dupe check only
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
sys.path.insert(0, str(_REPO))
from loadkit.archive import pick_member  # noqa: E402
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
BASE = "https://www.cftc.gov/files/dea/history"
CHECKPOINT = _REPO / "logs" / "cftc_cot_history_checkpoint.json"
SANITY_MAX_ROWS = 2_000_000  # a single yearly file is ~10k rows; refuse insanity

FUT_TABLE = "FED_CFTC_COT_FUTURES"
FIN_TABLE = "FED_CFTC_COT_FINANCIAL"

# 2024 already loaded in both tables -- never re-load it.
# 2027: bump the upper bound when the next year file appears.
FUT_YEARS = [y for y in range(1986, 2027) if y != 2024]
FIN_YEARS = [y for y in range(2010, 2027) if y != 2024]
FIN_BUNDLE_URL = f"{BASE}/fin_fut_txt_2006_2016.zip"  # sliced to <2010 only
FIN_DATE_COL = "REPORT_DATE_AS_YYYY_MM_DD"


def _load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())
    return {"done": []}


def _save_checkpoint(ck: dict) -> None:
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(json.dumps(ck, indent=2))


def _table_data_cols(conn, table: str) -> list[str]:
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME=%s ORDER BY ORDINAL_POSITION",
            (table,))
        cols = [r[0] for r in cur.fetchall()]
    finally:
        cur.close()
    meta = {bulk.sf_col(bulk.META_INGESTED_AT), bulk.sf_col(bulk.META_SOURCE_RUN_ID),
            bulk.sf_col(bulk.META_SRC_SHA256)}
    return [c for c in cols if c not in meta]


def _fetch_zip_df(url: str) -> tuple[pd.DataFrame, str]:
    """Download a CFTC yearly zip, parse its single text member, return (df, sha)."""
    resp = requests.get(url, timeout=300, headers=USER_AGENT)
    resp.raise_for_status()
    sha = hashlib.sha256(resp.content).hexdigest()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        # CFTC yearly zips carry ONE text member; ambiguity raises rather
        # than guessing by size (the EIA-860 largest-member trap).
        member = pick_member(zf, suffixes=(".txt", ".csv"))
        with zf.open(member) as f:
            content = f.read()
    df = pd.read_csv(io.BytesIO(content), dtype=str, low_memory=False,
                     encoding_errors="replace")
    if len(df) > SANITY_MAX_ROWS:
        raise RuntimeError(f"{url}: {len(df):,} rows exceeds sanity cap "
                           f"{SANITY_MAX_ROWS:,} -- refusing to load blindly.")
    return df, sha


def _append(conn, df: pd.DataFrame, table: str, *, sha: str,
            expected_cols: list[str] | None, auto_create: bool) -> int:
    """Stamp provenance and APPEND (never overwrite) to a landing table."""
    from snowflake.connector.pandas_tools import write_pandas
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    df = df.copy()
    df.columns = [bulk.sf_col(c) for c in df.columns]
    if expected_cols is not None and sorted(df.columns) != sorted(expected_cols):
        raise ValueError("column mismatch")
    df[bulk.sf_col(bulk.META_INGESTED_AT)] = started
    df[bulk.sf_col(bulk.META_SOURCE_RUN_ID)] = run_id
    df[bulk.sf_col(bulk.META_SRC_SHA256)] = sha
    ok, _c, _n, _ = write_pandas(
        conn, df, table_name=table,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=auto_create, overwrite=False, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas failed for {table}")
    return len(df)


def _load_year(conn, table: str, url: str, expected_cols: list[str],
               *, slice_before: str | None = None,
               date_col: str | None = None) -> tuple[int, str]:
    """Load one yearly zip. Returns (rows, landed_table).

    If the year's column set doesn't match the live table, land in
    <table>_HIST instead of forcing a merge.
    """
    df, sha = _fetch_zip_df(url)
    # Refuse to append a source file that is already in the table (restart /
    # rerun safety beyond the checkpoint -- exact-file dedupe by SHA256).
    sha_col = bulk.sf_col(bulk.META_SRC_SHA256)
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT COUNT(*) FROM {bulk.LANDING_FQS}."{table}" '
                    f'WHERE "{sha_col}" = %s', (sha,))
        if cur.fetchone()[0] > 0:
            raise RuntimeError(
                f"{table}: file sha {sha[:12]} already loaded -- refusing duplicate append")
    finally:
        cur.close()
    if slice_before:
        norm = {bulk.sf_col(c): c for c in df.columns}
        raw_date = norm[date_col]
        before = len(df)
        # BUG FIX 2026-08-11: v1 compared date strings lexicographically, but
        # the 2006-2016 bundle carries dates as 'M/D/YYYY 12:00:00 AM' -- the
        # string compare kept months 1,2,10-12 of ALL years (7,790 junk rows
        # appended; see report). Parse to real datetimes before slicing.
        parsed = pd.to_datetime(df[raw_date], errors="coerce", format="mixed")
        if parsed.isna().any():
            raise RuntimeError(
                f"{url}: {int(parsed.isna().sum())} unparseable {date_col} values -- "
                f"refusing to slice blindly")
        df = df[parsed < pd.Timestamp(slice_before)]
        print(f"      sliced bundle {before:,} -> {len(df):,} rows "
              f"({date_col} < {slice_before})")
    if df.empty:
        return 0, table
    got = sorted(bulk.sf_col(c) for c in df.columns)
    if got == sorted(expected_cols):
        n = _append(conn, df, table, sha=sha, expected_cols=expected_cols,
                    auto_create=False)
        return n, table
    hist = f"{table}_HIST"
    print(f"      COLUMN MISMATCH vs {table} -- landing in {hist}")
    print(f"      missing from file: {sorted(set(expected_cols) - set(got))[:8]}")
    print(f"      extra in file:     {sorted(set(got) - set(expected_cols))[:8]}")
    n = _append(conn, df, hist, sha=sha, expected_cols=None, auto_create=True)
    return n, hist


def _dupe_check(conn, table: str) -> tuple[int, int]:
    cur = conn.cursor()
    try:
        cur.execute(
            f"SELECT COUNT(*), COUNT(*) - COUNT(DISTINCT HASH(*)) "
            f"FROM (SELECT * EXCLUDE (INGESTED_AT, SOURCE_RUN_ID, SRC_SHA256) "
            f"FROM {bulk.LANDING_FQS}.\"{table}\")")
        total, dupes = cur.fetchone()
    finally:
        cur.close()
    return total, dupes


def verify(conn) -> None:
    for t in (FUT_TABLE, FIN_TABLE):
        total, dupes = _dupe_check(conn, t)
        print(f"  {t}: {total:,} rows, {dupes:,} exact-duplicate rows (ex-provenance)")


def main() -> int:
    ap = argparse.ArgumentParser(description="CFTC COT history backfill")
    ap.add_argument("--run", action="store_true", help="Actually load (default: preview)")
    ap.add_argument("--verify", action="store_true", help="Counts + dupe check only")
    args = ap.parse_args()

    plan: list[dict] = []
    for y in FUT_YEARS:
        plan.append({"table": FUT_TABLE, "year": str(y),
                     "url": f"{BASE}/deacot{y}.zip"})
    plan.append({"table": FIN_TABLE, "year": "2006_2009_bundle",
                 "url": FIN_BUNDLE_URL, "slice_before": "2010-01-01",
                 "date_col": FIN_DATE_COL})
    for y in FIN_YEARS:
        plan.append({"table": FIN_TABLE, "year": str(y),
                     "url": f"{BASE}/fut_fin_txt_{y}.zip"})

    if args.verify:
        conn = snow.connect()
        verify(conn)
        conn.close()
        return 0

    ck = _load_checkpoint()
    done = set(tuple(x) for x in ck["done"])
    todo = [p for p in plan if (p["table"], p["year"]) not in done]

    print(f"{len(plan)} units total, {len(done)} already done, {len(todo)} to load")
    if not args.run:
        for p in todo:
            print(f"  {p['table']:26s} {p['year']:16s} {p['url']}")
        print("\n(preview only -- add --run to execute)")
        return 0

    conn = snow.connect()
    expected = {t: _table_data_cols(conn, t) for t in (FUT_TABLE, FIN_TABLE)}
    run_id = str(uuid.uuid4())
    loaded_by_table: dict[str, int] = {}
    failures: list[str] = []

    for i, p in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {p['table']} {p['year']}")
        try:
            n, landed = _load_year(
                conn, p["table"], p["url"], expected[p["table"]],
                slice_before=p.get("slice_before"), date_col=p.get("date_col"))
            print(f"      -> {n:,} rows into {landed}")
            done.add((p["table"], p["year"]))
            ck["done"] = sorted(list(d) for d in done)
            _save_checkpoint(ck)
        except Exception as e:
            msg = f"{p['table']} {p['year']}: {str(e)[:160]}"
            print(f"      FAILED: {msg}")
            failures.append(msg)

    # Post-load: quality gate + dedupe check per touched table.
    for t in (FUT_TABLE, FIN_TABLE):
        try:
            src = "fed_cftc_cot_futures" if t == FUT_TABLE else "fed_cftc_cot_financial"
            bulk.run_quality_gate(conn, src, t, run_id,
                                  source_url=f"{BASE}/ (yearly zips backfill)")
        except Exception as e:
            failures.append(f"quality gate {t}: {str(e)[:160]}")
    verify(conn)
    conn.close()

    if failures:
        print(f"\nFAILED units ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nAll units loaded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
