# PORTAL_CKA_ANALYZE_BOSTON_DB29EC5366

rows 10.0K  columns 22  scan 4.8s

roles: amount 5, audit 2, category 5, date 1, empty 2, id 2, other 2, who 4

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NUMBEROF_ST | 10.0K | 0 | 1 | 1 | 17 | 10.0K |
| X_LONGITUDE | 10.0K | -71.17 | -71.07 | -71 | -71 | -710.7K |
| Y_LATITUDE | 10.0K | 42.23 | 42.35 | 42.39 | 42.39 | 423.5K |
| POINT_X | 10.0K | -71.17 | -71.07 | -71 | -71 | -710.7K |
| POINT_Y | 10.0K | 42.23 | 42.35 | 42.39 | 42.39 | 423.5K |

## who

SPP_COM by rows
      2.3K  Honeylocust
       951  Linden, Littleleaf
       584  Pear, Callery
       548  Maple, Red
       438  Maple, Norway
       414  Oak, Pin
       369  Zelkova, Japanese
       337  Ash, Green
       313  Planetree, London
       306  Ginkgo
       271  Elm, Accolade
       218  Oak, Northern Red
       198  Sweetgum, Common
       168  Oak, Swamp White
       168  Basswood, American
       165  Apple/Crabapple
       163  Elm, American
       133  Pagoda Tree, Japanese
       113  Empty Pit/Planting Site
       105  Hackberry, Northern

SPP_COM by dollars
        2.3K     2.3K rows  Honeylocust
         950      951 rows  Linden, Littleleaf
         584      584 rows  Pear, Callery
         548      548 rows  Maple, Red
         438      438 rows  Maple, Norway
         414      414 rows  Oak, Pin
         369      369 rows  Zelkova, Japanese
         367      337 rows  Ash, Green
         313      313 rows  Planetree, London
         306      306 rows  Ginkgo
         270      271 rows  Elm, Accolade
         218      218 rows  Oak, Northern Red
         198      198 rows  Sweetgum, Common
         172      165 rows  Apple/Crabapple
         171      168 rows  Basswood, American
         168      168 rows  Oak, Swamp White
         163      163 rows  Elm, American
         136      133 rows  Pagoda Tree, Japanese
         104      105 rows  Hackberry, Northern
         101      101 rows  Elm, Chinese

SPP_BOT by rows
      2.3K  Gleditsia triacanthos
       942  Tilia cordata
       579  Pyrus calleryana
       546  Acer rubrum
       427  Acer platanoides
       414  Quercus palustris
       366  Zelkova serrata
       336  Fraxinus pennsylvanica
       312  Platanus x acerifolia
       305  Ginkgo biloba
       271  Ulmus carpinifolia 'accolade'
       218  Quercus rubra
       198  Liquidambar styraciflua
       167  Quercus bicolor
       165  Empty Pit/Planting Site
       165  Tilia americana
       163  Malus species
       162  Ulmus americana
       133  Sophora japonica
       105  Celtis occidentalis

SPP_BOT by dollars
        2.3K     2.3K rows  Gleditsia triacanthos
         941      942 rows  Tilia cordata
         579      579 rows  Pyrus calleryana
         546      546 rows  Acer rubrum
         427      427 rows  Acer platanoides
         414      414 rows  Quercus palustris
         366      336 rows  Fraxinus pennsylvanica
         366      366 rows  Zelkova serrata
         312      312 rows  Platanus x acerifolia
         305      305 rows  Ginkgo biloba
         270      271 rows  Ulmus carpinifolia 'accolade'
         218      218 rows  Quercus rubra
         198      198 rows  Liquidambar styraciflua
         170      163 rows  Malus species
         168      165 rows  Tilia americana
         167      167 rows  Quercus bicolor
         162      162 rows  Ulmus americana
         136      133 rows  Sophora japonica
         104      105 rows  Celtis occidentalis
         101      101 rows  Ulmus parvifolia

STREET by rows
       258  Beacon Street
       221  Washington Street
       219  Commonwealth Avenue
       189  Newbury Street
       189  Marlborough Street
       180  Bennington Street
       176  Boylston Street
       168  Main Street
       138  Chelsea Street
       134  Huntington Avenue
       124  Tremont Street
       121  Columbus Avenue
       118  Bunker Hill Street
        99  Chestnut Street
        97  Commercial Street
        95  Sumner Street
        93  Bay State Road
        85  Saratoga Street
        80  Stuart Street
        78  Cambridge Street

STREET by dollars
         257      258 rows  Beacon Street
         221      219 rows  Commonwealth Avenue
         221      221 rows  Washington Street
         207      180 rows  Bennington Street
         188      189 rows  Marlborough Street
         187      189 rows  Newbury Street
         173      176 rows  Boylston Street
         166      168 rows  Main Street
         137      138 rows  Chelsea Street
         134      134 rows  Huntington Avenue
         124      124 rows  Tremont Street
         117      121 rows  Columbus Avenue
         116      118 rows  Bunker Hill Street
          99       99 rows  Chestnut Street
          96       95 rows  Sumner Street
          96       97 rows  Commercial Street
          92       93 rows  Bay State Road
          82       85 rows  Saratoga Street
          80       80 rows  Stuart Street
          76       78 rows  Mount Vernon Street

SRC_SHA256 by rows
     10.0K  f1b55645a6f8f563ee9ce21b1852e50122e8f826019456abdf35ebaf87e6ce2b

SRC_SHA256 by dollars
       10.0K    10.0K rows  f1b55645a6f8f563ee9ce21b1852e50122e8f826019456abdf35ebaf87e6

## who x when

