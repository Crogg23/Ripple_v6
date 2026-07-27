"""Bulk-load EPA ECHO facility and compliance datasets.

Known-manifest loader: EPA ECHO publishes program-specific ZIPs at stable URLs
(echo.epa.gov/files/echodownloads/). Each ZIP contains multiple CSVs. We unzip
in-memory, check headers for entity keys (REGISTRY_ID/FRS_ID/EIN), and load
matching tables in parallel.

    python scripts/epa_echo_bulk_load.py              # preview
    python scripts/epa_echo_bulk_load.py --run        # load all
    python scripts/epa_echo_bulk_load.py --run --limit 3  # first 3 ZIPs only
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

TABLE_PREFIX = "FED_EPA"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# Entity keys that connect EPA data to the graph
ENTITY_KEYS = {
    "REGISTRY_ID", "FRS_ID", "FAC_EIN", "EIN", "NPDES_ID", "RCRA_ID",
    "HANDLER_ID", "TRI_FACILITY_ID", "GHGRP_ID", "PWSID", "PGM_SYS_ID",
    "FAC_FIPS_CODE", "FAC_ZIP", "FACILITY_UIN", "FAC_DUNS",
}

# Known ECHO download ZIPs -- actual URLs verified from echo.epa.gov/tools/data-downloads
# Updated weekly as part of the ECHO data refresh. URLs are case-sensitive.
ECHO_MANIFEST = [
    {
        "name": "ECHO_EXPORTER",
        "url": "https://echo.epa.gov/files/echodownloads/echo_exporter.zip",
        "description": "1.5M regulated facilities master file (all programs, 392 MB)",
    },
    {
        "name": "FRS",
        "url": "https://echo.epa.gov/files/echodownloads/frs_downloads.zip",
        "description": "Facility Registry Service -- FRS IDs + program linkages (318 MB)",
    },
    {
        "name": "ICIS_AIR",
        "url": "https://echo.epa.gov/files/echodownloads/ICIS-AIR_downloads.zip",
        "description": "Clean Air Act stationary sources -- ICIS-Air (64 MB)",
    },
    {
        "name": "AIR_EMISSIONS",
        "url": "https://echo.epa.gov/files/echodownloads/POLL_RPT_COMBINED_EMISSIONS.zip",
        "description": "Combined air emissions: NEI + GHGRP + TRI + CAM (150 MB)",
    },
    {
        "name": "NPDES",
        "url": "https://echo.epa.gov/files/echodownloads/npdes_downloads.zip",
        "description": "NPDES water discharge permits -- Part 1 (301 MB)",
    },
    {
        "name": "RCRA",
        "url": "https://echo.epa.gov/files/echodownloads/rcra_downloads.zip",
        "description": "Hazardous waste handlers -- RCRAInfo (103 MB)",
    },
    {
        "name": "ICIS_FEC",
        "url": "https://echo.epa.gov/files/echodownloads/case_downloads.zip",
        "description": "Federal enforcement & compliance cases (73 MB)",
    },
    {
        "name": "SDWA",
        "url": "https://echo.epa.gov/files/echodownloads/SDWA_latest_downloads.zip",
        "description": "Safe Drinking Water Act -- SDWIS data (457 MB)",
    },
]


def main() -> int:
    ap = argparse.ArgumentParser(description="EPA ECHO bulk loader")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--limit", type=int, default=len(ECHO_MANIFEST))
    ap.add_argument("--max-rows", type=int, default=500000)
    args = ap.parse_args()

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING")

    # Determine which ZIPs to process (skip if we already have tables with that prefix)
    to_load = []
    for entry in ECHO_MANIFEST[:args.limit]:
        prefix = f"{TABLE_PREFIX}_{entry['name']}"
        existing = [t for t in loaded if t.startswith(prefix)]
        if existing:
            print(f"  SKIP {entry['name']} ({len(existing)} tables already loaded)")
        else:
            to_load.append(entry)

    print(f"\n{len(to_load)} ZIP packages to process")

    if not args.run:
        print("\n(preview only -- add --run to load)")
        for i, e in enumerate(to_load, 1):
            print(f"  {i}. {e['name']:20s} — {e['description']}")
        return 0

    # Process ZIPs (parallel across ZIPs, sequential within each ZIP)
    print(f"\nLoading {len(to_load)} ZIP packages (parallel, {min(4, len(to_load))} workers)...")
    total_tables = 0
    total_rows = 0

    tasks = []
    for entry in to_load:
        tasks.append({
            "fn": bulk.load_zip_csvs,
            "args": (conn, entry["url"], f"{TABLE_PREFIX}_{entry['name']}", ENTITY_KEYS),
            "kwargs": {"user_agent": USER_AGENT, "max_rows": args.max_rows, "timeout": 900},
            "name": entry["name"],
        })

    results = bulk.parallel_load(tasks, max_workers=min(4, len(to_load)), label="EPA")

    loaded_tables = []
    for r in results:
        if "result" in r and r["result"]:
            for tbl, rows, keys in r["result"]:
                total_tables += 1
                total_rows += rows
                loaded_tables.append(tbl)

    # Run quality gate on each newly loaded table
    import uuid as _uuid
    run_id = str(_uuid.uuid4())
    dq_failures = 0
    for tbl in loaded_tables:
        passed, _ = bulk.run_quality_gate(conn, f"fed_epa_echo_{tbl.lower()}", tbl, run_id)
        if not passed:
            dq_failures += 1

    print(f"\nDone: {total_tables} tables loaded, {total_rows:,} total rows"
          + (f", {dq_failures} DQ failures" if dq_failures else ""))
    conn.close()
    return 1 if dq_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
