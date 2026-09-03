# PORTAL_CKA_VIRGINIA_OPEN_DA_68AFE3AE03

rows 7.8K  columns 15  scan 3.8s

roles: amount 1, audit 2, category 3, date 2, other 5, who 3

## when

REPORT_DATE
  2024      2.3K  #####################
  2025      2.3K  #####################
  2026      3.2K  ##############################

INGESTED_AT
  2026      7.8K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| COVID_VACCINE_RATE | 5.5K | 0 | 0 | 0.50 | 4 | 209.79 |

## who

LOCALITY_NAME by rows
        60  Fairfax
        60  Henrico
        60  Suffolk
        60  Richmond City
        60  Spotsylvania
        59  Goochland
        59  Hampton
        59  Augusta
        59  Newport News
        59  Loudoun
        59  Bedford
        59  Not Reported
        59  Out-of-State
        59  Chesterfield
        59  Roanoke County
        58  York
        58  Floyd
        58  Fairfax City
        58  Harrisonburg
        58  Campbell

LOCALITY_NAME by dollars
        7.47       58 rows  Falls Church
        5.64       58 rows  Alexandria
        5.21       60 rows  Fairfax
        5.16       58 rows  Arlington
        4.59       58 rows  Charlottesville
        4.44       56 rows  Bath
        3.98       58 rows  Albemarle
        3.93       58 rows  Fairfax City
        3.47       59 rows  Loudoun
        3.34       57 rows  Lexington
        3.23       59 rows  Goochland
        2.69       58 rows  Madison
        2.66       58 rows  Fluvanna
        2.43       60 rows  Henrico
        2.36       58 rows  Hanover
        2.35       58 rows  Williamsburg
        2.34       55 rows  Norton
        2.33       58 rows  Prince William
        2.24       58 rows  James City
        2.17       58 rows  Manassas City

FIPS by rows
        60  51760
        60  51087
        60  51800
        60  51177
        60  51059
        59  51075
        59  51041
        59  51650
        59  51107
        59  51700
        59  51161
        59  51015
        59  Not Reported
        59  Out-of-State
        59  51019
        58  51005
        58  51033
        58  51550
        58  51089
        58  51085

FIPS by dollars
        7.47       58 rows  51610
        5.64       58 rows  51510
        5.21       60 rows  51059
        5.16       58 rows  51013
        4.59       58 rows  51540
        4.44       56 rows  51017
        3.98       58 rows  51003
        3.93       58 rows  51600
        3.47       59 rows  51107
        3.34       57 rows  51678
        3.23       59 rows  51075
        2.69       58 rows  51113
        2.66       58 rows  51065
        2.43       60 rows  51087
        2.36       58 rows  51085
        2.35       58 rows  51830
        2.34       55 rows  51720
        2.33       58 rows  51153
        2.24       58 rows  51095
        2.17       58 rows  51683

SRC_SHA256 by rows
      7.8K  2cd689f77fd58cf93f97b0e309f1c2d7ffb775473e2031df533d7070296b78e4

SRC_SHA256 by dollars
      209.79     7.8K rows  2cd689f77fd58cf93f97b0e309f1c2d7ffb775473e2031df533d7070296b

## who x when

LOCALITY_NAME by REPORT_DATE, dollars = COVID_VACCINE_RATE
  Albemarle                                 2024:17 2025:3.98 2026:0
  Alexandria                                2024:17 2025:5.64 2026:0
  Arlington                                 2024:17 2025:5.16 2026:0
  Augusta                                   2024:17 2025:1.30 2026:0
  Bath                                      2024:15 2025:4.44 2026:0
  Bedford                                   2024:17 2025:1.12 2026:0
  Campbell                                  2024:17 2025:0.72 2026:0
  Charlottesville                           2024:17 2025:4.59 2026:0
  Chesterfield                              2024:17 2025:2.14 2026:0
  Fairfax                                   2024:17 2025:5.21 2026:0
  Fairfax City                              2024:17 2025:3.93 2026:0
  Falls Church                              2024:17 2025:7.47 2026:0
  Floyd                                     2024:17 2025:1.88 2026:0
  Fluvanna                                  2024:17 2025:2.66 2026:0
  Goochland                                 2024:17 2025:3.23 2026:0
  Hampton                                   2024:17 2025:1.34 2026:0
  Hanover                                   2024:17 2025:2.36 2026:0
  Harrisonburg                              2024:17 2025:1.50 2026:0
  Henrico                                   2024:17 2025:2.43 2026:0
  Lexington                                 2024:17 2025:3.34 2026:0
  Loudoun                                   2024:17 2025:3.47 2026:0
  Madison                                   2024:17 2025:2.69 2026:0
  Newport News                              2024:17 2025:1.30 2026:0
  Not Reported                              2024:17 2025:0 2026:0
  Out-of-State                              2024:17 2025:0 2026:0
  Richmond City                             2024:17 2025:2.15 2026:0
  Roanoke County                            2024:17 2025:2.02 2026:0
  Spotsylvania                              2024:17 2025:1.41 2026:0
  Suffolk                                   2024:17 2025:1.33 2026:0
  York                                      2024:17 2025:1.82 2026:0

