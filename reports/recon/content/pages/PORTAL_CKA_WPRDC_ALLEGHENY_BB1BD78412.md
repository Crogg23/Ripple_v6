# PORTAL_CKA_WPRDC_ALLEGHENY_BB1BD78412

rows 10.0K  columns 21  scan 5.1s

roles: amount 6, audit 2, category 7, date 1, id 1, other 2, who 3

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CURRENT_DELQ_TAX | 10.0K | 0 | 656.88 | 13.5K | 867.2K | 17.73M |
| CURRENT_DELQ_PI | 10.0K | 0 | 0 | 0 | 1.5K | 3.4K |
| PRIOR_DELQ_TAX | 10.0K | 0 | 0 | 3.1K | 489.3K | 2.31M |
| PRIOR_DELQ_PI | 10.0K | 0 | 0 | 0 | 320.28 | 568.02 |
| LONGITUDE | 9.9K | -80.08 | -79.98 | -79.88 | -79.87 | -791.0K |
| LATITUDE | 9.9K | 40.36 | 40.44 | 40.49 | 40.50 | 399.9K |

## who

NEIGHBORHOOD by rows
       599  Brookline
       560  Carrick
       514  Beechview
       462  Bloomfield
       319  Brighton Heights
       246  Central Lawrenceville
       234  Mount Washington
       220  Squirrel Hill South
       209  South Side Slopes
       199  Hazelwood
       197  Marshall-Shadeland
       197  Greenfield
       196  Beltzhoover
       194  South Side Flats
       194  Allentown
       191  Shadyside
       187  Perry South
       180  Central Business District
       167  Lincoln-Lemington-Belmar
       166  Garfield

NEIGHBORHOOD by dollars
       1.93M      180 rows  Central Business District
       1.24M      101 rows  Bluff
      789.2K      191 rows  Shadyside
      776.3K      462 rows  Bloomfield
      691.2K       68 rows  North Oakland
      660.2K      194 rows  South Side Flats
      649.1K      220 rows  Squirrel Hill South
      648.7K      120 rows  Squirrel Hill North
      610.0K      599 rows  Brookline
      532.4K       75 rows  Central Oakland
      491.0K      560 rows  Carrick
      482.2K      514 rows  Beechview
      437.5K       36 rows  Strip District
      410.9K       76 rows  Crawford-Roberts
      410.4K      246 rows  Central Lawrenceville
      403.1K        3 rows  Northview Heights
      344.5K      234 rows  Mount Washington
      327.0K      104 rows  Point Breeze
      312.7K      100 rows  East Liberty
      299.4K      197 rows  Greenfield

BILLING_CITY by rows
      7.4K  PITTSBURGH, PA
       405  IRVING, TX
        83  ALLISON PARK, PA
        76  HOMESTEAD, PA
        66  MONROEVILLE, PA
        63  POMONA, CA
        54  SEWICKLEY, PA
        48  TRAFFORD, PA
        45  DES MOINES, IA
        39  BETHEL PARK, PA
        39  MC KEES ROCKS, PA
        38  CRANBERRY TWP, PA
        38  CANONSBURG, PA
        38  WEXFORD, PA
        34  CARNEGIE, PA
        30  BRIDGEVILLE, PA
        26  MARS, PA
        26  GIBSONIA, PA
        25  OAKDALE, PA
        24  SOUTH PARK, PA

