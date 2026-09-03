# PORTAL_ARC_HARRIS_COUNTY_OP_E87E81379A

rows 34  columns 44  scan 4.3s

roles: amount 4, audit 2, category 24, date 5, empty 5, other 2, who 3

## when

SOURCEDATE
  2014         3  ####
  2017         1  #
  2020         3  ####
  2024        25  ##############################

VAL_DATE
  2014        13  ##############################
  2015         1  ##
  2017         4  #########
  2019         1  ##
  2020         3  #######
  2022         5  ############
  2024         5  ############

CREATIONDATE
  2026        34  ##############################

EDITDATE
  2026        34  ##############################

INGESTED_AT
  2026        34  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POPULATION | 32 | -999 | 60 | 472.79 | 532 | 2.1K |
| LATITUDE | 32 | 29.51 | 29.64 | 29.87 | 29.87 | 949.29 |
| LONGITUDE | 32 | -95.41 | -95.13 | -94.92 | -94.90 | -3.0K |
| BEDS | 32 | -999 | 60 | 472.79 | 532 | 2.1K |

## who

CREATOR by rows
        34  JGuerraPct2

CREATOR by dollars
        2.1K       34 rows  JGuerraPct2

EDITOR by rows
        34  JGuerraPct2

EDITOR by dollars
        2.1K       34 rows  JGuerraPct2

SRC_SHA256 by rows
        34  1932b82261064b918e3b7f96131260c5a78d4bb362f9f140c95b6721a1807c38

SRC_SHA256 by dollars
        2.1K       34 rows  1932b82261064b918e3b7f96131260c5a78d4bb362f9f140c95b6721a180

## who x when

CREATOR by VAL_DATE, dollars = POPULATION
  JGuerraPct2                               2014:2.0K 2015:4 2017:339 2019:20 2020:-885 2022:328 2024:292

EDITOR by VAL_DATE, dollars = POPULATION
  JGuerraPct2                               2014:2.0K 2015:4 2017:339 2019:20 2020:-885 2022:328 2024:292

## what

OBJECTID_1: 35 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%

OBJECTID: nan 15%, 15966.0 8%, 15402.0 8%, 16152.0 8%, 14428.0 8%, 14286.0 8%, 16165.0 8%, 15400.0 8%, 13845.0 8%, 13840.0 8%, 16156.0 8%, 14108.0 8%

ID: nan 15%, 0025177093 8%, 0136877076 8%, 0196785082 8%, 0029677070 8%, 0196784846 8%, 0196785095 8%, 0010477530 8%, 0076077521 8%, 0143877015 8%, 0196785086 8%, 0004677521 8%

NAME: Lyndon B. Johnson Hospital 8%, Ben Taub Hospital  8%, ST. ANTHONY'S HOSPITAL 8%, KINDRED HOSPITAL NORTH HOUSTON 8%, BMC HEIGHTS HOSPITAL 8%, UNITED MEMORIAL MEDICAL CENTER 8%, PATIENTS EMERGENCY ROOM 8%, EAST HOUSTON MEDICAL CENTER 8%, KINDRED HOSPITAL EAST HOUSTON 8%, ALTUS BAYTOWN HOSPITAL - BAYTO 8%, AD HOSPITAL EAST LLC 8%, CLEARSKY REHABILITATION HOSPIT 8%

ADDRESS: 5656 Kelley Street 8%, 1504 Taub Loop 8%, 2807 LITTLE YORK ROAD 8%, 7407 NORTH FREEWAY 8%, 510 W TIDWELL RD 8%, 510 WEST TIDWELL ROAD 8%, 10133 INTERSTATE 10 EAST 8%, 15149 WALLISVILLE ROAD 8%, 15101 EAST FREEWAY 8%, 1626 W BAKER RD 8%, 12950 EAST FREEWAY, SUITE 100 8%, 150 BLUE HERON PKWY 8%

CITY: HOUSTON 35%, WEBSTER 26%, BAYTOWN 15%, PASADENA 15%, Houston 3%, CHANNELVIEW 3%, LEAGUE CITY 3%

ZIP: 77598 32%, 77521 14%, 77505 11%, 77091 7%, 77504 7%, 77058 7%, 77026 4%, 77030 4%, 77093 4%, 77076 4%, 77049 4%, 77530 4%

ZIP4: NOT AVAILABLE 88%, nan 6%, 2999 3%, 5710 3%

