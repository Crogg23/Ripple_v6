# PORTAL_CKA_WPRDC_ALLEGHENY_2DD6B565A7

rows 24  columns 9  scan 2.5s

roles: amount 1, audit 2, category 5, date 1, who 1

## when

INGESTED_AT
  2026        24  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERIMETER | 24 | 13.9K | 51.7K | 82.0K | 86.2K | 1.20M |

## who

SRC_SHA256 by rows
        24  18e57158469503d43454a558fe27c49676419d916b202b3733279745ba121619

SRC_SHA256 by dollars
       1.20M       24 rows  18e57158469503d43454a558fe27c49676419d916b202b3733279745ba12

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PERIMETER
  18e57158469503d43454a558fe27c49676419d91  2026:1.20M

## what

OBJECTID: 72 8%, 71 8%, 70 8%, 69 8%, 68 8%, 67 8%, 66 8%, 65 8%, 64 8%, 63 8%, 62 8%, 61 8%

ANNO: 2-2 8%, 5-3 8%, 2-1 8%, 1-2 8%, 1-1 8%, 3-1 8%, DPSC 8%, 1-3 8%, 6-3 8%, 6-2 8%, 3-4 8%, 1-5 8%

SECTORS: 2 25%, 3 25%, 1 25%, 4 17%, 0 4%, 5 4%

ZONE: 1 25%, 5 17%, 3 17%, 4 17%, 2 12%, 6 12%

GEOMETRY: MULTIPOLYGON (((1351444.212053 8%, MULTIPOLYGON (((1365795.296520 8%, POLYGON ((1360118.064547620015 8%, MULTIPOLYGON (((1344493.701353 8%, MULTIPOLYGON (((1332158.801481 8%, POLYGON ((1334963.375267839990 8%, MULTIPOLYGON (((1344030.891258 8%, POLYGON ((1336783.500007709953 8%, POLYGON ((1334726.203263510018 8%, POLYGON ((1328063.364463849924 8%, POLYGON ((1343000.291697579901 8%, POLYGON ((1341679.676562440115 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 24 | 0 | 72 1; 71 1; 70 1; 69 1 |
| ANNO | category | 23 | 0 | 2-2 1; 5-3 1; 2-1 1; 1-2 1 |
| PERIMETER | amount | 24 | 0 | 50315.43109132 1; 58279.78037601 1; 65466.65619621 1; 67283.18019348 1 |
| SECTORS | category | 6 | 0 | 2 6; 3 6; 1 6; 4 4 |
| ZONE | category | 6 | 0 | 1 6; 5 4; 3 4; 4 4 |
| GEOMETRY | category | 24 | 0 | MULTIPOLYGON (((1351444.2 1; MULTIPOLYGON (((1365795.2 1; POLYGON ((1360118.0645476 1; MULTIPOLYGON (((1344493.7 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:17:41.64689 24 |
| SOURCE_RUN_ID | audit | 1 | 0 | c3c7d3ff-1ece-4cc9-a8eb-2 24 |
| SRC_SHA256 | who | 1 | 0 | 18e57158469503d43454a558f 24 |
