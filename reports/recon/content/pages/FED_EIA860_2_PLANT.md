# FED_EIA860_2_PLANT

rows 16.1K  columns 45  scan 5.4s

roles: amount 5, audit 2, category 14, date 1, id 1, other 9, state 2, who 12

## when

_INGESTED_AT
  2026     16.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 16.1K | 18.97 | 39.35 | 48.95 | 71.29 | 622.3K |
| LONGITUDE | 16.1K | -171.71 | -90.15 | -69.92 | -67.40 | -1.50M |
| GRID_VOLTAGE_KV | 16.0K | 0 | 34.50 | 500 | 765 | 1.46M |
| GRID_VOLTAGE_2_KV | 483 | 0.28 | 34.50 | 500 | 765 | 41.6K |
| GRID_VOLTAGE_3_KV | 85 | 0.48 | 13.80 | 483.20 | 500 | 5.7K |

## who

PLANT_NAME by rows
         2  Bear Creek Solar (CA)
         2  Valdosta
         2  Birch Solar
         2  Unknown
         2  Harris
         1  AES Huntington Beach LLC
         1  Chili Bar
         1  Wheeler Dam
         1  Kings River PH
         1  Seward (AK)
         1  Hank Nikkels Plant 1
         1  Snettisham
         1  Alta Powerhouse
         1  Salt Springs
         1  Yates Dam
         1  Beluga
         1  Green Lake
         1  Copco 2
         1  Hat Creek 1
         1  Roosevelt

PLANT_NAME by dollars
       77.40        2 rows  Harris
       76.06        2 rows  Bear Creek Solar (CA)
       74.95        2 rows  Birch Solar
       71.29        1 rows  Barrow
       70.64        1 rows  NSB Wainwright Utility
       70.48        1 rows  NSB Atqasuk Utility
       70.24        1 rows  TNSG North Plant
       70.22        1 rows  NSB Nuiqsut Utility
       70.20        1 rows  TNSG South Plant
       70.13        1 rows  NSB Kaktovik Utility
       69.74        1 rows  NSB Point Lay Utility
       68.35        1 rows  NSB Point Hope Utility
       68.14        1 rows  NSB Anaktuvuk Pass
       67.73        1 rows  Kivalina
       67.57        1 rows  Noatak
       67.09        1 rows  Ambler
       66.97        1 rows  Kiana
       66.89        1 rows  Shungnak
       66.84        1 rows  Kotzebue Hybrid
       66.83        1 rows  Noorvik

UTILITY_NAME by rows
       241  Cypress Creek Renewables
       227  AES Distributed Energy
       202  Greenbacker Renewable Energy Corporation
       187  MN8 Energy LLC
       178  Altus Power America Management, LLC
       159  Florida Power & Light Co
       142  Strata Manager, LLC
       125  Nautilus Solar Solutions
       105  Consolidated Edison Development Inc.
        90  Walmart Stores Texas, LLC
        89  Southern California Edison Co
        87  Avangrid Power LLC
        87  Duke Energy Renewables Services
        86  Tesla Inc.
        86  Standard Solar
        85  Pacific Gas & Electric Co.
        82  Generate Capital
        78  SoCore Energy LLC
        76  Invenergy Services LLC
        76  PacifiCorp

UTILITY_NAME by dollars
        8.8K      241 rows  Cypress Creek Renewables
        8.6K      227 rows  AES Distributed Energy
        8.2K      202 rows  Greenbacker Renewable Energy Corporation
        7.2K      187 rows  MN8 Energy LLC
        7.0K      178 rows  Altus Power America Management, LLC
        5.3K      125 rows  Nautilus Solar Solutions
        5.1K      142 rows  Strata Manager, LLC
        4.4K      159 rows  Florida Power & Light Co
        3.9K      105 rows  Consolidated Edison Development Inc.
        3.6K       86 rows  Standard Solar
        3.5K       87 rows  Avangrid Power LLC
        3.5K       82 rows  Generate Capital
        3.4K       86 rows  Tesla Inc.
        3.3K       85 rows  Pacific Gas & Electric Co.
        3.2K       76 rows  PacifiCorp
        3.2K       78 rows  SoCore Energy LLC
        3.1K       71 rows  Erie Boulevard Hydropower LP
        3.1K       89 rows  Southern California Edison Co
        3.1K       87 rows  Duke Energy Renewables Services
        2.9K       76 rows  Invenergy Services LLC

