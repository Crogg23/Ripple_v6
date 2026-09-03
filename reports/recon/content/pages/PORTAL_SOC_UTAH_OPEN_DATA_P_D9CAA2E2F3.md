# PORTAL_SOC_UTAH_OPEN_DATA_P_D9CAA2E2F3

rows 93  columns 21  scan 3.2s

roles: amount 2, audit 2, category 9, date 1, other 7, who 1

## when

INGESTED_AT
  2026        93  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYANN | 91 | 31.6K | 148.1K | 4.59M | 4.82M | 26.56M |
| PAYANPW | 90 | 15.6K | 85.0K | 2.51M | 2.69M | 14.47M |

## who

SRC_SHA256 by rows
        93  19c4bb5aa4911e640774d7abb01d7742a5ae29b9bdae297ebf3fea6b402e7ca5

SRC_SHA256 by dollars
      26.56M       93 rows  19c4bb5aa4911e640774d7abb01d7742a5ae29b9bdae297ebf3fea6b402e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYANN
  19c4bb5aa4911e640774d7abb01d7742a5ae29b9  2026:26.56M

## what

GEO_ID: 0400000US49 99%, Geographic identifier code 1%

GEO_DISPLAY_LABEL: Utah 99%, Geographic area name 1%

NAICS_DISPLAY_LABEL: Petroleum & coal products mfg 14%, Printing & related support act 14%, Other miscellaneous mfg 7%, Medical equipment & supplies m 7%, Miscellaneous mfg 7%, Household & institutional furn 7%, Furniture & related product mf 7%, Aerospace product & parts mfg 7%, Motor vehicle parts mfg 7%, Motor vehicle body & trailer m 7%, Transportation equipment mfg 7%, Electrical equipment, applianc 7%

GEO_ID2: 49 99%, nan 1%

YEAR_ID: 2006 51%, 2005 48%, nan 1%

EMPSMAO_S: 1 42%, 5 9%, 7 8%, 2 7%, 3 7%, 6 7%, 10 6%, 8 5%, 4 4%, nan 2%, 23 1%, 31 1%

VALADDM_S: 1 39%, 2 19%, 11 6%, 3 5%, 6 5%, 7 5%, 4 5%, 17 4%, 16 4%, nan 4%, 5 4%, 9 2%

CEXTOT_S: 1 40%, 2 10%, 3 9%, 9 7%, 12 6%, nan 6%, 4 4%, 15 4%, 19 4%, 14 4%, 28 3%, 16 3%

NAICS_ID: nan 12%, 3399 8%, 3391 8%, 339 8%, 3371 8%, 337 8%, 3364 8%, 3363 8%, 3362 8%, 336 8%, 335 8%, 3345 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | category | 2 | 0 | 0400000US49 92; Geographic identifier cod 1 |
| GEO_DISPLAY_LABEL | category | 2 | 0 | Utah 92; Geographic area name 1 |
| NAICS_DISPLAY_LABEL | category | 45 | 0 | Petroleum & coal products 4; Printing & related suppor 4; Other miscellaneous mfg 2; Medical equipment & suppl 2 |
| GEO_ID2 | category | 2 | 0 | 49 92; nan 1 |
| YEAR_ID | category | 3 | 0 | 2006 47; 2005 45; nan 1 |
| EMPSMAO | other | 86 | 0 | 981 3; 973 2; 5360 2; 5433 2 |
| EMPSMAO_S | category | 20 | 0 | 1 36; 5 8; 7 7; 2 6 |
| PAYANN | amount | 88 | 0 | 68316 2; 71135 2; 200427 2; 195387 2 |
| EMPAVPW | other | 86 | 0 | nan 4; 584 2; 629 2; 3661 2 |
| PAYANPW | amount | 87 | 0 | nan 3; 39923 2; 43824 2; 114003 2 |
| HRSTOTM | other | 87 | 0 | 1176 2; 1283 2; 7781 2; 7815 2 |
| CSTMTOT | other | 86 | 0 | nan 3; 3552319 2; 4283540 2; 270791 2 |
| RCPTOT | other | 87 | 0 | 4254532 2; 5280876 2; 871378 2; 984946 2 |
| VALADDM | other | 87 | 0 | nan 3; 748678 2; 1053412 2; 594531 2 |
| VALADDM_S | category | 21 | 0 | 1 32; 2 16; 11 5; 3 4 |
| CEXTOT | other | 85 | 0 | nan 4; 37325 2; 192576 2; 30817 2 |
| CEXTOT_S | category | 30 | 0 | 1 28; 2 7; 3 6; 9 5 |
| NAICS_ID | category | 47 | 0 | nan 3; 3399 2; 3391 2; 339 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:49:47.41723 93 |
| SOURCE_RUN_ID | audit | 1 | 0 | 282e0f76-031a-43be-949e-b 93 |
| SRC_SHA256 | who | 1 | 0 | 19c4bb5aa4911e640774d7abb 93 |
