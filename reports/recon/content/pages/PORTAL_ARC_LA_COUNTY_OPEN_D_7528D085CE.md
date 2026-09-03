# PORTAL_ARC_LA_COUNTY_OPEN_D_7528D085CE

rows 329  columns 32  scan 4.6s

roles: amount 1, audit 2, category 14, date 1, other 9, who 6

## when

INGESTED_AT
  2026       329  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 329 | 97.13 | 100 | 100 | 100 | 32.9K |

## who

STATE_NAME by rows
       329  California

STATE_NAME by dollars
       32.9K      329 rows  California

NAICS by rows
       329  44611009

NAICS by dollars
       32.9K      329 rows  44611009

SIC by rows
       329  591205

SIC by dollars
       32.9K      329 rows  591205

SOURCE by rows
       329  INFOGROUP

SOURCE by dollars
       32.9K      329 rows  INFOGROUP

## who x when

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:32.9K

NAICS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  44611009                                  2026:32.9K

## what

CONAME: CVS/PHARMACY 84%, CVS PHARMACY Y MAS 13%, CVS AOC CORP 2%, CVS CAREMARK CORP 0%, CVS CAREMARK 0%, CVS SPECIALTY PHARMACY 0%

SALESVOL: 4612 30%, 2306 21%, 1318 10%, 6588 6%, 3294 5%, 2636 5%, 4941 5%, 18524 4%, 8235 4%, 1647 3%, 9882 3%, 1977 3%

HDBRCH: 2 100%

ULTNUM: 400624805 85%, 000000000 15%

PUBPRV: 2 100%

EMPNUM: 14 31%, 7 21%, 4 10%, 20 7%, 10 5%, 8 5%, 15 5%, 25 4%, 5 3%, 30 3%, 6 3%, 50 3%

FRNCOD: K 87%, Ý 13%

ISCODE: M 95%, I 5%

SQFTCODE: 5 65%, 1 19%, 3 4%, 4 4%, 7 3%, 6 3%, 8 1%, 2 1%

LOC_NAME: PointAddress 81%, StreetAddress 16%, Subaddress 3%, Postal 0%

STATUS: M 99%, T 1%

REC_TYPE: 0 100%, 1 0%

DISTRICT: 3 23%, 4 22%, 2 19%, 1 19%, 5 17%

LABEL: District 3 23%, District 4 22%, District 2 19%, District 1 19%, District 5 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 330 | 0 | 329 2; 328 2; 327 2; 326 2 |
| JOIN_COUNT | other | 1 | 0 | 1 329 |
| TARGET_FID | other | 332 | 0 | 1919 2; 1916 2; 1908 2; 1904 2 |
| LOCNUM | other | 323 | 0 | 995768314 2; 993097583 2; 989289210 2; 987888831 2 |
| CONAME | category | 6 | 0 | CVS/PHARMACY 278; CVS PHARMACY Y MAS 43; CVS AOC CORP 5; CVS CAREMARK CORP 1 |
| STREET | other | 212 | 1 | VENTURA BLVD 9; SEPULVEDA BLVD 8; WHITTIER BLVD 8; FIRESTONE BLVD 5 |
| CITY | who | 102 | 0 | LOS ANGELES 62; LONG BEACH 15; PASADENA 8; BURBANK 8 |
| STATE | other | 1 | 0 | CA 329 |
| STATE_NAME | who | 1 | 0 | California 329 |
| ZIP | other | 191 | 0 | 90650 5; 91344 4; 90660 4; 90045 4 |
| ZIP4 | other | 293 | 1 | 5832 3; 2150 3; 3013 3; 4603 3 |
| NAICS | who | 1 | 0 | 44611009 329 |
| SIC | who | 1 | 0 | 591205 329 |
| SALESVOL | category | 40 | 0 | 4612 79; 2306 55; 1318 26; 6588 17 |
| HDBRCH | category | 2 | 50 | 2 279 |
| ULTNUM | category | 2 | 0 | 400624805 279; 000000000 50 |
| PUBPRV | category | 2 | 50 | 2 279 |
| EMPNUM | category | 44 | 0 | 14 80; 7 55; 4 26; 20 17 |
| FRNCOD | category | 3 | 8 | K 278; Ý 43 |
| ISCODE | category | 3 | 265 | M 61; I 3 |
| SQFTCODE | category | 9 | 1 | 5 213; 1 61; 3 14; 4 13 |
| LOC_NAME | category | 4 | 0 | PointAddress 268; StreetAddress 51; Subaddress 9; Postal 1 |
| STATUS | category | 2 | 0 | M 327; T 2 |
| SCORE | amount | 5 | 0 | 100.0 317; 99.890625 9; 98.28125 1; 99.015625 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 329 |
| REC_TYPE | category | 2 | 0 | 0 328; 1 1 |
| DISTRICT | category | 5 | 0 | 3 77; 4 71; 2 63; 1 61 |
| LABEL | category | 5 | 0 | District 3 77; District 4 71; District 2 63; District 1 61 |
| GEOMETRY | other | 330 | 0 | {"type": "Point", "coordi 3; {"type": "Point", "coordi 3; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:22:23.00246 329 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9cb4cb8e-8963-4981-b988-3 329 |
| SRC_SHA256 | who | 1 | 0 | 9ba43c17f8b1e0c473335618f 329 |
