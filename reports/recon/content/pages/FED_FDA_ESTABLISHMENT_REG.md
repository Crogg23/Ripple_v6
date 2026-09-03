# FED_FDA_ESTABLISHMENT_REG

rows 166  columns 4  scan 3.2s

roles: audit 2, date 1, other 1, who 1

## when

_INGESTED_AT
  2026       166  ##############################

## who

_SRC_SHA256 by rows
       166  split_json:166:330251

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  split_json:166:330251                     2026:166

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAW | other | 168 | 0 | {"results":[{"establishme 5; {"results":[{"establishme 3; {"results":[{"establishme 2; {"results":[{"establishme 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05 21:43:33.000 166 |
| _SOURCE_RUN_ID | audit | 1 | 0 | e7f85ca1-a75f-44e2-8324-1 166 |
| _SRC_SHA256 | who | 1 | 0 | split_json:166:330251 166 |
