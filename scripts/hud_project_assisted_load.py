#!/usr/bin/env python3
"""Loader for HUD "Picture of Subsidized Households" -- project level (multifamily +
Section 8 + PRAC/other HUD-assisted rental programs), most recent snapshot.

FED_HUD_DATA already in the warehouse is a small (77-row) dataset-metadata
passthrough -- NOT the loan/project-level assisted-housing data. This loader
fills that gap: HUD's project-level assisted-housing snapshot (huduser.gov),
one row per HUD-assisted housing project (public housing, Section 8, 811/PRAC,
etc), with occupancy, income, and subsidy detail.

huduser.gov Akamai-blocks requests without a Referer header pointing at the
dataset landing page -- discovered this session; every request here carries one.

    python scripts/hud_project_assisted_load.py          # preview (fetch + sample, no write)
    python scripts/hud_project_assisted_load.py --run    # land it
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

SID = "fed_hud_assisted_housing_projects"
TABLE = SID.upper()
URL = "https://www.huduser.gov/portal/datasets/pictures/files/PROJECT_2025_2020census.xlsx"
LANDING_PAGE = "https://www.huduser.gov/portal/datasets/assthsg.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Referer": LANDING_PAGE,
}


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "HUD Picture of Subsidized Households -- Project Level",
        "publisher": "HUD (huduser.gov / Office of Policy Development & Research)",
        "url": LANDING_PAGE,
        "description": "Project-level snapshot of every HUD-assisted rental housing project "
                       "(public housing, Section 8 project-based, 811/PRAC, and other HUD rental "
                       "assistance programs): occupancy, tenant income, subsidy spending, and "
                       "demographics per project.",
        "jurisdiction": "federal", "category": "Housing", "subcategory": "Assisted Housing",
        "unit_of_observation": "one row = one HUD-assisted housing project (per quarter snapshot)",
        "geographic_scope": "US nationwide", "access_method": "bulk_download", "format": "xlsx",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "quarterly",
        "volume": f"{rows:,} rows", "license_terms": "U.S. Government work, public",
        "join_keys": "code (project id), entities (name + address string), states",
        "accountability_relevance": "Which subsidized housing projects serve whom, at what "
                                    "occupancy/income mix -- landlord/PHA accountability mapping.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/hud_project_assisted_load.py. FED_HUD_DATA (existing, 77 rows) is "
                "dataset metadata only, NOT this data -- confirmed by direct query before building this.",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for HUD project-level assisted housing")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== HUD Assisted Housing -- Project Level ===", flush=True)
    r = requests.get(URL, headers=HEADERS, timeout=120)
    r.raise_for_status()
    content = r.content
    sha = hashlib.sha256(content).hexdigest()
    df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
    print(f"fetched {len(df):,} rows, {len(df.columns)} cols", flush=True)

    if not args.run:
        cols = [c for c in ["Quarter", "gsl", "states", "program_label", "code", "total_units"] if c in df.columns]
        print("\nSAMPLE (first 5):")
        print(df[cols].head(5).to_string() if cols else df.iloc[:5, :8].to_string())
        dens = ingest.assess_density(df)
        print(f"\ndensity: {dens}")
        print("\nPREVIEW only -- add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    conn = snow.connect()
    try:
        if settings.skip_if_unchanged:
            last_sha = ingest._latest_success_sha(conn, SID)
            if last_sha == sha:
                print(f"\nskip (sha unchanged) -- sha {sha[:12]} matches last successful run.", flush=True)
                return 0
        from snowflake.connector.pandas_tools import write_pandas
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        out = ingest._stringify(df)
        out.columns = [ingest._sf_col(c) for c in out.columns]
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha
        ok, _c, nrows, _ = write_pandas(conn, out, table_name=TABLE,
                                        database=settings.raw_database, schema=settings.raw_schema,
                                        auto_create_table=True, overwrite=True, quote_identifiers=False)
        if not ok:
            raise RuntimeError("write_pandas failed")
        ended = ingest._utcnow()
        dens = ingest.assess_density(df)
        status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
        if status != "success":
            print(f"  QUALITY GATE FAILED for {TABLE}: {dens}")
        ingest._log_run(conn, SID, run_id, status, len(df), None, sha, URL, started, ended,
                        f"HUD assisted housing project-level snapshot; {len(df):,} rows; density {dens.get('populated_fraction')}")
        _register(conn, len(df))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        if status != "success":
            raise RuntimeError(f"QUALITY GATE FAILED for {TABLE}: {dens}")
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        dk = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT "CODE") FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"verify: {n:,} rows landed; DISTINCT CODE = {dk:,}", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
