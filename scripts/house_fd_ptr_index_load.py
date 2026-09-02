#!/usr/bin/env python3
"""Load the House Clerk financial-disclosure filing index, 2008-present.

One row = one filing logged by the Clerk: annual FD reports AND STOCK Act
periodic transaction reports (FilingType='P'). Filer name, state-district,
filing date, DocID. The DocID keys the public PDF:
  PTRs:   disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{DocID}.pdf
  others: .../public_disc/financial-pdfs/{year}/{DocID}.pdf

This is the machine-readable layer the Clerk publishes; transaction detail
lives inside the PDFs (a parse project, not a landing job). Landing the index
gives who-filed-what-when for every member since 2008 -- the join spine for
any PTR parsing later.

Each year's zip holds exactly two members ({year}FD.txt TSV + .xml twin) --
the .txt is picked BY NAME, never by zip order (zip largest-member trap).

    python scripts/house_fd_ptr_index_load.py          # preview
    python scripts/house_fd_ptr_index_load.py --run    # land it
"""
from __future__ import annotations

import argparse
import io
import sys
import zipfile
from datetime import date
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register  # noqa: E402

SID = "fed_house_fd_ptr_index"
TABLE = SID.upper()
BASE = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126"}
FIRST_YEAR = 2008


def fetch_year(year: int) -> pd.DataFrame | None:
    r = requests.get(f"{BASE}/{year}FD.zip", headers=UA, timeout=300)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    txts = [n for n in zf.namelist() if n.lower().endswith(".txt")]
    if len(txts) != 1:
        raise RuntimeError(f"{year}FD.zip: expected one .txt, got {zf.namelist()}")
    df = pd.read_csv(io.BytesIO(zf.read(txts[0])), sep="\t", dtype=str,
                     encoding="latin-1")
    if "FilingType" not in df.columns:
        raise RuntimeError(f"{year}FD.txt: header drifted, no FilingType column")
    df["INDEX_YEAR"] = str(year)
    return df


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== House Clerk FD/PTR filing index ===", flush=True)
    frames = []
    for year in range(FIRST_YEAR, date.today().year + 1):
        df = fetch_year(year)
        if df is None:
            print(f"  {year}: no zip (404), skipped", flush=True)
            continue
        print(f"  {year}: {len(df):,} filings", flush=True)
        frames.append(df)
    allf = pd.concat(frames, ignore_index=True)
    n_ptr = (allf["FilingType"] == "P").sum()
    print(f"  total {len(allf):,} filings, {n_ptr:,} PTRs", flush=True)
    cfg = {
        "source_id": SID,
        "name": "House financial disclosure filing index (FD + STOCK Act PTRs)",
        "publisher": "Clerk of the U.S. House of Representatives",
        "url": "https://disclosures-clerk.house.gov/FinancialDisclosure",
        "description": "Every financial-disclosure filing logged by the House Clerk since "
                       "2008: annual FD reports and STOCK Act periodic transaction reports "
                       "(FilingType='P'). Filer, state-district, filing date, DocID keying "
                       "the public PDF. Transaction detail stays in the PDFs.",
        "jurisdiction": "federal", "category": "Ethics & disclosure",
        "subcategory": "Congressional stock trades",
        "unit_of_observation": "one row = one filing (report-level, not transaction-level)",
        "geographic_scope": "US", "access_method": "bulk_download", "format": "tsv in zip",
        "auth": {"type": "none"}, "cost": "free",
        "update_cadence": "annual zip republished daily as filings arrive",
        "volume": "roughly 600-3,500 filings per year since 2008; ~8K PTRs total",
        "license_terms": "public domain",
        "join_keys": "Last+First+StateDst (member), DocID (PDF)",
        "accountability_relevance": "Who filed stock-trade disclosures and when; House half "
                                    "next to FED_SENATE_STOCK_WATCHER. PDF parse project "
                                    "unlocks transaction detail later.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/house_fd_ptr_index_load.py (snapshot-replace, "
                 "2008-present, ~1.6K-3K filings/year).",
    }
    status = load_and_register(allf, SID, TABLE, f"{BASE}/<year>FD.zip", cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
