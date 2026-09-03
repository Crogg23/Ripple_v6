# PORTAL_CKA_OPEN_DATA_SA_CC35A6D7FA

rows 11  columns 11  scan 3.2s

roles: amount 3, audit 2, category 4, date 1, who 2

## when

INGESTED_AT
  2026        11  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 11 | 22.30 | 319.44 | 1.3K | 1.4K | 4.8K |
| SHAPE__AREA | 11 | 971.5K | 13.91M | 58.73M | 60.52M | 207.74M |
| SHAPE__LENGTH | 11 | 3.9K | 20.3K | 47.4K | 47.7K | 248.4K |

## who

STATUS by rows
        11  Adopted

STATUS by dollars
        4.8K       11 rows  Adopted

SRC_SHA256 by rows
        11  eff9a6a587dd9547a4908623bc4c481325a059a7b5ccaf34aca18be994072e11

SRC_SHA256 by dollars
        4.8K       11 rows  eff9a6a587dd9547a4908623bc4c481325a059a7b5ccaf34aca18be99407

## who x when

STATUS by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  Adopted                                   2026:4.8K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  eff9a6a587dd9547a4908623bc4c481325a059a7  2026:4.8K

## what

OBJECTID: 11 9%, 10 9%, 9 9%, 8 9%, 7 9%, 6 9%, 5 9%, 4 9%, 3 9%, 2 9%, 1 9%

NAME: RIO-7D 9%, RIO-7E 9%, RIO-7A 9%, RIO-7C 9%, RIO-7B 9%, RIO-5 9%, RIO-1 9%, RIO-4 9%, RIO-6 9%, RIO-3 9%, RIO-2 9%

OVERLAYCODE: RIO-7D 9%, RIO-7E 9%, RIO-7A 9%, RIO-7C 9%, RIO-7B 9%, RIO-5 9%, RIO-1 9%, RIO-4 9%, RIO-6 9%, RIO-3 9%, RIO-2 9%

ORDINANCE: 2017-02-09-0079 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 11 | 0 | 11 1; 10 1; 9 1; 8 1 |
| NAME | category | 11 | 0 | RIO-7D 1; RIO-7E 1; RIO-7A 1; RIO-7C 1 |
| STATUS | who | 1 | 0 | Adopted 11 |
| ACRES | amount | 11 | 0 | 79.39605642 1; 109.51972307 1; 64.33966718 1; 22.3015584 1 |
| OVERLAYCODE | category | 11 | 0 | RIO-7D 1; RIO-7E 1; RIO-7A 1; RIO-7C 1 |
| ORDINANCE | category | 2 | 6 | 2017-02-09-0079 5 |
| SHAPE__AREA | amount | 11 | 0 | 3458478.50585938 1; 4770660.16210938 1; 2802624.69335938 1; 971451.984375 1 |
| SHAPE__LENGTH | amount | 11 | 0 | 8466.39976320456 1; 10271.1435443991 1; 7458.03218388793 1; 3945.35664184795 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:13:19.91055 11 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8cf0c5d2-414b-4852-a954-5 11 |
| SRC_SHA256 | who | 1 | 0 | eff9a6a587dd9547a4908623b 11 |
