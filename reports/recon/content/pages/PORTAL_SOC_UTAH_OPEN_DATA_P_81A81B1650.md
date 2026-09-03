# PORTAL_SOC_UTAH_OPEN_DATA_P_81A81B1650

rows 5.0K  columns 28  scan 5.5s

roles: amount 4, audit 2, category 6, date 3, id 3, other 4, state 1, who 6

## when

SOURCEDATE
  2014      2.0K  ##############################
  2015      1.9K  ############################
  2016       496  #######
  2017       321  #####
  2018       157  ##
  2019        39  #

VAL_DATE
  2014      1.3K  ################
  2015      2.5K  ##############################
  2016       442  #####
  2017       301  ####
  2018       196  ##
  2019       262  ###

INGESTED_AT
  2026      5.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 5.0K | 13.52 | 36.85 | 48.35 | 64.83 | 186.8K |
| LONGITUDE | 5.0K | -152.48 | -84.57 | -71.52 | 144.82 | -429.2K |
| MAX_VOLT | 5.0K | -1000.0K | 115 | 345 | 765 | -1.09B |
| MIN_VOLT | 5.0K | -1000.0K | 115 | 345 | 500 | -1.10B |

## who

NAME by rows
         2  BABCOCK
         2  OKLAHOMA GAS ELECTRIC
         2  HIGHLAND CITY
         2  YAPHANK
         2  MOUNT SINAI
         2  WILSON
         2  ATHENS
         2  NORTHSIDE
         2  HANSON
         2  SOUTHWEST
         2  NORTHWEST
         2  DALE MABRY
         2  TRACY
         2  JOHNSON
         1  TAP302593
         1  TAP148943
         1  LESTER
         1  TAP159622
         1  UNKNOWN130836
         1  TAP147148

NAME by dollars
       83.47        2 rows  TRACY
       82.31        2 rows  WILSON
       81.86        2 rows  MOUNT SINAI
       81.67        2 rows  YAPHANK
       70.94        2 rows  OKLAHOMA GAS ELECTRIC
       69.52        2 rows  BABCOCK
       68.79        2 rows  ATHENS
       66.39        2 rows  SOUTHWEST
       66.17        2 rows  NORTHWEST
       64.83        1 rows  UNKNOWN158480
       64.67        1 rows  UNKNOWN158554
       62.87        2 rows  JOHNSON
       61.23        1 rows  TAP158532
       60.63        2 rows  NORTHSIDE
       58.39        1 rows  UNKNOWN158516
       58.21        1 rows  RISER158512
       58.16        2 rows  HIGHLAND CITY
       57.78        1 rows  UNKNOWN158517
       56.49        1 rows  RISER158505
       56.22        2 rows  DALE MABRY

SOURCE by rows
      3.5K  IMAGERY
       709  OpenStreetMap
       468  IMAGERY, OpenStreetMap
        81  http://www.geostor.arkansas.gov/G6/Home.html
        32  IMAGERY, http://www.ct.gov/csc/lib/csc/finalswctreport.pdf
        27  Florida Geographic Data Library, OpenStreetMap
        22  Florida Geographic Data Library
        14  IMAGERY, https://www9.nationalgridus.com/oasis/non_html/pdf/NG%20LTP%2
        11  IMAGERY, http://www.oatioasis.com/TVA/TVAdocs/TVA_Transmission_Map_201
         9  IMAGERY, http://www.pjm.com/-/media/markets-ops/trans-service/trans-fa
         7  IMAGERY, http://www.nyiso.com/public/webdocs/markets_operations/servic
         6  IMAGERY, http://www.nyiso.com/public/webdocs/markets_operations/servic
         5  OpenStreetMap, http://www.pjm.com/~/media/documents/reports/2012-rtep/
         4  IMAGERY, https://aeptransmission.com/virginia/Tazewell-Bearwallow/docs
         4  IMAGERY, http://www.southeasternrtp.com/docs/general/2018/2018-SERTP-2
         3  http://www.geostor.arkansas.gov/G6/Home.html, OpenStreetMap
         3  IMAGERY, https://www.atlanticcityelectric.com/SiteCollectionDocuments/
         3  IMAGERY, OpenStreetMap, https://www.atlanticcityelectric.com/SiteColle
         3  IMAGERY, http://psc.ky.gov/pscscf/2009%20cases/2009-00106/20090422_EKP
         3  OpenStreetMap, http://www.progress-energy.com/assets/www/static-conten

