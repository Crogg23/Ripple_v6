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

# FEMA disaster declarations: 70,402 rows, 29 cols, one row per disaster x designated area. Probed 2026-09-10.
SPECS.append({
    "source_id": "FED_FEMA_DISASTER_DECLARATIONS",
    "name": "FEMA Disaster Declarations Summaries",
    "publisher": "FEMA",
    "url": "https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2",
    "download_url": "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv",
    "kind": "url_csv",
    "loader": "phase5",
    "key_cols": [{"col": "id", "as": "ID"}],
    "join_keys": "DISASTERNUMBER -> FEMA IA registrations; FIPSSTATECODE||FIPSCOUNTYCODE -> county FIPS",
    "category": "Housing",
    "subcategory": "Disaster Declarations",
    "unit_of_observation": "one row = one declaration x one designated area; disasterNumber repeats",
    "update_cadence": "daily",
    "temporal_coverage": "1953 to today",
    "accountability_relevance": "Which counties got declared, when, for what, with which programs turned on. The repeat-disaster county table.",
    "priority_tier": "1",
    "notes": "Landed 2026-09-10, phase 2. Served gzip on the wire; requests inflates it. 5,264 distinct disaster numbers over 70,402 rows.",
})

# NPPES monthly deactivations: one xlsx in a zip, title row then header, 351,912 data rows. Probed 2026-09-10.
SPECS.append({
    "source_id": "FED_CMS_NPPES_DEACTIVATED",
    "name": "NPPES Deactivated NPI Report",
    "publisher": "CMS",
    "url": "https://download.cms.gov/nppes/NPI_Files.html",
    "download_url": "https://download.cms.gov/nppes/NPPES_Deactivated_NPI_Report_081026_V2.zip",
    "kind": "zip_xlsx",
    "skip_rows": 1,
    "loader": "phase5",
    "key_cols": [{"col": "NPI", "as": "NPI"}],
    "join_keys": "NPI -> FED_CMS_NPPES",
    "category": "Health",
    "subcategory": "Provider Enumeration",
    "unit_of_observation": "one row = one deactivated NPI with its deactivation date",
    "update_cadence": "monthly",
    "temporal_coverage": "all deactivations on file as of 2026-08-10",
    "accountability_relevance": "The doctors who left: the only public date-stamped exit list. Fixes the NPPES snapshot problem for counts by year.",
    "priority_tier": "1",
    "notes": "Landed 2026-09-10, phase 2. Zip member is an xlsx with a title row above the header; the file name carries MMDDYY and rotates monthly.",
})

