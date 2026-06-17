#!/usr/bin/env python3
"""Unattended live batch -- grow the Library through the FULL agent.

Runs the real 5-checkpoint flow for each source: **Claude does recon and writes
the ingestion script**, the script runs and lands to LIBRARY_RAW, Claude generates
dbt models, and the source is registered. Unattended:

    ONBOARD_AUTO_APPROVE=1   every checkpoint auto-"go"s
    ONBOARD_AUTO_REPAIR=3    on a stage error, feed it back to Claude and retry

This is the canonical growing queue: each source pins its own ``source_id`` and the
runner **skips any source already landed** (a success row in INGEST_RUNS), so it's
safe to re-run -- it only onboards what's missing.

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
# Claude's codegen gets a real workout. Pinned source_ids avoid colliding with
# (overwriting) the broader family rows already in SOURCE_REGISTRY.
SOURCES = [
    # --- batch 1 (landed 2026-06-16) ----------------------------------------
    {"name": "SEC EDGAR Company Tickers", "source_id": "fed_sec_edgar_company_tickers",
     "url": "https://www.sec.gov/files/company_tickers.json",
     "jurisdiction": "federal", "layer": "us_federal", "identifiers": ["CIK", "ticker"]},
    {"name": "FDIC Failed Banks", "source_id": "fed_fdic_failed_banks",
     "url": "https://banks.data.fdic.gov/api/failures?limit=10000&format=json",
     "jurisdiction": "federal", "layer": "us_federal", "identifiers": ["FDIC_cert", "FIPS"]},
    {"name": "Federal Register Documents", "source_id": "fed_federal_register_documents",
     "url": "https://www.federalregister.gov/api/v1/documents.json?per_page=100&order=newest",
     "jurisdiction": "federal", "layer": "us_federal", "identifiers": ["document_number", "agency"]},

    # --- batch 2 ------------------------------------------------------------
    {"name": "Treasury Debt to the Penny", "source_id": "fed_treasury_debt_to_penny",
     "url": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?page[size]=500&sort=-record_date",
     "jurisdiction": "federal", "layer": "us_federal", "identifiers": ["record_date"]},
    {"name": "FDA Drug Enforcement Reports (Recalls)", "source_id": "fed_fda_drug_enforcement",
     "url": "https://api.fda.gov/drug/enforcement.json?limit=500",
     "jurisdiction": "federal", "layer": "us_federal", "identifiers": ["recall_number", "NDC", "event_id"]},

    # --- batch 3 (2026-06-17) -----------------------------------------------
    # Average interest rate the Treasury pays by security type -- the price tag on
    # the national debt. Same Fiscal Data API family as debt_to_penny (proven), so
    # codegen risk is low. Small + bounded (~4,961 monthly rows since FY2001).
    {"name": "Treasury Average Interest Rates", "source_id": "fed_treasury_avg_interest_rates",
     "url": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?page[size]=10000&sort=-record_date",
     "jurisdiction": "federal", "layer": "us_federal", "identifiers": ["record_date", "security_type_desc", "security_desc"]},
    # PARKED -- huge / effectively unbounded search APIs (millions of rows, grow
    # daily). A snapshot-replace mirror is the wrong shape; these want an
    # incremental load. Re-add once the agent supports bounded/incremental fetch:
    #   CFPB Consumer Complaints  https://www.consumerfinance.gov/.../search/api/v1/
    #   ProPublica Nonprofits     https://projects.propublica.org/nonprofits/api/v2/search.json
]


def _already_onboarded() -> set:
    """SOURCE_IDs that already have a successful ingest run -- skip these."""
    try:
        import snow
        conn = snow.connect()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT DISTINCT SOURCE_ID FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS WHERE STATUS='success'"
            )
            return {row[0] for row in cur.fetchall()}
        finally:
            conn.close()
    except Exception as exc:  # no creds / offline -> attempt everything
        cp.warn(f"Could not read existing runs ({exc}); will attempt all sources.")
        return set()


def main() -> int:
    done = _already_onboarded()
    todo = [s for s in SOURCES if s["source_id"] not in done]
    skipped = [s for s in SOURCES if s["source_id"] in done]
    for s in skipped:
        cp.info(f"already landed — skipping {s['source_id']}")

    total = len(todo)
    cp.info(f"Live batch: {total} new sources through the full agent (auto-approve + auto-repair).")
    results = []
    for i, source in enumerate(todo, 1):
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
    complete = sum(1 for _, r in results if r.get("status") == "complete")
    cp.info(f"\n{complete}/{total} complete ({len(skipped)} already landed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
