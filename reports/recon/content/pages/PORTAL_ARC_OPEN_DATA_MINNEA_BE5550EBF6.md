# PORTAL_ARC_OPEN_DATA_MINNEA_BE5550EBF6

rows 2.0K  columns 24  scan 3.6s

roles: amount 2, audit 2, category 4, date 6, id 3, other 4, who 4

## when

REPORTEDDATE
  2014      2.0K  ##############################

BEGINDATE
  2010         1  
  2011         3  
  2012         1  
  2013       135  ##
  2014      1.9K  ##############################

ENTEREDDATE
  2014      2.0K  ##############################

LASTCHANGED
  2014      2.0K  ##############################
  2015        17  
  2016         3  

LASTUPDATEDATE
  2017      2.0K  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 2.0K | -10.39M | -10.38M | -10.38M | 0 | -20.76B |
| Y | 2.0K | 0 | 5.62M | 5.63M | 5.63M | 11.23B |

## who

TIME by rows
       121  00:00:00
        60  18:00:00
        59  19:00:00
        48  20:00:00
        48  12:00:00
        46  22:00:00
        42  08:00:00
        42  17:00:00
        39  16:00:00
        38  15:00:00
        36  23:00:00
        35  10:00:00
        33  09:00:00
        29  13:00:00
        28  21:00:00
        27  14:00:00
        27  01:00:00
        26  02:00:00
        25  17:30:00
        20  00:01:00

TIME by dollars
     -10.38M        1 rows  16:14:00
     -10.38M        1 rows  12:53:00
     -10.38M        1 rows  00:25:00
     -10.38M        1 rows  04:41:00
     -10.38M        1 rows  23:50:00
     -10.38M        1 rows  06:26:00
     -10.38M        1 rows  21:41:00
     -10.38M        1 rows  10:42:00
     -10.38M        1 rows  18:49:00
     -10.38M        1 rows  20:50:00
     -10.38M        1 rows  00:22:00
     -10.38M        1 rows  00:06:00
     -10.38M        1 rows  14:56:00
     -10.38M        1 rows  20:02:00
     -10.38M        1 rows  21:38:00
     -10.38M        1 rows  13:24:00
     -10.38M        1 rows  22:04:00
     -10.38M        1 rows  03:54:00
     -10.38M        1 rows  18:17:00
     -10.38M        1 rows  20:24:00

NEIGHBORHOOD by rows
       317  DOWNTOWN WEST
        66  WHITTIER
        64  JORDAN
        63  NEAR - NORTH
        54  FOLWELL
        52  HAWTHORNE
        49  POWDERHORN PARK
        49  ELLIOT PARK
        46  LONGFELLOW
        46  VENTURA VILLAGE
        45  MIDTOWN PHILLIPS
        44  LORING PARK
        43  WILLARD - HAY
        42  LOWRY HILL EAST
        41  CENTRAL
        40  NORTH LOOP
        36  WEBBER - CAMDEN
        36  SEWARD
        36  CEDAR RIVERSIDE
        34  LYNDALE

NEIGHBORHOOD by dollars
     -10.38M        1 rows  MORRIS PARK
     -10.39M        1 rows  KENNY
     -10.39M        1 rows  HUMBOLDT INDUSTRIAL AREA
     -20.76M        2 rows  FIELD
     -20.78M        2 rows  WEST CALHOUN
     -31.14M        3 rows  HALE
     -31.15M        3 rows  MARSHALL TERRACE
     -31.15M        3 rows  PAGE
     -41.52M        4 rows  COLUMBIA PARK
     -41.53M        4 rows  SHERIDAN
     -41.54M        4 rows  CAMDEN INDUSTRIAL
     -41.55M        4 rows  BRYN - MAWR
     -51.91M        5 rows  ST. ANTHONY WEST
     -62.29M        6 rows  BOTTINEAU
     -62.31M        6 rows  LOWRY HILL
     -62.32M        6 rows  ARMATAGE
     -72.63M        7 rows  COOPER
     -72.65M        7 rows  MID - CITY INDUSTRIAL
     -72.65M        7 rows  UNIVERSITY OF MINNESOTA
     -72.66M        7 rows  BELTRAMI

