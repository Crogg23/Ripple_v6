# PORTAL_ARC_HARRIS_COUNTY_OP_89477F0032

rows 1.0K  columns 15  scan 4.1s

roles: amount 2, audit 2, category 1, date 1, id 7, who 3

## when

INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 1.0K | 13.83M | 4.28B | 52.23B | 135.67B | 7513.07B |
| SHAPE__LENGTH | 1.0K | 15.0K | 430.3K | 1.32M | 1.71M | 488.23M |

## who

NAME2 by rows
         2  nan
         1  Sweet Home
         1  Presidio
         1  Whitesboro
         1  Gordon
         1  Crockett County Cons CSD
         1  Shiner
         1  Miles
         1  Borger
         1  Midland
         1  Marathon
         1  Huckabay
         1  Sonora
         1  Mullin
         1  Eastland
         1  Pecos-Barstow-Toyah
         1  Leveretts Chapel
         1  Dawson (Dawson)
         1  Stamford
         1  Paint Creek

NAME2 by dollars
     135.67B        1 rows  Culberson County-Allamore
      84.94B        1 rows  Marfa
      84.46B        1 rows  Fort Stockton
      78.29B        1 rows  Crockett County Cons CSD
      69.41B        1 rows  United
      65.74B        1 rows  Terrell County
      64.33B        1 rows  Comstock
      63.18B        1 rows  Pecos-Barstow-Toyah
      56.61B        1 rows  Marathon
      54.13B        1 rows  Kenedy County-Wide CSD
      53.42B        1 rows  Alpine
      47.74B        1 rows  Fort Hancock
      45.32B        1 rows  Rocksprings
      43.32B        1 rows  San Vicente
      41.95B        1 rows  Andrews
      40.55B        1 rows  Sonora
      38.85B        1 rows  Cotulla
      38.09B        1 rows  Fort Davis
      38.05B        1 rows  Brackett
      38.02B        1 rows  Channing

NAME by rows
         2  Abilene ISD
         2  Abbott ISD
         1  Saint Jo ISD
         1  Buna ISD
         1  Dimmitt ISD
         1  Lovelady ISD
         1  Hico ISD
         1  Wharton ISD
         1  Garrison ISD
         1  Morgan Mill ISD
         1  Matagorda ISD
         1  Como-Pickton Cons ISD
         1  Grady ISD
         1  Latexo ISD
         1  Stephenville ISD
         1  Turkey-Quitaque ISD
         1  Floresville ISD
         1  Tidehaven ISD
         1  Ore City ISD
         1  Avinger ISD

NAME by dollars
     135.67B        1 rows  Culberson County-Allamore ISD
      84.94B        1 rows  Marfa ISD
      84.46B        1 rows  Fort Stockton ISD
      78.29B        1 rows  Crockett County Cons CSD
      69.41B        1 rows  United ISD
      65.74B        1 rows  Terrell County ISD
      64.33B        1 rows  Comstock ISD
      63.18B        1 rows  Pecos-Barstow-Toyah ISD
      56.61B        1 rows  Marathon ISD
      54.13B        1 rows  Kenedy County-Wide CSD
      53.42B        1 rows  Alpine ISD
      47.74B        1 rows  Fort Hancock ISD
      45.32B        1 rows  Rocksprings ISD
      43.32B        1 rows  San Vicente ISD
      41.95B        1 rows  Andrews ISD
      40.55B        1 rows  Sonora ISD
      38.85B        1 rows  Cotulla ISD
      38.09B        1 rows  Fort Davis ISD
      38.05B        1 rows  Brackett ISD
      38.02B        1 rows  Channing ISD

SRC_SHA256 by rows
      1.0K  e07b1a7dcebd9dbc9862da6723b6583b3ac77542d8bb4082c0134e81616c2cad

SRC_SHA256 by dollars
    7513.07B     1.0K rows  e07b1a7dcebd9dbc9862da6723b6583b3ac77542d8bb4082c0134e81616c

## who x when

