# PORTAL_CKA_WPRDC_ALLEGHENY_224873A888

rows 739  columns 34  scan 4.0s

roles: amount 3, audit 2, category 14, date 1, other 13, who 2

## when

INGESTED_AT
  2026       739  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LENGTH | 739 | 0 | 0 | 438.31 | 1.2K | 9.5K |
| L_FEET | 739 | 0 | 105 | 645.48 | 1.0K | 99.6K |
| SHAPE_LENGTH | 739 | 19.38 | 173.80 | 781.64 | 1.5K | 158.5K |

## who

STREET_NAME by rows
         4  Lappe Lane
         4  56th St
         3  Hawkins St
         3  Westborn St
         3  Wapello St
         3  Hartford St
         3  Belle Isle Ave
         3  Rosetta St
         3  Stetson St
         2  Andick Way
         2  Clover St
         2  Hancock St
         2  Berwick St
         2  Hilltop St
         2  Yarrow St
         2  Mann St
         2  Radcliffe St
         2  Chartiers Ave
         2  Colmar St
         2  Basin St

STREET_NAME by dollars
         977        1 rows  Suffolk St
         887        4 rows  56th St
         826        1 rows  Louisiana Ave
         794        3 rows  Stetson St
         781        1 rows  Jacob St
         715        3 rows  Belle Isle Ave
         693        1 rows  Rising Main Way
         647        1 rows  Sinton Way
         641        2 rows  Irwin Ave
         638        1 rows  Ray Ave
         625        1 rows  Gladstone St
         624        1 rows  Yard Way
         623        2 rows  Basin St
         593        4 rows  Lappe Lane
         572        1 rows  Eckert St
         527        1 rows  Anthony St
         524        1 rows  Graib St
         523        3 rows  Hawkins St
         509        1 rows  Inglenook Place
         500        2 rows  Berwick St

SRC_SHA256 by rows
       739  df8a811234212062df6a849f7243216172099d8fa28444f3e8e50ced9ba49da1

SRC_SHA256 by dollars
       99.6K      739 rows  df8a811234212062df6a849f7243216172099d8fa28444f3e8e50ced9ba4

## who x when

STREET_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = L_FEET
  56th St                                   2026:887
  Andick Way                                2026:42
  Basin St                                  2026:623
  Belle Isle Ave                            2026:715
  Berwick St                                2026:500
  Chartiers Ave                             2026:0
  Clover St                                 2026:234
  Colmar St                                 2026:375
  Eckert St                                 2026:572
  Gladstone St                              2026:625
  Hancock St                                2026:162
  Hartford St                               2026:275
  Hawkins St                                2026:523
  Hilltop St                                2026:378
  Irwin Ave                                 2026:641
  Jacob St                                  2026:781
  Lappe Lane                                2026:593
  Louisiana Ave                             2026:826
  Mann St                                   2026:316
  Radcliffe St                              2026:18
  Ray Ave                                   2026:638
  Rising Main Way                           2026:693
  Rosetta St                                2026:0
  Sinton Way                                2026:647
  Stetson St                                2026:794
  Suffolk St                                2026:977
  Wapello St                                2026:147
  Westborn St                               2026:275
  Yard Way                                  2026:624
  Yarrow St                                 2026:0

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = L_FEET
  df8a811234212062df6a849f7243216172099d8f  2026:99.6K

## what

STREETS: 0 98%, 7926 0%, 15423 0%, 15381 0%, 14871 0%, 13265 0%, 12573 0%, 12401 0%, 12289 0%, 11731 0%, 11715 0%, 11436 0%

STREETS_ID: 0 98%, 13 0%, 600 0%, 11 0%, 175 0%, 294 0%, 206 0%, 27 0%, 351 0%, 592 0%, 451 0%, 276 0%

CODE: 0 67%, 999 31%, 1081 2%

TYPE: 1 49%, 4 15%, 3 14%, 2 10%, 0 4%, 5 3%, 7 2%, 6 2%, 13 1%, 11 0%, 9 0%, 12 0%

DPWN2: 0 69%, 356 6%, 306 4%, 276 4%, 371 4%, 465 2%, 35 2%, 449 2%, 216 2%, 380 2%, 376 2%

