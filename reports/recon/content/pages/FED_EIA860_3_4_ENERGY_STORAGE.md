# FED_EIA860_3_4_ENERGY_STORAGE

rows 786  columns 52  scan 4.7s

roles: amount 7, audit 2, category 27, date 1, empty 2, other 9, state 1, who 4

## when

_INGESTED_AT
  2026       786  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NAMEPLATE_CAPACITY_MW | 786 | 0.20 | 9.90 | 273.73 | 409 | 27.8K |
| SUMMER_CAPACITY_MW | 786 | 0.20 | 9.90 | 266.00 | 409 | 27.5K |
| WINTER_CAPACITY_MW | 786 | 0.20 | 9.90 | 266.00 | 409 | 27.5K |
| NAMEPLATE_ENERGY_CAPACITY_MWH | 783 | 0.20 | 10 | 920 | 1.4K | 74.4K |
| MAXIMUM_CHARGE_RATE_MW | 783 | 0.10 | 9.90 | 260.54 | 380 | 25.9K |
| MAXIMUM_DISCHARGE_RATE_MW | 783 | 0.10 | 9.90 | 269.66 | 409 | 26.3K |

## who

PLANT_NAME by rows
         4  Menifee Power Bank
         4  Slate Hybrid
         3  Dynegy Moss Landing Power Plant Hybrid
         3  Johanna Energy Center, LLC
         2  EnerSmart Chula Vista Sub Station
         2  Grand Ridge Battery Projects
         2  SunAnza
         2  Yellow Pine II
         2  Central Heating Plant
         2  HEBT Irvine 1
         2  Walter C Beckjord
         2  Ortega Highway Energy Storage
         2  Solana Generating Station
         2  BigBeau Solar, LLC
         2  Tierra Buena Energy Storage
         2  Apache Solar I
         2  Stanton Energy Reliability Center Hybrid
         2  Acushnet Ball Plant 2
         2  Great Lakes Hydro America - ME
         2  Gunther

PLANT_NAME by dollars
         750        3 rows  Dynegy Moss Landing Power Plant Hybrid
         620        4 rows  Menifee Power Bank
         409        1 rows  Manatee Solar Energy Center
         380        1 rows  Gemini Solar Hybrid
         350        2 rows  Crimson
         325        1 rows  Desert Peak Energy Storage I
         300        1 rows  Eleven Mile Solar Center
         300        1 rows  Rodeo Ranch Energy Storage
         300        1 rows  Atrisco Energy Storage
      295.60        2 rows  Solana Generating Station
         260        1 rows  DeCordova Steam Electric Station
         260        1 rows  Sonoran Solar Energy
         259        1 rows  Five Wells Solar Center - Hybrid
         250        1 rows  Sierra Estrella Energy Storage
         250        1 rows  Gateway Energy Storage System
         230        1 rows  McCoy Solar Energy Project Hybrid
         230        1 rows  Sunlight Storage II
         230        1 rows  Sunlight Storage
         225        1 rows  Solar Blue
         220        1 rows  Reid Gardner

UTILITY_NAME by rows
        34  AES Distributed Energy
        28  North Carolina El Member Corp
        28  HEN Infrastructure, L.L.C.
        23  Engie North America
        13  San Diego Gas & Electric Co
        12  Key Capture Energy
        11  Southern California Edison Co
         9  Hybrid-Electric Building Technologies West Los Angeles 1, LLC
         9  United Power, Inc
         9  Terra-Gen Operating Co-Hybrid
         9  Arizona Public Service Co
         8  AES Clean Energy
         8  Convergent Energy and Power LP
         8  MN8 Energy LLC
         8  Terra-Gen Operating Co-BESS 2
         7  Tesla Inc.
         7  Madison Energy Investments LLC
         7  SDGE Batteries
         6  Agilitas Energy, Inc.
         6  Duke Energy Florida, LLC

UTILITY_NAME by dollars
        1.2K       23 rows  Engie North America
         750        3 rows  Dynegy -Moss Landing LLC
      649.80        9 rows  Terra-Gen Operating Co-Hybrid
         622        8 rows  AES Clean Energy
         620        4 rows  Nova Power, LLC
      599.70       12 rows  Key Capture Energy
      568.60        8 rows  Terra-Gen Operating Co-BESS 2
         493        6 rows  Florida Power & Light Co
      447.30       34 rows  AES Distributed Energy
         416        4 rows  Terra-Gen Operating Co-BESS
         380        1 rows  Gemini Solar
      361.40       11 rows  Southern California Edison Co
         350        2 rows  RE Crimson LLC
         330        3 rows  Nevada Power Co
         325        1 rows  Desert Peak Energy Storage I, LLC
         300        1 rows  Rodeo Ranch Energy Storage, LLC
         300        1 rows  Atrisco Energy Storage LLC
         300        1 rows  Eleven Mile Solar Center, LLC
      295.60        2 rows  Arizona Solar One LLC
      277.20       28 rows  HEN Infrastructure, L.L.C.

