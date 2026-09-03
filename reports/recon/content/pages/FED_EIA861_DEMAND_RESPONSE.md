# FED_EIA861_DEMAND_RESPONSE

rows 340  columns 39  scan 5.2s

roles: amount 24, audit 2, category 8, date 1, other 1, state 1, who 3

## when

_INGESTED_AT
  2026       340  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| UNNAMED_6 | 339 | 0 | 7 | 16.1K | 19.8K | 249.2K |
| UNNAMED_7 | 339 | 0 | 0 | 2.1K | 4.7K | 43.6K |
| UNNAMED_9 | 339 | 0 | 2.4K | 565.7K | 938.0K | 10.95M |
| ENERGY_SAVINGS_MWH | 339 | 0 | 0 | 23.4K | 80.6K | 248.0K |
| UNNAMED_11 | 339 | 0 | 0 | 6.0K | 10.2K | 88.1K |
| UNNAMED_12 | 339 | 0 | 0 | 4.0K | 33.2K | 73.4K |

## who

UNNAMED_2 by rows
         7  Tennessee Valley Authority
         4  Wabash Valley Power Assn, Inc
         3  PacifiCorp
         3  Midwest Energy Cooperative - (MI)
         3  Northern States Power Co - Minnesota
         3  Otter Tail Power Co
         2  Evergy Metro
         2  Indiana Michigan Power Co
         2  Tri-County Electric Coop, Inc (OK)
         2  MidAmerican Energy Co
         2  MiEnergy Cooperative
         2  Oklahoma Gas & Electric Co
         2  Montana-Dakota Utilities Co
         2  Idaho Power Co
         2  Duke Energy Progress - (NC)
         2  El Paso Electric Co
         2  Virginia Electric & Power Co
         2  Delmarva Power
         2  Highline Electric Assn
         2  Potomac Electric Power Co

UNNAMED_2 by dollars
       21.0K        3 rows  Northern States Power Co - Minnesota
       19.5K        2 rows  Delmarva Power
       19.3K        2 rows  El Paso Electric Co
       18.3K        1 rows  San Diego Gas & Electric Co
       17.3K        1 rows  Florida Power & Light Co
       15.7K        2 rows  Oklahoma Gas & Electric Co
       10.4K        1 rows  Great River Energy
        9.5K        1 rows  Hart Electric Member Corp
        9.5K        1 rows  United Electric Coop Service Inc - (TX)
        9.4K        1 rows  Choctawhatche Elec Coop, Inc
        9.3K        1 rows  Public Service Co of NM
        8.5K        2 rows  Duke Energy Carolinas, LLC
        7.2K        2 rows  Potomac Electric Power Co
        6.6K        1 rows  Consolidated Edison Co-NY Inc
        6.2K        1 rows  Southern California Edison Co
        4.7K        2 rows  Duke Energy Progress - (NC)
        4.4K        1 rows  Snapping Shoals El Member Corp
        4.1K        1 rows  Alameda Municipal Power
        3.9K        3 rows  Otter Tail Power Co
        3.3K        1 rows  Duke Energy Indiana, LLC

UNNAMED_1 by rows
         7  18642
         4  40211
         3  14354
         3  13781
         3  12377
         3  14232
         2  3046
         2  5416
         2  733
         2  19157
         2  14063
         2  5027
         2  9324
         2  19160
         2  12199
         2  5701
         2  10000
         2  9191
         2  15270
         2  19876

UNNAMED_1 by dollars
       21.0K        3 rows  13781
       19.5K        2 rows  5027
       19.3K        2 rows  5701
       18.3K        1 rows  16609
       17.3K        1 rows  6452
       15.7K        2 rows  14063
       10.4K        1 rows  7570
        9.5K        1 rows  8210
        9.5K        1 rows  19490
        9.4K        1 rows  3502
        9.3K        1 rows  15473
        8.5K        2 rows  5416
        7.2K        2 rows  15270
        6.6K        1 rows  4226
        6.2K        1 rows  17609
        4.7K        2 rows  3046
        4.4K        1 rows  17832
        4.1K        1 rows  207
        3.9K        3 rows  14232
        3.3K        1 rows  15470

