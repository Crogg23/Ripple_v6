# PORTAL_CKA_WPRDC_ALLEGHENY_1C103EE2CD

rows 3.4K  columns 18  scan 5.8s

roles: amount 2, audit 2, category 5, date 2, other 3, who 5

## when

CREATE_DATE
  2020      1.1K  ##############################
  2021       235  ######
  2022       306  ########
  2023       483  #############
  2024       537  ##############
  2025       353  #########
  2026       360  #########

INGESTED_AT
  2026      3.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 3.4K | 40.37 | 40.45 | 40.49 | 40.49 | 138.3K |
| LONGITUDE | 3.4K | -80.08 | -79.98 | -79.88 | -79.87 | -273.5K |

## who

OWNER by rows
       331  CITY OF PITTSBURGH
        38  R T HOMEWOOD LLC
        30  PITTSBURGH LAND BANK
        13  URBAN REDEVELOPMENT AUTHORITY OFPITTSBURGH
         8  INTISSAR LLC
         8  DIVILLY SARAH
         7  HILL COMMUNITY DEVELOPMENT CORPORATION
         7  RTH INVESTMENT LLC
         5  JAMES DOROTHY
         5  COMMUNITY REINVESTMENT PARTNERS LLC
         5  SECORD NORTH LLC
         5  BRYCE PETERS FINANCIAL CORPORATION
         5  PRF 100 LLC
         5  WEBCOR INC
         5  ECKENRODE ROBERT C
         4  PENN PIONEER ENTERPRISES LLC
         4  DEFRANCO BRYAN
         4  EAST LIBERTY DEVELOPMENT INC
         4  BENKOVSKI NESINKA & ZELJKO
         4  SNINSKY RONALD D

OWNER by dollars
       13.4K      331 rows  CITY OF PITTSBURGH
        1.5K       38 rows  R T HOMEWOOD LLC
        1.2K       30 rows  PITTSBURGH LAND BANK
      525.75       13 rows  URBAN REDEVELOPMENT AUTHORITY OFPITTSBURGH
      323.53        8 rows  DIVILLY SARAH
      323.51        8 rows  INTISSAR LLC
      283.15        7 rows  HILL COMMUNITY DEVELOPMENT CORPORATION
      282.86        7 rows  RTH INVESTMENT LLC
      202.35        5 rows  JAMES DOROTHY
      202.32        5 rows  COMMUNITY REINVESTMENT PARTNERS LLC
      202.31        5 rows  PRF 100 LLC
      202.20        5 rows  ECKENRODE ROBERT C
      202.17        5 rows  BRYCE PETERS FINANCIAL CORPORATION
      202.06        5 rows  WEBCOR INC
      202.04        5 rows  SECORD NORTH LLC
      161.88        4 rows  CULLEN EMMETT & LOUISE (W)
      161.88        4 rows  AMICONE LOUISE A
      161.84        4 rows  EAST LIBERTY DEVELOPMENT INC
      161.83        4 rows  PENN PIONEER ENTERPRISES LLC
      161.81        4 rows  BENKOVSKI NESINKA & ZELJKO

NEIGHBORHOOD by rows
       207  Hazelwood
       204  Perry South
       203  Homewood North
       200  Lincoln-Lemington-Belmar
       176  Marshall-Shadeland
       175  Knoxville
       164  Middle Hill
       141  Beltzhoover
       136  Homewood South
       112  Sheraden
       100  Carrick
        92  East Hills
        78  Allentown
        76  Upper Hill
        74  Elliott
        69  South Side Slopes
        66  Garfield
        58  Larimer
        52  Manchester
        50  Spring Hill-City View

NEIGHBORHOOD by dollars
        8.4K      207 rows  Hazelwood
        8.3K      204 rows  Perry South
        8.2K      203 rows  Homewood North
        8.1K      200 rows  Lincoln-Lemington-Belmar
        7.1K      176 rows  Marshall-Shadeland
        7.1K      175 rows  Knoxville
        6.6K      164 rows  Middle Hill
        5.7K      141 rows  Beltzhoover
        5.5K      136 rows  Homewood South
        4.5K      112 rows  Sheraden
        4.0K      100 rows  Carrick
        3.7K       92 rows  East Hills
        3.2K       78 rows  Allentown
        3.1K       76 rows  Upper Hill
        3.0K       74 rows  Elliott
        2.8K       69 rows  South Side Slopes
        2.7K       66 rows  Garfield
        2.3K       58 rows  Larimer
        2.1K       52 rows  Manchester
        2.0K       50 rows  Spring Hill-City View

