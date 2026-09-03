# FED_COURTLISTENER_RACE_CODES

rows 8  columns 5  scan 2.1s

roles: audit 2, category 2, date 1, who 1

## when

_INGESTED_AT
  2026         8  ##############################

## who

_SRC_SHA256 by rows
         8  ac7cea1e136207328883a9fa46d39435b0047ee71715950fb94974abc00ddca9

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  ac7cea1e136207328883a9fa46d39435b0047ee7  2026:8

## what

ID: 8 12%, 7 12%, 6 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

RACE: o 12%, mena 12%, h 12%, p 12%, a 12%, i 12%, b 12%, w 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | category | 8 | 0 | 8 1; 7 1; 6 1; 5 1 |
| RACE | category | 8 | 0 | o 1; mena 1; h 1; p 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:27.630 8 |
| _SOURCE_RUN_ID | audit | 1 | 0 | e60aa241-5b44-444a-8679-e 8 |
| _SRC_SHA256 | who | 1 | 0 | ac7cea1e136207328883a9fa4 8 |
