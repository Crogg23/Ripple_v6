# PORTAL_ARC_ATLANTA_DATAATLA_E1F71F6EE6

rows 544  columns 47  scan 4.6s

roles: amount 4, audit 2, category 21, date 1, empty 3, other 9, who 8

## when

INGESTED_AT
  2026       544  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EMPNUM | 542 | 1 | 3 | 70.90 | 205 | 4.1K |
| SALESVOL | 19 | 159.0K | 997.0K | 3.75M | 3.98M | 21.28M |
| LATITUDE | 544 | 33.65 | 33.75 | 33.87 | 33.88 | 18.4K |
| LONGITUDE | 544 | -84.54 | -84.40 | -84.31 | -84.29 | -45.9K |

## who

CONAME by rows
         7  Church's Texas Chicken
         3  New Shield of Faith Christian Ministries Inc
         3  Faith By Hearing Christian Center
         2  National Church Residences
         2  The Catholic Shrine of the Immaculate Conception
         2  Purpose Center Christian Church
         2  Christ Church of Atlanta
         2  Mount Olive Baptist Church
         2  First Christian Community Church
         2  Faith Development Christian
         2  Beleivers Bible Christian Church
         2  Faith Temple Christian Church
         2  Chapel of Christian Love
         2  Mount Nebo Baptist Church
         2  Central Christian Church
         2  River Of Life Christian Center
         2  Zoe Christian Fellowship
         2  The Universal Church
         2  Ben Hill Christian Church
         2  Springdale Christian Church

CONAME by dollars
      236.04        7 rows  Church's Texas Chicken
      101.28        3 rows  Faith By Hearing Christian Center
      101.16        3 rows  New Shield of Faith Christian Ministries Inc
       67.68        2 rows  Christ Church of Atlanta
       67.62        2 rows  Zoe Christian Fellowship
       67.60        2 rows  Peachtree Christian Church
       67.58        2 rows  First Christian Community Church
       67.56        2 rows  Atlanta Christian CHR-Downtown
       67.54        2 rows  New Jerusalem Baptist Church
       67.54        2 rows  Westminster Christian Fellowship
       67.52        2 rows  Redeeming Love Christian Ministries
       67.52        2 rows  Living in Faith Everyday
       67.52        2 rows  River Of Life Christian Center
       67.52        2 rows  The Universal Church
       67.50        2 rows  The Catholic Shrine of the Immaculate Conception
       67.49        2 rows  The Church of Jesus Christ of Latter-Day Saints
       67.49        2 rows  Kingdom Hall of Jehovah's Witnesses
       67.48        2 rows  Pathway Christian Church
       67.46        2 rows  Rehoboth Family Christian Church
       67.46        2 rows  In the Bible Christian Ministry

STATE_NAME by rows
       544  Georgia

STATE_NAME by dollars
       18.4K      544 rows  Georgia

ADDR by rows
        18  Campbellton Rd SW
        15  Martin Luther King Jr Dr SW
        11  Donald Lee Hollowell Pkwy NW
        11  Peachtree Rd NE
        11  Cascade Rd SW
        10  Peachtree St NE
         9  Fairburn Rd SW
         8  Ponce de Leon Ave NE
         8  Joseph E Boone Blvd NW
         7  Hollywood Rd NW
         7  Metropolitan Pkwy SW
         7  Ralph David Abernathy Blvd SW
         6  Springdale Rd SW
         6  Hamilton E Holmes Dr NW
         6  Memorial Dr SE
         6  Northside Dr NW
         6  Moreland Ave SE
         5  Boulevard NE
         5  Bolton Rd NW
         5  Jonesboro Rd SE

