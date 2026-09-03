# PORTAL_ARC_LA_COUNTY_OPEN_D_92EFBD96E7

rows 126  columns 32  scan 4.5s

roles: amount 1, audit 2, category 10, date 1, other 12, who 7

## when

INGESTED_AT
  2026       126  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 126 | 98.33 | 100 | 100 | 100 | 12.6K |

## who

CONAME by rows
       126  RITE AID

CONAME by dollars
       12.6K      126 rows  RITE AID

STATE_NAME by rows
       126  California

STATE_NAME by dollars
       12.6K      126 rows  California

NAICS by rows
       126  44611009

NAICS by dollars
       12.6K      126 rows  44611009

SIC by rows
       126  591205

SIC by dollars
       12.6K      126 rows  591205

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  RITE AID                                  2026:12.6K

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:12.6K

## what

SALESVOL: 1647 19%, 3294 14%, 1318 14%, 1977 11%, 2306 10%, 4941 8%, 6588 6%, 989 5%, 3953 4%, 9882 4%, 7576 4%, 5271 3%

HDBRCH: 2 100%

ULTNUM: 007531742 99%, 000000000 1%

PUBPRV: 2 100%

EMPNUM: 5 19%, 10 14%, 4 13%, 6 11%, 7 10%, 15 8%, 20 6%, 3 5%, 12 4%, 30 4%, 23 4%, 16 3%

ISCODE: M 96%, I 4%

SQFTCODE: 5 99%, 7 1%

LOC_NAME: PointAddress 75%, StreetAddress 24%, Subaddress 1%

DISTRICT: 3 23%, 4 22%, 5 21%, 1 18%, 2 16%

LABEL: District 3 23%, District 4 22%, District 5 21%, District 1 18%, District 2 16%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 125 | 0 | 126 1; 125 1; 124 1; 123 1 |
| JOIN_COUNT | other | 1 | 0 | 1 126 |
| TARGET_FID | other | 127 | 0 | 1921 1; 1909 1; 1905 1; 1902 1 |
| LOCNUM | other | 127 | 0 | 998176754 1; 989384730 1; 988228219 1; 987818499 1 |
| CONAME | who | 1 | 0 | RITE AID 126 |
| STREET | other | 107 | 0 | FOOTHILL BLVD 4; SEPULVEDA BLVD 3; WILSHIRE BLVD 3; W SUNSET BLVD 3 |
| CITY | who | 74 | 0 | LOS ANGELES 27; LONG BEACH 9; TORRANCE 3; SANTA MONICA 3 |
| STATE | other | 1 | 0 | CA 126 |
| STATE_NAME | who | 1 | 0 | California 126 |
| ZIP | other | 118 | 0 | 90017 2; 90027 2; 90403 2; 90028 2 |
| ZIP4 | other | 123 | 0 | 3403 2; 2302 2; 1430 1; 2408 1 |
| NAICS | who | 1 | 0 | 44611009 126 |
| SIC | who | 1 | 0 | 591205 126 |
| SALESVOL | category | 29 | 0 | 1647 19; 3294 14; 1318 14; 1977 11 |
| HDBRCH | category | 2 | 1 | 2 125 |
| ULTNUM | category | 2 | 0 | 007531742 125; 000000000 1 |
| PUBPRV | category | 2 | 1 | 2 125 |
| EMPNUM | category | 30 | 0 | 5 19; 10 14; 4 13; 6 11 |
| FRNCOD | other | 1 | 0 | F 126 |
| ISCODE | category | 3 | 74 | M 50; I 2 |
| SQFTCODE | category | 2 | 0 | 5 125; 7 1 |
| LOC_NAME | category | 3 | 0 | PointAddress 95; StreetAddress 30; Subaddress 1 |
| STATUS | other | 1 | 0 | M 126 |
| SCORE | amount | 2 | 0 | 100.0 125; 98.328125 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 126 |
| REC_TYPE | other | 1 | 0 | 0 126 |
| DISTRICT | category | 5 | 0 | 3 29; 4 28; 5 26; 1 23 |
| LABEL | category | 5 | 0 | District 3 29; District 4 28; District 5 26; District 1 23 |
| GEOMETRY | other | 126 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:20:09.09273 126 |
| SOURCE_RUN_ID | audit | 1 | 0 | ae50cf8d-04f4-4b50-9cdd-9 126 |
| SRC_SHA256 | who | 1 | 0 | 41e6872d6b16afa232daee4f9 126 |
