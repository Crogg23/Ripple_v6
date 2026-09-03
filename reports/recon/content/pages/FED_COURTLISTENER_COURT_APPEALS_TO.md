# FED_COURTLISTENER_COURT_APPEALS_TO

rows 8  columns 6  scan 2.2s

roles: audit 2, category 3, date 1, who 1

## when

_INGESTED_AT
  2026         8  ##############################

## who

_SRC_SHA256 by rows
         8  7be824ee1063c748507c14c23b7e9aa0e9315d965d5e116521a7b51053a18dde

## who x when

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  7be824ee1063c748507c14c23b7e9aa0e9315d96  2026:8

## what

ID: 8 12%, 7 12%, 6 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

FROM_COURT_ID: bpai 12%, ptab 12%, ttab 12%, mtd 12%, ccpa 12%, cit 12%, cavc 12%, uscfc 12%

TO_COURT_ID: cafc 88%, com 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | category | 8 | 0 | 8 1; 7 1; 6 1; 5 1 |
| FROM_COURT_ID | category | 8 | 0 | bpai 1; ptab 1; ttab 1; mtd 1 |
| TO_COURT_ID | category | 2 | 0 | cafc 7; com 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:03:56.267 8 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 235692f3-ffb7-406d-a56f-f 8 |
| _SRC_SHA256 | who | 1 | 0 | 7be824ee1063c748507c14c23 8 |
