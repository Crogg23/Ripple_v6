# PORTAL_CKA_WESTERN_PENNSYLV_645F59A90F

rows 361  columns 57  scan 4.9s

roles: amount 10, audit 2, category 22, date 1, other 20, who 3

## when

INGESTED_AT
  2026       361  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 361 | 124.1K | 490.0K | 2.80M | 7.82M | 249.49M |
| SHAPE__LENGTH | 361 | 1.5K | 3.5K | 10.3K | 22.6K | 1.49M |
| ACRES | 361 | 49.01 | 484.58 | 1.7K | 1.7K | 204.0K |
| INTPTLAT10 | 361 | 40.37 | 40.45 | 40.49 | 40.49 | 14.6K |
| INTPTLON10 | 361 | -80.08 | -79.97 | -79.89 | -79.87 | -28.9K |
| LMPER2018 | 361 | 0 | 0.56 | 0.99 | 1 | 195.70 |

## who

TRACTCE10 by rows
         7  191800
         6  151700
         6  562300
         6  300100
         6  020100
         5  141400
         5  310200
         5  191600
         5  290400
         5  562400
         5  290200
         5  192000
         4  140100
         4  481000
         4  561600
         4  160800
         4  010300
         4  563000
         4  110200
         4  111300

TRACTCE10 by dollars
      11.58M        3 rows  562900
       6.77M        4 rows  563000
       5.37M        6 rows  562300
       4.73M        3 rows  563100
       4.39M        5 rows  310200
       4.33M        4 rows  202300
       4.18M        5 rows  191600
       3.61M        4 rows  562600
       3.55M        1 rows  310300
       3.49M        5 rows  141400
       3.48M        4 rows  562500
       3.29M        5 rows  562400
       3.21M        3 rows  191700
       3.04M        2 rows  562800
       2.87M        6 rows  020100
       2.83M        1 rows  981800
       2.82M        3 rows  262000
       2.79M        2 rows  191100
       2.78M        1 rows  980500
       2.77M        5 rows  290400

HOOD by rows
        15  Brookline
        14  Shadyside
        13  Squirrel Hill South
        13  Carrick
        10  Beechview
        10  Bloomfield
        10  Squirrel Hill North
         9  Mount Washington
         9  Greenfield
         8  East Liberty
         8  Highland Park
         7  South Side Slopes
         7  Point Breeze
         7  Hazelwood
         7  Brighton Heights
         6  Lincoln-Lemington-Belmar
         6  Knoxville
         6  Central Business District
         6  Central Lawrenceville
         6  Perry South

HOOD by dollars
      11.95M       13 rows  Squirrel Hill South
       9.30M       15 rows  Brookline
       8.11M        6 rows  Lincoln-Lemington-Belmar
       7.82M        1 rows  Hays
       7.48M       13 rows  Carrick
       7.08M        7 rows  Hazelwood
       6.53M       10 rows  Beechview
       5.62M        6 rows  Marshall-Shadeland
       5.47M       10 rows  Squirrel Hill North
       5.42M        6 rows  Perry North
       5.21M        8 rows  Highland Park
       5.10M        9 rows  Mount Washington
       5.01M        7 rows  Brighton Heights
       4.50M        7 rows  Point Breeze
       4.39M        5 rows  Lincoln Place
       4.33M        4 rows  Banksville
       4.32M        1 rows  Fairywood
       4.32M        6 rows  Central Lawrenceville
       4.19M        6 rows  South Side Flats
       4.12M       14 rows  Shadyside

SRC_SHA256 by rows
       361  967159ff3be00ea9500e06717c012170d6345e9f5b3602706d65b954c0b3f32c

SRC_SHA256 by dollars
     249.49M      361 rows  967159ff3be00ea9500e06717c012170d6345e9f5b3602706d65b954c0b3

## who x when

TRACTCE10 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  010300                                    2026:1.47M
  020100                                    2026:2.87M
  110200                                    2026:1.40M
  111300                                    2026:936.8K
  140100                                    2026:2.53M
  141400                                    2026:3.49M
  151700                                    2026:2.05M
  160800                                    2026:1.79M
  191600                                    2026:4.18M
  191700                                    2026:3.21M
  191800                                    2026:2.51M
  192000                                    2026:2.35M
  202300                                    2026:4.33M
  262000                                    2026:2.82M
  290200                                    2026:2.52M
  290400                                    2026:2.77M
  300100                                    2026:1.35M
  310200                                    2026:4.39M
  310300                                    2026:3.55M
  481000                                    2026:1.52M
  561600                                    2026:2.69M
  562300                                    2026:5.37M
  562400                                    2026:3.29M
  562500                                    2026:3.48M
  562600                                    2026:3.61M
  562800                                    2026:3.04M
  562900                                    2026:11.58M
  563000                                    2026:6.77M
  563100                                    2026:4.73M
  981800                                    2026:2.83M

