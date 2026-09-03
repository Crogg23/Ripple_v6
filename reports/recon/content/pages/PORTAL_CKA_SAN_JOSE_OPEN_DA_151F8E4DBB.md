# PORTAL_CKA_SAN_JOSE_OPEN_DA_151F8E4DBB

rows 10.0K  columns 42  scan 4.7s

roles: amount 3, audit 2, category 16, date 1, id 4, other 9, who 8

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FOCWIDTH | 10.0K | 4 | 39.90 | 115.02 | 1.3K | 464.5K |
| ROWWIDTH | 10.0K | 17 | 60 | 134.52 | 1.3K | 657.4K |
| SHAPE_LENGTH | 10.0K | 5.18 | 313.06 | 2.3K | 20.4K | 4.94M |

## who

FULLNAME by rows
        79  Camden Ave
        63  Sierra Rd
        50  Santa Teresa Blvd
        46  Piedmont Rd
        44  Curtner Ave
        40  McKee Rd
        38  Branham Ln
        36  Almaden Rd
        36  N Capitol Ave
        36  Blossom Hill Rd
        35  Union Ave
        33  Meridian Ave
        32  Hostetter Rd
        30  Redmond Ave
        29  Foxworthy Ave
        29  N 1st St
        29  Zanker Rd
        28  Leigh Ave
        27  McKean Rd
        27  Snell Ave

FULLNAME by dollars
       37.7K       63 rows  Sierra Rd
       35.0K        6 rows  Hicks Rd
       34.8K       50 rows  Santa Teresa Blvd
       30.0K       79 rows  Camden Ave
       23.0K       29 rows  N 1st St
       22.6K       15 rows  McCarthy Blvd
       22.4K       29 rows  Zanker Rd
       20.4K        1 rows  280
       20.2K       22 rows  Monterey Rd
       18.9K       27 rows  McKean Rd
       18.6K       20 rows  Montague Expy
       18.2K        2 rows  Alum Rock Falls Rd
       18.2K        3 rows  237
       17.9K       38 rows  Branham Ln
       17.5K        9 rows  Casa Loma Rd
       17.4K       36 rows  Blossom Hill Rd
       17.4K        4 rows  Cherry Canyon Rd
       16.9K       12 rows  Monterey Hwy
       16.8K       16 rows  Lafayette St
       15.2K        6 rows  Metcalf Rd

PLANCRT by rows
      8.1K  MGE
      1.1K  COUNTY DATASET
       215  GDT
        67  AERIAL PHOTO
        23  TR8692
        16  TR8539
        16  TR9040
        15  TR8419
        15  TR9161
        14  D-0775
        13  TR9352
        12  TR9024
        11  TR8870
        11  9170
        11  3-12615
        10  CAL085
         9  TR8753
         9  TR8886
         9  TR8743
         9  TR8679

PLANCRT by dollars
       3.82M     8.1K rows  MGE
      672.8K     1.1K rows  COUNTY DATASET
      166.5K      215 rows  GDT
       43.9K       67 rows  AERIAL PHOTO
       11.2K       23 rows  TR8692
       10.3K       15 rows  TR8419
        6.8K       11 rows  9170
        6.8K        6 rows  TR8712
        6.4K       13 rows  TR9352
        6.3K       14 rows  D-0775
        5.9K       10 rows  CAL085
        5.3K        6 rows  TR8356
        4.6K       16 rows  TR8539
        4.2K       12 rows  TR9024
        4.0K        8 rows  TR8823
        3.7K       15 rows  TR9161
        3.7K        9 rows  TR8743
        3.6K       16 rows  TR9040
        3.5K        8 rows  TR8744
        3.4K        9 rows  TR8679

FEATURECLASS by rows
     10.0K  StreetCenterline

FEATURECLASS by dollars
       4.94M    10.0K rows  StreetCenterline

FACILITYID by rows
         1  83674
         1  23051
         1  21197
         1  82249
         1  23063
         1  83575
         1  83555
         1  23061
         1  21302
         1  23065
         1  21250
         1  82388
         1  83660
         1  22833
         1  83659
         1  23162
         1  21240
         1  23110
         1  21196
         1  83670

FACILITYID by dollars
       20.4K        1 rows  20981
       14.1K        1 rows  19752
       12.9K        1 rows  11844
       12.1K        1 rows  75140
       10.5K        1 rows  75923
        8.8K        1 rows  74097
        8.3K        1 rows  72236
        8.1K        1 rows  74447
        7.7K        1 rows  74104
        7.6K        1 rows  76123
        7.1K        1 rows  26231
        7.0K        1 rows  114751
        6.7K        1 rows  10139
        6.6K        1 rows  114655
        6.5K        1 rows  2777
        6.3K        1 rows  75185
        6.0K        1 rows  76044
        6.0K        1 rows  76015
        5.5K        1 rows  26023
        5.3K        1 rows  110133

## who x when

FULLNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  237                                       2026:18.2K
  280                                       2026:20.4K
  Almaden Rd                                2026:14.5K
  Alum Rock Falls Rd                        2026:18.2K
  Blossom Hill Rd                           2026:17.4K
  Branham Ln                                2026:17.9K
  Camden Ave                                2026:30.0K
  Casa Loma Rd                              2026:17.5K
  Cherry Canyon Rd                          2026:17.4K
  Curtner Ave                               2026:14.2K
  Foxworthy Ave                             2026:11.7K
  Hicks Rd                                  2026:35.0K
  Hostetter Rd                              2026:12.6K
  Leigh Ave                                 2026:12.5K
  McCarthy Blvd                             2026:22.6K
  McKean Rd                                 2026:18.9K
  McKee Rd                                  2026:8.0K
  Meridian Ave                              2026:12.6K
  Montague Expy                             2026:18.6K
  Monterey Hwy                              2026:16.9K
  Monterey Rd                               2026:20.2K
  N 1st St                                  2026:23.0K
  N Capitol Ave                             2026:13.9K
  Piedmont Rd                               2026:13.2K
  Redmond Ave                               2026:11.4K
  Santa Teresa Blvd                         2026:34.8K
  Sierra Rd                                 2026:37.7K
  Snell Ave                                 2026:9.5K
  Union Ave                                 2026:12.7K
  Zanker Rd                                 2026:22.4K

PLANCRT by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  3-12615                                   2026:3.2K
  9170                                      2026:6.8K
  AERIAL PHOTO                              2026:43.9K
  CAL085                                    2026:5.9K
  COUNTY DATASET                            2026:672.8K
  D-0775                                    2026:6.3K
  GDT                                       2026:166.5K
  MGE                                       2026:3.82M
  TR8356                                    2026:5.3K
  TR8419                                    2026:10.3K
  TR8539                                    2026:4.6K
  TR8679                                    2026:3.4K
  TR8692                                    2026:11.2K
  TR8712                                    2026:6.8K
  TR8743                                    2026:3.7K
  TR8744                                    2026:3.5K
  TR8753                                    2026:2.8K
  TR8823                                    2026:4.0K
  TR8870                                    2026:2.9K
  TR8886                                    2026:3.0K
  TR9024                                    2026:4.2K
  TR9040                                    2026:3.6K
  TR9161                                    2026:3.7K
  TR9352                                    2026:6.4K

## what

ADDRNUMTYPE: STD EVEN ODD 98%, CONTIGUOUS 2%, OTHER 0%

ONEWAYDIR: B 100%, N 0%, P 0%

MODELFLAG: S 93%, M 7%

STREETCLASS: RE 82%, MI 8%, CO 5%, MA 4%, EX 0%, FY 0%

FUNCTCLASS: LO 80%, MA 13%, NC 6%, AR 0%, CA 0%

SPEEDLIMIT: 25 82%, 35 9%, 40 4%, 30 3%, 45 1%, 55 1%, 50 0%, 65 0%, 15 0%, 20 0%

MUNILEFT: SJ 73%, CO 7%, CA 5%, SC 5%, MI 4%, LG 3%, SA 1%, CU 1%, MH 1%, SU 0%, FM 0%

MUNIRIGHT: SJ 72%, CO 8%, CA 5%, SC 5%, MI 4%, LG 2%, SA 1%, CU 1%, MH 1%, SU 0%, FM 0%

ZIPLEFT: 95132 14%, 95124 14%, 95120 11%, 95123 10%, 95008 9%, 95127 9%, 95131 8%, 95136 6%, 95035 5%, 95133 5%, 95125 4%, 95118 4%

ZIPRIGHT: 95132 14%, 95124 14%, 95120 11%, 95123 10%, 95008 9%, 95127 9%, 95131 8%, 95136 6%, 95133 5%, 95035 5%, 95125 4%, 95118 4%

PLANMOD: MGE 86%, COUNTY DATASET 11%, GDT 2%, AERIAL PHOTO 1%, TR9510 0%, APNU_20170101 0%, TR9150 0%, TR8991 0%, DB-10027 0%, DB-10138 0%, TR9285 0%

INCORPORATED: Yes 74%, No 26%

ESNLEFT: 216 73%, 225 5%, 204 5%, 222 5%, 226 4%, 217 3%, 206 1%, 230 1%, 201 1%, 227 1%, 210 1%

ESNRIGHT: 216 73%, 204 5%, 225 5%, 222 5%, 226 4%, 217 3%, 206 1%, 230 1%, 201 1%, 227 1%, 210 0%

FHWAFUNCTCLASS: 7 75%, 4 9%, 5 8%, 3 7%, 6 1%, 2 0%, 1 0%

