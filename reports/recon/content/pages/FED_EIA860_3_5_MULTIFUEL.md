# FED_EIA860_3_5_MULTIFUEL

rows 2.9K  columns 42  scan 6.8s

roles: amount 7, audit 2, category 21, date 1, other 7, state 1, who 4

## when

_INGESTED_AT
  2026      2.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NAMEPLATE_CAPACITY_MW | 2.9K | 0.20 | 22 | 707.22 | 1.2K | 210.8K |
| SUMMER_CAPACITY_MW | 2.9K | 0.20 | 18 | 635.59 | 1.1K | 187.1K |
| WINTER_CAPACITY_MW | 2.9K | 0.20 | 20.40 | 637.81 | 1.1K | 200.7K |
| NET_SUMMER_CAPACITY_WITH_NATURAL_GAS_MW | 1.9K | 0.20 | 40.06 | 469.36 | 987.30 | 132.0K |
| NET_WINTER_CAPACITY_WITH_NATURAL_GAS_MW | 1.9K | 0.12 | 44 | 489 | 968.30 | 143.9K |
| NET_SUMMER_CAPACITY_WITH_OIL_MW | 1.9K | 0 | 37.50 | 469.50 | 987.30 | 128.5K |

## who

PLANT_NAME by rows
        48  Amelia
        48  Mountain View
        48  Chesterfield Landfill Gas
        48  Charles City
        36  King & Queen
        35  Brunswick Landfill Gas
        20  Johnsonville
        20  Allen
        18  Pine Grove
        18  Wicomico
        18  New River
        18  New Bern
        18  Cedar Hills
        17  Lincoln Combustion
        16  Narrows Gas Turbines Generating
        16  Gowanus Gas Turbines Generating
        13  E F Barrett
        12  West County Energy Center
        12  Hines Energy Complex
        12  Henrico

PLANT_NAME by dollars
        3.8K       12 rows  West County Energy Center
        3.1K        4 rows  Monroe (MI)
        2.1K       12 rows  Hines Energy Complex
        2.0K        5 rows  Ravenswood
        1.9K       11 rows  Sherwood H Smith Jr Energy Complex
        1.8K        4 rows  Nine Mile Point
        1.7K        4 rows  Okeechobee Clean Energy Center
        1.7K        2 rows  TalenEnergy Martins Creek
        1.7K        2 rows  Keystone
        1.7K        2 rows  Conemaugh
        1.7K        2 rows  Limestone
        1.6K       10 rows  PSEG Linden Generating Station
        1.6K        2 rows  Manatee
        1.6K        4 rows  Northport
        1.6K        2 rows  Sherburne County
        1.5K       17 rows  Lincoln Combustion
        1.5K        2 rows  TalenEnergy Montour
        1.4K        3 rows  Brunner Island
        1.4K        7 rows  York Energy Center
        1.3K        2 rows  W A Parish

UTILITY_NAME by rows
       329  Industrial Power Generating Company LLC
        80  Tennessee Valley Authority
        58  Florida Power & Light Co
        35  U S Power Generating Company LLC
        33  Duke Energy Florida, LLC
        33  Duke Energy Carolinas, LLC
        33  Duke Energy Progress - (NC)
        29  Virginia Electric & Power Co
        23  National Grid Generation LLC
        22  Luminant Generation Company LLC
        22  Southern Power Co
        21  Northern States Power Co - Minnesota
        19  Archer Daniels Midland Co
        18  Kimura Power LLC
        18  Ingenco Renewable Development, LLC
        18  Bio Energy Washington, LLC
        18  Georgia Power Co
        18  Dominion Energy South Carolina, Inc
        16  Alabama Power Co
        15  Los Angeles Department of Water & Power

UTILITY_NAME by dollars
       17.7K       58 rows  Florida Power & Light Co
        5.3K       33 rows  Duke Energy Progress - (NC)
        5.2K       33 rows  Duke Energy Florida, LLC
        5.2K        9 rows  DTE Electric Company
        4.2K       80 rows  Tennessee Valley Authority
        4.1K       29 rows  Virginia Electric & Power Co
        4.1K       33 rows  Duke Energy Carolinas, LLC
        3.4K        4 rows  KeyCon Operating LLC
        3.0K        4 rows  NRG Texas Power LLC
        2.8K       23 rows  National Grid Generation LLC
        2.8K        8 rows  Southwestern Public Service Co
        2.7K       22 rows  Southern Power Co
        2.7K        7 rows  Entergy Louisiana LLC
        2.6K       22 rows  Luminant Generation Company LLC
        2.5K       14 rows  Orlando Utilities Comm
        2.3K       21 rows  Northern States Power Co - Minnesota
        2.3K       13 rows  Wisconsin Electric Power Co
        2.1K       18 rows  Georgia Power Co
        2.0K        8 rows  JEA
        2.0K       14 rows  East Kentucky Power Coop, Inc

