# PORTAL_SOC_UTAH_OPEN_DATA_P_86FCD42645

rows 103  columns 27  scan 3.5s

roles: amount 11, audit 2, category 4, date 1, other 9, who 1

## when

INGESTED_AT
  2026       103  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RCPTOT_S | 68 | 0 | 0.40 | 37.33 | 37.60 | 170.10 |
| VALADD_S | 80 | 0 | 0.30 | 15.98 | 19.30 | 165.20 |
| CEXTOT_S | 64 | 0 | 1 | 33.91 | 35.30 | 373.40 |
| EMP_S | 88 | 0 | 0.30 | 15.51 | 30.30 | 142.20 |
| PAYANN | 88 | 411 | 51.0K | 1.71M | 5.80M | 17.15M |
| PAYANN_S | 88 | 0 | 0.35 | 13.15 | 16.80 | 124.40 |

## who

SRC_SHA256 by rows
       103  33943f24adc426cb739b699f95f854c49c0443a64f1d1b738f60a8b33a301041

SRC_SHA256 by dollars
      17.15M      103 rows  33943f24adc426cb739b699f95f854c49c0443a64f1d1b738f60a8b33a30

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYANN
  33943f24adc426cb739b699f95f854c49c0443a6  2026:17.15M

## what

GEO_ID: 0400000US49 99%, Geographic identifier code 1%

GEO_DISPLAY_LABEL: Utah 99%, Geographic area name 1%

GEO_ID2: 49 99%, nan 1%

YEAR_ID: 2013 99%, nan 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | category | 2 | 0 | 0400000US49 102; Geographic identifier cod 1 |
| GEO_DISPLAY_LABEL | category | 2 | 0 | Utah 102; Geographic area name 1 |
| NAICS_DISPLAY_LABEL | other | 102 | 0 | Petroleum and coal produc 2; Printing and related supp 2; Other miscellaneous manuf 1; Medical equipment and sup 1 |
| RCPTOT | other | 69 | 0 | D 33; 7759425 2; 786855 2; 543900 2 |
| RCPTOT_S | amount | 30 | 0 | S 33; 0 24; 0.3 6; 0.7 3 |
| VALADD | other | 82 | 0 | D 20; 1947719 2; 511197 2; 145833 2 |
| VALADD_S | amount | 37 | 0 | 0 34; S 20; 0.8 5; 1.1000000000000001 3 |
| CEXTOT | other | 66 | 0 | D 35; 324198 2; 14050 2; 14711 2 |
| CEXTOT_S | amount | 37 | 0 | S 35; 0 25; 1 3; 4.5999999999999996 2 |
| GEO_ID2 | category | 2 | 0 | 49 102; nan 1 |
| YEAR_ID | category | 2 | 0 | 2013 102; nan 1 |
| EMP | other | 84 | 0 | nan 15; 1267 3; 93 2; 4079 2 |
| EMP_S | amount | 34 | 0 | 0 40; nan 15; 0.3 4; 1.9 3 |
| PAYANN | amount | 87 | 0 | nan 15; 127231 2; 173365 2; 30124 2 |
| PAYANN_S | amount | 32 | 0 | 0 39; nan 15; 0.4 5; 1.2 5 |
| EMPAVPW | other | 82 | 0 | nan 15; 541 2; 162 2; 504 2 |
| EMPAVPW_S | amount | 35 | 0 | 0 40; nan 15; 0.5 3; 0.3 3 |
| HOURS | other | 86 | 0 | nan 15; 685 2; 1819 2; 5149 2 |
| HOURS_S | amount | 33 | 0 | 0 40; nan 15; 1.5 5; 0.5 3 |
| PAYANPW | amount | 84 | 0 | nan 18; 70391 2; 97564 2; 16550 2 |
| PAYANPW_S | amount | 32 | 0 | 0 36; nan 18; 0.5 3; 1.9 3 |
| CSTMTOT | other | 83 | 0 | nan 19; 5817570 2; 275729 2; 399247 2 |
| CSTMTOT_S | amount | 36 | 0 | 0 38; nan 19; 0.4 4; 0.2 3 |
| NAICS_ID | other | 100 | 0 | nan 2; 3399 1; 3391 1; 339 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:51:30.14116 103 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4956e22b-b4c8-4d01-b5e8-2 103 |
| SRC_SHA256 | who | 1 | 0 | 33943f24adc426cb739b699f9 103 |
