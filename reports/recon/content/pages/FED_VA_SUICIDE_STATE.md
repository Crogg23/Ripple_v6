# FED_VA_SUICIDE_STATE

rows 19.7K  columns 19  scan 3.3s

roles: amount 3, audit 2, category 8, other 4, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VETERAN_SUICIDE_RATE_PER_100_000 | 5.1K | 9.10 | 30.40 | 65.90 | 133.30 | 163.2K |
| GENERAL_POPULATION_RATE_PER_100_000 | 6.0K | 5.20 | 17.70 | 37.76 | 61.60 | 110.3K |
| GROUP_PERCENTAGE | 8.5K | 2.40 | 19.80 | 100 | 100 | 255.1K |

## who

STATE by rows
       736  Region Total
       460  All
       391  Florida
       391  California
       391  U.S. Total
       390  Texas
       390  New York
       389  Illinois
       389  Pennsylvania
       387  Ohio
       385  Washington
       379  Michigan
       377  Virginia
       373  Wisconsin
       373  Arizona
       372  Colorado
       372  North Carolina
       372  Georgia
       371  Oregon
       371  Massachusetts

STATE by dollars
       18.4K      736 rows  Region Total
        4.6K      377 rows  Virginia
        4.6K      365 rows  Kentucky
        4.6K      391 rows  U.S. Total
        4.6K      389 rows  Illinois
        4.6K      372 rows  Colorado
        4.6K      303 rows  North Dakota
        4.6K      379 rows  Michigan
        4.6K      391 rows  California
        4.6K      339 rows  Maine
        4.6K      370 rows  Tennessee
        4.6K      389 rows  Pennsylvania
        4.6K      351 rows  Arkansas
        4.6K      368 rows  Maryland
        4.6K      369 rows  Indiana
        4.6K      391 rows  Florida
        4.6K      301 rows  Wyoming
        4.6K      352 rows  New Mexico
        4.6K      339 rows  Mississippi
        4.6K      371 rows  Missouri

_SRC_SHA256 by rows
     19.7K  b0529f40b70ffeca861dd0a62e365ec29b74ff1f3ddf13f48a1d982f3f482df1

_SRC_SHA256 by dollars
      255.1K    19.7K rows  b0529f40b70ffeca861dd0a62e365ec29b74ff1f3ddf13f48a1d982f3f48

## what

YEAR_OF_DEATH: 2023 9%, 2022 9%, 2021 9%, 2020 9%, 2019 9%, 2018 9%, 2017 9%, 2016 9%, 2015 9%, 2014 9%, 2013 9%

GEOGRAPHIC_REGION: Southern 32%, Western 25%, Midwestern 23%, Northeastern 18%, All 2%

SHEET: Suicides by Method 43%, Suicides by Age 33%, Veteran Suicides by Sex 18%, Veteran Suicides by State 6%

SEX: All 33%, Female 33%, Male 33%

YEAR: 2019 9%, 2013 9%, 2016 9%, 2015 9%, 2011 9%, 2017 9%, 2014 9%, 2012 9%, 2008 9%, 2007 9%, 2023 9%

AGE_GROUP: All 20%, 75+ 20%, 55-74 20%, 35-54 20%, 18-34 20%

GROUP_METHOD: General Population Method 59%, Veteran Method 41%

METHOD: Firearms 28%, Suffocation 23%, Poisoning 19%, Other suicide 17%, Other and low-count methods 13%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR_OF_DEATH | category | 24 | 14.9K | 2023 208; 2022 208; 2021 208; 2020 208 |
| GEOGRAPHIC_REGION | category | 5 | 0 | Southern 6.4K; Western 4.9K; Midwestern 4.6K; Northeastern 3.5K |
| STATE | who | 53 | 0 | Region Total 736; All 460; California 391; Florida 391 |
| VETERAN_SUICIDES | other | 759 | 8.5K | <10 2.4K; 10-19 292; 20-29 143; 21 142 |
| POPULATION_ESTIMATE | other | 669 | 18.5K | 121000 11; 71000 10; 75000 10; 44000 9 |
| VETERAN_SUICIDE_RATE_PER_100_000 | amount | 848 | 12.1K | -- 1.5K; 25 42; 33.3 41; 26.3 37 |
| SHEET | category | 4 | 0 | Suicides by Method 8.5K; Suicides by Age 6.4K; Veteran Suicides by Sex 3.6K; Veteran Suicides by State 1.2K |
| SEX | category | 4 | 16.1K | All 1.2K; Female 1.2K; Male 1.2K |
| YEAR | category | 24 | 4.8K | 2019 653; 2013 653; 2016 652; 2015 652 |
| AGE_GROUP | category | 6 | 13.3K | All 1.3K; 75+ 1.3K; 55-74 1.3K; 35-54 1.3K |
| GENERAL_POPULATION_SUICIDES | other | 1.6K | 13.3K | <10 159; 20-29 51; 10-19 45; 36 40 |
| GENERAL_POPULATION_RATE_PER_100_000 | amount | 500 | 13.3K | -- 279; 18.8 64; 17.2 58; 18.9 56 |
| GROUP_METHOD | category | 3 | 11.2K | General Population Method 5.0K; Veteran Method 3.5K |
| METHOD | category | 6 | 11.2K | Firearms 2.3K; Suffocation 1.9K; Poisoning 1.6K; Other suicide 1.5K |
| SUICIDES | other | 1.3K | 11.2K | 11 167; 19 163; 14 150; 13 144 |
| GROUP_PERCENTAGE | amount | 791 | 11.2K | 100 190; 16.7 50; 17.5 48; 6.5 47 |
| _INGESTED_AT | audit | 1 | 0 | 1786325075964258 19.7K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 963a7632-a391-4a33-8345-a 19.7K |
| _SRC_SHA256 | who | 1 | 0 | b0529f40b70ffeca861dd0a62 19.7K |
