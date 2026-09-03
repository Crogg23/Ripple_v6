# PORTAL_SOC_NEW_YORK_STATE_O_C08EFA40C8

rows 2.0K  columns 22  scan 5.0s

roles: amount 9, audit 2, category 1, date 1, other 5, who 5

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VOC | 2.0K | 0 | 4.87 | 128.24 | 314.47 | 32.4K |
| NOX | 2.0K | 0 | 13.56 | 1.1K | 4.5K | 178.8K |
| CO | 2.0K | 0 | 8.18 | 1.0K | 13.9K | 205.0K |
| CO2 | 2.0K | 0 | 12.9K | 2.17M | 4.51M | 236.71M |
| PARTICULATES | 2.0K | 0 | 1.61 | 278.19 | 5.8K | 38.9K |
| PM10 | 2.0K | 0 | 0.18 | 151.22 | 756.03 | 15.2K |

## who

FACILITY_NAME by rows
        14  FREEPORT POWER PLANT #1
        10  INDEPENDENCE STATION
        10  BALL METAL BEVERAGE CONTAINER CORP
         8  CALPINE JFK ENERGY CENTER
         8  AMERICAN PACKAGING CORP
         7  GLOBAL COMPANIES LLC - ALBANY TERMINAL
         7  BEECH HILL COMPRESSOR STATION
         7  GE GLOBAL RESEARCH CENTER
         7  INDECK-CORINTH ENERGY CENTER
         7  SOMERSET OPERATING COMPANY LLC
         7  FREEPORT POWER PLANT #2
         7  VULCRAFT OF NEW YORK INC
         7  BORGER STATION
         7  UNICELL BODY COMPANY INC
         7  NEW YORK PRESBYTERIAN HOSPITAL
         7  ARKEMA INC
         7  SELKIRK COGENERATION PROJECT
         7  NOVELIS CORPORATION
         7  PORT JEFFERSON POWER STATION
         7  NUCOR STEEL AUBURN INC

FACILITY_NAME by dollars
      958.82        4 rows  PACTIV LLC
      700.85        5 rows  3M TONAWANDA
      689.60       10 rows  BALL METAL BEVERAGE CONTAINER CORP
      624.77        5 rows  METAL CONTAINER CORP
      542.81        4 rows  E I DUPONT YERKES PLANT
      525.72        6 rows  ANHEUSER BUSCH BALDWINSVILLE BREWERY
      485.86        5 rows  GUNLOCKE CO
      467.24        7 rows  GLOBAL COMPANIES LLC - ALBANY TERMINAL
      461.54        6 rows  CON ED-EAST RIVER GENERATING STATION
      446.99        6 rows  PALL TRINITY MICRO
      442.99        8 rows  AMERICAN PACKAGING CORP
      439.76        6 rows  FINCH PAPER LLC
      414.52        6 rows  RAVENSWOOD GENERATING STATION
      412.14        4 rows  EASTMAN BUSINESS PARK
      397.08        5 rows  NORTHPORT POWER STATION
      384.17        5 rows  GLOBAL COMPANIES - CARGO TERMINAL
      382.79        5 rows  GLOBE METALLURGICAL INC
      339.94        7 rows  NOVELIS CORPORATION
      336.83        7 rows  ARKEMA INC
      336.52        5 rows  KINDER MORGAN LIQUIDS TERMINALS LLC

MUNICIPALITY by rows
        71  BROOKLYN
        47  BUFFALO
        46  NEW YORK
        36  NIAGARA FALLS
        36  HEMPSTEAD
        35  TONAWANDA
        34  ROCHESTER
        30  ALBANY
        27  BRONX
        27  BROOKHAVEN
        26  ISLIP
        26  RENSSELAER
        26  NEW WINDSOR
        22  BROOKLYN (6101)
        22  AUBURN
        20  OSWEGO
        19  QUEENS (6301)
        17  BRONX (6005)
        17  MANHATTAN (6204)
        17  BABYLON

