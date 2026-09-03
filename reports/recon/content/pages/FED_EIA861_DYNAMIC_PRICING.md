# FED_EIA861_DYNAMIC_PRICING

rows 858  columns 34  scan 4.3s

roles: amount 3, audit 2, category 23, date 1, other 1, state 1, who 4

## when

_INGESTED_AT
  2026       858  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CUSTOMERS_ENROLLED | 857 | 0 | 2 | 411.5K | 2.65M | 15.83M |
| UNNAMED_7 | 857 | 0 | 9 | 31.8K | 624.0K | 2.40M |
| UNNAMED_8 | 857 | 0 | 2 | 1.7K | 95.7K | 183.1K |

## who

UNNAMED_1 by rows
        18  13374
        15  64314
        13  50046
        10  59931
         8  61131
         6  14354
         5  7279
         5  59793
         4  12199
         4  66867
         4  18642
         3  13781
         3  12341
         3  88888
         3  17698
         3  14232
         3  27058
         2  5027
         2  2830
         2  9324

UNNAMED_1 by dollars
       2.65M        1 rows  17609
       1.64M        1 rows  4254
       1.17M        1 rows  1167
       1.09M        1 rows  15466
      891.4K        1 rows  19436
      772.9K        1 rows  803
      576.5K        1 rows  16534
      501.1K        1 rows  15474
      471.3K        3 rows  17698
      432.3K        1 rows  61475
      395.1K        1 rows  15270
      391.8K        2 rows  5027
      372.1K        1 rows  4110
      360.8K        1 rows  16572
      358.7K        1 rows  56692
      270.7K        1 rows  61432
      249.5K        2 rows  10000
      233.5K        1 rows  12698
      229.6K        1 rows  60181
      229.0K        1 rows  61858

UNNAMED_2 by rows
        18  Constellation NewEnergy, Inc
        15  BP Energy Retail LLC
        13  Texas Retail Energy, LLC
        10  MidAmerican Energy Services, LLC
         8  Freepoint Energy Solutions LLC
         6  PacifiCorp
         5  First Point Power, LLC
         5  NextEra Energy Services, LLC
         4  Montana-Dakota Utilities Co
         4  Tennessee Valley Authority
         4  David Energy Supply LLC
         3  Otter Tail Power Co
         3  MidAmerican Energy Co
         3  Northern States Power Co - Minnesota
         3  High West Energy, Inc
         3  Withheld
         3  Southwestern Electric Power Co
         2  Gibson Electric Members Corp
         2  Appalachian Power Co
         2  El Paso Electric Co

UNNAMED_2 by dollars
       2.65M        1 rows  Southern California Edison Co
       1.64M        1 rows  Consumers Energy Co - (MI)
       1.17M        1 rows  Baltimore Gas & Electric Co
       1.09M        1 rows  Public Service Co of Colorado
      891.4K        1 rows  Union Electric Co - (MO)
      772.9K        1 rows  Arizona Public Service Co
      576.5K        1 rows  Sacramento Municipal Util Dist
      501.1K        1 rows  Public Service Co of Oklahoma
      471.3K        3 rows  Southwestern Electric Power Co
      432.3K        1 rows  Ava Community Energy
      395.1K        1 rows  Potomac Electric Power Co
      391.8K        2 rows  Delmarva Power
      372.1K        1 rows  Commonwealth Edison Co
      360.8K        1 rows  Salt River Project
      358.7K        1 rows  Marin Clean Energy
      270.7K        1 rows  Central Coast Community Energy
      249.5K        2 rows  Evergy Metro
      233.5K        1 rows  Evergy Missouri West
      229.6K        1 rows  CleanPowerSF
      229.0K        1 rows  San Jose Clean Energy

UNNAMED_10 by rows
        70  1
        47  2
        38  3
        22  5
        18  4
        17  7
        15  18
        13  8
        11  9
        11  10
        10  15
        10  47
        10  24
         9  12
         8  13
         8  6
         7  14
         7  48
         6  16
         6  22

