# PORTAL_ARC_HARRIS_COUNTY_OP_87F4853C1A

rows 30  columns 42  scan 2.8s

roles: amount 2, audit 2, category 24, date 3, empty 5, other 5, who 2

## when

SOURCEDATE
  2014         3  ####
  2017         1  #
  2020         3  ####
  2024        23  ##############################

VAL_DATE
  2014        12  ##############################
  2015         1  ##
  2017         4  ##########
  2019         1  ##
  2020         3  ########
  2022         4  ##########
  2024         5  ############

INGESTED_AT
  2026        30  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 30 | 29.53 | 29.64 | 29.87 | 29.87 | 889.96 |
| LONGITUDE | 30 | -95.41 | -95.14 | -94.95 | -94.95 | -2.9K |

## who

COUNTY by rows
        30  HARRIS

COUNTY by dollars
      889.96       30 rows  HARRIS

SRC_SHA256 by rows
        30  2276aece3bd41df83f67f15b6cbb7423ae389277d1cd166a78502d586b444436

SRC_SHA256 by dollars
      889.96       30 rows  2276aece3bd41df83f67f15b6cbb7423ae389277d1cd166a78502d586b44

## who x when

COUNTY by VAL_DATE, dollars = LATITUDE
  HARRIS                                    2014:355.89 2015:29.77 2017:118.39 2019:29.62 2020:89.39 2022:118.29 2024:148.61

SRC_SHA256 by VAL_DATE, dollars = LATITUDE
  2276aece3bd41df83f67f15b6cbb7423ae389277  2014:355.89 2015:29.77 2017:118.39 2019:29.62 2020:89.39 2022:118.29 2024:148.61

## what

OBJECTID_1: 32 8%, 31 8%, 30 8%, 29 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%

OBJECTID: 15966 8%, 15402 8%, 16152 8%, 14428 8%, 16165 8%, 15400 8%, 13845 8%, 13840 8%, 16156 8%, 14108 8%, 15649 8%, 15696 8%

ID: 0025177093 8%, 0136877076 8%, 0196785082 8%, 0029677070 8%, 0196785095 8%, 0010477530 8%, 0076077521 8%, 0143877015 8%, 0196785086 8%, 0004677521 8%, 0076877520 8%, 0028377087 8%

NAME: ST. ANTHONY'S HOSPITAL 8%, KINDRED HOSPITAL NORTH HOUSTON 8%, BMC HEIGHTS HOSPITAL 8%, UNITED MEMORIAL MEDICAL CENTER 8%, EAST HOUSTON MEDICAL CENTER 8%, KINDRED HOSPITAL EAST HOUSTON 8%, ALTUS BAYTOWN HOSPITAL - BAYTO 8%, AD HOSPITAL EAST LLC 8%, CLEARSKY REHABILITATION HOSPIT 8%, HOUSTON METHODIST BAYTOWN HOSP 8%, KINDRED HOSPITAL BAYTOWN 8%, PINE VALLEY SPECIALTY HOSPITAL 8%

ADDRESS: 2807 LITTLE YORK ROAD 8%, 7407 NORTH FREEWAY 8%, 510 W TIDWELL RD 8%, 510 WEST TIDWELL ROAD 8%, 15149 WALLISVILLE ROAD 8%, 15101 EAST FREEWAY 8%, 1626 W BAKER RD 8%, 12950 EAST FREEWAY, SUITE 100 8%, 150 BLUE HERON PKWY 8%, 4401 GARTH RD 8%, 1700 JAMES BOWIE DRIVE, 3RD FL 8%, 6160 SOUTH LOOP EAST 8%

CITY: HOUSTON 37%, WEBSTER 30%, PASADENA 17%, BAYTOWN 13%, CHANNELVIEW 3%

ZIP: 77598 33%, 77521 11%, 77505 11%, 77091 7%, 77504 7%, 77058 7%, 77093 4%, 77076 4%, 77049 4%, 77530 4%, 77015 4%, 77520 4%