GBSID by rows
       226  nan
        38  21934.0
        37  19563.0
        16  21933.0
        12  11281.0
        11  25831.0
        11  14827.0
        11  21511.0
        10  19097.0
         9  19096.0
         8  16640.0
         8  17562.0
         8  17361.0
         8  25669.0
         8  21928.0
         8  17250.0
         8  16534.0
         7  17317.0
         7  22383.0
         7  21654.0

GBSID by dollars
           0        1 rows  0.0
     -10.38M        1 rows  14714.0
     -10.38M        1 rows  22569.0
     -10.38M        1 rows  20138.0
     -10.38M        1 rows  22329.0
     -10.38M        1 rows  14293.0
     -10.38M        1 rows  11096.0
     -10.38M        1 rows  17537.0
     -10.38M        1 rows  25335.0
     -10.38M        1 rows  11866.0
     -10.38M        1 rows  10308.0
     -10.38M        1 rows  13068.0
     -10.38M        1 rows  12266.0
     -10.38M        1 rows  12483.0
     -10.38M        1 rows  22054.0
     -10.38M        1 rows  13211.0
     -10.38M        1 rows  19878.0
     -10.38M        1 rows  22564.0
     -10.38M        1 rows  13710.0
     -10.38M        1 rows  12499.0

SRC_SHA256 by rows
      2.0K  b6f89a7030bc2a88b786950530ff0e6b9cd09a5e2817a35734209ba95792c003

SRC_SHA256 by dollars
     -20.76B     2.0K rows  b6f89a7030bc2a88b786950530ff0e6b9cd09a5e2817a35734209ba95792

## who x when

TIME by REPORTEDDATE, dollars = X
  00:00:00                                  2014:-1.26B
  00:01:00                                  2014:-207.66M
  00:25:00                                  2014:-10.38M
  01:00:00                                  2014:-280.30M
  02:00:00                                  2014:-269.96M
  04:41:00                                  2014:-10.38M
  06:26:00                                  2014:-10.38M
  08:00:00                                  2014:-436.06M
  09:00:00                                  2014:-342.61M
  10:00:00                                  2014:-363.43M
  10:42:00                                  2014:-10.38M
  12:00:00                                  2014:-498.36M
  12:53:00                                  2014:-10.38M
  13:00:00                                  2014:-301.09M
  14:00:00                                  2014:-280.33M
  15:00:00                                  2014:-394.57M
  16:00:00                                  2014:-404.90M
  16:14:00                                  2014:-10.38M
  17:00:00                                  2014:-436.04M
  17:30:00                                  2014:-259.59M
  18:00:00                                  2014:-622.97M
  18:49:00                                  2014:-10.38M
  19:00:00                                  2014:-612.60M
  20:00:00                                  2014:-498.39M
  20:50:00                                  2014:-10.38M
  21:00:00                                  2014:-290.76M
  21:41:00                                  2014:-10.38M
  22:00:00                                  2014:-477.60M
  23:00:00                                  2014:-373.79M
  23:50:00                                  2014:-10.38M

NEIGHBORHOOD by REPORTEDDATE, dollars = X
  CEDAR RIVERSIDE                           2014:-373.68M
  CENTRAL                                   2014:-425.69M
  COLUMBIA PARK                             2014:-41.52M
  DOWNTOWN WEST                             2014:-3.29B
  ELLIOT PARK                               2014:-508.72M
  FIELD                                     2014:-20.76M
  FOLWELL                                   2014:-560.86M
  HALE                                      2014:-31.14M
  HAWTHORNE                                 2014:-540.02M
  HUMBOLDT INDUSTRIAL AREA                  2014:-10.39M
  JORDAN                                    2014:-664.72M
  KENNY                                     2014:-10.39M
  LONGFELLOW                                2014:-477.41M
  LORING PARK                               2014:-456.89M
  LOWRY HILL EAST                           2014:-436.18M
  LYNDALE                                   2014:-353.06M
  MARSHALL TERRACE                          2014:-31.15M
  MIDTOWN PHILLIPS                          2014:-467.17M
  MORRIS PARK                               2014:-10.38M
  NEAR - NORTH                              2014:-654.29M
  NORTH LOOP                                2014:-415.34M
  PAGE                                      2014:-31.15M
  POWDERHORN PARK                           2014:-508.67M
  SEWARD                                    2014:-373.64M
  SHERIDAN                                  2014:-41.53M
  VENTURA VILLAGE                           2014:-477.56M
  WEBBER - CAMDEN                           2014:-373.88M
  WEST CALHOUN                              2014:-20.78M
  WHITTIER                                  2014:-685.33M
  WILLARD - HAY                             2014:-446.65M