SPP_COM by INGESTED_AT  LOAD STAMP, not an event date, dollars = NUMBEROF_ST
  Apple/Crabapple                           2026:172
  Ash, Green                                2026:367
  Basswood, American                        2026:171
  Elm, Accolade                             2026:270
  Elm, American                             2026:163
  Elm, Chinese                              2026:101
  Empty Pit/Planting Site                   2026:1
  Ginkgo                                    2026:306
  Hackberry, Northern                       2026:104
  Honeylocust                               2026:2.3K
  Linden, Littleleaf                        2026:950
  Maple, Norway                             2026:438
  Maple, Red                                2026:548
  Oak, Northern Red                         2026:218
  Oak, Pin                                  2026:414
  Oak, Swamp White                          2026:168
  Pagoda Tree, Japanese                     2026:136
  Pear, Callery                             2026:584
  Planetree, London                         2026:313
  Sweetgum, Common                          2026:198
  Zelkova, Japanese                         2026:369

SPP_BOT by INGESTED_AT  LOAD STAMP, not an event date, dollars = NUMBEROF_ST
  Acer platanoides                          2026:427
  Acer rubrum                               2026:546
  Celtis occidentalis                       2026:104
  Empty Pit/Planting Site                   2026:52
  Fraxinus pennsylvanica                    2026:366
  Ginkgo biloba                             2026:305
  Gleditsia triacanthos                     2026:2.3K
  Liquidambar styraciflua                   2026:198
  Malus species                             2026:170
  Platanus x acerifolia                     2026:312
  Pyrus calleryana                          2026:579
  Quercus bicolor                           2026:167
  Quercus palustris                         2026:414
  Quercus rubra                             2026:218
  Sophora japonica                          2026:136
  Tilia americana                           2026:168
  Tilia cordata                             2026:941
  Ulmus americana                           2026:162
  Ulmus carpinifolia 'accolade'             2026:270
  Ulmus parvifolia                          2026:101
  Zelkova serrata                           2026:366

## what

DBH_RANGE: 6-12in 27%, 12-18in 22%, 3-6in 22%, 0-3in 17%, 18-24in 8%, N/A 2%, 24-30in 2%, >30in 1%

DBH: 2 21%, 3 11%, 4 11%, 5 8%, 6 8%, 10 7%, 8 6%, 12 6%, 11 6%, 13 6%, 14 6%, 9 5%

DATE_PLANT: -- 91%, Spring 2024 2%, Spring 2025 2%, Fall 2025 1%, Fall 2022 1%, Spring 2023 1%, Spring 2022 1%, Spring 2026 1%, Fall 2024 1%, Fall 2021 0%, Spring 2021 0%, Fall 2020 0%

NEIGHBORHOOD: Back Bay/Beacon Hill 22%, East Boston 19%, Charlestown 15%, Central Boston 15%, South End 6%, Dorchester 5%, Fenway/Longwood 5%, Roxbury 3%, South Boston 3%, Allston-Brighton 3%, West Roxbury 2%, Mattapan 2%

SITE: 1 64%, 2 18%, 3 8%, 4 4%, 5 2%, 6 1%, 7 1%, 8 1%, 9 1%, 10 0%, 11 0%, 12 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 9.9K | 0 | 9210 50; 9209 50; 7914 50; 9208 50 |
| SPP_COM | who | 150 | 0 | Honeylocust 2.3K; Linden, Littleleaf 951; Pear, Callery 584; Maple, Red 548 |
| SPP_BOT | who | 146 | 0 | Gleditsia triacanthos 2.3K; Tilia cordata 942; Pyrus calleryana 579; Acer rubrum 546 |
| NUMBEROF_ST | amount | 9 | 0 | 1.00000000 9.8K; 0.00000000 162; 2.00000000 15; 3.00000000 12 |
| DBH_RANGE | category | 8 | 0 | 6-12in 2.7K; 12-18in 2.2K; 3-6in 2.2K; 0-3in 1.7K |
| DBH | category | 50 | 0 | 2 1.5K; 3 817; 4 812; 5 557 |
| DATE_PLANT | category | 12 | 0 | -- 9.1K; Spring 2024 204; Spring 2025 173; Fall 2025 94 |
| NEIGHBORHOOD | category | 16 | 0 | Back Bay/Beacon Hill 2.1K; East Boston 1.8K; Charlestown 1.5K; Central Boston 1.4K |
| PARK | empty | 1 | 10.0K |  |
| OS_ID | empty | 1 | 10.0K |  |
| ADDRESS | other | 1.0K | 0 | 1 192; 10 129; 20 114; 2 112 |
| STREET | who | 940 | 0 | Beacon Street 258; Washington Street 221; Commonwealth Avenue 219; Marlborough Street 189 |
| SUFFIX | other | 249 | 9.1K | A 224; a 89; b 66; B 37 |
| SITE | category | 26 | 0 | 1 6.3K; 2 1.8K; 3 747; 4 385 |
| X_LONGITUDE | amount | 6.4K | 0 | -71.0985641 52; -71.0853043 51; -71.0785828 51; -71.0628128 51 |
| Y_LATITUDE | amount | 7.4K | 0 | 42.3593102 53; 42.3602409 52; 42.3586273 51; 42.3612175 51 |
| SHAPE_WKT | id | 9.9K | 0 | POINT (-71.14741499999996 50; POINT (-71.14818599999995 50; POINT (-71.05819999999994 50; POINT (-71.15748599999994 50 |
| POINT_X | amount | 7.5K | 0 | -71.08530399999995 51; -71.07857999999999 51; -71.06280999999996 51; -71.09856399999995 51 |
| POINT_Y | amount | 7.4K | 0 | 42.35931000000005 53; 42.36024000000003 52; 42.35862700000007 51; 42.36121700000007 51 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:59:38.19849 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5330f5b3-1c1d-4147-b9d0-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | f1b55645a6f8f563ee9ce21b1 10.0K |
