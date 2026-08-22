"""Load US Census cartographic boundary polygons (county, state, ZCTA).

The one missing ingredient the Laboratory sweep found: zero polygon columns in
the whole warehouse (2 of 162,750 columns are geo-typed, both ship points).
This lands the Census 500k-resolution cartographic boundary shapefiles as
WKT TEXT in landing (byte-faithful, per standing rule), one row per shape:

  XC_CENSUS_CB_COUNTY  (~3,235 counties, GENZ2023)
  XC_CENSUS_CB_STATE   (~56 states/territories, GENZ2023)
  XC_CENSUS_CB_ZCTA    (~33k ZIP-code areas, GENZ2020 -- newest published)

Geometry becomes queryable via TO_GEOGRAPHY(wkt) downstream; the mart layer
adds that cast. Uses pyshp (no GDAL needed). ~80MB total download.

    python scripts/census_boundaries_load.py --run
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import sys
import uuid
import zipfile
from pathlib import Path

import pandas as pd
import requests
import shapefile  # pyshp

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

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
BASE23 = "https://www2.census.gov/geo/tiger/GENZ2023/shp"
BASE20 = "https://www2.census.gov/geo/tiger/GENZ2020/shp"

MANIFEST = [
    {"table": "XC_CENSUS_CB_COUNTY", "url": f"{BASE23}/cb_2023_us_county_500k.zip", "vintage": "2023"},
    {"table": "XC_CENSUS_CB_STATE", "url": f"{BASE23}/cb_2023_us_state_500k.zip", "vintage": "2023"},
    {"table": "XC_CENSUS_CB_ZCTA", "url": f"{BASE20}/cb_2020_us_zcta520_500k.zip", "vintage": "2020"},
]


def _ring_wkt(ring) -> str:
    return "(" + ", ".join(f"{x} {y}" for x, y in ring) + ")"


def shape_to_wkt(shp) -> str | None:
    """pyshp shape -> WKT MULTIPOLYGON. Census CB shapes are all polygons."""
    if shp.shapeType not in (shapefile.POLYGON, shapefile.POLYGONZ):
        return None
    parts = list(shp.parts) + [len(shp.points)]
    rings = [shp.points[parts[i]:parts[i + 1]] for i in range(len(parts) - 1)]
    # Census polygons: exterior rings are clockwise, holes counter-clockwise.
    # Group each hole with the last exterior seen (standard shapefile order).
    def is_cw(ring):
        s = sum((x2 - x1) * (y2 + y1) for (x1, y1), (x2, y2) in zip(ring, ring[1:]))
        return s > 0
    polys: list[list] = []
    for ring in rings:
        if is_cw(ring) or not polys:
            polys.append([ring])
        else:
            polys[-1].append(ring)
    body = ", ".join("(" + ", ".join(_ring_wkt(r) for r in rings_) + ")"
                     for rings_ in polys)
    return f"MULTIPOLYGON ({body})"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()

    conn = snow.connect() if args.run else None
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    from snowflake.connector.pandas_tools import write_pandas

    for entry in MANIFEST:
        print(f"downloading {entry['url'].rsplit('/', 1)[-1]}...", flush=True)
        r = requests.get(entry["url"], timeout=600, headers=UA)
        r.raise_for_status()
        zf = zipfile.ZipFile(io.BytesIO(r.content))
        names = {Path(n).suffix.lower(): n for n in zf.namelist()}
        rdr = shapefile.Reader(
            shp=io.BytesIO(zf.read(names[".shp"])),
            dbf=io.BytesIO(zf.read(names[".dbf"])),
            shx=io.BytesIO(zf.read(names[".shx"])))
        fields = [f[0] for f in rdr.fields[1:]]
        rows = []
        for sr in rdr.iterShapeRecords():
            rec = {bulk.sf_col(k): (None if v is None or v == "" else str(v))
                   for k, v in zip(fields, sr.record)}
            rec["GEOMETRY_WKT"] = shape_to_wkt(sr.shape)
            rows.append(rec)
        df = pd.DataFrame(rows)
        df["VINTAGE"] = entry["vintage"]
        df[bulk.META_INGESTED_AT] = started
        df[bulk.META_SOURCE_RUN_ID] = run_id
        df[bulk.META_SRC_SHA256] = None
        print(f"  {entry['table']}: {len(df):,} shapes, "
              f"{df['GEOMETRY_WKT'].str.len().sum() / 1e6:.0f}MB of WKT", flush=True)
        if args.run:
            data_cols = [c for c in df.columns]
            ddl = ", ".join(f"{c} VARCHAR" if c != bulk.META_INGESTED_AT
                            else f"{c} TIMESTAMP_NTZ" for c in data_cols)
            conn.cursor().execute(
                f"create or replace table {bulk.LANDING_DB}.{bulk.LANDING_SCHEMA}."
                f"{entry['table']} ({ddl})")
            ok, _c, n, _ = write_pandas(
                conn, df, table_name=entry["table"],
                database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
                auto_create_table=False, overwrite=False, quote_identifiers=False)
            if not ok:
                raise RuntimeError(f"{entry['table']}: write failed")
            print(f"  -> landed {n:,} rows", flush=True)
    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
