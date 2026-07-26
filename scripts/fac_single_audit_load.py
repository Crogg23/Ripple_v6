"""Load Federal Audit Clearinghouse (FAC) single audit data.

Source: https://api.fac.gov/general (REST API, JSON, paginated)
Entity keys: EIN (auditee_ein, auditor_ein), UEI (auditee_uei)
Estimated volume: ~300K-500K records (fiscal years 2016-present)

    python scripts/fac_single_audit_load.py          # preview (count + sample)
    python scripts/fac_single_audit_load.py --run    # actual load
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))

try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402

TABLE = "FED_FAC_SINGLE_AUDIT"
API_BASE = "https://api.fac.gov/general"
API_KEY = "wLMnDanzGi60LgkWgbHxf0aC1FQGlECvuki9VBRY"
PAGE_SIZE = 10000
RETRY_STATUS = {429, 500, 502, 503, 504}
MAX_RETRIES = 3

# Columns to keep (subset of the ~50 fields returned)
KEEP_COLS = [
    "report_id", "audit_year", "auditee_uei", "auditee_ein", "auditee_name",
    "auditee_city", "auditee_state", "auditee_zip", "auditee_address_line_1",
    "auditor_ein", "auditor_firm_name", "auditor_city", "auditor_state",
    "auditor_zip", "entity_type", "audit_type", "gaap_results",
    "is_going_concern_included", "is_internal_control_material_weakness_disclosed",
    "is_material_noncompliance_disclosed", "total_amount_expended",
    "is_low_risk_auditee", "oversight_agency", "cognizant_agency",
    "fy_start_date", "fy_end_date", "fac_accepted_date", "data_source",
]


def _fetch_page(offset: int) -> list[dict]:
    """Fetch one page from the FAC API with retry."""
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(API_BASE, params={
                "limit": PAGE_SIZE, "offset": offset, "api_key": API_KEY
            }, timeout=60)
            if resp.status_code in RETRY_STATUS:
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)
    return []


def fetch_all() -> pd.DataFrame:
    """Page through the entire FAC general endpoint."""
    all_rows = []
    offset = 0
    time.sleep(2)  # avoid rate-limit from back-to-back calls
    while True:
        page = _fetch_page(offset)
        if not page:
            break
        all_rows.extend(page)
        print(f"  fetched {len(all_rows):,} records (offset={offset:,})...", end="\r")
        offset += PAGE_SIZE
        if len(page) < PAGE_SIZE:
            break
        time.sleep(0.5)  # polite pacing
    print(f"  fetched {len(all_rows):,} records total.          ")
    if not all_rows:
        return pd.DataFrame()
    df = pd.DataFrame(all_rows)
    # Keep only the columns we want, uppercase for Snowflake
    keep = [c for c in KEEP_COLS if c in df.columns]
    df = df[keep]
    df.columns = [c.upper() for c in df.columns]
    return df


def load(conn, df: pd.DataFrame) -> int:
    """Load into LIBRARY_RAW.LANDING via staging + SWAP."""
    from snowflake.connector.pandas_tools import write_pandas

    staging = f"{TABLE}__STAGING"
    cur = conn.cursor()

    # Write data to staging (auto-creates the table from DataFrame dtypes)
    cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{staging}")
    write_pandas(conn, df, staging, database="LIBRARY_RAW", schema="LANDING",
                 auto_create_table=True, overwrite=True)

    # Add provenance columns
    cur.execute(f"ALTER TABLE LIBRARY_RAW.LANDING.{staging} ADD COLUMN IF NOT EXISTS "
                f"_INGESTED_AT TIMESTAMP_NTZ")
    cur.execute(f"ALTER TABLE LIBRARY_RAW.LANDING.{staging} ADD COLUMN IF NOT EXISTS "
                f"_SOURCE_RUN_ID STRING")
    cur.execute(f"UPDATE LIBRARY_RAW.LANDING.{staging} SET "
                f"_INGESTED_AT = CURRENT_TIMESTAMP(), _SOURCE_RUN_ID = UUID_STRING()")

    # Density gate
    cur.execute(f"SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.{staging}")
    n = cur.fetchone()[0]
    if n == 0:
        cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{staging}")
        print("  EMPTY — staging dropped, no swap.")
        return 0

    # Atomic swap
    cur.execute(f"CREATE TABLE IF NOT EXISTS LIBRARY_RAW.LANDING.{TABLE} "
                f"LIKE LIBRARY_RAW.LANDING.{staging}")
    cur.execute(f"ALTER TABLE LIBRARY_RAW.LANDING.{staging} "
                f"SWAP WITH LIBRARY_RAW.LANDING.{TABLE}")
    cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{staging}")
    print(f"  loaded {n:,} rows -> LIBRARY_RAW.LANDING.{TABLE}")
    return n


def register(conn, n_rows: int):
    """Register in SOURCE_REGISTRY."""
    cur = conn.cursor()
    cur.execute(f"""
        MERGE INTO LIBRARY_META.REGISTRY.SOURCE_REGISTRY t
        USING (SELECT 'FED_FAC_SINGLE_AUDIT' AS SOURCE_ID) s ON t.SOURCE_ID = s.SOURCE_ID
        WHEN NOT MATCHED THEN INSERT (SOURCE_ID, NAME, PUBLISHER, DESCRIPTION,
            JURISDICTION, CATEGORY, JOIN_KEYS, PRIORITY_TIER, ACCESS_METHOD, URL,
            UNIT_OF_OBSERVATION, UPDATE_CADENCE, DOMAIN_PRIMARY)
        VALUES ('FED_FAC_SINGLE_AUDIT',
            'Federal Audit Clearinghouse — Single Audits',
            'GSA / Federal Audit Clearinghouse',
            'Every single audit submitted to the FAC since 2016. One row per audit engagement. '
            'Links auditee EIN + UEI to audit findings, federal expenditures, and compliance.',
            'US', 'spending_budget', 'EIN, UEI, ZIP', '1', 'API + bulk download',
            'https://api.fac.gov/general',
            'one row = one single audit submission (engagement-level)',
            'annual', 'spending_budget')
    """)
    print(f"  registered {TABLE} in SOURCE_REGISTRY")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="actually load (default: preview)")
    args = ap.parse_args()

    print(f"FAC Single Audit Loader")
    print(f"  API: {API_BASE}")
    print(f"  Table: LIBRARY_RAW.LANDING.{TABLE}")

    if not args.run:
        # Preview: fetch first page, show schema + count
        page = _fetch_page(0)
        print(f"  first page: {len(page)} records")
        if page:
            print(f"  columns: {list(page[0].keys())}")
            print(f"  sample EIN: {page[0].get('auditee_ein')}")
            print(f"  sample UEI: {page[0].get('auditee_uei')}")
            print(f"  sample name: {page[0].get('auditee_name')}")
        print("\n  (preview only — add --run to actually load)")
        return 0

    print("Fetching all records from FAC API...")
    df = fetch_all()
    if df.empty:
        print("  ERROR: API returned 0 records. May be rate-limited (DEMO_KEY). Retry in a minute.")
        return 1
    print(f"  {len(df):,} rows, {len(df.columns)} columns")
    print(f"  EIN populated: {df['AUDITEE_EIN'].notna().sum():,} ({100*df['AUDITEE_EIN'].notna().mean():.0f}%)")
    print(f"  UEI populated: {df['AUDITEE_UEI'].notna().sum():,} ({100*df['AUDITEE_UEI'].notna().mean():.0f}%)")

    print("Loading to Snowflake (staging + SWAP)...")
    conn = snow.connect()
    try:
        n = load(conn, df)
        if n > 0:
            register(conn, n)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
