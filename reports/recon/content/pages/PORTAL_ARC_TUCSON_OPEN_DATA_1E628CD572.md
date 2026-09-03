# PORTAL_ARC_TUCSON_OPEN_DATA_1E628CD572

rows 71  columns 37  scan 3.7s

roles: amount 6, audit 2, category 24, date 1, other 4, who 1

## when

INGESTED_AT
  2026        71  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MIN_SQFT | 63 | 1 | 2.5K | 100.0K | 100.0K | 1.09M |
| MAX_SQFT | 56 | 1.5K | 5.0K | 100.0K | 100.0K | 892.4K |
| EMPNUM | 69 | 1 | 7 | 172.40 | 220 | 2.1K |
| SALESVOL | 69 | 267.0K | 1.87M | 45.97M | 58.67M | 563.25M |
| LATITUDE | 69 | 32.17 | 32.23 | 32.27 | 32.27 | 2.2K |
| LONGITUDE | 69 | -111 | -110.96 | -110.91 | -110.90 | -7.7K |

## who

SRC_SHA256 by rows
        71  3d34a691b2e0b64a5636ae22b38bf101954997cbceb86993c657a740613eb534

SRC_SHA256 by dollars
        2.1K       71 rows  3d34a691b2e0b64a5636ae22b38bf101954997cbceb86993c657a740613e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = EMPNUM
  3d34a691b2e0b64a5636ae22b38bf101954997cb  2026:2.1K

## what

CONAME: Circle K 39%, 7-Eleven 12%, Food City Supermarket 8%, QuikTrip 8%, Quik Mart 8%, Fry's Food 6%, Speedway 4%, Safeway 4%, Albertsons 4%, Z Market 2%, Whole Foods Market 2%, Walmart Neighborhood Market 2%

ADDR: E Speedway Blvd 16%, E Broadway Blvd 11%, E 22nd St 11%, E Fort Lowell Rd 9%, W Saint Marys Rd 9%, E Grant Rd 9%, N Campbell Ave 7%, S Alvernon Way 7%, S 6th Ave 7%, nan 5%, N 1st Ave 5%, W Grant Rd 5%

CITY: Tucson 97%, nan 3%

STATE_NAME: Arizona 97%, nan 3%

STATE: AZ 97%, nan 3%

ZIP: 85719 31%, 85713 18%, 85745 17%, 85716 14%, 85705 7%, 85711 6%, nan 3%, 85701 3%, 85714 1%

NAICS: 44513101 54%, 44511003 42%, nan 3%, 44511001 1%

NAICS_ALL: 44511003 24%, 44513101, 45712003 20%, 44513101 15%, 44513101, 45521903, 45712003 9%, 44513101, 45712003, 72251117,  7%, 44513101, 45712003, 45712006 7%, nan 4%, 44511003, 45611009, 45619102,  4%, 44511003, 45619105, 44523001,  4%, 44511003, 45619103, 72251117,  2%, 44511003, 44511009 2%, 44513101, 45511003 2%

SIC: 541103 54%, 541105 42%, nan 3%, 541101 1%

SIC_ALL: 541105 24%, 541103, 554101 20%, 541103 15%, 541103, 533101, 554101 9%, 541103, 554101, 581208, 592104 7%, 541103, 554101, 554110 7%, nan 4%, 541105, 591205, 549909, 549935 4%, 541105, 549935, 543102, 546102 4%, 541105, 549901, 581208, 549935 2%, 541105, 541110 2%, 541103, 531104 2%

INDUSTRY_DESC: Grocers-Retail 24%, Convenience Stores, Service St 20%, Convenience Stores 15%, Convenience Stores, Variety St 9%, Convenience Stores, Service St 7%, Convenience Stores, Service St 7%, nan 4%, Grocers-Retail, Pharmacies, Fo 4%, Grocers-Retail, Organic Foods  4%, Grocers-Retail, Health & Diet  2%, Grocers-Retail, Grocery Pickup 2%, Convenience Stores, Retail Sho 2%

AFFILIATE: nan 100%

BRAND: nan 67%, Valero 33%

HQNAME: Circle K Stores Inc 38%, 7-Eleven, Inc 12%, QuikTrip Corporation 8%, Southwest Convenience SPE LLC 8%, Fry's Food Stores 6%, Food City 6%, Albertsons Companies, Inc 6%, nan 4%, Speedway LLC 4%, Safeway Inc 4%, Whole Foods Market, Inc 2%

LOC_CONF: Very High 93%, nan 3%, High 3%, Low 1%

NAICS_SECT: Retail Trade 97%, nan 3%

PLACETYPE: Branch 73%, Independent 24%, nan 3%

SQFOOTAGE: 2500 - 4999 46%, 1500 - 2499 15%, 100000+ 11%, 40000 - 99999 9%, 1 - 1499 8%, 5000 - 9999 5%, nan 3%, 20000 - 39999 3%

SOURCE: Data Axle 97%, nan 3%