## what

PRECINCT: 03 26%, 01 25%, 04 22%, 05 17%, 02 11%, 18 0%

OFFENSE: THEFT 35%, BURGD 17%, TFMV 15%, AUTOTH 8%, SHOPLF 6%, ROBPAG 5%, BURGB 4%, ROBPER 3%, ASLT2 3%, CSCR 2%, DASTR 2%, THFTSW 1%

DESCRIPTION: Other Theft 35%, Burglary Of Dwelling 17%, Theft From Motr Vehc 15%, Motor Vehicle Theft 8%, Shoplifting 6%, Robbery Per Agg 5%, Burglary Of Business 4%, Robbery Of Person 3%, Asslt W/dngrs Weapon 3%, Crim Sex Cond-rape 2%, Domestic Assault/Strangulation 2%, Theft By Swindle 1%

UCRCODE: 07 56%, 06 20%, 08 8%, 04 7%, 05 7%, 03 2%, 10 0%, 01 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PUBLICADDRESS | other | 1.4K | 0 | 0009XX Nicollet Mall   35; 0007XX Nicollet Mall   33; 0006XX Nicollet Mall   16; 0028XX 26 AV S 13 |
| CONTROLNBR | id | 2.0K | 0 | 3252307 10; 3252188 10; 3252158 10; 3252105 10 |
| CCN | id | 2.0K | 0 | MP 2014 045642 10; MP 2014 045604 10; MP 2014 045569 10; MP 2014 045443 10 |
| PRECINCT | category | 6 | 0 | 03 515; 01 497; 04 431; 05 334 |
| REPORTEDDATE | date | 2.0K | 0 | 1392046200000 11; 1392037200000 11; 1392150120000 10; 1392146460000 10 |
| BEGINDATE | date | 1.7K | 0 | 1391457600000 13; 1391904000000 12; 1391713200000 12; 1392055200000 12 |
| TIME | who | 539 | 0 | 00:00:00 121; 18:00:00 60; 19:00:00 59; 20:00:00 48 |
| OFFENSE | category | 29 | 0 | THEFT 640; BURGD 316; TFMV 280; AUTOTH 157 |
| DESCRIPTION | category | 29 | 0 | Other Theft 640; Burglary Of Dwelling 316; Theft From Motr Vehc 280; Motor Vehicle Theft 157 |
| UCRCODE | category | 8 | 0 | 07 1.1K; 06 391; 08 162; 04 149 |
| ENTEREDDATE | date | 2.0K | 0 | 1392072260000 11; 1392150123000 10; 1392146439000 10; 1392145180000 10 |
| GBSID | who | 1.1K | 0 | nan 226; 21934.0 38; 19563.0 37; 21933.0 16 |
| LAT | other | 1.3K | 0 | 44.97641969 38; 44.97449942 37; 44.97736687 16; 44.95108135 13 |
| LONG | other | 1.3K | 0 | -93.27268029 38; -93.27431687 37; -93.2717965 16; -93.2347243 13 |
| X | amount | 1.3K | 0 | -10383067.275 38; -10383249.4581 37; -10382968.892 16; -10378842.0334 13 |
| Y | amount | 1.3K | 0 | 5617810.0129 38; 5617507.8346 37; 5617959.0665 16; 5613823.5304 13 |
| NEIGHBORHOOD | who | 87 | 3 | DOWNTOWN WEST 317; WHITTIER 66; JORDAN 64; NEAR - NORTH 63 |
| LASTCHANGED | date | 2.0K | 0 | 1392293691000 10; 1392184081000 10; 1392156749000 10; 1392294479000 10 |
| LASTUPDATEDATE | date | 1 | 0 | 1488548406000 2.0K |
| ESRI_OID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| GEOMETRY | other | 1.4K | 0 | {"type": "Point", "coordi 38; {"type": "Point", "coordi 37; {"type": "Point", "coordi 16; {"type": "Point", "coordi 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:37:40.71451 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 98d39331-ed24-4f4c-9b0c-2 2.0K |
| SRC_SHA256 | who | 1 | 0 | b6f89a7030bc2a88b78695053 2.0K |
