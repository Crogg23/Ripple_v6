# PORTAL_ARC_TUCSON_OPEN_DATA_32A72D9D1D

rows 5  columns 37  scan 3.8s

roles: amount 2, audit 2, category 16, date 3, empty 2, other 2, who 11

## when

CREATIONDATE
  2025         5  ##############################

EDITDATE
  2025         5  ##############################

INGESTED_AT
  2026         5  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 5 | 32.23 | 32.24 | 32.25 | 32.25 | 161.19 |
| LONGITUDE | 5 | -111 | -111 | -110.98 | -110.98 | -554.98 |

## who

STATE_NAME by rows
         5  Arizona

STATE_NAME by dollars
      161.19        5 rows  Arizona

NAICS by rows
         5  44513101

NAICS by dollars
      161.19        5 rows  44513101

SIC by rows
         5  541103

SIC by dollars
      161.19        5 rows  541103

LOC_CONF by rows
         5  Very High

LOC_CONF by dollars
      161.19        5 rows  Very High

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Arizona                                   2025:161.19

NAICS by CREATIONDATE, dollars = LATITUDE
  44513101                                  2025:161.19

## what

OBJECTID: 5 20%, 4 20%, 3 20%, 2 20%, 1 20%

CONAME: QuikTrip 20%, Jacksons 20%, Circle K 20%, ampm 20%, 7-Eleven 20%

ADDR: W Saint Marys Rd 40%, W Speedway Blvd 40%, W Grant Rd 20%

ZIP4: 1405 20%, 3153 20%, 2218 20%, 2461 20%, 3107 20%

NAICS_ALL: 44513101, 45712003, 72251117,  20%, 44513101, 45712003 20%, 44513101, 45521903, 45712003 20%, 44513101, 45712003, 45712006 20%, 44513101, 45712003, 72251117 20%

SIC_ALL: 541103, 554101, 581208, 592104 20%, 541103, 554101 20%, 541103, 533101, 554101 20%, 541103, 554101, 554110 20%, 541103, 554101, 581208 20%

INDUSTRY_DESC: Convenience Stores, Service St 20%, Convenience Stores, Service St 20%, Convenience Stores, Variety St 20%, Convenience Stores, Service St 20%, Convenience Stores, Service St 20%

HQNAME: QuikTrip Corporation 20%, Jacksons Food Stores Inc 20%, Circle K Stores Inc 20%, BP Refining & Marketing 20%, 7-Eleven, Inc 20%

SQFOOTAGE: 2500 - 4999 60%, 5000 - 9999 20%, 1500 - 2499 20%

MIN_SQFT: 2500 60%, 5000 20%, 1500 20%

MAX_SQFT: 4999 60%, 9999 20%, 2499 20%

EMPNUM: 12 20%, 6 20%, 4 20%, 10 20%, 5 20%

SALESVOL: 1601000 60%, 3201000 20%, 2667000 20%

ESRI_PID: d9f9d034aefe9b76ccf9d272f62a8d 20%, 1cfe660cac330591d53457871251a9 20%, 472791095c36dd18d156ac86e880b1 20%, 3bcde17635dd0959fc31ab7eb87a00 20%, f6a50342d68d8cb910e6fd4306c3f0 20%

DESC: QuikTrip, Tucson, Arizona 20%, Jacksons, Tucson, Arizona 20%, Circle K, Tucson, Arizona 20%, ampm, Tucson, Arizona 20%, 7-Eleven, Tucson, Arizona 20%

GEOMETRY: {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 5 | 0 | 5 1; 4 1; 3 1; 2 1 |
| CONAME | category | 5 | 0 | QuikTrip 1; Jacksons 1; Circle K 1; ampm 1 |
| ADDR | category | 3 | 0 | W Saint Marys Rd 2; W Speedway Blvd 2; W Grant Rd 1 |
| CITY | who | 1 | 0 | Tucson 5 |
| STATE_NAME | who | 1 | 0 | Arizona 5 |
| STATE | other | 1 | 0 | AZ 5 |
| ZIP | other | 1 | 0 | 85745 5 |
| ZIP4 | category | 5 | 0 | 1405 1; 3153 1; 2218 1; 2461 1 |
| NAICS | who | 1 | 0 | 44513101 5 |
| NAICS_ALL | category | 5 | 0 | 44513101, 45712003, 72251 1; 44513101, 45712003 1; 44513101, 45521903, 45712 1; 44513101, 45712003, 45712 1 |
| SIC | who | 1 | 0 | 541103 5 |
| SIC_ALL | category | 5 | 0 | 541103, 554101, 581208, 5 1; 541103, 554101 1; 541103, 533101, 554101 1; 541103, 554101, 554110 1 |
| INDUSTRY_DESC | category | 5 | 0 | Convenience Stores, Servi 1; Convenience Stores, Servi 1; Convenience Stores, Varie 1; Convenience Stores, Servi 1 |
| AFFILIATE | empty | 1 | 5 |  |
| BRAND | empty | 1 | 5 |  |
| HQNAME | category | 5 | 0 | QuikTrip Corporation 1; Jacksons Food Stores Inc 1; Circle K Stores Inc 1; BP Refining & Marketing 1 |
| LOC_CONF | who | 1 | 0 | Very High 5 |
| NAICS_SECT | who | 1 | 0 | Retail Trade 5 |
| PLACETYPE | who | 1 | 0 | Branch 5 |
| SQFOOTAGE | category | 3 | 0 | 2500 - 4999 3; 5000 - 9999 1; 1500 - 2499 1 |
| MIN_SQFT | category | 3 | 0 | 2500 3; 5000 1; 1500 1 |
| MAX_SQFT | category | 3 | 0 | 4999 3; 9999 1; 2499 1 |
| EMPNUM | category | 5 | 0 | 12 1; 6 1; 4 1; 10 1 |
| SALESVOL | category | 3 | 0 | 1601000 3; 3201000 1; 2667000 1 |
| SOURCE | who | 1 | 0 | Data Axle 5 |
| ESRI_PID | category | 5 | 0 | d9f9d034aefe9b76ccf9d272f 1; 1cfe660cac330591d53457871 1; 472791095c36dd18d156ac86e 1; 3bcde17635dd0959fc31ab7eb 1 |
| DESC | category | 5 | 0 | QuikTrip, Tucson, Arizona 1; Jacksons, Tucson, Arizona 1; Circle K, Tucson, Arizona 1; ampm, Tucson, Arizona 1 |
| LATITUDE | amount | 5 | 0 | 32.24995699987718 1; 32.22921400018983 1; 32.23521800004077 1; 32.23604699987471 1 |
| LONGITUDE | amount | 5 | 0 | -110.99848399995219 1; -110.99798299963678 1; -111.00331799978603 1; -110.98487399967996 1 |
| CREATIONDATE | date | 1 | 0 | 1742235902000 5 |
| CREATOR | who | 1 | 0 | ehammon1_cotgis 5 |
| EDITDATE | date | 1 | 0 | 1742235902000 5 |
| EDITOR | who | 1 | 0 | ehammon1_cotgis 5 |
| GEOMETRY | category | 5 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:20.36466 5 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7d68e646-9dc4-4383-ba81-e 5 |
| SRC_SHA256 | who | 1 | 0 | 47d11ca031def4ad58d089229 5 |