_SRC_FILE by rows
       786  3_4_Energy_Storage_Y2024.xlsx

_SRC_FILE by dollars
       27.5K      786 rows  3_4_Energy_Storage_Y2024.xlsx

COUNTY by rows
        38  Worcester
        38  Orange
        32  San Diego
        30  Kern
        29  Riverside
        24  Los Angeles
        17  Maricopa
        14  San Bernardino
        13  Plymouth
        13  Hampshire
        11  Reeves
        10  Brazoria
        10  Middlesex
         9  Clark
         9  Fresno
         8  Hidalgo
         8  Kings
         8  Bristol
         7  Norfolk
         7  Hampden

COUNTY by dollars
        3.5K       29 rows  Riverside
        1.9K       30 rows  Kern
        1.5K       17 rows  Maricopa
        1.0K        9 rows  Clark
        1.0K       14 rows  San Bernardino
         993        6 rows  Monterey
      972.70       24 rows  Los Angeles
      650.10       32 rows  San Diego
      585.30        8 rows  Kings
      502.30        6 rows  Pecos
         498        4 rows  Pinal
      482.20       11 rows  Reeves
      473.50       10 rows  Brazoria
         466        5 rows  Imperial
      449.90        8 rows  Hidalgo
      413.50        3 rows  Harris
         409        1 rows  Manatee
      395.90        9 rows  Fresno
         353        2 rows  Crane
         315        5 rows  Yuma

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  Acushnet Ball Plant 2                     2026:1.50
  Apache Solar I                            2026:20
  Atrisco Energy Storage                    2026:300
  BigBeau Solar, LLC                        2026:40
  Central Heating Plant                     2026:3.30
  Crimson                                   2026:350
  DeCordova Steam Electric Station          2026:260
  Desert Peak Energy Storage I              2026:325
  Dynegy Moss Landing Power Plant Hybrid    2026:750
  Eleven Mile Solar Center                  2026:300
  EnerSmart Chula Vista Sub Station         2026:6
  Five Wells Solar Center - Hybrid          2026:259
  Gemini Solar Hybrid                       2026:380
  Grand Ridge Battery Projects              2026:36
  Great Lakes Hydro America - ME            2026:18.80
  Gunther                                   2026:3
  HEBT Irvine 1                             2026:5.50
  Johanna Energy Center, LLC                2026:80
  Manatee Solar Energy Center               2026:409
  Menifee Power Bank                        2026:620
  Ortega Highway Energy Storage             2026:2
  Rodeo Ranch Energy Storage                2026:300
  Slate Hybrid                              2026:140.30
  Solana Generating Station                 2026:295.60
  Sonoran Solar Energy                      2026:260
  Stanton Energy Reliability Center Hybrid  2026:20
  SunAnza                                   2026:4.40
  Tierra Buena Energy Storage               2026:5
  Walter C Beckjord                         2026:4
  Yellow Pine II                            2026:85

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  AES Clean Energy                          2026:622
  AES Distributed Energy                    2026:447.30
  Agilitas Energy, Inc.                     2026:22.60
  Arizona Public Service Co                 2026:201
  Atrisco Energy Storage LLC                2026:300
  Convergent Energy and Power LP            2026:76.20
  Desert Peak Energy Storage I, LLC         2026:325
  Duke Energy Florida, LLC                  2026:50.10
  Dynegy -Moss Landing LLC                  2026:750
  Engie North America                       2026:1.2K
  Florida Power & Light Co                  2026:493
  Gemini Solar                              2026:380
  HEN Infrastructure, L.L.C.                2026:277.20
  Hybrid-Electric Building Technologies We  2026:16.90
  Key Capture Energy                        2026:599.70
  MN8 Energy LLC                            2026:266.80
  Madison Energy Investments LLC            2026:9
  Nevada Power Co                           2026:330
  North Carolina El Member Corp             2026:114.10
  Nova Power, LLC                           2026:620
  RE Crimson LLC                            2026:350
  Rodeo Ranch Energy Storage, LLC           2026:300
  SDGE Batteries                            2026:7.50
  San Diego Gas & Electric Co               2026:197.50
  Southern California Edison Co             2026:361.40
  Terra-Gen Operating Co-BESS               2026:416
  Terra-Gen Operating Co-BESS 2             2026:568.60
  Terra-Gen Operating Co-Hybrid             2026:649.80
  Tesla Inc.                                2026:16.10
  United Power, Inc                         2026:82.40

## where

