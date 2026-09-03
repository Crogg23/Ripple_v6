# PORTAL_SOC_UTAH_OPEN_DATA_P_A3773E6FF0

rows 88  columns 21  scan 2.9s

roles: amount 2, audit 2, category 9, date 1, other 7, who 1

## when

INGESTED_AT
  2026        88  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYANN | 85 | 35.8K | 152.8K | 5.14M | 5.29M | 29.10M |
| PAYANPW | 79 | 14.5K | 91.6K | 2.63M | 2.73M | 14.32M |

## who

SRC_SHA256 by rows
        88  8ea2c3341dc09050aa55bf51fd72e1737cc237af189ca9fec5bea0f7fe14ff15

SRC_SHA256 by dollars
      29.10M       88 rows  8ea2c3341dc09050aa55bf51fd72e1737cc237af189ca9fec5bea0f7fe14

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYANN
  8ea2c3341dc09050aa55bf51fd72e1737cc237af  2026:29.10M

## what

GEO_ID: 0400000US49 99%, Geographic identifier code 1%

GEO_DISPLAY_LABEL: Utah 99%, Geographic area name 1%

NAICS_DISPLAY_LABEL: Petroleum and coal products ma 14%, Printing and related support a 14%, Other miscellaneous manufactur 7%, Medical equipment and supplies 7%, Miscellaneous manufacturing 7%, Household and institutional fu 7%, Furniture and related product  7%, Aerospace product and parts ma 7%, Motor vehicle parts manufactur 7%, Motor vehicle body and trailer 7%, Transportation equipment manuf 7%, Electrical equipment, applianc 7%

GEO_ID2: 49 100%

YEAR_ID: 2011 51%, 2010 49%

EMP_S: 1 36%, 5 14%, 2 9%, 11 8%, 3 7%, 4 7%, 6 5%, 9 4%, 14 4%, 32 3%, 12 3%

VALADD_S: 1 44%, 3 10%, 2 10%, 5 7%, 6 6%, 4 6%, 7 6%, 10 4%, 8 4%, 9 3%, 21 1%

CEXTOT_S: 1 43%, 2 13%, 11 9%, 3 6%, 8 6%, 6 6%, 33 4%, 5 4%, 9 3%, 7 3%, 19 3%

NAICS_ID: 3399 9%, 3391 9%, 339 9%, 3371 9%, 337 9%, 3364 9%, 3363 9%, 3362 9%, 336 9%, 335 9%, 3345 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | category | 2 | 0 | 0400000US49 87; Geographic identifier cod 1 |
| GEO_DISPLAY_LABEL | category | 2 | 0 | Utah 87; Geographic area name 1 |
| NAICS_DISPLAY_LABEL | category | 43 | 0 | Petroleum and coal produc 4; Printing and related supp 4; Other miscellaneous manuf 2; Medical equipment and sup 2 |
| GEO_ID2 | category | 2 | 1 | 49 87 |
| YEAR_ID | category | 3 | 1 | 2011 44; 2010 43 |
| EMP | other | 82 | 3 | 1049 2; 1063 2; 3805 2; 3884 2 |
| EMP_S | category | 22 | 3 | 1 27; 5 10; 2 7; 11 6 |
| PAYANN | amount | 83 | 3 | 91100 2; 100482 2; 158737 2; 158314 2 |
| EMPAVPW | other | 79 | 5 | 3004 2; 734 2; 698 2; 2436 2 |
| PAYANPW | amount | 76 | 9 | 58109 2; 64459 2; 92214 2; 90442 2 |
| HOURS | other | 82 | 3 | 1607 2; 1588 2; 5358 2; 5204 2 |
| CSTMTOT | other | 78 | 7 | 4520330 2; 6101297 2; 246809 2; 259374 2 |
| RCPTOT | other | 74 | 12 | 5348632 2; 7365617 2; 693997 2; 718105 2 |
| VALADD | other | 74 | 11 | 928670 2; 1312755 2; 449062 2; 452933 2 |
| VALADD_S | category | 18 | 11 | 1 31; 3 7; 2 7; 5 5 |
| CEXTOT | other | 75 | 11 | 98532 2; 104706 2; 21726 2; 29847 2 |
| CEXTOT_S | category | 19 | 11 | 1 29; 2 9; 11 6; 3 4 |
| NAICS_ID | category | 44 | 3 | 3399 2; 3391 2; 339 2; 3371 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:47:19.38373 88 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0933c7d0-422f-40f4-8376-4 88 |
| SRC_SHA256 | who | 1 | 0 | 8ea2c3341dc09050aa55bf51f 88 |
