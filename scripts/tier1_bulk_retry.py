"""Retry loader for failed datasets -- corrected URLs from v1 run.

    python scripts/tier1_bulk_retry.py              # preview
    python scripts/tier1_bulk_retry.py --run        # load all
"""
from __future__ import annotations

import argparse
import bz2
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

# ---------------------------------------------------------------------------
# CORRECTED MANIFEST
# ---------------------------------------------------------------------------

MANIFEST = [
    # --- CFTC (fix: correct filename for combined/financial) ---
    {
        "table": "FED_CFTC_COT_FINANCIAL",
        "url": "https://www.cftc.gov/files/dea/history/fut_fin_txt_2024.zip",
        "description": "CFTC Commitments of Traders - Financial Futures (2024)",
        "format": "zip_csv",
    },
    # --- Federal Reserve Z.1 (fix: correct path) ---
    {
        "table": "FED_FRB_Z1_CSV",
        "url": "https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip",
        "description": "Fed Z.1 Financial Accounts of the US (CSV bulk)",
        "format": "zip_csv",
    },
    # --- OSHA (fix: date is 20250701 not 20250101) ---
    {
        "table": "FED_DOL_OSHA_INSPECTIONS",
        "url": "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250701.csv.zip",
        "description": "OSHA Enforcement - Inspection records (Jul 2025)",
        "format": "zip_csv",
    },
    {
        "table": "FED_DOL_OSHA_VIOLATIONS",
        "url": "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_violation_20250701.csv.zip",
        "description": "OSHA Enforcement - Violation records (Jul 2025)",
        "format": "zip_csv",
    },
    {
        "table": "FED_DOL_OSHA_ACCIDENTS",
        "url": "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_accident_20250701.csv.zip",
        "description": "OSHA Enforcement - Accident/injury records (Jul 2025)",
        "format": "zip_csv",
    },
    # --- DOL WHD (fix: same date pattern) ---
    {
        "table": "FED_DOL_WHD_WHISARD",
        "url": "https://enforcedata.dol.gov/views/data_catalogs/whd/whd_whisard_20250701.csv.zip",
        "description": "DOL Wage & Hour Division - WHISARD enforcement cases (Jul 2025)",
        "format": "zip_csv",
    },
    # --- EPA eGRID (now with openpyxl installed) ---
    {
        "table": "FED_EPA_EGRID_PLANT_2022",
        "url": "https://www.epa.gov/system/files/documents/2024-01/egrid2022_data.xlsx",
        "description": "EPA eGRID - Plant-level emissions & generation (2022)",
        "format": "xlsx",
        "sheet": "PLNT22",
    },
    # --- Mapping Police Violence (xlsx, openpyxl now installed) ---
    {
        "table": "XC_MAPPING_POLICE_VIOLENCE",
        "url": "https://mappingpoliceviolence.us/s/MPVDatasetDownload.xlsx",
        "description": "Mapping Police Violence comprehensive database",
        "format": "xlsx",
    },
    # --- CourtListener (fix: date-versioned files, latest = 2026-06-30) ---
    {
        "table": "FED_COURTLISTENER_JUDGES",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/people-db-people-2026-06-30.csv.bz2",
        "description": "CourtListener Judge/Person database (Jun 2026 snapshot)",
        "format": "bz2_csv",
    },
    {
        "table": "FED_COURTLISTENER_POSITIONS",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/people-db-positions-2026-06-30.csv.bz2",
        "description": "CourtListener judicial positions held (Jun 2026)",
        "format": "bz2_csv",
    },
    {
        "table": "FED_COURTLISTENER_FINANCIAL_DISCLOSURES",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/financial-disclosures-2026-06-30.csv.bz2",
        "description": "CourtListener judge financial disclosures (Jun 2026)",
        "format": "bz2_csv",
    },
    {
        "table": "FED_COURTLISTENER_INVESTMENTS",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/financial-disclosure-investments-2026-06-30.csv.bz2",
        "description": "CourtListener judge investment holdings (Jun 2026)",
        "format": "bz2_csv",
    },
    # --- Google Political Ads (fix: stream full download, load largest CSVs) ---
    {
        "table": "FED_GOOGLE_POLADS_CREATIVE_STATS",
        "url": "https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip",
        "description": "Google Political Ads Transparency (full bundle)",
        "format": "zip_multi_google",
    },
    # --- CDC NNDSS (try alternate Socrata dataset ID) ---
    {
        "table": "FED_CDC_NNDSS_WEEKLY_2024",
        "url": "https://data.cdc.gov/api/views/xbil-uhr4/rows.csv?accessType=DOWNLOAD",
        "description": "NNDSS Weekly Disease Tables (2024, alternate ID)",
        "format": "csv",
    },
]


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
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
                     low_memory=False, encoding_errors="replace")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_zip_csv(conn, entry, max_rows):
    resp = requests.get(entry["url"], timeout=600, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_files = [n for n in zf.namelist()
                     if n.lower().endswith(('.csv', '.txt'))
                     and '__MACOSX' not in n]
        if not csv_files:
            raise RuntimeError(f"No CSV/TXT in ZIP")
        csv_files.sort(key=lambda n: zf.getinfo(n).file_size, reverse=True)
        with zf.open(csv_files[0]) as f:
            content = f.read()
    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_xlsx(conn, entry, max_rows):
    resp = requests.get(entry["url"], timeout=300, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    sheet = entry.get("sheet", 0)
    df = pd.read_excel(io.BytesIO(resp.content), dtype=str, nrows=max_rows + 1,
                       sheet_name=sheet)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_bz2_csv(conn, entry, max_rows):
    resp = requests.get(entry["url"], timeout=600, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    decompressed = bz2.decompress(resp.content)
    df = pd.read_csv(io.BytesIO(decompressed), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"])


def load_zip_multi_google(conn, entry, max_rows):
    """Google Political Ads bundle -- multiple CSVs, load the key ones."""
    print("  Downloading Google Political Ads bundle (large)...")
    resp = requests.get(entry["url"], timeout=900, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    total = 0
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_files = [n for n in zf.namelist()
                     if n.lower().endswith('.csv') and '__MACOSX' not in n]
        csv_files.sort(key=lambda n: zf.getinfo(n).file_size, reverse=True)
        print(f"  Found {len(csv_files)} CSVs in bundle")
        for name in csv_files[:8]:
            stem = Path(name).stem.replace("google-political-ads-", "")
            tbl = bulk.table_name("FED_GOOGLE_POLADS", stem)
            try:
                with zf.open(name) as f:
                    content = f.read()
                df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                                 low_memory=False, encoding_errors="replace")
                if len(df) > max_rows:
                    raise RuntimeError(
                        f"{tbl}: source has more than max_rows={max_rows:,} rows -- "
                        f"refusing to silently truncate. Pass a higher max_rows explicitly.")
                if df.empty:
                    continue
                df = _stamp(df, sha, run_id, started)
                n = _write(conn, df, tbl)
                print(f"    {tbl}: {n:,} rows")
                total += n
            except Exception as e:
                print(f"    FAILED {tbl}: {str(e)[:100]}")
    return total


FORMAT_LOADERS = {
    "csv": load_csv,
    "zip_csv": load_zip_csv,
    "xlsx": load_xlsx,
    "bz2_csv": load_bz2_csv,
    "zip_multi_google": load_zip_multi_google,
}


def main():
    ap = argparse.ArgumentParser(description="Retry failed Tier-1 bulk downloads (corrected URLs)")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--max-rows", type=int, default=500_000)
    args = ap.parse_args()

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING\n")

    to_load = []
    for entry in MANIFEST:
        if entry["table"] in loaded:
            print(f"  SKIP {entry['table']} (exists)")
        else:
            to_load.append(entry)

    print(f"\n{len(to_load)} datasets to retry\n")

    if not args.run:
        print("(preview -- add --run to execute)\n")
        for i, e in enumerate(to_load, 1):
            print(f"  {i:2d}. {e['table']:50s} {e['format']}")
            print(f"      {e['url'][:100]}")
        return 0

    results = []
    for i, entry in enumerate(to_load, 1):
        print(f"\n[{i}/{len(to_load)}] {entry['table']}")
        print(f"  {entry['description']}")
        loader = FORMAT_LOADERS.get(entry["format"])
        if not loader:
            print(f"  SKIP: no loader for '{entry['format']}'")
            continue
        try:
            n = loader(conn, entry, args.max_rows)
            print(f"  -> {n:,} rows loaded")
            results.append({"name": entry["table"], "rows": n})
        except Exception as e:
            print(f"  FAILED: {str(e)[:200]}")
            results.append({"name": entry["table"], "error": str(e)[:200]})

    ok = sum(1 for r in results if r.get("rows", 0) > 0)
    total = sum(r.get("rows", 0) for r in results)
    failed = [r for r in results if "error" in r]
    print(f"\n{'='*60}")
    print(f"DONE: {ok}/{len(to_load)} loaded, {total:,} total rows")
    if failed:
        print(f"\nStill failing ({len(failed)}):")
        for r in failed:
            print(f"  - {r['name']}: {r['error'][:80]}")
    print(f"{'='*60}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