_SRC_FILE by rows
      2.9K  3_5_Multifuel_Y2024.xlsx

_SRC_FILE by dollars
      187.1K     2.9K rows  3_5_Multifuel_Y2024.xlsx

COUNTY by rows
        71  Franklin
        51  Chesterfield
        48  Charles City
        48  Amelia
        38  Brunswick
        36  King and Queen
        35  Los Angeles
        34  Kings
        28  Nassau
        27  Union
        25  Lincoln
        23  Polk
        22  Middlesex
        22  Jackson
        22  Jasper
        20  Pulaski
        20  Orange
        20  Montgomery
        20  Humphreys
        20  Craven

COUNTY by dollars
        5.2K       19 rows  Palm Beach
        4.4K       18 rows  Queens
        3.7K       18 rows  Monroe
        3.7K       14 rows  Broward
        3.5K       20 rows  Orange
        3.0K       23 rows  Polk
        3.0K       13 rows  Northampton
        3.0K       16 rows  Brevard
        2.9K       15 rows  York
        2.6K       19 rows  Suffolk
        2.5K       14 rows  Jefferson
        2.4K       27 rows  Union
        2.4K        6 rows  Armstrong
        2.4K       22 rows  Jackson
        2.3K       19 rows  Richmond
        2.1K       17 rows  Cherokee
        2.1K       35 rows  Los Angeles
        2.1K        4 rows  St Clair
        2.0K       16 rows  Duval
        2.0K       15 rows  New Castle

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  Allen                                     2026:427.20
  Amelia                                    2026:14.40
  Brunswick Landfill Gas                    2026:10.50
  Cedar Hills                               2026:5.40
  Charles City                              2026:14.40
  Chesterfield Landfill Gas                 2026:14.40
  Conemaugh                                 2026:1.7K
  E F Barrett                               2026:653.60
  Gowanus Gas Turbines Generating           2026:299.60
  Henrico                                   2026:3.60
  Hines Energy Complex                      2026:2.1K
  Johnsonville                              2026:1.0K
  Keystone                                  2026:1.7K
  King & Queen                              2026:10.80
  Limestone                                 2026:1.7K
  Lincoln Combustion                        2026:1.5K
  Monroe (MI)                               2026:3.1K
  Mountain View                             2026:14.40
  Narrows Gas Turbines Generating           2026:309.10
  New Bern                                  2026:5.40
  New River                                 2026:5.40
  Nine Mile Point                           2026:1.8K
  Okeechobee Clean Energy Center            2026:1.7K
  PSEG Linden Generating Station            2026:1.6K
  Pine Grove                                2026:5.40
  Ravenswood                                2026:2.0K
  Sherwood H Smith Jr Energy Complex        2026:1.9K
  TalenEnergy Martins Creek                 2026:1.7K
  West County Energy Center                 2026:3.8K
  Wicomico                                  2026:5.40

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  Alabama Power Co                          2026:2.0K
  Archer Daniels Midland Co                 2026:881
  Bio Energy Washington, LLC                2026:5.40
  DTE Electric Company                      2026:5.2K
  Dominion Energy South Carolina, Inc       2026:1.9K
  Duke Energy Carolinas, LLC                2026:4.1K
  Duke Energy Florida, LLC                  2026:5.2K
  Duke Energy Progress - (NC)               2026:5.3K
  East Kentucky Power Coop, Inc             2026:2.0K
  Entergy Louisiana LLC                     2026:2.7K
  Florida Power & Light Co                  2026:17.7K
  Georgia Power Co                          2026:2.1K
  Industrial Power Generating Company LLC   2026:98.70
  Ingenco Renewable Development, LLC        2026:5.40
  JEA                                       2026:2.0K
  KeyCon Operating LLC                      2026:3.4K
  Kimura Power LLC                          2026:902.10
  Los Angeles Department of Water & Power   2026:1.6K
  Luminant Generation Company LLC           2026:2.6K
  NRG Texas Power LLC                       2026:3.0K
  National Grid Generation LLC              2026:2.8K
  Northern States Power Co - Minnesota      2026:2.3K
  Orlando Utilities Comm                    2026:2.5K
  Southern Power Co                         2026:2.7K
  Southwestern Public Service Co            2026:2.8K
  Tennessee Valley Authority                2026:4.2K
  U S Power Generating Company LLC          2026:1.7K
  Virginia Electric & Power Co              2026:4.1K
  Wisconsin Electric Power Co               2026:2.3K

## where

STATE: VA 314, FL 198, KS 175, NY 162, PA 150, CA 129, NC 120, TX 97, GA 96, IA 89, NE 89, MN 86

