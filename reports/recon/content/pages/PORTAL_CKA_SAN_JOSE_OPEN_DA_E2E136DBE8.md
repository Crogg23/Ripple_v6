# PORTAL_CKA_SAN_JOSE_OPEN_DA_E2E136DBE8

rows 789  columns 26  scan 5.4s

roles: amount 6, audit 2, category 9, date 1, empty 1, other 5, who 3

## when

INGESTED_AT
  2026       789  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 789 | 6.12M | 6.16M | 6.19M | 6.20M | 4.86B |
| Y | 789 | 1.90M | 1.95M | 1.98M | 1.98M | 1.54B |
| DEMELEV | 727 | 3.05 | 90.76 | 562.76 | 623.84 | 89.1K |
| INVERTELEV | 74 | 14 | 91 | 666.27 | 667 | 13.7K |
| LATITUDE | 789 | 37.21 | 37.34 | 37.43 | 37.43 | 29.5K |
| LONGITUDE | 789 | -122.03 | -121.90 | -121.79 | -121.75 | -96.2K |

## who

FACILITYID by rows
         1  15066
         1  807670
         1  74060
         1  35271
         1  808234
         1  807669
         1  15178
         1  34046
         1  807267
         1  34052
         1  803211
         1  33919
         1  6440
         1  15241
         1  807977
         1  48
         1  34787
         1  35324
         1  2170
         1  2775

FACILITYID by dollars
       6.20M        1 rows  807087
       6.20M        1 rows  4036
       6.20M        1 rows  807090
       6.19M        1 rows  807091
       6.19M        1 rows  807092
       6.19M        1 rows  13278
       6.19M        1 rows  13277
       6.19M        1 rows  800005
       6.19M        1 rows  72922
       6.19M        1 rows  13572
       6.19M        1 rows  13571
       6.18M        1 rows  19900
       6.18M        1 rows  807132
       6.18M        1 rows  807308
       6.18M        1 rows  807309
       6.18M        1 rows  807310
       6.18M        1 rows  50855
       6.18M        1 rows  807175
       6.18M        1 rows  807176
       6.18M        1 rows  18166

NOTES by rows
        22  Caltrans Plan Route 880
        12  CPMS10294: FID request
        11  HD159415: Abandoned
         9  CALTRANS PLAN CONTRACT#04-487071 (D-10014)
         8  Removed by Airport TAXIWAY Project,D-2015
         8  UIF: HD210192
         7  3-16680H: Abandoned
         7  Abandon
         6  Removed by Airport TAXIWAY Project, D-2015
         6  SJ Airport GIS System (D-1982)
         5  Abandoned per CPMS6903
         5  CPMS2963(D-1983), Removed by others
         4  CPMS4880: Abandoned
         4  VTA-C830: Abandon
         4  Abandoned
         3  D-2056
         3  025824: Abandon
         3  INC0011824: Abandon
         3  CPMS10095: Abandon
         3  3-18854: Abandoned;

NOTES by dollars
     135.30M       22 rows  Caltrans Plan Route 880
      73.78M       12 rows  CPMS10294: FID request
      67.96M       11 rows  HD159415: Abandoned
      55.40M        9 rows  CALTRANS PLAN CONTRACT#04-487071 (D-10014)
      49.24M        8 rows  UIF: HD210192
      49.19M        8 rows  Removed by Airport TAXIWAY Project,D-2015
      43.17M        7 rows  Abandon
      43.11M        7 rows  3-16680H: Abandoned
      36.89M        6 rows  Removed by Airport TAXIWAY Project, D-2015
      36.87M        6 rows  SJ Airport GIS System (D-1982)
      30.85M        5 rows  CPMS2963(D-1983), Removed by others
      30.77M        5 rows  Abandoned per CPMS6903
      24.68M        4 rows  Abandoned
      24.67M        4 rows  VTA-C830: Abandon
      24.61M        4 rows  CPMS4880: Abandoned
      18.51M        3 rows  INC0011824: Abandon
      18.49M        3 rows  Abandoned.
      18.48M        3 rows  UIF: HD126872
      18.47M        3 rows  UIF: INC0044466
      18.47M        3 rows  CPMS10095: Abandon

