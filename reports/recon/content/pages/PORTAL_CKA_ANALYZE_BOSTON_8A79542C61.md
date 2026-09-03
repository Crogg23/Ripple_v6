# PORTAL_CKA_ANALYZE_BOSTON_8A79542C61

rows 227  columns 8  scan 2.8s

roles: amount 2, audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026       227  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 227 | 0 | 0 | 0.37 | 1.68 | 4.50 |
| SHAPE_AREA | 227 | 0 | 0 | 0 | 0.01 | 0.01 |

## who

SRC_SHA256 by rows
       227  cc076d84296e6fd23ac503bb4e6525458a68e7a2f7e2f77194241127b04ad312

SRC_SHA256 by dollars
        4.50      227 rows  cc076d84296e6fd23ac503bb4e6525458a68e7a2f7e2f77194241127b04a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  cc076d84296e6fd23ac503bb4e6525458a68e7a2  2026:4.50

## what

TYPE: WETAREA 35%, POND 28%, STREAM 21%, FWETAREA 9%, SALTWETAREA 5%, RETENT 0%, SHORELINE 0%

NAME: Canterbury Brookside I 40%, Back Bay 13%, Neponset River Reservation II 7%, Charles River 7%, Turtle Pond 7%, Chestnut Hill Reservoir 7%, Jamaica Pond 7%, Charles River  7%, Chandler Pond 7%

SHAPE_WKT: MULTIPOLYGON Z (((-71.16719543 20%, MULTIPOLYGON Z (((-71.13164636 20%, MULTIPOLYGON Z (((-70.93144968 20%, MULTIPOLYGON Z (((-71.11397354 20%, MULTIPOLYGON Z (((-71.17038604 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TYPE | category | 8 | 1 | WETAREA 80; POND 64; STREAM 48; FWETAREA 21 |
| NAME | category | 10 | 212 | Canterbury Brookside I 6; Back Bay 2; Neponset River Reservatio 1; Charles River 1 |
| SHAPE_LENGTH | amount | 229 | 0 | 0.002935621749634 2; 0.470265760901909 2; 0.077159211194082 2; 0.003076287295114 2 |
| SHAPE_AREA | amount | 229 | 0 | 0.000000295737504 2; 0.000183103391509 2; 0.000007756569395 2; 0.000000183974286 2 |
| SHAPE_WKT | category | 6 | 222 | MULTIPOLYGON Z (((-71.167 1; MULTIPOLYGON Z (((-71.131 1; MULTIPOLYGON Z (((-70.931 1; MULTIPOLYGON Z (((-71.113 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:37:19.55455 227 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9c42c7e7-3123-4424-b045-7 227 |
| SRC_SHA256 | who | 1 | 0 | cc076d84296e6fd23ac503bb4 227 |
