# PORTAL_ARC_LA_COUNTY_OPEN_D_E549C7C921

rows 76  columns 31  scan 4.3s

roles: amount 6, audit 2, category 10, date 2, other 7, who 5

## when

DCN
  2011        56  ##############################

INGESTED_AT
  2026        76  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 76 | 33.75 | 33.98 | 34.60 | 34.60 | 2.6K |
| LONGITUDE | 76 | -118.63 | -118.22 | -117.84 | -117.80 | -9.0K |
| RSEI_SCORE_FOR_CHROMIUM | 56 | 0 | 6.38 | 70.2K | 88.3K | 266.6K |
| CANCER_RSEI_SCORE_FOR_CHROMIUM | 56 | 0 | 6.38 | 70.2K | 88.3K | 266.6K |
| TOTAL_RSEI_SCORE_FOR_ALL_MEDIA | 56 | 0 | 1.2K | 1.03M | 1.54M | 3.04M |
| TOTAL_CANCER_RSEI_SCORE_FOR_ALL | 56 | 0 | 1.2K | 1.03M | 1.54M | 3.04M |

## who

TRI_FACILITY_NAME by rows
         2  OLYMPUS TERMINALS LLC
         2  ALATUS AEROSYSTEMS
         2  AIR PRODUCTS & CHEMICALS INC.
         1  CUNICO CORP, A BWXT COMPANY
         1  ALLOYS CLEANING INC
         1  AQUAFINE CORP
         1  CALIBER AERO LLC
         1  ORCHID ORTHOPEDIC SOLUTIONS
         1  SPS TECHNOLOGIES LLC DBA PB FASTENERS
         1  PACIFIC SCIENTIFIC HTL/KIN-TECH DIV
         1  GRISWOLD INDUSTRIES DBA SOUNDCAST
         1  PRECISION SPECIALTY METALS INC
         1  PRESS FORGE CO
         1  OLD COUNTRY MILLWORK INC.
         1  EXIDE TECHNOLOGIES
         1  HONEYWELL INTERNATIONAL INC
         1  ALTAIR PARAMOUNT LLC
         1  DESIGNED METAL CONNECTIONS
         1  NEW HAMPSHIRE BALL BEARINGS INC.
         1  AVK INDUSTRIAL PRODUCTS

TRI_FACILITY_NAME by dollars
       1.54M        1 rows  COAST PLATING INC
      609.1K        1 rows  TORRANCE REFINING CO LLC
      319.7K        1 rows  CHEVRON PRODUCTS CO. DIV OF CHEVRON USA INC.
      147.0K        1 rows  AERO-ELECTRIC CONNECTOR INC.
       70.4K        1 rows  LOCKHEED MARTIN AERONAUTICS CO
       65.6K        1 rows  TESORO LOS ANGELES REFINERY-CARSON OPERATIONS
       64.6K        1 rows  CUNICO CORP, A BWXT COMPANY
       41.6K        1 rows  CERTIFIED ALLOY PRODUCTS INC
       37.8K        1 rows  HI-SHEAR CORP
       24.4K        1 rows  SENIOR AEROSPACE INC SSP DIV
       20.1K        1 rows  EME INC
       18.7K        1 rows  DESIGNED METAL CONNECTIONS
       11.4K        1 rows  WOODWARD HRT-DUARTE
        8.4K        1 rows  PAC FOUNDRIES-INDUSTRY
        7.8K        1 rows  TECHNI-CAST CORP
        6.3K        1 rows  PACIFIC ALLOY CASTINGS
        5.9K        1 rows  PRESS FORGE CO
        5.8K        1 rows  AQUAFINE CORP
        5.6K        1 rows  MILLER CASTINGS INC.
        3.8K        1 rows  CALIBER AERO LLC

TRI_FACILITY_ID by rows
         1  90040THMCC5501E
         1  90201MTLSR6060S
         1  90280STRTG8616T
         1  9000WLDCNT5855H
         1  90670BRWNP13639
         1  9024WSPCLK1336H
         1  9135WTRSPC2865F
         1  90058GNBNC2717S
         1  9072WPRSSF77JAC
         1  90248CSTPL128W1
         1  9135WQFNCR291AV
         1  90255WSTCS245E5
         1  90813CNCCR191W1
         1  9060WMLLRC253PA
         1  90221MNCXX431OA
         1  90063PRCSN3301M
         1  90280SHLTZ5321F
         1  91745QMTCN720SO
         1  90249PBFST1700W
         1  90248NCMTL417WE

