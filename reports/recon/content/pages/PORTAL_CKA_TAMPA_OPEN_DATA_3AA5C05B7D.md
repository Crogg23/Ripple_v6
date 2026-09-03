# PORTAL_CKA_TAMPA_OPEN_DATA_3AA5C05B7D

rows 28  columns 13  scan 4.7s

roles: amount 1, audit 2, category 4, date 2, other 1, who 4

## when

DATE
  2023        28  ##############################

INGESTED_AT
  2026        28  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 28 | 0 | 1 | 10.46 | 11 | 71 |

## who

CHARTNAME by rows
        28  Total Number of City Planning Studies

CHARTNAME by dollars
          71       28 rows  Total Number of City Planning Studies

C_ORGANIZATION by rows
        28  Dvlpment and Econ Opportunity (Economic Opportunity Administrator)

C_ORGANIZATION by dollars
          71       28 rows  Dvlpment and Econ Opportunity (Economic Opportunity Administ

DESCRIPTION by rows
        28  Total Number of City Planning Studies

DESCRIPTION by dollars
          71       28 rows  Total Number of City Planning Studies

SRC_SHA256 by rows
        28  263c1252713ea585b52f8361c3c03c719ab47ab8ccc8371e6c4b1f696b43ef6d

SRC_SHA256 by dollars
          71       28 rows  263c1252713ea585b52f8361c3c03c719ab47ab8ccc8371e6c4b1f696b43

## who x when

CHARTNAME by DATE, dollars = VALUE
  Total Number of City Planning Studies     2023:71

C_ORGANIZATION by DATE, dollars = VALUE
  Dvlpment and Econ Opportunity (Economic   2023:71

## what

ID: 9026 8%, 9025 8%, 9024 8%, 9023 8%, 8513 8%, 8512 8%, 8511 8%, 8510 8%, 8509 8%, 8508 8%, 8507 8%, 8506 8%

CATEGORY: Project 54%, Type - NA 4%, Lead Department - NA 4%, Status - NA 4%, Coastal Planning 4%, Comprehensive Planning 4%, Housing 4%, Natural Resource Planning 4%, Neighborhoods & Corridors 4%, Transportation 4%, Planning & Development 4%, Parks & Recreation 4%

TYPEDATA: Date 54%, Period 46%

PERIOD: 2023 9%, 2022 9%, 2021 9%, 2020 9%, 2019 9%, 2018 9%, 2017 9%, 2016 9%, 2015 9%, 2014 9%, 2013 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | category | 28 | 0 | 9026 1; 9025 1; 9024 1; 9023 1 |
| C_ORGANIZATION | who | 1 | 0 | Dvlpment and Econ Opportu 28 |
| CHARTNAME | who | 1 | 0 | Total Number of City Plan 28 |
| DESCRIPTION | who | 1 | 0 | Total Number of City Plan 28 |
| CATEGORY | category | 16 | 0 | Project 13; Type - NA 1; Lead Department - NA 1; Status - NA 1 |
| SUMMARY | other | 1 | 0 | Total 28 |
| TYPEDATA | category | 2 | 0 | Date 15; Period 13 |
| DATE | date | 4 | 0 | 02/17/2023 00:00:00 19; 02/23/2023 00:00:00 4; 02/17/2023 14:24:00 4; 02/17/2023 14:23:00 1 |
| PERIOD | category | 14 | 15 | 2023 1; 2022 1; 2021 1; 2020 1 |
| VALUE | amount | 7 | 0 | 1.000 9; 0.000 6; 3.000 5; 2.000 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:10:22.26233 28 |
| SOURCE_RUN_ID | audit | 1 | 0 | 86f9c5a1-4726-489c-b642-8 28 |
| SRC_SHA256 | who | 1 | 0 | 263c1252713ea585b52f8361c 28 |