RESPONSIBILITY: SJ 73%, CO 7%, CA 5%, SC 5%, MI 4%, LG 3%, SA 1%, CU 1%, MH 1%, SU 0%, ST 0%, PR 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 15132 50; 15130 50; 15129 50; 15128 50 |
| PARCELID | id | 10.1K | 0 | 8000007595 50; 8000006237 50; 8000008947 50; 8000007503 50 |
| FACILITYID | who | 10.0K | 0 | 7595 50; 6237 50; 8947 50; 7503 50 |
| INTID | id | 10.0K | 0 | 7595 50; 6237 50; 8947 50; 7503 50 |
| STREETMASTERID | other | 4.0K | 0 | 2238 99; 2363 71; 2678 67; 115 65 |
| FROMINTERID | other | 7.4K | 0 | 16359 51; 2853 51; 24854 51; 2433 51 |
| TOINTERID | other | 7.8K | 0 | 10185 51; 2860 51; 10122 51; 10043 51 |
| FROMLEFT | other | 3.5K | 607 | 400 99; 2 95; 300 94; 1100 83 |
| TOLEFT | other | 3.6K | 608 | 498 99; 398 97; 198 90; 798 83 |
| FROMRIGHT | other | 3.5K | 612 | 301 96; 1 94; 401 93; 101 86 |
| TORIGHT | other | 3.6K | 611 | 499 99; 199 93; 399 92; 799 85 |
| ADDRNUMTYPE | category | 3 | 0 | STD EVEN ODD 9.8K; CONTIGUOUS 225; OTHER 13 |
| FULLNAME | who | 3.8K | 0 | Camden Ave 99; Santa Teresa Blvd 71; Curtner Ave 67; Sierra Rd 65 |
| ONEWAYDIR | category | 3 | 0 | B 10.0K; N 24; P 14 |
| MODELFLAG | category | 2 | 0 | S 9.3K; M 747 |
| STREETCLASS | category | 6 | 0 | RE 8.2K; MI 839; CO 498; MA 425 |
| FUNCTCLASS | category | 5 | 0 | LO 8.0K; MA 1.3K; NC 561; AR 39 |
| SPEEDLIMIT | category | 10 | 0 | 25 8.2K; 35 877; 40 417; 30 329 |
| PRIVATE | other | 1 | 0 | No 10.0K |
| OFFICIAL | other | 1 | 0 | Yes 10.0K |
| MUNILEFT | category | 11 | 0 | SJ 7.3K; CO 741; CA 512; SC 470 |
| MUNIRIGHT | category | 11 | 0 | SJ 7.2K; CO 758; CA 529; SC 494 |
| ZIPLEFT | category | 43 | 0 | 95132 1.0K; 95124 1.0K; 95120 833; 95123 756 |
| ZIPRIGHT | category | 43 | 0 | 95132 1.0K; 95124 1.0K; 95120 833; 95123 759 |
| FOCWIDTH | amount | 1.4K | 6 | 39 679; 40 265; 43 255; 39.1 249 |
| ROWWIDTH | amount | 1.4K | 6 | 60 1.1K; 59 546; 52 396; 59.1 181 |
| FEATURECLASS | who | 1 | 0 | StreetCenterline 10.0K |
| PLANCRT | who | 154 | 2 | MGE 8.1K; COUNTY DATASET 1.1K; GDT 215; AERIAL PHOTO 67 |
| PLANMOD | category | 36 | 34 | MGE 8.6K; COUNTY DATASET 1.1K; GDT 217; AERIAL PHOTO 65 |
| LASTUPDATE | who | 1.5K | 0 | 2025/07/30 21:25:21+00 2.1K; 2019/06/27 23:59:50+00 150; 2019/06/27 23:58:39+00 145; 2019/06/27 23:59:52+00 142 |
| NOTES | who | 78 | 7.1K | BM HD 90821 1.0K; DS: ZipUpdate 428; Directions: Address Gap I 288; T_Shape: Address Gap Igno 219 |
| RSN | id | 7.4K | 2.5K | 373894 38; 377841 38; 356972 38; 383780 38 |
| INCORPORATED | category | 2 | 0 | Yes 7.4K; No 2.6K |
| SHAPE_LENGTH | amount | 10.0K | 0 | 733.175897667674 50; 287.160215575092 50; 473.348609095919 50; 236.778471183639 50 |
| ESNLEFT | category | 15 | 559 | 216 6.9K; 225 487; 204 486; 222 449 |
| ESNRIGHT | category | 14 | 570 | 216 6.9K; 204 501; 225 500; 222 472 |
| FHWAFUNCTCLASS | category | 8 | 96 | 7 7.4K; 4 914; 5 832; 3 703 |
| CREATIONDATE | who | 1 | 0 | 1900/01/01 00:00:00+00 10.0K |
| RESPONSIBILITY | category | 12 | 0 | SJ 7.3K; CO 722; CA 510; SC 457 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:49:01.52149 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 968311de-aa2b-421f-a084-3 10.0K |
| SRC_SHA256 | who | 1 | 0 | 97967a37d89bb55e27358ac4d 10.0K |
