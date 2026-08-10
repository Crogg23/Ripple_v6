#!/usr/bin/env python3
"""EPA Superfund site boundaries (attributes), full pull.

The portal probe landed exactly 2,000 rows — the ArcGIS page cap. True count
is 2,114 (returnCountOnly). This pages with resultOffset and snapshot-replaces
the landing table. Attributes only (returnGeometry=false); polygon geometry
stays with EPA — the site EPA_ID is the join key to the modeled FRS/Superfund
tables.

    python scripts/superfund_boundaries_load.py          # preview
    python scripts/superfund_boundaries_load.py --run    # land it
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_epa_superfund_site_boundaries"
TABLE = SID.upper()
BASE = ("https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/"
        "FAC_Superfund_Site_Boundaries_EPA_Public/FeatureServer/0/query")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== EPA Superfund site boundaries (attributes, full) ===", flush=True)
    rows, offset = [], 0
    while True:
        r = requests.get(BASE, timeout=120, params={
            "where": "1=1", "outFields": "*", "returnGeometry": "false",
            "f": "json", "resultOffset": offset, "resultRecordCount": 2000,
            "orderByFields": "OBJECTID"})
        r.raise_for_status()
        feats = r.json().get("features", [])
        if not feats:
            break
        rows.extend(f["attributes"] for f in feats)
        offset += len(feats)
    df = pd.DataFrame(rows)
    cfg = {
        "source_id": SID,
        "name": "EPA Superfund Site Boundaries",
        "publisher": "U.S. Environmental Protection Agency",
        "url": BASE,
        "description": "Superfund (NPL and related) site boundary records, one row per site "
                       "boundary feature: EPA site id, name, status, acreage, location. "
                       "Attributes only — polygon geometry not landed.",
        "jurisdiction": "federal", "category": "Environment", "subcategory": "Superfund",
        "unit_of_observation": "one row = one Superfund site boundary feature",
        "geographic_scope": "United States", "access_method": "api", "format": "json",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "periodic",
        "volume": f"{len(df):,} rows", "license_terms": "US Government public data",
        "join_keys": "epa_id",
        "accountability_relevance": "Where contaminated sites sit relative to communities; "
                                    "joins to EPA FRS and enforcement corpora via EPA id.",
    }
    status = load_and_register(df, SID, TABLE, BASE, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
