"""Land the whole BJS NCVS person file, not the first Socrata page.

WHAT STOPPED THE OLD TABLE
  FED_BJS_DATA is 1,000 rows: the onboarding fetch_data hit
  api.ojp.gov/bjsdataset/v1/gcuy-rt5g.csv bare, and Socrata's default $limit
  is 1,000. Probed 2026-09-07: $select=count(*) says 68,852 rows, and
  $limit=50000 is honoured.

WHAT THIS DOES
  Pages the same CSV endpoint with $limit/$offset (ordered by idper so pages
  do not overlap) into LIBRARY_RAW.LANDING.FED_BJS_DATA_FULL, same 37 columns
  as the old table plus _INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256.
  The old table is not touched.

    python scripts/bjs_ncvs_full_load.py          # dry run: page it all, land nothing
    python scripts/bjs_ncvs_full_load.py --run    # land it
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _repage_land as rp  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

SOURCE_ID = "fed_bjs_data_full"
TABLE = "FED_BJS_DATA_FULL"
URL = "https://api.ojp.gov/bjsdataset/v1/gcuy-rt5g.csv"
COUNT_URL = "https://api.ojp.gov/bjsdataset/v1/gcuy-rt5g.json"
PAGE = 25_000
COLUMNS = ["IDPER", "YEARQ", "YEAR", "AGER", "SEX", "HISPANIC", "RACE", "RACE_ETHNICITY",
           "HINCOME1", "HINCOME2", "MARITAL", "POPSIZE", "REGION", "MSA", "LOCALITY",
           "EDUCATN1", "EDUCATN2", "VETERAN", "CITIZEN", "NEWCRIME", "NEWOFF",
           "SERIOUSVIOLENT", "NOTIFY", "VICSERVICES", "LOCATIONR", "DIREL", "WEAPON",
           "WEAPCAT", "INJURY", "SERIOUS", "TREATMENT", "OFFENDERAGE", "OFFENDERSEX",
           "OFFTRACENEW", "WGTVICCY", "SERIES", "NEWWGT"]


def total() -> int:
    r = requests.get(COUNT_URL, params={"$select": "count(*)"}, headers=rp.UA, timeout=60)
    r.raise_for_status()
    return int(r.json()[0]["count"])


def pages():
    offset = 0
    while True:
        r = requests.get(URL, params={"$limit": PAGE, "$offset": offset, "$order": "idper"},
                         headers=rp.UA, timeout=300)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text), dtype=str, keep_default_na=False)
        if df.empty:
            return
        df.columns = [bulk.sf_col(c) for c in df.columns]
        yield df
        if len(df) < PAGE:
            return
        offset += len(df)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="land it; default is dry run")
    ap.add_argument("--append", action="store_true", help="allow landing on top of existing rows")
    args = ap.parse_args()
    n = total()
    print(f"source {URL}\nserver says {n:,} rows; page size {PAGE:,}")
    rp.land_pages(source_id=SOURCE_ID, table=TABLE, source_url=URL, columns=COLUMNS,
                  pages=pages, run=args.run, append=args.append, expected_total=n)


if __name__ == "__main__":
    main()
