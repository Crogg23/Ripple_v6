# FED_EIA861_RELIABILITY

rows 973  columns 31  scan 4.8s

roles: amount 19, audit 2, category 6, date 1, state 1, who 3

## when

_INGESTED_AT
  2026       973  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ALL_EVENTS_WITH_MAJOR_EVENT_DAYS | 971 | 0 | 124.10 | 5.7K | 17.3K | 387.5K |
| UNNAMED_6 | 971 | 0 | 0.96 | 6.15 | 10.41 | 1.2K |
| UNNAMED_7 | 971 | 0 | 100.60 | 1.2K | 3.9K | 144.8K |
| WITHOUT_MAJOR_EVENT_DAYS | 971 | 0 | 67.20 | 906.26 | 17.1K | 123.4K |
| UNNAMED_9 | 971 | 0 | 0.70 | 4.24 | 6.86 | 860.62 |
| UNNAMED_10 | 971 | 0 | 80.25 | 254.17 | 5.3K | 77.6K |

## who

UNNAMED_1 by rows
         6  14354
         4  12199
         4  5860
         3  19545
         3  13781
         3  12341
         3  13758
         3  17698
         3  6169
         3  14232
         3  13314
         2  14289
         2  19876
         2  15293
         2  5027
         2  19157
         2  296
         2  13780
         2  84
         2  10817

UNNAMED_1 by dollars
       17.3K        1 rows  407
       10.3K        1 rows  9689
        9.6K        1 rows  8333
        9.4K        2 rows  5416
        8.3K        1 rows  19161
        8.3K        1 rows  10768
        7.9K        1 rows  162
        7.3K        1 rows  18360
        6.9K        1 rows  20146
        6.0K        1 rows  1889
        5.5K        1 rows  16496
        5.3K        1 rows  1890
        4.6K        1 rows  16613
        4.4K        1 rows  3245
        4.3K        1 rows  8901
        4.2K        1 rows  18454
        3.9K        1 rows  12462
        3.9K        1 rows  16461
        3.7K        1 rows  3843
        3.7K        1 rows  17683

UNNAMED_2 by rows
         6  PacifiCorp
         4  Montana-Dakota Utilities Co
         4  Empire District Electric Co
         3  Black Hills Power, Inc.
         3  Northern States Power Co - Minnesota
         3  MidAmerican Energy Co
         3  Navajo Tribal Utility Authority
         3  Northern Lights, Inc
         3  Fall River Rural Elec Coop Inc
         3  Otter Tail Power Co
         3  Southwestern Electric Power Co
         2  Duke Energy Progress - (NC)
         2  Lea County Electric Coop, Inc - (NM)
         2  Diverse Power Incorporated
         2  Heartland Power Coop
         2  Moon Lake Electric Assn Inc
         2  A & N Electric Coop
         2  Lower Yellowstone R E A, Inc
         2  Arkansas Valley Elec Coop Corp
         2  Okefenoke Rural El Member Corp

UNNAMED_2 by dollars
       17.3K        1 rows  Altamaha Electric Member Corp
       10.3K        1 rows  Jefferson Electric Member Corp
        9.6K        1 rows  Haywood Electric Member Corp
        9.4K        2 rows  Duke Energy Carolinas, LLC
        8.3K        1 rows  Tri-County Electric Coop, Inc (FL)
        8.3K        1 rows  Laurens Electric Coop, Inc
        7.9K        1 rows  Aiken Electric Coop Inc
        7.3K        1 rows  Suwannee Valley Elec Coop Inc
        6.9K        1 rows  Washington Elec Member Corp
        6.0K        1 rows  Blue Ridge Elec Member Corp - (NC)
        5.5K        1 rows  Rutherford Elec Member Corp
        5.3K        1 rows  Blue Ridge Electric Coop Inc - (SC)
        4.6K        1 rows  Sam Houston Electric Coop Inc
        4.4K        1 rows  Central Florida Elec Coop, Inc
        4.3K        1 rows  CenterPoint Energy
        4.2K        1 rows  Tampa Electric Co
        3.9K        1 rows  Mid-Carolina Electric Coop Inc
        3.9K        1 rows  Rusk County Electric Coop, Inc
        3.7K        1 rows  Coastal Electric Member Corp - (GA)
        3.7K        1 rows  Southwest Mississippi E P A

