# PORTAL_SOC_TEXAS_OPEN_DATA_A7AB49CB1A

rows 447  columns 7  scan 4.8s

roles: audit 2, category 1, date 2, other 2, who 1

## when

DATE_SUBMITTED
  2023       225  ##############################
  2024        62  ########
  2025        94  #############
  2026        66  #########

INGESTED_AT
  2026       447  ##############################

## who

SRC_SHA256 by rows
       447  35e83159fdceeb6848681790ebf450ca1451a3e681643dc97c3e538ee493b2d8

## who x when

SRC_SHA256 by DATE_SUBMITTED
  35e83159fdceeb6848681790ebf450ca1451a3e6  2023:225 2024:62 2025:94 2026:66

## what

YEAR: 2024 64%, 2025 21%, 2026 15%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 3 | 0 | 2024 287; 2025 94; 2026 66 |
| DATE_SUBMITTED | date | 92 | 0 | 2023-12-14T00:00:00.000 34; 2023-12-15T00:00:00.000 30; 2023-12-06T00:00:00.000 23; 2025-08-21T00:00:00.000 19 |
| POLITICAL_SUBDIVISION | other | 303 | 0 | Karnes County EMS 4; Blanco County ESD 2 4; City of Brownsville 4; City of Tulia 4 |
| NPI | other | 283 | 0 | 1710981774 29; 1194750802 21; 1639103864 9; 1780605311 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:44:12.58911 447 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9793be40-05a2-46c8-960b-8 447 |
| SRC_SHA256 | who | 1 | 0 | 35e83159fdceeb6848681790e 447 |
