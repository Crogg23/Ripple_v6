# PORTAL_CKA_WESTERN_PENNSYLV_440A699A5B

rows 10.0K  columns 9  scan 3.0s

roles: amount 1, audit 2, category 1, date 1, id 3, other 1, who 1

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LEN | 10.0K | 0.69 | 269.98 | 3.4K | 22.6K | 5.35M |

## who

SRC_SHA256 by rows
     10.0K  1b35cf795fa5199b847768dbc1986eb6b66f245fbf00b27811e2680285122fd0

SRC_SHA256 by dollars
       5.35M    10.0K rows  1b35cf795fa5199b847768dbc1986eb6b66f245fbf00b27811e268028512

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LEN
  1b35cf795fa5199b847768dbc1986eb6b66f245f  2026:5.35M

## what

FEATURECOD: 520 67%, 540 26%, 430 4%, 580 1%, 510 1%, 420 0%, 410 0%, 590 0%, 470 0%, 530 0%, 460 0%, 1510 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SHAPE_LEN | amount | 9.7K | 0 | 56.201871993 50; 35.5969071293 50; 233.24713606 50; 19.3670197317 50 |
| FEATURECOD | category | 12 | 0 | 520 6.7K; 540 2.6K; 430 439; 580 109 |
| FID | id | 10.0K | 0 | 10001 50; 10000 50; 9999 50; 9998 50 |
| UPDATE_YEA | other | 1 | 0 | 2004 10.0K |
| GLOBALID | id | 9.9K | 0 | a20d9cff-1d13-477d-b1d8-2 50; 45585fed-e006-40be-8b9d-1 50; e0f0fe1f-bacc-4d3b-8fe2-f 50; d859ddf8-001a-4307-bfa7-a 50 |
| DATASPATIAL_WKB | id | 9.9K | 0 | \x000000000200000003c0540 50; \x000000000200000002c0540 50; \x000000000200000007c0540 50; \x000000000200000002c0540 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:46:15.82816 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 92d75f22-c5cf-42f1-b620-f 10.0K |
| SRC_SHA256 | who | 1 | 0 | 1b35cf795fa5199b847768dbc 10.0K |
