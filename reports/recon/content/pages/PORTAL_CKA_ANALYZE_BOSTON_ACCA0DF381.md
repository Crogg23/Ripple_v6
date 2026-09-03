# PORTAL_CKA_ANALYZE_BOSTON_ACCA0DF381

rows 3.8K  columns 34  scan 5.1s

roles: amount 1, audit 2, category 21, date 2, empty 1, id 1, other 2, who 5

## when

TIMESTAMP
  2012      2.4K  ##############################
  2013       270  ###
  2014       151  ##
  2015       146  ##
  2016       181  ##
  2017       169  ##
  2018        46  #
  2019        60  #
  2020        97  #
  2021        47  #
  2022        57  #
  2023        66  #
  2024        60  #
  2025        21  
  2026        18  

INGESTED_AT
  2026      3.8K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MILES | 3.8K | -0.09 | 0.14 | 1.20 | 4.76 | 811.27 |

## who

ST_NAME by rows
        49  Washington St
        21  Columbia Rd
        19  Commonwealth Ave
        14  Columbus Ave
        14  Dorchester Ave
        14  Boylston St
        14  River St
        13  Tremont St
        13  Dartmouth St
        13  Shawmut Ave
        12  Linden St
        12  Massachusetts Ave
        11  Beacon St
        11  Centre St
        11  Summer St
        11  High St
        10  Adams St
        10  Putnam St
        10  Bartlett St
        10  Harrison Ave

ST_NAME by dollars
       33.24       19 rows  Commonwealth Ave
       33.09       49 rows  Washington St
       12.23       12 rows  Massachusetts Ave
       11.93       14 rows  Dorchester Ave
       11.47        9 rows  Blue Hill Ave
       10.37        7 rows  Morton St
        9.73       14 rows  River St
        7.98       21 rows  Columbia Rd
        6.77        6 rows  Huntington Ave
        6.06       14 rows  Columbus Ave
        5.64       11 rows  Beacon St
        5.58       13 rows  Tremont St
        5.34        8 rows  Cambridge St
        4.91        4 rows  Gallivan Blvd
        4.31        8 rows  Bennington St
        4.16       11 rows  Centre St
        3.92        4 rows  New Rutherford Ave
        3.86        5 rows  Saratoga St
        3.81       14 rows  Boylston St
        3.62        2 rows  William J Day Blvd

PARENT by rows
        29  WASHI1
        16  MASSA3
        13  SHAWM2
        13  DARTM2
        11  RIVER1
        11  DORCH1
        11  HARRI5
        10  COLUM15
        10  COMMO5
        10  WEST 18
        10  BOYLS6
         9  TREMO1
         9  WASHI5
         9  WASHI3
         9  BEACO1
         8  BROOK12
         8  PUTNA1
         8  TALBO1
         7  E BRO1
         7  DORCH3

PARENT by dollars
       23.17       29 rows  WASHI1
       22.58       10 rows  COMMO5
       12.95       16 rows  MASSA3
       11.69       11 rows  DORCH1
       10.37        7 rows  MORTO1
        9.49       11 rows  RIVER1
        8.87        6 rows  COMMO1
        6.77        6 rows  HUNTI1
        6.09        9 rows  WASHI5
        5.94        2 rows  BLUE 2
        4.91        4 rows  GALLI1
        4.54        9 rows  TREMO1
        3.92        5 rows  COLUM2
        3.92        4 rows  NEW R1
        3.86        5 rows  SARAT1
        3.62        2 rows  WILLI2
        3.55       11 rows  HARRI5
        3.50        9 rows  BEACO1
        3.35        9 rows  WASHI3
        3.34       13 rows  SHAWM2

C_TO by rows
       318  Dead End
        66  Columbia Rd
        64  Washington St
        62  Blue Hill Ave
        58  Tremont St
        44  Commonwealth Ave
        39  Medford St
        39  Dorchester Ave
        34  Columbus Ave
        31  Adams St
        30  Harvard St
        30  Boylston St
        27  Massachusetts Ave
        27  Morton St
        24  Norfolk St
        24  Bunker Hill St
        24  Shawmut Ave
        23  Quincy St
        22  Walnut Ave
        22  Faneuil St

