# PORTAL_ARC_OPEN_DATA_MINNEA_7EFDCA0423

rows 2.0K  columns 24  scan 3.3s

roles: amount 2, audit 2, category 4, date 6, id 3, other 5, who 3

## when

REPORTEDDATE
  2017      2.0K  ##############################

BEGINDATE
  2012         1  
  2013         1  
  2014         1  
  2015         2  
  2016         9  
  2017      2.0K  ##############################

ENTEREDDATE
  2017      2.0K  ##############################

LASTCHANGED
  2017      2.0K  ##############################

LASTUPDATEDATE
  2017      2.0K  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 2.0K | -10.39M | -10.38M | -10.38M | 0 | -20.62B |
| Y | 2.0K | 0 | 5.62M | 5.63M | 5.63M | 11.15B |

## who

TIME by rows
       107  00:00:00
        82  22:00:00
        57  21:00:00
        53  18:00:00
        50  12:00:00
        50  23:00:00
        50  20:00:00
        50  19:00:00
        42  17:00:00
        38  08:00:00
        30  10:00:00
        29  15:00:00
        28  14:00:00
        27  01:00:00
        26  13:00:00
        26  22:30:00
        26  09:00:00
        26  16:00:00
        25  00:01:00
        24  02:00:00

TIME by dollars
     -10.38M        1 rows  00:36:00
     -10.38M        1 rows  19:19:00
     -10.38M        1 rows  14:02:00
     -10.38M        1 rows  22:07:00
     -10.38M        1 rows  11:14:00
     -10.38M        1 rows  21:09:00
     -10.38M        1 rows  10:50:00
     -10.38M        1 rows  17:49:00
     -10.38M        1 rows  02:47:00
     -10.38M        1 rows  23:25:00
     -10.38M        1 rows  05:34:00
     -10.38M        1 rows  06:05:00
     -10.38M        1 rows  09:05:00
     -10.38M        1 rows  03:54:00
     -10.38M        1 rows  14:51:00
     -10.38M        1 rows  06:30:00
     -10.38M        1 rows  22:53:00
     -10.38M        1 rows  05:52:00
     -10.38M        1 rows  12:08:00
     -10.38M        1 rows  14:19:00

NEIGHBORHOOD by rows
       201  DOWNTOWN WEST
        93  WHITTIER
        70  JORDAN
        66  MARCY HOLMES
        64  LORING PARK
        56  LONGFELLOW
        52  HAWTHORNE
        51  NEAR - NORTH
        49  LOWRY HILL EAST
        46  NORTH LOOP
        46  CEDAR RIVERSIDE
        41  WILLARD - HAY
        39  CENTRAL
        38  MIDTOWN PHILLIPS
        36  PROSPECT PARK - EAST RIVER ROAD
        35  LYNDALE
        35  ELLIOT PARK
        34  CARAG
        34  WEBBER - CAMDEN
        31  SEWARD

NEIGHBORHOOD by dollars
     -20.76M        2 rows  LOGAN PARK
     -20.76M        2 rows  ST. ANTHONY WEST
     -31.15M        3 rows  COLUMBIA PARK
     -51.91M        5 rows  HALE
     -51.91M        5 rows  MARSHALL TERRACE
     -51.93M        5 rows  LYNNHURST
     -62.26M        6 rows  MID - CITY INDUSTRIAL
     -62.27M        6 rows  KEEWAYDIN
     -62.27M        6 rows  ERICSSON
     -62.29M        6 rows  SHERIDAN
     -62.31M        6 rows  KENNY
     -62.32M        6 rows  KENWOOD
     -62.32M        6 rows  ARMATAGE
     -62.33M        6 rows  BRYN - MAWR
     -72.64M        7 rows  MORRIS PARK
     -72.66M        7 rows  BELTRAMI
     -72.67M        7 rows  ST. ANTHONY EAST
     -72.67M        7 rows  NICOLLET ISLAND - EAST BANK
     -72.68M        7 rows  BOTTINEAU
     -72.68M        7 rows  FIELD

SRC_SHA256 by rows
      2.0K  50f9c37bfce21e8145b503fb127538eedc3adc6f3d7b23af6bff20bb58ec1977

SRC_SHA256 by dollars
     -20.62B     2.0K rows  50f9c37bfce21e8145b503fb127538eedc3adc6f3d7b23af6bff20bb58ec

## who x when

TIME by REPORTEDDATE, dollars = X
  00:00:00                                  2017:-1.10B
  00:01:00                                  2017:-259.56M
  00:36:00                                  2017:-10.38M
  01:00:00                                  2017:-280.32M
  02:00:00                                  2017:-249.21M
  02:47:00                                  2017:-10.38M
  08:00:00                                  2017:-394.57M
  09:00:00                                  2017:-269.93M
  10:00:00                                  2017:-311.50M
  10:50:00                                  2017:-10.38M
  11:14:00                                  2017:-10.38M
  12:00:00                                  2017:-508.74M
  13:00:00                                  2017:-269.95M
  14:00:00                                  2017:-290.70M
  14:02:00                                  2017:-10.38M
  15:00:00                                  2017:-290.73M
  16:00:00                                  2017:-269.95M
  17:00:00                                  2017:-436.06M
  17:49:00                                  2017:-10.38M
  18:00:00                                  2017:-550.29M
  19:00:00                                  2017:-519.15M
  19:19:00                                  2017:-10.38M
  20:00:00                                  2017:-519.14M
  21:00:00                                  2017:-571.02M
  21:09:00                                  2017:-10.38M
  22:00:00                                  2017:-851.38M
  22:07:00                                  2017:-10.38M
  22:30:00                                  2017:-269.94M
  23:00:00                                  2017:-487.98M
  23:25:00                                  2017:-10.38M

