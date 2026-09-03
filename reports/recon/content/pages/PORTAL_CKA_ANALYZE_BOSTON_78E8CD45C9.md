# PORTAL_CKA_ANALYZE_BOSTON_78E8CD45C9

rows 40  columns 13  scan 3.7s

roles: amount 2, audit 2, category 5, date 1, empty 1, who 3

## when

INGESTED_AT
  2026        40  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 40 | 0.01 | 0.06 | 0.39 | 0.40 | 4.50 |
| SHAPE_AREA | 40 | 0 | 0 | 0.01 | 0.01 | 0.01 |

## who

SHAPE_STAREA_1 by rows
        40  0.000000000000000

SHAPE_STAREA_1 by dollars
        4.50       40 rows  0.000000000000000

SHAPE_STLENGTH_1 by rows
        40  0.000000000000000

SHAPE_STLENGTH_1 by dollars
        4.50       40 rows  0.000000000000000

SRC_SHA256 by rows
        40  b457f9e34c2bc7b993d4c5a2cf33162cc59dace5918ad273c0c25c8b249dfe01

SRC_SHA256 by dollars
        4.50       40 rows  b457f9e34c2bc7b993d4c5a2cf33162cc59dace5918ad273c0c25c8b249d

## who x when

SHAPE_STAREA_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  0.000000000000000                         2026:4.50

SHAPE_STLENGTH_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  0.000000000000000                         2026:4.50

## what

DISTRICT: Boston Zoning Code 31%, Roslindale Neighborhood 6%, Roxbury Neighborhood 6%, Newmarket 21st Century Industr 6%, Stuart Street District 6%, Boston Proper 6%, Boston Harbor 6%, Government Center/Markets 6%, Bulfinch Triangle 6%, North End Neighborhood 6%, South End Neighborhood 6%, South Boston Neighborhood 6%

STAGE: Adopted 92%, Interim 8%

MAPNO: 8ABC 19%, 1C/1G/1N 19%, 1B/1J/1K/1L 14%, 10A-10B 10%, 6A/6B/6C 5%, 6E 5%, 1S 5%, 1 5%, 2A 5%, 1H 5%, 1P 5%, 4F 5%

ARTICLE: Underlying Zoning 37%, 42A 11%, 67 5%, 50 5%, 90 5%, 48 5%, 45 5%, 46 5%, 54 5%, 64 5%, 68 5%, 53 5%

VOLUME: Volume III 55%, Volume II 35%, Volume I 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DISTRICT | category | 36 | 0 | Boston Zoning Code 5; Roslindale Neighborhood 1; Roxbury Neighborhood 1; Newmarket 21st Century In 1 |
| STAGE | category | 2 | 0 | Adopted 37; Interim 3 |
| MAPNO | category | 30 | 0 | 8ABC 4; 1C/1G/1N 4; 1B/1J/1K/1L 3; 10A-10B 2 |
| ARTICLE | category | 32 | 0 | Underlying Zoning 7; 42A 2; 67 1; 50 1 |
| VOLUME | category | 3 | 0 | Volume III 22; Volume II 14; Volume I 4 |
| SHAPE_STAREA_1 | who | 1 | 0 | 0.000000000000000 40 |
| SHAPE_STLENGTH_1 | who | 1 | 0 | 0.000000000000000 40 |
| SHAPE_LENGTH | amount | 40 | 0 | 0.102219808501008 1; 0.256957361073665 1; 0.080064865684106 1; 0.018946002254858 1 |
| SHAPE_AREA | amount | 39 | 0 | 0.000064515772298 1; 0.000644731174746 1; 0.000046155671292 1; 0.000007710461412 1 |
| SHAPE_WKT | empty | 1 | 40 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:21:09.35490 40 |
| SOURCE_RUN_ID | audit | 1 | 0 | f90f123c-cbd4-452f-9aae-1 40 |
| SRC_SHA256 | who | 1 | 0 | b457f9e34c2bc7b993d4c5a2c 40 |
