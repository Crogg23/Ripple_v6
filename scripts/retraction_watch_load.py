#!/usr/bin/env python3
"""Deterministic loader for the Retraction Watch Database.

As of the RW/Crossref partnership, the full database is published as one CSV via
the Crossref Labs API (retractionwatch.com no longer hosts the raw download
directly). One flat CSV, no key required.

Snapshot-replace (overwrite=True) -> idempotent; rerun never duplicates.

    python scripts/retraction_watch_load.py          # preview (fetch + sample, no write)
    python scripts/retraction_watch_load.py --run     # land it
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

SID = "fed_retraction_watch"
TABLE = SID.upper()
URL = "http://api.labs.crossref.org/data/retractionwatch?jc"
RAW_CSV = _REPO / "library-onboarding" / "raw_downloads" / "retraction_watch.csv"


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "Retraction Watch Database",
        "publisher": "Retraction Watch / Crossref Labs",
        "url": "https://retractionwatch.com/retraction-watch-database-user-guide/",
        "description": "Every known retracted, corrected, or otherwise flagged scientific paper "
                       "tracked by Retraction Watch, distributed via the Crossref Labs API partnership.",
        "jurisdiction": "international", "category": "Science", "subcategory": "Research integrity",
        "unit_of_observation": "one row = one retracted/flagged paper record",
        "geographic_scope": "Global", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "rolling/daily",
        "volume": f"{rows:,} rows", "license_terms": "CC0 (Retraction Watch / Crossref Labs)",
        "join_keys": "RetractionDOI, OriginalPaperDOI, RetractionPubMedID, OriginalPaperPubMedID",
        "accountability_relevance": "Research misconduct radar: institutions/journals/authors with "
                                    "retracted or fraudulent published work.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/retraction_watch_load.py (LLM-free, single CSV via Crossref Labs API, "
                 "snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for Retraction Watch Database")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== Retraction Watch Database ===", flush=True)
    RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
    if not RAW_CSV.exists():
        with requests.get(URL, timeout=300, stream=True) as r:
            r.raise_for_status()
            with open(RAW_CSV, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
    df = pd.read_csv(RAW_CSV, dtype=str, keep_default_na=False)
    # drop the trailing unnamed/empty column the source CSV ships with
    df = df.loc[:, [c for c in df.columns if not c.startswith("Unnamed")]]
    print(f"{len(df):,} rows, {len(df.columns)} cols", flush=True)
    print(f"distinct Record ID: {df['Record ID'].nunique():,}", flush=True)

    if not args.run:
        print("\nSAMPLE (first 3):")
        for _, row in df.head(3).iterrows():
            print(f"  {row['Record ID']:>8}  {row['Journal'][:40]:40}  retracted {row['RetractionDate']}")
        dens = ingest.assess_density(df)
        print(f"\ndensity: {dens}")
        print("\nPREVIEW only — add --run to land.")
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
                        f"Retraction Watch DB; {len(df):,} rows; density {dens.get('populated_fraction')}")
        _register(conn, len(df))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        if status != "success":
            raise RuntimeError(f"QUALITY GATE FAILED for {TABLE}: {dens}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
