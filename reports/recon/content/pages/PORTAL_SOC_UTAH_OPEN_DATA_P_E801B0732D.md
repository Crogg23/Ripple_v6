# PORTAL_SOC_UTAH_OPEN_DATA_P_E801B0732D

rows 2.0K  columns 28  scan 4.6s

roles: amount 2, audit 2, category 16, date 3, id 3, who 3

## when

CREATE_DATE
  1899      2.0K  ##############################
  2016         3  

MODIFY_DATE
  1899      2.0K  ##############################
  2016         7  

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_STAREA | 2.0K | 0.04 | 1.94M | 3.21M | 7.51M | 3.00B |
| SHAPE_STLENGTH | 2.0K | 6.56 | 6.2K | 8.5K | 16.2K | 9.09M |

## who

SERIAL_NR by rows
      1.2K  Federal
       108  Tribal
         7  nan
         4  UTUTAA 022875
         4  UTSL  0063386
         3  UTU    077266PU
         3  UTSL  0025044  01
         3  UTU    0772666P
         3  UTSL  0066716
         3  UTSL  0025979
         3  UTV   0006080
         3  UTSL  0048977
         3  UTU   0142146
         3  UTU   0136789
         2  UTSL  0036466
         2  UTU    079162P4
         2  UTU    025761
         2  UTU  009761
         2  UTSL  0048048
         2  UTU  068271

SERIAL_NR by dollars
       2.53B     1.2K rows  Federal
     213.74M      108 rows  Tribal
       7.77M        3 rows  UTU    077266PU
       7.73M        3 rows  UTU    0772666P
       5.43M        4 rows  UTUTAA 022875
       5.18M        2 rows  UTU    048793PT
       5.18M        2 rows  UTU    079162P4
       3.06M        3 rows  UTU   0142146
       2.82M        7 rows  nan
       2.64M        2 rows  UTU    0772667P
       2.61M        1 rows  UTSL  0063390
       2.60M        1 rows  UTSL  0064934  01
       2.60M        1 rows  UTSL  0018699
       2.60M        2 rows  UTSL  0062624  01
       2.59M        1 rows  UTU    086338
       2.59M        1 rows  UTU    052743PT
       2.59M        1 rows  UTU    077266P4
       2.59M        1 rows  UTU    008965
       2.59M        1 rows  UTU    079162PC
       2.59M        1 rows  UTU    0772665P

PATENT_NR by rows
      1.2K  Federal
       105  Tribal
        72  RECON
        21  ACQ
         6  IL 107
         5  IL 73
         4  UNKNOWN
         4  1202944
         4  IL 123
         4  43690004
         4  ACQ 1/2 MIN
         4  1121151
         3  43650201
         3  IL 49
         3  979837
         3  1135721
         3  IL 124
         3  QCD
         3  630039
         3  1110812

PATENT_NR by dollars
       2.53B     1.2K rows  Federal
     211.86M      105 rows  Tribal
      80.18M       72 rows  RECON
       8.33M       21 rows  ACQ
       5.43M        4 rows  1202944
       3.10M        4 rows  UNKNOWN
       3.06M        3 rows  43660109
       2.61M        1 rows  1121759
       2.60M        1 rows  853380
       2.59M        1 rows  43700020
       2.58M        1 rows  1212876
       2.57M        1 rows  958750
       2.53M        1 rows  LS 5890
       2.38M        1 rows  1103617
       1.93M        2 rows  SS 18
       1.45M        2 rows  IL 2
       1.34M        1 rows  944899
       1.33M        1 rows  1091859
       1.32M        2 rows  1152615
       1.32M        2 rows  1102341

SRC_SHA256 by rows
      2.0K  e1a54bc2966e8587b7678b167dd5ff295dd9260de02fc8128f3bde5b4a4b60e6

SRC_SHA256 by dollars
       3.00B     2.0K rows  e1a54bc2966e8587b7678b167dd5ff295dd9260de02fc8128f3bde5b4a4b

## who x when

SERIAL_NR by CREATE_DATE, dollars = SHAPE_STAREA
  Federal                                   1899:2.53B 2016:158.21
  Tribal                                    1899:213.73M 2016:9.3K
  UTSL  0018699                             1899:2.60M
  UTSL  0025044  01                         1899:1.62M
  UTSL  0025979                             1899:508.7K
  UTSL  0036466                             1899:329.6K
  UTSL  0048048                             1899:487.5K
  UTSL  0048977                             1899:494.4K
  UTSL  0062624  01                         1899:2.60M
  UTSL  0063386                             1899:1.14M
  UTSL  0063390                             1899:2.61M
  UTSL  0064934  01                         1899:2.60M
  UTSL  0066716                             1899:491.2K
  UTU    008965                             1899:2.59M
  UTU    025761                             1899:314.7K
  UTU    048793PT                           1899:5.18M
  UTU    052743PT                           1899:2.59M
  UTU    0772666P                           1899:7.73M
  UTU    0772667P                           1899:2.64M
  UTU    077266P4                           1899:2.59M
  UTU    077266PU                           1899:7.77M
  UTU    079162P4                           1899:5.18M
  UTU    086338                             1899:2.59M
  UTU   0136789                             1899:400.7K
  UTU   0142146                             1899:3.06M
  UTU  009761                               1899:80.8K
  UTU  068271                               1899:249.3K
  UTUTAA 022875                             1899:5.43M
  UTV   0006080                             1899:472.4K
  nan                                       1899:2.82M

