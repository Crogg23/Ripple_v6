#!/usr/bin/env python3
"""Deterministic loader for the FHFA Suspended Counterparty Program list.

One row = one individual/entity suspended from doing business with Fannie Mae,
Freddie Mac, or the Federal Home Loan Banks for fraud or financial misconduct.
~241 rows. CSV export endpoint found on the FHFA program page's filter form.

    python scripts/fhfa_suspended_counterparty_load.py          # preview
    python scripts/fhfa_suspended_counterparty_load.py --run     # land it
"""
from __future__ import annotations
import argparse, io, sys
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_fhfa_suspended_counterparty"
TABLE = SID.upper()
URL = "https://www.fhfa.gov/document/d/scp/download/csv"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== FHFA Suspended Counterparty Program List ===", flush=True)
    r = requests.get(URL, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    cfg = {
        "source_id": SID,
        "name": "FHFA Suspended Counterparty Program List",
        "publisher": "Federal Housing Finance Agency (FHFA)",
        "url": "https://www.fhfa.gov/regulation/suspended-counterparty-program",
        "description": "Individuals/entities suspended from doing business with Fannie Mae, "
                       "Freddie Mac, and the Federal Home Loan Banks due to fraud or other "
                       "financial misconduct, with effective date and suspension order link.",
        "jurisdiction": "federal", "category": "Finance", "subcategory": "Enforcement",
        "unit_of_observation": "one row = one suspended person/entity",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "as suspensions issue",
        "volume": f"{len(df):,} rows", "license_terms": "U.S. Government work, public domain",
        "join_keys": "Last_Name + First_Name, Company",
        "accountability_relevance": "Ban list for mortgage-finance fraud actors; joins against "
                                    "HMDA/HUD lender data.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/fhfa_suspended_counterparty_load.py (snapshot-replace); "
                "CSV endpoint found via the program page's exposed filter form action.",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
