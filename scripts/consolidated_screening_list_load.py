#!/usr/bin/env python3
"""Deterministic loader for the US Consolidated Screening List (CSL).

One row = one restricted/denied party across the 11 export-control and sanctions
lists maintained by Commerce (BIS), State, and Treasury (OFAC), merged into one
feed by trade.gov. Nested fields (addresses, alt_names, ids, programs) are
flattened to '; '-joined strings; the full bulk JSON is returned in one payload
(no pagination trap -- verified 'total' == len(results)).

    python scripts/consolidated_screening_list_load.py          # preview
    python scripts/consolidated_screening_list_load.py --run     # land it
"""
from __future__ import annotations
import argparse, sys
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_consolidated_screening_list"
TABLE = SID.upper()
URL = "https://data.trade.gov/downloadable_consolidated_screening_list/v1/consolidated.json"


def _join(v):
    if v is None:
        return ""
    if isinstance(v, list):
        parts = []
        for item in v:
            if isinstance(item, dict):
                parts.append(" ".join(str(x) for x in item.values() if x))
            elif item:
                parts.append(str(item))
        return "; ".join(parts)
    return str(v)


def _flatten(rec: dict) -> dict:
    out = {}
    for k, v in rec.items():
        out[k.upper()] = _join(v) if isinstance(v, (list, dict)) else v
    return out


def _fetch_df() -> pd.DataFrame:
    r = requests.get(URL, timeout=120)
    r.raise_for_status()
    d = r.json()
    results = d.get("results", [])
    total = d.get("total")
    if total is not None and total != len(results):
        print(f"WARNING: API total={total} but results len={len(results)} -- possible pagination trap", flush=True)
    rows = [_flatten(r) for r in results]
    return pd.DataFrame(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== US Consolidated Screening List ===", flush=True)
    df = _fetch_df()
    cfg = {
        "source_id": SID,
        "name": "US Consolidated Screening List (CSL)",
        "publisher": "International Trade Administration / trade.gov (aggregating BIS, State, OFAC)",
        "url": "https://www.trade.gov/consolidated-screening-list",
        "description": "Combined feed of 11 US export-control and sanctions/denial lists "
                       "(BIS Entity/Denied Persons/Unverified, OFAC SDN/Consolidated/Capta, "
                       "State DDTC debarred, etc). One row per restricted party; SOURCE column "
                       "identifies the originating list.",
        "jurisdiction": "federal", "category": "Sanctions", "subcategory": "Export control / denial lists",
        "unit_of_observation": "one row = one restricted/denied party",
        "geographic_scope": "Global", "access_method": "bulk_download", "format": "json",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "daily (5am ET)",
        "volume": f"{len(df):,} rows", "license_terms": "U.S. Government work, public domain",
        "join_keys": "ID, ENTITY_NUMBER, SOURCE",
        "accountability_relevance": "US half of the ban-list triangulation; direct join bait "
                                    "against USAspending/SEC/corporate entity data.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/consolidated_screening_list_load.py (nested-field flatten, "
                "snapshot-replace).",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
