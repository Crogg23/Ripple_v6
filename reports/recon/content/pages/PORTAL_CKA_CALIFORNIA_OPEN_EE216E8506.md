# PORTAL_CKA_CALIFORNIA_OPEN_EE216E8506

rows 4  columns 15  scan 4.4s

roles: amount 3, audit 2, category 4, date 1, empty 1, other 1, who 4

## when

INGESTED_AT
  2026         4  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENG | 4 | 970.2K | 2.01M | 2.83M | 2.85M | 7.85M |
| SHAPE__AREA | 4 | 4.17B | 9.19B | 33.69B | 34.39B | 56.94B |
| SHAPE__LENGTH | 4 | 1.22M | 2.52M | 3.41M | 3.43M | 9.69M |

## who

CNAME by rows
         4  MARBLED MURRELLET

CNAME by dollars
       7.85M        4 rows  MARBLED MURRELLET

SNAME by rows
         4  Brachyramphus marmoratus

SNAME by dollars
       7.85M        4 rows  Brachyramphus marmoratus

OCC_YEARS by rows
         4  1892-2024

OCC_YEARS by dollars
       7.85M        4 rows  1892-2024

SRC_SHA256 by rows
         4  715a5612d2baf9b938d419f611b960c5939e567494d6f89646f3135787d40f3a

SRC_SHA256 by dollars
       7.85M        4 rows  715a5612d2baf9b938d419f611b960c5939e567494d6f89646f3135787d4

## who x when

CNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENG
  MARBLED MURRELLET                         2026:7.85M

SNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENG
  Brachyramphus marmoratus                  2026:7.85M

## what

OBJECTID: 4 25%, 3 25%, 2 25%, 1 25%

RANGESTART: November 50%, March 50%

RANGEEND: February 50%, October 50%

SEASON: Y 25%, N 25%, B 25%, P 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 4 | 0 | 4 1; 3 1; 2 1; 1 1 |
| SHAPE_LENG | amount | 3 | 0 | 2854452.93945 1; 2173160.41947 1; 1853625.67252 1; 970244.52399 1 |
| OCC_YEARS | who | 1 | 0 | 1892-2024 4 |
| RANGESTART | category | 3 | 2 | November 1; March 1 |
| RANGEEND | category | 3 | 2 | February 1; October 1 |
| SHAPE_NAME | other | 1 | 0 | B240 4 |
| CNAME | who | 1 | 0 | MARBLED MURRELLET 4 |
| SNAME | who | 1 | 0 | Brachyramphus marmoratus 4 |
| UNCERTAIN | empty | 1 | 4 |  |
| SEASON | category | 4 | 0 | Y 1; N 1; B 1; P 1 |
| SHAPE__AREA | amount | 4 | 0 | 10848199258.875 1; 7527662354.83984 1; 34394408572.668 1; 4167765250.85938 1 |
| SHAPE__LENGTH | amount | 4 | 0 | 3430678.52270622 1; 2624417.12959092 1; 2410452.30488848 1; 1220293.52084264 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:09:32.54018 4 |
| SOURCE_RUN_ID | audit | 1 | 0 | e45f4432-28c9-431d-b555-a 4 |
| SRC_SHA256 | who | 1 | 0 | 715a5612d2baf9b938d419f61 4 |
