# PORTAL_CKA_SAN_JOSE_OPEN_DA_2789EF054E

rows 6.5K  columns 42  scan 4.8s

roles: amount 3, audit 2, category 16, date 3, empty 1, id 4, other 8, who 6

## when

LASTUPDATE
  2019      5.6K  ##############################
  2020       229  #
  2021       187  #
  2022       376  ##
  2023       106  #
  2024         7  

CREATIONDATE
  1900      6.5K  ##############################
  2023         2  
  2024         3  

INGESTED_AT
  2026      6.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FOCWIDTH | 6.2K | 0 | 28.40 | 69.63 | 119.10 | 184.4K |
| ROWWIDTH | 6.3K | 0 | 46.50 | 87.67 | 139.10 | 280.1K |
| SHAPE_LENGTH | 6.5K | 2.87 | 189.16 | 1.9K | 14.8K | 2.08M |

## who

FULLNAME by rows
       300  New Street
       194  Rural Access
        51  Chateau La Salle Dr
        36  Pepper Tree Estates MHP Access
        32  Quimby Rd
        31  Kenbrook Cir
        27  San Jose MHP Access
        27  The Villages Fairway Dr
        26  Vista Roma Way
        26  Mill Pond Dr
        23  Mill River Ln
        23  Mountain Springs Dr
        23  Golden Wheel MHP Access
        22  Oakbridge Dr
        22  Cribari Ln
        20  Checkers Dr APT Access
        19  South Bay MHP Access
        19  Fairbanks Cir
        18  Ribisi Cir
        17  Villa Teresa Way

FULLNAME by dollars
      162.2K      194 rows  Rural Access
      132.5K      300 rows  New Street
       22.0K       27 rows  The Villages Fairway Dr
       16.4K       51 rows  Chateau La Salle Dr
       15.4K       16 rows  The Villages Pkwy
       14.8K        1 rows  Road L
       12.9K       17 rows  Country Club Pkwy
       11.2K       26 rows  Mill Pond Dr
        9.4K        2 rows  Bike Path
        8.6K        3 rows  San Felipe Rd
        8.6K       36 rows  Pepper Tree Estates MHP Access
        8.3K        2 rows  Guadalupe Mines Rd
        8.1K       11 rows  Eastridge Loop
        7.9K        3 rows  Harry Rd
        7.7K        4 rows  Great Mall Dr
        7.6K        1 rows  Las Animas Rd
        7.3K       32 rows  Quimby Rd
        6.8K       22 rows  Oakbridge Dr
        6.7K       27 rows  San Jose MHP Access
        6.6K       23 rows  Golden Wheel MHP Access

PLANCRT by rows
      1.7K  COUNTY DATASET
      1.5K  GDT
       736  AERIAL PHOTO
       603  MGE
        47  T-10186
        30  T-10022
        28  T-10390
        28  TR9094
        27  TR9422
        26  T-10204
        26  TR8650
        25  3-18939
        24  TR8988
        23  T-10026
        23  T-9753
        23  T-10169
        22  T-9726
        21  TR8385
        21  TR8772
        20  T-9835

PLANCRT by dollars
      603.6K     1.5K rows  GDT
      525.7K     1.7K rows  COUNTY DATASET
      279.1K      736 rows  AERIAL PHOTO
      190.1K      603 rows  MGE
       10.9K       12 rows  TR8475
        8.8K       47 rows  T-10186
        6.8K       13 rows  TR8369
        6.7K        9 rows  TR8841
        6.4K        6 rows  TR8712
        6.3K       15 rows  TR8714
        5.9K       26 rows  T-10204
        5.6K       13 rows  TR9275
        5.3K        3 rows  TR8703
        5.3K        7 rows  TR8399
        5.2K        8 rows  TR8598
        5.2K       15 rows  TR8842
        5.1K        5 rows  TR8470
        5.0K       28 rows  T-10390
        4.8K       30 rows  T-10022
        4.8K       20 rows  T-9835

FEATURECLASS by rows
      6.5K  StreetCenterline

FEATURECLASS by dollars
       2.08M     6.5K rows  StreetCenterline

