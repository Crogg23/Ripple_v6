# PORTAL_ARC_ATLANTA_DATAATLA_03DC194F2A

rows 130  columns 34  scan 3.3s

roles: amount 4, audit 2, category 11, date 3, empty 3, other 5, who 7

## when

CREATIONDATE
  2024       130  ##############################

EDITDATE
  2024       130  ##############################

INGESTED_AT
  2026       130  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EMPNUM | 129 | 1 | 3 | 34.32 | 75 | 809 |
| SALESVOL | 4 | 220.0K | 837.5K | 2.68M | 2.73M | 4.63M |
| LATITUDE | 130 | 33.67 | 33.76 | 33.79 | 33.79 | 4.4K |
| LONGITUDE | 130 | -84.50 | -84.44 | -84.35 | -84.35 | -11.0K |

## who

CONAME by rows
         2  Faith Development Christian
         2  True Worship Christian Fellowship
         2  Central Christian Church
         2  The Catholic Shrine of the Immaculate Conception
         2  Living in Faith Everyday
         2  Faith Temple Christian Church
         2  New Jerusalem Baptist Church
         2  First Christian Community Church
         1  Central United Methodist Church
         1  New Light Baptist Church
         1  Word of God Ministries
         1  Saint Lukes Episcopal Church
         1  Mount Nebo Baptist Church
         1  Independent Churches United
         1  Sims Ave Church of Christ
         1  Greater Mt Carmel Baptist Church
         1  Linden Shorts Institutional CME Church
         1  Life Church
         1  West Oak Baptist
         1  House of Yisra El of Atlanta

CONAME by dollars
       67.58        2 rows  First Christian Community Church
       67.54        2 rows  New Jerusalem Baptist Church
       67.52        2 rows  Living in Faith Everyday
       67.50        2 rows  The Catholic Shrine of the Immaculate Conception
       67.44        2 rows  Faith Temple Christian Church
       67.42        2 rows  True Worship Christian Fellowship
       67.42        2 rows  Faith Development Christian
       67.40        2 rows  Central Christian Church
       33.79        1 rows  Greater Leavy Missionary Baptist Church
       33.79        1 rows  Crown of Glory Missionary Baptist Church
       33.79        1 rows  House of Prayer
       33.79        1 rows  Church the Lord Jesus Christ
       33.79        1 rows  Baptist Woodward
       33.79        1 rows  Henry Street Church of God
       33.79        1 rows  Kingdom Harvest Church
       33.79        1 rows  Center Hill Baptist Church
       33.78        1 rows  The Grace of God Prophetic Deliverance Ministries
       33.78        1 rows  True Love Baptist Church
       33.78        1 rows  Word of God Ministries
       33.78        1 rows  Visions of Life Baptist Church

STATE_NAME by rows
       130  Georgia

STATE_NAME by dollars
        4.4K      130 rows  Georgia

ADDR by rows
        11  Donald Lee Hollowell Pkwy NW
         9  Campbellton Rd SW
         7  Joseph E Boone Blvd NW
         6  Hamilton E Holmes Dr NW
         4  Joseph E Lowery Blvd NW
         4  Hollywood Rd NW
         4  Peachtree St NE
         3  Bolton Rd NW
         3  Martin Luther King Jr Dr SW
         3  Sylvan Rd SW
         2  Dodson Dr SW
         2  Cascade Rd SW
         2  Jones Ave NW
         2  Westmont Rd SW
         2  Auburn Ave NE
         2  Washington St SW
         2  Fairburn Rd NW
         2  Griffin St NW
         2  Alvin Dr NW
         2  Vine St NW

