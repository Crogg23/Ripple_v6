# PORTAL_CKA_CALIFORNIA_OPEN_7F65D27DB7

rows 71  columns 18  scan 4.0s

roles: amount 2, audit 2, category 6, date 3, empty 1, other 3, who 2

## when

START_DATE_TIME
  2026        71  ##############################

ESTIMATED_RESTORATION_DATE_TIME
  2026        68  ##############################

INGESTED_AT
  2026        71  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 71 | -13.75M | -13.41M | -12.95M | -12.92M | -948.53M |
| Y | 71 | 3.98M | 4.40M | 5.00M | 5.00M | 309.41M |

## who

OUTAGE_STATUS by rows
        71  Active

OUTAGE_STATUS by dollars
    -948.53M       71 rows  Active

SRC_SHA256 by rows
        71  7f181bd6008e20690eea0e90f85b9b620189bc2d0059acaa5c798a0114fab2b1

SRC_SHA256 by dollars
    -948.53M       71 rows  7f181bd6008e20690eea0e90f85b9b620189bc2d0059acaa5c798a0114fa

## who x when

OUTAGE_STATUS by START_DATE_TIME, dollars = X
  Active                                    2026:-948.53M

SRC_SHA256 by START_DATE_TIME, dollars = X
  7f181bd6008e20690eea0e90f85b9b620189bc2d  2026:-948.53M

## what

UTILITYCOMPANY: PGE 59%, SCE 41%

CAUSE: Upgrading Equipment 27%, EMERG REPAIRS 17%, Pole Upgrade 13%, PATROLLING 10%, Equipment Problems 10%, BRKN UG EQUIPMNT 6%, PLNND SHUTDOWN 6%, THRD PARTY 4%, Cable Upgrade 4%, FOREIGN OBJ 2%, BRKN POLE EQUIPMNT 2%

IMPACTED_CUSTOMERS: 1 47%, 4 11%, 7 9%, 5 4%, 10 4%, 36 4%, 9 4%, 34 4%, 25 4%, 3 4%, 110 2%, 15 2%

COUNTY: LOS ANGELES 15%, SAN JOAQUIN 13%, ORANGE 12%, RIVERSIDE 10%, FRESNO 8%, SAN BERNARDINO 8%, VENTURA 8%, MONTEREY 6%, SANTA CLARA 6%, EL DORADO 6%, SAN FRANCISCO 6%, SUTTER 4%

OUTAGE_TYPE: Not Planned 63%, Planned 37%

OUTAGETYPECOLOR: #ffaa00 63%, #a8a800 37%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 70 | 0 | 42286337 1; 42286336 1; 42286335 1; 42286334 1 |
| UTILITYCOMPANY | category | 2 | 0 | PGE 42; SCE 29 |
| START_DATE_TIME | date | 65 | 0 | 7/1/2026 8:00:00 PM 4; 7/2/2026 1:00:00 AM 2; 7/1/2026 9:30:00 PM 2; 7/1/2026 9:00:00 PM 2 |
| ESTIMATED_RESTORATION_DATE_TIME | date | 32 | 3 | 7/2/2026 12:00:00 PM 12; 7/2/2026 10:00:00 AM 6; 7/2/2026 11:00:00 AM 5; 7/2/2026 1:00:00 PM 4 |
| CAUSE | category | 19 | 12 | Upgrading Equipment 14; EMERG REPAIRS 9; Pole Upgrade 7; PATROLLING 5 |
| IMPACTED_CUSTOMERS | category | 35 | 0 | 1 22; 4 5; 7 4; 5 2 |
| COUNTY | category | 27 | 0 | LOS ANGELES 8; SAN JOAQUIN 7; ORANGE 6; RIVERSIDE 5 |
| OUTAGE_STATUS | who | 1 | 0 | Active 71 |
| OUTAGE_TYPE | category | 2 | 0 | Not Planned 45; Planned 26 |
| GLOBALID | other | 72 | 0 | 4b888ef6-d5e5-4d52-b895-7 1; b477a163-3900-4c8f-a071-5 1; 4218f316-dbef-4498-9be2-2 1; 2f6ba09b-abb3-4e0b-ab5b-2 1 |
| OUTAGETYPECOLOR | category | 2 | 0 | #ffaa00 45; #a8a800 26 |
| OUTAGESTATUSCOLOR | empty | 1 | 71 |  |
| INDICENT_ID | other | 70 | 0 | 295586 1; 295585 1; 295583 1; 295579 1 |
| X | amount | 72 | 0 | -13554754.3443332 1; -13653603.8257678 1; -13550906.0295365 1; -13666690.5451055 1 |
| Y | amount | 72 | 0 | 4714930.00845547 1; 4935454.37839999 1; 4663239.77524016 1; 4648218.20814095 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:11:12.58927 71 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7866b0e9-f160-4d35-a42d-9 71 |
| SRC_SHA256 | who | 1 | 0 | 7f181bd6008e20690eea0e90f 71 |