_SRC_FILE by rows
       973  Reliability_2024.xlsx

_SRC_FILE by dollars
      387.5K      973 rows  Reliability_2024.xlsx

## who x when

UNNAMED_1 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = ALL_EVENTS_WITH_MAJOR_EVENT_DAYS
  10768                                     2026:8.3K
  10817                                     2026:0
  12199                                     2026:704.67
  12341                                     2026:999
  13314                                     2026:0
  13758                                     2026:0
  13780                                     2026:374.87
  13781                                     2026:463.41
  14232                                     2026:460.40
  14289                                     2026:507.44
  14354                                     2026:1.6K
  15293                                     2026:1.0K
  162                                       2026:7.9K
  17698                                     2026:3.0K
  18360                                     2026:7.3K
  1889                                      2026:6.0K
  19157                                     2026:170.47
  19161                                     2026:8.3K
  19545                                     2026:118.94
  19876                                     2026:0
  20146                                     2026:6.9K
  296                                       2026:0
  407                                       2026:17.3K
  5027                                      2026:206
  5416                                      2026:9.4K
  5860                                      2026:2.2K
  6169                                      2026:40.94
  8333                                      2026:9.6K
  84                                        2026:0
  9689                                      2026:10.3K

UNNAMED_2 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = ALL_EVENTS_WITH_MAJOR_EVENT_DAYS
  A & N Electric Coop                       2026:0
  Aiken Electric Coop Inc                   2026:7.9K
  Altamaha Electric Member Corp             2026:17.3K
  Arkansas Valley Elec Coop Corp            2026:785.95
  Black Hills Power, Inc.                   2026:118.94
  Blue Ridge Elec Member Corp - (NC)        2026:6.0K
  Diverse Power Incorporated                2026:418.54
  Duke Energy Carolinas, LLC                2026:9.4K
  Duke Energy Progress - (NC)               2026:2.1K
  Empire District Electric Co               2026:2.2K
  Fall River Rural Elec Coop Inc            2026:40.94
  Haywood Electric Member Corp              2026:9.6K
  Heartland Power Coop                      2026:129.94
  Jefferson Electric Member Corp            2026:10.3K
  Laurens Electric Coop, Inc                2026:8.3K
  Lea County Electric Coop, Inc - (NM)      2026:0
  Lower Yellowstone R E A, Inc              2026:0
  MidAmerican Energy Co                     2026:999
  Montana-Dakota Utilities Co               2026:704.67
  Moon Lake Electric Assn Inc               2026:0
  Navajo Tribal Utility Authority           2026:0
  Northern Lights, Inc                      2026:0
  Northern States Power Co - Minnesota      2026:463.41
  Okefenoke Rural El Member Corp            2026:3.5K
  Otter Tail Power Co                       2026:460.40
  PacifiCorp                                2026:1.6K
  Southwestern Electric Power Co            2026:3.0K
  Suwannee Valley Elec Coop Inc             2026:7.3K
  Tri-County Electric Coop, Inc (FL)        2026:8.3K
  Washington Elec Member Corp               2026:6.9K

## where

UNNAMED_3: TX 72, TN 52, NC 44, MN 43, IN 37, WI 37, FL 35, GA 35, MO 34, KY 33, OH 31, OK 28

## what

UNNAMED_0: 2024 100%, CAIDI = SAIDI / SAIFI.
MED- Ma 0%, Data Year 0%

UNNAMED_4: Cooperative 48%, Municipal 30%, Investor Owned 18%, Political Subdivision 4%, State 1%, Retail Power Marketer 0%, Ownership 0%

UNNAMED_16: Y 76%, N 24%, Outages Recorded Automatically 0%

UNNAMED_24: N 86%, Y 13%, Inactive Accounts Included 0%