ADDR by dollars
      606.56       18 rows  Campbellton Rd SW
      506.29       15 rows  Martin Luther King Jr Dr SW
      372.24       11 rows  Peachtree Rd NE
      371.54       11 rows  Donald Lee Hollowell Pkwy NW
      370.98       11 rows  Cascade Rd SW
      337.77       10 rows  Peachtree St NE
      303.34        9 rows  Fairburn Rd SW
      270.19        8 rows  Ponce de Leon Ave NE
      270.08        8 rows  Joseph E Boone Blvd NW
      236.54        7 rows  Hollywood Rd NW
      236.18        7 rows  Ralph David Abernathy Blvd SW
      235.89        7 rows  Metropolitan Pkwy SW
      203.03        6 rows  Northside Dr NW
      202.59        6 rows  Hamilton E Holmes Dr NW
      202.50        6 rows  Memorial Dr SE
      202.43        6 rows  Moreland Ave SE
      202.16        6 rows  Springdale Rd SW
      168.96        5 rows  Bolton Rd NW
      168.81        5 rows  Joseph E Lowery Blvd NW
      168.81        5 rows  Boulevard NE

NAICS_ALL by rows
       409  81311008
         8  81311008, 81311021
         7  72251117, 72251301
         6  81311021
         5  81311008, 81311023
         5  81311015
         4  81311026
         3  81311026, 81311041
         3  81311008, 81331908
         3  81311021, 81311008
         3  61111007, 61111004
         2  81341018
         2  81311008, 54161203
         2  81311008, 99999005
         2  81311008, 81311006, 81311026, 81311032
         2  81311008, 81311006
         2  81311008, 81311009
         2  81311006, 81311026
         2  81311008, 45921005
         2  81311008, 62441006

NAICS_ALL by dollars
       13.8K      409 rows  81311008
      270.17        8 rows  81311008, 81311021
      236.04        7 rows  72251117, 72251301
      202.29        6 rows  81311021
      168.78        5 rows  81311008, 81311023
      168.61        5 rows  81311015
      135.05        4 rows  81311026
      101.41        3 rows  81311026, 81311041
      101.36        3 rows  81311008, 81331908
      101.25        3 rows  81311021, 81311008
      101.17        3 rows  61111007, 61111004
       67.60        2 rows  81311008, 99999005
       67.59        2 rows  81311006, 81311008
       67.59        2 rows  81311008, 62441006
       67.59        2 rows  81311008, 54161401
       67.58        2 rows  81341018
       67.57        2 rows  81311008, 81311009
       67.55        2 rows  99999005
       67.53        2 rows  81311008, 81341018
       67.52        2 rows  81311008, 53112004

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  Atlanta Christian CHR-Downtown            2026:67.56
  Beleivers Bible Christian Church          2026:67.38
  Ben Hill Christian Church                 2026:67.40
  Central Christian Church                  2026:67.40
  Chapel of Christian Love                  2026:67.46
  Christ Church of Atlanta                  2026:67.68
  Church's Texas Chicken                    2026:236.04
  Faith By Hearing Christian Center         2026:101.28
  Faith Development Christian               2026:67.42
  Faith Temple Christian Church             2026:67.44
  First Christian Community Church          2026:67.58
  Kingdom Hall of Jehovah's Witnesses       2026:67.49
  Living in Faith Everyday                  2026:67.52
  Mount Nebo Baptist Church                 2026:67.43
  Mount Olive Baptist Church                2026:67.43
  National Church Residences                2026:67.42
  New Jerusalem Baptist Church              2026:67.54
  New Shield of Faith Christian Ministries  2026:101.16
  Pathway Christian Church                  2026:67.48
  Peachtree Christian Church                2026:67.60
  Purpose Center Christian Church           2026:67.36
  Redeeming Love Christian Ministries       2026:67.52
  Rehoboth Family Christian Church          2026:67.46
  River Of Life Christian Center            2026:67.52
  Springdale Christian Church               2026:67.40
  The Catholic Shrine of the Immaculate Co  2026:67.50
  The Church of Jesus Christ of Latter-Day  2026:67.49
  The Universal Church                      2026:67.52
  Westminster Christian Fellowship          2026:67.54
  Zoe Christian Fellowship                  2026:67.62

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  Georgia                                   2026:18.4K

## what

JOIN_COUNT: 1 100%, 2 0%, 0 0%

JOIN_COUNT_1: 1 89%, 0 10%, 2 1%

JOIN_COUNT_12: 1 100%, 0 0%

CITY: Atlanta 100%, East Point 0%

ZIP: 30315 15%, 30318 15%, 30314 12%, 30331 11%, 30310 10%, 30311 8%, 30316 7%, 30312 6%, 30305 4%, 30308 4%, 30317 4%, 30354 4%