C_TO by dollars
       32.46      318 rows  Dead End
       30.10       22 rows  Chestnut Hill Ave
       26.46       64 rows  Washington St
       24.40       66 rows  Columbia Rd
       23.89       62 rows  Blue Hill Ave
       16.91       27 rows  Massachusetts Ave
       10.85       39 rows  Dorchester Ave
       10.21       58 rows  Tremont St
        9.76       12 rows  River St
        8.85       31 rows  Adams St
        8.37       34 rows  Columbus Ave
        8.28       44 rows  Commonwealth Ave
        7.83       16 rows  Farragut Rd
        7.70       14 rows  South Huntington Ave
        7.66       21 rows  Dorchester St
        7.51       39 rows  Medford St
        7.22       27 rows  Morton St
        5.89        5 rows  Burnett St
        5.66       18 rows  Dudley St
        5.46       20 rows  Brookline Town Line

C_FROM by rows
       293  Washington St
       120  Blue Hill Ave
       120  Dorchester Ave
        78  Warren St
        69  Centre St
        68  Tremont St
        65  Commonwealth Ave
        51  Main St
        48  Columbia Rd
        46  Cambridge St
        42  Savin Hill Ave
        39  Morton St
        39  Columbus Ave
        38  Dorchester St
        37  Dudley St
        36  Shawmut Ave
        35  Bowdoin St
        35  River St
        32  Bunker Hill St
        32  Quincy St

C_FROM by dollars
       73.55      293 rows  Washington St
       30.68      120 rows  Blue Hill Ave
       27.59      120 rows  Dorchester Ave
       22.62       78 rows  Warren St
       19.21       16 rows  Arlington St
       16.44       37 rows  Dudley St
       15.89       65 rows  Commonwealth Ave
       15.80       68 rows  Tremont St
       14.91       69 rows  Centre St
       14.17        5 rows  Kenmore St
       11.23       39 rows  Morton St
        9.80       39 rows  Columbus Ave
        9.38       48 rows  Columbia Rd
        9.21       28 rows  Massachusetts Ave
        7.59       46 rows  Cambridge St
        7.09       22 rows  Brighton Av
        7.09       38 rows  Dorchester St
        7.06       22 rows  East Broadway
        6.98       32 rows  Quincy St
        6.92       13 rows  Summer St

## who x when

ST_NAME by TIMESTAMP, dollars = MILES
  Adams St                                  2012:1.84
  Bartlett St                               2012:0.90 2015:0.10 2021:0.16
  Beacon St                                 2012:5.01 2020:0.17 2021:0.46
  Bennington St                             2012:1.06 2016:2.03 2020:1.22
  Blue Hill Ave                             2012:3.23 2016:2.30 2026:5.94
  Boylston St                               2012:3.37 2016:0.44
  Cambridge St                              2012:2.06 2023:3.28
  Centre St                                 2012:3.52 2013:0 2025:0.64
  Columbia Rd                               2013:6.60 2014:1.38
  Columbus Ave                              2012:5.51 2017:0.55
  Commonwealth Ave                          2012:18.45 2013:0 2014:7.70 2015:0.68 2017:5.49 2021:0.92
  Dartmouth St                              2012:0.53 2015:0.44 2016:0.24 2017:0.36 2020:-0.09 2021:0.28
  Dorchester Ave                            2012:10.98 2016:0.95
  Gallivan Blvd                             2012:4.91
  Harrison Ave                              2012:0.97 2016:1.14 2020:0.32 2023:0.56
  High St                                   2012:1.38
  Huntington Ave                            2012:6.77
  Linden St                                 2012:1.38
  Massachusetts Ave                         2012:12.23
  Morton St                                 2012:10.37
  New Rutherford Ave                        2012:3.92
  Putnam St                                 2012:0.12 2015:0.40 2016:0.54
  River St                                  2012:9.61 2014:0.12
  Saratoga St                               2012:3.44 2020:0.42
  Shawmut Ave                               2012:2.26 2020:0.40 2022:0.68
  Summer St                                 2012:3.41
  Tremont St                                2012:2.13 2015:0.69 2016:2.16 2019:0.17 2021:0.43
  Washington St                             2012:27.17 2017:0.78 2020:1.45 2021:2.19 2023:0.72 2024:0.78
  William J Day Blvd                        2013:3.62

