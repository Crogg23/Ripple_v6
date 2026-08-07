#!/usr/bin/env python3
"""Loader for the National Inventory of Dams (NID), USACE.

One flat CSV export off the public NID API (nid.sec.usace.army.mil), no key.
Snapshot-replace (overwrite=True) -> idempotent; rerun never duplicates.

    python scripts/nid_dams_load.py          # preview (fetch + sample, no write)
    python scripts/nid_dams_load.py --run     # land it
"""
from __future__ import annotations

import argparse
import hashlib
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

SID = "fed_nid_dams"
TABLE = SID.upper()
URL = "https://nid.sec.usace.army.mil/api/nation/csv"


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "National Inventory of Dams (NID)",
        "publisher": "U.S. Army Corps of Engineers",
        "url": "https://nid.sec.usace.army.mil/",
        "description": "Federal inventory of dams meeting NID criteria (height/storage/hazard "
                       "thresholds), including hazard-potential classification, condition assessment, "
                       "owner, and location for each dam nationwide.",
        "jurisdiction": "federal", "category": "Infrastructure", "subcategory": "Dams",
        "unit_of_observation": "one row = one dam",
        "geographic_scope": "US nationwide", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "periodic (USACE-maintained)",
        "volume": f"{rows:,} rows", "license_terms": "U.S. Government work, public",
        "join_keys": "NIDID, dam name + state/county, lat/long",
        "accountability_relevance": "Dam hazard-potential + condition assessment vs. who lives "
                                    "downstream -- infrastructure-harm mapping.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/nid_dams_load.py (LLM-free, single CSV, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for National Inventory of Dams")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== National Inventory of Dams ===", flush=True)
    r = requests.get(URL, timeout=180, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    content = r.content
    # Row 0 is a "Data Last Updated:,<date>" banner, not the header -- skip it.
    df = pd.read_csv(pd.io.common.BytesIO(content), dtype=str, low_memory=False,
                      encoding_errors="replace", skiprows=1)
    print(f"fetched {len(df):,} rows, {len(df.columns)} cols", flush=True)

    if not args.run:
        print("\nSAMPLE (first 3 rows, first 8 cols):")
        print(df.iloc[:3, :8].to_string())
        dens = ingest.assess_density(df)
        print(f"\ndensity: {dens}")
        print("\nPREVIEW only -- add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    sha = hashlib.sha256(content).hexdigest()
    conn = snow.connect()
    try:
        if settings.skip_if_unchanged:
            last_sha = ingest._latest_success_sha(conn, SID)
            if last_sha == sha:
                print(f"\nskip (sha unchanged) -- sha {sha[:12]} matches last successful run.",
                      flush=True)
                return 0
        from snowflake.connector.pandas_tools import write_pandas
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        df.columns = [ingest._sf_col(c) for c in df.columns]
        out = df.copy()
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
                        f"NID nationwide dam inventory; {len(df):,} rows; density {dens.get('populated_fraction')}")
        _register(conn, len(df))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        if status != "success":
            raise RuntimeError(f"QUALITY GATE FAILED for {TABLE}: {dens}")
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        dk = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT "NID_ID") FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"verify: {n:,} rows landed; DISTINCT NID_ID = {dk:,}", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
