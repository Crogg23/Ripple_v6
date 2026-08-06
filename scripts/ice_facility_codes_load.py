#!/usr/bin/env python3
"""Deterministic loader for ICE detention facility codes (reference list only).

One row = one facility ICE has used for civilian immigration detention: code, name,
address, AOR, lat/long, facility type. NO person-level detention records, stints, or
detainers here -- this is the Vera Institute's facility metadata/lookup table (the
same codes ICE's own person-level data uses), which is explicitly the safe half of
this source per the RED gate on person-level ICE detention data.

    python scripts/ice_facility_codes_load.py          # preview
    python scripts/ice_facility_codes_load.py --run     # land it
"""
from __future__ import annotations
import argparse, io, sys
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_ice_detention_facility_codes"
TABLE = SID.upper()
URL = "https://raw.githubusercontent.com/vera-institute/ice-detention-trends/main/metadata/facilities.csv"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== ICE Detention Facility Codes (reference list, NOT person-level) ===", flush=True)
    r = requests.get(URL, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    cfg = {
        "source_id": SID,
        "name": "ICE Detention Facility Codes (reference list)",
        "publisher": "Vera Institute of Justice (ICE Detention Trends), sourced from ICE facility codes",
        "url": "https://github.com/vera-institute/ice-detention-trends",
        "description": "Facility-level reference table: detention facility code, name, address, "
                       "AOR, lat/long, facility type. No person-level detention data. This is the "
                       "codebook that ICE's own person-level detention data uses for facility codes.",
        "jurisdiction": "federal", "category": "Justice", "subcategory": "Immigration detention",
        "unit_of_observation": "one row = one ICE detention facility",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "periodic",
        "volume": f"{len(df):,} rows", "license_terms": "Vera Institute public dataset",
        "join_keys": "detention_facility_code",
        "accountability_relevance": "Facility-level reference for any future ICE detention "
                                    "conditions analysis. Person-level detention data explicitly "
                                    "NOT loaded here (RED-gated, pending Chris's ruling).",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/ice_facility_codes_load.py (snapshot-replace). "
                "Facility metadata only -- no stints/detainers/person-level records.",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
