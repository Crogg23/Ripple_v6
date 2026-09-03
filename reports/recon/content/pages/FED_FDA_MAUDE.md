# FED_FDA_MAUDE

rows 1.4K  columns 4  scan 13.8s

roles: audit 2, date 1, id 1, who 1

## when

_INGESTED_AT
  2026      1.4K  ##############################

## who

_SRC_SHA256 by rows
      1.4K  split_json_partial:1386:scope_cut_short

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  split_json_partial:1386:scope_cut_short   2026:1.4K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAW | id | 1.4K | 0 | {"results":[{"adverse_eve 2; {"results":[{"adverse_eve 1; {"results":[{"adverse_eve 1; {"results":[{"adverse_eve 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-06 00:25:45.000 1.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | fbf5ce8c-6591-4336-831c-4 1.4K |
| _SRC_SHA256 | who | 1 | 0 | split_json_partial:1386:s 1.4K |
