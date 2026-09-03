# PORTAL_CKA_CALIFORNIA_OPEN_0BC18BBA68

rows 2  columns 14  scan 3.7s

roles: amount 2, audit 2, category 2, date 1, empty 4, other 1, who 3

## when

INGESTED_AT
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 2 | 8.30B | 13.26B | 18.11B | 18.21B | 26.51B |
| SHAPE__LENGTH | 2 | 420.3K | 676.6K | 927.8K | 932.9K | 1.35M |

## who

SNAME by rows
         2  Vulpes vulpes necator pop. 1

SNAME by dollars
      26.51B        2 rows  Vulpes vulpes necator pop. 1

CNAME by rows
         2  Sierra Nevada red fox - Southern Cascades DPS

CNAME by dollars
      26.51B        2 rows  Sierra Nevada red fox - Southern Cascades DPS

SRC_SHA256 by rows
         2  025e1100ddb723c9f528fa955828501726226bfadd04cfea545c29a741dd9d00

SRC_SHA256 by dollars
      26.51B        2 rows  025e1100ddb723c9f528fa955828501726226bfadd04cfea545c29a741dd

## who x when

SNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Vulpes vulpes necator pop. 1              2026:26.51B

CNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Sierra Nevada red fox - Southern Cascade  2026:26.51B

## what

OBJECTID: 2 50%, 1 50%

SEASON: Y 50%, H 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 2 1; 1 1 |
| SNAME | who | 1 | 0 | Vulpes vulpes necator pop 2 |
| CNAME | who | 1 | 0 | Sierra Nevada red fox - S 2 |
| SHAPE_NAME | other | 1 | 0 | M147d 2 |
| SEASON | category | 2 | 0 | Y 1; H 1 |
| UNCERTAIN | empty | 1 | 2 |  |
| OCC_YEARS | empty | 1 | 2 |  |
| RANGESTART | empty | 1 | 2 |  |
| RANGEEND | empty | 1 | 2 |  |
| SHAPE__AREA | amount | 2 | 0 | 8297641713.10156 1; 18212890411.7695 1 |
| SHAPE__LENGTH | amount | 2 | 0 | 420262.055185799 1; 932881.859492896 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:08:44.06160 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | d05eb4dd-b3d4-4a0b-8fed-6 2 |
| SRC_SHA256 | who | 1 | 0 | 025e1100ddb723c9f528fa955 2 |