HOOD by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Banksville                                2026:4.33M
  Beechview                                 2026:6.53M
  Bloomfield                                2026:3.14M
  Brighton Heights                          2026:5.01M
  Brookline                                 2026:9.30M
  Carrick                                   2026:7.48M
  Central Business District                 2026:2.87M
  Central Lawrenceville                     2026:4.32M
  East Liberty                              2026:2.60M
  Fairywood                                 2026:4.32M
  Greenfield                                2026:3.46M
  Hays                                      2026:7.82M
  Hazelwood                                 2026:7.08M
  Highland Park                             2026:5.21M
  Knoxville                                 2026:1.35M
  Lincoln Place                             2026:4.39M
  Lincoln-Lemington-Belmar                  2026:8.11M
  Marshall-Shadeland                        2026:5.62M
  Mount Washington                          2026:5.10M
  Perry North                               2026:5.42M
  Perry South                               2026:4.05M
  Point Breeze                              2026:4.50M
  Shadyside                                 2026:4.12M
  South Side Flats                          2026:4.19M
  South Side Slopes                         2026:3.21M
  Squirrel Hill North                       2026:5.47M
  Squirrel Hill South                       2026:11.95M

## what

CDBG2018: Yes 55%, No 45%

AWATER10: 0 96%, 854869 1%, 327616 1%, 158932 0%, 163596 0%, 275741 0%, 187348 0%, 225010 0%, 131921 0%, 6854 0%, 282865 0%, 8799 0%

BLKGRP2014: 1 38%, 2 30%, 3 17%, 4 8%, 5 3%, 0 1%, 6 1%, 7 0%

BLKGRP2018: 1 38%, 2 30%, 3 17%, 4 8%, 5 3%, 0 1%, 6 1%, 7 0%

BLKGRPCE10: 1 39%, 2 31%, 3 17%, 4 8%, 5 3%, 6 1%, 7 0%

CDBGNAME20: Pittsburgh 100%

CDBGNAME_1: Pittsburgh 100%

CDBGTY2014: 51 99%, 0 1%

CDBGTY2018: 51 99%, 0 1%

CDBGUOGI_1: 425529 99%, 0 1%

CDBGUOGID2: 425529 99%, 0 1%

COUNTY2014: 3 99%, 0 1%

COUNTY2018: 3 99%, 0 1%

COUNTYNA_1: Allegheny County 100%

COUNTYNAME: Allegheny County 100%

LOWMODPCT2: 1 58%, 0 42%

NAMELSAD10: Block Group 1 39%, Block Group 2 31%, Block Group 3 17%, Block Group 4 8%, Block Group 5 3%, Block Group 6 1%, Block Group 7 0%

SECTORS: 12 17%, 5 15%, 10 10%, 2 8%, 11 8%, 6 8%, 4 8%, 7 6%, 13 6%, 9 5%, 15 5%, 14 5%

STATE2014: 42 99%, 0 1%

STATE2018: 42 99%, 0 1%

STUSAB2014: PA 100%

