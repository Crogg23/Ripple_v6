# PORTAL_CKA_SAN_JOSE_OPEN_DA_0D51EC3643

rows 10.0K  columns 42  scan 4.8s

roles: amount 3, audit 2, category 17, date 3, id 4, other 8, who 6

## when

LASTUPDATE
  2019      6.1K  ##############################
  2020      1.0K  #####
  2021       162  #
  2022       387  ##
  2023       132  #
  2024         2  
  2025      2.2K  ###########
  2026        76  

CREATIONDATE
  1900     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FOCWIDTH | 10.0K | 4 | 39.30 | 114.56 | 1.3K | 436.0K |
| ROWWIDTH | 10.0K | 10 | 59.20 | 133.96 | 1.3K | 617.0K |
| SHAPE_LENGTH | 10.0K | 5.18 | 290.31 | 2.2K | 20.4K | 4.52M |

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
        25  Morrill Ave
        25  Branham Ln
        25  Santa Teresa Blvd
        24  Moorpark Ave
        24  Penitencia Creek Rd
        23  Old Piedmont Rd
        23  Mabury Rd
        23  N White Rd
        23  Cropley Ave

FULLNAME by dollars
       37.7K       63 rows  Sierra Rd
       25.3K       25 rows  Santa Teresa Blvd
       23.2K        4 rows  Hicks Rd
       22.6K       15 rows  McCarthy Blvd
       22.6K       29 rows  N 1st St
       22.4K       29 rows  Zanker Rd
       20.4K        1 rows  280
       18.6K       20 rows  Montague Expy
       18.2K        2 rows  Alum Rock Falls Rd
       16.8K       16 rows  Lafayette St
       15.4K        2 rows  237
       14.8K        1 rows  Road L
       14.6K       12 rows  Tasman Dr
       13.8K        4 rows  Almaden Quicksilver Park
       13.8K        6 rows  San Tomas Expy
       13.6K       36 rows  N Capitol Ave
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
        16  TR8580
        16  TR8603
        16  TR8539
        16  TR9040
        15  TR9161
        15  TR8842
        14  TR8803

PLANCRT by dollars
       3.02M     6.4K rows  MGE
      774.0K     1.7K rows  COUNTY DATASET
      304.6K      616 rows  GDT
       73.7K      220 rows  AERIAL PHOTO
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
       4.52M    10.0K rows  StreetCenterline

FACILITYID by rows
         1  21187
         1  83650
         1  21171
         1  83652
         1  83667
         1  23165
         1  21193
         1  83573
         1  21195
         1  23111
         1  83677
         1  83704
         1  23091
         1  21172
         1  83656
         1  83643
         1  22685
         1  83675
         1  23055
         1  107251

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

FULLNAME by LASTUPDATE, dollars = SHAPE_LENGTH
  237                                       2025:1.3K 2026:14.1K
  280                                       2020:20.4K
  Almaden Quicksilver Park                  2019:13.8K
  Alum Rock Falls Rd                        2023:18.2K
  Berryessa Rd                              2019:3.9K 2020:3.5K 2021:3.2K 2025:817.31
  Branham Ln                                2020:4.3K 2022:508.80 2026:3.8K
  Camden Ave                                2019:1.3K 2020:7.0K 2021:285.92 2022:276.02 2025:2.9K
  Cropley Ave                               2019:2.3K 2020:4.7K 2021:735.37
  Curtner Ave                               2019:481.55 2020:10.1K 2025:253.30
  Hicks Rd                                  2020:21.0K 2025:708.67 2026:1.5K
  Hostetter Rd                              2019:2.6K 2020:10.1K
  Lafayette St                              2023:272.54 2025:16.5K
  Mabury Rd                                 2019:2.5K 2020:3.0K 2021:163.17 2022:3.8K
  McCarthy Blvd                             2025:22.6K
  McKee Rd                                  2020:4.4K 2022:112.07 2023:719.34 2025:2.7K
  Montague Expy                             2022:11.7K 2025:6.9K
  Moorpark Ave                              2019:4.4K 2020:5.2K 2025:1.5K
  Morrill Ave                               2020:9.9K 2022:160.13
  N 1st St                                  2020:2.9K 2023:472.09 2025:4.6K 2026:14.6K
  N Capitol Ave                             2022:13.0K 2025:597.05
  N White Rd                                2020:2.9K 2021:2.7K 2022:203.26 2023:205.34 2025:289.55
  Old Piedmont Rd                           2020:7.6K 2022:445.52 2023:111.16
  Penitencia Creek Rd                       2020:7.8K 2021:1.7K 2022:2.3K 2025:672.68
  Piedmont Rd                               2020:11.9K 2023:832.07 2025:432.30
  Road L                                    2023:14.8K
  Santa Teresa Blvd                         2019:6.8K 2020:15.9K 2021:2.7K
  Sierra Rd                                 2019:6.3K 2020:9.7K 2021:5.8K 2022:3.5K 2023:8.2K 2025:3.4K 2026:823.36
  Stevens Creek Blvd                        2020:10.3K 2025:1.9K
  Tasman Dr                                 2025:14.6K
  Zanker Rd                                 2019:2.3K 2020:12.2K 2021:1.4K 2022:1.4K 2025:5.2K

