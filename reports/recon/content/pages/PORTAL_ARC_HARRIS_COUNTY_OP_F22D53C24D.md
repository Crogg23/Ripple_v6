# PORTAL_ARC_HARRIS_COUNTY_OP_F22D53C24D

rows 56  columns 92  scan 3.7s

roles: amount 10, audit 2, category 33, date 2, empty 15, other 28, who 3

## when

EXPIRATION
  2019        13  ##############
  2020        27  ##############################
  2021        16  ##################

INGESTED_AT
  2026        56  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 56 | 96.24 | 100 | 100 | 100 | 5.6K |
| X | 56 | -106.58 | -96.87 | 1.38M | 3.06M | 3.06M |
| Y | 56 | 26.16 | 30.61 | 6.24M | 13.86M | 13.87M |
| DISPLAYX | 56 | -106.58 | -96.86 | -94.74 | -94.73 | -5.5K |
| DISPLAYY | 56 | 26.16 | 30.59 | 34.05 | 34.21 | 1.7K |
| XMIN | 56 | -106.58 | -96.87 | -94.75 | -94.74 | -5.5K |

## who

NAME by rows
         1  DEVEREUX TEXAS TREATMENT NETWORK
         1  GARLAND BEHAVIORAL HOSPITAL
         1  THE MENNINGER CLINIC
         1  CYPRESS CREEK HOSPITAL
         1  LONE STAR BEHAVIORAL HEALTH CYPRESS
         1  SAN ANTONIO BEHAVIORAL HEALTHCARE HOSPITAL, LLC
         1  TEXAS NEUROREHAB CENTER
         1  MESA SPRINGS
         1  ASCENSION SETON SHOAL CREEK
         1  UNIVERSITY BEHAVIORAL HEALTH OF DENTON
         1  AUSTIN OAKS HOSPITAL
         1  OCEANS BEHAVIORAL HOSPITAL OF ABILENE
         1  HICKORY TRAIL HOSPITAL
         1  WESTPARK SPRINGS
         1  MONTGOMERY COUNTY MENTAL HEALTH TREATMENT FACILITY
         1  DALLAS BEHAVIORAL HEALTHCARE HOSPITAL LLC
         1  WELLBRIDGE HOSPITAL OF PLANO
         1  OCEANS BEHAVIORAL HOSPITAL OF THE PERMIAN BASIN
         1  OCEANS BEHAVIORAL HOSPITAL OF PASADENA
         1  ROCK PRAIRIE BEHAVIORAL HEALTH

NAME by dollars
         100        1 rows  TEXAS HEALTH SPRINGWOOD BEHAVIORAL HEALTH HOSPITAL
         100        1 rows  CROSS CREEK HOSPITAL
         100        1 rows  HAVEN BEHAVIORAL HOSPITAL OF FRISCO
         100        1 rows  AUSTIN OAKS HOSPITAL
         100        1 rows  WELLBRIDGE HOSPITAL OF SAN MARCOS
         100        1 rows  KINGWOOD PINES HOSPITAL
         100        1 rows  RIO VISTA BEHAVIORAL HEALTH
         100        1 rows  DALLAS BEHAVIORAL HEALTHCARE HOSPITAL LLC
         100        1 rows  ROCK SPRINGS
         100        1 rows  EL PASO BEHAVIORAL HEALTH SYSTEM
         100        1 rows  MESA SPRINGS
         100        1 rows  MONTGOMERY COUNTY MENTAL HEALTH TREATMENT FACILITY
         100        1 rows  LONE STAR BEHAVIORAL HEALTH CYPRESS
         100        1 rows  TEXAS HEALTH SEAY BEHAVIORAL HEALTH HOSPITAL
         100        1 rows  OCEANS BEHAVIORAL HOSPITAL OF THE PERMIAN BASIN
         100        1 rows  CYPRESS CREEK HOSPITAL
         100        1 rows  OCEANS BEHAVIORAL HOSPITAL OF PASADENA
         100        1 rows  ALLEGIANCE BEHAVIORAL HEALTH CENTER OF PLAINVIEW LLC
         100        1 rows  ASCENSION SETON SHOAL CREEK
         100        1 rows  MEDICAL CITY GREEN OAKS HOSPITAL

