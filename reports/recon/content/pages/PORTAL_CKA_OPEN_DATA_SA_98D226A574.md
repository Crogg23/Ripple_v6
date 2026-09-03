# PORTAL_CKA_OPEN_DATA_SA_98D226A574

rows 12  columns 9  scan 2.6s

roles: amount 2, audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        12  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 12 | 0 | 0.01 | 0.23 | 0.25 | 0.37 |
| SHAPE__LENGTH | 12 | 0.04 | 1.12 | 2.42 | 2.45 | 12.55 |

## who

SRC_SHA256 by rows
        12  eebb9d00330d506c6c65d4d3191d0f5a8e4b1fcede508918f27e8843e5acf76c

SRC_SHA256 by dollars
        0.37       12 rows  eebb9d00330d506c6c65d4d3191d0f5a8e4b1fcede508918f27e8843e5ac

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  eebb9d00330d506c6c65d4d3191d0f5a8e4b1fce  2026:0.37

## what

OBJECTID: 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%, 1 8%

NAME: D5-0 25%, D6-0 17%, D8-0 8%, D7-0 8%, D4-0 8%, D3-0 8%, D2-0 8%, D1-0 8%, AST-0 8%

BATCODE: D5 25%, D6 17%, D8 8%, D7 8%, D4 8%, D3 8%, D2 8%, D1 8%, AST 8%

BATTALION: 5 25%, 6 17%, 8 8%, 7 8%, 4 8%, 3 8%, 2 8%, 1 8%, T 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 12 | 0 | 12 1; 11 1; 10 1; 9 1 |
| NAME | category | 9 | 0 | D5-0 3; D6-0 2; D8-0 1; D7-0 1 |
| BATCODE | category | 9 | 0 | D5 3; D6 2; D8 1; D7 1 |
| BATTALION | category | 9 | 0 | 5 3; 6 2; 8 1; 7 1 |
| SHAPE__AREA | amount | 12 | 0 | 0.00580928455883623 1; 0.0138776652345314 1; 0.0132646896545339 1; 0.0026779524137055 1 |
| SHAPE__LENGTH | amount | 12 | 0 | 0.640856026868808 1; 1.12064856448525 1; 1.15157749878853 1; 0.52735408673477 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:14:01.94473 12 |
| SOURCE_RUN_ID | audit | 1 | 0 | b075bb74-818c-470b-b396-a 12 |
| SRC_SHA256 | who | 1 | 0 | eebb9d00330d506c6c65d4d31 12 |
