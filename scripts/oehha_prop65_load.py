#!/usr/bin/env python3
"""Deterministic loader for the California OEHHA Proposition 65 chemicals list.

One row = one chemical known to the State of California to cause cancer or
reproductive toxicity, with listing mechanism and date. Trivial size, useful join
bait for later EPA/FDA chemical-hazard work.

    python scripts/oehha_prop65_load.py          # preview
    python scripts/oehha_prop65_load.py --run     # land it
"""
from __future__ import annotations
import argparse, io, sys
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "state_oehha_prop65_chemicals"
TABLE = SID.upper()
URL = "https://oehha.ca.gov/sites/default/files/media/2025-01/p65chemicalslist.csv"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== OEHHA Prop 65 Chemicals List ===", flush=True)
    r = requests.get(URL, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), skiprows=11)
    df = df.dropna(axis=1, how="all")
    df = df.dropna(how="all")
    cfg = {
        "source_id": SID,
        "name": "California Proposition 65 Chemicals List",
        "publisher": "California Office of Environmental Health Hazard Assessment (OEHHA)",
        "url": "https://oehha.ca.gov/proposition-65/chemicals-considered-or-listed-under-proposition-65",
        "description": "Every chemical listed under Prop 65 as known to California to cause "
                       "cancer or reproductive toxicity, with listing mechanism and date.",
        "jurisdiction": "state", "category": "Environment", "subcategory": "Chemical hazard",
        "unit_of_observation": "one row = one listed chemical", "geographic_scope": "California",
        "access_method": "bulk_download", "format": "csv", "auth": {"type": "none"}, "cost": "free",
        "update_cadence": "as listings change", "volume": f"{len(df):,} rows",
        "license_terms": "California public record", "join_keys": "CHEMICAL NAME, CAS NUMBER",
        "accountability_relevance": "Hazard reference list for joining against facility/product "
                                    "chemical-release and recall data.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/oehha_prop65_load.py (snapshot-replace).",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
