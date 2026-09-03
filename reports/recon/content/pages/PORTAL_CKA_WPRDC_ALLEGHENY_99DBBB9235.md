# PORTAL_CKA_WPRDC_ALLEGHENY_99DBBB9235

rows 10.0K  columns 12  scan 3.8s

roles: amount 2, audit 2, category 2, date 1, id 3, other 2, who 1

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LEN | 10.0K | 5.50 | 1.6K | 35.6K | 147.9K | 36.66M |
| SHAPE_AREA | 10.0K | 0.82 | 60.6K | 7.73M | 45.58M | 4.45B |

## who

SRC_SHA256 by rows
     10.0K  4e8a025c7af298c8310bf9cb47eb0d209b7e2c6db5e10910693f010c60ad3716

SRC_SHA256 by dollars
      36.66M    10.0K rows  4e8a025c7af298c8310bf9cb47eb0d209b7e2c6db5e10910693f010c60ad

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LEN
  4e8a025c7af298c8310bf9cb47eb0d209b7e2c6d  2026:36.66M

## what

FEATURECOD: 310 90%, 350 6%, 620 4%, 340 1%, 300 0%

UPDATE_YEA: 2004 73%, 1994 24%, 1993 3%, 2001 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SHAPE_LEN | amount | 10.1K | 0 | 3263.97816363 21; 1833.86003358 21; 1680.72586589 21; 5884.31086648 21 |
| FEATURECOD | category | 5 | 0 | 310 9.0K; 350 551; 620 404; 340 62 |
| FID | id | 10.0K | 0 | 4096 21; 4095 21; 4094 21; 4093 21 |
| SYSTEMID | other | 2.5K | 0 | 0 7.3K; 7934 44; 9685 15; 10364 13 |
| UPDATE_YEA | category | 4 | 0 | 2004 7.3K; 1994 2.4K; 1993 328; 2001 1 |
| SHAPE_AREA | amount | 10.0K | 0 | 176280.225666 21; 62199.2168774 21; 134987.719018 21; 494662.432177 21 |
| OBJECTID | id | 10.0K | 0 | 10176 21; 10175 21; 10174 21; 10173 21 |
| USERID | other | 2.5K | 0 | 0 7.3K; 7934 44; 9685 15; 10364 13 |
| DATASPATIAL_WKB | id | 10.0K | 0 | \x00000000030000000100000 21; \x00000000030000000100000 21; \x00000000030000000100000 21; \x00000000030000000100000 21 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:40:35.03266 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | a5fff122-8ce9-451a-8aeb-f 10.0K |
| SRC_SHA256 | who | 1 | 0 | 4e8a025c7af298c8310bf9cb4 10.0K |
