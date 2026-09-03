# PORTAL_CKA_TAMPA_OPEN_DATA_C8043A5DF9

rows 69  columns 13  scan 4.1s

roles: amount 1, audit 2, category 4, date 2, other 2, who 3

## when

DATE
  2021         6  ###
  2026        63  ##############################

INGESTED_AT
  2026        69  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 69 | 0 | 94 | 17.4K | 21.2K | 125.2K |

## who

C_ORGANIZATION by rows
        69  Parks & Recreation

C_ORGANIZATION by dollars
      125.2K       69 rows  Parks & Recreation

TYPEDATA by rows
        69  Period

TYPEDATA by dollars
      125.2K       69 rows  Period

SRC_SHA256 by rows
        69  65924b026b552d8690809083f665dde024f3c2bc97d89e9808991d077314460c

SRC_SHA256 by dollars
      125.2K       69 rows  65924b026b552d8690809083f665dde024f3c2bc97d89e9808991d077314

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Parks & Recreation                        2021:2.0K 2026:123.2K

TYPEDATA by DATE, dollars = VALUE
  Period                                    2021:2.0K 2026:123.2K

## what

CHARTNAME: Total Tree-Mendous Planted by  49%, Total Enrollments by Season an 23%, Combined Trees Planted for all 16%, Total Tree-Mendous Planted 9%, Total Enrollments by School Ye 3%

DESCRIPTION: Total Tree-Mendous Planted by  49%, Total Enrollments by Season an 23%, Combined Trees Planted for all 16%, Total Tree-Mendous Planted 9%, Total Enrollments by School Ye 3%

CATEGORY: Trees 41%, Summer: Jun-Aug 12%, Other 10%, Fall/Winter: Sep-Dec 10%, Spring: Jan-May 7%, Afterschool 5%, Yellow Tabebuia 2%, Sycamore 2%, Sweet Gum 2%, Slash Pine 2%, Shrubs 2%, Scrambled Egg Tree 2%

PERIOD: CY-2024 14%, CY-2023 14%, CY-2025 14%, CY-2022 11%, FY-2021 7%, FY-2020 7%, FY-2019 7%, FY-2018 7%, FY-2017 7%, FY-2016 7%, School Year 24-25 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 58 | 0 | 11 2; 10 2; 9 2; 8 2 |
| C_ORGANIZATION | who | 1 | 0 | Parks & Recreation 69 |
| CHARTNAME | category | 5 | 0 | Total Tree-Mendous Plante 34; Total Enrollments by Seas 16; Combined Trees Planted fo 11; Total Tree-Mendous Plante 6 |
| DESCRIPTION | category | 5 | 0 | Total Tree-Mendous Plante 34; Total Enrollments by Seas 16; Combined Trees Planted fo 11; Total Tree-Mendous Plante 6 |
| CATEGORY | category | 40 | 0 | Trees 17; Summer: Jun-Aug 5; Other 4; Fall/Winter: Sep-Dec 4 |
| SUMMARY | other | 1 | 0 | Total 69 |
| TYPEDATA | who | 1 | 0 | Period 69 |
| DATE | date | 3 | 0 | 07/02/2026 12:30:30 63; 07/26/2021 13:47:00 5; 07/26/2021 00:00:00 1 |
| PERIOD | category | 19 | 34 | CY-2024 4; CY-2023 4; CY-2025 4; CY-2022 3 |
| VALUE | amount | 51 | 0 | 0.000 17; 2.000 2; 1.000 2; 94.000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:13:18.89173 69 |
| SOURCE_RUN_ID | audit | 1 | 0 | c49248a9-57aa-4d93-8994-e 69 |
| SRC_SHA256 | who | 1 | 0 | 65924b026b552d8690809083f 69 |