FIPS by REPORT_DATE, dollars = COVID_VACCINE_RATE
  51003                                     2024:17 2025:3.98 2026:0
  51005                                     2024:17 2025:1.42 2026:0
  51013                                     2024:17 2025:5.16 2026:0
  51015                                     2024:17 2025:1.30 2026:0
  51017                                     2024:15 2025:4.44 2026:0
  51019                                     2024:17 2025:1.12 2026:0
  51033                                     2024:17 2025:1.08 2026:0
  51041                                     2024:17 2025:2.14 2026:0
  51059                                     2024:17 2025:5.21 2026:0
  51065                                     2024:17 2025:2.66 2026:0
  51075                                     2024:17 2025:3.23 2026:0
  51085                                     2024:17 2025:2.36 2026:0
  51087                                     2024:17 2025:2.43 2026:0
  51089                                     2024:17 2025:0.80 2026:0
  51107                                     2024:17 2025:3.47 2026:0
  51113                                     2024:17 2025:2.69 2026:0
  51161                                     2024:17 2025:2.02 2026:0
  51177                                     2024:17 2025:1.41 2026:0
  51510                                     2024:17 2025:5.64 2026:0
  51540                                     2024:17 2025:4.59 2026:0
  51550                                     2024:17 2025:1.37 2026:0
  51600                                     2024:17 2025:3.93 2026:0
  51610                                     2024:17 2025:7.47 2026:0
  51650                                     2024:17 2025:1.34 2026:0
  51678                                     2024:17 2025:3.34 2026:0
  51700                                     2024:17 2025:1.30 2026:0
  51760                                     2024:17 2025:2.15 2026:0
  51800                                     2024:17 2025:1.33 2026:0
  Not Reported                              2024:17 2025:0 2026:0
  Out-of-State                              2024:17 2025:0 2026:0

## what

INDICATOR: Age_Group 42%, Race and Ethnicity 42%, Sex 17%

SUB_INDICATOR: Female 12%, Male 12%, Not Reported 11%, Asian or Pacific Islander 7%, 65+ 7%, Black 7%, 5-11 7%, 50-64 7%, 31-49 7%, 18-30 7%, 12-17 7%, 0-4 7%

VACCINE_RESPIRATORY_SEASON: 2025-26 42%, 2024-25 29%, 2023-24 29%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 3 | 0 | 2026-06-22 3.2K; 2025-10-07 2.3K; 2024-09-10 2.3K |
| FIPS | who | 136 | 0 | 51800 60; 51087 60; 51760 60; 51177 60 |
| LOCALITY_NAME | who | 133 | 0 | Suffolk 60; Henrico 60; Richmond City 60; Spotsylvania 60 |
| INDICATOR | category | 3 | 0 | Age_Group 3.2K; Race and Ethnicity 3.2K; Sex 1.3K |
| SUB_INDICATOR | category | 19 | 0 | Female 675; Male 675; Not Reported 625; Asian or Pacific Islander 405 |
| COVID_VACCINE_COUNT | other | 1.9K | 0 | 0 3.1K; 1 109; 3 94; 2 93 |
| COVID_19_PEOPLE_COUNT | other | 1.8K | 0 | 0 3.1K; 1 114; 2 106; 3 89 |
| FLU_VACCINE_COUNT | other | 2.8K | 0 | 0 2.9K; 1 72; 2 45; 3 34 |
| FLU_PEOPLE_COUNT | other | 2.8K | 0 | 0 2.9K; 1 74; 2 44; 3 35 |
| COVID_VACCINE_RATE | amount | 763 | 271 | 0 3.7K; 0.001 83; 0.002 35; 0.007 30 |
| FLU_VACCINE_RATE | other | 1.2K | 271 | 0 3.6K; 26.8% 23; 22.4% 22; 0.009 22 |
| VACCINE_RESPIRATORY_SEASON | category | 3 | 0 | 2025-26 3.2K; 2024-25 2.3K; 2023-24 2.3K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:19:33.64278 7.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | f870248c-ff6f-4a4e-932b-2 7.8K |
| SRC_SHA256 | who | 1 | 0 | 2cd689f77fd58cf93f97b0e30 7.8K |
