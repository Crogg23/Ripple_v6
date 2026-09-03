# FED_EIA860_4_OWNER

rows 5.5K  columns 17  scan 4.0s

roles: amount 1, audit 2, category 1, date 1, other 3, state 2, who 8

## when

_INGESTED_AT
  2026      5.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERCENT_OWNED | 5.5K | 0 | 1 | 1 | 1 | 3.8K |

## who

PLANT_NAME by rows
        63  VMEA 1 Credit Gen
        60  Montpelier
        60  Dover Peaking
        38  Desert Sunlight 250, LLC
        36  Linden Cogen Plant
        35  Desert Sunlight 300, LLC
        30  Keystone
        30  Conemaugh
        30  Seville
        30  Galion
        28  VMEA Peaking Gen
        27  Versailles Peaking
        27  Stony Brook
        24  West Riverside Energy Center
        24  Tenaska Georgia Generation Facility
        24  Redbud Power Plant
        24  Napoleon Peaking
        21  Palo Verde
        20  Belleville Dam
        20  Tenaska Frontier Generation Station

PLANT_NAME by dollars
          16       16 rows  Second Imperial Geothermal
          14       14 rows  Anson Abenaki Hydros
          13       13 rows  PSEG Linden Generating Station
          12       12 rows  Ball Mountain Hydro
          12       12 rows  NCAH Central Utility Plant
          11       11 rows  Pelican
          11       35 rows  Desert Sunlight 300, LLC
          11       11 rows  Nantucket Hybrid
          11       11 rows  Sartell Dam
          10       10 rows  Pueblo Airport Generating Station
          10       10 rows  Topaz Generating
        9.50       14 rows  Long Beach Generation LLC
           9       36 rows  Linden Cogen Plant
           9        9 rows  Elwood Energy LLC
           9        9 rows  Union Power Station
           9       18 rows  Basin Creek Plant
           9       27 rows  Stony Brook
           9       38 rows  Desert Sunlight 250, LLC
           9        9 rows  International Paper Livermore Hydro
           9       63 rows  VMEA 1 Credit Gen

OWNER_NAME by rows
        40  Nordic Solar, LLC
        35  Other
        34  John Hancock Funding Company
        34  City of Hamilton - (OH)
        33  Manulife Infrastructure II Holdings A, L.P.
        33  Cordelio BNC Holdings, LLC
        30  Hunt Energy Network, LLC
        30  City of Wadsworth - (OH)
        30  City of Cuyahoga Falls - (OH)
        30  City of Bowling Green - (OH)
        29  Florida Municipal Power Agency
        29  Wisconsin Public Service Corp
        28  City of St Marys - (OH)
        28  City of Dover - (OH)
        28  City of Painesville
        27  FirstLight Hydro Generating Company
        26  NJR Clean Energy Ventures III Corporation
        26  Public Service Co of NM
        25  City of Galion
        24  Shaw Creek Solar

OWNER_NAME by dollars
          40       40 rows  Nordic Solar, LLC
          27       27 rows  FirstLight Hydro Generating Company
          26       26 rows  NJR Clean Energy Ventures III Corporation
          24       24 rows  Generate NY Community Solar Lessor III
          23       23 rows  Andro Hydro, LLC
          21       21 rows  Ormat Nevada Inc
          20       20 rows  SoCore 2016 ProjectCo-W1 LLC
          18       18 rows  Hawthorne Power Systems
          18       20 rows  Standard Solar
          18       18 rows  Lightstone Generation LLC
       17.49       33 rows  Manulife Infrastructure II Holdings A, L.P.
       17.32       24 rows  U S Bureau of Reclamation
          17       17 rows  Luminant Gen Co LLC Fin Holding
       16.50       33 rows  Cordelio BNC Holdings, LLC
       16.46       29 rows  Florida Municipal Power Agency
       16.32       26 rows  Public Service Co of NM
          16       16 rows  ArcLight Capital Partners LLC
          15       15 rows  CD US Solar PO 2 LLC
          15       15 rows  N.E.W. Hydro, LLC
          15       15 rows  TransAlta Corporation

