# PORTAL_CKA_WPRDC_ALLEGHENY_65D88E2BEF

rows 4.5K  columns 22  scan 4.2s

roles: amount 3, audit 2, category 12, date 1, other 2, who 3

## when

INGESTED_AT
  2026      4.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_COUNT | 4.5K | 1 | 1 | 5 | 55 | 5.7K |
| LATITUDE | 3.8K | 40.32 | 40.45 | 40.49 | 40.60 | 155.3K |
| LONGITUDE | 3.8K | -80.22 | -79.98 | -79.84 | -79.75 | -307.0K |

## who

TRACT by rows
       144  42003130300
       137  42003170200
       111  42003020100
       106  42003130400
       102  42003130600
        96  42003050100
        93  42003562300
        87  42003300100
        86  42003271500
        81  42003130100
        79  42003562500
        77  42003120800
        74  42003261400
        66  42003563200
        65  42003180300
        65  42003120300
        60  42003050900
        59  42003262000
        57  42003210700
        56  42003250900

TRACT by dollars
         215      144 rows  42003130300
         158      137 rows  42003170200
         131      106 rows  42003130400
         130      102 rows  42003130600
         123      111 rows  42003020100
         121       86 rows  42003271500
         117       93 rows  42003562300
         110       87 rows  42003300100
         107       96 rows  42003050100
         101       81 rows  42003130100
          97       36 rows  42003111500
          96       77 rows  42003120800
          92       39 rows  42003270300
          90       74 rows  42003261400
          89       79 rows  42003562500
          87       65 rows  42003180300
          77       66 rows  42003563200
          74       65 rows  42003120300
          73       60 rows  42003050900
          71       59 rows  42003262000

NEIGHBORHOOD by rows
       245  Homewood South
       177  South Side Flats
       129  Homewood North
       116  Carrick
       109  Central Business District
       109  Perry South
       108  Hazelwood
       106  Sheraden
       106  East Hills
       105  Marshall-Shadeland
       102  Lincoln-Lemington-Belmar
        99  Larimer
        93  Knoxville
        84  Middle Hill
        80  Garfield
        80  Brighton Heights
        78  Mount Washington
        73  East Liberty
        67  Bedford Dwellings
        66  Allentown

NEIGHBORHOOD by dollars
         338      245 rows  Homewood South
         204      177 rows  South Side Flats
         158      129 rows  Homewood North
         147       73 rows  East Liberty
         146      116 rows  Carrick
         146       80 rows  Brighton Heights
         145      105 rows  Marshall-Shadeland
         140      108 rows  Hazelwood
         135      102 rows  Lincoln-Lemington-Belmar
         134      106 rows  East Hills
         133      109 rows  Perry South
         121      109 rows  Central Business District
         119      106 rows  Sheraden
         118       99 rows  Larimer
         116       93 rows  Knoxville
          99       63 rows  Beechview
          95       80 rows  Garfield
          92       84 rows  Middle Hill
          90       78 rows  Mount Washington
          89       66 rows  Allentown

SRC_SHA256 by rows
      4.5K  a0079964d41f827807ea52f6df8e33953304b103ddd4b798ad1325bae980047d

SRC_SHA256 by dollars
        5.7K     4.5K rows  a0079964d41f827807ea52f6df8e33953304b103ddd4b798ad1325bae980

## who x when

TRACT by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_COUNT
  42003020100                               2026:123
  42003050100                               2026:107
  42003050900                               2026:73
  42003111500                               2026:97
  42003120300                               2026:74
  42003120800                               2026:96
  42003130100                               2026:101
  42003130300                               2026:215
  42003130400                               2026:131
  42003130600                               2026:130
  42003170200                               2026:158
  42003180300                               2026:87
  42003210700                               2026:64
  42003250900                               2026:68
  42003261400                               2026:90
  42003262000                               2026:71
  42003270300                               2026:92
  42003271500                               2026:121
  42003300100                               2026:110
  42003562300                               2026:117
  42003562500                               2026:89
  42003563200                               2026:77

NEIGHBORHOOD by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_COUNT
  Allentown                                 2026:89
  Bedford Dwellings                         2026:81
  Beechview                                 2026:99
  Brighton Heights                          2026:146
  Carrick                                   2026:146
  Central Business District                 2026:121
  East Hills                                2026:134
  East Liberty                              2026:147
  Garfield                                  2026:95
  Hazelwood                                 2026:140
  Homewood North                            2026:158
  Homewood South                            2026:338
  Knoxville                                 2026:116
  Larimer                                   2026:118
  Lincoln-Lemington-Belmar                  2026:135
  Marshall-Shadeland                        2026:145
  Middle Hill                               2026:92
  Mount Washington                          2026:90
  Perry South                               2026:133
  Sheraden                                  2026:119
  South Side Flats                          2026:204

