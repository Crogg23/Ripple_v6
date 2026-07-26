"""Load CMS nursing home Penalties + Health Deficiencies (+ Fire Safety).

Mission packet item #9 (Gap Acquisition Campaign).
  FED_CMS_NURSING_HOME_PENALTIES     -- NH_Penalties (CCN keyed)
  FED_CMS_NURSING_HOME_DEFICIENCIES  -- NH_HealthCitations (CCN keyed)
  FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES -- NH_FireSafetyCitations (bonus, same family)

Discovers current download URLs from the Provider Data Catalog metastore so
the shifting monthly filenames don't break the loader.

    python scripts/cms_nursing_home_penalties_load.py --run
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

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

METASTORE = "https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

TARGETS = {
    "Penalties": "FED_CMS_NURSING_HOME_PENALTIES",
    "Health Deficiencies": "FED_CMS_NURSING_HOME_DEFICIENCIES",
    "Fire Safety Deficiencies": "FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()

    items = requests.get(METASTORE, timeout=120, headers=USER_AGENT).json()
    plan = []
    for d in items:
        title = d.get("title", "")
        if title in TARGETS:
            url = d["distribution"][0]["downloadURL"]
            plan.append((TARGETS[title], url))
            print(f"{TARGETS[title]}: {url}")

    if len(plan) != len(TARGETS):
        raise SystemExit(f"Expected {len(TARGETS)} datasets, found {len(plan)}")
    if not args.run:
        return

    conn = snow.connect()
    try:
        for tbl, url in plan:
            n = bulk.fast_load(conn, url, tbl, user_agent=USER_AGENT, max_rows=5_000_000)
            print(f"  {tbl}: {n:,} rows  SOURCE_URL={url}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
