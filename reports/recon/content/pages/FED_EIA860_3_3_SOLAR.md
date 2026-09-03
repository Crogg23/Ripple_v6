# FED_EIA860_3_3_SOLAR

rows 7.2K  columns 44  scan 4.9s

roles: amount 6, audit 2, category 24, date 1, other 7, state 1, who 4

## when

_INGESTED_AT
  2026      7.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NAMEPLATE_CAPACITY_MW | 7.2K | 0.10 | 2.90 | 228.57 | 690 | 124.3K |
| SUMMER_CAPACITY_MW | 7.2K | 0.05 | 2.90 | 226.63 | 690 | 123.5K |
| WINTER_CAPACITY_MW | 7.2K | 0.05 | 2.80 | 226.63 | 690 | 122.7K |
| DC_NET_CAPACITY_MW | 7.1K | 0.06 | 3.60 | 296.09 | 966.80 | 160.0K |
| NET_METERING_DC_CAPACITY_MW | 1.0K | 0 | 2 | 20.84 | 70 | 3.1K |
| VIRTUAL_NET_METERING_DC_CAPACITY_MW | 1.3K | 0.10 | 2.50 | 12.51 | 231.70 | 4.6K |

## who

PLANT_NAME by rows
        17  Kotzebue Hybrid
        12  Lanai Solar-Electric Plant
        12  Mesquite Solar 1
        11  AZ State University - Tempe Campus Solar
        11  Desert Sunlight 300, LLC
        10  Pennsauken Solar
        10  Samarcand Solar Farm, LLC
        10  Copper Mountain Solar 3
        10  Solar Photovoltaic Project #42
        10  Waihonu North Solar
         9  Desert Sunlight 250, LLC
         9  Kenansville Solar Farm, LLC
         8  McCoy Solar Energy Project Hybrid
         8  Silver State Solar Power South
         7  Solar Star 1
         7  Stateline Solar
         6  Solar Star 2
         6  Tesla Reno GigaFactory
         6  CSUF Trigeneration
         6  River Terminal Development Solar

PLANT_NAME by dollars
         690        1 rows  Gemini Solar Hybrid
      592.80        1 rows  Double Back Diamond
      585.90        5 rows  Topaz Solar Farm
         577        1 rows  Fox Squirrel Solar
         500        1 rows  Aktina Solar
         500        1 rows  Hecate Energy Frye Solar LLC
         471        1 rows  Mockingbird Solar Center
         430        1 rows  Old 300 Solar Center, LLC
         420        1 rows  2W Permian Solar Project Hybrid
         400        1 rows  Mammoth North Solar
         400        2 rows  Roadrunner, LLC Hybrid
         400        1 rows  Waco Solar
         350        1 rows  Red Tailed Hawk Solar LLC
      347.70        3 rows  Agua Caliente Solar Project
         325        1 rows  Neptune Energy Center Hybrid
         325        1 rows  AEUG Union Solar, LLC
         321        1 rows  Lumina II Solar Project
         320        1 rows  IP Radian, LLC
         320        1 rows  Lumina Solar Project
         320        1 rows  Five Wells Solar Center - Hybrid

UTILITY_NAME by rows
       217  AES Distributed Energy
       206  MN8 Energy LLC
       196  Altus Power America Management, LLC
       194  Cypress Creek Renewables
       170  Greenbacker Renewable Energy Corporation
       139  Strata Manager, LLC
       121  Nautilus Solar Solutions
        99  Consolidated Edison Development Inc.
        98  Florida Power & Light Co
        96  Tesla Inc.
        88  Standard Solar
        82  SoCore Energy LLC
        77  Generate Capital
        76  National Grid Renewables
        67  Duke Energy Renewables Services
        62  Ecoplexus, Inc
        57  United States Solar Corporation
        57  REA Investments, LLC
        57  NJR Clean Energy Ventures Corporation
        56  Terraform Arcadia

