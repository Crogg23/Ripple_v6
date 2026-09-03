# PORTAL_CKA_ANALYZE_BOSTON_92EF0E3576

rows 52  columns 19  scan 2.8s

roles: amount 5, audit 2, category 7, date 1, empty 4, who 1

## when

INGESTED_AT
  2026        52  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| OBJECTID_2 | 52 | 1 | 25.50 | 49.49 | 50 | 1.3K |
| SHAPE_LENG | 52 | 1.0K | 27.0K | 62.5K | 67.8K | 1.45M |
| SHAPE_LE_1 | 52 | 413.50 | 11.1K | 25.8K | 27.9K | 582.4K |
| SHAPE_LENGTH | 52 | 0 | 0.09 | 0.20 | 0.21 | 4.58 |
| SHAPE_AREA | 52 | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
        52  1e48ad2c02479cc89c9ac841f3767000e208a2fd2c7776fdf74a9037a33b7920

SRC_SHA256 by dollars
        1.3K       52 rows  1e48ad2c02479cc89c9ac841f3767000e208a2fd2c7776fdf74a9037a33b

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = OBJECTID_2
  1e48ad2c02479cc89c9ac841f3767000e208a2fd  2026:1.3K

## what

RECOLLECT: T 16%, F 16%, M 16%, TH 16%, W 14%, MTH 8%, TF 4%, TH5 4%, W1A 2%, T5 2%, W5 2%, MF 2%

PWDDIST: 4 13%, 9 12%, 8 12%, 3 10%, 5 10%, 7 10%, 2 10%, 6 10%, 1 8%, 10 6%, 1A 2%

DT: 8M 15%, 1MFa 8%, 10MTHb 8%, 3W 8%, 3T 8%, 9Tb 8%, 4F 8%, 4Fa 8%, 1AW 8%, 3M 8%, 9W 8%, 5T 8%

TRASHDAY: TH 19%, W 17%, T 17%, F 17%, M 15%, MTH 8%, TF 4%, MF 2%

CURR_SCHED: T 16%, F 16%, M 16%, TH 16%, W 14%, MTH 8%, TF 4%, TH5 4%, W1A 2%, T5 2%, W5 2%, MF 2%

FUTR_SCHED: B 65%,  A 35%

ORIG_FID: 45.000000000000000 14%, 20.000000000000000 14%, 50.000000000000000 7%, 49.000000000000000 7%, 48.000000000000000 7%, 47.000000000000000 7%, 46.000000000000000 7%, 44.000000000000000 7%, 43.000000000000000 7%, 42.000000000000000 7%, 41.000000000000000 7%, 40.000000000000000 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | empty | 1 | 52 |  |
| OBJECTID_2 | amount | 49 | 0 | 45.000000000000000 2; 20.000000000000000 2; 50.000000000000000 1; 49.000000000000000 1 |
| RECOLLECT | category | 13 | 0 | T 8; F 8; M 8; TH 8 |
| PWDDIST | category | 11 | 0 | 4 7; 9 6; 8 6; 3 5 |
| DT | category | 50 | 0 | 8M 2; 1MFa 1; 10MTHb 1; 3W 1 |
| TRASHDAY | category | 8 | 0 | TH 10; W 9; T 9; F 9 |
| CURR_SCHED | category | 13 | 0 | T 8; F 8; M 8; TH 8 |
| FUTR_SCHED | category | 2 | 0 | B 34;  A 18 |
| C_SCH_END | empty | 1 | 52 |  |
| F_SCH_STRT | empty | 1 | 52 |  |
| SHAPE_LENG | amount | 50 | 0 | 18894.869831100000738 2; 20632.595531499999197 2; 18456.859938300000067 1; 3706.377051389999906 1 |
| ORIG_FID | category | 49 | 0 | 45.000000000000000 2; 20.000000000000000 2; 50.000000000000000 1; 49.000000000000000 1 |
| SHAPE_LE_1 | amount | 52 | 0 | 7615.191563960000167 1; 1529.659480499999972 1; 11749.457889499999510 1; 11150.603522600000360 1 |
| SHAPE_LENGTH | amount | 52 | 0 | 0.061387142080250 1; 0.011633327002174 1; 0.091410810786314 1; 0.092633625316454 1 |
| SHAPE_AREA | amount | 52 | 0 | 0.000062129505109 1; 0.000008113006612 1; 0.000157558883513 1; 0.000186327624615 1 |
| SHAPE_WKT | empty | 1 | 52 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:27:57.20703 52 |
| SOURCE_RUN_ID | audit | 1 | 0 | f67407ad-34f4-4bc7-bf91-e 52 |
| SRC_SHA256 | who | 1 | 0 | 1e48ad2c02479cc89c9ac841f 52 |