FACILITYID by rows
         1  83721
         1  83722
         1  101715
         1  50415
         1  82288
         1  70207
         1  101345
         1  70086
         1  70070
         1  70115
         1  70308
         1  70025
         1  52618
         1  83471
         1  51206
         1  83473
         1  70341
         1  82251
         1  70071
         1  70224

FACILITYID by dollars
       14.8K        1 rows  73198
       12.9K        1 rows  73130
        8.0K        1 rows  80908
        7.6K        1 rows  73353
        7.6K        1 rows  74754
        6.8K        1 rows  75078
        5.1K        1 rows  70875
        3.8K        1 rows  73509
        3.8K        1 rows  73548
        3.7K        1 rows  73179
        3.6K        1 rows  50611
        3.5K        1 rows  73340
        3.4K        1 rows  73398
        3.3K        1 rows  84198
        3.2K        1 rows  73244
        3.2K        1 rows  70469
        3.1K        1 rows  80958
        3.0K        1 rows  73239
        2.9K        1 rows  73333
        2.9K        1 rows  79150

## who x when

FULLNAME by LASTUPDATE, dollars = SHAPE_LENGTH
  Bike Path                                 2019:9.4K
  Chateau La Salle Dr                       2019:10.8K 2021:5.1K 2022:179.11 2023:359.08
  Checkers Dr APT Access                    2019:4.8K
  Country Club Pkwy                         2019:12.9K
  Cribari Ln                                2019:5.7K 2022:139.57
  Eastridge Loop                            2019:8.1K
  Fairbanks Cir                             2019:1.5K
  Golden Wheel MHP Access                   2019:6.6K
  Great Mall Dr                             2019:7.7K
  Guadalupe Mines Rd                        2019:8.3K
  Harry Rd                                  2019:1.1K 2022:6.8K
  Kenbrook Cir                              2019:5.0K
  Las Animas Rd                             2019:7.6K
  Mill Pond Dr                              2019:8.7K 2020:122.27 2021:865.74 2023:1.5K
  Mill River Ln                             2019:2.2K 2022:473.47
  Mountain Springs Dr                       2019:6.4K
  New Street                                2019:124.2K 2020:3.0K 2021:2.4K 2022:989.20 2023:1.9K
  Oakbridge Dr                              2019:6.3K 2022:418.42 2023:149.67
  Pepper Tree Estates MHP Access            2019:8.6K
  Quimby Rd                                 2019:6.8K 2022:166.46 2023:334.57
  Ribisi Cir                                2019:2.3K
  Road L                                    2023:14.8K
  Rural Access                              2019:104.4K 2020:10.1K 2021:26.0K 2022:3.2K 2023:18.5K
  San Felipe Rd                             2019:8.6K
  San Jose MHP Access                       2019:6.7K
  South Bay MHP Access                      2019:4.7K 2022:482.98
  The Villages Fairway Dr                   2019:20.0K 2021:2.0K
  The Villages Pkwy                         2019:12.5K 2020:1.3K 2022:1.7K
  Villa Teresa Way                          2019:5.2K
  Vista Roma Way                            2019:3.7K 2022:230.48 2023:46.19