BILLING_CITY by dollars
      11.46M     7.4K rows  PITTSBURGH, PA
       1.06M        6 rows  KING OF PRUSSI, PA
      600.1K      405 rows  IRVING, TX
      177.8K        7 rows  LOS ANGELES, CA
      176.2K       83 rows  ALLISON PARK, PA
      166.9K        2 rows  BEDMINSTER, NJ
      149.6K       22 rows  NEW YORK, NY
      145.3K        9 rows  PHILADELPHIA, PA
      139.6K        8 rows  DALLAS, TX
      131.7K       11 rows  BALTIMORE, MD
      115.5K       66 rows  MONROEVILLE, PA
      100.6K       26 rows  MARS, PA
       99.3K        5 rows  BOSTON, MA
       92.2K        3 rows  SEATTLE, WA
       91.0K       30 rows  BRIDGEVILLE, PA
       87.4K       63 rows  POMONA, CA
       77.2K       76 rows  HOMESTEAD, PA
       74.0K       38 rows  WEXFORD, PA
       71.7K       34 rows  CARNEGIE, PA
       71.1K       45 rows  DES MOINES, IA

SRC_SHA256 by rows
     10.0K  0eeb4bb0dd5437f7c3251807a8984ad3f72334724a25e288633bec5e517c44a8

SRC_SHA256 by dollars
      17.73M    10.0K rows  0eeb4bb0dd5437f7c3251807a8984ad3f72334724a25e288633bec5e517c

## who x when

NEIGHBORHOOD by INGESTED_AT  LOAD STAMP, not an event date, dollars = CURRENT_DELQ_TAX
  Allentown                                 2026:65.6K
  Beechview                                 2026:482.2K
  Beltzhoover                               2026:63.8K
  Bloomfield                                2026:776.3K
  Bluff                                     2026:1.24M
  Brighton Heights                          2026:250.3K
  Brookline                                 2026:610.0K
  Carrick                                   2026:491.0K
  Central Business District                 2026:1.93M
  Central Lawrenceville                     2026:410.4K
  Central Oakland                           2026:532.4K
  Crawford-Roberts                          2026:410.9K
  East Liberty                              2026:312.7K
  Garfield                                  2026:168.6K
  Greenfield                                2026:299.4K
  Hazelwood                                 2026:106.9K
  Lincoln-Lemington-Belmar                  2026:96.3K
  Marshall-Shadeland                        2026:121.6K
  Mount Washington                          2026:344.5K
  North Oakland                             2026:691.2K
  Northview Heights                         2026:403.1K
  Perry South                               2026:110.3K
  Point Breeze                              2026:327.0K
  Shadyside                                 2026:789.2K
  South Side Flats                          2026:660.2K
  South Side Slopes                         2026:236.0K
  Squirrel Hill North                       2026:648.7K
  Squirrel Hill South                       2026:649.1K
  Strip District                            2026:437.5K

BILLING_CITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = CURRENT_DELQ_TAX
  ALLISON PARK, PA                          2026:176.2K
  BALTIMORE, MD                             2026:131.7K
  BEDMINSTER, NJ                            2026:166.9K
  BETHEL PARK, PA                           2026:46.0K
  BOSTON, MA                                2026:99.3K
  BRIDGEVILLE, PA                           2026:91.0K
  CANONSBURG, PA                            2026:70.8K
  CARNEGIE, PA                              2026:71.7K
  CRANBERRY TWP, PA                         2026:42.6K
  DALLAS, TX                                2026:139.6K
  DES MOINES, IA                            2026:71.1K
  GIBSONIA, PA                              2026:48.2K
  HOMESTEAD, PA                             2026:77.2K
  IRVING, TX                                2026:600.1K
  KING OF PRUSSI, PA                        2026:1.06M
  LOS ANGELES, CA                           2026:177.8K
  MARS, PA                                  2026:100.6K
  MC KEES ROCKS, PA                         2026:30.7K
  MONROEVILLE, PA                           2026:115.5K
  NEW YORK, NY                              2026:149.6K
  OAKDALE, PA                               2026:28.7K
  PHILADELPHIA, PA                          2026:145.3K
  PITTSBURGH, PA                            2026:11.46M
  POMONA, CA                                2026:87.4K
  SEATTLE, WA                               2026:92.2K
  SEWICKLEY, PA                             2026:45.8K
  SOUTH PARK, PA                            2026:17.6K
  TRAFFORD, PA                              2026:38.6K
  WEXFORD, PA                               2026:74.0K

