# PORTAL_CKA_WESTERN_PENNSYLV_7880B791DF

rows 10.0K  columns 24  scan 5.9s

roles: amount 4, audit 2, category 2, date 1, id 4, other 9, who 3

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| INTPTLAT20 | 10.0K | 40.20 | 40.44 | 40.65 | 40.67 | 404.4K |
| INTPTLON20 | 10.0K | -80.36 | -79.96 | -79.72 | -79.70 | -799.5K |
| SHAPE__AREA | 10.0K | 2.0K | 138.3K | 15.36M | 71.50M | 8.87B |
| SHAPE__LENGTH | 10.0K | 333.08 | 1.8K | 23.3K | 59.0K | 34.34M |

## who

NAME20 by rows
       181  Block1006
       169  Block1003
       163  Block1007
       162  Block1001
       158  Block1000
       158  Block1005
       157  Block1010
       154  Block1002
       149  Block1009
       146  Block2005
       143  Block1004
       142  Block1011
       141  Block2003
       138  Block2002
       138  Block2000
       136  Block1012
       136  Block2004
       136  Block1008
       131  Block2001
       130  Block1013

NAME20 by dollars
        7.3K      181 rows  Block1006
        6.8K      169 rows  Block1003
        6.6K      163 rows  Block1007
        6.6K      162 rows  Block1001
        6.4K      158 rows  Block1000
        6.4K      158 rows  Block1005
        6.4K      157 rows  Block1010
        6.2K      154 rows  Block1002
        6.0K      149 rows  Block1009
        5.9K      146 rows  Block2005
        5.8K      143 rows  Block1004
        5.7K      142 rows  Block1011
        5.7K      141 rows  Block2003
        5.6K      138 rows  Block2000
        5.6K      138 rows  Block2002
        5.5K      136 rows  Block1012
        5.5K      136 rows  Block1008
        5.5K      136 rows  Block2004
        5.3K      131 rows  Block2001
        5.3K      130 rows  Block1013

TRACTCE20 by rows
        98  403500
        93  562600
        82  310200
        79  500300
        76  130800
        72  020300
        70  271600
        68  552300
        68  504100
        68  020100
        66  452000
        66  513800
        65  496102
        64  564400
        61  503002
        60  424000
        58  507000
        57  488200
        56  565200
        56  401200

TRACTCE20 by dollars
        4.0K       98 rows  403500
        3.8K       93 rows  562600
        3.3K       82 rows  310200
        3.2K       79 rows  500300
        3.1K       76 rows  130800
        2.9K       72 rows  020300
        2.8K       70 rows  271600
        2.7K       68 rows  020100
        2.7K       68 rows  504100
        2.7K       68 rows  552300
        2.7K       66 rows  452000
        2.7K       66 rows  513800
        2.6K       65 rows  496102
        2.6K       64 rows  564400
        2.5K       61 rows  503002
        2.4K       60 rows  424000
        2.3K       58 rows  507000
        2.3K       57 rows  488200
        2.3K       56 rows  401200
        2.3K       56 rows  565200

SRC_SHA256 by rows
     10.0K  22b0d639cb91bad66cca1ef26668b9d3e540a2a5cbed13615aa08e7e930d3853

SRC_SHA256 by dollars
      404.4K    10.0K rows  22b0d639cb91bad66cca1ef26668b9d3e540a2a5cbed13615aa08e7e930d

## who x when

NAME20 by INGESTED_AT  LOAD STAMP, not an event date, dollars = INTPTLAT20
  Block1000                                 2026:6.4K
  Block1001                                 2026:6.6K
  Block1002                                 2026:6.2K
  Block1003                                 2026:6.8K
  Block1004                                 2026:5.8K
  Block1005                                 2026:6.4K
  Block1006                                 2026:7.3K
  Block1007                                 2026:6.6K
  Block1008                                 2026:5.5K
  Block1009                                 2026:6.0K
  Block1010                                 2026:6.4K
  Block1011                                 2026:5.7K
  Block1012                                 2026:5.5K
  Block1013                                 2026:5.3K
  Block2000                                 2026:5.6K
  Block2001                                 2026:5.3K
  Block2002                                 2026:5.6K
  Block2003                                 2026:5.7K
  Block2004                                 2026:5.5K
  Block2005                                 2026:5.9K

