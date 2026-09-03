# PORTAL_CKA_WESTERN_PENNSYLV_F66E0E22DA

rows 1.4K  columns 15  scan 3.7s

roles: amount 3, audit 2, category 3, date 3, id 2, who 3

## when

APP_DATE
  2020       214  #######################
  2021       272  #############################
  2022       279  ##############################
  2023       257  ############################
  2024       219  ########################
  2025       190  ####################

APP_SORT
  2020       213  #######################
  2021       272  #############################
  2022       280  ##############################
  2023       257  ############################
  2024       219  #######################
  2025       190  ####################

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 1.4K | 0.01 | 0.98 | 72.30 | 299 | 8.7K |
| POSTIMPERV | 1.4K | -999 | -999 | 24.96 | 68.75 | -812.6K |
| PREIMPERV | 1.4K | -999 | -999 | 17.58 | 68.75 | -813.7K |

## who

MUNICIPALI by rows
       218  Pittsburgh
        69  Moon Township
        52  Plum Borough
        51  Fox Chapel Borough
        50  North Fayette Township
        47  South Fayette Township
        40  Monroeville Municipality
        38  Findlay Township
        35  Collier Township
        33  Robinson Township
        33  Marshall Township
        31  Franklin Park Borough
        30  West Mifflin Borough
        30  Penn Hills Municipality
        30  Jefferson Hills Borough
        27  Hampton Township
        27  Indiana Township
        26  Bethel Park Municipality
        26  Ross Township
        25  West Deer Township

MUNICIPALI by dollars
      826.99      218 rows  Pittsburgh
      705.49       38 rows  Findlay Township
      697.03       50 rows  North Fayette Township
      589.27       69 rows  Moon Township
      518.80       30 rows  Jefferson Hills Borough
      506.40       33 rows  Marshall Township
      468.12       47 rows  South Fayette Township
      368.99       25 rows  West Deer Township
      277.36       52 rows  Plum Borough
      217.94       33 rows  Robinson Township
      205.99       30 rows  West Mifflin Borough
      179.33       40 rows  Monroeville Municipality
      174.31        4 rows  Stowe Township
      171.91       31 rows  Franklin Park Borough
      165.65       27 rows  Indiana Township
      151.59       35 rows  Collier Township
      147.61       27 rows  Hampton Township
      144.12       22 rows  Upper St. Clair Municipality
      142.26       26 rows  Bethel Park Municipality
      130.92       21 rows  Pine Township

STATUS by rows
      1.4K  Issued/Authorized

STATUS by dollars
        8.7K     1.4K rows  Issued/Authorized

SRC_SHA256 by rows
      1.4K  8565b6fa7f6669e92e3e7f1ab70be0db305099047bf0b45518fb06e4f0917c95

SRC_SHA256 by dollars
        8.7K     1.4K rows  8565b6fa7f6669e92e3e7f1ab70be0db305099047bf0b45518fb06e4f091

## who x when

