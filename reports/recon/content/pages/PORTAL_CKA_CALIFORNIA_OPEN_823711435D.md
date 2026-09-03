# PORTAL_CKA_CALIFORNIA_OPEN_823711435D

rows 27  columns 14  scan 3.7s

roles: amount 2, audit 2, category 9, date 1, who 1

## when

INGESTED_AT
  2026        27  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 27 | 2.20B | 8.06B | 65.61B | 77.49B | 363.32B |
| SHAPE__LENGTH | 27 | 258.3K | 526.7K | 1.21M | 1.25M | 16.99M |

## who

SRC_SHA256 by rows
        27  e15851454b441178ce21dcafe2d9072bb91644aee50b8f83fe43d6e141f9f61a

SRC_SHA256 by dollars
     363.32B       27 rows  e15851454b441178ce21dcafe2d9072bb91644aee50b8f83fe43d6e141f9

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  e15851454b441178ce21dcafe2d9072bb91644ae  2026:363.32B

## what

OBJECTID: 5924388 8%, 5924387 8%, 5924385 8%, 5924384 8%, 5924383 8%, 5924382 8%, 5924380 8%, 5924379 8%, 5924376 8%, 5924374 8%, 5924373 8%, 5924371 8%

NAME: YOLO 8%, VENTURA 8%, TULARE 8%, TRINITY 8%, TEHAMA 8%, SUTTER 8%, SONOMA 8%, SOLANO 8%, SHASTA 8%, SANTA CLARA 8%, SANTA BARBARA 8%, SAN LUIS OBISPO 8%

REGION: 2 22%, 1 19%, 4 15%, 6 15%, 5 11%, 3 7%, 0 7%, 10 4%

ADMINISTRATION_REGION: Inland 44%, Southern 30%, Coastal 26%

MUTUAL_AID_REGION: 2 26%, 1 19%, 3 19%, 5 15%, 4 11%, 6 11%

NUMBER_IMPACTED_CUSTOMERS: 1 12%, 5 12%, 2 12%, 8 12%, 1144 6%, 26 6%, 287 6%, 110 6%, 27 6%, 9 6%, 50 6%, 13 6%

NUMBER_INCIDENTS: 1 37%, 2 22%, 4 11%, 3 11%, 7 7%, 12 4%, 5 4%, 6 4%

IMPACTED_CUSTOMERS_PLANNED_OUTAGE: 0 63%, 1144 4%, 5 4%, 7 4%, 441 4%, 162 4%, 171 4%, 224 4%, 390 4%, 3 4%, 4 4%

IMPACTED_CUSTOMERS_NON_PLANNED_OUTAGE: 1 18%, 2 18%, 0 12%, 26 6%, 287 6%, 110 6%, 27 6%, 50 6%, 8 6%, 5 6%, 13 6%, 392 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 27 | 0 | 5924388 1; 5924387 1; 5924385 1; 5924384 1 |
| NAME | category | 27 | 0 | YOLO 1; VENTURA 1; TULARE 1; TRINITY 1 |
| REGION | category | 8 | 0 | 2 6; 1 5; 4 4; 6 4 |
| ADMINISTRATION_REGION | category | 3 | 0 | Inland 12; Southern 8; Coastal 7 |
| MUTUAL_AID_REGION | category | 6 | 0 | 2 7; 1 5; 3 5; 5 4 |
| NUMBER_IMPACTED_CUSTOMERS | category | 23 | 0 | 1 2; 5 2; 2 2; 8 2 |
| NUMBER_INCIDENTS | category | 8 | 0 | 1 10; 2 6; 4 3; 3 3 |
| IMPACTED_CUSTOMERS_PLANNED_OUTAGE | category | 11 | 0 | 0 17; 1144 1; 5 1; 7 1 |
| IMPACTED_CUSTOMERS_NON_PLANNED_OUTAGE | category | 22 | 0 | 1 3; 2 3; 0 2; 26 1 |
| SHAPE__AREA | amount | 27 | 0 | 4349584387.69922 1; 7125912319.42188 1; 19305183028.1328 1; 14451716739.8867 1 |
| SHAPE__LENGTH | amount | 27 | 0 | 418928.090467787 1; 477805.316092939 1; 648995.873854277 1; 806709.768708414 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:16:39.17686 27 |
| SOURCE_RUN_ID | audit | 1 | 0 | 14728d5f-e066-4e59-9cef-4 27 |
| SRC_SHA256 | who | 1 | 0 | e15851454b441178ce21dcafe 27 |
