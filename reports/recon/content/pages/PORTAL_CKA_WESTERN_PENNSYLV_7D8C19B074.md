# PORTAL_CKA_WESTERN_PENNSYLV_7D8C19B074

rows 523  columns 15  scan 3.7s

roles: amount 6, audit 2, date 1, other 5, who 2

## when

INGESTED_AT
  2026       523  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 523 | -8.93M | -8.90M | -8.87M | -8.87M | -4.66B |
| Y | 523 | 4.90M | 4.93M | 4.96M | 4.96M | 2.58B |
| SHAPE_LENG | 523 | 0 | 14 | 1.2K | 3.1K | 37.6K |
| ET_X | 523 | 0 | 1.35M | 1.42M | 1.43M | 705.22M |
| ET_Y | 523 | 0 | 417.2K | 488.9K | 497.2K | 215.95M |
| ET_ANGLE | 523 | -60 | 134.08 | 354.47 | 359.63 | 77.4K |

## who

FACILITYID by rows
         3  390
         3  388
         3  366
         3  385
         3  490
         3  180
         2  387
         2  335
         2  392
         2  276
         2  492
         2  264
         2  407
         2  288
         2  376
         2  485
         2  352
         2  75
         2  396
         2  370

FACILITYID by dollars
      -8.87M        1 rows  274
      -8.87M        1 rows  273
      -8.87M        1 rows  167
      -8.87M        1 rows  166
      -8.87M        1 rows  321
      -8.87M        1 rows  320
      -8.87M        1 rows  420
      -8.87M        1 rows  322
      -8.88M        1 rows  319
      -8.88M        1 rows  417
      -8.88M        1 rows  379
      -8.88M        1 rows  382
      -8.88M        1 rows  380
      -8.88M        1 rows  471
      -8.88M        1 rows  383
      -8.88M        1 rows  381
      -8.88M        1 rows  482
      -8.88M        1 rows  483
      -8.88M        1 rows  416
      -8.88M        1 rows  414

SRC_SHA256 by rows
       523  0fd7130c33f4a0cfb15c556bde20ed489053071952f9e962df2b6742d356ee20

SRC_SHA256 by dollars
      -4.66B      523 rows  0fd7130c33f4a0cfb15c556bde20ed489053071952f9e962df2b6742d356

## who x when

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  166                                       2026:-8.87M
  167                                       2026:-8.87M
  180                                       2026:-26.75M
  264                                       2026:-17.76M
  273                                       2026:-8.87M
  274                                       2026:-8.87M
  276                                       2026:-17.80M
  288                                       2026:-17.79M
  319                                       2026:-8.88M
  320                                       2026:-8.87M
  321                                       2026:-8.87M
  322                                       2026:-8.87M
  335                                       2026:-17.80M
  352                                       2026:-17.86M
  366                                       2026:-26.69M
  370                                       2026:-17.82M
  376                                       2026:-17.81M
  385                                       2026:-26.68M
  387                                       2026:-17.78M
  388                                       2026:-26.66M
  390                                       2026:-26.71M
  392                                       2026:-17.78M
  396                                       2026:-17.83M
  407                                       2026:-17.81M
  417                                       2026:-8.88M
  420                                       2026:-8.87M
  485                                       2026:-17.80M
  490                                       2026:-26.65M
  492                                       2026:-17.81M
  75                                        2026:-17.83M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  0fd7130c33f4a0cfb15c556bde20ed4890530719  2026:-4.66B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 526 | 0 | -8922480.58096512 3; -8931691.8320377 3; -8930552.95626917 3; -8894757.50036173 3 |
| Y | amount | 528 | 0 | 4941251.07652476 3; 4932754.00540911 3; 4932220.63001282 3; 4912270.75936552 3 |
| FID | other | 515 | 0 | 554 3; 553 3; 552 3; 551 3 |
| BRIDGE_COD | other | 509 | 0 | LC11 4; OB02 3; MX01 3; MT15 3 |
| BRBIDGE_NA | other | 507 | 0 | Lick's Run #11 4; Thompson's Run North Side 4; Coraopolis Bridge 3; Montour Run NB Br #1 3 |
| FACILITYID | who | 457 | 18 | 353 4; 335 4; 297 4; 291 4 |
| SHAPE_LENG | amount | 174 | 0 | 5.0 38; 4.0 34; 6.0 30; 3.0 26 |
| ET_ID | other | 513 | 0 | 462 3; 461 3; 460 3; 459 3 |
| ET_IDP | other | 513 | 0 | 462 3; 461 3; 460 3; 459 3 |
| ET_X | amount | 526 | 0 | 1300751.73367 3; 1277159.62653 3; 1279968.18982 3; 1368209.46849 3 |
| ET_Y | amount | 530 | 0 | 440008.187706 3; 419504.09918 3; 418096.540046 3; 366038.877228 3 |
| ET_ANGLE | amount | 518 | 0 | 90.0 5; 0.0 4; 25.8969137022 3; 156.037483231 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:42:44.90114 523 |
| SOURCE_RUN_ID | audit | 1 | 0 | a656678a-d290-4d12-b49f-9 523 |
| SRC_SHA256 | who | 1 | 0 | 0fd7130c33f4a0cfb15c556bd 523 |
