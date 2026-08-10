#!/usr/bin/env python3
"""Deterministic loader for SEC EDGAR company_tickers_exchange.json.

Re-ingest of a broken 2026-08 load that landed the whole JSON file as ONE row.
The file is a columnar JSON: {"fields": [...], "data": [[...], ...]}. One row =
one listed company (CIK, name, ticker, exchange).

    python scripts/sec_tickers_exchange_load.py          # preview
    python scripts/sec_tickers_exchange_load.py --run    # land it
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_sec_edgar_company_tickers_exchange"
TABLE = SID.upper()
URL = "https://www.sec.gov/files/company_tickers_exchange.json"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== SEC EDGAR company tickers + exchange ===", flush=True)
    r = requests.get(URL, timeout=120,
                     headers={"User-Agent": "ripple-research w.rogers9999@gmail.com"})
    r.raise_for_status()
    payload = r.json()
    df = pd.DataFrame(payload["data"], columns=payload["fields"])
    cfg = {
        "source_id": SID,
        "name": "SEC EDGAR Company Tickers + Exchange",
        "publisher": "U.S. Securities and Exchange Commission",
        "url": URL,
        "description": "SEC's official CIK-to-ticker-to-exchange map: one row per listed "
                       "company registration (CIK, company name, ticker, exchange).",
        "jurisdiction": "federal", "category": "Finance", "subcategory": "Securities reference",
        "unit_of_observation": "one row = one CIK+ticker listing",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "json",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "daily",
        "volume": f"{len(df):,} rows", "license_terms": "US Government public data",
        "join_keys": "cik, ticker",
        "accountability_relevance": "The canonical CIK<->ticker bridge for joining SEC filings "
                                    "to market identifiers across the platform.",
    }
    status = load_and_register(df, SID, TABLE, URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