PROPERTY_TYPE by rows
      3.4K  Condemned/Dead End Property

PROPERTY_TYPE by dollars
      138.3K     3.4K rows  Condemned/Dead End Property

INSPECTION_STATUS by rows
      3.4K  Active

INSPECTION_STATUS by dollars
      138.3K     3.4K rows  Active

## who x when

OWNER by CREATE_DATE, dollars = LATITUDE
  AMICONE LOUISE A                          2021:121.41 2022:40.47
  BENKOVSKI NESINKA & ZELJKO                2020:161.81
  BRYCE PETERS FINANCIAL CORPORATION        2020:80.88 2022:40.42 2023:40.41 2024:40.46
  CITY OF PITTSBURGH                        2020:8.5K 2021:1.2K 2022:930.42 2023:1.1K 2024:849.22 2025:444.91 2026:444.85
  COMMUNITY REINVESTMENT PARTNERS LLC       2020:80.95 2021:40.43 2023:80.94
  CULLEN EMMETT & LOUISE (W)                2022:40.46 2025:40.46 2026:80.96
  DEFRANCO BRYAN                            2020:80.82 2023:80.82
  DIVILLY SARAH                             2022:242.65 2023:40.44 2025:40.44
  EAST LIBERTY DEVELOPMENT INC              2020:80.92 2021:40.46 2024:40.46
  ECKENRODE ROBERT C                        2022:80.88 2023:121.32
  HILL COMMUNITY DEVELOPMENT CORPORATION    2020:242.70 2021:40.45
  INTISSAR LLC                              2022:80.84 2023:161.73 2025:40.47 2026:40.47
  JAMES DOROTHY                             2024:161.88 2026:40.47
  PENN PIONEER ENTERPRISES LLC              2022:80.92 2024:40.46 2026:40.45
  PITTSBURGH LAND BANK                      2020:808.86 2021:121.36 2022:80.88 2023:161.70 2024:40.45
  PRF 100 LLC                               2021:40.46 2022:40.46 2026:121.39
  R T HOMEWOOD LLC                          2020:647.24 2022:283.20 2024:606.84
  RTH INVESTMENT LLC                        2020:161.64 2021:40.41 2023:40.40 2026:40.41
  SECORD NORTH LLC                          2020:80.81 2023:40.41 2025:40.40 2026:40.42
  SNINSKY RONALD D                          2020:80.92 2022:40.46 2025:40.38
  URBAN REDEVELOPMENT AUTHORITY OFPITTSBUR  2020:404.42 2022:40.44 2023:40.44 2024:40.45
  WEBCOR INC                                2020:121.24 2023:40.42 2024:40.40

NEIGHBORHOOD by CREATE_DATE, dollars = LATITUDE
  Allentown                                 2020:1.4K 2021:80.84 2022:202.10 2023:808.40 2024:242.52 2025:242.52 2026:161.68
  Beltzhoover                               2020:2.3K 2021:242.52 2022:363.77 2023:1.3K 2024:687.12 2025:525.46 2026:242.52
  Carrick                                   2020:1.1K 2021:121.19 2022:242.40 2023:767.50 2024:646.26 2025:605.95 2026:565.53
  East Hills                                2020:1.2K 2021:40.46 2022:80.91 2023:485.42 2024:849.50 2025:80.90 2026:970.87
  Elliott                                   2020:727.98 2021:283.11 2022:485.33 2023:242.65 2024:727.94 2025:202.21 2026:323.54
  Garfield                                  2020:1.6K 2021:283.29 2022:161.88 2023:283.29 2024:202.35 2025:121.41
  Hazelwood                                 2020:2.1K 2021:444.50 2022:444.47 2023:767.70 2024:2.7K 2025:1.3K 2026:565.78
  Homewood North                            2020:2.5K 2021:445.06 2022:930.58 2023:566.44 2024:1.7K 2025:606.90 2026:1.5K
  Homewood South                            2020:2.3K 2021:202.27 2022:647.27 2023:202.26 2024:1.1K 2025:444.99 2026:606.76
  Knoxville                                 2020:3.0K 2021:404.15 2022:525.43 2023:1.7K 2024:889.12 2025:484.97 2026:121.24
  Larimer                                   2020:930.64 2021:121.38 2022:242.77 2023:121.38 2024:445.09 2025:323.70 2026:161.85
  Lincoln-Lemington-Belmar                  2020:3.1K 2021:202.35 2022:526.11 2023:930.77 2024:1.6K 2025:566.57 2026:1.2K
  Manchester                                2020:970.97 2021:80.92 2022:121.37 2023:323.67 2025:283.21 2026:323.67
  Marshall-Shadeland                        2020:1.4K 2021:283.29 2022:1.3K 2023:1.4K 2024:849.84 2025:647.50 2026:1.3K
  Middle Hill                               2020:3.0K 2021:1.5K 2022:485.39 2023:525.83 2024:566.30 2025:404.50 2026:161.80
  Perry South                               2020:1.9K 2021:364.19 2022:768.87 2023:1.9K 2024:1.0K 2025:1.2K 2026:1.2K
  Sheraden                                  2020:1.9K 2021:525.94 2022:445.02 2023:445 2024:687.77 2025:242.73 2026:283.18
  South Side Slopes                         2020:565.88 2021:161.68 2022:202.10 2023:687.15 2024:485.07 2025:404.20 2026:282.94
  Spring Hill-City View                     2020:768.88 2021:121.39 2022:161.87 2023:242.80 2024:161.87 2025:242.79 2026:323.73
  Upper Hill                                2020:1.5K 2021:525.87 2022:161.81 2023:404.55 2024:364.06 2025:121.36 2026:40.45

