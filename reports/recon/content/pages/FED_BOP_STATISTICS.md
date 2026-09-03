# FED_BOP_STATISTICS

rows 50  columns 11  scan 2.6s

roles: audit 2, category 3, date 1, empty 2, other 1, who 2

## when

REPORT_DATE
  2026        50  ##############################

## who

CATEGORY by rows
        50  Federal Bureau of Prisons

_SRC_SHA256 by rows
        50  0ef7d0fc4089a902404c86b0632eb108c4e80b0cd425374443aebabf56a99acf

## who x when

CATEGORY by REPORT_DATE
  Federal Bureau of Prisons                 2026:50

_SRC_SHA256 by REPORT_DATE
  0ef7d0fc4089a902404c86b0632eb108c4e80b0c  2026:50

## what

METRIC_NAME: 0 56%, 1 16%, 2 12%, Receive Code is always 2%, Location 2%, Release Date 2%, Sex 2%, Race 2%, Age 2%, Register # 2%, Name 2%

METRIC_VALUE: Search 15%, Change 8%, Population 8%, FY 8%, All Facilities 8%, Facility 8%, All States  Alabama  Alaska  A 8%, State 8%, All Regions  Mid-Atlantic Regi 8%, Region 8%, Hol 8%, Sat 8%

SOURCE_URL: https://www.bop.gov/inmateloc/ 62%, https://www.bop.gov/about/stat 18%, https://www.bop.gov/inmates/vi 18%, https://www.bop.gov/inmates/co 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 1 | 0 | 2026-07-01 50 |
| CATEGORY | who | 1 | 0 | Federal Bureau of Prisons 50 |
| METRIC_NAME | category | 11 | 0 | 0 28; 1 8; 2 6; Receive Code is always 1 |
| METRIC_VALUE | category | 48 | 0 | Search 2; Change 1; Population 1; FY 1 |
| METRIC_UNIT | other | 1 | 0 | count 50 |
| FACILITY_TYPE | empty | 1 | 50 |  |
| STATE_FIPS | empty | 1 | 50 |  |
| SOURCE_URL | category | 4 | 0 | https://www.bop.gov/inmat 31; https://www.bop.gov/about 9; https://www.bop.gov/inmat 9; https://www.bop.gov/inmat 1 |
| _INGESTED_AT | audit | 1 | 0 | 1782941026761043 50 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 11ee6bd4-1fa8-4364-b293-9 50 |
| _SRC_SHA256 | who | 1 | 0 | 0ef7d0fc4089a902404c86b06 50 |
