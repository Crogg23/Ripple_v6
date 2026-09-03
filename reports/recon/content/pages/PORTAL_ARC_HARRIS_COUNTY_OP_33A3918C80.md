# PORTAL_ARC_HARRIS_COUNTY_OP_33A3918C80

rows 363  columns 40  scan 4.2s

roles: amount 2, audit 2, category 12, date 5, other 15, who 5

## when

SOURCE_DAT
  2024       363  ##############################

VAL_DATE
  2010       193  ##############################
  2011         3  
  2013        15  ##
  2014         6  #
  2016        58  #########
  2017         5  #
  2018        13  ##
  2019        23  ####
  2020         9  #
  2022        28  ####
  2024        10  ##

CREATIONDATE
  2026       363  ##############################

EDITDATE
  2026       363  ##############################

INGESTED_AT
  2026       363  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 363 | 29.52 | 29.73 | 29.93 | 29.94 | 10.8K |
| LONGITUDE | 363 | -95.47 | -95.24 | -94.96 | -94.93 | -34.6K |

## who

NAME by rows
         3  DE ZAVALA EL
         2  HIGHPOINT
         2  SAN JACINTO EL
         2  BETA ACADEMY
         1  DR KIRK LEWIS CAREER AND TECHNICAL H S
         1  LA PORTE J H
         1  CARTER LOMAX MIDDLE
         1  MAE SMYTHE EL
         1  G H WHITCOMB EL
         1  MELILLO MIDDLE
         1  ATKINSON EL
         1  GALENA PARK H S
         1  GALLEGOS EL
         1  LEO A RIZZUTO EL
         1  L F SMITH EL
         1  WHITTIER EL
         1  GREGG EL
         1  JOHN F WARD EL
         1  PSTEM ACADEMY
         1  SPACE CENTER INT

NAME by dollars
       89.24        3 rows  DE ZAVALA EL
       59.66        2 rows  HIGHPOINT
       59.44        2 rows  SAN JACINTO EL
       59.26        2 rows  BETA ACADEMY
       29.94        1 rows  HALL SUCCESS ACADEMY
       29.94        1 rows  SST EXCELLENCE
       29.93        1 rows  MARCELLA EL
       29.93        1 rows  LANE SCHOOL
       29.93        1 rows  ECKERT EL
       29.93        1 rows  DE SANTIAGO EC/PK/K
       29.93        1 rows  BLACK EL
       29.93        1 rows  ALDINE MIDDLE
       29.92        1 rows  ALDINE H S
       29.92        1 rows  GRAY EL
       29.92        1 rows  WILSON EL
       29.92        1 rows  BUSSEY EL
       29.92        1 rows  NORTH CENTRAL EL
       29.92        1 rows  STEHLIK EL
       29.92        1 rows  CARTER ACADEMY
       29.92        1 rows  THOMPSON EL

NAICS_DESC by rows
       363  ELEMENTARY AND SECONDARY SCHOOLS

NAICS_DESC by dollars
       10.8K      363 rows  ELEMENTARY AND SECONDARY SCHOOLS

CREATOR by rows
       363  JGuerraPct2

CREATOR by dollars
       10.8K      363 rows  JGuerraPct2

COUNTY by rows
       363  HARRIS

COUNTY by dollars
       10.8K      363 rows  HARRIS

## who x when

NAME by VAL_DATE, dollars = LATITUDE
  ALDINE H S                                2011:29.92
  ALDINE MIDDLE                             2010:29.93
  ATKINSON EL                               2010:29.61
  BETA ACADEMY                              2019:29.63 2022:29.63
  BLACK EL                                  2010:29.93
  CARTER LOMAX MIDDLE                       2010:29.63
  DE SANTIAGO EC/PK/K                       2010:29.93
  DE ZAVALA EL                              2010:89.24
  DR KIRK LEWIS CAREER AND TECHNICAL H S    2020:29.63
  ECKERT EL                                 2022:29.93
  G H WHITCOMB EL                           2010:29.56
  GALENA PARK H S                           2010:29.74
  GALLEGOS EL                               2016:29.73
  GRAY EL                                   2010:29.92
  GREGG EL                                  2016:29.67
  HALL SUCCESS ACADEMY                      2013:29.94
  HIGHPOINT                                 2013:29.82 2018:29.84
  JOHN F WARD EL                            2010:29.58
  L F SMITH EL                              2010:29.67
  LA PORTE J H                              2010:29.66
  LANE SCHOOL                               2010:29.93
  LEO A RIZZUTO EL                          2010:29.66
  MAE SMYTHE EL                             2010:29.68
  MARCELLA EL                               2022:29.93
  MELILLO MIDDLE                            2019:29.58
  PSTEM ACADEMY                             2013:29.70
  SAN JACINTO EL                            2010:59.44
  SPACE CENTER INT                          2010:29.56
  SST EXCELLENCE                            2020:29.94
  WHITTIER EL                               2016:29.77

