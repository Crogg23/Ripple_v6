# PORTAL_CKA_WESTERN_PENNSYLV_57184A8FE4

rows 394  columns 18  scan 3.0s

roles: amount 1, audit 2, date 1, other 13, who 2

## when

INGESTED_AT
  2026       394  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NAME | 394 | 103.01 | 4.6K | 9.8K | 9.8K | 1.64M |

## who

NAMELSAD by rows
         1  Census Tract 4850
         1  Census Tract 5648
         1  Census Tract 4050
         1  Census Tract 4267
         1  Census Tract 1308
         1  Census Tract 2620
         1  Census Tract 4012
         1  Census Tract 4751.01
         1  Census Tract 4610
         1  Census Tract 4705.02
         1  Census Tract 4282
         1  Census Tract 9811
         1  Census Tract 4724
         1  Census Tract 5080
         1  Census Tract 103.02
         1  Census Tract 5653
         1  Census Tract 4550
         1  Census Tract 5632.02
         1  Census Tract 5130
         1  Census Tract 5647

NAMELSAD by dollars
        9.8K        1 rows  Census Tract 9822
        9.8K        1 rows  Census Tract 9818
        9.8K        1 rows  Census Tract 9812
        9.8K        1 rows  Census Tract 9811
        9.8K        1 rows  Census Tract 9810
        9.8K        1 rows  Census Tract 9809
        9.8K        1 rows  Census Tract 9808
        9.8K        1 rows  Census Tract 9807
        9.8K        1 rows  Census Tract 9806
        9.8K        1 rows  Census Tract 9805
        9.8K        1 rows  Census Tract 9804
        9.8K        1 rows  Census Tract 9803
        9.8K        1 rows  Census Tract 9801
        9.8K        1 rows  Census Tract 9800
        5.7K        1 rows  Census Tract 5653
        5.7K        1 rows  Census Tract 5652
        5.7K        1 rows  Census Tract 5651
        5.6K        1 rows  Census Tract 5648
        5.6K        1 rows  Census Tract 5647
        5.6K        1 rows  Census Tract 5645

SRC_SHA256 by rows
       394  cfd85f233d18ef968c2181d3df270cb051c2a5f5f6c003f4239d21acf145c6cd

SRC_SHA256 by dollars
       1.64M      394 rows  cfd85f233d18ef968c2181d3df270cb051c2a5f5f6c003f4239d21acf145

## who x when

NAMELSAD by INGESTED_AT  LOAD STAMP, not an event date, dollars = NAME
  Census Tract 103.02                       2026:103.02
  Census Tract 1308                         2026:1.3K
  Census Tract 2620                         2026:2.6K
  Census Tract 4012                         2026:4.0K
  Census Tract 4050                         2026:4.0K
  Census Tract 4267                         2026:4.3K
  Census Tract 4282                         2026:4.3K
  Census Tract 4550                         2026:4.5K
  Census Tract 4610                         2026:4.6K
  Census Tract 4705.02                      2026:4.7K
  Census Tract 4724                         2026:4.7K
  Census Tract 4751.01                      2026:4.8K
  Census Tract 4850                         2026:4.8K
  Census Tract 5080                         2026:5.1K
  Census Tract 5130                         2026:5.1K
  Census Tract 5632.02                      2026:5.6K
  Census Tract 5647                         2026:5.6K
  Census Tract 5648                         2026:5.6K
  Census Tract 5653                         2026:5.7K
  Census Tract 9804                         2026:9.8K
  Census Tract 9805                         2026:9.8K
  Census Tract 9806                         2026:9.8K
  Census Tract 9807                         2026:9.8K
  Census Tract 9808                         2026:9.8K
  Census Tract 9809                         2026:9.8K
  Census Tract 9810                         2026:9.8K
  Census Tract 9811                         2026:9.8K
  Census Tract 9812                         2026:9.8K
  Census Tract 9818                         2026:9.8K
  Census Tract 9822                         2026:9.8K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = NAME
  cfd85f233d18ef968c2181d3df270cb051c2a5f5  2026:1.64M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ALAND | other | 395 | 0 | 1121761 2; 6548443 2; 7972525 2; 49019304 2 |
| AWATER | other | 120 | 0 | 0 275; 296443 1; 15818 1; 2462216 1 |
| COUNTYFP | other | 1 | 0 | 003 394 |
| FID | other | 392 | 0 | 394 2; 393 2; 392 2; 391 2 |
| FUNCSTAT | other | 1 | 0 | S 394 |
| GEOID | other | 393 | 0 | 42003525200 2; 42003523701 2; 42003521302 2; 42003495000 2 |
| GEOIDFQ | other | 399 | 0 | 1400000US42003525200 2; 1400000US42003523701 2; 1400000US42003521302 2; 1400000US42003495000 2 |
| INTPTLAT | other | 376 | 0 | 40.5158744 2; 40.5041079 2; 40.4156159 2; 40.2320479 2 |
| INTPTLON | other | 397 | 0 | -79.8451025 2; -79.8181437 2; -79.787208 2; -79.9068 2 |
| MTFCC | other | 1 | 0 | G5020 394 |
| NAME | amount | 392 | 0 | 5252.0 2; 5237.01 2; 5213.02 2; 4950.0 2 |
| NAMELSAD | who | 387 | 0 | Census Tract 5252 2; Census Tract 5237.01 2; Census Tract 5213.02 2; Census Tract 4950 2 |
| STATEFP | other | 1 | 0 | 42 394 |
| TRACTCE | other | 398 | 0 | 525200 2; 523701 2; 521302 2; 495000 2 |
| GEOMETRY | other | 394 | 0 | POLYGON ((597338.14192641 2; POLYGON ((598472.74557347 2; POLYGON ((601431.02038118 2; POLYGON ((587515.54534002 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:40:58.37481 394 |
| SOURCE_RUN_ID | audit | 1 | 0 | f801ebd0-4fe5-4816-9147-f 394 |
| SRC_SHA256 | who | 1 | 0 | cfd85f233d18ef968c2181d3d 394 |