NEIGHBORHOOD by REPORTEDDATE, dollars = X
  CARAG                                     2017:-353.11M
  CEDAR RIVERSIDE                           2017:-477.48M
  CENTRAL                                   2017:-404.92M
  COLUMBIA PARK                             2017:-31.15M
  DOWNTOWN WEST                             2017:-2.09B
  ELLIOT PARK                               2017:-363.37M
  ERICSSON                                  2017:-62.27M
  HALE                                      2017:-51.91M
  HAWTHORNE                                 2017:-540.01M
  JORDAN                                    2017:-727.05M
  KEEWAYDIN                                 2017:-62.27M
  LOGAN PARK                                2017:-20.76M
  LONGFELLOW                                2017:-581.20M
  LORING PARK                               2017:-664.57M
  LOWRY HILL EAST                           2017:-508.88M
  LYNDALE                                   2017:-363.44M
  LYNNHURST                                 2017:-51.93M
  MARCY HOLMES                              2017:-685.05M
  MARSHALL TERRACE                          2017:-51.91M
  MID - CITY INDUSTRIAL                     2017:-62.26M
  MIDTOWN PHILLIPS                          2017:-394.49M
  NEAR - NORTH                              2017:-529.66M
  NORTH LOOP                                2017:-477.63M
  PROSPECT PARK - EAST RIVER ROAD           2017:-373.58M
  SEWARD                                    2017:-321.75M
  SHERIDAN                                  2017:-62.29M
  ST. ANTHONY WEST                          2017:-20.76M
  WEBBER - CAMDEN                           2017:-353.11M
  WHITTIER                                  2017:-965.70M
  WILLARD - HAY                             2017:-425.88M

## what

PRECINCT: 03 25%, 05 21%, 01 20%, 04 20%, 02 13%, 99 1%, nan 0%, 18 0%

OFFENSE: THEFT 29%, TFMV 19%, BURGD 15%, AUTOTH 9%, SHOPLF 5%, ROBPAG 4%, BIKETF 4%, ROBPER 4%, BURGB 4%, ASLT2 3%, CSCR 2%, DASTR 2%

DESCRIPTION: Other Theft 29%, Theft From Motr Vehc 19%, Burglary Of Dwelling 15%, Motor Vehicle Theft 9%, Shoplifting 5%, Robbery Per Agg 4%, Bike Theft 4%, Robbery Of Person 4%, Burglary Of Business 4%, Asslt W/dngrs Weapon 3%, Crim Sex Cond-rape 2%, Domestic Assault/Strangulation 2%

UCRCODE: 07 55%, 06 17%, 08 9%, 04 8%, 05 8%, 03 2%, 10 0%, 01 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PUBLICADDRESS | other | 1.5K | 0 | 0025XX Lake ST E 23; 00001X Lake ST W 16; 0014XX Lake ST W 13; 0009XX Nicollet Mall   13 |
| CONTROLNBR | id | 2.0K | 0 | 3686523 10; 3686522 10; 3686520 10; 3686518 10 |
| CCN | id | 2.0K | 0 | MP 2017 234786 10; MP 2017 996622 10; MP 2017 234839 10; MP 2017 234782 10 |
| PRECINCT | category | 8 | 0 | 03 495; 05 427; 01 405; 04 403 |
| REPORTEDDATE | date | 1.9K | 0 | 1499520600000 11; 1499470200000 11; 1499461800000 11; 1499450400000 11 |
| BEGINDATE | date | 1.8K | 0 | 1492898400000 15; 1492905600000 14; 1499464800000 12; 1498244400000 11 |
| TIME | who | 549 | 0 | 00:00:00 107; 22:00:00 82; 21:00:00 57; 18:00:00 53 |
| OFFENSE | category | 26 | 0 | THEFT 525; TFMV 342; BURGD 269; AUTOTH 173 |
| DESCRIPTION | category | 26 | 0 | Other Theft 525; Theft From Motr Vehc 342; Burglary Of Dwelling 269; Motor Vehicle Theft 173 |
| UCRCODE | category | 8 | 0 | 07 1.1K; 06 334; 08 179; 04 168 |
| ENTEREDDATE | date | 2.0K | 0 | 1498339768000 10; 1498339733000 10; 1498338870000 10; 1498338313000 10 |
| GBSID | other | 1.2K | 0 | nan 249; 19097.0 24; 21928.0 16; 0.0 14 |
| LAT | other | 1.4K | 0 | 44.94837171 24; 44.94834704 16; 0.0 14; 44.99913768 13 |
| LONG | other | 1.4K | 0 | -93.23514707 24; -93.27880784 16; 0.0 14; -93.28875577 13 |
| X | amount | 1.4K | 0 | -10378889.0961 24; -10383749.3904 16; 0.0 14; -10384856.7885 13 |
| Y | amount | 1.4K | 0 | 5613397.3273 24; 5613393.4476 16; 0.0 14; 5621385.7319 13 |
| NEIGHBORHOOD | who | 87 | 20 | DOWNTOWN WEST 201; WHITTIER 93; JORDAN 70; MARCY HOLMES 66 |
| LASTCHANGED | date | 2.0K | 0 | 1498357706000 10; 1498339737000 10; 1498354315000 10; 1498353945000 10 |
| LASTUPDATEDATE | date | 34 | 0 | 1495483230000 115; 1496174441000 93; 1502136032000 83; 1499976031000 77 |
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| GEOMETRY | other | 1.4K | 0 | {"type": "Point", "coordi 24; {"type": "Point", "coordi 16; {"type": "Point", "coordi 14; {"type": "Point", "coordi 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:38:02.53163 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2b613728-c0bd-4e62-ad34-f 2.0K |
| SRC_SHA256 | who | 1 | 0 | 50f9c37bfce21e8145b503fb1 2.0K |
