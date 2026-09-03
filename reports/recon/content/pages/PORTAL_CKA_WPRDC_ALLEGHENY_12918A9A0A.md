# PORTAL_CKA_WPRDC_ALLEGHENY_12918A9A0A

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
         1  Census Tract 3206
         1  Census Tract 5632.01
         1  Census Tract 5652
         1  Census Tract 4734.02
         1  Census Tract 4751.02
         1  Census Tract 4869
         1  Census Tract 4511.01
         1  Census Tract 9800
         1  Census Tract 5215
         1  Census Tract 5638
         1  Census Tract 3204
         1  Census Tract 5232
         1  Census Tract 5138
         1  Census Tract 4230
         1  Census Tract 5651
         1  Census Tract 5647
         1  Census Tract 203
         1  Census Tract 4639
         1  Census Tract 4090.01
         1  Census Tract 4742.03

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
  Census Tract 203                          2026:203
  Census Tract 3204                         2026:3.2K
  Census Tract 3206                         2026:3.2K
  Census Tract 4090.01                      2026:4.1K
  Census Tract 4230                         2026:4.2K
  Census Tract 4511.01                      2026:4.5K
  Census Tract 4639                         2026:4.6K
  Census Tract 4734.02                      2026:4.7K
  Census Tract 4742.03                      2026:4.7K
  Census Tract 4751.02                      2026:4.8K
  Census Tract 4869                         2026:4.9K
  Census Tract 5138                         2026:5.1K
  Census Tract 5215                         2026:5.2K
  Census Tract 5232                         2026:5.2K
  Census Tract 5632.01                      2026:5.6K
  Census Tract 5638                         2026:5.6K
  Census Tract 5647                         2026:5.6K
  Census Tract 5651                         2026:5.7K
  Census Tract 5652                         2026:5.7K
  Census Tract 9800                         2026:9.8K
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
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:41:07.04541 394 |
| SOURCE_RUN_ID | audit | 1 | 0 | 08b0389f-ba79-429a-9ec5-0 394 |
| SRC_SHA256 | who | 1 | 0 | cfd85f233d18ef968c2181d3d 394 |
