# PORTAL_ARC_HARRIS_COUNTY_OP_2718B3279A

rows 77  columns 106  scan 4.6s

roles: amount 24, audit 2, category 30, date 3, empty 16, other 26, who 6

## when

USER_EXPIRATION
  2019        29  #######################
  2020        38  ##############################
  2021        10  ########

USER_EFFECTIVE
  1971         1  ####
  1972         1  ####
  1974         1  ####
  1976         2  ########
  1981         1  ####
  1991         2  ########
  1993         1  ####
  1995         1  ####
  1999         2  ########
  2000         1  ####
  2002         1  ####
  2005         3  ###########
  2006         2  ########
  2007         4  ###############
  2008         1  ####
  2009         2  ########
  2010         4  ###############
  2011         3  ###########
  2012         3  ###########
  2013         2  ########
  2014         4  ###############
  2015         6  ######################
  2016         6  ######################
  2017         8  ##############################
  2018         4  ###############
  2019         1  ####

INGESTED_AT
  2026        77  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 77 | 81.35 | 100 | 100 | 100 | 7.7K |
| X | 77 | -95.79 | -95.40 | -94.97 | -94.95 | -7.3K |
| Y | 77 | 29.53 | 29.77 | 30.09 | 30.09 | 2.3K |
| DISPLAYX | 77 | -95.79 | -95.40 | -94.97 | -94.95 | -7.3K |
| DISPLAYY | 77 | 29.53 | 29.77 | 30.09 | 30.09 | 2.3K |
| XMIN | 77 | -95.79 | -95.41 | -94.97 | -94.95 | -7.3K |

## who

USER_NAME by rows
         1  PROVIDENCE HOSPITAL OF NORTH HOUSTON LLC
         1  HERMANN DRIVE SURGICAL HOSPITAL LP
         1  ST JOSEPH MEDICAL CENTER IN THE HEIGHTS
         1  AD HOSPITAL EAST LLC
         1  SPRING EXCELLENCE SURGICAL HOSPITAL LLC
         1  ALTUS HOUSTON HOSPITAL, CELESTIAL HOSPITAL, ODYSSEY HOSPITAL
         1  HARRIS HEALTH SYSTEM BEN TAUB HOSPITAL
         1  HCA HOUSTON HEALTHCARE SOUTHEAST
         1  HCA HOUSTON HEALTHCARE CLEAR LAKE
         1  HEALTHBRIDGE CHILDRENS HOSPITAL-HOUSTON LTD
         1  TRINITY HOSPITAL
         1  PAM REHABILITATION HOSPITAL OF CLEAR LAKE
         1  HCA HOUSTON HEALTHCARE NORTHWEST
         1  UGH PAIN & SPINE
         1  HOUSTON METHODIST BAYTOWN HOSPITAL - ALEXANDER CAMPUS
         1  CORNERSTONE SPECIALTY HOSPITALS BELLAIRE
         1  ST LUKES PATIENTS MEDICAL CENTER
         1  TOPS SURGICAL SPECIALTY HOSPITAL
         1  MEMORIAL HERMANN TOMBALL HOSPITAL
         1  MEMORIAL HERMANN SOUTHEAST HOSPITAL

USER_NAME by dollars
         100        1 rows  TEXAS CHILDRENS HOSPITAL WEST CAMPUS
         100        1 rows  HCA HOUSTON HEALTHCARE WEST
         100        1 rows  HCA HOUSTON HEALTHCARE SPECIALTY HOSPITAL MEDICAL CENTER
         100        1 rows  MEMORIAL HERMANN NORTHEAST
         100        1 rows  HCA HOUSTON HEALTHCARE NORTH CYPRESS
         100        1 rows  UNITED MEMORIAL MEDICAL CENTER
         100        1 rows  HEALTHBRIDGE CHILDRENS HOSPITAL-HOUSTON LTD
         100        1 rows  CORNERSTONE SPECIALTY HOSPITALS MEDICAL CENTER
         100        1 rows  HOUSTON METHODIST WILLOWBROOK HOSPITAL
         100        1 rows  HOUSTON METHODIST BAYTOWN HOSPITAL - ALEXANDER CAMPUS
         100        1 rows  ALTUS BAYTOWN HOSPITAL, BAYTOWN MEDICAL CENTER
         100        1 rows  SHRINERS HOSPITALS FOR CHILDREN
         100        1 rows  PAM REHABILITATION HOSPITAL OF CLEAR LAKE
         100        1 rows  THE HEIGHTS HOSPITAL
         100        1 rows  TEXAS CHILDRENS HOSPITAL
         100        1 rows  MEMORIAL HERMANN TOMBALL HOSPITAL
         100        1 rows  MEMORIAL HERMANN GREATER HEIGHTS HOSPITAL
         100        1 rows  ST JOSEPH MEDICAL CENTER IN THE HEIGHTS
         100        1 rows  ST LUKES HOSPITAL AT THE VINTAGE
         100        1 rows  CORNERSTONE SPECIALTY HOSPITALS BELLAIRE