DESC: Circle K, Tucson, Arizona 38%, 7-Eleven, Tucson, Arizona 12%, QuikTrip, Tucson, Arizona 8%, Quik Mart, Tucson, Arizona 8%, Fry's Food, Tucson, Arizona 6%, Food City Supermarket, Tucson, 6%, nan 4%, Speedway, Tucson, Arizona 4%, Safeway, Tucson, Arizona 4%, Albertsons, Tucson, Arizona 4%, Z Market, Tucson, Arizona 2%, Whole Foods Market, Tucson, Ar 2%

CREATIONDATE: 1742235902000.0 97%, nan 3%

CREATOR: ehammon1_cotgis 97%, nan 3%

EDITDATE: 1742235902000.0 97%, nan 3%

EDITOR: ehammon1_cotgis 97%, nan 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 71 | 0 | 71 1; 70 1; 69 1; 68 1 |
| CONAME | category | 34 | 0 | Circle K 19; 7-Eleven 6; Food City Supermarket 4; QuikTrip 4 |
| ADDR | category | 34 | 0 | E Speedway Blvd 7; E Broadway Blvd 5; E 22nd St 5; E Fort Lowell Rd 4 |
| CITY | category | 2 | 0 | Tucson 69; nan 2 |
| STATE_NAME | category | 2 | 0 | Arizona 69; nan 2 |
| STATE | category | 2 | 0 | AZ 69; nan 2 |
| ZIP | category | 9 | 0 | 85719 22; 85713 13; 85745 12; 85716 10 |
| ZIP4 | other | 63 | 3 | nan 2; 3107 2; 1405 2; 1909 2 |
| NAICS | category | 4 | 0 | 44513101 38; 44511003 30; nan 2; 44511001 1 |
| NAICS_ALL | category | 29 | 0 | 44511003 13; 44513101, 45712003 11; 44513101 8; 44513101, 45521903, 45712 5 |
| SIC | category | 4 | 0 | 541103 38; 541105 30; nan 2; 541101 1 |
| SIC_ALL | category | 29 | 0 | 541105 13; 541103, 554101 11; 541103 8; 541103, 533101, 554101 5 |
| INDUSTRY_DESC | category | 29 | 0 | Grocers-Retail 13; Convenience Stores, Servi 11; Convenience Stores 8; Convenience Stores, Varie 5 |
| AFFILIATE | category | 2 | 69 | nan 2 |
| BRAND | category | 3 | 68 | nan 2; Valero 1 |
| HQNAME | category | 18 | 17 | Circle K Stores Inc 18; 7-Eleven, Inc 6; QuikTrip Corporation 4; Southwest Convenience SPE 4 |
| LOC_CONF | category | 4 | 0 | Very High 66; nan 2; High 2; Low 1 |
| NAICS_SECT | category | 2 | 0 | Retail Trade 69; nan 2 |
| PLACETYPE | category | 3 | 0 | Branch 52; Independent 17; nan 2 |
| SQFOOTAGE | category | 9 | 6 | 2500 - 4999 30; 1500 - 2499 10; 100000+ 7; 40000 - 99999 6 |
| MIN_SQFT | amount | 8 | 0 | 2500.0 30; 1500.0 10; nan 8; 100000.0 7 |
| MAX_SQFT | amount | 7 | 0 | 4999.0 30; nan 15; 2499.0 10; 99999.0 6 |
| EMPNUM | amount | 32 | 0 | 7.0 15; 3.0 5; 4.0 5; 6.0 4 |
| SALESVOL | amount | 30 | 0 | 1867000.0 16; 801000.0 6; 1601000.0 6; 1334000.0 4 |
| SOURCE | category | 2 | 0 | Data Axle 69; nan 2 |
| ESRI_PID | other | 70 | 0 | nan 2; d42b9804b70258ba73460d914 1; b03e450839f86be82fdacb2bf 1; 98b7cdc46b81188234d29d068 1 |
| DESC | category | 35 | 0 | Circle K, Tucson, Arizona 18; 7-Eleven, Tucson, Arizona 6; QuikTrip, Tucson, Arizona 4; Quik Mart, Tucson, Arizon 4 |
| LATITUDE | amount | 70 | 0 | nan 2; 32.23909999991011 2; 32.2574110002608 1; 32.23569600005985 1 |
| LONGITUDE | amount | 70 | 0 | nan 2; -111.00405299955484 2; -110.9613189997306 1; -110.9213819997648 1 |
| CREATIONDATE | category | 2 | 0 | 1742235902000.0 69; nan 2 |
| CREATOR | category | 2 | 0 | ehammon1_cotgis 69; nan 2 |
| EDITDATE | category | 2 | 0 | 1742235902000.0 69; nan 2 |
| EDITOR | category | 2 | 0 | ehammon1_cotgis 69; nan 2 |
| GEOMETRY | other | 71 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:20.53858 71 |
| SOURCE_RUN_ID | audit | 1 | 0 | ca9cc670-729c-447c-9f31-1 71 |
| SRC_SHA256 | who | 1 | 0 | 3d34a691b2e0b64a5636ae22b 71 |
