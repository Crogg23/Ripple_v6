# PORTAL_ARC_HARRIS_COUNTY_OP_1966AC023B

rows 55  columns 36  scan 3.7s

roles: amount 4, audit 2, category 12, date 2, empty 1, other 12, who 4

## when

VAL_DATE
  2010        17  ##############################
  2011         3  #####
  2013         5  #########
  2016         4  #######
  2017         4  #######
  2018         5  #########
  2019         7  ############
  2020         2  ####
  2022         6  ###########
  2024         1  ##

INGESTED_AT
  2026        55  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POPULATION | 54 | 10 | 502 | 4.0K | 4.3K | 60.4K |
| LATITUDE | 54 | 29.53 | 29.73 | 29.93 | 29.94 | 1.6K |
| LONGITUDE | 54 | -95.42 | -95.24 | -94.97 | -94.97 | -5.1K |
| FT_TEACHER | 51 | 2 | 37 | 227.50 | 262 | 3.5K |

## who

NAME by rows
         1  HIGHPOINT SCHOOL EAST (DAEP)
         1  LA PORTE H S
         1  YES PREP - EAST END
         1  GEORGE I SANCHEZ NORTH
         1  YES PREP - NORTH CENTRAL
         1  CLEAR LAKE H S
         1  AVALOS P-TECH SCHOOL
         1  HIGH POINT EAST
         1  POINT ALTERNATIVE CENTER
         1  CLEAR BROOK H S
         1  GALENA PARK H S
         1  TEXANS CAN ACADEMY - HOUSTON HOBBY
         1  STERLING H S
         1  NORTHSIDE H S
         1  THE SUMMIT (HIGH SCHOOL)
         1  CLEAR HORIZONS EARLY COLLEGE H S
         1  EASTWOOD ACADEMY
         1  HIGHPOINT EAST
         1  PASADENA H S
         1  UNLIMITED VISIONS AFTERCARE

NAME by dollars
        4.3K        1 rows  DEER PARK H S
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
        1.5K        1 rows  AUSTIN H S
        1.4K        1 rows  BLANSON CTE H S
        1.2K        1 rows  NORTHSIDE H S
        1.2K        1 rows  FURR H S

NAICS_DESC by rows
        55  ELEMENTARY AND SECONDARY SCHOOLS

NAICS_DESC by dollars
       60.4K       55 rows  ELEMENTARY AND SECONDARY SCHOOLS

COUNTY by rows
        55  HARRIS

COUNTY by dollars
       60.4K       55 rows  HARRIS

SRC_SHA256 by rows
        55  eaaf9eab4fa7f36f46e9496dbecafbcdd07c1a1239b7be2417c52522af0370a8

SRC_SHA256 by dollars
       60.4K       55 rows  eaaf9eab4fa7f36f46e9496dbecafbcdd07c1a1239b7be2417c52522af03

## who x when

NAME by VAL_DATE, dollars = POPULATION
  ALDINE H S                                2011:2.8K
  AVALOS P-TECH SCHOOL                      2022:477
  CHAVEZ H S                                2011:2.4K
  CLEAR BROOK H S                           2010:2.5K
  CLEAR HORIZONS EARLY COLLEGE H S          2010:439
  CLEAR LAKE H S                            2010:2.7K
  DEER PARK H S                             2017:4.3K
  EASTWOOD ACADEMY                          2019:412
  GALENA PARK H S                           2010:2.0K
  GEORGE I SANCHEZ NORTH                    2018:383
  HIGH POINT EAST                           2010:12
  HIGHPOINT EAST                            2018:27
  HIGHPOINT SCHOOL EAST (DAEP)              2010:10
  HOUSTON MATH SCIENCE AND TECHNOLOGY CENT  2019:2.9K
  LA PORTE H S                              2010:2.2K
  LEE H S                                   2019:2.0K
  MACARTHUR H S                             2019:3.7K
  MILBY H S                                 2020:2.2K
  NORTHSIDE H S                             2016:1.2K
  PASADENA H S                              2010:2.4K
  PASADENA MEMORIAL H S                     2010:3.2K
  POINT ALTERNATIVE CENTER                  2010:116
  SAM RAYBURN H S                           2010:2.8K
  SOUTH HOUSTON H S                         2011:2.4K
  STERLING H S                              2017:2.2K
  TEXANS CAN ACADEMY - HOUSTON HOBBY        2016:330
  THE SUMMIT (HIGH SCHOOL)                  2010:163
  UNLIMITED VISIONS AFTERCARE               2018:17
  YES PREP - EAST END                       2010:1.0K
  YES PREP - NORTH CENTRAL                  2010:1.0K

NAICS_DESC by VAL_DATE, dollars = POPULATION
  ELEMENTARY AND SECONDARY SCHOOLS          2010:22.0K 2011:7.6K 2013:3.0K 2016:3.1K 2017:7.1K 2018:950 2019:10.3K 2020:2.7K 2022:3.7K 2024:72

## what

CITY: HOUSTON 60%, PASADENA 13%, BAYTOWN 9%, LA PORTE 4%, Channelview 2%, HIGHLANDS 2%, GALENA PARK 2%, DEER PARK 2%, DALLAS 2%, SO HOUSTON 2%, FRIENDSWOOD 2%, WEBSTER 2%

ZIP: 77049 13%, 77039 10%, 77076 10%, 77520 10%, 77034 10%, 77022 7%, 77009 7%, 77521 7%, 77003 7%, 77023 7%, 77012 7%, 77506 7%

