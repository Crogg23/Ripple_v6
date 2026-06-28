#!/usr/bin/env python3
"""Full-history backfill for USGS earthquakes (discovery sweep Phase 3 #46:
FED_USGS_EARTHQUAKES is a 30-day rolling snapshot -- the whole table only ever
sees the last month, so any "earthquakes over time" question is impossible). This
turns the snapshot into a real ~16.5-year time series.

Source: USGS FDSNWS event service (CSV)
  https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=..&endtime=..&minmagnitude=2.5
The API caps ~20,000 events per query, so we PAGINATE BY MONTH. Even the densest
swarm months (Tohoku 2011-03, Ridgecrest 2019-07) top out ~4,400 events at mag>=2.5,
a >4x margin under the cap -- no window ever truncates.

BOUNDED WINDOW: 2010-01-01 .. 2026-06-14, minmagnitude 2.5  (~443k events total,
trivially small -- a few MB, ~0 credits). This is SNAPSHOT-REPLACE: the first
written chunk uses overwrite=True (drops the 30-day snapshot), every chunk after
appends. Re-running fully rebuilds the table, so it's idempotent.

The CSV header matches the landing table's 22 data columns exactly (uppercased):
  time, latitude, longitude, depth, mag, magType, nst, gap, dmin, rms, net, id,
  updated, place, type, horizontalError, depthError, magError, magNst, status,
  locationSource, magSource

    python3 scripts/usgs_quake_backfill.py            # preview (counts per month, no load)
    python3 scripts/usgs_quake_backfill.py --run      # snapshot-replace the full history
    python3 scripts/usgs_quake_backfill.py --run --start 2015-01-01 --end 2016-01-01
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import io
import sys
import time
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import register      # noqa: E402
import snow          # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

TABLE = "FED_USGS_EARTHQUAKES"
SID = "fed_usgs_earthquakes"
BASE = "https://earthquake.usgs.gov/fdsnws/event/1"
MIN_MAG = "2.5"
UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
SCRATCH = Path("/private/tmp/claude-501/-Users-chrisr--Documents-GitHub-Ripple-v6/"
               "e8eac5fb-de36-4362-9440-da24a904b9b4/scratchpad")
CAP = 20_000  # FDSNWS hard cap per query; we monitor to never silently truncate

# CSV header (lowercase camelCase) -> landing column (UPPER). Order = table order.
COLMAP = {
    "time": "TIME", "latitude": "LATITUDE", "longitude": "LONGITUDE", "depth": "DEPTH",
    "mag": "MAG", "magType": "MAGTYPE", "nst": "NST", "gap": "GAP", "dmin": "DMIN",
    "rms": "RMS", "net": "NET", "id": "ID", "updated": "UPDATED", "place": "PLACE",
    "type": "TYPE", "horizontalError": "HORIZONTALERROR", "depthError": "DEPTHERROR",
    "magError": "MAGERROR", "magNst": "MAGNST", "status": "STATUS",
    "locationSource": "LOCATIONSOURCE", "magSource": "MAGSOURCE",
}
DATA_COLS = list(COLMAP.values())
TABLE_COLS = DATA_COLS + [ingest.META_INGESTED_AT, ingest.META_SOURCE_RUN_ID,
                          ingest.META_SRC_SHA256]


def _months(start: _dt.date, end: _dt.date) -> list[tuple[_dt.date, _dt.date]]:
    """Half-open [month_start, next_month_start) windows covering [start, end)."""
    out = []
    cur = _dt.date(start.year, start.month, 1)
    if cur < start:
        cur = start
    while cur < end:
        if cur.month == 12:
            nxt = _dt.date(cur.year + 1, 1, 1)
        else:
            nxt = _dt.date(cur.year, cur.month + 1, 1)
        win_end = min(nxt, end)
        out.append((cur, win_end))
        cur = nxt
    return out


def _count(a: _dt.date, b: _dt.date) -> int:
    url = (f"{BASE}/count?format=text&starttime={a.isoformat()}"
           f"&endtime={b.isoformat()}&minmagnitude={MIN_MAG}")
    for attempt in range(4):
        try:
            r = requests.get(url, headers=UA, timeout=120)
            if r.status_code == 200 and r.text.strip().isdigit():
                return int(r.text.strip())
        except Exception:
            pass
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"count failed for {a}..{b}")


def _fetch_csv(a: _dt.date, b: _dt.date) -> str:
    url = (f"{BASE}/query?format=csv&starttime={a.isoformat()}"
           f"&endtime={b.isoformat()}&minmagnitude={MIN_MAG}&orderby=time-asc")
    for attempt in range(5):
        try:
            r = requests.get(url, headers=UA, timeout=300)
            if r.status_code == 200:
                return r.text
            # 429/503: back off
        except Exception:
            pass
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"query failed for {a}..{b}")


def main() -> int:
    ap = argparse.ArgumentParser(description="USGS earthquake full-history backfill (snapshot-replace).")
    ap.add_argument("--start", default="2010-01-01", help="window start YYYY-MM-DD (inclusive)")
    ap.add_argument("--end", default="2026-06-14", help="window end YYYY-MM-DD (exclusive)")
    ap.add_argument("--min-mag", default=MIN_MAG, help="minimum magnitude (default 2.5)")
    ap.add_argument("--run", action="store_true", help="actually load (else preview counts)")
    args = ap.parse_args()

    globals()["MIN_MAG"] = args.min_mag
    start = _dt.date.fromisoformat(args.start)
    end = _dt.date.fromisoformat(args.end)
    windows = _months(start, end)

    # ---- preview: total + spot-check that no month nears the cap ----
    total = _count(start, end)
    print(f"USGS backfill window {start} .. {end}  minmag={MIN_MAG}")
    print(f"  total events in window: {total:,}  ({len(windows)} monthly sub-queries)")
    if not args.run:
        print("\n  PREVIEW only. Sampling a few months for cap safety...")
        sample = windows[::max(1, len(windows) // 8)][:8]
        worst = 0
        for a, b in sample:
            n = _count(a, b)
            worst = max(worst, n)
            flag = "  <-- NEAR CAP" if n > CAP * 0.8 else ""
            print(f"    {a:%Y-%m}: {n:>6,}{flag}")
        print(f"\n  worst sampled month: {worst:,} (cap {CAP:,}). Per-month pagination is safe.")
        print(f"  Add --run to snapshot-replace {TABLE} with the full history.")
        return 0

    run_id = uuid.uuid4().hex[:16]
    started = ingest._utcnow()
    conn = snow.connect()
    total_rows = 0
    sha = hashlib.sha256()
    # IMPORTANT: write _INGESTED_AT as an explicit ISO STRING, not a datetime.
    # write_pandas serializes any datetime/datetime64 column to int64 nanoseconds in the
    # parquet, and the COPY into a TIMESTAMP_NTZ column then reads those as epoch-SECONDS
    # -> garbage years (e.g. 56492535). A string column is COPY-cast correctly. (The NOAA
    # AIS template has this latent bug -- its _INGESTED_AT is corrupted too; we fix it here.)
    ingested_at = started.replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S.%f")
    try:
        # snapshot-replace: clear the 30-day snapshot up front, then append every
        # month with overwrite=False (the template's type-safe path -- overwrite=True
        # in write_pandas mis-infers the TIMESTAMP_NTZ meta col as epoch NUMBER).
        cur = conn.cursor()
        cur.execute(f"TRUNCATE TABLE LIBRARY_RAW.LANDING.{TABLE}")
        cur.close()
        print(f"  truncated {TABLE} (snapshot cleared); appending full history...")
        for i, (a, b) in enumerate(windows):
            text = _fetch_csv(a, b)
            sha.update(text.encode("utf-8", "replace"))
            df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False,
                             low_memory=False)
            n = len(df)
            if n >= CAP:
                # safety: a month somehow hit the cap -- bail loudly rather than truncate
                conn.close()
                raise SystemExit(f"ABORT: {a:%Y-%m} returned {n} >= cap {CAP}; "
                                 f"split this month finer before reloading.")
            if n == 0:
                print(f"  {a:%Y-%m}: 0 events", flush=True)
                continue
            df = df.rename(columns=COLMAP)
            for c in DATA_COLS:
                if c not in df.columns:
                    df[c] = ""
            out = df[DATA_COLS].copy()
            out[ingest.META_INGESTED_AT] = ingested_at
            out[ingest.META_SOURCE_RUN_ID] = run_id
            out[ingest.META_SRC_SHA256] = sha.hexdigest()
            out = out[TABLE_COLS]
            ok, _c, wrote, _ = write_pandas(
                conn, out, table_name=TABLE,
                database=settings.raw_database, schema=settings.raw_schema,
                auto_create_table=False, overwrite=False,
                quote_identifiers=False)
            if not ok:
                conn.close()
                raise SystemExit(f"write_pandas failed at {a:%Y-%m} after {total_rows:,} rows")
            total_rows += wrote
            print(f"  {a:%Y-%m}: {wrote:>6,} rows  (running {total_rows:,})", flush=True)

        ended = ingest._utcnow()
        final_sha = sha.hexdigest()
        ingest._log_run(conn, SID, run_id, "success", total_rows, len(final_sha), final_sha,
                        f"{BASE}/query?format=csv&minmagnitude={MIN_MAG}",
                        started, ended,
                        f"USGS full-history backfill {start}..{end}: snapshot-replaced "
                        f"with {total_rows:,} rows across {len(windows)} monthly windows")

        # re-register (snapshot -> time series; loaders may register autonomously)
        try:
            cfg = {
                "source_id": SID,
                "name": "USGS Earthquake Catalog (M2.5+ full history)",
                "url": f"{BASE}/query",
                "publisher": "U.S. Geological Survey",
                "jurisdiction": "fed",
                "category": "natural_hazards",
                "subcategory": "seismology",
                "unit_of_observation": "one seismic event",
                "access_method": "rest_api",
                "format": "csv",
                "auth_required": False,
                "cost": "free",
                "update_cadence": "real-time (backfilled 2010-present)",
                "join_keys": ["lat/lon"],
                "notes": (f"FDSNWS event service. Backfilled 2010-01-01..2026-06-14 at "
                          f"minmagnitude {MIN_MAG} via per-month pagination (20k/query cap). "
                          f"Was a 30-day rolling snapshot before 2026-06-28."),
            }
            row = register._build_row(cfg, register._enrich(cfg))
            merge_sql, params = register._merge_sql(row)
            cur = conn.cursor()
            cur.execute(merge_sql, params)
            cur.close()
            print("  registry: re-registered (snapshot -> full history)")
        except Exception as ex:  # noqa: BLE001
            print(f"  registry: skipped ({type(ex).__name__}: {str(ex)[:120]})")

        # confirm the unlock
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT LEFT(TIME,4)), MIN(TIME), MAX(TIME) "
                    f"FROM LIBRARY_RAW.LANDING.{TABLE}")
        cnt, yrs, mn, mx = cur.fetchone()
        cur.close()
        print(f"\nDONE: snapshot-replaced. {TABLE} now holds {cnt:,} rows spanning "
              f"{yrs} distinct year(s), {str(mn)[:10]} .. {str(mx)[:10]}.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