ADDR by dollars
      371.54       11 rows  Donald Lee Hollowell Pkwy NW
      303.34        9 rows  Campbellton Rd SW
      236.32        7 rows  Joseph E Boone Blvd NW
      202.59        6 rows  Hamilton E Holmes Dr NW
      135.14        4 rows  Hollywood Rd NW
      135.06        4 rows  Peachtree St NE
      135.05        4 rows  Joseph E Lowery Blvd NW
      101.33        3 rows  Bolton Rd NW
      101.25        3 rows  Martin Luther King Jr Dr SW
      101.13        3 rows  Sylvan Rd SW
       67.58        2 rows  Alvin Dr NW
       67.54        2 rows  Fairburn Rd NW
       67.52        2 rows  Vine St NW
       67.52        2 rows  Walnut St NW
       67.52        2 rows  Jones Ave NW
       67.52        2 rows  Griffin St NW
       67.52        2 rows  Auburn Ave NE
       67.50        2 rows  Washington St SW
       67.44        2 rows  Cascade Rd SW
       67.44        2 rows  Westmont Rd SW

SOURCE by rows
       130  Data Axle

SOURCE by dollars
        4.4K      130 rows  Data Axle

## who x when

CONAME by CREATIONDATE, dollars = LATITUDE
  Baptist Woodward                          2024:33.79
  Center Hill Baptist Church                2024:33.79
  Central Christian Church                  2024:67.40
  Central United Methodist Church           2024:33.75
  Church the Lord Jesus Christ              2024:33.79
  Crown of Glory Missionary Baptist Church  2024:33.79
  Faith Development Christian               2024:67.42
  Faith Temple Christian Church             2024:67.44
  First Christian Community Church          2024:67.58
  Greater Leavy Missionary Baptist Church   2024:33.79
  Greater Mt Carmel Baptist Church          2024:33.70
  Henry Street Church of God                2024:33.79
  House of Prayer                           2024:33.79
  House of Yisra El of Atlanta              2024:33.68
  Independent Churches United               2024:33.71
  Kingdom Harvest Church                    2024:33.79
  Life Church                               2024:33.67
  Linden Shorts Institutional CME Church    2024:33.77
  Living in Faith Everyday                  2024:67.52
  Mount Nebo Baptist Church                 2024:33.70
  New Jerusalem Baptist Church              2024:67.54
  New Light Baptist Church                  2024:33.70
  Saint Lukes Episcopal Church              2024:33.77
  Sims Ave Church of Christ                 2024:33.78
  The Catholic Shrine of the Immaculate Co  2024:67.50
  The Grace of God Prophetic Deliverance M  2024:33.78
  True Love Baptist Church                  2024:33.78
  True Worship Christian Fellowship         2024:67.42
  West Oak Baptist                          2024:33.73
  Word of God Ministries                    2024:33.78

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2024:4.4K

## what

CITY: Atlanta 99%, East Point 1%

ZIP: 30318 32%, 30314 20%, 30311 13%, 30303 8%, 30331 8%, 30310 7%, 30315 5%, 30308 4%, 30301 2%, 30344 1%, 30313 1%

NAICS: 81311008 91%, 81311021 2%, 61111007 2%, 99999005 1%, 45921005 1%, 32711011 1%, 52213003 1%, 72251117 1%, 51612006 1%, 81311015 1%

NAICS_ALL: 81311008 85%, 81311008, 81311021 3%, 81311021 2%, 81311008, 81311006 2%, 81311008, 81311023 2%, 99999005 1%, 45921005 1%, 61111007, 61111004, 62441003 1%, 32711011, 42499050 1%, 61111007, 61111004 1%, 52213003, 52213006 1%, 72251117, 72251301 1%

SIC: 866107 91%, 866110 2%, 821103 2%, 999966 1%, 594201 1%, 326902 1%, 606101 1%, 581208 1%, 738301 1%, 866114 1%

SIC_ALL: 866107 85%, 866107, 866110 3%, 866110 2%, 866107, 866104 2%, 866107, 866101 2%, 999966 1%, 594201 1%, 821103, 821101, 835101 1%, 326902, 519910 1%, 821103, 821101 1%, 606101, 606102 1%, 581208, 581206 1%

HQNAME: Cajun Global LLC 50%, Church of Jesus Christ of Latt 50%

LOC_CONF: Very High 85%, High 13%, Low 2%

PLACETYPE: Independent 98%, Branch 2%

