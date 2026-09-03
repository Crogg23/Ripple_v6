# PORTAL_SOC_UTAH_OPEN_DATA_P_51F192B9AC

rows 99  columns 21  scan 2.8s

roles: amount 2, audit 2, category 9, date 1, other 7, who 1

## when

INGESTED_AT
  2026        99  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYANN | 95 | 30.3K | 141.8K | 5.43M | 5.51M | 30.52M |
| PAYANPW | 91 | 13.9K | 91.3K | 2.97M | 3.02M | 16.05M |

## who

SRC_SHA256 by rows
        99  412b6dd5c343431ad5c4283d2f19152e9fbd42b29da0bff27c36b086aa19ead4

SRC_SHA256 by dollars
      30.52M       99 rows  412b6dd5c343431ad5c4283d2f19152e9fbd42b29da0bff27c36b086aa19

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYANN
  412b6dd5c343431ad5c4283d2f19152e9fbd42b2  2026:30.52M

## what

GEO_ID: 0400000US49 99%, Geographic identifier code 1%

GEO_DISPLAY_LABEL: Utah 99%, Geographic area name 1%

NAICS_DISPLAY_LABEL: Petroleum and coal products ma 14%, Printing and related support a 14%, Other miscellaneous manufactur 7%, Medical equipment and supplies 7%, Miscellaneous manufacturing 7%, Other furniture related produc 7%, Household and institutional fu 7%, Furniture and related product  7%, Aerospace product and parts ma 7%, Motor vehicle parts manufactur 7%, Motor vehicle body and trailer 7%, Transportation equipment manuf 7%

EMP_S: X 51%, 1 28%, 3 6%, 2 4%, 4 3%, 5 2%, 11 1%, 17 1%, 12 1%, 6 1%, 19 1%, 16 1%

VALADD_S: X 52%, 1 24%, 2 6%, 8 4%, 3 3%, 4 3%, 9 2%, 49(s) 1%, 11 1%, 13 1%, 26 1%, 5 1%

CEXTOT_S: X 56%, 1 16%, S 5%, 2 4%, 23 3%, 28 3%, 3 2%, 6 2%, 8 2%, 24 2%, 9 1%, 7 1%

GEO_ID2: 49 99%, nan 1%

YEAR_ID: 2007 49%, 2008 49%, nan 1%

NAICS_ID: nan 12%, 3399 8%, 3391 8%, 339 8%, 3379 8%, 3371 8%, 337 8%, 3364 8%, 3363 8%, 3362 8%, 336 8%, 3359 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | category | 2 | 0 | 0400000US49 98; Geographic identifier cod 1 |
| GEO_DISPLAY_LABEL | category | 2 | 0 | Utah 98; Geographic area name 1 |
| NAICS_DISPLAY_LABEL | category | 48 | 0 | Petroleum and coal produc 4; Printing and related supp 4; Other miscellaneous manuf 2; Medical equipment and sup 2 |
| EMP_S | category | 14 | 0 | X 49; 1 27; 3 6; 2 4 |
| VALADD_S | category | 15 | 0 | X 49; 1 23; 2 6; 8 4 |
| CEXTOT_S | category | 20 | 0 | X 51; 1 15; S 5; 2 4 |
| GEO_ID2 | category | 2 | 0 | 49 98; nan 1 |
| YEAR_ID | category | 3 | 0 | 2007 49; 2008 49; nan 1 |
| EMP | other | 92 | 0 | nan 4; 3758 2; 1041 2; 1088 2 |
| PAYANN | amount | 93 | 0 | nan 4; 76830 2; 91845 2; 225145 2 |
| EMPAVPW | other | 89 | 0 | nan 7; 678 2; 652 2; 4431 2 |
| PAYANPW | amount | 89 | 0 | nan 8; 46679 2; 49324 2; 134517 2 |
| HOURS | other | 93 | 0 | nan 3; 1321 2; 1543 2; 8371 2 |
| CSTMTOT | other | 86 | 0 | nan 10; 4778681 2; 6064972 2; 357621 2 |
| RCPTOT | other | 90 | 0 | nan 6; 5757938 2; 6823042 2; 980835 2 |
| VALADD | other | 89 | 0 | nan 8; 985238 2; 769441 2; 623166 2 |
| CEXTOT | other | 85 | 0 | nan 11; 100999 2; 272392 2; 51273 2 |
| NAICS_ID | category | 49 | 0 | nan 3; 3399 2; 3391 2; 339 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:50:56.06392 99 |
| SOURCE_RUN_ID | audit | 1 | 0 | 52918966-e4e4-41e9-b73b-9 99 |
| SRC_SHA256 | who | 1 | 0 | 412b6dd5c343431ad5c4283d2 99 |
