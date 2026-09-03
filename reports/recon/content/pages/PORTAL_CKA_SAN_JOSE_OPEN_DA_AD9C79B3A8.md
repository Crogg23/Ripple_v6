# PORTAL_CKA_SAN_JOSE_OPEN_DA_AD9C79B3A8

rows 10.0K  columns 42  scan 5.4s

roles: amount 3, audit 2, category 16, date 1, empty 1, id 4, other 8, who 8

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FOCWIDTH | 10.0K | 4 | 39.30 | 114.56 | 1.3K | 436.2K |
| ROWWIDTH | 10.0K | 10 | 59.20 | 133.96 | 1.3K | 617.2K |
| SHAPE_LENGTH | 10.0K | 5.18 | 290.36 | 2.2K | 20.4K | 4.53M |

## who

FULLNAME by rows
        63  Sierra Rd
        46  Piedmont Rd
        40  McKee Rd
        37  Curtner Ave
        36  N Capitol Ave
        35  Camden Ave
        32  Hostetter Rd
        29  N 1st St
        29  Zanker Rd
        28  Berryessa Rd
        26  Stevens Creek Blvd
        25  Santa Teresa Blvd
        25  Morrill Ave
        25  Branham Ln
        24  Penitencia Creek Rd
        24  Moorpark Ave
        24  N White Rd
        23  Mabury Rd
        23  Old Piedmont Rd
        23  Cropley Ave

FULLNAME by dollars
       37.7K       63 rows  Sierra Rd
       25.3K       25 rows  Santa Teresa Blvd
       23.3K        4 rows  Hicks Rd
       23.0K       29 rows  N 1st St
       23.0K       15 rows  McCarthy Blvd
       22.4K       29 rows  Zanker Rd
       20.4K        1 rows  280
       18.6K       20 rows  Montague Expy
       18.2K        2 rows  Alum Rock Falls Rd
       18.2K        3 rows  237
       16.8K       16 rows  Lafayette St
       14.8K        1 rows  Road L
       14.6K       12 rows  Tasman Dr
       13.9K       36 rows  N Capitol Ave
       13.8K        4 rows  Almaden Quicksilver Park
       13.8K        6 rows  San Tomas Expy
       13.2K       46 rows  Piedmont Rd
       12.9K       17 rows  Country Club Pkwy
       12.8K        4 rows  Mine Hill Rd
       12.7K       11 rows  Mt Hamilton Rd

PLANCRT by rows
      6.4K  MGE
      1.7K  COUNTY DATASET
       616  GDT
       220  AERIAL PHOTO
        28  TR9094
        26  TR8650
        24  TR8988
        22  TR9422
        21  TR8385
        21  TR8772
        20  TR8549
        18  TR8720
        17  TR8882
        16  TR8603
        16  TR9040
        16  TR8539
        16  TR8580
        15  TR8842
        15  TR9161
        14  TR8714

PLANCRT by dollars
       3.02M     6.4K rows  MGE
      773.8K     1.7K rows  COUNTY DATASET
      306.1K      616 rows  GDT
       74.0K      220 rows  AERIAL PHOTO
       10.9K       12 rows  TR8475
        9.1K        8 rows  TR8712
        6.8K       13 rows  TR8369
        6.7K        9 rows  TR8841
        6.1K       14 rows  TR8714
        5.3K        3 rows  TR8703
        5.3K        7 rows  TR8399
        5.3K        6 rows  TR8356
        5.2K        8 rows  TR8598
        5.2K       15 rows  TR8842
        5.1K        5 rows  TR8470
        4.7K       20 rows  TR8549
        4.6K       16 rows  TR8539
        4.4K        6 rows  TR8610
        4.3K       24 rows  TR8988
        4.2K       12 rows  TR9024

FEATURECLASS by rows
     10.0K  StreetCenterline

FEATURECLASS by dollars
       4.53M    10.0K rows  StreetCenterline

FACILITYID by rows
         1  107252
         1  107254
         1  23059
         1  82237
         1  21179
         1  21196
         1  21203
         1  83576
         1  83564
         1  18139
         1  20775
         1  21038
         1  21061
         1  82245
         1  23053
         1  107251
         1  21073
         1  83668
         1  23157
         1  83672

FACILITYID by dollars
       20.4K        1 rows  20981
       14.8K        1 rows  73198
       14.1K        1 rows  19752
       12.9K        1 rows  11844
       12.1K        1 rows  75140
        8.8K        1 rows  74097
        8.3K        1 rows  72236
        8.1K        1 rows  74447
        7.7K        1 rows  74104
        7.6K        1 rows  73353
        7.1K        1 rows  26231
        6.7K        1 rows  10139
        6.6K        1 rows  114655
        6.5K        1 rows  2777
        5.5K        1 rows  26023
        5.3K        1 rows  110133
        5.3K        1 rows  74248
        5.1K        1 rows  70875
        4.9K        1 rows  74133
        4.5K        1 rows  72597

## who x when

FULLNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  237                                       2026:18.2K
  280                                       2026:20.4K
  Almaden Quicksilver Park                  2026:13.8K
  Alum Rock Falls Rd                        2026:18.2K
  Berryessa Rd                              2026:11.4K
  Branham Ln                                2026:8.6K
  Camden Ave                                2026:11.8K
  Cropley Ave                               2026:7.7K
  Curtner Ave                               2026:10.9K
  Hicks Rd                                  2026:23.3K
  Hostetter Rd                              2026:12.6K
  Lafayette St                              2026:16.8K
  Mabury Rd                                 2026:9.4K
  McCarthy Blvd                             2026:23.0K
  McKee Rd                                  2026:8.0K
  Montague Expy                             2026:18.6K
  Moorpark Ave                              2026:11.1K
  Morrill Ave                               2026:10.0K
  N 1st St                                  2026:23.0K
  N Capitol Ave                             2026:13.9K
  N White Rd                                2026:6.7K
  Old Piedmont Rd                           2026:8.2K
  Penitencia Creek Rd                       2026:12.5K
  Piedmont Rd                               2026:13.2K
  Road L                                    2026:14.8K
  Santa Teresa Blvd                         2026:25.3K
  Sierra Rd                                 2026:37.7K
  Stevens Creek Blvd                        2026:12.2K
  Tasman Dr                                 2026:14.6K
  Zanker Rd                                 2026:22.4K

PLANCRT by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  AERIAL PHOTO                              2026:74.0K
  COUNTY DATASET                            2026:773.8K
  GDT                                       2026:306.1K
  MGE                                       2026:3.02M
  TR8356                                    2026:5.3K
  TR8369                                    2026:6.8K
  TR8385                                    2026:3.4K
  TR8399                                    2026:5.3K
  TR8470                                    2026:5.1K
  TR8475                                    2026:10.9K
  TR8539                                    2026:4.6K
  TR8549                                    2026:4.7K
  TR8580                                    2026:2.8K
  TR8598                                    2026:5.2K
  TR8603                                    2026:3.2K
  TR8610                                    2026:4.4K
  TR8650                                    2026:3.2K
  TR8703                                    2026:5.3K
  TR8712                                    2026:9.1K
  TR8714                                    2026:6.1K
  TR8720                                    2026:2.3K
  TR8772                                    2026:3.0K
  TR8841                                    2026:6.7K
  TR8842                                    2026:5.2K
  TR8882                                    2026:1.7K
  TR8988                                    2026:4.3K
  TR9040                                    2026:3.6K
  TR9094                                    2026:3.0K
  TR9161                                    2026:3.7K
  TR9422                                    2026:3.6K

## what

ADDRNUMTYPE: STD EVEN ODD 94%, CONTIGUOUS 6%, OTHER 0%

ONEWAYDIR: B 100%, N 0%, P 0%

MODELFLAG: S 93%, M 7%

STREETCLASS: RE 86%, MI 7%, CO 4%, MA 3%, EX 0%, FY 0%, DW 0%, PA 0%

FUNCTCLASS: LO 85%, MA 10%, NC 4%, CA 0%, AR 0%

SPEEDLIMIT: 25 86%, 35 7%, 40 3%, 30 2%, 45 1%, 55 0%, 15 0%, 50 0%, 65 0%

PRIVATE: No 77%, Yes 23%

MUNILEFT: SJ 75%, CO 6%, SC 5%, MI 5%, CA 3%, LG 2%, SU 1%, SA 1%, CU 1%, MH 0%, FM 0%

MUNIRIGHT: SJ 75%, CO 6%, SC 5%, MI 4%, CA 4%, LG 2%, SU 1%, SA 1%, CU 1%, MH 0%, FM 0%

ZIPLEFT: 95132 17%, 95131 13%, 95123 9%, 95120 9%, 95127 9%, 95136 7%, 95133 7%, 95124 7%, 95035 6%, 95134 6%, 95008 5%, 95138 4%

ZIPRIGHT: 95132 17%, 95131 13%, 95123 9%, 95127 9%, 95120 9%, 95136 7%, 95124 7%, 95133 7%, 95035 6%, 95134 6%, 95008 5%, 95125 4%

PLANMOD: MGE 75%, COUNTY DATASET 17%, GDT 6%, AERIAL PHOTO 2%, TR9510 0%, APNU_20170101 0%, T-6375 0%, TR9150 0%, T-10107 0%, 9179 0%, TR9285 0%

INCORPORATED: Yes 76%, No 24%

ESNLEFT: 216 76%, 222 5%, 226 5%, 204 5%, 225 4%, 217 2%, 206 1%, 201 1%, 230 1%, 224 0%, 227 0%

ESNRIGHT: 216 75%, 222 5%, 204 5%, 226 5%, 225 4%, 217 2%, 206 1%, 201 1%, 230 1%, 224 0%, 227 0%

