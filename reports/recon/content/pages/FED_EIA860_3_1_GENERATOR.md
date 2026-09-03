# FED_EIA860_3_1_GENERATOR

rows 26.9K  columns 76  scan 6.6s

roles: amount 10, audit 2, category 51, date 1, other 6, state 1, who 6

## when

_INGESTED_AT
  2026     26.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NAMEPLATE_CAPACITY_MW | 26.9K | 0.10 | 4.40 | 620.37 | 1.5K | 1.32M |
| NAMEPLATE_POWER_FACTOR | 18.2K | 0.70 | 0.85 | 1 | 1 | 15.9K |
| SUMMER_CAPACITY_MW | 26.8K | 0.05 | 4 | 588.45 | 1.4K | 1.23M |
| WINTER_CAPACITY_MW | 26.8K | 0.05 | 4 | 598.48 | 1.4K | 1.27M |
| MINIMUM_LOAD_MW | 19.4K | 0 | 1 | 250 | 1.3K | 416.2K |
| PLANNED_NET_SUMMER_CAPACITY_UPRATE_MW | 149 | 0 | 10 | 75.66 | 110.10 | 1.9K |

## who

PLANT_NAME by rows
        73  Edison Sault
        48  Charles City
        48  Chesterfield Landfill Gas
        48  Mountain View
        48  Amelia
        44  SC 1 Data Center, Phase 2
        36  King & Queen
        35  Brunswick Landfill Gas
        35  Kotzebue Hybrid
        33  Great Lakes Hydro America - ME
        33  Grand Coulee
        32  Gowanus Gas Turbines Generating
        32  HEBHoustonDistributionCenter
        30  Pebbly Beach Generating Station Hybrid
        28  FTBLID2
        27  Chief Joseph
        24  The Dalles
        24  OTHERTexasA&M
        24  Pearsall
        23  Allen

PLANT_NAME by dollars
        7.1K       33 rows  Grand Coulee
        4.5K        4 rows  Vogtle
        3.9K        3 rows  Palo Verde
        3.8K       12 rows  West County Energy Center
        3.7K        3 rows  Browns Ferry
        3.6K        9 rows  W A Parish
        3.2K        4 rows  Bowen
        3.1K        5 rows  Gibson
        3.1K       12 rows  Barry
        3.1K        9 rows  Monroe (MI)
        3.0K        8 rows  Crystal River
        3.0K        6 rows  Bath County
        3.0K        7 rows  Turkey Point
        2.9K        3 rows  John E Amos
        2.8K        4 rows  James H Miller Jr
        2.8K        7 rows  Manatee
        2.7K       14 rows  Fort Myers
        2.7K        2 rows  Gavin Power, LLC
        2.6K        2 rows  Rockport
        2.6K        2 rows  South Texas Project

UTILITY_NAME by rows
       329  Industrial Power Generating Company LLC
       285  Tennessee Valley Authority
       267  Power Depot Group A, LLC
       260  AES Distributed Energy
       256  WM Renewable Energy LLC
       247  Walmart Stores Texas, LLC
       214  MN8 Energy LLC
       210  Florida Power & Light Co
       207  Eagle Creek Renewable Energy, LLC
       196  Altus Power America Management, LLC
       196  Cypress Creek Renewables
       191  Texas Microgrid, LLC
       190  Greenbacker Renewable Energy Corporation
       185  U S Bureau of Reclamation
       174  Erie Boulevard Hydropower LP
       153  USACE Northwestern Division
       145  Georgia Power Co
       142  Strata Manager, LLC
       132  MidAmerican Energy Co
       129  Duke Energy Carolinas, LLC

