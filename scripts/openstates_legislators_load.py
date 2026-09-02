#!/usr/bin/env python3
"""Load Open States current-legislators CSVs, all states + DC + PR.

One row = one sitting state legislator: party, chamber, district, contact,
socials, wikidata id. The who's-who layer for every statehouse -- the join
target for state lobbying, contracts, and campaign-finance sources already
landed. Bills/votes are separate per-session bulk files (a later, bigger job);
this lands the people layer, refreshed monthly upstream.

    python scripts/openstates_legislators_load.py          # preview
    python scripts/openstates_legislators_load.py --run    # land it
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register  # noqa: E402

SID = "st_openstates_legislators"
TABLE = SID.upper()
BASE = "https://data.openstates.org/people/current"
JURISDICTIONS = [
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id",
    "il", "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms",
    "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nc", "nd", "oh", "ok",
    "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv",
    "wi", "wy", "dc", "pr",
]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== Open States current legislators ===", flush=True)
    frames, missing = [], []
    for j in JURISDICTIONS:
        r = requests.get(f"{BASE}/{j}.csv", timeout=120)
        if r.status_code == 404:
            missing.append(j)
            continue
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text), dtype=str)
        df["JURISDICTION"] = j.upper()
        frames.append(df)
    if not frames:
        raise RuntimeError("every jurisdiction fetch 404'd -- endpoint moved?")
    allf = pd.concat(frames, ignore_index=True)
    print(f"  {len(allf):,} legislators across {len(frames)} jurisdictions"
          + (f" (404: {','.join(missing)})" if missing else ""), flush=True)
    cfg = {
        "source_id": SID,
        "name": "Open States current state legislators",
        "publisher": "Open States / Plural Policy",
        "url": "https://open.pluralpolicy.com/data/",
        "description": "Every sitting state legislator, all 50 states + DC + PR: party, "
                       "chamber, district, contact info, socials, wikidata id. Scraped "
                       "from statehouse sites, refreshed monthly.",
        "jurisdiction": "state", "category": "Government officials",
        "subcategory": "State legislators",
        "unit_of_observation": "one row = one current state legislator",
        "geographic_scope": "US, all states", "access_method": "bulk_download",
        "format": "csv", "auth": {"type": "none"}, "cost": "free",
        "update_cadence": "monthly",
        "volume": "every sitting state legislator nationally, ~7.4K people",
        "license_terms": "public domain, attribution appreciated",
        "join_keys": "id (ocd-person UUID), wikidata, name+state+district",
        "accountability_relevance": "The who's-who join target for state-level lobbying, "
                                    "contracts, and campaign finance already landed.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/openstates_legislators_load.py (snapshot-replace, "
                 "people layer only; per-session bills/votes are a separate job).",
    }
    status = load_and_register(allf, SID, TABLE, f"{BASE}/<state>.csv", cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
