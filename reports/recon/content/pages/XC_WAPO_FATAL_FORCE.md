# XC_WAPO_FATAL_FORCE

rows 10.4K  columns 22  scan 4.6s

roles: amount 2, audit 2, category 9, date 1, id 1, other 1, state 1, who 5

## when

DATE
  2015       995  #########################
  2016       959  ########################
  2017       984  #########################
  2018       992  #########################
  2019       993  #########################
  2020      1.0K  ##########################
  2021      1.1K  ###########################
  2022      1.1K  ############################
  2023      1.2K  ##############################
  2024      1.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 9.3K | 19.50 | 36.06 | 47.89 | 71.30 | 340.3K |
| LONGITUDE | 9.3K | -160.01 | -94.19 | -71.36 | -67.87 | -899.7K |

## who

NAME by rows
         5  Michael Johnson
         2  Isaias Garcia
         2  Jeffrey Sims
         2  Robert Edwards
         2  Richard Ruiz
         2  Brandon Evans
         2  Eduardo Munoz
         2  Mark Anthony Sanchez
         2  Robert Musser
         2  Eric Harris
         2  Jose Moreno
         2  Robert Anderson
         2  Tyler Hodge
         2  Justin Roberts
         2  Gabriel Parker
         2  Michael Ferguson
         2  Anthony Nunez
         2  Brandon Jones
         2  Robert Miller
         2  Joseph Garcia

NAME by dollars
      122.01        5 rows  Michael Johnson
       94.53        2 rows  Robert Musser
       88.01        2 rows  Malik Williams
       85.27        2 rows  James Anderson
       82.41        2 rows  Joseph Santos
       81.15        2 rows  Robert Anderson
       81.13        2 rows  Brandon Jones
       80.59        2 rows  James Williams
       79.95        2 rows  Curtis Smith
       77.76        2 rows  Anthony Gomez
       77.01        2 rows  Jeffrey Sims
       75.95        2 rows  Justin Anderson
       75.94        2 rows  Daniel Rivera
       75.74        2 rows  Michael Brown
       74.37        2 rows  Jason Smith
       73.16        2 rows  Jose Mendez
       72.99        2 rows  Robert Miller
       71.78        2 rows  Anthony Nunez
       71.65        2 rows  Tyler Hodge
       71.30        1 rows  Vincent Nageak III

AGENCY_IDS by rows
       143  38
       125  80
       114  20
        83  298
        83  102
        81  44
        75  375
        60  236
        58  19
        53  17
        53  265
        52  267
        50  508
        47  90
        46  219
        45  266
        45  141
        43  23
        43  130
        42  106

AGENCY_IDS by dollars
        4.4K      143 rows  38
        3.8K      125 rows  80
        3.7K      114 rows  20
        2.9K       83 rows  298
        2.5K       75 rows  375
        2.4K       83 rows  102
        2.2K       81 rows  44
        2.1K       53 rows  265
        1.8K       58 rows  19
        1.8K       60 rows  236
        1.7K       47 rows  90
        1.7K       52 rows  267
        1.6K       42 rows  106
        1.6K       50 rows  508
        1.5K       53 rows  17
        1.5K       45 rows  266
        1.5K       39 rows  77
        1.5K       39 rows  671
        1.4K       45 rows  141
        1.3K       43 rows  23

CITY by rows
       157  Los Angeles
       131  Phoenix
       126  Houston
       101  San Antonio
        87  Las Vegas
        77  Albuquerque
        63  Columbus
        60  Jacksonville
        57  Chicago
        57  Kansas City
        56  Denver
        54  Tucson
        52  Austin
        48  New York
        47  Miami
        47  Oklahoma City
        44  Indianapolis
        42  Philadelphia
        42  Tulsa
        41  St. Louis

