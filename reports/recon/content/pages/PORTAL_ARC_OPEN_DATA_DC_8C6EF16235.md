# PORTAL_ARC_OPEN_DATA_DC_8C6EF16235

rows 204  columns 29  scan 4.3s

roles: amount 8, audit 2, category 5, date 1, other 13, who 1

## when

INGESTED_AT
  2026       204  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POP_SQMI | 204 | 2.2K | 16.2K | 70.2K | 80.8K | 4.24M |
| SQMI | 204 | 0.04 | 0.19 | 1.11 | 2.22 | 57.40 |
| POP20_SQMI | 204 | 2.3K | 16.1K | 64.3K | 74.5K | 4.12M |
| SUM_CCN | 167 | 24.01M | 75.21M | 418.63M | 702.42M | 16.36B |
| PCTCHG | 204 | -100 | -11.31 | 300 | 400 | -2.4K |
| TOTAL | 204 | 0 | 4 | 37.94 | 43 | 1.4K |

## who

SRC_SHA256 by rows
       204  8af7c5f207c7ecd2f77fe9f57df50aa7496d73ce5fc208d8e7c231817e6ce130

SRC_SHA256 by dollars
        1.4K      204 rows  8af7c5f207c7ecd2f77fe9f57df50aa7496d73ce5fc208d8e7c231817e6c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL
  8af7c5f207c7ecd2f77fe9f57df50aa7496d73ce  2026:1.4K

## what

YEAR: 2025.0 68%, nan 18%, 2024.0 14%

FREQUENCY: 1 42%, 2 15%, 3 14%, 4 7%, 5 7%, 6 5%, 8 3%, 7 3%, 9 2%, 10 2%, 15 1%, 14 1%

COUNT24: 1 22%, 0 19%, 2 15%, 3 9%, 5 8%, 4 6%, 6 6%, 7 4%, 8 4%, 10 3%, 12 2%, 13 1%

COUNT25: 0 34%, 1 16%, 3 13%, 2 10%, 4 7%, 5 7%, 6 5%, 8 3%, 7 3%, 9 2%, 10 1%, 15 1%

TREND: -1 46%, 0 33%, 1 16%, -2 4%, 2 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 204 | 0 | 204 2; 203 2; 202 2; 201 2 |
| STATE_ABBR | other | 1 | 0 | DC 204 |
| STATE_FIPS | other | 1 | 0 | 11 204 |
| COUNTY_FIPS | other | 1 | 0 | 001 204 |
| STCOFIPS | other | 1 | 0 | 11001 204 |
| TRACT_FIPS | other | 207 | 0 | 002704 2; 007603 2; 003200 2; 007709 2 |
| FIPS | other | 206 | 0 | 11001002704 2; 11001007603 2; 11001003200 2; 11001007709 2 |
| POPULATION | other | 205 | 0 | 3037 2; 4096 2; 5308 2; 4482 2 |
| POP_SQMI | amount | 206 | 0 | 27609.1 2; 8714.9 2; 31223.5 2; 6221.9 2 |
| SQMI | amount | 66 | 0 | 0.11 13; 0.08 12; 0.12 10; 0.17 8 |
| POPULATION_2020 | other | 200 | 0 | 5099 2; 4676 2; 3103 2; 3927 2 |
| POP20_SQMI | amount | 202 | 0 | 27209.1 2; 8904.3 2; 8350.0 2; 12800.0 2 |
| HAS_DATA | other | 1 | 0 | 1 204 |
| OBJECTID_1 | other | 203 | 0 | 63 2; 184 2; 74 2; 195 2 |
| TRACT_FIPS_1 | other | 207 | 0 | 002704 2; 007603 2; 003200 2; 007709 2 |
| YEAR | category | 3 | 0 | 2025.0 138; nan 37; 2024.0 29 |
| FREQUENCY | category | 16 | 0 | 1 84; 2 29; 3 27; 4 14 |
| SUM_CCN | amount | 169 | 0 | nan 37; 75272027.0 1; 200760070.0 1; 25077347.0 1 |
| PCTCHG | amount | 45 | 0 | 0.0 68; -100.0 29; -50.0 17; -33.33333333333333 8 |
| COUNT24 | category | 22 | 0 | 1 42; 0 37; 2 29; 3 17 |
| COUNT25 | category | 17 | 0 | 0 66; 1 32; 3 25; 2 20 |
| TREND | category | 5 | 0 | -1 94; 0 68; 1 32; -2 9 |
| TOTAL | amount | 33 | 0 | 0 37; 2 21; 3 19; 5 16 |
| SHAPE__AREA | amount | 203 | 0 | 3204181.569946289 2; 13200828.519592285 2; 4820941.382202148 2; 8920763.716796875 2 |
| SHAPE__LENGTH | amount | 208 | 0 | 11054.393520133488 2; 16365.13174806869 2; 9940.302013466486 2; 14634.625113715307 2 |
| GEOMETRY | other | 202 | 0 | {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:32:46.56936 204 |
| SOURCE_RUN_ID | audit | 1 | 0 | 19f731be-7180-4857-bf7c-e 204 |
| SRC_SHA256 | who | 1 | 0 | 8af7c5f207c7ecd2f77fe9f57 204 |
