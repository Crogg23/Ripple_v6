# PORTAL_ARC_HARRIS_COUNTY_OP_58FAB3B4F7

rows 1.0K  columns 15  scan 4.8s

roles: amount 2, audit 2, category 1, date 1, id 7, who 3

## when

INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 1.0K | 0 | 0.04 | 0.45 | 1.19 | 65.97 |
| SHAPE__LENGTH | 1.0K | 0.05 | 1.28 | 3.88 | 5.11 | 1.5K |

## who

NAME2 by rows
         2  nan
         1  Ranger
         1  Denison
         1  Ennis
         1  Klondike
         1  Sanford-Fritch
         1  Paint Creek
         1  Pringle-Morse Cons
         1  De Leon
         1  Eastland
         1  Ezzell
         1  Leveretts Chapel
         1  Grandfalls-Royalty
         1  Jonesboro
         1  Huckabay
         1  Trinity
         1  Blackwell Cons
         1  Dalhart
         1  Trent
         1  Bronte

NAME2 by dollars
        1.19        1 rows  Culberson County-Allamore
        0.74        1 rows  Marfa
        0.74        1 rows  Fort Stockton
        0.68        1 rows  Crockett County Cons CSD
        0.59        1 rows  United
        0.57        1 rows  Terrell County
        0.56        1 rows  Pecos-Barstow-Toyah
        0.56        1 rows  Comstock
        0.49        1 rows  Marathon
        0.46        1 rows  Alpine
        0.46        1 rows  Kenedy County-Wide CSD
        0.42        1 rows  Fort Hancock
        0.39        1 rows  Rocksprings
        0.37        1 rows  San Vicente
        0.37        1 rows  Andrews
        0.35        1 rows  Channing
        0.35        1 rows  Sonora
        0.33        1 rows  Brackett
        0.33        1 rows  Fort Davis
        0.33        1 rows  Cotulla

NAME by rows
         2  Abilene ISD
         2  Abbott ISD
         1  Hico ISD
         1  Palmer ISD
         1  Nursery ISD
         1  Cushing ISD
         1  Bells ISD
         1  Dilley ISD
         1  Dimmitt ISD
         1  Hamilton ISD
         1  Van Vleck ISD
         1  Marfa ISD
         1  Anson ISD
         1  Sweet Home ISD
         1  Montague ISD
         1  Bronte ISD
         1  Laneville ISD
         1  Nocona ISD
         1  Tarkington ISD
         1  Springlake-Earth ISD

NAME by dollars
        1.19        1 rows  Culberson County-Allamore ISD
        0.74        1 rows  Marfa ISD
        0.74        1 rows  Fort Stockton ISD
        0.68        1 rows  Crockett County Cons CSD
        0.59        1 rows  United ISD
        0.57        1 rows  Terrell County ISD
        0.56        1 rows  Comstock ISD
        0.56        1 rows  Pecos-Barstow-Toyah ISD
        0.49        1 rows  Marathon ISD
        0.46        1 rows  Alpine ISD
        0.46        1 rows  Kenedy County-Wide CSD
        0.42        1 rows  Fort Hancock ISD
        0.39        1 rows  Rocksprings ISD
        0.37        1 rows  San Vicente ISD
        0.37        1 rows  Andrews ISD
        0.35        1 rows  Channing ISD
        0.35        1 rows  Sonora ISD
        0.33        1 rows  Fort Davis ISD
        0.33        1 rows  Brackett ISD
        0.33        1 rows  Cotulla ISD

SRC_SHA256 by rows
      1.0K  f22316851c6e3c437508414b40eb21cddcecd97ff3e7969705107512281fa572

SRC_SHA256 by dollars
       65.97     1.0K rows  f22316851c6e3c437508414b40eb21cddcecd97ff3e7969705107512281f

## who x when

