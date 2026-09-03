# PORTAL_CKA_OPEN_DATA_SA_87C271A71E

rows 10  columns 7  scan 2.6s

roles: amount 2, audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026        10  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 10 | 84.93M | 177.20M | 286.49M | 292.91M | 1.73B |
| SHAPE__LENGTH | 10 | 62.5K | 134.4K | 278.1K | 281.9K | 1.52M |

## who

SRC_SHA256 by rows
        10  f821e1c34301c94441deb65762ecb9360aca2d8183456294e2116c2e1c208493

SRC_SHA256 by dollars
       1.73B       10 rows  f821e1c34301c94441deb65762ecb9360aca2d8183456294e2116c2e1c20

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  f821e1c34301c94441deb65762ecb9360aca2d81  2026:1.73B

## what

OBJECTID: 10 10%, 9 10%, 8 10%, 7 10%, 6 10%, 5 10%, 4 10%, 3 10%, 2 10%, 1 10%

DISTRICT: 10 10%, 9 10%, 8 10%, 7 10%, 6 10%, 5 10%, 4 10%, 3 10%, 2 10%, 1 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 10 | 0 | 10 1; 9 1; 8 1; 7 1 |
| DISTRICT | category | 10 | 0 | 10 1; 9 1; 8 1; 7 1 |
| SHAPE__AREA | amount | 10 | 0 | 173241729.898438 1; 170733801.425781 1; 181162836.40625 1; 105682671.363281 1 |
| SHAPE__LENGTH | amount | 10 | 0 | 116850.777152178 1; 129650.987030356 1; 139193.677037404 1; 97574.0859020039 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:12:19.88120 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | 497bb5a3-49c3-4f04-9603-f 10 |
| SRC_SHA256 | who | 1 | 0 | f821e1c34301c94441deb6576 10 |
