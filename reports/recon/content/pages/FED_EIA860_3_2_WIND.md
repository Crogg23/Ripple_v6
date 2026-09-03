# FED_EIA860_3_2_WIND

rows 1.6K  columns 26  scan 4.8s

roles: amount 5, audit 2, category 9, date 1, other 5, state 1, who 4

## when

_INGESTED_AT
  2026      1.6K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NAMEPLATE_CAPACITY_MW | 1.6K | 0.10 | 77.70 | 416.44 | 1.0K | 153.5K |
| SUMMER_CAPACITY_MW | 1.6K | 0.10 | 77.70 | 399.82 | 1.0K | 152.1K |
| WINTER_CAPACITY_MW | 1.6K | 0.10 | 77.70 | 399.82 | 1.0K | 152.2K |
| DESIGN_WIND_SPEED_MPH | 1.6K | 7.30 | 17.40 | 26.80 | 27 | 27.3K |
| TURBINE_HUB_HEIGHT_FEET | 1.6K | 80 | 262.40 | 400 | 489 | 409.9K |

## who

PLANT_NAME by rows
        11  Kotzebue Hybrid
         7  Highland Wind Project (IA)
         6  Worthington
         5  Fowler Ridge Wind Farm LLC
         4  Ida Grove Wind
         4  Bowling Green Wind
         4  Allendorf
         4  Grand Ridge Wind Energy Center
         4  Adams Wind
         4  Capricorn Ridge Wind LLC
         4  Maple Ridge Wind Farm
         4  Pomeroy Wind Farm
         4  Fairmont Wind
         4  Gordon Butte Wind LLC
         4  Huerfano River Wind
         4  Solano Wind
         4  Oak Creek Energy Systems I
         3  Deerfield Wind Energy, LLC
         3  Storm Lake 1
         3  Haviland Plastic Products

PLANT_NAME by dollars
        1.0K        1 rows  Great Prairie Wind
         999        1 rows  Traverse Wind Project, LLC
      735.50        3 rows  Horse Hollow Wind Energy Center
      662.50        4 rows  Capricorn Ridge Wind LLC
         604        1 rows  High Banks Wind
      588.30        5 rows  Fowler Ridge Wind Farm LLC
      582.30        1 rows  Rush Creek Wind
         525        1 rows  Aviator Wind
      503.20        1 rows  TB Flats
      500.60        1 rows  White Mesa Wind
         500        7 rows  Highland Wind Project (IA)
         500        2 rows  Orient Wind Farm
         500        1 rows  Young Wind
      499.50        2 rows  High Lonesome Wind Power, LLC Hybrid
      491.60        1 rows  Maverick Creek Wind
      477.10        1 rows  Cheyenne Ridge Wind Farm
      470.40        1 rows  Flat Ridge 2 Wind Energy LLC
      449.70        3 rows  Biglow Canyon Wind Farm
      443.20        1 rows  Rolling Hills Wind Farm
      418.90        1 rows  Mesquite Star

UTILITY_NAME by rows
        65  Avangrid Power LLC
        60  MidAmerican Energy Co
        34  Invenergy Services LLC
        32  Big Sky Wind, LLC
        26  Terra-Gen Operating Co-Wind
        24  Duke Energy Renewables Services
        24  EDF Renewable Asset Holdings, Inc.
        22  Leeward Asset Management, LLC
        18  Greenbacker Renewable Energy Corporation
        18  Pattern Operators LP
        17  PacifiCorp
        16  Consolidated Edison Development Inc.
        16  Northern States Power Co - Minnesota
        15  Southern Power Co
        15  ALLETE Clean Energy
        15  CHI Operations Inc
        14  Evergreen Wind, LLC
        14  DTE Electric Company
        12  Engie North America
        11  Kotzebue Electric Assn Inc

UTILITY_NAME by dollars
        7.8K       65 rows  Avangrid Power LLC
        7.4K       60 rows  MidAmerican Energy Co
        5.6K       32 rows  Big Sky Wind, LLC
        4.5K       34 rows  Invenergy Services LLC
        3.6K       18 rows  Pattern Operators LP
        3.4K       24 rows  Duke Energy Renewables Services
        3.3K       24 rows  EDF Renewable Asset Holdings, Inc.
        2.6K       12 rows  Engie North America
        2.5K       15 rows  Southern Power Co
        2.4K       17 rows  PacifiCorp
        2.3K       16 rows  Northern States Power Co - Minnesota
        2.0K       22 rows  Leeward Asset Management, LLC
        1.6K       11 rows  AE Power Services LLC
        1.6K        9 rows  Enel Green Power NA, Inc.
        1.5K       14 rows  DTE Electric Company
        1.4K        6 rows  BHE Renewables, LLC
        1.3K        7 rows  Interstate Power and Light Co
        1.3K        7 rows  Algonquin Power Co
        1.2K       15 rows  ALLETE Clean Energy
        1.2K        3 rows  Southwestern Electric Power Co