PARENT by TIMESTAMP, dollars = MILES
  BEACO1                                    2012:2.87 2020:0.17 2021:0.46
  BLUE 2                                    2026:5.94
  BOYLS6                                    2012:1.89 2016:0.44
  BROOK12                                   2012:0.66 2015:0.50
  COLUM15                                   2012:2.78 2017:0.36
  COLUM2                                    2013:3.92
  COMMO1                                    2012:2.75 2014:0.68 2015:0.68 2017:4.76
  COMMO5                                    2012:13.91 2014:7.02 2017:0.73 2021:0.92
  DARTM2                                    2012:0.53 2015:0.44 2016:0.24 2017:0.36 2020:-0.09 2021:0.28
  DORCH1                                    2012:10.74 2016:0.95
  DORCH3                                    2012:0.68 2026:1.26
  E BRO1                                    2012:2.36
  GALLI1                                    2012:4.91
  HARRI5                                    2012:0.97 2016:1.14 2020:0.32 2023:1.12
  HUNTI1                                    2012:6.77
  MASSA3                                    2012:12.95
  MORTO1                                    2012:10.37
  NEW R1                                    2012:3.92
  PUTNA1                                    2012:0 2015:0.40 2016:0.54
  RIVER1                                    2012:9.49
  SARAT1                                    2012:3.44 2020:0.42
  SHAWM2                                    2012:2.26 2020:0.40 2022:0.68
  TALBO1                                    2012:1.66 2021:1.18
  TREMO1                                    2012:2.13 2015:0.69 2016:1.12 2019:0.17 2021:0.43
  WASHI1                                    2012:20.89 2017:0.78 2023:0.72 2024:0.78
  WASHI3                                    2012:2.29 2021:1.06
  WASHI5                                    2012:3.51 2020:1.45 2021:1.13
  WEST 18                                   2012:0.54 2020:0.88 2022:0.46
  WILLI2                                    2013:3.62

## what

DIST: 3 22%, 7 16%, 10R 11%, 4 9%, 2 9%, 5 8%, 1C 7%, 1S 6%, 9 6%, 1B 3%, 10M 3%, 1N 2%

DIST_NAME: North Dorchester 22%, South Dorchester 16%, Roxbury 11%, Allston/Brighton 9%, Jamaica Plain 8%, South Boston 8%, Charlestown 7%, South End 6%, East Boston 6%, Back Bay 3%, Mission Hill 3%, North End 2%

START_TIME: 08:00 45%, 12:00 37%, 00:01 8%, 09:00 4%, 13:00 3%, 05:00 1%, 00:00 1%, 06:00 1%, 02:00 0%

END_TIME: 12:00 45%, 16:00 36%, 07:00 10%, 13:00 4%, 17:00 3%, 08:00 1%, 15:00 0%, 04:00 0%, 00:00 0%, 06:00 0%, 01:00 0%

SIDE: Odd 49%, Even 49%, Even Side Median 1%, Odd Side Median 0%, Outbound 0%, Both 0%, Inbound 0%, Median 0%, Residential 0%, Ramp 0%, Ext 0%

ONE_WAY: f 94%, t 6%

WEEK_1: t 56%, f 44%

WEEK_2: t 56%, f 44%

WEEK_3: t 56%, f 44%

WEEK_4: t 55%, f 45%

WEEK_5: f 85%, t 15%