NAME2 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Alpine                                    2026:0.46
  Blackwell Cons                            2026:0.12
  Bronte                                    2026:0.08
  Comstock                                  2026:0.56
  Crockett County Cons CSD                  2026:0.68
  Culberson County-Allamore                 2026:1.19
  Dalhart                                   2026:0.22
  De Leon                                   2026:0.06
  Denison                                   2026:0.02
  Eastland                                  2026:0.06
  Ennis                                     2026:0.06
  Ezzell                                    2026:0.04
  Fort Stockton                             2026:0.74
  Grandfalls-Royalty                        2026:0.04
  Huckabay                                  2026:0.04
  Jonesboro                                 2026:0.04
  Klondike                                  2026:0.14
  Leveretts Chapel                          2026:0
  Marathon                                  2026:0.49
  Marfa                                     2026:0.74
  Paint Creek                               2026:0.06
  Pecos-Barstow-Toyah                       2026:0.56
  Pringle-Morse Cons                        2026:0.10
  Ranger                                    2026:0.05
  Sanford-Fritch                            2026:0.01
  Terrell County                            2026:0.57
  Trent                                     2026:0.04
  Trinity                                   2026:0.04
  United                                    2026:0.59
  nan                                       2026:0.05

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Abbott ISD                                2026:0.02
  Abilene ISD                               2026:0.08
  Alpine ISD                                2026:0.46
  Anson ISD                                 2026:0.07
  Bells ISD                                 2026:0.01
  Bronte ISD                                2026:0.08
  Comstock ISD                              2026:0.56
  Crockett County Cons CSD                  2026:0.68
  Culberson County-Allamore ISD             2026:1.19
  Cushing ISD                               2026:0.04
  Dilley ISD                                2026:0.08
  Dimmitt ISD                               2026:0.11
  Fort Stockton ISD                         2026:0.74
  Hamilton ISD                              2026:0.13
  Hico ISD                                  2026:0.05
  Kenedy County-Wide CSD                    2026:0.46
  Laneville ISD                             2026:0.03
  Marathon ISD                              2026:0.49
  Marfa ISD                                 2026:0.74
  Montague ISD                              2026:0.01
  Nocona ISD                                2026:0.04
  Nursery ISD                               2026:0.01
  Palmer ISD                                2026:0.01
  Pecos-Barstow-Toyah ISD                   2026:0.56
  Springlake-Earth ISD                      2026:0.05
  Sweet Home ISD                            2026:0.02
  Tarkington ISD                            2026:0.06
  Terrell County ISD                        2026:0.57
  United ISD                                2026:0.59
  Van Vleck ISD                             2026:0.11

## what

COLOR: 6 15%, 3 15%, 1 15%, 2 14%, 4 14%, 7 13%, 5 13%, 0 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.0K | 0 | 1000 2; 999 2; 998 2; 997 2 |
| SDLEA10 | id | 1.0K | 0 | nan 3; 17070 2; 16410 2; 09450 2 |
| NAME | who | 1.0K | 0 | Clear Creek ISD 2; Dickinson ISD 2; Dayton ISD 2; Barbers Hill ISD 2 |
| NAME2 | who | 1.0K | 0 | nan 3; Dickinson 2; Dayton 2; Barbers Hill 2 |
| DISTRICT_N | id | 1.0K | 0 | 0 3; 84901 2; 146902 2; 36902 2 |
| DISTRICT | id | 1.0K | 0 | nan 3; 084-901 2; 146-902 2; 036-902 2 |
| DISTRICT_C | id | 1.0K | 0 | nan 3; 084901 2; 146902 2; 036902 2 |
| NCES_DISTR | id | 1.0K | 0 | nan 3; 4817070 2; 4816410 2; 4809450 2 |
| COLOR | category | 8 | 0 | 6 158; 3 152; 1 151; 2 147 |
| SHAPE__AREA | amount | 1.0K | 0 | 0.02542443780703252 2; 0.022323274778045743 2; 0.06346264903663723 2; 0.04684164443551708 2 |
| SHAPE__LENGTH | amount | 1.0K | 0 | 1.206494831712251 2; 0.9865897242332982 2; 1.7398294485500438 2; 1.806004453374775 2 |
| GEOMETRY | id | 1.0K | 0 | {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2; {"type": "MultiPolygon",  2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:28:49.28865 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2490e413-37c8-44ba-9bc1-4 1.0K |
| SRC_SHA256 | who | 1 | 0 | f22316851c6e3c437508414b4 1.0K |
