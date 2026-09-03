# PORTAL_CKA_OPEN_DATA_SA_6B3408D74F

rows 9.5K  columns 12  scan 4.1s

roles: amount 1, audit 2, category 4, date 3, other 1, who 2

## when

REPORT_DATE
  2023      2.4K  #######################
  2024      2.9K  ############################
  2025      3.1K  ##############################
  2026      1.0K  ##########

DATETIME
  2026      9.5K  ##############################

INGESTED_AT
  2026      9.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERSON | 9.5K | 16.23B | 16.27B | 68.41B | 71.08B | 241573.79B |

## who

OFFENSE by rows
      3.2K  Wanted Person
       419  Public Intoxication MC
       322  Criminal Trespass Into Private Property MB
       304  Poss Marij - 0 To < 2 Oz MB
       292  Possession Of Drug Paraphernalia MC
       263  Poss Cs Pg 1 - 0 To < 1 Gram (Other Narcotic) FS
       194  Evade Arrest/Detention MA
       179  Poss Cs Pg 1 - 1 To < 4 Grams (Other Narcotic) F3
       174  Poss Cs Pg 1 - 0 To < 1 Gram (Opium/Cocaine) FS
       148  Resisting Arrest-Search-Transportation MA
       118  Assault-Bi-Family/Household MA
       111  Assault Causes Bodily Injury Family Member (Married/Cohab) MA
       106  Traffic Violation
       100  Assault-Bi-Married/Cohab MA
       100  Aggravated Assault W/ Deadly Weapon F2
        98  Unlawful Carrying Weapon MA
        86  Assault Bodily Injury MA
        86  Unlawful Carrying Weapon-Handgun-Motor Vehicle MA
        83  Unauthorized Use Vehicle FS
        74  Poss Cs Pg 1 - 1 To < 4 Grams (Opium/Cocaine) F3

OFFENSE by dollars
   73156.11B     3.2K rows  Wanted Person
   11385.10B      419 rows  Public Intoxication MC
    8143.44B      304 rows  Poss Marij - 0 To < 2 Oz MB
    7723.79B      322 rows  Criminal Trespass Into Private Property MB
    7102.09B      292 rows  Possession Of Drug Paraphernalia MC
    6263.41B      263 rows  Poss Cs Pg 1 - 0 To < 1 Gram (Other Narcotic) FS
    5382.28B      194 rows  Evade Arrest/Detention MA
    4365.29B      174 rows  Poss Cs Pg 1 - 0 To < 1 Gram (Opium/Cocaine) FS
    4247.61B      179 rows  Poss Cs Pg 1 - 1 To < 4 Grams (Other Narcotic) F3
    3949.04B      148 rows  Resisting Arrest-Search-Transportation MA
    3818.63B      111 rows  Assault Causes Bodily Injury Family Member (Married/Cohab) M
    3664.26B      118 rows  Assault-Bi-Family/Household MA
    3145.40B       98 rows  Unlawful Carrying Weapon MA
    3063.63B      100 rows  Aggravated Assault W/ Deadly Weapon F2
    3017.42B      106 rows  Traffic Violation
    2835.35B      100 rows  Assault-Bi-Married/Cohab MA
    2789.13B       86 rows  Unlawful Carrying Weapon-Handgun-Motor Vehicle MA
    2310.48B       86 rows  Assault Bodily Injury MA
    2211.27B       83 rows  Unauthorized Use Vehicle FS
    2139.27B       74 rows  Poss Cs Pg 2 - 0 To < 1 Gram (Other Narcotic) FS

SRC_SHA256 by rows
      9.5K  d038479520315e3c3676cc1fe941ae9d27604b5dda63a81e21e5056914ba1b34

SRC_SHA256 by dollars
  241573.79B     9.5K rows  d038479520315e3c3676cc1fe941ae9d27604b5dda63a81e21e5056914ba

## who x when

