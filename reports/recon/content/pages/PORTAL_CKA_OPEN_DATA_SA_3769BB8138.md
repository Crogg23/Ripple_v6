# PORTAL_CKA_OPEN_DATA_SA_3769BB8138

rows 10  columns 13  scan 3.7s

roles: amount 3, audit 2, category 3, date 1, empty 4, who 1

## when

INGESTED_AT
  2026        10  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 10 | 10.92 | 68.94 | 705.55 | 734.30 | 2.1K |
| SHAPE__AREA | 10 | 475.5K | 3.00M | 30.73M | 31.99M | 89.76M |
| SHAPE__LENGTH | 10 | 4.1K | 15.8K | 54.8K | 55.4K | 228.0K |

## who

SRC_SHA256 by rows
        10  f3f907f4f843dc3a41425bc493b584363302ebaa4dc11206eaa9935698561dd6

SRC_SHA256 by dollars
        2.1K       10 rows  f3f907f4f843dc3a41425bc493b584363302ebaa4dc11206eaa993569856

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  f3f907f4f843dc3a41425bc493b584363302ebaa  2026:2.1K

## what

OBJECTID: 10 10%, 9 10%, 8 10%, 7 10%, 6 10%, 5 10%, 4 10%, 3 10%, 2 10%, 1 10%

MLIDA: RIO - 7E MLIDA 10%, RIO - 2 MLIDA 10%, RIO - 7D MLIDA 10%, RIO - 7B MLIDA 10%, RIO - 7C MLIDA 10%, RIO - 6 MLIDA 10%, RIO - 7A MLIDA 10%, RIO - 1 MLIDA 10%, RIO - 5 MLIDA 10%, RIO - 4 MLIDA 10%

GLOBALID: 385c6291-2b9b-4ba1-8005-26f54a 10%, f2824f5e-c793-4b73-8fbe-add35f 10%, a5d3500d-60d6-476f-9c38-7901d9 10%, 922a2250-2d7b-44fd-9ad2-6592fe 10%, 7301382c-d9d9-4659-ab57-5de3ad 10%, 2365bbf6-6305-4431-a11b-268005 10%, 445d94d1-2642-4efc-aa07-21341d 10%, e7f11a5f-2707-4d74-bec0-d6b81c 10%, e800e34d-36f7-40a3-a60e-ff758f 10%, 061730b4-689e-4207-95c1-b2aa3a 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 10 | 0 | 10 1; 9 1; 8 1; 7 1 |
| MLIDA | category | 10 | 0 | RIO - 7E MLIDA 1; RIO - 2 MLIDA 1; RIO - 7D MLIDA 1; RIO - 7B MLIDA 1 |
| ACRES | amount | 10 | 0 | 33.9 1; 102.73 1; 35.15 1; 29.54 1 |
| GLOBALID | category | 10 | 0 | 385c6291-2b9b-4ba1-8005-2 1; f2824f5e-c793-4b73-8fbe-a 1; a5d3500d-60d6-476f-9c38-7 1; 922a2250-2d7b-44fd-9ad2-6 1 |
| CREATED_USER | empty | 1 | 10 |  |
| CREATED_DATE | empty | 1 | 10 |  |
| LAST_EDITED_USER | empty | 1 | 10 |  |
| LAST_EDITED_DATE | empty | 1 | 10 |  |
| SHAPE__AREA | amount | 10 | 0 | 1476904.52148438 1; 4474770.50976563 1; 1531373.73828125 1; 1287136.98242188 1 |
| SHAPE__LENGTH | amount | 10 | 0 | 9766.09593542598 1; 22052.3345172512 1; 7985.05088517717 1; 6767.15228437047 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:12:49.89434 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | 05b8162a-af73-448f-bab4-f 10 |
| SRC_SHA256 | who | 1 | 0 | f3f907f4f843dc3a41425bc49 10 |
