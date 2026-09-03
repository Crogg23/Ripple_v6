# PORTAL_CKA_ANALYZE_BOSTON_CF53830F73

rows 9  columns 8  scan 2.6s

roles: amount 2, audit 2, category 2, date 1, empty 1, who 1

## when

INGESTED_AT
  2026         9  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 9 | 0 | 0.03 | 0.18 | 0.19 | 0.45 |
| SHAPE_AREA | 9 | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
         9  950b9aef8efa344724b33104121c53a55bc420653516aff99da5231ea2913f98

SRC_SHA256 by dollars
        0.45        9 rows  950b9aef8efa344724b33104121c53a55bc420653516aff99da5231ea291

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  950b9aef8efa344724b33104121c53a55bc42065  2026:0.45

## what

ADOPTED: 2021 44%, 2007 44%, 2006 11%

TYPE: 1"" Capture and No Harm Area 56%, No Harm Area 44%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ADOPTED | category | 3 | 0 | 2021 4; 2007 4; 2006 1 |
| TYPE | category | 2 | 0 | 1"" Capture and No Harm A 5; No Harm Area 4 |
| SHAPE_LENGTH | amount | 9 | 0 | 0.060688099049578 1; 0.018445618644377 1; 0.030578931830452 1; 0.035970428880565 1 |
| SHAPE_AREA | amount | 9 | 0 | 0.000097648066521 1; 0.000021890366966 1; 0.000050212344113 1; 0.000032440350805 1 |
| SHAPE_WKT | empty | 1 | 9 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:12:03.56683 9 |
| SOURCE_RUN_ID | audit | 1 | 0 | 44ce169e-7f11-44b9-901f-e 9 |
| SRC_SHA256 | who | 1 | 0 | 950b9aef8efa344724b331041 9 |
