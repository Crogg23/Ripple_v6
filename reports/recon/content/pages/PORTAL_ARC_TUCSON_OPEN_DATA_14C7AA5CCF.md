# PORTAL_ARC_TUCSON_OPEN_DATA_14C7AA5CCF

rows 19  columns 37  scan 4.6s

roles: amount 4, audit 2, category 18, date 3, empty 1, other 1, who 9

## when

CREATIONDATE
  2025        19  ##############################

EDITDATE
  2025        19  ##############################

INGESTED_AT
  2026        19  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MIN_SQFT | 17 | 2.5K | 20.0K | 100.0K | 100.0K | 622.5K |
| MAX_SQFT | 13 | 5.0K | 20.0K | 100.0K | 100.0K | 505.0K |
| LATITUDE | 19 | 32.18 | 32.22 | 32.26 | 32.26 | 612.08 |
| LONGITUDE | 19 | -111 | -110.95 | -110.90 | -110.90 | -2.1K |

## who

STATE_NAME by rows
        19  Arizona

STATE_NAME by dollars
      612.08       19 rows  Arizona

LOC_CONF by rows
        19  Very High

LOC_CONF by dollars
      612.08       19 rows  Very High

NAICS_SECT by rows
        19  Retail Trade

NAICS_SECT by dollars
      612.08       19 rows  Retail Trade

PLACETYPE by rows
        19  Branch

PLACETYPE by dollars
      612.08       19 rows  Branch

## who x when

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Arizona                                   2025:612.08

LOC_CONF by CREATIONDATE, dollars = LATITUDE
  Very High                                 2025:612.08

## what

OBJECTID: 102 8%, 100 8%, 94 8%, 85 8%, 81 8%, 78 8%, 70 8%, 68 8%, 59 8%, 52 8%, 49 8%, 37 8%

CONAME: Family Dollar 16%, Dollar Tree 16%, Walmart Supercenter 11%, Ross Dress For Less 11%, Burlington 11%, Target 5%, Marshalls 5%, Five Below 5%, Dollar General 5%, dd's DISCOUNTS 5%, Curacao Tucson 5%, Costco Wholesale 5%

ADDR: E Broadway Blvd 26%, E 22 Nd St 21%, E Tucson Marketplace Blvd 11%, E Grant Rd 11%, W Saint Marys Rd 11%, N Campbell Ave 5%, S 6 Th Ave 5%, S 6th Ave 5%, S 16th Ave 5%

ZIP: 85713 37%, 85716 26%, 85719 11%, 85745 11%, 85711 11%, 85705 5%

ZIP4: 5410 15%, 5335 15%, 6508 8%, 5400 8%, 2876 8%, 5706 8%, 2255 8%, 3115 8%, 6112 8%, 2931 8%, 3107 8%

NAICS: 45511001 53%, 45521903 42%, 45521101 5%

NAICS_ALL: 45511001, 44412003, 45511003,  8%, 45511001, 44412003, 44511003,  8%, 45511001, 44511003, 45811034,  8%, 45511001, 45511003, 45811017,  8%, 45511001, 45811041, 45511003,  8%, 45511001, 45511003, 45811041,  8%, 45521903, 45942013, 45942050,  8%, 45521903, 45511003, 45511001,  8%, 45521903, 45811041, 45511001,  8%, 45521903, 45511001, 45511003,  8%, 45521903, 45511003, 45521906 8%, 45521903, 45511003, 45942026,  8%

SIC: 531102 53%, 533101 42%, 531110 5%

SIC_ALL: 531102, 523107, 531104, 564101 8%, 531102, 523107, 541105, 564101 8%, 531102, 541105, 564101, 564103 8%, 531102, 531104, 562101, 561101 8%, 531102, 565101, 531104, 562101 8%, 531102, 531104, 565101, 561103 8%, 533101, 594712, 594748, 594517 8%, 533101, 531104, 531102, 599929 8%, 533101, 565101, 531102, 531104 8%, 533101, 531102, 531104, 599929 8%, 533101, 531104, 533104 8%, 533101, 531104, 594716, 531102 8%

INDUSTRY_DESC: Department Stores, Paint-Retai 8%, Department Stores, Paint-Retai 8%, Department Stores, Grocers-Ret 8%, Department Stores, Retail Shop 8%, Department Stores, Clothing-Re 8%, Department Stores, Retail Shop 8%, Variety Stores, Gift Shops, Gi 8%, Variety Stores, Retail Shops,  8%, Variety Stores, Clothing-Retai 8%, Variety Stores, Department Sto 8%, Variety Stores, Retail Shops,  8%, Variety Stores, Retail Shops,  8%

AFFILIATE: Boost Mobile 100%

HQNAME: Ross Stores, Inc 16%, Family Dollar Stores, Inc 16%, Dollar Tree Stores Inc 16%, Walmart U.S. Division 11%, Burlington Stores, Inc 11%, Target Stores Inc 5%, Marmaxx Group 5%, Five Below, Inc 5%, Dollar General Corporation 5%, Adir International, LLC 5%, Costco Wholesale Corporation 5%

SQFOOTAGE: 100000+ 24%, 5000 - 9999 24%, 20000 - 39999 18%, 40000 - 99999 18%, 10000 - 19999 12%, 2500 - 4999 6%

EMPNUM: 8 13%, 5 13%, 65 13%, 154 7%, 477 7%, 4 7%, 73 7%, 21 7%, 27 7%, 6 7%, 7 7%, 14 7%

SALESVOL: 1487000 13%, 930000 13%, 12285000 13%, 29105000 7%, 90150000 7%, 756000 7%, 13797000 7%, 3969000 7%, 5103000 7%, 1328000 7%, 1302000 7%, 2603000 7%

