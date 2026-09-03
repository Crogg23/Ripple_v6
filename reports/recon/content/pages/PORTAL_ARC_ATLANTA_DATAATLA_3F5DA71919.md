# PORTAL_ARC_ATLANTA_DATAATLA_3F5DA71919

rows 58  columns 35  scan 3.4s

roles: amount 5, audit 2, category 13, date 3, empty 2, other 5, who 6

## when

CREATIONDATE
  2024        58  ##############################

EDITDATE
  2024        58  ##############################

INGESTED_AT
  2026        58  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MIN_SQFT | 57 | 1.5K | 2.5K | 66.4K | 100.0K | 629.5K |
| MAX_SQFT | 56 | 2.5K | 5.0K | 100.0K | 100.0K | 1.17M |
| SALESVOL | 48 | 82.0K | 245.0K | 7.62M | 11.11M | 30.87M |
| LATITUDE | 58 | 33.60 | 33.75 | 33.82 | 33.82 | 2.0K |
| LONGITUDE | 58 | -84.64 | -84.39 | -84.19 | -84.19 | -4.9K |

## who

CONAME by rows
         2  Atlanta Bass Recreation Center
         2  South Cobb Recreation Center
         1  Hamilton Recreation Center
         1  Atlanta City Government Recreation Center
         1  Milam Tennis Courts
         1  City of Atlanta Facility
         1  C A Scott Recreation Center
         1  Martin Luther King Jr Recreation Center & Aquatic Center
         1  Tobie Grant Recreation Center
         1  Brownwood Recreation Center
         1  Clayton County Recreation Center FCLTS
         1  City of Decatur
         1  Central Park Recreation Center
         1  Hoyt Smith Center
         1  Sandtown Park Recreation Center
         1  Fulton County Government
         1  Collier Heights Recreation Center
         1  N H Scott Recreation Center
         1  Mason Mill Recreation Center
         1  Ben Hill Tigertrack Club

CONAME by dollars
       67.60        2 rows  South Cobb Recreation Center
       67.52        2 rows  Atlanta Bass Recreation Center
       33.82        1 rows  Peachtree Hills Recreation Center
       33.81        1 rows  Mason Mill Recreation Center
       33.81        1 rows  Milam Tennis Courts
       33.80        1 rows  Tobie Grant Recreation Center
       33.80        1 rows  Emory Student Activity & Academic Center
       33.80        1 rows  Morningside Recreation Center
       33.80        1 rows  Ismali Center Headquarters
       33.79        1 rows  A D Williams Recreation Center
       33.79        1 rows  Hamilton Recreation Center
       33.79        1 rows  Claremont Student Activity & Academic Center
       33.78        1 rows  Georgia Tech Campus Recreation Center
       33.78        1 rows  Buzy Beez Blingz 'n Thingz
       33.77        1 rows  Decatur Recreation Department
       33.77        1 rows  City of Decatur
       33.77        1 rows  Central Park Recreation Center
       33.77        1 rows  Collier Heights Recreation Center
       33.76        1 rows  Martin Luther King Jr Rec Center
       33.76        1 rows  Bessie Branham Recreation Center

STATE_NAME by rows
        58  Georgia

STATE_NAME by dollars
        2.0K       58 rows  Georgia

SOURCE by rows
        58  Data Axle

SOURCE by dollars
        2.0K       58 rows  Data Axle

CREATOR by rows
        58  gpickren2

CREATOR by dollars
        2.0K       58 rows  gpickren2

## who x when

