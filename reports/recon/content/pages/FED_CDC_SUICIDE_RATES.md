# FED_CDC_SUICIDE_RATES

rows 6.4K  columns 16  scan 3.4s

roles: amount 1, audit 2, category 9, other 1, who 3

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ESTIMATE | 5.5K | 0.30 | 10.50 | 56.17 | 74.80 | 75.2K |

## who

STUB_LABEL by rows
        87  Female: Black or African American
        86  Female: Not Hispanic or Latino: Black or African American
        86  Male: Not Hispanic or Latino: Black or African American
        86  Male: Hispanic or Latino: All races
        86  Male: Not Hispanic or Latino: White
        86  Female: American Indian or Alaska Native
        86  Female: White
        86  Male: White
        86  Female: Not Hispanic or Latino: White
        86  Male: American Indian or Alaska Native
        86  Female: Hispanic or Latino: All races
        85  Male: Black or African American
        84  Female
        84  All persons
        84  Male: Asian or Pacific Islander
        84  Male
        84  Female: Asian or Pacific Islander
        45  Female: Black or African American: 65 years and over
        45  Male: Black or African American: 65 years and over
        45  Female: Black or African American: 45-64 years

STUB_LABEL by dollars
        2.5K       43 rows  Male: White: 85 years and over
        2.3K       42 rows  Male: 85 years and over
        2.0K       43 rows  Male: White: 75-84 years
        1.9K       86 rows  Male: White
        1.8K       42 rows  Male: 75-84 years
        1.7K       84 rows  Male
        1.6K       86 rows  Male: Not Hispanic or Latino: White
        1.6K       43 rows  Male: White: 65 years and over
        1.5K       42 rows  Male: 65 years and over
        1.3K       86 rows  Male: American Indian or Alaska Native
        1.3K       43 rows  Male: White: 65-74 years
        1.3K       43 rows  Male: Not Hispanic or Latino: White: 65 years and over
        1.2K       43 rows  Male: White: 45-64 years
        1.2K       42 rows  Male: 65-74 years
        1.1K       43 rows  Male: American Indian or Alaska Native: 15-24 years
        1.1K       42 rows  Male: Not Hispanic or Latino: American Indian or Alaska Nati
        1.1K       42 rows  Male: 55-64 years
        1.1K       43 rows  Male: White: 25-44 years
        1.1K       42 rows  Male: 45-64 years
        1.1K       42 rows  Male: 45-54 years

INDICATOR by rows
      6.4K  Death rates for suicide

INDICATOR by dollars
       75.2K     6.4K rows  Death rates for suicide

SRC_SHA256 by rows
      6.4K  7162644976d80876501684e7451f06d5596447db242a7a21b07b504244717c9b

SRC_SHA256 by dollars
       75.2K     6.4K rows  7162644976d80876501684e7451f06d5596447db242a7a21b07b50424471

## what

UNIT: Deaths per 100,000 resident po 87%, Deaths per 100,000 resident po 13%

UNIT_NUM: 2 87%, 1 13%

STUB_NAME: Sex, age and race 25%, Sex, age and race and Hispanic 21%, Sex and age 18%, Sex and race 11%, Sex and race and Hispanic orig 10%, Age 9%, Sex 3%, Total 1%, Sex, age and race and Hispanic 1%, Sex, age and race (Single race 0%, Sex and race and Hispanic orig 0%, Sex and race (Single race) 0%

STUB_NAME_NUM: 5 25%, 7 21%, 3 18%, 4 11%, 6 10%, 1 9%, 2 3%, 0 1%, 11 1%, 9 0%, 10 0%, 8 0%

YEAR: 2018 13%, 2017 8%, 2016 8%, 2015 8%, 2014 8%, 2013 8%, 2012 8%, 2011 8%, 2010 8%, 2009 8%, 2008 8%, 2007 8%

YEAR_NUM: 42 13%, 41 8%, 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%

AGE: All ages 27%, 65 years and over 14%, 45-64 years 14%, 25-44 years 14%, 15-24 years 14%, 85 years and over 4%, 75-84 years 4%, 65-74 years 4%, 55-64 years 2%, 45-54 years 2%, 35-44 years 2%, 25-34 years 2%

AGE_NUM: 0 27%, 5 14%, 4 14%, 3 14%, 2 14%, 6 4%, 5.2 4%, 5.1 4%, 4.2 2%, 4.1 2%, 3.2 2%, 3.1 2%

FLAG: ... 71%, * 29%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDICATOR | who | 1 | 0 | Death rates for suicide 6.4K |
| UNIT | category | 2 | 0 | Deaths per 100,000 reside 5.6K; Deaths per 100,000 reside 812 |
| UNIT_NUM | category | 2 | 0 | 2 5.6K; 1 812 |
| STUB_NAME | category | 12 | 0 | Sex, age and race 1.6K; Sex, age and race and His 1.3K; Sex and age 1.2K; Sex and race 672 |
| STUB_NAME_NUM | category | 12 | 0 | 5 1.6K; 7 1.3K; 3 1.2K; 4 672 |
| STUB_LABEL | who | 163 | 0 | Female: Black or African  87; Female: Hispanic or Latin 86; Female: Not Hispanic or L 86; Female: Not Hispanic or L 86 |
| STUB_LABEL_NUM | other | 158 | 0 | 4.22 87; 6.23 86; 6.22 86; 6.21 86 |
| YEAR | category | 42 | 0 | 2018 276; 2017 162; 2016 162; 2015 162 |
| YEAR_NUM | category | 42 | 0 | 42 276; 41 162; 40 162; 39 162 |
| AGE | category | 15 | 0 | All ages 1.6K; 65 years and over 812; 45-64 years 812; 25-44 years 812 |
| AGE_NUM | category | 15 | 0 | 0 1.6K; 5 812; 4 812; 3 812 |
| ESTIMATE | amount | 521 | 906 | 4.3 54; 4.2 52; 2.1 50; 3.8 49 |
| FLAG | category | 3 | 5.5K | ... 645; * 261 |
| INGESTED_AT | audit | 1 | 0 | 1782620731620901 6.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | a4f6d697-317b-4188-a8cd-b 6.4K |
| SRC_SHA256 | who | 1 | 0 | 7162644976d80876501684e74 6.4K |
