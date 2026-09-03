# PORTAL_ARC_TUCSON_OPEN_DATA_E0EDEA39BE

rows 2  columns 37  scan 3.4s

roles: amount 2, audit 2, category 15, date 3, empty 2, other 2, who 12

## when

CREATIONDATE
  2025         2  ##############################

EDITDATE
  2025         2  ##############################

INGESTED_AT
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 2 | 32.23 | 32.23 | 32.23 | 32.23 | 64.46 |
| LONGITUDE | 2 | -111 | -111.00 | -110.99 | -110.99 | -221.99 |

## who

STATE_NAME by rows
         2  Arizona

STATE_NAME by dollars
       64.46        2 rows  Arizona

ADDR by rows
         2  W Saint Marys Rd

ADDR by dollars
       64.46        2 rows  W Saint Marys Rd

NAICS by rows
         2  45521903

NAICS by dollars
       64.46        2 rows  45521903

SIC by rows
         2  533101

SIC by dollars
       64.46        2 rows  533101

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Arizona                                   2025:64.46

ADDR by CREATIONDATE, dollars = LATITUDE
  W Saint Marys Rd                          2025:64.46

## what

OBJECTID: 2 50%, 1 50%

CONAME: Family Dollar 50%, Dollar Tree 50%

ZIP4: 3115 50%, 3107 50%

NAICS_ALL: 45521903, 45811041, 45511001,  50%, 45521903, 45511003, 45942026,  50%

SIC_ALL: 533101, 565101, 531102, 531104 50%, 533101, 531104, 594716, 531102 50%

INDUSTRY_DESC: Variety Stores, Clothing-Retai 50%, Variety Stores, Retail Shops,  50%

HQNAME: Family Dollar Stores, Inc 50%, Dollar Tree Stores Inc 50%

SQFOOTAGE: 2500 - 4999 50%, 10000 - 19999 50%

MIN_SQFT: 2500 50%, 10000 50%

MAX_SQFT: 4999 50%, 19999 50%

EMPNUM: 8 50%, 14 50%

SALESVOL: 1487000 50%, 2603000 50%

ESRI_PID: a9001532f6ef54aca749c471bc5979 50%, 6ab937947318c6da9692b60cce1f08 50%

DESC: Family Dollar, Tucson, Arizona 50%, Dollar Tree, Tucson, Arizona 50%

GEOMETRY: {"type": "Point", "coordinates 50%, {"type": "Point", "coordinates 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 2 1; 1 1 |
| CONAME | category | 2 | 0 | Family Dollar 1; Dollar Tree 1 |
| ADDR | who | 1 | 0 | W Saint Marys Rd 2 |
| CITY | who | 1 | 0 | Tucson 2 |
| STATE_NAME | who | 1 | 0 | Arizona 2 |
| STATE | other | 1 | 0 | AZ 2 |
| ZIP | other | 1 | 0 | 85745 2 |
| ZIP4 | category | 2 | 0 | 3115 1; 3107 1 |
| NAICS | who | 1 | 0 | 45521903 2 |
| NAICS_ALL | category | 2 | 0 | 45521903, 45811041, 45511 1; 45521903, 45511003, 45942 1 |
| SIC | who | 1 | 0 | 533101 2 |
| SIC_ALL | category | 2 | 0 | 533101, 565101, 531102, 5 1; 533101, 531104, 594716, 5 1 |
| INDUSTRY_DESC | category | 2 | 0 | Variety Stores, Clothing- 1; Variety Stores, Retail Sh 1 |
| AFFILIATE | empty | 1 | 2 |  |
| BRAND | empty | 1 | 2 |  |
| HQNAME | category | 2 | 0 | Family Dollar Stores, Inc 1; Dollar Tree Stores Inc 1 |
| LOC_CONF | who | 1 | 0 | Very High 2 |
| NAICS_SECT | who | 1 | 0 | Retail Trade 2 |
| PLACETYPE | who | 1 | 0 | Branch 2 |
| SQFOOTAGE | category | 2 | 0 | 2500 - 4999 1; 10000 - 19999 1 |
| MIN_SQFT | category | 2 | 0 | 2500 1; 10000 1 |
| MAX_SQFT | category | 2 | 0 | 4999 1; 19999 1 |
| EMPNUM | category | 2 | 0 | 8 1; 14 1 |
| SALESVOL | category | 2 | 0 | 1487000 1; 2603000 1 |
| SOURCE | who | 1 | 0 | Data Axle 2 |
| ESRI_PID | category | 2 | 0 | a9001532f6ef54aca749c471b 1; 6ab937947318c6da9692b60cc 1 |
| DESC | category | 2 | 0 | Family Dollar, Tucson, Ar 1; Dollar Tree, Tucson, Ariz 1 |
| LATITUDE | amount | 2 | 0 | 32.228516999816186 1; 32.2277920003169 1 |
| LONGITUDE | amount | 2 | 0 | -110.99189799965002 1; -110.99741600009737 1 |
| CREATIONDATE | date | 1 | 0 | 1743694109000 2 |
| CREATOR | who | 1 | 0 | ehammon1_cotgis 2 |
| EDITDATE | date | 1 | 0 | 1743694109000 2 |
| EDITOR | who | 1 | 0 | ehammon1_cotgis 2 |
| GEOMETRY | category | 2 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:07.94694 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | b2cd607f-ebc9-484d-8bb7-7 2 |
| SRC_SHA256 | who | 1 | 0 | dbce579cb1697290b415ba21b 2 |