## what

ZIP_CODE: 15210 19%, 15212 15%, 15219 11%, 15206 10%, 15207 9%, 15208 9%, 15214 9%, 15221 6%, 15204 5%, 15220 3%, 15203 2%, 15224 2%

LATEST_INSPECTION_RESULT: Fail 65%, Pass 35%

LATEST_INSPECTION_SCORE: 0 35%, 2 32%, 1 24%, 3 8%, 4 0%

COUNCIL_DISTRICT: 6 24%, 9 23%, 3 17%, 2 10%, 1 9%, 5 9%, 4 6%, 7 2%, 8 0%

WARD: 13 16%, 12 11%, 5 10%, 20 9%, 18 9%, 26 9%, 15 9%, 27 8%, 30 7%, 25 5%, 16 4%, 29 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PARCEL_ID | other | 2.8K | 0 | 0014J00173000000 20; 0060E00108000000 18; 0056F00306000000 18; 0046K00058000000 18 |
| ADDRESS | other | 2.3K | 0 | No primary address specif 534; 706 BERND ST, Pittsburgh, 18; 160 MARSDEN ST, Pittsburg 16; 200 CUTLER ST, Pittsburgh 16 |
| ZIP_CODE | category | 24 | 0 | 15210 581; 15212 447; 15219 347; 15206 309 |
| OWNER | who | 1.9K | 563 | CITY OF PITTSBURGH 331; R T HOMEWOOD LLC 38; PITTSBURGH LAND BANK 30; URBAN REDEVELOPMENT AUTHO 17 |
| PROPERTY_TYPE | who | 1 | 0 | Condemned/Dead End Proper 3.4K |
| CREATE_DATE | date | 924 | 0 | 2020-09-09 91; 2020-09-08 68; 2026-04-17 57; 2020-09-10 56 |
| LATEST_INSPECTION_RESULT | category | 3 | 314 | Fail 2.0K; Pass 1.1K |
| LATEST_INSPECTION_SCORE | category | 6 | 314 | 0 1.1K; 2 1.0K; 1 758; 3 240 |
| RECORD_NUMBER | other | 2.8K | 0 | 0014J00173000000 20; 0060E00108000000 18; 0056F00306000000 18; 0046K00058000000 18 |
| INSPECTION_STATUS | who | 1 | 0 | Active 3.4K |
| LATITUDE | amount | 2.8K | 0 | 40.4164448183 20; 40.3999920931 18; 40.4106272781 18; 40.4662665323 18 |
| LONGITUDE | amount | 2.8K | 0 | -79.9979107332 20; -79.9980839747 18; -79.9424275223 18; -80.0119031739 18 |
| NEIGHBORHOOD | who | 87 | 0 | Hazelwood 207; Perry South 204; Homewood North 203; Lincoln-Lemington-Belmar 200 |
| COUNCIL_DISTRICT | category | 9 | 0 | 6 812; 9 801; 3 580; 2 331 |
| WARD | category | 33 | 1 | 13 429; 12 283; 5 273; 20 253 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:06:13.87662 3.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 56b6b157-bb38-4c52-98ea-9 3.4K |
| SRC_SHA256 | who | 1 | 0 | 97254f1194e8f46caf9ae1ef2 3.4K |
