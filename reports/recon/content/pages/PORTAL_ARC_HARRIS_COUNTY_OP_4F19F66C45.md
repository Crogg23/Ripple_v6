# PORTAL_ARC_HARRIS_COUNTY_OP_4F19F66C45

rows 56  columns 92  scan 4.4s

roles: amount 10, audit 2, category 28, date 2, empty 20, other 28, who 3

## when

USER_EXPIRATION
  2019        13  ##############
  2020        27  ##############################
  2021        16  ##################

INGESTED_AT
  2026        56  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 56 | 96.24 | 100 | 100 | 100 | 5.6K |
| X | 56 | -106.58 | -96.87 | -94.74 | -94.73 | -5.5K |
| Y | 56 | 26.16 | 30.59 | 34.05 | 34.21 | 1.7K |
| DISPLAYX | 56 | -106.58 | -96.86 | -94.74 | -94.73 | -5.5K |
| DISPLAYY | 56 | 26.16 | 30.59 | 34.05 | 34.21 | 1.7K |
| XMIN | 56 | -106.58 | -96.87 | -94.75 | -94.74 | -5.5K |

## who

USER_NAME by rows
         1  OCEANS BEHAVIORAL HOSPITAL OF PASADENA
         1  DALLAS BEHAVIORAL HEALTHCARE HOSPITAL LLC
         1  WELLBRIDGE HOSPITAL OF SAN MARCOS
         1  AUSTIN OAKS HOSPITAL
         1  WELLBRIDGE HOSPITAL OF FORT WORTH
         1  EL PASO BEHAVIORAL HEALTH SYSTEM
         1  OCEANS BEHAVIORAL HOSPITAL OF LONGVIEW
         1  WOODLANDS INTEGRATIVE CARE HOSPITAL INC
         1  OCEANS BEHAVIORAL HOSPITAL OF THE PERMIAN BASIN
         1  PALMS BEHAVIORAL HEALTH
         1  CARROLLTON SPRINGS
         1  UNIVERSITY BEHAVIORAL HEALTH OF DENTON
         1  RIVER CREST HOSPITAL
         1  OCEANS BEHAVIORAL HOSPITAL OF KATY
         1  HICKORY TRAIL HOSPITAL
         1  ALLEGIANCE BEHAVIORAL HEALTH CENTER OF PLAINVIEW LLC
         1  AUSTIN LAKES HOSPITAL
         1  ASCENSION SETON SHOAL CREEK
         1  MILLWOOD HOSPITAL
         1  CLARITY CHILD GUIDANCE CENTER

USER_NAME by dollars
         100        1 rows  TEXAS HEALTH SPRINGWOOD BEHAVIORAL HEALTH HOSPITAL
         100        1 rows  MILLWOOD HOSPITAL
         100        1 rows  WESTPARK SPRINGS
         100        1 rows  HAVEN BEHAVIORAL HOSPITAL OF FRISCO
         100        1 rows  WOODLANDS INTEGRATIVE CARE HOSPITAL INC
         100        1 rows  OCEANS BEHAVIORAL HOSPITAL OF LONGVIEW
         100        1 rows  OCEANS BEHAVIORAL HOSPITAL OF LUFKIN
         100        1 rows  CROSS CREEK HOSPITAL
         100        1 rows  SAN ANTONIO BEHAVIORAL HEALTHCARE HOSPITAL, LLC
         100        1 rows  RIVER CREST HOSPITAL
         100        1 rows  WELLBRIDGE HOSPITAL OF FORT WORTH
         100        1 rows  TEXAS HEALTH SEAY BEHAVIORAL HEALTH HOSPITAL
         100        1 rows  LONE STAR BEHAVIORAL HEALTH CYPRESS
         100        1 rows  SACRED OAK MEDICAL CENTER
         100        1 rows  ASCENSION SETON SHOAL CREEK
         100        1 rows  WOODLAND SPRINGS
         100        1 rows  AUSTIN LAKES HOSPITAL
         100        1 rows  RIO VISTA BEHAVIORAL HEALTH
         100        1 rows  KINGWOOD PINES HOSPITAL
         100        1 rows  GARLAND BEHAVIORAL HOSPITAL