ZIP4: NOT AVAILABLE 68%, 2305 5%, 6496 5%, 3518 2%, 3097 2%, 1183 2%, 5999 2%, 5224 2%, 8501 2%, 7815 2%, 5217 2%, 2301 2%

TYPE: 1 65%, 4 33%, nan 2%

STATUS: 1 98%, nan 2%

COUNTRY: USA 98%, US 2%

SOURCE_DAT: 1706680800000.0 98%, nan 2%

VAL_METHOD: IMAGERY/OTHER 71%, IMAGERY 20%, GEOCODE 7%, nan 2%

WEBSITE: NOT AVAILABLE 33%, http://www.houstonisd.org 24%, http://www.aldineisd.org 11%, http://www.ccisd.net 9%, http://www.responsiveed.com/pr 4%, http://www.texanscan.org 4%, www.cvisd.org 2%, http://northcentral.yesprep.or 2%, http://www.kipptexas.org 2%, http://www.hcde-texas.org 2%, http://www.galenaparkisd.com/c 2%, http://gccisd.net 2%

ST_GRADE: 09 78%, 06 9%, 08 5%, 07 4%, 10 2%, 05 2%

DISTRICTID: 4823640 24%, 4821150 13%, 4834320 13%, 4807710 11%, 4814280 9%, 4800209 7%, 4820250 7%, 4800207 4%, 4800016 4%, 4826190 4%, 4813590 2%, 4800020 2%

SHELTER_ID: NOT AVAILABLE 95%, nan 2%, 11548754 2%, 11548760 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 55 | 0 | 55 1; 54 1; 53 1; 52 1 |
| NCESID | other | 54 | 0 | 4813590 1; 480771012521 1; 480771000057 1; 480020909503 1 |
| NAME | who | 54 | 0 | Channelview High School 1; HALL SUCCESS ACADEMY 1; ALDINE H S 1; YES PREP - NORTH CENTRAL 1 |
| ADDRESS | other | 55 | 0 | 1100 Sheldon Rd 1; 15014 ALDINE WESTFIELD 1; 11101 AIRLINE DR 1; 13703 ALDINE WESTFIELD RD 1 |
| CITY | category | 12 | 0 | HOUSTON 33; PASADENA 7; BAYTOWN 5; LA PORTE 2 |
| STATE | other | 1 | 0 | TX 55 |
| ZIP | category | 33 | 0 | 77049 4; 77039 3; 77076 3; 77520 3 |
| ZIP4 | category | 27 | 0 | NOT AVAILABLE 27; 2305 2; 6496 2; 3518 1 |
| TELEPHONE | other | 55 | 0 | (281) 452-8002 1; (281) 985-7446 1; (281) 448-5231 1; (713) 967-8800 1 |
| TYPE | category | 3 | 0 | 1 36; 4 18; nan 1 |
| STATUS | category | 2 | 0 | 1 54; nan 1 |
| POPULATION | amount | 54 | 0 | 383.0 2; nan 1; 213.0 1; 2803.0 1 |
| COUNTY | who | 1 | 0 | HARRIS 55 |
| COUNTYFIPS | other | 1 | 0 | 48201 55 |
| COUNTRY | category | 2 | 0 | USA 54; US 1 |
| LATITUDE | amount | 55 | 0 | nan 1; 29.9363791 1; 29.9170766 1; 29.9142901 1 |
| LONGITUDE | amount | 55 | 0 | nan 1; -95.3552656 1; -95.4087653 1; -95.3561581 1 |
| NAICS_CODE | other | 1 | 0 | 611110 55 |
| NAICS_DESC | who | 1 | 0 | ELEMENTARY AND SECONDARY  55 |
| SOURCE | other | 54 | 0 | nan 1; https://nces.ed.gov/ccd/s 1; https://nces.ed.gov/ccd/s 1; https://nces.ed.gov/ccd/s 1 |
| SOURCE_DAT | category | 2 | 0 | 1706680800000.0 54; nan 1 |
| VAL_METHOD | category | 4 | 0 | IMAGERY/OTHER 39; IMAGERY 11; GEOCODE 4; nan 1 |
| VAL_DATE | date | 33 | 0 | 1652335200000.0 6; 1509343200000.0 4; 1540274400000.0 3; 1369634400000.0 3 |
| WEBSITE | category | 22 | 0 | NOT AVAILABLE 15; http://www.houstonisd.org 11; http://www.aldineisd.org 5; http://www.ccisd.net 4 |
| LEVEL | other | 1 | 0 | HIGH 55 |
| ENROLLMENT | other | 54 | 0 | 452 2; 2903 1; 193 1; 2663 1 |
| ST_GRADE | category | 6 | 0 | 09 43; 06 5; 08 3; 07 2 |
| END_GRADE | other | 1 | 0 | 12 55 |
| DISTRICTID | category | 21 | 0 | 4823640 11; 4821150 6; 4834320 6; 4807710 5 |
| FT_TEACHER | amount | 42 | 0 | nan 4; 25.0 3; 22.0 3; 140.0 2 |
| SHELTER_ID | category | 4 | 0 | NOT AVAILABLE 52; nan 1; 11548754 1; 11548760 1 |
| VAILD | empty | 1 | 55 |  |
| GEOMETRY | other | 55 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:29.19847 55 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3ed7c967-2e93-41fc-b733-8 55 |
| SRC_SHA256 | who | 1 | 0 | eaaf9eab4fa7f36f46e9496db 55 |
