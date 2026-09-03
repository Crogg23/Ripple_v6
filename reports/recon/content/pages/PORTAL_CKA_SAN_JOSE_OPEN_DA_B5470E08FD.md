# PORTAL_CKA_SAN_JOSE_OPEN_DA_B5470E08FD

rows 3.0K  columns 13  scan 5.5s

roles: amount 3, audit 2, category 1, date 2, id 4, who 2

## when

LASTUPDATE
  2022      3.0K  ##############################

INGESTED_AT
  2026      3.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 3.0K | 0.01 | 0.09 | 10.30 | 156.39 | 2.7K |
| SHAPE_LENGTH | 3.0K | 76.70 | 294.90 | 5.6K | 32.3K | 2.22M |
| SHAPE_AREA | 3.0K | 232.34 | 4.2K | 605.1K | 16.77M | 165.69M |

## who

FACILITYID by rows
         1  107
         1  6
         1  66
         1  32
         1  125
         1  80
         1  110
         1  133
         1  119
         1  167
         1  77
         1  182
         1  124
         1  79
         1  7
         1  3
         1  40
         1  31
         1  12
         1  8

FACILITYID by dollars
      156.39        1 rows  2047
       56.57        1 rows  1571
       33.36        1 rows  2119
       31.42        1 rows  190
       24.26        1 rows  2190
       22.45        1 rows  1999
       21.87        1 rows  1544
       21.43        1 rows  1038
       19.75        1 rows  2158
       19.73        1 rows  2243
       19.35        1 rows  2219
       18.83        1 rows  1034
       17.61        1 rows  947
       16.69        1 rows  2092
       15.38        1 rows  2000
       14.70        1 rows  2605
       14.04        1 rows  169
       13.93        1 rows  1035
       13.85        1 rows  160
       13.72        1 rows  594

SRC_SHA256 by rows
      3.0K  7c63b0329438a2f19823ab3fc49c168fd4dbace73373b2c8313fa917e0a95a6a

SRC_SHA256 by dollars
        2.7K     3.0K rows  7c63b0329438a2f19823ab3fc49c168fd4dbace73373b2c8313fa917e0a9

## who x when

FACILITYID by LASTUPDATE, dollars = ACRES
  1038                                      2022:21.43
  107                                       2022:0.72
  110                                       2022:0.58
  119                                       2022:1.12
  12                                        2022:0.46
  124                                       2022:1.76
  125                                       2022:3.49
  133                                       2022:0.70
  1544                                      2022:21.87
  1571                                      2022:56.57
  167                                       2022:0.70
  182                                       2022:0.19
  190                                       2022:31.42
  1999                                      2022:22.45
  2047                                      2022:156.39
  2119                                      2022:33.36
  2158                                      2022:19.75
  2190                                      2022:24.26
  2243                                      2022:19.73
  3                                         2022:0.85
  31                                        2022:5.92
  32                                        2022:0.06
  40                                        2022:7.43
  6                                         2022:0.11
  66                                        2022:1.28
  7                                         2022:0.23
  77                                        2022:0.42
  79                                        2022:0.50
  8                                         2022:0.76
  80                                        2022:0.13

SRC_SHA256 by LASTUPDATE, dollars = ACRES
  7c63b0329438a2f19823ab3fc49c168fd4dbace7  2022:2.7K

## what

LANDUSE: Residential 42%, Light Industrial 36%, Other - Urban Open 5%, Other - Transportation Rail 5%, Retail 3%, Commercial/Industrial Mixed 3%, Heavy Industrial 2%, Other - Transportation Airport 2%, Commercial 1%, Residential/Commercial Mixed 0%, Other - Transportation Highway 0%, Other - Rangeland 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 3.0K | 0 | 3000 15; 2999 15; 2998 15; 2997 15 |
| FACILITYID | who | 3.0K | 0 | 3000 15; 2999 15; 2998 15; 2997 15 |
| INTID | id | 3.0K | 0 | 3000 15; 2999 15; 2998 15; 2997 15 |
| APN | id | 3.0K | 0 | 23054113 15; 23054112 15; 23054111 15; 23054110 15 |
| LANDUSE | category | 18 | 0 | Residential 1.3K; Light Industrial 1.1K; Other - Urban Open 152; Other - Transportation Ra 152 |
| ACRES | amount | 3.0K | 0 | 0.01752516 15; 0.01580146 15; 0.01753209 15; 0.01580528 15 |
| LASTUPDATE | date | 1 | 0 | 2022-08-17T17:38:30 3.0K |
| GLOBALID | id | 3.0K | 0 | {E4B7DE1D-F421-4E7C-9934- 15; {F01DF0E2-0179-467A-AB0C- 15; {E487867C-0703-4E1A-9D8B- 15; {808F53A5-5672-49B8-B874- 15 |
| SHAPE_LENGTH | amount | 3.0K | 0 | 87.2448093822832 17; 88.2893210180743 16; 97.1547325354886 16; 127.816773813256 16 |
| SHAPE_AREA | amount | 2.9K | 0 | 474.789464157607 17; 486.267227763868 16; 556.646943189313 16; 789.780781833571 16 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:05:25.18844 3.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4d536b8d-36f9-4cd2-bb7b-5 3.0K |
| SRC_SHA256 | who | 1 | 0 | 7c63b0329438a2f19823ab3fc 3.0K |
