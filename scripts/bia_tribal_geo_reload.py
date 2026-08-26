#!/usr/bin/env python3
"""BIA tribal land geography, RELOAD against the real source.

2026-07-31 finding (CHRIS_DECISIONS.md): the registered URL
(https://opendata-1-bia-geospatial.hub.arcgis.com/) is an ArcGIS Hub HOME
PAGE, not a dataset -- the original crawl scraped the portal's item
directory (StoryMaps, web apps) instead of real tribal land records. This
is the actual BIA American Indian & Alaska Native Land Area Representation
(AIAN-LAR) FeatureServer, found 2026-08-26 and verified live: 335 features,
real polygon geometry, fields OBJECTID/LARID/LARName/GISAcres. Hosted on the
same ArcGIS Online org (cJ9YHowT8TU7DUyn) as scripts/superfund_boundaries_load.py's
EPA Superfund boundaries -- a known-good source in this repo already.

Same source_id/table as the dead source (fed_bia_tribal_geo /
FED_BIA_TRIBAL_GEO) so downstream staging/mart wiring doesn't need to change,
only the data underneath it. Geometry rings are landed as a JSON string
column (GEOMETRY_JSON) -- attributes stay flat, geometry stays recoverable.

    python scripts/bia_tribal_geo_reload.py          # preview
    python scripts/bia_tribal_geo_reload.py --run    # land it
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_bia_tribal_geo"
TABLE = "FED_BIA_TRIBAL_GEO"
BASE = ("https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/"
        "BND___American_Indian___Alaska_Native_Land_Area_Representations__BIA_/"
        "FeatureServer/1/query")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== BIA tribal land (AIAN-LAR) reload ===", flush=True)
    r = requests.get(BASE, timeout=120, params={
        "where": "1=1", "outFields": "*", "returnGeometry": "true",
        "f": "json", "orderByFields": "OBJECTID"})
    r.raise_for_status()
    feats = r.json().get("features", [])
    rows = []
    for f in feats:
        row = dict(f["attributes"])
        row["GEOMETRY_JSON"] = json.dumps(f.get("geometry")) if f.get("geometry") else None
        rows.append(row)
    df = pd.DataFrame(rows)
    cfg = {
        "source_id": SID,
        "name": "BIA Tribal Land Area Representations (AIAN-LAR)",
        "publisher": "U.S. Department of the Interior, Bureau of Indian Affairs",
        "url": BASE,
        "description": "American Indian and Alaska Native Land Area Representations: "
                       "the exterior extent of land held in trust or restricted-fee "
                       "status by the United States for federally recognized Tribes.",
        "jurisdiction": "federal", "category": "Reference", "subcategory": "Land and Territory",
        "unit_of_observation": "one row = one BIA Land Area Representation (LAR) polygon",
        "geographic_scope": "United States", "access_method": "api", "format": "json",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "periodic",
        "volume": f"{len(df):,} rows", "license_terms": "US Government public data",
        "join_keys": "larid",
        "accountability_relevance": "Where federally-recognized tribal trust land sits, "
                                    "for joining against environmental/enforcement/resource "
                                    "data that touches those areas.",
    }
    status = load_and_register(df, SID, TABLE, BASE, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