STNAME by rows
         2  Parker
         1  Division
         1  Gobblers Knob
         1  Tom Slick
         1  Space Center
         1  Inner
         1  Ladbrook
         1  Overton Ridge
         1  Kirnwood
         1  Mapleshade
         1  Clodus Fields
         1  8th
         1  Fannin
         1  Old Conroe
         1  Dimmitt
         1  Frisco Square
         1  Huebner
         1  Hilbig
         1  Cypress Station
         1  Aspen

STNAME by dollars
         200        2 rows  Parker
         100        1 rows  Victoria
         100        1 rows  Clodus Fields
         100        1 rows  Northwestern
         100        1 rows  Overton Ridge
         100        1 rows  Huebner
         100        1 rows  Gobblers Knob
         100        1 rows  Normand
         100        1 rows  Cross Park
         100        1 rows  Stassney
         100        1 rows  Mapleshade
         100        1 rows  Woods
         100        1 rows  Tibbets
         100        1 rows  Hilbig
         100        1 rows  Mills
         100        1 rows  Preston
         100        1 rows  Cali
         100        1 rows  32nd
         100        1 rows  Grant
         100        1 rows  Dimmitt

SRC_SHA256 by rows
        56  9306f4ddc50f69db2ab614a0db64bd89198f9a62849860a0e59a852b720acfc2

SRC_SHA256 by dollars
        5.6K       56 rows  9306f4ddc50f69db2ab614a0db64bd89198f9a62849860a0e59a852b720a

## who x when

NAME by EXPIRATION, dollars = SCORE
  ALLEGIANCE BEHAVIORAL HEALTH CENTER OF P  2021:100
  ASCENSION SETON SHOAL CREEK               2021:100
  AUSTIN OAKS HOSPITAL                      2021:100
  CROSS CREEK HOSPITAL                      2021:100
  CYPRESS CREEK HOSPITAL                    2021:100
  DALLAS BEHAVIORAL HEALTHCARE HOSPITAL LL  2019:100
  DEVEREUX TEXAS TREATMENT NETWORK          2019:100
  EL PASO BEHAVIORAL HEALTH SYSTEM          2019:100
  GARLAND BEHAVIORAL HOSPITAL               2019:100
  HAVEN BEHAVIORAL HOSPITAL OF FRISCO       2020:100
  HICKORY TRAIL HOSPITAL                    2020:99.04
  KINGWOOD PINES HOSPITAL                   2021:100
  LONE STAR BEHAVIORAL HEALTH CYPRESS       2019:100
  MESA SPRINGS                              2020:100
  MONTGOMERY COUNTY MENTAL HEALTH TREATMEN  2021:100
  OCEANS BEHAVIORAL HOSPITAL OF ABILENE     2019:100
  OCEANS BEHAVIORAL HOSPITAL OF PASADENA    2021:100
  OCEANS BEHAVIORAL HOSPITAL OF THE PERMIA  2021:100
  RIO VISTA BEHAVIORAL HEALTH               2021:100
  ROCK PRAIRIE BEHAVIORAL HEALTH            2020:100
  ROCK SPRINGS                              2020:100
  SAN ANTONIO BEHAVIORAL HEALTHCARE HOSPIT  2020:100
  TEXAS HEALTH SEAY BEHAVIORAL HEALTH HOSP  2019:100
  TEXAS HEALTH SPRINGWOOD BEHAVIORAL HEALT  2021:100
  TEXAS NEUROREHAB CENTER                   2020:97.25
  THE MENNINGER CLINIC                      2020:99
  UNIVERSITY BEHAVIORAL HEALTH OF DENTON    2019:99.01
  WELLBRIDGE HOSPITAL OF PLANO              2020:100
  WELLBRIDGE HOSPITAL OF SAN MARCOS         2021:100
  WESTPARK SPRINGS                          2020:100

