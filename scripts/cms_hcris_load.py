#!/usr/bin/env python3
"""Load the CMS Hospital Provider Cost Report, every fiscal year 2011 to 2023.

The warehouse held ONE vintage: 6,103 rows, fiscal years ending in 2022-2023.
CMS publishes one file per fiscal year and all thirteen are still live, so the
other twelve years were simply never fetched. That single vintage is what blocks
docket questions E43, E47, E48 and 11 -- every one of them asks how a hospital
CHANGED, and one snapshot cannot answer a change question.

MEASURED 2026-09-06, not assumed:

  the files are small
      4.1 MB and about 6,100 rows each, not the 60 MB the handoff guessed.
      Thirteen years is roughly 80,000 rows and 53 MB, which fits in memory
      comfortably. No chunking needed here; that would be cargo cult.

  the header never moves
      117 columns, byte-identical across 2011, 2017 and 2023. So a year is a
      straight append, not a schema reconciliation. The loader still ASSERTS it
      rather than trusting it, because a silent column shift is how a wide
      financial table starts lying.

  the URLs are resolved live, never frozen
      data.cms.gov/data.json is read on every run and the per-year CSV links are
      pulled out of the dataset's distributions. A frozen manifest is exactly
      what broke the USAspending server-side spec earlier today, when all 20 of
      its pinned URLs 404'd after the publisher rotated the month.

GRAIN CHANGES, and downstream feels it: the mart goes from one row per hospital
to one row per hospital per fiscal year. Its unique test has to move to
PROVIDER_CCN plus SOURCE_FILE_YEAR, and findings E43, E47 and E48 change shape
because they can finally see a before and an after.

COLUMN NAMES arrive human-readable -- 'Provider CCN', 'FTE - Employees on
Payroll' -- and ingest._stringify sanitises them to PROVIDER_CCN and
FTE___EMPLOYEES_ON_PAYROLL on the way into landing. Do not rename here; the
existing table already carries the sanitised forms and a hand-rename would drift
from whatever the house sanitiser does next.

SOURCE_FILE_YEAR is the CMS file's own year label. It is NOT the same as the
fiscal year in FISCAL_YEAR_END_DATE, which varies per hospital -- Irwin County
Hospital's 2023 report covers 2022-12-01 to 2023-01-31. Group by the stamp for
"which file", by the date for "which period".
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "scripts"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

from land_frame import land  # noqa: E402

CATALOG = "https://data.cms.gov/data.json"
DATASET = "Hospital Provider Cost Report"
SID = "fed_cms_hcris"
UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

FIRST_YEAR, LAST_YEAR = 2011, 2023


def resolve() -> dict[str, str]:
    """year -> CSV url, read live from the CMS catalog. Never a pinned list."""
    r = requests.get(CATALOG, headers=UA, timeout=120)
    r.raise_for_status()
    sets = [d for d in r.json().get("dataset", []) if d.get("title") == DATASET]
    if len(sets) != 1:
        raise SystemExit(f"expected one '{DATASET}' dataset in the catalog, found {len(sets)}")
    urls = {}
    for dist in sets[0].get("distribution") or []:
        u = dist.get("downloadURL") or ""
        m = re.search(r"CostReport_(\d{4})_", u)
        if m and u.lower().endswith(".csv"):
            urls[m.group(1)] = u
    print(f"  catalog lists {len(urls)} yearly files: {min(urls)} to {max(urls)}", flush=True)
    return urls


def fetch(year: str, url: str) -> pd.DataFrame:
    r = requests.get(url, headers=UA, timeout=600)
    r.raise_for_status()
    # dtype=str and no NA coercion: this is the raw layer, and several columns
    # are money that must not become floats on the way in.
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, keep_default_na=False,
                     na_values=[], encoding="utf-8-sig", low_memory=False)
    df["SOURCE_FILE_YEAR"] = year
    print(f"  {year}: {len(df):,} rows, {len(r.content)/1e6:.1f} MB", flush=True)
    return df


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--years", default="",
                    help=f"comma-separated years (default {FIRST_YEAR}-{LAST_YEAR})")
    ap.add_argument("--dry-run", action="store_true",
                    help="fetch and check the shape, land nothing")
    args = ap.parse_args()

    print(f"=== CMS Hospital Provider Cost Report ===", flush=True)
    urls = resolve()
    want = ([y.strip() for y in args.years.split(",") if y.strip()]
            if args.years else [str(y) for y in range(FIRST_YEAR, LAST_YEAR + 1)])
    missing = [y for y in want if y not in urls]
    if missing:
        raise SystemExit(f"the catalog has no file for {missing}; it lists {sorted(urls)}")

    frames = []
    header = None
    for y in want:
        df = fetch(y, urls[y])
        cols = [c for c in df.columns if c != "SOURCE_FILE_YEAR"]
        if header is None:
            header = cols
        elif cols != header:
            # A silent column shift is how a wide financial table starts lying.
            only_new = [c for c in cols if c not in header]
            only_old = [c for c in header if c not in cols]
            raise SystemExit(
                f"{y} has a different header: {len(cols)} columns against "
                f"{len(header)}.\n  only in {y}: {only_new[:6]}\n  missing from {y}: {only_old[:6]}")
        frames.append(df)

    out = pd.concat(frames, ignore_index=True)
    # The raw header is human-readable; landing holds the sanitised form. Find
    # the CCN column by shape rather than by either spelling.
    ccn = next((c for c in out.columns if c.strip().lower().replace("_", " ") == "provider ccn"), None)
    if not ccn:
        raise SystemExit(f"no Provider CCN column in {list(out.columns)[:8]}")
    print(f"\n  total {len(out):,} rows across {len(want)} years, "
          f"{out[ccn].nunique():,} distinct hospitals", flush=True)
    per = out.groupby("SOURCE_FILE_YEAR")[ccn].nunique()
    print(f"  hospitals per year: {per.min():,} to {per.max():,}", flush=True)
    dupes = int(out.duplicated([ccn, "SOURCE_FILE_YEAR"]).sum())
    print(f"  duplicate hospital-year rows: {dupes:,}", flush=True)

    if args.dry_run:
        print("DRY RUN: nothing landed", flush=True)
        return 0

    result = land(out, SID, "https://data.cms.gov/provider-compliance/cost-reports/hospital-provider-cost-report",
                  "CMS Hospital Provider Cost Report, fiscal years 2011-2023; one row = one "
                  "hospital-year; SOURCE_FILE_YEAR is the CMS file label, not the hospital's "
                  "own fiscal period.")
    if result.get("status") != "success":
        raise RuntimeError(f"QUALITY GATE FAILED for {SID}: {result}")
    print(f"\nDONE -> LIBRARY_RAW.LANDING.{SID.upper()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