STNAME by rows
         2  Parker
         1  Dimmitt
         1  Cooper
         1  Corporate Woods
         1  Dittmar
         1  I-35
         1  Preston
         1  Fannin
         1  Clodus Fields
         1  Denver
         1  Ladbrook
         1  Northwestern
         1  FM 1788
         1  Windsor Lakes
         1  Mills
         1  Hilbig
         1  Gessner
         1  Austin
         1  Victoria
         1  Hunters Glen

STNAME by dollars
         200        2 rows  Parker
         100        1 rows  Ladbrook
         100        1 rows  Northwestern
         100        1 rows  Clodus Fields
         100        1 rows  Dimmitt
         100        1 rows  Cooper
         100        1 rows  Corporate Woods
         100        1 rows  Clinic
         100        1 rows  Huebner
         100        1 rows  Devereux
         100        1 rows  Victoria
         100        1 rows  Inner
         100        1 rows  Interstate 35
         100        1 rows  Normand
         100        1 rows  Space Center
         100        1 rows  Stassney
         100        1 rows  Mesa Springs
         100        1 rows  32nd
         100        1 rows  Cali
         100        1 rows  Hilbig

SRC_SHA256 by rows
        56  97ba7ef2eae451e82c6e042a1efcd69b55ec5a6de954996522923757af06a6a0

SRC_SHA256 by dollars
        5.6K       56 rows  97ba7ef2eae451e82c6e042a1efcd69b55ec5a6de954996522923757af06

## who x when

USER_NAME by USER_EXPIRATION, dollars = SCORE
  ALLEGIANCE BEHAVIORAL HEALTH CENTER OF P  2021:100
  ASCENSION SETON SHOAL CREEK               2021:100
  AUSTIN LAKES HOSPITAL                     2021:100
  AUSTIN OAKS HOSPITAL                      2021:100
  CARROLLTON SPRINGS                        2020:100
  CLARITY CHILD GUIDANCE CENTER             2020:98.34
  CROSS CREEK HOSPITAL                      2021:100
  DALLAS BEHAVIORAL HEALTHCARE HOSPITAL LL  2019:100
  EL PASO BEHAVIORAL HEALTH SYSTEM          2019:100
  HAVEN BEHAVIORAL HOSPITAL OF FRISCO       2020:100
  HICKORY TRAIL HOSPITAL                    2020:99.04
  LONE STAR BEHAVIORAL HEALTH CYPRESS       2019:100
  MILLWOOD HOSPITAL                         2020:100
  OCEANS BEHAVIORAL HOSPITAL OF KATY        2021:100
  OCEANS BEHAVIORAL HOSPITAL OF LONGVIEW    2019:100
  OCEANS BEHAVIORAL HOSPITAL OF LUFKIN      2020:100
  OCEANS BEHAVIORAL HOSPITAL OF PASADENA    2021:100
  OCEANS BEHAVIORAL HOSPITAL OF THE PERMIA  2021:100
  PALMS BEHAVIORAL HEALTH                   2020:100
  RIVER CREST HOSPITAL                      2020:100
  SACRED OAK MEDICAL CENTER                 2019:100
  SAN ANTONIO BEHAVIORAL HEALTHCARE HOSPIT  2020:100
  TEXAS HEALTH SEAY BEHAVIORAL HEALTH HOSP  2019:100
  TEXAS HEALTH SPRINGWOOD BEHAVIORAL HEALT  2021:100
  UNIVERSITY BEHAVIORAL HEALTH OF DENTON    2019:99.01
  WELLBRIDGE HOSPITAL OF FORT WORTH         2020:100
  WELLBRIDGE HOSPITAL OF SAN MARCOS         2021:100
  WESTPARK SPRINGS                          2020:100
  WOODLAND SPRINGS                          2020:100
  WOODLANDS INTEGRATIVE CARE HOSPITAL INC   2020:100

