#!/usr/bin/env python3
"""Deterministic loader for PBGC's Single-Employer Plans Trusteed by PBGC list.

Plan-LEVEL data (not the aggregate Data Book statistical tables already landed as
fed_pbgc_data): one row = one single-employer defined-benefit pension plan PBGC has
taken over (trusteed) since its creation in 1974, after the sponsoring employer
failed or the plan otherwise terminated with insufficient assets. Carries the plan's
real EIN and Plan Number (PN) -- the join keys needed to connect PBGC to DOL Form
5500 (fed_dol_form5500.EIN / .PLAN_NUM), i.e. "did this plan sponsor's other
pension filings show trouble before PBGC had to step in."

Source: PBGC's "Find a trusteed pension plan" page publishes a live XLSX export,
distinct from the aggregate Data Book (pbgc.gov/about/reports/pension-insurance-data,
already landed as fed_pbgc_data -- do not touch). Confirmed via WebFetch + direct
download 2026-08-05: single 'Export' sheet, 5,176 rows, EIN and Plan Number both
100% non-null with real distinct values (not a masked/blank sentinel column).

Known source-data quirk (PBGC's own export, not introduced by this loader): 574 of
5,176 rows (11.1%) carry an EIN shorter than 9 digits. Breakdown by length: 531 rows
at 8 digits (plausible dropped leading zero -- valid EIN prefixes 01-06 legitimately
start with 0), plus 43 outliers at 4-6 digits (1 at 4, 36 at 5, 6 at 6) that are too
short to be a 9-digit EIN missing one digit and look like some other internal PBGC
sequence number, not an EIN at all -- mostly very old case numbers (earliest PBGC
trusteeships, pre-1980s). Landed AS-IS/unpadded since the true original value can't
be recovered from this file alone. Flagged here, not silently reformatted -- treat
EIN as unreliable for the ~11% of rows shorter than 9 digits if using it as a hard
join key downstream.

    python scripts/pbgc_trusteed_plans_load.py          # preview
    python scripts/pbgc_trusteed_plans_load.py --run     # land it
"""
from __future__ import annotations
import argparse, io, sys
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_pbgc_trusteed_plans"
TABLE = SID.upper()
URL = "https://www.pbgc.gov/sites/default/files/trusteedplans.xlsx"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== PBGC Single-Employer Plans Trusteed by PBGC (plan-level, EIN/PN) ===", flush=True)
    r = requests.get(URL, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    df = pd.read_excel(io.BytesIO(r.content), sheet_name="Export", dtype=str)
    cfg = {
        "source_id": SID,
        "name": "PBGC Single-Employer Plans Trusteed by PBGC",
        "publisher": "Pension Benefit Guaranty Corporation (PBGC)",
        "url": "https://www.pbgc.gov/workers-retirees/trusteed-plans",
        "description": "Plan-level list of every single-employer defined-benefit pension plan "
                       "PBGC has trusteed (taken over) since 1974, after the sponsor/plan failed. "
                       "One row = one trusteed plan: case number, sponsor name, plan name, EIN, "
                       "plan number (PN), city/state, date of plan termination, date of PBGC "
                       "trusteeship, participant count at termination. Distinct from the aggregate "
                       "PBGC Data Book statistics already landed as fed_pbgc_data (no EIN/PN there).",
        "jurisdiction": "federal", "category": "Economy", "subcategory": "Pension & Retirement Insurance",
        "unit_of_observation": "one row = one PBGC-trusteed single-employer pension plan",
        "temporal_coverage": "1974-present (plan termination/trusteeship dates)",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "xlsx",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "quarterly (per PBGC)",
        "volume": f"{len(df):,} rows", "license_terms": "U.S. Government work, public domain",
        "join_keys": "EIN, Plan Number",
        "accountability_relevance": "The EIN+PN pair joins directly to DOL Form 5500 "
                                    "(fed_dol_form5500.EIN / .PLAN_NUM): lets Ripple trace a "
                                    "sponsor's pension-plan filing history in the years BEFORE "
                                    "PBGC had to trustee the plan -- e.g. funding-status red flags "
                                    "on 5500s that preceded a failure PBGC ultimately covered.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/pbgc_trusteed_plans_load.py (snapshot-replace). Live XLSX "
                "export, single 'Export' sheet. EIN/Plan Number read as text (dtype=str) to avoid "
                "int-cast leading-zero loss on top of the source's own pre-existing short-EIN rows "
                "(574/5,176, 11.1%, shorter than 9 digits -- 531 at 8 digits (likely dropped leading "
                "zero), 43 at 4-6 digits (likely not an EIN at all); see script docstring). Treat EIN "
                "as unreliable for ~11% of rows if using it as a hard join key. Separate product from "
                "fed_pbgc_data (aggregate Data Book statistics, no EIN/PN there).",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