NAICS: 81311008 90%, 81311021 2%, 81311026 2%, 72251117 1%, 81311006 1%, 81311015 1%, 61111007 1%, 81331908 1%, 81341018 0%, 99999005 0%, 52213003 0%, 52111001 0%

SIC: 866107 90%, 866110 2%, 866112 2%, 581208 1%, 866104 1%, 866114 1%, 821103 1%, 839998 1%, 869903 0%, 999966 0%, 606101 0%, 601101 0%

HQNAME: Cajun Global LLC 58%, Church of Jesus Christ of Latt 17%, Soka Gakkai International-USA 8%, YWCA USA 8%, Christian Louboutin USA LLC 8%

LOC_CONF: Very High 88%, High 11%, Low 1%

PLACETYPE: Independent 98%, Branch 2%

SQFOOTAGE: 1,500 - 2,499 61%, 2,500 - 4,999 20%, 5,000 - 9,999 7%, 20,000 - 39,999 3%, 1 - 1,499 3%, 10,000 - 19,999 3%, 40,000 - 99,999 2%, 100,000+ 1%

DESC: CONAME, Atlanta, Georgia 100%, CONAME, East Point, Georgia 0%

SPI: 1 16%, 19 16%, 4 15%, 3 15%, 16 11%, 18 7%, 9 5%, 21 4%, 24 4%, 20 4%, 12 3%

SUBAREA: 1 32%, 4 10%, 8 10%, 2 9%, 6 9%, 3 9%, SA1 6%, 12 5%, 7 5%, 5 3%, BL 2%

STATUS: Current 100%, nan 0%

LANDUSECODE: SFR 38%, LDC 14%, LDR 14%, MU 8%, HDC 6%, O-I 6%, MDR 5%, MULD 3%, MUMD 2%, I 2%, HDR 1%, OS 1%

LANDUSEDESC: Single-Family Residential 38%, Low-Density Commercial 14%, Low-Density Residential 14%, Mixed-Use 8%, High-Density Commercial 6%, Office/Institutional 6%, Medium-Density Residential 5%, Mixed-Use Low-Density 3%, Mixed-Use Medium-Density 2%, Industrial 2%, High-Density Residential 1%, Open Space 1%

DENSITY: 0-8 59%, 0-16 22%, 9-16 12%, 17-29 4%, nan 3%

FAR: nan 67%, 0.0 - 3.0 33%

CONVERSION: FLU only 44%, FLU + Zoning 38%, nan 10%, Technical Conversion 5%, R2 Survey 2%, Team Recommendation 1%

