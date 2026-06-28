#!/usr/bin/env python3
"""Deterministic loader for the SlaveVoyages Intra-American Slave Trade Database.

Re-scout of the dead-scrape source `fed_slavevoyages_intraamerican` (finding #72).
The previous landing table held 201 rows of HTML page chrome (<html>, <head>, ...),
NOT data. The real machine-readable source is a single flat CSV the project ships
on its API host:

    https://api.slavevoyages.org/static/uploads/I-Am1.0.csv   (~5.7 MB)

Each row = one documented intra-American (Americas-to-Americas) slaving voyage:
voyage id, year, ship/rig, captain(s), embarkation/arrival ports & regions, the
number of captives embarked/disembarked, voyage fate, dates, and source citation.
11,521 voyages, 169 variables. The file carries non-UTF-8 bytes (Latin-1 place
names like "San Jose de la Vega"), so we decode latin-1.

Snapshot-replace (overwrite=True) -> idempotent; rerun never duplicates.

    python scripts/slavevoyages_intraamerican_load.py          # preview (fetch + sample, no write)
    python scripts/slavevoyages_intraamerican_load.py --run     # land it
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

SID = "fed_slavevoyages_intraamerican"
TABLE = SID.upper()
URL = "https://api.slavevoyages.org/static/uploads/I-Am1.0.csv"


def _fetch() -> pd.DataFrame:
    """Fetch the CSV and parse every column as TEXT (raw mirror)."""
    r = requests.get(URL, timeout=180)
    r.raise_for_status()
    df = pd.read_csv(
        io.BytesIO(r.content),
        dtype=str,
        keep_default_na=False,
        low_memory=False,
        encoding="latin-1",
    )
    # normalize column names to UPPER snake (write_pandas-safe), keep all 169
    df.columns = [ingest._sf_col(str(c)) for c in df.columns]
    return df


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "SlaveVoyages — Intra-American Slave Trade Database",
        "publisher": "SlaveVoyages (Emory University / Hutchins Center, Harvard)",
        "url": "https://www.slavevoyages.org/voyage/intra-american",
        "description": "Voyage-level database of the intra-American (Americas-to-Americas) slave "
                       "trade, ~1550-1888. One row = one documented slaving voyage with ship, "
                       "captain(s), embarkation/arrival ports and regions, captives embarked and "
                       "disembarked, voyage fate, dates, and source citation. "
                       f"{rows:,} voyages, 169 variables (dataset I-Am 1.0).",
        "jurisdiction": "federal", "category": "History", "subcategory": "Slave Trade",
        "unit_of_observation": "one row = one intra-American slaving voyage",
        "geographic_scope": "Americas", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "irregular (dataset releases)",
        "volume": f"{rows:,} rows", "license_terms": "Open / academic use — cite SlaveVoyages.org",
        "join_keys": "VOYAGEID (SlaveVoyages voyage id)",
        "accountability_relevance": "Primary-source record of the intra-American slave trade; "
                                    "foundational reparations / historical-accountability data. "
                                    "Re-scout of dead-scrape finding #72.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/slavevoyages_intraamerican_load.py (LLM-free, single flat CSV "
                 "from api.slavevoyages.org/static/uploads/I-Am1.0.csv, latin-1, snapshot-replace). "
                 "Replaces a prior load that captured HTML page chrome instead of data.",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for SlaveVoyages Intra-American")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== SlaveVoyages Intra-American ===", flush=True)
    df = _fetch()
    print(f"{len(df):,} voyages, {len(df.columns)} cols", flush=True)

    if not args.run:
        print("\nSAMPLE (first 4):")
        cols = [c for c in ["VOYAGEID", "YEARAM", "SHIPNAME", "CAPTAINA", "ARRPORT"] if c in df.columns]
        for _, row in df[cols].head(4).iterrows():
            print("   " + " | ".join(f"{c}={row[c]!s}" for c in cols))
        for c in ["VOYAGEID", "YEARAM", "SHIPNAME", "CAPTAINA"]:
            if c in df.columns:
                nd = df[c].replace("", pd.NA).nunique(dropna=True)
                print(f"   distinct {c}: {nd:,}")
        dens = ingest.assess_density(df)
        print(f"\ndensity: {dens}")
        print("\nPREVIEW only — add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    sha = hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()
    conn = snow.connect()
    try:
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
        ingest._log_run(conn, SID, run_id, status, len(df), None, sha, URL, started, ended,
                        f"SlaveVoyages Intra-American I-Am 1.0; {len(df):,} voyages; "
                        f"density {dens.get('populated_fraction')}")
        _register(conn, len(df))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        # show what landed
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        nd = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT VOYAGEID) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"verify: {n:,} rows in landing; {nd:,} distinct VOYAGEID", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