SRC_SHA256 by rows
       789  6507c5601246c6a14efc64ef89e9b3d9251315b2ffbc5f880a4654b79fd895b2

SRC_SHA256 by dollars
       4.86B      789 rows  6507c5601246c6a14efc64ef89e9b3d9251315b2ffbc5f880a4654b79fd8

## who x when

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  13277                                     2026:6.19M
  13278                                     2026:6.19M
  13572                                     2026:6.19M
  15066                                     2026:6.16M
  15178                                     2026:6.16M
  15241                                     2026:6.16M
  2170                                      2026:6.15M
  2775                                      2026:6.16M
  33919                                     2026:6.14M
  34046                                     2026:6.14M
  34052                                     2026:6.14M
  34787                                     2026:6.14M
  35271                                     2026:6.15M
  35324                                     2026:6.15M
  4036                                      2026:6.20M
  48                                        2026:6.15M
  6440                                      2026:6.17M
  72922                                     2026:6.19M
  74060                                     2026:6.16M
  800005                                    2026:6.19M
  803211                                    2026:6.14M
  807087                                    2026:6.20M
  807090                                    2026:6.20M
  807091                                    2026:6.19M
  807092                                    2026:6.19M
  807267                                    2026:6.17M
  807669                                    2026:6.15M
  807670                                    2026:6.15M
  807977                                    2026:6.15M
  808234                                    2026:6.16M

NOTES by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  025824: Abandon                           2026:18.46M
  3-16680H: Abandoned                       2026:43.11M
  3-18854: Abandoned;                       2026:18.44M
  Abandon                                   2026:43.17M
  Abandoned                                 2026:24.68M
  Abandoned per CPMS6903                    2026:30.77M
  Abandoned.                                2026:18.49M
  CALTRANS PLAN CONTRACT#04-487071 (D-1001  2026:55.40M
  CPMS10095: Abandon                        2026:18.47M
  CPMS10294: FID request                    2026:73.78M
  CPMS2963(D-1983), Removed by others       2026:30.85M
  CPMS4880: Abandoned                       2026:24.61M
  Caltrans Plan Route 880                   2026:135.30M
  D-2056                                    2026:18.46M
  HD159415: Abandoned                       2026:67.96M
  INC0011824: Abandon                       2026:18.51M
  Removed by Airport TAXIWAY Project, D-20  2026:36.89M
  Removed by Airport TAXIWAY Project,D-201  2026:49.19M
  SJ Airport GIS System (D-1982)            2026:36.87M
  UIF: HD126872                             2026:18.48M
  UIF: HD210192                             2026:49.24M
  UIF: INC0044466                           2026:18.47M
  VTA-C830: Abandon                         2026:24.67M

## what

MHTYPE: STD 53%, UNK 44%, SY 3%, DRP 0%, GST 0%

WALLMAT: RCP 55%, UNK 45%, CP 0%

REHABYEAR: 2017 100%

INSTALLYEAR: 1963 55%, 1966 15%, 2016 10%, 2012 10%, 2002 5%, 1980 5%

SOURCEYEAR: MAGE 83%, ABPL 17%

PLANCRT: UNK 95%, CPMS10294 2%, TR3319 1%, PP0805  0%, MGE 0%, CPMS10132 0%, PP3151 0%, CPMS6310 0%, 3-15699B 0%, CPMS6723 0%, 3-12898 0%

PLANMOD: CPMS6403 22%, 3-16680H 12%, CPMS6903 10%, CPMS6391 10%, HD79262 8%, CPMS4880 8%, 3-18854 7%, CPMS8746 7%, VTA-C830 7%, CPMS7233 5%, HD80090 5%