NAME2 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Alpine                                    2026:53.42B
  Borger                                    2026:1.36B
  Comstock                                  2026:64.33B
  Crockett County Cons CSD                  2026:78.29B
  Culberson County-Allamore                 2026:135.67B
  Dawson (Dawson)                           2026:3.86B
  Eastland                                  2026:7.21B
  Fort Hancock                              2026:47.74B
  Fort Stockton                             2026:84.46B
  Gordon                                    2026:4.55B
  Huckabay                                  2026:4.42B
  Kenedy County-Wide CSD                    2026:54.13B
  Leveretts Chapel                          2026:327.73M
  Marathon                                  2026:56.61B
  Marfa                                     2026:84.94B
  Midland                                   2026:21.70B
  Miles                                     2026:3.95B
  Mullin                                    2026:6.98B
  Paint Creek                               2026:6.58B
  Pecos-Barstow-Toyah                       2026:63.18B
  Presidio                                  2026:22.54B
  Rocksprings                               2026:45.32B
  Shiner                                    2026:3.16B
  Sonora                                    2026:40.55B
  Stamford                                  2026:3.89B
  Sweet Home                                2026:1.77B
  Terrell County                            2026:65.74B
  United                                    2026:69.41B
  Whitesboro                                2026:4.85B
  nan                                       2026:6.01B

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Abbott ISD                                2026:2.11B
  Abilene ISD                               2026:8.98B
  Avinger ISD                               2026:1.97B
  Buna ISD                                  2026:6.13B
  Como-Pickton Cons ISD                     2026:3.39B
  Comstock ISD                              2026:64.33B
  Crockett County Cons CSD                  2026:78.29B
  Culberson County-Allamore ISD             2026:135.67B
  Dimmitt ISD                               2026:12.57B
  Floresville ISD                           2026:7.82B
  Fort Stockton ISD                         2026:84.46B
  Garrison ISD                              2026:3.00B
  Grady ISD                                 2026:8.60B
  Hico ISD                                  2026:5.70B
  Kenedy County-Wide CSD                    2026:54.13B
  Latexo ISD                                2026:2.69B
  Lovelady ISD                              2026:9.10B
  Marathon ISD                              2026:56.61B
  Marfa ISD                                 2026:84.94B
  Matagorda ISD                             2026:3.99B
  Morgan Mill ISD                           2026:2.08B
  Ore City ISD                              2026:1.96B
  Pecos-Barstow-Toyah ISD                   2026:63.18B
  Saint Jo ISD                              2026:4.63B
  Stephenville ISD                          2026:6.54B
  Terrell County ISD                        2026:65.74B
  Tidehaven ISD                             2026:8.20B
  Turkey-Quitaque ISD                       2026:12.60B
  United ISD                                2026:69.41B
  Wharton ISD                               2026:5.11B

## what

COLOR: 6 15%, 3 15%, 1 15%, 2 14%, 4 14%, 7 13%, 5 13%, 0 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.0K | 0 | 490 2; 489 2; 488 2; 487 2 |
| SDLEA10 | id | 1.0K | 0 | nan 3; 36780 2; 40410 2; 42690 2 |
| NAME | who | 1.0K | 0 | Abilene ISD 3; Skidmore-Tynan ISD 2; Three Rivers ISD 2; Pawnee ISD 2 |
| NAME2 | who | 1.0K | 0 | nan 3; Refugio 2; Skidmore-Tynan 2; Three Rivers 2 |
| DISTRICT_N | id | 1.0K | 0 | 0 3; 196903 2; 13905 2; 149902 2 |
| DISTRICT | id | 1.0K | 0 | nan 3; 196-903 2; 013-905 2; 149-902 2 |
| DISTRICT_C | id | 1.0K | 0 | nan 3; 196903 2; 013905 2; 149902 2 |
| NCES_DISTR | id | 1.0K | 0 | nan 3; 4836780 2; 4840410 2; 4842690 2 |
| COLOR | category | 8 | 0 | 6 158; 3 152; 1 151; 2 147 |
| SHAPE__AREA | amount | 1.0K | 0 | 7103571431.904297 2; 12415011703.728516 2; 4210837640.419922 2; 1821921904.140625 2 |
| SHAPE__LENGTH | amount | 1.0K | 0 | 584431.6711895681 2; 662954.1059787485 2; 426725.1435281382 2; 271991.65714206995 2 |
| GEOMETRY | id | 1.0K | 0 | {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:27:32.44041 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5c051ba5-6d3d-4cb2-9cfc-6 1.0K |
| SRC_SHA256 | who | 1 | 0 | e07b1a7dcebd9dbc9862da672 1.0K |
