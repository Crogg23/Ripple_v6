# PORTAL_CKA_WESTERN_PENNSYLV_2A71C11D68

rows 7  columns 8  scan 2.8s

roles: amount 1, audit 2, category 3, date 1, other 1, who 1

## when

INGESTED_AT
  2026         7  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MILEAGE | 7 | 19.55 | 91.44 | 199.79 | 200.99 | 743.96 |

## who

SRC_SHA256 by rows
         7  c622245b53be9e4884ba3d96523be99e3f64c3c232b8e44179f681e9dae6f519

SRC_SHA256 by dollars
      743.96        7 rows  c622245b53be9e4884ba3d96523be99e3f64c3c232b8e44179f681e9dae6

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = MILEAGE
  c622245b53be9e4884ba3d96523be99e3f64c3c2  2026:743.96

## what

DISTRICT: 8 14%, 7 14%, 5 14%, 2 14%, 4 14%, 3 14%, 1 14%

OBJECTID_1: 14 14%, 13 14%, 12 14%, 11 14%, 10 14%, 9 14%, 8 14%

GEOMETRY: POLYGON ((595146.1298324390081 14%, POLYGON ((587207.8844213101547 14%, POLYGON ((588838.2267572610871 14%, POLYGON ((577618.0056063869269 14%, POLYGON ((600115.7188244387507 14%, POLYGON ((593965.2168440623208 14%, POLYGON ((597318.7821788347791 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTYFIPS | other | 1 | 0 | 42003 7 |
| DISTRICT | category | 7 | 0 | 8 1; 7 1; 5 1; 2 1 |
| MILEAGE | amount | 7 | 0 | 19.54877718 1; 22.42688439 1; 48.46920248 1; 200.9896408 1 |
| OBJECTID_1 | category | 7 | 0 | 14 1; 13 1; 12 1; 11 1 |
| GEOMETRY | category | 7 | 0 | POLYGON ((595146.12983243 1; POLYGON ((587207.88442131 1; POLYGON ((588838.22675726 1; POLYGON ((577618.00560638 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:11:05.68192 7 |
| SOURCE_RUN_ID | audit | 1 | 0 | 74dc9b3c-fd27-496b-a67d-9 7 |
| SRC_SHA256 | who | 1 | 0 | c622245b53be9e4884ba3d965 7 |
