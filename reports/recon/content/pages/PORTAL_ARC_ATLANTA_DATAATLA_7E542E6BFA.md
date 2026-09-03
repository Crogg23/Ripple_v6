# PORTAL_ARC_ATLANTA_DATAATLA_7E542E6BFA

rows 20  columns 36  scan 4.8s

roles: amount 5, audit 2, category 17, date 3, empty 2, other 1, who 7

## when

CREATIONDATE
  2025        20  ##############################

EDITDATE
  2025        20  ##############################

INGESTED_AT
  2026        20  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MIN_SQFT | 15 | 1 | 10.0K | 37.2K | 40.0K | 161.5K |
| MAX_SQFT | 15 | 1.5K | 20.0K | 91.6K | 100.0K | 344.0K |
| SALESVOL | 19 | 109.0K | 1.34M | 6.43M | 6.91M | 36.99M |
| LATITUDE | 20 | 33.65 | 33.77 | 33.86 | 33.86 | 675.41 |
| LONGITUDE | 20 | -84.51 | -84.39 | -84.35 | -84.35 | -1.7K |

## who

STATE_NAME by rows
        20  Georgia

STATE_NAME by dollars
      675.41       20 rows  Georgia

SOURCE by rows
        20  Data Axle

SOURCE by dollars
      675.41       20 rows  Data Axle

DESC by rows
        20  CONAME, Atlanta, Georgia

DESC by dollars
      675.41       20 rows  CONAME, Atlanta, Georgia

CREATOR by rows
        20  gpickren2

CREATOR by dollars
      675.41       20 rows  gpickren2

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2025:675.41

SOURCE by CREATIONDATE, dollars = LATITUDE
  Data Axle                                 2025:675.41

## what

OBJECTID: 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%

CONAME: Piedmont Urgent Care 25%, Concentra Urgent Care 12%, Westside-Med 6%, Viral Solutions-Cascade 6%, MEDICI Urgent Care & Wellness  6%, Acsh Urgent Care of Alabama LL 6%, Acsh Urgent Care of Al LLC 6%, Mordern Internal Medicine Urge 6%, Peachtree Immedidate Care-Edge 6%, Peachtree Immediate Care-Midto 6%, Urgent Care 24/7 Atlanta 6%, Kays Urgent Care Clinic LLC 6%

ADDR: Ponce De Leon Ave NE 13%, Roswell Rd NE 13%, Peachtree Rd NW 13%, Marietta Blvd NW 7%, Benjamin E Mays Dr SW 7%, Grant St SE 7%, Ivan Allen Jr Blvd NW 7%, Peachtree St NE 7%, Martin Luther King Jr Dr SW 7%, Caroline St NE 7%, 14th St NW 7%, Centennial Olympic Park Dr NW 7%

ZIP: 30318 16%, 30309 16%, 30311 11%, 30308 11%, 30306 11%, 30315 5%, 30307 5%, 30313 5%, 30342 5%, 30331 5%, 30312 5%, 30305 5%

ZIP4: 2260 8%, 3242 8%, 2014 8%, 3050 8%, 7694 8%, 1712 8%, 2749 8%, 7963 8%, 1834 8%, 2673 8%, 4212 8%, 4451 8%

NAICS: 62149306 90%, 62111129 5%, 62149803 5%

NAICS_ALL: 62149306 45%, 62149306, 62111107 10%, 62149306, 62111107, 62139923,  5%, 62111129, 62111107, 62149306 5%, 62149803, 62199921, 62111107,  5%, 62149306, 62111107, 52411409 5%, 62149306, 62111107, 62311007,  5%, 62149306, 62111107, 62149803 5%, 62149306, 62111107, 62111129 5%, 62149306, 62111129 5%, 62149306, 62111107, 62134007,  5%

SIC: 809320 90%, 801104 5%, 809307 5%

SIC_ALL: 809320 45%, 809320, 801101 10%, 809320, 801101, 804907, 801104 5%, 801104, 801101, 809320 5%, 809307, 809907, 801101, 809320 5%, 809320, 801101, 632403 5%, 809320, 801101, 805905, 873402 5%, 809320, 801101, 809307 5%, 809320, 801101, 801104 5%, 809320, 801104 5%, 809320, 801101, 804918, 801104 5%

INDUSTRY_DESC: Urgent Medical Care Centers an 45%, Urgent Medical Care Centers an 10%, Urgent Medical Care Centers an 5%, Clinics, Physicians & Surgeons 5%, Minor Medical Centers and Clin 5%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 5%, Urgent Medical Care Centers an 5%

HQNAME: Piedmont Healthcare 50%, Concentra Inc 25%, CRH Healthcare LLC 12%, Wellstar Health System 12%

LOC_CONF: Very High 90%, High 5%, Low 5%

PLACETYPE: Independent 60%, Branch 40%

SQFOOTAGE: 10000 - 19999 27%, 5000 - 9999 20%, 20000 - 39999 20%, 2500 - 4999 13%, 1500 - 2499 7%, 1 - 1499 7%, 40000 - 99999 7%

