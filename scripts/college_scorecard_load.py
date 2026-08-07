#!/usr/bin/env python3
"""Loader for U.S. Dept of Education College Scorecard -- institution-level file.

Bulk download (no API key needed) off collegescorecard.ed.gov/data -- the
"Most Recent Cohorts (Institution)" CSV, one row per institution per year of
data collected, ~3,300 columns (cost, debt, earnings, completion by cohort).
The download URL is date-stamped by ED and changes periodically; this loader
resolves it live off the data page rather than hardcoding a stale link.

    python scripts/college_scorecard_load.py          # preview (fetch + sample, no write)
    python scripts/college_scorecard_load.py --run    # land it
"""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import uuid
import zipfile
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

SID = "fed_college_scorecard_institution"
TABLE = SID.upper()
DATA_PAGE = "https://collegescorecard.ed.gov/data/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _resolve_zip_url() -> str:
    r = requests.get(DATA_PAGE, timeout=30, headers=HEADERS)
    r.raise_for_status()
    links = re.findall(r'href="([^"]*Most-Recent-Cohorts-Institution[^"]*\.zip)"', r.text, re.I)
    if not links:
        raise RuntimeError("could not find Most-Recent-Cohorts-Institution zip link on data page")
    return links[0]


def _register(conn, rows: int, cols: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "College Scorecard -- Institution-level file (Most Recent Cohorts)",
        "publisher": "U.S. Department of Education",
        "url": "https://collegescorecard.ed.gov/data/",
        "description": "Institution-level higher-ed outcomes: cost, student debt, loan repayment, "
                       f"earnings after enrollment, and completion, one row per institution ({cols:,} cols "
                       "spanning many cohort-years). No API key required (bulk CSV).",
        "jurisdiction": "federal", "category": "Education", "subcategory": "Higher Education Outcomes",
        "unit_of_observation": "one row = one institution (UNITID)",
        "geographic_scope": "US nationwide", "access_method": "bulk_download", "format": "csv (zipped)",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "annual (ED-maintained)",
        "volume": f"{rows:,} rows x {cols:,} cols", "license_terms": "U.S. Government work, public",
        "join_keys": "UNITID, OPEID, OPEID6",
        "accountability_relevance": "Which schools leave students with debt and no earnings bump -- "
                                    "predatory-education mapping.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/college_scorecard_load.py (LLM-free, bulk zip CSV, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for College Scorecard institution file")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== College Scorecard (Institution) ===", flush=True)
    zip_url = _resolve_zip_url()
    print(f"resolved: {zip_url}", flush=True)
    r = requests.get(zip_url, timeout=180, headers=HEADERS)
    r.raise_for_status()
    content = r.content
    sha = hashlib.sha256(content).hexdigest()
    z = zipfile.ZipFile(io.BytesIO(content))
    csv_name = next(n for n in z.namelist() if n.lower().endswith(".csv") and "macosx" not in n.lower())
    with z.open(csv_name) as f:
        df = pd.read_csv(f, dtype=str, low_memory=False, encoding_errors="replace")
    print(f"fetched {len(df):,} rows, {len(df.columns):,} cols from {csv_name}", flush=True)

    if not args.run:
        cols = [c for c in ["UNITID", "OPEID", "INSTNM", "STABBR"] if c in df.columns]
        print("\nSAMPLE (first 5):")
        print(df[cols].head(5).to_string() if cols else df.iloc[:5, :6].to_string())
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
        out = df.copy()
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
        ingest._log_run(conn, SID, run_id, status, len(df), None, sha, zip_url, started, ended,
                        f"College Scorecard institution file; {len(df):,} rows x {len(df.columns):,} cols; "
                        f"density {dens.get('populated_fraction')}")
        _register(conn, len(df), len(df.columns))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        if status != "success":
            raise RuntimeError(f"QUALITY GATE FAILED for {TABLE}: {dens}")
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        dk = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT "UNITID") FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"verify: {n:,} rows landed; DISTINCT UNITID = {dk:,}", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