TRI_FACILITY_ID by dollars
       1.54M        1 rows  90248NCMTL417WE
      609.1K        1 rows  90509MBLLC3700W
      319.7K        1 rows  90245CHVRN324WE
      147.0K        1 rows  90501CNSYS548AM
       70.4K        1 rows  93550LCKHD1011L
       65.6K        1 rows  90749RCPRD1801E
       64.6K        1 rows  90813CNCCR191W1
       41.6K        1 rows  90801CRTFD3245C
       37.8K        1 rows  90509HSHRC2600S
       24.4K        1 rows  91504STNLS2980N
       20.1K        1 rows  90221MNCXX431OA
       18.7K        1 rows  90248DTSCH14800
       11.4K        1 rows  91010DWTYR1700B
        8.4K        1 rows  91745TLDYN16800
        7.8K        1 rows  90280TCHNC11220
        6.3K        1 rows  90280PCFCL5900E
        5.9K        1 rows  9072WPRSSF77JAC
        5.8K        1 rows  9135WQFNCR291AV
        5.6K        1 rows  9060WMLLRC253PA
        3.8K        1 rows  9067WCLBRR1265C

COUNTY by rows
        76  LOS ANGELES, CA

COUNTY by dollars
       3.04M       76 rows  LOS ANGELES, CA

STATE by rows
        76  California

STATE by dollars
       3.04M       76 rows  California

## who x when

TRI_FACILITY_NAME by DCN, dollars = TOTAL_RSEI_SCORE_FOR_ALL_MEDIA
  AERO-ELECTRIC CONNECTOR INC.              2011:147.0K
  AIR PRODUCTS & CHEMICALS INC.             2011:2.6K
  ALATUS AEROSYSTEMS                        2011:16.88
  ALLOYS CLEANING INC                       2011:0
  AQUAFINE CORP                             2011:5.8K
  CALIBER AERO LLC                          2011:3.8K
  CERTIFIED ALLOY PRODUCTS INC              2011:41.6K
  CHEVRON PRODUCTS CO. DIV OF CHEVRON USA   2011:319.7K
  COAST PLATING INC                         2011:1.54M
  CUNICO CORP, A BWXT COMPANY               2011:64.6K
  DESIGNED METAL CONNECTIONS                2011:18.7K
  EME INC                                   2011:20.1K
  EXIDE TECHNOLOGIES                        2011:2.7K
  GRISWOLD INDUSTRIES DBA SOUNDCAST         2011:2.8K
  HI-SHEAR CORP                             2011:37.8K
  HONEYWELL INTERNATIONAL INC               2011:1.2K
  LOCKHEED MARTIN AERONAUTICS CO            2011:70.4K
  NEW HAMPSHIRE BALL BEARINGS INC.          2011:0.43
  OLYMPUS TERMINALS LLC                     2011:175.40
  PRECISION SPECIALTY METALS INC            2011:413.19
  PRESS FORGE CO                            2011:5.9K
  SENIOR AEROSPACE INC SSP DIV              2011:24.4K
  SPS TECHNOLOGIES LLC DBA PB FASTENERS     2011:587
  TESORO LOS ANGELES REFINERY-CARSON OPERA  2011:65.6K
  TORRANCE REFINING CO LLC                  2011:609.1K

