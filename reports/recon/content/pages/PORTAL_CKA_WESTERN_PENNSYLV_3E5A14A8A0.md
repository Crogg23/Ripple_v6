# PORTAL_CKA_WESTERN_PENNSYLV_3E5A14A8A0

rows 138  columns 11  scan 2.7s

roles: amount 1, audit 2, category 2, date 1, other 5, who 1

## when

INGESTED_AT
  2026       138  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERIMETER | 138 | 6.8K | 39.2K | 561.0K | 1.39M | 9.98M |

## who

SRC_SHA256 by rows
       138  2b4940d28c1b5a13dbde65554747e8bb2debc1672b8487134c8ecbe16dbe1233

SRC_SHA256 by dollars
       9.98M      138 rows  2b4940d28c1b5a13dbde65554747e8bb2debc1672b8487134c8ecbe16dbe

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PERIMETER
  2b4940d28c1b5a13dbde65554747e8bb2debc167  2026:9.98M

## what

COUNT: 10 17%, 4 12%, 8 10%, 7 9%, 11 9%, 5 8%, 13 6%, 12 6%, 6 6%, 18 6%, 17 5%, 16 5%

RINGS_OK: 1 91%, 2 5%, 3 1%, 10 1%, 6 1%, 18 1%, 17 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DESCR | other | 139 | 1 | YUTES RUN BASIN 1; YOUGHIOGHENY RIVER 1; WYLIE RUN BASIN 1; WILLOW RUN BASIN 1 |
| FID | other | 137 | 0 | 138 1; 137 1; 136 1; 135 1 |
| AREA | other | 139 | 0 | 15648580 1; 15513140 1; 356308800 1; 106623800 1 |
| COUNT | category | 49 | 0 | 10 13; 4 9; 8 8; 7 7 |
| RINGS_OK | category | 7 | 0 | 1 125; 2 7; 3 2; 10 1 |
| GLOBALID | other | 140 | 0 | 35bb9750-14a2-484c-9e43-3 1; 379b0c7a-1560-4426-b24b-2 1; 554b13a9-2fff-4b14-a356-a 1; dd1ba489-5484-4af0-9cfc-e 1 |
| PERIMETER | amount | 137 | 0 | 57548.05 1; 18214.71 1; 201652.2 1; 47341.82 1 |
| DATASPATIAL_WKB | other | 135 | 0 | \x00000000060000000a00000 1; \x00000000030000000100000 1; \x00000000060000000600000 1; \x00000000030000000100000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:34:44.84969 138 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7542f50d-588b-4dc3-af94-6 138 |
| SRC_SHA256 | who | 1 | 0 | 2b4940d28c1b5a13dbde65554 138 |
