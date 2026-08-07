#!/usr/bin/env python3
"""Deterministic loader for the IRS FATCA Foreign Financial Institution (FFI) List.

Published monthly by IRS at apps.irs.gov/app/fatcaFfiList. Each row = one FFI that
has registered for FATCA with a Global Intermediary Identification Number (GIIN) --
the entity-spine join key. Small, flat, no key required.

Snapshot-replace (overwrite=True) -> idempotent; rerun never duplicates.

    python scripts/fatca_ffi_load.py          # preview (fetch + sample, no write)
    python scripts/fatca_ffi_load.py --run     # land it
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

SID = "fed_fatca_ffi"
TABLE = SID.upper()
URL = "https://apps.irs.gov/app/fatcaFfiList/data/FFIListFull.csv"


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "FATCA Foreign Financial Institution (FFI) List",
        "publisher": "Internal Revenue Service (IRS)",
        "url": "https://apps.irs.gov/app/fatcaFfiList/",
        "description": "Every foreign financial institution registered with IRS under FATCA, "
                       "with its Global Intermediary Identification Number (GIIN) -- the "
                       "identifier used to report US-person accounts held abroad. Entity-spine "
                       "join fuel: name + country + GIIN for foreign banks/funds/trusts.",
        "jurisdiction": "federal", "category": "Finance", "subcategory": "Financial Institutions",
        "unit_of_observation": "one row = one FATCA-registered foreign financial institution (GIIN)",
        "geographic_scope": "Global (non-US financial institutions)", "access_method": "bulk_download",
        "format": "csv", "auth": {"type": "none"}, "cost": "free", "update_cadence": "monthly",
        "volume": f"{rows:,} rows", "license_terms": "US Gov work, public",
        "join_keys": "GIIN, entity name, country",
        "accountability_relevance": "Entity spine block (Phase 5): foreign financial institutions "
                                    "self-registered with the US -- cross-reference against sanctions "
                                    "and offshore-leaks entity names.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/fatca_ffi_load.py (LLM-free, single monthly CSV, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for IRS FATCA FFI List")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== FATCA FFI List ===", flush=True)
    r = requests.get(URL, timeout=180)
    r.raise_for_status()
    from io import StringIO
    df = pd.read_csv(StringIO(r.text), dtype=str)
    df.columns = ["GIIN", "FI_NAME", "COUNTRY_NAME"]
    print(f"{len(df):,} rows, {len(df.columns)} cols; distinct GIIN={df['GIIN'].nunique():,}", flush=True)

    if not args.run:
        print("\nSAMPLE (first 5):")
        print(df.head(5).to_string())
        dens = ingest.assess_density(df)
        print(f"\ndensity: {dens}")
        print("\nPREVIEW only -- add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    sha = hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()
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
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha
        out.columns = [ingest._sf_col(c) for c in out.columns]
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
                        f"FATCA FFI list; {len(df):,} rows; density {dens.get('populated_fraction')}")
        _register(conn, len(df))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        if status != "success":
            raise RuntimeError(f"QUALITY GATE FAILED for {TABLE}: {dens}")
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        d = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT GIIN) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"verify: {n:,} rows in landing; {d:,} distinct GIIN", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