TRACTCE20 by INGESTED_AT  LOAD STAMP, not an event date, dollars = INTPTLAT20
  020100                                    2026:2.7K
  020300                                    2026:2.9K
  130800                                    2026:3.1K
  271600                                    2026:2.8K
  310200                                    2026:3.3K
  401200                                    2026:2.3K
  403500                                    2026:4.0K
  424000                                    2026:2.4K
  452000                                    2026:2.7K
  488200                                    2026:2.3K
  496102                                    2026:2.6K
  500300                                    2026:3.2K
  503002                                    2026:2.5K
  504100                                    2026:2.7K
  507000                                    2026:2.3K
  513800                                    2026:2.7K
  552300                                    2026:2.7K
  562600                                    2026:3.8K
  564400                                    2026:2.6K
  565200                                    2026:2.3K

## what

UACE20: 69697 100%, 58162 0%

UR20: U 96%, R 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ALAND20 | other | 8.9K | 0 | 0 110; 37803 50; 30742 50; 2510 50 |
| AWATER20 | other | 129 | 0 | 0 9.9K; 3562 1; 1126977 1; 8794 1 |
| BLOCKCE20 | other | 377 | 0 | 1006 181; 1003 169; 1007 163; 1001 162 |
| COUNTYFP20 | other | 1 | 0 | 003 10.0K |
| FID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| FUNCSTAT20 | other | 1 | 0 | S 10.0K |
| GEOID20 | id | 9.9K | 0 | 420034264004014 50; 420039806001031 50; 420035652002004 50; 420032716002025 50 |
| GEOIDFQ20 | id | 10.1K | 0 | 1010000US420034264004014 50; 1010000US420039806001031 50; 1010000US420035652002004 50; 1010000US420032716002025 50 |
| HOUSING20 | other | 284 | 0 | 0 1.6K; 8 310; 6 301; 9 300 |
| INTPTLAT20 | amount | 9.8K | 0 | 40.5261262 50; 40.4581031 50; 40.4594314 50; 40.4702831 50 |
| INTPTLON20 | amount | 10.2K | 0 | -79.9688094 50; -80.0313711 50; -80.0297711 50; -80.0259593 50 |
| MTFCC20 | other | 1 | 0 | G5040 10.0K |
| NAME20 | who | 381 | 0 | Block1006 181; Block1003 169; Block1007 163; Block1001 162 |
| POP20 | other | 450 | 0 | 0 1.6K; 15 163; 10 156; 19 156 |
| STATEFP20 | other | 1 | 0 | 42 10.0K |
| SHAPE__AREA | amount | 9.9K | 0 | 406866.50970458984 50; 330877.6072998047 50; 27014.556762695312 50; 37025.674377441406 50 |
| SHAPE__LENGTH | amount | 9.9K | 0 | 3324.7614004891657 50; 2408.885260452101 50; 659.4501484125235 50; 833.2981141087259 50 |
| TRACTCE20 | who | 395 | 0 | 403500 98; 562600 94; 020100 90; 310200 83 |
| UACE20 | category | 3 | 353 | 69697 9.6K; 58162 13 |
| UR20 | category | 2 | 0 | U 9.6K; R 353 |
| GEOMETRY | id | 10.1K | 0 | POLYGON ((587283.11581859 50; POLYGON ((582034.36839057 50; POLYGON ((582228.94352809 50; POLYGON ((582541.33065626 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:45:15.71005 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5e4c83f1-cb67-4f6d-8d07-d 10.0K |
| SRC_SHA256 | who | 1 | 0 | 22b0d639cb91bad66cca1ef26 10.0K |
