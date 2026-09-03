# PORTAL_ARC_ATLANTA_DATAATLA_5ADD5EAF6A

rows 454  columns 34  scan 4.0s

roles: amount 4, audit 2, category 8, date 3, empty 2, other 5, who 11

## when

CREATIONDATE
  2024       454  ##############################

EDITDATE
  2024       454  ##############################

INGESTED_AT
  2026       454  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EMPNUM | 449 | 1 | 5 | 100 | 300 | 4.3K |
| SALESVOL | 401 | 41.0K | 512.0K | 12.35M | 33.47M | 431.60M |
| LATITUDE | 454 | 33.65 | 33.76 | 33.86 | 33.88 | 15.3K |
| LONGITUDE | 454 | -84.54 | -84.39 | -84.33 | -84.29 | -38.3K |

## who

CONAME by rows
        37  Starbucks
        20  Circle K
        16  Dunkin'
         7  Smoothie King
         5  Baskin-Robbins
         4  Insomnia Cookies
         4  QuikTrip
         4  sweetgreen
         4  Caribou Coffee
         3  Great American Cookies
         3  Einstein Bros Bagels
         3  Kale Me Crazy
         3  Arden's Garden
         3  Panera Bread
         3  WFM Coffee Bar
         2  NrGize Lifestyle Cafe Inside LA Fitness
         2  IT'SUGAR
         2  Tiff's Treats
         2  Quick Mart
         2  Krispy Kreme Doughnuts

CONAME by dollars
        1.3K       37 rows  Starbucks
      675.52       20 rows  Circle K
      540.65       16 rows  Dunkin'
      236.59        7 rows  Smoothie King
      168.98        5 rows  Baskin-Robbins
      135.19        4 rows  sweetgreen
      135.19        4 rows  QuikTrip
      135.14        4 rows  Caribou Coffee
      135.04        4 rows  Insomnia Cookies
      101.45        3 rows  Panera Bread
      101.42        3 rows  Arden's Garden
      101.41        3 rows  WFM Coffee Bar
      101.39        3 rows  Kale Me Crazy
      101.37        3 rows  Einstein Bros Bagels
      101.24        3 rows  Great American Cookies
       67.64        2 rows  IT'SUGAR
       67.62        2 rows  Tiff's Treats
       67.54        2 rows  Pic N Pay
       67.54        2 rows  Quick Mart
       67.52        2 rows  Rising Roll Gourmet

STATE_NAME by rows
       454  Georgia

STATE_NAME by dollars
       15.3K      454 rows  Georgia

ADDR by rows
        24  Peachtree St NE
        21  Peachtree Rd NE
        15  Piedmont Rd NE
        12  Joseph E Boone Blvd NW
        12  Howell Mill Rd NW
        12  Donald Lee Hollowell Pkwy NW
        11  Campbellton Rd SW
        10  Edgewood Ave SE
        10  Piedmont Ave NE
         9  Martin Luther King Jr Dr SW
         9  Roswell Rd NE
         8  Ponce de Leon Ave NE
         8  N Highland Ave NE
         7  Glenwood Ave SE
         7  Moreland Ave SE
         7  Marietta St NW
         7  Auburn Ave NE
         6  14th St NW
         5  Jonesboro Rd SE
         5  Memorial Dr SE

ADDR by dollars
      810.58       24 rows  Peachtree St NE
      710.68       21 rows  Peachtree Rd NE
      507.47       15 rows  Piedmont Rd NE
      405.54       12 rows  Howell Mill Rd NW
      405.35       12 rows  Donald Lee Hollowell Pkwy NW
      405.12       12 rows  Joseph E Boone Blvd NW
      370.69       11 rows  Campbellton Rd SW
      337.91       10 rows  Piedmont Ave NE
      337.50       10 rows  Edgewood Ave SE
      304.76        9 rows  Roswell Rd NE
      303.77        9 rows  Martin Luther King Jr Dr SW
      270.18        8 rows  Ponce de Leon Ave NE
      270.18        8 rows  N Highland Ave NE
      236.39        7 rows  Marietta St NW
      236.32        7 rows  Auburn Ave NE
      236.18        7 rows  Glenwood Ave SE
      236.10        7 rows  Moreland Ave SE
      202.74        6 rows  14th St NW
      168.91        5 rows  Spring St NW
      168.75        5 rows  Memorial Dr SE

