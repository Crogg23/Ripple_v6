# PORTAL_CKA_WESTERN_PENNSYLV_38F78BA9E4

rows 23  columns 12  scan 2.1s

roles: audit 2, category 7, date 1, empty 2, who 1

## when

INGESTED_AT
  2026        23  ##############################

## who

SRC_SHA256 by rows
        23  d8c8cd71dadc01a1aab019e9c494e15a2694fa88c8be52b23aa005d348ccc596

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  d8c8cd71dadc01a1aab019e9c494e15a2694fa88  2026:23

## what

FID: 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%

MSLINK: 125 8%, 2 8%, 31 8%, 137 8%, 140 8%, 143 8%, 132 8%, 136 8%, 145 8%, 134 8%, 135 8%, 126 8%

LEG_DISTRICT: 54 8%, 46 8%, 45 8%, 44 8%, 42 8%, 40 8%, 39 8%, 38 8%, 36 8%, 35 8%, 34 8%, 33 8%

LAST_NAME: Costa, 15%, Evankovich, 8%, Ortitay, 8%, Kotik, 8%, Mustio, 8%, Miller, 8%, Maher, 8%, Saccone, 8%, Kortz, 8%, Readshaw, 8%, Gergely, 8%, Dermody, 8%

FIRST_NAME: Eli 8%, Jason A. 8%, Nickolas M. 8%, Mark 8%, Daniel L. 8%, John A. 8%, Rick 8%, William C., ll 8%, Harry A., lll 8%, Marc J. 8%, Paul 8%, Frank J. 8%

HOME_COUNTY: Allegheny 91%, Westmoreland 4%, Beaver 4%

PARTY: D 70%, R 30%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 23 | 0 | 23 1; 22 1; 21 1; 20 1 |
| MSLINK | category | 23 | 0 | 125 1; 2 1; 31 1; 137 1 |
| LEG_DISTRICT | category | 23 | 0 | 54 1; 46 1; 45 1; 44 1 |
| LAST_NAME | category | 22 | 0 | Costa, 2; Evankovich, 1; Ortitay, 1; Kotik, 1 |
| FIRST_NAME | category | 23 | 0 | Eli 1; Jason A. 1; Nickolas M. 1; Mark 1 |
| HOME_COUNTY | category | 3 | 0 | Allegheny 21; Westmoreland 1; Beaver 1 |
| PARTY | category | 2 | 0 | D 16; R 7 |
| SHAPE_LENGTH | empty | 1 | 23 |  |
| SHAPE_AREA | empty | 1 | 23 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:16:57.21847 23 |
| SOURCE_RUN_ID | audit | 1 | 0 | a034a521-6f24-4921-952d-2 23 |
| SRC_SHA256 | who | 1 | 0 | d8c8cd71dadc01a1aab019e9c 23 |
