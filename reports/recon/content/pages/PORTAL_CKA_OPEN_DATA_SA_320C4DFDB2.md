# PORTAL_CKA_OPEN_DATA_SA_320C4DFDB2

rows 6  columns 7  scan 3.4s

roles: amount 2, audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026         6  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 6 | 9.00M | 15.00M | 21.18M | 21.19M | 90.18M |
| SHAPE__LENGTH | 6 | 12.0K | 16.0K | 20.1K | 20.1K | 96.1K |

## who

SRC_SHA256 by rows
         6  26315063814d39605d8239e0e977d9c218f5155d9016f332ffe14e36941e7733

SRC_SHA256 by dollars
      90.18M        6 rows  26315063814d39605d8239e0e977d9c218f5155d9016f332ffe14e36941e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  26315063814d39605d8239e0e977d9c218f5155d  2026:90.18M

## what

OBJECTID: 6 17%, 5 17%, 4 17%, 3 17%, 2 17%, 1 17%

UDCOVERLAY: MAOZ-1 33%, MAOZ-0 33%, MAOZ-2 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 6 | 0 | 6 1; 5 1; 4 1; 3 1 |
| UDCOVERLAY | category | 3 | 0 | MAOZ-1 2; MAOZ-0 2; MAOZ-2 2 |
| SHAPE__AREA | amount | 6 | 0 | 15000496.1074219 1; 9000248.88476563 1; 21185641.0996094 1; 21000002.9160156 1 |
| SHAPE__LENGTH | amount | 6 | 0 | 16000.3313130586 1; 12000.1659285785 1; 20082.0292883652 1; 20000.0008945745 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:10:53.90098 6 |
| SOURCE_RUN_ID | audit | 1 | 0 | c28d910f-565b-4517-8813-4 6 |
| SRC_SHA256 | who | 1 | 0 | 26315063814d39605d8239e0e 6 |
