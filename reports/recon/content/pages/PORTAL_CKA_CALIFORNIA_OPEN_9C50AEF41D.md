# PORTAL_CKA_CALIFORNIA_OPEN_9C50AEF41D

rows 1.7K  columns 16  scan 2.9s

roles: amount 2, audit 2, category 7, date 2, id 3, who 1

## when

DATE
  2026      1.7K  ##############################

INGESTED_AT
  2026      1.7K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 1.7K | 175.1K | 67.57M | 4.52B | 14.09B | 649.45B |
| SHAPE__LENGTH | 1.7K | 1.9K | 53.7K | 494.2K | 922.2K | 162.70M |

## who

SRC_SHA256 by rows
      1.7K  9fa07c2228cdc1085dee3e9c76150c2e34570554bfe36d128474fb06ff8186f6

SRC_SHA256 by dollars
     649.45B     1.7K rows  9fa07c2228cdc1085dee3e9c76150c2e34570554bfe36d128474fb06ff81

## who x when

SRC_SHA256 by DATE, dollars = SHAPE__AREA
  9fa07c2228cdc1085dee3e9c76150c2e34570554  2026:649.45B

## what

CHS_DAY_0: 0 78%, 1 22%

CHS_DAY_1: 0 59%, 1 39%, 2 2%

CHS_DAY_2: 0 53%, 1 39%, 2 8%, 3 0%

CHS_DAY_3: 0 63%, 1 33%, 2 4%, 3 0%

CHS_DAY_4: 0 69%, 1 28%, 2 3%, 3 0%

CHS_DAY_5: 0 62%, 1 34%, 2 3%, 3 1%

CHS_DAY_6: 0 48%, 1 46%, 2 4%, 3 1%, 4 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.7K | 0 | 1721 9; 1720 9; 1719 9; 1718 9 |
| ZIP_CODE | id | 1.7K | 0 | 96162 9; 96161 9; 96150 9; 96148 9 |
| DATE | date | 1 | 0 | 2026-07-02 1.7K |
| CHS_DAY_0 | category | 2 | 0 | 0 1.3K; 1 382 |
| CHS_DAY_1 | category | 3 | 0 | 0 1.0K; 1 679; 2 28 |
| CHS_DAY_2 | category | 4 | 0 | 0 909; 1 666; 2 144; 3 2 |
| CHS_DAY_3 | category | 4 | 0 | 0 1.1K; 1 561; 2 73; 3 1 |
| CHS_DAY_4 | category | 4 | 0 | 0 1.2K; 1 480; 2 58; 3 1 |
| CHS_DAY_5 | category | 4 | 0 | 0 1.1K; 1 585; 2 57; 3 10 |
| CHS_DAY_6 | category | 5 | 0 | 0 831; 1 795; 2 73; 3 21 |
| GLOBALID | id | 1.7K | 0 | a41e175e-572d-4d06-9725-8 9; 8dff61ed-e156-4b47-a7ad-5 9; fd4a587b-bd9a-4332-a22c-e 9; c56e2dfb-dba9-49fa-b9df-b 9 |
| SHAPE__AREA | amount | 1.7K | 0 | 1819769.078125 9; 845238476.640625 9; 930732119.796875 9; 6480417.71875 9 |
| SHAPE__LENGTH | amount | 1.7K | 0 | 7539.75163965412 9; 195205.538960823 9; 179543.134757657 9; 12649.8886685852 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:02:16.82302 1.7K |
| SOURCE_RUN_ID | audit | 1 | 0 | 71da43b9-9804-4f44-8974-4 1.7K |
| SRC_SHA256 | who | 1 | 0 | 9fa07c2228cdc1085dee3e9c7 1.7K |
