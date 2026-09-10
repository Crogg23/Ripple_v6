"""Phase 2 specs, 2026-09-10: HMDA LAR 2018-2024, one table per year.

Probe 2026-09-10: ffiec.cfpb.gov data-browser nationwide csv, one file per year,
Range supported, 99 columns, header present. Row counts from the same API's
aggregations endpoint summed over actions_taken 1-8:

  2018 15,138,510   2019 17,573,963   2020 25,699,043   2021 26,269,980
  2022 16,125,975   2023 11,564,178   2024 12,259,199      total 124,630,848

Chris asked for state by year. The nationwide file is the same rows with
STATE_CODE on every row, 7 downloads instead of 364, so that is the fetch.
One table per year follows the CMS year-series shape. No row key exists in the
public LAR; LEI is the join key and repeats. Every file is over 5M rows: fast loader.
"""

SPECS = [
    {
        "source_id": f"FED_CFPB_HMDA_LAR_{y}",
        "name": f"HMDA Loan Application Register {y}, nationwide",
        "publisher": "CFPB / FFIEC",
        "url": "https://ffiec.cfpb.gov/data-browser/",
        "download_url": f"https://ffiec.cfpb.gov/v2/data-browser-api/view/nationwide/csv?years={y}",
        "kind": "url_csv",
        "encoding": "utf-8-sig",
        "loader": "phase5",
        "key_cols": [{"col": "lei", "as": "LEI"}],
        "join_keys": "LEI; STATE_CODE + COUNTY_CODE (5-digit FIPS); CENSUS_TRACT",
        "category": "Housing",
        "subcategory": "Mortgage Lending",
        "unit_of_observation": "one row = one loan application or purchased loan; no row key in the public file",
        "update_cadence": "annual",
        "temporal_coverage": f"activity year {y}",
        "accountability_relevance": "Every mortgage application in the country with lender, county, tract, action, denial reason, race, income. The redlining and disaster-lending table by year.",
        "priority_tier": "1",
        "notes": (f"Landed 2026-09-10, phase 2. Nationwide file for {y} from the data-browser API. "
                  "All columns TEXT. Sibling FED_CFPB_HMDA_HISTORIC covers 2007-2017 with a different, pre-2018 layout."),
    }
    for y in range(2018, 2025)
]