## what

PRIOR_YEARS: 0 82%, 1 18%

STATE_DESCRIPTION: Residential 88%, Commercial 11%, Industrial 1%, Gov't Owned 0%, Other 0%, Utilities 0%

COUNCIL_DISTRICT: 4 18%, 3 14%, 1 12%, 7 12%, 6 12%, 9 11%, 2 10%, 5 9%, 8 4%

WARD: 19 20%, 29 9%, 14 9%, 27 8%, 20 8%, 18 8%, 16 7%, 15 6%, 8 6%, 10 6%, 9 6%, 26 5%

PUBLIC_WORKS_DIVISION: 4 27%, 2 23%, 1 19%, 3 16%, 5 15%

PLI_DIVISION: 19 20%, 29 9%, 14 9%, 27 8%, 20 8%, 18 8%, 16 7%, 15 6%, 8 6%, 10 6%, 9 6%, 26 5%

POLICE_ZONE: 3 22%, 6 18%, 1 16%, 5 16%, 4 16%, 2 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PIN | id | 9.9K | 0 | 0049B00234000000 50; 0080P00071000000 50; 0080F00148000000 50; 0049G00086000000 50 |
| ADDRESS | other | 9.2K | 0 | 514 3RD AVE 52; 1821 BRIGHTON RD 52; 42ND ST 51; 628 SMITHFIELD ST 51 |
| BILLING_CITY | who | 508 | 0 | PITTSBURGH, PA 7.4K; IRVING, TX 405; ALLISON PARK, PA 83; HOMESTEAD, PA 76 |
| CURRENT_DELQ_TAX | amount | 6.0K | 0 | 0.0 924; 31.33 70; 20.88 51; 8334.09 48 |
| CURRENT_DELQ_PI | amount | 56 | 0 | 0.0 9.9K; 0.26 2; 1.18 2; 12.68 1 |
| PRIOR_YEARS | category | 2 | 0 | 0 8.2K; 1 1.8K |
| PRIOR_DELQ_TAX | amount | 1.6K | 0 | 0.0 8.2K; 28.6 30; 148.67 11; 0.01 10 |
| PRIOR_DELQ_PI | amount | 5 | 0 | 0.0 10.0K; 17.8 1; 34.59 1; 195.35 1 |
| STATE_DESCRIPTION | category | 6 | 0 | Residential 8.8K; Commercial 1.1K; Industrial 53; Gov't Owned 48 |
| NEIGHBORHOOD | who | 92 | 16 | Brookline 599; Carrick 560; Beechview 514; Bloomfield 462 |
| COUNCIL_DISTRICT | category | 10 | 112 | 4 1.8K; 3 1.4K; 1 1.2K; 7 1.2K |
| WARD | category | 33 | 112 | 19 1.2K; 29 552; 14 546; 27 512 |
| PUBLIC_WORKS_DIVISION | category | 6 | 111 | 4 2.6K; 2 2.3K; 1 1.9K; 3 1.5K |
| PLI_DIVISION | category | 33 | 112 | 19 1.2K; 29 552; 14 546; 27 512 |
| POLICE_ZONE | category | 7 | 112 | 3 2.2K; 6 1.8K; 1 1.6K; 5 1.6K |
| FIRE_ZONE | other | 94 | 112 | 4-28 508; 1-14 488; 4-26 474; 4-23 285 |
| LONGITUDE | amount | 9.9K | 110 | -80.0071933155924 51; -79.95998398605238 50; -79.96085779884038 50; -79.95807916033246 50 |
| LATITUDE | amount | 9.8K | 110 | 40.44244131300167 51; 40.47072022483473 50; 40.472987077703856 50; 40.47765107119047 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:51:05.57390 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5e8d0194-2caf-4b1c-810d-4 10.0K |
| SRC_SHA256 | who | 1 | 0 | 0eeb4bb0dd5437f7c3251807a 10.0K |