CONAME by CREATIONDATE, dollars = LATITUDE
  A D Williams Recreation Center            2024:33.79
  Atlanta Bass Recreation Center            2024:67.52
  Atlanta City Government Recreation Cente  2024:33.76
  Ben Hill Tigertrack Club                  2024:33.69
  Brownwood Recreation Center               2024:33.74
  Buzy Beez Blingz 'n Thingz                2024:33.78
  C A Scott Recreation Center               2024:33.75
  Central Park Recreation Center            2024:33.77
  City of Atlanta Facility                  2024:33.74
  City of Decatur                           2024:33.77
  Claremont Student Activity & Academic Ce  2024:33.79
  Clayton County Recreation Center FCLTS    2024:33.60
  Collier Heights Recreation Center         2024:33.77
  Decatur Recreation Department             2024:33.77
  Emory Student Activity & Academic Center  2024:33.80
  Fulton County Government                  2024:33.74
  Georgia Tech Campus Recreation Center     2024:33.78
  Hamilton Recreation Center                2024:33.79
  Hoyt Smith Center                         2024:33.66
  Ismali Center Headquarters                2024:33.80
  Martin Luther King Jr Rec Center          2024:33.76
  Martin Luther King Jr Recreation Center   2024:33.75
  Mason Mill Recreation Center              2024:33.81
  Milam Tennis Courts                       2024:33.81
  Morningside Recreation Center             2024:33.80
  N H Scott Recreation Center               2024:33.72
  Peachtree Hills Recreation Center         2024:33.82
  Sandtown Park Recreation Center           2024:33.70
  South Cobb Recreation Center              2024:67.60
  Tobie Grant Recreation Center             2024:33.80

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2024:2.0K

## what

CITY: Atlanta 69%, Decatur 12%, Scottdale 3%, Morrow 2%, Austell 2%, Mableton 2%, Clarkston 2%, Forest Park 2%, Lithia Springs 2%, Lithonia 2%, College Park 2%, Stockbridge 2%

ZIP: 30331 13%, 30312 13%, 30310 11%, 30314 11%, 30311 11%, 30317 8%, 30033 8%, 30337 5%, 30315 5%, 30079 5%, 30354 5%, 30316 5%

ZIP4: 4013 13%, 2223 13%, 2530 13%, 1822 13%, 1705 7%, 0001 7%, 3731 7%, 1900 7%, 1927 7%, 3801 7%, 5613 7%

NAICS: 71394015 86%, 71219004 7%, 61131013 2%, 23622047 2%, 62411006 2%, 81341004 2%

NAICS_ALL: 71394015 78%, 71394015, 71394020 5%, 71219004 3%, 71219004, 71394015, 71399002 2%, 61131013 2%, 71219004, 71394015 2%, 23622047 2%, 62411006, 81331908 2%, 81341004 2%, 71394015, 92112006, 92119001,  2%, 71394015, 71219004, 92112006 2%

SIC: 799701 86%, 799951 7%, 822113 2%, 154227 2%, 832222 2%, 864108 2%

SIC_ALL: 799701 78%, 799701, 799969 5%, 799951 3%, 799951, 799701, 799999 2%, 822113 2%, 799951, 799701 2%, 154227 2%, 832222, 839998 2%, 864108 2%, 799701, 912104, 919904, 912101 2%, 799701, 799951, 912104 2%

HQNAME: Georgia Institute of Technolog 100%

LOC_CONF: Very High 79%, High 19%, Low 2%

PLACETYPE: Independent 98%, Branch 2%

SQFOOTAGE: 2500 - 4999 37%, 10000 - 19999 16%, 1500 - 2499 14%, 5000 - 9999 12%, 40000 - 99999 11%, 20000 - 39999 9%, 100000+ 2%

EMPNUM: 4 31%, 3 17%, 6 10%, 5 8%, 2 8%, 13 6%, 15 6%, 10 6%, 7 4%, 21 2%, 25 2%, 11 2%

