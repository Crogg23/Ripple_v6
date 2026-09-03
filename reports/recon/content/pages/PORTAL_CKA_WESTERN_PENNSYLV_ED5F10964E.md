# PORTAL_CKA_WESTERN_PENNSYLV_ED5F10964E

rows 11  columns 7  scan 2.0s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        11  ##############################

## who

SRC_SHA256 by rows
        11  acdb96d01b4d9425299b759b9fd8538243b4a89a1b9beec369c4846057e0ca53

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  acdb96d01b4d9425299b759b9fd8538243b4a89a  2026:11

## what

COLUMN_NAME: Referendum 9%, Vote For 9%, Precinct Name 9%, Cand. Name 9%, Cand. Number 9%, Contest Title 9%, Dist. Code 9%, Dist. Type 9%, Party 9%, Votes 9%, Registered Voters 9%

DESCRIPTION: Whether or not the contest is  9%, The maximum number of candidat 9%, The name of the precinct. Prec 9%, The name of the candidate that 9%, The order in which the candida 9%, The name of the office for whi 9%, The number of the district tha 9%, The type of district that the  9%, The party affiliation of the c 9%, Number of votes cast for the c 9%, The number of registered voter 9%

DATA_TYPE: Text 55%, Number 45%

EXAMPLE_DATA: 1.0 25%, 123456.0 25%, PITTSBURGH WARD 1 DIST 1 12%, Barack Obama 12%, President of the United States 12%, DEM 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COLUMN_NAME | category | 11 | 0 | Referendum 1; Vote For 1; Precinct Name 1; Cand. Name 1 |
| DESCRIPTION | category | 11 | 0 | Whether or not the contes 1; The maximum number of can 1; The name of the precinct. 1; The name of the candidate 1 |
| DATA_TYPE | category | 2 | 0 | Text 6; Number 5 |
| EXAMPLE_DATA | category | 7 | 3 | 1.0 2; 123456.0 2; PITTSBURGH WARD 1 DIST 1 1; Barack Obama 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:03.72177 11 |
| SOURCE_RUN_ID | audit | 1 | 0 | c927ba1f-8e3a-4871-a672-7 11 |
| SRC_SHA256 | who | 1 | 0 | acdb96d01b4d9425299b759b9 11 |
