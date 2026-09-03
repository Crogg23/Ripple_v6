# PORTAL_CKA_ANALYZE_BOSTON_BBE6F0FD04

rows 12  columns 11  scan 2.8s

roles: amount 3, audit 2, category 4, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        12  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| DISTRICT_2 | 12 | 1 | 6.50 | 17.67 | 18 | 99 |
| SHAPE_LENGTH | 12 | 0.14 | 0.22 | 0.44 | 0.45 | 2.99 |
| SHAPE_AREA | 12 | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
        12  0bf728741badc471cadbdb4b4ed851279ccd345062267bea1320d5dfbfd0998f

SRC_SHA256 by dollars
          99       12 rows  0bf728741badc471cadbdb4b4ed851279ccd345062267bea1320d5dfbfd0

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = DISTRICT_2
  0bf728741badc471cadbdb4b4ed851279ccd3450  2026:99

## what

DISTRICT: B2 8%, E18 8%, C11 8%, B3 8%, E5 8%, E13 8%, D14 8%, D4 8%, C6 8%, A1 8%, A7 8%, A15 8%

ID: B2 8%, E18 8%, C11 8%, B3 8%, E5 8%, E13 8%, D14 8%, D4 8%, C6 8%, A1 8%, A7 8%, A15 8%

BPDGIS_GIS: E 25%, A 25%, B 17%, C 17%, D 17%

DISTRICT_3: 02 8%, 18 8%, 11 8%, 03 8%, 05 8%, 13 8%, 14 8%, 04 8%, 06 8%, 01 8%, 07 8%, 15 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DISTRICT | category | 12 | 0 | B2 1; E18 1; C11 1; B3 1 |
| ID | category | 12 | 0 | B2 1; E18 1; C11 1; B3 1 |
| BPDGIS_GIS | category | 5 | 0 | E 3; A 3; B 2; C 2 |
| DISTRICT_2 | amount | 12 | 0 | 2.000000000000000 1; 18.000000000000000 1; 11.000000000000000 1; 3.000000000000000 1 |
| DISTRICT_3 | category | 12 | 0 | 02 1; 18 1; 11 1; 03 1 |
| SHAPE_LENGTH | amount | 12 | 0 | 0.231994920608382 1; 0.252090784857594 1; 0.384663943846038 1; 0.198405663958900 1 |
| SHAPE_AREA | amount | 12 | 0 | 0.001204207958740 1; 0.001649618107973 1; 0.001350604379469 1; 0.000944521846130 1 |
| SHAPE_WKT | empty | 1 | 12 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:13:44.20778 12 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3aae214a-c3bf-436c-aa2f-a 12 |
| SRC_SHA256 | who | 1 | 0 | 0bf728741badc471cadbdb4b4 12 |
