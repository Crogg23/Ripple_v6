# PORTAL_CKA_WPRDC_ALLEGHENY_86091A7F3E

rows 102  columns 16  scan 3.3s

roles: amount 4, audit 2, category 2, date 1, other 7, who 1

## when

INGESTED_AT
  2026       102  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 102 | 2.16M | 10.48M | 71.31M | 75.37M | 1.65B |
| SHAPE__LENGTH | 102 | 7.9K | 17.9K | 48.9K | 62.2K | 2.14M |
| PERIMETER | 97 | 8.4K | 22.0K | 50.5K | 72.6K | 2.42M |
| PGHDB_SDE_FIRE_ZONES_AREA | 97 | 4.18M | 18.16M | 79.57M | 80.21M | 2.28B |

## who

SRC_SHA256 by rows
       102  8887403ca5b503f1765010f1fa340e965cd74957afa27321e28bac266afe936f

SRC_SHA256 by dollars
       1.65B      102 rows  8887403ca5b503f1765010f1fa340e965cd74957afa27321e28bac266afe

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  8887403ca5b503f1765010f1fa340e965cd74957  2026:1.65B

## what

FIREZONES: 24 8%, 5 8%, 20 8%, 19 8%, 14 8%, 1 8%, 23 8%, 7 8%, 18 8%, 12 8%, 8 8%, 21 8%

PAGEROTATE: 90 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 101 | 0 | 109 1; 102 1; 101 1; 100 1 |
| SHAPE__AREA | amount | 102 | 0 | 26309339.4353638 1; 7479788.18908691 1; 10567780.7286987 1; 5996945.27639771 1 |
| SHAPE__LENGTH | amount | 103 | 0 | 42822.3296395676 1; 14589.1878406573 1; 14951.117704705 1; 10891.1670859303 1 |
| DIST_ZONE | other | 102 | 0 | 1-14 2; 1-14A 1; 1-24 1; 4-5 1 |
| FIREZONES | category | 31 | 2 | 24 4; 5 4; 20 4; 19 4 |
| FIREZONES_2 | other | 71 | 5 | 61 4; 20 3; 31 3; 28 3 |
| FIREZONES_ID | other | 70 | 5 | 54 4; 15 3; 71 3; 23 3 |
| MAPBOOK | other | 103 | 0 | 1-14A 1; 1-24 1; 4-5 1; 1-4 1 |
| OLDDIST_ZONE | other | 72 | 4 | 4-5 4; 1-14 3; 1-5 3; 2-8 3 |
| PAGEROTATE | category | 2 | 77 | 90 25 |
| PERIMETER | amount | 70 | 5 | 23130.34179688 4; 35271.57421875 3; 18632.82226563 3; 40074.53515625 3 |
| PGHDB_SDE_FIRE_ZONES_AREA | amount | 69 | 5 | 26184048.0 4; 21662238.0 3; 15531931.0 3; 48572012.0 3 |
| GEOMETRY | other | 101 | 0 | MULTIPOLYGON (((582641.38 1; POLYGON ((585334.39322069 1; POLYGON ((584751.46923465 1; POLYGON ((585246.13253733 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:32:01.72161 102 |
| SOURCE_RUN_ID | audit | 1 | 0 | 15ac048e-5e87-4964-8e09-2 102 |
| SRC_SHA256 | who | 1 | 0 | 8887403ca5b503f1765010f1f 102 |