NDP: MLSF 29%, LDMU 15%, LDR 11%, nan 10%, HDMU 9%, MDMU 8%, MDR 6%, LLSF 6%, CMTY 2%, I 1%, OS 1%, HDR 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 534 | 0 | 544 3; 543 3; 542 3; 541 3 |
| JOIN_COUNT | category | 3 | 0 | 1 542; 2 1; 0 1 |
| TARGET_FID | other | 534 | 0 | 544 3; 543 3; 542 3; 541 3 |
| JOIN_COUNT_1 | category | 3 | 0 | 1 484; 0 54; 2 6 |
| TARGET_FID_1 | other | 534 | 0 | 544 3; 543 3; 542 3; 541 3 |
| JOIN_COUNT_12 | category | 2 | 0 | 1 543; 0 1 |
| TARGET_FID_12 | other | 534 | 0 | 544 3; 543 3; 542 3; 541 3 |
| CONAME | who | 494 | 0 | Church's Texas Chicken 9; The Catholic Shrine of th 4; The Universal Church 4; The Church of Jesus Chris 4 |
| ADDR | who | 289 | 10 | Campbellton Rd SW 18; Martin Luther King Jr Dr  15; Peachtree Rd NE 11; Donald Lee Hollowell Pkwy 11 |
| CITY | category | 2 | 0 | Atlanta 543; East Point 1 |
| STATE_NAME | who | 1 | 0 | Georgia 544 |
| STATE | other | 1 | 0 | GA 544 |
| ZIP | category | 26 | 4 | 30315 68; 30318 66; 30314 53; 30331 51 |
| ZIP4 | other | 449 | 25 | 5219 5; 3506 4; 4108 4; 3659 4 |
| NAICS | category | 32 | 0 | 81311008 472; 81311021 13; 81311026 9; 72251117 7 |
| NAICS_ALL | who | 84 | 0 | 81311008 409; 81311008, 81311021 8; 72251117, 72251301 7; 81311021 6 |
| SIC | category | 32 | 0 | 866107 472; 866110 13; 866112 9; 581208 7 |
| SIC_ALL | who | 84 | 0 | 866107 409; 866107, 866110 8; 581208, 581206 7; 866110 6 |
| AFFILIATE | empty | 1 | 544 |  |
| BRAND | empty | 1 | 544 |  |
| HQNAME | category | 6 | 532 | Cajun Global LLC 7; Church of Jesus Christ of 2; Soka Gakkai International 1; YWCA USA 1 |
| LOC_CONF | category | 3 | 0 | Very High 478; High 60; Low 6 |
| PLACETYPE | category | 2 | 0 | Independent 532; Branch 12 |
| PROFSPEC | empty | 1 | 544 |  |
| SQFOOTAGE | category | 9 | 14 | 1,500 - 2,499 321; 2,500 - 4,999 107; 5,000 - 9,999 35; 20,000 - 39,999 18 |
| EMPNUM | amount | 41 | 0 | 3.0 169; 2.0 92; 4.0 66; 5.0 41 |
| SALESVOL | amount | 16 | 0 | nan 525; 997000.0 3; 1174000.0 3; 1440000.0 1 |
| SOURCE | who | 1 | 0 | Data Axle 544 |
| ESRI_PID | other | 512 | 0 | 3dc9cf06d9a31589e302b8a01 4; 4fc9f6daa849fee256e65a299 3; 7b56ce395d96400b6a901d7a0 3; efd55fcae7997f7fa80266dad 3 |
| DESC | category | 2 | 0 | CONAME, Atlanta, Georgia 543; CONAME, East Point, Georg 1 |
| LATITUDE | amount | 518 | 0 | 33.73374551987 4; 33.7639499998294 4; 33.6914279998733 4; 33.75036900008508 3 |
| LONGITUDE | amount | 522 | 0 | -84.3645749201314 4; -84.3399179999421 4; -84.5073540002972 4; -84.38958000037528 3 |
| ZONECLASS | other | 97 | 0 | R-4 142; R-4A 34; C-1 26; R-3 23 |
| ZONEDESC | who | 51 | 0 | https://library.municode. 144; https://library.municode. 37; https://library.municode. 34; https://library.municode. 33 |
| SPI | category | 16 | 441 | 1 15; 19 15; 4 14; 3 14 |
| SUBAREA | category | 18 | 429 | 1 34; 4 11; 8 11; 2 10 |
| STATUS | category | 2 | 0 | Current 543; nan 1 |
| LANDUSECODE | category | 18 | 0 | SFR 200; LDC 73; LDR 71; MU 44 |
| LANDUSEDESC | category | 19 | 0 | Single-Family Residential 200; Low-Density Commercial 73; Low-Density Residential 71; Mixed-Use 44 |
| DENSITY | category | 6 | 468 | 0-8 45; 0-16 17; 9-16 9; 17-29 3 |
| FAR | category | 3 | 538 | nan 4; 0.0 - 3.0 2 |
| CONVERSION | category | 6 | 0 | FLU only 237; FLU + Zoning 209; nan 54; Technical Conversion 28 |
| NDP | category | 13 | 0 | MLSF 158; LDMU 83; LDR 62; nan 54 |
| GEOMETRY | other | 487 | 0 | {"type": "Point", "coordi 4; {"type": "Point", "coordi 4; {"type": "Point", "coordi 4; {"type": "Point", "coordi 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:24:57.68428 544 |
| SOURCE_RUN_ID | audit | 1 | 0 | 53265fe6-8bea-48c3-a3fa-0 544 |
| SRC_SHA256 | who | 1 | 0 | 35c33ae7634f4e477a27fd857 544 |