NAME_OF_WATER_SOURCE by rows
       732  Municipality
       423  Wells
        65  Mississippi River
        62  Well
        47  Ohio River
        39  Missouri River
        27  Wisconsin River
        26  Lake Michigan
        26  Colorado River
        25  River
        24  Snake River
        23  Androscoggin River
        22  Connecticut River
        21  Air Cooled Condensor
        21  Hudson River
        21  Black River
        20  Arkansas River
        20  Delaware River
        19  Columbia River
        19  Chattahoochee River

NAME_OF_WATER_SOURCE by dollars
       28.3K      732 rows  Municipality
       15.7K      423 rows  Wells
        2.5K       62 rows  Well
        2.5K       65 rows  Mississippi River
        1.8K       47 rows  Ohio River
        1.7K       39 rows  Missouri River
        1.2K       27 rows  Wisconsin River
        1.1K       26 rows  Lake Michigan
        1.0K       24 rows  Snake River
        1.0K       23 rows  Androscoggin River
      946.02       22 rows  Connecticut River
      922.86       21 rows  Black River
      913.94       26 rows  Colorado River
      896.94       25 rows  River
      895.78       21 rows  Hudson River
      883.90       19 rows  Columbia River
      803.20       18 rows  Raquette River
      800.09       20 rows  Delaware River
      791.53       21 rows  Air Cooled Condensor
      719.43       20 rows  Arkansas River

NATURAL_GAS_LDC_NAME by rows
       210  Other - See pipeline notes.
       151  SOUTHERN CALIFORNIA GAS COMPANY
        93  CENTERPOINT ENERGY
        91  ATMOS ENERGY CORPORATION
        59  PACIFIC GAS
        36  KANSAS GAS SERVICE COMPANY
        35  BLACK HILLS ENERGY
        33  CONSOLIDATED EDISON NEW YORK INC
        32  NICOR GAS
        31  SAN DIEGO GAS AND ELECTRIC COMPANY
        27  PUBLIC SERVICE ELECTRIC GAS CO
        27  CONSUMERS ENERGY COMPANY
        26  PIEDMONT NATURAL GAS
        23  QUESTAR GAS COMPANY
        21  TEXAS GAS SERVICE
        17  MINNESOTA ENERGY RESOURCES
        16  MIDAMERICAN ENERGY COMPANY
        16  NIAGARA MOHAWK DBA NATIONAL GRID
        15  YANKEE GAS SVC CO
        15  PEOPLES GAS SYS

