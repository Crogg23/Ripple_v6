# PORTAL_SOC_COLORADO_INFORMA_C4D7351098

rows 150  columns 18  scan 1.9s

roles: audit 2, category 3, date 1, other 12, who 1

## when

INGESTED_AT
  2026       150  ##############################

## who

SRC_SHA256 by rows
       150  622dc63ef3ce25056fba1195ade20a1ac09342036273bab44d60c4c856012225

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  622dc63ef3ce25056fba1195ade20a1ac0934203  2026:150

## what

YEAR: 2019 21%, 2020 21%, 2021 21%, 2023 19%, 2022 19%

NAICS_CODE: 92 8%, 722 8%, 721 8%, 71 8%, 62 8%, 61 8%, 56 8%, 55; 81 8%, 54 8%, 53 8%, 52 8%, 51 8%

INDUSTRY: Public Administration 8%, Food Services and Drinking Pla 8%, Accommodation 8%, Arts, Entertainment, and Recre 8%, Health Care and Social Assista 8%, Educational Services 8%, Administrative and Support and 8%, Professional, Scientific, and  8%, Real Estate and Rental and Lea 8%, Finance and Insurance 8%, Information 8%, Transportation and Warehousing 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 5 | 0 | 2019 31; 2020 31; 2021 31; 2023 29 |
| NAICS_CODE | category | 38 | 0 | 92 5; 722 5; 721 5; 71 5 |
| INDUSTRY | category | 39 | 0 | Public Administration 5; Food Services and Drinkin 5; Accommodation 5; Arts, Entertainment, and  5 |
| NUMBER_OF_RETURNS_AGGREGATE | other | 137 | 0 | nan 6; 212 3; 3 2; 1471 2 |
| NUMBER_OF_TAXPAYERS_AGGREGATE | other | 55 | 0 | nan 93; 3 2; 212 2; 220 2 |
| FEDERAL_TAXABLE_INCOME | other | 138 | 0 | nan 10; 44618292213 1; 8168545355 1; 8048131527 1 |
| COLORADO_TAXABLE_INCOME | other | 142 | 0 | nan 6; 0 2; 341357486 1; 134289567 1 |
| COLORADO_GROSS_TAX_AGGREGATE | other | 138 | 0 | nan 10; 0 3; 29007351 1; 8742389 1 |
| COLORADO_NET_TAX_AGGREGATE | other | 142 | 0 | nan 8; 0 3; 28163559 1; 8559516 1 |
| NUMBER_OF_RETURNS_AVERAGE | other | 137 | 0 | nan 6; 212 3; 3 2; 1471 2 |
| NUMBER_OF_TAXPAYERS_AVERAGE | other | 55 | 0 | nan 93; 3 2; 212 2; 220 2 |
| FEDERAL_TAXABLE_INCOME_AVERAGE | other | 143 | 0 | nan 8; 0 2; 8383745 1; 13217711 1 |
| COLORADO_TAXABLE_INCOME_1 | other | 145 | 0 | 0 4; nan 4; 64141 1; 217297 1 |
| COLORADO_GROSS_TAX_AVERAGE | other | 141 | 0 | nan 8; 0 5; 5450 1; 14146 1 |
| COLORADO_NET_TAX_AVERAGE | other | 135 | 0 | nan 6; 0 5; 4203 2; 24456 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:45:56.46380 150 |
| SOURCE_RUN_ID | audit | 1 | 0 | ded0d506-c899-46e9-9e50-4 150 |
| SRC_SHA256 | who | 1 | 0 | 622dc63ef3ce25056fba1195a 150 |
