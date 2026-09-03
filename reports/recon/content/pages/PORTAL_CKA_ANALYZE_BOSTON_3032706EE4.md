# PORTAL_CKA_ANALYZE_BOSTON_3032706EE4

rows 24  columns 7  scan 2.6s

roles: amount 2, audit 2, category 1, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        24  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 24 | 0.03 | 0.14 | 0.36 | 0.37 | 3.47 |
| SHAPE_AREA | 24 | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
        24  56a0ae4cd0fd033974f325309145fa2348a040fb166f47bd312ea956e5ef6737

SRC_SHA256 by dollars
        3.47       24 rows  56a0ae4cd0fd033974f325309145fa2348a040fb166f47bd312ea956e5ef

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  56a0ae4cd0fd033974f325309145fa2348a040fb  2026:3.47

## what

NEIGHBORHOOD: West Roxbury 8%, West End 8%, South End 8%, South Boston Waterfront 8%, South Boston 8%, Roxbury 8%, Roslindale 8%, North End 8%, Mission Hill 8%, Mattapan 8%, Longwood 8%, Jamaica Plain 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NEIGHBORHOOD | category | 24 | 0 | West Roxbury 1; West End 1; South End 1; South Boston Waterfront 1 |
| SHAPE_LENGTH | amount | 24 | 0 | 0.216024567398815 1; 0.044883419286384 1; 0.075146685095101 1; 0.116811059933182 1 |
| SHAPE_AREA | amount | 24 | 0 | 0.001477334739468 1; 0.000085035791687 1; 0.000239139128120 1; 0.000534542458901 1 |
| SHAPE_WKT | empty | 1 | 24 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:18:02.28101 24 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3e3c5a64-0fc4-4408-96bf-3 24 |
| SRC_SHA256 | who | 1 | 0 | 56a0ae4cd0fd033974f325309 24 |
