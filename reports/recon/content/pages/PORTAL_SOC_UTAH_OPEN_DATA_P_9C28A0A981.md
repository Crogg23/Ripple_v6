# PORTAL_SOC_UTAH_OPEN_DATA_P_9C28A0A981

rows 88  columns 21  scan 3.1s

roles: amount 2, audit 2, category 9, date 1, other 7, who 1

## when

INGESTED_AT
  2026        88  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYANN | 86 | 37.5K | 156.4K | 5.03M | 5.36M | 28.99M |
| PAYANPW | 82 | 25.3K | 97.1K | 2.69M | 2.95M | 15.00M |

## who

SRC_SHA256 by rows
        88  3de66c75fbef8e12f991ca16f0a4f4431f12e184e572c9d7c83a3f221156ade4

SRC_SHA256 by dollars
      28.99M       88 rows  3de66c75fbef8e12f991ca16f0a4f4431f12e184e572c9d7c83a3f221156

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYANN
  3de66c75fbef8e12f991ca16f0a4f4431f12e184  2026:28.99M

## what

GEO_ID: 0400000US49 99%, Geographic identifier code 1%

GEO_DISPLAY_LABEL: Utah 99%, Geographic area name 1%

NAICS_DISPLAY_LABEL: Petroleum and coal products ma 14%, Printing and related support a 14%, Other miscellaneous manufactur 7%, Medical equipment and supplies 7%, Miscellaneous manufacturing 7%, Household and institutional fu 7%, Furniture and related product  7%, Aerospace product and parts ma 7%, Motor vehicle parts manufactur 7%, Transportation equipment manuf 7%, Electrical equipment, applianc 7%, Navigational, measuring, elect 7%

GEO_ID2: 49 100%

YEAR_ID: 2009 51%, 2008 49%

EMP_S: 1 53%, 4 10%, 2 9%, 3 9%, 5 5%, 10 4%, 7 3%, 6 3%, 8 1%, 21 1%, 14 1%

VALADD_S: 1 47%, 2 13%, 4 10%, 5 6%, 8 6%, 3 4%, 7 4%, 16 3%, 13 3%, 6 3%, 11 1%

CEXTOT_S: 1 42%, 2 12%, 3 8%, 8 6%, 10 6%, 6 6%, 11 5%, 23 5%, 15 5%, 7 3%, 18 3%

NAICS_ID: 3399 9%, 3391 9%, 339 9%, 3371 9%, 337 9%, 3364 9%, 3363 9%, 336 9%, 335 9%, 3345 9%, 3344 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | category | 2 | 0 | 0400000US49 87; Geographic identifier cod 1 |
| GEO_DISPLAY_LABEL | category | 2 | 0 | Utah 87; Geographic area name 1 |
| NAICS_DISPLAY_LABEL | category | 43 | 0 | Petroleum and coal produc 4; Printing and related supp 4; Other miscellaneous manuf 2; Medical equipment and sup 2 |
| GEO_ID2 | category | 2 | 1 | 49 87 |
| YEAR_ID | category | 3 | 1 | 2009 44; 2008 43 |
| EMP | other | 81 | 3 | 1088 2; 1092 2; 6212 2; 4951 2 |
| EMP_S | category | 20 | 3 | 1 41; 4 8; 2 7; 3 7 |
| PAYANN | amount | 84 | 2 | 91845 2; 90476 2; 231680 2; 177099 2 |
| EMPAVPW | other | 81 | 5 | 652 2; 699 2; 4577 2; 3420 2 |
| PAYANPW | amount | 80 | 6 | 49324 2; 49352 2; 141977 2; 111184 2 |
| HOURS | other | 81 | 2 | 1543 2; 1562 2; 8606 2; 6789 2 |
| CSTMTOT | other | 82 | 3 | 6064972 2; 3746044 2; 376219 2; 294088 2 |
| RCPTOT | other | 80 | 4 | 6823042 2; 4405083 2; 999983 2; 746350 2 |
| VALADD | other | 82 | 4 | 769441 2; 596770 2; 622243 2; 448869 2 |
| VALADD_S | category | 18 | 4 | 1 37; 2 10; 4 8; 5 5 |
| CEXTOT | other | 77 | 7 | 272392 2; 361854 2; 27414 2; 16183 2 |
| CEXTOT_S | category | 24 | 7 | 1 27; 2 8; 3 5; 8 4 |
| NAICS_ID | category | 44 | 3 | 3399 2; 3391 2; 339 2; 3371 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:46:32.17800 88 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2165cf7e-64a9-4001-ac7b-0 88 |
| SRC_SHA256 | who | 1 | 0 | 3de66c75fbef8e12f991ca16f 88 |