UNNAMED_10 by dollars
       2.65M        1 rows  3301482
       1.64M        1 rows  1648381
       1.17M        1 rows  1171615
       1.09M        1 rows  1152804
      891.4K        1 rows  898913
      772.9K        1 rows  773970
      576.5K        1 rows  642588
      501.1K        1 rows  571691
      432.3K        1 rows  488497
      395.1K        1 rows  395081
      372.1K        1 rows  381701
      360.8K        1 rows  374983
      358.7K        1 rows  411661
      270.7K        1 rows  329721
      262.6K        1 rows  279018
      245.5K        1 rows  245555
      233.5K        1 rows  233550
      229.6K        1 rows  257235
      229.0K        1 rows  254358
      206.9K        1 rows  208703

_SRC_FILE by rows
       858  Dynamic_Pricing_2024.xlsx

_SRC_FILE by dollars
      15.83M      858 rows  Dynamic_Pricing_2024.xlsx

## who x when

UNNAMED_1 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = CUSTOMERS_ENROLLED
  1167                                      2026:1.17M
  12199                                     2026:4
  12341                                     2026:110
  13374                                     2026:2.1K
  13781                                     2026:16.1K
  14232                                     2026:36.1K
  14354                                     2026:14.3K
  15270                                     2026:395.1K
  15466                                     2026:1.09M
  15474                                     2026:501.1K
  16534                                     2026:576.5K
  17609                                     2026:2.65M
  17698                                     2026:471.3K
  18642                                     2026:0
  19436                                     2026:891.4K
  27058                                     2026:195
  2830                                      2026:0
  4254                                      2026:1.64M
  50046                                     2026:0
  5027                                      2026:391.8K
  59793                                     2026:69
  59931                                     2026:0
  61131                                     2026:0
  61475                                     2026:432.3K
  64314                                     2026:0
  66867                                     2026:0
  7279                                      2026:0
  803                                       2026:772.9K
  88888                                     2026:0
  9324                                      2026:19.5K

UNNAMED_2 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = CUSTOMERS_ENROLLED
  Appalachian Power Co                      2026:1.8K
  Arizona Public Service Co                 2026:772.9K
  Ava Community Energy                      2026:432.3K
  BP Energy Retail LLC                      2026:0
  Baltimore Gas & Electric Co               2026:1.17M
  Constellation NewEnergy, Inc              2026:2.1K
  Consumers Energy Co - (MI)                2026:1.64M
  David Energy Supply LLC                   2026:0
  El Paso Electric Co                       2026:261
  First Point Power, LLC                    2026:69
  Freepoint Energy Solutions LLC            2026:0
  Gibson Electric Members Corp              2026:0
  High West Energy, Inc                     2026:195
  MidAmerican Energy Co                     2026:110
  MidAmerican Energy Services, LLC          2026:0
  Montana-Dakota Utilities Co               2026:4
  NextEra Energy Services, LLC              2026:0
  Northern States Power Co - Minnesota      2026:16.1K
  Otter Tail Power Co                       2026:36.1K
  PacifiCorp                                2026:14.3K
  Potomac Electric Power Co                 2026:395.1K
  Public Service Co of Colorado             2026:1.09M
  Public Service Co of Oklahoma             2026:501.1K
  Sacramento Municipal Util Dist            2026:576.5K
  Southern California Edison Co             2026:2.65M
  Southwestern Electric Power Co            2026:471.3K
  Tennessee Valley Authority                2026:0
  Texas Retail Energy, LLC                  2026:0
  Union Electric Co - (MO)                  2026:891.4K
  Withheld                                  2026:0

## where

UNNAMED_4: WI 81, TN 73, CA 41, TX 39, MN 37, NC 35, MS 32, AL 31, IN 27, GA 26, CO 24, IL 23

## what

UNNAMED_0: 2024 100%, Data Year 0%

UNNAMED_3: Y 99%, Short Form 1%

UNNAMED_5: MISO 28%, TVA 19%, PJM 15%, SWPP 7%, ISNE 6%, SOCO 5%, ERCO 5%, WACM 4%, CISO 4%, DUK 3%, NYIS 2%, CPLE 2%

UNNAMED_9: . 54%, 0 45%, 1 1%, 3 0%, 2 0%, Transportation 0%

TIME_OF_USE_PRICING: Y 100%, Residential 0%

UNNAMED_12: Y 100%, Commercial 0%

UNNAMED_13: Y 100%, Industrial 0%

UNNAMED_14: Y 97%, Transportation 3%

