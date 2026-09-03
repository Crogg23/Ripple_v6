# PORTAL_ARC_HARRIS_COUNTY_OP_19FE875D1D

rows 35  columns 39  scan 4.9s

roles: amount 2, audit 2, category 20, date 5, other 5, who 6

## when

SOURCE_DAT
  2024        35  ##############################

VAL_DATE
  2009         2  #####
  2010        13  ##############################
  2012         3  #######
  2018         2  #####
  2019         1  ##
  2022         7  ################
  2024         7  ################

CREATIONDATE
  2026        35  ##############################

EDITDATE
  2026        35  ##############################

INGESTED_AT
  2026        35  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 35 | 29.52 | 29.63 | 29.90 | 29.92 | 1.0K |
| LONGITUDE | 35 | -95.44 | -95.18 | -94.97 | -94.97 | -3.3K |

## who

NAICS_DESC by rows
        35  ELEMENTARY AND SECONDARY SCHOOLS

NAICS_DESC by dollars
        1.0K       35 rows  ELEMENTARY AND SECONDARY SCHOOLS

WEBSITE by rows
        35  NOT AVAILABLE

WEBSITE by dollars
        1.0K       35 rows  NOT AVAILABLE

CREATOR by rows
        35  JGuerraPct2

CREATOR by dollars
        1.0K       35 rows  JGuerraPct2

EDITOR by rows
        35  JGuerraPct2

EDITOR by dollars
        1.0K       35 rows  JGuerraPct2

## who x when

NAICS_DESC by VAL_DATE, dollars = LATITUDE
  ELEMENTARY AND SECONDARY SCHOOLS          2009:59.55 2010:385.93 2012:89.12 2018:59.42 2019:29.52 2022:207.43 2024:207.28

WEBSITE by VAL_DATE, dollars = LATITUDE
  NOT AVAILABLE                             2009:59.55 2010:385.93 2012:89.12 2018:59.42 2019:29.52 2022:207.43 2024:207.28

## what

OBJECTID: 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%

NCESID: BB981426 8%, 01325141 8%, A0303111 8%, 01328437 8%, A1171677 8%, 02061312 8%, BB943633 8%, BB201768 8%, A0771883 8%, 01325061 8%, 01325491 8%, BB201846 8%

NAME: QUBA ACADEMY 15%, ETERNITY CHRISTIAN SCHOOL 8%, ASSUMPTION CATHOLIC SCHOOL 8%, OUR REDEEMER LUTHERAN NORTH SC 8%, CHINQUAPIN PREPARATORY SCHOOL 8%, CREATIVE CORNER 8%, BAYTOWN CHRISTIAN ACADEMY 8%, HOLY TRINITY UMC DAY SCHOOL/DA 8%, HARBOR CHRISTIAN ACADEMY 8%, FIRST BAPTIST ACADEMY 8%, OUR LADY OF GUADALUPE SCHOOL 8%, ST JOSEPH CATHOLIC SCHOOL 8%

ADDRESS: 730 FM 1959 RD 15%, 1122 W RD 8%, 801 ROSELANE ST 8%, 215 RITTENHOUSE ST 8%, 2615 E WALLISVILLE RD 8%, 335 AUDRY LN 8%, 5555 N MAIN ST 8%, 13207 ORLEANS ST 8%, 623 KRESS ST 8%, 505 ROLLINGBROOK DR 8%, 2405 NAVIGATION BLVD 8%, 1811 CAROLINA ST 8%

CITY: HOUSTON 63%, PASADENA 14%, BAYTOWN 9%, FRIENDSWOOD 9%, HIGHLANDS 3%, WEBSTER 3%

ZIP: 77062 19%, 77505 12%, 77034 12%, 77546 12%, 77015 8%, 77521 8%, 77017 8%, 77058 8%, 77038 4%, 77037 4%, 77076 4%, 77562 4%

ZIP4: NOT AVAILABLE 31%, 2140 6%, 4696 6%, 3152 6%, 2209 6%, 8628 6%, 3699 6%, 4036 6%, 1510 6%, 6099 6%, 2404 6%, 6729 6%

TELEPHONE: (832) 582-7328 15%, (281) 999-5107 8%, (281) 447-2132 8%, (713) 694-0332 8%, (281) 426-5551 8%, (713) 450-3610 8%, (281) 421-4150 8%, (713) 453-7212 8%, (713) 637-4406 8%, (281) 420-2740 8%, (713) 224-6904 8%, (281) 422-9749 8%

TYPE: 1 43%, 3 20%, 7 17%, 2 11%, 4 9%

POPULATION: 14 19%, 8 12%, 79 12%, 43 6%, 231 6%, 163 6%, 10 6%, 250 6%, 7 6%, 89 6%, 84 6%, 198 6%

COUNTYFIPS: 20148 80%, 48201 20%

SOURCE: https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%, https://nces.ed.gov/surveys/ps 8%

VAL_METHOD: IMAGERY/OTHER 80%, IMAGERY 20%

LEVEL: 1 71%, 3 29%

ENROLLMENT: 13 18%, 6 12%, 4 12%, 68 12%, 39 6%, 218 6%, 146 6%, 8 6%, 228 6%, 81 6%, 76 6%, 183 6%

ST_GRADE: 2 74%, 3 11%, 11 6%, 10 3%, 1 3%, 4 3%

