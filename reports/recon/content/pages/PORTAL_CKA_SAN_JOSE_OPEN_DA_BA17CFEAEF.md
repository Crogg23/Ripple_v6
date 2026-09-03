# PORTAL_CKA_SAN_JOSE_OPEN_DA_BA17CFEAEF

rows 2  columns 10  scan 3.6s

roles: amount 2, audit 2, category 4, date 1, who 2

## when

INGESTED_AT
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 2 | 730.4K | 1.16M | 1.58M | 1.59M | 2.32M |
| SHAPE_AREA | 2 | 7.81B | 22.95B | 37.78B | 38.09B | 45.89B |

## who

LASTUPDATE by rows
         2  2022/07/28 18:46:52+00

LASTUPDATE by dollars
       2.32M        2 rows  2022/07/28 18:46:52+00

SRC_SHA256 by rows
         2  a6cc59a800cf81e4d849f868a48f184143ee5cf7489b86de20d98b301753862e

SRC_SHA256 by dollars
       2.32M        2 rows  a6cc59a800cf81e4d849f868a48f184143ee5cf7489b86de20d98b301753

## who x when

LASTUPDATE by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  2022/07/28 18:46:52+00                    2026:2.32M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  a6cc59a800cf81e4d849f868a48f184143ee5cf7  2026:2.32M

## what

OBJECTID: 2 50%, 1 50%

FACILITYID: 10 50%, 11 50%

INTID: 10 50%, 11 50%

NOTES: Inside 50%, Outside 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 2 1; 1 1 |
| FACILITYID | category | 2 | 0 | 10 1; 11 1 |
| INTID | category | 2 | 0 | 10 1; 11 1 |
| LASTUPDATE | who | 1 | 0 | 2022/07/28 18:46:52+00 2 |
| NOTES | category | 2 | 0 | Inside 1; Outside 1 |
| SHAPE_LENGTH | amount | 2 | 0 | 730389.920147196 1; 1587567.53387253 1 |
| SHAPE_AREA | amount | 2 | 0 | 7808543493.03889 1; 38085691285.9083 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:08:38.45127 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1aa1ad17-ab43-4f1e-82c9-6 2 |
| SRC_SHA256 | who | 1 | 0 | a6cc59a800cf81e4d849f868a 2 |
