# PORTAL_SOC_UTAH_OPEN_DATA_P_B21F81E6F9

rows 2.0K  columns 28  scan 4.5s

roles: amount 2, audit 2, category 15, date 3, id 3, who 4

## when

CREATE_DATE
  1899      2.0K  ##############################

MODIFY_DATE
  1899      2.0K  ##############################
  2016         6  

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_STAREA | 2.0K | 0.14 | 1.95M | 3.07M | 5.20M | 3.05B |
| SHAPE_STLENGTH | 2.0K | 7.37 | 6.3K | 8.2K | 10.0K | 9.19M |

## who

SERIAL_NR by rows
      1.2K  Federal
        88  Tribal
         7  nan
         6  UTU    0772666P
         5  UTU    0772667P
         4  UTU   0142146
         4  UTUTAA 022875
         4  UTU    077266PU
         3  UTU   0136789
         3  UTSL  0051064
         3  UTSL  0030956
         2  UTSL  0025044  01
         2  UTSL  0036239
         2  UTSL  0020297
         2  UTSL  0019043
         2  UTV   0008041
         2  UTU   0032432
         2  UTU   0004794
         2  UTSL  0019698
         2  UTU   0002226

SERIAL_NR by dollars
       2.61B     1.2K rows  Federal
     180.01M       88 rows  Tribal
      13.20M        6 rows  UTU    0772666P
      12.99M        5 rows  UTU    0772667P
       7.76M        4 rows  UTU    077266PU
       5.61M        4 rows  UTUTAA 022875
       2.88M        7 rows  nan
       2.88M        1 rows  UTU    040126
       2.74M        2 rows  UTU    077266PZ
       2.69M        2 rows  UTU    016707FD
       2.64M        1 rows  UTU    050116PT
       2.61M        1 rows  UTSL  0018771
       2.60M        1 rows  UTSL  0018699
       2.59M        1 rows  UTU    086338
       2.59M        1 rows  UTU    052743PT
       2.59M        1 rows  UTU    008965
       2.59M        1 rows  UTU    079162PC
       2.59M        1 rows  UTU    079162PN
       2.59M        1 rows  UTU    048793PT
       2.59M        1 rows  UTSL  0033178

PATENT_NR by rows
      1.2K  Federal
        85  Tribal
        71  RECON
        19  ACQ
         4  IL 73
         4  IL 68
         4  1202944
         4  ACQ 1/2 MIN
         4  43660109
         3  1036037
         3  SS 19
         3  IL 107
         3  3-52
         3  IL 124
         3  43690004
         3  IL 31
         3  1113585
         3  43650201
         2  1001543
         2  43-84-0021;

PATENT_NR by dollars
       2.61B     1.2K rows  Federal
     178.23M       85 rows  Tribal
      76.59M       71 rows  RECON
       7.23M       19 rows  ACQ
       5.61M        4 rows  1202944
       5.16M        2 rows  X
       2.88M        1 rows  43820011
       2.69M        2 rows  43-82-0002;
       2.61M        1 rows  956309
       2.60M        1 rows  853380
       2.59M        1 rows  43700020
       2.59M        1 rows  1041236
       2.57M        1 rows  958750
       2.46M        1 rows  UNKNOWN
       2.27M        1 rows  1033541
       1.90M        2 rows  43-86-0009;
       1.34M        1 rows  944899
       1.34M        1 rows  1151463
       1.33M        1 rows  1091859
       1.33M        2 rows  1121151

CREATE_BY by rows
      2.0K  vjones

CREATE_BY by dollars
       3.05B     2.0K rows  vjones

SRC_SHA256 by rows
      2.0K  6a41c35ee0dc1f77cb4a6372b1d0f50bd9f6f24cdc51799eaa8c6e3c5d254dc1

SRC_SHA256 by dollars
       3.05B     2.0K rows  6a41c35ee0dc1f77cb4a6372b1d0f50bd9f6f24cdc51799eaa8c6e3c5d25

## who x when

SERIAL_NR by MODIFY_DATE, dollars = SHAPE_STAREA
  Federal                                   1899:2.61B 2016:1.45M
  Tribal                                    1899:176.30M 2016:3.71M
  UTSL  0018699                             1899:2.60M
  UTSL  0018771                             1899:2.61M
  UTSL  0019043                             1899:492.4K
  UTSL  0019698                             1899:318.0K
  UTSL  0020297                             1899:339.3K
  UTSL  0025044  01                         1899:1.94M
  UTSL  0030956                             1899:645.4K
  UTSL  0036239                             1899:323.4K
  UTSL  0051064                             1899:485.4K
  UTU    008965                             1899:2.59M
  UTU    016707FD                           1899:2.69M
  UTU    040126                             1899:2.88M
  UTU    050116PT                           1899:2.64M
  UTU    052743PT                           1899:2.59M
  UTU    0772666P                           1899:13.20M
  UTU    0772667P                           1899:12.99M
  UTU    077266PU                           1899:7.76M
  UTU    077266PZ                           1899:2.74M
  UTU    079162PC                           1899:2.59M
  UTU    086338                             1899:2.59M
  UTU   0002226                             1899:325.8K
  UTU   0004794                             1899:323.0K
  UTU   0032432                             1899:808.2K
  UTU   0136789                             1899:971.8K
  UTU   0142146                             1899:957.6K
  UTUTAA 022875                             1899:5.61M
  UTV   0008041                             1899:283.1K
  nan                                       1899:2.88M

