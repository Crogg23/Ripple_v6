# PORTAL_CKA_WPRDC_ALLEGHENY_8E6BDE379C

rows 420  columns 28  scan 4.9s

roles: amount 5, audit 2, category 10, date 3, other 6, who 3

## when

COUNT_START_DATE
  2017         4  #
  2018        37  ########
  2019       140  ##############################
  2020       108  #######################
  2021        78  #################

COUNT_END_DATE
  2018        28  #######
  2019       127  ##############################
  2020       113  ###########################
  2021        67  ################

INGESTED_AT
  2026       420  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MEDIAN_SPEED | 298 | 14 | 26 | 38.03 | 43 | 7.7K |
| SPEED85_PERCENT | 301 | 17 | 30 | 45 | 50 | 9.2K |
| SPEED95_PERCENT | 291 | 19.80 | 34 | 50 | 95 | 10.0K |
| LONGITUDE | 419 | -80.08 | -79.96 | -79.88 | -79.87 | -33.5K |
| LATITUDE | 419 | 40.37 | 40.45 | 40.49 | 40.50 | 16.9K |

## who

TRACT by rows
        12  42003130300
        12  42003190300
        11  42003020300
        11  42003210700
        10  42003111300
        10  42003141300
         9  42003080900
         9  42003110200
         9  42003120800
         8  42003101400
         8  42003070900
         8  42003010300
         8  42003140800
         8  42003141400
         8  42003290400
         7  42003260200
         7  42003130600
         7  42003060500
         7  42003140300
         7  42003151700

TRACT by dollars
      -79.89        1 rows  42003130100
      -79.89        1 rows  42003130400
      -79.90        1 rows  42003141100
      -79.90        1 rows  42003141000
      -79.91        1 rows  42003980300
      -79.92        1 rows  42003980100
      -79.92        1 rows  42003310200
      -79.92        1 rows  42003310300
      -79.93        1 rows  42003140200
      -79.93        1 rows  42003980500
      -79.95        1 rows  42003040600
      -79.96        1 rows  42003101100
      -79.97        1 rows  42003050100
      -79.98        1 rows  42003170200
      -79.98        1 rows  42003030500
      -79.98        1 rows  42003240600
      -79.98        1 rows  42003290200
      -79.99        1 rows  42003241200
      -79.99        1 rows  42003320400
      -79.99        1 rows  42003290100

NEIGHBORHOOD by rows
        28  Squirrel Hill South
        21  Bloomfield
        18  Shadyside
        16  Mount Washington
        16  Highland Park
        16  East Liberty
        14  Perry North
        12  Squirrel Hill North
        12  Homewood South
        12  Point Breeze
        12  Brookline
        11  Strip District
        11  South Side Slopes
        11  Larimer
        10  Manchester
        10  Carrick
         8  North Oakland
         8  Central Oakland
         8  Morningside
         8  Bluff

NEIGHBORHOOD by dollars
      -79.90        1 rows  Swisshelm Park
      -79.90        1 rows  Regent Square
      -79.92        1 rows  Lincoln Place
      -79.92        1 rows  New Homestead
      -79.96        1 rows  Upper Lawrenceville
      -79.97        1 rows  Middle Hill
      -79.98        1 rows  Troy Hill
      -79.98        1 rows  Crawford-Roberts
      -79.99        1 rows  Spring Garden
         -80        1 rows  East Allegheny
      -80.01        1 rows  Fineview
      -80.01        1 rows  Allegheny Center
      -80.02        1 rows  Allegheny West
      -80.02        1 rows  Duquesne Heights
      -80.02        1 rows  Chateau
      -80.04        1 rows  Banksville
      -80.05        1 rows  Crafton Heights
      -80.07        1 rows  Oakwood
      -80.07        1 rows  Chartiers City
     -159.79        2 rows  Point Breeze North

SRC_SHA256 by rows
       420  b506a182c7e723e687d43460e28457623d6afe0063006ade7c8bf1ba323cac33

SRC_SHA256 by dollars
      -33.5K      420 rows  b506a182c7e723e687d43460e28457623d6afe0063006ade7c8bf1ba323c

## who x when

