# PORTAL_ARC_ATLANTA_DATAATLA_5D9B9C30A9

rows 14  columns 36  scan 4.1s

roles: amount 3, audit 2, category 18, date 3, empty 2, other 1, who 8

## when

CREATIONDATE
  2025        14  ##############################

EDITDATE
  2025        14  ##############################

INGESTED_AT
  2026        14  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MAX_SQFT | 10 | 2.5K | 5.0K | 40.0K | 40.0K | 137.5K |
| LATITUDE | 14 | 33.73 | 33.75 | 33.83 | 33.83 | 472.68 |
| LONGITUDE | 14 | -84.51 | -84.39 | -84.32 | -84.32 | -1.2K |

## who

STATE_NAME by rows
        14  Georgia

STATE_NAME by dollars
      472.68       14 rows  Georgia

LOC_CONF by rows
        14  Very High

LOC_CONF by dollars
      472.68       14 rows  Very High

SOURCE by rows
        14  Data Axle

SOURCE by dollars
      472.68       14 rows  Data Axle

DESC by rows
        14  CONAME, Atlanta, Georgia

DESC by dollars
      472.68       14 rows  CONAME, Atlanta, Georgia

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2025:472.68

LOC_CONF by CREATIONDATE, dollars = LATITUDE
  Very High                                 2025:472.68

## what

OBJECTID: 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%

CONAME: Substance Abuse 8%, Xcovid 8%, Learn to Grow Inc 8%, Georgia Dept of Community Heal 8%, Fulton County Mental Health Ce 8%, Fulton County Board of Health 8%, Centers-Disease Control & Prev 8%, Health Resource & Service Admn 8%, Fulton County Health Center 8%, Georgia Department of Public H 8%, Mental Health & Retardation 8%, AHF Public Health Division 8%

ADDR: Peachtree St NW 36%, Clifton Rd NE 14%, W Peachtree St NW 7%, Cascade Rd SW 7%, Fairburn Rd SW 7%, Park Place South SE 7%, Forsyth St SW 7%, Martin Luther King Jr Dr SW 7%, Lenox Pointe NE 7%

ZIP: 30303 50%, 30331 14%, 30308 7%, 30311 7%, 30329 7%, 30324 7%, 30322 7%

ZIP4: 3142 21%, 3141 7%, 3536 7%, 2662 7%, 3172 7%, 1907 7%, 3045 7%, 4018 7%, 8931 7%, 3674 7%, 7423 7%, 4250 7%

NAICS: 92312004 29%, 92312005 21%, 92312002 21%, 62199921 14%, 92312003 7%, 62111129 7%

NAICS_ALL: 62199921 15%, 92312004, 92112007 8%, 92312005 8%, 92312005, 62419012, 99999005,  8%, 92312004, 92313004, 52411407,  8%, 92312002, 92112007, 62199921 8%, 92312002 8%, 92312005, 99999005 8%, 92312003, 62199921 8%, 92312002, 92112007 8%, 92312004, 92112008 8%, 92312004 8%

SIC: 943102 29%, 943105 21%, 943103 21%, 809907 14%, 943101 7%, 801104 7%

SIC_ALL: 809907 15%, 943102, 912103 8%, 943105 8%, 943105, 832218, 999966, 832251 8%, 943102, 944102, 632401, 999966 8%, 943103, 912103, 809907 8%, 943103 8%, 943105, 999966 8%, 943101, 809907 8%, 943103, 912103 8%, 943102, 912102 8%, 943102 8%

INDUSTRY_DESC: Health Services 15%, State Government-Public Health 8%, Public Health Programs Adminis 8%, Public Health Programs Adminis 8%, State Government-Public Health 8%, County Government-Public Healt 8%, County Government-Public Healt 8%, Public Health Programs Adminis 8%, Federal Government-Public Hlth 8%, County Government-Public Healt 8%, State Government-Public Health 8%, State Government-Public Health 8%

HQNAME: Georgia Department of Public H 100%

PLACETYPE: Independent 71%, Headquarters 21%, Branch 7%

SQFOOTAGE: 2500 - 4999 36%, 100000+ 29%, 20000 - 39999 14%, 10000 - 19999 7%, 5000 - 9999 7%, 1500 - 2499 7%

MIN_SQFT: 2500 36%, 100000 29%, 20000 14%, 10000 7%, 5000 7%, 1500 7%

EMPNUM: 3 29%, 2 14%, 5 14%, 1 7%, 53 7%, 39 7%, 300 7%, 100 7%, 6 7%

SALESVOL: nan 86%, 1339000.0 7%, 502000.0 7%

