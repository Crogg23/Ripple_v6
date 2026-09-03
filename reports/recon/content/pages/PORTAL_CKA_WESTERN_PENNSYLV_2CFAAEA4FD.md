# PORTAL_CKA_WESTERN_PENNSYLV_2CFAAEA4FD

rows 138  columns 35  scan 5.7s

roles: amount 10, audit 2, category 7, date 1, other 14, who 2

## when

INGESTED_AT
  2026       138  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 138 | 335.1K | 1.49M | 6.25M | 11.58M | 249.49M |
| SHAPE__LENGTH | 138 | 2.5K | 6.4K | 14.1K | 37.1K | 969.7K |
| ACRES | 138 | 68.30 | 451.41 | 1.7K | 1.7K | 73.0K |
| INTPTLAT10 | 138 | 40.37 | 40.45 | 40.49 | 40.49 | 5.6K |
| INTPTLON10 | 138 | -80.08 | -79.96 | -79.89 | -79.88 | -11.0K |
| LOWMODPERCANNO | 138 | 0 | 57.48 | 99.31 | 100 | 7.5K |

## who

HOOD by rows
         5  Squirrel Hill South
         5  Bloomfield
         5  Shadyside
         4  Lincoln-Lemington-Belmar
         4  Brookline
         4  Mount Washington
         3  Perry North
         3  Brighton Heights
         3  North Oakland
         3  Squirrel Hill North
         3  Garfield
         3  Point Breeze
         3  Marshall-Shadeland
         3  Highland Park
         3  Carrick
         3  Central Lawrenceville
         2  Beechview
         2  Overbrook
         2  Central Oakland
         2  East Liberty

HOOD by dollars
      16.94M        2 rows  Hazelwood
      11.95M        5 rows  Squirrel Hill South
       9.30M        4 rows  Brookline
       8.11M        4 rows  Lincoln-Lemington-Belmar
       7.48M        3 rows  Carrick
       6.77M        1 rows  Windgap
       6.53M        2 rows  Beechview
       5.62M        3 rows  Marshall-Shadeland
       5.47M        3 rows  Squirrel Hill North
       5.42M        3 rows  Perry North
       5.21M        3 rows  Highland Park
       5.10M        4 rows  Mount Washington
       5.01M        2 rows  Sheraden
       5.01M        3 rows  Brighton Heights
       4.73M        1 rows  Westwood
       4.50M        3 rows  Point Breeze
       4.39M        1 rows  Lincoln Place
       4.33M        1 rows  Banksville
       4.32M        3 rows  Central Lawrenceville
       4.19M        2 rows  South Side Flats

SRC_SHA256 by rows
       138  b0d18a79ee510602165ae69e35dae293ce567778de1866ecec1a8e4dc25ff5de

SRC_SHA256 by dollars
     249.49M      138 rows  b0d18a79ee510602165ae69e35dae293ce567778de1866ecec1a8e4dc25f

## who x when

HOOD by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Banksville                                2026:4.33M
  Beechview                                 2026:6.53M
  Bloomfield                                2026:3.14M
  Brighton Heights                          2026:5.01M
  Brookline                                 2026:9.30M
  Carrick                                   2026:7.48M
  Central Lawrenceville                     2026:4.32M
  Central Oakland                           2026:1.26M
  East Liberty                              2026:2.60M
  Garfield                                  2026:2.05M
  Hazelwood                                 2026:16.94M
  Highland Park                             2026:5.21M
  Lincoln Place                             2026:4.39M
  Lincoln-Lemington-Belmar                  2026:8.11M
  Marshall-Shadeland                        2026:5.62M
  Mount Washington                          2026:5.10M
  North Oakland                             2026:2.23M
  Overbrook                                 2026:3.75M
  Perry North                               2026:5.42M
  Point Breeze                              2026:4.50M
  Shadyside                                 2026:4.12M
  Sheraden                                  2026:5.01M
  South Side Flats                          2026:4.19M
  Squirrel Hill North                       2026:5.47M
  Squirrel Hill South                       2026:11.95M
  Westwood                                  2026:4.73M
  Windgap                                   2026:6.77M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  b0d18a79ee510602165ae69e35dae293ce567778  2026:249.49M

## what

AWATER10: 0 92%, 163596 1%, 854869 1%, 131921 1%, 282865 1%, 8799 1%, 4114 1%, 473795 1%, 156623 1%, 416134 1%, 115879 1%, 252755 1%

BLKGRPCE10: 2 36%, 1 36%, 3 20%, 4 7%, 5 2%

