# FED_EIA861_SHORT_FORM

rows 1.7K  columns 16  scan 3.0s

roles: amount 3, audit 2, category 6, date 1, id 2, other 1, state 1, who 1

## when

_INGESTED_AT
  2026      1.7K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| C_1269_4 | 1.7K | 0 | 3.7K | 29.8K | 38.2K | 11.36M |
| C_1976 | 1.7K | 0 | 31.1K | 198.5K | 372.3K | 90.14M |
| C_254 | 1.7K | 0 | 1.6K | 12.4K | 19.2K | 4.56M |

## who

_SRC_FILE by rows
      1.7K  Short_Form_2024.xlsx

_SRC_FILE by dollars
      11.36M     1.7K rows  Short_Form_2024.xlsx

## who x when

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date, dollars = C_1269_4
  Short_Form_2024.xlsx                      2026:11.36M

## where

AK: IA 156, KS 128, NE 125, MN 124, MO 85, OH 80, IN 71, TX 61, OK 60, AK 54, NC 53, SD 52

## what

C_2024: 2024 100%, These entities are one of the  0%

COOPERATIVE: Municipal 79%, Cooperative 17%, Political Subdivision 3%, Investor Owned 1%, Federal 0%, State 0%

NA: MISO 33%, SWPP 28%, PJM 12%, WACM 4%, SOCO 4%, AECI 3%, ISNE 3%, BPAT 3%, ERCO 3%, NYIS 3%, PACE 2%, CPLE 2%

N: N 58%, Y 42%

N_1: N 88%, Y 12%

N_2: N 93%, Y 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| C_2024 | category | 2 | 0 | 2024 1.7K; These entities are one of 1 |
| C_192 | id | 1.7K | 1 | 31516 9; 21664 9; 21079 9; 20512 9 |
| AKIACHAK_NATIVE_COMMUNITY_ELECTRIC | id | 1.7K | 1 | Midvale Irrigation Distri 9; Willwood Light & Power Co 9; Wyrulec Company 9; Town of Wheatland - (WY) 9 |
| COOPERATIVE | category | 6 | 1 | Municipal 1.4K; Cooperative 292; Political Subdivision 51; Investor Owned 11 |
| AK | state | 47 | 1 | IA 156; KS 128; NE 125; MN 124 |
| NA | category | 38 | 56 | MISO 489; SWPP 413; PJM 181; WACM 56 |
| C_1269_4 | amount | 1.7K | 1 | . 12; 2.8 9; 242.5 9; 22227.5 9 |
| C_1976 | amount | 1.7K | 1 | . 12; 95 9; 1251 9; 189887 9 |
| C_254 | amount | 1.5K | 1 | . 11; 5 9; 75 9; 5216 9 |
| COL | other | 1 | 1 | . 1.7K |
| N | category | 2 | 5 | N 992; Y 727 |
| N_1 | category | 2 | 5 | N 1.5K; Y 208 |
| N_2 | category | 2 | 5 | N 1.6K; Y 118 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:40.44500 1.7K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 8330a09c-9755-45a5-bfed-d 1.7K |
| _SRC_FILE | who | 1 | 0 | Short_Form_2024.xlsx 1.7K |