TRI_FACILITY_ID by DCN, dollars = TOTAL_RSEI_SCORE_FOR_ALL_MEDIA
  90058GNBNC2717S                           2011:2.7K
  90063PRCSN3301M                           2011:413.19
  90201MTLSR6060S                           2011:0
  90221MNCXX431OA                           2011:20.1K
  90245CHVRN324WE                           2011:319.7K
  90248CSTPL128W1                           2011:1.6K
  90248DTSCH14800                           2011:18.7K
  90248NCMTL417WE                           2011:1.54M
  90249PBFST1700W                           2011:587
  9024WSPCLK1336H                           2011:301.58
  90255WSTCS245E5                           2011:800.63
  90280SHLTZ5321F                           2011:472.62
  90280STRTG8616T                           2011:2.8K
  90501CNSYS548AM                           2011:147.0K
  90509HSHRC2600S                           2011:37.8K
  90509MBLLC3700W                           2011:609.1K
  9060WMLLRC253PA                           2011:5.6K
  90670BRWNP13639                           2011:1.78
  9072WPRSSF77JAC                           2011:5.9K
  90749RCPRD1801E                           2011:65.6K
  90801CRTFD3245C                           2011:41.6K
  90813CNCCR191W1                           2011:64.6K
  91010DWTYR1700B                           2011:11.4K
  9135WQFNCR291AV                           2011:5.8K
  91504STNLS2980N                           2011:24.4K
  91745QMTCN720SO                           2011:31.30
  93550LCKHD1011L                           2011:70.4K

## what

YEAR: 2022 59%, 2020 8%, 2013 8%, 2021 5%, 2019 5%, 2015 5%, 2018 4%, 2014 4%, 2017 1%

ZIP_CODE: 91355 15%, 90723 12%, 90280 12%, 90670 9%, 90248 9%, 90058 9%, 91745 6%, 91746 6%, 91605 6%, 91352 6%, 91010 6%, 90810 6%

CITY: TORRANCE, CA 12%, LOS ANGELES, CA 12%, VALENCIA, CA 10%, GARDENA, CA 10%, CITY OF INDUSTRY, CA 8%, CARSON, CA 8%, PARAMOUNT, CA 8%, SOUTH GATE, CA 8%, LONG BEACH, CA 6%, SANTA FE SPRINGS, CA 6%, PALMDALE, CA 4%, NORTH HOLLYWOOD, CA 4%

CHEMICAL: Chromium and chromi 74%, Chromium 14%, Chromium compounds 12%

INDUSTRY_SECTOR: 332 Fabricated Metals 45%, 331 Primary Metals 16%, 336 Transportation Equipment 14%, 325 Chemicals 8%, 333 Machinery 5%, 324 Petroleum Products 4%, 4247 Petroleum Bulk Terminals 3%, 334 Computers and Electronic P 1%, 339 Miscellaneous Manufacturin 1%, 4246 Chemical Wholesalers 1%, 562 Hazardous Waste 1%