STNAME by EXPIRATION, dollars = SCORE
  8th                                       2020:99.07
  Aspen                                     2021:98.61
  Cali                                      2021:100
  Clodus Fields                             2019:100
  Cross Park                                2021:100
  Cypress Station                           2019:99
  Dimmitt                                   2021:100
  Division                                  2019:99.04
  Fannin                                    2020:99
  Frisco Square                             2020:100
  Gobblers Knob                             2020:100
  Hilbig                                    2021:100
  Huebner                                   2020:100
  Inner                                     2020:100
  Kirnwood                                  2019:100
  Ladbrook                                  2021:100
  Mapleshade                                2020:100
  Mills                                     2021:100
  Normand                                   2020:100
  Northwestern                              2021:100
  Old Conroe                                2020:100
  Overton Ridge                             2020:100
  Parker                                    2019:100 2020:100
  Preston                                   2021:100
  Space Center                              2019:100
  Stassney                                  2021:100
  Tibbets                                   2021:100
  Tom Slick                                 2020:98.34
  Victoria                                  2020:100
  Woods                                     2019:100

## what

MATCH_TYPE: A 98%, M 2%

ADDR_TYPE: PointAddress 80%, StreetAddress 18%, Subaddress 2%

ADDNUMFROM: 1006 10%, 12357 10%, 2717 10%, 6100 10%, 1374 10%, 457 10%, 5626 10%, 307 10%, 1998 10%, 4704 10%

ADDNUMTO: 1002 10%, 12301 10%, 2735 10%, 6152 10%, 1390 10%, 455 10%, 5702 10%, 301 10%, 1900 10%, 4708 10%

ADDRANGE: 1002-1006 10%, 12301-12357 10%, 2717-2735 10%, 6100-6152 10%, 1374-1390 10%, 455-457 10%, 5626-5702 10%, 301-307 10%, 1900-1998 10%, 4704-4708 10%

SIDE: L 67%, R 33%

STPREDIR: S 33%, W 33%, N 17%, SE 8%, E 8%

STTYPE: Dr 31%, Rd 23%, Blvd 12%, St 12%, Ave 10%, Ln 8%, Loop 2%, Pl 2%, Trl 2%

UNITTYPE: Ste 100%

UNITNAME: 150 100%

SUBADDR: Ste 150 100%

NBRHD: Central Southwest 25%, Spring Shadows 25%, Frisco Square 25%, Highland Park 25%

CITY: Houston 24%, Austin 15%, Conroe 9%, Plano 9%, San Antonio 9%, Fort Worth 6%, Georgetown 6%, El Paso 6%, Desoto 6%, Richmond 3%, San Marcos 3%, Denton 3%

METROAREA: Dallas-Fort Worth Metroplex 67%, Houston-Galveston Metro Area 33%

SUBREGION: Harris 29%, Travis 12%, Collin 10%, Tarrant 10%, Montgomery 7%, Bexar 7%, Dallas 7%, Williamson 5%, El Paso County 5%, Fort Bend 2%, Hays 2%, Denton County 2%

ZONE: The Woodlands 100%

POSTAL: 75093 16%, 77384 11%, 78745 11%, 78626 11%, 77090 11%, 75115 11%, 77407 5%, 77074 5%, 78666 5%, 76132 5%, 76201 5%, 77035 5%

EXINFO: 15 17%, 79423 17%, 1500 17%, ATTN JULIA SPENCE 17%, THIRD 17%, 300 17%

ARC_ADDRESS2: nan 100%

ARC_ADDRESS3: nan 100%

ARC_NEIGHBORHOOD: nan 100%

ARC_CITY: HOUSTON 24%, AUSTIN 15%, CONROE 9%, PLANO 9%, SAN ANTONIO 9%, FORT WORTH 6%, GEORGETOWN 6%, EL PASO 6%, DESOTO 6%, RICHMOND 3%, SAN MARCOS 3%, DENTON 3%

ARC_SUBREGION: HARRIS 28%, TRAVIS 12%, COLLIN 9%, TARRANT 9%, DALLAS 9%, MONTGOMERY 7%, BEXAR 7%, DENTON 5%, WILLIAMSON 5%, EL PASO 5%, FORT BEND 2%, HAYS 2%

ARC_POSTAL: 75093 16%, 77384 11%, 78745 11%, 78626 11%, 77090 11%, 75115 11%, 77407 5%, 77074 5%, 78666 5%, 76132 5%, 76201 5%, 77035 5%

