# PORTAL_CKA_TAMPA_OPEN_DATA_9909AA9ED8

rows 2.4K  columns 13  scan 3.2s

roles: amount 1, audit 2, category 5, date 2, empty 1, id 1, other 1, who 1

## when

DATE
  2008         2  
  2009         2  
  2018         2  
  2019         5  
  2020        70  ####
  2021       140  #########
  2022       484  ##############################
  2023       482  ##############################
  2024       484  ##############################
  2025       485  ##############################
  2026       236  ###############

INGESTED_AT
  2026      2.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 2.4K | -3 | 100 | 3.8K | 3.9K | 854.9K |

## who

SRC_SHA256 by rows
      2.4K  07955aa86c718b848041407bd7e7e897df9dcab587ecbe06ab7735ee9b3647d2

SRC_SHA256 by dollars
      854.9K     2.4K rows  07955aa86c718b848041407bd7e7e897df9dcab587ecbe06ab7735ee9b36

## who x when

SRC_SHA256 by DATE, dollars = VALUE
  07955aa86c718b848041407bd7e7e897df9dcab5  2008:3.5K 2009:3.5K 2018:3.5K 2019:13.4K 2020:85.1K 2021:105.9K 2022:135.0K 2023:139.2K 2024:145.7K 2025:149.5K 2026:70.5K

## what

C_ORGANIZATION: Logistics & Asset Management ( 72%, Logistics & Asset Management 28%

CHARTNAME: Facilities Department 27%, Number of Vehicles Available b 8%, Fleet Work Orders Closed by Mo 8%, Fleet Work Orders Opened by Mo 8%, Fleet PM Completed by Month 8%, Preventative Maintenance (PM)  7%, Percent of Vehicles Available  6%, Percent of Vehicles Available  6%, Percent of Vehicles Available  6%, Percent of Vehicles Available  6%, Percent of Vehicles Available  6%, Percent of Vehicles Available  6%

CATEGORY: Percent of Vehicles 71%, Number of Vehicles 3%, Fleet Work Orders Closed by Mo 3%, Work Orders Opened by Month 3%, Fleet PM Completed by Month 3%, PM 3%, Facilities Emergency Work Orde 3%, Facilities Preventative Mainte 3%, Facilities Total # of Work Ord 3%, Facilities Emergency WO Respon 3%, Total Electric Cars by Year 0%, Total Vehicles by Fiscal Year 0%

SUMMARY: Percent 71%, Total 26%, Average 3%

PERIOD: 07-2021 15%, 06-2021 12%, 05-2021 12%, 08-2021 8%, 09-2020 8%, 10-2020 8%, 11-2020 8%, 12-2020 8%, 01-2021 8%, 02-2021 8%, 03-2021 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 2.3K | 0 | 21321 12; 21320 12; 21319 12; 21318 12 |
| C_ORGANIZATION | category | 2 | 0 | Logistics & Asset Managem 1.7K; Logistics & Asset Managem 681 |
| CHARTNAME | category | 40 | 0 | Facilities Department 273; Number of Vehicles Availa 81; Fleet Work Orders Closed  79; Fleet Work Orders Opened  78 |
| DESCRIPTION | empty | 1 | 2.4K |  |
| CATEGORY | category | 13 | 0 | Percent of Vehicles 1.7K; Number of Vehicles 81; Fleet Work Orders Closed  79; Work Orders Opened by Mon 78 |
| SUMMARY | category | 3 | 0 | Percent 1.7K; Total 620; Average 67 |
| TYPEDATA | other | 1 | 0 | Date 2.4K |
| DATE | date | 97 | 0 | 2024-01-01T00:00:00 43; 2023-01-01T00:00:00 43; 2022-01-01T00:00:00 43; 2025-10-01T00:00:00 42 |
| PERIOD | category | 15 | 2.4K | 07-2021 4; 06-2021 3; 05-2021 3; 08-2021 2 |
| VALUE | amount | 1.1K | 0 | 100.0 667; 96.0 15; 3827.0 15; 91.0 14 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:27:56.47409 2.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 798c06c1-871e-423a-a3a0-c 2.4K |
| SRC_SHA256 | who | 1 | 0 | 07955aa86c718b848041407bd 2.4K |
