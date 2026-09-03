# PORTAL_CKA_OPEN_DATA_SA_CE75F7FDDE

rows 7  columns 9  scan 4.8s

roles: amount 4, audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026         7  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 7 | 1.0K | 8.6K | 38.9K | 39.8K | 96.1K |
| SQMILES | 7 | 1.62 | 13.38 | 60.81 | 62.17 | 150.16 |
| SHAPE__AREA | 7 | 5.58M | 45.61M | 208.94M | 213.58M | 515.58M |
| SHAPE__LENGTH | 7 | 18.8K | 51.9K | 118.6K | 120.3K | 428.2K |

## who

SRC_SHA256 by rows
         7  0f7dd0290a15906aa3628d1f6903462967621a2ab9498d80ff14b30343a61155

SRC_SHA256 by dollars
       96.1K        7 rows  0f7dd0290a15906aa3628d1f6903462967621a2ab9498d80ff14b30343a6

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  0f7dd0290a15906aa3628d1f6903462967621a2a  2026:96.1K

## what

OBJECTID: 7 14%, 6 14%, 5 14%, 4 14%, 3 14%, 2 14%, 1 14%

COUNTYNAME: Guadalupe County 14%, Medina County 14%, Bandera County 14%, Wilson County 14%, Kendall County 14%, Comal County 14%, Atascosa County 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 7 | 0 | 7 1; 6 1; 5 1; 4 1 |
| ACRES | amount | 7 | 0 | 2642.24564705 1; 39787.89457596 1; 1038.04487353 1; 12045.72847657 1 |
| SQMILES | amount | 7 | 0 | 4.12850882 1; 62.16858528 1; 1.62194512 1; 18.82145075 1 |
| COUNTYNAME | category | 7 | 0 | Guadalupe County 1; Medina County 1; Bandera County 1; Wilson County 1 |
| SHAPE__AREA | amount | 7 | 0 | 14166797.1445313 1; 213579168.015625 1; 5581248.29296875 1; 64201333.7382813 1 |
| SHAPE__LENGTH | amount | 7 | 0 | 27235.1271142179 1; 91267.1497253882 1; 18817.4621576439 1; 51907.9841598716 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:11:26.60104 7 |
| SOURCE_RUN_ID | audit | 1 | 0 | 98513b46-1390-4e27-9cb6-5 7 |
| SRC_SHA256 | who | 1 | 0 | 0f7dd0290a15906aa3628d1f6 7 |