STYLE: 1 48%, 3 16%, 4 15%, 2 11%, 5 3%, 6 2%, 7 2%, 13 1%, 12 1%, 11 1%, 10 0%, 9 0%

ANGLE: n 91%, y 9%

SEGS: 1 83%, 2 12%, 3 3%, 4 1%, 5 0%, 0 0%, 7 0%, 6 0%

ST: n 53%, y 46%,  y 0%

INT: n 94%, y 5%,  n 0%

HOOD2: 3 23%, 62 13%, 87 10%, 52 10%, 60 6%, 25 6%, 16 6%, 67 6%, 73 6%, 74 6%, 84 6%

WIDTH: 4 42%, 5 34%, 3 18%, 0 4%, 6 2%, 11 0%, 7 0%, 2 0%, 8 0%, 10 0%, 12 0%

CODED: y 100%

PIX: y 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 721 | 0 | 739 4; 738 4; 737 4; 736 4 |
| LENGTH | amount | 21 | 0 | 0 719; 350.30571 1; 376.00239 1; 640.66402 1 |
| STREETS | category | 22 | 0 | 0 718; 7926 1; 15423 1; 15381 1 |
| STREETS_ID | category | 22 | 0 | 0 718; 13 1; 600 1; 11 1 |
| CODE | category | 3 | 0 | 0 494; 999 232; 1081 13 |
| TYPE | category | 13 | 0 | 1 361; 4 107; 3 105; 2 76 |
| ID_NO | other | 721 | 0 | 739 4; 738 4; 737 4; 736 4 |
| OID | other | 721 | 0 | 737 4; 738 4; 736 4; 735 4 |
| ID | other | 721 | 0 | 739 4; 738 4; 737 4; 736 4 |
| DPWN1 | other | 476 | 0 | 0 253; 342 4; 350 4; 223 3 |
| DPWN2 | category | 43 | 660 | 0 33; 356 3; 306 2; 276 2 |
| LOCATION | other | 598 | 1 | Habermann Ave 8; 56th St 6; Eleanor St 6; Frank St 5 |
| STYLE | category | 13 | 0 | 1 357; 3 115; 4 107; 2 82 |
| ANGLE | category | 3 | 2 | n 674; y 63 |
| SEGS | category | 8 | 0 | 1 616; 2 87; 3 25; 4 4 |
| ST | category | 3 | 0 | n 395; y 342;  y 2 |
| STREET_NAME | who | 339 | 338 | 56th St 4; Lappe Lane 4; Stetson St 4; Belle Isle Ave 4 |
| FROM_STREET | other | 534 | 5 | Arlington Ave 12; Chartiers Ave 9; W Liberty Ave 8; Centre Ave 8 |
| TO_STREET | other | 570 | 45 | Brownsville Rd 9; Arlington Ave 9; end 8; Brookline Blvd 7 |
| INT | category | 3 | 0 | n 698; y 39;  n 2 |
| HOOD | other | 67 | 0 | 73 68; 8 40; 53 35; 14 29 |
| HOOD2 | category | 24 | 696 | 3 7; 62 4; 87 3; 52 3 |
| L_FEET | amount | 299 | 0 | 0 236; 100 7; 12 6; 216 5 |
| WIDTH | category | 11 | 0 | 4 308; 5 253; 3 130; 0 26 |
| STEPS | other | 182 | 0 | 12 15; 26 13; 8 13; 21 12 |
| TREADS | other | 116 | 0 | 0 581; 44 4; 40 4; 67 4 |
| YEAR | other | 55 | 0 | 0 237; 1950 94; 1949 57; 1948 49 |
| CODED | category | 2 | 692 | y 47 |
| PIX | category | 2 | 660 | y 79 |
| COMMENT | other | 160 | 561 | asphalt and brick 7; abandoned 4; asphalt 3; check ROW 3 |
| SHAPE_LENGTH | amount | 742 | 0 | 99.1916658724658 4; 92.4981325681083 4; 132.703549507756 4; 206.105621522317 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:46:12.55949 739 |
| SOURCE_RUN_ID | audit | 1 | 0 | a0e3e85d-5f64-44bd-a1fc-d 739 |
| SRC_SHA256 | who | 1 | 0 | df8a811234212062df6a849f7 739 |