STUSAB2018: PA 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CDBG2018 | category | 2 | 0 | Yes 200; No 161 |
| SHAPE__AREA | amount | 349 | 0 | 449306.59765625 2; 367390.70703125 2; 334907.17578125 2; 365601.8125 2 |
| SHAPE__LENGTH | amount | 360 | 0 | 3648.82858899818 2; 2623.61905295328 2; 2859.44583500715 2; 3380.55221733603 2 |
| ACRES | amount | 95 | 0 | 1338.669 15; 592.104 14; 1717.485 13; 1075.67 13 |
| ALAND10 | other | 347 | 0 | 1453388 3; 260030 2; 212675 2; 195227 2 |
| AWATER10 | category | 39 | 0 | 0 321; 854869 2; 327616 2; 158932 1 |
| BLKGRP2014 | category | 8 | 0 | 1 138; 2 110; 3 62; 4 28 |
| BLKGRP2018 | category | 8 | 0 | 1 138; 2 110; 3 62; 4 28 |
| BLKGRPCE10 | category | 7 | 0 | 1 140; 2 111; 3 63; 4 29 |
| CDBGNAME20 | category | 2 | 5 | Pittsburgh 356 |
| CDBGNAME_1 | category | 2 | 5 | Pittsburgh 356 |
| CDBGTY2014 | category | 2 | 0 | 51 356; 0 5 |
| CDBGTY2018 | category | 2 | 0 | 51 356; 0 5 |
| CDBGUOGI_1 | category | 2 | 0 | 425529 356; 0 5 |
| CDBGUOGID2 | category | 2 | 0 | 425529 356; 0 5 |
| CENSUSBLOC | other | 364 | 0 | 9809001 3; 4810004 2; 4810001 2; 4810003 2 |
| COUNTY2014 | category | 2 | 0 | 3 356; 0 5 |
| COUNTY2018 | category | 2 | 0 | 3 356; 0 5 |
| COUNTYFP10 | other | 1 | 0 | 003 361 |
| COUNTYNA_1 | category | 2 | 5 | Allegheny County 356 |
| COUNTYNAME | category | 2 | 5 | Allegheny County 356 |
| FUNCSTAT10 | other | 1 | 0 | S 361 |
| GEOID10 | other | 364 | 1 | 420034810004 2; 420034810001 2; 420034810003 2; 420034810002 2 |
| GEOID2014 | other | 357 | 0 | 0 6; 1608002 2; 1304001 2; 1005001 2 |
| GEOID2018 | other | 351 | 5 | 15000US420031608002 2; 15000US420031304001 2; 15000US420031005001 2; 15000US420031609001 2 |
| HOOD | who | 92 | 0 | Brookline 15; Shadyside 14; Squirrel Hill South 13; Carrick 13 |
| HOOD_NO | other | 91 | 0 | 14 15; 68 14; 77 13; 16 13 |
| HUDTRACTNU | other | 354 | 0 | 15000US420034810004 2; 15000US420034810001 2; 15000US420034810003 2; 15000US420034810002 2 |
| INTPTLAT10 | amount | 361 | 0 | 40.4659231 3; 40.4077982 2; 40.415885 2; 40.4100338 2 |
| INTPTLON10 | amount | 358 | 0 | -80.0458881 3; -79.9851751 2; -79.985154 2; -79.9884063 2 |
| LMPER2018 | amount | 81 | 0 | 0.0 19; 0.44999999 9; 0.60000002 9; 0.57999998 9 |
| LOWMOD2014 | other | 159 | 0 | 0 21; 325 8; 250 6; 445 6 |
| LOWMOD2018 | other | 155 | 0 | 0 19; 365 8; 465 7; 330 6 |
| LOWMODPC_1 | amount | 85 | 0 | 0.0 21; 0.47 11; 0.44 11; 0.63 10 |
| LOWMODPCT2 | category | 2 | 0 | 1 208; 0 153 |
| LOWMODUN_1 | other | 197 | 0 | 0 18; 440 6; 625 6; 850 6 |
| LOWMODUNIV | other | 205 | 0 | 0 18; 525 6; 530 6; 1040 5 |
| MTFCC10 | other | 1 | 0 | G5030 361 |
| NAMELSAD10 | category | 7 | 0 | Block Group 1 140; Block Group 2 111; Block Group 3 63; Block Group 4 29 |
| OBJECTID | other | 361 | 0 | 296 2; 295 2; 294 2; 280 2 |
| OBJECTID_1 | other | 361 | 0 | 361 2; 360 2; 359 2; 358 2 |
| SECTORS | category | 17 | 0 | 12 55; 5 47; 10 32; 2 25 |
| SQMILES | amount | 91 | 0 | 2.082 15; 0.921 14; 2.671 13; 1.673 13 |
| ST_AREA_SH | amount | 363 | 0 | 2800839.4192 2; 2289654.75704 2; 2087573.46585 2; 2278765.65211 2 |
| ST_LENGTH | amount | 365 | 0 | 9112.32749307 2; 6550.10727907 2; 7136.43464388 2; 8438.62973558 2 |
| STATE2014 | category | 2 | 0 | 42 356; 0 5 |
| STATE2018 | category | 2 | 0 | 42 356; 0 5 |
| STATEFP10 | other | 1 | 0 | 42 361 |
| STUSAB2014 | category | 2 | 5 | PA 356 |
| STUSAB2018 | category | 2 | 5 | PA 356 |
| TRACT2014 | other | 138 | 0 | 191800 7; 562300 6; 151700 6; 300100 6 |
| TRACT2018 | other | 138 | 0 | 191800 7; 562300 6; 151700 6; 300100 6 |
| TRACTCE10 | who | 136 | 0 | 191800 7; 562300 6; 151700 6; 300100 6 |
| GEOMETRY | other | 360 | 0 | POLYGON ((586251.12041445 2; POLYGON ((586021.30147166 2; POLYGON ((585813.63475754 2; POLYGON ((585877.43561052 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:40:11.45646 361 |
| SOURCE_RUN_ID | audit | 1 | 0 | f95abcfe-395b-47fb-8e6b-3 361 |
| SRC_SHA256 | who | 1 | 0 | 967159ff3be00ea9500e06717 361 |