CITY by dollars
        4.8K      157 rows  Los Angeles
        3.9K      131 rows  Phoenix
        3.6K      126 rows  Houston
        3.0K       87 rows  Las Vegas
        2.8K      101 rows  San Antonio
        2.5K       77 rows  Albuquerque
        2.3K       57 rows  Chicago
        2.2K       63 rows  Columbus
        2.2K       56 rows  Denver
        1.9K       57 rows  Kansas City
        1.7K       60 rows  Jacksonville
        1.7K       44 rows  Indianapolis
        1.6K       54 rows  Tucson
        1.6K       52 rows  Austin
        1.6K       42 rows  Philadelphia
        1.5K       48 rows  New York
        1.5K       41 rows  St. Louis
        1.5K       47 rows  Oklahoma City
        1.4K       41 rows  Bakersfield
        1.4K       42 rows  Tulsa

COUNTY by rows
       222  Los Angeles
       151  Maricopa
        97  Harris
        83  Orange
        79  San Bernardino
        79  Jefferson
        73  Clark
        65  Washington
        64  Bexar
        60  Marion
        59  Riverside
        57  Franklin
        55  San Diego
        54  Jackson
        52  Dallas
        49  Miami-Dade
        49  Cook
        49  Montgomery
        44  Bernalillo
        42  Tarrant

COUNTY by dollars
        7.5K      222 rows  Los Angeles
        5.0K      151 rows  Maricopa
        2.8K       97 rows  Harris
        2.7K       79 rows  Jefferson
        2.7K       73 rows  Clark
        2.6K       79 rows  San Bernardino
        2.6K       83 rows  Orange
        2.5K       65 rows  Washington
        2.2K       60 rows  Marion
        2.2K       57 rows  Franklin
        2.0K       49 rows  Cook
        2.0K       54 rows  Jackson
        1.9K       59 rows  Riverside
        1.9K       64 rows  Bexar
        1.8K       55 rows  San Diego
        1.7K       52 rows  Dallas
        1.6K       49 rows  Montgomery
        1.5K       44 rows  Bernalillo
        1.4K       37 rows  Adams
        1.4K       30 rows  King

## who x when

NAME by DATE, dollars = LATITUDE
  Anthony Gomez                             2015:40.04 2019:37.72
  Anthony Nunez                             2016:37.37 2022:34.41
  Brandon Evans                             2020:1 2024:33.35
  Brandon Jones                             2015:41.53 2016:39.60
  Curtis Smith                              2015:39.96 2023:39.99
  Daniel Rivera                             2022:40.83 2023:35.11
  Eduardo Munoz                             2019:63.45
  Eric Harris                               2015:36.18 2016:29.94
  Gabriel Parker                            2016:32.88 2021:33.80
  Isaias Garcia                             2023:31.19
  James Anderson                            2015:41.90 2021:43.37
  James Williams                            2021:39.80 2022:40.79
  Jason Smith                               2015:40.03 2022:34.34
  Jeffrey Sims                              2016:28.90 2018:48.11
  Jose Moreno                               2020:33.41 2024:34.07
  Joseph Garcia                             2016:35.72 2024:29.43
  Joseph Santos                             2017:41.83 2018:40.58
  Justin Anderson                           2019:35.51 2022:40.44
  Justin Roberts                            2021:1 2023:1
  Malik Williams                            2019:47.32 2022:40.69
  Mark Anthony Sanchez                      2017:39.36 2018:29.42
  Michael Brown                             2016:32.87 2017:42.87
  Michael Ferguson                          2016:39.66 2020:26.18
  Michael Johnson                           2015:45.53 2016:41.80 2018:1 2023:34.68
  Richard Ruiz                              2019:33.48 2023:1
  Robert Anderson                           2019:39.36 2021:41.79
  Robert Edwards                            2015:29.03 2017:39.59
  Robert Miller                             2017:36.20 2024:36.79
  Robert Musser                             2016:61.11 2020:33.42
  Tyler Hodge                               2018:34.02 2021:37.63

