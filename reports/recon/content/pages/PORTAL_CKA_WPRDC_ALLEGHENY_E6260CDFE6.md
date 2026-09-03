# PORTAL_CKA_WPRDC_ALLEGHENY_E6260CDFE6

rows 51  columns 14  scan 2.8s

roles: amount 2, audit 2, category 4, date 2, empty 2, other 2, who 1

## when

LAST_EDITED_DATE
  2018         7  ##############################
  2019         3  #############
  2021         1  ####

INGESTED_AT
  2026        51  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 51 | 25.9K | 681.4K | 15.96M | 21.45M | 98.30M |
| SHAPE__LENGTH | 51 | 1.3K | 4.8K | 36.5K | 49.7K | 394.9K |

## who

SRC_SHA256 by rows
        51  1222f161421276e7c7007111b031034bf197f09dd1dbcf3e53fb4e56b07e444c

SRC_SHA256 by dollars
      98.30M       51 rows  1222f161421276e7c7007111b031034bf197f09dd1dbcf3e53fb4e56b07e

## who x when

SRC_SHA256 by LAST_EDITED_DATE, dollars = SHAPE__AREA
  1222f161421276e7c7007111b031034bf197f09d  2018:39.42M 2019:1.01M 2021:80.3K

## what

MIN_BASE_HEIGHT: 60 45%, 40 20%, 45 16%, 65 10%, 85 10%

HLIMIT: 90 26%, 45 16%, 150 12%, 85 10%, 95 10%, 120 8%, 65 6%, 185 4%, 210 4%, 140 2%, 250 2%

ID: 0 100%

LAST_EDITED_USER: SDE 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MIN_BASE_HEIGHT | category | 5 | 0 | 60 23; 40 10; 45 8; 65 5 |
| OBJECTID | other | 51 | 0 | 440 1; 438 1; 436 1; 434 1 |
| SHAPE__AREA | amount | 51 | 0 | 425091.5455932617 1; 905477.5272216797 1; 300931.9171142578 1; 207611.85961914062 1 |
| SHAPE__LENGTH | amount | 51 | 0 | 3077.514641834483 1; 4811.848043163761 1; 2624.010190416047 1; 1882.8582003878546 1 |
| CREATED_DATE | empty | 1 | 51 |  |
| CREATED_USER | empty | 1 | 51 |  |
| HLIMIT | category | 12 | 1 | 90 13; 45 8; 150 6; 85 5 |
| ID | category | 2 | 19 | 0 32 |
| LAST_EDITED_DATE | date | 10 | 40 | 2019-04-16T15:03:09 3; 2021-09-28T19:11:36 1; 2018-08-01T13:41:29 1; 2018-08-01T13:42:45 1 |
| LAST_EDITED_USER | category | 2 | 40 | SDE 11 |
| GEOMETRY | other | 51 | 0 | POLYGON ((588536.52590003 1; POLYGON ((588852.69186037 1; POLYGON ((588265.27600594 1; POLYGON ((587796.78321775 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:24:04.20098 51 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9b4e608a-1a72-41e7-8b83-c 51 |
| SRC_SHA256 | who | 1 | 0 | 1222f161421276e7c7007111b 51 |