UTILITY_NAME by dollars
        7.0K       98 rows  Florida Power & Light Co
        2.8K      217 rows  AES Distributed Energy
        2.8K       99 rows  Consolidated Edison Development Inc.
        2.7K       31 rows  Lightsource Renewable Energy Asset Management, LLC
        2.5K       39 rows  Southern Power Co
        2.1K      206 rows  MN8 Energy LLC
        2.1K       67 rows  Duke Energy Renewables Services
        1.9K       18 rows  Invenergy Services LLC
        1.6K      194 rows  Cypress Creek Renewables
        1.6K       23 rows  AES Clean Energy
        1.5K       33 rows  Dominion Renewable Energy
        1.5K       24 rows  Duke Energy Florida, LLC
        1.4K       35 rows  Onward Energy
        1.3K       27 rows  Tampa Electric Co
        1.2K       22 rows  Dominion Energy Inc.
        1.2K       54 rows  Arevon Energy, Inc.
        1.1K       15 rows  Wisconsin Power & Light Co
        1.0K      170 rows  Greenbacker Renewable Energy Corporation
        1.0K        4 rows  Acciona Energy USA Global, LLC
      979.80        7 rows  EDF Renewable Asset Holdings, Inc.

_SRC_FILE by rows
      7.2K  3_3_Solar_Y2024.xlsx

_SRC_FILE by dollars
      123.5K     7.2K rows  3_3_Solar_Y2024.xlsx

COUNTY by rows
       163  Worcester
       152  Los Angeles
       150  Kern
       122  Middlesex
       104  Riverside
        96  Washington
        94  San Bernardino
        78  Clark
        78  Fresno
        72  Orange
        70  Tulare
        66  Maricopa
        65  Plymouth
        63  Franklin
        60  Bristol
        59  Hampden
        59  Stearns
        58  Chisago
        55  Wayne
        51  Sacramento

COUNTY by dollars
        4.9K      150 rows  Kern
        4.7K      104 rows  Riverside
        4.3K       78 rows  Clark
        2.4K       94 rows  San Bernardino
        2.2K       14 rows  Pecos
        2.1K       66 rows  Maricopa
        2.1K       45 rows  Imperial
        1.8K       44 rows  Kings
        1.6K       78 rows  Fresno
        1.5K      152 rows  Los Angeles
        1.4K       32 rows  Madison
        1.3K        7 rows  Lamar
        1.2K        6 rows  Fort Bend
        1.2K       17 rows  Calhoun
        1.1K        9 rows  Pueblo
        1.1K       22 rows  San Luis Obispo
        1.1K       16 rows  Yuma
        1.1K       13 rows  Pinal
        1.1K        4 rows  Wharton
        1.1K        4 rows  Andrews

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  2W Permian Solar Project Hybrid           2026:420
  AZ State University - Tempe Campus Solar  2026:2.40
  Aktina Solar                              2026:500
  CSUF Trigeneration                        2026:4.30
  Copper Mountain Solar 3                   2026:255
  Desert Sunlight 250, LLC                  2026:249.70
  Desert Sunlight 300, LLC                  2026:313.70
  Double Back Diamond                       2026:592.80
  Fox Squirrel Solar                        2026:577
  Gemini Solar Hybrid                       2026:690
  Hecate Energy Frye Solar LLC              2026:500
  Kenansville Solar Farm, LLC               2026:4.50
  Kotzebue Hybrid                           2026:1.70
  Lanai Solar-Electric Plant                2026:1.20
  Mammoth North Solar                       2026:400
  McCoy Solar Energy Project Hybrid         2026:270.60
  Mesquite Solar 1                          2026:170
  Mockingbird Solar Center                  2026:471
  Old 300 Solar Center, LLC                 2026:430
  Pennsauken Solar                          2026:3.90
  River Terminal Development Solar          2026:2.90
  Samarcand Solar Farm, LLC                 2026:5
  Silver State Solar Power South            2026:260.10
  Solar Photovoltaic Project #42            2026:5
  Solar Star 1                              2026:309.90
  Solar Star 2                              2026:275
  Stateline Solar                           2026:300
  Tesla Reno GigaFactory                    2026:6.70
  Topaz Solar Farm                          2026:585.90
  Waihonu North Solar                       2026:4.90

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  AES Clean Energy                          2026:1.6K
  AES Distributed Energy                    2026:2.8K
  Altus Power America Management, LLC       2026:555.83
  Arevon Energy, Inc.                       2026:1.2K
  Consolidated Edison Development Inc.      2026:2.8K
  Cypress Creek Renewables                  2026:1.6K
  Dominion Energy Inc.                      2026:1.2K
  Dominion Renewable Energy                 2026:1.5K
  Duke Energy Florida, LLC                  2026:1.5K
  Duke Energy Renewables Services           2026:2.1K
  Ecoplexus, Inc                            2026:240.80
  Florida Power & Light Co                  2026:7.0K
  Generate Capital                          2026:242.30
  Greenbacker Renewable Energy Corporation  2026:1.0K
  Invenergy Services LLC                    2026:1.9K
  Lightsource Renewable Energy Asset Manag  2026:2.7K
  MN8 Energy LLC                            2026:2.1K
  NJR Clean Energy Ventures Corporation     2026:302.70
  National Grid Renewables                  2026:681.70
  Nautilus Solar Solutions                  2026:333.20
  Onward Energy                             2026:1.4K
  REA Investments, LLC                      2026:109.10
  SoCore Energy LLC                         2026:171.60
  Southern Power Co                         2026:2.5K
  Standard Solar                            2026:194.20
  Strata Manager, LLC                       2026:666.50
  Tampa Electric Co                         2026:1.3K
  Terraform Arcadia                         2026:111.80
  Tesla Inc.                                2026:180.20
  United States Solar Corporation           2026:60.40

