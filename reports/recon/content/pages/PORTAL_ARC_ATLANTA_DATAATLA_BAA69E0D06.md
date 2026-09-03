# PORTAL_ARC_ATLANTA_DATAATLA_BAA69E0D06

rows 51  columns 36  scan 4.6s

roles: amount 5, audit 2, category 18, date 3, empty 2, other 2, who 5

## when

CREATIONDATE
  2025        51  ##############################

EDITDATE
  2025        51  ##############################

INGESTED_AT
  2026        51  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MIN_SQFT | 35 | 1 | 10.0K | 79.6K | 100.0K | 636.5K |
| MAX_SQFT | 34 | 1.5K | 20.0K | 100.0K | 100.0K | 1.19M |
| SALESVOL | 45 | 139.0K | 1.78M | 6.81M | 6.91M | 98.81M |
| LATITUDE | 51 | 33.54 | 33.82 | 34.10 | 34.10 | 1.7K |
| LONGITUDE | 51 | -84.58 | -84.38 | -84.20 | -84.18 | -4.3K |

## who

STATE_NAME by rows
        51  Georgia

STATE_NAME by dollars
        1.7K       51 rows  Georgia

SOURCE by rows
        51  Data Axle

SOURCE by dollars
        1.7K       51 rows  Data Axle

CREATOR by rows
        51  gpickren2

CREATOR by dollars
        1.7K       51 rows  gpickren2

EDITOR by rows
        51  gpickren2

EDITOR by dollars
        1.7K       51 rows  gpickren2

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2025:1.7K

SOURCE by CREATIONDATE, dollars = LATITUDE
  Data Axle                                 2025:1.7K

## what

CONAME: Piedmont Urgent Care 32%, Concentra Urgent Care 23%, Wellstar Urgent Care 13%, GoHealth Urgent Care 6%, Westside-Med 3%, Wellstar Intensivists 3%, Viral Solutions-Roswell 3%, Viral Solutions-Cascade 3%, Nauc 3%, Essential Screening-Supl SLTNS 3%, American Family Care Roswell 3%, MEDICI Urgent Care & Wellness  3%

ADDR: Roswell Rd 18%, W Crossville Rd 9%, Holcomb Bridge Rd 9%, Crabapple Rd 9%, Ponce De Leon Ave NE 9%, Roswell Rd NE 9%, Peachtree Rd NW 9%, Glenridge Connector 9%, Marietta Blvd NW 5%, Hospital Blvd 5%, Benjamin E Mays Dr SW 5%, Norman Berry Dr 5%

CITY: Atlanta 45%, Alpharetta 16%, Roswell 14%, Sandy Springs 8%, Hapeville 6%, East Point 4%, College Park 2%, Fairburn 2%, Duluth 2%, Milton 2%

ZIP: 30075 15%, 30022 10%, 30328 10%, 30354 10%, 30318 8%, 30344 8%, 30309 8%, 30342 8%, 30004 8%, 30311 5%, 30308 5%, 30009 5%

ZIP4: 6812 15%, 4758 15%, 2260 8%, 0001 8%, 7502 8%, 3242 8%, 5121 8%, 2205 8%, 2014 8%, 3050 8%, 7694 8%

NAICS: 62149306 92%, 54161110 4%, 62111129 2%, 54194009 2%

NAICS_ALL: 62149306 46%, 62149306, 62111107 16%, 62149306, 62111107, 62111129 5%, 62149306, 62111129 5%, 62149306, 62149803 5%, 62149306, 62111107, 62134007,  5%, 62149306, 62111107, 62139923,  3%, 62149306, 62211003, 62111117,  3%, 62149306, 45521908 3%, 62111129, 62111107, 62149306 3%, 62149306, 62134006, 62149803 3%, 62149306, 62111107, 52411409 3%

SIC: 809320 92%, 874242 4%, 801104 2%, 074201 2%

SIC_ALL: 809320 46%, 809320, 801101 16%, 809320, 801101, 801104 5%, 809320, 801104 5%, 809320, 809307 5%, 809320, 801101, 804918, 801104 5%, 809320, 801101, 804907, 801104 3%, 809320, 806201, 801138, 801104 3%, 809320, 539901 3%, 801104, 801101, 809320 3%, 809320, 804911, 809307 3%, 809320, 801101, 632403 3%

INDUSTRY_DESC: Urgent Medical Care Centers an 46%, Urgent Medical Care Centers an 16%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 3%, Urgent Medical Care Centers an 3%, Urgent Medical Care Centers an 3%, Clinics, Physicians & Surgeons 3%, Urgent Medical Care Centers an 3%, Urgent Medical Care Centers an 3%

HQNAME: Piedmont Healthcare 37%, Concentra Inc 23%, Wellstar Health System 17%, CRH Healthcare LLC 13%, American Family Care 3%, Petfolk, Inc 3%, TPG Inc 3%

LOC_CONF: Very High 96%, Low 2%, High 2%

PLACETYPE: Branch 57%, Independent 39%, Headquarters 4%

SQFOOTAGE: 20000 - 39999 26%, 10000 - 19999 23%, 40000 - 99999 17%, 5000 - 9999 14%, 2500 - 4999 11%, 100000+ 3%, 1500 - 2499 3%, 1 - 1499 3%

EMPNUM: 3 16%, 6 16%, 15 14%, 5 12%, 9 7%, 4 7%, 10 7%, 8 5%, 7 5%, 30 5%, 12 5%, 2 2%

