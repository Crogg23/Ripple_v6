# PORTAL_CKA_WESTERN_PENNSYLV_E91E8047AA

rows 10.0K  columns 9  scan 4.3s

roles: amount 2, audit 2, category 1, date 1, id 2, who 2

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENG | 10.0K | 0.18 | 410.37 | 15.6K | 113.1K | 12.51M |
| SHAPE_AREA | 10.0K | 0 | 4.3K | 1.38M | 31.74M | 770.01M |

## who

STATUS by rows
     10.0K  Unprotected Land

STATUS by dollars
      12.51M    10.0K rows  Unprotected Land

SRC_SHA256 by rows
     10.0K  0f634021879efc78d582718724dd5635193f411bc6d6e0c46ddbe62ad4088611

SRC_SHA256 by dollars
      12.51M    10.0K rows  0f634021879efc78d582718724dd5635193f411bc6d6e0c46ddbe62ad408

## who x when

STATUS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENG
  Unprotected Land                          2026:12.51M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENG
  0f634021879efc78d582718724dd5635193f411b  2026:12.51M

## what

TYPE: Sensitive Slope Areas 65%, Allegheny Land Trust GREENPRIN 29%, Rivers & Streams, Wetlands, Fo 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SHAPE_LENG | amount | 9.9K | 0 | 1405.43467813 50; 250.905510103 50; 284.326928822 50; 278.953964972 50 |
| OBJECTID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| TYPE | category | 3 | 0 | Sensitive Slope Areas 6.5K; Allegheny Land Trust GREE 2.9K; Rivers & Streams, Wetland 602 |
| STATUS | who | 1 | 0 | Unprotected Land 10.0K |
| SHAPE_AREA | amount | 10.0K | 0 | 21146.7785073 50; 3112.32925925 50; 3940.795292 50; 2630.15942117 50 |
| DATASPATIAL_WKB | id | 9.8K | 0 | \x00000000060000000100000 50; \x00000000060000000100000 50; \x00000000060000000100000 50; \x00000000060000000100000 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:58:34.00066 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 87deb679-5bd7-447e-b8a2-c 10.0K |
| SRC_SHA256 | who | 1 | 0 | 0f634021879efc78d58271872 10.0K |