## what

STATUS: OP 92%, SB 5%, OS 2%, OA 1%

TECHNOLOGY: Natural Gas Fired Combustion T 29%, Natural Gas Fired Combined Cyc 14%, Natural Gas Internal Combustio 13%, Landfill Gas 11%, Petroleum Liquids 11%, Natural Gas Steam Turbine 8%, Wood/Wood Waste Biomass 7%, Conventional Steam Coal 4%, Other Waste Biomass 2%, Other Gases 1%, Municipal Solid Waste 0%, Petroleum Coke 0%

PRIME_MOVER: IC 35%, GT 31%, ST 20%, CT 11%, CA 3%, CS 0%, OT 0%

SECTOR_NAME: Electric Utility 49%, IPP Non-CHP 27%, Industrial CHP 12%, Commercial CHP 7%, IPP CHP 3%, Commercial Non-CHP 1%, Industrial Non-CHP 1%

SECTOR: 1 49%, 2 27%, 7 12%, 5 7%, 3 3%, 4 1%, 6 1%

OPERATING_MONTH: 6 19%, 1 11%, 5 10%, 8 9%, 7 9%, 12 8%, 4 7%, 3 6%, 11 6%, 10 6%, 9 5%, 2 4%

ENERGY_SOURCE_1: NG 64%, LFG 12%, DFO 11%, BLQ 4%, WDS 2%, SUB 2%, OBG 2%, BIT 2%, KER 1%, OG 0%, MSW 0%, OBL 0%

ENERGY_SOURCE_2: DFO 68%, NG 19%, LFG 3%, WDS 2%, OG 2%, BIT 2%, RFO 2%, KER 1%, OBG 1%, TDF 0%, SUB 0%, OBS 0%

MULTIPLE_FUELS: Y 100%, N 0%

COFIRE_FUELS: Y 55%, N 45%

COFIRE_ENERGY_SOURCE_1: NG 38%, DFO 34%, BLQ 5%, WDS 5%, BIT 4%, SUB 4%, LFG 3%, OBG 3%, RFO 2%, OG 1%, PC 1%, MSW 1%

COFIRE_ENERGY_SOURCE_2: DFO 31%, NG 27%, LFG 23%, OG 4%, BIT 4%, WDS 3%, RFO 3%, OBG 2%, SUB 1%, OBL 1%, BLQ 1%, TDF 1%

COFIRE_ENERGY_SOURCE_3: NG 31%, WDS 20%, DFO 15%, RFO 9%, BIT 6%, BLQ 4%, SLW 4%, TDF 3%, LFG 3%, OTH 2%, WO 2%, AB 1%

COFIRE_ENERGY_SOURCE_4: WDS 24%, TDF 11%, DFO 10%, SLW 8%, NG 8%, BIT 8%, OBL 6%, WO 6%, RFO 6%, BLQ 5%, PC 5%, OTH 3%

COFIRE_ENERGY_SOURCE_5: WDS 19%, RFO 18%, DFO 14%, SLW 11%, NG 9%, OBS 9%, BIT 7%, BLQ 5%, TDF 4%, OBL 4%, WO 2%

COFIRE_ENERGY_SOURCE_6: DFO 21%, NG 15%, OTH 15%, SLW 9%, TDF 9%, RFO 6%, BLQ 6%, PC 6%, OBS 3%, BIT 3%, WO 3%, PG 3%

SWITCH_BETWEEN_OIL_AND_NATURAL_GAS: Y 68%, N 32%

SWITCH_WHEN_OPERATING: Y 89%, N 11%

TIME_TO_SWITCH_FROM_GAS_TO_OIL: 1H 76%, 6H 17%, UNK 5%, 24H 2%, 72H 1%, OVER 0%

TIME_TO_SWITCH_FROM_OIL_TO_GAS: 1H 75%, 6H 18%, UNK 6%, 24H 1%, 72H 0%, OVER 0%