UTILITY_NAME by dollars
       36.9K      210 rows  Florida Power & Light Co
       32.5K      285 rows  Tennessee Valley Authority
       22.3K       22 rows  Constellation Nuclear
       21.7K      129 rows  Duke Energy Carolinas, LLC
       19.5K      145 rows  Georgia Power Co
       19.2K      106 rows  Virginia Electric & Power Co
       15.1K      185 rows  U S Bureau of Reclamation
       14.5K       92 rows  Alabama Power Co
       12.9K      153 rows  USACE Northwestern Division
       12.6K       73 rows  Duke Energy Progress - (NC)
       12.6K      103 rows  Southern Power Co
       12.3K      132 rows  MidAmerican Energy Co
       12.0K      114 rows  PacifiCorp
       11.6K       44 rows  Entergy Louisiana LLC
       11.6K       97 rows  Duke Energy Florida, LLC
       10.9K      103 rows  DTE Electric Company
       10.8K       43 rows  Luminant Generation Company LLC
       10.4K       78 rows  Invenergy Services LLC
        9.8K       75 rows  Arizona Public Service Co
        9.3K      127 rows  Northern States Power Co - Minnesota

RTO_ISO_LMP_NODE_DESIGNATION by rows
        78  AMIL.IP.IMEA
        73  MIUP.CLVHDRTN1
        57  none
        48  21601804
        48  36181301
        48  36181313
        48  36181305
        42  CP/Comm Pricing
        36  61482315
        35  Zonal
        35  WPS.WPSM
        35  57967665
        35  WE
        24  PEARSA_1_24
        24  24048
        24  AMIL.IMEA1
        23  4168
        22  CONS.MPPA
        21  SPP
        20  24044

RTO_ISO_LMP_NODE_DESIGNATION by dollars
        6.8K       42 rows  CP/Comm Pricing
        5.4K       57 rows  none
        2.8K       15 rows  FRCC
        2.5K       13 rows  PJM
        1.4K        1 rows  EES.G_GULF_A
        1.3K        1 rows  40243839
        1.3K        1 rows  40243837
        1.3K        1 rows  20141103
        1.3K        1 rows  20141102
        1.3K        3 rows  Carson Substation
        1.2K        1 rows  50655
        1.2K        1 rows  50654
        1.2K        1 rows  UN.MILLSTONE3
        1.2K        6 rows  VLSES_Unit 3
        1.2K        6 rows  DLTAPLNT
        1.2K        1 rows  AMMO.CALLAWAY1
        1.2K        1 rows  86031201
        1.2K        1 rows  1097732449
        1.2K        1 rows  40243803
        1.2K        1 rows  86041201

RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC by rows
        78  AMIL.IP.IMEA
        57  none
        45  34497125
        42  CP/Comm Pricing
        35  WPS.WPSM
        35  WE
        35  Zonal
        25  MISO
        24  24048
        24  AMIL.IMEA1
        21  TH_ZP26_GEN-APND
        21  SPP
        20  Centra Homa
        20  24044
        20  24041
        19  EIA
        19  ALTW.ALTW
        18  BPA
        17  24058
        16  591_:_UN_PRID_CRN115_SWBK

RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC by dollars
        6.8K       42 rows  CP/Comm Pricing
        5.4K       57 rows  none
        4.8K       45 rows  34497125
        3.1K       14 rows  PJM
        2.8K       15 rows  FRCC
        2.3K        2 rows  SALEM   25 KV
        1.4K        1 rows  EES.G_GULF_A
        1.4K       19 rows  EIA
        1.3K        6 rows  LINDEN  18 KV
        1.3K        1 rows  20141103
        1.3K        1 rows  20141102
        1.3K        3 rows  Carson Substation
        1.3K        8 rows  BERGEN  18 KV
        1.2K        1 rows  50655
        1.2K        1 rows  50654
        1.2K        1 rows  UN.MILLSTONE3
        1.2K        6 rows  VLSES_Unit 3
        1.2K        6 rows  DLTAPLNT
        1.2K        1 rows  86031201
        1.2K        1 rows  HOPECREE25 KV

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  Allen                                     2026:1.5K
  Amelia                                    2026:14.40
  Barry                                     2026:3.1K
  Bowen                                     2026:3.2K
  Browns Ferry                              2026:3.7K
  Brunswick Landfill Gas                    2026:10.50
  Charles City                              2026:14.40
  Chesterfield Landfill Gas                 2026:14.40
  Chief Joseph                              2026:2.5K
  Crystal River                             2026:3.0K
  Edison Sault                              2026:29.20
  FTBLID2                                   2026:11.20
  Gibson                                    2026:3.1K
  Gowanus Gas Turbines Generating           2026:580.20
  Grand Coulee                              2026:7.1K
  Great Lakes Hydro America - ME            2026:153.10
  HEBHoustonDistributionCenter              2026:12.80
  King & Queen                              2026:10.80
  Kotzebue Hybrid                           2026:18
  Monroe (MI)                               2026:3.1K
  Mountain View                             2026:14.40
  OTHERTexasA&M                             2026:9.60
  Palo Verde                                2026:3.9K
  Pearsall                                  2026:201.60
  Pebbly Beach Generating Station Hybrid    2026:12.70
  SC 1 Data Center, Phase 2                 2026:99.60
  The Dalles                                2026:1.8K
  Vogtle                                    2026:4.5K
  W A Parish                                2026:3.6K
  West County Energy Center                 2026:3.8K

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = SUMMER_CAPACITY_MW
  AES Distributed Energy                    2026:4.4K
  Alabama Power Co                          2026:14.5K
  Altus Power America Management, LLC       2026:555.83
  Constellation Nuclear                     2026:22.3K
  Cypress Creek Renewables                  2026:1.8K
  DTE Electric Company                      2026:10.9K
  Duke Energy Carolinas, LLC                2026:21.7K
  Duke Energy Florida, LLC                  2026:11.6K
  Duke Energy Progress - (NC)               2026:12.6K
  Eagle Creek Renewable Energy, LLC         2026:639.70
  Entergy Louisiana LLC                     2026:11.6K
  Erie Boulevard Hydropower LP              2026:671.20
  Florida Power & Light Co                  2026:36.9K
  Georgia Power Co                          2026:19.5K
  Greenbacker Renewable Energy Corporation  2026:1.3K
  Industrial Power Generating Company LLC   2026:98.70
  Luminant Generation Company LLC           2026:10.8K
  MN8 Energy LLC                            2026:2.4K
  MidAmerican Energy Co                     2026:12.3K
  PacifiCorp                                2026:12.0K
  Power Depot Group A, LLC                  2026:134.70
  Southern Power Co                         2026:12.6K
  Strata Manager, LLC                       2026:746.50
  Tennessee Valley Authority                2026:32.5K
  Texas Microgrid, LLC                      2026:76.40
  U S Bureau of Reclamation                 2026:15.1K
  USACE Northwestern Division               2026:12.9K
  Virginia Electric & Power Co              2026:19.2K
  WM Renewable Energy LLC                   2026:289.30
  Walmart Stores Texas, LLC                 2026:107.80

## where

STATE: CA 3.0K, TX 2.2K, NY 1.9K, MN 1.3K, NC 1.2K, MA 971, IL 838, MI 770, VA 730, IA 717, FL 707, WI 645

## what

TECHNOLOGY: Solar Photovoltaic 28%, Conventional Hydroelectric 15%, Petroleum Liquids 15%, Natural Gas Fired Combustion T 9%, Natural Gas Fired Combined Cyc 8%, Natural Gas Internal Combustio 7%, Onshore Wind Turbine 6%, Landfill Gas 5%, Batteries 3%, Natural Gas Steam Turbine 2%, Conventional Steam Coal 2%, Wood/Wood Waste Biomass 1%

PRIME_MOVER: PV 27%, IC 24%, HY 15%, GT 10%, ST 6%, WT 6%, CT 5%, BA 3%, CA 3%, FC 1%, PS 1%, BT 0%

OWNERSHIP: S 88%, W 9%, J 3%

DUCT_BURNERS: X 97%, Y 2%, N 1%

CAN_BYPASS_HEAT_RECOVERY_STEAM_GENERATOR: X 95%, N 4%, Y 1%

UPRATE_OR_DERATE_COMPLETED_DURING_YEAR: N 100%, Y 0%

MONTH_UPRATE_OR_DERATE_COMPLETED: 4 23%, 7 19%, 5 19%, 6 9%, 10 6%, 12 6%, 11 6%, 8 4%, 1 4%, 3 4%, 2 2%

YEAR_UPRATE_OR_DERATE_COMPLETED: 2024 100%

STATUS: OP 92%, SB 6%, OS 2%, OA 1%

SYNCHRONIZED_TO_TRANSMISSION_GRID: X 94%, Y 4%, N 2%

