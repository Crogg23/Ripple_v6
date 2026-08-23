"""Load the SAM.gov public Exclusions extract file into LANDING (plan B loader).

The paged Entity API burned its daily quota twice (2026-08-22/23: attempt 1 died
at page 14 with 10k of ~168k landed; attempt 2 with 25s pacing + 10-min backoff
also never got past the throttle). This loader instead pulls SAM Data Services'
daily public extract ZIP — no API key, no paging, one ~12MB file — and lands it
into FED_SAM_EXCLUSIONS_FULL_R2, the table the staging model actually reads.

Filename format is 2-digit-year + Julian day (e.g. ..._V2_26235.ZIP); the MMDDYYYY
form documented in older notes now returns 204. We walk back up to 10 days to find
the newest published file. Extract headers map 1:1 onto FULL_R2's columns
(verified 2026-08-23), so the write is a same-shape overwrite — the write_pandas
keeps-old-schema trap is moot here.

    python scripts/sam_exclusions_extract_load.py            # preview
    python scripts/sam_exclusions_extract_load.py --run      # download + land
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
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
except Exception:
    pass

import ingest  # noqa: E402
import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402
from config import settings  # noqa: E402

SID = "fed_sam_exclusions"
TABLE = "FED_SAM_EXCLUSIONS_FULL_R2"
URL_TPL = ("https://sam.gov/api/prod/fileextractservices/v1/api/download/"
           "Exclusions/Public%20V2/SAM_Exclusions_Public_Extract_V2_{stamp}.ZIP")
DATA_DIR = _REPO / "data" / "sam_exclusions"

HEADER_MAP = {
    "Classification": "CLASSIFICATION", "Name": "NAME", "Prefix": "PREFIX",
    "First": "FIRST", "Middle": "MIDDLE", "Last": "LAST", "Suffix": "SUFFIX",
    "Address 1": "ADDRESS_1", "Address 2": "ADDRESS_2", "Address 3": "ADDRESS_3",
    "Address 4": "ADDRESS_4", "City": "CITY", "State / Province": "STATE_PROVINCE",
    "Country": "COUNTRY", "Zip Code": "ZIP_CODE", "Open Data Flag": "OPEN_DATA_FLAG",
    "Blank (Deprecated)": "BLANK_DEPRECATED", "Unique Entity ID": "UNIQUE_ENTITY_ID",
    "Exclusion Program": "EXCLUSION_PROGRAM", "Excluding Agency": "EXCLUDING_AGENCY",
    "CT Code": "CT_CODE", "Exclusion Type": "EXCLUSION_TYPE",
    "Additional Comments": "ADDITIONAL_COMMENTS", "Active Date": "ACTIVE_DATE",
    "Termination Date": "TERMINATION_DATE", "Record Status": "RECORD_STATUS",
    "Cross-Reference": "CROSS_REFERENCE", "SAM Number": "SAM_NUMBER",
    "CAGE": "CAGE", "NPI": "NPI", "Creation_Date": "CREATION_DATE",
}


def _fetch_latest() -> tuple[Path, str]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today()
    for back in range(10):
        stamp = (today - dt.timedelta(days=back)).strftime("%y%j")
        url = URL_TPL.format(stamp=stamp)
        r = requests.get(url, timeout=300, stream=True)
        head = next(r.iter_content(4), b"")
        if r.status_code == 200 and head[:2] == b"PK":
            path = DATA_DIR / f"SAM_Exclusions_Public_Extract_V2_{stamp}.ZIP"
            with open(path, "wb") as fh:
                fh.write(head)
                for chunk in r.iter_content(1 << 20):
                    fh.write(chunk)
            print(f"downloaded {path.name} ({path.stat().st_size:,} bytes)", flush=True)
            return path, url
        r.close()
    raise SystemExit("no extract file found in the last 10 days (all 204)")


def _read(path: Path) -> pd.DataFrame:
    z = zipfile.ZipFile(path)
    name = z.namelist()[0]
    with z.open(name) as fh:
        txt = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
        rdr = csv.reader(txt)
        hdr = next(rdr)
        unmapped = [h for h in hdr if h not in HEADER_MAP]
        if unmapped:
            raise SystemExit(f"extract header drift — unmapped columns: {unmapped}")
        rows = list(rdr)
    df = pd.DataFrame(rows, columns=[HEADER_MAP[h] for h in hdr])
    # byte-faithful landing: keep strings, blank -> None (never the text 'nan')
    return df.map(lambda v: None if v is None or str(v).strip() == "" else str(v))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="SAM exclusions extract-file loader")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    path, url = _fetch_latest()
    df = _read(path)
    print(f"parsed {len(df):,} rows x {len(df.columns)} cols", flush=True)
    if not args.run:
        print(df.head(3).to_string())
        print("\nPREVIEW only — add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    df[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
    df[ingest.META_SOURCE_RUN_ID] = run_id
    df[ingest.META_SRC_SHA256] = hashlib.sha256(path.read_bytes()).hexdigest()

    from snowflake.connector.pandas_tools import write_pandas
    conn = snow.connect()
    try:
        ok, _c, _r, _ = write_pandas(
            conn, df, table_name=TABLE, database=settings.raw_database,
            schema=settings.raw_schema, auto_create_table=True,
            overwrite=True, quote_identifiers=False)
        if not ok:
            raise RuntimeError("write_pandas failed")
        passed, report = bulk.run_quality_gate(
            conn, SID, TABLE, run_id, row_count=len(df),
            source_url=url, expected_min_rows=160_000)
        if not passed:
            print(f"QUALITY GATE FAILED {TABLE}: {report}")
            return 1
        print(f"LOADED {len(df):,} rows -> LIBRARY_RAW.LANDING.{TABLE}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
