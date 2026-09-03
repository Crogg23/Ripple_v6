# PORTAL_SOC_UTAH_OPEN_DATA_P_8DE28DA9D9

rows 1.4K  columns 33  scan 5.0s

roles: amount 4, audit 2, category 10, date 3, id 3, other 7, who 5

## when

SOURCEDATE
  2014       380  ##############################
  2015       304  ########################
  2016       123  ##########
  2017       213  #################
  2018       236  ###################
  2019       165  #############

VAL_DATE
  2014       380  ##############################
  2015       304  ########################
  2016       123  ##########
  2017       213  #################
  2018       236  ###################
  2019       165  #############

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 1.4K | 37 | 40.49 | 41.88 | 42.18 | 56.8K |
| LONGITUDE | 1.4K | -114.05 | -111.93 | -109.28 | -109.10 | -159.0K |
| MAX_VOLT | 1.4K | -1000.0K | 115 | 345 | 500 | -71.85M |
| MIN_VOLT | 1.4K | -1000.0K | 69 | 230 | 345 | -71.88M |

## who

NAME by rows
        28  DEAD HEAD
         2  RED ROCK
         2  ST GEORGE
         1  US GYPSUM
         1  UNKNOWN206674
         1  UNKNOWN208005
         1  UNKNOWN206757
         1  TAP205508
         1  TAP207942
         1  TAP205250
         1  TAP208877
         1  UNKNOWN201743
         1  TAP207433
         1  UNKNOWN206643
         1  TAP205506
         1  UNKNOWN209672
         1  UNKNOWN208856
         1  UNKNOWN201816
         1  UNKNOWN201696
         1  TAP206705

NAME by dollars
        1.1K       28 rows  DEAD HEAD
       74.28        2 rows  ST GEORGE
       74.13        2 rows  RED ROCK
       42.18        1 rows  TAP208025
       42.04        1 rows  TAP208019
       42.04        1 rows  UNKNOWN208022
       42.04        1 rows  TAP208021
       42.01        1 rows  UNKNOWN208020
       41.99        1 rows  UNKNOWN209702
       41.98        1 rows  UNKNOWN206143
       41.97        1 rows  CURLEW
       41.97        1 rows  UNKNOWN208018
       41.95        1 rows  UNKNOWN207243
       41.92        1 rows  UNKNOWN206233
       41.89        1 rows  TAP206393
       41.89        1 rows  TAP206392
       41.89        1 rows  UNKNOWN206394
       41.88        1 rows  UNKNOWN206395
       41.86        1 rows  UNKNOWN206777
       41.85        1 rows  UNKNOWN206390

NAICS_DESC by rows
      1.4K  ELECTRIC BULK POWER TRANSMISSION AND CONTROL

NAICS_DESC by dollars
       56.8K     1.4K rows  ELECTRIC BULK POWER TRANSMISSION AND CONTROL

STATUS by rows
      1.4K  IN SERVICE

STATUS by dollars
       56.8K     1.4K rows  IN SERVICE

CITY by rows
       602  NOT AVAILABLE
        97  SALT LAKE CITY
        48  ST GEORGE
        36  OGDEN
        24  PROVO
        23  WEST VALLEY CITY
        23  WEST JORDAN
        18  OREM
        17  BRIGHAM CITY
        17  SPANISH FORK
        15  MAGNA
        14  LOGAN
        14  SOUTH JORDAN
        14  HURRICANE
        13  TOOELE
        13  WASHINGTON
        13  SPRINGVILLE
        12  DELTA
        12  NEPHI
        11  LEHI

CITY by dollars
       24.0K      602 rows  NOT AVAILABLE
        4.0K       97 rows  SALT LAKE CITY
        1.8K       48 rows  ST GEORGE
        1.5K       36 rows  OGDEN
      965.69       24 rows  PROVO
      935.65       23 rows  WEST VALLEY CITY
      933.60       23 rows  WEST JORDAN
      725.48       18 rows  OREM
      705.66       17 rows  BRIGHAM CITY
      681.94       17 rows  SPANISH FORK
      611.23       15 rows  MAGNA
      584.50       14 rows  LOGAN
      567.74       14 rows  SOUTH JORDAN
      525.63       13 rows  TOOELE
      522.20       13 rows  SPRINGVILLE
      520.47       14 rows  HURRICANE
      482.65       13 rows  WASHINGTON
      476.43       12 rows  NEPHI
      473.35       12 rows  DELTA
      444.65       11 rows  LEHI