PATENT_NR by CREATE_DATE, dollars = SHAPE_STAREA
  1103617                                   1899:2.38M
  1110812                                   1899:494.4K
  1121151                                   1899:1.14M
  1121759                                   1899:2.61M
  1135721                                   1899:491.2K
  1202944                                   1899:5.43M
  1212876                                   1899:2.58M
  43650201                                  1899:400.7K
  43660109                                  1899:3.06M
  43690004                                  1899:972.0K
  43700020                                  1899:2.59M
  630039                                    1899:472.4K
  853380                                    1899:2.60M
  958750                                    1899:2.57M
  979837                                    1899:508.7K
  ACQ                                       1899:8.33M
  ACQ 1/2 MIN                               1899:635.4K
  Federal                                   1899:2.53B 2016:158.21
  IL 107                                    1899:808.1K
  IL 123                                    1899:648.8K
  IL 124                                    1899:973.5K
  IL 2                                      1899:1.45M
  IL 49                                     1899:479.9K
  IL 73                                     1899:984.7K
  LS 5890                                   1899:2.53M
  QCD                                       1899:329.8K
  RECON                                     1899:80.18M
  SS 18                                     1899:1.93M
  Tribal                                    1899:211.85M 2016:9.3K
  UNKNOWN                                   1899:3.10M

## what

ALL_MIN: X 82%, nan 11%, I 7%

COUNTY: SAN JUAN 17%, TOOELE 12%, UINTAH 9%, MILLARD 9%, GARFIELD 8%, KANE 8%, DUCHESNE 8%, EMERY 7%, CARBON 7%, GRAND 6%, JUAB 5%, WASHINGTON 5%

ADMIN: Federal 87%, Tribal 6%, NPS 3%, DOD 3%, Private 1%, USP 0%, SL&F 0%, USFWS 0%

SECTION: 30 10%, 4 9%, 6 9%, 24 9%, 13 8%, 7 8%, 35 8%, 1 8%, 12 8%, 28 8%, 17 8%, 21 8%

CREATE_BY: vjones 100%, TJNELSON 0%

MODIFY_BY: UNK 100%, TJNELSON 0%

STATUS: AX 82%, PX 9%, AI 7%, PI 1%, UK 0%

OIL_GAS: nan 94%, X 5%, I 1%

POTASH_POT: nan 99%, X 1%

OIL_SHALE: nan 98%, I 1%, X 1%

COAL: nan 95%, X 4%, I 0%

PHOSPHATE: nan 99%, X 1%

UNKNOWN: nan 100%, X 0%

SODIUM: nan 99%, X 1%

GILSONITE: nan 100%, X 0%

GEO_STEAM: nan 100%, X 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| THE_GEOM | id | 2.0K | 0 | {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10 |
| OBJECTID | id | 2.0K | 0 | 82809 10; 64072 10; 100790 10; 94896 10 |
| SERIAL_NR | who | 607 | 0 | Federal 1.2K; Tribal 108; nan 7; UTSL  0063386 5 |
| GCDBDIVID | id | 1.9K | 0 | UT260150S0120E25 10; UT260430S0010W0SN290 10; UT260310S0030E0SN010 10; UT260330S0250E0SN130 10 |
| ALL_MIN | category | 3 | 0 | X 1.6K; nan 217; I 134 |
| COUNTY | category | 29 | 0 | SAN JUAN 238; TOOELE 169; UINTAH 126; MILLARD 124 |
| PATENT_NR | who | 499 | 0 | Federal 1.2K; Tribal 105; RECON 72; ACQ 21 |
| ADMIN | category | 8 | 0 | Federal 1.7K; Tribal 112; NPS 64; DOD 61 |
| SHAPE_STAREA | amount | 1.9K | 0 | 157504.65197929999 10; 795979.91437899997 10; 2576456.074273 10; 648432.5111 10 |
| SHAPE_STLENGTH | amount | 2.0K | 0 | 1587.8394015238737 10; 4258.6262150635921 10; 6419.9777664719368 10; 3221.0088002232587 10 |
| SECTION | category | 39 | 0 | 30 79; 4 76; 6 74; 24 73 |
| CREATE_DATE | date | 4 | 0 | 1899-12-30T00:43:34.000Z 2.0K; 2016-07-01T14:55:34.000Z 1; 2016-07-01T14:50:56.000Z 1; 2016-07-01T14:44:46.000Z 1 |
| CREATE_BY | category | 2 | 0 | vjones 2.0K; TJNELSON 3 |
| MODIFY_DATE | date | 8 | 0 | 1899-12-30T00:00:09.000Z 2.0K; 2016-07-01T15:13:22.000Z 1; 2016-07-01T14:56:48.000Z 1; 2016-07-01T14:50:56.000Z 1 |
| MODIFY_BY | category | 2 | 0 | UNK 2.0K; TJNELSON 7 |
| STATUS | category | 5 | 0 | AX 1.6K; PX 180; AI 134; PI 28 |
| OIL_GAS | category | 3 | 0 | nan 1.9K; X 91; I 27 |
| POTASH_POT | category | 2 | 0 | nan 2.0K; X 23 |
| OIL_SHALE | category | 3 | 0 | nan 2.0K; I 26; X 14 |
| COAL | category | 3 | 0 | nan 1.9K; X 90; I 1 |
| PHOSPHATE | category | 2 | 0 | nan 2.0K; X 18 |
| UNKNOWN | category | 2 | 0 | nan 2.0K; X 10 |
| SODIUM | category | 2 | 0 | nan 2.0K; X 20 |
| GILSONITE | category | 2 | 0 | nan 2.0K; X 4 |
| GEO_STEAM | category | 2 | 0 | nan 2.0K; X 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:10:50.16041 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4dab3f80-40a1-49f2-9ba2-4 2.0K |
| SRC_SHA256 | who | 1 | 0 | e1a54bc2966e8587b7678b167 2.0K |