## what

OTHER_COUNT: 0 98%, 1 2%, 2 0%, 3 0%, 14 0%

PISTOL_COUNT: 1 72%, 0 19%, 2 7%, 3 2%, 4 0%, 5 0%, 9 0%, 8 0%, 30 0%, 19 0%, 12 0%, 10 0%

REVOLVER_COUNT: 0 86%, 1 13%, 2 1%, 3 0%, 4 0%, 6 0%

RIFLE_COUNT: 0 93%, 1 5%, 2 1%, 3 0%, 5 0%, 4 0%, 7 0%, 22 0%, 17 0%, 15 0%

SHOTGUN_COUNT: 0 95%, 1 4%, 2 0%, 3 0%, 5 0%, 7 0%

YEAR: 2017 15%, 2021 14%, 2015 12%, 2016 12%, 2019 12%, 2018 12%, 2022 11%, 2020 11%

MONTH: 9 10%, 7 10%, 6 9%, 5 9%, 10 9%, 8 9%, 3 8%, 4 8%, 1 8%, 2 7%, 11 7%, 12 6%

DOW: 5 16%, 3 16%, 2 15%, 4 15%, 6 14%, 1 13%, 0 11%

COUNCIL_DISTRICT: 9 25%, 6 20%, 1 14%, 3 14%, 2 9%, 4 7%, 5 5%, 7 5%, 8 1%

WARD: 13 21%, 12 11%, 5 10%, 26 9%, 20 9%, 27 8%, 19 7%, 15 7%, 17 7%, 25 6%, 18 6%

PUBLIC_WORKS_DIVISION: 2 29%, 3 26%, 1 21%, 5 19%, 6 4%, 0 0%

POLICE_ZONE: 5 26%, 1 23%, 3 18%, 2 13%, 6 10%, 4 9%, OSC 2%, NA 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ADDRESS | other | 3.0K | 0 | 1700 BLOCK BELLEAU DR PIT 40; 300 BLOCK EAST OHIO ST PI 39; 2300 BLOCK EAST HILLS DR  28; 300 BLOCK CEDAR AVE PITTS 25 |
| TOTAL_COUNT | amount | 18 | 0 | 1 3.8K; 2 443; 3 118; 4 44 |
| OTHER_COUNT | category | 5 | 0 | 0 4.4K; 1 82; 2 8; 3 2 |
| PISTOL_COUNT | category | 12 | 0 | 1 3.2K; 0 840; 2 319; 3 69 |
| REVOLVER_COUNT | category | 6 | 0 | 0 3.9K; 1 567; 2 33; 3 5 |
| RIFLE_COUNT | category | 10 | 0 | 0 4.2K; 1 246; 2 29; 3 12 |
| SHOTGUN_COUNT | category | 6 | 0 | 0 4.3K; 1 184; 2 13; 3 4 |
| YEAR | category | 8 | 0 | 2017 664; 2021 649; 2015 560; 2016 554 |
| MONTH | category | 12 | 0 | 9 432; 7 430; 6 411; 5 411 |
| DOW | category | 7 | 0 | 5 729; 3 714; 2 673; 4 657 |
| NEIGHBORHOOD | who | 90 | 773 | Homewood South 245; South Side Flats 177; Homewood North 129; Carrick 116 |
| COUNCIL_DISTRICT | category | 10 | 782 | 9 927; 6 741; 1 512; 3 510 |
| WARD | category | 34 | 773 | 13 481; 12 261; 5 222; 26 202 |
| TRACT | who | 187 | 646 | 42003130300 144; 42003170200 137; 42003020100 111; 42003130400 106 |
| PUBLIC_WORKS_DIVISION | category | 7 | 773 | 2 1.1K; 3 981; 1 792; 5 702 |
| POLICE_ZONE | category | 8 | 0 | 5 1.2K; 1 1.0K; 3 798; 2 580 |
| FIRE_ZONE | other | 99 | 737 | 3-17 432; 4-24 178; 1-14 171; 1-16 134 |
| LATITUDE | amount | 2.5K | 646 | 40.460310552493 38; 40.4125315408834 35; 40.4653596489546 26; 40.4566162367709 25 |
| LONGITUDE | amount | 2.4K | 646 | -80.0069833937371 38; -79.8427960425285 35; -79.871328586779 25; -79.992041845149 23 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:07:33.17069 4.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 217cb173-584e-4607-a38d-a 4.5K |
| SRC_SHA256 | who | 1 | 0 | a0079964d41f827807ea52f6d 4.5K |
