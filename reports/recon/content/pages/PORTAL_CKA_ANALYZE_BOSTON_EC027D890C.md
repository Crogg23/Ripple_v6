# PORTAL_CKA_ANALYZE_BOSTON_EC027D890C

rows 6  columns 11  scan 4.9s

roles: amount 2, audit 2, category 1, date 1, empty 5, who 1

## when

INGESTED_AT
  2026         6  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 6 | 0.20 | 0.29 | 0.48 | 0.49 | 1.83 |
| SHAPE_AREA | 6 | 0 | 0 | 0.01 | 0.01 | 0.01 |

## who

SRC_SHA256 by rows
         6  8afaed00eb90900913fdc1fa60f2884a0eab5c17327c12906485204a35e060e6

SRC_SHA256 by dollars
        1.83        6 rows  8afaed00eb90900913fdc1fa60f2884a0eab5c17327c12906485204a35e0

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  8afaed00eb90900913fdc1fa60f2884a0eab5c17  2026:1.83

## what

DIST: 6 17%, 5 17%, 4 17%, 3 17%, 2 17%, 1 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | empty | 1 | 6 |  |
| PWD | empty | 1 | 6 |  |
| NAME | empty | 1 | 6 |  |
| COMBO | empty | 1 | 6 |  |
| DIST | category | 6 | 0 | 6 1; 5 1; 4 1; 3 1 |
| SHAPE_LENGTH | amount | 6 | 0 | 0.242854856924961 1; 0.336734835673633 1; 0.199629101073944 1; 0.201586170812283 1 |
| SHAPE_AREA | amount | 6 | 0 | 0.001328974324937 1; 0.002017853783597 1; 0.001530705875752 1; 0.001444718242330 1 |
| SHAPE_WKT | empty | 1 | 6 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:10:22.17988 6 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6936e75b-c442-404b-acb8-c 6 |
| SRC_SHA256 | who | 1 | 0 | 8afaed00eb90900913fdc1fa6 6 |
