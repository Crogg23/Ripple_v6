# XC_NAGIX_DPRK_MISSILE_TESTS

rows 340  columns 15  scan 3.7s

roles: amount 1, audit 2, category 4, date 1, other 4, who 3

## when

DATE
  1984         6  ###
  1986         1  
  1990         2  #
  1991         1  
  1992         1  
  1993         4  ##
  1998         1  
  2006         7  ###
  2009         8  ###
  2012         2  #
  2013         6  ###
  2014        19  ########
  2015        15  #######
  2016        24  ##########
  2017        21  #########
  2019        27  ############
  2020         9  ####
  2021         6  ###
  2022        69  ##############################
  2023        33  ##############
  2024        41  ##################
  2025        11  #####
  2026        26  ###########

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SERIES | 249 | 1 | 2 | 15.52 | 18 | 710 |

## who

FACILITY by rows
        56  pyongyang
        26  hodo
        20  kittaeryong
        19  wonsan
        18  sohae
        17  tonghae
        15  sinpo
        14  hwangju
        14  sunan
        10  chunghwa
        10  samsok-test
         9  hungnam
         8  sunchon
         8  kaechon
         6  mupyong-ni
         6  taesong
         6  uiju
         6  samsok-test-3
         4  jangyon
         4  tongchon

FACILITY by dollars
         280       56 rows  pyongyang
          47       20 rows  kittaeryong
          43       26 rows  hodo
          32       19 rows  wonsan
          27       18 rows  sohae
          22        8 rows  kaechon
          22        9 rows  hungnam
          21        6 rows  samsok-test-3
          21       14 rows  hwangju
          21        6 rows  taesong
          18       10 rows  chunghwa
          16       14 rows  sunan
          15       17 rows  tonghae
          15       15 rows  sinpo
          13        6 rows  uiju
          12        8 rows  sunchon
          10       10 rows  samsok-test
           6        3 rows  koksan
           6        3 rows  sondok
           6        4 rows  tongchon

TIME by rows
        84  unknown
        18  21:13 (UTC)
        12  04:24 (UTC)
         7  21:10 (UTC)
         6  09:20 (UTC)
         5  23:10 (UTC)
         5  22:34 (UTC)
         4  06:00 (UTC)
         4  21:51 (UTC)
         4  00:30 (UTC)
         4  09:29 (UTC)
         3  22:44 (UTC)
         3  23:21 (UTC)
         3  07:59 (UTC)
         3  23:51 (UTC)
         3  23:50 (UTC)
         3  03:13 (UTC)
         3  21:42 (UTC)
         3  21:53 (UTC)
         2  21:45 (UTC)

TIME by dollars
         171       18 rows  21:13 (UTC)
         133       84 rows  unknown
          78       12 rows  04:24 (UTC)
          21        6 rows  09:20 (UTC)
          18        7 rows  21:10 (UTC)
          18        3 rows  23:51 (UTC)
          15        3 rows  23:21 (UTC)
          15        5 rows  22:34 (UTC)
          10        4 rows  21:51 (UTC)
          10        4 rows  06:00 (UTC)
           9        4 rows  00:30 (UTC)
           8        1 rows  00:41 (UTC)
           6        5 rows  23:10 (UTC)
           6        3 rows  03:13 (UTC)
           6        3 rows  22:44 (UTC)
           6        3 rows  23:50 (UTC)
           6        4 rows  09:29 (UTC)
           5        1 rows  00:24 (UTC)
           4        2 rows  22:12 (UTC)
           4        3 rows  21:42 (UTC)

SRC_SHA256 by rows
       340  d68b7b3f4d33028e45c6d2b752f86b54c1a6cef29fe0f88be20430e870f6c766

SRC_SHA256 by dollars
         710      340 rows  d68b7b3f4d33028e45c6d2b752f86b54c1a6cef29fe0f88be20430e870f6

## who x when

FACILITY by DATE, dollars = SERIES
  chunghwa                                  2022:6 2023:3 2024:6 2025:3
  hodo                                      2013:9 2014:4 2015:25 2019:6 2020:3
  hungnam                                   2019:3 2022:19
  hwangju                                   2014:3 2016:15 2025:3
  jangyon                                   2023:3 2024:2
  kaechon                                   2019:6 2022:13 2024:3
  kittaeryong                               2006:13 2009:18 2014:10 2017:6
  koksan                                    2022:6
  mupyong-ni                                2017:1 2021:1 2022:4
  pyongyang                                 2017:2 2022:21 2023:6 2024:171 2026:82
  samsok-test                               2023:2 2024:10
  samsok-test-3                             2024:21
  sinpo                                     2015:3 2016:3 2017:2 2021:1 2022:1 2026:15
  sohae                                     2012:2 2016:1 2017:15 2022:12 2023:4 2024:1
  sondok                                    2020:6
  sunan                                     2022:7 2023:9
  sunchon                                   2014:3 2016:3 2019:3 2022:3
  taesong                                   2023:21
  tongchon                                  2019:3 2022:3
  tonghae                                   1984:12 1986:1 1990:2 1992:1 1993:3 1998:1 2006:1 2009:1
  uiju                                      2022:13
  wonsan                                    2014:3 2016:3 2017:2 2019:3 2022:18 2026:5