NAICS_CODE: 332813 Electroplating, Plating 27%, 336413 Other Aircraft Parts an 16%, 332722 Bolt, Nut, Screw, Rivet 14%, 332111 Iron and Steel Forging 6%, 331513 Steel Foundries (except 6%, 324110 Petroleum Refineries 6%, 332721 Precision Turned Produc 4%, 336411 Aircraft Manufacturing 4%, 331512 Steel Investment Foundr 4%, 331492 Secondary Smelting, Ref 4%, 332710 Machine Shops 4%, 325120 Industrial Gas Manufact 4%

CAS_CODE: 7440-47-3 68%, N090 32%

PARENT_COMPANY: NA 33%, BERKSHIRE HATHAWAY INC 21%, HOWMET AEROSPACE INC 9%, NOVARIA GROUP 7%, VALENCE SURFACE TECHNOLOGIES L 7%, AEROSPACE SYSTEMS & STRUCTURES 5%, AIR PRODUCTS & CHEMICALS INC 5%, OLYMPUS TERMINALS LLC 5%, LOCKHEED MARTIN CORP 2%, KPS GLOBAL LLC 2%, SIGMA PLATING CO INC 2%, CUSTOM ALLOY SALES INC 2%

YEAR_LAST_REPORTED_TO_TRI_PROGR: 2022 37%, No Data 25%, 2020 12%, 2013 5%, 2018 4%, 2021 4%, 2019 4%, nan 3%, 2014 3%, 2015 3%, 2017 1%

NON_CANCER_RSEI_SCORE_FOR_CHROM: No Data 48%, 0 28%, nan 2%, 0.000278583 2%, 0.00825169 2%, 0.00288758 2%, 5.21754E-06 2%, 2.93852E-05 2%, 8.93154E-06 2%, 0.000161978 2%, 0.000678923 2%, 8.72215E-08 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 76 | 0 | 76 1; 75 1; 74 1; 73 1 |
| TRI_FACILITY_NAME | who | 74 | 0 | ALATUS AEROSYSTEMS 2; AIR PRODUCTS & CHEMICALS  2; OLYMPUS TERMINALS LLC 2; LUSK QUALITY MACHINE PROD 1 |
| TRI_FACILITY_ID | who | 76 | 0 | 9359WLSKQLPBX91 1; 93550LCKHD1011L 1; 9178WTRMPH2415E 1; 91773NTNLC420EA 1 |
| FRSID | other | 77 | 0 | 110002892157 1; 110018950982 1; 110055500079 1; 110012701889 1 |
| YEAR | category | 9 | 0 | 2022 45; 2020 6; 2013 6; 2021 4 |
| CENSUS_TRACT | other | 58 | 0 | 6037980035 4; 6037920106 4; 6037980002 3; 6037980016 3 |
| CENSUS_BLOCK_GROUP | other | 59 | 0 | 60379800351 4; 60379201061 4; 60379800021 3; 60379800161 3 |
| ZIP_CODE | category | 48 | 0 | 91355 5; 90723 4; 90280 4; 90670 3 |
| STREET_ADDRESS | other | 77 | 0 | 39457 15TH STREET EAST 1; 1011 LOCKHEED WAY - MZ 01 1; 20415 EAST WALNUT DRIVE N 1; 420 E ARROW HWY 1 |
| CITY | category | 37 | 0 | TORRANCE, CA 6; LOS ANGELES, CA 6; VALENCIA, CA 5; GARDENA, CA 5 |
| COUNTY | who | 1 | 0 | LOS ANGELES, CA 76 |
| STATE | who | 1 | 0 | California 76 |
| LATITUDE | amount | 74 | 0 | 34.20119 2; 34.599518 1; 34.60263 1; 33.99986 1 |
| LONGITUDE | amount | 76 | 0 | -118.103187 1; -118.116485 1; -117.85886 1; -117.80011 1 |
| CHEMICAL | category | 3 | 0 | Chromium and chromi 56; Chromium 11; Chromium compounds 9 |
| INDUSTRY_SECTOR | category | 11 | 0 | 332 Fabricated Metals 34; 331 Primary Metals 12; 336 Transportation Equipm 11; 325 Chemicals 6 |
| NAICS_CODE | category | 38 | 0 | 332813 Electroplating, Pl 13; 336413 Other Aircraft Par 8; 332722 Bolt, Nut, Screw,  7; 332111 Iron and Steel For 3 |
| CAS_CODE | category | 2 | 0 | 7440-47-3 52; N090 24 |
| PARENT_COMPANY | category | 45 | 0 | NA 14; BERKSHIRE HATHAWAY INC 9; HOWMET AEROSPACE INC 4; NOVARIA GROUP 3 |
| YEAR_LAST_REPORTED_TO_TRI_PROGR | category | 11 | 0 | 2022 28; No Data 19; 2020 9; 2013 4 |
| DCN | date | 58 | 0 | No Data 19; nan 1; 1322220939716 1; 1318217516121 1 |
| RSEI_SCORE_FOR_CHROMIUM | amount | 48 | 0 | No Data 19; 0 11; nan 1; 0.4220949 1 |
| CANCER_RSEI_SCORE_FOR_CHROMIUM | amount | 48 | 0 | No Data 19; 0 11; nan 1; 0.4220949 1 |
| NON_CANCER_RSEI_SCORE_FOR_CHROM | category | 47 | 0 | No Data 19; 0 11; nan 1; 0.000278583 1 |
| TOTAL_RSEI_SCORE_FOR_ALL_MEDIA | amount | 54 | 0 | No Data 19; 0 5; nan 1; 70368.42209 1 |
| TOTAL_CANCER_RSEI_SCORE_FOR_ALL | amount | 54 | 0 | No Data 19; 0 5; nan 1; 70368.42209 1 |
| TOTAL_NON_CANCER_RSEI_SCORE_FOR | other | 54 | 0 | No Data 19; 0 5; nan 1; 57.27657858 1 |
| GEOMETRY | other | 75 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:54.31908 76 |
| SOURCE_RUN_ID | audit | 1 | 0 | d83a4a32-fff6-407b-862c-1 76 |
| SRC_SHA256 | who | 1 | 0 | 595a9319835b590e784ee18b8 76 |
