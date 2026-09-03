# PORTAL_CKA_ANALYZE_BOSTON_59330DA889

rows 22  columns 10  scan 3.5s

roles: amount 4, audit 2, category 2, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        22  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| COUNT | 22 | 6 | 12 | 22.58 | 23 | 275 |
| SHAPE_LENG | 22 | 9.3K | 16.5K | 97.6K | 114.5K | 489.5K |
| SHAPE_LENGTH | 22 | 0.07 | 0.13 | 0.80 | 0.94 | 3.86 |
| SHAPE_AREA | 22 | 0 | 0 | 0.01 | 0.01 | 0.01 |

## who

SRC_SHA256 by rows
        22  cf5bebd84afd6aca5ce799dafd953c00a245db5461c6e6a2b7bfe9a844ec278b

SRC_SHA256 by dollars
         275       22 rows  cf5bebd84afd6aca5ce799dafd953c00a245db5461c6e6a2b7bfe9a844ec

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = COUNT
  cf5bebd84afd6aca5ce799dafd953c00a245db54  2026:275

## what

WARD1: 21 8%, 09 8%, 16 8%, 19 8%, 12 8%, 05 8%, 03 8%, 04 8%, 22 8%, 10 8%, 20 8%, 01 8%

WARDLABEL: Ward 21 8%, Ward 9 8%, Ward 16 8%, Ward 19 8%, Ward 12 8%, Ward 5 8%, Ward 3 8%, Ward 4 8%, Ward 22 8%, Ward 10 8%, Ward 20 8%, Ward 1 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| WARD1 | category | 22 | 0 | 21 1; 09 1; 16 1; 19 1 |
| COUNT | amount | 13 | 0 | 12.000000000000000 3; 9.000000000000000 3; 10.000000000000000 3; 13.000000000000000 2 |
| WARDLABEL | category | 22 | 0 | Ward 21 1; Ward 9 1; Ward 16 1; Ward 19 1 |
| SHAPE_LENG | amount | 22 | 0 | 25216.145229999998264 1; 10577.191367199999149 1; 16242.678742199999760 1; 24600.560042299999623 1 |
| SHAPE_LENGTH | amount | 22 | 0 | 0.205034870517245 1; 0.082853612572283 1; 0.124984961418013 1; 0.191926744349708 1 |
| SHAPE_AREA | amount | 22 | 0 | 0.000516666663976 1; 0.000190365942275 1; 0.000679375437826 1; 0.000882717990819 1 |
| SHAPE_WKT | empty | 1 | 22 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:16:52.02656 22 |
| SOURCE_RUN_ID | audit | 1 | 0 | aad39c90-4584-4051-b296-d 22 |
| SRC_SHA256 | who | 1 | 0 | cf5bebd84afd6aca5ce799daf 22 |
