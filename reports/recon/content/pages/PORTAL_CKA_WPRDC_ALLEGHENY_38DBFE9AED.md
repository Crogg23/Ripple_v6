# PORTAL_CKA_WPRDC_ALLEGHENY_38DBFE9AED

rows 5  columns 14  scan 4.1s

roles: amount 6, audit 2, category 5, date 1, who 1

## when

INGESTED_AT
  2026         5  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 5 | 288.39M | 302.56M | 336.90M | 337.54M | 1.54B |
| SHAPE__LENGTH | 5 | 102.9K | 143.0K | 187.7K | 189.0K | 701.9K |
| AREA_SQFT | 5 | 288.60M | 302.76M | 337.03M | 337.67M | 1.55B |
| AREA_SQM | 5 | 10.35 | 10.86 | 12.09 | 12.11 | 55.42 |
| PERIMETER | 5 | 19.58 | 27.32 | 35.68 | 35.92 | 133.78 |
| SHAPE_LENG | 5 | 103.4K | 144.3K | 188.4K | 189.7K | 706.4K |

## who

SRC_SHA256 by rows
         5  3d36ad66cf26570dda157e29108f4098fccb52e3bdca007189d7021ca2bd34f4

SRC_SHA256 by dollars
       1.54B        5 rows  3d36ad66cf26570dda157e29108f4098fccb52e3bdca007189d7021ca2bd

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  3d36ad66cf26570dda157e29108f4098fccb52e3  2026:1.54B

## what

GLOBALID: 6f0333a5-9e95-4c99-ad01-a67dc6 20%, 9139acea-d6ae-49d7-a54b-18c31b 20%, 30ed1817-4f72-44de-8bed-b88328 20%, 58c54901-a07a-42b2-bff2-dfe43b 20%, 131722ea-c063-428c-8f82-9db288 20%

OBJECTID_1: 5 20%, 4 20%, 3 20%, 2 20%, 1 20%

DIVISION: 4 20%, 5 20%, 3 20%, 1 20%, 2 20%

OBJECTID: 88 20%, 70 20%, 49 20%, 26 20%, 6 20%

GEOMETRY: MULTIPOLYGON (((586747.8515608 20%, POLYGON ((585037.9439264956163 20%, POLYGON ((588520.1877988283522 20%, MULTIPOLYGON (((583818.5050168 20%, MULTIPOLYGON (((590453.9938536 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GLOBALID | category | 5 | 0 | 6f0333a5-9e95-4c99-ad01-a 1; 9139acea-d6ae-49d7-a54b-1 1; 30ed1817-4f72-44de-8bed-b 1; 58c54901-a07a-42b2-bff2-d 1 |
| OBJECTID_1 | category | 5 | 0 | 5 1; 4 1; 3 1; 2 1 |
| SHAPE__AREA | amount | 5 | 0 | 337535259.698822 1; 288393240.549622 1; 302563476.645721 1; 294490152.733551 1 |
| SHAPE__LENGTH | amount | 5 | 0 | 188956.800093742 1; 142953.818039156 1; 102905.536507062 1; 156822.779876193 1 |
| AREA_SQFT | amount | 5 | 0 | 337667198.668 1; 288595435.444 1; 302764129.258 1; 294518336.103 1 |
| AREA_SQM | amount | 5 | 0 | 12.11219257 1; 10.35197823 1; 10.86021222 1; 10.56443391 1 |
| DIVISION | category | 5 | 0 | 4 1; 5 1; 3 1; 1 1 |
| OBJECTID | category | 5 | 0 | 88 1; 70 1; 49 1; 26 1 |
| PERIMETER | amount | 5 | 0 | 35.92148707 1; 27.32185488 1; 19.57980864 1; 29.89833553 1 |
| SHAPE_LENG | amount | 5 | 0 | 189665.451713 1; 144259.393761 1; 103381.389611 1; 157863.211584 1 |
| GEOMETRY | category | 5 | 0 | MULTIPOLYGON (((586747.85 1; POLYGON ((585037.94392649 1; POLYGON ((588520.18779882 1; MULTIPOLYGON (((583818.50 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:09:54.02984 5 |
| SOURCE_RUN_ID | audit | 1 | 0 | 02806c94-23bc-4237-83d0-1 5 |
| SRC_SHA256 | who | 1 | 0 | 3d36ad66cf26570dda157e291 5 |