STNAME by USER_EXPIRATION, dollars = SCORE
  32nd                                      2021:100
  Austin                                    2020:97.32
  Clinic                                    2019:100
  Clodus Fields                             2019:100
  Cooper                                    2020:100
  Corporate Woods                           2020:100
  Denver                                    2019:100
  Devereux                                  2019:100
  Dimmitt                                   2021:100
  Dittmar                                   2020:97.25
  FM 1788                                   2021:100
  Fannin                                    2020:99
  Gessner                                   2020:100
  Hilbig                                    2021:100
  Huebner                                   2020:100
  Hunters Glen                              2020:100
  I-35                                      2021:99.90
  Inner                                     2020:100
  Interstate 35                             2021:100
  Ladbrook                                  2021:100
  Mesa Springs                              2020:100
  Mills                                     2021:100
  Normand                                   2020:100
  Northwestern                              2021:100
  Parker                                    2019:100 2020:100
  Preston                                   2021:100
  Space Center                              2019:100
  Stassney                                  2021:100
  Victoria                                  2020:100
  Windsor Lakes                             2020:100

## what

MATCH_TYPE: A 98%, PP 2%

ADDR_TYPE: PointAddress 80%, StreetAddress 18%, Subaddress 2%

ADDNUMFROM: 1006 10%, 12357 10%, 6100 10%, 2717 10%, 1374 10%, 457 10%, 5626 10%, 307 10%, 4704 10%, 1998 10%

ADDNUMTO: 1000 10%, 12301 10%, 6152 10%, 2735 10%, 1390 10%, 455 10%, 5702 10%, 301 10%, 4708 10%, 1900 10%

ADDRANGE: 1000-1006 10%, 12301-12357 10%, 6100-6152 10%, 2717-2735 10%, 1374-1390 10%, 455-457 10%, 5626-5702 10%, 301-307 10%, 4704-4708 10%, 1900-1998 10%

SIDE: L 65%, R 35%

STPREDIR: W 33%, S 33%, N 17%, SE 8%, E 8%

STTYPE: Dr 31%, Rd 23%, Blvd 12%, St 12%, Ave 10%, Ln 8%, Loop 2%, Pl 2%, Trl 2%

UNITTYPE: Ste 100%

UNITNAME: 150 100%

SUBADDR: Ste 150 100%

NBRHD: Central Southwest 25%, Spring Shadows 25%, Frisco Square 25%, Highland Park 25%

CITY: Houston 24%, Austin 15%, Conroe 9%, Plano 9%, San Antonio 9%, Fort Worth 6%, Georgetown 6%, El Paso 6%, Desoto 6%, Richmond 3%, San Marcos 3%, Lubbock 3%

METROAREA: Dallas-Fort Worth Metroplex 67%, Houston-Galveston Metro Area 33%

SUBREGION: Harris 29%, Travis 12%, Tarrant 10%, Collin 10%, Montgomery 7%, Bexar 7%, Dallas 7%, Williamson 5%, El Paso County 5%, Fort Bend 2%, Hays 2%, Lubbock County 2%

ZONE: The Woodlands 100%

POSTAL: 75093 16%, 77384 11%, 78745 11%, 77090 11%, 78626 11%, 75115 11%, 77407 5%, 77035 5%, 78666 5%, 77074 5%, 76132 5%, 79404 5%

EXINFO: 15 17%, 79423 17%, 1500 17%, ATTN JULIA SPENCE 17%, THIRD 17%, 300 17%

IN_CITY: HOUSTON 24%, AUSTIN 15%, CONROE 9%, PLANO 9%, SAN ANTONIO 9%, FORT WORTH 6%, GEORGETOWN 6%, EL PASO 6%, DESOTO 6%, RICHMOND 3%, SAN MARCOS 3%, LUBBOCK 3%

IN_SUBREGION: HARRIS 28%, TRAVIS 12%, TARRANT 9%, COLLIN 9%, DALLAS 9%, MONTGOMERY 7%, BEXAR 7%, DENTON 5%, WILLIAMSON 5%, EL PASO 5%, FORT BEND 2%, HAYS 2%

IN_POSTAL: 75093 16%, 77384 11%, 78745 11%, 77090 11%, 78626 11%, 75115 11%, 77407 5%, 77035 5%, 78666 5%, 77074 5%, 76132 5%, 79423 5%

