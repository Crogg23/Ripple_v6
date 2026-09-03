# PORTAL_CKA_HOUSTON_OPEN_DAT_19CBD263CC

rows 15  columns 9  scan 2.9s

roles: amount 3, audit 2, category 1, date 1, other 1, who 2

## when

INGESTED_AT
  2026        15  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| B25010_001E | 15 | 2.46 | 2.66 | 2.69 | 2.69 | 39.36 |
| B25010_002E | 15 | 2.70 | 2.84 | 2.87 | 2.87 | 42.30 |
| B25010_003E | 15 | 2.29 | 2.52 | 2.56 | 2.56 | 37.09 |

## who

NAME by rows
        15  Houston city, Texas

NAME by dollars
       39.36       15 rows  Houston city, Texas

SRC_SHA256 by rows
        15  b399285ce28b15a938cf1c5a9c8795d381afc1cef054e34b09494e4df5a922cd

SRC_SHA256 by dollars
       39.36       15 rows  b399285ce28b15a938cf1c5a9c8795d381afc1cef054e34b09494e4df5a9

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = B25010_001E
  Houston city, Texas                       2026:39.36

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = B25010_001E
  b399285ce28b15a938cf1c5a9c8795d381afc1ce  2026:39.36

## what

YEAR: 2010 8%, 2011 8%, 2012 8%, 2013 8%, 2014 8%, 2015 8%, 2016 8%, 2017 8%, 2018 8%, 2019 8%, 2020 8%, 2021 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 15 | 0 | 2010 1; 2011 1; 2012 1; 2013 1 |
| GEO_ID | other | 1 | 0 | 4835000 15 |
| NAME | who | 1 | 0 | Houston city, Texas 15 |
| B25010_001E | amount | 10 | 0 | 2.67 3; 2.69 3; 2.66 2; 2.68 1 |
| B25010_002E | amount | 8 | 0 | 2.87 3; 2.83 2; 2.84 2; 2.85 2 |
| B25010_003E | amount | 11 | 0 | 2.52 3; 2.53 2; 2.56 2; 2.55 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:08:03.32380 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | 32c8f7dc-5ed0-48d8-b9bf-e 15 |
| SRC_SHA256 | who | 1 | 0 | b399285ce28b15a938cf1c5a9 15 |
