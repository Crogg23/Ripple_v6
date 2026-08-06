"""Batch loader for remaining Tier-1 bulk download sources.

Targets ~30 datasets that are direct CSV/ZIP downloads with no auth required.
Clusters: CFTC, Fed Reserve, OSHA, DOL Wage-Hour, EPA (TRI/eGRID), Treasury
FiscalData, OPM FedScope, Google Political Ads, CourtListener, Mapping Police
Violence, Tax Justice, Transparency International, state lobbying/CF, and more.

    python scripts/tier1_bulk_batch_load.py              # preview
    python scripts/tier1_bulk_batch_load.py --run        # load all
    python scripts/tier1_bulk_batch_load.py --run --group fed_reserve
    python scripts/tier1_bulk_batch_load.py --run --group cftc
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

# ---------------------------------------------------------------------------
# MANIFEST -- grouped by publisher cluster
# ---------------------------------------------------------------------------

MANIFEST = [
    # --- CFTC ---
    {
        "group": "cftc",
        "table": "FED_CFTC_COT_FUTURES",
        "url": "https://www.cftc.gov/files/dea/history/deacot2024.zip",
        "description": "CFTC Commitments of Traders - Futures Only (2024)",
        "format": "zip_csv",
    },
    {
        "group": "cftc",
        "table": "FED_CFTC_COT_COMBINED",
        "url": "https://www.cftc.gov/files/dea/history/deahistfo_2024.zip",
        "description": "CFTC Commitments of Traders - Financial Futures (2024)",
        "format": "zip_csv",
    },
    # --- Federal Reserve ---
    {
        "group": "fed_reserve",
        "table": "FED_FRB_H15_SELECTED_RATES",
        "url": "https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&series=bf17364827e38702b42a58cf8eaa3f78&lastobs=&from=&to=&filetype=csv&label=include&layout=seriescolumn",
        "description": "Fed H.15 Selected Interest Rates (full history CSV)",
        "format": "csv",
    },
    {
        "group": "fed_reserve",
        "table": "FED_FRB_Z1_LEVELS",
        "url": "https://www.federalreserve.gov/releases/z1/dataviz/z1/csv/z1_csv.zip",
        "description": "Fed Z.1 Financial Accounts CSV bulk download",
        "format": "zip_csv",
    },
    {
        "group": "fed_reserve",
        "table": "FED_FRB_H8_COMMERCIAL_BANKS",
        "url": "https://www.federalreserve.gov/datadownload/Output.aspx?rel=H8&series=3d8bce8e3fc3b8d78be3e5a4d4b83a68&lastobs=&from=&to=&filetype=csv&label=include&layout=seriescolumn",
        "description": "Fed H.8 Assets & Liabilities of Commercial Banks",
        "format": "csv",
    },
    # --- OSHA ---
    {
        "group": "osha",
        "table": "FED_DOL_OSHA_INSPECTIONS",
        "url": "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250101.csv.zip",
        "description": "OSHA Enforcement - Inspection records",
        "format": "zip_csv",
        "fallback_url": "https://enforcedata.dol.gov/views/data_summary.php",
    },
    {
        "group": "osha",
        "table": "FED_DOL_OSHA_VIOLATIONS",
        "url": "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_violation_20250101.csv.zip",
        "description": "OSHA Enforcement - Violation records",
        "format": "zip_csv",
        "fallback_url": "https://enforcedata.dol.gov/views/data_summary.php",
    },
    {
        "group": "osha",
        "table": "FED_DOL_OSHA_ACCIDENTS",
        "url": "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_accident_20250101.csv.zip",
        "description": "OSHA Enforcement - Accident/injury records",
        "format": "zip_csv",
        "fallback_url": "https://enforcedata.dol.gov/views/data_summary.php",
    },
    # --- DOL Wage & Hour ---
    {
        "group": "dol_whd",
        "table": "FED_DOL_WHD_WHISARD",
        "url": "https://enforcedata.dol.gov/views/data_catalogs/whd/whd_whisard_20250101.csv.zip",
        "description": "DOL Wage & Hour Division - WHISARD enforcement cases",
        "format": "zip_csv",
        "fallback_url": "https://enforcedata.dol.gov/views/data_summary.php",
    },
    # --- EPA TRI ---
    {
        "group": "epa",
        "table": "FED_EPA_TRI_BASIC_2023",
        "url": "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/2023_us/csv",
        "description": "EPA Toxics Release Inventory - Basic data file (2023)",
        "format": "csv",
        "fallback_url": "https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present",
    },
    {
        "group": "epa",
        "table": "FED_EPA_EGRID_PLANT_2022",
        "url": "https://www.epa.gov/system/files/documents/2024-01/egrid2022_data.xlsx",
        "description": "EPA eGRID - Plant-level emissions (2022, Excel)",
        "format": "xlsx",
        "sheet": "PLNT22",
    },
    # --- Treasury FiscalData ---
    {
        "group": "treasury",
        "table": "FED_TREASURY_DTS_DEPOSITS",
        "url": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/deposits_withdrawals_operating_cash?format=csv&page[size]=10000",
        "description": "Daily Treasury Statement - Deposits/Withdrawals (recent)",
        "format": "csv",
    },
    {
        "group": "treasury",
        "table": "FED_TREASURY_MTS_RECEIPTS",
        "url": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_4?format=csv&page[size]=10000",
        "description": "Monthly Treasury Statement - Receipts/Outlays",
        "format": "csv",
    },
    {
        "group": "treasury",
        "table": "FED_TREASURY_DEBT_OUTSTANDING",
        "url": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_outstanding?format=csv&page[size]=10000",
        "description": "Treasury Debt Outstanding (historical)",
        "format": "csv",
    },
    # --- OPM FedScope ---
    {
        "group": "opm",
        "table": "FED_OPM_FEDSCOPE_EMPLOYMENT",
        "url": "https://www.opm.gov/data/datasets/Files/508/14cee05b-73be-4a1b-8987-f0afbce7fd5c.zip",
        "description": "OPM FedScope Employment data (FY2024 Q4)",
        "format": "zip_csv",
        "fallback_url": "https://www.opm.gov/data/datasets/",
    },
    # --- Google Political Ads ---
    {
        "group": "google_polads",
        "table": "FED_GOOGLE_POLADS_CREATIVE_STATS",
        "url": "https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip",
        "description": "Google Political Ads Transparency Report (full bundle ZIP)",
        "format": "zip_multi",
    },
    # --- Mapping Police Violence ---
    {
        "group": "policing",
        "table": "XC_MAPPING_POLICE_VIOLENCE",
        "url": "https://mappingpoliceviolence.us/s/MPVDatasetDownload.xlsx",
        "description": "Mapping Police Violence comprehensive database",
        "format": "xlsx",
    },
    # --- CourtListener (Free Law Project) ---
    {
        "group": "courtlistener",
        "table": "FED_COURTLISTENER_JUDGES",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/people-db-all.csv.bz2",
        "description": "CourtListener Judge/Person database (all)",
        "format": "bz2_csv",
        "fallback_url": "https://www.courtlistener.com/help/api/bulk-data/",
    },
    {
        "group": "courtlistener",
        "table": "FED_COURTLISTENER_POSITIONS",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/positions-db-all.csv.bz2",
        "description": "CourtListener judicial positions held",
        "format": "bz2_csv",
    },
    {
        "group": "courtlistener",
        "table": "FED_COURTLISTENER_FINANCIAL_DISCLOSURES",
        "url": "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/financial-disclosures-db-all.csv.bz2",
        "description": "CourtListener judge financial disclosures",
        "format": "bz2_csv",
    },
    # --- Tax Justice Network ---
    {
        "group": "taxjustice",
        "table": "INTL_TAXJUSTICE_CTHI",
        "url": "https://cthi.taxjustice.net/cthi2024/CTHI-2024-Results.xlsx",
        "description": "Corporate Tax Haven Index 2024",
        "format": "xlsx",
    },
    {
        "group": "taxjustice",
        "table": "INTL_TAXJUSTICE_FSI",
        "url": "https://fsi.taxjustice.net/fsi2024/FSI-Rankings-2024.xlsx",
        "description": "Financial Secrecy Index 2024",
        "format": "xlsx",
    },
    # --- Transparency International ---
    {
        "group": "transparency_intl",
        "table": "INTL_TI_CPI_2024",
        "url": "https://images.transparencycdn.org/images/CPI-2024-Full-Data-Set.zip",
        "description": "Transparency International Corruption Perceptions Index 2024",
        "format": "zip_xlsx",
    },
    # --- WJP Rule of Law ---
    {
        "group": "wjp",
        "table": "INTL_WJP_ROLI_2024",
        "url": "https://worldjusticeproject.org/rule-of-law-index/downloads/WJPIndex2024_DATA_all_countries.xlsx",
        "description": "WJP Rule of Law Index 2024 - all countries",
        "format": "xlsx",
    },
    # --- State Lobbying ---
    {
        "group": "state_lobby",
        "table": "ST_CO_LOBBY_EXPENDITURES",
        "url": "https://tracer.sos.colorado.gov/PublicSite/Docs/BulkDataDownloads/LobbyistExpenditureData.csv",
        "description": "Colorado lobbying expenditure disclosures",
        "format": "csv",
        "fallback_url": "https://tracer.sos.colorado.gov/PublicSite/SearchPages/Lobbyist/LobbyistExpenditureData.aspx",
    },
    {
        "group": "state_lobby",
        "table": "ST_NY_LOBBY_ACTIVITY",
        "url": "https://data.ny.gov/api/views/jm74-shp9/rows.csv?accessType=DOWNLOAD",
        "description": "NY State lobbying activity (Open Data)",
        "format": "csv",
    },
    {
        "group": "state_lobby",
        "table": "ST_WA_PDC_LOBBY_EMPLOYERS",
        "url": "https://data.wa.gov/api/views/mwm3-kp97/rows.csv?accessType=DOWNLOAD",
        "description": "WA PDC lobbyist employer compensation",
        "format": "csv",
        "fallback_url": "https://www.pdc.wa.gov/political-disclosure-reporting-data/open-data",
    },
    {
        "group": "state_lobby",
        "table": "ST_TX_LOBBY_REGISTRATIONS",
        "url": "https://www.ethics.state.tx.us/data/search/lobby/2024Lobbyists.zip",
        "description": "TX Ethics Commission lobbyist registrations 2024",
        "format": "zip_csv",
    },
    # --- Florida Campaign Finance ---
    {
        "group": "state_cf",
        "table": "ST_FL_CF_CONTRIBUTIONS",
        "url": "https://dos.elections.myflorida.com/campaign-finance/contributions/DownloadContributions.aspx?typ=ContributionsAll&elecYear=2024&format=CSV",
        "description": "Florida all campaign contributions 2024",
        "format": "csv",
        "fallback_url": "https://dos.elections.myflorida.com/campaign-finance/contributions/",
    },
    # --- CDC NNDSS ---
    {
        "group": "cdc",
        "table": "FED_CDC_NNDSS_WEEKLY_2024",
        "url": "https://data.cdc.gov/api/views/x9gk-5huc/rows.csv?accessType=DOWNLOAD",
        "description": "NNDSS Weekly Tables of Notifiable Diseases (2024)",
        "format": "csv",
    },
    # --- EITI ---
    {
        "group": "eiti",
        "table": "INTL_EITI_SUMMARY_DATA",
        "url": "https://eiti.org/sites/default/files/2024-12/eiti_summary_data_2024.xlsx",
        "description": "EITI summary data - extractive industries transparency",
        "format": "xlsx",
    },
    # --- FinCEN SAR Stats ---
    {
        "group": "fincen",
        "table": "FED_FINCEN_SAR_STATS_2024",
        "url": "https://www.fincen.gov/sites/default/files/sar_stats/SARStats2024Q4.xlsx",
        "description": "FinCEN SAR Statistics 2024 Q4",
        "format": "xlsx",
        "fallback_url": "https://www.fincen.gov/reports/sar-stats",
    },
]


# ---------------------------------------------------------------------------
# Loaders by format
# ---------------------------------------------------------------------------
def _provenance(content: bytes) -> tuple[str, str, dt.datetime]:
    sha = hashlib.sha256(content).hexdigest()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc)
    return sha, run_id, started


def _stamp(df: pd.DataFrame, sha: str, run_id: str, started: dt.datetime) -> pd.DataFrame:
    df[bulk.META_INGESTED_AT] = started.replace(tzinfo=None)
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha
    return df


def _write(conn, df: pd.DataFrame, tbl: str, *,
           sha: str = "", run_id: str = "", source_url: str = "") -> int:
    from snowflake.connector.pandas_tools import write_pandas
    df.columns = [bulk.sf_col(c) for c in df.columns]
    ok, _c, _n, _ = write_pandas(
        conn, df, table_name=tbl,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas failed for {tbl}")
    # Quality gate + INGEST_RUNS row (audit 2026-08-05 finding #3: this loader
    # was a gate-bypass lane). A dq_failed load raises so it lands in the
    # failure summary and the exit code, never a silent "success".
    passed, report = bulk.run_quality_gate(
        conn, tbl, tbl, run_id or str(uuid.uuid4()),
        sha256=sha, source_url=source_url)
    if not passed:
        raise RuntimeError(f"{tbl}: quality gate failed -- {report}")
    return len(df)


def load_csv(conn, entry: dict, max_rows: int) -> int:
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
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_zip_csv(conn, entry: dict, max_rows: int) -> int:
    resp = requests.get(entry["url"], timeout=600, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_files = [n for n in zf.namelist()
                     if n.lower().endswith(('.csv', '.txt'))
                     and not n.startswith('__MACOSX')]
        if not csv_files:
            raise RuntimeError(f"No CSV/TXT in ZIP for {entry['table']}")
        # Take the largest
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
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_zip_multi(conn, entry: dict, max_rows: int) -> int:
    """Load multiple CSVs from a ZIP (e.g., Google Political Ads bundle)."""
    resp = requests.get(entry["url"], timeout=900, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    total = 0
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_files = [n for n in zf.namelist()
                     if n.lower().endswith('.csv') and not n.startswith('__MACOSX')]
        # Load up to 5 largest CSVs
        csv_files.sort(key=lambda n: zf.getinfo(n).file_size, reverse=True)
        for name in csv_files[:5]:
            tbl = bulk.table_name(entry["table"].rsplit("_", 1)[0], Path(name).stem)
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
                n = _write(conn, df, tbl, sha=sha, run_id=run_id,
                           source_url=entry["url"])
                print(f"      {tbl}: {n:,} rows")
                total += n
            except Exception as e:
                print(f"      FAILED {tbl}: {str(e)[:100]}")
    return total


def load_zip_xlsx(conn, entry: dict, max_rows: int) -> int:
    """Load Excel from inside a ZIP."""
    resp = requests.get(entry["url"], timeout=600, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        xlsx_files = [n for n in zf.namelist()
                      if n.lower().endswith(('.xlsx', '.xls'))
                      and not n.startswith('__MACOSX')]
        if not xlsx_files:
            raise RuntimeError(f"No Excel in ZIP for {entry['table']}")
        xlsx_files.sort(key=lambda n: zf.getinfo(n).file_size, reverse=True)
        with zf.open(xlsx_files[0]) as f:
            content = f.read()
    df = pd.read_excel(io.BytesIO(content), dtype=str, nrows=max_rows + 1, sheet_name=0)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_xlsx(conn, entry: dict, max_rows: int) -> int:
    resp = requests.get(entry["url"], timeout=300, headers=USER_AGENT)
    resp.raise_for_status()
    sha, run_id, started = _provenance(resp.content)
    sheet = entry.get("sheet", 0)
    df = pd.read_excel(io.BytesIO(resp.content), dtype=str, nrows=max_rows + 1, sheet_name=sheet)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_bz2_csv(conn, entry: dict, max_rows: int) -> int:
    import bz2
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
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


FORMAT_LOADERS = {
    "csv": load_csv,
    "zip_csv": load_zip_csv,
    "zip_multi": load_zip_multi,
    "zip_xlsx": load_zip_xlsx,
    "xlsx": load_xlsx,
    "bz2_csv": load_bz2_csv,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Batch loader for remaining Tier-1 bulk sources")
    ap.add_argument("--run", action="store_true", help="Actually load (default: preview)")
    ap.add_argument("--group", type=str, default=None, help="Only load a specific group")
    ap.add_argument("--max-rows", type=int, default=5_000_000, help="Row cap per dataset")
    args = ap.parse_args()

    entries = MANIFEST
    if args.group:
        entries = [e for e in entries if e["group"] == args.group]
        if not entries:
            print(f"No entries for group '{args.group}'")
            groups = sorted(set(e["group"] for e in MANIFEST))
            print(f"Available groups: {', '.join(groups)}")
            return 1

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING\n")

    to_load = []
    for entry in entries:
        if entry["table"] in loaded:
            print(f"  SKIP {entry['table']} (exists)")
        else:
            to_load.append(entry)

    print(f"\n{'='*60}")
    print(f"{len(to_load)} datasets to load")
    print(f"{'='*60}")

    if not args.run:
        print("\n(preview only -- add --run to execute)\n")
        for i, e in enumerate(to_load, 1):
            print(f"  {i:2d}. [{e['group']:15s}] {e['table']:45s}")
            print(f"      {e['description']}")
            print(f"      {e['url'][:90]}")
            print()
        return 0

    # Execute loads sequentially (many are large ZIPs)
    results = []
    for i, entry in enumerate(to_load, 1):
        print(f"\n[{i}/{len(to_load)}] {entry['table']}")
        print(f"  {entry['description']}")
        loader = FORMAT_LOADERS.get(entry["format"])
        if not loader:
            print(f"  SKIP: no loader for format '{entry['format']}'")
            results.append({"name": entry["table"], "error": f"no loader for {entry['format']}"})
            continue
        try:
            n = loader(conn, entry, args.max_rows)
            print(f"  -> {n:,} rows loaded")
            results.append({"name": entry["table"], "rows": n})
        except Exception as e:
            msg = str(e)[:200]
            print(f"  FAILED: {msg}")
            if entry.get("fallback_url"):
                print(f"  Check: {entry['fallback_url']}")
            results.append({"name": entry["table"], "error": msg})

    # Summary
    ok = sum(1 for r in results if "rows" in r and r["rows"] > 0)
    total_rows = sum(r.get("rows", 0) for r in results)
    failed = [r for r in results if "error" in r]

    print(f"\n{'='*60}")
    print(f"DONE: {ok}/{len(to_load)} loaded, {total_rows:,} total rows")
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for r in failed:
            print(f"  - {r['name']}: {r['error'][:80]}")
    print(f"{'='*60}")

    conn.close()
    # Non-zero exit when anything failed (audit: main() previously always
    # returned 0, hiding failures from calling schedulers).
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
