# PORTAL_SOC_UTAH_OPEN_DATA_P_193D6FEEC1

rows 87  columns 21  scan 3.0s

roles: amount 2, audit 2, category 9, date 1, other 7, who 1

## when

INGESTED_AT
  2026        87  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYANN | 84 | 37.5K | 152.7K | 4.92M | 5.12M | 28.00M |
| PAYANPW | 80 | 14.5K | 96.3K | 2.58M | 2.60M | 13.96M |

## who

SRC_SHA256 by rows
        87  c285a059e4c232a3c5f84b999815b7e320a60018a08618e5b96acc13089e609a

SRC_SHA256 by dollars
      28.00M       87 rows  c285a059e4c232a3c5f84b999815b7e320a60018a08618e5b96acc13089e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYANN
  c285a059e4c232a3c5f84b999815b7e320a60018  2026:28.00M

## what

GEO_ID: 0400000US49 99%, Geographic identifier code 1%

GEO_DISPLAY_LABEL: Utah 99%, Geographic area name 1%

NAICS_DISPLAY_LABEL: Petroleum and coal products ma 14%, Printing and related support a 14%, Other miscellaneous manufactur 7%, Medical equipment and supplies 7%, Miscellaneous manufacturing 7%, Household and institutional fu 7%, Furniture and related product  7%, Aerospace product and parts ma 7%, Motor vehicle parts manufactur 7%, Transportation equipment manuf 7%, Electrical equipment, applianc 7%, Navigational, measuring, elect 7%

GEO_ID2: 49 99%, nan 1%

YEAR_ID: 2009 51%, 2010 48%, nan 1%

EMP_S: 1 37%, 5 13%, 2 12%, 4 10%, 3 5%, nan 5%, 11 4%, 10 4%, 26 3%, 9 3%, 13 3%, 6 3%

VALADD_S: 1 39%, 5 11%, nan 10%, 6 8%, 2 8%, 3 6%, 4 5%, 10 4%, 7 4%, 21 3%, 17 1%, 8 1%

CEXTOT_S: 1 37%, nan 10%, 11 8%, 3 8%, 2 7%, 8 5%, 10 4%, 7 4%, 14 4%, 6 4%, 5 4%, 17 4%

NAICS_ID: nan 12%, 3399 8%, 3391 8%, 339 8%, 3371 8%, 337 8%, 3364 8%, 3363 8%, 336 8%, 335 8%, 3345 8%, 3344 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | category | 2 | 0 | 0400000US49 86; Geographic identifier cod 1 |
| GEO_DISPLAY_LABEL | category | 2 | 0 | Utah 86; Geographic area name 1 |
| NAICS_DISPLAY_LABEL | category | 43 | 0 | Petroleum and coal produc 4; Printing and related supp 4; Other miscellaneous manuf 2; Medical equipment and sup 2 |
| GEO_ID2 | category | 2 | 0 | 49 86; nan 1 |
| YEAR_ID | category | 3 | 0 | 2009 44; 2010 42; nan 1 |
| EMP | other | 79 | 0 | nan 4; 1081 2; 1061 2; 4934 2 |
| EMP_S | category | 21 | 0 | 1 29; 5 10; 2 9; 4 8 |
| PAYANN | amount | 82 | 0 | nan 3; 89341 2; 91770 2; 176299 2 |
| EMPAVPW | other | 76 | 0 | nan 6; 969 2; 692 2; 743 2 |
| PAYANPW | amount | 78 | 0 | nan 7; 48701 2; 58595 2; 110691 2 |
| HOURS | other | 81 | 0 | nan 4; 1546 2; 1625 2; 6763 2 |
| CSTMTOT | other | 79 | 0 | nan 5; 3722065 2; 4531582 2; 293332 2 |
| RCPTOT | other | 76 | 0 | nan 9; 4376774 2; 5363654 2; 743469 2 |
| VALADD | other | 76 | 0 | nan 8; 624272 2; 920724 2; 448347 2 |
| VALADD_S | category | 20 | 0 | 1 31; 5 9; nan 8; 6 6 |
| CEXTOT | other | 78 | 0 | nan 7; 361407 2; 98877 2; 16085 2 |
| CEXTOT_S | category | 22 | 0 | 1 27; nan 7; 11 6; 3 6 |
| NAICS_ID | category | 44 | 0 | nan 3; 3399 2; 3391 2; 339 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:48:13.14346 87 |
| SOURCE_RUN_ID | audit | 1 | 0 | a93fbea4-d92f-4d81-bb72-c 87 |
| SRC_SHA256 | who | 1 | 0 | c285a059e4c232a3c5f84b999 87 |
