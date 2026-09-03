# PORTAL_CKA_WPRDC_ALLEGHENY_9BB7597D03

rows 2.1K  columns 8  scan 2.9s

roles: amount 3, audit 2, category 1, date 1, id 1, who 1

## when

INGESTED_AT
  2026      2.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SIDEWALKSTEPLFT | 1.1K | 6.27 | 15.8K | 75.9K | 226.0K | 19.56M |
| STREETLFT | 1.1K | 247.17 | 22.6K | 167.9K | 293.4K | 36.03M |
| RATIO | 1.1K | 0 | 0.79 | 2.99 | 9.87 | 980.11 |

## who

SRC_SHA256 by rows
      2.1K  6764e6b7d1a8d2eaae39b731e1770fcd8f1ebe5bf6d162147d778f17a55d51fa

SRC_SHA256 by dollars
      36.03M     2.1K rows  6764e6b7d1a8d2eaae39b731e1770fcd8f1ebe5bf6d162147d778f17a55d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = STREETLFT
  6764e6b7d1a8d2eaae39b731e1770fcd8f1ebe5b  2026:36.03M

## what

NAMELSAD: Block Group 1 37%, Block Group 2 32%, Block Group 3 20%, Block Group 4 9%, Block Group 5 2%, Block Group 6 1%, Block Group 7 0%, Block Group 8 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEOID | id | 2.1K | 0 | 421298086003 11; 421298086002 11; 421298086001 11; 421298085001 11 |
| NAMELSAD | category | 8 | 0 | Block Group 1 771; Block Group 2 678; Block Group 3 415; Block Group 4 180 |
| SIDEWALKSTEPLFT | amount | 1.1K | 1.0K | 51352.28584 6; 14588.90832 6; 31844.77914 6; 7645.350565 6 |
| STREETLFT | amount | 1.1K | 1.0K | 12695.0221 6; 9012.302205 6; 10014.3523 6; 4327.467375 6 |
| RATIO | amount | 1.1K | 1.0K | 0 21; 4.045072582 6; 1.618777088 6; 3.179914008 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:03:09.36978 2.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | f5887a93-8d3c-4ab2-8433-5 2.1K |
| SRC_SHA256 | who | 1 | 0 | 6764e6b7d1a8d2eaae39b731e 2.1K |
