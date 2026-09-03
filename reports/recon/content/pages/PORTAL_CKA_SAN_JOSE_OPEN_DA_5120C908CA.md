# PORTAL_CKA_SAN_JOSE_OPEN_DA_5120C908CA

rows 3  columns 13  scan 2.6s

roles: amount 2, audit 2, category 4, date 1, empty 4, who 1

## when

INGESTED_AT
  2026         3  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 3 | 4.2K | 4.7K | 12.0K | 12.2K | 21.0K |
| SHAPE_AREA | 3 | 851.9K | 1.25M | 7.31M | 7.43M | 9.54M |

## who

SRC_SHA256 by rows
         3  258ef370e9e30ab415ee40cca638e0d5159824d1c849cfb72701a80de3fee217

SRC_SHA256 by dollars
       21.0K        3 rows  258ef370e9e30ab415ee40cca638e0d5159824d1c849cfb72701a80de3fe

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  258ef370e9e30ab415ee40cca638e0d5159824d1  2026:21.0K

## what

OBJECTID: 3 33%, 2 33%, 1 33%

FACILITYID: 3 33%, 2 33%, 1 33%

INTID: 3 33%, 2 33%, 1 33%

NAME: Oak Hill Cemetery 33%, Los Gatos Cemetery 33%, Calvary Catholic Cemetery 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 3 | 0 | 3 1; 2 1; 1 1 |
| FACILITYID | category | 3 | 0 | 3 1; 2 1; 1 1 |
| INTID | category | 3 | 0 | 3 1; 2 1; 1 1 |
| NAME | category | 3 | 0 | Oak Hill Cemetery 1; Los Gatos Cemetery 1; Calvary Catholic Cemetery 1 |
| FULLADDR | empty | 1 | 3 |  |
| ZIPCODE | empty | 1 | 3 |  |
| LASTUPDATE | empty | 1 | 3 |  |
| NOTES | empty | 1 | 3 |  |
| SHAPE_LENGTH | amount | 3 | 0 | 12180.5273911309 1; 4668.53935185314 1; 4160.27304330836 1 |
| SHAPE_AREA | amount | 3 | 0 | 7433060.99476405 1; 1250584.69563188 1; 851900.069689152 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:08:55.05886 3 |
| SOURCE_RUN_ID | audit | 1 | 0 | 73181141-7079-4013-941e-b 3 |
| SRC_SHA256 | who | 1 | 0 | 258ef370e9e30ab415ee40cca 3 |
