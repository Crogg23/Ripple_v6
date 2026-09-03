# PORTAL_SOC_AUSTIN_OPEN_DATA_0B4C639A1C

rows 526  columns 9  scan 2.5s

roles: audit 2, category 3, date 2, other 2, who 1

## when

DATE
  2022       148  ############################
  2023       161  ##############################
  2024        95  ##################
  2025        84  ################
  2026        38  #######

INGESTED_AT
  2026       526  ##############################

## who

SRC_SHA256 by rows
       526  f58ccbddeb7ea1d20ae75b592b35b0f54b3416eb983716f72818083b6d1f39d0

## who x when

SRC_SHA256 by DATE
  f58ccbddeb7ea1d20ae75b592b35b0f54b3416eb  2022:148 2023:161 2024:95 2025:84 2026:38

## what

YEAR_DATE: 2023 31%, 2022 28%, 2024 18%, 2025 16%, 2026 7%

NUM_MONTH_DATE: 3 16%, 1 12%, 4 11%, 2 10%, 5 10%, 6 8%, 7 7%, 11 6%, 10 6%, 8 5%, 12 4%, 9 4%

REASON: Retirement 61%, Resignation 36%, Death 2%, Termination 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| EMPLOYEE_ID | other | 520 | 0 | RMMOAMIP 4; RMMRPSEI 4; RMRENNEG 4; RMMIPPMO 3 |
| DATE | date | 397 | 0 | 2023-03-31T00:00:00.000 15; 2022-05-31T00:00:00.000 8; 2023-03-30T00:00:00.000 7; 2022-09-30T00:00:00.000 6 |
| YEAR_DATE | category | 5 | 0 | 2023 161; 2022 148; 2024 95; 2025 84 |
| NUM_MONTH_DATE | category | 12 | 0 | 3 84; 1 64; 4 56; 2 54 |
| REASON | category | 4 | 0 | Retirement 323; Resignation 189; Death 8; Termination 6 |
| COUNT_DISTINCT_EIN | other | 1 | 0 | 1 526 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:41:18.13367 526 |
| SOURCE_RUN_ID | audit | 1 | 0 | 23dbe3e2-6788-4669-825c-f 526 |
| SRC_SHA256 | who | 1 | 0 | f58ccbddeb7ea1d20ae75b592 526 |