_SRC_FILE by rows
       340  Demand_Response_2024.xlsx

_SRC_FILE by dollars
      249.2K      340 rows  Demand_Response_2024.xlsx

## who x when

UNNAMED_2 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = UNNAMED_6
  Choctawhatche Elec Coop, Inc              2026:9.4K
  Consolidated Edison Co-NY Inc             2026:6.6K
  Delmarva Power                            2026:19.5K
  Duke Energy Carolinas, LLC                2026:8.5K
  Duke Energy Progress - (NC)               2026:4.7K
  El Paso Electric Co                       2026:19.3K
  Evergy Metro                              2026:273
  Florida Power & Light Co                  2026:17.3K
  Great River Energy                        2026:10.4K
  Hart Electric Member Corp                 2026:9.5K
  Highline Electric Assn                    2026:0
  Idaho Power Co                            2026:309
  Indiana Michigan Power Co                 2026:111
  MiEnergy Cooperative                      2026:638
  MidAmerican Energy Co                     2026:12
  Midwest Energy Cooperative - (MI)         2026:494
  Montana-Dakota Utilities Co               2026:21
  Northern States Power Co - Minnesota      2026:21.0K
  Oklahoma Gas & Electric Co                2026:15.7K
  Otter Tail Power Co                       2026:3.9K
  PacifiCorp                                2026:0
  Potomac Electric Power Co                 2026:7.2K
  Public Service Co of NM                   2026:9.3K
  San Diego Gas & Electric Co               2026:18.3K
  Southern California Edison Co             2026:6.2K
  Tennessee Valley Authority                2026:953
  Tri-County Electric Coop, Inc (OK)        2026:16
  United Electric Coop Service Inc - (TX)   2026:9.5K
  Virginia Electric & Power Co              2026:21
  Wabash Valley Power Assn, Inc             2026:10

UNNAMED_1 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = UNNAMED_6
  10000                                     2026:273
  12199                                     2026:21
  12377                                     2026:494
  13781                                     2026:21.0K
  14063                                     2026:15.7K
  14232                                     2026:3.9K
  14354                                     2026:0
  15270                                     2026:7.2K
  15473                                     2026:9.3K
  16609                                     2026:18.3K
  17609                                     2026:6.2K
  17832                                     2026:4.4K
  18642                                     2026:953
  19157                                     2026:638
  19160                                     2026:16
  19490                                     2026:9.5K
  19876                                     2026:21
  3046                                      2026:4.7K
  3502                                      2026:9.4K
  40211                                     2026:10
  4226                                      2026:6.6K
  5027                                      2026:19.5K
  5416                                      2026:8.5K
  5701                                      2026:19.3K
  6452                                      2026:17.3K
  733                                       2026:0
  7570                                      2026:10.4K
  8210                                      2026:9.5K
  9191                                      2026:309
  9324                                      2026:111

## where

UNNAMED_3: TX 26, NC 20, MN 18, GA 16, SC 14, NE 14, CA 13, IN 13, VA 11, FL 11, IL 10, AR 10

## what

UNNAMED_0: 2024 100%, Data Year 0%

UNNAMED_4: MISO 28%, PJM 17%, SWPP 14%, SOCO 8%, ERCO 7%, ISNE 6%, DUK 5%, CPLE 4%, NYIS 3%, CISO 3%, TVA 2%, SC 2%

UNNAMED_8: . 75%, 0 24%, 1 0%, Transportation 0%

UNNAMED_13: . 76%, 0 24%, Transportation 0%

UNNAMED_18: . 75%, 0 24%, Transportation 0%

UNNAMED_23: . 76%, 0 24%, Transportation 0%

UNNAMED_28: . 76%, 0 23%, Transportation 0%