NAICS_ALL by rows
        48  72251505, 44529805
        45  44513101
        43  44511003
        15  72251510, 31181102, 72251117, 72251502, 72251505
        14  44511003, 44513101
        13  44529202
        11  44513101, 45712003
         9  44523005
         8  72251117, 44525004
         7  72251510
         7  44529805
         6  44524006
         6  44523003
         5  44529814
         5  44529812
         5  72251117, 31181102
         5  72251518, 44523005
         5  44525004
         5  72251505, 44529805, 72251117
         4  72251506, 72251117

NAICS_ALL by dollars
        1.6K       48 rows  72251505, 44529805
        1.5K       45 rows  44513101
        1.5K       43 rows  44511003
      506.87       15 rows  72251510, 31181102, 72251117, 72251502, 72251505
      472.47       14 rows  44511003, 44513101
      439.23       13 rows  44529202
      371.52       11 rows  44513101, 45712003
      303.74        9 rows  44523005
      270.05        8 rows  72251117, 44525004
      236.42        7 rows  44529805
      236.37        7 rows  72251510
      202.61        6 rows  44524006
      202.55        6 rows  44523003
      168.93        5 rows  72251518, 44523005
      168.90        5 rows  44529812
      168.88        5 rows  44529814
      168.88        5 rows  72251117, 31181102
      168.77        5 rows  72251505, 44529805, 72251117
      168.67        5 rows  44525004
      135.19        4 rows  72251117, 45619103, 48411004, 72251301

## who x when

CONAME by CREATIONDATE, dollars = LATITUDE
  Arden's Garden                            2024:101.42
  Baskin-Robbins                            2024:168.98
  Caribou Coffee                            2024:135.14
  Circle K                                  2024:675.52
  Dunkin'                                   2024:540.65
  Einstein Bros Bagels                      2024:101.37
  Great American Cookies                    2024:101.24
  IT'SUGAR                                  2024:67.64
  Insomnia Cookies                          2024:135.04
  Kale Me Crazy                             2024:101.39
  Krispy Kreme Doughnuts                    2024:67.51
  NrGize Lifestyle Cafe Inside LA Fitness   2024:67.50
  Panera Bread                              2024:101.45
  Pic N Pay                                 2024:67.54
  Quick Mart                                2024:67.54
  QuikTrip                                  2024:135.19
  Rising Roll Gourmet                       2024:67.52
  Smoothie King                             2024:236.59
  Starbucks                                 2024:1.3K
  Tiff's Treats                             2024:67.62
  WFM Coffee Bar                            2024:101.41
  sweetgreen                                2024:135.19

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2024:15.3K

## what

ZIP: 30318 18%, 30303 13%, 30310 9%, 30308 8%, 30324 8%, 30305 7%, 30309 7%, 30315 7%, 30316 7%, 30331 6%, 30307 5%, 30311 5%

NAICS: 44513101 21%, 44511003 19%, 72251117 17%, 72251505 15%, 72251510 7%, 44523005 4%, 44529202 4%, 72251518 4%, 44529805 3%, 72251506 3%, 44524006 3%, 44525004 2%

SIC: 541103 21%, 541105 19%, 581208 17%, 581228 15%, 546105 7%, 543104 4%, 544101 4%, 581248 4%, 549915 3%, 546109 3%, 542107 3%, 542101 2%

BRAND: Exxon 27%, Chevron 20%, 76 20%, Shell 13%, Phillips 66 7%, Marathon 7%, BP 7%

HQNAME: Starbucks Corporation 36%, Circle K Stores Inc 19%, Dunkin' Brands, Inc 15%, Baskin-Robbins LLC 5%, sweetgreen, Inc 4%, QuikTrip Corporation 4%, Kahala Brands, Ltd 4%, Insomnia Cookies LLC 4%, Caribou Coffee Company, Inc 4%, Whole Foods Market, Inc 3%, Panera Bread 3%

