# PORTAL_CKA_WPRDC_ALLEGHENY_91FAE70B2D

rows 10.0K  columns 15  scan 4.8s

roles: amount 2, audit 2, category 1, date 1, id 6, other 3, who 1

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERIMETER | 10.0K | 4.1K | 4.1K | 4.1K | 4.1K | 40.86M |
| SHAPE_LENGTH | 10.0K | 0.01 | 0.01 | 0.01 | 0.01 | 100 |

## who

SRC_SHA256 by rows
     10.0K  cf0e8abdbd0774326ab08e9c1fd07d8d2a71455c8143729a47ad0d1fb02cc1fb

SRC_SHA256 by dollars
      40.86M    10.0K rows  cf0e8abdbd0774326ab08e9c1fd07d8d2a71455c8143729a47ad0d1fb02c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PERIMETER
  cf0e8abdbd0774326ab08e9c1fd07d8d2a71455c  2026:40.86M

## what

BLOCK: B 9%, C 9%, A 9%, D 9%, F 8%, E 8%, H 8%, G 8%, K 8%, J 8%, L 8%, M 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| AREA | other | 6.0K | 0 | 1025581 52; 1025570 51; 1025517 51; 1027325 51 |
| PERIMETER | amount | 7.4K | 0 | 4087.4519 53; 4087.449 51; 4087.562 51; 4087.541 51 |
| BLOCKS | id | 10.0K | 0 | 9601 50; 9600 50; 9201 50; 9599 50 |
| BLOCKS_ID | id | 9.9K | 0 | 9307 50; 9956 50; 9356 50; 9430 50 |
| TILE_BLOCK | id | 9.8K | 0 | 0971L 50; 1791S 50; 0502S 50; 0227P 50 |
| TILE | other | 637 | 0 | 0166 60; 0168 60; 1791 59; 0167 59 |
| BLOCK | category | 16 | 0 | B 643; C 643; A 643; D 643 |
| TILE_NUM | other | 631 | 0 | 166 60; 168 60; 1791 59; 167 59 |
| TILE_BLK_NUM | id | 9.9K | 0 | 971L 50; 1791S 50; 502S 50; 227P 50 |
| SHAPE_LENGTH | amount | 9.9K | 0 | 0.013191173024585 50; 0.0131449480207361 50; 0.0131603560353406 50; 0.0131821750072373 50 |
| SHAPE_AREA | id | 10.1K | 0 | 1.0122221589456e-05 50; 1.00591721609546e-05 50; 1.00788763272202e-05 50; 1.01034793485479e-05 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:43:40.84467 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 769b360e-361d-4158-868b-6 10.0K |
| SRC_SHA256 | who | 1 | 0 | cf0e8abdbd0774326ab08e9c1 10.0K |