## where

STATE: CA 1.0K, NC 794, MN 700, NY 632, MA 545, NJ 391, IL 218, FL 193, TX 186, MD 168, CO 166, GA 154

## what

STATUS: OP 100%, OA 0%, OS 0%

TECHNOLOGY: Solar Photovoltaic 100%, Solar Thermal without Energy S 0%, Solar Thermal with Energy Stor 0%

PRIME_MOVER: PV 100%, ST 0%, CP 0%, OT 0%

SECTOR_NAME: IPP Non-CHP 86%, Electric Utility 10%, Commercial Non-CHP 3%, Industrial Non-CHP 1%, Commercial CHP 0%, Industrial CHP 0%, IPP CHP 0%

SECTOR: 2 86%, 1 10%, 4 3%, 6 1%, 5 0%, 7 0%, 3 0%

OPERATING_MONTH: 12 28%, 11 9%, 10 7%, 6 7%, 9 7%, 3 7%, 1 7%, 7 6%, 4 6%, 5 6%, 8 6%, 2 4%

OPERATING_YEAR: 2021 11%, 2024 11%, 2020 10%, 2017 10%, 2023 9%, 2018 9%, 2019 9%, 2016 8%, 2022 8%, 2014 6%, 2015 6%, 2013 4%

LENSES_MIRRORS: N 78%, Y 22%

SINGLE_AXIS_TRACKING: Y 94%, N 6%

DUAL_AXIS_TRACKING: Y 52%, N 48%

FIXED_TILT: Y 95%, N 5%

BIFACIAL: Y 95%, N 5%

EAST_WEST_FIXED_TILT: N 59%, Y 41%

PARABOLIC_TROUGH: N 68%, Y 32%

POWER_TOWER: N 60%, Y 40%

OTHER_SOLAR_TECHNOLOGY: N 83%, Y 17%

CRYSTALLINE_SILICON: Y 100%, N 0%

THIN_FILM_CDTE: Y 94%, N 6%

THIN_FILM_A_SI: Y 65%, N 35%

THIN_FILM_CIGS: Y 91%, N 9%

THIN_FILM_OTHER: Y 63%, N 37%

OTHER_MATERIALS: N 73%, Y 27%

NET_METERING_AGREEMENT: N 85%, Y 14%, X 0%

