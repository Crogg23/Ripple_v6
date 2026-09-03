# PORTAL_ARC_ATLANTA_DATAATLA_A29D594B47

rows 7  columns 35  scan 3.7s

roles: amount 2, audit 2, category 16, date 3, empty 3, other 1, who 9

## when

CREATIONDATE
  2024         7  ##############################

EDITDATE
  2024         7  ##############################

INGESTED_AT
  2026         7  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 7 | 33.70 | 33.72 | 33.79 | 33.79 | 236.12 |
| LONGITUDE | 7 | -84.51 | -84.43 | -84.36 | -84.36 | -591.08 |

## who

STATE_NAME by rows
         7  Georgia

STATE_NAME by dollars
      236.12        7 rows  Georgia

LOC_CONF by rows
         7  Very High

LOC_CONF by dollars
      236.12        7 rows  Very High

PLACETYPE by rows
         7  Independent

PLACETYPE by dollars
      236.12        7 rows  Independent

SOURCE by rows
         7  Data Axle

SOURCE by dollars
      236.12        7 rows  Data Axle

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2024:236.12

LOC_CONF by CREATIONDATE, dollars = LATITUDE
  Very High                                 2024:236.12

## what

OBJECTID: 7 14%, 6 14%, 5 14%, 4 14%, 3 14%, 2 14%, 1 14%

CONAME: Thomasville Recreation Center 14%, Perkerson Park Recreation Cent 14%, Oakland City Park Recreation 14%, James Orange Recreation Center 14%, Collier Heights Recreation Cen 14%, A D Williams Recreation Center 14%, Adams Recreation Center 14%

ADDR: Oakland Dr SW 29%, Henry Thomas Dr SE 14%, Deckner Ave SW 14%, Collier Dr NW 14%, James Jackson Pkwy NW 14%, Delowe Dr SW 14%

ZIP: 30310 43%, 30315 14%, 30331 14%, 30318 14%, 30311 14%

ZIP4: 4013 29%, 5613 14%, 4300 14%, 1531 14%, 3827 14%, 3914 14%

NAICS: 71394015 86%, 81341004 14%

NAICS_ALL: 71394015 86%, 81341004 14%

SIC: 799701 86%, 864108 14%

SIC_ALL: 799701 86%, 864108 14%

SQFOOTAGE: 2500 - 4999 57%, 1500 - 2499 29%, 10000 - 19999 14%

MIN_SQFT: 2500 57%, 1500 29%, 10000 14%

MAX_SQFT: 4999 57%, 2499 29%, 19999 14%

EMPNUM: 4 43%, 3 29%, 15 14%, 2 14%

SALESVOL: 245000.0 43%, 184000.0 29%, nan 14%, 123000.0 14%

ESRI_PID: 88b5ffd3f3efc87030c7d372d69d11 14%, 1b8e1a9b641a67b1cc23f676805daf 14%, b772475719ea950e95621579419216 14%, 4b17f4502e1effc3089ad2f28c93a9 14%, ab582b4ee7e5c735eaeecaa6b2d47e 14%, 6339cea777fa34412a6559e21277f1 14%, cdb898a86321b45df60e349dffd014 14%

GEOMETRY: {"type": "Point", "coordinates 29%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 7 | 0 | 7 1; 6 1; 5 1; 4 1 |
| CONAME | category | 7 | 0 | Thomasville Recreation Ce 1; Perkerson Park Recreation 1; Oakland City Park Recreat 1; James Orange Recreation C 1 |
| ADDR | category | 6 | 0 | Oakland Dr SW 2; Henry Thomas Dr SE 1; Deckner Ave SW 1; Collier Dr NW 1 |
| CITY | who | 1 | 0 | Atlanta 7 |
| STATE_NAME | who | 1 | 0 | Georgia 7 |
| STATE | other | 1 | 0 | GA 7 |
| ZIP | category | 5 | 0 | 30310 3; 30315 1; 30331 1; 30318 1 |
| ZIP4 | category | 6 | 0 | 4013 2; 5613 1; 4300 1; 1531 1 |
| NAICS | category | 2 | 0 | 71394015 6; 81341004 1 |
| NAICS_ALL | category | 2 | 0 | 71394015 6; 81341004 1 |
| SIC | category | 2 | 0 | 799701 6; 864108 1 |
| SIC_ALL | category | 2 | 0 | 799701 6; 864108 1 |
| AFFILIATE | empty | 1 | 7 |  |
| BRAND | empty | 1 | 7 |  |
| HQNAME | empty | 1 | 7 |  |
| LOC_CONF | who | 1 | 0 | Very High 7 |
| PLACETYPE | who | 1 | 0 | Independent 7 |
| SQFOOTAGE | category | 3 | 0 | 2500 - 4999 4; 1500 - 2499 2; 10000 - 19999 1 |
| MIN_SQFT | category | 3 | 0 | 2500 4; 1500 2; 10000 1 |
| MAX_SQFT | category | 3 | 0 | 4999 4; 2499 2; 19999 1 |
| EMPNUM | category | 4 | 0 | 4 3; 3 2; 15 1; 2 1 |
| SALESVOL | category | 4 | 0 | 245000.0 3; 184000.0 2; nan 1; 123000.0 1 |
| SOURCE | who | 1 | 0 | Data Axle 7 |
| ESRI_PID | category | 7 | 0 | 88b5ffd3f3efc87030c7d372d 1; 1b8e1a9b641a67b1cc23f6768 1; b772475719ea950e956215794 1; 4b17f4502e1effc3089ad2f28 1 |
| DESC | who | 1 | 0 | CONAME, Atlanta, Georgia 7 |
| LATITUDE | amount | 6 | 0 | 33.719266000228764 2; 33.7039979997743 1; 33.71192099968331 1; 33.76968499994345 1 |
| LONGITUDE | amount | 6 | 0 | -84.42925100020226 2; -84.35810099993225 1; -84.41307699970002 1; -84.50678100001181 1 |
| CREATIONDATE | date | 1 | 0 | 1724425870152 7 |
| CREATOR | who | 1 | 0 | gpickren2 7 |
| EDITDATE | date | 1 | 0 | 1724425870152 7 |
| EDITOR | who | 1 | 0 | gpickren2 7 |
| GEOMETRY | category | 6 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:37.81959 7 |
| SOURCE_RUN_ID | audit | 1 | 0 | e496f0d2-df3b-4f39-85ea-e 7 |
| SRC_SHA256 | who | 1 | 0 | afebe3234833385e395d1564f 7 |
