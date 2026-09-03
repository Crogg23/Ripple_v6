# PORTAL_CKA_WPRDC_ALLEGHENY_4D7552BF98

rows 79  columns 19  scan 2.7s

roles: amount 2, audit 2, category 11, date 1, other 3, who 1

## when

INGESTED_AT
  2026        79  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 79 | 40.38 | 40.44 | 40.49 | 40.49 | 3.2K |
| LONGITUDE | 79 | -80.01 | -79.96 | -79.89 | -79.89 | -6.3K |

## who

SRC_SHA256 by rows
        79  b4755fe3995eaa4d39dad06a8db306a460a5b43c4c336f2b393fe6c19a59450b

SRC_SHA256 by dollars
        3.2K       79 rows  b4755fe3995eaa4d39dad06a8db306a460a5b43c4c336f2b393fe6c19a59

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  b4755fe3995eaa4d39dad06a8db306a460a5b43c  2026:3.2K

## what

LOCATOR_STREET: Saline St 11%, Melwood Ave 11%, Gold Way 9%, Parkview Blvd 9%, Boundary St 9%, Maytide St 7%, Mission St 7%, Venture St 7%, Beechwood Blvd 7%, Webster Ave 7%, Finance St 7%, Jacob St 7%

PAVEMENT: 1755 14%, 4523 14%, 2077 11%, 17688 11%, 15541 8%, 15080 8%, 9257 8%, 16410 5%, 15244 5%, 19094 5%, 9592 5%, 10908 5%

SPEED_HUMP_MATERIAL: Asphalt 100%

NEIGHBORHOOD: Squirrel Hill South 26%, Carrick 13%, North Oakland 9%, Polish Hill 9%, South Side Slopes 6%, Perry North 6%, Upper Hill 6%, Homewood South 6%, Brookline 6%, Garfield 4%, Squirrel Hill North 4%, South Side Flats 4%

COUNCIL_DISTRICT: 5 23%, 4 18%, 7 14%, 6 11%, 9 10%, 3 10%, 1 5%, 8 5%, 2 4%

WARD: 14 18%, 29 13%, 5 13%, 15 10%, 6 8%, 32 7%, 11 6%, 16 6%, 26 6%, 13 6%, 4 4%, 17 4%

TRACT: 42003141400 20%, 42003290400 10%, 42003060500 10%, 42003562000 8%, 42003160800 7%, 42003260700 7%, 42003140800 7%, 42003050600 7%, 42003130300 7%, 42003320600 7%, 42003290100 5%, 42003140100 5%

PUBLIC_WORKS_DIVISION: 3 61%, 2 16%, 5 10%, 6 8%, 1 5%

PLI_DIVISION: 14 18%, 29 13%, 5 13%, 15 10%, 6 8%, 32 7%, 11 6%, 16 6%, 26 6%, 13 6%, 4 4%, 17 4%

POLICE_ZONE: 4 35%, 3 25%, 5 16%, 2 13%, 1 5%, 6 5%

FIRE_ZONE: 4-23 16%, 2-20 9%, 2-21 9%, 2-15 9%, 2-6 9%, 2-23 8%, 2-8 8%, 3-4 6%, 4-24 6%, 1-15 6%, 2-22 6%, 3-17 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 79 | 0 | 1352764849 1; 724005157 1; 965432088 1; 1379652923 1 |
| HUMP_ID | other | 79 | 0 | 79 1; 78 1; 77 1; 76 1 |
| LOCATOR_ADDRESS_NUMBER | other | 74 | 6 | 273 1; 217 1; 378 1; 622 1 |
| LOCATOR_STREET | category | 22 | 0 | Saline St 6; Melwood Ave 6; Gold Way 5; Parkview Blvd 5 |
| PAVEMENT | category | 46 | 0 | 1755 5; 4523 5; 2077 4; 17688 4 |
| SPEED_HUMP_MATERIAL | category | 2 | 5 | Asphalt 74 |
| NEIGHBORHOOD | category | 18 | 0 | Squirrel Hill South 18; Carrick 9; North Oakland 6; Polish Hill 6 |
| COUNCIL_DISTRICT | category | 9 | 0 | 5 18; 4 14; 7 11; 6 9 |
| WARD | category | 15 | 0 | 14 13; 29 9; 5 9; 15 7 |
| TRACT | category | 24 | 0 | 42003141400 12; 42003290400 6; 42003060500 6; 42003562000 5 |
| PUBLIC_WORKS_DIVISION | category | 5 | 0 | 3 48; 2 13; 5 8; 6 6 |
| PLI_DIVISION | category | 15 | 0 | 14 13; 29 9; 5 9; 15 7 |
| POLICE_ZONE | category | 6 | 0 | 4 28; 3 20; 5 13; 2 10 |
| FIRE_ZONE | category | 17 | 0 | 4-23 10; 2-20 6; 2-21 6; 2-15 6 |
| LATITUDE | amount | 79 | 0 | 40.38444369 1; 40.38435854 1; 40.38449785 1; 40.3839836 1 |
| LONGITUDE | amount | 78 | 0 | -79.98382743 1; -79.98262603 1; -79.98649778 1; -79.9906467 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:30:02.33756 79 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5b6e2150-b5b0-41ab-9396-5 79 |
| SRC_SHA256 | who | 1 | 0 | b4755fe3995eaa4d39dad06a8 79 |
