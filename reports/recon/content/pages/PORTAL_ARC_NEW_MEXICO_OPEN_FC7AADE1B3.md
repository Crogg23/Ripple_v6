# PORTAL_ARC_NEW_MEXICO_OPEN_FC7AADE1B3

rows 2.0K  columns 29  scan 4.6s

roles: amount 10, audit 2, category 7, date 3, id 2, other 3, who 3

## when

EVENT_START_DATE
  2019      1.9K  ##############################
  2020       128  ##
  2022         1  

EVENT_END_DATE
  2019      1.8K  ##############################
  2020       143  ##
  2021         3  
  2022         1  
  2023        12  

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 2.0K | 31.80 | 32.61 | 35.89 | 36.80 | 65.1K |
| LONGITUDE | 2.0K | -108.61 | -103.81 | -103.15 | -103.13 | -207.5K |
| CO_EXCESS_EMISSIONS__LBS | 2.0K | 0 | 13.93 | 9.4K | 360.3K | 2.08M |
| NOX_EXCESS_EMISSIONS__LBS | 2.0K | 0 | 1.89 | 3.5K | 79.0K | 499.6K |
| PM_EXCESS_EMISSIONS__LBS | 2.0K | 0 | 0 | 38.92 | 6.4K | 12.1K |
| PM10_EXCESS_EMISSIONS__LBS | 2.0K | 0 | 0 | 0 | 525.80 | 586.40 |

## who

FACILITY_NAME by rows
       295  Jal No3 Gas Plant
       290  Zia II Gas Plant
       253  HF Sinclair Navajo Refining LLC (Artesia)
       102  Eunice Gas Plant
        99  South Hat Mesa Booster Station
        89  Turkey Track CTB and Gas Sales Compression
        66  Monument Gas Plant
        57  Indian Basin Gas Plant
        56  Lynch Booster Station
        51  Chevron - HY NM Section 10 CTB and Compressor Stations
        47  OXY - Corral CS 2S
        46  Fitz Compressor Station
        35  Eunice Gas Processing Plant
        33  Monument Booster Station
        27  West Turkey Track Booster
        26  Western Refining - Gallup Refinery
        26  Salado Draw 23 Compressor Station & Tank Battery
        24  Eunice North Compressor Station
        23  Penasco Compressor Station
        20  Maljamar Gas Plant

FACILITY_NAME by dollars
      360.3K        1 rows  Nandina CTB
      294.7K       14 rows  Red Hills Gas Processing Plant
      292.4K        2 rows  Red Bud CTB
      227.5K        3 rows  Azalea Battery
      206.7K      295 rows  Jal No3 Gas Plant
      197.7K        1 rows  Amen Corner CTB
       87.3K       66 rows  Monument Gas Plant
       71.0K      102 rows  Eunice Gas Plant
       48.4K        2 rows  Firethorn CTB
       40.5K       57 rows  Indian Basin Gas Plant
       35.4K       24 rows  Eunice North Compressor Station
       31.5K       17 rows  Dagger Draw Gas Plant
       31.5K      290 rows  Zia II Gas Plant
       29.7K      253 rows  HF Sinclair Navajo Refining LLC (Artesia)
       24.2K       89 rows  Turkey Track CTB and Gas Sales Compression
       15.8K       35 rows  Eunice Gas Processing Plant
        9.8K       51 rows  Chevron - HY NM Section 10 CTB and Compressor Stations
        9.7K       47 rows  OXY - Corral CS 2S
        8.6K       15 rows  Artesia Gas Plant
        4.9K       26 rows  Salado Draw 23 Compressor Station & Tank Battery

GEOMETRY by rows
       295  {"type": "Point", "coordinates": [-103.174167, 32.173611]}
       290  {"type": "Point", "coordinates": [-103.808867, 32.643022]}
       253  {"type": "Point", "coordinates": [-104.395167, 32.842611]}
       102  {"type": "Point", "coordinates": [-103.286101, 32.513937]}
        99  {"type": "Point", "coordinates": [-103.672169, 32.507253]}
        89  {"type": "Point", "coordinates": [-104.095775, 32.682039]}
        66  {"type": "Point", "coordinates": [-103.312139, 32.6105]}
        57  {"type": "Point", "coordinates": [-104.574117, 32.463897]}
        56  {"type": "Point", "coordinates": [-103.538908, 32.565758]}
        51  {"type": "Point", "coordinates": [-104.173333, 32.062222]}
        47  {"type": "Point", "coordinates": [-103.952222, 32.155833]}
        46  {"type": "Point", "coordinates": [-104.059167, 32.616944]}
        35  {"type": "Point", "coordinates": [-103.147222, 32.424444]}
        33  {"type": "Point", "coordinates": [-103.2558, 32.623]}
        27  {"type": "Point", "coordinates": [-104.019, 32.6854]}
        26  {"type": "Point", "coordinates": [-108.425, 35.490278]}
        26  {"type": "Point", "coordinates": [-103.645555, 32.036167]}
        24  {"type": "Point", "coordinates": [-103.163211, 32.450114]}
        23  {"type": "Point", "coordinates": [-104.447222, 32.712778]}
        20  {"type": "Point", "coordinates": [-103.771389, 32.814444]}