END_GRADE: 13 29%, 17 26%, 3 17%, 10 14%, 6 3%, 11 3%, 1 3%, 9 3%, 4 3%

FT_TEACHER: 1 21%, 4 14%, 8 14%, 2 7%, 9 7%, 6 7%, 14 7%, 3 7%, 13 4%, 17 4%, 22 4%, 15 4%

GLOBALID: 1a597c7b-baba-4172-b030-bf8ec6 8%, 0fe766e4-2a1f-46c3-b646-49712c 8%, 1799bda4-a5e3-440f-ad20-22bc09 8%, 507a888a-8dfe-434c-9e12-a77a16 8%, 79e331e0-f8cc-4b54-9b18-e29af3 8%, e95b7f1c-a394-4d17-85b4-90c4b0 8%, b4102045-3fe3-4ece-8109-16d1fb 8%, 30cbb35d-a977-488a-8d9f-10e4b5 8%, f20e0191-c80b-4ec8-bfa4-e61a46 8%, c9f47a7e-e030-4342-8fde-22fc0c 8%, 10d37475-34e1-44af-b6cf-3a0382 8%, 01e9a4aa-05d6-48e3-9387-549b9d 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 35 | 0 | 35 1; 34 1; 33 1; 32 1 |
| NCESID | category | 34 | 0 | BB981426 1; 01325141 1; A0303111 1; 01328437 1 |
| NAME | category | 34 | 0 | QUBA ACADEMY 2; ETERNITY CHRISTIAN SCHOOL 1; ASSUMPTION CATHOLIC SCHOO 1; OUR REDEEMER LUTHERAN NOR 1 |
| ADDRESS | category | 34 | 0 | 730 FM 1959 RD 2; 1122 W RD 1; 801 ROSELANE ST 1; 215 RITTENHOUSE ST 1 |
| CITY | category | 6 | 0 | HOUSTON 22; PASADENA 5; BAYTOWN 3; FRIENDSWOOD 3 |
| STATE | other | 1 | 0 | TX 35 |
| ZIP | category | 21 | 0 | 77062 5; 77505 3; 77034 3; 77546 3 |
| ZIP4 | category | 31 | 0 | NOT AVAILABLE 5; 2140 1; 4696 1; 3152 1 |
| TELEPHONE | category | 34 | 0 | (832) 582-7328 2; (281) 999-5107 1; (281) 447-2132 1; (713) 694-0332 1 |
| TYPE | category | 5 | 0 | 1 15; 3 7; 7 6; 2 4 |
| STATUS | other | 1 | 0 | 1 35 |
| POPULATION | category | 31 | 0 | 14 3; 8 2; 79 2; 43 1 |
| COUNTY | who | 1 | 0 | HARRIS 35 |
| COUNTYFIPS | category | 2 | 0 | 20148 28; 48201 7 |
| COUNTRY | other | 1 | 0 | USA 35 |
| LATITUDE | amount | 35 | 0 | 29.915223 1; 29.871768 1; 29.865639 1; 29.81972 1 |
| LONGITUDE | amount | 35 | 0 | -95.44024 1; -95.387446 1; -95.375369 1; -95.021961 1 |
| NAICS_CODE | other | 1 | 0 | 611110 35 |
| NAICS_DESC | who | 1 | 0 | ELEMENTARY AND SECONDARY  35 |
| SOURCE | category | 35 | 0 | https://nces.ed.gov/surve 1; https://nces.ed.gov/surve 1; https://nces.ed.gov/surve 1; https://nces.ed.gov/surve 1 |
| SOURCE_DAT | date | 1 | 0 | 1706680800000 35 |
| VAL_METHOD | category | 2 | 0 | IMAGERY/OTHER 28; IMAGERY 7 |
| VAL_DATE | date | 15 | 0 | 1655877600000 7; 1710396000000 4; 1266904800000 4; 1267423200000 3 |
| WEBSITE | who | 1 | 0 | NOT AVAILABLE 35 |
| LEVEL | category | 2 | 0 | 1 25; 3 10 |
| ENROLLMENT | category | 30 | 0 | 13 3; 6 2; 4 2; 68 2 |
| ST_GRADE | category | 6 | 0 | 2 26; 3 4; 11 2; 10 1 |
| END_GRADE | category | 9 | 0 | 13 10; 17 9; 3 6; 10 5 |
| FT_TEACHER | category | 19 | 0 | 1 6; 4 4; 8 4; 2 2 |
| SHELTER_ID | other | 1 | 0 | NOT AVAILABLE 35 |
| GLOBALID | category | 35 | 0 | 1a597c7b-baba-4172-b030-b 1; 0fe766e4-2a1f-46c3-b646-4 1; 1799bda4-a5e3-440f-ad20-2 1; 507a888a-8dfe-434c-9e12-a 1 |
| CREATIONDATE | date | 1 | 0 | 1768918783239 35 |
| CREATOR | who | 1 | 0 | JGuerraPct2 35 |
| EDITDATE | date | 1 | 0 | 1768918783239 35 |
| EDITOR | who | 1 | 0 | JGuerraPct2 35 |
| GEOMETRY | category | 35 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:16:27.60693 35 |
| SOURCE_RUN_ID | audit | 1 | 0 | 16cd30a3-f722-4f01-92ec-7 35 |
| SRC_SHA256 | who | 1 | 0 | d317ec5687c3f8637bfe1f7b2 35 |