NAICS_DESC by VAL_DATE, dollars = LATITUDE
  ELEMENTARY AND SECONDARY SCHOOLS          2010:5.7K 2011:89.26 2013:446.44 2014:178.39 2016:1.7K 2017:148.45 2018:386.09 2019:683.94 2020:267.81 2022:834.88 2024:297.97

## what

CITY: HOUSTON 65%, PASADENA 13%, BAYTOWN 7%, LA PORTE 3%, DEER PARK 3%, CHANNELVIEW 2%, SO HOUSTON 1%, FRIENDSWOOD 1%, HIGHLANDS 1%, GALENA PARK 1%, SEABROOK 1%, WEBSTER 1%

ZIP: 77049 12%, 77039 9%, 77520 8%, 77023 8%, 77012 8%, 77093 8%, 77076 8%, 77503 8%, 77017 8%, 77075 8%, 77571 8%, 77015 7%

TYPE: 1 89%, 4 10%, 2 0%

STATUS: 1 95%, CLOSED 2%, 3 1%, 6 1%, 2 1%

VAL_METHOD: IMAGERY/OTHER 81%, IMAGERY 17%, GEOCODE 2%

WEBSITE: NOT AVAILABLE 38%, http://www.houstonisd.org 26%, http://www.aldineisd.org 11%, http://www.ccisd.net 7%, http://www.galenaparkisd.com 6%, http://www.dpisd.org 3%, http://www.cvisd.org 2%, http://www.kipptexas.org 2%, http://ryss.org 2%, http://www.hcde-texas.org 1%, http://ideapublicschools.org/o 1%, http://www.responsiveed.com/pr 1%

LEVEL: ELEMENTARY 57%, MIDDLE 21%, HIGH 15%, SECONDARY 2%, OTHER 2%, NOT REPORTED 2%, PREKINDERGARTEN 1%

ST_GRADE: PK 47%, 06 15%, 09 12%, 01 6%, KG 6%, 05 4%, 07 4%, 08 2%, M 2%, 03 1%, 02 0%, 10 0%

END_GRADE: 05 40%, 08 19%, 12 17%, 04 11%, 06 4%, KG 2%, M 2%, 11 2%, PK 1%, 02 1%, 10 1%, 07 1%

DISTRICTID: 4823640 27%, 4834320 20%, 4807710 12%, 4821150 9%, 4814280 7%, 4820250 7%, 4816530 5%, 4826190 4%, 4800209 3%, 4800264 2%, 4813590 2%, 4800022 2%

SHELTER_ID: NOT AVAILABLE 97%, 10799857 0%, 10822833 0%, 11548720 0%, 10794047 0%, 11548739 0%, 11548743 0%, 11548722 0%, 11548749 0%, 11548734 0%, 11548740 0%, 11548746 0%