PLANCRT by LASTUPDATE, dollars = SHAPE_LENGTH
  3-18939                                   2019:2.9K 2022:52.40 2023:131.94
  AERIAL PHOTO                              2019:229.7K 2020:11.9K 2021:15.5K 2022:12.2K 2023:9.7K
  COUNTY DATASET                            2019:448.6K 2020:9.8K 2021:24.4K 2022:36.8K 2023:6.1K
  GDT                                       2019:479.6K 2020:21.2K 2021:23.2K 2022:38.2K 2023:41.4K
  MGE                                       2019:164.1K 2020:5.3K 2021:946.19 2022:13.4K 2023:5.3K 2024:1.1K
  T-10022                                   2019:4.0K 2020:173.72 2022:585.58
  T-10026                                   2019:2.3K 2020:81.37 2022:520.32
  T-10169                                   2019:2.6K
  T-10186                                   2019:8.0K 2020:649.25 2022:148.64
  T-10204                                   2019:3.5K 2022:2.5K
  T-10390                                   2020:4.0K 2021:479.83 2022:518.49
  T-9726                                    2019:3.9K 2020:59.17
  T-9753                                    2019:3.7K
  T-9835                                    2019:4.8K
  TR8369                                    2019:6.8K
  TR8385                                    2019:3.4K
  TR8399                                    2019:5.3K
  TR8475                                    2019:10.9K
  TR8598                                    2019:5.2K
  TR8650                                    2019:3.2K
  TR8703                                    2019:5.3K
  TR8712                                    2019:4.0K 2020:2.4K
  TR8714                                    2019:6.3K
  TR8772                                    2019:3.0K
  TR8841                                    2019:6.7K
  TR8842                                    2019:5.0K 2021:227.24
  TR8988                                    2019:4.3K
  TR9094                                    2019:3.0K
  TR9275                                    2019:4.8K 2022:361.15 2023:468.27
  TR9422                                    2019:3.9K 2022:230.48 2023:46.19

## what

ADDRNUMTYPE: STD EVEN ODD 84%, CONTIGUOUS 15%, OTHER 0%

ONEWAYDIR: B 99%, P 0%, N 0%

MODELFLAG: S 99%, D 1%, M 0%

STREETCLASS: RE 97%, DW 2%, PA 0%, CO 0%, MI 0%, AL 0%

FUNCTCLASS: LO 100%, MA 0%, NC 0%

SPEEDLIMIT: 25 91%, 15 9%, 20 0%, 35 0%, 5 0%, 30 0%

OFFICIAL: Yes 86%, No 14%

MUNILEFT: SJ 91%, CO 4%, SU 1%, MI 1%, SC 1%, LG 1%, CA 1%, CU 1%, SA 0%, MH 0%

MUNIRIGHT: SJ 92%, CO 4%, SU 1%, MI 1%, SC 1%, LG 1%, CA 1%, CU 1%, SA 0%, MH 0%

ZIPLEFT: 95131 12%, 95136 11%, 95123 11%, 95135 10%, 95111 10%, 95125 9%, 95133 8%, 95138 8%, 95134 6%, 95120 6%, 95132 5%, 95116 5%

ZIPRIGHT: 95131 12%, 95136 11%, 95123 11%, 95135 10%, 95111 10%, 95125 9%, 95133 8%, 95138 8%, 95134 6%, 95120 6%, 95132 5%, 95116 5%

PLANMOD: COUNTY DATASET 32%, GDT 28%, MGE 27%, AERIAL PHOTO 11%, T-6375 0%, T-10462 0%, 3-24334 0%, 3-24335 0%, T-10368 0%, T-7950 0%, 9179 0%

INCORPORATED: Yes 92%, No 8%

ESNLEFT: 216 95%, 226 1%, 204 1%, 217 1%, 201 1%, 225 1%, 222 1%, 206 0%, 230 0%, 227 0%, 215 0%

ESNRIGHT: 216 95%, 226 1%, 217 1%, 204 1%, 201 1%, 225 1%, 222 1%, 206 0%, 227 0%, 230 0%, 215 0%