OPERATING_MONTH: 12 16%, 1 11%, 6 11%, 7 9%, 5 8%, 8 8%, 11 7%, 10 7%, 9 6%, 4 6%, 3 6%, 2 4%

PLANNED_RETIREMENT_MONTH: 12 52%, 6 12%, 3 8%, 5 7%, 10 5%, 7 4%, 1 3%, 8 3%, 9 2%, 4 2%, 11 2%

PLANNED_RETIREMENT_YEAR: 2025 23%, 2026 17%, 2027 15%, 2028 11%, 2031 8%, 2030 6%, 2033 5%, 2032 5%, 2029 4%, 2040 3%, 2035 2%

ASSOCIATED_WITH_COMBINED_HEAT_AND_POWER_SYSTEM: N 93%, Y 7%

SECTOR_NAME: IPP Non-CHP 49%, Electric Utility 37%, Commercial Non-CHP 5%, Industrial CHP 4%, Commercial CHP 3%, Industrial Non-CHP 2%, IPP CHP 2%

SECTOR: 2 49%, 1 37%, 4 5%, 7 4%, 5 3%, 6 2%, 3 2%

TOPPING_OR_BOTTOMING: X 93%, T 7%, B 1%

ENERGY_SOURCE_1: SUN 27%, NG 26%, WAT 16%, DFO 14%, WND 6%, LFG 5%, MWH 3%, SUB 1%, BIT 1%, OBG 1%, GEO 1%, WDS 1%

ENERGY_SOURCE_2: DFO 63%, NG 21%, OG 3%, BIT 3%, LFG 2%, WDS 2%, RFO 2%, KER 1%, SUB 1%, OBG 1%, PG 1%, OBL 0%

ENERGY_SOURCE_3: WDS 21%, DFO 19%, NG 17%, RFO 10%, BIT 10%, WO 5%, SLW 5%, OBG 4%, LFG 3%, OTH 3%, TDF 2%, OBS 2%

ENERGY_SOURCE_4: RFO 16%, DFO 15%, BIT 12%, TDF 10%, WDS 9%, OTH 9%, NG 8%, OBL 6%, SLW 5%, PC 5%, OBS 3%, WO 2%

ENERGY_SOURCE_5: DFO 21%, SLW 18%, RFO 11%, NG 10%, TDF 9%, BIT 9%, WDS 8%, WO 4%, OBS 3%, OBG 2%, BLQ 2%, OTH 2%

ENERGY_SOURCE_6: TDF 21%, DFO 19%, RFO 13%, OTH 11%, WDS 9%, OBS 6%, NG 6%, SLW 4%, BLQ 4%, PC 4%, BIT 2%

STARTUP_SOURCE_1: NG 58%, DFO 30%, GEO 2%, WDS 2%, RFO 2%, WH 1%, OG 1%, PG 1%, SUB 1%, LFG 0%, OBG 0%, BLQ 0%

STARTUP_SOURCE_2: DFO 36%, NG 28%, RFO 11%, PG 7%, OG 4%, OBG 4%, WDS 3%, BIT 3%, WO 2%, SUB 1%, BLQ 0%

STARTUP_SOURCE_3: NG 41%, DFO 33%, SUB 11%, BLQ 7%, WDS 7%

STARTUP_SOURCE_4: BLQ 60%, WDS 20%, WDL 20%

SOLID_FUEL_GASIFICATION_SYSTEM: N 100%, Y 0%

CARBON_CAPTURE_TECHNOLOGY: N 100%, Y 0%

TIME_FROM_COLD_SHUTDOWN_TO_FULL_LOAD: 10M 45%, 1H 31%, 12H 18%, OVER 6%

FLUIDIZED_BED_TECHNOLOGY: N 52%, Y 48%

PULVERIZED_COAL_TECHNOLOGY: Y 66%, N 34%

STOKER_TECHNOLOGY: N 51%, Y 49%

OTHER_COMBUSTION_TECHNOLOGY: N 84%, Y 16%

SUBCRITICAL_TECHNOLOGY: Y 63%, N 37%

SUPERCRITICAL_TECHNOLOGY: Y 61%, N 39%

