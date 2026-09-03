# PORTAL_CKA_HOUSTON_OPEN_DAT_49FFAB9EDC

rows 42  columns 10  scan 2.8s

roles: audit 2, category 5, date 3, who 1

## when

PER_EFFECTIVE_START_DATE
  2014        27  ##############################
  2015        15  #################

PER_EFFECTIVE_END_DATE
  2015        27  ##############################
  2016        15  #################

INGESTED_AT
  2026        42  ##############################

## who

SRC_SHA256 by rows
        42  2704a440cd5733e11622bd8733ef7d50054978a4fd7187f7f43b6eb625f19104

## who x when

SRC_SHA256 by PER_EFFECTIVE_START_DATE
  2704a440cd5733e11622bd8733ef7d50054978a4  2014:27 2015:15

## what

ENT_GROUP_NAME: Greenstreet 24%, HOUSTON FIRST CORPORATION 14%, HOUSTON ASTROS BASEBALL CLUB 10%, POST APARTMENT HOMES, LP 10%, HOUSTON MUSEUM OF FINE ARTS 10%, Henke & Pillot 5%, COURTLAND SQUARE LTD 5%, The Corinthian 5%, Massa's Seafood Grill 5%, BACKSTREET CAFE 5%, LANCASTER HOTEL 5%, Batanga 5%

PER_NUMBER: VZP0266 8%, VZP0263 8%, VZP0261 8%, VZP0259 8%, VZP0258 8%, VZP0254 8%, VZP0255 8%, VZP0253 8%, VZP0246 8%, VZP0264 8%, VZP0248 8%, VZP0245 8%

PER_VL: 800 Congress, North Side 9%, 500 STUART, NORTH SIDE 9%, 200 FANNIN 9%, 1331 LAMAR 9%, 1100 S. SHEPHERD (SOUTH SIDE) 9%, 1600 TEXAS, NORTH SIDE 9%, 500 CRAWFORD, EAST SIDE 9%, 300 GRAY 9%, 700 Texas, North Side 9%, 900 Congress, South Side 9%, 1000 RUSK @ FANNIN (NORTH SIDE 9%

PER_VOH: Monday - Sunday, Daily 24hrs. 19%, AS NEEDED - PER ZONE STIPULATI 12%, 8:00am - 1:30am, Daily 12%, MONDAY-SUNDAY, 11:00 AM - 3:00 12%, Thursday - Sunday, 6:00pm - 2: 6%, MONDAY - SUNDAY, 10:00AM - 12: 6%, MONDAY - SUNDAY, 6:00 PM - 3:0 6%, FRIDAY - SATURDAY, 6:00PM - 12 6%, SUNDAY - SATURDAY, 11:00AM TO  6%, MONDAY - SUNDAY, 10:00AM - 2:0 6%, Tuesday - Sunday, 6:00PM - 1:0 6%

PER_VS: State Parking Services Inc. 21%, COURTESY PARKING SERVICE 17%, SOVEREIGN SERVICES OF HOUSTON 12%, R and R Valet Services 12%, LAZ PARKING TEXAS, LLC 8%, Sovereign Services 8%, Service Pro Parking LLC 4%, R AND R VALET SERVICES 4%, S.P. CHOICE VALET PARKING 4%, CMV VALET 4%, Valet Downtown Houston LLC 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENT_GROUP_NAME | category | 33 | 0 | Greenstreet 5; HOUSTON FIRST CORPORATION 3; HOUSTON ASTROS BASEBALL C 2; POST APARTMENT HOMES, LP 2 |
| PER_NUMBER | category | 42 | 0 | VZP0266 1; VZP0263 1; VZP0261 1; VZP0259 1 |
| PER_EFFECTIVE_START_DATE | date | 32 | 0 | 2014-11-24 00:00:00 5; 2014-08-12 00:00:00 3; 2015-02-26 00:00:00 2; 2015-01-27 00:00:00 2 |
| PER_EFFECTIVE_END_DATE | date | 32 | 0 | 2015-11-24 23:59:59 5; 2015-08-12 23:59:59 3; 2016-02-26 23:59:59 2; 2016-01-27 23:59:59 2 |
| PER_VL | category | 40 | 3 | 800 Congress, North Side 1; 500 STUART, NORTH SIDE 1; 200 FANNIN 1; 1331 LAMAR 1 |
| PER_VOH | category | 35 | 3 | Monday - Sunday, Daily 24 3; AS NEEDED - PER ZONE STIP 2; 8:00am - 1:30am, Daily 2; MONDAY-SUNDAY, 11:00 AM - 2 |
| PER_VS | category | 26 | 4 | State Parking Services In 5; COURTESY PARKING SERVICE 4; SOVEREIGN SERVICES OF HOU 3; R and R Valet Services 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:11:58.93392 42 |
| SOURCE_RUN_ID | audit | 1 | 0 | 101432e1-757a-441b-82c0-3 42 |
| SRC_SHA256 | who | 1 | 0 | 2704a440cd5733e11622bd873 42 |
