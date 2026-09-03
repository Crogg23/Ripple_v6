# PORTAL_CKA_WESTERN_PENNSYLV_38ABDAEC9D

rows 1.7K  columns 15  scan 4.8s

roles: amount 2, audit 2, date 1, id 2, other 2, who 7

## when

INGESTED_AT
  2026      1.7K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 1.7K | 3.41 | 194.8K | 719.1K | 819.1K | 391.65M |
| SHAPE__LENGTH | 1.7K | 13.53 | 13.1K | 35.7K | 43.2K | 23.45M |

## who

LAST_EDI_1 by rows
      1.7K  2018/04/04 16:11:46.484+00

LAST_EDI_1 by dollars
     391.65M     1.7K rows  2018/04/04 16:11:46.484+00

CREATED_DA by rows
      1.7K  2018/04/04 16:11:46.484+00

CREATED_DA by dollars
     391.65M     1.7K rows  2018/04/04 16:11:46.484+00

CREATED_US by rows
      1.7K  pgh.admin

CREATED_US by dollars
     391.65M     1.7K rows  pgh.admin

LAST_EDITE by rows
      1.7K  pgh.admin

LAST_EDITE by dollars
     391.65M     1.7K rows  pgh.admin

## who x when

LAST_EDI_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  2018/04/04 16:11:46.484+00                2026:391.65M

CREATED_DA by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  2018/04/04 16:11:46.484+00                2026:391.65M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SLOPE25 | other | 1 | 0 | Yes 1.7K |
| LAST_EDI_1 | who | 1 | 0 | 2018/04/04 16:11:46.484+0 1.7K |
| CREATED_DA | who | 1 | 0 | 2018/04/04 16:11:46.484+0 1.7K |
| OBJECTID | other | 1 | 0 | 2 1.7K |
| CREATED_US | who | 1 | 0 | pgh.admin 1.7K |
| SHAPE__LEN | who | 1 | 0 | 69.93739244 1.7K |
| SHAPE__ARE | who | 1 | 0 | 0.00386219 1.7K |
| OBJECTID_1 | id | 1.7K | 0 | 1714 9; 1713 9; 1712 9; 1711 9 |
| LAST_EDITE | who | 1 | 0 | pgh.admin 1.7K |
| SHAPE__AREA | amount | 1.7K | 0 | 64640.9200744629 9; 227481.784484863 9; 56913.3984069824 9; 175890.199493408 9 |
| SHAPE__LENGTH | amount | 1.7K | 0 | 5580.51037228953 9; 16986.1695287063 9; 7023.77412968074 9; 20061.5305064219 9 |
| DATASPATIAL_WKB | id | 1.7K | 0 | \x00000000060000002f00000 9; \x00000000060000007a00000 9; \x00000000060000002500000 9; \x00000000060000006000000 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:56:01.00747 1.7K |
| SOURCE_RUN_ID | audit | 1 | 0 | 394705f6-187f-4d4f-9484-c 1.7K |
| SRC_SHA256 | who | 1 | 0 | 19d992bf7acb94430aa7c9280 1.7K |