ESRI_PID: f9f416c9730c1eeac7a98724bb1e60 8%, 78aada32b217e86d7d79c658562782 8%, 6d5afb52de0c80f3d9747763256785 8%, 85506ad409ac4e4ad8f9388cfc1fd1 8%, 133e41d200b9a9b2e15ec1504e2c88 8%, 33a8d51394bb2ec611dcb344431c0a 8%, ec4fc1eb0de0dbb929ae6373fe1934 8%, c1855e98238d8976aa1824c5bd1af4 8%, 2a0b46f13db54ebffcc6001dff707a 8%, 35ab5bd237f193e1504c52afe3f8a2 8%, 0c1030717d9ee947cbdad34a72924f 8%, bc8a40ac23c31bd60c7885eabfd41c 8%

DESC: CONAME, Atlanta, Georgia 45%, CONAME, Alpharetta, Georgia 16%, CONAME, Roswell, Georgia 14%, CONAME, Sandy Springs, Georgia 8%, CONAME, Hapeville, Georgia 6%, CONAME, East Point, Georgia 4%, CONAME, College Park, Georgia 2%, CONAME, Fairburn, Georgia 2%, CONAME, Duluth, Georgia 2%, CONAME, Milton, Georgia 2%

GEOMETRY: {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 51 | 0 | 51 1; 50 1; 49 1; 48 1 |
| CONAME | category | 32 | 0 | Piedmont Urgent Care 10; Concentra Urgent Care 7; Wellstar Urgent Care 4; GoHealth Urgent Care 2 |
| ADDR | category | 41 | 0 | Roswell Rd 4; W Crossville Rd 2; Holcomb Bridge Rd 2; Crabapple Rd 2 |
| CITY | category | 10 | 0 | Atlanta 23; Alpharetta 8; Roswell 7; Sandy Springs 4 |
| STATE_NAME | who | 1 | 0 | Georgia 51 |
| STATE | other | 1 | 0 | GA 51 |
| ZIP | category | 23 | 0 | 30075 6; 30022 4; 30328 4; 30354 4 |
| ZIP4 | category | 46 | 4 | 6812 2; 4758 2; 2260 1; 0001 1 |
| NAICS | category | 4 | 0 | 62149306 47; 54161110 2; 62111129 1; 54194009 1 |
| NAICS_ALL | category | 26 | 0 | 62149306 17; 62149306, 62111107 6; 62149306, 62111107, 62111 2; 62149306, 62111129 2 |
| SIC | category | 4 | 0 | 809320 47; 874242 2; 801104 1; 074201 1 |
| SIC_ALL | category | 26 | 0 | 809320 17; 809320, 801101 6; 809320, 801101, 801104 2; 809320, 801104 2 |
| INDUSTRY_DESC | category | 26 | 0 | Urgent Medical Care Cente 17; Urgent Medical Care Cente 6; Urgent Medical Care Cente 2; Urgent Medical Care Cente 2 |
| AFFILIATE | empty | 1 | 51 |  |
| BRAND | empty | 1 | 51 |  |
| HQNAME | category | 8 | 21 | Piedmont Healthcare 11; Concentra Inc 7; Wellstar Health System 5; CRH Healthcare LLC 4 |
| LOC_CONF | category | 3 | 0 | Very High 49; Low 1; High 1 |
| PLACETYPE | category | 3 | 0 | Branch 29; Independent 20; Headquarters 2 |
| SQFOOTAGE | category | 9 | 16 | 20000 - 39999 9; 10000 - 19999 8; 40000 - 99999 6; 5000 - 9999 5 |
| MIN_SQFT | amount | 9 | 0 | nan 16; 20000.0 9; 10000.0 8; 40000.0 6 |
| MAX_SQFT | amount | 8 | 0 | nan 17; 39999.0 9; 19999.0 8; 99999.0 6 |
| EMPNUM | category | 20 | 0 | 3 7; 6 7; 15 6; 5 5 |
| SALESVOL | amount | 32 | 0 | nan 6; 2073000.0 4; 415000.0 3; 670000.0 3 |
| SOURCE | who | 1 | 0 | Data Axle 51 |
| ESRI_PID | category | 50 | 0 | f9f416c9730c1eeac7a98724b 1; 78aada32b217e86d7d79c6585 1; 6d5afb52de0c80f3d97477632 1; 85506ad409ac4e4ad8f9388cf 1 |
| DESC | category | 10 | 0 | CONAME, Atlanta, Georgia 23; CONAME, Alpharetta, Georg 8; CONAME, Roswell, Georgia 7; CONAME, Sandy Springs, Ge 4 |
| LATITUDE | amount | 49 | 0 | 33.99461499985777 2; 33.90406799971364 2; 33.816874000273806 1; 34.06171600028111 1 |
| LONGITUDE | amount | 49 | 0 | -84.28099000042236 2; -84.35997600042418 2; -84.44835200025938 1; -84.32044600016418 1 |
| CREATIONDATE | date | 1 | 0 | 1738179779009 51 |
| CREATOR | who | 1 | 0 | gpickren2 51 |
| EDITDATE | date | 1 | 0 | 1738179779009 51 |
| EDITOR | who | 1 | 0 | gpickren2 51 |
| GEOMETRY | category | 49 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:17.95378 51 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1be23b8a-ad96-4f1a-ad9d-0 51 |
| SRC_SHA256 | who | 1 | 0 | 77b77eb4b201d50c103470f15 51 |
