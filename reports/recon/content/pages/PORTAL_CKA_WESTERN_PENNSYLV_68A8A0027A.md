# PORTAL_CKA_WESTERN_PENNSYLV_68A8A0027A

rows 10.0K  columns 15  scan 3.5s

roles: amount 3, audit 2, category 3, date 1, id 4, other 2, who 1

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 10.0K | 0.70 | 68.92 | 1.6K | 100.1K | 1.81M |
| AREA | 10.0K | 2.8K | 278.9K | 6.46M | 404.94M | 7.31B |
| PERIMETER | 10.0K | 208.54 | 3.1K | 46.1K | 1.52M | 59.56M |

## who

SRC_SHA256 by rows
     10.0K  5bf98b250fda3d1a87b16eb431c5740b17e7b360013a1f963285ae24cde5de0e

SRC_SHA256 by dollars
       1.81M    10.0K rows  5bf98b250fda3d1a87b16eb431c5740b17e7b360013a1f963285ae24cde5

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  5bf98b250fda3d1a87b16eb431c5740b17e7b360  2026:1.81M

## what

CAPABILITY: 3 Medium 22%, 2 High 22%, 4 Medium 21%, Other 20%, 3 High 7%, 2 Very High 3%, 3 Very High 2%, 4 High 2%, 1 Very High 0%, 3 Medium Low 0%

CLASS: 3 32%, 2 25%, 4 23%, Other 20%, 1 0%

SUBCLASS: Medium 54%, High 39%, Very High 7%, Medium Low 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACRES | amount | 10.1K | 0 | 93.320195184257 50; 52.288218076172 50; 94.486021966013 50; 55.034774150781 50 |
| AREA | amount | 10.1K | 0 | 377661.655946 50; 211607.51953125 50; 382379.69229467 50; 222722.6796875 50 |
| CAPABILITY | category | 10 | 0 | 3 Medium 2.2K; 2 High 2.2K; 4 Medium 2.1K; Other 2.0K |
| CLASS | category | 5 | 0 | 3 3.2K; 2 2.5K; 4 2.3K; Other 2.0K |
| FID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| MINOR1 | other | 71 | 0 | 31 1.1K; 32 1.1K; 30 887; 78 725 |
| PERIMETER | amount | 10.1K | 0 | 4706.6297182792 50; 1693.6483671557 50; 5433.4225714919 50; 2445.5234858835 50 |
| SOILS | id | 10.0K | 0 | 9201 50; 9200 50; 9199 50; 9198 50 |
| SOILS_ID | id | 10.0K | 0 | 9178 50; 9177 50; 9176 50; 9175 50 |
| SOIL_CODE | other | 71 | 0 | GlC 1.1K; GlD 1.1K; GlB 887; WhB 725 |
| SUBCLASS | category | 5 | 2.0K | Medium 4.3K; High 3.2K; Very High 527; Medium Low 5 |
| GEOMETRY | id | 10.0K | 0 | POLYGON ((593675.55049720 50; POLYGON ((570495.39097381 50; POLYGON ((590288.83509738 50; POLYGON ((565328.58655320 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:48:15.88175 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 500f92f3-ed1d-46cc-a990-e 10.0K |
| SRC_SHA256 | who | 1 | 0 | 5bf98b250fda3d1a87b16eb43 10.0K |
