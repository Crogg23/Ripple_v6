# PORTAL_ARC_ATLANTA_DATAATLA_CC5FA4CA01

rows 390  columns 34  scan 3.3s

roles: amount 4, audit 2, category 6, date 3, empty 2, other 5, who 13

## when

CREATIONDATE
  2023       390  ##############################

EDITDATE
  2023       390  ##############################

INGESTED_AT
  2026       390  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EMPNUM | 225 | 1 | 5 | 832.76 | 6.0K | 11.0K |
| SALESVOL | 187 | 28.0K | 2.51M | 42.92M | 410.46M | 1.13B |
| LATITUDE | 390 | 33.68 | 33.76 | 33.79 | 33.80 | 13.2K |
| LONGITUDE | 390 | -84.50 | -84.39 | -84.38 | -84.35 | -32.9K |

## who

CONAME by rows
       144  ATM
        10  LibertyX Bitcoin ATM
         7  Western Union Agent Location
         5  Truist
         4  Truist Mortgage
         4  Coinsource Bitcoin ATM
         3  Wells Fargo
         3  Bank of America
         3  TitleMax
         2  Northeast Bonding Co
         2  HilltopSecurities
         2  Action Capital Corp
         2  Consumer Credit Counseling Service
         2  Georgia United Credit Union
         2  Fannie Mae
         2  Chase
         2  Grandbridge Real Estate Capital
         2  ATC Income Tax
         2  Cash America Pawn
         2  Georgia's Own Credit Union

CONAME by dollars
        4.9K      144 rows  ATM
      337.32       10 rows  LibertyX Bitcoin ATM
      236.06        7 rows  Western Union Agent Location
      168.73        5 rows  Truist
      135.03        4 rows  Coinsource Bitcoin ATM
      135.02        4 rows  Truist Mortgage
      101.22        3 rows  Bank of America
      101.17        3 rows  Wells Fargo
      101.10        3 rows  TitleMax
       67.52        2 rows  Fannie Mae
       67.52        2 rows  HilltopSecurities
       67.52        2 rows  Action Capital Corp
       67.52        2 rows  Grandbridge Real Estate Capital
       67.50        2 rows  Georgia United Credit Union
       67.50        2 rows  Northeast Bonding Co
       67.50        2 rows  Consumer Credit Counseling Service
       67.49        2 rows  Cash America Pawn
       67.48        2 rows  Associated Credit Union
       67.47        2 rows  CoinFlip Bitcoin ATM
       67.47        2 rows  Georgia's Own Credit Union

STATE_NAME by rows
       390  Georgia

STATE_NAME by dollars
       13.2K      390 rows  Georgia

NAICS_ALL by rows
       144  52211001
        21  52316004
        20  81299056
        16  52229202
        14  52391001
        12  52394006
         8  52211002
         7  55111201
         7  52213003
         6  52213003, 52213005
         4  52229103
         4  52211002, 52229202
         4  52394001
         3  52394009
         3  52232003
         3  52211002, 52229103, 52391001, 52394006
         3  52213003, 52213006
         2  52232008
         2  52229108
         2  52421001, 52394006

NAICS_ALL by dollars
        4.9K      144 rows  52211001
      708.49       21 rows  52316004
      675.03       20 rows  81299056
      540.15       16 rows  52229202
      472.58       14 rows  52391001
      405.06       12 rows  52394006
      269.99        8 rows  52211002
      236.27        7 rows  55111201
      236.25        7 rows  52213003
      202.48        6 rows  52213003, 52213005
      135.02        4 rows  52394001
         135        4 rows  52229103
      134.99        4 rows  52211002, 52229202
      101.29        3 rows  52213003, 52213006
      101.28        3 rows  52394009
      101.17        3 rows  52211002, 52229103, 52391001, 52394006
      101.17        3 rows  52232003
       67.53        2 rows  52421001, 52394006
       67.53        2 rows  52394013
       67.52        2 rows  52229108

SIC_ALL by rows
       144  602103
        21  609919
        20  614114
        16  616201
        14  621111
        12  628203
         8  602101
         7  606101
         7  671901
         6  606101, 606298
         4  628202
         4  602101, 616201
         4  614101
         3  628205
         3  602101, 614101, 621111, 628203
         3  609903
         3  606101, 606102
         2  641112, 628203
         2  609902
         2  602101, 601101, 609999, 614101, 628203

SIC_ALL by dollars
        4.9K      144 rows  602103
      708.49       21 rows  609919
      675.03       20 rows  614114
      540.15       16 rows  616201
      472.58       14 rows  621111
      405.06       12 rows  628203
      269.99        8 rows  602101
      236.27        7 rows  671901
      236.25        7 rows  606101
      202.48        6 rows  606101, 606298
      135.02        4 rows  628202
         135        4 rows  614101
      134.99        4 rows  602101, 616201
      101.29        3 rows  606101, 606102
      101.28        3 rows  628205
      101.17        3 rows  602101, 614101, 621111, 628203
      101.17        3 rows  609903
       67.53        2 rows  641112, 628203
       67.53        2 rows  628207
       67.52        2 rows  614108

## who x when

CONAME by CREATIONDATE, dollars = LATITUDE
  ATC Income Tax                            2023:67.46
  ATM                                       2023:4.9K
  Action Capital Corp                       2023:67.52
  Associated Credit Union                   2023:67.48
  Bank of America                           2023:101.22
  Cash America Pawn                         2023:67.49
  Chase                                     2023:67.45
  CoinFlip Bitcoin ATM                      2023:67.47
  Coinsource Bitcoin ATM                    2023:135.03
  Consumer Credit Counseling Service        2023:67.50
  Fannie Mae                                2023:67.52
  Georgia United Credit Union               2023:67.50
  Georgia's Own Credit Union                2023:67.47
  Grandbridge Real Estate Capital           2023:67.52
  HilltopSecurities                         2023:67.52
  LibertyX Bitcoin ATM                      2023:337.32
  Northeast Bonding Co                      2023:67.50
  TitleMax                                  2023:101.10
  Truist                                    2023:168.73
  Truist Mortgage                           2023:135.02
  Wells Fargo                               2023:101.17
  Western Union Agent Location              2023:236.06

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2023:13.2K

