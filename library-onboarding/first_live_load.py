#!/usr/bin/env python3
"""First live load -- prove the onboarding agent's write path end to end.

This is a one-off (re-runnable) bootstrap that drives the agent's *real* LOAD and
REGISTRY code against a small, reliable, no-auth federal source:

    USAspending.gov -- Top-tier federal agencies
    https://api.usaspending.gov/api/v2/references/toptier_agencies/
    one row = one top-tier federal agency (current fiscal year)

It deliberately does NOT call Claude for recon/codegen -- the config and the
``fetch_data`` below are hand-built so the first live write is deterministic.
It DOES exercise the agent's actual machinery:

    run_ingest()      -> LIBRARY_RAW.LANDING.FED_USASPENDING_TOPTIER_AGENCIES
                         + one row in LIBRARY_META.INGEST_LOGS.INGEST_RUNS
    register_source() -> upsert into LIBRARY_META.REGISTRY.SOURCE_REGISTRY
                         (with best-effort live Claude catalog enrichment)

DBT (checkpoint 4) is intentionally skipped -- DBT_PROJECT_PATH isn't wired yet.

    python first_live_load.py
"""

from __future__ import annotations

import json
import os

# RIPPLE_WH is the documented Ripple compute warehouse. Set it before the config
# module reads the environment, so this runs even if the env var is missing OR
# present-but-blank (setdefault won't override an existing empty string).
if not os.environ.get("SNOWFLAKE_WAREHOUSE", "").strip():
    os.environ["SNOWFLAKE_WAREHOUSE"] = "RIPPLE_WH"

import naming  # noqa: E402
from ingest import run_ingest  # noqa: E402
from register import register_source  # noqa: E402

URL = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
JURISDICTION = "federal"
SOURCE_ID = naming.source_id("fed_usaspending_toptier_agencies", JURISDICTION)
ENTITY = "agencies"

# The ingestion script -- exactly what Checkpoint 2 would hand to Checkpoint 3,
# run through the same exec() path the agent uses for model-generated code.
INGEST_CODE = '''
import requests
import pandas as pd


def fetch_data(context):
    """Pull every top-tier federal agency from the USAspending reference API."""
    resp = requests.get(
        context["url"],
        headers={"User-Agent": "RippleOnboardingAgent/1.0 (+https://github.com/Crogg23/Ripple_v6)"},
        timeout=60,
    )
    resp.raise_for_status()
    context["source_bytes"] = resp.content          # raw bytes -> SHA-256 content hash
    context["source_file"] = "toptier_agencies.json"
    results = resp.json().get("results", [])
    return pd.DataFrame(results)
'''

CONFIG = {
    # --- identity -------------------------------------------------------
    "name": "USAspending Top-Tier Federal Agencies",
    "url": URL,
    "layer": "us_federal",
    "source_id": SOURCE_ID,
    "landing_table": naming.landing_table(SOURCE_ID),
    "entity": ENTITY,
    # --- registry profile ----------------------------------------------
    "jurisdiction": JURISDICTION,
    "category": "Government Finance",
    "subcategory": "Federal agency budget & spending",
    "publisher": "U.S. Department of the Treasury (USAspending.gov)",
    "description": (
        "Top-tier federal agencies with current fiscal-year budgetary resources, "
        "obligations, and outlays from the USAspending.gov reference API."
    ),
    "unit_of_observation": "one row = one top-tier federal agency (current fiscal year)",
    "temporal_coverage": "current fiscal year snapshot",
    "geographic_scope": "United States (federal)",
    "access_method": "REST API",
    "access_pattern": "rest_api",
    "format": "JSON",
    "auth": {"type": "none", "notes": "no API key required"},
    "cost": "free",
    "update_cadence": "daily",
    "volume": "~111 agencies",
    "license_terms": "U.S. Government public domain (USAspending.gov open data)",
    "key_identifiers": ["toptier_code", "agency_id"],
    "join_keys": "toptier_code, agency_id",
    "accountability_relevance": (
        "Agency-level budget authority, obligations, and outlays -- the spine of "
        "follow-the-money analysis across the federal government."
    ),
    "priority_tier": "2",
    # --- dbt naming (unused here; kept for parity with recon output) ----
    "staging_model": naming.staging_model(SOURCE_ID, ENTITY),
    "mart_model": naming.mart_model("gov", SOURCE_ID),
    "schema_fields": [],
    "notes": "First live load through the onboarding agent.",
}


def _banner(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> int:
    print(f"Source     : {CONFIG['name']}")
    print(f"SOURCE_ID  : {CONFIG['source_id']}")
    print(f"Landing    : LIBRARY_RAW.LANDING.{CONFIG['landing_table']}")
    print(f"URL        : {CONFIG['url']}")

    _banner("CHECKPOINT 3 -- LOAD")
    load = run_ingest(CONFIG, INGEST_CODE)
    print(f"status   : {load.get('status')}")
    print(f"run_id   : {load.get('run_id')}")
    print(f"rows     : {load.get('rows')}")
    print(f"sha256   : {load.get('sha256', '')[:16]}...")
    print(f"columns  : {load.get('columns')}")
    if load.get("sample_rows"):
        print("sample   :")
        print(json.dumps(load["sample_rows"][:2], indent=2, default=str))

    _banner("CHECKPOINT 5 -- REGISTRY")
    reg = register_source(CONFIG)
    print(f"status   : {reg.get('status')}")
    print(f"fqn      : {reg.get('fqn')}")
    print(f"join_keys: {reg.get('join_keys')}")

    _banner("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
