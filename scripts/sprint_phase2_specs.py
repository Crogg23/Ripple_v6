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

# EIA-860 prior years, option C chosen by Chris 2026-09-10: plant and generator per year, every sheet,
# SHEET_NAME column first. The live FED_EIA860_3_1_GENERATOR reads only the Operable sheet, so retired
# units were never landed; the Retired and Canceled sheet is the gap the ledger names.
_EIA_URL = {y: f"https://www.eia.gov/electricity/data/eia860/archive/xls/eia860{y}.zip" for y in range(2019, 2024)}
for _y in range(2019, 2024):
    for _mem, _tag, _grain in (("2___Plant", "PLANT", "one row = one plant"),
                               ("3_1_Generator", "GENERATOR", "one row = one generator x one sheet: Operable, Proposed, Retired and Canceled")):
        SPECS.append({
            "source_id": f"FED_EIA860_{_tag}_Y{_y}",
            "name": f"EIA-860 {_tag.title()} {_y}, all sheets",
            "publisher": "EIA",
            "url": "https://www.eia.gov/electricity/data/eia860/",
            "download_url": _EIA_URL[_y],
            "kind": "zip_xlsx",
            "member": _mem,
            "sheets": "all",
            "skip_rows": 1,
            "loader": "phase5",
            "key_cols": [{"col": "Plant Code", "as": "PLANT_CODE"}],
            "join_keys": "PLANT_CODE = ORIS plant id -> eGRID ORISPL, EPA CAMPD; UTILITY_ID",
            "category": "Energy",
            "subcategory": "Power Plants",
            "unit_of_observation": _grain,
            "update_cadence": "annual",
            "temporal_coverage": f"form year {_y}",
            "accountability_relevance": "Plant and generator roster by year, retired units included. The before and after for closures.",
            "priority_tier": "1",
            "notes": (f"Landed 2026-09-10, phase 3. Year {_y} archive zip, member {_mem}, every sheet unioned on the "
                      "superset of headers with SHEET_NAME first. Row 0 is a title, header is row 1. "
                      "Sibling unsuffixed FED_EIA860_* tables are the 2024 vintage, Operable sheet only."),
        })

# eGRID plant sheet by year. 2022 is already landed as FED_EPA_EGRID_PLANT_2022.
_EGRID = {
    2019: "https://www.epa.gov/sites/default/files/2021-02/egrid2019_data.xlsx",
    2020: "https://www.epa.gov/system/files/documents/2022-09/eGRID2020_Data_v2.xlsx",
    2021: "https://www.epa.gov/system/files/documents/2023-01/eGRID2021_data.xlsx",
    2023: "https://www.epa.gov/system/files/documents/2025-06/egrid2023_data_rev2.xlsx",
}
for _y, _u in _EGRID.items():
    SPECS.append({
        "source_id": f"FED_EPA_EGRID_PLANT_{_y}",
        "name": f"EPA eGRID plant file {_y}",
        "publisher": "EPA",
        "url": "https://www.epa.gov/egrid",
        "download_url": _u,
        "kind": "url_xlsx",
        "sheet": f"PLNT{str(_y)[2:]}",
        "skip_rows": 1,
        "loader": "phase5",
        "key_cols": [{"col": "ORISPL", "as": "ORISPL"}],
        "join_keys": "ORISPL -> EIA-860 PLANT_CODE, EPA CAMPD; PSTATABB; FIPSST + FIPSCNTY",
        "category": "Environment",
        "subcategory": "Power Plant Emissions",
        "unit_of_observation": "one row = one plant x one data year",
        "update_cadence": "annual",
        "temporal_coverage": f"data year {_y}",
        "accountability_relevance": "Plant emissions, capacity, fuel and county by year. The other side of the closure story.",
        "priority_tier": "1",
        "notes": (f"Landed 2026-09-10, phase 3. Sheet PLNT{str(_y)[2:]}; row 0 is the long-name caption, row 1 the code header. "
                  "Sibling FED_EPA_EGRID_PLANT_2022 landed earlier by another path."),
    })

# USAspending prime contracts, one table per fiscal year from the monthly award archive. Chris 2026-09-10: "do it".
# The archive carries every column, 297 in FY2024, including the county FIPS, agency codes and entity flags
# the 36-column R2 table lacks. One zip a year, 1M-row csv members, direct download; no API generation jobs.
_USA_ARCHIVE = "https://files.usaspending.gov/award_data_archive/FY{y}_All_Contracts_Full_20260806.zip"
for _y in range(2007, 2027):
    SPECS.append({
        "source_id": f"FED_USASPENDING_CONTRACTS_FY{_y}",
        "name": f"USAspending prime contract transactions FY{_y}, full archive columns",
        "publisher": "Treasury / USAspending",
        "url": "https://www.usaspending.gov/download_center/award_data_archive",
        "download_url": _USA_ARCHIVE.format(y=_y),
        "kind": "zip_multi_csv",
        "loader": "phase5",
        "key_cols": [{"col": "contract_transaction_unique_key", "as": "CONTRACT_TRANSACTION_UNIQUE_KEY"}],
        "join_keys": ("RECIPIENT_UEI, RECIPIENT_PARENT_UEI, CAGE_CODE; PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE; "
                      "AWARDING_AGENCY_CODE; NAICS_CODE"),
        "category": "Economics",
        "subcategory": "Federal Contracts",
        "unit_of_observation": "one row = one contract transaction; CONTRACT_TRANSACTION_UNIQUE_KEY is unique",
        "update_cadence": "monthly archive",
        "temporal_coverage": f"fiscal year {_y}, archive stamped 2026-08-06",
        "accountability_relevance": "Every contract action with county FIPS, agency code and entity type. Joins contracts to storms, aid, mortgages and jobs at county grain.",
        "priority_tier": "1",
        "notes": (f"Landed 2026-09-10, phase 2. FY{_y} archive zip, all csv members concatenated, headers checked equal. "
                  "All columns TEXT. FED_USASPENDING_CONTRACTS_FULL_R2 is the 36-column API pull and stays as is."),
    })

# Census national county list, 2020 vintage: the clean county name to FIPS dimension. Landed 2026-09-10
# because REF__DIM_GEOGRAPHY fans out and misses counties, see traps.md.
SPECS.append({
    "source_id": "FED_CENSUS_COUNTY_2020",
    "name": "Census national county codes 2020",
    "publisher": "Census Bureau",
    "url": "https://www.census.gov/library/reference/code-lists/ansi.html",
    "download_url": "https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt",
    "kind": "url_csv",
    "delimiter": "|",
    "loader": "phase5",
    "key_cols": [{"col": "COUNTYNS", "as": "COUNTYNS"}],
    "join_keys": "STATEFP||COUNTYFP = 5-digit county FIPS; STATE abbr; COUNTYNAME with County/Parish/Borough suffix",
    "category": "Reference",
    "subcategory": "Geography",
    "unit_of_observation": "one row = one county or county equivalent, 3,235 rows",
    "update_cadence": "decennial",
    "temporal_coverage": "2020 vintage",
    "accountability_relevance": "The county name to FIPS lookup every name-only county column needs.",
    "priority_tier": "1",
    "notes": "Landed 2026-09-10. Pipe-delimited, 7 columns, FIPS unique. COUNTYNAME carries the legal suffix: County, Parish, Borough, Census Area, Municipio, city.",
})

