# PORTAL_CKA_TAMPA_OPEN_DATA_8B7716D270

rows 316  columns 13  scan 3.3s

roles: amount 1, audit 2, category 3, date 2, empty 2, other 2, who 2

## when

DATE
  2018         9  ######
  2019        35  ######################
  2020        36  ######################
  2021        48  ##############################
  2022        47  #############################
  2023        48  ##############################
  2024        39  ########################
  2025        36  ######################
  2026        18  ###########

INGESTED_AT
  2026       316  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 316 | 0 | 8.5K | 23.35M | 38.37M | 870.82M |

## who

C_ORGANIZATION by rows
       316  Convention Center & Tourism

C_ORGANIZATION by dollars
     870.82M      316 rows  Convention Center & Tourism

SRC_SHA256 by rows
       316  182916468b2b592fa4d1dfd625187a97102e8c488233b62ff5fb0f8acaa639ab

SRC_SHA256 by dollars
     870.82M      316 rows  182916468b2b592fa4d1dfd625187a97102e8c488233b62ff5fb0f8acaa6

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Convention Center & Tourism               2018:12.17M 2019:105.89M 2020:25.20M 2021:64.85M 2022:105.87M 2023:163.02M 2024:146.87M 2025:150.26M 2026:96.70M

SRC_SHA256 by DATE, dollars = VALUE
  182916468b2b592fa4d1dfd625187a97102e8c48  2018:12.17M 2019:105.89M 2020:25.20M 2021:64.85M 2022:105.87M 2023:163.02M 2024:146.87M 2025:150.26M 2026:96.70M

## what

CHARTNAME: TCC Sum of Forecasted Attendan 29%, TCC Event Activity by Month 29%, TCC Economic Impact by Month 29%, TCC Social Media 4 to 5 Star R 12%

CATEGORY: Forcasted Attendance by Month 29%, TCC Event Activity by Month 29%, Economic Impact by Month 29%, Social Media 4 to 5 Star Ratin 12%

SUMMARY: Total 88%, Percent 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 314 | 0 | 21274 2; 21273 2; 21272 2; 20965 2 |
| C_ORGANIZATION | who | 1 | 0 | Convention Center & Touri 316 |
| CHARTNAME | category | 4 | 0 | TCC Sum of Forecasted Att 93; TCC Event Activity by Mon 93; TCC Economic Impact by Mo 92; TCC Social Media 4 to 5 S 38 |
| DESCRIPTION | empty | 1 | 316 |  |
| CATEGORY | category | 4 | 0 | Forcasted Attendance by M 93; TCC Event Activity by Mon 93; Economic Impact by Month 92; Social Media 4 to 5 Star  38 |
| SUMMARY | category | 2 | 0 | Total 278; Percent 38 |
| TYPEDATA | other | 1 | 0 | Date 316 |
| DATE | date | 95 | 0 | 2024-03-01T00:00:00 4; 2024-02-01T00:00:00 4; 2024-01-01T00:00:00 4; 2023-12-01T00:00:00 4 |
| PERIOD | empty | 1 | 316 |  |
| VALUE | amount | 203 | 0 | 95.0 32; 0.0 19; 12.0 9; 9.0 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:18:48.82401 316 |
| SOURCE_RUN_ID | audit | 1 | 0 | cb70a3d5-9a37-4500-85d3-d 316 |
| SRC_SHA256 | who | 1 | 0 | 182916468b2b592fa4d1dfd62 316 |
