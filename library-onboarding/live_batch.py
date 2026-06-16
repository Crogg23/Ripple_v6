#!/usr/bin/env python3
"""Unattended live batch -- onboard several real sources through the FULL agent.

Unlike ``first_live_load.py`` (deterministic, hand-built), this runs the real
5-checkpoint flow for each source: **Claude does recon and writes the ingestion
script**, the script runs and lands to RIPPLE_RAW, Claude generates dbt models,
and the source is registered. It runs unattended:

    ONBOARD_AUTO_APPROVE=1   every checkpoint auto-"go"s
    ONBOARD_AUTO_REPAIR=3    on a stage error, feed it back to Claude and retry

Each source pins its own ``source_id`` so we land a specific slice without
colliding with the broader family rows already in SOURCE_REGISTRY.

    python live_batch.py
"""

from __future__ import annotations

import os

# --- environment: unattended, live, with the scaffolded dbt project ---------
os.environ["ONBOARD_AUTO_APPROVE"] = "1"
os.environ.setdefault("ONBOARD_AUTO_REPAIR", "3")
if not os.environ.get("SNOWFLAKE_WAREHOUSE", "").strip():
    os.environ["SNOWFLAKE_WAREHOUSE"] = "RIPPLE_WH"
if not os.environ.get("DBT_PROJECT_PATH", "").strip():
    os.environ["DBT_PROJECT_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ripple_dbt")

import checkpoint as cp  # noqa: E402
from onboard import onboard_source  # noqa: E402

# Small, reliable, no-auth federal sources -- varied JSON shapes on purpose, so
# Claude's codegen gets a real workout. Pinned source_ids are all NEW (distinct
# from the curated fed_sec_edgar / fed_fdic_bank_data / fed_federal_register rows).
SOURCES = [
    {
        "name": "SEC EDGAR Company Tickers",
        "source_id": "fed_sec_edgar_company_tickers",
        "url": "https://www.sec.gov/files/company_tickers.json",
        "jurisdiction": "federal",
        "layer": "us_federal",
        "identifiers": ["CIK", "ticker"],
    },
    {
        "name": "FDIC Failed Banks",
        "source_id": "fed_fdic_failed_banks",
        "url": "https://banks.data.fdic.gov/api/failures?limit=10000&format=json",
        "jurisdiction": "federal",
        "layer": "us_federal",
        "identifiers": ["FDIC_cert", "FIPS"],
    },
    {
        "name": "Federal Register Documents",
        "source_id": "fed_federal_register_documents",
        "url": "https://www.federalregister.gov/api/v1/documents.json?per_page=100&order=newest",
        "jurisdiction": "federal",
        "layer": "us_federal",
        "identifiers": ["document_number", "agency"],
    },
]


def main() -> int:
    total = len(SOURCES)
    cp.info(f"Live batch: {total} sources through the full agent (auto-approve + auto-repair).")
    results = []
    for i, source in enumerate(SOURCES, 1):
        record = onboard_source(source, position=(i, total))
        results.append((source["name"], record))

    cp.info("\n" + "=" * 60)
    cp.info("LIVE BATCH SUMMARY")
    cp.info("=" * 60)
    for name, rec in results:
        status = rec.get("status", "?")
        sid = rec.get("source_id", "")
        table = rec.get("landing_table", "")
        run_id = rec.get("run_id", "")
        line = f"  {status:<9} {name}"
        if sid:
            line += f"  -> {sid} ({table})"
        if run_id:
            line += f"  run={run_id[:8]}"
        cp.info(line)
    done = sum(1 for _, r in results if r.get("status") == "complete")
    cp.info(f"\n{done}/{total} complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