## who x when

NAME by VAL_DATE, dollars = LATITUDE
  CURLEW                                    2014:41.97
  DEAD HEAD                                 2016:185.48 2017:317.30 2018:39.34 2019:566.98
  RED ROCK                                  2015:37.02 2019:37.11
  ST GEORGE                                 2014:74.28
  TAP205250                                 2015:40.59
  TAP205506                                 2015:40.11
  TAP205508                                 2015:40.10
  TAP206705                                 2016:40.82
  TAP207433                                 2017:40.08
  TAP207942                                 2018:40.56
  TAP208019                                 2018:42.04
  TAP208021                                 2018:42.04
  TAP208025                                 2018:42.18
  TAP208877                                 2018:41.41
  UNKNOWN201696                             2014:40.65
  UNKNOWN201743                             2014:40.80
  UNKNOWN201816                             2014:37.59
  UNKNOWN206143                             2015:41.98
  UNKNOWN206643                             2016:37.70
  UNKNOWN206674                             2017:41.51
  UNKNOWN206757                             2017:39.52
  UNKNOWN207243                             2017:41.95
  UNKNOWN208005                             2018:40.66
  UNKNOWN208018                             2018:41.97
  UNKNOWN208020                             2018:42.01
  UNKNOWN208022                             2018:42.04
  UNKNOWN208856                             2018:39.82
  UNKNOWN209672                             2019:38.56
  UNKNOWN209702                             2019:41.99
  US GYPSUM                                 2017:38.84

NAICS_DESC by VAL_DATE, dollars = LATITUDE
  ELECTRIC BULK POWER TRANSMISSION AND CON  2014:15.3K 2015:12.3K 2016:4.8K 2017:8.4K 2018:9.5K 2019:6.6K

## what

COUNTY: SALT LAKE 31%, UTAH 14%, WASHINGTON 10%, WEBER 8%, DAVIS 7%, CARBON 6%, BOX ELDER 5%, CACHE 4%, TOOELE 4%, SAN JUAN 3%, JUAB 3%, BEAVER 3%

COUNTYFIPS: 49035 31%, 49049 14%, 49053 10%, 49057 8%, 49011 7%, 49007 6%, 49003 5%, 49005 4%, 49045 4%, 49037 3%, 49023 3%, 49001 3%

LINES: 3 35%, 1 32%, 2 20%, 0 5%, 4 3%, 5 1%, 6 1%, 7 1%, 9 1%, 8 0%, 11 0%, 12 0%

MAX_INFER: Y 80%, N 15%, NOT AVAILABLE 5%

MIN_INFER: Y 80%, N 15%, NOT AVAILABLE 5%

SOURCE: IMAGERY 78%, Company Map 12%, https://www.openstreetmap.org/ 9%, IMAGERY and FAA data 1%, http://geonames.usgs.gov/domes 0%, Delete? 0%, http://bpagis.maps.arcgis.com/ 0%

TYPE: SUBSTATION 62%, TAP 36%, DEAD END 2%

VAL_METHOD: IMAGERY 74%, IMAGERY/OTHER 25%, UNVERIFIED 1%

COMPUTED_REGION_5D9V_6BUI: 26 31%, 5 14%, 8 10%, 16 8%, 22 7%, 4 6%, 14 5%, 6 4%, 11 4%, 29 3%, 28 3%, 20 3%

