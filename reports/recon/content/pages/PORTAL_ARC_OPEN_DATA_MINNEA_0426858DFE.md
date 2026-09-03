# PORTAL_ARC_OPEN_DATA_MINNEA_0426858DFE

rows 110  columns 30  scan 3.1s

roles: amount 2, audit 2, category 7, date 5, other 13, who 2

## when

REPORTEDDATE
  2018       110  ##############################

BEGINDATE
  2018       110  ##############################

ENTEREDDATE
  2018       110  ##############################

ENDDATE
  2018       110  ##############################

INGESTED_AT
  2026       110  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 110 | 514.5K | 528.2K | 544.6K | 545.3K | 58.20M |
| Y | 110 | 140.0K | 161.0K | 193.0K | 193.9K | 18.04M |

## who

CITY by rows
       110  Minneapolis

CITY by dollars
      58.20M      110 rows  Minneapolis

SRC_SHA256 by rows
       110  72920be8f06dd01e27d785922e2e56c81d30ec475a8924a1ca7a5cf3938df9e1

SRC_SHA256 by dollars
      58.20M      110 rows  72920be8f06dd01e27d785922e2e56c81d30ec475a8924a1ca7a5cf3938d

## who x when

CITY by REPORTEDDATE, dollars = X
  Minneapolis                               2018:58.20M

SRC_SHA256 by REPORTEDDATE, dollars = X
  72920be8f06dd01e27d785922e2e56c81d30ec47  2018:58.20M

## what

OFFENSE: BURGD 85%, BURGB 15%

UCRCODE: 06 70%, 06  30%

DAY: Tue 26%, Wed 20%, Thu 13%, Sat 11%, Mon 10%, Fri 10%, Sun 10%

MONTH: May 82%, Jun 18%

HOUR: 08 13%, 20 13%, 22 11%, 21 8%, 00 8%, 10 8%, 13 7%, 06 7%, 01 7%, 12 6%, 18 6%, 09 6%

PRECINCT: 03 35%, 04 27%, 05 21%, 02 14%, 01 4%

ZIPCODE: 55407 17%, 55411 15%, 55408 13%, 55409 8%, 55412 8%, 55406 7%, 55414 6%, 55418 6%, 55417 6%, 55404 5%, 55430 4%, 55405 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 106 | 0 | 682 1; 675 1; 673 1; 666 1 |
| CONTROLNBR | other | 110 | 0 | 3766363 1; 3766327 1; 3766321 1; 3766303 1 |
| CITYCODE | other | 1 | 0 | MP 110 |
| CASEYEAR | other | 1 | 0 | 2018 110 |
| CASENBR | other | 110 | 0 | 184172 1; 183753 1; 183652 1; 183747 1 |
| CCN | other | 109 | 0 | MP 2018 184172 1; MP 2018 183753 1; MP 2018 183652 1; MP 2018 183747 1 |
| OFFENSE | category | 2 | 0 | BURGD 94; BURGB 16 |
| UCRCODE | category | 2 | 0 | 06 77; 06  33 |
| REPORTEDDATE | date | 110 | 0 | 1528152900000 1; 1528144680000 1; 1528142220000 1; 1528135860000 1 |
| BEGINDATE | date | 104 | 0 | 1528012800000 3; 1527847200000 2; 1527670800000 2; 1527631200000 2 |
| DAY | category | 7 | 0 | Tue 29; Wed 22; Thu 14; Sat 12 |
| MONTH | category | 2 | 0 | May 90; Jun 20 |
| YEAR | other | 1 | 0 | 2018 110 |
| TIME | other | 75 | 0 | 20:00 7; 08:00 5; 21:00 4; 00:00 4 |
| HOUR | category | 24 | 0 | 08 9; 20 9; 22 8; 21 6 |
| PRECINCT | category | 5 | 0 | 03 38; 04 30; 05 23; 02 15 |
| ADDRESS | other | 106 | 0 | 000800 Aldrich AV N /    2; 002939 Sheridan AV N /    2; 001455 Lake ST W /    2; 003337 Nicollet AV S /    1 |
| CITY | who | 1 | 0 | Minneapolis 110 |
| STATE | other | 1 | 0 | MN 110 |
| ZIPCODE | category | 18 | 0 | 55407 17; 55411 15; 55408 13; 55409 8 |
| ENTEREDDATE | date | 105 | 0 | 1528152962000 1; 1528144695000 1; 1528142111000 1; 1528135856000 1 |
| ENDDATE | date | 105 | 0 | 1527073200000 3; 1527613200000 2; 1527095460000 2; 1528149000000 1 |
| X | amount | 104 | 0 | 523928.72559737 2; 533653.78833333 2; 524073.75499999 2; 518345.41999999 2 |
| Y | amount | 105 | 0 | 171180.36277668 2; 180091.83141666 2; 157239.51491667 2; 154993.12833333 1 |
| LAT | other | 107 | 0 | 44.95491 2; 44.98629 2; 45.01075 2; 44.94807 2 |
| LONG | other | 107 | 0 | -93.29086 2; -93.3124 2; -93.29995 2; -93.27752 1 |
| GEOMETRY | other | 105 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:32:24.88407 110 |
| SOURCE_RUN_ID | audit | 1 | 0 | 50ea66be-da17-4711-9e99-f 110 |
| SRC_SHA256 | who | 1 | 0 | 72920be8f06dd01e27d785922 110 |
