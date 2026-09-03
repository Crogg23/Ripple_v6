# PORTAL_ARC_HARRIS_COUNTY_OP_7BD125DFB0

rows 359  columns 40  scan 4.8s

roles: amount 5, audit 2, category 16, date 5, other 9, who 4

## when

SOURCE_DAT
  2024       358  ##############################
  2025         1  

VAL_DATE
  2010       188  ##############################
  2011         3  
  2013        15  ##
  2014         6  #
  2016        58  #########
  2017         5  #
  2018        13  ##
  2019        23  ####
  2020         8  #
  2022        28  ####
  2024        10  ##
  2025         2  

CREATIONDATE
  2025       359  ##############################

EDITDATE
  2025       359  ##############################

INGESTED_AT
  2026       359  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POPULATION | 358 | -999 | 597 | 2.9K | 4.3K | 234.7K |
| LATITUDE | 358 | 29.52 | 29.73 | 29.93 | 29.94 | 10.6K |
| LONGITUDE | 358 | -95.47 | -95.24 | -94.96 | -94.93 | -34.1K |
| ENROLLMENT | 358 | -999 | 557.50 | 2.7K | 4.0K | 220.0K |
| FT_TEACHER | 358 | -999 | 37 | 162.73 | 262 | 761 |

## who

NAME by rows
         3  DE ZAVALA EL
         2  HIGHPOINT
         2  SAN JACINTO EL
         1  MAE SMYTHE EL
         1  CHAVEZ H S
         1  LOMAX J H
         1  DEER PARK EL
         1  EARLY COLLEGE T-STEM ACADEMY HS
         1  SPACE CENTER INT
         1  STEVENSON MIDDLE
         1  PASADENA H S
         1  DEADY MIDDLE
         1  ILTEXAS HOUSTON WINDMILL LAKES EL
         1  MCMASTERS EL
         1  NORTHSIDE H S
         1  EDISON MIDDLE
         1  MACARTHUR EL
         1  THE SUMMIT (HIGH SCHOOL)
         1  HARTMAN MIDDLE
         1  LA PORTE EL

NAME by dollars
        4.3K        1 rows  DEER PARK H S SOUTH
        3.7K        1 rows  MACARTHUR H S
        3.2K        1 rows  PASADENA MEMORIAL H S
        2.9K        1 rows  HOUSTON MATH SCIENCE AND TECHNOLOGY CENTER
        2.8K        1 rows  SAM RAYBURN H S
        2.8K        1 rows  ALDINE H S
        2.7K        1 rows  CLEAR LAKE H S
        2.5K        1 rows  CLEAR BROOK H S
        2.4K        1 rows  CHAVEZ H S
        2.4K        1 rows  PASADENA H S
        2.4K        1 rows  SOUTH HOUSTON H S
        2.2K        1 rows  STERLING H S
        2.2K        1 rows  MILBY H S
        2.2K        1 rows  LA PORTE H S
        2.0K        1 rows  GALENA PARK H S
        2.0K        1 rows  LEE H S
        1.6K        3 rows  DE ZAVALA EL
        1.6K        2 rows  SAN JACINTO EL
        1.5K        1 rows  DR KIRK LEWIS CAREER AND TECHNICAL H S
        1.5K        1 rows  AUSTIN H S

CREATOR by rows
       359  JGuerraPct2

CREATOR by dollars
      234.7K      359 rows  JGuerraPct2

EDITOR by rows
       359  JGuerraPct2

EDITOR by dollars
      234.7K      359 rows  JGuerraPct2

SRC_SHA256 by rows
       359  45226ee9c117ab6ca951174050ae963d076f032753d02043e6fd81a482b48f07

SRC_SHA256 by dollars
      234.7K      359 rows  45226ee9c117ab6ca951174050ae963d076f032753d02043e6fd81a482b4

## who x when

