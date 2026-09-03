# PORTAL_CKA_WPRDC_ALLEGHENY_4F79FA2E0C

rows 71  columns 9  scan 4.4s

roles: amount 2, audit 2, category 1, date 1, other 2, who 2

## when

INGESTED_AT
  2026        71  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_AREA | 71 | 374.1K | 2.85M | 19.71M | 26.14M | 313.98M |
| SHAPE_LENGTH | 71 | 2.8K | 9.4K | 52.9K | 57.0K | 858.1K |

## who

AREA_NAME by rows
         2  Area 51
         2  Area 50
         1  Area 62
         1  Area 56
         1  Area 06
         1  Area 18
         1  Area 20
         1  Area 43
         1  Area 57
         1  Area 48a
         1  Area 41
         1  Area 48b
         1  Area 45
         1  Area 63
         1  Area 14
         1  Area 11
         1  Area 21
         1  Area 04
         1  Area 07
         1  Area 03

AREA_NAME by dollars
      26.14M        1 rows  Area 19
      16.95M        1 rows  Area 56
      14.74M        1 rows  Area 35
      13.96M        1 rows  Area 55
      12.69M        1 rows  Area 20
      11.69M        1 rows  Area 09
      11.54M        1 rows  Area 52
       9.63M        1 rows  Area 30
       9.54M        1 rows  Area 39
       9.20M        1 rows  Area 47
       8.61M        1 rows  Area 02
       8.27M        2 rows  Area 50
       8.01M        1 rows  Area 61
       7.42M        1 rows  Area 36a
       6.68M        1 rows  Area 36c
       6.65M        1 rows  Area 10
       5.90M        1 rows  Area 37
       5.70M        1 rows  Area 28
       5.25M        1 rows  Area 15
       5.12M        1 rows  Area 29

SRC_SHA256 by rows
        71  e095386d2b0fc29e9e8484c9af59f7b4846e71f420e5a2ea3f0c18a28201c043

SRC_SHA256 by dollars
     313.98M       71 rows  e095386d2b0fc29e9e8484c9af59f7b4846e71f420e5a2ea3f0c18a28201

## who x when

AREA_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  Area 02                                   2026:8.61M
  Area 03                                   2026:3.67M
  Area 04                                   2026:1.89M
  Area 06                                   2026:1.79M
  Area 07                                   2026:447.4K
  Area 09                                   2026:11.69M
  Area 11                                   2026:4.40M
  Area 14                                   2026:717.8K
  Area 18                                   2026:2.25M
  Area 19                                   2026:26.14M
  Area 20                                   2026:12.69M
  Area 21                                   2026:2.70M
  Area 30                                   2026:9.63M
  Area 35                                   2026:14.74M
  Area 39                                   2026:9.54M
  Area 41                                   2026:3.11M
  Area 43                                   2026:1.78M
  Area 45                                   2026:1.42M
  Area 47                                   2026:9.20M
  Area 48a                                  2026:1.35M
  Area 48b                                  2026:1.90M
  Area 50                                   2026:8.27M
  Area 51                                   2026:3.66M
  Area 52                                   2026:11.54M
  Area 55                                   2026:13.96M
  Area 56                                   2026:16.95M
  Area 57                                   2026:1.60M
  Area 61                                   2026:8.01M
  Area 62                                   2026:2.11M
  Area 63                                   2026:1.00M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  e095386d2b0fc29e9e8484c9af59f7b4846e71f4  2026:313.98M

## what

RENEWAL_TYPE: M 45%, E 32%, P 23%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA_NAME | who | 69 | 0 | Area 51 2; Area 50 2; Area 59 1; Area 31 1 |
| OBJECTID | other | 71 | 0 | 72 1; 71 1; 70 1; 69 1 |
| RENEWAL_TYPE | category | 3 | 0 | M 32; E 23; P 16 |
| SHAPE_AREA | amount | 72 | 0 | 1004043.9993796679 1; 2592751.044474084 1; 26140341.47204691 1; 2697445.1201032302 1 |
| SHAPE_LENGTH | amount | 72 | 0 | 5096.816713271675 1; 9380.304689642175 1; 32530.04689104461 1; 8735.051428304683 1 |
| GEOMETRY | other | 71 | 0 | POLYGON ((590245.11520977 1; POLYGON ((580681.46623960 1; POLYGON ((578275.19112300 1; POLYGON ((578321.89968323 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:29:05.74110 71 |
| SOURCE_RUN_ID | audit | 1 | 0 | 25112b71-e7b4-4256-9df5-d 71 |
| SRC_SHA256 | who | 1 | 0 | e095386d2b0fc29e9e8484c9a 71 |
