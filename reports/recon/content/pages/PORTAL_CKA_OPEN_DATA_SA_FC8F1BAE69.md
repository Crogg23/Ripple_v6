# PORTAL_CKA_OPEN_DATA_SA_FC8F1BAE69

rows 11  columns 7  scan 2.6s

roles: amount 2, audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026        11  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 11 | 79.4K | 740.20M | 1.66B | 1.68B | 8.21B |
| SHAPE__LENGTH | 11 | 1.3K | 191.6K | 371.4K | 377.5K | 2.25M |

## who

SRC_SHA256 by rows
        11  1ca76a6f31e53a9b41b41e23308c2be6dbf5b03ec28775b88c7ec1279ae3116e

SRC_SHA256 by dollars
       8.21B       11 rows  1ca76a6f31e53a9b41b41e23308c2be6dbf5b03ec28775b88c7ec1279ae3

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  1ca76a6f31e53a9b41b41e23308c2be6dbf5b03e  2026:8.21B

## what

OBJECTID: 11 9%, 10 9%, 9 9%, 8 9%, 7 9%, 6 9%, 5 9%, 4 9%, 3 9%, 2 9%, 1 9%

NAME: MLOD-1 - Camp Bullis 45%, MLOD-2 - Lackland AFB Annex 36%, MLOD-3 - Martindale Army Air F 18%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 11 | 0 | 11 1; 10 1; 9 1; 8 1 |
| NAME | category | 3 | 0 | MLOD-1 - Camp Bullis 5; MLOD-2 - Lackland AFB Ann 4; MLOD-3 - Martindale Army  2 |
| SHAPE__AREA | amount | 11 | 0 | 406546106.248047 1; 260044436.121094 1; 79162002.4863281 1; 546099594.341797 1 |
| SHAPE__LENGTH | amount | 11 | 0 | 121509.337049075 1; 127718.468067915 1; 47984.0833851289 1; 158081.265377423 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:13:08.87818 11 |
| SOURCE_RUN_ID | audit | 1 | 0 | cc44f613-5e68-470a-bf86-8 11 |
| SRC_SHA256 | who | 1 | 0 | 1ca76a6f31e53a9b41b41e233 11 |