NAME by VAL_DATE, dollars = POPULATION
  ALDINE H S                                2011:2.8K
  CHAVEZ H S                                2011:2.4K
  CLEAR BROOK H S                           2010:2.5K
  CLEAR LAKE H S                            2010:2.7K
  DE ZAVALA EL                              2010:1.6K
  DEADY MIDDLE                              2016:626
  DEER PARK EL                              2010:779
  DEER PARK H S SOUTH                       2017:4.3K
  EARLY COLLEGE T-STEM ACADEMY HS           2017:335
  EDISON MIDDLE                             2016:497
  HARTMAN MIDDLE                            2016:962
  HIGHPOINT                                 2013:13 2018:-999
  HOUSTON MATH SCIENCE AND TECHNOLOGY CENT  2019:2.9K
  ILTEXAS HOUSTON WINDMILL LAKES EL         2020:891
  LA PORTE EL                               2010:564
  LOMAX J H                                 2010:616
  MACARTHUR EL                              2010:657
  MACARTHUR H S                             2019:3.7K
  MAE SMYTHE EL                             2010:752
  MCMASTERS EL                              2010:393
  NORTHSIDE H S                             2016:1.2K
  PASADENA H S                              2010:2.4K
  PASADENA MEMORIAL H S                     2010:3.2K
  SAM RAYBURN H S                           2010:2.8K
  SAN JACINTO EL                            2010:1.6K
  SOUTH HOUSTON H S                         2011:2.4K
  SPACE CENTER INT                          2010:885
  STERLING H S                              2017:2.2K
  STEVENSON MIDDLE                          2016:1.3K
  THE SUMMIT (HIGH SCHOOL)                  2010:163

CREATOR by VAL_DATE, dollars = POPULATION
  JGuerraPct2                               2010:126.5K 2011:7.6K 2013:7.9K 2014:3.2K 2016:33.4K 2017:7.6K 2018:3.6K 2019:18.4K 2020:7.5K 2022:16.2K 2024:2.1K 2025:948

## what

CITY: HOUSTON 65%, PASADENA 13%, BAYTOWN 7%, LA PORTE 3%, DEER PARK 3%, CHANNELVIEW 2%, SO HOUSTON 1%, FRIENDSWOOD 1%, GALENA PARK 1%, SEABROOK 1%, HIGHLANDS 1%, WEBSTER 1%

ZIP: 77049 12%, 77039 9%, 77520 8%, 77023 8%, 77012 8%, 77093 8%, 77076 8%, 77503 8%, 77017 8%, 77075 8%, 77571 8%, 77536 7%

TYPE: 1 90%, 4 10%, High School 0%, 2 0%

STATUS: 1 97%, 6 1%, 3 1%, 2 1%

COUNTY: HARRIS 100%, Harris 0%

COUNTYFIPS: 48201 100%

COUNTRY: USA 100%, United States 0%

NAICS_CODE: 611110 100%

NAICS_DESC: ELEMENTARY AND SECONDARY SCHOO 100%

VAL_METHOD: IMAGERY/OTHER 82%, IMAGERY 16%, GEOCODE 2%

WEBSITE: NOT AVAILABLE 38%, http://www.houstonisd.org 26%, http://www.aldineisd.org 11%, http://www.ccisd.net 7%, http://www.galenaparkisd.com 6%, http://www.dpisd.org 3%, http://www.cvisd.org 2%, http://www.kipptexas.org 2%, http://ryss.org 2%, http://www.hcde-texas.org 1%, http://ideapublicschools.org/o 1%, http://www.responsiveed.com/pr 1%

LEVEL: ELEMENTARY 57%, MIDDLE 21%, HIGH 15%, SECONDARY 2%, OTHER 2%, NOT REPORTED 2%, PREKINDERGARTEN 1%, High 0%

ST_GRADE: PK 48%, 06 15%, 09 13%, KG 6%, 01 5%, 05 4%, 07 4%, M 2%, 08 2%, 03 1%, 9th 0%, 02 0%

END_GRADE: 05 40%, 08 19%, 12 17%, 04 12%, 06 4%, KG 2%, M 2%, 11 2%, PK 1%, 02 1%, 07 1%, 9th 0%

DISTRICTID: 4823640 27%, 4834320 20%, 4807710 12%, 4821150 8%, 4814280 7%, 4820250 7%, 4816530 4%, 4826190 4%, 4800209 3%, 4800264 2%, 4813590 2%, 4800022 2%

