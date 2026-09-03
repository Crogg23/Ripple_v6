# PORTAL_CKA_WESTERN_PENNSYLV_BCBE92C64C

rows 12  columns 9  scan 2.6s

roles: amount 3, audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026        12  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREA_SQ_MI | 12 | 0.09 | 2.55 | 17.04 | 17.61 | 58.59 |
| SHAPE__AREA | 12 | 2.61M | 71.14M | 475.01M | 491.00M | 1.63B |
| SHAPE__LENGTH | 12 | 11.5K | 65.4K | 161.9K | 162.7K | 854.3K |

## who

SRC_SHA256 by rows
        12  0ecd4109396ea09c9ba597960b4751d4f48e63b403fdfd154b970b950d0a148a

SRC_SHA256 by dollars
       58.59       12 rows  0ecd4109396ea09c9ba597960b4751d4f48e63b403fdfd154b970b950d0a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREA_SQ_MI
  0ecd4109396ea09c9ba597960b4751d4f48e63b4  2026:58.59

## what

NAME: Monongahela River Basin 8%, Ohio River Basin 8%, Allegheny River Basin 8%, Chartiers Creek Basin 8%, Jacks Run Basin 8%, Nelson Run Basin 8%, Nine Mile Run Basin 8%, Saw Mill Run Basin 8%, Shades Run Basin 8%, Streets Run Basin 8%, Thompson Run Basin 8%, Becks Run Basin 8%

OBJECTID: 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%, 1 8%

GEOMETRY: MULTIPOLYGON (((591806.9889421 8%, POLYGON ((582574.4530348059488 8%, POLYGON ((584395.0867670023581 8%, MULTIPOLYGON (((580914.5645700 8%, MULTIPOLYGON (((581289.7044846 8%, POLYGON ((584395.0867670023581 8%, MULTIPOLYGON (((594907.4736798 8%, POLYGON ((582485.6674645239254 8%, POLYGON ((594267.6539268343476 8%, MULTIPOLYGON (((587102.2040252 8%, MULTIPOLYGON (((593101.4217593 8%, MULTIPOLYGON (((588577.1173527 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA_SQ_MI | amount | 12 | 0 | 12.3982183785 1; 6.6416866969 1; 17.6121440974 1; 3.20403581629 1 |
| NAME | category | 12 | 0 | Monongahela River Basin 1; Ohio River Basin 1; Allegheny River Basin 1; Chartiers Creek Basin 1 |
| OBJECTID | category | 12 | 0 | 12 1; 11 1; 10 1; 9 1 |
| SHAPE__AREA | amount | 12 | 0 | 345640977.015503 1; 185158787.277435 1; 490996247.075195 1; 89322999.9967041 1 |
| SHAPE__LENGTH | amount | 12 | 0 | 155887.396046788 1; 78724.035024529 1; 162697.790784449 1; 90978.4308006516 1 |
| GEOMETRY | category | 12 | 0 | MULTIPOLYGON (((591806.98 1; POLYGON ((582574.45303480 1; POLYGON ((584395.08676700 1; MULTIPOLYGON (((580914.56 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:13:36.21939 12 |
| SOURCE_RUN_ID | audit | 1 | 0 | d4386dbe-4c6e-4073-ace4-3 12 |
| SRC_SHA256 | who | 1 | 0 | 0ecd4109396ea09c9ba597960 12 |
