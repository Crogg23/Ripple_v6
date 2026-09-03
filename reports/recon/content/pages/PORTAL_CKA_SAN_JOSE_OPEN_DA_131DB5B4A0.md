# PORTAL_CKA_SAN_JOSE_OPEN_DA_131DB5B4A0

rows 10.0K  columns 13  scan 3.5s

roles: amount 2, audit 2, category 2, date 3, empty 1, id 2, who 2

## when

LASTUPDATE
  2010     10.0K  ##############################

CREATIONDATE
  1900     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 10.0K | 17.74 | 577.84 | 2.5K | 6.8K | 7.30M |
| SHAPE_AREA | 10.0K | 13.92 | 1.5K | 8.3K | 22.4K | 20.27M |

## who

FACILITYID by rows
         1  1168
         1  88
         1  95
         1  538
         1  2047
         1  477
         1  693
         1  390
         1  49467
         1  1342
         1  364
         1  343
         1  860
         1  43
         1  1236
         1  200
         1  423
         1  1238
         1  418
         1  420

FACILITYID by dollars
        6.8K        1 rows  6209
        6.2K        1 rows  2366
        5.7K        1 rows  40
        5.6K        1 rows  39
        5.5K        1 rows  661
        5.3K        1 rows  663
        4.7K        1 rows  350
        4.7K        1 rows  351
        4.3K        1 rows  700
        4.3K        1 rows  654
        4.3K        1 rows  1230
        4.3K        1 rows  1252
        4.1K        1 rows  3160
        4.1K        1 rows  820
        4.1K        1 rows  210
        4.0K        1 rows  634
        3.9K        1 rows  2841
        3.9K        1 rows  6802
        3.9K        1 rows  876
        3.9K        1 rows  214

SRC_SHA256 by rows
     10.0K  c3b53673fd30dd762b1f0e8a4cef751bcd76d6d9f71a30e7b5113a254200d608

SRC_SHA256 by dollars
       7.30M    10.0K rows  c3b53673fd30dd762b1f0e8a4cef751bcd76d6d9f71a30e7b5113a254200

## who x when

FACILITYID by CREATIONDATE, dollars = SHAPE_LENGTH
  1168                                      1900:1.4K
  1236                                      1900:110.49
  1238                                      1900:1.5K
  1342                                      1900:1.3K
  200                                       1900:1.7K
  2047                                      1900:623.94
  2366                                      1900:6.2K
  343                                       1900:1.8K
  350                                       1900:4.7K
  351                                       1900:4.7K
  364                                       1900:439.66
  39                                        1900:5.6K
  390                                       1900:2.4K
  40                                        1900:5.7K
  418                                       1900:1.1K
  420                                       1900:616.20
  423                                       1900:863.86
  43                                        1900:1.5K
  477                                       1900:245.56
  49467                                     1900:479.93
  538                                       1900:857.10
  6209                                      1900:6.8K
  654                                       1900:4.3K
  661                                       1900:5.5K
  663                                       1900:5.3K
  693                                       1900:272.60
  700                                       1900:4.3K
  860                                       1900:339
  88                                        1900:22.32
  95                                        1900:506.57

SRC_SHA256 by CREATIONDATE, dollars = SHAPE_LENGTH
  c3b53673fd30dd762b1f0e8a4cef751bcd76d6d9  1900:7.30M

## what

ADACOMPLY: Yes 81%, No 19%

COVERED: No 100%, Yes 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| FACILITYID | who | 9.9K | 0 | 11332 50; 11641 50; 11652 50; 11580 50 |
| INTID | id | 9.9K | 0 | 11332 50; 11641 50; 11652 50; 11580 50 |
| ADACOMPLY | category | 2 | 0 | Yes 8.1K; No 1.9K |
| WIDTH | empty | 1 | 10.0K |  |
| COVERED | category | 2 | 0 | No 10.0K; Yes 1 |
| LASTUPDATE | date | 39 | 2 | 2010-09-09T12:43:26 395; 2010-09-09T12:43:16 395; 2010-09-09T12:43:27 393; 2010-09-09T12:43:15 393 |
| SHAPE_LENGTH | amount | 9.9K | 0 | 672.994246115855 50; 1076.54567029065 50; 478.777422636308 50; 805.348776885149 50 |
| SHAPE_AREA | amount | 10.0K | 0 | 1665.78549483786 50; 2434.32637485655 50; 1051.22788301698 50; 3052.86485618578 50 |
| CREATIONDATE | date | 1 | 0 | 1900-01-01T00:00:00 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:56:52.22959 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | af1338b1-03c8-4626-acf0-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | c3b53673fd30dd762b1f0e8a4 10.0K |
