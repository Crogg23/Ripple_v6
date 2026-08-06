#!/usr/bin/env python3
"""Loader for HRSA UDS (Uniform Data System) -- health center reporting data.

The OTHER half of HRSA beyond FED_HRSA_SHORTAGE_AREAS (which is HPSA shortage
areas only). UDS is HRSA's annual health-center performance/reporting workbook
(data.hrsa.gov), one file per year (H80-YYYY.xlsx), ~37 sheets. This loader
lands the two highest-value sheets:
  - HealthCenterInfo   (one row = one funded health center grantee, BHCMISID key)
  - Table3A             (patient demographics by health center, BHCMISID key)

Full workbook has 37 tables (clinical measures, workforce, HIT, financials, zip
codes served, etc) -- add more sheets here later if a specific join needs them;
these two are the identity + core-volume tables analogous to how HPSA was landed.

    python scripts/hrsa_uds_load.py          # preview (fetch + sample, no write)
    python scripts/hrsa_uds_load.py --run    # land it
"""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
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

URL = "https://data.hrsa.gov/DataDownload/StaticDocuments/H80-2025.xlsx"
HEADERS = {"User-Agent": "Mozilla/5.0"}

SHEETS = {
    "HealthCenterInfo": ("fed_hrsa_uds_health_center_info", "one row = one funded health center grantee"),
    "Table3A": ("fed_hrsa_uds_table3a_patients", "one row = one health center's patient demographics for the reporting year"),
}


def _register(conn, sid: str, table: str, rows: int, unit: str) -> None:
    cfg = {
        "source_id": sid,
        "name": f"HRSA UDS (Uniform Data System) -- {table}",
        "publisher": "Health Resources and Services Administration (HRSA)",
        "url": "https://data.hrsa.gov/topics/health-centers/uds",
        "description": "Annual HRSA Uniform Data System (UDS) health-center reporting workbook, "
                       f"sheet {table}. UDS is the OTHER half of HRSA data beyond HPSA shortage areas "
                       "(already landed as FED_HRSA_SHORTAGE_AREAS) -- this is what funded health "
                       "centers actually reported: patients served, demographics, funding.",
        "jurisdiction": "federal", "category": "Health", "subcategory": "Health Center Reporting",
        "unit_of_observation": unit,
        "geographic_scope": "US nationwide", "access_method": "bulk_download", "format": "xlsx (multi-sheet)",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "annual",
        "volume": f"{rows:,} rows", "license_terms": "U.S. Government work, public",
        "join_keys": "BHCMISID, GrantNumber",
        "accountability_relevance": "Federally-funded health centers -- who they actually serve, "
                                    "vs. where HPSA says need is highest.",
        "priority_tier": "2", "landing_table": table.upper(),
        "notes": "Loaded by scripts/hrsa_uds_load.py. FY2025 workbook (H80-2025.xlsx); rerun with the "
                "next year's file to refresh.",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for HRSA UDS health center data")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== HRSA UDS (Health Center Reporting) ===", flush=True)
    r = requests.get(URL, headers=HEADERS, timeout=180)
    r.raise_for_status()
    content = r.content
    sha = hashlib.sha256(content).hexdigest()
    print(f"downloaded H80-2025.xlsx: {len(content):,} bytes", flush=True)
    xl = pd.ExcelFile(io.BytesIO(content))

    dfs = {}
    for sheet in SHEETS:
        df = xl.parse(sheet)
        dfs[sheet] = df
        print(f"  {sheet}: {len(df):,} rows, {len(df.columns)} cols", flush=True)

    if not args.run:
        hc = dfs["HealthCenterInfo"]
        cols = [c for c in ["BHCMISID", "GrantNumber", "HealthCenterName", "HealthCenterState"] if c in hc.columns]
        print("\nSAMPLE HealthCenterInfo (first 5):")
        print(hc[cols].head(5).to_string() if cols else hc.head(5).to_string())
        print("\nPREVIEW only -- add --run to land.")
        return 0

    started = ingest._utcnow()
    conn = snow.connect()
    try:
        from snowflake.connector.pandas_tools import write_pandas
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        for sheet, (sid, unit) in SHEETS.items():
            df = dfs[sheet]
            table = sid.upper()
            run_id = str(uuid.uuid4())
            out = ingest._stringify(df)
            out.columns = [ingest._sf_col(c) for c in out.columns]
            out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
            out[ingest.META_SOURCE_RUN_ID] = run_id
            out[ingest.META_SRC_SHA256] = sha
            ok, _c, nrows, _ = write_pandas(conn, out, table_name=table,
                                            database=settings.raw_database, schema=settings.raw_schema,
                                            auto_create_table=True, overwrite=True, quote_identifiers=False)
            if not ok:
                raise RuntimeError(f"write_pandas failed for {table}")
            ended = ingest._utcnow()
            dens = ingest.assess_density(df)
            status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
            ingest._log_run(conn, sid, run_id, status, len(df), None, sha, URL, started, ended,
                            f"HRSA UDS FY2025 / {sheet} sheet; {len(df):,} rows; density {dens.get('populated_fraction')}")
            _register(conn, sid, table, len(df), unit)
            print(f"LOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{table} "
                  f"(status={status}); registered INCLUDE=Y", flush=True)

        n1 = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."FED_HRSA_UDS_HEALTH_CENTER_INFO"')
        dk1 = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT "BHCMISID") FROM "{settings.raw_database}"."{settings.raw_schema}"."FED_HRSA_UDS_HEALTH_CENTER_INFO"')
        n2 = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."FED_HRSA_UDS_TABLE3A_PATIENTS"')
        join_ok = snow.fetch_scalar(conn,
            f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."FED_HRSA_UDS_TABLE3A_PATIENTS" t '
            f'JOIN "{settings.raw_database}"."{settings.raw_schema}"."FED_HRSA_UDS_HEALTH_CENTER_INFO" h ON t."BHCMISID" = h."BHCMISID"')
        print(f"verify: HealthCenterInfo {n1:,} rows (DISTINCT BHCMISID={dk1:,}); Table3A {n2:,} rows; "
              f"Table3A->HealthCenterInfo join matches {join_ok:,}", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
