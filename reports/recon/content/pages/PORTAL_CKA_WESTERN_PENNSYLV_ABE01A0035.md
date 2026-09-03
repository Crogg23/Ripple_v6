# PORTAL_CKA_WESTERN_PENNSYLV_ABE01A0035

rows 4  columns 15  scan 3.8s

roles: amount 4, audit 2, category 8, date 1, who 1

## when

INGESTED_AT
  2026         4  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 4 | 296.16M | 387.72M | 472.04M | 473.04M | 1.54B |
| SHAPE__LENGTH | 4 | 91.3K | 165.1K | 226.3K | 226.6K | 648.1K |
| PERIMETER | 4 | 13.3K | 52.7K | 111.2K | 111.8K | 230.5K |
| SQ_MILES | 4 | 10.65 | 13.91 | 16.92 | 16.95 | 55.42 |

## who

SRC_SHA256 by rows
         4  222405469b890ec5590e1fb75c44d182208c7702171bc29cf95533a494368c5a

SRC_SHA256 by dollars
       1.54B        4 rows  222405469b890ec5590e1fb75c44d182208c7702171bc29cf95533a49436

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  222405469b890ec5590e1fb75c44d182208c7702  2026:1.54B

## what

OBJECTID: 10 25%, 8 25%, 2 25%, 1 25%

ACREAGE: 7699 25%, 6819 25%, 10105 25%, 10848 25%

DIVISION: Southern 25%, Central 25%, Northern 25%, Eastern 25%

ENV_SERV: 11 25%, 9 25%, 3 25%, 2 25%

ENV_SERV_I: 179 25%, 177 25%, 176 25%, 181 25%

PGHDB_SDE_DPW_ES_DIVISIONS_AREA: 335347488 25%, 297013088 25%, 6426384 25%, 7809404 25%

UNIQUE_ID: 85 25%, 7 25%, 14 25%, 25 25%

GEOMETRY: POLYGON ((581770.6712289026472 25%, POLYGON ((592714.3080640749540 25%, MULTIPOLYGON (((583818.5049902 25%, MULTIPOLYGON (((592738.7636973 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 4 | 0 | 10 1; 8 1; 2 1; 1 1 |
| SHAPE__AREA | amount | 4 | 0 | 335457509.515808 1; 296160853.997192 1; 439981866.472473 1; 473036333.077576 1 |
| SHAPE__LENGTH | amount | 4 | 0 | 112132.504439966 1; 91297.0361682965 1; 226564.086893133 1; 218120.043426378 1 |
| ACREAGE | category | 4 | 0 | 7699 1; 6819 1; 10105 1; 10848 1 |
| DIVISION | category | 4 | 0 | Southern 1; Central 1; Northern 1; Eastern 1 |
| ENV_SERV | category | 4 | 0 | 11 1; 9 1; 3 1; 2 1 |
| ENV_SERV_I | category | 4 | 0 | 179 1; 177 1; 176 1; 181 1 |
| PERIMETER | amount | 4 | 0 | 111773.703125 1; 91896.3515625 1; 13292.99023438 1; 13582.99023438 1 |
| PGHDB_SDE_DPW_ES_DIVISIONS_AREA | category | 4 | 0 | 335347488 1; 297013088 1; 6426384 1; 7809404 1 |
| SQ_MILES | amount | 4 | 0 | 12.02990394 1; 10.6547414 1; 15.78949341 1; 16.95041302 1 |
| UNIQUE_ID | category | 4 | 0 | 85 1; 7 1; 14 1; 25 1 |
| GEOMETRY | category | 4 | 0 | POLYGON ((581770.67122890 1; POLYGON ((592714.30806407 1; MULTIPOLYGON (((583818.50 1; MULTIPOLYGON (((592738.76 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:09:22.63226 4 |
| SOURCE_RUN_ID | audit | 1 | 0 | 26b0b5e5-c8e9-40a1-a28f-3 4 |
| SRC_SHA256 | who | 1 | 0 | 222405469b890ec5590e1fb75 4 |
