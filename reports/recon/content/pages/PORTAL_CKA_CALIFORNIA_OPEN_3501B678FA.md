# PORTAL_CKA_CALIFORNIA_OPEN_3501B678FA

rows 572  columns 15  scan 4.1s

roles: audit 2, category 4, date 4, empty 1, other 1, who 4

## when

SYSTEM_END_DATE
  2024         8  ##############################
  2025         1  ####

APPLICABLE_START_DATE
  2023       528  ##############################
  2024         9  #
  2025        35  ##

APPLICABLE_END_DATE
  2024        11  #########
  2025        38  ##############################

INGESTED_AT
  2026       572  ##############################

## who

PWS_NAME by rows
         2  CWS - MULLEN WATER COMPANY
         2  BIG BEAR SHORES RV RESORT
         2  WESTERN MWD (ID A - RAINBOW)
         2  CITY OF MODESTO - WALNUT MANOR
         2  TAHOE CITY PUD - TIMBERLAND
         2  AWA LA MEL HEIGHTS #3
         2  CCWD - WALLACE
         2  CAL AM - SECURITY PARK
         2  EL DORADO ID - OUTINGDALE
         2  CWS-SPLIT MOUNTAIN WATER SYSTEM
         2  HOOD WATER MAINTENCE DIST [SWS]
         2  NORTHGATE 880 [SWS]
         2  PLACER CWA - MONTE VISTA
         2  CWS - TULCO WATER COMPANY
         2  NEVADA ID - SMARTSVILLE
         2  CAL AM WATER COMPANY - GARRAPATA
         2  LOS ANGELES CWWD 40, REG. 35-N.E. L.A.
         2  LOS ANGELES CWWD 40, REG. 39-ROCK CREEK
         2  PLACER CWA - ALTA
         2  CAL AM WATER COMPANY - RALPH LANE

SUPPLIER_NAME by rows
        13  California American Water Company - Sacramento District
        12  Tuolumne Utilities District
        11  Placer County Water Agency
        11  Sacramento County Water Agency
        11  Modesto  City Of
        10  California Water Service Company Kern River Valley
        10  California American Water Company - Monterey District
         9  Tahoe City Public Utilities District
         8  Los Angeles County Waterworks District 40 - Antelope Valley
         8  Calaveras County Water District
         7  Nevada Irrigation District
         6  Big Bear Lake  City Of
         6  Amador Water Agency
         6  Santa Clarita Valley Water Agency
         5  California Water Service Company Salinas District
         5  California Water Service Company Visalia
         5  El Dorado Irrigation District
         4  Western Municipal Water District Of Riverside
         4  California American Water Company - Los Angeles Division
         4  Mission Springs Water District

ORG_ID by rows
        13  372
        12  2523
        11  1927
        11  2132
        11  1631
        10  369
        10  397
         9  2444
         8  351
         8  1484
         7  1718
         6  55
         6  4993
         6  198
         5  816
         5  427
         5  417
         4  1626
         4  368
         4  2697

SRC_SHA256 by rows
       572  c19369522e1371ba19ee260be8fc770eaf773b64569e78a06dbd609f9617edd3

## who x when

PWS_NAME by APPLICABLE_START_DATE
  AWA LA MEL HEIGHTS #3                     2023:1 2025:1
  BIG BEAR SHORES RV RESORT                 2023:1 2024:1
  CAL AM - SECURITY PARK                    2023:1 2025:1
  CAL AM WATER COMPANY - GARRAPATA          2023:1 2025:1
  CAL AM WATER COMPANY - RALPH LANE         2023:1 2025:1
  CCWD - WALLACE                            2023:1 2025:1
  CITY OF MODESTO - WALNUT MANOR            2023:1 2025:1
  CWS - MULLEN WATER COMPANY                2023:1 2025:1
  CWS - TULCO WATER COMPANY                 2023:1 2025:1
  CWS-SPLIT MOUNTAIN WATER SYSTEM           2023:1 2025:1
  EL DORADO ID - OUTINGDALE                 2023:1 2025:1
  HOOD WATER MAINTENCE DIST [SWS]           2023:1 2025:1
  LOS ANGELES CWWD 40, REG. 35-N.E. L.A.    2023:1 2024:1
  LOS ANGELES CWWD 40, REG. 39-ROCK CREEK   2023:1 2024:1
  NEVADA ID - SMARTSVILLE                   2023:1 2025:1
  NORTHGATE 880 [SWS]                       2023:1 2024:1
  PLACER CWA - ALTA                         2023:1 2024:1
  PLACER CWA - MONTE VISTA                  2023:1 2025:1
  TAHOE CITY PUD - TIMBERLAND               2023:1 2025:1
  WESTERN MWD (ID A - RAINBOW)              2023:1 2025:1