SQFOOTAGE: 1,500 - 2,499 63%, 2,500 - 4,999 20%, 20,000 - 39,999 5%, 5,000 - 9,999 5%, 10,000 - 19,999 3%, 1 - 1,499 2%, 40,000 - 99,999 1%

DESC: CONAME, Atlanta, Georgia 99%, CONAME, East Point, Georgia 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 129 | 0 | 142 1; 141 1; 140 1; 139 1 |
| CONAME | who | 123 | 0 | The Catholic Shrine of th 2; True Worship Christian Fe 2; First Christian Community 2; Faith Temple Christian Ch 2 |
| ADDR | who | 74 | 2 | Donald Lee Hollowell Pkwy 11; Campbellton Rd SW 9; Joseph E Boone Blvd NW 7; Hamilton E Holmes Dr NW 6 |
| CITY | category | 2 | 0 | Atlanta 129; East Point 1 |
| STATE_NAME | who | 1 | 0 | Georgia 130 |
| STATE | other | 1 | 0 | GA 130 |
| ZIP | category | 11 | 0 | 30318 41; 30314 26; 30311 17; 30303 11 |
| ZIP4 | other | 117 | 5 | 3506 2; 4951 2; 7413 2; 3904 2 |
| NAICS | category | 10 | 0 | 81311008 118; 81311021 3; 61111007 2; 99999005 1 |
| NAICS_ALL | category | 22 | 0 | 81311008 102; 81311008, 81311021 4; 81311021 3; 81311008, 81311006 2 |
| SIC | category | 10 | 0 | 866107 118; 866110 3; 821103 2; 999966 1 |
| SIC_ALL | category | 22 | 0 | 866107 102; 866107, 866110 4; 866110 3; 866107, 866104 2 |
| AFFILIATE | empty | 1 | 130 |  |
| BRAND | empty | 1 | 130 |  |
| HQNAME | category | 3 | 128 | Cajun Global LLC 1; Church of Jesus Christ of 1 |
| LOC_CONF | category | 3 | 0 | Very High 111; High 17; Low 2 |
| PLACETYPE | category | 2 | 0 | Independent 128; Branch 2 |
| PROFSPEC | empty | 1 | 130 |  |
| SQFOOTAGE | category | 8 | 2 | 1,500 - 2,499 81; 2,500 - 4,999 25; 20,000 - 39,999 7; 5,000 - 9,999 7 |
| EMPNUM | amount | 24 | 0 | 3.0 41; 2.0 23; 4.0 17; 5.0 7 |
| SALESVOL | amount | 5 | 0 | nan 126; 678000.0 1; 220000.0 1; 997000.0 1 |
| SOURCE | who | 1 | 0 | Data Axle 130 |
| ESRI_PID | other | 124 | 0 | 3dc9cf06d9a31589e302b8a01 2; ecf55e4bfb3717d65bfd53751 2; 9636a40050c5e662597cd7916 2; d50198fe333eb38d645a9d084 2 |
| DESC | category | 2 | 0 | CONAME, Atlanta, Georgia 129; CONAME, East Point, Georg 1 |
| LATITUDE | amount | 125 | 0 | 33.708645000029534 2; 33.7032810000519 2; 33.7741947403539 2; 33.75036900008508 1 |
| LONGITUDE | amount | 130 | 0 | -84.45310200042765 2; -84.4735666502726 2; -84.38958000037528 1; -84.40611749966567 1 |
| CREATIONDATE | date | 6 | 0 | 1707152735059 114; 1707152711187 10; 1707152728927 2; 1707152705131 2 |
| CREATOR | who | 1 | 0 | gpickren2 130 |
| EDITDATE | date | 6 | 0 | 1707152735059 114; 1707152711187 10; 1707152728927 2; 1707152705131 2 |
| EDITOR | who | 1 | 0 | gpickren2 130 |
| GEOMETRY | other | 124 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:20:22.04286 130 |
| SOURCE_RUN_ID | audit | 1 | 0 | df465a7a-b89e-4be2-9268-1 130 |
| SRC_SHA256 | who | 1 | 0 | f5a75efd653a531cc12eb148a 130 |