PLANREF: INC0090372 26%, HD159415 22%, HD127902 10%, HD118677 10%, INC0011824 6%, HD194454 6%, INC0146319 6%, INC0217733 4%, HD121064 4%, HD85444 4%, HD74333 2%

CREATIONDATE: 1900/01/01 00:00:00+00 97%, 2025/02/06 21:15:13+00 1%, 2025/02/06 21:06:20+00 0%, 2024/05/09 16:15:08+00 0%, 2025/02/06 21:27:32+00 0%, 2025/02/06 21:23:18+00 0%, 2025/02/05 22:33:45+00 0%, 2025/11/18 15:29:23+00 0%, 2025/11/18 15:29:04+00 0%, 2025/02/06 21:10:58+00 0%, 2025/02/06 18:59:18+00 0%, 2025/02/06 18:28:03+00 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 766 | 0 | 6178183.90553991 6; 6175407.93012075 4; 6175528.31734717 4; 6146698.79364149 4 |
| Y | amount | 780 | 0 | 1970559.60217707 5; 1971013.76432648 4; 1970732.51981023 4; 1935735.79879332 4 |
| OBJECTID | other | 782 | 0 | 338555 4; 338554 4; 338078 4; 338077 4 |
| FACILITYID | who | 763 | 0 | 1002434 4; 1002433 4; 1002351 4; 1002350 4 |
| INTID | other | 763 | 0 | 1002434 4; 1002433 4; 1002351 4; 1002350 4 |
| DEMELEV | amount | 709 | 62 | 168.34 4; 76.6 4; 96.64 4; 83.73 4 |
| RIMELEV | other | 135 | 583 | 89 7; 150 6; 212 6; 91 4 |
| INVERTELEV | amount | 62 | 715 | 62 4; 84 3; 644.8 2; 635 2 |
| MHTYPE | category | 5 | 0 | STD 419; UNK 344; SY 22; DRP 3 |
| CVTYPE | empty | 1 | 789 |  |
| WALLMAT | category | 3 | 0 | RCP 432; UNK 356; CP 1 |
| OWNEDBY | other | 1 | 0 | SJ 789 |
| REHABYEAR | category | 2 | 788 | 2017 1 |
| INSTALLYEAR | category | 7 | 769 | 1963 11; 1966 3; 2016 2; 2012 2 |
| SOURCEYEAR | category | 3 | 736 | MAGE 44; ABPL 9 |
| PLANCRT | category | 15 | 2 | UNK 744; CPMS10294 14; TR3319 11; PP0805  3 |
| PLANMOD | category | 45 | 676 | CPMS6403 13; 3-16680H 7; CPMS6903 6; CPMS6391 6 |
| LASTUPDATE | other | 476 | 0 | 2006/04/28 13:56:53+00 19; 2006/04/28 13:56:51+00 19; 2006/04/28 13:52:15+00 17; 2006/04/28 13:56:52+00 16 |
| NOTES | who | 110 | 534 | Caltrans Plan Route 880 22; CPMS10294: FID request 12; HD159415: Abandoned 11; CALTRANS PLAN CONTRACT#04 9 |
| PLANREF | category | 29 | 722 | INC0090372 13; HD159415 11; HD127902 5; HD118677 5 |
| LATITUDE | amount | 775 | 0 | 37.300693 5; 37.400424 4; 37.399657 4; 37.302384 4 |
| LONGITUDE | amount | 795 | 0 | -121.894629 5; -121.829776 4; -121.829348 4; -121.926747 4 |
| CREATIONDATE | category | 12 | 0 | 1900/01/01 00:00:00+00 768; 2025/02/06 21:15:13+00 4; 2025/02/06 21:06:20+00 3; 2024/05/09 16:15:08+00 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:47:11.13158 789 |
| SOURCE_RUN_ID | audit | 1 | 0 | 40a71816-38c5-45d4-a3f0-7 789 |
| SRC_SHA256 | who | 1 | 0 | 6507c5601246c6a14efc64ef8 789 |