ARC_POSTALEXT: nan 100%

ARC_COUNTRYCODE: nan 100%

DESIGNATION_SERVICES_ACCREDITAT: Chemical Dependency In Patient 40%, Chemical Dependency In Patient 19%, Emergency Treatment, For Profi 9%, Chemical Dependency In Patient 8%, Emergency Treatment, For Profi 6%, Chemical Dependency In Patient 6%, Emergency Treatment, Lab Servi 4%, Chemical Dependency In Patient 2%, Emergency Treatment, Joint Com 2%, Chemical Dependency In Patient 2%, Chemical Dependency In Patient 2%, Chemical Dependency In Patient 2%

CITY_1: HOUSTON 24%, AUSTIN 15%, CONROE 9%, PLANO 9%, SAN ANTONIO 9%, FORT WORTH 6%, GEORGETOWN 6%, EL PASO 6%, DESOTO 6%, RICHMOND 3%, SAN MARCOS 3%, DENTON 3%

ZIP: 75093 16%, 77384 11%, 78745 11%, 78626 11%, 77090 11%, 75115 11%, 77407 5%, 77074 5%, 78666 5%, 76132 5%, 76201 5%, 77035 5%

COUNTY: HARRIS 28%, TRAVIS 12%, COLLIN 9%, TARRANT 9%, DALLAS 9%, MONTGOMERY 7%, BEXAR 7%, DENTON 5%, WILLIAMSON 5%, EL PASO 5%, FORT BEND 2%, HAYS 2%

MAILING_CITY: PLANO 22%, HOUSTON 19%, AUSTIN 14%, CONROE 8%, SAN ANTONIO 8%, FORT WORTH 5%, GEORGETOWN 5%, EL PASO 5%, DESOTO 5%, RICHMOND 3%, SAN MARCOS 3%, DENTON 3%

MAILING_ZIP: 75024 23%, 75093 14%, 77384 9%, 78626 9%, 77090 9%, 75115 9%, 77407 5%, 77074 5%, 78666 5%, 76132 5%, 76201 5%, 77035 5%