AGENCY_IDS by DATE, dollars = LATITUDE
  102                                       2015:297.84 2016:208.89 2017:148.94 2018:59.77 2019:207.93 2020:207.85 2021:298.16 2022:328.01 2023:297.93 2024:297.79
  106                                       2015:158.91 2016:198.64 2017:39.75 2018:198.62 2019:238.44 2020:277.99 2021:158.84 2022:119.51 2023:157.99 2024:79.48
  130                                       2015:186.59 2016:225.40 2017:75.92 2018:148.54 2019:189.47 2020:298.29 2021:38.60 2022:113 2023:3 2024:2
  141                                       2015:181.64 2016:181.75 2017:121.29 2018:151.14 2019:121.11 2020:30.22 2021:90.72 2022:151.35 2023:181.75 2024:151.75
  17                                        2015:151.54 2016:91.03 2017:212.09 2018:121.42 2019:181.95 2020:242.76 2021:60.45 2022:151.50 2023:242.56 2024:91.05
  19                                        2015:120.22 2016:160.61 2017:200.66 2018:163.44 2019:163.29 2020:245.85 2021:243.76 2022:327.47 2023:122.21 2024:82.72
  20                                        2015:510.42 2016:477.43 2017:238.42 2018:238.63 2019:375.49 2020:546.45 2021:308.42 2022:307.93 2023:342.61 2024:375.07
  219                                       2015:225.26 2016:128.47 2017:128.89 2018:77.18 2019:103.26 2020:154.15 2021:51.37 2022:103.40 2023:102.84 2024:51.03
  23                                        2015:248.05 2016:141.70 2017:177.15 2018:106.37 2019:177.69 2020:177.43 2021:70.98 2022:70.77 2023:35.35 2024:142.07
  236                                       2015:206.86 2016:34.14 2017:136.73 2018:34.12 2019:274.07 2020:274.64 2021:34.54 2022:207.50 2023:274.36 2024:342.06
  265                                       2015:376.39 2016:376.46 2017:293.07 2018:125.47 2019:125.46 2020:251.13 2021:167.38 2022:83.66 2023:167.27 2024:125.64
  266                                       2015:154.75 2016:183.25 2017:259.92 2018:74.36 2019:209.37 2020:174.54 2021:38.46 2022:187.41 2023:148.94 2024:109.05
  267                                       2015:270.29 2016:100.74 2017:169.37 2018:101.27 2019:304.10 2020:101.01 2021:203.02 2022:135.13 2023:135.18 2024:134.85
  298                                       2015:285.36 2016:285.06 2017:366.54 2018:162.85 2019:448.20 2020:244.51 2021:81.58 2022:407.61 2023:163.14 2024:447.60
  375                                       2015:361.76 2016:108.65 2017:361.13 2018:397.35 2019:143.57 2020:325.44 2021:180.74 2022:180.76 2023:144.64 2024:325.07
  38                                        2015:715.86 2016:613.22 2017:512.06 2018:477.47 2019:340.53 2020:238.29 2021:306.57 2022:374.50 2023:477.45 2024:375.19
  44                                        2015:117.97 2016:235.50 2017:88.25 2018:147.36 2019:264.97 2020:205.94 2021:235.24 2022:147.18 2023:382.23 2024:382.96
  508                                       2015:105.24 2016:35.13 2017:70.23 2018:210.53 2019:140.34 2020:175.47 2021:105.21 2022:280.75 2023:175.52 2024:280.79
  671                                       2015:40.10 2016:199.94 2017:159.91 2018:159.98 2020:239.95 2021:160.06 2022:159.85 2023:200.09 2024:160.02
  77                                        2015:318.33 2016:119.38 2017:39.80 2018:39.68 2019:39.83 2020:119.59 2021:79.61 2022:39.74 2023:358.01 2024:358.26
  80                                        2015:268.39 2016:536.01 2017:435.95 2018:603.13 2019:401.77 2020:402.02 2021:167.55 2022:163.75 2023:401.89 2024:468.95
  90                                        2015:199.82 2016:239.86 2017:159.92 2018:319.76 2019:1 2020:160.08 2021:119.95 2022:39.94 2023:159.50 2024:322.81

