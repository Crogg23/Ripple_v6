# PORTAL_CKA_WESTERN_PENNSYLV_4D90100824

rows 1.1K  columns 16  scan 3.6s

roles: amount 9, audit 2, category 1, date 1, id 3, who 1

## when

INGESTED_AT
  2026      1.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PVIOLADDRE | 1.1K | 0 | 0 | 0.06 | 0.63 | 10.46 |
| PCOND_FLAG | 1.1K | -10.0K | 0 | 0.13 | 0.25 | -190.0K |
| PFORC1719 | 1.1K | -10.0K | 0.01 | 0.06 | 0.11 | -190.0K |
| PHHOO | 1.1K | 0 | 0.66 | 1 | 1 | 706.65 |
| PNROFRCNT | 1.1K | -10.0K | 0 | 0.15 | 1 | -70.0K |
| VSP1719 | 1.1K | -10.0K | 0.51 | 1.47 | 2.21 | -359.4K |

## who

SRC_SHA256 by rows
      1.1K  4ca82645137fc709b3da4e18729e65fe10b8ea8adac58f1d95217f35ffb4e943

SRC_SHA256 by dollars
       10.46     1.1K rows  4ca82645137fc709b3da4e18729e65fe10b8ea8adac58f1d95217f35ffb4

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PVIOLADDRE
  4ca82645137fc709b3da4e18729e65fe10b8ea8a  2026:10.46

## what

MVA21: E 18%, G 17%, C 17%, H 11%, B 10%, D 9%, A 7%, J 4%, NC 3%, I 3%, F 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PVIOLADDRE | amount | 62 | 0 | 0.0 318; 0.003 100; 0.002 82; 0.004 63 |
| ESRI_OID | id | 1.1K | 0 | 1114 6; 1113 6; 1112 6; 1111 6 |
| PCOND_FLAG | amount | 94 | 0 | 0.0 410; 0.003 86; 0.002 69; 0.004 52 |
| PFORC1719 | amount | 71 | 0 | 0.0 135; 0.011 57; 0.008 50; 0.004 44 |
| PHHOO | amount | 601 | 0 | 1.0 42; 0.0 24; 0.682 8; 0.58 7 |
| GEOID | id | 1.1K | 0 | 420035521002 6; 420039804001 6; 420032609001 6; 420030201005 6 |
| PNROFRCNT | amount | 76 | 0 | 0.0 776; 0.002 54; 0.003 48; 0.001 32 |
| VSP1719 | amount | 581 | 0 | -10000.0 41; 0.48 9; 0.37 8; 0.589 8 |
| PROSUBHH | amount | 287 | 0 | 0.0 633; 1.0 21; 0.037 6; 0.027 4 |
| MSP1719 | amount | 723 | 0 | -9999.0 41; 150000.0 9; 80000.0 9; 205000.0 8 |
| MVA21 | category | 11 | 0 | E 196; G 190; C 185; H 122 |
| PVACLOT | amount | 60 | 0 | 0.0 480; 0.002 78; 0.003 70; 0.004 52 |
| DATASPATIAL_WKB | id | 1.1K | 0 | \x00000000060000000100000 6; \x00000000060000000100000 6; \x00000000060000000100000 6; \x00000000060000000100000 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:50:32.51732 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | b25b0b82-aa3c-4bfb-9df9-f 1.1K |
| SRC_SHA256 | who | 1 | 0 | 4ca82645137fc709b3da4e187 1.1K |
