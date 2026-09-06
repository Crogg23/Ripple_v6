#!/usr/bin/env python3
"""Load the FEC Independent Expenditure file (Schedule E), cycles 2018 to 2026.

This is the CLEAN outside-spending source: each row carries CAND_ID (candidate),
SPE_ID (the spender committee), and SUP_OPP = S(upport) / O(ppose) -- the explicit
for/against flag. We use this as the source of truth for "ad money for/against a
member" instead of reconstructing it from pas2's 24A/24E, so support and oppose are
never accidentally summed together.

Unlike the pipe bulk files, this one is COMMA-delimited WITH a header -> parse_csv,
not parse_pipe.

TWO THINGS INFLATE THE RAW TOTAL, measured 2026-09-06 against the live mart:

  prank filings                                             about 91.0 of 92.4 $B
      FEC's bulk file carries whatever gets web-filed, including a $9.98 billion
      "expenditure" from THE COURT OF DIVINE JUSTICE and one from Republican Emo
      Girl. Nineteen rows across four cycles. Every one is BOTH web-filed, so
      TRAN_ID starts 'WFT', AND over $20M. Neither test alone is safe: the plain
      dollar cap also catches 23 real rows worth $1.371B from FF PAC, MAGA Inc
      and Preserve America; the WFT prefix alone catches 5,339 real small filers
      worth $191M. The pair together catches the junk and nothing else.

  superseded amendments                                        about 1.7 $B, 2024
      An amended filing restates its transactions, so the original and every
      revision all sit in the file. Food & Water Action's $114M row appears nine
      times. A filing is superseded when its FILE_NUM turns up as some other
      row's PREV_FILE_NUM.

Both are FLAGGED here, never dropped. Landing keeps what the source published;
the mart filters on IS_SUSPECT_FILING = 'False' and IS_SUPERSEDED = 'False'.

Walked out on 2024: raw $49.68B -> drop superseded $47.93B -> drop suspect
$5.73B -> both $3.99B, against the roughly $4.4B the FEC publishes.
"""
from __future__ import annotations

import argparse
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

from land_frame import land  # noqa: E402
from loadkit import fec_parse    # noqa: E402

YEARS = ["2018", "2020", "2022", "2024", "2026"]
SID = "fed_fec_independent_expenditures"

# A junk filing is web-filed AND over this. See the module docstring for why one
# test alone is not enough.
SUSPECT_FLOOR = 20_000_000
WEB_FILED_PREFIX = "WFT"


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


def flag(df: pd.DataFrame) -> pd.DataFrame:
    """Add IS_SUSPECT_FILING and IS_SUPERSEDED. Nothing is dropped."""
    amt = pd.to_numeric(df["exp_amo"], errors="coerce").fillna(0)
    tran = df["tran_id"].astype(str)
    suspect = tran.str.startswith(WEB_FILED_PREFIX) & (amt > SUSPECT_FLOOR)

    # FILE_NUM is unique FEC-wide, so this is safe to compute across all cycles at
    # once. A blank prev_file_num must not match a blank file_num.
    prev = set(df["prev_file_num"].astype(str)) - {"", "nan", "None"}
    superseded = df["file_num"].astype(str).isin(prev)

    df["IS_SUSPECT_FILING"] = suspect.map({True: "True", False: "False"})
    df["IS_SUPERSEDED"] = superseded.map({True: "True", False: "False"})

    keep = ~(suspect | superseded)
    print(f"\n  flagged suspect  : {int(suspect.sum()):,} rows, ${amt[suspect].sum()/1e9:,.2f}B", flush=True)
    print(f"  flagged superseded: {int(superseded.sum()):,} rows, ${amt[superseded].sum()/1e9:,.2f}B", flush=True)
    print(f"  clean spend       : {int(keep.sum()):,} rows, ${amt[keep].sum()/1e9:,.2f}B", flush=True)
    for y, g in df.assign(_a=amt, _k=keep).groupby("CYCLE_FILE"):
        print(f"    {y}: clean ${g.loc[g._k, '_a'].sum()/1e9:,.2f}B of ${g._a.sum()/1e9:,.2f}B raw", flush=True)
    return df


def main() -> int:
    ap = argparse.ArgumentParser(description="Load FEC Schedule E independent expenditures.")
    ap.add_argument("--cycles", default=",".join(YEARS),
                    help=f"comma-separated cycles to load (default {','.join(YEARS)})")
    args = ap.parse_args()
    years = [y.strip() for y in args.cycles.split(",") if y.strip()]

    print(f"=== FEC Independent Expenditures cycles {'+'.join(years)} ===", flush=True)
    df = flag(pd.concat([fetch(y) for y in years], ignore_index=True))
    result = land(df, SID, "https://www.fec.gov/files/bulk-downloads/",
         "FEC Independent Expenditures (Schedule E), 2018-2026; one row = one IE; "
         "SUP_OPP = for/against; filter IS_SUSPECT_FILING and IS_SUPERSEDED to 'False' for real spend.")
    if result.get("status") != "success":
        raise RuntimeError(f"QUALITY GATE FAILED for {SID}: {result}")
    print(f"\nDONE -> LIBRARY_RAW.LANDING.{SID.upper()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