USER_DESIGNATION_SERVICES_ACCRE: Chemical Dependency In Patient 40%, Chemical Dependency In Patient 19%, Emergency Treatment, For Profi 9%, Chemical Dependency In Patient 8%, Emergency Treatment, For Profi 6%, Chemical Dependency In Patient 6%, Emergency Treatment, Lab Servi 4%, Chemical Dependency In Patient 2%, Emergency Treatment, Joint Com 2%, Chemical Dependency In Patient 2%, Chemical Dependency In Patient 2%, Chemical Dependency In Patient 2%

USER_CITY: HOUSTON 24%, AUSTIN 15%, CONROE 9%, PLANO 9%, SAN ANTONIO 9%, FORT WORTH 6%, GEORGETOWN 6%, EL PASO 6%, DESOTO 6%, RICHMOND 3%, SAN MARCOS 3%, LUBBOCK 3%

USER_ZIP: 75093 16%, 77384 11%, 78745 11%, 77090 11%, 78626 11%, 75115 11%, 77407 5%, 77035 5%, 78666 5%, 77074 5%, 76132 5%, 79423 5%

USER_COUNTY: HARRIS 28%, TRAVIS 12%, TARRANT 9%, COLLIN 9%, DALLAS 9%, MONTGOMERY 7%, BEXAR 7%, DENTON 5%, WILLIAMSON 5%, EL PASO 5%, FORT BEND 2%, HAYS 2%

USER_MAILING_CITY: PLANO 22%, HOUSTON 19%, AUSTIN 14%, CONROE 8%, SAN ANTONIO 8%, FORT WORTH 5%, GEORGETOWN 5%, EL PASO 5%, DESOTO 5%, RICHMOND 3%, SAN MARCOS 3%, LUBBOCK 3%

USER_MAILING_ZIP: 75024 23%, 75093 14%, 77384 9%, 77090 9%, 78626 9%, 75115 9%, 78715 5%, 77407 5%, 77035 5%, 78666 5%, 77074 5%, 76132 5%