FHWAFUNCTCLASS: 7 100%, 4 0%, 5 0%, 3 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 6.5K | 0 | 96515 33; 96514 33; 96107 33; 95709 33 |
| PARCELID | id | 6.5K | 0 | 8000115618 33; 8000115617 33; 8000115606 33; 8000115604 33 |
| FACILITYID | who | 6.5K | 0 | 115618 33; 115617 33; 115606 33; 115604 33 |
| INTID | id | 6.5K | 0 | 115618 33; 115617 33; 115606 33; 115604 33 |
| STREETMASTERID | other | 2.7K | 0 | 180 300; 832 194; 7413 64; 3224 50 |
| FROMINTERID | other | 5.0K | 0 | 54589 34; 53989 34; 53991 34; 53993 34 |
| TOINTERID | other | 5.1K | 0 | 53993 34; 53994 34; 53992 34; 53746 34 |
| FROMLEFT | other | 1.9K | 2.5K | 100 43; 101 40; 400 34; 1100 34 |
| TOLEFT | other | 2.0K | 2.5K | 498 35; 199 34; 1198 34; 1598 33 |
| FROMRIGHT | other | 2.0K | 2.5K | 101 45; 201 41; 100 37; 401 35 |
| TORIGHT | other | 2.1K | 2.5K | 1199 37; 499 35; 198 34; 199 31 |
| ADDRNUMTYPE | category | 4 | 2 | STD EVEN ODD 5.5K; CONTIGUOUS 988; OTHER 25 |
| FULLNAME | who | 2.6K | 0 | New Street 300; Rural Access 194; Chateau La Salle Dr 64; Mountain Springs Dr 50 |
| ONEWAYDIR | category | 3 | 0 | B 6.4K; P 25; N 12 |
| MODELFLAG | category | 3 | 0 | S 6.4K; D 38; M 23 |
| STREETCLASS | category | 6 | 0 | RE 6.3K; DW 154; PA 8; CO 5 |
| FUNCTCLASS | category | 3 | 0 | LO 6.5K; MA 6; NC 5 |
| SPEEDLIMIT | category | 7 | 4 | 25 5.9K; 15 553; 20 26; 35 12 |
| PRIVATE | other | 1 | 0 | Yes 6.5K |
| OFFICIAL | category | 3 | 3 | Yes 5.6K; No 887 |
| MUNILEFT | category | 11 | 38 | SJ 5.9K; CO 243; SU 76; MI 52 |
| MUNIRIGHT | category | 11 | 20 | SJ 5.9K; CO 239; SU 76; MI 52 |
| ZIPLEFT | category | 44 | 0 | 95131 509; 95136 481; 95123 466; 95135 442 |
| ZIPRIGHT | category | 44 | 0 | 95131 508; 95136 480; 95123 467; 95135 442 |
| FOCWIDTH | amount | 770 | 248 | 20.0 258; 26.0 141; 30.0 121; 24.0 101 |
| ROWWIDTH | amount | 746 | 208 | 20.0 212; 26.0 201; 46.0 182; 44.0 176 |
| FEATURECLASS | who | 1 | 0 | StreetCenterline 6.5K |
| PLANCRT | who | 341 | 18 | COUNTY DATASET 1.7K; GDT 1.5K; AERIAL PHOTO 736; MGE 603 |
| PLANMOD | category | 28 | 1.1K | COUNTY DATASET 1.7K; GDT 1.5K; MGE 1.4K; AERIAL PHOTO 611 |
| LASTUPDATE | date | 1.1K | 0 | 2019-06-27T23:59:11 153; 2019-06-27T23:59:12 139; 2019-06-27T23:59:10 134; 2019-06-27T23:59:09 124 |
| NOTES | who | 121 | 4.5K | T_Shape: Address Gap Igno 668; Directions: Address Gap I 245; From Intersection ID Corr 162; DS: ZipUpdate 153 |
| RSN | id | 6.0K | 552 | 489700 30; 489699 30; 489300 30; 489188 30 |
| INCORPORATED | category | 2 | 0 | Yes 5.9K; No 545 |
| SHAPE_LENGTH | amount | 6.5K | 0 | 96.6357655662026 33; 165.914065051396 33; 365.775061131691 33; 162.299914453261 33 |
| ESNLEFT | category | 13 | 2.5K | 216 3.8K; 226 42; 204 38; 217 35 |
| ESNRIGHT | category | 13 | 2.5K | 216 3.8K; 226 41; 217 35; 204 31 |
| FHWAFUNCTCLASS | category | 5 | 488 | 7 6.0K; 4 11; 5 5; 3 4 |
| CREATIONDATE | date | 4 | 0 | 1900-01-01T00:00:00 6.5K; 2024-06-27T16:28:47 2; 2023-11-20T23:19:16 2; 2024-02-07T01:11:38 1 |
| RESPONSIBILITY | empty | 1 | 6.5K |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:11:43.39377 6.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0ff45639-d2d6-4951-abee-f 6.5K |
| SRC_SHA256 | who | 1 | 0 | e3717506519e4381d2edb2d92 6.5K |