TRACT by COUNT_START_DATE, dollars = LONGITUDE
  42003010300                               2018:-159.99 2019:-479.88
  42003020300                               2017:-79.99 2018:-79.98 2019:-239.93 2020:-79.97
  42003060500                               2018:-79.96 2019:-319.85 2020:-159.92
  42003070900                               2019:-239.82 2020:-159.89 2021:-159.88
  42003080900                               2019:-79.95 2020:-479.69
  42003101400                               2018:-159.86 2019:-159.86 2021:-319.71
  42003110200                               2018:-79.92 2020:-559.44 2021:-79.92
  42003111300                               2018:-239.79 2019:-319.71 2020:-79.92 2021:-79.93
  42003120800                               2018:-79.92 2019:-479.46 2020:-79.92 2021:-79.91
  42003130100                               2021:-79.89
  42003130300                               2020:-719.06 2021:-239.69
  42003130400                               2020:-79.89
  42003130600                               2019:-79.88 2021:-479.25
  42003140200                               2019:-79.93
  42003140300                               2019:-399.61 2021:-79.92
  42003140800                               2018:-159.82 2019:-159.83 2020:-79.91 2021:-239.76
  42003141000                               2019:-79.90
  42003141300                               2018:-79.93 2019:-159.86 2020:-159.84 2021:-399.65
  42003141400                               2019:-239.78 2020:-319.67 2021:-79.92
  42003151700                               2018:-159.86 2019:-79.93 2020:-79.93 2021:-79.93
  42003190300                               2018:-80.01 2019:-320.05 2021:-80.01
  42003210700                               2019:-320.10 2020:-320.11 2021:-240.07
  42003260200                               2019:-80.01 2020:-240.04
  42003290400                               2019:-159.98 2020:-399.93 2021:-79.99
  42003310200                               2020:-79.92
  42003310300                               2020:-79.92
  42003980100                               2018:-79.92
  42003980300                               2019:-79.91
  42003980500                               2019:-79.93

NEIGHBORHOOD by COUNT_START_DATE, dollars = LONGITUDE
  Bloomfield                                2017:-79.95 2019:-559.62 2020:-559.64 2021:-239.83
  Bluff                                     2018:-159.99 2019:-479.88
  Brookline                                 2019:-400.07 2020:-320.05 2021:-240.07
  Carrick                                   2019:-159.98 2020:-559.90 2021:-79.99
  Central Oakland                           2017:-79.96 2018:-159.91 2019:-159.91 2021:-159.91
  Crawford-Roberts                          2021:-79.98
  East Allegheny                            2019:-80
  East Liberty                              2018:-319.72 2019:-479.56 2020:-159.84 2021:-79.93
  Highland Park                             2018:-159.84 2019:-479.52 2020:-559.44 2021:-79.92
  Homewood South                            2020:-719.05 2021:-239.69
  Larimer                                   2018:-79.92 2019:-479.46 2020:-159.83 2021:-159.82
  Lincoln Place                             2020:-79.92
  Manchester                                2019:-320.10 2020:-240.08 2021:-240.07
  Middle Hill                               2021:-79.97
  Morningside                               2018:-159.86 2019:-159.86 2021:-319.71
  Mount Washington                          2018:-160.02 2019:-400.06 2020:-80 2021:-160.01
  New Homestead                             2020:-79.92
  North Oakland                             2018:-239.85 2019:-319.82 2020:-79.96
  Perry North                               2019:-160.02 2020:-560.08
  Point Breeze                              2018:-79.91 2019:-319.62 2020:-399.54 2021:-79.92
  Regent Square                             2019:-79.90
  Shadyside                                 2019:-639.46 2020:-159.89 2021:-559.54
  South Side Slopes                         2019:-79.98 2020:-319.91 2021:-319.89
  Spring Garden                             2020:-79.99
  Squirrel Hill North                       2018:-79.94 2019:-719.36 2021:-79.92
  Squirrel Hill South                       2018:-239.75 2019:-719.31 2020:-559.42 2021:-719.33
  Strip District                            2017:-79.99 2018:-79.98 2019:-239.93 2020:-79.97

## what

AVERAGE_DAILY_BIKE_TRAFFIC: 892 14%, 1278 14%, 102 14%, 88 14%, 954 14%, 198 14%, 2063 14%

COUNTER_NUMBER: 2 17%, 4 16%, 3 16%, 1 16%, 5 15%, 6 12%, 11 3%, 13 2%, 12 2%, 14 2%, #2 1%

COUNTER_TYPE: StatTrak 93%, Intersection Study 5%, Tube 2%

SPEED_LIMIT: 25 95%, 35 3%, 15 1%, 30 0%, 20 0%

