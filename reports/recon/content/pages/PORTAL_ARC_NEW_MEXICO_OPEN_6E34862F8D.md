# PORTAL_ARC_NEW_MEXICO_OPEN_6E34862F8D

rows 2.0K  columns 174  scan 6.8s

roles: amount 29, audit 2, category 77, date 8, empty 12, id 2, other 36, who 9

## when

DISCOVERY_DATE
  2019      1.8K  ##############################
  2020       161  ###
  2021         5  
  2022         1  
  2023        12  

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

FINAL_EER_DUE_DATE
  2020         5  ##############################

FINAL_EER_ACTUAL_DATE
  2019      1.7K  ##############################
  2020       219  ####
  2021        34  #
  2022         1  
  2023        12  
  2025         1  

EVENT_START_DATETIME
  2019      1.9K  ##############################
  2020       128  ##
  2022         1  

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 2.0K | 31.80 | 32.61 | 35.89 | 36.80 | 65.1K |
| LONGITUDE | 2.0K | -108.61 | -103.81 | -103.15 | -103.13 | -207.5K |
| CO_EMISSION_LIMIT | 2.0K | 0 | 0 | 454.70 | 1.1K | 17.5K |
| CO_EXCESS_EMISSIONS_OF_EVENT | 2.0K | 0 | 13.93 | 9.4K | 360.3K | 2.08M |
| CO_AVERAGE_EMISSION_RATE | 2.0K | 0 | 0.33 | 527.02 | 2.3K | 84.7K |
| NOX_EMISSION_LIMIT | 2.0K | 0 | 0 | 42.10 | 460.50 | 5.7K |

## who

AGENCY_INTEREST_NAME by rows
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
        20  Sand Dunes Booster Station

AGENCY_INTEREST_NAME by dollars
        5.2K      253 rows  HF Sinclair Navajo Refining LLC (Artesia)
        2.6K       20 rows  Maljamar Gas Plant
        2.1K        7 rows  Rio Grande Generating Station
        1.4K        5 rows  Empire Abo CS
         997       14 rows  BKU Compressor Station
         969        2 rows  Lobo Compressor Station
      642.60       66 rows  Monument Gas Plant
      613.20       12 rows  Lovington Booster Station
      607.40        4 rows  Occidental - North Hobbs Unit RCF and WIB
      522.90       24 rows  Eunice North Compressor Station
      416.44        3 rows  Loco Hills CS
      204.20       35 rows  Eunice Gas Processing Plant
      178.40        8 rows  Animas Power Plant
      132.60        4 rows  San Juan River Gas Plant
       94.10        1 rows  Fiddle Fee 24-28-23 7H-8H-3H-4H
       80.45      102 rows  Eunice Gas Plant
       72.32      295 rows  Jal No3 Gas Plant
       67.20       14 rows  Red Hills Gas Processing Plant
       65.40        9 rows  HF Sinclair Navajo Refining LLC (Lovington)
       54.34        8 rows  White Sands Missile Range

EVENT_END_TIME by rows
        81  23:59:00
        69  09:00:00
        60  17:00:00
        57  00:00:00
        56  14:00:00
        50  21:00:00
        47  04:00:00
        45  16:00:00
        43  18:00:00
        43  13:00:00
        42  10:00:00
        42  12:00:00
        41  11:00:00
        41  01:00:00
        40  22:00:00
        39  07:00:00
        39  20:00:00
        39  19:00:00
        38  08:00:00
        37  15:00:00

EVENT_END_TIME by dollars
        3.2K       39 rows  07:00:00
        1.8K       24 rows  02:00:00
        1.0K       29 rows  05:00:00
        1.0K       39 rows  19:00:00
        1.0K        2 rows  19:59:00
        1.0K        2 rows  10:59:00
      704.79       45 rows  16:00:00
      687.33       35 rows  23:00:00
      541.84       42 rows  12:00:00
      536.92       43 rows  18:00:00
      529.69       47 rows  04:00:00
      523.51       40 rows  22:00:00
      517.09       39 rows  20:00:00
      505.54       29 rows  06:00:00
      498.50        1 rows  01:11:00
      232.68       50 rows  21:00:00
      211.92       57 rows  00:00:00
      163.20        3 rows  14:10:00
      162.14        3 rows  14:06:00
      161.10        2 rows  15:09:00

EVENT_START_TIME by rows
       119  00:00:00
        89  09:00:00
        74  12:00:00
        73  10:00:00
        55  14:00:00
        54  11:00:00
        53  13:00:00
        52  15:00:00
        51  07:00:00
        51  16:00:00
        48  08:00:00
        47  17:00:00
        39  03:00:00
        39  18:00:00
        38  06:00:00
        37  01:00:00
        34  20:00:00
        33  04:00:00
        31  19:00:00
        30  05:00:00

EVENT_START_TIME by dollars
        4.8K       73 rows  10:00:00
        2.1K       29 rows  22:00:00
        1.5K       31 rows  19:00:00
        1.4K      119 rows  00:00:00
        1.1K       89 rows  09:00:00
      772.12       47 rows  17:00:00
      608.05       55 rows  14:00:00
      582.08       33 rows  04:00:00
      568.50       27 rows  21:00:00
      536.45       39 rows  18:00:00
      513.29       39 rows  03:00:00
      300.89       48 rows  08:00:00
      262.52       29 rows  23:00:00
      152.14        2 rows  11:58:00
      152.10        2 rows  17:45:00
      152.10        1 rows  13:44:00
      151.10        1 rows  14:08:00
      138.16       54 rows  11:00:00
      108.85       51 rows  07:00:00
       79.09       74 rows  12:00:00

