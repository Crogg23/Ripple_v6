# PORTAL_CKA_OPEN_DATA_SA_9770EB9EBD

rows 14  columns 12  scan 2.8s

roles: amount 2, audit 2, category 5, date 1, other 2, who 1

## when

INGESTED_AT
  2026        14  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_INJURIES | 14 | 2 | 2 | 4 | 4 | 35 |
| SHAPE__LENGTH | 14 | 99.70 | 4.0K | 13.0K | 13.4K | 67.7K |

## who

SRC_SHA256 by rows
        14  2dd7dd07745cdbea8d8b644b741e6c6e5086d4201628f8084497b22b4227dee7

SRC_SHA256 by dollars
          35       14 rows  2dd7dd07745cdbea8d8b644b741e6c6e5086d4201628f8084497b22b4227

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_INJURIES
  2dd7dd07745cdbea8d8b644b741e6c6e5086d420  2026:35

## what

OBJECTID: 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%

FROMSTREET: Allensworth 8%, Williamsburg 8%, IH 35 8%, Fitch 8%, Guenther 8%, Timber Path 8%, Hickman 8%, Willard 8%, Desert View 8%, Callaghan 8%, Romero 8%, Alamo Pkwy 8%

TOSTREET: Casa Blanca 8%, IH 10 8%, Duval 8%, Hutchins Place 8%, Mission 8%, Reed 8%, Croft Trace 8%, Woodlawn 8%, Sun Gate 8%, Bonanza 8%, Hamilton 8%, Westwood 8%

INCAPACITATED_INJURIES: 2 57%, 3 21%, 1 14%, 4 7%

FATAL_INJURIES: 0 71%, 1 29%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 14 | 0 | 14 1; 13 1; 12 1; 11 1 |
| STREETNAME | other | 1 | 0 | TBD 14 |
| FROMSTREET | category | 14 | 0 | Allensworth 1; Williamsburg 1; IH 35 1; Fitch 1 |
| TOSTREET | category | 14 | 0 | Casa Blanca 1; IH 10 1; Duval 1; Hutchins Place 1 |
| INCAPACITATED_INJURIES | category | 4 | 0 | 2 8; 3 3; 1 2; 4 1 |
| FATAL_INJURIES | category | 2 | 0 | 0 10; 1 4 |
| TOTAL_INJURIES | amount | 3 | 0 | 2 9; 3 3; 4 2 |
| SBIA_YEAR | other | 1 | 0 | 2020 14 |
| SHAPE__LENGTH | amount | 14 | 0 | 9605.6696556218 1; 13425.2708477548 1; 847.21341356509 1; 8757.82476722234 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:14:58.40087 14 |
| SOURCE_RUN_ID | audit | 1 | 0 | b6ae7c0b-ed6e-4dd8-8154-f 14 |
| SRC_SHA256 | who | 1 | 0 | 2dd7dd07745cdbea8d8b644b7 14 |