UTILITY_NAME by rows
       285  American Mun Power-Ohio, Inc
       211  Eagle Creek Renewable Energy, LLC
       140  Strata Manager, LLC
       102  HEN Infrastructure, L.L.C.
        93  City of Manassas - (VA)
        87  Generate Capital
        64  Duke Energy Renewables Services
        60  KeyCon Operating LLC
        60  MN8 Energy LLC
        57  Southern Power Co
        54  United States Solar Corporation
        53  Lightsource Renewable Energy Asset Management, LLC
        48  Georgia Power Co
        44  MidAmerican Energy Co
        43  NJR Clean Energy Ventures Corporation
        43  Bloom Energy
        43  CleanCapital Holdings
        40  ProEnergy Services
        40  Standard Solar
        40  National Grid Renewables

UTILITY_NAME by dollars
         211      211 rows  Eagle Creek Renewable Energy, LLC
         140      140 rows  Strata Manager, LLC
          87       87 rows  Generate Capital
          59       64 rows  Duke Energy Renewables Services
          58       60 rows  MN8 Energy LLC
          57       57 rows  Southern Power Co
          54       54 rows  United States Solar Corporation
          53       53 rows  Lightsource Renewable Energy Asset Management, LLC
          43       43 rows  NJR Clean Energy Ventures Corporation
          43       43 rows  Bloom Energy
          40       40 rows  ProEnergy Services
          40       40 rows  National Grid Renewables
          38       38 rows  SoCore Energy LLC
          34       34 rows  Luminant Generation Company LLC
       33.90      102 rows  HEN Infrastructure, L.L.C.
          33       33 rows  Tesla Inc.
       32.75      285 rows  American Mun Power-Ohio, Inc
          31       31 rows  Ecoplexus, Inc
          27       27 rows  FirstLight Power Resources Services LLC
          25       43 rows  CleanCapital Holdings

_SRC_FILE by rows
      5.5K  4___Owner_Y2024.xlsx

_SRC_FILE by dollars
        3.8K     5.5K rows  4___Owner_Y2024.xlsx

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = PERCENT_OWNED
  Anson Abenaki Hydros                      2026:14
  Ball Mountain Hydro                       2026:12
  Belleville Dam                            2026:2.02
  Conemaugh                                 2026:6
  Desert Sunlight 250, LLC                  2026:9
  Desert Sunlight 300, LLC                  2026:11
  Dover Peaking                             2026:5.94
  Galion                                    2026:2.97
  Keystone                                  2026:6
  Linden Cogen Plant                        2026:9
  Montpelier                                2026:5.94
  NCAH Central Utility Plant                2026:12
  Nantucket Hybrid                          2026:11
  Napoleon Peaking                          2026:2.97
  PSEG Linden Generating Station            2026:13
  Palo Verde                                2026:3
  Pelican                                   2026:11
  Pueblo Airport Generating Station         2026:10
  Redbud Power Plant                        2026:8
  Sartell Dam                               2026:11
  Second Imperial Geothermal                2026:16
  Seville                                   2026:2.97
  Stony Brook                               2026:9
  Tenaska Frontier Generation Station       2026:3.96
  Tenaska Georgia Generation Facility       2026:5.94
  Topaz Generating                          2026:10
  VMEA 1 Credit Gen                         2026:9
  VMEA Peaking Gen                          2026:4
  Versailles Peaking                        2026:2.97
  West Riverside Energy Center              2026:4.08