STATE: CA 227, TX 136, MA 117, NY 48, AZ 35, NC 33, FL 15, HI 14, CO 14, NV 13, NM 11, NJ 10

## what

STATUS: OP 97%, OS 2%, OA 1%, SB 0%

TECHNOLOGY: Batteries 99%, Flywheels 1%, Solar Thermal with Energy Stor 0%, Natural Gas with Compressed Ai 0%

PRIME_MOVER: BA 99%, FW 1%, CP 0%, CE 0%

SECTOR_NAME: IPP Non-CHP 72%, Electric Utility 23%, Commercial Non-CHP 2%, Commercial CHP 1%, Industrial Non-CHP 1%, IPP CHP 0%, Industrial CHP 0%

SECTOR: 2 72%, 1 23%, 4 2%, 5 1%, 6 1%, 3 0%, 7 0%

OPERATING_MONTH: 12 21%, 3 10%, 6 9%, 9 8%, 8 7%, 10 7%, 11 7%, 7 7%, 5 7%, 4 6%, 1 6%, 2 4%

OPERATING_YEAR: 2024 24%, 2021 16%, 2022 16%, 2023 16%, 2020 8%, 2019 6%, 2018 4%, 2017 3%, 2016 2%, 2015 2%, 2012 1%, 2013 1%

STORAGE_TECHNOLOGY_1: LIB 97%, OTH 1%, NIB 1%, FLB 0%, PBB 0%, MAB 0%, NAB 0%

STORAGE_TECHNOLOGY_2: LIB 50%, PBB 50%

STORAGE_ENCLOSURE_TYPE: CS 87%, CT 8%, BL 5%, OT 1%

ARBITRAGE: Y 52%, PR 48%

FREQUENCY_REGULATION: Y 60%, PR 40%

LOAD_FOLLOWING: Y 80%, PR 20%

RAMPING_SPINNING_RESERVE: Y 93%, PR 7%

CO_LOCATED_RENEWABLE_FIRMING: Y 72%, PR 28%

TRANSMISSION_AND_DISTRIBUTION_DEFERRAL: Y 84%, PR 16%

SYSTEM_PEAK_SHAVING: Y 55%, PR 45%

LOAD_MANAGEMENT: Y 52%, PR 48%

VOLTAGE_OR_REACTIVE_POWER_SUPPORT: Y 90%, PR 10%

BACKUP_POWER: Y 78%, PR 22%

EXCESS_WIND_AND_SOLAR_GENERATION: Y 55%, PR 45%

DIRECT_SUPPORT_OF_ANOTHER_UNIT: N 61%, Y 39%

DIRECT_SUPPORT_PLANT_ID_2: 67743 9%, 67275 9%, 65568 9%, 64980 9%, 64851 9%, 64481 9%, 63859 9%, 61956 9%, 60092 9%, 58462 9%, 57187 9%

DIRECT_SUPPORT_GEN_ID_2: 4057R 8%, 4072G 8%, GMSP2 8%, SOL2 8%, DAGGP 8%, AEC2 8%, RCTR 8%, CARPT 8%, BLCK5 8%, BLK2 8%, 2 8%, PV2 8%

DIRECT_SUPPORT_PLANT_ID_3: 60092 50%, 58462 50%

DIRECT_SUPPORT_GEN_ID_3: BLCK6 50%, BLK3 50%