LOC_CONF: Very High 89%, High 11%

PLACETYPE: Independent 67%, Branch 33%

SQFOOTAGE: 1,500 - 2,499 42%, 2,500 - 4,999 29%, 1 - 1,499 11%, 5,000 - 9,999 7%, 10,000 - 19,999 5%, 100,000+ 2%, 20,000 - 39,999 2%, 40,000 - 99,999 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 449 | 0 | 454 3; 453 3; 452 3; 451 3 |
| CONAME | who | 342 | 0 | Starbucks 38; Circle K 20; Dunkin' 16; Smoothie King 8 |
| ADDR | who | 172 | 3 | Peachtree St NE 24; Peachtree Rd NE 21; Piedmont Rd NE 15; Joseph E Boone Blvd NW 12 |
| CITY | who | 1 | 0 | Atlanta 454 |
| STATE_NAME | who | 1 | 0 | Georgia 454 |
| STATE | other | 1 | 0 | GA 454 |
| ZIP | category | 28 | 0 | 30318 62; 30303 45; 30310 32; 30308 28 |
| ZIP4 | other | 366 | 19 | 3012 7; 1162 5; 1804 4; 2705 4 |
| NAICS | category | 36 | 0 | 44513101 82; 44511003 75; 72251117 65; 72251505 57 |
| NAICS_ALL | who | 172 | 0 | 72251505, 44529805 48; 44513101 45; 44511003 43; 72251510, 31181102, 72251 15 |
| SIC | category | 36 | 0 | 541103 82; 541105 75; 581208 65; 581228 57 |
| SIC_ALL | who | 170 | 0 | 581228, 549915 48; 541103 45; 541105 43; 546105, 546101, 546102, 5 15 |
| AFFILIATE | empty | 1 | 454 |  |
| BRAND | category | 8 | 439 | Exxon 4; Chevron 3; 76 3; Shell 2 |
| HQNAME | category | 41 | 312 | Starbucks Corporation 37; Circle K Stores Inc 20; Dunkin' Brands, Inc 16; Baskin-Robbins LLC 5 |
| LOC_CONF | category | 2 | 0 | Very High 402; High 52 |
| PLACETYPE | category | 2 | 0 | Independent 303; Branch 151 |
| PROFSPEC | empty | 1 | 454 |  |
| SQFOOTAGE | category | 9 | 53 | 1,500 - 2,499 170; 2,500 - 4,999 117; 1 - 1,499 43; 5,000 - 9,999 30 |
| EMPNUM | amount | 41 | 0 | 2.0 83; 4.0 52; 5.0 46; 3.0 41 |
| SALESVOL | amount | 108 | 0 | 410000.0 77; nan 53; 997000.0 19; 599000.0 17 |
| SOURCE | who | 1 | 0 | Data Axle 454 |
| ESRI_PID | other | 451 | 0 | 4626e0c676de4d038b8ec67da 3; f990f692dcc1669f2a4dd7472 3; 739314fdd83b9aea416bc714f 3; 1d22a90b4859c121bfe770360 3 |
| DESC | who | 1 | 0 | CONAME, Atlanta, Georgia 454 |
| LATITUDE | amount | 383 | 0 | 33.84611100016598 8; 33.75404999982484 7; 33.78187800016436 3; 33.72303600011218 3 |
| LONGITUDE | amount | 390 | 0 | -84.36227850017669 8; -84.3798734998128 7; -84.40480800032317 3; -84.46284450007683 3 |
| CREATIONDATE | date | 1 | 0 | 1707161670730 454 |
| CREATOR | who | 1 | 0 | gpickren2 454 |
| EDITDATE | date | 1 | 0 | 1707161670730 454 |
| EDITOR | who | 1 | 0 | gpickren2 454 |
| GEOMETRY | other | 394 | 0 | {"type": "Point", "coordi 8; {"type": "Point", "coordi 7; {"type": "Point", "coordi 3; {"type": "Point", "coordi 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:24:00.38942 454 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6a6833f6-802f-4f8e-b686-7 454 |
| SRC_SHA256 | who | 1 | 0 | 72a05dac8f98172c1f0ed86a9 454 |