UNNAMED_33: . 76%, 0 23%, 10.2 0%, Transportation 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | category | 2 | 0 | 2024 339; Data Year 1 |
| UNNAMED_1 | who | 309 | 0 | 18642 8; 40211 5; 19876 3; 19160 3 |
| UNNAMED_2 | who | 310 | 0 | Tennessee Valley Authorit 8; Wabash Valley Power Assn, 5; Virginia Electric & Power 3; Tri-County Electric Coop, 3 |
| UNNAMED_3 | state | 50 | 0 | TX 26; NC 20; MN 18; GA 16 |
| UNNAMED_4 | category | 39 | 3 | MISO 79; PJM 49; SWPP 40; SOCO 24 |
| NUMBER_OF_CUSTOMERS_ENROLLED | other | 242 | 0 | . 77; 0 23; 887 2; 11457 2 |
| UNNAMED_6 | amount | 158 | 0 | . 107; 0 28; 1 11; 2 9 |
| UNNAMED_7 | amount | 87 | 0 | . 154; 0 30; 1 21; 5 12 |
| UNNAMED_8 | category | 4 | 0 | . 256; 0 82; 1 1; Transportation 1 |
| UNNAMED_9 | amount | 290 | 0 | 1 11; 4 7; 8 6; 5 6 |
| ENERGY_SAVINGS_MWH | amount | 141 | 0 | . 138; 0 61; 96 2; 1 2 |
| UNNAMED_11 | amount | 96 | 0 | . 168; 0 71; 1 4; 2 3 |
| UNNAMED_12 | amount | 67 | 0 | . 208; 0 68; 991.541 1; 1042.5 1 |
| UNNAMED_13 | category | 3 | 0 | . 258; 0 81; Transportation 1 |
| UNNAMED_14 | amount | 183 | 0 | . 100; 0 56; 1 3; 27 2 |
| POTENTIAL_PEAK_DEMAND_SAVINGS_MW | amount | 210 | 0 | . 87; 0 24; 1 6; 3 5 |
| UNNAMED_16 | amount | 181 | 0 | . 110; 0 31; 1 5; 0.1 4 |
| UNNAMED_17 | amount | 147 | 0 | . 159; 0 31; 11 3; 4 2 |
| UNNAMED_18 | category | 3 | 0 | . 256; 0 83; Transportation 1 |
| UNNAMED_19 | amount | 301 | 0 | . 13; 1 6; 3.4 4; 4 3 |
| ACTUAL_PEAK_DEMAND_SAVINGS_MW | amount | 174 | 0 | . 116; 0 34; 1 4; 2.5 3 |
| UNNAMED_21 | amount | 143 | 0 | . 135; 0 47; 1 5; 0.1 3 |
| UNNAMED_22 | amount | 108 | 0 | . 186; 0 44; 2 3; 3 2 |
| UNNAMED_23 | category | 3 | 0 | . 257; 0 82; Transportation 1 |
| UNNAMED_24 | amount | 243 | 0 | . 53; 0 21; 1 4; 10 4 |
| CUSTOMER_INCENTIVES_THOUSAND_DOLLARS | amount | 202 | 0 | . 104; 0 31; 297.301 2; 299.71 2 |
| UNNAMED_26 | amount | 153 | 0 | . 142; 0 45; 1 3; 10 2 |
| UNNAMED_27 | amount | 105 | 0 | . 193; 0 44; 36 2; 3223.31 1 |
| UNNAMED_28 | category | 3 | 0 | . 260; 0 79; Transportation 1 |
| UNNAMED_29 | amount | 271 | 0 | . 54; 0 15; 376.806 2; 297.301 2 |
| ALL_OTHER_COSTS_THOUSAND_DOLLARS | amount | 190 | 0 | . 120; 0 32; 1305 2; 15 2 |
| UNNAMED_31 | amount | 140 | 0 | . 155; 0 35; 1 4; 13 2 |
| UNNAMED_32 | amount | 82 | 0 | . 203; 0 53; 6 3; 1 2 |
| UNNAMED_33 | category | 4 | 0 | . 260; 0 78; 10.2 1; Transportation 1 |
| UNNAMED_34 | amount | 231 | 0 | . 82; 0 26; 3 3; 402.685 2 |
| GRID_CONNECTED | amount | 32 | 0 | . 276; 0 31; 45 2; 39 2 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:58.34876 340 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 4144bd65-9e1c-48a1-a60d-0 340 |
| _SRC_FILE | who | 1 | 0 | Demand_Response_2024.xlsx 340 |
