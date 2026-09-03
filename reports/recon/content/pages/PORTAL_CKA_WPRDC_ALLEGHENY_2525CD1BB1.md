# PORTAL_CKA_WPRDC_ALLEGHENY_2525CD1BB1

rows 583  columns 10  scan 3.5s

roles: amount 2, audit 2, category 1, date 1, other 2, who 3

## when

INGESTED_AT
  2026       583  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENG | 517 | 0 | 14 | 1.2K | 3.1K | 37.0K |
| SHAPE_LENGTH | 583 | 1.65 | 18.89 | 1.5K | 3.1K | 47.7K |

## who

BRBIDGE_NAME by rows
         4  Thompson's Run North Side Br
         2  Thoms Run No. 2
         2  Beck's Run Rd Bridge No.2
         2  Thompson Run  North Side Br #
         2  Thompson Run East Branch Br #
         2  Homestead High Level (Ramp)
         1  Tennis Court's S Park Br #13
         1  Girty's Run Br #1
         1  Wible Run No. 1
         1  Gourdhead Run Br #5
         1  Catfish Run Bridge #21
         1  Bull Run Br #1
         1  Big Sewickley Creek Br #17
         1  Douglas Run Br #14
         1  Girty's Run No. 10
         1  Mansfield Br
         1  Pangburn Hollow Br #13
         1  McRobert's Run Br #2
         1  Plum Creek Upper Branch No 2
         1  Catfish Run No 5

BRBIDGE_NAME by dollars
        3.1K        1 rows  HOMESTEAD HIGH LEV
        2.4K        1 rows  Rankin Bridge
        2.3K        1 rows  Glenwood Bridge
        2.1K        1 rows  Sixteenth St Bridge
        1.9K        1 rows  Mansfield Br
        1.5K        1 rows  Riverton Bridge
        1.4K        1 rows  Armstrong Tunnels
        1.3K        1 rows  S Tenth St Bridge
        1.1K        1 rows  Coraopolis Bridge
        1.1K        1 rows  Seventh St Br
        1.1K        2 rows  Homestead High Level (Ramp)
      996.43        1 rows  Ninth St Br
      994.63        1 rows  Sixth St Br
      916.85        1 rows  Douglas Run Road over Youghio
      854.65        1 rows  Windgap Avenue Bridge
      832.96        1 rows  Levi Bird Duff Br
      811.32        1 rows  Fleming Park Bridge
      779.27        1 rows  Homeville Rd Viaduct
      769.19        1 rows  JACKS RUN NO. 1
      673.29        1 rows  Dooker's Hollow Br #1

FACILITY_ID by rows
         3  180
         3  390
         3  366
         3  388
         3  490
         3  385
         2  387
         2  41
         2  491
         2  392
         2  352
         2  259
         2  288
         2  370
         2  247
         2  267
         2  358
         2  386
         2  492
         2  384

FACILITY_ID by dollars
        3.1K        1 rows  317
        2.4K        1 rows  38
        2.3K        1 rows  294
        1.9K        1 rows  50
        1.4K        1 rows  1
        1.3K        1 rows  295
        1.1K        2 rows  353
        1.1K        1 rows  239
      996.43        1 rows  240
      994.63        1 rows  238
      916.85        1 rows  500
      903.40        2 rows  256
      854.65        1 rows  73
      832.96        1 rows  89
      811.32        1 rows  354
      779.27        1 rows  57
      769.19        1 rows  333
      668.99        1 rows  316
      593.04        1 rows  61
      469.47        1 rows  62

SRC_SHA256 by rows
       583  6cb64a71156c3df73ffd0a079e579bd51221e21f53c5eef1a202350d1b6a1aae

SRC_SHA256 by dollars
       47.7K      583 rows  6cb64a71156c3df73ffd0a079e579bd51221e21f53c5eef1a202350d1b6a

## who x when

