# FED_USASPENDING_SUBAWARDS

rows 5.0K  columns 4  scan 2.3s

roles: audit 2, date 1, id 1, who 1

## when

_INGESTED_AT
  2026      5.0K  ##############################

## who

_SRC_SHA256 by rows
      5.0K  10d86cdbda2296587c3455c82fad5e2a2fc4420b51e63c6183081914585c8d56

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  10d86cdbda2296587c3455c82fad5e2a2fc4420b  2026:5.0K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RECORD | id | 5.0K | 0 | {"action_date":"2016-09-2 29; {"action_date":"2013-10-2 27; {"action_date":"2013-10-2 27; {"action_date":"2016-09-2 26 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-06-10 16:00:23.716 5.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | d8f3adfe-e254-41e7-86f8-4 5.0K |
| _SRC_SHA256 | who | 1 | 0 | 10d86cdbda2296587c3455c82 5.0K |