PLANCRT by LASTUPDATE, dollars = SHAPE_LENGTH
  AERIAL PHOTO                              2019:29.9K 2020:1.2K 2021:72.77 2022:3.0K 2025:39.6K
  COUNTY DATASET                            2019:199.3K 2020:31.9K 2021:15.1K 2022:20.4K 2023:4.5K 2025:502.4K 2026:421.83
  GDT                                       2019:101.1K 2020:5.7K 2021:131.54 2022:17.2K 2023:22.4K 2024:2.3K 2025:154.8K 2026:970.85
  MGE                                       2019:1.75M 2020:449.4K 2021:87.4K 2022:169.9K 2023:77.8K 2024:614.91 2025:427.5K 2026:55.1K
  TR8356                                    2019:5.3K
  TR8369                                    2019:6.7K 2025:136.40
  TR8385                                    2019:3.4K
  TR8399                                    2019:5.3K
  TR8470                                    2019:5.1K
  TR8475                                    2019:10.9K
  TR8539                                    2019:4.3K 2025:289.80
  TR8549                                    2019:4.6K 2025:146.48
  TR8580                                    2019:1.7K 2020:153.08 2022:838.36 2023:91.24
  TR8598                                    2019:5.1K 2025:80.59
  TR8603                                    2019:246.79 2022:2.2K 2023:784.35
  TR8650                                    2019:3.2K
  TR8703                                    2019:5.3K
  TR8712                                    2019:6.7K 2020:2.4K
  TR8714                                    2019:6.1K
  TR8720                                    2019:2.3K
  TR8772                                    2019:3.0K
  TR8803                                    2019:1.9K
  TR8841                                    2019:6.7K
  TR8842                                    2019:5.0K 2021:227.24
  TR8882                                    2019:1.5K 2022:97.38 2023:97.83
  TR8988                                    2019:4.3K
  TR9040                                    2019:3.0K 2022:653.26
  TR9094                                    2019:3.0K
  TR9161                                    2019:3.7K
  TR9422                                    2019:3.3K 2022:230.48 2023:46.19

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

ESNLEFT: 216 75%, 222 5%, 226 5%, 204 5%, 225 4%, 217 2%, 206 1%, 201 1%, 230 1%, 224 0%, 227 0%

ESNRIGHT: 216 75%, 222 5%, 204 5%, 226 5%, 225 4%, 217 2%, 206 1%, 201 1%, 230 1%, 224 0%, 227 0%

FHWAFUNCTCLASS: 7 80%, 4 7%, 5 6%, 3 6%, 6 0%, 2 0%, 1 0%