VIRTUAL_NET_METERING_AGREEMENT: N 81%, Y 19%, X 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 2.5K | 0 | 61012 217; 61944 206; 60281 196; 61060 195 |
| UTILITY_NAME | who | 2.4K | 0 | AES Distributed Energy 217; MN8 Energy LLC 206; Altus Power America Manag 196; Cypress Creek Renewables 195 |
| PLANT_CODE | other | 6.7K | 0 | 68798 37; 69098 36; 69097 36; 69096 36 |
| PLANT_NAME | who | 6.6K | 1 | Lockheed Martin Palmdale  37; NJ - CS Energy - Berkeley 36; NJ - CS Energy - Berkeley 36; Jericho 36 |
| STATE | state | 50 | 1 | CA 1.0K; NC 794; MN 700; NY 632 |
| COUNTY | who | 880 | 1 | Worcester 163; Los Angeles 152; Kern 150; Middlesex 122 |
| GENERATOR_ID | other | 4.8K | 0 | PV1 658; 1 617; GEN1 173; SC 81 |
| STATUS | category | 3 | 0 | OP 7.1K; OA 7; OS 4 |
| TECHNOLOGY | category | 3 | 0 | Solar Photovoltaic 7.1K; Solar Thermal without Ene 9; Solar Thermal with Energy 3 |
| PRIME_MOVER | category | 4 | 0 | PV 7.1K; ST 8; CP 3; OT 1 |
| SECTOR_NAME | category | 7 | 1 | IPP Non-CHP 6.1K; Electric Utility 694; Commercial Non-CHP 206; Industrial Non-CHP 92 |
| SECTOR | category | 8 | 1 | 2 6.1K; 1 694; 4 206; 6 92 |
| NAMEPLATE_CAPACITY_MW | amount | 491 | 0 | 1 1.0K; 5 806; 2 787; 1.5 303 |
| SUMMER_CAPACITY_MW | amount | 513 | 0 | 1 930; 5 766; 2 763; 1.5 295 |
| WINTER_CAPACITY_MW | amount | 514 | 0 | 1 914; 5 737; 2 722; 1.5 296 |
| OPERATING_MONTH | category | 13 | 1 | 12 2.0K; 11 647; 10 506; 6 501 |
| OPERATING_YEAR | category | 24 | 1 | 2021 695; 2024 693; 2020 678; 2017 628 |
| LENSES_MIRRORS | category | 2 | 7.1K | N 45; Y 13 |
| SINGLE_AXIS_TRACKING | category | 2 | 3.8K | Y 3.1K; N 202 |
| DUAL_AXIS_TRACKING | category | 2 | 7.0K | Y 71; N 65 |
| FIXED_TILT | category | 2 | 3.0K | Y 3.9K; N 194 |
| BIFACIAL | category | 2 | 6.9K | Y 259; N 14 |
| EAST_WEST_FIXED_TILT | category | 2 | 7.0K | N 79; Y 54 |
| PARABOLIC_TROUGH | category | 2 | 7.1K | N 15; Y 7 |
| LINEAR_FRESNEL | other | 1 | 7.2K | N 4 |
| POWER_TOWER | category | 2 | 7.1K | N 6; Y 4 |
| DISH_ENGINE | other | 1 | 7.2K | N 4 |
| OTHER_SOLAR_TECHNOLOGY | category | 2 | 7.0K | N 104; Y 22 |
| AZIMUTH_ANGLE | other | 253 | 161 | 180 4.7K; 0 747; 90 362; 185 97 |
| TILT_ANGLE | other | 98 | 1.5K | 25 1.2K; 20 1.2K; 0 643; 30 430 |
| DC_NET_CAPACITY_MW | amount | 1.1K | 21 | 1.4 445; 1.3 307; 2.8 218; 1.5 176 |
| CRYSTALLINE_SILICON | category | 2 | 782 | Y 6.3K; N 29 |
| THIN_FILM_CDTE | category | 2 | 6.4K | Y 688; N 41 |
| THIN_FILM_A_SI | category | 2 | 7.1K | Y 17; N 9 |
| THIN_FILM_CIGS | category | 2 | 7.1K | Y 48; N 5 |
| THIN_FILM_OTHER | category | 2 | 7.1K | Y 33; N 19 |
| OTHER_MATERIALS | category | 2 | 7.0K | N 82; Y 31 |
| NET_METERING_AGREEMENT | category | 3 | 6 | N 6.1K; Y 1.0K; X 35 |
| NET_METERING_DC_CAPACITY_MW | amount | 112 | 6.1K | 2 65; 1.1 53; 1.2 52; 1 45 |
| VIRTUAL_NET_METERING_AGREEMENT | category | 3 | 5 | N 5.8K; Y 1.3K; X 6 |
| VIRTUAL_NET_METERING_DC_CAPACITY_MW | amount | 103 | 5.8K | 1.4 151; 1 123; 2 79; 1.3 68 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:02.10895 7.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 5beb74b7-afc5-4813-9b5d-d 7.2K |
| _SRC_FILE | who | 1 | 0 | 3_3_Solar_Y2024.xlsx 7.2K |