STNAME by rows
         4  Katy
         4  Medical Center
         4  Fannin
         3  Main
         3  Red Oak
         3  Sam Houston
         3  Hermann
         2  Ashland
         2  Chasewood Park
         2  McKay
         2  Northwest
         1  Bertner
         1  Mossy Oaks
         1  Louetta
         1  State Highway 249
         1  Woodland Park
         1  Memorial North
         1  Cypress Creek
         1  Taub
         1  FM 1960 Bypass

STNAME by dollars
      398.28        4 rows  Medical Center
         398        4 rows  Fannin
      393.94        4 rows  Katy
         300        3 rows  Sam Houston
         300        3 rows  Red Oak
         300        3 rows  Hermann
      298.05        3 rows  Main
         200        2 rows  Ashland
         200        2 rows  McKay
         200        2 rows  Chasewood Park
         200        2 rows  Northwest
         100        1 rows  St Joseph
         100        1 rows  Binz
         100        1 rows  Mckay
         100        1 rows  Cambridge
         100        1 rows  East
         100        1 rows  Mossy Oaks
         100        1 rows  Wortham Center
         100        1 rows  Baker
         100        1 rows  Taub

SUBREGION by rows
        77  Harris

SUBREGION by dollars
        7.7K       77 rows  Harris

IN_SUBREGION by rows
        77  HARRIS

IN_SUBREGION by dollars
        7.7K       77 rows  HARRIS

## who x when

USER_NAME by USER_EFFECTIVE, dollars = SCORE
  AD HOSPITAL EAST LLC                      2016:100
  ALTUS BAYTOWN HOSPITAL, BAYTOWN MEDICAL   2014:100
  ALTUS HOUSTON HOSPITAL, CELESTIAL HOSPIT  2017:100
  CORNERSTONE SPECIALTY HOSPITALS BELLAIRE  2015:100
  CORNERSTONE SPECIALTY HOSPITALS MEDICAL   2015:100
  HCA HOUSTON HEALTHCARE CLEAR LAKE         1972:99.62
  HCA HOUSTON HEALTHCARE NORTH CYPRESS      2018:100
  HCA HOUSTON HEALTHCARE NORTHWEST          2008:100
  HCA HOUSTON HEALTHCARE SPECIALTY HOSPITA  2017:100
  HCA HOUSTON HEALTHCARE WEST               1974:100
  HEALTHBRIDGE CHILDRENS HOSPITAL-HOUSTON   1999:100
  HERMANN DRIVE SURGICAL HOSPITAL LP        2011:100
  HOUSTON METHODIST BAYTOWN HOSPITAL - ALE  2002:100
  HOUSTON METHODIST WILLOWBROOK HOSPITAL    2000:100
  MEMORIAL HERMANN NORTHEAST                2007:100
  MEMORIAL HERMANN TOMBALL HOSPITAL         2017:100
  PAM REHABILITATION HOSPITAL OF CLEAR LAK  2015:100
  PROVIDENCE HOSPITAL OF NORTH HOUSTON LLC  2016:100
  SPRING EXCELLENCE SURGICAL HOSPITAL LLC   2016:100
  ST JOSEPH MEDICAL CENTER IN THE HEIGHTS   2012:100
  ST LUKES PATIENTS MEDICAL CENTER          2010:100
  TEXAS CHILDRENS HOSPITAL WEST CAMPUS      2011:100
  TOPS SURGICAL SPECIALTY HOSPITAL          1991:100
  TRINITY HOSPITAL                          2017:93.94
  UGH PAIN & SPINE                          2018:100
  UNITED MEMORIAL MEDICAL CENTER            2006:100

