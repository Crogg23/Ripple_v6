#!/usr/bin/env python3
"""Load current congressional committee membership (who sits on / chairs what).

Two @unitedstates/congress-legislators files: committee-membership-current.yaml
(committee_code -> [members]) + committees-current.yaml (committee/subcommittee
names). Flattened to one row per (committee_code, bioguide), keyed on bioguide so it
joins straight to POLITICS__MEMBER_CROSSWALK. 119th-current only.
"""
from __future__ import annotations

import sys

import pandas as pd
import requests
import yaml

sys.path.insert(0, r"c:\Code\Ripple_v6")
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
sys.path.insert(0, r"c:\Code\Ripple_v6\politics\loaders")

from dotenv import load_dotenv  # noqa: E402

load_dotenv(r"c:\Code\Ripple_v6\library-onboarding\.env", override=True)

from build_skeleton import land  # noqa: E402

GH = "https://raw.githubusercontent.com/unitedstates/congress-legislators/main"
SID = "fed_congress_committee_membership"


def fetch() -> pd.DataFrame:
    mem = yaml.safe_load(requests.get(f"{GH}/committee-membership-current.yaml", timeout=120).content)
    coms = yaml.safe_load(requests.get(f"{GH}/committees-current.yaml", timeout=120).content)
    cname = {}
    for c in coms or []:
        tid = c.get("thomas_id")
        if tid:
            cname[tid] = c.get("name", "")
        for sc in c.get("subcommittees", []) or []:
            cname[(tid or "") + sc.get("thomas_id", "")] = f"{c.get('name','')} -- {sc.get('name','')}"
    rows = []
    for code, members in (mem or {}).items():
        for m in (members or []):
            rows.append({
                "COMMITTEE_CODE": code,
                "COMMITTEE_NAME": cname.get(code, ""),
                "IS_SUBCOMMITTEE": str(len(code) > 4),
                "BIOGUIDE": m.get("bioguide", ""),
                "MEMBER_NAME": m.get("name", ""),
                "PARTY": m.get("party", ""),
                "RANK": str(m.get("rank", "")),
                "TITLE": m.get("title", ""),  # Chair / Ranking Member / Vice Chair / ''
            })
    df = pd.DataFrame(rows)
    print(f"  flattened {len(df):,} committee seats across {df['COMMITTEE_CODE'].nunique()} committees/subcommittees", flush=True)
    return df


def main() -> int:
    print("=== Congressional committee membership (current) ===", flush=True)
    df = fetch()
    land(df, SID, f"{GH}/committee-membership-current.yaml",
         "Current congressional committee + subcommittee membership; one row = one member-seat.")
    print(f"\nDONE -> LIBRARY_RAW.LANDING.{SID.upper()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
