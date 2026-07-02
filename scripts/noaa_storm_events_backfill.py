#!/usr/bin/env python3
"""DEPRECATED (2026-07-02) — one-off, NON-ATOMIC backfill. Kept for provenance only.
Appends directly to the live table (a mid-run crash leaves a partial year). For any
new or repeat bulk load use scripts/bridge_fuel_load.py, which lands through a
staging table + atomic swap, density-gates, and guards the registry.
Provenance fix 2026-07-02: the meta column is now _INGESTED_AT stamped TIMESTAMP_NTZ
(was underscore-less INGESTED_AT epoch-micros NUMBER) — if the live table still
carries the old column, migrate it before re-running (the strict column selection
below will otherwise fail loudly, never mis-stamp).

Year-by-year backfill for NOAA NCEI Storm Events (discovery sweep #77:
FED_NOAA_STORM_EVENTS was a single-year SNAPSHOT -- 2025 only, 72,360 rows --
so every "storms over time" question saw one year). This appends the modern,
event-type-consistent era (1996-2024) and turns the snapshot into a ~29-year
time series.

Why 1996-2024: NCEI's own docs note that pre-1996 the database carries only
3 event types (Tornado, Thunderstorm Wind, Hail); 1996-onward uses the full
~50 event-type taxonomy. 2025 is already loaded (the snapshot); we skip it.

Source: NCEI Storm Events bulk CSVs
  https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/
The "details" file per year is:
  StormEvents_details-ftp_v1.0_d<YYYY>_c<CCCCCCCC>.csv.gz
The c-suffix (creation date) VARIES per year, so we fetch the directory listing
and parse the real filename for each year -- never guess the suffix.

Each year is a small .csv.gz (a few MB; ~50k-80k rows). This STREAMS each gz to
the scratchpad, reads it in chunks, and APPENDS (overwrite=False) to
LIBRARY_RAW.LANDING.FED_NOAA_STORM_EVENTS matching its existing schema:
  - 51 data cols = the CSV header verbatim (BEGIN_YEARMONTH ... DATA_SOURCE)
  - 3 meta cols  = _INGESTED_AT (TIMESTAMP_NTZ), SOURCE_RUN_ID, SRC_SHA256
    (HISTORY: the original template loader wrote 2025 with an underscore-less
    INGESTED_AT as NUMBER epoch-us; fixed to the shared contract 2026-07-02 —
    see the DEPRECATED header for the migration caveat.)

Idempotent: a YEAR already present in the table is skipped, so re-running never
duplicates. Per-year SHA-256 is computed from the raw gz bytes for provenance.

    python3 scripts/noaa_storm_events_backfill.py                 # preview (sizes, what's to load)
    python3 scripts/noaa_storm_events_backfill.py --run           # land 1996-2024
    python3 scripts/noaa_storm_events_backfill.py --start 2010 --end 2014 --run

BUDGET: tiny. 29 years total is on the order of ~1.5M rows / ~250 MB gzipped
across the whole window -- a cheap append on RIPPLE_WH (X-Small). No bounding
needed beyond the 1996-2024 era cap.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import uuid
from pathlib import Path

import pandas as pd

# NOTE: we fetch NCEI over `curl` (subprocess), not `requests`. In this runtime the
# urllib3-v2-on-LibreSSL stack hangs indefinitely on the ncei.noaa.gov TLS handshake,
# while the system `curl` returns the same files in ~1s. Snowflake's own connector is
# unaffected. So all NCEI I/O goes through _curl_* below.

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import snow          # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

TABLE = "FED_NOAA_STORM_EVENTS"
SID = "fed_noaa_storm_events"
BASE = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
CHUNK = 250_000
SCRATCH = Path("c:/Code/Ripple_v6/.scratch/"
               "e8eac5fb-de36-4362-9440-da24a904b9b4/scratchpad")

ERA_START, ERA_END = 1996, 2024  # modern, full event-type taxonomy; 2025 = snapshot already loaded

# The 51 data columns, in table order, are the CSV header verbatim. We pull them
# straight from each file's header (defensive: NCEI has been stable here for years).
META_INGESTED_AT = "_INGESTED_AT"     # TIMESTAMP_NTZ — the shared provenance contract
META_SOURCE_RUN_ID = "SOURCE_RUN_ID"
META_SRC_SHA256 = "SRC_SHA256"

_DETAIL_RE = re.compile(r'StormEvents_details-ftp_v1\.0_d(\d{4})_c(\d{8})\.csv\.gz')


def _curl_text(url: str, timeout: int = 120) -> str:
    """GET a URL as text via system curl (requests hangs on NCEI TLS here)."""
    r = subprocess.run(
        ["curl", "-sS", "--fail", "--max-time", str(timeout),
         "-A", UA["User-Agent"], url],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl listing failed rc={r.returncode}: {r.stderr.strip()[:160]}")
    return r.stdout


def _curl_download(url: str, dest: Path, timeout: int = 300) -> None:
    """Stream a URL to disk via system curl (never holds the file in memory)."""
    r = subprocess.run(
        ["curl", "-sS", "--fail", "--max-time", str(timeout),
         "-A", UA["User-Agent"], "-o", str(dest), url],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl download failed rc={r.returncode}: {r.stderr.strip()[:160]}")


def _listing() -> dict[int, str]:
    """Fetch the directory and return {year: filename} for every details file."""
    text = _curl_text(BASE, timeout=120)
    out: dict[int, str] = {}
    for m in _DETAIL_RE.finditer(text):
        yr = int(m.group(1))
        out[yr] = m.group(0)  # if dupes appear, last wins; NCEI lists one per year
    return out


def _table_cols(conn) -> list[str]:
    cur = conn.cursor()
    try:
        cur.execute(f"DESCRIBE TABLE {settings.raw_database}.{settings.raw_schema}.{TABLE}")
        return [row[0] for row in cur.fetchall()]
    finally:
        cur.close()


def _years_loaded(conn) -> set[str]:
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT DISTINCT YEAR FROM {settings.raw_database}.{settings.raw_schema}.{TABLE}")
        return {str(r[0]).strip() for r in cur.fetchall() if r[0] is not None}
    finally:
        cur.close()


def _load_year(conn, year: int, fn: str, table_cols: list[str], run_id: str) -> tuple[bool, str]:
    url = BASE + fn
    tmp = SCRATCH / fn
    try:
        # stream gz to disk via curl (never hold the file in memory)
        _curl_download(url, tmp, timeout=300)
        sha = hashlib.sha256(tmp.read_bytes()).hexdigest()
        size = tmp.stat().st_size
        started = ingest._utcnow()
        # TIMESTAMP_NTZ like every other loader (was epoch-micros NUMBER — the
        # provenance type drift the 2026-07-02 audit flagged).
        ingested_at = started.replace(tzinfo=None)
        data_cols = [c for c in table_cols
                     if c not in {META_INGESTED_AT, META_SOURCE_RUN_ID, META_SRC_SHA256}]
        appended = 0
        # pandas reads .csv.gz transparently; chunk it so memory stays flat
        for chunk in pd.read_csv(tmp, dtype=str, keep_default_na=False, na_values=[],
                                 low_memory=False, compression="gzip", chunksize=CHUNK):
            chunk.columns = [c.strip().upper() for c in chunk.columns]
            for c in data_cols:
                if c not in chunk.columns:
                    chunk[c] = ""  # defensive against header drift
            out = chunk[data_cols].copy()
            out[META_INGESTED_AT] = ingested_at
            out[META_SOURCE_RUN_ID] = run_id
            out[META_SRC_SHA256] = sha
            out = out[table_cols]  # exact table order
            ok, _n_chunks, n, _ = write_pandas(
                conn, out, table_name=TABLE,
                database=settings.raw_database, schema=settings.raw_schema,
                auto_create_table=False, overwrite=False, quote_identifiers=False)
            if not ok:
                return False, f"write_pandas failed after {appended:,} rows"
            appended += len(out)
        ended = ingest._utcnow()
        ingest._log_run(conn, SID, run_id, "success", appended, size, sha, url,
                        started, ended,
                        f"Storm Events backfill {year}: appended {appended:,} rows from {fn}")
        return True, f"appended {appended:,} rows ({size/1e6:.1f} MB gz)"
    except Exception as ex:  # noqa: BLE001
        return False, f"{type(ex).__name__}: {str(ex)[:160]}"
    finally:
        try:
            tmp.unlink()
        except Exception:
            pass


def main() -> int:
    ap = argparse.ArgumentParser(description="NOAA Storm Events year-by-year backfill (append).")
    ap.add_argument("--start", type=int, default=ERA_START, help=f"first year (default {ERA_START})")
    ap.add_argument("--end", type=int, default=ERA_END, help=f"last year (default {ERA_END})")
    ap.add_argument("--run", action="store_true", help="actually download + append (else preview)")
    args = ap.parse_args()

    want = [y for y in range(args.start, args.end + 1)]
    listing = _listing()
    print(f"Directory listing: {len(listing)} details files found "
          f"({min(listing)}-{max(listing)}).")
    missing = [y for y in want if y not in listing]
    if missing:
        print(f"  WARNING: requested years with no file in listing: {missing}")
    want = [y for y in want if y in listing]

    conn = snow.connect()
    try:
        loaded = _years_loaded(conn)
        table_cols = _table_cols(conn)
        print(f"Table currently holds year(s): {sorted(loaded) if loaded else '(none)'}")
        todo = [y for y in want if str(y) not in loaded]
        skip = [y for y in want if str(y) in loaded]
        for y in skip:
            print(f"  - {y}  already in table (YEAR present) -- skip")
        if not args.run:
            for y in todo:
                print(f"  + {y}  {BASE}{listing[y]}")
            print(f"\nPREVIEW only. {len(todo)} year(s) to append; each is a few MB gz / "
                  f"~50k-80k rows. Add --run to load.")
            return 0
        run_id = uuid.uuid4().hex[:16]
        ok = fail = 0
        for y in todo:
            good, msg = _load_year(conn, y, listing[y], table_cols, run_id)
            print(f"  {'OK ' if good else 'ERR'} {y}  {msg}", flush=True)
            ok += good
            fail += (not good)
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT YEAR), MIN(YEAR), MAX(YEAR) "
                    f"FROM {settings.raw_database}.{settings.raw_schema}.{TABLE}")
        n, yrs, mn, mx = cur.fetchone()
        cur.close()
        print(f"\nDONE: {ok} year(s) loaded, {fail} failed. "
              f"FED_NOAA_STORM_EVENTS now {n:,} rows spanning {yrs} year(s) ({mn}-{mx}).")
        return 0 if fail == 0 else 1
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
