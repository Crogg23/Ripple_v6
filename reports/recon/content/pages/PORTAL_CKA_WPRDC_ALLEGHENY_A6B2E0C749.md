# PORTAL_CKA_WPRDC_ALLEGHENY_A6B2E0C749

rows 5  columns 12  scan 2.3s

roles: audit 2, category 5, date 1, empty 3, who 2

## when

INGESTED_AT
  2026         5  ##############################

## who

HOME_COUNT by rows
         5  Allegheny

SRC_SHA256 by rows
         5  7b9e0b1010c9740e5661a11f2f222e4ededc3558a7ae3dcd392773227cf5b5e3

## who x when

HOME_COUNT by INGESTED_AT  LOAD STAMP, not an event date
  Allegheny                                 2026:5

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  7b9e0b1010c9740e5661a11f2f222e4ededc3558  2026:5

## what

MSLINK: 11 20%, 9 20%, 8 20%, 7 20%, 6 20%

LEG_DISTRICT: 43 20%, 38 20%, 45 20%, 37 20%, 42 20%

S_LASTNAME: Costa 20%, Williams 20%, Brewster 20%, Robinson 20%, Fontana 20%

S_FIRSTNAME: Jay, Jr. 20%, Lindsey Marie 20%, James R. 20%, Devlin 20%, Wayne D. 20%

PARTY: D 80%, R 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | empty | 1 | 5 |  |
| MSLINK | category | 5 | 0 | 11 1; 9 1; 8 1; 7 1 |
| LEG_DISTRICT | category | 5 | 0 | 43 1; 38 1; 45 1; 37 1 |
| S_LASTNAME | category | 5 | 0 | Costa 1; Williams 1; Brewster 1; Robinson 1 |
| S_FIRSTNAME | category | 5 | 0 | Jay, Jr. 1; Lindsey Marie 1; James R. 1; Devlin 1 |
| HOME_COUNT | who | 1 | 0 | Allegheny 5 |
| PARTY | category | 2 | 0 | D 4; R 1 |
| SHAPE_LENGTH | empty | 1 | 5 |  |
| SHAPE_AREA | empty | 1 | 5 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:09:59.07986 5 |
| SOURCE_RUN_ID | audit | 1 | 0 | 32173b70-ab2f-4ef1-9c4a-3 5 |
| SRC_SHA256 | who | 1 | 0 | 7b9e0b1010c9740e5661a11f2 5 |