FHWAFUNCTCLASS: 7 82%, 4 7%, 5 5%, 3 5%, 6 0%, 2 0%, 1 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 12301 50; 12298 50; 12297 50; 12296 50 |
| FACILITYID | who | 10.0K | 0 | 5303 50; 5281 50; 6342 50; 9423 50 |
| INTID | id | 10.0K | 0 | 5303 50; 5281 50; 6342 50; 9423 50 |
| STREETMASTERID | other | 4.2K | 0 | 2678 70; 2238 65; 115 65; 2363 57 |
| FROMINTERID | other | 7.4K | 0 | 24067 51; 9491 51; 23886 51; 2200 50 |
| TOINTERID | other | 7.7K | 0 | 24540 51; 24248 51; 856 51; 1476 51 |
| FROMLEFT | other | 3.3K | 1.2K | 400 105; 2 93; 1100 83; 300 83 |
| TOLEFT | other | 3.3K | 1.2K | 498 101; 398 84; 198 83; 1299 82 |
| FROMRIGHT | other | 3.3K | 1.1K | 401 99; 1 96; 1101 83; 301 83 |
| TORIGHT | other | 3.4K | 1.1K | 499 101; 199 84; 1298 83; 399 79 |
| ADDRNUMTYPE | category | 3 | 0 | STD EVEN ODD 9.4K; CONTIGUOUS 635; OTHER 11 |
| FULLNAME | who | 4.1K | 0 | Curtner Ave 70; Camden Ave 65; Sierra Rd 65; Santa Teresa Blvd 57 |
| ONEWAYDIR | category | 3 | 0 | B 10.0K; N 21; P 13 |
| MODELFLAG | category | 2 | 0 | S 9.3K; M 662 |
| STREETCLASS | category | 8 | 0 | RE 8.6K; MI 668; CO 376; MA 345 |
| FUNCTCLASS | category | 5 | 0 | LO 8.5K; MA 1.0K; NC 410; CA 33 |
| SPEEDLIMIT | category | 9 | 0 | 25 8.6K; 35 693; 40 333; 30 218 |
| PRIVATE | category | 2 | 0 | No 7.7K; Yes 2.3K |
| OFFICIAL | other | 1 | 0 | Yes 10.0K |
| MUNILEFT | category | 12 | 1 | SJ 7.5K; CO 618; SC 502; MI 463 |
| MUNIRIGHT | category | 12 | 1 | SJ 7.5K; CO 636; SC 525; MI 446 |
| ZIPLEFT | category | 43 | 0 | 95132 1.2K; 95131 989; 95123 687; 95120 669 |
| ZIPRIGHT | category | 43 | 0 | 95132 1.2K; 95131 986; 95123 689; 95127 674 |
| FOCWIDTH | amount | 1.6K | 19 | 39 434; 43 227; 40 187; 39.1 169 |
| ROWWIDTH | amount | 1.5K | 15 | 60 774; 59 353; 52 289; 46 185 |
| FEATURECLASS | who | 1 | 0 | StreetCenterline 10.0K |
| PLANCRT | who | 222 | 5 | MGE 6.4K; COUNTY DATASET 1.7K; GDT 616; AERIAL PHOTO 220 |
| PLANMOD | category | 33 | 90 | MGE 7.4K; COUNTY DATASET 1.7K; GDT 618; AERIAL PHOTO 204 |
| LASTUPDATE | who | 1.4K | 0 | 2019/06/27 23:59:32+00 167; 2019/06/27 23:59:12+00 163; 2019/06/27 23:59:01+00 161; 2019/06/27 23:58:39+00 155 |
| NOTES | who | 79 | 7.1K | BM HD 90821 777; T_Shape: Address Gap Igno 513; DS: ZipUpdate 355; Directions: Address Gap I 331 |
| SHAPE_LENGTH | amount | 9.9K | 0 | 434.767389028345 50; 1074.70801442959 50; 437.221744965241 50; 498.013316170897 50 |
| INCORPORATED | category | 2 | 0 | Yes 7.6K; No 2.4K |
| RSN | id | 7.6K | 2.3K | 357234 39; 380842 39; 379028 39; 359530 39 |
| PARCELID | id | 10.2K | 0 | 8000005303 50; 8000005281 50; 8000006342 50; 8000009423 50 |
| ESNLEFT | category | 14 | 1.1K | 216 6.7K; 222 466; 226 444; 204 421 |
| ESNRIGHT | category | 14 | 1.1K | 216 6.7K; 222 488; 204 447; 226 422 |
| FHWAFUNCTCLASS | category | 8 | 1.9K | 7 6.7K; 4 601; 5 436; 3 410 |
| CREATIONDATE | who | 1 | 0 | 1900/01/01 00:00:00+00 10.0K |
| RESPONSIBILITY | empty | 1 | 10.0K |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:51:49.95813 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 700be7f1-6817-4a4e-b6e9-0 10.0K |
| SRC_SHA256 | who | 1 | 0 | 89f37f53bd1d1946c59113b3e 10.0K |
