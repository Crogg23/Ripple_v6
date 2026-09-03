# PORTAL_CKA_WESTERN_PENNSYLV_82D49E467F

rows 645  columns 9  scan 2.9s

roles: amount 2, audit 2, category 1, date 1, other 3, who 1

## when

INGESTED_AT
  2026       645  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LEN | 645 | 33.10 | 722.31 | 132.0K | 1.20M | 4.04M |
| SHAPE_AREA | 645 | 30.65 | 24.0K | 2.78M | 463.46M | 588.49M |

## who

SRC_SHA256 by rows
       645  6ff5dce04758f8dc1ceeb3977fe0c5f6a99a10f9b97327dfda5bc1a014278466

SRC_SHA256 by dollars
       4.04M      645 rows  6ff5dce04758f8dc1ceeb3977fe0c5f6a99a10f9b97327dfda5bc1a01427

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LEN
  6ff5dce04758f8dc1ceeb3977fe0c5f6a99a10f9  2026:4.04M

## what

FEATURECOD: 430 68%, 420 12%, 470 11%, 460 8%, 410 1%, 450 0%, 520 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SHAPE_LEN | amount | 651 | 0 | 107.709970956 4; 1890.6695784 4; 240.10867769 4; 170.092731873 4 |
| FEATURECOD | category | 7 | 0 | 430 437; 420 79; 470 68; 460 51 |
| FID | other | 632 | 0 | 646 4; 645 4; 644 4; 643 4 |
| SHAPE_AREA | amount | 656 | 0 | 637.644185879 4; 111136.617723 4; 3466.51267376 4; 1629.42744585 4 |
| UPDATE_YEA | other | 1 | 0 | 2004 645 |
| DATASPATIAL_WKB | other | 637 | 0 | \x00000000030000000100000 4; \x00000000030000000100000 4; \x00000000030000000100000 4; \x00000000030000000100000 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:45:12.04074 645 |
| SOURCE_RUN_ID | audit | 1 | 0 | 29547891-e9a0-49e6-811f-1 645 |
| SRC_SHA256 | who | 1 | 0 | 6ff5dce04758f8dc1ceeb3977 645 |