REAL_TIME_PRICING: Y 94%, Residential 6%

UNNAMED_16: Y 99%, Commercial 1%

UNNAMED_17: Y 99%, Industrial 1%

UNNAMED_18: Y 75%, Transportation 25%

VARIABLE_PEAK_PRICING: Y 86%, Residential 14%

UNNAMED_20: Y 94%, Commercial 6%

UNNAMED_21: Y 93%, Industrial 7%

CRITICAL_PEAK_PRICING: Y 96%, Residential 4%

UNNAMED_24: Y 98%, Commercial 2%

UNNAMED_25: Y 98%, Industrial 2%

UNNAMED_26: Y 75%, Transportation 25%

CRITICAL_PEAK_REBATE: Y 92%, Residential 8%

UNNAMED_28: Y 94%, Commercial 6%

UNNAMED_29: Y 94%, Industrial 6%

UNNAMED_30: Y 50%, Transportation 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | category | 2 | 0 | 2024 857; Data Year 1 |
| UNNAMED_1 | who | 744 | 0 | 13374 19; 64314 18; 50046 16; 59931 13 |
| UNNAMED_2 | who | 736 | 0 | Constellation NewEnergy,  19; BP Energy Retail LLC 18; Texas Retail Energy, LLC 16; MidAmerican Energy Servic 13 |
| UNNAMED_3 | category | 2 | 744 | Y 113; Short Form 1 |
| UNNAMED_4 | state | 52 | 0 | WI 81; TN 73; CA 41; TX 39 |
| UNNAMED_5 | category | 45 | 4 | MISO 210; TVA 138; PJM 114; SWPP 53 |
| CUSTOMERS_ENROLLED | amount | 319 | 0 | 0 233; . 174; 1 16; 5 14 |
| UNNAMED_7 | amount | 302 | 0 | . 135; 0 84; 1 78; 2 35 |
| UNNAMED_8 | amount | 142 | 0 | . 212; 1 102; 0 99; 2 63 |
| UNNAMED_9 | category | 6 | 0 | . 461; 0 385; 1 8; 3 2 |
| UNNAMED_10 | who | 432 | 0 | 1 70; 2 47; 3 38; 5 22 |
| TIME_OF_USE_PRICING | category | 2 | 499 | Y 358; Residential 1 |
| UNNAMED_12 | category | 2 | 398 | Y 459; Commercial 1 |
| UNNAMED_13 | category | 2 | 441 | Y 416; Industrial 1 |
| UNNAMED_14 | category | 2 | 829 | Y 28; Transportation 1 |
| REAL_TIME_PRICING | category | 2 | 842 | Y 15; Residential 1 |
| UNNAMED_16 | category | 2 | 727 | Y 130; Commercial 1 |
| UNNAMED_17 | category | 2 | 747 | Y 110; Industrial 1 |
| UNNAMED_18 | category | 2 | 854 | Y 3; Transportation 1 |
| VARIABLE_PEAK_PRICING | category | 2 | 851 | Y 6; Residential 1 |
| UNNAMED_20 | category | 2 | 840 | Y 17; Commercial 1 |
| UNNAMED_21 | category | 2 | 844 | Y 13; Industrial 1 |
| UNNAMED_22 | other | 1 | 857 | Transportation 1 |
| CRITICAL_PEAK_PRICING | category | 2 | 832 | Y 25; Residential 1 |
| UNNAMED_24 | category | 2 | 817 | Y 40; Commercial 1 |
| UNNAMED_25 | category | 2 | 801 | Y 56; Industrial 1 |
| UNNAMED_26 | category | 2 | 854 | Y 3; Transportation 1 |
| CRITICAL_PEAK_REBATE | category | 2 | 845 | Y 12; Residential 1 |
| UNNAMED_28 | category | 2 | 841 | Y 16; Commercial 1 |
| UNNAMED_29 | category | 2 | 840 | Y 17; Industrial 1 |
| UNNAMED_30 | category | 2 | 856 | Y 1; Transportation 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:39:05.80546 858 |
| _SOURCE_RUN_ID | audit | 1 | 0 | a95621dd-7366-44fa-a2cd-2 858 |
| _SRC_FILE | who | 1 | 0 | Dynamic_Pricing_2024.xlsx 858 |