OFFENSE by REPORT_DATE, dollars = PERSON
  Aggravated Assault W/ Deadly Weapon F2    2023:649.04B 2024:1553.31B 2025:522.33B 2026:338.95B
  Assault Bodily Injury MA                  2023:390.41B 2024:743.48B 2025:838.88B 2026:337.72B
  Assault Causes Bodily Injury Family Memb  2024:813.27B 2025:2020.87B 2026:984.49B
  Assault-Bi-Family/Household MA            2023:1052.18B 2024:1455.01B 2025:913.30B 2026:243.77B
  Assault-Bi-Married/Cohab MA               2023:1637.22B 2024:1198.13B
  Criminal Trespass Into Private Property   2023:1860.94B 2024:2579.16B 2025:1992.41B 2026:1291.29B
  Evade Arrest/Detention MA                 2023:906.42B 2024:1845.71B 2025:1938.45B 2026:691.70B
  Poss Cs Pg 1 - 0 To < 1 Gram (Opium/Coca  2023:890.13B 2024:1323.32B 2025:1626.20B 2026:525.64B
  Poss Cs Pg 1 - 0 To < 1 Gram (Other Narc  2023:1097.07B 2024:2121.81B 2025:2174.26B 2026:870.27B
  Poss Cs Pg 1 - 1 To < 4 Grams (Opium/Coc  2023:496.69B 2024:671.65B 2025:592.27B 2026:65.02B
  Poss Cs Pg 1 - 1 To < 4 Grams (Other Nar  2023:768.46B 2024:1761.52B 2025:1164.59B 2026:553.04B
  Poss Cs Pg 2 - 0 To < 1 Gram (Other Narc  2023:130.08B 2024:685.15B 2025:934.81B 2026:389.24B
  Poss Marij - 0 To < 2 Oz MB               2023:1699.80B 2024:2763.44B 2025:2862.50B 2026:817.70B
  Possession Of Drug Paraphernalia MC       2023:824.38B 2024:1970.54B 2025:3038.08B 2026:1269.09B
  Public Intoxication MC                    2023:3255.91B 2024:2507.89B 2025:4554.58B 2026:1066.72B
  Resisting Arrest-Search-Transportation M  2023:1123.97B 2024:1047.91B 2025:1326.57B 2026:450.59B
  Traffic Violation                         2023:478.65B 2024:542.28B 2025:1551.43B 2026:445.04B
  Unauthorized Use Vehicle FS               2023:810.30B 2024:833.44B 2025:387.69B 2026:179.84B
  Unlawful Carrying Weapon MA               2023:452.77B 2024:882.87B 2025:1312.77B 2026:496.99B
  Unlawful Carrying Weapon-Handgun-Motor V  2023:980.85B 2024:1229.21B 2025:459.90B 2026:119.17B
  Wanted Person                             2023:16800.76B 2024:21130.54B 2025:26657.23B 2026:8567.57B

SRC_SHA256 by REPORT_DATE, dollars = PERSON
  d038479520315e3c3676cc1fe941ae9d27604b5d  2023:52313.48B 2024:76356.69B 2025:83755.42B 2026:29148.20B

## what

SEVERITY: Misdemeanor (Ladder Crime) 35%, Class A Misdemeanor 15%, Class B Misdemeanor 12%, Class C Misdemeanor 12%, State Jail Felony 10%, 3rd Degree Felony 9%, 2nd Degree Felony 4%, 1st Degree Felony 1%, Misdemeanor 1%, Felony (Ladder Crime) 0%, Felony 0%, Capital Felony 0%

SERVICE_AREA: WEST 42%, EAST 28%, CENTRAL 24%, DOWNTOWN 6%, PRUE 0%, NORTH 0%, SOUTH 0%

REPORT_MONTH: June 10%, March 10%, January 9%, May 9%, April 9%, August 8%, February 8%, December 8%, September 8%, October 8%, November 7%, July 7%

ZIP_CODE: 78201 70%, 78202 30%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_ID | other | 6.4K | 0 | 66122086893 53; 67148979598 51; 67514083038 50; 67397695348 50 |
| REPORT_DATE | date | 1.2K | 0 | 2025-06-03 59; 2025-06-22 58; 2025-09-01 57; 2025-12-07 56 |
| PERSON | amount | 5.7K | 1 | 16279063374.0 53; 16246097922.0 52; 16259145975.0 50; 16250954344.0 50 |
| OFFENSE | who | 410 | 0 | Wanted Person 3.2K; Public Intoxication MC 419; Criminal Trespass Into Pr 322; Poss Marij - 0 To < 2 Oz  304 |
| SEVERITY | category | 12 | 0 | Misdemeanor (Ladder Crime 3.3K; Class A Misdemeanor 1.5K; Class B Misdemeanor 1.2K; Class C Misdemeanor 1.1K |
| SERVICE_AREA | category | 7 | 0 | WEST 4.0K; EAST 2.6K; CENTRAL 2.3K; DOWNTOWN 565 |
| REPORT_MONTH | category | 12 | 0 | June 938; March 918; January 865; May 855 |
| ZIP_CODE | category | 2 | 0 | 78201 6.6K; 78202 2.8K |
| DATETIME | date | 1 | 0 | 2026-07-01 9.5K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:05:28.71985 9.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | b1cd4cea-11e6-49e1-95c3-f 9.5K |
| SRC_SHA256 | who | 1 | 0 | d038479520315e3c3676cc1fe 9.5K |
