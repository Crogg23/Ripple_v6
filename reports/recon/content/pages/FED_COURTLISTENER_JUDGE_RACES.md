# FED_COURTLISTENER_JUDGE_RACES

rows 6.5K  columns 6  scan 2.5s

roles: audit 2, category 1, date 1, id 2, who 1

## when

_INGESTED_AT
  2026      6.5K  ##############################

## who

_SRC_SHA256 by rows
      6.5K  8b1d588cf94795706de805be3d232daa23f3e7f0460262adbd9d1826ba993844

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  8b1d588cf94795706de805be3d232daa23f3e7f0  2026:6.5K

## what

RACE_ID: 1 81%, 2 8%, 6 8%, 4 3%, 7 0%, 3 0%, 5 0%, 8 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 6.5K | 0 | 6626 33; 6625 33; 6624 33; 6623 33 |
| PERSON_ID | id | 6.5K | 0 | 16067 34; 16241 33; 16240 33; 16239 33 |
| RACE_ID | category | 8 | 0 | 1 5.3K; 2 500; 6 498; 4 205 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:22.769 6.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 8504a65d-1b0e-4a0e-b5d1-e 6.5K |
| _SRC_SHA256 | who | 1 | 0 | 8b1d588cf94795706de805be3 6.5K |