CDBG2014: Yes 51%, No 49%

CDBG2018: Yes 61%, No 39%

CNT_TRACTCE10: 2 35%, 3 25%, 1 19%, 4 12%, 5 5%, 6 3%, 7 1%

NAMELSAD10: Block Group 2 36%, Block Group 1 36%, Block Group 3 20%, Block Group 4 7%, Block Group 5 2%

SECTORS: 12 18%, 10 11%, 5 10%, 2 9%, 11 9%, 13 7%, 14 7%, 3 7%, 4 7%, 6 7%, 15 6%, 7 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SHAPE__AREA | amount | 139 | 0 | 676426.7578125 1; 683966.44140625 1; 972157.734375 1; 2514798.92578125 1 |
| SHAPE__LENGTH | amount | 138 | 0 | 6278.71428843785 1; 3632.1948111435 1; 4691.52370965652 1; 11988.8793914627 1 |
| ACRES | amount | 81 | 0 | 1717.485 5; 592.104 5; 451.405 5; 1338.669 4 |
| ALAND10 | other | 136 | 0 | 400091 1; 395541 1; 560320 1; 1453388 1 |
| AWATER10 | category | 19 | 0 | 0 120; 163596 1; 854869 1; 131921 1 |
| BLKGRPCE10 | category | 5 | 0 | 2 50; 1 49; 3 27; 4 9 |
| CDBG2014 | category | 2 | 0 | Yes 71; No 67 |
| CDBG2018 | category | 2 | 0 | Yes 84; No 54 |
| CNT_TRACTCE10 | category | 7 | 0 | 2 48; 3 35; 1 26; 4 17 |
| COUNTYFP10 | other | 1 | 0 | 003 138 |
| FUNCSTAT10 | other | 1 | 0 | S 138 |
| GEOID10 | other | 139 | 0 | 420039808001 1; 420032704001 1; 420032507001 1; 420039809001 1 |
| HOOD | who | 80 | 0 | Squirrel Hill South 5; Shadyside 5; Bloomfield 5; Lincoln-Lemington-Belmar 4 |
| HOOD_NO | other | 79 | 0 | 77 5; 68 5; 10 5; 47 4 |
| INTPTLAT10 | amount | 138 | 0 | 40.4341374 1; 40.4654064 1; 40.4599421 1; 40.4659231 1 |
| INTPTLON10 | amount | 137 | 0 | -79.9683957 1; -80.0285012 1; -80.0218657 1; -80.0458881 1 |
| LOWMODPERCANNO | amount | 128 | 0 | 0.0 10; 100.0 2; 65.21 1; 72.54 1 |
| LOWMODPERCT | amount | 128 | 0 | 0.0 10; 100.0 2; 65.2173913 1; 72.54901961 1 |
| MTFCC10 | other | 1 | 0 | G5030 138 |
| NAMELSAD10 | category | 5 | 0 | Block Group 2 50; Block Group 1 49; Block Group 3 27; Block Group 4 9 |
| OBJECTID | other | 137 | 0 | 138 1; 137 1; 136 1; 135 1 |
| OBJECTID_1 | other | 137 | 0 | 132 1; 96 1; 85 1; 133 1 |
| SECTORS | category | 17 | 0 | 12 22; 10 13; 5 12; 2 11 |
| SQMILES | amount | 80 | 0 | 2.671 5; 0.921 5; 0.702 5; 2.082 4 |
| STATEFP10 | other | 1 | 0 | 42 138 |
| SUM_LOWMOD2018 | amount | 114 | 0 | 0 10; 1025 3; 760 3; 945 2 |
| SUM_LOWMODUNIV | amount | 112 | 0 | 0 10; 2525 3; 1035 2; 1730 2 |
| TRACT | other | 136 | 0 | 9808 1; 2704 1; 2507 1; 9809 1 |
| TRACTCE10 | other | 136 | 0 | 980800 1; 270400 1; 250700 1; 980900 1 |
| TRACTCE10_1 | other | 136 | 0 | 980800 1; 270400 1; 250700 1; 980900 1 |
| TRACTTEXT | other | 139 | 0 | 9808 1; 2704 1; 2507 1; 9809 1 |
| GEOMETRY | other | 138 | 0 | POLYGON ((587353.70766711 1; POLYGON ((582507.60963466 1; POLYGON ((583052.60711105 1; MULTIPOLYGON (((581663.04 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:34:51.22106 138 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2fc69cf0-c339-409c-9da5-b 138 |
| SRC_SHA256 | who | 1 | 0 | b0d18a79ee510602165ae69e3 138 |
