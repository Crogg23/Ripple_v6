# PORTAL_CKA_VIRGINIA_OPEN_DA_4E05A500E2

rows 1.9K  columns 11  scan 3.8s

roles: amount 1, audit 2, category 4, date 2, other 1, who 2

## when

REPORT_DATE
  2026      1.9K  ##############################

INGESTED_AT
  2026      1.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| IMMUNIZATION_RATE | 1.8K | 0 | 67.15 | 95 | 95 | 113.2K |

## who

LOCALITY_NAME by rows
       143  All
        13  Fluvanna
        13  Washington
        13  Appomattox
        13  Chesterfield
        13  Lunenburg
        13  Galax
        13  Roanoke
        13  Bland
        13  Charlotte
        13  Virginia Beach
        13  Craig
        13  Frederick
        13  Fredericksburg
        13  Hampton
        13  Rockbridge
        13  Emporia
        13  Brunswick
        13  Waynesboro
        13  Spotsylvania

LOCALITY_NAME by dollars
        5.4K      143 rows  All
        1.1K       13 rows  Manassas Park
        1.1K       13 rows  Alexandria
        1.1K       13 rows  Loudoun
        1.1K       13 rows  Arlington
        1.0K       13 rows  Fairfax County
        1.0K       13 rows  Richmond County
        1.0K       13 rows  Henrico
        1.0K       13 rows  Roanoke County
        1.0K       13 rows  Falls Church
        1.0K       13 rows  Prince William
        1.0K       13 rows  Roanoke
        1.0K       13 rows  Manassas
      987.10       13 rows  Botetourt
      979.70       13 rows  Norton
      976.80       13 rows  Smyth
      976.20       13 rows  Pulaski
      964.60       13 rows  Powhatan
      964.20       13 rows  Hanover
      963.40       13 rows  New Kent

SRC_SHA256 by rows
      1.9K  e09d76e4af39a3c954214f41756b59e478772148f03735fdfda5fd0be52431b2

SRC_SHA256 by dollars
      113.2K     1.9K rows  e09d76e4af39a3c954214f41756b59e478772148f03735fdfda5fd0be524

## who x when

LOCALITY_NAME by REPORT_DATE, dollars = IMMUNIZATION_RATE
  Alexandria                                2026:1.1K
  All                                       2026:5.4K
  Appomattox                                2026:773
  Arlington                                 2026:1.1K
  Bland                                     2026:738.30
  Brunswick                                 2026:792.70
  Charlotte                                 2026:840.60
  Chesterfield                              2026:961.20
  Craig                                     2026:805.50
  Emporia                                   2026:719.50
  Fairfax County                            2026:1.0K
  Falls Church                              2026:1.0K
  Fluvanna                                  2026:934.30
  Frederick                                 2026:847.70
  Fredericksburg                            2026:600.20
  Galax                                     2026:767.60
  Hampton                                   2026:828
  Henrico                                   2026:1.0K
  Loudoun                                   2026:1.1K
  Lunenburg                                 2026:894
  Manassas Park                             2026:1.1K
  Prince William                            2026:1.0K
  Richmond County                           2026:1.0K
  Roanoke                                   2026:1.0K
  Roanoke County                            2026:1.0K
  Rockbridge                                2026:801.90
  Spotsylvania                              2026:802.70
  Virginia Beach                            2026:925.10
  Washington                                2026:646.90
  Waynesboro                                2026:921.60

SRC_SHA256 by REPORT_DATE, dollars = IMMUNIZATION_RATE
  e09d76e4af39a3c954214f41756b59e478772148  2026:113.2K

## what

VACCINATION_TYPE: Men ACWY 31%, HPV 31%, Tdap 23%, Men B 15%

DEMOGRAPHICS_TYPE: Race and Ethnicity 70%, Sex 30%

DEMOGRAPHICS_VARIABLE: Not Reported 20%, Female 10%, Asian or Pacific Islander 10%, Male 10%, White 10%, Latino 10%, Other Race 10%, Native American 10%, Black 10%

AGE_GROUP: 15 year olds at least one dose 15%, 13 year olds at least one dose 15%, 18 year olds at least one dose 15%, 18 year olds series complete 15%, 18 year olds 8%, 15 year olds 8%, 18 year olds a series complete 8%, 18 year olds a series complete 8%, 13 year olds 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 1 | 0 | 2026-06-22 1.9K |
| VACCINATION_TYPE | category | 4 | 0 | Men ACWY 580; HPV 580; Tdap 435; Men B 287 |
| LOCALITY_NAME | who | 133 | 0 | All 143; Galax 13; Poquoson 13; York 13 |
| DEMOGRAPHICS_TYPE | category | 3 | 1.8K | Race and Ethnicity 91; Sex 39 |
| DEMOGRAPHICS_VARIABLE | category | 10 | 1.8K | Not Reported 26; Female 13; Asian or Pacific Islander 13; Male 13 |
| AGE_GROUP | category | 9 | 0 | 15 year olds at least one 290; 13 year olds at least one 290; 18 year olds at least one 289; 18 year olds series compl 288 |
| IMMUNIZATION_COUNT | other | 66 | 1.8K | 50 2; 10827 1; 10270 1; 99 1 |
| IMMUNIZATION_RATE | amount | 711 | 52 | 95.0 168; 0.0 38; 66.7 14; 94.2 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:27:00.96533 1.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4b30b90e-bbb5-4d7c-9a19-5 1.9K |
| SRC_SHA256 | who | 1 | 0 | e09d76e4af39a3c954214f417 1.9K |