NATURAL_GAS_LDC_NAME by dollars
        7.9K      210 rows  Other - See pipeline notes.
        5.2K      151 rows  SOUTHERN CALIFORNIA GAS COMPANY
        3.0K       93 rows  CENTERPOINT ENERGY
        3.0K       91 rows  ATMOS ENERGY CORPORATION
        2.2K       59 rows  PACIFIC GAS
        1.4K       35 rows  BLACK HILLS ENERGY
        1.4K       36 rows  KANSAS GAS SERVICE COMPANY
        1.3K       33 rows  CONSOLIDATED EDISON NEW YORK INC
        1.3K       32 rows  NICOR GAS
        1.2K       27 rows  CONSUMERS ENERGY COMPANY
        1.1K       27 rows  PUBLIC SERVICE ELECTRIC GAS CO
        1.0K       31 rows  SAN DIEGO GAS AND ELECTRIC COMPANY
      932.83       23 rows  QUESTAR GAS COMPANY
      918.70       26 rows  PIEDMONT NATURAL GAS
      757.83       17 rows  MINNESOTA ENERGY RESOURCES
      686.90       16 rows  NIAGARA MOHAWK DBA NATIONAL GRID
      668.85       16 rows  MIDAMERICAN ENERGY COMPANY
      639.20       21 rows  TEXAS GAS SERVICE
      629.99       14 rows  NORTHERN STATES PWR CO
      623.09       15 rows  YANKEE GAS SVC CO

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  AES Huntington Beach LLC                  2026:33.64
  Alta Powerhouse                           2026:39.22
  Barrow                                    2026:71.29
  Bear Creek Solar (CA)                     2026:76.06
  Beluga                                    2026:61.19
  Birch Solar                               2026:74.95
  Chili Bar                                 2026:38.77
  Copco 2                                   2026:41.98
  Green Lake                                2026:56.99
  Hank Nikkels Plant 1                      2026:61.22
  Harris                                    2026:77.40
  Hat Creek 1                               2026:40.93
  Kings River PH                            2026:36.89
  NSB Anaktuvuk Pass                        2026:68.14
  NSB Atqasuk Utility                       2026:70.48
  NSB Kaktovik Utility                      2026:70.13
  NSB Nuiqsut Utility                       2026:70.22
  NSB Point Hope Utility                    2026:68.35
  NSB Point Lay Utility                     2026:69.74
  NSB Wainwright Utility                    2026:70.64
  Roosevelt                                 2026:33.67
  Salt Springs                              2026:38.50
  Seward (AK)                               2026:60.13
  Snettisham                                2026:58.14
  TNSG North Plant                          2026:70.24
  TNSG South Plant                          2026:70.20
  Unknown                                   2026:27.63
  Valdosta                                  2026:61.61
  Wheeler Dam                               2026:34.81
  Yates Dam                                 2026:32.57

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  AES Distributed Energy                    2026:8.6K
  Altus Power America Management, LLC       2026:7.0K
  Avangrid Power LLC                        2026:3.5K
  Consolidated Edison Development Inc.      2026:3.9K
  Cypress Creek Renewables                  2026:8.8K
  Duke Energy Renewables Services           2026:3.1K
  Erie Boulevard Hydropower LP              2026:3.1K
  Florida Power & Light Co                  2026:4.4K
  Generate Capital                          2026:3.5K
  Greenbacker Renewable Energy Corporation  2026:8.2K
  Invenergy Services LLC                    2026:2.9K
  MN8 Energy LLC                            2026:7.2K
  Nautilus Solar Solutions                  2026:5.3K
  PacifiCorp                                2026:3.2K
  Pacific Gas & Electric Co.                2026:3.3K
  SoCore Energy LLC                         2026:3.2K
  Southern California Edison Co             2026:3.1K
  Standard Solar                            2026:3.6K
  Strata Manager, LLC                       2026:5.1K
  Tesla Inc.                                2026:3.4K
  Walmart Stores Texas, LLC                 2026:2.8K

## where

STATE: CA 2.2K, TX 1.4K, NY 1.2K, NC 988, MN 837, MA 700, IL 566, NJ 427, FL 405, CO 342, MI 332, IA 331

TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_STATE: CA 2.2K, NY 1.2K, TX 1.2K, NC 985, MN 802, MA 724, IL 552, NJ 425, FL 385, PA 326, OR 321, CO 311

## what

NERC_REGION: WECC 25%, SERC 20%, NPCC 17%, RFC 15%, MRO 14%, TRE 8%, REC 0%

REGULATORY_STATUS: NR 75%, RE 25%

SECTOR: 2 65%, 1 25%, 4 3%, 7 3%, 6 1%, 5 1%, 3 1%

SECTOR_NAME: IPP Non-CHP 65%, Electric Utility 25%, Commercial Non-CHP 3%, Industrial CHP 3%, Industrial Non-CHP 1%, Commercial CHP 1%, IPP CHP 1%

FERC_COGENERATION_STATUS: N 97%, Y 3%

FERC_SMALL_POWER_PRODUCER_STATUS: N 71%, Y 29%

FERC_EXEMPT_WHOLESALE_GENERATOR_STATUS: N 91%, Y 9%

ASH_IMPOUNDMENT: N 97%, Y 3%

