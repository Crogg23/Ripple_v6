# PORTAL_ARC_TUCSON_OPEN_DATA_F0203665DD

rows 2  columns 37  scan 4.0s

roles: amount 2, audit 2, category 16, date 3, empty 2, other 2, who 11

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
| LATITUDE | 2 | 32.23 | 32.24 | 32.25 | 32.25 | 64.48 |
| LONGITUDE | 2 | -111 | -111.00 | -110.99 | -110.99 | -221.99 |

## who

STATE_NAME by rows
         2  Arizona

STATE_NAME by dollars
       64.48        2 rows  Arizona

NAICS by rows
         2  45611009

NAICS by dollars
       64.48        2 rows  45611009

SIC by rows
         2  591205

SIC by dollars
       64.48        2 rows  591205

LOC_CONF by rows
         2  Very High

LOC_CONF by dollars
       64.48        2 rows  Very High

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Arizona                                   2025:64.48

NAICS by CREATIONDATE, dollars = LATITUDE
  45611009                                  2025:64.48

## what

OBJECTID: 4 50%, 2 50%

CONAME: Walgreens 50%, Amerita, Inc 50%

ADDR: N Silverbell Rd 50%, N Forbes Blvd 50%

ZIP4: 2626 50%, 1446 50%

NAICS_ALL: 45611009, 45521903, 45619106,  50%, 45611009, 99999005, 62419025,  50%

SIC_ALL: 591205, 533101, 549904, 591202 50%, 591205, 999966, 832259, 808201 50%

INDUSTRY_DESC: Pharmacies, Variety Stores, Vi 50%, Pharmacies, Federal Government 50%

HQNAME: Walgreen Co 50%, Amerita, Inc 50%

SQFOOTAGE: 10000 - 19999 50%, 5000 - 9999 50%

MIN_SQFT: 10000 50%, 5000 50%

MAX_SQFT: 19999 50%, 9999 50%

EMPNUM: 25 50%, 15 50%

SALESVOL: 9926000 50%, 5956000 50%

ESRI_PID: ed159895e291417ce8c70173f243c9 50%, 4f619efb86ffdef763537e1e30fc7f 50%

DESC: Walgreens, Tucson, Arizona 50%, Amerita, Inc, Tucson, Arizona 50%

GEOMETRY: {"type": "Point", "coordinates 50%, {"type": "Point", "coordinates 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 4 1; 2 1 |
| CONAME | category | 2 | 0 | Walgreens 1; Amerita, Inc 1 |
| ADDR | category | 2 | 0 | N Silverbell Rd 1; N Forbes Blvd 1 |
| CITY | who | 1 | 0 | Tucson 2 |
| STATE_NAME | who | 1 | 0 | Arizona 2 |
| STATE | other | 1 | 0 | AZ 2 |
| ZIP | other | 1 | 0 | 85745 2 |
| ZIP4 | category | 2 | 0 | 2626 1; 1446 1 |
| NAICS | who | 1 | 0 | 45611009 2 |
| NAICS_ALL | category | 2 | 0 | 45611009, 45521903, 45619 1; 45611009, 99999005, 62419 1 |
| SIC | who | 1 | 0 | 591205 2 |
| SIC_ALL | category | 2 | 0 | 591205, 533101, 549904, 5 1; 591205, 999966, 832259, 8 1 |
| INDUSTRY_DESC | category | 2 | 0 | Pharmacies, Variety Store 1; Pharmacies, Federal Gover 1 |
| AFFILIATE | empty | 1 | 2 |  |
| BRAND | empty | 1 | 2 |  |
| HQNAME | category | 2 | 0 | Walgreen Co 1; Amerita, Inc 1 |
| LOC_CONF | who | 1 | 0 | Very High 2 |
| NAICS_SECT | who | 1 | 0 | Retail Trade 2 |
| PLACETYPE | who | 1 | 0 | Branch 2 |
| SQFOOTAGE | category | 2 | 0 | 10000 - 19999 1; 5000 - 9999 1 |
| MIN_SQFT | category | 2 | 0 | 10000 1; 5000 1 |
| MAX_SQFT | category | 2 | 0 | 19999 1; 9999 1 |
| EMPNUM | category | 2 | 0 | 25 1; 15 1 |
| SALESVOL | category | 2 | 0 | 9926000 1; 5956000 1 |
| SOURCE | who | 1 | 0 | Data Axle 2 |
| ESRI_PID | category | 2 | 0 | ed159895e291417ce8c70173f 1; 4f619efb86ffdef763537e1e3 1 |
| DESC | category | 2 | 0 | Walgreens, Tucson, Arizon 1; Amerita, Inc, Tucson, Ari 1 |
| LATITUDE | amount | 2 | 0 | 32.23040499992974 1; 32.2461020002276 1 |
| LONGITUDE | amount | 2 | 0 | -110.9999359999465 1; -110.99049099986155 1 |
| CREATIONDATE | date | 1 | 0 | 1743027867000 2 |
| CREATOR | who | 1 | 0 | ehammon1_cotgis 2 |
| EDITDATE | date | 1 | 0 | 1743027867000 2 |
| EDITOR | who | 1 | 0 | ehammon1_cotgis 2 |
| GEOMETRY | category | 2 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:01.12653 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | fab2b0f8-389b-4b2b-9428-f 2 |
| SRC_SHA256 | who | 1 | 0 | 69dcf0a7d41976ebc67350c02 2 |
