# PORTAL_SOC_AUSTIN_OPEN_DATA_B5E56C7A67

rows 51  columns 29  scan 3.0s

roles: amount 3, audit 2, category 19, date 1, other 4, who 1

## when

INGESTED_AT
  2026        51  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_EARNINGS | 51 | 120.6K | 15.56M | 1.03B | 1.73B | 3.47B |
| CHANGE_OF_EARNINGS_PER_JOB | 50 | -0.28 | 0.03 | 0.71 | 0.86 | 2.63 |
| NATIONAL_LQ_2016 | 50 | 0.09 | 1.14 | 3.19 | 3.20 | 60.30 |

## who

SRC_SHA256 by rows
        51  fac4c95c19d88a73db9f6f4f24e7265d99858ea5be763ca24ca74ae6afc8a614

SRC_SHA256 by dollars
       3.47B       51 rows  fac4c95c19d88a73db9f6f4f24e7265d99858ea5be763ca24ca74ae6afc8

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_EARNINGS
  fac4c95c19d88a73db9f6f4f24e7265d99858ea5  2026:3.47B

## what

CAD_DEFINED_SECTOR: Visual Arts & Design 27%, Printing, Publishing,  and Rel 20%, Film, TV, Radio 16%, Music 14%, Advertising, Public Relations, 8%, Performing Arts 6%, Museums, Libraries, and Arts E 6%, nan 2%, Independent artists, writers,  2%

SALES_2016: 5522995378 8%, 4155624 8%, 41739467 8%, 103708138 8%, 169118400 8%, 46766007 8%, 33359545 8%, 85790519 8%, 133627605 8%, 6774058 8%, 31619888 8%, 25796400 8%

JOBS_2016: 68 15%, 46828 8%, 109 8%, 673 8%, 2319 8%, 2280 8%, 502 8%, 560 8%, 746 8%, 419 8%, 31 8%, 220 8%

EARNINGS_PER_JOB_2015: 2026045 8%, 23112 8%, 28507 8%, 20166 8%, 31752 8%, 31375 8%, 19454 8%, 42652 8%, 82458 8%, 42208 8%, 45450 8%, 35991 8%

BLACK_OR_AFRICAN_AMERICAN: 4 12%, 5 12%, 2 12%, 12 12%, 31 8%, 13 8%, 10 8%, 0 8%, 7 8%, 1 8%, 3351 4%, 23 4%

AMER_INDIAN_OR_AK_NATIVE: 0 41%, 1 31%, 2 6%, 4 4%, 3 4%, 5 4%, 107 2%, 17 2%, 31 2%, 6 2%, 8 2%

ASIAN: 1 17%, 0 17%, 7 11%, 9 9%, 24 9%, 21 6%, 11 6%, 8 6%, 17 6%, 3 6%, 2 6%, 1240 3%

HAWAIIAN_OR_OTHER_PAC_ISLAND: 0 75%, 1 18%, 2 6%, 14 2%

HISPANIC_OR_LATINO: 113 12%, 6 12%, 7 12%, 3 12%, 8593 6%, 27 6%, 205 6%, 686 6%, 416 6%, 136 6%, 251 6%, 102 6%

TWO_OR_MORE_RACES: 0 26%, 4 16%, 1 11%, 6 11%, 5 8%, 14 8%, 19 5%, 2 5%, 1009 3%, 65 3%, 10 3%, 11 3%

MALE: 469 15%, 26122 8%, 22 8%, 276 8%, 949 8%, 957 8%, 281 8%, 337 8%, 501 8%, 264 8%, 19 8%, 141 8%

FEMALE: 22 15%, 20730 8%, 87 8%, 398 8%, 1370 8%, 1323 8%, 221 8%, 224 8%, 245 8%, 155 8%, 12 8%, 79 8%

C_0_24_AGE: 1 14%, 6 14%, 3 14%, 19 9%, 21 9%, 0 9%, 2 9%, 4604 5%, 7 5%, 38 5%, 143 5%, 126 5%

C_25_34_AGE: 15 12%, 167 12%, 76 12%, 22 12%, 11398 6%, 578 6%, 421 6%, 166 6%, 151 6%, 89 6%, 2 6%, 77 6%

C_35_44_AGE: 88 13%, 189 13%, 38 13%, 11198 7%, 24 7%, 163 7%, 557 7%, 523 7%, 95 7%, 80 7%, 96 7%, 8 7%

