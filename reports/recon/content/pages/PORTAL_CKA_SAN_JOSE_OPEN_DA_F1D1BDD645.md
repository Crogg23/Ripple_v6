# PORTAL_CKA_SAN_JOSE_OPEN_DA_F1D1BDD645

rows 2  columns 13  scan 3.1s

roles: amount 2, audit 2, category 8, date 1, who 1

## when

INGESTED_AT
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 2 | 12.2K | 22.7K | 33.0K | 33.2K | 45.4K |
| SHAPE_AREA | 2 | 1.85M | 12.51M | 22.96M | 23.18M | 25.03M |

## who

SRC_SHA256 by rows
         2  5a1f0da04b8f5d6584e3e4f67fb4c20cfef141974a82386d0de113f5e89ccbe3

SRC_SHA256 by dollars
       45.4K        2 rows  5a1f0da04b8f5d6584e3e4f67fb4c20cfef141974a82386d0de113f5e89c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  5a1f0da04b8f5d6584e3e4f67fb4c20cfef14197  2026:45.4K

## what

OBJECTID: 7 50%, 6 50%

FACILITYID: 5 50%, 4 50%

ZONE: Downtown Improvement District 50%, Willow Glen Improvement Distri 50%

AGENCY: SJ Downtown Assn 50%, Willow Glen Bus Assn 50%

LASTUPDATE: 2024/04/30 18:48:35+00 50%, 2024/04/30 18:48:50+00 50%

NOTES: PBID 50%, CBID 50%

ENTERPRISEID: REF-PBID-0000000005 50%, REF-PBID-0000000004 50%

TYPE: PBID 50%, CBID 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 7 1; 6 1 |
| FACILITYID | category | 2 | 0 | 5 1; 4 1 |
| ZONE | category | 2 | 0 | Downtown Improvement Dist 1; Willow Glen Improvement D 1 |
| AGENCY | category | 2 | 0 | SJ Downtown Assn 1; Willow Glen Bus Assn 1 |
| LASTUPDATE | category | 2 | 0 | 2024/04/30 18:48:35+00 1; 2024/04/30 18:48:50+00 1 |
| NOTES | category | 2 | 0 | PBID 1; CBID 1 |
| ENTERPRISEID | category | 2 | 0 | REF-PBID-0000000005 1; REF-PBID-0000000004 1 |
| SHAPE_LENGTH | amount | 2 | 0 | 33167.7938183567 1; 12235.031424376 1 |
| SHAPE_AREA | amount | 2 | 0 | 23177532.5716778 1; 1850147.99460264 1 |
| TYPE | category | 2 | 0 | PBID 1; CBID 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:08:49.29287 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | daf8d422-ae56-47ae-aa65-6 2 |
| SRC_SHA256 | who | 1 | 0 | 5a1f0da04b8f5d6584e3e4f67 2 |