ESRI_PID: 2ee0fffc4589c1b4e48fcb77935c33 8%, 6c665eac49532575fc6511f30f5f14 8%, 968b9bf32487859e2e970703f1667f 8%, eb8d0a7e2314d5d12ac51ef9514f8e 8%, bfba974f11877ad659c1232693f8e7 8%, 0a4c80c3f1923ec904710b75d794dd 8%, f52b44b3a48a7c02d79d6c565b6cdd 8%, 8fe5a69ffc63f7f280ce0ff995ba8f 8%, a9001532f6ef54aca749c471bc5979 8%, 614e9d314c255f21ff9bba867a4a7a 8%, e2d0d9fbdb7a59a3f29189835b0f7b 8%, 6ab937947318c6da9692b60cce1f08 8%

DESC: Family Dollar, Tucson, Arizona 16%, Dollar Tree, Tucson, Arizona 16%, Walmart Supercenter, Tucson, A 11%, Ross Dress For Less, Tucson, A 11%, Burlington, Tucson, Arizona 11%, Target, Tucson, Arizona 5%, Marshalls, Tucson, Arizona 5%, Five Below, Tucson, Arizona 5%, Dollar General, Tucson, Arizon 5%, dd's DISCOUNTS, Tucson, Arizon 5%, Curacao Tucson, Tucson, Arizon 5%, Costco Wholesale, Tucson, Ariz 5%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 19 | 0 | 102 1; 100 1; 94 1; 85 1 |
| CONAME | category | 12 | 0 | Family Dollar 3; Dollar Tree 3; Walmart Supercenter 2; Ross Dress For Less 2 |
| ADDR | category | 9 | 0 | E Broadway Blvd 5; E 22 Nd St 4; E Tucson Marketplace Blvd 2; E Grant Rd 2 |
| CITY | who | 1 | 0 | Tucson 19 |
| STATE_NAME | who | 1 | 0 | Arizona 19 |
| STATE | other | 1 | 0 | AZ 19 |
| ZIP | category | 6 | 0 | 85713 7; 85716 5; 85719 2; 85745 2 |
| ZIP4 | category | 17 | 1 | 5410 2; 5335 2; 6508 1; 5400 1 |
| NAICS | category | 3 | 0 | 45511001 10; 45521903 8; 45521101 1 |
| NAICS_ALL | category | 19 | 0 | 45511001, 44412003, 45511 1; 45511001, 44412003, 44511 1; 45511001, 44511003, 45811 1; 45511001, 45511003, 45811 1 |
| SIC | category | 3 | 0 | 531102 10; 533101 8; 531110 1 |
| SIC_ALL | category | 19 | 0 | 531102, 523107, 531104, 5 1; 531102, 523107, 541105, 5 1; 531102, 541105, 564101, 5 1; 531102, 531104, 562101, 5 1 |
| INDUSTRY_DESC | category | 19 | 0 | Department Stores, Paint- 1; Department Stores, Paint- 1; Department Stores, Grocer 1; Department Stores, Retail 1 |
| AFFILIATE | category | 2 | 18 | Boost Mobile 1 |
| BRAND | empty | 1 | 19 |  |
| HQNAME | category | 11 | 0 | Ross Stores, Inc 3; Family Dollar Stores, Inc 3; Dollar Tree Stores Inc 3; Walmart U.S. Division 2 |
| LOC_CONF | who | 1 | 0 | Very High 19 |
| NAICS_SECT | who | 1 | 0 | Retail Trade 19 |
| PLACETYPE | who | 1 | 0 | Branch 19 |
| SQFOOTAGE | category | 7 | 2 | 100000+ 4; 5000 - 9999 4; 20000 - 39999 3; 40000 - 99999 3 |
| MIN_SQFT | amount | 7 | 0 | 100000.0 4; 5000.0 4; 20000.0 3; 40000.0 3 |
| MAX_SQFT | amount | 6 | 0 | nan 6; 9999.0 4; 39999.0 3; 99999.0 3 |
| EMPNUM | category | 16 | 0 | 8 2; 5 2; 65 2; 154 1 |
| SALESVOL | category | 16 | 0 | 1487000 2; 930000 2; 12285000 2; 29105000 1 |
| SOURCE | who | 1 | 0 | Data Axle 19 |
| ESRI_PID | category | 19 | 0 | 2ee0fffc4589c1b4e48fcb779 1; 6c665eac49532575fc6511f30 1; 968b9bf32487859e2e970703f 1; eb8d0a7e2314d5d12ac51ef95 1 |
| DESC | category | 12 | 0 | Family Dollar, Tucson, Ar 3; Dollar Tree, Tucson, Ariz 3; Walmart Supercenter, Tucs 2; Ross Dress For Less, Tucs 2 |
| LATITUDE | amount | 18 | 0 | 32.22380700024169 1; 32.185621000345215 1; 32.22309099980118 1; 32.22327399988666 1 |
| LONGITUDE | amount | 19 | 0 | -110.91920099984944 1; -110.95343899961783 1; -110.91511000018033 1; -110.9181849998732 1 |
| CREATIONDATE | date | 1 | 0 | 1743694109000 19 |
| CREATOR | who | 1 | 0 | ehammon1_cotgis 19 |
| EDITDATE | date | 1 | 0 | 1743694109000 19 |
| EDITOR | who | 1 | 0 | ehammon1_cotgis 19 |
| GEOMETRY | category | 19 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:46.41278 19 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0a147e74-84d9-4b4c-89da-5 19 |
| SRC_SHA256 | who | 1 | 0 | bd12ec2973f388afc60e71e35 19 |
