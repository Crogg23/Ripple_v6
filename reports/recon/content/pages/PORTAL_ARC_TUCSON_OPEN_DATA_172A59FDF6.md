# PORTAL_ARC_TUCSON_OPEN_DATA_172A59FDF6

rows 4  columns 37  scan 4.4s

roles: amount 2, audit 2, category 18, date 3, empty 2, other 2, who 9

## when

CREATIONDATE
  2025         4  ##############################

EDITDATE
  2025         4  ##############################

INGESTED_AT
  2026         4  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 4 | 32.23 | 32.23 | 32.24 | 32.24 | 128.93 |
| LONGITUDE | 4 | -111 | -111.00 | -110.99 | -110.99 | -443.98 |

## who

STATE_NAME by rows
         4  Arizona

STATE_NAME by dollars
      128.93        4 rows  Arizona

NAICS by rows
         4  44511003

NAICS by dollars
      128.93        4 rows  44511003

SIC by rows
         4  541105

SIC by dollars
      128.93        4 rows  541105

NAICS_SECT by rows
         4  Retail Trade

NAICS_SECT by dollars
      128.93        4 rows  Retail Trade

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Arizona                                   2025:128.93

NAICS by CREATIONDATE, dollars = LATITUDE
  44511003                                  2025:128.93

## what

OBJECTID: 4 25%, 3 25%, 2 25%, 1 25%

CONAME: Safeway Grocery & Pharmacy 25%, Food City Supermarket 25%, El Rio Carniceria LLC 25%, Albertsons Grocery & Pharmacy 25%

ADDR: W Saint Marys Rd 50%, W High Rd 25%, N Silverbell Rd 25%

ZIP4: 3107 33%, 3115 33%, 2228 33%

NAICS_ALL: 44511003 50%, 44511003, 31181102, 44532004,  25%, 44511003, 45619105, 44523001,  25%

SIC_ALL: 541105 50%, 541105, 546102, 592102, 599201 25%, 541105, 549935, 543102, 546102 25%

INDUSTRY_DESC: Grocers-Retail 50%, Grocers-Retail, Bakers-Retail, 25%, Grocers-Retail, Organic Foods  25%

HQNAME: Safeway Inc 33%, Food City 33%, Albertsons Companies, Inc 33%

LOC_CONF: Very High 75%, Low 25%

PLACETYPE: Branch 75%, Independent 25%

SQFOOTAGE: 40000 - 99999 67%, 100000+ 33%

MIN_SQFT: 40000.0 50%, 100000.0 25%, nan 25%

MAX_SQFT: 99999.0 50%, nan 50%

EMPNUM: 71 25%, 86 25%, 55 25%, 130 25%

SALESVOL: 18934000 25%, 31735000 25%, 14668000 25%, 34668000 25%

ESRI_PID: d0d05f9dc42d1acd738124d8bfe53c 25%, 55dcc523fff25012d689eefe0913bd 25%, 0d4b635ae7656dcdd75539fb24bd13 25%, 7fe33240f77c5560e032d48f77fce8 25%

DESC: Safeway, Tucson, Arizona 25%, Food City Supermarket, Tucson, 25%, El Rio Carniceria LLC, Tucson, 25%, Albertsons, Tucson, Arizona 25%

GEOMETRY: {"type": "Point", "coordinates 25%, {"type": "Point", "coordinates 25%, {"type": "Point", "coordinates 25%, {"type": "Point", "coordinates 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 4 | 0 | 4 1; 3 1; 2 1; 1 1 |
| CONAME | category | 4 | 0 | Safeway Grocery & Pharmac 1; Food City Supermarket 1; El Rio Carniceria LLC 1; Albertsons Grocery & Phar 1 |
| ADDR | category | 3 | 0 | W Saint Marys Rd 2; W High Rd 1; N Silverbell Rd 1 |
| CITY | who | 1 | 0 | Tucson 4 |
| STATE_NAME | who | 1 | 0 | Arizona 4 |
| STATE | other | 1 | 0 | AZ 4 |
| ZIP | other | 1 | 0 | 85745 4 |
| ZIP4 | category | 4 | 1 | 3107 1; 3115 1; 2228 1 |
| NAICS | who | 1 | 0 | 44511003 4 |
| NAICS_ALL | category | 3 | 0 | 44511003 2; 44511003, 31181102, 44532 1; 44511003, 45619105, 44523 1 |
| SIC | who | 1 | 0 | 541105 4 |
| SIC_ALL | category | 3 | 0 | 541105 2; 541105, 546102, 592102, 5 1; 541105, 549935, 543102, 5 1 |
| INDUSTRY_DESC | category | 3 | 0 | Grocers-Retail 2; Grocers-Retail, Bakers-Re 1; Grocers-Retail, Organic F 1 |
| AFFILIATE | empty | 1 | 4 |  |
| BRAND | empty | 1 | 4 |  |
| HQNAME | category | 4 | 1 | Safeway Inc 1; Food City 1; Albertsons Companies, Inc 1 |
| LOC_CONF | category | 2 | 0 | Very High 3; Low 1 |
| NAICS_SECT | who | 1 | 0 | Retail Trade 4 |
| PLACETYPE | category | 2 | 0 | Branch 3; Independent 1 |
| SQFOOTAGE | category | 3 | 1 | 40000 - 99999 2; 100000+ 1 |
| MIN_SQFT | category | 3 | 0 | 40000.0 2; 100000.0 1; nan 1 |
| MAX_SQFT | category | 2 | 0 | 99999.0 2; nan 2 |
| EMPNUM | category | 4 | 0 | 71 1; 86 1; 55 1; 130 1 |
| SALESVOL | category | 4 | 0 | 18934000 1; 31735000 1; 14668000 1; 34668000 1 |
| SOURCE | who | 1 | 0 | Data Axle 4 |
| ESRI_PID | category | 4 | 0 | d0d05f9dc42d1acd738124d8b 1; 55dcc523fff25012d689eefe0 1; 0d4b635ae7656dcdd75539fb2 1; 7fe33240f77c5560e032d48f7 1 |
| DESC | category | 4 | 0 | Safeway, Tucson, Arizona 1; Food City Supermarket, Tu 1; El Rio Carniceria LLC, Tu 1; Albertsons, Tucson, Arizo 1 |
| LATITUDE | amount | 4 | 0 | 32.22765300018092 1; 32.22848700008785 1; 32.22936499984429 1; 32.23909999991011 1 |
| LONGITUDE | amount | 4 | 0 | -110.99801199994906 1; -110.99104800025346 1; -110.9924449999962 1; -111.00405299955484 1 |
| CREATIONDATE | date | 1 | 0 | 1742235902000 4 |
| CREATOR | who | 1 | 0 | ehammon1_cotgis 4 |
| EDITDATE | date | 1 | 0 | 1742235902000 4 |
| EDITOR | who | 1 | 0 | ehammon1_cotgis 4 |
| GEOMETRY | category | 4 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:14.58323 4 |
| SOURCE_RUN_ID | audit | 1 | 0 | d2063c4b-c02a-4ac6-89f9-9 4 |
| SRC_SHA256 | who | 1 | 0 | 4a17bd6028c33673ab1e48c42 4 |