MUNICIPALITY by dollars
        1.9K       35 rows  TONAWANDA
        1.3K       26 rows  NEW WINDSOR
        1.2K       34 rows  ROCHESTER
      960.19        8 rows  CANANDAIGUA
      868.38       47 rows  BUFFALO
      725.54        9 rows  SARATOGA SPRINGS
      702.10       30 rows  ALBANY
      497.17       36 rows  NIAGARA FALLS
      485.86        5 rows  WAYLAND
      471.28       12 rows  GLENS FALLS
      461.22        4 rows  TICONDEROGA
      438.49        5 rows  BALDWINSVILLE
      436.63       46 rows  NEW YORK
      433.88       36 rows  HEMPSTEAD
      420.28       71 rows  BROOKLYN
      398.73       26 rows  RENSSELAER
      394.12       16 rows  MIDDLETOWN
      382.40        5 rows  CORTLAND
      368.24       10 rows  HUNTINGTON
      365.76       19 rows  QUEENS (6301)

LOCATION by rows
       132  {"type": "Point", "coordinates": [-73.99036, 40.69245]}
        72  {"type": "Point", "coordinates": [-73.82999, 40.714]}
        70  {"type": "Point", "coordinates": [-73.92309, 40.826]}
        55  {"type": "Point", "coordinates": [-74.00602, 40.71451]}
        47  {"type": "Point", "coordinates": [-78.87846, 42.88545]}
        46  {"type": "Point", "coordinates": [-74.00712, 40.71453]}
        36  {"type": "Point", "coordinates": [-79.05551, 43.096]}
        36  {"type": "Point", "coordinates": [-73.62194, 40.7101]}
        35  {"type": "Point", "coordinates": [-78.88617, 43.01888]}
        34  {"type": "Point", "coordinates": [-77.61632, 43.1558]}
        30  {"type": "Point", "coordinates": [-73.75521, 42.65155]}
        27  {"type": "Point", "coordinates": [-72.91224, 40.7737]}
        26  {"type": "Point", "coordinates": [-73.74127, 42.64472]}
        26  {"type": "Point", "coordinates": [-74.02274, 41.47742]}
        26  {"type": "Point", "coordinates": [-73.218, 40.72817]}
        25  {"type": "Point", "coordinates": [-74.07527, 40.64242]}
        22  {"type": "Point", "coordinates": [-76.56591, 42.92936]}
        20  {"type": "Point", "coordinates": [-76.51119, 43.45646]}
        17  {"type": "Point", "coordinates": [-73.32601, 40.69573]}
        16  {"type": "Point", "coordinates": [-74.42261, 41.44584]}

LOCATION by dollars
        1.9K       35 rows  {"type": "Point", "coordinates": [-78.88617, 43.01888]}
        1.3K       26 rows  {"type": "Point", "coordinates": [-74.02274, 41.47742]}
        1.2K       34 rows  {"type": "Point", "coordinates": [-77.61632, 43.1558]}
        1.1K       72 rows  {"type": "Point", "coordinates": [-73.82999, 40.714]}
      975.03      132 rows  {"type": "Point", "coordinates": [-73.99036, 40.69245]}
      960.19        8 rows  {"type": "Point", "coordinates": [-77.28094, 42.88809]}
      868.38       47 rows  {"type": "Point", "coordinates": [-78.87846, 42.88545]}
      725.54        9 rows  {"type": "Point", "coordinates": [-73.78441, 43.08412]}
      702.10       30 rows  {"type": "Point", "coordinates": [-73.75521, 42.65155]}
      627.18       25 rows  {"type": "Point", "coordinates": [-74.07527, 40.64242]}
      497.17       36 rows  {"type": "Point", "coordinates": [-79.05551, 43.096]}
      485.86        5 rows  {"type": "Point", "coordinates": [-77.58991, 42.56779]}
      471.28       12 rows  {"type": "Point", "coordinates": [-73.64375, 43.31128]}
      461.22        4 rows  {"type": "Point", "coordinates": [-73.42423, 43.84879]}
      445.76       55 rows  {"type": "Point", "coordinates": [-74.00602, 40.71451]}
      438.49        5 rows  {"type": "Point", "coordinates": [-76.33276, 43.15867]}
      436.63       46 rows  {"type": "Point", "coordinates": [-74.00712, 40.71453]}
      433.88       36 rows  {"type": "Point", "coordinates": [-73.62194, 40.7101]}
      398.73       26 rows  {"type": "Point", "coordinates": [-73.74127, 42.64472]}
      394.12       16 rows  {"type": "Point", "coordinates": [-74.42261, 41.44584]}

