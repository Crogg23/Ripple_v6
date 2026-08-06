#!/usr/bin/env python3
"""Deterministic loader for JPML Pending Multidistrict Litigation (MDL) dockets.

Judicial Panel on Multidistrict Litigation publishes a monthly PDF report of every
active MDL: docket number, case caption, transferee judge, transferee district,
master docket number, date filed, date transferred/closed. One row = one MDL.
Small table (~160 rows), PDF-only source -> parsed with pdfplumber + regex.

Snapshot-replace (overwrite=True) -> idempotent; rerun never duplicates.

    python scripts/jpml_pending_mdl_load.py          # preview (fetch + sample, no write)
    python scripts/jpml_pending_mdl_load.py --run     # land it
"""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import uuid
from pathlib import Path

import pandas as pd
import pdfplumber
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

SID = "fed_jpml_pending_mdl"
TABLE = SID.upper()
URL = "https://www.jpml.uscourts.gov/sites/jpml/files/Pending_MDL_Dockets_By_MDL_Number-August-3-2026.pdf"
ROW_RE = re.compile(
    r"(\d{3,5})\s+(IN RE:.*?)\s+([A-Z][A-Za-z'\-]+,\s+[A-Za-z\.\s]+?)\s+"
    r"([A-Z]{2,3})\s+(\S+)\s+(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})"
)


def _fetch_df() -> pd.DataFrame:
    r = requests.get(URL, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    pdf = pdfplumber.open(io.BytesIO(r.content))
    full = " ".join((p.extract_text() or "").replace("\n", " ") for p in pdf.pages)
    rows = ROW_RE.findall(full)
    df = pd.DataFrame(rows, columns=[
        "MDL_NUMBER", "CASE_CAPTION", "TRANSFEREE_JUDGE", "TRANSFEREE_DISTRICT",
        "MASTER_DOCKET", "DATE_FILED", "DATE_TRANSFERRED",
    ])
    return df


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "JPML Pending Multidistrict Litigation (MDL) Dockets",
        "publisher": "Judicial Panel on Multidistrict Litigation (jpml.uscourts.gov)",
        "url": "https://www.jpml.uscourts.gov/pending-mdls-0",
        "description": "Every active multidistrict litigation docket: caption, transferee "
                       "judge/district, master docket number, dates filed/transferred. "
                       "Monthly PDF report, parsed with pdfplumber.",
        "jurisdiction": "federal", "category": "Justice", "subcategory": "Litigation",
        "unit_of_observation": "one row = one active MDL docket",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "pdf",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "monthly",
        "volume": f"{rows:,} rows", "license_terms": "U.S. Government work, public domain",
        "join_keys": "MDL_NUMBER, MASTER_DOCKET",
        "accountability_relevance": "Maps which companies/products are under active mass "
                                    "litigation and which judges/districts hold them.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/jpml_pending_mdl_load.py (PDF parse, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for JPML Pending MDLs")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== JPML Pending MDLs ===", flush=True)
    df = _fetch_df()
    print(f"{len(df):,} MDL dockets parsed, {len(df.columns)} cols", flush=True)

    if not args.run:
        print("\nSAMPLE (first 3):")
        for _, row in df.head(3).iterrows():
            print(f"  {row['MDL_NUMBER']} {row['CASE_CAPTION'][:60]} ({row['TRANSFEREE_DISTRICT']})")
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
        ingest._log_run(conn, SID, run_id, status, len(df), None, sha, URL, started, ended,
                        f"JPML pending MDLs; {len(df):,} rows; density {dens.get('populated_fraction')}")
        _register(conn, len(df))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        dk = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT MDL_NUMBER) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"verify: {n:,} rows in landing; {dk:,} distinct MDL_NUMBER", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