BRBIDGE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Armstrong Tunnels                         2026:1.4K
  Beck's Run Rd Bridge No.2                 2026:69.57
  Big Sewickley Creek Br #17                2026:5.03
  Bull Run Br #1                            2026:6.80
  Catfish Run Bridge #21                    2026:5.44
  Catfish Run No 5                          2026:28.07
  Coraopolis Bridge                         2026:1.1K
  Douglas Run Br #14                        2026:4.41
  Girty's Run Br #1                         2026:10.75
  Girty's Run No. 10                        2026:39.84
  Glenwood Bridge                           2026:2.3K
  Gourdhead Run Br #5                       2026:6.53
  HOMESTEAD HIGH LEV                        2026:3.1K
  Homestead High Level (Ramp)               2026:1.1K
  Mansfield Br                              2026:1.9K
  McRobert's Run Br #2                      2026:8.59
  Ninth St Br                               2026:996.43
  Pangburn Hollow Br #13                    2026:6.20
  Plum Creek Upper Branch No 2              2026:31.06
  Rankin Bridge                             2026:2.4K
  Riverton Bridge                           2026:1.5K
  S Tenth St Bridge                         2026:1.3K
  Seventh St Br                             2026:1.1K
  Sixteenth St Bridge                       2026:2.1K
  Tennis Court's S Park Br #13              2026:7.13
  Thompson Run  North Side Br #             2026:49.87
  Thompson Run East Branch Br #             2026:89.19
  Thompson's Run North Side Br              2026:48.15
  Thoms Run No. 2                           2026:22.72
  Wible Run No. 1                           2026:21.34

FACILITY_ID by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  1                                         2026:1.4K
  180                                       2026:189.16
  238                                       2026:994.63
  239                                       2026:1.1K
  240                                       2026:996.43
  247                                       2026:29.83
  259                                       2026:98.79
  267                                       2026:95.03
  288                                       2026:22.11
  294                                       2026:2.3K
  295                                       2026:1.3K
  317                                       2026:3.1K
  352                                       2026:12.64
  353                                       2026:1.1K
  358                                       2026:53
  366                                       2026:57.27
  370                                       2026:67.05
  38                                        2026:2.4K
  384                                       2026:12.01
  385                                       2026:96.86
  386                                       2026:80.40
  387                                       2026:77.83
  388                                       2026:130.29
  390                                       2026:115.60
  392                                       2026:6.33
  41                                        2026:133.75
  490                                       2026:48.15
  491                                       2026:22.47
  492                                       2026:28.43
  50                                        2026:1.9K

## what

BRIDGE_TYPE: Vehicle 91%, Trail 7%, Pedestrian 1%, CULVERT 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 568 | 0 | 595 3; 594 3; 593 3; 592 3 |
| BRIDGE_COD | other | 574 | 0 | TL20 3; SH01 3; PS11 3; PR01 3 |
| BRBIDGE_NAME | who | 562 | 1 | Thompson's Run North Side 6; TURTLE CREEK NO. 20 3; SHAM RUN NO 1 3; PINE CREEK, S BRANCH NO.  3 |
| FACILITY_ID | who | 452 | 87 | 390 5; 385 5; 366 5; 492 4 |
| SHAPE_LENG | amount | 169 | 66 | 5.0 38; 4.0 33; 6.0 30; 3.0 26 |
| BRIDGE_TYPE | category | 6 | 8 | Vehicle 526; Trail 41; Pedestrian 7; CULVERT 1 |
| SHAPE_LENGTH | amount | 584 | 0 | 13.0164093282702 3; 7.20842743781844 3; 7.26288430951589 3; 16.3092548496243 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:43:34.16880 583 |
| SOURCE_RUN_ID | audit | 1 | 0 | d629fe5b-43ff-4aae-bad1-0 583 |
| SRC_SHA256 | who | 1 | 0 | 6cb64a71156c3df73ffd0a079 583 |