RESPONSIBILITY: SJ 55%, PR 23%, CO 6%, SC 5%, MI 4%, CA 3%, LG 2%, SA 1%, CU 1%, SU 0%, MH 0%, ST 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 12325 50; 12324 50; 12323 50; 12322 50 |
| FACILITYID | who | 10.0K | 0 | 7063 50; 74968 50; 15250 50; 74967 50 |
| INTID | id | 10.0K | 0 | 7063 50; 74968 50; 15250 50; 74967 50 |
| STREETMASTERID | other | 4.2K | 0 | 2678 70; 2238 65; 115 65; 2363 57 |
| FROMINTERID | other | 7.4K | 0 | 24360 51; 24545 51; 24067 51; 9491 51 |
| TOINTERID | other | 7.8K | 0 | 23741 51; 24540 51; 24248 51; 856 51 |
| FROMLEFT | other | 3.3K | 1.2K | 400 106; 2 93; 1100 83; 300 83 |
| TOLEFT | other | 3.4K | 1.2K | 498 102; 398 84; 198 82; 1299 82 |
| FROMRIGHT | other | 3.3K | 1.1K | 401 100; 1 96; 1101 83; 301 83 |
| TORIGHT | other | 3.4K | 1.1K | 499 102; 199 84; 1298 83; 399 79 |
| ADDRNUMTYPE | category | 3 | 0 | STD EVEN ODD 9.4K; CONTIGUOUS 635; OTHER 11 |
| FULLNAME | who | 4.1K | 0 | Curtner Ave 70; Camden Ave 65; Sierra Rd 65; Santa Teresa Blvd 57 |
| ONEWAYDIR | category | 3 | 0 | B 10.0K; N 22; P 13 |
| MODELFLAG | category | 2 | 0 | S 9.3K; M 656 |
| STREETCLASS | category | 8 | 0 | RE 8.6K; MI 664; CO 377; MA 345 |
| FUNCTCLASS | category | 5 | 0 | LO 8.5K; MA 1.0K; NC 410; CA 32 |
| SPEEDLIMIT | category | 9 | 0 | 25 8.6K; 35 736; 40 294; 30 231 |
| PRIVATE | category | 2 | 0 | No 7.7K; Yes 2.3K |
| OFFICIAL | other | 1 | 0 | Yes 10.0K |
| MUNILEFT | category | 11 | 0 | SJ 7.5K; CO 613; SC 497; MI 460 |
| MUNIRIGHT | category | 11 | 0 | SJ 7.5K; CO 639; SC 520; MI 443 |
| ZIPLEFT | category | 43 | 0 | 95132 1.2K; 95131 989; 95123 687; 95120 672 |
| ZIPRIGHT | category | 43 | 0 | 95132 1.2K; 95131 984; 95123 689; 95127 673 |
| FOCWIDTH | amount | 1.5K | 19 | 39.0 435; 43.0 227; 40.0 188; 39.1 169 |
| ROWWIDTH | amount | 1.5K | 15 | 60.0 776; 59.0 354; 52.0 289; 46.0 186 |
| FEATURECLASS | who | 1 | 0 | StreetCenterline 10.0K |
| PLANCRT | who | 222 | 5 | MGE 6.4K; COUNTY DATASET 1.7K; GDT 616; AERIAL PHOTO 220 |
| PLANMOD | category | 33 | 90 | MGE 7.4K; COUNTY DATASET 1.7K; GDT 618; AERIAL PHOTO 204 |
| LASTUPDATE | date | 1.4K | 0 | 2025-07-30T21:25:21 1.9K; 2019-06-27T23:59:32 163; 2019-06-27T23:59:12 161; 2019-06-27T23:59:01 153 |
| NOTES | who | 84 | 7.1K | BM HD 90821 769; T_Shape: Address Gap Igno 513; DS: ZipUpdate 349; Directions: Address Gap I 333 |
| SHAPE_LENGTH | amount | 9.9K | 0 | 531.781510043394 50; 91.4893749422366 50; 587.605074656704 50; 345.816615597773 50 |
| INCORPORATED | category | 2 | 0 | Yes 7.6K; No 2.4K |
| RSN | id | 7.6K | 2.3K | 368754 39; 357116 39; 358715 39; 363094 39 |
| PARCELID | id | 10.2K | 0 | 8000007063 50; 8000074968 50; 8000015250 50; 8000074967 50 |
| ESNLEFT | category | 15 | 1.1K | 216 6.7K; 222 465; 226 442; 204 424 |
| ESNRIGHT | category | 14 | 1.1K | 216 6.7K; 222 488; 204 447; 226 420 |
| FHWAFUNCTCLASS | category | 8 | 110 | 7 7.9K; 4 712; 5 614; 3 576 |
| CREATIONDATE | date | 1 | 0 | 1900-01-01T00:00:00 10.0K |
| RESPONSIBILITY | category | 12 | 0 | SJ 5.5K; PR 2.3K; CO 580; SC 452 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:51:58.48265 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0b31ccd0-0d40-48d0-97b6-9 10.0K |
| SRC_SHA256 | who | 1 | 0 | 0ac79ed6f359ee850f6b8ceb0 10.0K |
