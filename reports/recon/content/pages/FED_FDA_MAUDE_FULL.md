# FED_FDA_MAUDE_FULL

rows 13.0K  columns 4  scan 103.5s

roles: audit 2, date 1, id 1, who 1

## when

_INGESTED_AT
  2026     13.0K  ##############################

## who

_SRC_SHA256 by rows
     13.0K  split_json:13042:7958989

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  split_json:13042:7958989                  2026:13.0K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAW | id | 13.0K | 0 | {"results":[{"adverse_eve 9; {"results":[{"adverse_eve 9; {"results":[{"adverse_eve 9; {"results":[{"adverse_eve 9 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-28 15:48:22.000 13.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 823ed98d-7725-4c95-9a33-a 13.0K |
| _SRC_SHA256 | who | 1 | 0 | split_json:13042:7958989 13.0K |
