# FED_FDA_DEVICE_ENFORCEMENT

rows 20  columns 4  scan 2.8s

roles: audit 2, category 1, date 1, who 1

## when

_INGESTED_AT
  2026        20  ##############################

## who

_SRC_SHA256 by rows
        20  split_json:20:39635

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  split_json:20:39635                       2026:20

## what

RAW: {"results":[{"address_1":"5405 8%, {"results":[{"address_1":"595  8%, {"results":[{"address_1":"100  8%, {"results":[{"address_1":"60 M 8%, {"results":[{"address_1":"1600 8%, {"results":[{"address_1":"3000 8%, {"results":[{"address_1":"1915 8%, {"results":[{"address_1":"400  8%, {"results":[{"address_1":"7000 8%, {"results":[{"address_1":"Call 8%, {"results":[{"address_1":"BD D 8%, {"results":[{"address_1":"9000 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAW | category | 20 | 0 | {"results":[{"address_1": 1; {"results":[{"address_1": 1; {"results":[{"address_1": 1; {"results":[{"address_1": 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-10 18:55:38.000 20 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 16b1c979-1aaa-4ae1-ae78-5 20 |
| _SRC_SHA256 | who | 1 | 0 | split_json:20:39635 20 |
