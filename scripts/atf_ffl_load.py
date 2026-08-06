"""Load ATF Federal Firearms Licensees (FFL) list.

Source: ATF's ArcGIS Feature Service (hosted at atf-geoplatform.maps.arcgis.com),
pulled via the item's public FeatureServer REST endpoint. atf.gov itself
site-wide-blocks automated fetches (403 on plain requests/curl even with a
browser UA) -- this is a NEW fetch trap, same family as sec.gov/cbp.gov.
The ArcGIS-hosted service is NOT blocked and returns clean JSON.

    python scripts/atf_ffl_load.py --run
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import sys
import uuid
from pathlib import Path

import pandas as pd
import requests

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

FEATURE_SERVER = (
    "https://services6.arcgis.com/PrP5ZtrES07DmVmv/arcgis/rest/services/"
    "Federal_Firearm_Licensees_locations/FeatureServer/0/query"
)
TABLE = "FED_ATF_FFL"
PAGE_SIZE = 2000
UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}


def fetch_all() -> pd.DataFrame:
    rows = []
    offset = 0
    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "f": "json",
            "resultOffset": offset,
            "resultRecordCount": PAGE_SIZE,
        }
        r = requests.get(FEATURE_SERVER, params=params, headers=UA, timeout=60)
        r.raise_for_status()
        data = r.json()
        feats = data.get("features", [])
        if not feats:
            break
        for f in feats:
            rows.append(f.get("attributes", {}))
        print(f"  fetched {len(rows):,} rows so far...")
        offset += len(feats)
        if len(feats) < PAGE_SIZE:
            break
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()

    print("Fetching ATF FFL list from ArcGIS FeatureServer...")
    df = fetch_all()
    print(f"Total fetched: {len(df):,} rows, {len(df.columns)} columns")
    print(list(df.columns))

    if not args.run:
        print("Preview only. Pass --run to load.")
        return

    df = df.astype(str)
    content = df.to_csv(index=False).encode("utf-8")
    sha = hashlib.sha256(content).hexdigest()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)

    df.columns = [bulk.sf_col(c) for c in df.columns]
    df[bulk.META_INGESTED_AT] = started
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha

    conn = snow.connect()
    from snowflake.connector.pandas_tools import write_pandas
    ok, _c, nrows, _ = write_pandas(
        conn, df, table_name=TABLE,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    print(f"Loaded {TABLE}: ok={ok} rows={nrows}")
    passed, _report = bulk.run_quality_gate(
        conn, TABLE, TABLE, run_id, sha256=sha, source_url=FEATURE_SERVER)
    conn.close()
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
