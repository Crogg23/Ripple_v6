# FED_FDA_DEVICE_510K

rows 88  columns 4  scan 3.2s

roles: audit 2, date 1, other 1, who 1

## when

_INGESTED_AT
  2026        88  ##############################

## who

_SRC_SHA256 by rows
        88  split_json:88:175686

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  split_json:88:175686                      2026:88

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAW | other | 87 | 0 | {"results":[{"address_1": 1; {"results":[{"address_1": 1; {"results":[{"address_1": 1; {"results":[{"address_1": 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-06 00:00:35.000 88 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 8e1d5836-fcec-4548-b8d6-5 88 |
| _SRC_SHA256 | who | 1 | 0 | split_json:88:175686 88 |
