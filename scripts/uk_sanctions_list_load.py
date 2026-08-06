#!/usr/bin/env python3
"""Deterministic loader for the UK Sanctions List (gov.uk / OFSI-FCDO).

One row = one name-line for a sanctioned individual/entity/vessel under a UK
sanctions regime (the file is genuinely wide: aliases, addresses, DOB, national
IDs, all in one row per listing). Replaced the old OFSI Consolidated List in
Jan 2026 -- this is now the single authoritative UK list.

    python scripts/uk_sanctions_list_load.py          # preview
    python scripts/uk_sanctions_list_load.py --run     # land it
"""
from __future__ import annotations
import argparse, io, sys
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "intl_uk_sanctions_list"
TABLE = SID.upper()
URL = "https://sanctionslist.fcdo.gov.uk/docs/UK-Sanctions-List.csv"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== UK Sanctions List ===", flush=True)
    r = requests.get(URL, timeout=120)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), skiprows=1, low_memory=False)
    cfg = {
        "source_id": SID,
        "name": "UK Sanctions List",
        "publisher": "UK Foreign, Commonwealth & Development Office (FCDO) / OFSI",
        "url": "https://www.gov.uk/government/publications/the-uk-sanctions-list",
        "description": "All individuals, entities, and vessels designated under UK sanctions "
                       "regimes -- names/aliases, DOB, addresses, national IDs, sanctions "
                       "imposed, regime name. Replaced the OFSI Consolidated List (retired "
                       "Jan 2026) as the sole authoritative UK list.",
        "jurisdiction": "international", "category": "Sanctions", "subcategory": "UK sanctions",
        "unit_of_observation": "one row = one name-line for a sanctioned party",
        "geographic_scope": "Global (UK-administered)", "access_method": "bulk_download",
        "format": "csv", "auth": {"type": "none"}, "cost": "free",
        "update_cadence": "as designations change", "volume": f"{len(df):,} rows",
        "license_terms": "Open Government Licence", "join_keys": "Unique ID, OFSI Group ID, UN Reference Number",
        "accountability_relevance": "UK half of the ban-list triangulation (UN/UK/US); "
                                    "UN Reference Number is a direct join to the UN list.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/uk_sanctions_list_load.py (snapshot-replace, ~50MB CSV).",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
