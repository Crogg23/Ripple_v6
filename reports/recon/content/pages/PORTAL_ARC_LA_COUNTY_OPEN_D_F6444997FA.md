# PORTAL_ARC_LA_COUNTY_OPEN_D_F6444997FA

rows 111  columns 32  scan 4.3s

roles: amount 1, audit 2, category 10, date 1, other 12, who 7

## when

INGESTED_AT
  2026       111  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 111 | 99.48 | 100 | 100 | 100 | 11.1K |

## who

CONAME by rows
       111  WALGREENS

CONAME by dollars
       11.1K      111 rows  WALGREENS

STATE_NAME by rows
       111  California

STATE_NAME by dollars
       11.1K      111 rows  California

NAICS by rows
       111  44611009

NAICS by dollars
       11.1K      111 rows  44611009

SIC by rows
       111  591205

SIC by dollars
       11.1K      111 rows  591205

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  WALGREENS                                 2026:11.1K

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:11.1K

## what

SALESVOL: 6918 43%, 6588 11%, 9882 10%, 1977 8%, 3294 6%, 8235 5%, 1647 4%, 2306 3%, 4941 3%, 2636 2%, 7247 2%, 989 2%

HDBRCH: 2 100%

ULTNUM: 007539588 98%, 000000000 2%

PUBPRV: 2 100%

EMPNUM: 21 43%, 20 11%, 30 10%, 6 8%, 10 6%, 25 5%, 5 4%, 7 3%, 15 3%, 8 2%, 22 2%, 3 2%

ISCODE: I 60%, M 40%

SQFTCODE: 5 98%, 7 2%

LOC_NAME: PointAddress 78%, StreetAddress 19%, Subaddress 3%

DISTRICT: 5 24%, 4 22%, 3 21%, 1 19%, 2 14%

LABEL: District 5 24%, District 4 22%, District 3 21%, District 1 19%, District 2 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 110 | 0 | 111 1; 110 1; 109 1; 108 1 |
| JOIN_COUNT | other | 1 | 0 | 1 111 |
| TARGET_FID | other | 112 | 0 | 1922 1; 1918 1; 1917 1; 1915 1 |
| LOCNUM | other | 110 | 0 | 998976658 1; 995704871 1; 995641313 1; 992975557 1 |
| CONAME | who | 1 | 0 | WALGREENS 111 |
| STREET | other | 97 | 0 | VENTURA BLVD 3; TELEGRAPH RD 2; E FOOTHILL BLVD 2; DEVONSHIRE ST 2 |
| CITY | who | 61 | 0 | LOS ANGELES 17; TORRANCE 4; LONG BEACH 4; LANCASTER 4 |
| STATE | other | 1 | 0 | CA 111 |
| STATE_NAME | who | 1 | 0 | California 111 |
| ZIP | other | 99 | 0 | 90505 3; 91767 2; 91016 2; 91006 2 |
| ZIP4 | other | 110 | 1 | 5613 2; 1001 1; 1060 1; 3936 1 |
| NAICS | who | 1 | 0 | 44611009 111 |
| SIC | who | 1 | 0 | 591205 111 |
| SALESVOL | category | 23 | 0 | 6918 43; 6588 11; 9882 10; 1977 8 |
| HDBRCH | category | 2 | 2 | 2 109 |
| ULTNUM | category | 2 | 0 | 007539588 109; 000000000 2 |
| PUBPRV | category | 2 | 2 | 2 109 |
| EMPNUM | category | 23 | 0 | 21 43; 20 11; 30 10; 6 8 |
| FRNCOD | other | 1 | 0 | 4 111 |
| ISCODE | category | 3 | 106 | I 3; M 2 |
| SQFTCODE | category | 2 | 0 | 5 109; 7 2 |
| LOC_NAME | category | 3 | 0 | PointAddress 87; StreetAddress 21; Subaddress 3 |
| STATUS | other | 1 | 0 | M 111 |
| SCORE | amount | 3 | 0 | 100.0 106; 99.890625 4; 99.484375 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 111 |
| REC_TYPE | other | 1 | 0 | 0 111 |
| DISTRICT | category | 5 | 0 | 5 27; 4 24; 3 23; 1 21 |
| LABEL | category | 5 | 0 | District 5 27; District 4 24; District 3 23; District 1 21 |
| GEOMETRY | other | 109 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:19:51.26719 111 |
| SOURCE_RUN_ID | audit | 1 | 0 | e0b1e348-50d4-43bf-aadc-1 111 |
| SRC_SHA256 | who | 1 | 0 | 10878fc115549a7daa4eda119 111 |