SHELTER_ID: NOT AVAILABLE 97%, 10799857 0%, 10822833 0%, 11548720 0%, 10794047 0%, 11548739 0%, 11548743 0%, 11548722 0%, 11548749 0%, 11548734 0%, 11548740 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NCESID | other | 358 | 1 | 480025813571 2; 480771012521 2; 480771013776 2; 480771013688 2 |
| NAME | who | 360 | 0 | HIGHPOINT 3; DE ZAVALA EL 3; DEER PARK H S North 2; SST EXCELLENCE 2 |
| ADDRESS | other | 340 | 0 | 8003 E SAM HOUSTON PKWY N 4; 11101 AIRLINE DR 3; 1930 LITTLE YORK RD 3; 500 TIDWELL DR 3 |
| CITY | category | 16 | 0 | HOUSTON 231; PASADENA 47; BAYTOWN 24; LA PORTE 12 |
| STATE | other | 1 | 0 | TX 359 |
| ZIP | category | 48 | 0 | 77049 18; 77039 14; 77520 13; 77023 13 |
| ZIP4 | other | 219 | 1 | NOT AVAILABLE 122; 6496 12; 3097 3; 2916 2 |
| TELEPHONE | other | 347 | 0 | (713) 640-3700 5; (832) 230-0566 4; (281) 420-4800 4; (832) 360-7453 3 |
| TYPE | category | 4 | 0 | 1 322; 4 35; High School 1; 2 1 |
| STATUS | category | 5 | 1 | 1 347; 6 5; 3 4; 2 2 |
| POPULATION | amount | 296 | 0 | -999.0 7; 657.0 4; 554.0 3; 638.0 3 |
| COUNTY | category | 2 | 0 | HARRIS 358; Harris 1 |
| COUNTYFIPS | category | 2 | 1 | 48201 358 |
| COUNTRY | category | 2 | 0 | USA 358; United States 1 |
| LATITUDE | amount | 356 | 0 | 29.814193 3; nan 2; 29.9385318 2; 29.9363791 2 |
| LONGITUDE | amount | 359 | 0 | -95.211247 3; nan 2; -95.4007166 2; -95.3552656 2 |
| NAICS_CODE | category | 2 | 1 | 611110 358 |
| NAICS_DESC | category | 2 | 1 | ELEMENTARY AND SECONDARY  358 |
| SOURCE | other | 355 | 1 | https://nces.ed.gov/ccd/s 2; https://nces.ed.gov/ccd/s 2; https://nces.ed.gov/ccd/s 2; https://nces.ed.gov/ccd/s 2 |
| SOURCE_DAT | date | 2 | 0 | 1706659200000 358; 1750438781000 1 |
| VAL_METHOD | category | 4 | 1 | IMAGERY/OTHER 292; IMAGERY 58; GEOCODE 8 |
| VAL_DATE | date | 57 | 0 | 1475107200000 54; 1652313600000 28; 1268697600000 25; 1266969600000 25 |
| WEBSITE | category | 41 | 0 | NOT AVAILABLE 122; http://www.houstonisd.org 86; http://www.aldineisd.org 35; http://www.ccisd.net 24 |
| LEVEL | category | 8 | 0 | ELEMENTARY 203; MIDDLE 77; HIGH 53; SECONDARY 8 |
| ENROLLMENT | amount | 304 | 0 | -999.0 7; 607.0 3; 552.0 3; 714.0 3 |
| ST_GRADE | category | 13 | 0 | PK 171; 06 53; 09 45; KG 21 |
| END_GRADE | category | 16 | 0 | 05 143; 08 67; 12 60; 04 41 |
| DISTRICTID | category | 35 | 0 | 4823640 88; 4834320 64; 4807710 37; 4821150 27 |
| FT_TEACHER | amount | 90 | 0 | -999.0 14; 36.0 12; 37.0 12; 41.0 12 |
| SHELTER_ID | category | 24 | 1 | NOT AVAILABLE 335; 10799857 1; 10822833 1; 11548720 1 |
| OBJECTID | other | 359 | 0 | 359 2; 358 2; 357 2; 356 2 |
| GLOBALID | other | 361 | 0 | 8ae3eff3-ebc8-46f6-b42c-8 2; b42df006-51d3-42bb-bc8a-2 2; e8e69919-fdce-4e87-aee6-0 2; b865a659-7937-4e77-9c94-5 2 |
| CREATIONDATE | date | 1 | 0 | 1751916681547 359 |
| CREATOR | who | 1 | 0 | JGuerraPct2 359 |
| EDITDATE | date | 1 | 0 | 1751916681547 359 |
| EDITOR | who | 1 | 0 | JGuerraPct2 359 |
| GEOMETRY | other | 360 | 0 | {"type": "Point", "coordi 3; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:45:47.71438 359 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1cee6a88-2ded-485e-bc84-e 359 |
| SRC_SHA256 | who | 1 | 0 | 45226ee9c117ab6ca95117405 359 |
