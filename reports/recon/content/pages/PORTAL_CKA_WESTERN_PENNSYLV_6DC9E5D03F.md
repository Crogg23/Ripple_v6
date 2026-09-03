# PORTAL_CKA_WESTERN_PENNSYLV_6DC9E5D03F

rows 114  columns 7  scan 2.6s

roles: audit 2, category 1, date 1, empty 1, other 2, who 1

## when

INGESTED_AT
  2026       114  ##############################

## who

SRC_SHA256 by rows
       114  ba554c0fe228b1a45e95cca6d457da919f49e44110c9b526099e4f828bc5b792

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  ba554c0fe228b1a45e95cca6d457da919f49e441  2026:114

## what

HOLC_GRADE: C 37%, D 30%, B 24%, A 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| HOLC_GRADE | category | 4 | 0 | C 42; D 34; B 27; A 11 |
| NAME | empty | 1 | 114 |  |
| HOLC_ID | other | 115 | 0 | D9 1; D8 1; D7 1; D6 1 |
| DATASPATIAL_WKB | other | 116 | 0 | \x00000000060000000100000 1; \x00000000060000000100000 1; \x00000000060000000100000 1; \x00000000060000000100000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:32:45.82792 114 |
| SOURCE_RUN_ID | audit | 1 | 0 | 52cfeed5-30cf-43c6-9a38-7 114 |
| SRC_SHA256 | who | 1 | 0 | ba554c0fe228b1a45e95cca6d 114 |
