#!/usr/bin/env python3
"""Chunked, incremental multi-day backfill for NOAA AIS vessel positions
(discovery sweep #4: FED_NOAA_AIS is a single 24h snapshot, 2024-01-01 only --
the entire OFAC/OpenSanctions <-> AIS bridge sees one calendar day). Each extra
day turns the snapshot into a surveillance time series and unlocks loitering /
port-call / behavior-over-time detectors.

Source: marinecadastre.gov daily zips
  https://coast.noaa.gov/htdata/CMSP/AISDataHandler/<YYYY>/AIS_<YYYY_MM_DD>.zip
Each day is ~292 MB zipped / ~7M rows, so this STREAMS the inner CSV in chunks and
APPENDS (overwrite=False) to LIBRARY_RAW.LANDING.FED_NOAA_AIS, matching the existing
schema (adds SOURCE_FILE + DATE). Idempotent: a date whose SOURCE_FILE is already in
the table is skipped, so re-running never duplicates.

    python3 scripts/noaa_ais_backfill.py --dates 2024-01-02 2024-01-03           # preview
    python3 scripts/noaa_ais_backfill.py --start 2024-01-02 --end 2024-01-07     # preview range
    python3 scripts/noaa_ais_backfill.py --start 2024-01-02 --end 2024-01-07 --run

BUDGET: each day is a real (small) load + storage. Check RIPPLE_BUDGET before a big
window. Loading is cheap on RIPPLE_WH (X-Small) -- ~0.1 credit/day -- but storage and
wall-clock add up; pick the window deliberately.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import io
import sys
import uuid
import zipfile
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
import snow          # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

TABLE = "FED_NOAA_AIS"
SID = "fed_noaa_ais"
UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
CHUNK = 500_000
SCRATCH = Path("/private/tmp/claude-501/-Users-chrisr--Documents-GitHub-Ripple-v6/"
               "e8eac5fb-de36-4362-9440-da24a904b9b4/scratchpad")

# marinecadastre CSV header -> landing column. Their casing is CamelCase; the table
# is UPPER with TRANSCEIVER_CLASS underscored.
COLMAP = {
    "MMSI": "MMSI", "BaseDateTime": "BASEDATETIME", "LAT": "LAT", "LON": "LON",
    "SOG": "SOG", "COG": "COG", "Heading": "HEADING", "VesselName": "VESSELNAME",
    "IMO": "IMO", "CallSign": "CALLSIGN", "VesselType": "VESSELTYPE", "Status": "STATUS",
    "Length": "LENGTH", "Width": "WIDTH", "Draft": "DRAFT", "Cargo": "CARGO",
    "TransceiverClass": "TRANSCEIVER_CLASS",
}
TABLE_COLS = list(COLMAP.values()) + ["SOURCE_FILE", "DATE",
                                      "_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"]


def _url(d: _dt.date) -> tuple[str, str]:
    fn = f"AIS_{d:%Y_%m_%d}.zip"
    return f"https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{d:%Y}/{fn}", fn


def _already_loaded(conn) -> set[str]:
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT DISTINCT SOURCE_FILE FROM LIBRARY_RAW.LANDING.{TABLE}")
        return {r[0] for r in cur.fetchall() if r[0]}
    finally:
        cur.close()


def _dates(args) -> list[_dt.date]:
    if args.dates:
        return [_dt.date.fromisoformat(s) for s in args.dates]
    if args.start and args.end:
        a, b = _dt.date.fromisoformat(args.start), _dt.date.fromisoformat(args.end)
        return [a + _dt.timedelta(days=i) for i in range((b - a).days + 1)]
    raise SystemExit("give --dates or --start/--end")


def _load_day(conn, d: _dt.date, run_id: str) -> tuple[bool, str]:
    url, fn = _url(d)
    tmp = SCRATCH / fn
    try:
        # stream to disk (don't hold 292MB in memory)
        with requests.get(url, headers=UA, timeout=600, stream=True) as r:
            if r.status_code != 200:
                return False, f"HTTP {r.status_code}"
            with open(tmp, "wb") as fh:
                for c in r.iter_content(1 << 20):
                    fh.write(c)
        sha = hashlib.sha256(tmp.read_bytes()).hexdigest()
        started = ingest._utcnow()
        appended = 0
        zf = zipfile.ZipFile(tmp)
        csv_name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
        with zf.open(csv_name) as fh:
            for chunk in pd.read_csv(fh, dtype=str, keep_default_na=False,
                                     low_memory=False, chunksize=CHUNK):
                chunk = chunk.rename(columns=COLMAP)
                # keep only known cols (defensive against header drift)
                for c in COLMAP.values():
                    if c not in chunk.columns:
                        chunk[c] = ""
                out = chunk[list(COLMAP.values())].copy()
                out["SOURCE_FILE"] = fn
                out["DATE"] = d.isoformat()
                out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
                out[ingest.META_SOURCE_RUN_ID] = run_id
                out[ingest.META_SRC_SHA256] = sha
                out = out[TABLE_COLS]
                ok, _c, n, _ = write_pandas(conn, out, table_name=TABLE,
                                            database=settings.raw_database, schema=settings.raw_schema,
                                            auto_create_table=False, overwrite=False,
                                            quote_identifiers=False)
                if not ok:
                    return False, f"write_pandas failed after {appended:,}"
                appended += len(out)
        ended = ingest._utcnow()
        ingest._log_run(conn, SID, run_id, "success", appended, tmp.stat().st_size, sha, url,
                        started, ended, f"AIS backfill {d.isoformat()}: appended {appended:,} rows")
        return True, f"appended {appended:,} rows"
    except Exception as ex:  # noqa: BLE001
        return False, f"{type(ex).__name__}: {str(ex)[:140]}"
    finally:
        try:
            tmp.unlink()
        except Exception:
            pass


def main() -> int:
    ap = argparse.ArgumentParser(description="Chunked multi-day NOAA AIS backfill (append).")
    ap.add_argument("--dates", nargs="*", help="explicit YYYY-MM-DD dates")
    ap.add_argument("--start", help="range start YYYY-MM-DD")
    ap.add_argument("--end", help="range end YYYY-MM-DD")
    ap.add_argument("--run", action="store_true", help="actually download + append (else preview)")
    args = ap.parse_args()
    dates = _dates(args)

    conn = snow.connect()
    try:
        loaded = _already_loaded(conn)
        todo = [d for d in dates if f"AIS_{d:%Y_%m_%d}.zip" not in loaded]
        skip = [d for d in dates if d not in todo]
        print(f"AIS backfill: {len(dates)} date(s) requested; {len(skip)} already loaded; "
              f"{len(todo)} to load.")
        for d in skip:
            print(f"  - {d}  already in table (SOURCE_FILE present) -- skip")
        if not args.run:
            for d in todo:
                url, fn = _url(d)
                print(f"  + {d}  {url}")
            print(f"\nPREVIEW only. ~7M rows/day (~292 MB zip each). Add --run to load {len(todo)} day(s).")
            return 0
        run_id = uuid.uuid4().hex[:16]
        ok = fail = 0
        for d in todo:
            good, msg = _load_day(conn, d, run_id)
            print(f"  {'✓' if good else '✗'} {d}  {msg}", flush=True)
            ok += good; fail += (not good)
        # confirm the unlock: distinct dates now in the table
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(DISTINCT DATE) FROM LIBRARY_RAW.LANDING.{TABLE}")
        ndates = cur.fetchone()[0]; cur.close()
        print(f"\nDONE: {ok} day(s) loaded, {fail} failed. FED_NOAA_AIS now spans {ndates} distinct date(s).")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