STNAME by USER_EFFECTIVE, dollars = SCORE
  Ashland                                   2012:100 2018:100
  Baker                                     2014:100
  Binz                                      2017:100
  Cambridge                                 2019:100
  Chasewood Park                            2012:100 2013:100
  Cypress Creek                             2008:100
  East                                      2016:100
  FM 1960 Bypass                            2017:99.01
  Fannin                                    1976:100
  Hermann                                   2011:100 2015:100 2017:100
  Katy                                      1981:100 2010:100 2011:100 2017:93.94
  Louetta                                   2016:100
  Main                                      1991:100 1995:98.05
  McKay                                     2009:100 2012:100
  Mckay                                     2014:100
  Medical Center                            1972:99.62 2005:99.04 2015:199.62
  Memorial North                            2007:100
  Mossy Oaks                                2016:100
  Northwest                                 2017:100 2018:100
  Red Oak                                   1991:100 2016:100 2018:100
  Sam Houston                               2010:200 2017:100
  St Joseph                                 2006:100
  State Highway 249                         2000:100
  Woodland Park                             1999:100
  Wortham Center                            2011:100

## what

MATCH_TYPE: A 94%, PP 5%, M 1%

ADDR_TYPE: PointAddress 78%, StreetAddress 18%, Subaddress 3%, POI 1%

TYPE: Hospital 100%

PLACENAME: Houston Methodist Clear Lake H 100%

PHONE: (281) 523-2000 100%

URL: http://www.houstonmethodist.or 100%

RANK: 20 99%, 18 1%

ADDNUMFROM: 4640 9%, 1499 9%, 19201 9%, 16700 9%, 6160 9%, 24423 9%, 5428 9%, 18915 9%, 1689 9%, 27398 9%, 18901 9%

ADDNUMTO: 4600 9%, 1401 9%, 19469 9%, 16908 9%, 6182 9%, 24515 9%, 5300 9%, 18951 9%, 1629 9%, 27898 9%, 18803 9%

ADDRANGE: 4600-4640 9%, 1401-1499 9%, 19201-19469 9%, 16700-16908 9%, 6160-6182 9%, 24423-24515 9%, 5300-5428 9%, 18915-18951 9%, 1629-1689 9%, 27398-27898 9%, 18803-18901 9%

SIDE: L 50%, R 50%

STPREDIR: W 50%, E 33%, N 8%, S 8%

STTYPE: St 24%, Dr 21%, Rd 13%, Blvd 12%, Fwy 9%, Pkwy 8%, Loop 5%, Ave 4%, Ln 1%, Hwy 1%

STDIR: S 57%, E 29%, W 14%

UNITTYPE: Ste 100%

UNITNAME: 102 50%, 100 50%

SUBADDR: Ste 102 50%, Ste 100 50%

NBRHD: Downtown 20%, Golfcrest/Bellfort/Reveille 20%, Greater Heights 20%, Fairfield 20%, Binz 20%

CITY: Houston 61%, Webster 8%, Humble 6%, Pasadena 5%, Tomball 4%, Katy 4%, Baytown 4%, Spring 3%, Bellaire 3%, Cypress 3%

METROAREA: Houston-Galveston Metro Area 100%

POSTAL: 77030 20%, 77598 12%, 77338 10%, 77090 10%, 77004 10%, 77008 8%, 77070 8%, 77375 6%, 77094 4%, 77504 4%, 77505 4%, 77450 4%

EXINFO: OLD 25%, B 25%, 4 & 5 25%, 18300 | DRIVE 25%

IN_CITY: HOUSTON 60%, WEBSTER 8%, HUMBLE 6%, PASADENA 5%, TOMBALL 4%, KATY 4%, BAYTOWN 4%, SPRING 3%, BELLAIRE 3%, CYPRESS 3%, NASSAU BAY 1%

IN_POSTAL: 77030 20%, 77598 12%, 77338 10%, 77090 10%, 77004 10%, 77008 8%, 77070 8%, 77375 6%, 77094 4%, 77504 4%, 77505 4%, 77450 4%

USER_CITY: HOUSTON 60%, WEBSTER 8%, HUMBLE 6%, PASADENA 5%, TOMBALL 4%, KATY 4%, BAYTOWN 4%, SPRING 3%, BELLAIRE 3%, CYPRESS 3%, NASSAU BAY 1%