COUNTY by rows
       186  SUFFOLK
       132  KINGS
       122  ERIE
       115  QUEENS
       102  NASSAU
       101  NEW YORK
        83  ALBANY
        82  NIAGARA
        72  BRONX
        70  ORANGE
        63  ONONDAGA
        59  MONROE
        46  WESTCHESTER
        43  OSWEGO
        40  ROCKLAND
        35  RENSSELAER
        34  JEFFERSON
        33  CHAUTAUQUA
        31  ONTARIO
        30  STEUBEN

COUNTY by dollars
        3.6K      122 rows  ERIE
        1.9K       83 rows  ALBANY
        1.9K       70 rows  ORANGE
        1.8K       59 rows  MONROE
        1.8K       31 rows  ONTARIO
        1.7K      186 rows  SUFFOLK
        1.4K      115 rows  QUEENS
        1.4K       63 rows  ONONDAGA
        1.2K      102 rows  NASSAU
        1.1K       27 rows  SARATOGA
      975.03      132 rows  KINGS
      882.39      101 rows  NEW YORK
      855.21       82 rows  NIAGARA
      764.37       30 rows  STEUBEN
      634.57       26 rows  RICHMOND
      628.09       27 rows  CHEMUNG
      559.34       20 rows  WAYNE
      515.48       35 rows  RENSSELAER
      487.17       11 rows  SENECA
      471.28       12 rows  WARREN

## who x when

FACILITY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = VOC
  3M TONAWANDA                              2026:700.85
  AMERICAN PACKAGING CORP                   2026:442.99
  ANHEUSER BUSCH BALDWINSVILLE BREWERY      2026:525.72
  ARKEMA INC                                2026:336.83
  BALL METAL BEVERAGE CONTAINER CORP        2026:689.60
  BEECH HILL COMPRESSOR STATION             2026:79.72
  BORGER STATION                            2026:5.84
  CALPINE JFK ENERGY CENTER                 2026:115.76
  CON ED-EAST RIVER GENERATING STATION      2026:461.54
  E I DUPONT YERKES PLANT                   2026:542.81
  FINCH PAPER LLC                           2026:439.76
  FREEPORT POWER PLANT #1                   2026:1.30
  FREEPORT POWER PLANT #2                   2026:19.42
  GE GLOBAL RESEARCH CENTER                 2026:37.52
  GLOBAL COMPANIES LLC - ALBANY TERMINAL    2026:467.24
  GUNLOCKE CO                               2026:485.86
  INDECK-CORINTH ENERGY CENTER              2026:91.34
  INDEPENDENCE STATION                      2026:312.89
  METAL CONTAINER CORP                      2026:624.77
  NEW YORK PRESBYTERIAN HOSPITAL            2026:24.31
  NOVELIS CORPORATION                       2026:339.94
  NUCOR STEEL AUBURN INC                    2026:28.64
  PACTIV LLC                                2026:958.82
  PALL TRINITY MICRO                        2026:446.99
  PORT JEFFERSON POWER STATION              2026:86.68
  RAVENSWOOD GENERATING STATION             2026:414.52
  SELKIRK COGENERATION PROJECT              2026:88.74
  SOMERSET OPERATING COMPANY LLC            2026:97.12
  UNICELL BODY COMPANY INC                  2026:61.36
  VULCRAFT OF NEW YORK INC                  2026:163.19

MUNICIPALITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = VOC
  ALBANY                                    2026:702.10
  AUBURN                                    2026:251.27
  BABYLON                                   2026:58.37
  BALDWINSVILLE                             2026:438.49
  BRONX                                     2026:62.45
  BRONX (6005)                              2026:26.89
  BROOKHAVEN                                2026:189.79
  BROOKLYN                                  2026:420.28
  BROOKLYN (6101)                           2026:325.87
  BUFFALO                                   2026:868.38
  CANANDAIGUA                               2026:960.19
  CORTLAND                                  2026:382.40
  GLENS FALLS                               2026:471.28
  HEMPSTEAD                                 2026:433.88
  HUNTINGTON                                2026:368.24
  ISLIP                                     2026:236.72
  MANHATTAN (6204)                          2026:98.73
  MIDDLETOWN                                2026:394.12
  NEW WINDSOR                               2026:1.3K
  NEW YORK                                  2026:436.63
  NIAGARA FALLS                             2026:497.17
  OSWEGO                                    2026:203.41
  QUEENS (6301)                             2026:365.76
  RENSSELAER                                2026:398.73
  ROCHESTER                                 2026:1.2K
  SARATOGA SPRINGS                          2026:725.54
  TICONDEROGA                               2026:461.22
  TONAWANDA                                 2026:1.9K
  WAYLAND                                   2026:485.86

## what

YEAR: 2015 9%, 2010 9%, 2014 9%, 2019 9%, 2011 9%, 2012 9%, 2016 8%, 2013 8%, 2020 8%, 2017 8%, 2018 8%, 2023 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 14 | 0 | 2015 164; 2010 162; 2014 157; 2019 155 |
| COUNTY | who | 60 | 0 | SUFFOLK 186; KINGS 132; ERIE 122; QUEENS 115 |
| MUNICIPALITY | who | 336 | 0 | BROOKLYN 71; BUFFALO 47; NEW YORK 46; HEMPSTEAD 36 |
| DEC_ID | other | 455 | 0 | 1282000357 14; 4102600037 12; 2600700726 11; 5154800008 11 |
| FACILITY_NAME | who | 555 | 0 | FREEPORT POWER PLANT #1 14; BALL METAL BEVERAGE CONTA 12; COMPRESSOR STATION 254 12; HARLEM RIVER YARDS PLANT 11 |
| SIC_CODE | other | 123 | 0 | 4911 463; 4953 180; 8062 102; 5171 100 |
| VOC | amount | 1.3K | 0 | 0 86; 0.01 24; 0.02 17; 0.09 15 |
| NOX | amount | 1.5K | 0 | 0 120; 0.01 22; 0.06 14; 0.33 11 |
| CO | amount | 1.4K | 0 | 0 138; 0.01 26; 0.03 16; 0.02 14 |
| CO2 | amount | 1.9K | 0 | 0 106; 3.53 10; 59326.47 10; 596725.26 10 |
| PARTICULATES | amount | 898 | 0 | 0 235; 0.01 53; 0.03 25; 0.04 15 |
| PM10 | amount | 611 | 0 | 0 623; 0.01 92; 0.03 35; 0.02 32 |
| PM2_5 | amount | 628 | 0 | 0 528; 0.01 69; 0.02 54; 0.03 41 |
| HAPS | amount | 401 | 0 | 0 1.2K; 0.01 40; 0.02 20; 0.04 13 |
| SO2 | amount | 766 | 0 | 0 298; 0.01 111; 0.03 59; 0.02 55 |
| LOCATION | who | 301 | 0 | {"type": "Point", "coordi 132; {"type": "Point", "coordi 72; {"type": "Point", "coordi 70; {"type": "Point", "coordi 55 |
| COMPUTED_REGION_YAMH_8V7K | other | 209 | 0 | 894 132; 196 110; 749 101; 62 73 |
| COMPUTED_REGION_WBG7_3WHC | other | 251 | 0 | 880 132; 723 101; 1162 72; 647 70 |
| COMPUTED_REGION_KJDX_G34T | other | 59 | 0 | 2179 182; 2090 132; 2041 122; 2137 110 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:44.38068 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | bfff8854-0a8a-4674-9300-f 2.0K |
| SRC_SHA256 | who | 1 | 0 | 9a68f4ff7d218679cef021c89 2.0K |