FACTORS_THAT_LIMIT_SWITCHING: Y 76%, N 24%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 676 | 0 | 55938 337; 18642 80; 6452 58; 54863 36 |
| UTILITY_NAME | who | 676 | 0 | Industrial Power Generati 337; Tennessee Valley Authorit 80; Florida Power & Light Co 58; U S Power Generating Comp 36 |
| PLANT_CODE | other | 886 | 0 | 56687 57; 56684 57; 56683 57; 56681 57 |
| PLANT_NAME | who | 878 | 0 | Mountain View 57; Chesterfield Landfill Gas 57; Charles City 57; Amelia 57 |
| STATE | state | 51 | 0 | VA 314; FL 198; KS 175; NY 162 |
| COUNTY | who | 492 | 0 | Franklin 71; Chesterfield 55; Charles City 55; Amelia 55 |
| GENERATOR_ID | other | 642 | 0 | 1 192; 2 176; 3 146; 4 132 |
| STATUS | category | 4 | 0 | OP 2.7K; SB 139; OS 66; OA 16 |
| TECHNOLOGY | category | 14 | 0 | Natural Gas Fired Combust 823; Natural Gas Fired Combine 398; Natural Gas Internal Comb 377; Landfill Gas 328 |
| PRIME_MOVER | category | 7 | 0 | IC 1.0K; GT 905; ST 578; CT 323 |
| SECTOR_NAME | category | 7 | 0 | Electric Utility 1.4K; IPP Non-CHP 777; Industrial CHP 355; Commercial CHP 204 |
| SECTOR | category | 7 | 0 | 1 1.4K; 2 777; 7 355; 5 204 |
| NAMEPLATE_CAPACITY_MW | amount | 634 | 0 | 0.3 374; 1.1 53; 2.5 49; 2 47 |
| SUMMER_CAPACITY_MW | amount | 739 | 8 | 0.3 376; 1.1 40; 1.2 38; 1 37 |
| WINTER_CAPACITY_MW | amount | 713 | 7 | 0.3 375; 1.2 39; 1.1 38; 2 38 |
| OPERATING_MONTH | category | 12 | 0 | 6 554; 1 323; 5 294; 8 267 |
| OPERATING_YEAR | other | 89 | 0 | 2003 180; 2001 140; 2002 128; 1972 103 |
| ENERGY_SOURCE_1 | category | 22 | 0 | NG 1.8K; LFG 328; DFO 306; BLQ 122 |
| ENERGY_SOURCE_2 | category | 27 | 3 | DFO 1.9K; NG 527; LFG 74; WDS 61 |
| MULTIPLE_FUELS | category | 2 | 0 | Y 2.9K; N 1 |
| COFIRE_FUELS | category | 2 | 14 | Y 1.6K; N 1.3K |
| COFIRE_ENERGY_SOURCE_1 | category | 22 | 1.3K | NG 600; DFO 538; BLQ 81; WDS 74 |
| COFIRE_ENERGY_SOURCE_2 | category | 20 | 1.3K | DFO 477; NG 413; LFG 361; OG 56 |
| COFIRE_ENERGY_SOURCE_3 | category | 18 | 2.6K | NG 72; WDS 47; DFO 36; RFO 20 |
| COFIRE_ENERGY_SOURCE_4 | category | 17 | 2.8K | WDS 29; TDF 13; DFO 12; SLW 10 |
| COFIRE_ENERGY_SOURCE_5 | category | 11 | 2.8K | WDS 11; RFO 10; DFO 8; SLW 6 |
| COFIRE_ENERGY_SOURCE_6 | category | 13 | 2.9K | DFO 7; NG 5; OTH 5; SLW 3 |
| SWITCH_BETWEEN_OIL_AND_NATURAL_GAS | category | 2 | 62 | Y 1.9K; N 916 |
| SWITCH_WHEN_OPERATING | category | 2 | 949 | Y 1.7K; N 209 |
| NET_SUMMER_CAPACITY_WITH_NATURAL_GAS_MW | amount | 607 | 979 | 1.2 38; 1 27; 1.8 25; 2.5 25 |
| NET_WINTER_CAPACITY_WITH_NATURAL_GAS_MW | amount | 561 | 979 | 1.2 35; 1 31; 93 30; 6 25 |
| NET_SUMMER_CAPACITY_WITH_OIL_MW | amount | 561 | 982 | 1.2 36; 1 36; 2.5 27; 3 25 |
| NET_WINTER_CAPACITY_WITH_OIL_MW | amount | 537 | 982 | 1 38; 1.2 35; 3 28; 6 26 |
| TIME_TO_SWITCH_FROM_GAS_TO_OIL | category | 6 | 977 | 1H 1.5K; 6H 327; UNK 89; 24H 29 |
| TIME_TO_SWITCH_FROM_OIL_TO_GAS | category | 6 | 978 | 1H 1.4K; 6H 349; UNK 107; 24H 24 |
| FACTORS_THAT_LIMIT_SWITCHING | category | 2 | 978 | Y 1.5K; N 463 |
| STORAGE_LIMITS | other | 1 | 2.1K | Y 818 |
| AIR_PERMIT_LIMITS | other | 1 | 1.7K | Y 1.2K |
| OTHER_LIMITS | other | 1 | 2.8K | Y 141 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:18.98050 2.9K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 51a699c6-c629-4633-be43-c 2.9K |
| _SRC_FILE | who | 1 | 0 | 3_5_Multifuel_Y2024.xlsx 2.9K |
