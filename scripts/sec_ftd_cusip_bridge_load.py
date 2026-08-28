#!/usr/bin/env python3
"""Deterministic loader for the SEC fails-to-deliver CUSIP->issuer bridge.

One row = one settlement-date x CUSIP fails-to-deliver record from the two
most recent half-month SEC FOIA files. Loaded here for the CUSIP + SYMBOL +
DESCRIPTION (issuer name) bridge, not for the fails quantities themselves.
(No cleaner free official SEC CUSIP->CIK mapping exists: company_tickers.json
is CIK->ticker only, and 13F CUSIPs are per-filing. Verified 2026-08-27.)

Auto-discovers the two most recent files by probing the SEC's fixed
cnsfailsYYYYMM[ab].zip naming backward from the current month.

    python scripts/sec_ftd_cusip_bridge_load.py          # preview
    python scripts/sec_ftd_cusip_bridge_load.py --run    # land it
"""
from __future__ import annotations
import argparse, datetime as dt, io, sys, zipfile
import pandas as pd
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _small_flat_loader import load_and_register

SID = "fed_sec_ftd_cusip_bridge"
TABLE = SID.upper()
PAGE_URL = "https://www.sec.gov/data/foiadocsfailsdatahtm"
BASE = "https://www.sec.gov/files/data/fails-deliver-data/cnsfails{ym}{half}.zip"
# SEC requires a declared UA with contact info on all automated requests.
HEADERS = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}


def discover_latest(n: int = 2) -> list[str]:
    """Return URLs of the n most recent half-month files, newest first."""
    today = dt.date.today()
    candidates = []
    y, m = today.year, today.month
    for _ in range(8):  # look back up to 4 months
        for half in ("b", "a"):
            candidates.append(BASE.format(ym=f"{y}{m:02d}", half=half))
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    found = []
    for url in candidates:
        try:
            r = requests.head(url, headers=HEADERS, timeout=30)
        except requests.RequestException:
            continue
        if r.status_code == 200:
            found.append(url)
            if len(found) == n:
                return found
    return found


def fetch_one(url: str) -> pd.DataFrame:
    r = requests.get(url, headers=HEADERS, timeout=300)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        name = zf.namelist()[0]
        with zf.open(name) as f:
            df = pd.read_csv(f, sep="|", dtype=str, low_memory=False,
                             encoding="cp1252", encoding_errors="replace")
    # Trailing junk line ("Trailer record count" style) has null CUSIP; keep
    # only real records.
    df = df[df["CUSIP"].notna()]
    df["SRC_FILE"] = url.rsplit("/", 1)[-1]
    return df


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    print("=== SEC fails-to-deliver CUSIP bridge (2 most recent half-months) ===", flush=True)
    urls = discover_latest(2)
    if len(urls) < 2:
        print(f"ERROR: only found {len(urls)} recent FTD files: {urls}", flush=True)
        return 1
    print("files:", ", ".join(u.rsplit('/', 1)[-1] for u in urls), flush=True)
    df = pd.concat([fetch_one(u) for u in urls], ignore_index=True)
    cfg = {
        "source_id": SID,
        "name": "SEC Fails-to-Deliver CUSIP-Issuer Bridge",
        "publisher": "U.S. Securities and Exchange Commission (SEC)",
        "url": PAGE_URL,
        "description": "The two most recent half-month SEC fails-to-deliver files, kept as a "
                       "CUSIP -> ticker symbol -> issuer-name bridge covering every security "
                       "with a settlement fail in the window.",
        "jurisdiction": "federal", "category": "Finance", "subcategory": "Securities",
        "unit_of_observation": "one row = one settlement date x CUSIP fails record",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "twice monthly",
        "volume": f"{len(df):,} rows", "license_terms": "U.S. Government work, public domain",
        "join_keys": "CUSIP, SYMBOL",
        "accountability_relevance": "Free CUSIP->issuer-name/ticker crosswalk; bridges 13F "
                                    "holdings and other CUSIP-keyed data to named issuers.",
        "priority_tier": "2", "landing_table": TABLE,
        "notes": "Loaded by scripts/sec_ftd_cusip_bridge_load.py (snapshot-replace, "
                 "auto-discovers the 2 newest cnsfailsYYYYMM[ab].zip files).",
    }
    status = load_and_register(df, SID, TABLE, PAGE_URL, cfg, args.run)
    return 0 if status in ("preview", "skipped", "success") else 1


if __name__ == "__main__":
    sys.exit(main())
