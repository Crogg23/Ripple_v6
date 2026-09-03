# PORTAL_CKA_SAN_JOSE_OPEN_DA_B374FEDA3D

rows 24  columns 17  scan 3.3s

roles: amount 4, audit 2, category 10, date 1, who 1

## when

INGESTED_AT
  2026        24  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREASQFT | 24 | 210.4K | 10.54M | 115.23M | 138.79M | 378.46M |
| AREAACRE | 24 | 4.83 | 241.97 | 2.6K | 3.2K | 8.7K |
| SHAPE_LENGTH | 24 | 2.1K | 16.7K | 75.0K | 83.4K | 496.1K |
| SHAPE_AREA | 24 | 210.4K | 10.54M | 115.23M | 138.79M | 378.46M |

## who

SRC_SHA256 by rows
        24  52d282d1b120badcaf68130a309a49dd2d232a55cee48e159eeb2959b162c381

SRC_SHA256 by dollars
     378.46M       24 rows  52d282d1b120badcaf68130a309a49dd2d232a55cee48e159eeb2959b162

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREASQFT
  52d282d1b120badcaf68130a309a49dd2d232a55  2026:378.46M

## what

OBJECTID: 26 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%

FACILITYID: 26 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%

INTID: 26 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%

DISTRICTNAME: CFD 17 8%, CFD11 8%, CFD8 8%, CFD 16 8%, CFD 15 8%, CFD 13 8%, CFD 14 8%, CFD 12 8%, MD 15 8%, MD 18 8%, MD 11 8%, MD 13 8%

DESCRIPTIVENAME: Communications Hill 15%, Capitol Expy - Evergreen Place 8%, Raleigh, Coronado, Via Del Oro 8%, Coyote Creek Trail/Berryessa 8%, Guadalupe Mines/Brookside Esta 8%, Hitachi 8%, Basking Ridge 8%, Silver Creek Valley 8%, Meadowlands 8%, Brokaw - Old Oakland Road 8%, Karina - O’Nel 8%, Evergreen 8%

APNPARCELCOUNT: 105 9%, 16 9%, 346 9%, 104 9%, 694 9%, 223 9%, 3499 9%, 434 9%, 196 9%, 10 9%, 2913 9%

CREATIONDATE: 2023/05/09 17:54:05+00 100%

LASTUPDATE: 2023/08/31 21:33:34+00 54%, 2023/08/31 21:33:14+00 46%

NOTES: MD 54%, CFD 46%

TYPE: MD 54%, CFD 46%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 24 | 0 | 26 1; 24 1; 23 1; 22 1 |
| FACILITYID | category | 24 | 0 | 26 1; 24 1; 23 1; 22 1 |
| INTID | category | 24 | 0 | 26 1; 24 1; 23 1; 22 1 |
| DISTRICTNAME | category | 24 | 0 | CFD 17 1; CFD11 1; CFD8 1; CFD 16 1 |
| DESCRIPTIVENAME | category | 23 | 0 | Communications Hill 2; Capitol Expy - Evergreen  1; Raleigh, Coronado, Via De 1; Coyote Creek Trail/Berrye 1 |
| APNPARCELCOUNT | category | 23 | 2 | 105 1; 16 1; 346 1; 104 1 |
| AREASQFT | amount | 24 | 0 | 2815464.71917717 1; 210442.29763357 1; 11458906.3493542 1; 3410291.37154516 1 |
| AREAACRE | amount | 23 | 0 | 64.63417629 1; 4.8310904 1; 263.06029268 1; 78.28951725 1 |
| CREATIONDATE | category | 2 | 23 | 2023/05/09 17:54:05+00 1 |
| LASTUPDATE | category | 2 | 0 | 2023/08/31 21:33:34+00 13; 2023/08/31 21:33:14+00 11 |
| NOTES | category | 2 | 0 | MD 13; CFD 11 |
| SHAPE_LENGTH | amount | 24 | 0 | 8273.54233057384 1; 2123.7276028544 1; 32883.8153101163 1; 8474.43881920629 1 |
| SHAPE_AREA | amount | 24 | 0 | 2815464.71918065 1; 210442.2976347 1; 11458906.3493674 1; 3410291.37153858 1 |
| TYPE | category | 2 | 0 | MD 13; CFD 11 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:17:13.55839 24 |
| SOURCE_RUN_ID | audit | 1 | 0 | 66f9c7f2-7c13-434b-9286-3 24 |
| SRC_SHA256 | who | 1 | 0 | 52d282d1b120badcaf68130a3 24 |