BEDS: 72 16%, 24 16%, 48 13%, 80 10%, 96 6%, 70 6%, 20 6%, 124 6%, 116 6%, 90 6%, 18 3%, 160 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 56 | 0 | 56 1; 55 1; 54 1; 53 1 |
| LOC_NAME | other | 1 | 0 | World 56 |
| STATUS | other | 1 | 0 | M 56 |
| SCORE | amount | 12 | 0 | 100.0 42; 99.0 3; 99.04 2; 99.01 1 |
| MATCH_TYPE | category | 2 | 0 | A 55; M 1 |
| MATCH_ADDR | other | 56 | 0 | 1006 Windsor Lakes Blvd,  1; 15860 Old Conroe Rd, Conr 1; 6902 S Peek Rd, Richmond, 1; 6500 Hornwood Dr, Houston 1 |
| LONGLABEL | other | 55 | 0 | 1006 Windsor Lakes Blvd,  1; 15860 Old Conroe Rd, Conr 1; 6902 S Peek Rd, Richmond, 1; 6500 Hornwood Dr, Houston 1 |
| SHORTLABEL | other | 56 | 0 | 1006 Windsor Lakes Blvd 1; 15860 Old Conroe Rd 1; 6902 S Peek Rd 1; 6500 Hornwood Dr 1 |
| ADDR_TYPE | category | 3 | 0 | PointAddress 45; StreetAddress 10; Subaddress 1 |
| TYPE | empty | 1 | 56 |  |
| PLACENAME | empty | 1 | 56 |  |
| PLACE_ADDR | other | 56 | 0 | 1006 Windsor Lakes Blvd,  1; 15860 Old Conroe Rd, Conr 1; 6902 S Peek Rd, Richmond, 1; 6500 Hornwood Dr, Houston 1 |
| PHONE | empty | 1 | 56 |  |
| URL | empty | 1 | 56 |  |
| RANK | other | 1 | 0 | 20 56 |
| ADDBLDG | empty | 1 | 56 |  |
| ADDNUM | other | 54 | 0 | 1106 2; 700 2; 1006 1; 15860 1 |
| ADDNUMFROM | category | 11 | 46 | 1006 1; 12357 1; 2717 1; 6100 1 |
| ADDNUMTO | category | 11 | 46 | 1002 1; 12301 1; 2735 1; 6152 1 |
| ADDRANGE | category | 11 | 46 | 1002-1006 1; 12301-12357 1; 2717-2735 1; 6100-6152 1 |
| SIDE | category | 3 | 38 | L 12; R 6 |
| STPREDIR | category | 6 | 44 | S 4; W 4; N 2; SE 1 |
| STPRETYPE | empty | 1 | 56 |  |
| STNAME | who | 55 | 0 | Parker 2; Windsor Lakes 1; Old Conroe 1; Peek 1 |
| STTYPE | category | 10 | 4 | Dr 16; Rd 12; Blvd 6; St 6 |
| STDIR | empty | 1 | 56 |  |
| BLDGTYPE | empty | 1 | 56 |  |
| BLDGNAME | empty | 1 | 56 |  |
| LEVELTYPE | empty | 1 | 56 |  |
| LEVELNAME | empty | 1 | 56 |  |
| UNITTYPE | category | 2 | 55 | Ste 1 |
| UNITNAME | category | 2 | 55 | 150 1 |
| SUBADDR | category | 2 | 55 | Ste 150 1 |
| STADDR | other | 56 | 0 | 1006 Windsor Lakes Blvd 1; 15860 Old Conroe Rd 1; 6902 S Peek Rd 1; 6500 Hornwood Dr 1 |
| BLOCK | empty | 1 | 56 |  |
| SECTOR | empty | 1 | 56 |  |
| NBRHD | category | 5 | 52 | Central Southwest 1; Spring Shadows 1; Frisco Square 1; Highland Park 1 |
| DISTRICT | empty | 1 | 56 |  |
| CITY | category | 35 | 0 | Houston 8; Austin 5; Conroe 3; Plano 3 |
| METROAREA | category | 3 | 47 | Dallas-Fort Worth Metropl 6; Houston-Galveston Metro A 3 |
| SUBREGION | category | 27 | 0 | Harris 12; Travis 5; Collin 4; Tarrant 4 |
| REGION | other | 1 | 0 | Texas 56 |
| REGIONABBR | other | 1 | 0 | TX 56 |
| TERRITORY | empty | 1 | 56 |  |
| ZONE | category | 2 | 55 | The Woodlands 1 |
| POSTAL | category | 49 | 0 | 75093 3; 77384 2; 78745 2; 78626 2 |
| POSTALEXT | other | 55 | 2 | 4885 1; 3485 1; 1741 1; 5095 1 |
| COUNTRY | other | 1 | 0 | USA 56 |
| LANGCODE | other | 1 | 0 | ENG 56 |
| DISTANCE | other | 1 | 0 | 0 56 |
| X | amount | 56 | 0 | -95.46102089 1; -95.540409 1; -95.76026709 1; -95.49862882 1 |
| Y | amount | 55 | 0 | 30.21169615 1; 30.229299 1; 29.69433863 1; 29.70886179 1 |
| DISPLAYX | amount | 55 | 0 | -95.46102089 1; -95.540409 1; -95.761143 1; -95.4986175 1 |
| DISPLAYY | amount | 56 | 0 | 30.21169615 1; 30.229299 1; 29.69433 1; 29.709675 1 |
| XMIN | amount | 56 | 0 | -95.46202089 1; -95.541409 1; -95.762143 1; -95.4996175 1 |
| XMAX | amount | 54 | 0 | -95.46002089 1; -95.539409 1; -95.760143 1; -95.4976175 1 |
| YMIN | amount | 56 | 0 | 30.21069615 1; 30.228299 1; 29.69333 1; 29.708675 1 |
| YMAX | amount | 56 | 0 | 30.21269615 1; 30.230299 1; 29.69533 1; 29.710675 1 |
| EXINFO | category | 7 | 50 | 15 1; 79423 1; 1500 1; ATTN JULIA SPENCE 1 |
| ARC_ADDRESS | other | 56 | 0 | 1006 WINDSOR LAKE BLVD ST 1; 15860 OLD CONROE ROAD 1; 6902 S PEEK ROAD 1; 6500 HORNWOOD DRIVE 1 |
| ARC_ADDRESS2 | category | 2 | 1 | nan 55 |
| ARC_ADDRESS3 | category | 2 | 1 | nan 55 |
| ARC_NEIGHBORHOOD | category | 2 | 1 | nan 55 |
| ARC_CITY | category | 35 | 0 | HOUSTON 8; AUSTIN 5; CONROE 3; PLANO 3 |
| ARC_SUBREGION | category | 25 | 0 | HARRIS 12; TRAVIS 5; COLLIN 4; TARRANT 4 |
| ARC_REGION | other | 1 | 0 | TX 56 |
| ARC_POSTAL | category | 49 | 0 | 75093 3; 77384 2; 78745 2; 78626 2 |
| ARC_POSTALEXT | category | 2 | 1 | nan 55 |
| ARC_COUNTRYCODE | category | 2 | 1 | nan 55 |
| FIELD1 | other | 56 | 0 | 55 1; 54 1; 53 1; 52 1 |
| NAME | who | 56 | 0 | WOODLANDS INTEGRATIVE CAR 1; WOODLAND SPRINGS 1; WESTPARK SPRINGS 1; WEST OAKS HOSPITAL 1 |
| LICENSE_NUMBER | other | 56 | 0 | 100445 1; 100432 1; 100270 1; 755 1 |
| CCN | amount | 48 | 0 | nan 8; 454131.0 1; 454026.0 1; 454137.0 1 |
| EXPIRATION | date | 22 | 0 | 1598832000000 5; 1569801600000 5; 1580428800000 5; 1614470400000 5 |
| EFFECTIVE | other | 54 | 0 | 1506816000000 2; 1533859200000 1; 1525305600000 1; 1411689600000 1 |
| DESIGNATION_SERVICES_ACCREDITAT | category | 15 | 0 | Chemical Dependency In Pa 21; Chemical Dependency In Pa 10; Emergency Treatment, For  5; Chemical Dependency In Pa 4 |
| CEO_ADMINISTRATOR | other | 55 | 0 | MCCAMMON, COLLEEN 2; SUTTON, ALEXANDRA 1; DAVIS, DUSTIN 1; WESTERMAN, MANDY 1 |
| ADDRESS | other | 56 | 0 | 1006 WINDSOR LAKE BLVD ST 1; 15860 OLD CONROE ROAD 1; 6902 S PEEK ROAD 1; 6500 HORNWOOD DRIVE 1 |
| CITY_1 | category | 35 | 0 | HOUSTON 8; AUSTIN 5; CONROE 3; PLANO 3 |
| STATE | other | 1 | 0 | TX 56 |
| ZIP | category | 49 | 0 | 75093 3; 77384 2; 78745 2; 78626 2 |
| PHONE_1 | other | 56 | 0 | 2812927246 1; 9362707520 1; 8325352770 1; 7139950909 1 |
| COUNTY | category | 25 | 0 | HARRIS 12; TRAVIS 5; COLLIN 4; TARRANT 4 |
| MAILING_ADDRESS | other | 52 | 0 | 5850 GRANITE PARKWAY SUIT 5; 1006 WINDSOR LAKE BLVD ST 1; 15860 OLD CONROE ROAD 1; 6902 S PEEK ROAD 1 |
| MAILING_CITY | category | 31 | 0 | PLANO 8; HOUSTON 7; AUSTIN 5; CONROE 3 |
| MAILING_STATE | other | 1 | 0 | TX 56 |
| MAILING_ZIP | category | 46 | 0 | 75024 5; 75093 3; 77384 2; 78626 2 |
| BEDS | category | 36 | 0 | 72 5; 24 5; 48 4; 80 3 |
| GEOMETRY | other | 56 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:31:52.21915 56 |
| SOURCE_RUN_ID | audit | 1 | 0 | 334a50c8-48bf-4af6-b513-e 56 |
| SRC_SHA256 | who | 1 | 0 | 9306f4ddc50f69db2ab614a0d 56 |