SUNDAY: f 94%, t 6%

MONDAY: f 83%, t 17%

TUESDAY: f 76%, t 24%

WEDNESDAY: f 71%, t 29%

THURSDAY: f 70%, t 30%

FRIDAY: f 76%, t 24%

SATURDAY: f 94%, t 6%

EVERY_DAY: f 94%, t 6%

YEAR_ROUND: f 90%, t 10%

NORTH_END_PILOT: f 91%, t 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MAIN_ID | id | 3.7K | 0 | 3899 19; 3898 19; 3897 19; 3896 19 |
| ST_NAME | who | 1.5K | 0 | Washington St 61; Columbia Rd 30; Commonwealth Ave 24; Tremont St 23 |
| DIST | category | 25 | 3 | 3 727; 7 521; 10R 352; 4 300 |
| DIST_NAME | category | 22 | 13 | North Dorchester 727; South Dorchester 521; Roxbury 382; Allston/Brighton 300 |
| START_TIME | category | 9 | 0 | 08:00 1.7K; 12:00 1.4K; 00:01 301; 09:00 147 |
| END_TIME | category | 11 | 0 | 12:00 1.7K; 16:00 1.4K; 07:00 382; 13:00 144 |
| SIDE | category | 21 | 198 | Odd 1.8K; Even 1.7K; Even Side Median 26; Odd Side Median 14 |
| C_FROM | who | 606 | 3 | Washington St 293; Blue Hill Ave 120; Dorchester Ave 120; Warren St 78 |
| C_TO | who | 711 | 3 | Dead End 318; Columbia Rd 66; Washington St 64; Blue Hill Ave 62 |
| MILES | amount | 1.4K | 0 | 0 169; 0.07859848484 20; 0.0365530303 20; 0.11666666666 20 |
| SECTION | empty | 1 | 3.8K |  |
| ONE_WAY | category | 2 | 0 | f 3.5K; t 215 |
| WEEK_1 | category | 2 | 0 | t 2.1K; f 1.6K |
| WEEK_2 | category | 2 | 0 | t 2.1K; f 1.7K |
| WEEK_3 | category | 2 | 0 | t 2.1K; f 1.6K |
| WEEK_4 | category | 2 | 0 | t 2.1K; f 1.7K |
| WEEK_5 | category | 2 | 0 | f 3.2K; t 579 |
| SUNDAY | category | 2 | 0 | f 3.5K; t 226 |
| MONDAY | category | 2 | 0 | f 3.1K; t 635 |
| TUESDAY | category | 2 | 0 | f 2.9K; t 896 |
| WEDNESDAY | category | 2 | 0 | f 2.7K; t 1.1K |
| THURSDAY | category | 2 | 0 | f 2.6K; t 1.1K |
| FRIDAY | category | 2 | 0 | f 2.9K; t 904 |
| SATURDAY | category | 2 | 0 | f 3.5K; t 227 |
| EVERY_DAY | category | 2 | 0 | f 3.5K; t 226 |
| YEAR_ROUND | category | 2 | 0 | f 3.4K; t 361 |
| NORTH_END_PILOT | category | 2 | 0 | f 3.4K; t 333 |
| TIMESTAMP | date | 1.4K | 0 | 2012-02-14 13:36:32+00 1.8K; 2012-02-29 15:06:53+00 495; 2024-08-22 12:49:22+00 9; 2026-02-20 20:56:14+00 8 |
| PARENT | who | 1.6K | 127 | WASHI1 41; MASSA3 24; SHAWM2 23; WEST 18 22 |
| LOSTA | other | 405 | 6 | 0 3.0K; 2145 6; 1163 6; 611 6 |
| HISTA | other | 1.4K | 6 | 0 134; 616 21; 415 20; 193 20 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:31:53.09814 3.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | c89e9dc6-9cd2-489b-a2c3-3 3.8K |
| SRC_SHA256 | who | 1 | 0 | a487522fbab79df6bc8647972 3.8K |