_SRC_FILE by rows
      1.6K  3_2_Wind_Y2024.xlsx

_SRC_FILE by dollars
      152.1K     1.6K rows  3_2_Wind_Y2024.xlsx

COUNTY by rows
        55  Kern
        34  Lincoln
        26  Pipestone
        25  Riverside
        17  Logan
        17  Huron
        16  Solano
        15  Nobles
        15  Hancock
        15  Nolan
        14  Adair
        13  Sherman
        13  Morrow
        11  Franklin
        11  Twin Falls
        11  Kent
        11  NORTHWEST ARCTIC
        11  Umatilla
        11  Gilliam
        10  Benton

COUNTY by dollars
        3.6K       55 rows  Kern
        2.9K       34 rows  Lincoln
        2.6K       15 rows  Nolan
        1.9K       17 rows  Logan
        1.7K       11 rows  Gilliam
        1.5K        6 rows  Custer
        1.5K        7 rows  Garfield
        1.5K        9 rows  Ford
        1.4K        7 rows  Scurry
        1.4K        7 rows  Carbon
        1.3K        8 rows  Sterling
        1.3K       13 rows  Sherman
        1.3K       10 rows  Benton
        1.2K        9 rows  Klickitat
        1.2K        4 rows  Hansford
        1.2K        9 rows  Grant
        1.2K        8 rows  White
        1.2K        5 rows  Haskell
        1.2K        9 rows  Carson
        1.1K        9 rows  Converse

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  Adams Wind                                2026:150
  Allendorf                                 2026:5.60
  Aviator Wind                              2026:525
  Bowling Green Wind                        2026:7.20
  Capricorn Ridge Wind LLC                  2026:662.50
  Deerfield Wind Energy, LLC                2026:149
  Fairmont Wind                             2026:5.20
  Fowler Ridge Wind Farm LLC                2026:588.30
  Gordon Butte Wind LLC                     2026:17.70
  Grand Ridge Wind Energy Center            2026:210
  Great Prairie Wind                        2026:1.0K
  Haviland Plastic Products                 2026:4.50
  High Banks Wind                           2026:604
  Highland Wind Project (IA)                2026:500
  Horse Hollow Wind Energy Center           2026:735.50
  Huerfano River Wind                       2026:8
  Ida Grove Wind                            2026:300
  Kotzebue Hybrid                           2026:3.30
  Maple Ridge Wind Farm                     2026:322.10
  Oak Creek Energy Systems I                2026:34.50
  Orient Wind Farm                          2026:500
  Pomeroy Wind Farm                         2026:296.90
  Rush Creek Wind                           2026:582.30
  Solano Wind                               2026:300.50
  Storm Lake 1                              2026:105.70
  TB Flats                                  2026:503.20
  Traverse Wind Project, LLC                2026:999
  White Mesa Wind                           2026:500.60
  Worthington                               2026:5.60
  Young Wind                                2026:500

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  AE Power Services LLC                     2026:1.6K
  ALLETE Clean Energy                       2026:1.2K
  Algonquin Power Co                        2026:1.3K
  Avangrid Power LLC                        2026:7.8K
  BHE Renewables, LLC                       2026:1.4K
  Big Sky Wind, LLC                         2026:5.6K
  CHI Operations Inc                        2026:28.50
  Consolidated Edison Development Inc.      2026:325.90
  DTE Electric Company                      2026:1.5K
  Duke Energy Renewables Services           2026:3.4K
  EDF Renewable Asset Holdings, Inc.        2026:3.3K
  Enel Green Power NA, Inc.                 2026:1.6K
  Engie North America                       2026:2.6K
  Evergreen Wind, LLC                       2026:700
  Greenbacker Renewable Energy Corporation  2026:290.40
  Interstate Power and Light Co             2026:1.3K
  Invenergy Services LLC                    2026:4.5K
  Kotzebue Electric Assn Inc                2026:3.30
  Leeward Asset Management, LLC             2026:2.0K
  MidAmerican Energy Co                     2026:7.4K
  Northern States Power Co - Minnesota      2026:2.3K
  PacifiCorp                                2026:2.4K
  Pattern Operators LP                      2026:3.6K
  Southern Power Co                         2026:2.5K
  Southwestern Electric Power Co            2026:1.2K
  Terra-Gen Operating Co-Wind               2026:1.1K

## where

STATE: TX 238, IA 158, MN 144, CA 128, OK 72, IL 60, KS 53, OR 53, ND 43, CO 42, OH 41, NE 41