## what

ZIP: 30303 48%, 30308 13%, 30311 12%, 30313 7%, 30318 7%, 30310 4%, 30331 4%, 30314 3%, 30315 2%, 30334 1%, 30369 1%, 30343 0%

BRAND: AMEX ATM 40%, STAR,AMEX ATM 23%, Truist ATM 8%, LibertyX Bitcoin ATM 7%, Wells Fargo ATM,AMEX ATM 6%, STAR 3%, STAR,AMEX ATM,Bank Of America  3%, Wells Fargo ATM 3%, Coinsource Bitcoin ATM 3%, STAR,Truist ATM,AMEX ATM 3%, Chase ATM 2%

HQNAME: NCR Corporation 20%, Truist Bank 18%, The Western Union Company 14%, TMX Finance LLC 8%, Bank of America, N.A. 8%, Clark, Sharp & Reynolds LLC 8%, Wells Fargo Bank NA 6%, Associated Credit Union 6%, Kalbas, Inc 4%, Hilltop Securities Inc 4%, Atlanta Life Financial Group 4%

LOC_CONF: Very High 81%, High 16%, Medium 2%, Low 2%

PLACETYPE: Kiosk 42%, Independent 37%, Branch 17%, Headquarters 3%

SQFOOTAGE: 2,500 - 4,999 20%, 5,000 - 9,999 18%, 10,000 - 19,999 18%, 20,000 - 39,999 15%, 1,500 - 2,499 11%, 100,000+ 8%, 40,000 - 99,999 7%, 1 - 1,499 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 389 | 0 | 393 2; 392 2; 391 2; 390 2 |
| CONAME | who | 204 | 0 | ATM 144; LibertyX Bitcoin ATM 10; Western Union Agent Locat 7; Truist 5 |
| ADDR | who | 95 | 12 | Peachtree St NE 56; Peachtree St NW 31; Campbellton Rd SW 27; Peachtree St SW 21 |
| CITY | who | 1 | 0 | Atlanta 390 |
| STATE_NAME | who | 1 | 0 | Georgia 390 |
| STATE | other | 1 | 0 | GA 390 |
| ZIP | category | 16 | 0 | 30303 187; 30308 49; 30311 47; 30313 27 |
| ZIP4 | other | 251 | 29 | 2219 8; 1400 7; 2609 5; 4840 5 |
| NAICS | who | 56 | 0 | 52211001 144; 52211002 23; 52229202 23; 81299056 22 |
| NAICS_ALL | who | 120 | 0 | 52211001 144; 52316004 21; 81299056 20; 52229202 16 |
| SIC | who | 55 | 0 | 602103 144; 602101 23; 616201 23; 614114 22 |
| SIC_ALL | who | 120 | 0 | 602103 144; 609919 21; 614114 20; 616201 16 |
| AFFILIATE | empty | 1 | 390 |  |
| BRAND | category | 29 | 227 | AMEX ATM 57; STAR,AMEX ATM 33; Truist ATM 11; LibertyX Bitcoin ATM 10 |
| HQNAME | category | 47 | 298 | NCR Corporation 10; Truist Bank 9; The Western Union Company 7; TMX Finance LLC 4 |
| LOC_CONF | category | 4 | 0 | Very High 317; High 61; Medium 6; Low 6 |
| PLACETYPE | category | 4 | 0 | Kiosk 165; Independent 145; Branch 68; Headquarters 12 |
| PROFSPEC | empty | 1 | 390 |  |
| SQFOOTAGE | category | 9 | 179 | 2,500 - 4,999 43; 5,000 - 9,999 39; 10,000 - 19,999 37; 20,000 - 39,999 31 |
| EMPNUM | amount | 38 | 0 | nan 165; 4.0 56; 5.0 35; 6.0 24 |
| SALESVOL | amount | 77 | 0 | nan 203; 3067000.0 20; 1422000.0 13; 1777000.0 11 |
| SOURCE | who | 1 | 0 | Data Axle 390 |
| ESRI_PID | other | 394 | 0 | c89994bfc8d50bd37328ad348 2; 1cbf02e3523c3894d5ef59e76 2; 9e7f87dc82c9b0735a1debfd2 2; f30f000078adc89ab304b2d24 2 |
| DESC | who | 1 | 0 | CONAME, Atlanta, Georgia 390 |
| LATITUDE | amount | 242 | 0 | 33.76045800014437 14; 33.760359000202506 12; 33.77086200034552 9; 33.758990999890756 9 |
| LONGITUDE | amount | 249 | 0 | -84.38667300001357 14; -84.3883559999866 12; -84.3861330002384 9; -84.38688450026238 9 |
| CREATIONDATE | date | 1 | 0 | 1703001518978 390 |
| CREATOR | who | 1 | 0 | gpickren2 390 |
| EDITDATE | date | 1 | 0 | 1703001518978 390 |
| EDITOR | who | 1 | 0 | gpickren2 390 |
| GEOMETRY | other | 247 | 0 | {"type": "Point", "coordi 14; {"type": "Point", "coordi 12; {"type": "Point", "coordi 9; {"type": "Point", "coordi 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:23:41.27080 390 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9f1ee8d7-246d-4534-aac7-b 390 |
| SRC_SHA256 | who | 1 | 0 | 7f21707ce80266b96a04003c3 390 |