ESRI_PID: 7a769c79a301b2f4c513efdd72fbab 8%, fad98e8b5156de4d1c14d91153b677 8%, 61aa1e45e6819b539cb8d7d9b19e92 8%, e6600e241b8a7b6a165341bcea078b 8%, 102cfcfbbd077c9cd7c38e31035864 8%, e24cd4725cf9c8657f7b5f75959d96 8%, ce62ff98523c1b6fd153a6102ea858 8%, e647b87da46ed68de2cdffbc062d12 8%, e7c9bd7c614b12211d8771e2eaf47b 8%, 9c0ed3aca4ed73163fa7fa982516a2 8%, 76a983dcdc0ceaee048a43f12f5c02 8%, 23ba86300fca4452a0734fd8b58df3 8%

GEOMETRY: {"type": "Point", "coordinates 29%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 14 | 0 | 14 1; 13 1; 12 1; 11 1 |
| CONAME | category | 14 | 0 | Substance Abuse 1; Xcovid 1; Learn to Grow Inc 1; Georgia Dept of Community 1 |
| ADDR | category | 9 | 0 | Peachtree St NW 5; Clifton Rd NE 2; W Peachtree St NW 1; Cascade Rd SW 1 |
| CITY | who | 1 | 0 | Atlanta 14 |
| STATE_NAME | who | 1 | 0 | Georgia 14 |
| STATE | other | 1 | 0 | GA 14 |
| ZIP | category | 7 | 0 | 30303 7; 30331 2; 30308 1; 30311 1 |
| ZIP4 | category | 12 | 0 | 3142 3; 3141 1; 3536 1; 2662 1 |
| NAICS | category | 6 | 0 | 92312004 4; 92312005 3; 92312002 3; 62199921 2 |
| NAICS_ALL | category | 13 | 0 | 62199921 2; 92312004, 92112007 1; 92312005 1; 92312005, 62419012, 99999 1 |
| SIC | category | 6 | 0 | 943102 4; 943105 3; 943103 3; 809907 2 |
| SIC_ALL | category | 13 | 0 | 809907 2; 943102, 912103 1; 943105 1; 943105, 832218, 999966, 8 1 |
| INDUSTRY_DESC | category | 13 | 0 | Health Services 2; State Government-Public H 1; Public Health Programs Ad 1; Public Health Programs Ad 1 |
| AFFILIATE | empty | 1 | 14 |  |
| BRAND | empty | 1 | 14 |  |
| HQNAME | category | 2 | 13 | Georgia Department of Pub 1 |
| LOC_CONF | who | 1 | 0 | Very High 14 |
| PLACETYPE | category | 3 | 0 | Independent 10; Headquarters 3; Branch 1 |
| SQFOOTAGE | category | 6 | 0 | 2500 - 4999 5; 100000+ 4; 20000 - 39999 2; 10000 - 19999 1 |
| MIN_SQFT | category | 6 | 0 | 2500 5; 100000 4; 20000 2; 10000 1 |
| MAX_SQFT | amount | 6 | 0 | 4999.0 5; nan 4; 39999.0 2; 19999.0 1 |
| EMPNUM | category | 9 | 0 | 3 4; 2 2; 5 2; 1 1 |
| SALESVOL | category | 3 | 0 | nan 12; 1339000.0 1; 502000.0 1 |
| SOURCE | who | 1 | 0 | Data Axle 14 |
| ESRI_PID | category | 14 | 0 | 7a769c79a301b2f4c513efdd7 1; fad98e8b5156de4d1c14d9115 1; 61aa1e45e6819b539cb8d7d9b 1; e6600e241b8a7b6a165341bce 1 |
| DESC | who | 1 | 0 | CONAME, Atlanta, Georgia 14 |
| LATITUDE | amount | 11 | 0 | 33.754166000195085 4; 33.76512799979668 1; 33.731931000187764 1; 33.75416700027488 1 |
| LONGITUDE | amount | 11 | 0 | -84.39064499985699 4; -84.388188999582 1; -84.43912100043467 1; -84.39064650004353 1 |
| CREATIONDATE | date | 1 | 0 | 1738179808754 14 |
| CREATOR | who | 1 | 0 | gpickren2 14 |
| EDITDATE | date | 1 | 0 | 1738179808754 14 |
| EDITOR | who | 1 | 0 | gpickren2 14 |
| GEOMETRY | category | 11 | 0 | {"type": "Point", "coordi 4; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:05.40268 14 |
| SOURCE_RUN_ID | audit | 1 | 0 | dab8540a-dda6-43fb-9f7c-b 14 |
| SRC_SHA256 | who | 1 | 0 | 19c4149518eddd04201087dfe 14 |
