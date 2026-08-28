#!/usr/bin/env python3
"""Deterministic loader for the HHS OIG LEIE (List of Excluded Individuals/Entities).

One row = one individual/entity currently excluded from participation in
Medicare, Medicaid, and all federal health care programs. ~83k rows.
Full-replacement CSV published monthly by OIG (UPDATED.csv).

Snapshot-replace via _small_flat_loader (sha-skip + density + never-shrink
guards). Refreshes the existing FED_HHS_OIG_LEIE table under the same
source_id used by the June 2026 loads.

    python scripts/hhs_oig_leie_load.py          # preview
    python scripts/hhs_oig_leie_load.py --run    # land it
"""
from __future__ import annotations
import argparse, io, sys
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_hhs_oig_leie"
TABLE = SID.upper()
URL = "https://oig.hhs.gov/exclusions/downloadables/UPDATED.csv"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== HHS OIG LEIE exclusions list ===", flush=True)
    r = requests.get(URL, timeout=300,
                     headers={"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"})
    r.raise_for_status()
    # dtype=str: NPI/UPIN/ZIP/dates must land as text, never floats.
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, low_memory=False,
                     encoding_errors="replace")
    cfg = {
        "source_id": SID,
        "name": "HHS OIG List of Excluded Individuals/Entities (LEIE)",
        "publisher": "HHS Office of Inspector General (OIG)",
        "url": "https://oig.hhs.gov/exclusions/exclusions_list.asp",
        "description": "Individuals and entities currently excluded from Medicare, Medicaid, "
                       "and all federal health care programs, with exclusion type/date, "
                       "reinstatement and waiver fields.",
        "jurisdiction": "federal", "category": "Health", "subcategory": "Enforcement",
        "unit_of_observation": "one row = one excluded individual/entity",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "monthly full replacement",
        "volume": f"{len(df):,} rows", "license_terms": "U.S. Government work, public domain",
        "join_keys": "NPI, UPIN, LASTNAME+FIRSTNAME+DOB, BUSNAME",
        "accountability_relevance": "The federal health-care ban list; joins against NPPES, "
                                    "PECOS, Open Payments and CMS provider data for "
                                    "banned-but-still-billing patterns.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/hhs_oig_leie_load.py (snapshot-replace of the monthly "
                 "UPDATED.csv full file).",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