DISCOVERY_TIME by rows
       230  11:00:00
        90  09:00:00
        79  08:00:00
        79  10:00:00
        77  12:00:00
        60  14:00:00
        55  00:00:00
        52  07:00:00
        51  15:00:00
        49  13:00:00
        46  18:00:00
        45  16:00:00
        43  17:00:00
        38  03:00:00
        37  06:00:00
        33  01:00:00
        32  04:00:00
        29  05:00:00
        29  19:00:00
        28  02:00:00

DISCOVERY_TIME by dollars
        4.4K       79 rows  10:00:00
        2.1K       27 rows  22:00:00
        2.1K       90 rows  09:00:00
        1.5K       60 rows  14:00:00
        1.3K       55 rows  00:00:00
      772.08       43 rows  17:00:00
      558.75       46 rows  18:00:00
      551.78       32 rows  04:00:00
      513.08       38 rows  03:00:00
      506.48       23 rows  21:00:00
      308.80       79 rows  08:00:00
      262.48       27 rows  23:00:00
      155.14      230 rows  11:00:00
      152.10        1 rows  13:44:00
      152.10        1 rows  11:58:00
      152.10        2 rows  17:45:00
      151.10        1 rows  14:08:00
      142.40       77 rows  12:00:00
      131.11       52 rows  07:00:00
      128.46       51 rows  15:00:00

## who x when