## what

STATUS: OP 99%, OS 1%, OA 0%

TECHNOLOGY: Onshore Wind Turbine 100%, Offshore Wind Turbine 0%

PRIME_MOVER: WT 100%, WS 0%

SECTOR_NAME: IPP Non-CHP 78%, Electric Utility 18%, Commercial Non-CHP 2%, Industrial Non-CHP 2%, Industrial CHP 0%, Commercial CHP 0%

SECTOR: 2 78%, 1 18%, 4 2%, 6 2%, 7 0%, 5 0%

OPERATING_MONTH: 12 33%, 1 8%, 10 8%, 11 8%, 5 6%, 3 6%, 9 6%, 2 6%, 6 5%, 8 5%, 7 5%, 4 5%

OPERATING_YEAR: 2012 15%, 2009 12%, 2011 10%, 2020 9%, 2008 9%, 2016 8%, 2021 7%, 2017 7%, 2015 7%, 2018 6%, 2010 6%, 2007 5%

PREDOMINANT_TURBINE_MANUFACTURER: GE 43%, Vestas 25%, Siemens 8%, Suzlon 5%, Gamesa 5%, Goldwind 3%, Acciona 2%, VENSYS 2%, Mitsubishi 2%, Nordex 2%, Siemens Gamesa 2%, NEG-Micon 2%

WIND_QUALITY_CLASS: 2 59%, 3 27%, 1 11%, 4 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 744 | 0 | 15399 65; 12341 60; 49893 34; 56215 32 |
| UTILITY_NAME | who | 744 | 0 | Avangrid Power LLC 65; MidAmerican Energy Co 60; Invenergy Services LLC 34; Big Sky Wind, LLC 32 |
| PLANT_CODE | other | 1.3K | 0 | 58883 11; 6304 11; 66261 10; 64377 10 |
| PLANT_NAME | who | 1.4K | 0 | Highland Wind Project (IA 11; Kotzebue Hybrid 11; Martin Marietta Wind Proj 10; Milligan 1 Wind Farm 10 |
| STATE | state | 43 | 0 | TX 238; IA 158; MN 144; CA 128 |
| COUNTY | who | 454 | 0 | Kern 55; Lincoln 34; Pipestone 26; Riverside 25 |
| GENERATOR_ID | other | 734 | 0 | 1 439; GEN1 68; WT1 54; 2 39 |
| STATUS | category | 3 | 0 | OP 1.5K; OS 18; OA 4 |
| TECHNOLOGY | category | 2 | 0 | Onshore Wind Turbine 1.6K; Offshore Wind Turbine 3 |
| PRIME_MOVER | category | 2 | 0 | WT 1.6K; WS 3 |
| SECTOR_NAME | category | 6 | 0 | IPP Non-CHP 1.2K; Electric Utility 280; Commercial Non-CHP 30; Industrial Non-CHP 29 |
| SECTOR | category | 6 | 0 | 2 1.2K; 1 280; 4 30; 6 29 |
| NAMEPLATE_CAPACITY_MW | amount | 636 | 0 | 1.5 76; 200 47; 150 42; 10 29 |
| SUMMER_CAPACITY_MW | amount | 643 | 0 | 1.5 72; 200 52; 150 43; 10 29 |
| WINTER_CAPACITY_MW | amount | 646 | 0 | 1.5 72; 200 52; 150 43; 10 29 |
| OPERATING_MONTH | category | 12 | 0 | 12 516; 1 129; 10 124; 11 119 |
| OPERATING_YEAR | category | 41 | 0 | 2012 163; 2009 125; 2011 103; 2020 96 |
| NUMBER_OF_TURBINES | other | 177 | 0 | 1 263; 100 45; 2 38; 3 36 |
| PREDOMINANT_TURBINE_MANUFACTURER | category | 38 | 0 | GE 618; Vestas 360; Siemens 112; Suzlon 79 |
| PREDOMINANT_TURBINE_MODEL_NUMBER | other | 195 | 1 | 1.5 SLE 138; 2.82-127 84; V82-1.65 57; V110-2.0 50 |
| DESIGN_WIND_SPEED_MPH | amount | 110 | 0 | 19 282; 16.8 118; 17 85; 18 57 |
| WIND_QUALITY_CLASS | category | 4 | 0 | 2 920; 3 426; 1 175; 4 42 |
| TURBINE_HUB_HEIGHT_FEET | amount | 198 | 0 | 262.4 306; 262 198; 262.5 98; 213 50 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:37:57.11868 1.6K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 2bf9a448-eb04-42e9-8411-9 1.6K |
| _SRC_FILE | who | 1 | 0 | 3_2_Wind_Y2024.xlsx 1.6K |
