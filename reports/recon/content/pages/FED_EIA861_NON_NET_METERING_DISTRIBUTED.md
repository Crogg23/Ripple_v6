# FED_EIA861_NON_NET_METERING_DISTRIBUTED

rows 507  columns 79  scan 7.6s

roles: amount 50, audit 2, category 22, date 1, other 2, state 1, who 2

## when

_INGESTED_AT
  2026       507  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_CAPACITY | 506 | -8.97 | 0.80 | 229.05 | 1.1K | 6.0K |
| CAPACITY_BACK_UP_ONLY | 506 | 0 | 0 | 68.43 | 207.84 | 1.1K |
| CAPACITY_UTILITY_OWNED | 506 | 0 | 0 | 7.82 | 35.69 | 239.01 |
| RESIDENTIAL | 506 | -8.26 | 0.01 | 57.02 | 865.90 | 2.0K |
| COMMERCIAL | 506 | -2.69 | 0.05 | 42.38 | 130.93 | 1.1K |
| INDUSTRIAL | 506 | -0.79 | 0 | 4.43 | 143.62 | 233.71 |

## who

UTILITY_NAME by rows
        43  State Adjustment
         5  PacifiCorp
         3  MidAmerican Energy Co
         3  Tri-State Electric Member Corp
         2  City of Jellico
         2  Blue Ridge Mountain EMC - (GA)
         2  Tri-County Elec Member Corp (TN)
         2  Montana-Dakota Utilities Co
         2  Sioux Valley SW Elec Coop
         2  Duke Energy Carolinas, LLC
         2  Idaho Power Co
         2  Gibson Electric Members Corp
         2  Powell Valley Electric Coop
         2  Virginia Electric & Power Co
         2  Evergy Metro
         2  Mountain Electric Coop, Inc
         2  City of Chattanooga - (TN)
         2  MiEnergy Cooperative
         2  Duke Energy Progress - (NC)
         1  DTE Electric Company

UTILITY_NAME by dollars
        1.1K        1 rows  Oncor Electric Delivery Company LLC
      511.51        1 rows  CenterPoint Energy
      384.16        1 rows  Southern California Edison Co
      242.06        1 rows  AEP Texas Central Company
      241.28        1 rows  Georgia Power Co
      229.86        1 rows  Hawaiian Electric Co Inc
      213.60        1 rows  Florida Power & Light Co
      202.26        1 rows  Massachusetts Electric Co
      166.52        1 rows  Pacific Gas & Electric Co.
      149.27        1 rows  Austin Energy
      121.90        1 rows  PUD No 1 of Clark County - (WA)
      108.87        1 rows  City of Tallahassee - (FL)
      102.25        1 rows  North Carolina Eastern M P A
      101.30        1 rows  The Narragansett Electric Co
       98.77        1 rows  Duke Energy Florida, LLC
       79.25        1 rows  GreyStone Power Corporation
       75.65        1 rows  Texas-New Mexico Power Co
       63.88        1 rows  Consolidated Edison Co-NY Inc
       61.35        1 rows  San Diego Gas & Electric Co
       60.05        1 rows  Hawaii Electric Light Co Inc

_SRC_FILE by rows
       507  Non_Net_Metering_Distributed_2024.xlsx

_SRC_FILE by dollars
        6.0K      507 rows  Non_Net_Metering_Distributed_2024.xlsx