AGENCY_INTEREST_NAME by EVENT_END_DATE, dollars = CO_EMISSION_LIMIT
  Animas Power Plant                        2019:178.40
  BKU Compressor Station                    2019:997
  Chevron - HY NM Section 10 CTB and Compr  2019:0
  Empire Abo CS                             2019:1.4K 2020:0
  Eunice Gas Plant                          2019:80.45
  Eunice Gas Processing Plant               2019:204.20
  Eunice North Compressor Station           2019:522.90
  Fitz Compressor Station                   2019:0
  HF Sinclair Navajo Refining LLC (Artesia  2019:2.5K 2020:2.7K 2021:0
  Indian Basin Gas Plant                    2019:33.10 2020:14.08
  Jal No3 Gas Plant                         2019:72.32
  Lobo Compressor Station                   2019:969
  Loco Hills CS                             2019:416.44
  Lovington Booster Station                 2019:613.20
  Lynch Booster Station                     2019:0
  Maljamar Gas Plant                        2019:2.6K
  Monument Booster Station                  2019:23.05
  Monument Gas Plant                        2019:642.60
  OXY - Corral CS 2S                        2019:9.66
  Occidental - North Hobbs Unit RCF and WI  2019:607.40
  Penasco Compressor Station                2019:25.30
  Rio Grande Generating Station             2019:1.0K 2020:1.1K
  Salado Draw 23 Compressor Station & Tank  2019:0
  San Juan River Gas Plant                  2019:132.60
  Sand Dunes Booster Station                2019:0
  South Hat Mesa Booster Station            2019:0
  Turkey Track CTB and Gas Sales Compressi  2019:3.52
  West Turkey Track Booster                 2019:0
  Western Refining - Gallup Refinery        2019:0 2020:0
  Zia II Gas Plant                          2019:14.10

EVENT_END_TIME by EVENT_END_DATE, dollars = CO_EMISSION_LIMIT
  00:00:00                                  2019:151.18 2020:60.74
  01:00:00                                  2019:3.95 2020:0
  01:11:00                                  2019:498.50
  02:00:00                                  2019:1.8K 2020:0
  04:00:00                                  2019:522.20 2020:0 2022:7.49
  05:00:00                                  2019:545.72 2020:502.20
  06:00:00                                  2019:500.43 2020:5.11
  07:00:00                                  2019:3.1K 2020:68.25
  08:00:00                                  2019:27.33 2020:0
  09:00:00                                  2019:2.61 2020:0.90
  10:00:00                                  2019:52.02 2020:0
  10:59:00                                  2019:1.0K
  11:00:00                                  2019:7.89 2020:8
  12:00:00                                  2019:1.08 2020:540.76
  13:00:00                                  2019:16.09 2020:5.17
  14:00:00                                  2019:66.89 2020:27.71
  14:06:00                                  2019:162.14
  14:10:00                                  2019:163.20
  15:00:00                                  2019:0.26 2020:14.16
  15:09:00                                  2019:161.10
  16:00:00                                  2019:704.63 2020:0.16
  17:00:00                                  2019:88.83 2020:5.11 2021:0
  18:00:00                                  2019:36.82 2020:500.10
  19:00:00                                  2019:519.99 2020:510
  19:59:00                                  2019:5.50 2020:1.0K
  20:00:00                                  2019:517.09 2020:0
  21:00:00                                  2019:229.18 2020:3.50
  22:00:00                                  2019:23.51 2020:500
  23:00:00                                  2019:680.54 2020:0 2021:6.79
  23:59:00                                  2019:101.17 2020:0 2021:6.79

## what

SOURCE_CLASSIFICATION_DESC: Major-Title V  61%, Synthetic Minor 16%, Synthetic Minor - >80% 14%, Minor 6%, Major-Title V - >80% 1%, Notice of Intent - >80% 1%, Minor - >80% 1%, Multiple 0%, Notice of Intent 0%

TEMPO_OWNER: DCP Operating Company LP 38%, ET Gathering & Processing LLC 16%, HF Sinclair Navajo Refining LL 14%, OXY USA WTP Limited Partnershi 8%, Versado Gas Processors, LLC 7%, Chevron USA Inc - Midland 5%, OXY USA Inc  5%, Frontier Field Services LLC  3%, Western Refining Southwest LLC 1%, XTO Energy Inc 1%, nan 1%, Targa Northern Delaware LLC 1%

TEMPO_COUNTY_NAME: Lea 58%, Eddy 38%, McKinley 1%, San Juan 1%, Dona Ana 1%, Valencia 0%, Chaves 0%, Rio Arriba 0%, Hidalgo 0%

TV_PERMIT_NO: nan 36%, TV P090R3M1 16%, P270-R1 15%, TV P051R3M2 13%, 0044M10R7 5%, P110R3M1 3%, P103R4 3%, P123R4 2%, P109R3M1 2%, P059R1 2%, P021R4 1%, P095R4 1%

IS_ACTIVE: Yes 93%, No 7%

IS_PORTABLE_SOURCE: No 100%, Yes 0%

EE_EVENT_TYPE_DESC: Malfunction, Title V Deviation 51%, Malfunction 31%, Emergency 5%, Title V Deviation, Malfunction 4%, Emergency, Title V Deviation 2%, Other, Title V Deviation 2%, Other 2%, Shutdown, Title V Deviation 1%, Startup 1%, Title V Deviation, Other 0%, Title V Deviation, Startup 0%, Startup, Title V Deviation 0%

AI_NAICS_CODE: 21113 50%, 48621 18%, 21112 15%, 32411 13%, 562219 1%, 221112 1%, 92811 0%, 213112 0%

AI_NAICS_DESCRIPTION: Natural Gas Extraction 50%, Pipeline Transportation of Nat 18%, Crude Petroleum Extraction 15%, Petroleum Refineries 13%, Other Nonhazardous Waste Treat 1%, Fossil Fuel Electric Power Gen 1%, National Security 0%, Support Activities for Oil and 0%

CO_CHEMICAL_CODE: CO 65%, nan 35%

CO_CHEMICAL_NAME: Carbon Monoxide 65%, nan 35%

CO_UOM: lbs. 65%, nan 35%

CO_EMISSION_LIMIT_UOM: lbs./hour 54%, nan 36%, tons/year 9%, PPM 0%, lbs./MMbtu 0%, minutes 0%, ppmv 0%

CO_AVERAGING_PERIOD_UOM: hour 47%, nan 38%, annual, monthly rolling 6%, minutes 4%, hour, hourly rolling 2%, hour block 1%, daily, daily rolling 1%, annual 1%, monthly 0%, hours and minutes 0%

CO_AVERAGE_EMISSION_RATE_UOM: nan 47%, lbs./hour 47%, minutes 3%, tons/year 2%, other 0%, lbs./MMbtu 0%

NOX_CHEMICAL_CODE: Nox 59%, nan 41%

NOX_CHEMICAL_NAME: Nitrogen Dioxide 59%, nan 41%

NOX_UOM: lbs. 59%, nan 41%

NOX_EMISSION_LIMIT_UOM: lbs./hour 48%, nan 42%, tons/year 8%, lbs./MMbtu 1%, PPM 0%, minutes 0%, ppmv 0%

NOX_AVERAGING_PERIOD_UOM: nan 44%, hour 42%, annual, monthly rolling 6%, minutes 4%, hour, hourly rolling 2%, hour block 1%, annual 1%, daily, daily rolling 0%, hours and minutes 0%, monthly 0%

NOX_AVERAGE_EMISSION_RATE_UOM: nan 53%, lbs./hour 41%, minutes 3%, tons/year 2%, other 0%, lbs./MMbtu 0%, PPM 0%

PM_CHEMICAL_CODE: nan 95%, PM 5%

PM_CHEMICAL_NAME: nan 95%, Particulate Matter (total susp 5%

PM_UOM: nan 95%, lbs. 5%

PM_EMISSION_LIMIT_UOM: nan 95%, lbs./hour 4%, tons/year 0%

PM_AVERAGING_PERIOD: 0 95%, 1 4%, 3 1%

PM_AVERAGING_PERIOD_UOM: nan 95%, hour 3%, hour, hourly rolling 1%, annual 0%, daily, daily rolling 0%, hour block 0%

PM_NUMBER_OF_EXCEEDENCES: 0 96%, 1 4%, 71 0%, 34 0%, 236 0%, 98 0%, 166 0%, 72 0%, 408 0%, 35 0%, 221 0%, 19 0%

PM_AVERAGE_EMISSION_RATE_UOM: nan 99%, lbs./hour 1%, tons/year 0%

PM10_CHEMICAL_CODE: nan 99%, PM10 1%

PM10_CHEMICAL_NAME: nan 99%, Particulate Matter (10 microns 1%

PM10_UOM: nan 99%, lbs. 1%

PM10_DURATION: 0 99%, 60 0%, 720 0%, 240 0%, 726 0%, 38880 0%, 4860 0%

PM10_EMISSION_LIMIT_UOM: nan 99%, tons/year 0%, lbs./hour 0%

PM10_AVERAGING_PERIOD: 0 99%, 1 1%

PM10_AVERAGING_PERIOD_UOM: nan 99%, annual 0%, hour 0%, hour block 0%

PM10_NUMBER_OF_EXCEEDENCES: 0 99%, 1 0%, 4 0%, 12 0%

PM10_AVERAGE_EMISSION_RATE_UOM: nan 99%, tons/year 0%, lbs./hour 0%

PM25_CHEMICAL_CODE: nan 100%, 1770318000000.0 0%

PM25_CHEMICAL_NAME: nan 100%, Particulate Matter (2.5 micron 0%

PM25_UOM: nan 100%, lbs. 0%

PM25_DURATION: 0 100%, 60 0%, 720 0%, 4860 0%

PM25_EMISSION_LIMIT_UOM: nan 100%, tons/year 0%

PM25_AVERAGING_PERIOD: 0 100%, 1 0%

PM25_AVERAGING_PERIOD_UOM: nan 100%, annual 0%

PM25_NUMBER_OF_EXCEEDENCES: 0 100%, 1 0%

PM25_AVERAGE_EMISSION_RATE_UOM: nan 100%, tons/year 0%

SO2_CHEMICAL_CODE: SO2 59%, nan 41%

SO2_CHEMICAL_NAME: Sulfur Dioxide 59%, nan 41%

SO2_UOM: lbs 59%, nan 41%

SO2_EMISSION_LIMIT_UOM: lbs./hour 46%, nan 42%, PPM 7%, tons/year 5%, minutes 0%

SO2_AVERAGING_PERIOD_UOM: nan 43%, hour 38%, hour, hourly rolling 10%, minutes 4%, annual, monthly rolling 3%, hour block 2%, annual 0%, hours and minutes 0%, daily, daily rolling 0%, monthly 0%

SO2_AVERAGE_EMISSION_RATE_UOM: nan 52%, lbs./hour 43%, minutes 3%, tons/year 0%, other 0%, PPM 0%, lbs./MMbtu 0%

VOC_CHEMICAL_CODE: VOC 70%, nan 30%

VOC_CHEMICAL_NAME: Volatile Organic Compounds (VO 70%, nan 30%

VOC_UOM: lbs. 70%, nan 30%

VOC_EMISSION_LIMIT_UOM: lbs./hour 52%, nan 33%, tons/year 15%, minutes 0%, other 0%, lbs./MMbtu 0%

VOC_AVERAGING_PERIOD_UOM: hour 47%, nan 34%, annual, monthly rolling 11%, minutes 3%, annual 3%, hour, hourly rolling 1%, hour block 1%, hours and minutes 0%, monthly 0%, daily, daily rolling 0%

VOC_AVERAGE_EMISSION_RATE_UOM: lbs./hour 44%, nan 43%, tons/year 9%, minutes 3%, other 0%, lbs./MMbtu 0%, ppmv 0%

H2S_CHEMICAL_CODE: nan 66%, H2S 34%

H2S_CHEMICAL_NAME: nan 66%, Hydrogen Sulfide 34%

H2S_UOM: nan 66%, lbs. 34%

H2S_EMISSION_LIMIT_UOM: nan 67%, lbs./hour 29%, tons/year 4%, minutes 0%, PPM 0%, lbs./MMbtu 0%

H2S_AVERAGING_PERIOD_UOM: nan 68%, hour 25%, annual, monthly rolling 3%, minutes 3%, hour block 1%, daily, daily rolling 0%, monthly 0%, hours and minutes 0%, hour, hourly rolling 0%, annual 0%

H2S_NUMBER_OF_EXCEEDENCES: 0 71%, 1 24%, 2 2%, 3 1%, 4 1%, 5 0%, 7 0%, 11 0%, 17 0%, 10 0%, 9 0%, 12 0%

H2S_AVERAGE_EMISSION_RATE_UOM: nan 75%, lbs./hour 21%, minutes 3%, lbs./MMbtu 0%, other 0%, tons/year 0%

DUPLICATE: Unlikely 96%, Somewhat Likely 3%, Likely 0%

EVENT_START_MONTH: 12 11%, 10 10%, 4 10%, 1 9%, 3 9%, 11 8%, 8 8%, 6 8%, 2 7%, 7 7%, 9 7%, 5 6%

EVENT_START_YEAR: 2019 94%, 2020 6%, 2022 0%

EVENT_START_QUARTER: 4 29%, 1 25%, 2 24%, 3 22%

EE_EVENT_TYPE_DESC_CLEAN: Malfunction 85%, Emergency 7%, Other 4%, Shutdown 2%, Startup 1%, Scheduled Maintenance 0%

MULTI_DAY_EVENT: FALSE 86%, TRUE 14%

FACILITY_NO_EVENTS_IN_12_MO: TRUE 54%, FALSE 46%

FACILITY_EVENTS_12_MO_AND_BEFORE: FALSE 54%, TRUE 46%

FACILITY_EVENTS_SINGLE_YEAR: FALSE 96%, TRUE 4%

FACILITY_NO_EVENTS_IN_24_MO: FALSE 50%, TRUE 50%

FACILITY_EVENTS_MULTIPLE_YEARS: TRUE 96%, FALSE 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TEMPO_ACTIVITY_NO | id | 2.0K | 0 | 032800-11052019-01 10; 032800-11042019-05 10; 032800-11042019-04 10; 032800-11042019-03 10 |
| TEMPO_AI_ID | other | 105 | 0 | 569 295; 32800 290; 198 253; 595 102 |
| AGENCY_INTEREST_NAME | who | 104 | 0 | Jal No3 Gas Plant 295; Zia II Gas Plant 290; HF Sinclair Navajo Refini 253; Eunice Gas Plant 102 |
| SOURCE_CLASSIFICATION_DESC | category | 9 | 0 | Major-Title V  1.2K; Synthetic Minor 318; Synthetic Minor - >80% 285; Minor 114 |
| TEMPO_OWNER | category | 33 | 0 | DCP Operating Company LP 729; ET Gathering & Processing 297; HF Sinclair Navajo Refini 262; OXY USA WTP Limited Partn 146 |
| TEMPO_COUNTY_NAME | category | 9 | 0 | Lea 1.2K; Eddy 765; McKinley 26; San Juan 19 |
| TV_PERMIT_NO | category | 33 | 0 | nan 693; TV P090R3M1 295; P270-R1 290; TV P051R3M2 253 |
| NSR_PERMIT_NO | other | 102 | 0 | 1092M11 295; PSD5217-M2 290; PSD0195M43R2 253; 44M7R9 102 |
| LATITUDE | amount | 104 | 0 | 32.173611 295; 32.643022 290; 32.842611 253; 32.513937 102 |
| LONGITUDE | amount | 104 | 0 | -103.174167 295; -103.808867 290; -104.395167 253; -103.286101 102 |
| IS_ACTIVE | category | 2 | 0 | Yes 1.9K; No 145 |
| IS_PORTABLE_SOURCE | category | 2 | 0 | No 2.0K; Yes 2 |
| TEMPO_FAILURE_PT_NO | other | 232 | 0 | Unit 55 151; Fl-1 144; FL2 (SSM + pilot) 134; Pipeline C-23-10-1-10-3 100 |
| TEMPO_FAILURE_PT_DESC | who | 230 | 0 | Flare 185; Acid Gas Flare 145; General Plant, Racks, and 145; Acid Gas Injection Compre 115 |
| TEMPO_RELEASE_PT_NO | other | 209 | 0 | 10F 171; Fl-1 144; Emergency vent 125; 9F 113 |
| TEMPO_RELEASE_PT_DESC | who | 191 | 0 | Acid Gas Flare 187; Flare 186; Inlet Flare 172; Emergency vent 126 |
| DISCOVERY_DATE | date | 467 | 0 | 1578898800000 18; 1692079200000 17; 1572501600000 15; 1570168800000 14 |
| DISCOVERY_TIME | who | 446 | 0 | 11:00:00 230; 09:00:00 90; 08:00:00 79; 10:00:00 79 |
| EVENT_START_DATE | date | 460 | 0 | 1549522800000 20; 1572501600000 17; 1576134000000 15; 1570773600000 14 |
| EVENT_START_TIME | who | 487 | 0 | 00:00:00 119; 09:00:00 89; 12:00:00 74; 10:00:00 73 |
| EVENT_END_DATE | date | 469 | 0 | 1572501600000.0 23; 1692856800000.0 17; 1554962400000.0 15; 1576134000000.0 14 |
| EVENT_END_TIME | who | 521 | 0 | 23:59:00 81; 09:00:00 69; 17:00:00 60; 00:00:00 57 |
| EE_EVENT_TYPE_DESC | category | 18 | 0 | Malfunction, Title V Devi 1.0K; Malfunction 610; Emergency 95; Title V Deviation, Malfun 79 |
| FINAL_EER_DUE_DATE | date | 6 | 0 | nan 2.0K; 9-Nov-20 1; 8-Sep-20 1; 9-Sep-20 1 |
| AI_NAICS_CODE | category | 8 | 0 | 21113 1.0K; 48621 369; 21112 306; 32411 262 |
| AI_NAICS_DESCRIPTION | category | 8 | 0 | Natural Gas Extraction 1.0K; Pipeline Transportation o 369; Crude Petroleum Extractio 306; Petroleum Refineries 262 |
| FINAL_EER_ACTUAL_DATE | date | 367 | 0 | 1548399600000.0 25; 1635400800000.0 24; 1576220400000.0 19; 1573714800000.0 18 |
| CO_CHEMICAL_CODE | category | 2 | 0 | CO 1.3K; nan 703 |
| CO_CHEMICAL_NAME | category | 2 | 0 | Carbon Monoxide 1.3K; nan 703 |
| CO_UOM | category | 2 | 0 | lbs. 1.3K; nan 703 |
| CO_DURATION | other | 357 | 0 | 0 709; 60 124; 120 85; 180 56 |
| CO_EMISSION_LIMIT | amount | 69 | 0 | 0.0 1.2K; 0.06 176; 0.04 94; 0.57 65 |
| CO_EMISSION_LIMIT_UOM | category | 7 | 0 | lbs./hour 1.1K; nan 729; tons/year 171; PPM 9 |
| CO_AVERAGING_PERIOD | other | 98 | 0 | 0 851; 1 827; 3 56; 2 44 |
| CO_AVERAGING_PERIOD_UOM | category | 10 | 0 | hour 948; nan 760; annual, monthly rolling 126; minutes 73 |
| CO_EXCESS_EMISSIONS_OF_EVENT | amount | 1.2K | 0 | 0.0 703; 9.6 8; 3.51 8; 18.62 7 |
| CO_NUMBER_OF_EXCEEDENCES | other | 53 | 0 | 0 848; 1 725; 2 87; 3 61 |
| CO_AVERAGE_EMISSION_RATE | amount | 983 | 0 | 0.0 939; 61.4 9; 0.1 7; 44.7 7 |
| CO_AVERAGE_EMISSION_RATE_UOM | category | 6 | 0 | nan 948; lbs./hour 938; minutes 68; tons/year 35 |
| NOX_CHEMICAL_CODE | category | 2 | 0 | Nox 1.2K; nan 814 |
| NOX_CHEMICAL_NAME | category | 2 | 0 | Nitrogen Dioxide 1.2K; nan 814 |
| NOX_UOM | category | 2 | 0 | lbs. 1.2K; nan 814 |
| NOX_DURATION | other | 360 | 0 | 0 820; 60 109; 120 74; 180 49 |
| NOX_EMISSION_LIMIT | amount | 68 | 0 | 0.0 1.4K; 0.08 104; 10.0 83; 0.1 82 |
| NOX_EMISSION_LIMIT_UOM | category | 7 | 0 | lbs./hour 965; nan 843; tons/year 169; lbs./MMbtu 16 |
| NOX_AVERAGING_PERIOD | other | 97 | 0 | 0 961; 1 703; 3 63; 2 46 |
| NOX_AVERAGING_PERIOD_UOM | category | 10 | 0 | nan 871; hour 841; annual, monthly rolling 127; minutes 74 |
| NOX_EXCESS_EMISSIONS_OF_EVENT | amount | 1.0K | 0 | 0.0 814; 1.0 9; 1.82 8; 4.7 7 |
| NOX_NUMBER_OF_EXCEEDENCES | other | 53 | 0 | 0 959; 1 677; 2 72; 3 54 |
| NOX_AVERAGE_EMISSION_RATE | amount | 867 | 0 | 0.0 1.1K; 30.75 8; 0.1 7; 22.39 7 |
| NOX_AVERAGE_EMISSION_RATE_UOM | category | 7 | 0 | nan 1.1K; lbs./hour 819; minutes 68; tons/year 34 |
| PM_CHEMICAL_CODE | category | 2 | 0 | nan 1.9K; PM 99 |
| PM_CHEMICAL_NAME | category | 2 | 0 | nan 1.9K; Particulate Matter (total 99 |
| PM_UOM | category | 2 | 0 | nan 1.9K; lbs. 99 |
| PM_DURATION | other | 69 | 0 | 0 1.9K; 60 12; 10 6; 20 4 |
| PM_EMISSION_LIMIT | amount | 8 | 0 | 0.0 2.0K; 0.6 11; 1.0 7; 2.236 6 |
| PM_EMISSION_LIMIT_UOM | category | 3 | 0 | nan 1.9K; lbs./hour 89; tons/year 10 |
| PM_AVERAGING_PERIOD | category | 3 | 0 | 0 1.9K; 1 78; 3 19 |
| PM_AVERAGING_PERIOD_UOM | category | 6 | 0 | nan 1.9K; hour 63; hour, hourly rolling 18; annual 10 |
| PM_EXCESS_EMISSIONS_OF_EVENT | amount | 100 | 0 | 0.0 1.9K; 13.11 2; 7.1 1; 3.4 1 |
| PM_NUMBER_OF_EXCEEDENCES | category | 21 | 0 | 0 1.9K; 1 78; 71 1; 34 1 |
| PM_AVERAGE_EMISSION_RATE | amount | 17 | 0 | 0.0 2.0K; 0.1 13; 1.0 2; 0.142 1 |
| PM_AVERAGE_EMISSION_RATE_UOM | category | 3 | 0 | nan 2.0K; lbs./hour 20; tons/year 9 |
| PM10_CHEMICAL_CODE | category | 2 | 0 | nan 2.0K; PM10 12 |
| PM10_CHEMICAL_NAME | category | 2 | 0 | nan 2.0K; Particulate Matter (10 mi 12 |
| PM10_UOM | category | 2 | 0 | nan 2.0K; lbs. 12 |
| PM10_DURATION | category | 7 | 0 | 0 2.0K; 60 7; 720 1; 240 1 |
| PM10_EMISSION_LIMIT | amount | 4 | 0 | 0.0 2.0K; 2.236 6; 2.2 2; 49.2 1 |
| PM10_EMISSION_LIMIT_UOM | category | 3 | 0 | nan 2.0K; tons/year 9; lbs./hour 3 |
| PM10_AVERAGING_PERIOD | category | 2 | 0 | 0 2.0K; 1 11 |
| PM10_AVERAGING_PERIOD_UOM | category | 4 | 0 | nan 2.0K; annual 9; hour 2; hour block 1 |
| PM10_EXCESS_EMISSIONS_OF_EVENT | amount | 13 | 0 | 0.0 2.0K; 0.671 1; 0.124 1; 0.66 1 |
| PM10_NUMBER_OF_EXCEEDENCES | category | 4 | 0 | 0 2.0K; 1 10; 4 1; 12 1 |
| PM10_AVERAGE_EMISSION_RATE | amount | 12 | 0 | 0.0 2.0K; 2.907 1; 2.36 1; 0.66 1 |
| PM10_AVERAGE_EMISSION_RATE_UOM | category | 3 | 0 | nan 2.0K; tons/year 9; lbs./hour 2 |
| PM25_CHEMICAL_CODE | category | 2 | 0 | nan 2.0K; 1770318000000.0 8 |
| PM25_CHEMICAL_NAME | category | 2 | 0 | nan 2.0K; Particulate Matter (2.5 m 8 |
| PM25_UOM | category | 2 | 0 | nan 2.0K; lbs. 8 |
| PM25_DURATION | category | 4 | 0 | 0 2.0K; 60 6; 720 1; 4860 1 |
| PM25_EMISSION_LIMIT | amount | 3 | 0 | 0.0 2.0K; 2.236 6; 2.2 2 |
| PM25_EMISSION_LIMIT_UOM | category | 2 | 0 | nan 2.0K; tons/year 8 |
| PM25_AVERAGING_PERIOD | category | 2 | 0 | 0 2.0K; 1 8 |
| PM25_AVERAGING_PERIOD_UOM | category | 2 | 0 | nan 2.0K; annual 8 |
| PM25_EXCESS_EMISSIONS_OF_EVENT | amount | 9 | 0 | 0.0 2.0K; 0.671 1; 0.124 1; 0.076 1 |
| PM25_NUMBER_OF_EXCEEDENCES | category | 2 | 0 | 0 2.0K; 1 8 |
| PM25_AVERAGE_EMISSION_RATE | amount | 9 | 0 | 0.0 2.0K; 2.907 1; 2.36 1; 2.312 1 |
| PM25_AVERAGE_EMISSION_RATE_UOM | category | 2 | 0 | nan 2.0K; tons/year 8 |
| SO2_CHEMICAL_CODE | category | 2 | 0 | SO2 1.2K; nan 821 |
| SO2_CHEMICAL_NAME | category | 2 | 0 | Sulfur Dioxide 1.2K; nan 821 |
| SO2_UOM | category | 2 | 0 | lbs 1.2K; nan 821 |
| SO2_DURATION | other | 287 | 0 | 0 827; 60 110; 120 92; 180 83 |
| SO2_EMISSION_LIMIT | amount | 49 | 0 | 0.0 1.5K; 162.0 134; 10.0 89; 0.011 65 |
| SO2_EMISSION_LIMIT_UOM | category | 5 | 0 | lbs./hour 910; nan 835; PPM 147; tons/year 106 |
| SO2_AVERAGING_PERIOD | other | 88 | 0 | 0 918; 1 618; 3 178; 24 44 |
| SO2_AVERAGING_PERIOD_UOM | category | 10 | 0 | nan 858; hour 758; hour, hourly rolling 200; minutes 73 |
| SO2_EXCESS_EMISSIONS_OF_EVENT | amount | 1.1K | 0 | 0.0 821; 0.17 10; 0.3 9; 0.5 9 |
| SO2_NUMBER_OF_EXCEEDENCES | other | 67 | 0 | 0 903; 1 615; 2 79; 3 71 |
| SO2_AVERAGE_EMISSION_RATE | amount | 847 | 0 | 0.0 1.0K; 0.4 10; 0.17 8; 0.23 8 |
| SO2_AVERAGE_EMISSION_RATE_UOM | category | 7 | 0 | nan 1.0K; lbs./hour 869; minutes 68; tons/year 8 |
| VOC_CHEMICAL_CODE | category | 2 | 0 | VOC 1.4K; nan 594 |
| VOC_CHEMICAL_NAME | category | 2 | 0 | Volatile Organic Compound 1.4K; nan 594 |
| VOC_UOM | category | 2 | 0 | lbs. 1.4K; nan 594 |
| VOC_DURATION | other | 360 | 0 | 0 601; 60 127; 120 109; 180 70 |
| VOC_EMISSION_LIMIT | amount | 56 | 0 | 0.0 1.4K; 10.0 150; 0.03 102; 0.12 47 |
| VOC_EMISSION_LIMIT_UOM | category | 6 | 0 | lbs./hour 1.0K; nan 652; tons/year 305; minutes 8 |
| VOC_AVERAGING_PERIOD | other | 97 | 0 | 1 871; 0 751; 2 58; 3 52 |
| VOC_AVERAGING_PERIOD_UOM | category | 10 | 0 | hour 931; nan 683; annual, monthly rolling 216; minutes 65 |
| VOC_EXCESS_EMISSIONS_OF_EVENT | amount | 1.1K | 0 | 0.0 594; 0.01 51; 0.02 25; 0.03 20 |
| VOC_NUMBER_OF_EXCEEDENCES | other | 52 | 0 | 1 908; 0 726; 2 73; 4 52 |
| VOC_AVERAGE_EMISSION_RATE | amount | 895 | 0 | 0.0 857; 0.01 31; 0.001 19; 0.02 16 |
| VOC_AVERAGE_EMISSION_RATE_UOM | category | 7 | 0 | lbs./hour 874; nan 868; tons/year 184; minutes 63 |
| OP_CHEMICAL_CODE | empty | 1 | 2.0K |  |
| OP_CHEMICAL_NAME | empty | 1 | 2.0K |  |
| OP_UOM | empty | 1 | 2.0K |  |
| OP_DURATION | other | 1 | 0 | 0 2.0K |
| OP_EMISSION_LIMIT | other | 1 | 0 | 0 2.0K |
| OP_EMISSION_LIMIT_UOM | empty | 1 | 2.0K |  |
| OP_AVERAGING_PERIOD | other | 1 | 0 | 0 2.0K |
| OP_AVERAGING_PERIOD_UOM | empty | 1 | 2.0K |  |
| OP_EXCESS_EMISSIONS_OF_EVENT | other | 1 | 0 | 0 2.0K |
| OP_NUMBER_OF_EXCEEDENCES | other | 1 | 0 | 0 2.0K |
| OP_AVERAGE_EMISSION_RATE | other | 1 | 0 | 0 2.0K |
| OP_AVERAGE_EMISSION_RATE_UOM | empty | 1 | 2.0K |  |
| VE_CHEMICAL_CODE | empty | 1 | 2.0K |  |
| VE_CHEMICAL_NAME | empty | 1 | 2.0K |  |
| VE_UOM | empty | 1 | 2.0K |  |
| VE_DURATION | other | 1 | 0 | 0 2.0K |
| VE_EMISSION_LIMIT | other | 1 | 0 | 0 2.0K |
| VE_EMISSION_LIMIT_UOM | empty | 1 | 2.0K |  |
| VE_AVERAGING_PERIOD | other | 1 | 0 | 0 2.0K |
| VE_AVERAGING_PERIOD_UOM | empty | 1 | 2.0K |  |
| VE_EXCESS_EMISSIONS_OF_EVENT | other | 1 | 0 | 0 2.0K |
| VE_NUMBER_OF_EXCEEDENCES | other | 1 | 0 | 0 2.0K |
| VE_AVERAGE_EMISSION_RATE | other | 1 | 0 | 0 2.0K |
| VE_AVERAGE_EMISSION_RATE_UOM | empty | 1 | 2.0K |  |
| H2S_CHEMICAL_CODE | category | 2 | 0 | nan 1.3K; H2S 683 |
| H2S_CHEMICAL_NAME | category | 2 | 0 | nan 1.3K; Hydrogen Sulfide 683 |
| H2S_UOM | category | 2 | 0 | nan 1.3K; lbs. 683 |
| H2S_DURATION | other | 240 | 0 | 0 1.3K; 60 61; 120 49; 180 32 |
| H2S_EMISSION_LIMIT | amount | 29 | 0 | 0 1.9K; 5 71; 12.3 7; 19.9 5 |
| H2S_EMISSION_LIMIT_UOM | category | 6 | 0 | nan 1.3K; lbs./hour 579; tons/year 81; minutes 2 |
| H2S_AVERAGING_PERIOD | other | 86 | 0 | 0 1.4K; 1 329; 2 35; 5 28 |
| H2S_AVERAGING_PERIOD_UOM | category | 10 | 0 | nan 1.4K; hour 496; annual, monthly rolling 64; minutes 60 |
| H2S_EXCESS_EMISSIONS_OF_EVENT | amount | 386 | 0 | 0 1.3K; 0.01 51; 0.02 29; 0.03 19 |
| H2S_NUMBER_OF_EXCEEDENCES | category | 24 | 0 | 0 1.4K; 1 485; 2 35; 3 17 |
| H2S_AVERAGE_EMISSION_RATE | amount | 351 | 0 | 0 1.5K; 0.0004 14; 0.03 12; 0.02 12 |
| H2S_AVERAGE_EMISSION_RATE_UOM | category | 6 | 0 | nan 1.5K; lbs./hour 428; minutes 55; lbs./MMbtu 6 |
| TEMPO_FAILURE_PT_DESC_NA | other | 1 | 0 | FALSE 2.0K |
| TEMPO_FAILURE_PT_NO_NA | other | 1 | 0 | FALSE 2.0K |
| TEMPO_RELEASE_PT_DESC_NA | other | 1 | 0 | FALSE 2.0K |
| TEMPO_RELEASE_PT_NO_NA | other | 1 | 0 | FALSE 2.0K |
| DUPLICATE | category | 3 | 0 | Unlikely 1.9K; Somewhat Likely 65; Likely 10 |
| EVENT_START_MONTH | category | 12 | 0 | 12 211; 10 197; 4 194; 1 186 |
| EVENT_START_YEAR | category | 3 | 0 | 2019 1.9K; 2020 128; 2022 1 |
| EVENT_START_QUARTER | category | 4 | 0 | 4 574; 1 509; 2 478; 3 439 |
| EVENT_START_DATETIME | date | 1.8K | 0 | 1549566000000 18; 1562464800000 12; 1571025600000 11; 1570636800000 11 |
| EVENT_END_DATETIME | date | 1.8K | 0 | 1692910920000.0 18; 1572447600000.0 11; 1571032800000.0 11; 1570719600000.0 11 |
| EVENT_DURATION_DAYS | amount | 451 | 0 | 0.041666666666666664 171; 0.083333333 139; 0.125 103; 0.16666666666666666 71 |
| PMSELECTED_EXCESS_EMISSIONS_OF_EVENT | amount | 100 | 0 | 0.0 1.9K; 13.11 2; 7.1 1; 3.4 1 |
| TOTAL_EXCESS_EMISSIONS_OF_EVENT | amount | 1.9K | 0 | 48900.0 18; 0.2 12; 12.16 11; 3.4 11 |
| EE_EVENT_TYPE_DESC_CLEAN | category | 6 | 0 | Malfunction 1.7K; Emergency 145; Other 85; Shutdown 33 |
| FAILURE_POINT_COMBINED | who | 333 | 0 | 198_Unit 55 151; 32800_FL2 (SSM + pilot) 134; 37954_Fl-1 86; 32800_FL1 (SSM+pilot) 54 |
| MULTI_DAY_EVENT | category | 2 | 0 | FALSE 1.7K; TRUE 283 |
| FACILITY_ONLY_EVENTS_LAST_12_MO | other | 1 | 0 | FALSE 2.0K |
| FACILITY_NO_EVENTS_IN_12_MO | category | 2 | 0 | TRUE 1.1K; FALSE 921 |
| FACILITY_EVENTS_12_MO_AND_BEFORE | category | 2 | 0 | FALSE 1.1K; TRUE 921 |
| FACILITY_EVENTS_SINGLE_YEAR | category | 2 | 0 | FALSE 1.9K; TRUE 82 |
| FACILITY_NO_EVENTS_IN_24_MO | category | 2 | 0 | FALSE 1.0K; TRUE 997 |
| FACILITY_EVENTS_MULTIPLE_YEARS | category | 2 | 0 | TRUE 1.9K; FALSE 82 |
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| GEOMETRY | who | 106 | 0 | {"type": "Point", "coordi 295; {"type": "Point", "coordi 290; {"type": "Point", "coordi 253; {"type": "Point", "coordi 102 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:35:18.87872 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c4623690-e0a2-4297-8e7b-f 2.0K |
| SRC_SHA256 | who | 1 | 0 | 3b07e6a34a2be417cd8fe2c0e 2.0K |
