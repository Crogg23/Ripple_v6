# PORTAL_CKA_SAN_JOSE_OPEN_DA_E5E353E19D

rows 6  columns 12  scan 2.6s

roles: amount 2, audit 2, category 6, date 1, empty 1, who 1

## when

INGESTED_AT
  2026         6  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 6 | 43.1K | 115.9K | 492.3K | 511.2K | 1.03M |
| SHAPE_AREA | 6 | 31.62M | 341.29M | 2.57B | 2.68B | 4.10B |

## who

SRC_SHA256 by rows
         6  d7fae5829dad03182d0dcfd899ec1947bca87c6b5bf38a0104f2bedcff74a4b5

SRC_SHA256 by dollars
       1.03M        6 rows  d7fae5829dad03182d0dcfd899ec1947bca87c6b5bf38a0104f2bedcff74

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  d7fae5829dad03182d0dcfd899ec1947bca87c6b  2026:1.03M

## what

OBJECTID: 6 17%, 5 17%, 4 17%, 3 17%, 2 17%, 1 17%

FACILITYID: 3 17%, 2 17%, 25 17%, 21 17%, 20 17%, 30 17%

INTID: 3 17%, 2 17%, 25 17%, 21 17%, 20 17%, 30 17%

NAME: San Jose Municipal Water Syste 67%, Great Oaks Water Company 17%, San Jose Water Company 17%

SERVICEAREA: North San Jose/Alviso 25%, Coyote 25%, Edenvale 25%, Evergreen 25%

LASTUPDATE: 2013/03/05 13:31:37+00 17%, 2007/04/17 12:31:25+00 17%, 2007/04/23 13:30:14+00 17%, 2007/04/17 12:29:41+00 17%, 2007/04/17 12:27:29+00 17%, 2025/03/01 00:16:32+00 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 6 | 0 | 6 1; 5 1; 4 1; 3 1 |
| FACILITYID | category | 6 | 0 | 3 1; 2 1; 25 1; 21 1 |
| INTID | category | 6 | 0 | 3 1; 2 1; 25 1; 21 1 |
| NAME | category | 3 | 0 | San Jose Municipal Water  4; Great Oaks Water Company 1; San Jose Water Company 1 |
| SERVICEAREA | category | 5 | 2 | North San Jose/Alviso 1; Coyote 1; Edenvale 1; Evergreen 1 |
| LASTUPDATE | category | 6 | 0 | 2013/03/05 13:31:37+00 1; 2007/04/17 12:31:25+00 1; 2007/04/23 13:30:14+00 1; 2007/04/17 12:29:41+00 1 |
| NOTES | empty | 1 | 6 |  |
| SHAPE_LENGTH | amount | 6 | 0 | 106445.887095039 1; 118352.08024872 1; 134077.659586047 1; 43119.2720029085 1 |
| SHAPE_AREA | amount | 6 | 0 | 241088315.638061 1; 322645463.138813 1; 359927972.843892 1; 31623709.7295254 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:10:41.46536 6 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2959ef97-babe-4a17-937c-6 6 |
| SRC_SHA256 | who | 1 | 0 | d7fae5829dad03182d0dcfd89 6 |