## who x when

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_CAPACITY
  AEP Texas Central Company                 2026:242.06
  Austin Energy                             2026:149.27
  Blue Ridge Mountain EMC - (GA)            2026:15.43
  CenterPoint Energy                        2026:511.51
  City of Chattanooga - (TN)                2026:5.52
  City of Jellico                           2026:0.25
  DTE Electric Company                      2026:21.49
  Duke Energy Carolinas, LLC                2026:25.99
  Duke Energy Progress - (NC)               2026:20.93
  Evergy Metro                              2026:20.70
  Florida Power & Light Co                  2026:213.60
  Georgia Power Co                          2026:241.28
  Gibson Electric Members Corp              2026:1.27
  Hawaiian Electric Co Inc                  2026:229.86
  Idaho Power Co                            2026:11.31
  Massachusetts Electric Co                 2026:202.26
  MiEnergy Cooperative                      2026:19.09
  MidAmerican Energy Co                     2026:2.74
  Montana-Dakota Utilities Co               2026:0.66
  Mountain Electric Coop, Inc               2026:1.29
  Oncor Electric Delivery Company LLC       2026:1.1K
  PacifiCorp                                2026:17.42
  Pacific Gas & Electric Co.                2026:166.52
  Powell Valley Electric Coop               2026:0.37
  Sioux Valley SW Elec Coop                 2026:0.22
  Southern California Edison Co             2026:384.16
  State Adjustment                          2026:-14.93
  Tri-County Elec Member Corp (TN)          2026:0.17
  Tri-State Electric Member Corp            2026:1.11
  Virginia Electric & Power Co              2026:11.64

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_CAPACITY
  Non_Net_Metering_Distributed_2024.xlsx    2026:6.0K

## where

STATE: TN 76, NC 31, TX 27, MS 24, KY 24, MN 22, AL 21, CO 18, GA 17, CA 17, IA 16, IN 14

## what

YEAR: 2024 100%, Note: Data includes distribute 0%

BA_CODE: TVA 32%, MISO 20%, SWPP 9%, PJM 8%, ERCO 5%, DUK 5%, SOCO 4%, WACM 4%, ISNE 4%, BPAT 3%, CPLE 3%, CISO 3%

TYPE: AC 86%, DC 14%

TRANSPORTATION: . 68%, 0 32%

TRANSPORTATION_1: . 96%, 0 4%

INDUSTRIAL_2: . 96%, 0 4%, 0.016 0%, 2.07 0%

TRANSPORTATION_2: . 96%, 0 4%

TRANSPORTATION_3: . 69%, 0 31%

RESIDENTIAL_4: . 69%, 0 31%, 0.024 0%, 2.5 0%

TRANSPORTATION_4: . 70%, 0 30%

RESIDENTIAL_5: . 69%, 0 30%, 0.117 0%

INDUSTRIAL_5: . 70%, 0 30%, 0.6 0%, 2.685 0%

TRANSPORTATION_5: . 70%, 0 30%

DIRECT_CONNECTED_5: . 70%, 0 30%, 0.42 0%, 0.225 0%

TRANSPORTATION_6: . 69%, 0 31%

TRANSPORTATION_7: . 70%, 0 30%

DIRECT_CONNECTED_7: . 70%, 0 30%, 1.013 0%

RESIDENTIAL_8: . 69%, 0 31%

TRANSPORTATION_8: . 70%, 0 30%

TRANSPORTATION_9: . 69%, 0 31%

DIRECT_CONNECTED_9: . 69%, 0 31%, 0.85 0%, 0.269 0%

