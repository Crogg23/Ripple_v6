# PORTAL_CKA_ANALYZE_BOSTON_0012B002BE

rows 539  columns 17  scan 3.9s

roles: amount 2, audit 2, category 5, date 4, other 4, who 1

## when

CREATIONDATE
  2022       109  ################
  2023        93  ##############
  2024       205  ##############################
  2025        86  #############
  2026        46  #######

EDITDATE
  2022       109  ################
  2023        93  ##############
  2024       205  ##############################
  2025        86  #############
  2026        46  #######

DATE_AND_TIME
  2022       109  ################
  2023        93  ##############
  2024       205  ##############################
  2025        86  #############
  2026        46  #######

INGESTED_AT
  2026       539  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 539 | -71.51 | -71.09 | -71.03 | -71.01 | -38.3K |
| POINT_Y | 539 | 42.24 | 42.34 | 42.39 | 42.49 | 22.8K |

## who

SRC_SHA256 by rows
       539  4c66a4aa71326d18b84d9bf7efc2622b4385a772687de3c490cc5963f35af886

SRC_SHA256 by dollars
      -38.3K      539 rows  4c66a4aa71326d18b84d9bf7efc2622b4385a772687de3c490cc5963f35a

## who x when

SRC_SHA256 by DATE_AND_TIME, dollars = POINT_X
  4c66a4aa71326d18b84d9bf7efc2622b4385a772  2022:-7.7K 2023:-6.6K 2024:-14.6K 2025:-6.1K 2026:-3.3K

## what

CREATOR: dlamere_bowmanconsulting 50%, akleyman_CTPS 25%, 168240_boston 25%

EDITOR: dlamere_bowmanconsulting 50%, akleyman_CTPS 25%, 168240_boston 25%

YOUR_MODE_OF_TRANSPORTATION: walks 51%, bikes 31%, drives 15%, other 3%, uses an assistive device 0%

MODE_OTHER: resident 9%, I have lived at this intersect 9%, I live 3 stops from stop sign  9%, walking and driving 9%, At home 9%, on the 66 bus 9%, From being a local resident 9%, bike/walk 9%, I've seen this occur on a dail 9%, walks/bikes 9%, walk/bike 9%

REQUEST: bikefacility 17%, speeding 15%, other 15%, runlightssigns 12%, yieldturn 10%, visibility 6%, yieldgoing 6%, notenoughtime 5%, doublepark 4%, walksignal 3%, sidewalk 3%, toomanylanes 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GLOBALID | other | 539 | 0 | {A7E36AEE-4624-41BB-87B1- 3; {33172E78-B20A-446E-AD18- 3; {1949FD83-A8BB-414D-951F- 3; {E09F16DB-CC55-405A-BA8F- 3 |
| CREATIONDATE | date | 545 | 0 | 6/17/2026 21:53:11.061 3; 6/12/2026 18:35:09.087 3; 6/12/2026 11:07:29.782 3; 6/10/2026 1:09:24.855 3 |
| CREATOR | category | 4 | 535 | dlamere_bowmanconsulting 2; akleyman_CTPS 1; 168240_boston 1 |
| EDITDATE | date | 545 | 0 | 6/17/2026 21:53:11.061 3; 6/12/2026 18:35:09.087 3; 6/12/2026 11:07:29.782 3; 6/10/2026 1:09:24.855 3 |
| EDITOR | category | 4 | 535 | dlamere_bowmanconsulting 2; akleyman_CTPS 1; 168240_boston 1 |
| DATE_AND_TIME | date | 539 | 0 | 6/17/2026 21:49:00.000 3; 6/12/2026 18:24:00.000 3; 6/12/2026 11:00:00.000 3; 6/10/2026 0:59:00.000 3 |
| YOUR_MODE_OF_TRANSPORTATION | category | 5 | 0 | walks 275; bikes 167; drives 82; other 14 |
| MODE_OTHER | category | 15 | 525 | resident 1; I have lived at this inte 1; I live 3 stops from stop  1; walking and driving 1 |
| REQUEST | category | 14 | 0 | bikefacility 89; speeding 78; other 78; runlightssigns 61 |
| REQUEST_OTHER | other | 58 | 465 | Electronic Billboard 18; Daily near-miss pedestria 1; very confusing intersecti 1; Gas powered mopeds riding 1 |
| ADDITIONAL_COMMENTS | other | 468 | 57 | Digital advertising has b 21; I was nearly hit by a cyc 3; Drivers routinely run the 3; I'm a longtime resident a 3 |
| SHAPE_WKT | other | 511 | 0 | POINT (-71.08699165799998 8; POINT (-71.12539527499996 4; POINT (-71.12623472299998 4; POINT (-71.12477249999994 4 |
| POINT_X | amount | 533 | 0 | -71.086991657999988 8; -71.125395274999960 4; -71.126234722999982 4; -71.124772499999949 4 |
| POINT_Y | amount | 530 | 0 | 42.346302803000071 8; 42.302899799000045 4; 42.301809020000064 4; 42.304398609000032 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:42:51.34670 539 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6be2c143-57cd-41bd-aeba-5 539 |
| SRC_SHA256 | who | 1 | 0 | 4c66a4aa71326d18b84d9bf7e 539 |
