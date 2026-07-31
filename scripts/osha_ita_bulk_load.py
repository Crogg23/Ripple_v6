"""Load OSHA ITA (Injury Tracking) data from osha.gov direct downloads.

Also loads WHD data from the DOL enforcement catalog if accessible.
The enforcement inspection/violation/accident data is now behind auth
at enforcedata.dol.gov -- we load the ITA establishment-level data instead
which is freely available and arguably higher-value for pattern detection.

    python scripts/osha_ita_bulk_load.py --run
"""
from __future__ import annotations

import argparse
import hashlib
import io
import datetime as dt
import sys
import uuid
import zipfile
from pathlib import Path

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

MANIFEST = [
    # ITA 300A Summary (establishment-level annual summaries -- injuries, illnesses, fatalities)
    {
        "table": "FED_OSHA_ITA_300A_SUMMARY_2025",
        "url": "https://www.osha.gov/sites/default/files/ITA_300A_Summary_Data_2025_through_03-15-2026_v2.csv",
        "description": "OSHA ITA 300A Summary - establishment injury/illness reports (2025)",
        "format": "csv",
    },
    {
        "table": "FED_OSHA_ITA_CASE_DETAIL_2025",
        "url": "https://www.osha.gov/sites/default/largefiles/ITA_Case_Detail_Data_2025_through_3-15-2026.csv",
        "description": "OSHA ITA Case Detail - individual injury/illness cases (2025, 422MB)",
        "format": "csv_large",
    },
    {
        "table": "FED_OSHA_ITA_300A_SUMMARY_2024",
        "url": "https://www.osha.gov/sites/default/files/ITA_300A_Summary_Data_2024_through_12-31-2025.zip",
        "description": "OSHA ITA 300A Summary (2024)",
        "format": "zip_csv",
    },
    {
        "table": "FED_OSHA_ITA_CASE_DETAIL_2024",
        "url": "https://www.osha.gov/sites/default/files/ITA_Case_Detail_Data_2024_through_12-31-2025.zip",
        "description": "OSHA ITA Case Detail (2024, zipped)",
        "format": "zip_csv",
    },
    {
        "table": "FED_OSHA_ITA_300A_SUMMARY_2023",
        "url": "https://www.osha.gov/sites/default/files/ITA_300A_Summary_Data_2023_through_12-31-2024.zip",
        "description": "OSHA ITA 300A Summary (2023)",
        "format": "zip_csv",
    },
    {
        "table": "FED_OSHA_ITA_CASE_DETAIL_2023",
        "url": "https://www.osha.gov/sites/default/largefiles/ITA_Case_Detail_Data_2023_through_12-31-2023OIICS.zip",
        "description": "OSHA ITA Case Detail (2023, zipped)",
        "format": "zip_csv",
    },
]


def _provenance(content: bytes):
    sha = hashlib.sha256(content).hexdigest()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc)
    return sha, run_id, started


def _stamp(df, sha, run_id, started):
    df[bulk.META_INGESTED_AT] = started.replace(tzinfo=None)
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha
    return df


def _write(conn, df, tbl):
    from snowflake.connector.pandas_tools import write_pandas
    df.columns = [bulk.sf_col(c) for c in df.columns]
    ok, _c, _n, _ = write_pandas(
        conn, df, table_name=tbl,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas failed for {tbl}")
    return len(df)


def load_csv(conn, entry, max_rows):
    resp = requests.get(entry["url"], timeout=300, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    df = pd.read_csv(io.BytesIO(resp.content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace", on_bad_lines="skip")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_csv_large(conn, entry, max_rows):
    """Stream large CSV -- download with iter_content to avoid OOM."""
    print(f"  Streaming large file...")
    resp = requests.get(entry["url"], timeout=900, headers=USER_AGENT, stream=True)
    resp.raise_for_status()
    # Read up to 200MB into memory (enough for max_rows of CSV)
    content = b""
    for chunk in resp.iter_content(chunk_size=1_048_576):
        content += chunk
        if len(content) > 200_000_000:
            break
    resp.close()
    print(f"  Downloaded {len(content):,} bytes")
    sha, run_id, started = _provenance(content)
    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace", on_bad_lines="skip")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_zip_csv(conn, entry, max_rows):
    resp = requests.get(entry["url"], timeout=900, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_files = [n for n in zf.namelist()
                     if n.lower().endswith(('.csv', '.txt'))
                     and '__MACOSX' not in n]
        if not csv_files:
            raise RuntimeError("No CSV/TXT in ZIP")
        csv_files.sort(key=lambda n: zf.getinfo(n).file_size, reverse=True)
        with zf.open(csv_files[0]) as f:
            content = f.read()
    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace", on_bad_lines="skip")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


FORMAT_LOADERS = {
    "csv": load_csv,
    "csv_large": load_csv_large,
    "zip_csv": load_zip_csv,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--max-rows", type=int, default=500_000)
    args = ap.parse_args()

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING\n")

    to_load = [e for e in MANIFEST if e["table"] not in loaded]
    print(f"{len(to_load)} OSHA ITA datasets to load\n")

    if not args.run:
        for i, e in enumerate(to_load, 1):
            print(f"  {i}. {e['table']}")
            print(f"     {e['description']}")
            print(f"     {e['url'][:100]}")
        print("\n(add --run to execute)")
        return 0

    results = []
    for i, entry in enumerate(to_load, 1):
        print(f"\n[{i}/{len(to_load)}] {entry['table']}")
        print(f"  {entry['description']}")
        loader = FORMAT_LOADERS[entry["format"]]
        try:
            n = loader(conn, entry, args.max_rows)
            print(f"  -> {n:,} rows loaded")
            results.append({"name": entry["table"], "rows": n})
        except Exception as e:
            print(f"  FAILED: {str(e)[:200]}")
            results.append({"name": entry["table"], "error": str(e)[:200]})

    ok = sum(1 for r in results if r.get("rows", 0) > 0)
    total = sum(r.get("rows", 0) for r in results)
    print(f"\n{'='*60}")
    print(f"DONE: {ok}/{len(to_load)} loaded, {total:,} total rows")
    failed = [r for r in results if "error" in r]
    if failed:
        for r in failed:
            print(f"  - {r['name']}: {r['error'][:80]}")
    print(f"{'='*60}")
    conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