## where

STATE: CA 1.4K, TX 1.0K, FL 672, AZ 461, GA 393, CO 375, NC 310, OH 305, TN 293, WA 277, OK 266, MO 263

## what

THREAT_TYPE: shoot 28%, threat 26%, point 18%, attack 14%, move 6%, undetermined 5%, flee 2%, accident 1%

FLEE_STATUS: not 62%, car 18%, foot 15%, other 4%

ARMED_WITH: gun 59%, knife 17%, unarmed 6%, undetermined 5%, vehicle 4%, replica 3%, blunt_object 2%, unknown 2%, other 1%, gun;knife 0%, gun;vehicle 0%

LOCATION_PRECISION: not_available 76%, block 9%, address 7%, intersection 6%, road 1%, poi_small 0%, poi_large 0%

GENDER: male 96%, female 4%, non-binary 0%

RACE: W 50%, B 27%, H 19%, A 2%, N 2%, O 0%, W;B 0%, W;H 0%, B;H 0%, W;A 0%, N;H 0%

RACE_SOURCE: not_available 67%, photo 16%, public_record 13%, clip 3%, other 0%, undetermined 0%

WAS_MENTAL_ILLNESS_RELATED: False 80%, True 20%

BODY_CAMERA: False 83%, True 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 10.4K | 0 | 11287 53; 11285 53; 11286 53; 11284 53 |
| DATE | date | 3.5K | 0 | 2024-12-21 56; 2024-12-05 56; 2024-11-30 56; 2024-10-15 56 |
| THREAT_TYPE | category | 9 | 68 | shoot 2.9K; threat 2.7K; point 1.9K; attack 1.5K |
| FLEE_STATUS | category | 5 | 1.5K | not 5.6K; car 1.6K; foot 1.3K; other 385 |
| ARMED_WITH | category | 30 | 211 | gun 6.0K; knife 1.8K; unarmed 565; undetermined 463 |
| CITY | who | 3.7K | 74 | Los Angeles 157; Phoenix 131; Houston 126; San Antonio 101 |
| COUNTY | who | 981 | 4.7K | Los Angeles 222; Maricopa 151; Harris 97; Orange 83 |
| STATE | state | 51 | 0 | CA 1.4K; TX 1.0K; FL 672; AZ 461 |
| LATITUDE | amount | 9.2K | 1.1K | 40.546806662127 47; 35.044134730016 47; 41.122823179062 47; 28.580447203664 47 |
| LONGITUDE | amount | 9.3K | 1.1K | -84.570866195499 47; -85.149669534589 47; -112.070576118467 47; -81.445027102501 47 |
| LOCATION_PRECISION | category | 8 | 1.1K | not_available 7.1K; block 859; address 665; intersection 582 |
| NAME | who | 10.1K | 318 | Moses Alik 51; James Junior Holder 51; Nathan Paul 51; Timothy Woods 51 |
| AGE | other | 85 | 372 | 33 348; 34 345; 31 343; 32 335 |
| GENDER | category | 4 | 20 | male 9.9K; female 462; non-binary 5 |
| RACE | category | 13 | 1.2K | W 4.7K; B 2.5K; H 1.7K; A 184 |
| RACE_SOURCE | category | 7 | 1.2K | not_available 6.2K; photo 1.5K; public_record 1.2K; clip 269 |
| WAS_MENTAL_ILLNESS_RELATED | category | 2 | 0 | False 8.4K; True 2.1K |
| BODY_CAMERA | category | 2 | 0 | False 8.6K; True 1.8K |
| AGENCY_IDS | who | 3.8K | 1 | 38 143; 80 125; 20 114; 298 84 |
| INGESTED_AT | audit | 1 | 0 | 1782615452178739 10.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5d93e8ab-0cf9-4683-9b47-d 10.4K |
| SRC_SHA256 | who | 1 | 0 | 606745b7e5189d0291709390e 10.4K |
