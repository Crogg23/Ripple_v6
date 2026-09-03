# PORTAL_ARC_ATLANTA_DATAATLA_E2C03512E7

rows 42  columns 36  scan 3.7s

roles: amount 5, audit 2, category 17, date 3, empty 2, other 1, who 7

## when

CREATIONDATE
  2025        42  ##############################

EDITDATE
  2025        42  ##############################

INGESTED_AT
  2026        42  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MAX_SQFT | 26 | 1.5K | 20.0K | 100.0K | 100.0K | 1.10M |
| EMPNUM | 35 | 3 | 17 | 3.2K | 3.6K | 8.5K |
| SALESVOL | 35 | 508.0K | 3.12M | 637.14M | 674.30M | 1.72B |
| LATITUDE | 42 | 33.75 | 33.79 | 33.81 | 33.81 | 1.4K |
| LONGITUDE | 42 | -84.41 | -84.39 | -84.32 | -84.32 | -3.5K |

## who

STATE_NAME by rows
        42  Georgia

STATE_NAME by dollars
        1.4K       42 rows  Georgia

SOURCE by rows
        42  Data Axle

SOURCE by dollars
        1.4K       42 rows  Data Axle

DESC by rows
        42  CONAME, Atlanta, Georgia

DESC by dollars
        1.4K       42 rows  CONAME, Atlanta, Georgia

CREATOR by rows
        42  gpickren2

CREATOR by dollars
        1.4K       42 rows  gpickren2

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2025:1.4K

SOURCE by CREATIONDATE, dollars = LATITUDE
  Data Axle                                 2025:1.4K

## what

OBJECTID: 42 8%, 41 8%, 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%

CONAME: Emory University Hospital 19%, Piedmont Atlanta Hospital Outp 12%, Piedmont Atlanta Hospital Slee 12%, Children's Healthcare of Atlan 6%, Piedmont Atlanta Hospital Dori 6%, Emergency Dept, Piedmont Atlan 6%, Emergency Dept, Children's Hea 6%, Emory Clinic at Emory Universi 6%, Winship at Emory University Ho 6%, Piedmont Atlanta Hospital Radi 6%, Piedmont Atlanta Hospital Fuqu 6%, Piedmont Atlanta Hospital Diab 6%

ADDR: Peachtree Rd NW 28%, Clifton Rd NE 22%, Jesse Hill Jr Dr SE 15%, Peachtree St NE 10%, Peachtree Rd NE 8%, Howell Mill Rd NW 2%, Peachtree Road Nw 77 B 2%, Peachtree Road 77 2%, Upper Gate Dr NE 2%, W Peachtree St NW 2%, Piedmont Ave NE 2%, Linden Ave NE 2%

ZIP: 30309 43%, 30322 21%, 30303 14%, 30308 14%, 30318 2%, 30306 2%, 30329 2%

ZIP4: 1281 27%, 2247 10%, 1476 10%, 1465 10%, 1064 10%, 3032 7%, 1062 7%, 1013 7%, 3050 7%, 2212 3%, 2593 3%

NAICS: 62211002 29%, 62199921 21%, 62111107 17%, 62211001 14%, 62111129 14%, 62231007 5%

NAICS_ALL: 62199921 24%, 62211001 20%, 62111107 12%, 62111129 8%, 62211002, 62211001 8%, 62111107, 62111129 4%, 62211001, 62111129 4%, 62111129, 62111107 4%, 62111129, 62211003 4%, 62199921, 62111107, 62111129 4%, 62231007, 62111107, 62111129,  4%, 62231007, 81331908, 62431009,  4%

SIC: 806202 29%, 809907 21%, 801101 17%, 806203 14%, 801104 14%, 806998 5%

SIC_ALL: 809907 24%, 806203 20%, 801101 12%, 801104 8%, 806202, 806203 8%, 801101, 801104 4%, 806203, 801104 4%, 801104, 801101 4%, 801104, 806201 4%, 809907, 801101, 801104 4%, 806998, 801101, 801104, 833102 4%, 806998, 839998, 833102, 873304 4%

INDUSTRY_DESC: Health Services 24%, Emergency Medical & Surgical S 20%, Physicians & Surgeons 12%, Clinics 8%, Hospitals, Emergency Medical & 8%, Physicians & Surgeons, Clinics 4%, Emergency Medical & Surgical S 4%, Clinics, Physicians & Surgeons 4%, Clinics, Medical Centers 4%, Health Services, Physicians &  4%, Specialty Hospitals-Except Psy 4%, Specialty Hospitals-Except Psy 4%

HQNAME: Piedmont Atlanta 33%, Emory Healthcare Network 15%, Emory University Hospital 12%, Children's Healthcare of Atlan 9%, Emory University Hospital Midt 9%, Shepherd Center Inc 6%, Children's Healthcare of Atlan 3%, Children's Healthcare Egleston 3%, Emory University 3%, Grady Memorial Hospital 3%, Select Medical Corporation 3%

LOC_CONF: Very High 90%, High 7%, Low 2%

PLACETYPE: Branch 62%, Headquarters 24%, Independent 14%

SQFOOTAGE: 100000+ 38%, 40000 - 99999 21%, 1 - 1499 17%, 20000 - 39999 7%, 5000 - 9999 5%, 2500 - 4999 5%, 10000 - 19999 5%, 1500 - 2499 2%