TRANSPORTATION_10: 0 92%, . 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 2 | 0 | 2024 506; Note: Data includes distr 1 |
| STATE | state | 48 | 1 | TN 76; NC 31; TX 27; MS 24 |
| UTILITY_NUMBER | other | 435 | 1 | 99999 43; 14354 5; 3461 3; 20521 3 |
| UTILITY_NAME | who | 442 | 1 | State Adjustment 43; PacifiCorp 5; Cheyenne Light Fuel & Pow 3; Wheeling Power Co 3 |
| BA_CODE | category | 39 | 9 | TVA 136; MISO 87; SWPP 38; PJM 33 |
| NUMBER_OF_GENERATORS | other | 142 | 1 | 1 58; . 43; 2 39; 3 30 |
| TOTAL_CAPACITY | amount | 445 | 1 | 0.8 6; 0.074 5; 0.1 5; 0.006 4 |
| CAPACITY_BACK_UP_ONLY | amount | 80 | 1 | . 228; 0 193; 0.8 4; 0.5 3 |
| CAPACITY_UTILITY_OWNED | amount | 110 | 1 | . 198; 0 175; 0.5 5; 1 4 |
| TYPE | category | 2 | 115 | AC 337; DC 55 |
| RESIDENTIAL | amount | 207 | 1 | . 197; 0 32; 0.011 5; 0.006 5 |
| COMMERCIAL | amount | 276 | 1 | . 158; 0 31; 0.05 7; 0.006 5 |
| INDUSTRIAL | amount | 62 | 1 | . 287; 0 156; 0.1 2; 0.05 2 |
| TRANSPORTATION | category | 2 | 1 | . 344; 0 162 |
| DIRECT_CONNECTED | amount | 81 | 1 | . 267; 0 156; 0.05 2; 0.134 2 |
| TOTAL | amount | 364 | 1 | 0 86; 0.006 6; 0.1 6; 0.05 5 |
| RESIDENTIAL_1 | amount | 41 | 1 | . 450; 0 16; 0.008 2; 0.076 1 |
| COMMERCIAL_1 | amount | 40 | 1 | . 447; 0 17; 0.153 2; 0.03 2 |
| INDUSTRIAL_1 | amount | 10 | 1 | . 479; 0 19; 0.206 1; 0.015 1 |
| TRANSPORTATION_1 | category | 2 | 1 | . 486; 0 20 |
| DIRECT_CONNECTED_1 | amount | 8 | 1 | . 483; 0 16; 0.25 2; 1 1 |
| TOTAL_1 | amount | 58 | 1 | 0 265; . 179; 0.25 4; 0.008 2 |
| RESIDENTIAL_2 | amount | 23 | 1 | . 468; 0 16; 0.081 2; 4.111 1 |
| COMMERCIAL_2 | amount | 19 | 1 | . 470; 0 19; 0.02 1; 0.336 1 |
| INDUSTRIAL_2 | category | 4 | 1 | . 484; 0 20; 0.016 1; 2.07 1 |
| TRANSPORTATION_2 | category | 2 | 1 | . 486; 0 20 |
| DIRECT_CONNECTED_2 | amount | 7 | 1 | . 482; 0 19; 0.25 1; 0.475 1 |
| TOTAL_2 | amount | 32 | 1 | 0 297; . 179; 0.02 1; 0.336 1 |
| RESIDENTIAL_3 | amount | 25 | 1 | . 316; 0 150; 0.002 6; 0.012 5 |
| COMMERCIAL_3 | amount | 41 | 1 | . 305; 0 151; 0.002 5; 0.005 4 |
| INDUSTRIAL_3 | amount | 11 | 1 | . 338; 0 156; 0.004 2; 0.01 2 |
| TRANSPORTATION_3 | category | 2 | 1 | . 349; 0 157 |
| DIRECT_CONNECTED_3 | amount | 10 | 1 | . 342; 0 156; 0.86 1; 0.01 1 |
| TOTAL_3 | amount | 59 | 1 | 0 380; . 43; 0.002 10; 0.005 4 |
| RESIDENTIAL_4 | category | 4 | 1 | . 348; 0 156; 0.024 1; 2.5 1 |
| COMMERCIAL_4 | amount | 40 | 1 | . 318; 0 149; 0.95 1; 2.86 1 |
| INDUSTRIAL_4 | amount | 5 | 1 | . 349; 0 154; 0.465 1; 1.215 1 |
| TRANSPORTATION_4 | category | 2 | 1 | . 352; 0 154 |
| DIRECT_CONNECTED_4 | amount | 29 | 1 | . 325; 0 151; 0.8 3; 0.5 2 |
| TOTAL_4 | amount | 61 | 1 | 0 399; . 43; 0.8 3; 0.26 2 |
| RESIDENTIAL_5 | category | 3 | 1 | . 351; 0 154; 0.117 1 |
| COMMERCIAL_5 | amount | 11 | 1 | . 342; 0 154; 0.6 2; 0.4 1 |
| INDUSTRIAL_5 | category | 4 | 1 | . 352; 0 152; 0.6 1; 2.685 1 |
| TRANSPORTATION_5 | category | 2 | 1 | . 353; 0 153 |
| DIRECT_CONNECTED_5 | category | 4 | 1 | . 354; 0 150; 0.42 1; 0.225 1 |
| TOTAL_5 | amount | 12 | 1 | 0 451; . 43; 0.6 3; 0.4 1 |
| RESIDENTIAL_6 | amount | 18 | 1 | . 333; 0 156; 6.5 2; 0.04 1 |
| COMMERCIAL_6 | amount | 92 | 1 | . 256; 0 149; 0.8 5; 0.95 2 |
| INDUSTRIAL_6 | amount | 33 | 1 | . 320; 0 153; 1.35 2; 1 2 |
| TRANSPORTATION_6 | category | 2 | 1 | . 350; 0 156 |
| DIRECT_CONNECTED_6 | amount | 19 | 1 | . 336; 0 151; 0.5 2; 0.8 2 |
| TOTAL_6 | amount | 114 | 1 | 0 333; . 43; 0.8 7; 0.5 6 |
| RESIDENTIAL_7 | amount | 5 | 1 | . 348; 0 155; 0.002 1; 0.581 1 |
| COMMERCIAL_7 | amount | 21 | 1 | . 332; 0 154; 0.065 2; 0.633 1 |
| INDUSTRIAL_7 | amount | 8 | 1 | . 348; 0 152; 0.36 1; 0.756 1 |
| TRANSPORTATION_7 | category | 2 | 1 | . 353; 0 153 |
| DIRECT_CONNECTED_7 | category | 3 | 1 | . 353; 0 152; 1.013 1 |
| TOTAL_7 | amount | 24 | 1 | 0 440; . 43; 0.065 2; 0.995 1 |
| RESIDENTIAL_8 | category | 2 | 1 | . 351; 0 155 |
| COMMERCIAL_8 | amount | 8 | 1 | . 343; 0 156; 0.275 2; 0.4 1 |
| INDUSTRIAL_8 | amount | 5 | 1 | . 350; 0 153; 0.455 1; 0.2 1 |
| TRANSPORTATION_8 | category | 2 | 1 | . 353; 0 153 |
| DIRECT_CONNECTED_8 | amount | 8 | 1 | . 349; 0 151; 0.076 1; 0.65 1 |
| TOTAL_8 | amount | 15 | 1 | 0 449; . 43; 0.275 2; 0.076 1 |
| RESIDENTIAL_9 | amount | 8 | 1 | . 342; 0 158; 0.613 1; 0.007 1 |
| COMMERCIAL_9 | amount | 30 | 1 | . 325; 0 149; 0.999 5; 0.758 1 |
| INDUSTRIAL_9 | amount | 12 | 1 | . 340; 0 156; 0.315 1; 0.325 1 |
| TRANSPORTATION_9 | category | 2 | 1 | . 349; 0 157 |
| DIRECT_CONNECTED_9 | category | 4 | 1 | . 348; 0 156; 0.85 1; 0.269 1 |
| TOTAL_9 | amount | 36 | 1 | 0 425; . 43; 0.999 5; 0.315 1 |
| RESIDENTIAL_10 | amount | 222 | 1 | 0 193; . 14; 0.02 7; 0.009 6 |
| COMMERCIAL_10 | amount | 340 | 1 | 0 114; . 13; 0.05 7; 0.8 3 |
| INDUSTRIAL_10 | amount | 90 | 1 | 0 384; . 31; 0.315 1; 0.421 1 |
| TRANSPORTATION_10 | category | 2 | 1 | 0 463; . 43 |
| DIRECT_CONNECTED_10 | amount | 101 | 1 | 0 375; . 21; 0.5 5; 0.8 3 |
| TOTAL_10 | amount | 445 | 1 | 0.8 6; 0.074 5; 0.1 5; 0.006 4 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:39:28.59933 507 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 2667b6ca-9c67-4477-bc96-2 507 |
| _SRC_FILE | who | 1 | 0 | Non_Net_Metering_Distribu 507 |