ULTRASUPERCRITICAL_TECHNOLOGY: N 84%, Y 16%

PLANNED_UPRATE_MONTH: 12 28%, 6 19%, 5 13%, 1 10%, 10 9%, 4 7%, 7 4%, 11 4%, 3 3%, 9 3%, 2 1%

PLANNED_UPRATE_YEAR: 2025 33%, 2026 28%, 2027 20%, 2028 7%, 2029 6%, 2035 2%, 2030 2%, 2031 1%, 2024 1%

PLANNED_DERATE_MONTH: 1 40%, 4 40%, 6 20%

PLANNED_DERATE_YEAR: 2025 80%, 2026 20%

PLANNED_NEW_PRIME_MOVER: WT 62%, ST 19%, IC 6%, HY 6%, PV 5%, BA 2%

PLANNED_ENERGY_SOURCE_1: WND 62%, NG 25%, WAT 6%, SUN 5%, MWH 2%

PLANNED_REPOWER_MONTH: 12 33%, 1 12%, 10 12%, 11 9%, 3 8%, 6 6%, 7 5%, 8 5%, 5 5%, 9 3%, 2 2%

PLANNED_REPOWER_YEAR: 2025 59%, 2026 19%, 2028 11%, 2027 8%, 2030 2%, 2024 2%

OTHER_PLANNED_MODIFICATIONS: N 92%, Y 8%

OTHER_MODIFICATIONS_MONTH: 12 25%, 10 16%, 6 13%, 5 13%, 3 7%, 4 6%, 11 6%, 8 5%, 2 4%, 7 3%, 9 2%

OTHER_MODIFICATIONS_YEAR: 2025 38%, 2026 24%, 2028 9%, 2027 8%, 2029 8%, 2030 4%, 2031 4%, 2033 2%, 2032 2%, 2024 1%, 2035 1%

MULTIPLE_FUELS: N 82%, Y 18%, U 0%

COFIRE_FUELS: N 83%, Y 17%