MIN_SQFT: 100000 38%, 40000 21%, 1 17%, 20000 7%, 5000 5%, 2500 5%, 10000 5%, 1500 2%

ESRI_PID: 87f9b96d398b01504b5e904a8f5b88 8%, 82704d791a30531d2178402d689f58 8%, 44737e312ee18e1b25051baff50e9d 8%, 7af5acef2130f6da84abce1801484f 8%, b65c0752888d7cf778711798435644 8%, 05993a8268514907766cb169176413 8%, ca18a52cdfd96f1827f27aaefc1171 8%, 5f86d5446eaf8bb3fb92c325da14d4 8%, 0b6efa1a6c6190fe7d850a081ed7fb 8%, 787503b28a2a66230b961f60e1da24 8%, c300037703564f7a8163d7d55d67b2 8%, a986194dd3e2986516351275122d8d 8%

GEOMETRY: {"type": "Point", "coordinates 25%, {"type": "Point", "coordinates 12%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 6%, {"type": "Point", "coordinates 6%, {"type": "Point", "coordinates 6%, {"type": "Point", "coordinates 6%, {"type": "Point", "coordinates 3%, {"type": "Point", "coordinates 3%, {"type": "Point", "coordinates 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 42 | 0 | 42 1; 41 1; 40 1; 39 1 |
| CONAME | category | 37 | 0 | Emory University Hospital 3; Piedmont Atlanta Hospital 2; Piedmont Atlanta Hospital 2; Children's Healthcare of  1 |
| ADDR | category | 14 | 0 | Peachtree Rd NW 11; Clifton Rd NE 9; Jesse Hill Jr Dr SE 6; Peachtree St NE 4 |
| CITY | who | 1 | 0 | Atlanta 42 |
| STATE_NAME | who | 1 | 0 | Georgia 42 |
| STATE | other | 1 | 0 | GA 42 |
| ZIP | category | 7 | 0 | 30309 18; 30322 9; 30303 6; 30308 6 |
| ZIP4 | category | 20 | 4 | 1281 8; 2247 3; 1476 3; 1465 3 |
| NAICS | category | 6 | 0 | 62211002 12; 62199921 9; 62111107 7; 62211001 6 |
| NAICS_ALL | category | 29 | 0 | 62199921 6; 62211001 5; 62111107 3; 62111129 2 |
| SIC | category | 6 | 0 | 806202 12; 809907 9; 801101 7; 806203 6 |
| SIC_ALL | category | 29 | 0 | 809907 6; 806203 5; 801101 3; 801104 2 |
| INDUSTRY_DESC | category | 29 | 0 | Health Services 6; Emergency Medical & Surgi 5; Physicians & Surgeons 3; Clinics 2 |
| AFFILIATE | empty | 1 | 42 |  |
| BRAND | empty | 1 | 42 |  |
| HQNAME | category | 14 | 7 | Piedmont Atlanta 11; Emory Healthcare Network 5; Emory University Hospital 4; Children's Healthcare of  3 |
| LOC_CONF | category | 3 | 0 | Very High 38; High 3; Low 1 |
| PLACETYPE | category | 3 | 0 | Branch 26; Headquarters 10; Independent 6 |
| SQFOOTAGE | category | 8 | 0 | 100000+ 16; 40000 - 99999 9; 1 - 1499 7; 20000 - 39999 3 |
| MIN_SQFT | category | 8 | 0 | 100000 16; 40000 9; 1 7; 20000 3 |
| MAX_SQFT | amount | 8 | 0 | nan 16; 99999.0 9; 1499.0 7; 39999.0 3 |
| EMPNUM | amount | 25 | 0 | nan 7; 19.0 4; 10.0 3; 4.0 3 |
| SALESVOL | amount | 32 | 0 | nan 7; 4197000.0 2; 762000.0 2; 3558000.0 2 |
| SOURCE | who | 1 | 0 | Data Axle 42 |
| ESRI_PID | category | 42 | 0 | 87f9b96d398b01504b5e904a8 1; 82704d791a30531d2178402d6 1; 44737e312ee18e1b25051baff 1; 7af5acef2130f6da84abce180 1 |
| DESC | who | 1 | 0 | CONAME, Atlanta, Georgia 42 |
| LATITUDE | amount | 22 | 0 | 33.80998999980422 8; 33.76895100019894 4; 33.808856000373005 3; 33.8104979996309 3 |
| LONGITUDE | amount | 22 | 0 | -84.39584799976178 8; -84.38628800004909 4; -84.39248799966357 3; -84.39380099974072 3 |
| CREATIONDATE | date | 1 | 0 | 1738179764295 42 |
| CREATOR | who | 1 | 0 | gpickren2 42 |
| EDITDATE | date | 1 | 0 | 1738179764295 42 |
| EDITOR | who | 1 | 0 | gpickren2 42 |
| GEOMETRY | category | 22 | 0 | {"type": "Point", "coordi 8; {"type": "Point", "coordi 4; {"type": "Point", "coordi 3; {"type": "Point", "coordi 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:05.60995 42 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8d1ab6a3-4b08-452e-957c-9 42 |
| SRC_SHA256 | who | 1 | 0 | 448dc74db2c647ed7d9f7d9ed 42 |