EDITOR: JGuerraPct2 98%, camerondavis1 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 361 | 0 | 364 2; 363 2; 362 2; 361 2 |
| NCESID | other | 363 | 0 | 480025813571 2; 480771012521 2; 480771013776 2; 480771013688 2 |
| NAME | who | 361 | 0 | HIGHPOINT 3; DE ZAVALA EL 3; SST EXCELLENCE 2; HALL SUCCESS ACADEMY 2 |
| ADDRESS | other | 343 | 0 | 8003 E SAM HOUSTON PKWY N 4; 11101 AIRLINE DR 3; 1930 LITTLE YORK RD 3; 500 TIDWELL DR 3 |
| CITY | category | 15 | 0 | HOUSTON 234; PASADENA 47; BAYTOWN 24; LA PORTE 12 |
| STATE | other | 1 | 0 | TX 363 |
| ZIP | category | 48 | 0 | 77049 18; 77039 14; 77520 13; 77023 13 |
| ZIP4 | other | 220 | 0 | NOT AVAILABLE 125; 6496 12; 3097 3; 2916 2 |
| TELEPHONE | other | 352 | 0 | (713) 640-3700 5; (832) 230-0566 4; (281) 420-4800 4; (832) 360-7453 3 |
| TYPE | category | 3 | 0 | 1 324; 4 38; 2 1 |
| STATUS | category | 5 | 0 | 1 344; CLOSED 9; 3 4; 6 4 |
| POPULATION | other | 303 | 0 | -999 7; 657 4; 554 3; 638 3 |
| COUNTY | who | 1 | 0 | HARRIS 363 |
| COUNTYFIPS | other | 1 | 0 | 48201 363 |
| COUNTRY | other | 1 | 0 | USA 363 |
| LATITUDE | amount | 360 | 0 | 29.814193 3; 29.9385318 2; 29.9363791 2; 29.9349796 2 |
| LONGITUDE | amount | 364 | 0 | -95.211247 3; -95.4007166 2; -95.3552656 2; -95.3948516 2 |
| NAICS_CODE | other | 1 | 0 | 611110 363 |
| NAICS_DESC | who | 1 | 0 | ELEMENTARY AND SECONDARY  363 |
| SOURCE | other | 358 | 0 | https://nces.ed.gov/ccd/s 2; https://nces.ed.gov/ccd/s 2; https://nces.ed.gov/ccd/s 2; https://nces.ed.gov/ccd/s 2 |
| SOURCE_DAT | date | 1 | 0 | 1706680800000 363 |
| VAL_METHOD | category | 3 | 0 | IMAGERY/OTHER 294; IMAGERY 60; GEOCODE 9 |
| VAL_DATE | date | 55 | 0 | 1475128800000 54; 1652335200000 28; 1266991200000 26; 1268719200000 25 |
| WEBSITE | category | 41 | 0 | NOT AVAILABLE 124; http://www.houstonisd.org 86; http://www.aldineisd.org 37; http://www.ccisd.net 24 |
| LEVEL | category | 7 | 0 | ELEMENTARY 206; MIDDLE 77; HIGH 54; SECONDARY 9 |
| ENROLLMENT | other | 306 | 0 | -999 7; 607 3; 552 3; 714 3 |
| ST_GRADE | category | 12 | 0 | PK 171; 06 54; 09 45; 01 22 |
| END_GRADE | category | 15 | 0 | 05 145; 08 68; 12 61; 04 41 |
| DISTRICTID | category | 35 | 0 | 4823640 88; 4834320 64; 4807710 39; 4821150 28 |
| FT_TEACHER | other | 90 | 0 | -999 15; 36 12; 37 12; 41 12 |
| SHELTER_ID | category | 23 | 0 | NOT AVAILABLE 340; 10799857 1; 10822833 1; 11548720 1 |
| GLOBALID | other | 360 | 0 | 83830ac7-5bbd-4bd0-94f1-1 2; bca14b0e-febb-40d3-9d94-6 2; e08bbdaa-7467-4b15-ae39-5 2; 03056040-5360-466f-a0f1-2 2 |
| CREATIONDATE | date | 1 | 0 | 1768918783661 363 |
| CREATOR | who | 1 | 0 | JGuerraPct2 363 |
| EDITDATE | date | 10 | 0 | 1768918783661 354; 1773939503239 1; 1773939368664 1; 1773939198593 1 |
| EDITOR | category | 2 | 0 | JGuerraPct2 354; camerondavis1 9 |
| GEOMETRY | other | 363 | 0 | {"type": "Point", "coordi 3; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:22:51.30389 363 |
| SOURCE_RUN_ID | audit | 1 | 0 | 720bfa01-3554-4823-93a9-8 363 |
| SRC_SHA256 | who | 1 | 0 | b52a50fe15fcfd96168d46afd 363 |