DESC: CONAME, Atlanta, Georgia 69%, CONAME, Decatur, Georgia 12%, CONAME, Scottdale, Georgia 3%, CONAME, Morrow, Georgia 2%, CONAME, Austell, Georgia 2%, CONAME, Mableton, Georgia 2%, CONAME, Clarkston, Georgia 2%, CONAME, Forest Park, Georgia 2%, CONAME, Lithia Springs, Georgi 2%, CONAME, Lithonia, Georgia 2%, CONAME, College Park, Georgia 2%, CONAME, Stockbridge, Georgia 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 58 | 0 | 59 1; 58 1; 57 1; 56 1 |
| CONAME | who | 56 | 0 | Atlanta Bass Recreation C 2; South Cobb Recreation Cen 2; Wayman & Bessie Brady Rec 1; Georgia Tech Campus Recre 1 |
| ADDR | other | 53 | 0 | Oakland Dr SW 2; Martin Luther King Jr Dr  2; Windsor St SW 2; Brownwood Ave SE 2 |
| CITY | category | 12 | 0 | Atlanta 40; Decatur 7; Scottdale 2; Morrow 1 |
| STATE_NAME | who | 1 | 0 | Georgia 58 |
| STATE | other | 1 | 0 | GA 58 |
| ZIP | category | 31 | 0 | 30331 5; 30312 5; 30310 4; 30314 4 |
| ZIP4 | category | 47 | 6 | 4013 2; 2223 2; 2530 2; 1822 2 |
| NAICS | category | 5 | 0 | 71394015 50; 71219004 4; 61131013 1; 23622047 1 |
| NAICS_ALL | category | 10 | 0 | 71394015 45; 71394015, 71394020 3; 71219004 2; 71219004, 71394015, 71399 1 |
| SIC | category | 6 | 0 | 799701 50; 799951 4; 822113 1; 154227 1 |
| SIC_ALL | category | 11 | 0 | 799701 45; 799701, 799969 3; 799951 2; 799951, 799701, 799999 1 |
| AFFILIATE | empty | 1 | 58 |  |
| BRAND | empty | 1 | 58 |  |
| HQNAME | category | 2 | 57 | Georgia Institute of Tech 1 |
| LOC_CONF | category | 3 | 0 | Very High 46; High 11; Low 1 |
| PLACETYPE | category | 2 | 0 | Independent 57; Branch 1 |
| SQFOOTAGE | category | 8 | 1 | 2500 - 4999 21; 10000 - 19999 9; 1500 - 2499 8; 5000 - 9999 7 |
| MIN_SQFT | amount | 8 | 0 | 2500.0 21; 10000.0 9; 1500.0 8; 5000.0 7 |
| MAX_SQFT | amount | 7 | 0 | 4999.0 21; 19999.0 9; 2499.0 8; 9999.0 7 |
| EMPNUM | category | 18 | 0 | 4 16; 3 9; 6 5; 5 4 |
| SALESVOL | amount | 24 | 0 | nan 10; 245000.0 10; 164000.0 6; 184000.0 4 |
| SOURCE | who | 1 | 0 | Data Axle 58 |
| ESRI_PID | other | 58 | 0 | 69f595c6a8a2b59ae8881c6ef 1; 11b269c9d54c86f17c98953cd 1; 0b4a66fb66211f1b5f343c0df 1; a61816558d7a7e3aced8bfa7c 1 |
| DESC | category | 12 | 0 | CONAME, Atlanta, Georgia 40; CONAME, Decatur, Georgia 7; CONAME, Scottdale, Georgi 2; CONAME, Morrow, Georgia 1 |
| LATITUDE | amount | 53 | 0 | 33.719266000228764 2; 33.753656999902034 2; 33.741254999884184 2; 33.73766099981426 2 |
| LONGITUDE | amount | 53 | 0 | -84.42925100020226 2; -84.4397440000505 2; -84.3996980003048 2; -84.34831049970418 2 |
| CREATIONDATE | date | 1 | 0 | 1724425870152 58 |
| CREATOR | who | 1 | 0 | gpickren2 58 |
| EDITDATE | date | 1 | 0 | 1724425870152 58 |
| EDITOR | who | 1 | 0 | gpickren2 58 |
| GEOMETRY | other | 52 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:44.81137 58 |
| SOURCE_RUN_ID | audit | 1 | 0 | 60a24a7c-e604-4b00-b9f4-1 58 |
| SRC_SHA256 | who | 1 | 0 | 347ad9231d403efd740f962d7 58 |
