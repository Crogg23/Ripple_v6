"""Land the whole 3DEP ImageServer footprint catalog, not the first 5,000.

WHAT THE ROWS ARE
  One row per DEM tile in USGS's 3DEPElevation mosaic: the tile name, its
  resolution, source, acquisition and publish dates, the URL of the GeoTIFF
  and the tile's footprint polygon (SHAPE). It is the inventory of elevation
  files, not elevation values. Probed 2026-09-07: returnCountOnly says 138,326
  rows; maxRecordCount is 2,000.

WHAT STOPPED THE OLD TABLE
  FED_USGS_3DEP is 5,000 rows: the onboarding fetch_data looped without
  walking resultOffset past its own cap.

WHAT THIS DOES
  Pages /query with resultOffset in steps of 2,000 into
  LIBRARY_RAW.LANDING.FED_USGS_3DEP_FULL, same 31 columns as the old table
  (SHAPE is the geometry JSON as text) plus _INGESTED_AT / _SOURCE_RUN_ID /
  _SRC_SHA256. The old table is not touched.

    python scripts/usgs_3dep_full_load.py          # dry run
    python scripts/usgs_3dep_full_load.py --run    # land it
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _repage_land as rp  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

SOURCE_ID = "fed_usgs_3dep_full"
TABLE = "FED_USGS_3DEP_FULL"
BASE = "https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer"
QUERY = BASE + "/query"
PAGE = 2000
COLUMNS = ["OBJECTID", "NAME", "MINPS", "MAXPS", "LOWPS", "HIGHPS", "CATEGORY", "TAG",
           "GROUPNAME", "PRODUCTNAME", "CENTERX", "CENTERY", "ZORDER", "SHAPE_LENGTH",
           "SHAPE_AREA", "DATASET_ID", "BEST", "DEM_TYPE", "SOURCE", "VERTICALDATUM",
           "ACQUISITIONDATE", "URL", "METADATA", "PUBDATE", "TITLE", "RESOLUTION_X",
           "RESOLUTION_Y", "CDATE", "STARTDATE", "ENDDATE", "SHAPE"]


def total() -> int:
    r = requests.get(QUERY, params={"where": "1=1", "returnCountOnly": "true", "f": "json"},
                     headers=rp.UA, timeout=60)
    r.raise_for_status()
    return int(r.json()["count"])


def pages():
    offset = 0
    while True:
        params = {"where": "1=1", "outFields": "*", "returnGeometry": "true", "f": "json",
                  "orderByFields": "OBJECTID", "resultOffset": offset,
                  "resultRecordCount": PAGE}
        r = requests.get(QUERY, params=params, headers=rp.UA, timeout=300)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise RuntimeError(f"ArcGIS error at offset {offset}: {data['error']}")
        feats = data.get("features", [])
        if not feats:
            return
        rows = []
        for f in feats:
            a = dict(f.get("attributes", {}))
            a["SHAPE"] = json.dumps(f.get("geometry")) if f.get("geometry") is not None else None
            rows.append(a)
        df = pd.DataFrame(rows)
        df.columns = [bulk.sf_col(c) for c in df.columns]
        yield df
        offset += len(feats)
        if len(feats) < PAGE and not data.get("exceededTransferLimit"):
            return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="land it; default is dry run")
    ap.add_argument("--append", action="store_true", help="allow landing on top of existing rows")
    args = ap.parse_args()
    n = total()
    print(f"source {QUERY}\nserver says {n:,} tiles; page size {PAGE:,}")
    rp.land_pages(source_id=SOURCE_ID, table=TABLE, source_url=QUERY, columns=COLUMNS,
                  pages=pages, run=args.run, append=args.append, expected_total=n)


if __name__ == "__main__":
    main()