USER_BEDS: 72 16%, 24 16%, 48 13%, 80 10%, 96 6%, 70 6%, 20 6%, 90 6%, 124 6%, 116 6%, 18 3%, 60 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 56 | 0 | 56 1; 55 1; 54 1; 53 1 |
| STATUS | other | 1 | 0 | M 56 |
| SCORE | amount | 12 | 0 | 100.0 42; 99.0 3; 99.04 2; 97.25 1 |
| MATCH_TYPE | category | 2 | 0 | A 55; PP 1 |
| MATCH_ADDR | other | 56 | 0 | 15860 Old Conroe Rd, Conr 1; 1006 Windsor Lakes Blvd,  1; 1106 W Dittmar Rd, Austin 1; 6902 S Peek Rd, Richmond, 1 |
| LONGLABEL | other | 55 | 0 | 15860 Old Conroe Rd, Conr 1; 1006 Windsor Lakes Blvd,  1; 1106 W Dittmar Rd, Austin 1; 6902 S Peek Rd, Richmond, 1 |
| SHORTLABEL | other | 56 | 0 | 15860 Old Conroe Rd 1; 1006 Windsor Lakes Blvd 1; 1106 W Dittmar Rd 1; 6902 S Peek Rd 1 |
| ADDR_TYPE | category | 3 | 0 | PointAddress 45; StreetAddress 10; Subaddress 1 |
| TYPE | empty | 1 | 56 |  |
| PLACENAME | empty | 1 | 56 |  |
| PLACE_ADDR | other | 56 | 0 | 15860 Old Conroe Rd, Conr 1; 1006 Windsor Lakes Blvd,  1; 1106 W Dittmar Rd, Austin 1; 6902 S Peek Rd, Richmond, 1 |
| PHONE | empty | 1 | 56 |  |
| URL | empty | 1 | 56 |  |
| RANK | other | 1 | 0 | 20 56 |
| ADDBLDG | empty | 1 | 56 |  |
| ADDNUM | other | 54 | 0 | 1106 2; 700 2; 15860 1; 1006 1 |
| ADDNUMFROM | category | 11 | 46 | 1006 1; 12357 1; 6100 1; 2717 1 |
| ADDNUMTO | category | 11 | 46 | 1000 1; 12301 1; 6152 1; 2735 1 |
| ADDRANGE | category | 11 | 46 | 1000-1006 1; 12301-12357 1; 6100-6152 1; 2717-2735 1 |
| SIDE | category | 3 | 39 | L 11; R 6 |
| STPREDIR | category | 6 | 44 | W 4; S 4; N 2; SE 1 |
| STPRETYPE | empty | 1 | 56 |  |
| STNAME | who | 55 | 0 | Parker 2; Old Conroe 1; Windsor Lakes 1; Dittmar 1 |
| STTYPE | category | 10 | 4 | Dr 16; Rd 12; Blvd 6; St 6 |
| STDIR | empty | 1 | 56 |  |
| BLDGTYPE | empty | 1 | 56 |  |
| BLDGNAME | empty | 1 | 56 |  |
| LEVELTYPE | empty | 1 | 56 |  |
| LEVELNAME | empty | 1 | 56 |  |
| UNITTYPE | category | 2 | 55 | Ste 1 |
| UNITNAME | category | 2 | 55 | 150 1 |
| SUBADDR | category | 2 | 55 | Ste 150 1 |
| STADDR | other | 56 | 0 | 15860 Old Conroe Rd 1; 1006 Windsor Lakes Blvd 1; 1106 W Dittmar Rd 1; 6902 S Peek Rd 1 |
| BLOCK | empty | 1 | 56 |  |
| SECTOR | empty | 1 | 56 |  |
| NBRHD | category | 5 | 52 | Central Southwest 1; Spring Shadows 1; Frisco Square 1; Highland Park 1 |
| DISTRICT | empty | 1 | 56 |  |
| CITY | category | 35 | 0 | Houston 8; Austin 5; Conroe 3; Plano 3 |
| METROAREA | category | 3 | 47 | Dallas-Fort Worth Metropl 6; Houston-Galveston Metro A 3 |
| SUBREGION | category | 27 | 0 | Harris 12; Travis 5; Tarrant 4; Collin 4 |
| REGION | other | 1 | 0 | Texas 56 |
| REGIONABBR | other | 1 | 0 | TX 56 |
| TERRITORY | empty | 1 | 56 |  |
| ZONE | category | 2 | 55 | The Woodlands 1 |
| POSTAL | category | 49 | 0 | 75093 3; 77384 2; 78745 2; 77090 2 |
| POSTALEXT | other | 56 | 1 | 3485 1; 4973 1; 6328 1; 1741 1 |
| COUNTRY | other | 1 | 0 | USA 56 |
| LANGCODE | other | 1 | 0 | ENG 56 |
| DISTANCE | other | 1 | 0 | 0 56 |
| X | amount | 56 | 0 | -95.540409 1; -95.46102037 1; -97.80532148 1; -95.76026709 1 |
| Y | amount | 55 | 0 | 30.229299 1; 30.21169669 1; 30.18574039 1; 29.69433863 1 |
| DISPLAYX | amount | 55 | 0 | -95.540409 1; -95.46102037 1; -97.80534 1; -95.761143 1 |
| DISPLAYY | amount | 56 | 0 | 30.229299 1; 30.21169669 1; 30.186162 1; 29.69433 1 |
| XMIN | amount | 56 | 0 | -95.541409 1; -95.46202037 1; -97.80634 1; -95.762143 1 |
| XMAX | amount | 54 | 0 | -95.539409 1; -95.46002037 1; -97.80434 1; -95.760143 1 |
| YMIN | amount | 56 | 0 | 30.228299 1; 30.21069669 1; 30.185162 1; 29.69333 1 |
| YMAX | amount | 56 | 0 | 30.230299 1; 30.21269669 1; 30.187162 1; 29.69533 1 |
| EXINFO | category | 7 | 50 | 15 1; 79423 1; 1500 1; ATTN JULIA SPENCE 1 |
| RESULTID | other | 56 | 0 | 55 1; 56 1; 47 1; 54 1 |
| IN_ADDRESS | other | 56 | 0 | 15860 OLD CONROE ROAD 1; 1006 WINDSOR LAKE BLVD ST 1; 1106 WEST DITTMAR BUILDIN 1; 6902 S PEEK ROAD 1 |
| IN_ADDRESS2 | empty | 1 | 56 |  |
| IN_ADDRESS3 | empty | 1 | 56 |  |
| IN_NEIGHBORHOOD | empty | 1 | 56 |  |
| IN_CITY | category | 35 | 0 | HOUSTON 8; AUSTIN 5; CONROE 3; PLANO 3 |
| IN_SUBREGION | category | 25 | 0 | HARRIS 12; TRAVIS 5; TARRANT 4; COLLIN 4 |
| IN_REGION | other | 1 | 0 | TX 56 |
| IN_POSTAL | category | 49 | 0 | 75093 3; 77384 2; 78745 2; 77090 2 |
| IN_POSTALEXT | empty | 1 | 56 |  |
| IN_COUNTRYCODE | empty | 1 | 56 |  |
| USER_FIELD1 | other | 56 | 0 | 54 1; 55 1; 46 1; 53 1 |
| USER_NAME | who | 56 | 0 | WOODLAND SPRINGS 1; WOODLANDS INTEGRATIVE CAR 1; TEXAS NEUROREHAB CENTER 1; WESTPARK SPRINGS 1 |
| USER_LICENSE_NUMBER | other | 56 | 0 | 100432 1; 100445 1; 739 1; 100270 1 |
| USER_CCN | amount | 48 | 0 | nan 8; 454111.0 1; 454131.0 1; 454137.0 1 |
| USER_EXPIRATION | date | 22 | 0 | 1598832000000 5; 1569801600000 5; 1580428800000 5; 1614470400000 5 |
| USER_EFFECTIVE | other | 54 | 0 | 1506816000000 2; 1525305600000 1; 1533859200000 1; 325296000000 1 |
| USER_DESIGNATION_SERVICES_ACCRE | category | 15 | 0 | Chemical Dependency In Pa 21; Chemical Dependency In Pa 10; Emergency Treatment, For  5; Chemical Dependency In Pa 4 |
| USER_CEO_ADMINISTRATOR | other | 55 | 0 | MCCAMMON, COLLEEN 2; DAVIS, DUSTIN 1; SUTTON, ALEXANDRA 1; PRETTYMAN, ED 1 |
| USER_ADDRESS | other | 56 | 0 | 15860 OLD CONROE ROAD 1; 1006 WINDSOR LAKE BLVD ST 1; 1106 WEST DITTMAR BUILDIN 1; 6902 S PEEK ROAD 1 |
| USER_CITY | category | 35 | 0 | HOUSTON 8; AUSTIN 5; CONROE 3; PLANO 3 |
| USER_STATE | other | 1 | 0 | TX 56 |
| USER_ZIP | category | 49 | 0 | 75093 3; 77384 2; 78745 2; 77090 2 |
| USER_PHONE | other | 56 | 0 | 9362707520 1; 2812927246 1; 5124444835 1; 8325352770 1 |
| USER_COUNTY | category | 25 | 0 | HARRIS 12; TRAVIS 5; TARRANT 4; COLLIN 4 |
| USER_MAILING_ADDRESS | other | 52 | 0 | 5850 GRANITE PARKWAY SUIT 5; 15860 OLD CONROE ROAD 1; 1006 WINDSOR LAKE BLVD ST 1; PO BOX 150459 1 |
| USER_MAILING_CITY | category | 31 | 0 | PLANO 8; HOUSTON 7; AUSTIN 5; CONROE 3 |
| USER_MAILING_STATE | other | 1 | 0 | TX 56 |
| USER_MAILING_ZIP | category | 46 | 0 | 75024 5; 75093 3; 77384 2; 77090 2 |
| USER_BEDS | category | 36 | 0 | 72 5; 24 5; 48 4; 80 3 |
| GEOMETRY | other | 56 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:31:47.12352 56 |
| SOURCE_RUN_ID | audit | 1 | 0 | fae3fc15-24bd-4346-9eab-b 56 |
| SRC_SHA256 | who | 1 | 0 | 97ba7ef2eae451e82c6e042a1 56 |
