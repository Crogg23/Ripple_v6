# PORTAL_ARC_OPEN_DATA_MINNEA_D808F6BF62

rows 25  columns 30  scan 3.2s

roles: amount 2, audit 2, category 17, date 5, other 3, who 2

## when

REPORTEDDATE
  2018        25  ##############################

BEGINDATE
  2018        25  ##############################

ENTEREDDATE
  2018        25  ##############################

ENDDATE
  2018        25  ##############################

INGESTED_AT
  2026        25  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 25 | 521.1K | 531.0K | 541.4K | 541.7K | 13.28M |
| Y | 25 | 138.6K | 161.4K | 184.6K | 186.2K | 4.11M |

## who

CITY by rows
        25  Minneapolis

CITY by dollars
      13.28M       25 rows  Minneapolis

SRC_SHA256 by rows
        25  61b37591264573be8d2cdb5bef75b58aafd37a450f6786edcbfe1da52a02d274

SRC_SHA256 by dollars
      13.28M       25 rows  61b37591264573be8d2cdb5bef75b58aafd37a450f6786edcbfe1da52a02

## who x when

CITY by REPORTEDDATE, dollars = X
  Minneapolis                               2018:13.28M

SRC_SHA256 by REPORTEDDATE, dollars = X
  61b37591264573be8d2cdb5bef75b58aafd37a45  2018:13.28M

## what

OBJECTID: 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%

CONTROLNBR: 3766358 8%, 3766147 8%, 3766065 8%, 3765931 8%, 3765560 8%, 3765532 8%, 3765496 8%, 3765279 8%, 3765270 8%, 3765154 8%, 3765128 8%, 3765065 8%

CITYCODE: MP 96%, UM 4%

CASENBR: 183916 8%, 182801 8%, 182406 8%, 182092 8%, 180392 8%, 180296 8%, 179625 8%, 178756 8%, 178438 8%, 178197 8%, 178013 8%, 177686 8%

CCN: MP 2018 183916 8%, MP 2018 182801 8%, MP 2018 182406 8%, MP 2018 182092 8%, MP 2018 180392 8%, MP 2018 180296 8%, MP 2018 179625 8%, MP 2018 178756 8%, MP 2018 178438 8%, MP 2018 178197 8%, MP 2018 178013 8%, MP 2018 177686 8%

OFFENSE: RECVEH 88%, NARC 8%, FLEE 4%

UCRCODE: 99 72%, 99  16%, 28 8%, 40  4%

TIME: 19:13 8%, 21:23 8%, 14:05 8%, 02:34 8%, 11:30 8%, 18:15 8%, 09:55 8%, 17:45 8%, 13:22 8%, 10:16 8%, 03:33 8%, 21:00 8%

HOUR: 19 11%, 21 11%, 14 11%, 11 11%, 09 11%, 17 11%, 03 11%, 02 5%, 18 5%, 13 5%, 10 5%, 16 5%

DAY: Wed 32%, Tue 24%, Thu 16%, Sun 12%, Fri 12%, Mon 4%

MONTH: May 72%, Jun 28%

PRECINCT: 03 36%, 04 20%, 02 16%, 01 12%, 05 12%, 18 4%

ADDRESS:  27 AV N / Knox AV N 8%, 000707 Tyler ST NE /    8%, 001026 11 AV SE /    8%,  17 AV S / 25 ST E 8%, 002736 Cedar AV S /    8%,  Polk ST NE / Spring ST NE 8%, 000027 15 ST N /    8%, 002726 Fremont AV N /    8%, 000112 6 ST S /    8%, 005739 Bossen TE  /    8%, 002721 Columbus AV S /    8%, 003527 Dight AV  /    8%

ZIPCODE: 55407 25%, 55411 17%, 55404 17%, 55413 8%, 55414 8%, 55403 4%, 55402 4%, 55417 4%, 55406 4%, 55419 4%, 55418 4%

LAT: 45.0078 8%, 44.99721 8%, 44.98853 8%, 44.95734 8%, 44.95246 8%, 44.99594 8%, 44.97489 8%, 45.0086 8%, 44.97714 8%, 44.89905 8%, 44.95301 8%, 44.93878 8%

LONG: -93.30189 8%, -93.24592 8%, -93.23574 8%, -93.24987 8%, -93.24777 8%, -93.24501 8%, -93.28436 8%, -93.29522 8%, -93.26936 8%, -93.22626 8%, -93.26352 8%, -93.22977 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 25 | 0 | 25 1; 24 1; 23 1; 22 1 |
| CONTROLNBR | category | 25 | 0 | 3766358 1; 3766147 1; 3766065 1; 3765931 1 |
| CITYCODE | category | 2 | 0 | MP 24; UM 1 |
| CASEYEAR | other | 1 | 0 | 2018 25 |
| CASENBR | category | 25 | 0 | 183916 1; 182801 1; 182406 1; 182092 1 |
| CCN | category | 25 | 0 | MP 2018 183916 1; MP 2018 182801 1; MP 2018 182406 1; MP 2018 182092 1 |
| OFFENSE | category | 3 | 0 | RECVEH 22; NARC 2; FLEE 1 |
| UCRCODE | category | 4 | 0 | 99 18; 99  4; 28 2; 40  1 |
| REPORTEDDATE | date | 25 | 0 | 1528151820000 1; 1528068000000 1; 1528036860000 1; 1527995760000 1 |
| BEGINDATE | date | 25 | 0 | 1528175580000 1; 1528096980000 1; 1528070700000 1; 1528029240000 1 |
| TIME | category | 25 | 0 | 19:13 1; 21:23 1; 14:05 1; 02:34 1 |
| HOUR | category | 18 | 0 | 19 2; 21 2; 14 2; 11 2 |
| DAY | category | 6 | 0 | Wed 8; Tue 6; Thu 4; Sun 3 |
| MONTH | category | 2 | 0 | May 18; Jun 7 |
| YEAR | other | 1 | 0 | 2018 25 |
| PRECINCT | category | 6 | 0 | 03 9; 04 5; 02 4; 01 3 |
| ADDRESS | category | 25 | 0 |  27 AV N / Knox AV N 1; 000707 Tyler ST NE /    1; 001026 11 AV SE /    1;  17 AV S / 25 ST E 1 |
| CITY | who | 1 | 0 | Minneapolis 25 |
| STATE | other | 1 | 0 | MN 25 |
| ZIPCODE | category | 12 | 1 | 55407 6; 55411 4; 55404 4; 55413 2 |
| ENTEREDDATE | date | 25 | 0 | 1528151732000 1; 1528068003000 1; 1528036856000 1; 1527995687000 1 |
| ENDDATE | date | 25 | 0 | 1528147380000 1; 1528061400000 1; 1528036860000 1; 1527993540000 1 |
| X | amount | 25 | 0 | 521065.74023612 1; 535551.02237219 1; 538188.6969318 1; 534550.84347914 1 |
| Y | amount | 25 | 0 | 179016.81833087 1; 175176.85775078 1; 172018.05175693 1; 160636.39025259 1 |
| LAT | category | 25 | 0 | 45.0078 1; 44.99721 1; 44.98853 1; 44.95734 1 |
| LONG | category | 25 | 0 | -93.30189 1; -93.24592 1; -93.23574 1; -93.24987 1 |
| GEOMETRY | category | 25 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:31:24.53999 25 |
| SOURCE_RUN_ID | audit | 1 | 0 | 66661bf0-cef2-48db-8521-4 25 |
| SRC_SHA256 | who | 1 | 0 | 61b37591264573be8d2cdb5be 25 |