MAX_SPEED: 56 16%, 51 11%, 59 11%, 57 9%, 67 9%, 64 9%, 61 9%, 63 7%, 48 7%, 58 7%, 49 7%

COUNCIL_DISTRICT: 7 18%, 9 16%, 6 11%, 5 11%, 1 10%, 8 9%, 3 9%, 2 8%, 4 7%

WARD: 14 20%, 19 11%, 11 10%, 26 8%, 13 8%, 8 8%, 4 8%, 7 6%, 12 6%, 6 5%, 21 5%, 10 5%

PUBLIC_WORKS_DIVISION: 2 33%, 3 32%, 1 15%, 5 15%, 6 5%

PLI_DIVISION: 14 20%, 19 11%, 11 10%, 26 8%, 13 8%, 8 8%, 4 8%, 7 6%, 12 6%, 6 5%, 21 5%, 10 5%

POLICE_ZONE: 4 26%, 5 25%, 1 16%, 3 13%, 2 11%, 6 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 420 | 0 | 1814538648 3; 704127706 3; 1329604877 3; 1037219067 3 |
| DEVICE_ID | other | 415 | 0 | 438 3; 437 3; 436 3; 435 3 |
| RECORD_OID | other | 372 | 45 | 1741898762 2; 1832664152 2; 1001258944 2; 1965316306 2 |
| COUNT_START_DATE | date | 126 | 53 | 2020-02-14 12; 2019-11-14 7; 2021-06-15 6; 2021-06-03 6 |
| COUNT_END_DATE | date | 108 | 85 | 2020-02-22 12; 2021-07-07 8; 2019-12-24 7; 2021-06-23 6 |
| AVERAGE_DAILY_CAR_TRAFFIC | other | 273 | 134 | 317 3; 3454 2; 271 2; 910 2 |
| AVERAGE_DAILY_BIKE_TRAFFIC | category | 8 | 413 | 892 1; 1278 1; 102 1; 88 1 |
| COUNTER_NUMBER | category | 26 | 152 | 2 41; 4 38; 3 38; 1 38 |
| COUNTER_TYPE | category | 4 | 56 | StatTrak 338; Intersection Study 19; Tube 7 |
| SPEED_LIMIT | category | 6 | 159 | 25 247; 35 9; 15 3; 30 1 |
| MAX_SPEED | category | 45 | 329 | 56 7; 51 5; 59 5; 57 4 |
| MEDIAN_SPEED | amount | 31 | 122 | 21.0 29; 29.0 24; 23.0 23; 28.0 23 |
| PERCENT_OVER_LIMIT | other | 90 | 179 | 97 7; 21 6; 73 5; 14 5 |
| SPEED85_PERCENT | amount | 31 | 119 | 27.0 27; 29.0 26; 32.0 22; 33.0 19 |
| SPEED95_PERCENT | amount | 37 | 129 | 32.0 29; 33.0 21; 36.0 20; 37.0 19 |
| LONGITUDE | amount | 422 | 1 | -79.98065059 3; -79.96677427 3; -79.96037954 3; -80.03777058 3 |
| LATITUDE | amount | 413 | 1 | 40.44082605 3; 40.45014681 3; 40.4550574 3; 40.48255664 3 |
| NEIGHBORHOOD | who | 76 | 2 | Squirrel Hill South 28; Bloomfield 21; Shadyside 18; Mount Washington 16 |
| COUNCIL_DISTRICT | category | 10 | 2 | 7 77; 9 66; 6 47; 5 47 |
| WARD | category | 33 | 1 | 14 56; 19 30; 11 28; 26 23 |
| TRACT | who | 122 | 0 | 42003190300 12; 42003130300 12; 42003210700 11; 42003020300 11 |
| PUBLIC_WORKS_DIVISION | category | 6 | 1 | 2 137; 3 134; 1 64; 5 62 |
| PLI_DIVISION | category | 33 | 1 | 14 56; 19 30; 11 28; 26 23 |
| POLICE_ZONE | category | 7 | 2 | 4 110; 5 105; 1 67; 3 55 |
| FIRE_ZONE | other | 85 | 1 | 2-21 22; 3-17 20; 3-9 17; 1-15 15 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:41:46.55510 420 |
| SOURCE_RUN_ID | audit | 1 | 0 | be09b3f2-94a0-498b-91b5-5 420 |
| SRC_SHA256 | who | 1 | 0 | b506a182c7e723e687d43460e 420 |
