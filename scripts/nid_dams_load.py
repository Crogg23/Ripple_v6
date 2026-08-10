#!/usr/bin/env python3
"""Deterministic loader for the USACE National Inventory of Dams (NID).

Re-ingest of a broken 2026-08 load that landed the inventory as a two-column
key/value mush. This pulls the official full-nation CSV export (one row = one
dam) and snapshot-replaces the landing table.

    python scripts/nid_dams_load.py          # preview
    python scripts/nid_dams_load.py --run    # land it
"""
from __future__ import annotations
import argparse
import io
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_usace_nid_dams"
TABLE = SID.upper()
URL = "https://nid.sec.usace.army.mil/api/nation/csv"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== USACE National Inventory of Dams (full nation CSV) ===", flush=True)
    r = requests.get(URL, timeout=300, headers={"User-Agent": "ripple-research/1.0"})
    r.raise_for_status()
    # The export ships a title line above the real header; sniff for it.
    text = r.text
    first_line = text.split("\n", 1)[0]
    skip = 1 if first_line.startswith("Data Last Updated") else 0
    df = pd.read_csv(io.StringIO(text), skiprows=skip, low_memory=False)
    cfg = {
        "source_id": SID,
        "name": "USACE National Inventory of Dams",
        "publisher": "U.S. Army Corps of Engineers",
        "url": "https://nid.sec.usace.army.mil/",
        "description": "Full National Inventory of Dams: one row per dam with NID ID, name, "
                       "owner, hazard potential classification, condition assessment, height, "
                       "storage, river, location, inspection dates.",
        "jurisdiction": "federal", "category": "Environment", "subcategory": "Dam safety",
        "unit_of_observation": "one row = one dam",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "continuous",
        "volume": f"{len(df):,} rows", "license_terms": "US Government public data",
        "join_keys": "nid_id",
        "accountability_relevance": "Hazard classification + condition + private ownership of "
                                    "dams upstream of communities; joins to FEMA flood and "
                                    "county geography.",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
