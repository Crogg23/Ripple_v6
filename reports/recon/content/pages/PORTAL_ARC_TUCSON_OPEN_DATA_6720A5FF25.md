# PORTAL_ARC_TUCSON_OPEN_DATA_6720A5FF25

rows 5  columns 37  scan 4.0s

roles: amount 2, audit 2, category 19, date 3, empty 2, other 2, who 8

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
| LATITUDE | 5 | 32.23 | 32.23 | 32.25 | 32.25 | 161.17 |
| LONGITUDE | 5 | -111.01 | -111 | -110.99 | -110.99 | -555 |

## who

STATE_NAME by rows
         5  Arizona

STATE_NAME by dollars
      161.17        5 rows  Arizona

LOC_CONF by rows
         5  Very High

LOC_CONF by dollars
      161.17        5 rows  Very High

NAICS_SECT by rows
         5  Health Care & Social Assistance

NAICS_SECT by dollars
      161.17        5 rows  Health Care & Social Assistance

SOURCE by rows
         5  Data Axle

SOURCE by dollars
      161.17        5 rows  Data Axle

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Arizona                                   2025:161.17

LOC_CONF by CREATIONDATE, dollars = LATITUDE
  Very High                                 2025:161.17

## what

OBJECTID: 9 20%, 8 20%, 5 20%, 3 20%, 2 20%

CONAME: Northwest Gastroenterology At  20%, MHC Westside Health Center 20%, General Surgery 20%, Community Partners Integrated  20%, Carondalet St Mary's Hospital 20%

ADDR: W Saint Marys Rd 40%, W Grant Rd 20%, N Silverbell Rd 20%, N Bonita Ave 20%

ZIP4: 1173 20%, 2613 20%, 2981 20%, 2750 20%, 2682 20%

NAICS: 62211003 40%, 62199921 40%, 62211002 20%

NAICS_ALL: 62211003 40%, 62199921 40%, 62211002, 62211001 20%

SIC: 806201 40%, 809907 40%, 806202 20%

SIC_ALL: 806201 40%, 809907 40%, 806202, 806203 20%

INDUSTRY_DESC: Medical Centers 40%, Health Services 40%, Hospitals, Emergency Medical & 20%

HQNAME: Tenet Healthcare Corporation 100%

PLACETYPE: Independent 80%, Headquarters 20%

SQFOOTAGE: 2500 - 4999 40%, 20000 - 39999 20%, 10000 - 19999 20%, 100000+ 20%

MIN_SQFT: 2500 40%, 20000 20%, 10000 20%, 100000 20%

MAX_SQFT: 4999.0 40%, 39999.0 20%, 19999.0 20%, nan 20%

EMPNUM: 10 20%, 3 20%, 5 20%, 4 20%, 1184 20%

SALESVOL: 1856000 20%, 1042000 20%, 928000 20%, 1389000 20%, 219695000 20%

ESRI_PID: 48980c75adf72b1e9a9b52baff372e 20%, 0bfd590c36262d4c537668a18fe85b 20%, ecabe4495eb5c94139aef2ad1f7242 20%, 24f90e69177d45f43c61a3224daf92 20%, c3f5d7e3e39c3cb791340852f8d755 20%

DESC: Northwest Gastroenterology At  20%, MHC Westside Health Center, Tu 20%, General Surgery, Tucson, Arizo 20%, Community Partners Integrated  20%, Carondalet St Mary's Hospital, 20%

GEOMETRY: {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 5 | 0 | 9 1; 8 1; 5 1; 3 1 |
| CONAME | category | 5 | 0 | Northwest Gastroenterolog 1; MHC Westside Health Cente 1; General Surgery 1; Community Partners Integr 1 |
| ADDR | category | 4 | 0 | W Saint Marys Rd 2; W Grant Rd 1; N Silverbell Rd 1; N Bonita Ave 1 |
| CITY | who | 1 | 0 | Tucson 5 |
| STATE_NAME | who | 1 | 0 | Arizona 5 |
| STATE | other | 1 | 0 | AZ 5 |
| ZIP | other | 1 | 0 | 85745 5 |
| ZIP4 | category | 5 | 0 | 1173 1; 2613 1; 2981 1; 2750 1 |
| NAICS | category | 3 | 0 | 62211003 2; 62199921 2; 62211002 1 |
| NAICS_ALL | category | 3 | 0 | 62211003 2; 62199921 2; 62211002, 62211001 1 |
| SIC | category | 3 | 0 | 806201 2; 809907 2; 806202 1 |
| SIC_ALL | category | 3 | 0 | 806201 2; 809907 2; 806202, 806203 1 |
| INDUSTRY_DESC | category | 3 | 0 | Medical Centers 2; Health Services 2; Hospitals, Emergency Medi 1 |
| AFFILIATE | empty | 1 | 5 |  |
| BRAND | empty | 1 | 5 |  |
| HQNAME | category | 2 | 4 | Tenet Healthcare Corporat 1 |
| LOC_CONF | who | 1 | 0 | Very High 5 |
| NAICS_SECT | who | 1 | 0 | Health Care & Social Assi 5 |
| PLACETYPE | category | 2 | 0 | Independent 4; Headquarters 1 |
| SQFOOTAGE | category | 4 | 0 | 2500 - 4999 2; 20000 - 39999 1; 10000 - 19999 1; 100000+ 1 |
| MIN_SQFT | category | 4 | 0 | 2500 2; 20000 1; 10000 1; 100000 1 |
| MAX_SQFT | category | 4 | 0 | 4999.0 2; 39999.0 1; 19999.0 1; nan 1 |
| EMPNUM | category | 5 | 0 | 10 1; 3 1; 5 1; 4 1 |
| SALESVOL | category | 5 | 0 | 1856000 1; 1042000 1; 928000 1; 1389000 1 |
| SOURCE | who | 1 | 0 | Data Axle 5 |
| ESRI_PID | category | 5 | 0 | 48980c75adf72b1e9a9b52baf 1; 0bfd590c36262d4c537668a18 1; ecabe4495eb5c94139aef2ad1 1; 24f90e69177d45f43c61a3224 1 |
| DESC | category | 5 | 0 | Northwest Gastroenterolog 1; MHC Westside Health Cente 1; General Surgery, Tucson,  1; Community Partners Integr 1 |
| LATITUDE | amount | 5 | 0 | 32.25005799992489 1; 32.22735300036011 1; 32.22640500022376 1; 32.226586000351354 1 |
| LONGITUDE | amount | 5 | 0 | -111.00862600017112 1; -111.00209500012059 1; -111.00001700013735 1; -110.98532300011681 1 |
| CREATIONDATE | date | 1 | 0 | 1742236997000 5 |
| CREATOR | who | 1 | 0 | ehammon1_cotgis 5 |
| EDITDATE | date | 1 | 0 | 1742236997000 5 |
| EDITOR | who | 1 | 0 | ehammon1_cotgis 5 |
| GEOMETRY | category | 5 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:26.65736 5 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8f9334ea-30cc-45e1-b8a9-0 5 |
| SRC_SHA256 | who | 1 | 0 | b1d895f3707f27a59596d08c5 5 |
