# PORTAL_SOC_UTAH_OPEN_DATA_P_2F94947455

rows 2.0K  columns 26  scan 3.2s

roles: audit 2, category 16, date 3, id 3, who 3

## when

CREATE_DATE
  1899      2.0K  ##############################
  2016         5  

MODIFY_DATE
  1899      2.0K  ##############################
  2016        13  

INGESTED_AT
  2026      2.0K  ##############################

## who

SERIAL_NR by rows
      1.2K  Federal
        74  Tribal
         6  nan
         4  UTU    0772666P
         4  UTU   0136789
         4  UTU    0772667P
         4  UTU    077266PU
         3  UTU    049193FD
         3  UTV   0006022
         3  UTSL  0049624
         3  UTSL  0025044  01
         3  UTU    077266PS
         3  UTU   0013961
         3  UTSL  0066716
         3  UTU   0032432
         3  UTSL  0034460
         3  UTU   0096457
         3  UTU    077266FA
         3  UTU   0142146
         2  UTSL  0022268

PATENT_NR by rows
      1.2K  Federal
        73  Tribal
        66  RECON
        21  ACQ
         5  ACQ 1/2 MIN
         4  IL 109
         4  43650201
         3  43690008
         3  1098599
         3  1168033
         3  IL 73
         3  1135721
         3  IL 102
         3  1130380
         3  1064056
         3  43-84-0018;
         3  SS 19
         3  43-99-0014;
         3  43660109
         3  IL 253

SRC_SHA256 by rows
      2.0K  64a2acad34c913a7597bc19cf90650be8666ac9114d8e340442eb31fff0e6977

## who x when

SERIAL_NR by CREATE_DATE
  Federal                                   1899:1.2K 2016:3
  Tribal                                    1899:72 2016:2
  UTSL  0022268                             1899:2
  UTSL  0025044  01                         1899:3
  UTSL  0034460                             1899:3
  UTSL  0049624                             1899:3
  UTSL  0066716                             1899:3
  UTU    049193FD                           1899:3
  UTU    0772666P                           1899:4
  UTU    0772667P                           1899:4
  UTU    077266FA                           1899:3
  UTU    077266PS                           1899:3
  UTU    077266PU                           1899:4
  UTU   0013961                             1899:3
  UTU   0032432                             1899:3
  UTU   0096457                             1899:3
  UTU   0136789                             1899:4
  UTU   0142146                             1899:3
  UTV   0006022                             1899:3
  nan                                       1899:6

PATENT_NR by CREATE_DATE
  1064056                                   1899:3
  1098599                                   1899:3
  1130380                                   1899:3
  1135721                                   1899:3
  1168033                                   1899:3
  43-84-0018;                               1899:3
  43-99-0014;                               1899:3
  43650201                                  1899:4
  43660109                                  1899:3
  43690008                                  1899:3
  ACQ                                       1899:21
  ACQ 1/2 MIN                               1899:5
  Federal                                   1899:1.2K 2016:3
  IL 102                                    1899:3
  IL 109                                    1899:4
  IL 253                                    1899:3
  IL 73                                     1899:3
  RECON                                     1899:66
  SS 19                                     1899:3
  Tribal                                    1899:71 2016:2

## what

COUNTY: SAN JUAN 13%, TOOELE 11%, UINTAH 10%, GARFIELD 10%, EMERY 8%, MILLARD 8%, KANE 8%, DUCHESNE 7%, GRAND 7%, IRON 7%, BOX ELDER 6%, WASHINGTON 6%

SECTION: 6 10%, 18 9%, 24 8%, 20 8%, 3 8%, 31 8%, 30 8%, 14 8%, 7 8%, 10 8%, 33 8%, 12 8%

ALL_MIN: X 85%, nan 10%, I 5%

ADMIN: Federal 87%, NPS 5%, Tribal 4%, DOD 3%, Private 1%, USFWS 0%, USP 0%, SL&F 0%, UDWR 0%

CREATE_BY: vjones 100%, TJNELSON 0%

MODIFY_BY: UNK 99%, TJNELSON 1%

STATUS: AX 85%, PX 8%, AI 5%, PI 2%, UK 0%

COAL: nan 97%, X 3%, I 0%

OIL_GAS: nan 94%, X 5%, I 2%

PHOSPHATE: nan 99%, X 1%

GILSONITE: nan 100%, X 0%

POTASH_POT: nan 99%, X 1%

SODIUM: nan 99%, X 1%

GEO_STEAM: nan 100%, X 0%

OIL_SHALE: nan 98%, I 1%, X 1%

UNKNOWN: nan 100%, X 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| THE_GEOM | id | 2.0K | 0 | {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10 |
| OBJECTID | id | 2.0K | 0 | 76322 10; 46682 10; 85299 10; 38320 10 |
| SERIAL_NR | who | 595 | 0 | Federal 1.2K; Tribal 74; nan 6; UTU   0136789 6 |
| PATENT_NR | who | 522 | 0 | Federal 1.2K; Tribal 73; RECON 66; ACQ 21 |
| COUNTY | category | 30 | 0 | SAN JUAN 180; TOOELE 150; UINTAH 141; GARFIELD 135 |
| GCDBDIVID | id | 1.9K | 0 | UT260020S0150W0SN330 10; UT260300S0190E0UP180 10; UT300060S0060W0SN230 10; UT260260S0140W0SN010 10 |
| SECTION | category | 38 | 0 | 6 79; 18 75; 24 70; 20 69 |
| ALL_MIN | category | 3 | 0 | X 1.7K; nan 192; I 109 |
| ADMIN | category | 9 | 0 | Federal 1.7K; NPS 91; Tribal 78; DOD 58 |
| CREATE_DATE | date | 6 | 0 | 1899-12-30T00:43:34.000Z 2.0K; 2016-07-01T15:03:15.000Z 1; 2016-07-01T14:55:34.000Z 1; 2016-07-01T15:04:45.000Z 1 |
| CREATE_BY | category | 2 | 0 | vjones 2.0K; TJNELSON 5 |
| MODIFY_DATE | date | 14 | 0 | 1899-12-30T00:00:09.000Z 2.0K; 2016-07-01T15:03:41.000Z 1; 2016-07-01T15:31:57.000Z 1; 2016-07-01T15:33:47.000Z 1 |
| MODIFY_BY | category | 2 | 0 | UNK 2.0K; TJNELSON 13 |
| STATUS | category | 5 | 0 | AX 1.7K; PX 157; AI 109; PI 33 |
| COAL | category | 3 | 0 | nan 1.9K; X 66; I 3 |
| OIL_GAS | category | 3 | 0 | nan 1.9K; X 91; I 30 |
| PHOSPHATE | category | 2 | 0 | nan 2.0K; X 13 |
| GILSONITE | category | 2 | 0 | nan 2.0K; X 6 |
| POTASH_POT | category | 2 | 0 | nan 2.0K; X 21 |
| SODIUM | category | 2 | 0 | nan 2.0K; X 21 |
| GEO_STEAM | category | 2 | 0 | nan 2.0K; X 10 |
| OIL_SHALE | category | 3 | 0 | nan 2.0K; I 27; X 12 |
| UNKNOWN | category | 2 | 0 | nan 2.0K; X 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:09:12.38284 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0afe7e81-0975-473e-8221-c 2.0K |
| SRC_SHA256 | who | 1 | 0 | 64a2acad34c913a7597bc19cf 2.0K |
