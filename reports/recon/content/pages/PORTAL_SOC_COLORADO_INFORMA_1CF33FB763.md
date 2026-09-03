# PORTAL_SOC_COLORADO_INFORMA_1CF33FB763

rows 2.0K  columns 27  scan 3.2s

roles: amount 1, audit 2, category 11, date 1, other 12, who 1

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CENCTY | 2.0K | 1 | 1 | 3 | 3 | 3.0K |

## who

SRC_SHA256 by rows
      2.0K  45cd5e4c2c6379ef87e7ccabb2b261ba62630d10c314caa43a2d41a348191b49

SRC_SHA256 by dollars
        3.0K     2.0K rows  45cd5e4c2c6379ef87e7ccabb2b261ba62630d10c314caa43a2d41a34819

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CENCTY
  45cd5e4c2c6379ef87e7ccabb2b261ba62630d10  2026:3.0K

## what

FIPSCTY: 1 74%, 3 26%

N20_49: 0 57%, 1 22%, 2 7%, 3 5%, 4 3%, 5 1%, 6 1%, 7 1%, 8 1%, 9 1%, 10 0%, 11 0%

N50_99: 0 78%, 1 12%, 2 4%, 3 2%, 4 1%, 5 1%, 7 0%, 6 0%, 20 0%, 16 0%, 8 0%, 14 0%

N100_249: 0 83%, 1 10%, 2 3%, 3 1%, 4 1%, 6 0%, 7 0%, 5 0%, 9 0%, 11 0%, 8 0%, 16 0%

N250_499: 0 94%, 1 4%, 2 1%, 4 0%, 5 0%, 3 0%, 7 0%, 39 0%

N500_999: 0 98%, 1 1%, 2 0%, 3 0%, 9 0%

N1000: 0 99%, 1 1%, 2 0%, 6 0%

N1000_1: 0 99%, 1 0%, 2 0%, 4 0%

N1000_2: 0 100%, 1 0%

N1000_4: 0 100%, 1 0%

EMPFLAG: nan 43%, A 31%, B 18%, C 5%, E 2%, F 1%, G 0%, I 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | other | 1 | 0 | 2000 2.0K |
| FIPSTATE | other | 1 | 0 | 8 2.0K |
| FIPSCTY | category | 2 | 0 | 1 1.5K; 3 514 |
| NAICS | other | 1.5K | 0 | 6219// 10; 621610 10; 62161/ 10; 6216// 10 |
| EMP | other | 377 | 0 | 0 1.1K; 15 23; 11 9; 102 9 |
| QP1 | other | 507 | 0 | 0 1.1K; 184 8; 205 8; 38 7 |
| AP | other | 531 | 0 | 0 1.1K; 802 6; 592 6; 857 6 |
| EST | other | 133 | 0 | 1 515; 2 254; 3 154; 4 107 |
| N5_9 | other | 57 | 0 | 0 857; 1 433; 2 222; 3 106 |
| N10_19 | other | 52 | 0 | 0 1.0K; 1 421; 2 162; 3 75 |
| N20_49 | category | 37 | 0 | 0 1.1K; 1 427; 2 144; 3 98 |
| N50_99 | category | 27 | 0 | 0 1.6K; 1 241; 2 81; 3 35 |
| N100_249 | category | 19 | 0 | 0 1.7K; 1 198; 2 59; 3 28 |
| N250_499 | category | 8 | 0 | 0 1.9K; 1 89; 2 22; 4 7 |
| N500_999 | category | 5 | 0 | 0 2.0K; 1 27; 2 6; 3 2 |
| N1000 | category | 4 | 0 | 0 2.0K; 1 20; 2 1; 6 1 |
| N1000_1 | category | 4 | 0 | 0 2.0K; 1 10; 2 1; 4 1 |
| N1000_2 | category | 2 | 0 | 0 2.0K; 1 6 |
| N1000_3 | other | 1 | 0 | 0 2.0K |
| N1000_4 | category | 2 | 0 | 0 2.0K; 1 6 |
| CENSTATE | other | 1 | 0 | 84.0 2.0K |
| CENCTY | amount | 2 | 0 | 1.0 1.5K; 3.0 514 |
| N_5 | other | 101 | 0 | 1 492; 0 423; 2 206; 4 118 |
| EMPFLAG | category | 8 | 0 | nan 853; A 623; B 353; C 102 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:45:10.64779 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c77b4e48-e435-48ef-964e-a 2.0K |
| SRC_SHA256 | who | 1 | 0 | 45cd5e4c2c6379ef87e7ccabb 2.0K |
