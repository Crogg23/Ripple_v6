# PORTAL_CKA_TAMPA_OPEN_DATA_E589C6750A

rows 218  columns 13  scan 3.2s

roles: amount 1, audit 2, category 5, date 2, other 2, who 2

## when

DATE
  2024       104  ###########################
  2026       114  ##############################

INGESTED_AT
  2026       218  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 218 | 0 | 12.1K | 18.20M | 21.79M | 577.62M |

## who

TYPEDATA by rows
       218  Period

TYPEDATA by dollars
     577.62M      218 rows  Period

SRC_SHA256 by rows
       218  d1afb7258193d8b485e7b2b4b060ec2e52de987fbeb4dd9f6b28f3261c362fea

SRC_SHA256 by dollars
     577.62M      218 rows  d1afb7258193d8b485e7b2b4b060ec2e52de987fbeb4dd9f6b28f3261c36

## who x when

TYPEDATA by DATE, dollars = VALUE
  Period                                    2024:108.10M 2026:469.52M

SRC_SHA256 by DATE, dollars = VALUE
  d1afb7258193d8b485e7b2b4b060ec2e52de987f  2024:108.10M 2026:469.52M

## what

C_ORGANIZATION: Neighborhood Empowerment 85%, Community Redevelopment (Chann 15%

CHARTNAME: Growth of City Art Collection 37%, Dollars Spent on the Arts by A 27%, Dollars Spent on the Arts by C 15%, Dollars Spent on the Arts by C 11%, Dollars Spent on the Arts by A 10%

DESCRIPTION: Arts and Cultural Affairs 37%, Dollars Spent on the Arts by A 37%, Arts and Cultural Affairs; Dol 15%, Arts and Cultural Affairs; Dol 11%

CATEGORY: Acquisition Value 16%, Value After Appraisal 16%, Works in Collection 15%, Downtown 8%, West Tampa 8%, East Tampa 8%, Ybor City 6%, Channel District 6%, South Tampa 5%, City-Wide 5%, District 6 3%, At-Large 3%

PERIOD: FY-2024 14%, FY-2023 14%, FY-2021 14%, FY-2022 14%, FY-2020 14%, 2024 6%, 2023 6%, 2022 6%, FY2025 5%, 2026 2%, 2025 2%, 2021 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 215 | 0 | 19651 2; 19650 2; 19390 2; 19389 2 |
| C_ORGANIZATION | category | 2 | 0 | Neighborhood Empowerment 185; Community Redevelopment ( 33 |
| CHARTNAME | category | 5 | 0 | Growth of City Art Collec 80; Dollars Spent on the Arts 59; Dollars Spent on the Arts 33; Dollars Spent on the Arts 25 |
| DESCRIPTION | category | 4 | 0 | Arts and Cultural Affairs 80; Dollars Spent on the Arts 80; Arts and Cultural Affairs 33; Arts and Cultural Affairs 25 |
| CATEGORY | category | 25 | 0 | Acquisition Value 27; Value After Appraisal 27; Works in Collection 26; Downtown 14 |
| SUMMARY | other | 1 | 0 | Total 218 |
| TYPEDATA | who | 1 | 0 | Period 218 |
| DATE | date | 56 | 0 | 07/02/2026 12:31:06 100; 04/07/2024 00:00:00 6; 03/01/2024 15:27:00 6; 03/01/2024 15:30:00 4 |
| PERIOD | category | 34 | 0 | FY-2024 22; FY-2023 22; FY-2021 22; FY-2022 21 |
| VALUE | amount | 127 | 0 | 0.000 45; 30000.000 6; 8546.000 4; 1000.000 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:17:41.62376 218 |
| SOURCE_RUN_ID | audit | 1 | 0 | 94ce93e2-dc9c-4437-b44b-6 218 |
| SRC_SHA256 | who | 1 | 0 | d1afb7258193d8b485e7b2b4b 218 |
