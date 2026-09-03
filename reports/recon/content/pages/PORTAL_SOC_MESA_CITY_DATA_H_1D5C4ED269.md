# PORTAL_SOC_MESA_CITY_DATA_H_1D5C4ED269

rows 598  columns 11  scan 2.8s

roles: amount 1, audit 2, category 4, date 2, other 2, who 1

## when

DATE
  2015        70  #############################
  2016        70  #############################
  2017        70  #############################
  2018        70  #############################
  2019        70  #############################
  2020        70  #############################
  2021        70  #############################
  2024        36  ###############
  2025        72  ##############################

INGESTED_AT
  2026       598  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| YOY_PERCENTAGE_CHANGE | 516 | -0.86 | -0.01 | 1.00 | 1.48 | 10.71 |

## who

SRC_SHA256 by rows
       598  789b661e82e5fdcfd026d0f4d9929ec4a92df70adab7b8846247764ec3f87a5c

SRC_SHA256 by dollars
       10.71      598 rows  789b661e82e5fdcfd026d0f4d9929ec4a92df70adab7b8846247764ec3f8

## who x when

SRC_SHA256 by DATE, dollars = YOY_PERCENTAGE_CHANGE
  789b661e82e5fdcfd026d0f4d9929ec4a92df70a  2015:70 2016:-1.09 2017:-4.06 2018:-1.51 2019:2.05 2020:0.84 2021:3.38 2024:5.48 2025:5.62

## what

INDUSTRY: Wholesale Trade 8%, Utilities 8%, Unclassified Establishments 8%, Transportation & Warehousing 8%, Sport Goods, Hobby, Book, & Mu 8%, Real Estate, Rental & Leasing 8%, Public Administration 8%, Professional, Scientific & Tec 8%, Other Services (except Public  8%, Nonstore Retailers 8%, Motor Vehicle & Parts Dealers 8%, Miscellaneous Store Retailers 8%

TYPE: Employees 53%, Businesses 47%

YEAR: 2025 12%, 2015 12%, 2016 12%, 2017 12%, 2018 12%, 2019 12%, 2020 12%, 2021 12%, 2024 6%

NAICS_CODE: 42 8%, 22 8%, 99 8%, 48-49 8%, 451 8%, 523 8%, 53 8%, 92 8%, 54 8%, 81 8%, 454 8%, 441 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY | category | 38 | 0 | Wholesale Trade 17; Utilities 17; Unclassified Establishmen 17; Transportation & Warehous 17 |
| TYPE | category | 2 | 0 | Employees 317; Businesses 281 |
| YEAR | category | 9 | 0 | 2025 72; 2015 70; 2016 70; 2017 70 |
| COUNT | other | 498 | 0 | nan 6; 54 4; 7 4; 181 4 |
| DATE | date | 10 | 0 | 2025-07-01T00:00:00.000 71; 2015-01-01T00:00:00.000 70; 2016-01-01T00:00:00.000 70; 2017-01-01T00:00:00.000 70 |
| NAICS_CODE | category | 36 | 0 | 42 17; 22 17; 99 17; 48-49 17 |
| YOY_CHANGE | other | 299 | 0 | nan 87; 1 14; -1 14; -3 11 |
| YOY_PERCENTAGE_CHANGE | amount | 306 | 0 | nan 82; 0.0 10; -0.004 8; -0.09 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:50:26.19028 598 |
| SOURCE_RUN_ID | audit | 1 | 0 | c24459d1-42b2-4a48-9435-9 598 |
| SRC_SHA256 | who | 1 | 0 | 789b661e82e5fdcfd026d0f4d 598 |