SUPPLIER_NAME by APPLICABLE_START_DATE
  Amador Water Agency                       2023:5 2025:1
  Big Bear Lake  City Of                    2023:4 2024:1 2025:1
  Calaveras County Water District           2023:6 2025:2
  California American Water Company - Los   2023:3 2024:1
  California American Water Company - Mont  2023:7 2025:3
  California American Water Company - Sacr  2023:11 2025:2
  California Water Service Company Kern Ri  2023:7 2025:3
  California Water Service Company Salinas  2023:5
  California Water Service Company Visalia  2023:3 2025:2
  El Dorado Irrigation District             2023:3 2025:2
  Los Angeles County Waterworks District 4  2023:5 2024:3
  Mission Springs Water District            2023:3 2025:1
  Modesto  City Of                          2023:8 2025:3
  Nevada Irrigation District                2023:6 2025:1
  Placer County Water Agency                2023:7 2024:1 2025:3
  Sacramento County Water Agency            2023:7 2024:1 2025:3
  Santa Clarita Valley Water Agency         2023:6
  Tahoe City Public Utilities District      2023:6 2024:2 2025:1
  Tuolumne Utilities District               2023:11 2025:1
  Western Municipal Water District Of Rive  2023:3 2025:1

## what

COUNTY: LOS ANGELES 26%, SAN BERNARDINO 10%, SACRAMENTO 9%, RIVERSIDE 8%, KERN 8%, ORANGE 7%, PLACER 7%, SAN DIEGO 6%, MONTEREY 5%, SAN MATEO 5%, VENTURA 5%, STANISLAUS 5%

WS_INCLUDED_YN: Yes 92%, No 8%

NUM_SC_LT200: Yes 100%

NOTES: Not included per supplier resp 33%, Consolidated with CA1910240 24%, Consolidated with CA5510012 14%, Not included per supplier resp 10%, Not included per supplier resp 10%, Consolidated with CA2710010 5%, LAM data unavailable 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ORG_ID | who | 409 | 0 | 2523 13; 372 13; 2132 12; 1927 12 |
| PWSID | other | 537 | 0 | CA3310076 4; CA5500363 4; CA3110013 4; CA3100029 4 |
| SUPPLIER_NAME | who | 402 | 0 | Tuolumne Utilities Distri 13; California American Water 13; Sacramento County Water A 12; Placer County Water Agenc 12 |
| PWS_NAME | who | 531 | 0 | WESTERN MWD (ID A - RAINB 4; TUD-WARDS FERRY RANCHES 4; TAHOE CITY PUD - TAHOE CE 4; TAHOE CITY PUD - TIMBERLA 4 |
| COUNTY | category | 49 | 0 | LOS ANGELES 99; SAN BERNARDINO 37; SACRAMENTO 34; RIVERSIDE 29 |
| WS_INCLUDED_YN | category | 3 | 1 | Yes 525; No 46 |
| SYSTEM_START_DATE | empty | 1 | 572 |  |
| SYSTEM_END_DATE | date | 4 | 563 | 2024-12-31T00:00:00 5; 2024-06-30T00:00:00 3; 2025-03-30T00:00:00 1 |
| APPLICABLE_START_DATE | date | 3 | 0 | 2023-07-01T00:00:00 528; 2025-07-01T00:00:00 35; 2024-07-01T00:00:00 9 |
| APPLICABLE_END_DATE | date | 3 | 523 | 2025-06-30T00:00:00 38; 2024-06-30T00:00:00 11 |
| NUM_SC_LT200 | category | 2 | 499 | Yes 73 |
| NOTES | category | 8 | 551 | Not included per supplier 7; Consolidated with CA19102 5; Consolidated with CA55100 3; Not included per supplier 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:21:32.90804 572 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5ed376e2-0e8d-4938-9430-5 572 |
| SRC_SHA256 | who | 1 | 0 | c19369522e1371ba19ee260be 572 |