C_45_54_AGE: 38 15%, 9192 8%, 35 8%, 149 8%, 503 8%, 656 8%, 73 8%, 145 8%, 138 8%, 88 8%, 5 8%, 41 8%

C_55_64_AGE: 1 14%, 13 14%, 74 10%, 52 10%, 16 10%, 103 10%, 8 10%, 6788 5%, 26 5%, 117 5%, 396 5%, 338 5%

C_65_99_AGE: 2 14%, 0 14%, 44 10%, 1 10%, 6 10%, 4 10%, 14 10%, 3674 5%, 40 5%, 142 5%, 216 5%, 45 5%

EARNINGS_BY_SECTOR: nan 82%, 1733500175 2%, 325594895 2%, 247783148 2%, 29889694 2%, 74276596 2%, 37773611 2%, 336122737 2%, 342215722 2%, 339843772 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAICS_CODE | other | 51 | 0 | Total 1; 812921 1; 541922 1; 541921 1 |
| CAD_DEFINED_SECTOR | category | 9 | 0 | Visual Arts & Design 14; Printing, Publishing,  an 10; Film, TV, Radio 8; Music 7 |
| INDUSTRY | other | 51 | 0 | nan 1; Photofinishing laboratori 1; Commercial photography 1; Photography studios, port 1 |
| SALES_2016 | category | 50 | 0 | 5522995378 1; 4155624 1; 41739467 1; 103708138 1 |
| JOBS_2016 | category | 49 | 0 | 68 2; 46828 1; 109 1; 673 1 |
| TOTAL_EARNINGS | amount | 51 | 0 | 1733500175 1; 2291018 1; 19505532 1; 47988557 1 |
| EARNINGS_PER_JOB_2015 | category | 50 | 0 | 2026045 1; 23112 1; 28507 1; 20166 1 |
| EARNINGS_PER_JOB_2016 | other | 51 | 0 | 2132739 1; 20954 1; 28946 1; 20691 1 |
| CHANGE_OF_EARNINGS_PER_JOB | amount | 47 | 0 | 0.026 2; -0.058 2; 0.077 2; nan 1 |
| NATIONAL_LQ_2016 | amount | 48 | 0 | 1.00 2; 1.40 2; 1.62 2; nan 1 |
| WHITE | other | 51 | 0 | 32538 1; 77 1; 420 1; 1453 1 |
| BLACK_OR_AFRICAN_AMERICAN | category | 37 | 0 | 4 3; 5 3; 2 3; 12 3 |
| AMER_INDIAN_OR_AK_NATIVE | category | 11 | 0 | 0 21; 1 16; 2 3; 4 2 |
| ASIAN | category | 28 | 0 | 1 6; 0 6; 7 4; 9 3 |
| HAWAIIAN_OR_OTHER_PAC_ISLAND | category | 4 | 0 | 0 38; 1 9; 2 3; 14 1 |
| HISPANIC_OR_LATINO | category | 47 | 0 | 113 2; 6 2; 7 2; 3 2 |
| TWO_OR_MORE_RACES | category | 25 | 0 | 0 10; 4 6; 1 4; 6 4 |
| MALE | category | 50 | 0 | 469 2; 26122 1; 22 1; 276 1 |
| FEMALE | category | 50 | 0 | 22 2; 20730 1; 87 1; 398 1 |
| C_0_24_AGE | category | 41 | 0 | 1 3; 6 3; 3 3; 19 2 |
| C_25_34_AGE | category | 47 | 0 | 15 2; 167 2; 76 2; 22 2 |
| C_35_44_AGE | category | 48 | 0 | 88 2; 189 2; 38 2; 11198 1 |
| C_45_54_AGE | category | 50 | 0 | 38 2; 9192 1; 35 1; 149 1 |
| C_55_64_AGE | category | 41 | 0 | 1 3; 13 3; 74 2; 52 2 |
| C_65_99_AGE | category | 42 | 0 | 2 3; 0 3; 44 2; 1 2 |
| EARNINGS_BY_SECTOR | category | 10 | 0 | nan 42; 1733500175 1; 325594895 1; 247783148 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:43:46.38128 51 |
| SOURCE_RUN_ID | audit | 1 | 0 | 19c319dd-5de6-42f4-a7bc-4 51 |
| SRC_SHA256 | who | 1 | 0 | fac4c95c19d88a73db9f6f4f2 51 |
