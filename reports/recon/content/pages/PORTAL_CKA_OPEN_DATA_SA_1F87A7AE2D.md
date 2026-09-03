# PORTAL_CKA_OPEN_DATA_SA_1F87A7AE2D

rows 8.5K  columns 10  scan 2.6s

roles: amount 2, audit 2, category 2, date 1, empty 1, id 2, who 1

## when

INGESTED_AT
  2026      8.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 8.5K | 0 | 170.3K | 24.52M | 964.72M | 13.08B |
| SHAPE__LENGTH | 8.5K | 0.13 | 2.2K | 37.7K | 393.5K | 36.13M |

## who

SRC_SHA256 by rows
      8.5K  9cb3e7a1019d6d8a3c687ab52ce7ec66cf0001774182507e98ba09a79f87cd6a

SRC_SHA256 by dollars
      13.08B     8.5K rows  9cb3e7a1019d6d8a3c687ab52ce7ec66cf0001774182507e98ba09a79f87

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  9cb3e7a1019d6d8a3c687ab52ce7ec66cf000177  2026:13.08B

## what

PLANNAME: West 56%, North 34%, Heritage South 5%, Monte Vista 2%, NE I-35 and Loop 410 Area Regi 1%, Meadow Village 1%, Medical Center Area Regional C 0%, Port San Antonio Area Regional 0%, Bandera Road Corridor Plan 0%, Midtown Area Regional Center P 0%, Downtown Area Regional Center  0%

CENTERTIERS: Suburban Tier 45%, General Urban Tier 25%, Natural Tier 15%, Rural Estate Tier 7%, Civic Center 3%, Country Tier 2%, Mixed Use Center 1%, Specialized Center 1%, Regional Center 1%, Agribusiness RIMSE Tier 0%, Agribusiness Tier 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 8.5K | 0 | 8547 43; 8546 43; 8545 43; 8544 43 |
| PLANNAME | category | 16 | 193 | West 4.7K; North 2.9K; Heritage South 439; Monte Vista 142 |
| LANDUSE | empty | 1 | 8.5K |  |
| CENTERTIERS | category | 13 | 286 | Suburban Tier 3.7K; General Urban Tier 2.1K; Natural Tier 1.2K; Rural Estate Tier 543 |
| GLOBALID | id | 8.5K | 0 | f8f64b9a-eef7-48f1-96c3-5 43; 1923df37-d335-463b-af74-5 43; b9d74ced-138f-4d82-994c-8 43; 2050606d-ec8a-48f4-b189-8 43 |
| SHAPE__AREA | amount | 8.6K | 2 | 17481.41015625 43; 84145.701171875 43; 14613.515625 43; 120409.349609375 43 |
| SHAPE__LENGTH | amount | 8.5K | 2 | 529.052064070236 43; 1596.63564773353 43; 488.205829279907 43; 1394.4453761668 43 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:20:57.64342 8.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | dbf60f04-4128-4a61-a0d5-2 8.5K |
| SRC_SHA256 | who | 1 | 0 | 9cb3e7a1019d6d8a3c687ab52 8.5K |