GEOMETRY by dollars
      360.3K        1 rows  {"type": "Point", "coordinates": [-103.3026, 32.0823]}
      294.7K       14 rows  {"type": "Point", "coordinates": [-103.523889, 32.210556]}
      292.4K        2 rows  {"type": "Point", "coordinates": [-103.286218, 32.077582]}
      227.5K        3 rows  {"type": "Point", "coordinates": [-103.276044, 32.020856]}
      206.7K      295 rows  {"type": "Point", "coordinates": [-103.174167, 32.173611]}
      197.7K        1 rows  {"type": "Point", "coordinates": [-103.257822, 32.023171]}
       87.3K       66 rows  {"type": "Point", "coordinates": [-103.312139, 32.6105]}
       71.0K      102 rows  {"type": "Point", "coordinates": [-103.286101, 32.513937]}
       48.4K        2 rows  {"type": "Point", "coordinates": [-103.273082, 32.077584]}
       40.5K       57 rows  {"type": "Point", "coordinates": [-104.574117, 32.463897]}
       35.4K       24 rows  {"type": "Point", "coordinates": [-103.163211, 32.450114]}
       31.5K       17 rows  {"type": "Point", "coordinates": [-104.445864, 32.714722]}
       31.5K      290 rows  {"type": "Point", "coordinates": [-103.808867, 32.643022]}
       29.7K      253 rows  {"type": "Point", "coordinates": [-104.395167, 32.842611]}
       24.2K       89 rows  {"type": "Point", "coordinates": [-104.095775, 32.682039]}
       15.8K       35 rows  {"type": "Point", "coordinates": [-103.147222, 32.424444]}
        9.8K       51 rows  {"type": "Point", "coordinates": [-104.173333, 32.062222]}
        9.7K       47 rows  {"type": "Point", "coordinates": [-103.952222, 32.155833]}
        8.6K       15 rows  {"type": "Point", "coordinates": [-104.210028, 32.754972]}
        4.9K       26 rows  {"type": "Point", "coordinates": [-103.645555, 32.036167]}

SRC_SHA256 by rows
      2.0K  35593e907d8e02172d7a2b9b293fcc80c4ebb9d02288f3cc5cbe15098e60a4df

SRC_SHA256 by dollars
       2.08M     2.0K rows  35593e907d8e02172d7a2b9b293fcc80c4ebb9d02288f3cc5cbe15098e60

## who x when