MUNICIPALI by APP_DATE, dollars = ACRES
  Bethel Park Municipality                  2020:6.14 2021:13.17 2022:71.98 2023:15.15 2024:28.20 2025:7.62
  Collier Township                          2020:25.37 2021:35.52 2022:31.61 2023:14.01 2024:11.14 2025:33.94
  Findlay Township                          2020:261.26 2021:8.87 2022:162.06 2023:10.54 2024:119.96 2025:142.80
  Fox Chapel Borough                        2020:5.41 2021:34.86 2022:4.60 2023:10.89 2024:7.29 2025:2.69
  Franklin Park Borough                     2020:54.45 2021:11.38 2022:13.57 2023:16.57 2024:61.46 2025:14.48
  Hampton Township                          2020:59.78 2021:42.35 2022:1.22 2023:8.66 2024:31.93 2025:3.67
  Indiana Township                          2020:21.83 2021:36.50 2022:41.29 2023:32.05 2024:0.71 2025:33.27
  Jefferson Hills Borough                   2020:414.99 2021:3.40 2022:6.89 2023:21.13 2024:72.39
  Marshall Township                         2020:106.32 2021:48.27 2022:37.86 2023:91.60 2024:166.98 2025:55.37
  Monroeville Municipality                  2020:10.21 2021:38.30 2022:18.27 2023:41.75 2024:62.80 2025:8
  Moon Township                             2020:102.12 2021:163.14 2022:66.47 2023:52.11 2024:169.80 2025:35.63
  North Fayette Township                    2020:172.95 2021:154.53 2022:118.19 2023:12.02 2024:50.45 2025:188.89
  Penn Hills Municipality                   2020:9.60 2021:12.36 2022:14.92 2023:28.45 2024:0.64 2025:9.05
  Pine Township                             2020:0.99 2021:11.27 2022:79.57 2023:3.69 2024:35.40
  Pittsburgh                                2020:93.23 2021:57.66 2022:117.10 2023:144.03 2024:232.10 2025:182.87
  Plum Borough                              2020:9.66 2021:25.98 2022:140.89 2023:58 2024:11.47 2025:31.36
  Robinson Township                         2020:61.34 2021:43.27 2022:41.35 2023:29.03 2024:40.21 2025:2.74
  Ross Township                             2020:32.52 2021:1.21 2022:17.41 2023:8.88 2024:8.02 2025:0.98
  South Fayette Township                    2020:133.48 2021:68.14 2022:48.04 2023:39.58 2024:29.99 2025:148.89
  Stowe Township                            2020:49.60 2022:73.40 2023:48.05 2024:3.26
  Upper St. Clair Municipality              2020:0.25 2021:43.45 2022:14.24 2023:22.19 2024:63.09 2025:0.90
  West Deer Township                        2020:46.73 2021:33.88 2022:99.08 2023:148.68 2024:13.21 2025:27.41
  West Mifflin Borough                      2020:0.58 2021:37.41 2022:27.18 2023:22.48 2024:73.38 2025:44.96

STATUS by APP_DATE, dollars = ACRES
  Issued/Authorized                         2020:2.0K 2021:1.3K 2022:1.6K 2023:1.0K 2024:1.6K 2025:1.2K

## what

DSCHRG_PTS: -999 57%, 1 19%, 2 9%, 0 7%, 3 4%, 4 2%, 5 1%, 6 0%, 7 0%, 8 0%, 9 0%, 11 0%

LANDUSE: Commercial/Industrial 25%, Utility Facility/Transmission 15%, Remediation/Restoration 11%, Institutional 8%, Sewer/Water System 8%, Residential-Private 8%, Residential-Subdivision 8%, Residential-Rental 4%, Recreation 4%, Park 3%, Public Road Construction 3%, Borrow/Disposal Site 3%

MAX_NONSTR: No 72%, N/A 26%, Yes 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACRES | amount | 561 | 0 | 0.49 113; 0.99 46; 0.98 24; 0.96 20 |
| APP_DATE | date | 879 | 0 | 2025-06-17 11; 2024-10-23 9; 2025-01-07 9; 2025-01-14 9 |
| APP_SORT | date | 857 | 0 | 20250617 11; 20241023 9; 20250107 9; 20250114 9 |
| DSCHRG_PTS | category | 15 | 0 | -999 815; 1 270; 2 129; 0 104 |
| FEATURE_ID | id | 1.4K | 0 | ACGP00535 8; ACGP00550 8; ACGP00566 8; ACCD20051 8 |
| LANDUSE | category | 22 | 0 | Commercial/Industrial 326; Utility Facility/Transmis 195; Remediation/Restoration 149; Institutional 112 |
| MAX_NONSTR | category | 4 | 820 | No 440; N/A 158; Yes 13 |
| POSTIMPERV | amount | 384 | 0 | -999.0 816; 0.0 45; 0.92 7; 0.46 6 |
| PREIMPERV | amount | 290 | 0 | -999.0 816; 0.0 110; 0.1 8; 0.18 7 |
| STATUS | who | 1 | 0 | Issued/Authorized 1.4K |
| MUNICIPALI | who | 108 | 1 | Pittsburgh 218; Moon Township 69; Plum Borough 52; Fox Chapel Borough 51 |
| GEOMETRY | id | 1.5K | 0 | POLYGON ((-8929598.589610 8; MULTIPOLYGON (((-8928880. 8; POLYGON ((-8918513.223271 8; POLYGON ((-8912242.925677 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:54:27.72417 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | fc1731db-a623-462c-9056-8 1.4K |
| SRC_SHA256 | who | 1 | 0 | 8565b6fa7f6669e92e3e7f1ab 1.4K |