USER_ZIP: 77030 20%, 77598 12%, 77338 10%, 77090 10%, 77004 10%, 77008 8%, 77070 8%, 77375 6%, 77094 4%, 77504 4%, 77505 4%, 77450 4%

USER_MAILING_CITY: HOUSTON 57%, HUMBLE 7%, TOMBALL 7%, PASADENA 5%, WEBSTER 5%, KATY 4%, BAYTOWN 4%, SPRING 3%, BELLAIRE 3%, DALLAS 3%, ENOLA 1%, NASSAU BAY 1%

USER_MAILING_STATE: TX 99%, PA 1%

USER_MAILING_ZIP: 77030 23%, 77338 11%, 77375 11%, 77598 9%, 77004 9%, 77054 6%, 77070 6%, 77065 6%, 77521 6%, 77091 4%, 77090 4%, 77008 4%

USER_CHEMICAL_DEPENDENCY_BEDS: nan 99%, 24.0 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 77 | 0 | 77 1; 76 1; 75 1; 74 1 |
| STATUS | other | 1 | 0 | M 77 |
| SCORE | amount | 11 | 0 | 100.0 63; 99.0 4; 99.62 2; 99.01 1 |
| MATCH_TYPE | category | 3 | 0 | A 72; PP 4; M 1 |
| MATCH_ADDR | other | 75 | 0 | 1917 Ashland St, Houston, 2; 1475 FM 1960 Bypass Rd E, 1; 9430 Katy Fwy, Houston, T 1; 510 W Tidwell Rd, Houston 1 |
| LONGLABEL | other | 74 | 0 | 1917 Ashland St, Houston, 2; 1475 FM 1960 Bypass Rd E, 1; 9430 Katy Fwy, Houston, T 1; 510 W Tidwell Rd, Houston 1 |
| SHORTLABEL | other | 77 | 0 | 1917 Ashland St 2; 1475 FM 1960 Bypass Rd E 1; 9430 Katy Fwy 1; 510 W Tidwell Rd 1 |
| ADDR_TYPE | category | 4 | 0 | PointAddress 60; StreetAddress 14; Subaddress 2; POI 1 |
| TYPE | category | 2 | 76 | Hospital 1 |
| PLACENAME | category | 2 | 76 | Houston Methodist Clear L 1 |
| PLACE_ADDR | other | 75 | 0 | 1917 Ashland St, Houston, 2; 1475 FM 1960 Bypass Rd E, 1; 9430 Katy Fwy, Houston, T 1; 510 W Tidwell Rd, Houston 1 |
| PHONE | category | 2 | 76 | (281) 523-2000 1 |
| URL | category | 2 | 76 | http://www.houstonmethodi 1 |
| RANK | category | 2 | 0 | 20 76; 18 1 |
| ADDBLDG | empty | 1 | 77 |  |
| ADDNUM | other | 72 | 0 | 7600 2; 1917 2; 4801 2; 2001 2 |
| ADDNUMFROM | category | 15 | 63 | 4640 1; 1499 1; 19201 1; 16700 1 |
| ADDNUMTO | category | 15 | 63 | 4600 1; 1401 1; 19469 1; 16908 1 |
| ADDRANGE | category | 15 | 63 | 4600-4640 1; 1401-1499 1; 19201-19469 1; 16700-16908 1 |
| SIDE | category | 3 | 63 | L 7; R 7 |
| STPREDIR | category | 5 | 65 | W 6; E 4; N 1; S 1 |
| STPRETYPE | empty | 1 | 77 |  |
| STNAME | who | 56 | 0 | Katy 4; Fannin 4; Medical Center 4; Red Oak 3 |
| STTYPE | category | 11 | 2 | St 18; Dr 16; Rd 10; Blvd 9 |
| STDIR | category | 4 | 70 | S 4; E 2; W 1 |
| BLDGTYPE | empty | 1 | 77 |  |
| BLDGNAME | empty | 1 | 77 |  |
| LEVELTYPE | empty | 1 | 77 |  |
| LEVELNAME | empty | 1 | 77 |  |
| UNITTYPE | category | 2 | 75 | Ste 2 |
| UNITNAME | category | 3 | 75 | 102 1; 100 1 |
| SUBADDR | category | 3 | 75 | Ste 102 1; Ste 100 1 |
| STADDR | other | 76 | 0 | 1917 Ashland St 2; 2001 Hermann Dr 2; 1475 FM 1960 Bypass Rd E 1; 9430 Katy Fwy 1 |
| BLOCK | empty | 1 | 77 |  |
| SECTOR | empty | 1 | 77 |  |
| NBRHD | category | 6 | 72 | Downtown 1; Golfcrest/Bellfort/Reveil 1; Greater Heights 1; Fairfield 1 |
| DISTRICT | empty | 1 | 77 |  |
| CITY | category | 10 | 0 | Houston 47; Webster 6; Humble 5; Pasadena 4 |
| METROAREA | category | 2 | 59 | Houston-Galveston Metro A 18 |
| SUBREGION | who | 1 | 0 | Harris 77 |
| REGION | other | 1 | 0 | Texas 77 |
| REGIONABBR | other | 1 | 0 | TX 77 |
| TERRITORY | empty | 1 | 77 |  |
| ZONE | empty | 1 | 77 |  |
| POSTAL | category | 35 | 0 | 77030 10; 77598 6; 77338 5; 77090 5 |
| POSTALEXT | other | 73 | 4 | 3907 2; 7643 2; 3909 1; 6320 1 |
| COUNTRY | other | 1 | 0 | USA 77 |
| LANGCODE | other | 1 | 0 | ENG 77 |
| DISTANCE | other | 1 | 0 | 0 77 |
| X | amount | 75 | 0 | -95.404221 2; -95.38235404 2; -95.2524675 1; -95.52509536 1 |
| Y | amount | 75 | 0 | 29.803644 2; 29.71812634 2; 30.004884 1; 29.78501023 1 |
| DISPLAYX | amount | 75 | 0 | -95.404221 2; -95.382621 2; -95.2524675 1; -95.525091 1 |
| DISPLAYY | amount | 75 | 0 | 29.803644 2; 29.718441 2; 30.004884 1; 29.78523 1 |
| XMIN | amount | 76 | 0 | -95.405221 2; -95.383621 2; -95.2534675 1; -95.526091 1 |
| XMAX | amount | 75 | 0 | -95.403221 2; -95.381621 2; -95.2514675 1; -95.524091 1 |
| YMIN | amount | 76 | 0 | 29.802644 2; 29.717441 2; 30.003884 1; 29.78423 1 |
| YMAX | amount | 75 | 0 | 29.804644 2; 29.719441 2; 30.005884 1; 29.78623 1 |
| EXINFO | category | 5 | 73 | OLD 1; B 1; 4 & 5 1; 18300 / DRIVE 1 |
| RESULTID | other | 77 | 0 | 588 1; 589 1; 594 1; 595 1 |
| IN_ADDRESS | other | 77 | 0 | 1475 FM 1960 BYPASS E 1; 9430 OLD KATY ROAD SUITE  1; 510 WEST TIDWELL ROAD 1; 17400 RED OAK DR 1 |
| IN_ADDRESS2 | empty | 1 | 77 |  |
| IN_ADDRESS3 | empty | 1 | 77 |  |
| IN_NEIGHBORHOOD | empty | 1 | 77 |  |
| IN_CITY | category | 11 | 0 | HOUSTON 46; WEBSTER 6; HUMBLE 5; PASADENA 4 |
| IN_SUBREGION | who | 1 | 0 | HARRIS 77 |
| IN_REGION | other | 1 | 0 | TX 77 |
| IN_POSTAL | category | 35 | 0 | 77030 10; 77598 6; 77338 5; 77090 5 |
| IN_POSTALEXT | empty | 1 | 77 |  |
| IN_COUNTRYCODE | empty | 1 | 77 |  |
| USER_FIELD1 | other | 78 | 0 | 587 1; 588 1; 593 1; 594 1 |
| USER_NAME | who | 76 | 0 | TOWNSEN MEMORIAL HOSPITAL 1; TRINITY HOSPITAL 1; UNITED MEMORIAL MEDICAL C 1; UNITED MEMORIAL MEDICAL C 1 |
| USER_LICENSE_NUMBER | other | 65 | 0 | 8450 3; 347 3; 7134 3; 117 2 |
| USER_CCN | amount | 54 | 0 | nan 9; 450803.0 3; 450184.0 3; 450068.0 3 |
| USER_EXPIRATION | date | 23 | 0 | 1577750400000 11; 1580428800000 7; 1612051200000 5; 1564531200000 5 |
| USER_EFFECTIVE | date | 69 | 0 | -315619200000 4; 1498867200000 3; 1188518400000 2; 1391212800000 2 |
| USER_DESIGNATION_SERVICES_ACCRE | other | 68 | 0 | Comprehensive Medical Reh 4; Diagnostic X-ray, Emergen 3; Diagnostic X-ray, Emergen 3; Det Norske Veritas Health 2 |
| USER_CEO_ADMINISTRATOR | other | 57 | 0 | HARALSON, GREGORY 3; KOHLER, TRACY 3; GERKEN, GREGG 3; VARON, JOSEPH 2 |
| USER_ADDRESS | other | 77 | 0 | 1475 FM 1960 BYPASS E 1; 9430 OLD KATY ROAD SUITE  1; 510 WEST TIDWELL ROAD 1; 17400 RED OAK DR 1 |
| USER_CITY | category | 11 | 0 | HOUSTON 46; WEBSTER 6; HUMBLE 5; PASADENA 4 |
| USER_STATE | other | 1 | 0 | TX 77 |
| USER_ZIP | category | 35 | 0 | 77030 10; 77598 6; 77338 5; 77090 5 |
| USER_PHONE | other | 77 | 0 | 7135666297 2; 2819642100 1; 7134611000 1; 2816188505 1 |
| USER_COUNTY | who | 1 | 0 | HARRIS 77 |
| USER_MAILING_ADDRESS | other | 71 | 0 | 505 GRAHAM DRIVE 3; 510 WEST TIDWELL 2; 1401 ST JOSEPH PARKWAY 2; 6411 FANNIN 2 |
| USER_MAILING_CITY | category | 14 | 0 | HOUSTON 43; HUMBLE 5; TOMBALL 5; PASADENA 4 |
| USER_MAILING_STATE | category | 2 | 0 | TX 76; PA 1 |
| USER_MAILING_ZIP | category | 35 | 0 | 77030 11; 77338 5; 77375 5; 77598 4 |
| USER_ICU_CCU_BEDS | amount | 31 | 0 | nan 28; 12.0 6; 16.0 4; 24.0 3 |
| USER_MED_SURG_BEDS | amount | 54 | 0 | nan 13; 4.0 3; 101.0 2; 46.0 2 |
| USER_NICU_BEDS | amount | 16 | 0 | nan 59; 10.0 3; 20.0 2; 146.0 1 |
| USER_POSTPARTUM_BEDS | amount | 16 | 0 | nan 61; 24.0 2; 144.0 1; 48.0 1 |
| USER_ANTEPARTUM_BEDS | amount | 9 | 0 | nan 67; 8.0 3; 48.0 1; 22.0 1 |
| USER_PEDIATRIC_BEDS | amount | 11 | 0 | nan 66; 18.0 2; 64.0 1; 331.0 1 |
| USER_LDRP_BEDS | amount | 9 | 0 | nan 65; 14.0 3; 10.0 3; 50.0 1 |
| USER_PSYCH_BEDS | amount | 7 | 0 | nan 71; 95.0 1; 31.0 1; 14.0 1 |
| USER_SKILLED_NURSING_BEDS | amount | 5 | 0 | nan 72; 9.0 2; 50.0 1; 18.0 1 |
| USER_COMP_MED_REHAB_BEDS | amount | 19 | 0 | nan 53; 60.0 3; 24.0 3; 22.0 2 |
| USER_CONTINUING_CARE_BEDS | amount | 7 | 0 | nan 66; 8.0 3; 6.0 2; 1.0 2 |
| USER_INTERMEDIATE_CARE_BEDS | amount | 7 | 0 | nan 69; 3.0 2; 26.0 1; 24.0 1 |
| USER_UNIVERSAL_CARE_BEDS | amount | 7 | 0 | nan 71; 3.0 1; 163.0 1; 72.0 1 |
| USER_CHEMICAL_DEPENDENCY_BEDS | category | 2 | 0 | nan 76; 24.0 1 |
| USER_TOTAL_BEDS | amount | 65 | 0 | 60.0 3; 74.0 3; nan 2; 134.0 2 |
| GEOMETRY | other | 75 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:32:08.23228 77 |
| SOURCE_RUN_ID | audit | 1 | 0 | ccdd5485-1049-41d0-bf63-7 77 |
| SRC_SHA256 | who | 1 | 0 | d8ecead257d110c8c40aea8c8 77 |
