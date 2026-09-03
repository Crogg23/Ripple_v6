# PORTAL_CKA_ANALYZE_BOSTON_BD5A2F9374

rows 1.5K  columns 7  scan 2.6s

roles: amount 1, audit 2, category 1, date 1, empty 1, id 1, who 1

## when

INGESTED_AT
  2026      1.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 1.5K | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
      1.5K  494535f0f1fd436569a021d98ad75c3b21e644f3d8eb80f8264752a2000c1b0c

SRC_SHA256 by dollars
           0     1.5K rows  494535f0f1fd436569a021d98ad75c3b21e644f3d8eb80f8264752a2000c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  494535f0f1fd436569a021d98ad75c3b21e644f3  2026:0

## what

TYPE: STREAM 63%, OPEN-CULVERT 29%, COVERED-CULVERT 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TYPE | category | 3 | 0 | STREAM 928; OPEN-CULVERT 422; COVERED-CULVERT 119 |
| NAME | empty | 1 | 1.5K |  |
| SHAPE_LENGTH | amount | 1.5K | 0 | 0.000093453193288 8; 0.000189813061735 8; 0.000142612009846 8; 0.000080936352018 8 |
| SHAPE_WKT | id | 1.2K | 300 | MULTILINESTRING ((-71.041 6; MULTILINESTRING ((-71.046 6; MULTILINESTRING ((-71.046 6; MULTILINESTRING ((-71.105 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:54:56.81627 1.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 17df55a2-9bd1-4979-a1b2-7 1.5K |
| SRC_SHA256 | who | 1 | 0 | 494535f0f1fd436569a021d98 1.5K |