TELEPHONE: NOT AVAILABLE 19%, (713) 359-2000 12%, (281) 286-1500 12%, 713-566-5000 6%, 713-873-2000 6%, (281) 618-8500 6%, (281) 618-8505 6%, (281) 576-0555 6%, (281) 988-9800 6%, (281) 837-7600 6%, (713) 330-3887 6%, (281) 724-5442 6%

TYPE: GENERAL ACUTE CARE 62%, LONG TERM CARE 15%, PSYCHIATRIC 12%, REHABILITATION 9%, SPECIAL 3%

STATUS: OPEN 79%, CLOSED 21%

COUNTY: HARRIS 94%, CHAMBERS 3%, GALVESTON 3%

NAICS_CODE: 622110 56%, 622310 26%, 622210 12%, nan 6%

NAICS_DESC: GENERAL MEDICAL AND SURGICAL H 56%, PSYCHIATRIC AND SUBSTANCE ABUS 12%, EXTENDED CARE HOSPITALS (EXCEP 9%, SPECIALTY (EXCEPT PSYCHIATRIC  9%, REHABILITATION HOSPITALS (EXCE 9%, nan 6%

SOURCE: https://www.hhs.texas.gov/prov 74%, http://www.dshs.state.tx.us/ch 9%, https://hhs.texas.gov/doing-bu 9%, nan 6%, http://www.dshs.texas.gov/faci 3%

VAL_METHOD: IMAGERY/OTHER 47%, IMAGERY 44%, nan 6%, UNVERIFIED 3%

WEBSITE: NOT AVAILABLE 56%, https://www.harrishealth.org/l 4%, https://www.harrishealth.org/l 4%, http://www.stanthonyshouston.c 4%, www.khnorthhouston.com 4%, http://www.ummc.care/ 4%, http://www.kheasthouston.com 4%, http://www.altusbaytownhospita 4%, http://adhealthcare.net/ 4%, http://www.khbayareahouston.co 4%, http://www.pinevalleyspecialty 4%, http://www.bayshoremedical.com 4%

STATE_ID: NOT AVAILABLE 36%, nan 9%, 100254 9%, 100301 9%, 8450 5%, 100548 5%, 100567 5%, 100344 5%, 100620 5%, 405 5%, 349 5%, 6941 5%

OWNER: PROPRIETARY 65%, NOT AVAILABLE 15%, NON-PROFIT 12%, nan 6%, GOVERNMENT - STATE 3%

TTL_STAFF: -999.0 94%, nan 6%

TRAUMA: NOT AVAILABLE 79%, LEVEL III 9%, nan 6%, LEVEL IV 3%, LEVEL II 3%

HELIPAD: N 65%, Y 29%, nan 6%

GLOBALID: c7ec6a8b-4488-45d1-8946-691df2 8%, c508a8c2-7b1a-48b8-8f80-091831 8%, c6716c63-031a-4a15-8a40-428c98 8%, 4754b2be-5b9f-42a5-a713-3ece26 8%, a553ef4c-7904-4369-861a-249005 8%, 81dc1b60-37ff-4e3b-8750-8d8c3a 8%, 8196170b-e01e-4736-a654-0d1384 8%, 6e19469b-37a1-4740-bc71-2c7d59 8%, e63a3f89-da20-4d1a-98a0-67381f 8%, fb55727d-7bb6-4628-81e7-97a25d 8%, 29d38302-bd5a-4992-8a74-a1330a 8%, 69a733e2-bd4b-4e9d-8974-2a0103 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | category | 34 | 0 | 35 1; 33 1; 32 1; 31 1 |
| OBJECTID | category | 33 | 0 | nan 2; 15966.0 1; 15402.0 1; 16152.0 1 |
| ID | category | 33 | 0 | nan 2; 0025177093 1; 0136877076 1; 0196785082 1 |
| NAME | category | 33 | 0 | Lyndon B. Johnson Hospita 1; Ben Taub Hospital  1; ST. ANTHONY'S HOSPITAL 1; KINDRED HOSPITAL NORTH HO 1 |
| ADDRESS | category | 34 | 0 | 5656 Kelley Street 1; 1504 Taub Loop 1; 2807 LITTLE YORK ROAD 1; 7407 NORTH FREEWAY 1 |
| CITY | category | 7 | 0 | HOUSTON 12; WEBSTER 9; BAYTOWN 5; PASADENA 5 |
| STATE | other | 1 | 0 | TX 34 |
| ZIP | category | 18 | 0 | 77598 9; 77521 4; 77505 3; 77091 2 |
| ZIP4 | category | 4 | 0 | NOT AVAILABLE 30; nan 2; 2999 1; 5710 1 |
| TELEPHONE | category | 30 | 0 | NOT AVAILABLE 3; (713) 359-2000 2; (281) 286-1500 2; 713-566-5000 1 |
| TYPE | category | 5 | 0 | GENERAL ACUTE CARE 21; LONG TERM CARE 5; PSYCHIATRIC 4; REHABILITATION 3 |
| STATUS | category | 2 | 0 | OPEN 27; CLOSED 7 |
| POPULATION | amount | 28 | 0 | nan 2; 117.0 2; 4.0 2; 61.0 2 |
| COUNTY | category | 3 | 0 | HARRIS 32; CHAMBERS 1; GALVESTON 1 |
| COUNTRY | other | 1 | 0 | USA 34 |
| LATITUDE | amount | 33 | 0 | nan 2; 29.871493220000048 1; 29.867380190000063 1; 29.84795040000006 1 |
| LONGITUDE | amount | 33 | 0 | nan 2; -95.34211248999998 1; -95.40800377999994 1; -95.40847099999996 1 |
| NAICS_CODE | category | 4 | 0 | 622110 19; 622310 9; 622210 4; nan 2 |
| NAICS_DESC | category | 6 | 0 | GENERAL MEDICAL AND SURGI 19; PSYCHIATRIC AND SUBSTANCE 4; EXTENDED CARE HOSPITALS ( 3; SPECIALTY (EXCEPT PSYCHIA 3 |
| SOURCE | category | 5 | 0 | https://www.hhs.texas.gov 25; http://www.dshs.state.tx. 3; https://hhs.texas.gov/doi 3; nan 2 |
| SOURCEDATE | date | 5 | 0 | 1709877600000.0 25; 1411452000000.0 3; 1599026400000.0 3; nan 2 |
| VAL_METHOD | category | 4 | 0 | IMAGERY/OTHER 16; IMAGERY 15; nan 2; UNVERIFIED 1 |
| VAL_DATE | date | 19 | 0 | 1392012000000.0 7; 1588917600000.0 3; nan 2; 1391407200000.0 2 |
| WEBSITE | category | 21 | 0 | NOT AVAILABLE 14; https://www.harrishealth. 1; https://www.harrishealth. 1; http://www.stanthonyshous 1 |
| STATE_ID | category | 24 | 0 | NOT AVAILABLE 8; nan 2; 100254 2; 100301 2 |
| OWNER | category | 5 | 0 | PROPRIETARY 22; NOT AVAILABLE 5; NON-PROFIT 4; nan 2 |
| TTL_STAFF | category | 2 | 0 | -999.0 32; nan 2 |
| BEDS | amount | 28 | 0 | nan 2; 117.0 2; 4.0 2; 61.0 2 |
| TRAUMA | category | 5 | 0 | NOT AVAILABLE 27; LEVEL III 3; nan 2; LEVEL IV 1 |
| HELIPAD | category | 3 | 0 | N 22; Y 10; nan 2 |
| GENERATOR_ONSITE | empty | 1 | 34 |  |
| SELF_SUFFICIENT_ELECTRICITY | empty | 1 | 34 |  |
| IN_100_YR_FLOODPLAIN | empty | 1 | 34 |  |
| IN_500_YR_FLOODPLAIN | empty | 1 | 34 |  |
| IN_SURGE_SLOSH_AREA | empty | 1 | 34 |  |
| GLOBALID | category | 33 | 0 | c7ec6a8b-4488-45d1-8946-6 1; c508a8c2-7b1a-48b8-8f80-0 1; c6716c63-031a-4a15-8a40-4 1; 4754b2be-5b9f-42a5-a713-3 1 |
| CREATIONDATE | date | 1 | 0 | 1768918779032 34 |
| CREATOR | who | 1 | 0 | JGuerraPct2 34 |
| EDITDATE | date | 1 | 0 | 1768918779032 34 |
| EDITOR | who | 1 | 0 | JGuerraPct2 34 |
| GEOMETRY | category | 34 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:16:12.17365 34 |
| SOURCE_RUN_ID | audit | 1 | 0 | d6418c8f-d279-4050-813a-2 34 |
| SRC_SHA256 | who | 1 | 0 | 1932b82261064b918e3b7f961 34 |
