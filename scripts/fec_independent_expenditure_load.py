#!/usr/bin/env python3
"""Load the FEC Independent Expenditure file (Schedule E), cycles 2024 + 2026.

This is the CLEAN outside-spending source: each row carries CAN_ID (candidate),
SPE_ID (the spender committee), and SUP_OPP = S(upport) / O(ppose) -- the explicit
for/against flag. We use this as the source of truth for "ad money for/against a
member" instead of reconstructing it from pas2's 24A/24E, so support and oppose are
never accidentally summed together.

Unlike the pipe bulk files, this one is COMMA-delimited WITH a header -> parse_csv,
not parse_pipe.
"""
from __future__ import annotations

import sys

import pandas as pd
import requests

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

from build_skeleton import land  # noqa: E402
from loadkit import fec_parse    # noqa: E402

YEARS = ["2024", "2026"]
SID = "fed_fec_independent_expenditures"


def fetch(year: str) -> pd.DataFrame:
    url = f"https://www.fec.gov/files/bulk-downloads/{year}/independent_expenditure_{year}.csv"
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    # The live file uses lowercase names (cand_id/spe_id/exp_amo/...); validate the
    # ones we rely on, keep the rest as-is.
    df = fec_parse.parse_csv(r.content, expected_columns=["cand_id", "spe_id", "exp_amo"])
    df["CYCLE_FILE"] = year
    print(f"  IE {year}: {len(df):,} rows", flush=True)
    return df


def main() -> int:
    print(f"=== FEC Independent Expenditures cycles {'+'.join(YEARS)} ===", flush=True)
    df = pd.concat([fetch(y) for y in YEARS], ignore_index=True)
    land(df, SID, "https://www.fec.gov/files/bulk-downloads/",
         "FEC Independent Expenditures (Schedule E), 2024+2026; one row = one IE; SUP_OPP = for/against.")
    print(f"\nDONE -> LIBRARY_RAW.LANDING.{SID.upper()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
