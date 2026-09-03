# FED_BIA_TRIBAL_GEO

rows 335  columns 10  scan 3.4s

roles: amount 2, audit 2, other 4, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISACRES | 335 | 1.33 | 7.1K | 5.17M | 23.98M | 126.89M |
| SHAPE__LENGTH | 335 | 0 | 0.38 | 22.70 | 83.45 | 571.69 |

## who

LARNAME by rows
         1  Siletz LAR
         1  Nooksack LAR
         1  Lac du Flambeau LAR
         1  Big Lagoon LAR
         1  Barona LAR
         1  Bridgeport LAR
         1  Buena Vista LAR
         1  Morongo LAR
         1  Cloverdale LAR
         1  San Manuel LAR
         1  Viejas LAR
         1  Susanville LAR
         1  Colusa LAR
         1  Sault Ste. Marie LAR
         1  Alturas LAR
         1  Lac Courte Oreilles LAR
         1  Twenty-Nine Palms LAR
         1  Big Bend LAR
         1  Pechanga LAR
         1  Berry Creek LAR

LARNAME by dollars
      23.98M        1 rows  Navajo LAR
       7.71M        1 rows  Uintah and Ouray LAR
       5.70M        1 rows  Cheyenne River LAR
       5.27M        1 rows  Pine Ridge LAR
       4.99M        1 rows  Crow LAR
       4.84M        1 rows  Standing Rock LAR
       4.78M        1 rows  Fort Peck LAR
       3.90M        1 rows  Wind River LAR
       3.89M        1 rows  Tohono O'odham LAR
       3.51M        1 rows  Blackfeet LAR
       3.15M        1 rows  Colville LAR
       2.89M        1 rows  Flathead LAR
       2.88M        1 rows  Yakama LAR
       2.70M        1 rows  Hopi LAR
       2.67M        1 rows  San Carlos LAR
       2.53M        1 rows  Rosebud LAR
       2.45M        1 rows  Fort Apache LAR
       2.24M        1 rows  Fort Berthold LAR
       1.88M        1 rows  Red Lake LAR
       1.79M        1 rows  Leech Lake LAR

SRC_SHA256 by rows
       335  0e09026c8622556af458f8338b5b84a3c7d66c3c5a4176afc36643ed774170fe

SRC_SHA256 by dollars
     126.89M      335 rows  0e09026c8622556af458f8338b5b84a3c7d66c3c5a4176afc36643ed7741

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 336 | 0 | 335 2; 334 2; 333 2; 332 2 |
| LARID | other | 339 | 0 | LAR0370 2; LAR0369 2; LAR0368 2; LAR0367 2 |
| LARNAME | who | 335 | 0 | Wells LAR 2; Washoe LAR 2; Big Sandy (Truxton Canyon 2; Fort Sill Arizona LAR 2 |
| GISACRES | amount | 339 | 0 | 142.43258141 2; 5547.55129702 2; 970.30740753 2; 5.57371387 2 |
| SHAPE__AREA | other | 329 | 0 | 3.504223468553391e-05 2; 0.0014076860556997417 2; 0.0002597541119939706 2; 1.5447537862200988e-06 2 |
| SHAPE__LENGTH | amount | 338 | 0 | 0.026534720832800483 2; 0.5496573881508112 2; 0.08751291650385425 2; 0.00550146767780194 2 |
| GEOMETRY_JSON | other | 334 | 0 | {"rings": [[[-114.9790564 2; {"rings": [[[-119.8462106 2; {"rings": [[[-113.6348128 2; {"rings": [[[-109.9642014 2 |
| INGESTED_AT | audit | 1 | 0 | 1787755793979815 335 |
| SOURCE_RUN_ID | audit | 1 | 0 | cf67a1e2-419b-4d3e-b476-1 335 |
| SRC_SHA256 | who | 1 | 0 | 0e09026c8622556af458f8338 335 |