SOURCE by dollars
      132.3K     3.5K rows  IMAGERY
       25.9K      709 rows  OpenStreetMap
       16.9K      468 rows  IMAGERY, OpenStreetMap
        2.8K       81 rows  http://www.geostor.arkansas.gov/G6/Home.html
        1.3K       32 rows  IMAGERY, http://www.ct.gov/csc/lib/csc/finalswctreport.pdf
      747.56       27 rows  Florida Geographic Data Library, OpenStreetMap
      624.53       22 rows  Florida Geographic Data Library
      602.61       14 rows  IMAGERY, https://www9.nationalgridus.com/oasis/non_html/pdf/
      406.60       11 rows  IMAGERY, http://www.oatioasis.com/TVA/TVAdocs/TVA_Transmissi
      339.13        9 rows  IMAGERY, http://www.pjm.com/-/media/markets-ops/trans-servic
      301.80        7 rows  IMAGERY, http://www.nyiso.com/public/webdocs/markets_operati
      250.51        6 rows  IMAGERY, http://www.nyiso.com/public/webdocs/markets_operati
      208.49        5 rows  OpenStreetMap, http://www.pjm.com/~/media/documents/reports/
      152.57        4 rows  IMAGERY, http://www.southeasternrtp.com/docs/general/2018/20
      150.45        4 rows  IMAGERY, https://aeptransmission.com/virginia/Tazewell-Bearw
      118.07        3 rows  IMAGERY, OpenStreetMap, https://www.atlanticcityelectric.com
      117.92        3 rows  IMAGERY, https://www.atlanticcityelectric.com/SiteCollection
      113.24        3 rows  IMAGERY, http://psc.ky.gov/pscscf/2009%20cases/2009-00106/20
      103.48        3 rows  OpenStreetMap, http://sppoasis.spp.org/documents/swpp/transm
      103.01        3 rows  http://www.geostor.arkansas.gov/G6/Home.html, OpenStreetMap

NAICS_DESC by rows
      5.0K  ELECTRIC BULK POWER TRANSMISSION AND CONTROL

NAICS_DESC by dollars
      186.8K     5.0K rows  ELECTRIC BULK POWER TRANSMISSION AND CONTROL

CITY by rows
        34  LEXINGTON
        33  NOT AVAILABLE
        30  MIAMI
        27  TULSA
        25  TAMPA
        24  KNOXVILLE
        23  OKLAHOMA CITY
        22  INDIANAPOLIS
        19  CHARLOTTE
        19  LOUISVILLE
        18  JACKSONVILLE
        17  BIRMINGHAM
        16  RICHMOND
        15  ORLANDO
        15  FLORENCE
        14  BOWLING GREEN
        14  LINCOLN
        14  LANCASTER
        14  MONTGOMERY
        13  MARION

CITY by dollars
        1.3K       34 rows  LEXINGTON
        1.2K       33 rows  NOT AVAILABLE
      975.36       27 rows  TULSA
      875.22       22 rows  INDIANAPOLIS
      863.21       24 rows  KNOXVILLE
      815.66       23 rows  OKLAHOMA CITY
      807.42       30 rows  MIAMI
      725.91       19 rows  LOUISVILLE
      700.28       25 rows  TAMPA
      668.74       19 rows  CHARLOTTE
      610.92       16 rows  RICHMOND
      569.78       17 rows  BIRMINGHAM
      566.62       18 rows  JACKSONVILLE
      559.49       14 rows  LINCOLN
      544.99       14 rows  LANCASTER
      527.01       15 rows  FLORENCE
      493.85       13 rows  EVANSVILLE
      492.36       13 rows  WILMINGTON
      490.21       11 rows  SAINT PAUL
      489.19       14 rows  BOWLING GREEN