SWITCH_BETWEEN_OIL_AND_NATURAL_GAS: N 78%, Y 22%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 5.6K | 0 | 55938 387; 64812 371; 64315 348; 61012 318 |
| UTILITY_NAME | who | 5.7K | 1 | Industrial Power Generati 387; Power Depot Group A, LLC 371; Walmart Stores Texas, LLC 348; AES Distributed Energy 318 |
| PLANT_CODE | other | 13.1K | 1 | 66567 157; 66595 153; 67318 152; 67766 148 |
| PLANT_NAME | who | 13.6K | 2 | HEBHoustonDistributionCen 157; FTBLID2 153; OTHERTexasA&M 152; Yellowstone County Genera 148 |
| STATE | state | 51 | 2 | CA 3.0K; TX 2.2K; NY 1.9K; MN 1.3K |
| COUNTY | who | 1.4K | 2 | Los Angeles 417; Kern 363; Harris 334; Worcester 275 |
| GENERATOR_ID | other | 9.9K | 1 | 1 2.9K; 2 1.5K; GEN1 1.0K; 3 996 |
| TECHNOLOGY | category | 27 | 1 | Solar Photovoltaic 7.1K; Conventional Hydroelectri 4.0K; Petroleum Liquids 3.9K; Natural Gas Fired Combust 2.2K |
| PRIME_MOVER | category | 18 | 1 | PV 7.1K; IC 6.4K; HY 4.0K; GT 2.8K |
| UNIT_CODE | other | 305 | 24.7K | CC1 778; CC2 72; CC01 59; 1 47 |
| OWNERSHIP | category | 3 | 1 | S 23.6K; W 2.5K; J 746 |
| DUCT_BURNERS | category | 3 | 1 | X 26.1K; Y 492; N 258 |
| CAN_BYPASS_HEAT_RECOVERY_STEAM_GENERATOR | category | 3 | 1 | X 25.5K; N 1.0K; Y 268 |
| RTO_ISO_LMP_NODE_DESIGNATION | who | 2.9K | 21.3K | AMIL.IP.IMEA 78; MIUP.CLVHDRTN1 75; 21601804 65; 36181301 65 |
| RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC | who | 2.5K | 22.4K | AMIL.IP.IMEA 78; none 57; 34497125 45; Zonal 44 |
| NAMEPLATE_CAPACITY_MW | amount | 2.0K | 1 | 1 1.6K; 2 1.6K; 5 985; 0.4 779 |
| NAMEPLATE_POWER_FACTOR | amount | 52 | 8.7K | 0.8 6.7K; 0.85 3.5K; 0.9 3.4K; 1 2.4K |
| SUMMER_CAPACITY_MW | amount | 2.2K | 78 | 1 1.4K; 2 1.4K; 5 920; 0.4 905 |
| WINTER_CAPACITY_MW | amount | 2.2K | 96 | 1 1.4K; 2 1.4K; 5 897; 0.4 826 |
| MINIMUM_LOAD_MW | amount | 583 | 7.5K | 0.1 3.1K; 0 1.5K; 1 1.2K; 0.5 1.2K |
| UPRATE_OR_DERATE_COMPLETED_DURING_YEAR | category | 2 | 1 | N 26.8K; Y 51 |
| MONTH_UPRATE_OR_DERATE_COMPLETED | category | 12 | 26.8K | 4 12; 7 10; 5 10; 6 5 |
| YEAR_UPRATE_OR_DERATE_COMPLETED | category | 2 | 26.8K | 2024 53 |
| STATUS | category | 4 | 1 | OP 24.7K; SB 1.5K; OS 479; OA 203 |
| SYNCHRONIZED_TO_TRANSMISSION_GRID | category | 3 | 1 | X 25.3K; Y 949; N 561 |
| OPERATING_MONTH | category | 13 | 2 | 12 4.3K; 1 3.0K; 6 3.0K; 7 2.4K |
| OPERATING_YEAR | other | 131 | 2 | 2021 1.2K; 2020 1.1K; 2024 1.0K; 2017 959 |
| PLANNED_RETIREMENT_MONTH | category | 13 | 26.3K | 12 272; 6 63; 3 43; 5 39 |
| PLANNED_RETIREMENT_YEAR | category | 35 | 26.3K | 2025 107; 2026 81; 2027 69; 2028 50 |
| ASSOCIATED_WITH_COMBINED_HEAT_AND_POWER_SYSTEM | category | 2 | 344 | N 24.6K; Y 2.0K |
| SECTOR_NAME | category | 7 | 2 | IPP Non-CHP 13.2K; Electric Utility 9.8K; Commercial Non-CHP 1.2K; Industrial CHP 1.0K |
| SECTOR | category | 8 | 2 | 2 13.2K; 1 9.8K; 4 1.2K; 7 1.0K |
| TOPPING_OR_BOTTOMING | category | 3 | 344 | X 24.6K; T 1.8K; B 183 |
| ENERGY_SOURCE_1 | category | 34 | 1 | SUN 7.2K; NG 6.7K; WAT 4.1K; DFO 3.7K |
| ENERGY_SOURCE_2 | category | 29 | 23.5K | DFO 2.1K; NG 680; OG 108; BIT 84 |
| ENERGY_SOURCE_3 | category | 25 | 26.4K | WDS 75; DFO 70; NG 60; RFO 36 |
| ENERGY_SOURCE_4 | category | 19 | 26.7K | RFO 27; DFO 26; BIT 20; TDF 17 |
| ENERGY_SOURCE_5 | category | 16 | 26.8K | DFO 20; SLW 17; RFO 11; NG 10 |
| ENERGY_SOURCE_6 | category | 11 | 26.8K | TDF 10; DFO 9; RFO 6; OTH 5 |
| STARTUP_SOURCE_1 | category | 25 | 24.1K | NG 1.5K; DFO 810; GEO 62; WDS 51 |
| STARTUP_SOURCE_2 | category | 11 | 26.6K | DFO 88; NG 69; RFO 26; PG 18 |
| STARTUP_SOURCE_3 | category | 5 | 26.8K | NG 11; DFO 9; SUB 3; BLQ 2 |
| STARTUP_SOURCE_4 | category | 3 | 26.9K | BLQ 3; WDS 1; WDL 1 |
| SOLID_FUEL_GASIFICATION_SYSTEM | category | 2 | 8.8K | N 18.0K; Y 19 |
| CARBON_CAPTURE_TECHNOLOGY | category | 2 | 11.6K | N 15.2K; Y 13 |
| TURBINES_OR_HYDROKINETIC_BUOYS | other | 178 | 23.4K | 0 1.9K; 1 263; 100 45; 2 38 |
| TIME_FROM_COLD_SHUTDOWN_TO_FULL_LOAD | category | 4 | 8.4K | 10M 8.3K; 1H 5.8K; 12H 3.3K; OVER 1.1K |
| FLUIDIZED_BED_TECHNOLOGY | category | 2 | 26.7K | N 95; Y 86 |
| PULVERIZED_COAL_TECHNOLOGY | category | 2 | 26.2K | Y 416; N 215 |
| STOKER_TECHNOLOGY | category | 2 | 26.7K | N 60; Y 58 |
| OTHER_COMBUSTION_TECHNOLOGY | category | 2 | 26.7K | N 164; Y 31 |
| SUBCRITICAL_TECHNOLOGY | category | 2 | 26.1K | Y 492; N 292 |
| SUPERCRITICAL_TECHNOLOGY | category | 2 | 26.7K | Y 89; N 58 |
| ULTRASUPERCRITICAL_TECHNOLOGY | category | 2 | 26.8K | N 31; Y 6 |
| PLANNED_NET_SUMMER_CAPACITY_UPRATE_MW | amount | 51 | 26.7K | 10 10; 14 10; 0.9 8; 4 7 |
| PLANNED_NET_WINTER_CAPACITY_UPRATE_MW | amount | 46 | 26.7K | 0 21; 14 10; 20 8; 0.9 8 |
| PLANNED_UPRATE_MONTH | category | 13 | 26.7K | 12 41; 6 28; 5 19; 1 14 |
| PLANNED_UPRATE_YEAR | category | 10 | 26.7K | 2025 49; 2026 42; 2027 29; 2028 10 |
| PLANNED_NET_SUMMER_CAPACITY_DERATE_MW | amount | 5 | 26.9K | 0.2 2; 179 1; 12.3 1; 57 1 |
| PLANNED_NET_WINTER_CAPACITY_DERATE_MW | amount | 5 | 26.9K | 0.2 2; 179 1; 12.3 1; 62 1 |
| PLANNED_DERATE_MONTH | category | 4 | 26.9K | 1 2; 4 2; 6 1 |
| PLANNED_DERATE_YEAR | category | 3 | 26.9K | 2025 4; 2026 1 |
| PLANNED_NEW_PRIME_MOVER | category | 6 | 26.8K | WT 40; ST 12; IC 4; HY 4 |
| PLANNED_ENERGY_SOURCE_1 | category | 5 | 26.8K | WND 40; NG 16; WAT 4; SUN 3 |
| PLANNED_NEW_NAMEPLATE_CAPACITY_MW | amount | 49 | 26.8K | 1.6 5; 1 3; 0.5 3; 360 3 |
| PLANNED_REPOWER_MONTH | category | 12 | 26.8K | 12 21; 1 8; 10 8; 11 6 |
| PLANNED_REPOWER_YEAR | category | 7 | 26.8K | 2025 38; 2026 12; 2028 7; 2027 5 |
| OTHER_PLANNED_MODIFICATIONS | category | 2 | 25.3K | N 1.5K; Y 129 |
| OTHER_MODIFICATIONS_MONTH | category | 13 | 26.7K | 12 31; 10 20; 6 17; 5 16 |
| OTHER_MODIFICATIONS_YEAR | category | 14 | 26.7K | 2025 48; 2026 30; 2028 12; 2027 10 |
| MULTIPLE_FUELS | category | 3 | 8.1K | N 15.4K; Y 3.4K; U 12 |
| COFIRE_FUELS | category | 2 | 17.5K | N 7.8K; Y 1.6K |
| SWITCH_BETWEEN_OIL_AND_NATURAL_GAS | category | 2 | 18.0K | N 6.9K; Y 1.9K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:37:51.63084 26.9K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 3a8a9967-5770-4f52-b871-0 26.9K |
| _SRC_FILE | who | 1 | 0 | 3_1_Generator_Y2024.xlsx 26.9K |