ASH_IMPOUNDMENT_LINED: X 96%, N 2%, Y 1%

ASH_IMPOUNDMENT_STATUS: OP 70%, OS 29%, OA 1%, SB 0%

ENERGY_STORAGE: N 92%, Y 8%

NATURAL_GAS_PIPELINE_NAME_3: VARIBUS LLC 18%, KINDER MORGAN TEXAS PIPELINE L 15%, Other - Please explain in pipe 12%, ENTERPRISE TEXAS PIPELINE 10%, ENBRIDGE PIPELINES EAST TEXAS 8%, BRIDGELINE HOLDINGS LP 8%, MID LOUISIANA GAS TRANSMISSION 8%, ENERGY TRANSFER FUEL LP 5%, TEXAS EASTERN TRANSMISSION LP 5%, KINDER MORGAN TEJAS PIPELINE L 5%, FLORIDA GAS TRANSMISSION COMPA 5%, PANHANDLE EASTERN PIPELINE COM 2%

NATURAL_GAS_STORAGE: N 66%, X 33%, Y 0%

LIQUEFIED_NATURAL_GAS_STORAGE: X 77%, N 23%, Y 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 6.6K | 0 | 61060 269; 61012 242; 60025 224; 61944 210 |
| UTILITY_NAME | who | 6.7K | 0 | Cypress Creek Renewables 269; AES Distributed Energy 242; Greenbacker Renewable Ene 224; MN8 Energy LLC 210 |
| PLANT_CODE | id | 15.8K | 0 | 69099 81; 69098 81; 69097 81; 69096 81 |
| PLANT_NAME | who | 16.3K | 0 | Orion - Helion 81; NJ - CS Energy - Berkeley 81; NJ - CS Energy - Berkeley 81; Jericho 81 |
| STREET_ADDRESS | other | 14.3K | 121 | TBD 805; 5 CO BAR RANCH RD, 80; 24601 West Oakland Ave 79; 500 Las Piedras 78 |
| CITY | who | 5.7K | 36 | TBD 136; Lancaster 104; Houston 86; Coalinga 84 |
| STATE | state | 51 | 0 | CA 2.2K; TX 1.4K; NY 1.2K; NC 988 |
| ZIP | other | 8.1K | 21 | 86001 84; 93210 84; 20774 83; 12883 83 |
| COUNTY | who | 1.5K | 24 | Kern 293; Los Angeles 280; Worcester 198; San Bernardino 181 |
| LATITUDE | amount | 15.4K | 28 | 35.636594 83; 39.9051 82; 33.582903 82; 41.517746 82 |
| LONGITUDE | amount | 15.4K | 28 | -111.88345 83; -74.235121 82; -113.576923 82; -72.897774 82 |
| NERC_REGION | category | 7 | 246 | WECC 4.0K; SERC 3.2K; NPCC 2.7K; RFC 2.4K |
| BALANCING_AUTHORITY_CODE | other | 68 | 292 | MISO 2.6K; PJM 2.2K; CISO 1.9K; ISNE 1.5K |
| BALANCING_AUTHORITY_NAME | who | 69 | 271 | Midcontinent Independent  2.6K; PJM Interconnection, LLC 2.2K; California Independent Sy 1.9K; ISO New England Inc. 1.5K |
| NAME_OF_WATER_SOURCE | who | 1.6K | 11.8K | Municipality 732; Wells 423; Mississippi River 65; Well 62 |
| PRIMARY_PURPOSE_NAICS_CODE | other | 84 | 0 | 22 14.7K; 611 160; 441 116; 622 106 |
| REGULATORY_STATUS | category | 2 | 0 | NR 12.0K; RE 4.1K |
| SECTOR | category | 7 | 0 | 2 10.5K; 1 4.1K; 4 493; 7 451 |
| SECTOR_NAME | category | 7 | 0 | IPP Non-CHP 10.5K; Electric Utility 4.1K; Commercial Non-CHP 493; Industrial CHP 451 |
| FERC_COGENERATION_STATUS | category | 2 | 0 | N 15.7K; Y 447 |
| FERC_COGENERATION_DOCKET_NUMBER | other | 440 | 15.7K | 20-35-000 4; QF22-683-000 3; QF22-609-000 3; QF21-519-000 3 |
| FERC_SMALL_POWER_PRODUCER_STATUS | category | 2 | 0 | N 11.4K; Y 4.7K |
| FERC_SMALL_POWER_PRODUCER_DOCKET_NUMBER | other | 4.4K | 11.4K | pending 53; 22-723-000 29; QF18-1512, QF18-1512-002 25; TBD 25 |
| FERC_EXEMPT_WHOLESALE_GENERATOR_STATUS | category | 2 | 0 | N 14.6K; Y 1.5K |
| FERC_EXEMPT_WHOLESALE_GENERATOR_DOCKET_NUMBER | other | 1.2K | 14.6K | 99-156-000 68; EG22-209-000 26; pending 25; 99-35-000 21 |
| ASH_IMPOUNDMENT | category | 2 | 6.5K | N 9.3K; Y 316 |
| ASH_IMPOUNDMENT_LINED | category | 3 | 7.5K | X 8.3K; N 191; Y 125 |
| ASH_IMPOUNDMENT_STATUS | category | 4 | 15.8K | OP 221; OS 93; OA 2; SB 1 |
| TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER | who | 1.2K | 118 | Southern California Ediso 786; Northern States Power Co  587; Niagara Mohawk Power Corp 558; Pacific Gas & Electric Co 553 |
| TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_ID | who | 1.1K | 123 | 14328 905; 17609 786; 13781 588; 13573 558 |
| TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_STATE | state | 51 | 897 | CA 2.2K; NY 1.2K; TX 1.2K; NC 985 |
| GRID_VOLTAGE_KV | amount | 312 | 147 | 12.47 1.6K; 230 1.2K; 138 1.2K; 115 1.2K |
| GRID_VOLTAGE_2_KV | amount | 73 | 15.6K | 0.48 62; 69 50; 115 43; 138 39 |
| GRID_VOLTAGE_3_KV | amount | 33 | 16.0K | 0.48 14; 69 9; 12 7; 138 6 |
| ENERGY_STORAGE | category | 2 | 205 | N 14.6K; Y 1.3K |
| NATURAL_GAS_LDC_NAME | who | 185 | 14.6K | Other - See pipeline note 210; SOUTHERN CALIFORNIA GAS C 151; CENTERPOINT ENERGY 93; ATMOS ENERGY CORPORATION 91 |
| NATURAL_GAS_PIPELINE_NAME_1 | who | 140 | 14.7K | PACIFIC GAS 105; Other - Please explain in 99; FLORIDA GAS TRANSMISSION  65; TRANSCONTINENTAL GAS PIPE 63 |
| NATURAL_GAS_PIPELINE_NAME_2 | who | 68 | 15.9K | Other - Please explain in 20; GULFSTREAM NATURAL GAS SY 14; KINDER MORGAN TEXAS PIPEL 14; TRANSWESTERN PIPELINE COM 12 |
| NATURAL_GAS_PIPELINE_NAME_3 | category | 27 | 16.1K | VARIBUS LLC 7; KINDER MORGAN TEXAS PIPEL 6; Other - Please explain in 5; ENTERPRISE TEXAS PIPELINE 4 |
| PIPELINE_NOTES | other | 223 | 15.9K | San Joaquin Fuel System;  8; National Grid 5; City of Vernon Gas 3; THUNDER CREEK NGL P L, LL 3 |
| NATURAL_GAS_STORAGE | category | 3 | 7.5K | N 5.7K; X 2.9K; Y 24 |
| LIQUEFIED_NATURAL_GAS_STORAGE | category | 3 | 8.6K | X 5.7K; N 1.7K; Y 10 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:37:40.60977 16.1K |
| _SOURCE_RUN_ID | audit | 1 | 0 | fd7df351-7907-4cc2-8452-1 16.1K |
| _SRC_FILE | who | 1 | 0 | 2___Plant_Y2024.xlsx 16.1K |