ZIP4: NOT AVAILABLE 93%, 2999 3%, 5710 3%

TELEPHONE: NOT AVAILABLE 19%, (713) 359-2000 12%, (281) 286-1500 12%, (281) 618-8500 6%, (281) 618-8505 6%, (281) 988-9800 6%, (281) 837-7600 6%, (713) 330-3887 6%, (281) 724-5442 6%, (281) 420-8600 6%, (281) 420-7800 6%, (713) 640-2400 6%

TYPE: GENERAL ACUTE CARE 63%, LONG TERM CARE 17%, PSYCHIATRIC 10%, REHABILITATION 10%

STATUS: OPEN 77%, CLOSED 23%

POPULATION: 117 12%, 4 12%, 61 12%, 20 12%, 60 12%, 39 6%, -999 6%, 83 6%, 14 6%, 36 6%, 230 6%, 31 6%

NAICS_CODE: 622110 60%, 622310 30%, 622210 10%

NAICS_DESC: GENERAL MEDICAL AND SURGICAL H 60%, EXTENDED CARE HOSPITALS (EXCEP 10%, SPECIALTY (EXCEPT PSYCHIATRIC  10%, PSYCHIATRIC AND SUBSTANCE ABUS 10%, REHABILITATION HOSPITALS (EXCE 10%

SOURCE: https://www.hhs.texas.gov/prov 77%, http://www.dshs.state.tx.us/ch 10%, https://hhs.texas.gov/doing-bu 10%, http://www.dshs.texas.gov/faci 3%

VAL_METHOD: IMAGERY/OTHER 50%, IMAGERY 47%, UNVERIFIED 3%

WEBSITE: NOT AVAILABLE 54%, http://www.stanthonyshouston.c 4%, www.khnorthhouston.com 4%, http://www.ummc.care/ 4%, http://www.kheasthouston.com 4%, http://www.altusbaytownhospita 4%, http://adhealthcare.net/ 4%, http://www.khbayareahouston.co 4%, http://www.pinevalleyspecialty 4%, http://www.bayshoremedical.com 4%, http://www.sacredoakmedical.co 4%, https://memorialhermann.org/lo 4%

STATE_ID: NOT AVAILABLE 38%, 100254 10%, 100301 10%, 8450 5%, 100567 5%, 100344 5%, 100620 5%, 405 5%, 349 5%, 6941 5%, 100459 5%, 100081 5%

ALT_NAME: NOT AVAILABLE 97%, TEXAS SPECIALTY HOSPITAL AT HO 3%

OWNER: PROPRIETARY 70%, NOT AVAILABLE 17%, NON-PROFIT 10%, GOVERNMENT - STATE 3%

BEDS: 117 12%, 4 12%, 61 12%, 20 12%, 60 12%, 39 6%, -999 6%, 83 6%, 14 6%, 36 6%, 230 6%, 31 6%

TRAUMA: NOT AVAILABLE 83%, LEVEL III 10%, LEVEL IV 3%, LEVEL II 3%

HELIPAD: N 70%, Y 30%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | category | 30 | 0 | 32 1; 31 1; 30 1; 29 1 |
| OBJECTID | category | 30 | 0 | 15966 1; 15402 1; 16152 1; 14428 1 |
| ID | category | 30 | 0 | 0025177093 1; 0136877076 1; 0196785082 1; 0029677070 1 |
| NAME | category | 29 | 0 | ST. ANTHONY'S HOSPITAL 1; KINDRED HOSPITAL NORTH HO 1; BMC HEIGHTS HOSPITAL 1; UNITED MEMORIAL MEDICAL C 1 |
| ADDRESS | category | 30 | 0 | 2807 LITTLE YORK ROAD 1; 7407 NORTH FREEWAY 1; 510 W TIDWELL RD 1; 510 WEST TIDWELL ROAD 1 |
| CITY | category | 5 | 0 | HOUSTON 11; WEBSTER 9; PASADENA 5; BAYTOWN 4 |
| STATE | other | 1 | 0 | TX 30 |
| ZIP | category | 15 | 0 | 77598 9; 77521 3; 77505 3; 77091 2 |
| ZIP4 | category | 3 | 0 | NOT AVAILABLE 28; 2999 1; 5710 1 |
| TELEPHONE | category | 26 | 0 | NOT AVAILABLE 3; (713) 359-2000 2; (281) 286-1500 2; (281) 618-8500 1 |
| TYPE | category | 4 | 0 | GENERAL ACUTE CARE 19; LONG TERM CARE 5; PSYCHIATRIC 3; REHABILITATION 3 |
| STATUS | category | 2 | 0 | OPEN 23; CLOSED 7 |
| POPULATION | category | 25 | 0 | 117 2; 4 2; 61 2; 20 2 |
| COUNTY | who | 1 | 0 | HARRIS 30 |
| COUNTYFIPS | other | 1 | 0 | 48201 30 |
| COUNTRY | other | 1 | 0 | USA 30 |
| LATITUDE | amount | 30 | 0 | 29.871493220000048 1; 29.867380190000063 1; 29.84795040000006 1; 29.847812770000075 1 |
| LONGITUDE | amount | 30 | 0 | -95.34211248999998 1; -95.40800377999994 1; -95.40847099999996 1; -95.40845776999998 1 |
| NAICS_CODE | category | 3 | 0 | 622110 18; 622310 9; 622210 3 |
| NAICS_DESC | category | 5 | 0 | GENERAL MEDICAL AND SURGI 18; EXTENDED CARE HOSPITALS ( 3; SPECIALTY (EXCEPT PSYCHIA 3; PSYCHIATRIC AND SUBSTANCE 3 |
| SOURCE | category | 4 | 0 | https://www.hhs.texas.gov 23; http://www.dshs.state.tx. 3; https://hhs.texas.gov/doi 3; http://www.dshs.texas.gov 1 |
| SOURCEDATE | date | 4 | 0 | 1709856000000 23; 1411430400000 3; 1599004800000 3; 1483920000000 1 |
| VAL_METHOD | category | 3 | 0 | IMAGERY/OTHER 15; IMAGERY 14; UNVERIFIED 1 |
| VAL_DATE | date | 18 | 0 | 1391990400000 6; 1588896000000 3; 1391385600000 2; 1483920000000 2 |
| WEBSITE | category | 18 | 0 | NOT AVAILABLE 13; http://www.stanthonyshous 1; www.khnorthhouston.com 1; http://www.ummc.care/ 1 |
| STATE_ID | category | 21 | 0 | NOT AVAILABLE 8; 100254 2; 100301 2; 8450 1 |
| ALT_NAME | category | 2 | 0 | NOT AVAILABLE 29; TEXAS SPECIALTY HOSPITAL  1 |
| ST_FIPS | other | 1 | 0 | 48 30 |
| OWNER | category | 4 | 0 | PROPRIETARY 21; NOT AVAILABLE 5; NON-PROFIT 3; GOVERNMENT - STATE 1 |
| TTL_STAFF | other | 1 | 0 | -999 30 |
| BEDS | category | 25 | 0 | 117 2; 4 2; 61 2; 20 2 |
| TRAUMA | category | 4 | 0 | NOT AVAILABLE 25; LEVEL III 3; LEVEL IV 1; LEVEL II 1 |
| HELIPAD | category | 2 | 0 | N 21; Y 9 |
| GENERATOR_ONSITE | empty | 1 | 30 |  |
| SELF_SUFFICIENT_ELECTRICITY | empty | 1 | 30 |  |
| IN_100_YR_FLOODPLAIN | empty | 1 | 30 |  |
| IN_500_YR_FLOODPLAIN | empty | 1 | 30 |  |
| IN_SURGE_SLOSH_AREA | empty | 1 | 30 |  |
| GEOMETRY | category | 30 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:15:22.09370 30 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7df641c1-a75b-44c9-b657-7 30 |
| SRC_SHA256 | who | 1 | 0 | 2276aece3bd41df83f67f15b6 30 |