TIME by DATE, dollars = SERIES
  00:24 (UTC)                               2022:5
  00:30 (UTC)                               2022:6 2025:3
  00:41 (UTC)                               2022:8
  03:13 (UTC)                               2016:6
  04:24 (UTC)                               2026:78
  06:00 (UTC)                               2024:10
  07:59 (UTC)                               2017:1 2019:3
  09:20 (UTC)                               2023:21
  09:29 (UTC)                               2016:1 2022:6
  21:10 (UTC)                               2020:3 2026:15
  21:13 (UTC)                               2024:171
  21:42 (UTC)                               2017:1 2022:4
  21:45 (UTC)                               2019:1 2020:1
  21:51 (UTC)                               2022:10
  21:53 (UTC)                               2019:1 2022:1 2024:1
  22:12 (UTC)                               2019:2 2024:2
  22:34 (UTC)                               2017:15
  22:44 (UTC)                               2024:6
  23:10 (UTC)                               2022:1 2025:6
  23:21 (UTC)                               2024:15
  23:50 (UTC)                               2022:1 2026:5
  23:51 (UTC)                               2022:18
  unknown                                   1984:12 1986:1 1990:2 1991:1 1992:1 1993:3 1998:1 2006:13 2009:18 2012:2 2013:9 2014:25 2015:28 2016:6 2019:5 2022:13 2026:1

## what

MISSILE: kn-25 27%, unknown 24%, scud-c 10%, hwasong-11a 7%, kn-02 7%, nodong 6%, hwasong-11d 5%, hwasong-11b 4%, scud-b 4%, er-scud 3%, musudan 3%, hwasong-12 2%

LANDING: sea-of-japan 83%, unknown 6%, yellow-sea 4%, na 4%, pacific-ocean 2%, north-korea 1%

OUTCOME: success 67%, unknown 21%, failure 11%

GLIDE: nan 99%, [{'distance': 600, 'maneuverin 0%, [{'distance': 500, 'maneuverin 0%, [{'distance': 600, 'maneuverin 0%, [{'distance': 500, 'maneuverin 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATE | date | 166 | 0 | 2024-05-29 18; 2026-03-14 12; 2022-06-05 8; 2022-11-01 7 |
| TIME | who | 159 | 0 | unknown 84; 21:13 (UTC) 18; 04:24 (UTC) 12; 21:10 (UTC) 7 |
| SERIES | amount | 19 | 0 | nan 91; 2.0 85; 1.0 85; 3.0 28 |
| MISSILE | category | 37 | 0 | kn-25 77; unknown 67; scud-c 27; hwasong-11a 20 |
| FACILITY | who | 56 | 0 | pyongyang 56; hodo 26; kittaeryong 20; wonsan 19 |
| LANDING | category | 6 | 0 | sea-of-japan 283; unknown 20; yellow-sea 15; na 12 |
| APOGEE | other | 56 | 0 | unknown 100; 50 51; 100 37; 150 17 |
| DISTANCE | other | 63 | 0 | unknown 68; 350 48; 500 17; 400 16 |
| BEARING | other | 53 | 0 | 90 86; 62 45; 70 29; 58 18 |
| OUTCOME | category | 3 | 0 | success 229; unknown 73; failure 38 |
| DESCRIPTION | other | 258 | 35 | On May 30 (local time), N 18; On June 5, North Korea la 8; 2 of 2 6; 1 of 2 6 |
| GLIDE | category | 5 | 0 | nan 336; [{'distance': 600, 'maneu 1; [{'distance': 500, 'maneu 1; [{'distance': 600, 'maneu 1 |
| INGESTED_AT | audit | 1 | 0 | 1782663939414691 340 |
| SOURCE_RUN_ID | audit | 1 | 0 | e1fe400e-7607-48d1-8090-1 340 |
| SRC_SHA256 | who | 1 | 0 | d68b7b3f4d33028e45c6d2b75 340 |