OWNER_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = PERCENT_OWNED
  Andro Hydro, LLC                          2026:23
  ArcLight Capital Partners LLC             2026:16
  City of Bowling Green - (OH)              2026:4.24
  City of Cuyahoga Falls - (OH)             2026:2.30
  City of Dover - (OH)                      2026:1.40
  City of Galion                            2026:1
  City of Hamilton - (OH)                   2026:9.78
  City of Painesville                       2026:1.40
  City of St Marys - (OH)                   2026:1
  City of Wadsworth - (OH)                  2026:1.80
  Cordelio BNC Holdings, LLC                2026:16.50
  FirstLight Hydro Generating Company       2026:27
  Florida Municipal Power Agency            2026:16.46
  Generate NY Community Solar Lessor III    2026:24
  Hawthorne Power Systems                   2026:18
  Hunt Energy Network, LLC                  2026:1.14
  John Hancock Funding Company              2026:14.62
  Lightstone Generation LLC                 2026:18
  Luminant Gen Co LLC Fin Holding           2026:17
  Manulife Infrastructure II Holdings A, L  2026:17.49
  NJR Clean Energy Ventures III Corporatio  2026:26
  Nordic Solar, LLC                         2026:40
  Ormat Nevada Inc                          2026:21
  Other                                     2026:13.17
  Public Service Co of NM                   2026:16.32
  Shaw Creek Solar                          2026:13
  SoCore 2016 ProjectCo-W1 LLC              2026:20
  Standard Solar                            2026:18
  U S Bureau of Reclamation                 2026:17.32
  Wisconsin Public Service Corp             2026:13.32

## where

STATE: CA 771, TX 485, OH 347, NY 330, MN 302, NC 266, MA 191, NJ 189, PA 167, VA 166, WI 158, GA 148

OWNER_STATE: CA 709, TX 407, OH 364, NY 298, MA 280, MD 275, NC 270, FL 226, NJ 210, CT 148, GA 146, MN 144

## what

STATUS: OP 84%, RE 7%, L 2%, SB 2%, CN 1%, OS 1%, U 1%, P 1%, V 1%, OA 0%, IP 0%, TS 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 803 | 0 | 40577 285; 57280 211; 64778 147; 65076 116 |
| UTILITY_NAME | who | 828 | 0 | American Mun Power-Ohio,  285; Eagle Creek Renewable Ene 211; Strata Manager, LLC 147; HEN Infrastructure, L.L.C 116 |
| PLANT_CODE | other | 2.4K | 0 | 7440 63; 7791 61; 7777 61; 58542 51 |
| PLANT_NAME | who | 2.3K | 0 | VMEA 1 Credit Gen 63; Montpelier 61; Dover Peaking 61; Desert Sunlight 250, LLC 51 |
| STATE | state | 51 | 0 | CA 771; TX 485; OH 347; NY 330 |
| GENERATOR_ID | other | 1.9K | 1 | 1 671; 2 377; GEN1 226; 3 226 |
| STATUS | category | 13 | 0 | OP 4.6K; RE 395; L 107; SB 96 |
| OWNER_NAME | who | 1.9K | 0 | Cordelio BNC Holdings, LL 57; Nordic Solar, LLC 57; John Hancock Funding Comp 56; Manulife Infrastructure I 55 |
| OWNER_STREET_ADDRESS | who | 1.1K | 68 | 7315 Wisconsin Ave 156; 800 Taylor St, Suite 200 153; 14302 FNB Parkway 118; 560 Davis Street, Suite 2 97 |
| OWNER_CITY | who | 532 | 69 | San Francisco 238; Bethesda 230; Houston 198; New York 193 |
| OWNER_STATE | state | 54 | 103 | CA 709; TX 407; OH 364; NY 298 |
| OWNER_ZIP | who | 759 | 91 | 20814 231; 27701 158; 68154 122; 94111 115 |
| OWNERSHIP_ID | who | 1.9K | 0 | 66722 57; 61020 57; 65074 56; 65075 55 |
| PERCENT_OWNED | amount | 421 | 2 | 1 2.9K; 0.5 462; 0.25 77; 0.0522 56 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:23.11895 5.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 8622828c-6704-49e7-aaf5-3 5.5K |
| _SRC_FILE | who | 1 | 0 | 4___Owner_Y2024.xlsx 5.5K |