UNNAMED_25: F 46%, L 40%, O 13%, Momentary Interruptions 0%

UNNAMED_27: Y 55%, N 45%, Outages Recorded Automatically 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | category | 3 | 0 | 2024 971; CAIDI = SAIDI / SAIFI.
ME 1; Data Year 1 |
| UNNAMED_1 | who | 909 | 1 | 14354 8; 19545 7; 40165 6; 31833 6 |
| UNNAMED_2 | who | 901 | 1 | PacifiCorp 8; Black Hills Power, Inc. 7; Dixie Escalante R E A, In 6; Okefenoke Rural El Member 6 |
| UNNAMED_3 | state | 52 | 1 | TX 72; TN 52; NC 44; MN 43 |
| UNNAMED_4 | category | 7 | 1 | Cooperative 467; Municipal 287; Investor Owned 171; Political Subdivision 37 |
| ALL_EVENTS_WITH_MAJOR_EVENT_DAYS | amount | 740 | 1 | . 227; 402.64 4; 212.921 4; 267.47 4 |
| UNNAMED_6 | amount | 573 | 1 | . 261; 0.66 6; 0.88 6; 1.13 5 |
| UNNAMED_7 | amount | 721 | 1 | . 263; 217.52566 4; 130.78686 4; 60.719637 4 |
| WITHOUT_MAJOR_EVENT_DAYS | amount | 732 | 1 | . 242; 220.51 4; 90.16 4; 267.47 4 |
| UNNAMED_9 | amount | 522 | 1 | . 277; 1 7; 0.66 6; 1.13 6 |
| UNNAMED_10 | amount | 702 | 1 | . 279; 148.49158 4; 90.522088 4; 60.719637 4 |
| LOSS_OF_SUPPLY_REMOVED_WITH_MAJOR_EVENT_DAYS | amount | 628 | 1 | . 328; 0 13; 373.01 4; 176.202 4 |
| UNNAMED_12 | amount | 516 | 1 | . 358; 0 13; 1.43 5; 0.85 5 |
| UNNAMED_13 | amount | 609 | 1 | . 371; 235.93295 4; 111.37927 4; 60.719637 4 |
| COL | amount | 745 | 1 | . 224; 2076402 4; 38491 4; 3582 4 |
| UNNAMED_15 | amount | 44 | 1 | . 239; 12.5 151; 25 112; 34.5 74 |
| UNNAMED_16 | category | 3 | 225 | Y 569; N 178; Outages Recorded Automati 1 |
| ALL_EVENTS_WITH_MAJOR_EVENT_DAYS_1 | amount | 224 | 1 | . 750; 936.75 2; 919.23 2; 25.91 2 |
| UNNAMED_18 | amount | 187 | 1 | . 772; 0.1 3; 0.11 3; 0.99 2 |
| UNNAMED_19 | amount | 202 | 1 | . 773; 90.909091 2; 234.24606 1; 190.04135 1 |
| WITHOUT_MAJOR_EVENT_DAYS_1 | amount | 191 | 1 | . 779; 0 5; 81 2; 7.865 2 |
| UNNAMED_21 | amount | 157 | 1 | . 801; 0 5; 1.21 2; 0.29 2 |
| UNNAMED_22 | amount | 168 | 1 | . 806; 25.208333 2; 184.10966 1; 73.770417 1 |
| C_1 | amount | 226 | 1 | . 747; 1207 2; 26996 2; 15018 2 |
| UNNAMED_24 | category | 3 | 746 | N 196; Y 30; Inactive Accounts Include 1 |
| UNNAMED_25 | category | 4 | 746 | F 105; L 91; O 30; Momentary Interruptions 1 |
| UNNAMED_26 | amount | 28 | 1 | . 752; 12.5 47; 25 36; 24.9 25 |
| UNNAMED_27 | category | 3 | 747 | Y 124; N 101; Outages Recorded Automati 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:39:36.49836 973 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 40d28df2-2c1e-4d4e-bd9a-d 973 |
| _SRC_FILE | who | 1 | 0 | Reliability_2024.xlsx 973 |