PATENT_NR by MODIFY_DATE, dollars = SHAPE_STAREA
  1001543                                   1899:318.0K
  1033541                                   1899:2.27M
  1036037                                   1899:645.4K
  1041236                                   1899:2.59M
  1113585                                   1899:485.4K
  1202944                                   1899:5.61M
  3-52                                      1899:491.1K
  43-82-0002;                               1899:2.69M
  43-84-0021;                               1899:201.4K
  43650201                                  1899:971.8K
  43660109                                  1899:957.6K
  43690004                                  1899:440.0K
  43700020                                  1899:2.59M
  43820011                                  1899:2.88M
  853380                                    1899:2.60M
  956309                                    1899:2.61M
  958750                                    1899:2.57M
  ACQ                                       1899:7.23M
  ACQ 1/2 MIN                               1899:578.6K
  Federal                                   1899:2.61B 2016:1.45M
  IL 107                                    1899:484.1K
  IL 124                                    1899:488.3K
  IL 31                                     1899:647.4K
  IL 68                                     1899:648.7K
  IL 73                                     1899:656.5K
  RECON                                     1899:76.59M
  SS 19                                     1899:437.5K
  Tribal                                    1899:174.52M 2016:3.71M
  UNKNOWN                                   1899:2.46M
  X                                         1899:5.16M

## what

ALL_MIN: X 84%, nan 11%, I 6%

COUNTY: SAN JUAN 15%, TOOELE 12%, MILLARD 10%, UINTAH 9%, KANE 9%, DUCHESNE 8%, GARFIELD 8%, GRAND 7%, EMERY 7%, CARBON 6%, UTAH 5%, BOX ELDER 5%

ADMIN: Federal 88%, Tribal 4%, NPS 3%, DOD 3%, Private 1%, USP 0%, BR 0%, SL&F 0%, UDWR 0%, UDOT 0%, USFWS 0%

SECTION: 13 9%, 4 9%, 35 9%, 6 9%, 22 8%, 34 8%, 31 8%, 24 8%, 30 8%, 21 8%, 7 8%, 28 7%

MODIFY_BY: UNK 100%, TJNELSON 0%

STATUS: AX 84%, PX 9%, AI 6%, PI 1%, UK 0%

OIL_GAS: nan 94%, X 4%, I 1%

OIL_SHALE: nan 98%, I 1%, X 1%

POTASH_POT: nan 99%, X 1%

COAL: nan 95%, X 5%, I 0%

PHOSPHATE: nan 99%, X 1%

UNKNOWN: nan 100%, X 0%

SODIUM: nan 99%, X 1%

GILSONITE: nan 100%, X 0%

GEO_STEAM: nan 99%, X 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| THE_GEOM | id | 2.0K | 0 | {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10 |
| OBJECTID | id | 2.0K | 0 | 78395 10; 65947 10; 29825 10; 84899 10 |
| SERIAL_NR | who | 598 | 0 | Federal 1.2K; Tribal 88; nan 7; UTU    0772666P 6 |
| GCDBDIVID | id | 2.0K | 0 | UT260030N0050E12 10; UT260210S0100W0SN230 10; UT300060S0090W0SN180 10; UT260340S0240E17 10 |
| ALL_MIN | category | 3 | 0 | X 1.7K; nan 212; I 112 |
| COUNTY | category | 28 | 0 | SAN JUAN 220; TOOELE 168; MILLARD 139; UINTAH 132 |
| PATENT_NR | who | 506 | 0 | Federal 1.2K; Tribal 85; RECON 71; ACQ 19 |
| ADMIN | category | 11 | 0 | Federal 1.8K; Tribal 88; NPS 62; DOD 61 |
| SHAPE_STAREA | amount | 2.0K | 0 | 156363.536000575 10; 40514.805719999997 10; 2486453.7888500001 10; 161525.427716265 10 |
| SHAPE_STLENGTH | amount | 2.0K | 0 | 1582.0844032985697 10; 805.13456543574387 10; 6309.5764189177016 10; 1607.6113515952031 10 |
| SECTION | category | 39 | 0 | 13 77; 4 76; 35 74; 6 72 |
| CREATE_DATE | date | 1 | 0 | 1899-12-30T00:43:34.000Z 2.0K |
| CREATE_BY | who | 1 | 0 | vjones 2.0K |
| MODIFY_DATE | date | 7 | 0 | 1899-12-30T00:00:09.000Z 2.0K; 2016-06-30T15:37:47.000Z 1; 2016-06-30T16:20:42.000Z 1; 2016-07-01T15:23:22.000Z 1 |
| MODIFY_BY | category | 2 | 0 | UNK 2.0K; TJNELSON 6 |
| STATUS | category | 5 | 0 | AX 1.7K; PX 177; AI 112; PI 28 |
| OIL_GAS | category | 3 | 0 | nan 1.9K; X 88; I 27 |
| OIL_SHALE | category | 3 | 0 | nan 2.0K; I 26; X 14 |
| POTASH_POT | category | 2 | 0 | nan 2.0K; X 21 |
| COAL | category | 3 | 0 | nan 1.9K; X 92; I 1 |
| PHOSPHATE | category | 2 | 0 | nan 2.0K; X 21 |
| UNKNOWN | category | 2 | 0 | nan 2.0K; X 8 |
| SODIUM | category | 2 | 0 | nan 2.0K; X 20 |
| GILSONITE | category | 2 | 0 | nan 2.0K; X 5 |
| GEO_STEAM | category | 2 | 0 | nan 2.0K; X 12 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:09:20.52381 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | ae09e778-0240-431a-9e6a-3 2.0K |
| SRC_SHA256 | who | 1 | 0 | 6a41c35ee0dc1f77cb4a6372b 2.0K |