FACILITY_NAME by EVENT_END_DATE, dollars = CO_EXCESS_EMISSIONS__LBS
  Amen Corner CTB                           2020:197.7K
  Artesia Gas Plant                         2019:8.6K
  Azalea Battery                            2019:114.3K 2020:113.2K
  Chevron - HY NM Section 10 CTB and Compr  2019:9.8K
  Dagger Draw Gas Plant                     2019:17.0K 2020:14.5K
  Eunice Gas Plant                          2019:71.0K
  Eunice Gas Processing Plant               2019:15.8K
  Eunice North Compressor Station           2019:35.4K
  Firethorn CTB                             2019:48.4K
  Fitz Compressor Station                   2019:0
  HF Sinclair Navajo Refining LLC (Artesia  2019:7.3K 2020:22.3K 2021:0
  Indian Basin Gas Plant                    2019:30.8K 2020:9.7K
  Jal No3 Gas Plant                         2019:206.7K
  Lynch Booster Station                     2019:550.47
  Maljamar Gas Plant                        2019:4.7K
  Monument Booster Station                  2019:2.6K
  Monument Gas Plant                        2019:87.3K
  Nandina CTB                               2020:360.3K
  OXY - Corral CS 2S                        2019:9.7K
  Penasco Compressor Station                2019:2.2K
  Red Bud CTB                               2019:207.7K 2020:84.7K
  Red Hills Gas Processing Plant            2019:294.7K
  Salado Draw 23 Compressor Station & Tank  2019:4.9K
  South Hat Mesa Booster Station            2019:0
  Turkey Track CTB and Gas Sales Compressi  2019:24.2K
  West Turkey Track Booster                 2019:3.5K
  Western Refining - Gallup Refinery        2019:0 2020:0
  Zia II Gas Plant                          2019:31.5K

GEOMETRY by EVENT_END_DATE, dollars = CO_EXCESS_EMISSIONS__LBS
  {"type": "Point", "coordinates": [-103.1  2019:15.8K
  {"type": "Point", "coordinates": [-103.1  2019:35.4K
  {"type": "Point", "coordinates": [-103.1  2019:206.7K
  {"type": "Point", "coordinates": [-103.2  2019:2.6K
  {"type": "Point", "coordinates": [-103.2  2020:197.7K
  {"type": "Point", "coordinates": [-103.2  2019:48.4K
  {"type": "Point", "coordinates": [-103.2  2019:114.3K 2020:113.2K
  {"type": "Point", "coordinates": [-103.2  2019:71.0K
  {"type": "Point", "coordinates": [-103.2  2019:207.7K 2020:84.7K
  {"type": "Point", "coordinates": [-103.3  2020:360.3K
  {"type": "Point", "coordinates": [-103.3  2019:87.3K
  {"type": "Point", "coordinates": [-103.5  2019:294.7K
  {"type": "Point", "coordinates": [-103.5  2019:550.47
  {"type": "Point", "coordinates": [-103.6  2019:4.9K
  {"type": "Point", "coordinates": [-103.6  2019:0
  {"type": "Point", "coordinates": [-103.7  2019:4.7K
  {"type": "Point", "coordinates": [-103.8  2019:31.5K
  {"type": "Point", "coordinates": [-103.9  2019:9.7K
  {"type": "Point", "coordinates": [-104.0  2019:3.5K
  {"type": "Point", "coordinates": [-104.0  2019:0
  {"type": "Point", "coordinates": [-104.0  2019:24.2K
  {"type": "Point", "coordinates": [-104.1  2019:9.8K
  {"type": "Point", "coordinates": [-104.2  2019:8.6K
  {"type": "Point", "coordinates": [-104.3  2019:7.3K 2020:22.3K 2021:0
  {"type": "Point", "coordinates": [-104.4  2019:17.0K 2020:14.5K
  {"type": "Point", "coordinates": [-104.4  2019:2.2K
  {"type": "Point", "coordinates": [-104.5  2019:30.8K 2020:9.7K
  {"type": "Point", "coordinates": [-108.4  2019:0 2020:0

## what

SOURCE_CLASSIFICATION: Major-Title V  61%, Synthetic Minor 16%, Synthetic Minor - >80% 14%, Minor 6%, Major-Title V - >80% 1%, Notice of Intent - >80% 1%, Minor - >80% 1%, Multiple 0%, Notice of Intent 0%

COMPANY: DCP Operating Company LP 38%, ET Gathering & Processing LLC 16%, HF Sinclair Navajo Refining LL 14%, OXY USA WTP Limited Partnershi 8%, Versado Gas Processors, LLC 7%, Chevron USA Inc - Midland 5%, OXY USA Inc  5%, Frontier Field Services LLC  3%, Western Refining Southwest LLC 1%, XTO Energy Inc 1%, nan 1%, Targa Northern Delaware LLC 1%

COUNTY_NAME: Lea 58%, Eddy 38%, McKinley 1%, San Juan 1%, Dona Ana 1%, Valencia 0%, Chaves 0%, Rio Arriba 0%, Hidalgo 0%

TITLE_5_PERMIT_NUMBER: nan 36%, TV P090R3M1 16%, P270-R1 15%, TV P051R3M2 13%, 0044M10R7 5%, P110R3M1 3%, P103R4 3%, P123R4 2%, P109R3M1 2%, P059R1 2%, P021R4 1%, P095R4 1%

NAICS_DESCRIPTION: Natural Gas Extraction 50%, Pipeline Transportation of Nat 18%, Crude Petroleum Extraction 15%, Petroleum Refineries 13%, Other Nonhazardous Waste Treat 1%, Fossil Fuel Electric Power Gen 1%, National Security 0%, Support Activities for Oil and 0%

EVENT_TYPE_DESCRIPTION_CLEANED: Malfunction 85%, Emergency 7%, Other 4%, Shutdown 2%, Startup 1%, Scheduled Maintenance 0%

FACILITY_WITH_EXCESS_EMISSIONS_OVER_MULTIPLE_YEARS: True 96%, False 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACTIVITY_NUMBER | id | 2.0K | 0 | 032800-11052019-01 10; 032800-11042019-05 10; 032800-11042019-04 10; 032800-11042019-03 10 |
| FACILITY_NAME | who | 104 | 0 | Jal No3 Gas Plant 295; Zia II Gas Plant 290; HF Sinclair Navajo Refini 253; Eunice Gas Plant 102 |
| SOURCE_CLASSIFICATION | category | 9 | 0 | Major-Title V  1.2K; Synthetic Minor 318; Synthetic Minor - >80% 285; Minor 114 |
| COMPANY | category | 33 | 0 | DCP Operating Company LP 729; ET Gathering & Processing 297; HF Sinclair Navajo Refini 262; OXY USA WTP Limited Partn 146 |
| COUNTY_NAME | category | 9 | 0 | Lea 1.2K; Eddy 765; McKinley 26; San Juan 19 |
| TITLE_5_PERMIT_NUMBER | category | 33 | 0 | nan 693; TV P090R3M1 295; P270-R1 290; TV P051R3M2 253 |
| NEW_SOURCE_REVIEW_PERMIT_NUMBER | other | 102 | 0 | 1092M11 295; PSD5217-M2 290; PSD0195M43R2 253; 44M7R9 102 |
| LATITUDE | amount | 104 | 0 | 32.173611 295; 32.643022 290; 32.842611 253; 32.513937 102 |
| LONGITUDE | amount | 104 | 0 | -103.174167 295; -103.808867 290; -104.395167 253; -103.286101 102 |
| EVENT_START_DATE | date | 465 | 0 | 2019-02-07 21; 2019-10-31 17; 2019-12-12 15; 2019-10-11 14 |
| EVENT_END_DATE | date | 472 | 0 | 2019-10-31 23; 2023-08-24 20; 2019-04-11 15; 2019-12-12 14 |
| NAICS_DESCRIPTION | category | 8 | 0 | Natural Gas Extraction 1.0K; Pipeline Transportation o 369; Crude Petroleum Extractio 306; Petroleum Refineries 262 |
| CO_EXCESS_EMISSIONS__LBS | amount | 1.2K | 0 | 0.0 703; 9.6 8; 1.0 8; 40.89 8 |
| NOX_EXCESS_EMISSIONS__LBS | amount | 1.0K | 0 | 0.0 814; 1.0 9; 4.7 7; 10.68 7 |
| PM_EXCESS_EMISSIONS__LBS | amount | 100 | 0 | 0.0 1.9K; 13.11 2; 2.538 1; 1.462 1 |
| PM10_EXCESS_EMISSIONS__LBS | amount | 13 | 0 | 0.0 2.0K; 55.41 1; 0.671 1; 0.124 1 |
| PM2_5_EXCESS_EMISSIONS__LBS | amount | 9 | 0 | 0.0 2.0K; 0.671 1; 0.124 1; 0.076 1 |
| SO2_EXCESS_EMISSIONS__LBS | amount | 1.1K | 0 | 0.0 821; 0.17 11; 0.02 10; 0.3 9 |
| VOC_EXCESS_EMISSIONS__LBS | amount | 1.1K | 0 | 0.0 594; 0.01 51; 0.02 25; 0.03 20 |
| OPAQUE_EXCESS_EMISSIONS__LBS | other | 1 | 0 | 0 2.0K |
| EXCESS_VISIBLE_EMISSIONS__LBS | other | 1 | 0 | 0 2.0K |
| H2S_EXCESS_EMISSIONS__LBS | amount | 388 | 0 | 0.0 1.3K; 0.01 51; 0.02 29; 0.03 20 |
| EVENT_TYPE_DESCRIPTION_CLEANED | category | 6 | 0 | Malfunction 1.7K; Emergency 145; Other 85; Shutdown 33 |
| FACILITY_WITH_EXCESS_EMISSIONS_OVER_MULTIPLE_YEARS | category | 2 | 0 | True 1.9K; False 82 |
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| GEOMETRY | who | 106 | 0 | {"type": "Point", "coordi 295; {"type": "Point", "coordi 290; {"type": "Point", "coordi 253; {"type": "Point", "coordi 102 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:34:50.06668 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | fc8642c5-7bef-4b55-85a0-0 2.0K |
| SRC_SHA256 | who | 1 | 0 | 35593e907d8e02172d7a2b9b2 2.0K |