EMPNUM: 6 21%, 3 21%, 5 11%, 2 5%, 4 5%, 11 5%, 7 5%, 9 5%, 1 5%, 13 5%, 8 5%, 50 5%

ESRI_PID: f9f416c9730c1eeac7a98724bb1e60 8%, 85506ad409ac4e4ad8f9388cfc1fd1 8%, c1855e98238d8976aa1824c5bd1af4 8%, 2a0b46f13db54ebffcc6001dff707a 8%, 35ab5bd237f193e1504c52afe3f8a2 8%, bc8a40ac23c31bd60c7885eabfd41c 8%, 84c8688fb786e40463b5f9af2df348 8%, d0a0e19e7db5b55d8dd39d9dc803e7 8%, c079f2d872304aea3f46564ee7789d 8%, 160191795b4588039972dabc1c8e91 8%, e49347bc7102ab999c39e5bdf8eccf 8%, 5249a28d6b2afd15a1fc5e08e7036b 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 20 | 0 | 20 1; 19 1; 18 1; 17 1 |
| CONAME | category | 16 | 0 | Piedmont Urgent Care 4; Concentra Urgent Care 2; Westside-Med 1; Viral Solutions-Cascade 1 |
| ADDR | category | 17 | 0 | Ponce De Leon Ave NE 2; Roswell Rd NE 2; Peachtree Rd NW 2; Marietta Blvd NW 1 |
| CITY | who | 1 | 0 | Atlanta 20 |
| STATE_NAME | who | 1 | 0 | Georgia 20 |
| STATE | other | 1 | 0 | GA 20 |
| ZIP | category | 13 | 0 | 30318 3; 30309 3; 30311 2; 30308 2 |
| ZIP4 | category | 20 | 1 | 2260 1; 3242 1; 2014 1; 3050 1 |
| NAICS | category | 3 | 0 | 62149306 18; 62111129 1; 62149803 1 |
| NAICS_ALL | category | 11 | 0 | 62149306 9; 62149306, 62111107 2; 62149306, 62111107, 62139 1; 62111129, 62111107, 62149 1 |
| SIC | category | 3 | 0 | 809320 18; 801104 1; 809307 1 |
| SIC_ALL | category | 11 | 0 | 809320 9; 809320, 801101 2; 809320, 801101, 804907, 8 1; 801104, 801101, 809320 1 |
| INDUSTRY_DESC | category | 11 | 0 | Urgent Medical Care Cente 9; Urgent Medical Care Cente 2; Urgent Medical Care Cente 1; Clinics, Physicians & Sur 1 |
| AFFILIATE | empty | 1 | 20 |  |
| BRAND | empty | 1 | 20 |  |
| HQNAME | category | 5 | 12 | Piedmont Healthcare 4; Concentra Inc 2; CRH Healthcare LLC 1; Wellstar Health System 1 |
| LOC_CONF | category | 3 | 0 | Very High 18; High 1; Low 1 |
| PLACETYPE | category | 2 | 0 | Independent 12; Branch 8 |
| SQFOOTAGE | category | 8 | 5 | 10000 - 19999 4; 5000 - 9999 3; 20000 - 39999 3; 2500 - 4999 2 |
| MIN_SQFT | amount | 8 | 0 | nan 5; 10000.0 4; 5000.0 3; 20000.0 3 |
| MAX_SQFT | amount | 8 | 0 | nan 5; 19999.0 4; 9999.0 3; 39999.0 3 |
| EMPNUM | category | 13 | 0 | 6 4; 3 4; 5 2; 2 1 |
| SALESVOL | amount | 19 | 0 | 670000.0 2; 4263000.0 1; 4238000.0 1; 1116000.0 1 |
| SOURCE | who | 1 | 0 | Data Axle 20 |
| ESRI_PID | category | 20 | 0 | f9f416c9730c1eeac7a98724b 1; 85506ad409ac4e4ad8f9388cf 1; c1855e98238d8976aa1824c5b 1; 2a0b46f13db54ebffcc6001df 1 |
| DESC | who | 1 | 0 | CONAME, Atlanta, Georgia 20 |
| LATITUDE | amount | 20 | 0 | 33.816874000273806 1; 33.72318300006842 1; 33.72558900015068 1; 33.76506399986448 1 |
| LONGITUDE | amount | 20 | 0 | -84.44835200025938 1; -84.46363600028376 1; -84.37739500033321 1; -84.38994900044622 1 |
| CREATIONDATE | date | 1 | 0 | 1738179771249 20 |
| CREATOR | who | 1 | 0 | gpickren2 20 |
| EDITDATE | date | 1 | 0 | 1738179771249 20 |
| EDITOR | who | 1 | 0 | gpickren2 20 |
| GEOMETRY | category | 20 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:51.36547 20 |
| SOURCE_RUN_ID | audit | 1 | 0 | e693cb46-47c0-4afe-a973-b 20 |
| SRC_SHA256 | who | 1 | 0 | d757af381e9030663d2094332 20 |
