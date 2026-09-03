# FED_FDA_GUDID

rows 2.5K  columns 4  scan 11.7s

roles: audit 2, date 1, id 1, who 1

## when

_INGESTED_AT
  2026      2.5K  ##############################

## who

_SRC_SHA256 by rows
      2.5K  split_json:2542:5083948

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  split_json:2542:5083948                   2026:2.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAW | id | 2.5K | 0 | {"results":[{"brand_name" 22; {"results":[{"brand_name" 18; {"results":[{"brand_name" 16; {"results":[{"brand_name" 12 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05 21:50:00.000 2.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 0cf4ed02-d2d4-4051-8ed3-c 2.5K |
| _SRC_SHA256 | who | 1 | 0 | split_json:2542:5083948 2.5K |