## who x when

NAME by VAL_DATE, dollars = LATITUDE
  ATHENS                                    2014:34.82 2017:33.97
  BABCOCK                                   2015:69.52
  DALE MABRY                                2015:28.11 2016:28.11
  HANSON                                    2015:53.71
  HIGHLAND CITY                             2015:58.16
  JOHNSON                                   2015:62.87
  LESTER                                    2015:41.40
  MOUNT SINAI                               2015:81.86
  NORTHSIDE                                 2015:60.63
  NORTHWEST                                 2014:37.74 2015:28.43
  OKLAHOMA GAS ELECTRIC                     2014:70.94
  RISER158505                               2018:56.49
  RISER158512                               2018:58.21
  SOUTHWEST                                 2015:66.39
  TAP147148                                 2016:33.41
  TAP148943                                 2015:36.04
  TAP158532                                 2018:61.23
  TAP159622                                 2018:45.37
  TAP302593                                 2017:33.56
  TRACY                                     2015:83.47
  UNKNOWN130836                             2015:43.29
  UNKNOWN158480                             2018:64.83
  UNKNOWN158516                             2018:58.39
  UNKNOWN158517                             2018:57.78
  UNKNOWN158554                             2018:64.67
  WILSON                                    2015:44.86 2017:37.45
  YAPHANK                                   2015:81.67

SOURCE by VAL_DATE, dollars = LATITUDE
  Florida Geographic Data Library           2015:624.53
  Florida Geographic Data Library, OpenStr  2015:747.56
  IMAGERY                                   2014:38.1K 2015:58.2K 2016:13.8K 2017:8.0K 2018:6.3K 2019:7.9K
  IMAGERY, OpenStreetMap                    2014:1.5K 2015:14.7K 2016:301.26 2017:38.52 2018:62.99 2019:243.12
  IMAGERY, OpenStreetMap, https://www.atla  2019:118.07
  IMAGERY, http://psc.ky.gov/pscscf/2009%2  2019:113.24
  IMAGERY, http://www.ct.gov/csc/lib/csc/f  2015:1.2K 2016:83.17
  IMAGERY, http://www.nyiso.com/public/web  2015:208.57 2019:41.94
  IMAGERY, http://www.nyiso.com/public/web  2015:172.61 2019:129.19
  IMAGERY, http://www.oatioasis.com/TVA/TV  2015:369.65 2018:36.95
  IMAGERY, http://www.pjm.com/-/media/mark  2017:301.30 2019:37.83
  IMAGERY, http://www.southeasternrtp.com/  2019:152.57
  IMAGERY, https://aeptransmission.com/vir  2019:150.45
  IMAGERY, https://www.atlanticcityelectri  2019:117.92
  IMAGERY, https://www9.nationalgridus.com  2019:602.61
  OpenStreetMap                             2014:6.1K 2015:13.7K 2016:3.3K 2017:2.6K 2018:220.81
  OpenStreetMap, http://sppoasis.spp.org/d  2015:103.48
  OpenStreetMap, http://www.pjm.com/~/medi  2015:208.49
  OpenStreetMap, http://www.progress-energ  2015:85.18
  http://www.geostor.arkansas.gov/G6/Home.  2015:2.7K 2018:69.90 2019:35.08
  http://www.geostor.arkansas.gov/G6/Home.  2015:69.66 2016:33.35

## where

STATE: FL 509, NY 482, OK 419, NC 380, KY 334, AL 326, IN 285, SC 225, AR 214, GA 192, KS 186, ND 172

## what

LINES: 3 32%, 2 29%, 1 24%, 4 6%, 5 3%, 6 2%, 7 1%, 0 1%, 8 1%, 9 1%, 10 1%, 11 0%

MAX_INFER: Y 67%, NOT AVAILABLE 22%, N 11%