SUPPORT_T_D_ASSET: N 78%, Y 22%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 428 | 0 | 61012 34; 65076 29; 13683 28; 56201 23 |
| UTILITY_NAME | who | 435 | 0 | AES Distributed Energy 34; HEN Infrastructure, L.L.C 29; North Carolina El Member  28; Engie North America 23 |
| PLANT_CODE | other | 744 | 0 | 66494 7; 68493 5; 67886 5; 67883 5 |
| PLANT_NAME | who | 741 | 0 | Menifee Power Bank 7; Central Heating Plant 5; Gunther 5; Gabby Giffords Clean Ener 5 |
| STATE | state | 42 | 0 | CA 227; TX 136; MA 117; NY 48 |
| COUNTY | who | 276 | 0 | Orange 38; Worcester 38; San Diego 32; Kern 30 |
| GENERATOR_ID | other | 577 | 0 | BESS 35; BAT1 33; 1 24; BA1 22 |
| STATUS | category | 4 | 0 | OP 766; OS 12; OA 6; SB 2 |
| TECHNOLOGY | category | 4 | 0 | Batteries 777; Flywheels 5; Solar Thermal with Energy 3; Natural Gas with Compress 1 |
| PRIME_MOVER | category | 4 | 0 | BA 777; FW 5; CP 3; CE 1 |
| SECTOR_NAME | category | 7 | 0 | IPP Non-CHP 569; Electric Utility 181; Commercial Non-CHP 19; Commercial CHP 7 |
| SECTOR | category | 7 | 0 | 2 569; 1 181; 4 19; 5 7 |
| NAMEPLATE_CAPACITY_MW | amount | 170 | 0 | 10 56; 1 54; 9.9 52; 2 46 |
| SUMMER_CAPACITY_MW | amount | 166 | 0 | 1 56; 9.9 53; 10 50; 2 45 |
| WINTER_CAPACITY_MW | amount | 166 | 0 | 1 54; 9.9 53; 10 50; 2 41 |
| OPERATING_MONTH | category | 12 | 0 | 12 167; 3 77; 6 73; 9 62 |
| OPERATING_YEAR | category | 16 | 0 | 2024 188; 2021 126; 2022 126; 2023 125 |
| NAMEPLATE_ENERGY_CAPACITY_MWH | amount | 237 | 3 | 10 47; 9.9 46; 2 24; 3 22 |
| MAXIMUM_CHARGE_RATE_MW | amount | 158 | 3 | 1 56; 9.9 53; 10 52; 2 49 |
| MAXIMUM_DISCHARGE_RATE_MW | amount | 157 | 3 | 1 54; 10 53; 9.9 53; 2 50 |
| STORAGE_TECHNOLOGY_1 | category | 7 | 9 | LIB 754; OTH 8; NIB 8; FLB 3 |
| STORAGE_TECHNOLOGY_2 | category | 2 | 784 | LIB 1; PBB 1 |
| STORAGE_TECHNOLOGY_3 | empty | 0 | 786 |  |
| STORAGE_TECHNOLOGY_4 | empty | 0 | 786 |  |
| NAMEPLATE_REACTIVE_POWER_RATING | amount | 224 | 6 | 1 60; 0.9 45; 5 30; 2 28 |
| STORAGE_ENCLOSURE_TYPE | category | 4 | 3 | CS 679; CT 59; BL 36; OT 9 |
| ARBITRAGE | category | 2 | 416 | Y 194; PR 176 |
| FREQUENCY_REGULATION | category | 2 | 421 | Y 218; PR 147 |
| LOAD_FOLLOWING | category | 2 | 703 | Y 66; PR 17 |
| RAMPING_SPINNING_RESERVE | category | 2 | 589 | Y 184; PR 13 |
| CO_LOCATED_RENEWABLE_FIRMING | category | 2 | 705 | Y 58; PR 23 |
| TRANSMISSION_AND_DISTRIBUTION_DEFERRAL | category | 2 | 741 | Y 38; PR 7 |
| SYSTEM_PEAK_SHAVING | category | 2 | 465 | Y 177; PR 144 |
| LOAD_MANAGEMENT | category | 2 | 642 | Y 75; PR 69 |
| VOLTAGE_OR_REACTIVE_POWER_SUPPORT | category | 2 | 660 | Y 114; PR 12 |
| BACKUP_POWER | category | 2 | 727 | Y 46; PR 13 |
| EXCESS_WIND_AND_SOLAR_GENERATION | category | 2 | 443 | Y 188; PR 155 |
| AC_COUPLED | other | 1 | 575 | Y 211 |
| DC_COUPLED | other | 1 | 692 | Y 94 |
| DC_TIGHTLY_COUPLED | other | 1 | 736 | Y 50 |
| INDEPENDENT | other | 1 | 777 | Y 9 |
| DIRECT_SUPPORT_OF_ANOTHER_UNIT | category | 2 | 10 | N 470; Y 306 |
| DIRECT_SUPPORT_PLANT_ID_1 | other | 309 | 458 | 63727 4; 69076 2; 69075 2; 69073 2 |
| DIRECT_SUPPORT_GEN_ID_1 | other | 241 | 458 | PV1 28; 1 18; PV 12; SOL1 11 |
| DIRECT_SUPPORT_PLANT_ID_2 | category | 15 | 772 | 67743 1; 67275 1; 65568 1; 64980 1 |
| DIRECT_SUPPORT_GEN_ID_2 | category | 14 | 772 | 4057R 1; 4072G 1; GMSP2 1; SOL2 1 |
| DIRECT_SUPPORT_PLANT_ID_3 | category | 3 | 784 | 60092 1; 58462 1 |
| DIRECT_SUPPORT_GEN_ID_3 | category | 2 | 784 | BLCK6 1; BLK3 1 |
| SUPPORT_T_D_ASSET | category | 2 | 10 | N 605; Y 171 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:09.54518 786 |
| _SOURCE_RUN_ID | audit | 1 | 0 | a6723d9d-7ae6-4016-96f8-f 786 |
| _SRC_FILE | who | 1 | 0 | 3_4_Energy_Storage_Y2024. 786 |