COMPUTED_REGION_MI24_NG5Q: 29 31%, 19 14%, 15 10%, 4 8%, 23 7%, 28 6%, 11 5%, 12 4%, 9 4%, 5 3%, 18 3%, 10 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CITY | who | 153 | 0 | NOT AVAILABLE 602; SALT LAKE CITY 97; ST GEORGE 48; OGDEN 36 |
| COUNTRY | other | 1 | 0 | USA 1.4K |
| COUNTY | category | 32 | 0 | SALT LAKE 341; UTAH 156; WASHINGTON 110; WEBER 90 |
| COUNTYFIPS | category | 32 | 0 | 49035 341; 49049 156; 49053 110; 49057 90 |
| ID | id | 1.4K | 0 | 201689 8; 202608 8; 201630 8; 207485 8 |
| LATITUDE | amount | 1.4K | 0 | 40.5775433410001 8; 37.1997331810001 8; 40.368843993 8; 38.319670047 8 |
| LINES | category | 19 | 0 | 3 498; 1 448; 2 289; 0 72 |
| LONGITUDE | amount | 1.4K | 0 | -111.896239407 8; -113.602344136 8; -111.744432647 8; -111.382839883 8 |
| MAX_INFER | category | 3 | 0 | Y 1.1K; N 217; NOT AVAILABLE 72 |
| MAX_VOLT | amount | 16 | 0 | 69 487; 115 297; 138 296; 230 105 |
| MIN_INFER | category | 3 | 0 | Y 1.1K; N 207; NOT AVAILABLE 72 |
| MIN_VOLT | amount | 18 | 0 | 69 624; 115 273; 138 186; 46 173 |
| NAICS_CODE | other | 1 | 0 | 221121 1.4K |
| NAICS_DESC | who | 1 | 0 | ELECTRIC BULK POWER TRANS 1.4K |
| NAME | who | 1.4K | 0 | DEAD HEAD 28; UNKNOWN201689 7; LEDGES 7; UNKNOWN201630 7 |
| OBJECTID | id | 1.4K | 0 | 50072 8; 50956 8; 50013 8; 55746 8 |
| SOURCE | category | 7 | 0 | IMAGERY 1.1K; Company Map 165; https://www.openstreetmap 132; IMAGERY and FAA data 9 |
| SOURCEDATE | date | 198 | 0 | 2014-12-05T00:00:00.000Z 380; 2019-04-30T00:00:00.000Z 118; 2015-06-29T00:00:00.000Z 87; 2017-05-31T00:00:00.000Z 67 |
| STATE | other | 1 | 0 | UT 1.4K |
| STATUS | who | 1 | 0 | IN SERVICE 1.4K |
| TYPE | category | 3 | 0 | SUBSTATION 887; TAP 506; DEAD END 28 |
| VAL_DATE | date | 198 | 0 | 2014-12-05T00:00:00.000Z 380; 2019-04-30T00:00:00.000Z 118; 2015-06-29T00:00:00.000Z 87; 2017-05-31T00:00:00.000Z 67 |
| VAL_METHOD | category | 3 | 0 | IMAGERY 1.0K; IMAGERY/OTHER 352; UNVERIFIED 20 |
| ZIP | other | 169 | 0 | NOT AVAILABLE 537; 84116 39; 84404 28; 84770 25 |
| POINT | id | 1.4K | 0 | {"type": "Point", "coordi 8; {"type": "Point", "coordi 8; {"type": "Point", "coordi 8; {"type": "Point", "coordi 8 |
| COMPUTED_REGION_5D9V_6BUI | category | 30 | 0 | 26 341; 5 156; 8 110; 16 90 |
| COMPUTED_REGION_QMWN_IMPY | other | 135 | 0 | nan 628; 220 95; 159 56; 98 52 |
| COMPUTED_REGION_JDNU_JMST | other | 216 | 0 | 75 48; 80 36; 171 32; 141 32 |
| COMPUTED_REGION_2FPW_SWV9 | other | 65 | 0 | 55 95; 57 86; 37 80; 54 62 |
| COMPUTED_REGION_MI24_NG5Q | category | 30 | 0 | 29 341; 19 156; 15 110; 4 90 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:37:24.80696 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | bef82ad5-9ab0-47f9-b626-a 1.4K |
| SRC_SHA256 | who | 1 | 0 | 22f0b275642fdd1bc3cadeb88 1.4K |