MIN_INFER: Y 68%, NOT AVAILABLE 22%, N 10%

STATUS: IN SERVICE 99%, NOT AVAILABLE 1%

TYPE: SUBSTATION 75%, TAP 25%, RISER 1%

VAL_METHOD: IMAGERY 80%, IMAGERY/OTHER 19%, UNVERIFIED 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CITY | who | 2.5K | 0 | LEXINGTON 36; NOT AVAILABLE 33; MIAMI 30; TAMPA 29 |
| COUNTRY | other | 1 | 0 | USA 5.0K |
| COUNTY | who | 871 | 0 | JEFFERSON 83; ONONDAGA 53; MARION 52; HILLSBOROUGH 50 |
| COUNTYFIPS | other | 1.3K | 0 | 36067 53; 40143 42; 12057 40; 12105 37 |
| ID | id | 5.0K | 0 | 127784 25; 132708 25; 147432 25; 124047 25 |
| LATITUDE | amount | 5.0K | 0 | 42.6758361010001 25; 43.092895943 25; 35.098755811 25; 40.244884384 25 |
| LINES | category | 21 | 0 | 3 1.6K; 2 1.4K; 1 1.2K; 4 276 |
| LONGITUDE | amount | 5.0K | 0 | -73.698418831 25; -70.778675399 25; -78.827796688 25; -85.4103270689999 25 |
| MAX_INFER | category | 3 | 0 | Y 3.4K; NOT AVAILABLE 1.1K; N 546 |
| MAX_VOLT | amount | 16 | 0 | 115 1.2K; -999999 1.1K; 69 913; 138 743 |
| MIN_INFER | category | 3 | 0 | Y 3.4K; NOT AVAILABLE 1.1K; N 505 |
| MIN_VOLT | amount | 15 | 0 | 115 1.3K; -999999 1.1K; 69 1.1K; 138 720 |
| NAICS_CODE | other | 1 | 0 | 221121 5.0K |
| NAICS_DESC | who | 1 | 0 | ELECTRIC BULK POWER TRANS 5.0K |
| NAME | who | 5.0K | 0 | UNKNOWN127784 25; UNKNOWN132708 25; FAYETTEVILLE EAST 25; UNKNOWN124047 25 |
| OBJECTID | id | 5.0K | 0 | 23381 25; 21812 25; 19371 25; 11325 25 |
| SOURCE | who | 96 | 0 | IMAGERY 3.5K; OpenStreetMap 709; IMAGERY, OpenStreetMap 468; http://www.geostor.arkans 81 |
| SOURCEDATE | date | 565 | 0 | 2014-04-07T00:00:00.000Z 378; 2015-01-07T00:00:00.000Z 206; 2016-08-04T00:00:00.000Z 142; 2015-07-29T00:00:00.000Z 103 |
| STATE | state | 44 | 0 | FL 509; NY 482; OK 419; NC 380 |
| STATUS | category | 2 | 0 | IN SERVICE 5.0K; NOT AVAILABLE 36 |
| TYPE | category | 3 | 0 | SUBSTATION 3.7K; TAP 1.2K; RISER 27 |
| VAL_DATE | date | 558 | 0 | 2015-08-14T00:00:00.000Z 739; 2015-09-08T00:00:00.000Z 106; 2015-06-22T00:00:00.000Z 97; 2014-12-15T00:00:00.000Z 97 |
| VAL_METHOD | category | 3 | 0 | IMAGERY 4.0K; IMAGERY/OTHER 966; UNVERIFIED 35 |
| ZIP | other | 3.4K | 0 | NOT AVAILABLE 31; 12180 26; 03801 25; 28312 25 |
| POINT | id | 5.1K | 0 | {"type": "Point", "coordi 25; {"type": "Point", "coordi 25; {"type": "Point", "coordi 25; {"type": "Point", "coordi 25 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:49:23.25354 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 78ba8244-602b-46ec-8219-7 5.0K |
| SRC_SHA256 | who | 1 | 0 | 35b20640c7c1973e3c0e6d254 5.0K |
