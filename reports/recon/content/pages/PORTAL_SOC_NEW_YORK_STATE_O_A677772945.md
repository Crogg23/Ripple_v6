# PORTAL_SOC_NEW_YORK_STATE_O_A677772945

rows 2.0K  columns 16  scan 3.0s

roles: amount 4, audit 2, category 7, date 1, other 2, who 1

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT_OF_CREDIT | 1.8K | 0 | 0 | 34.44M | 448.68M | 3.96B |
| PERCENT_OF_CREDIT | 1.8K | 0 | 0 | 100 | 100 | 7.4K |
| MEDIAN_AMOUNT_OF_CREDIT | 1.8K | 0 | 0 | 1.02M | 40.25M | 107.18M |
| MEAN_AMOUNT_OF_CREDIT | 1.8K | 0 | 0 | 6.40M | 31.84M | 258.92M |

## who

SRC_SHA256 by rows
      2.0K  ec18cde193865220a0fdb2f2c9ad1e7c326544f6ba41469e056db3516406b363

SRC_SHA256 by dollars
       3.96B     2.0K rows  ec18cde193865220a0fdb2f2c9ad1e7c326544f6ba41469e056db3516406

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = AMOUNT_OF_CREDIT
  ec18cde193865220a0fdb2f2c9ad1e7c326544f6  2026:3.96B

## what

CREDIT_TYPE: Credit Carried Forward 25%, Credit Used 25%, Credit Claimed 25%, Credit Earned 25%

CREDIT_NAME: Empire State Jobs Retention Pr 8%, Empire State Film Production C 8%, Empire State Film Post Product 8%, Empire State Commercial Produc 8%, Empire State Apprentice Tax Cr 8%, Economic Transformation and Fa 8%, Credit for Taxicabs & Livery S 8%, Credit for Purchase of an Auto 8%, Credit for Employment of Perso 8%, COVID-19 Capital costs Credit 8%, Conservation Easement Tax Cred 8%, Clean Heating Fuel Credit 8%

NAICS_DESCRIPTION: Arts, Entertainment, and Recre 8%, Health Care and Social Assista 8%, Educational Services 8%, Administrative and Support and 8%, Management of Companies and En 8%, Professional, Scientific, and  8%, Real Estate and Rental and Lea 8%, Finance and Insurance 8%, Information 8%, Transportation and Warehousing 8%, Retail Trade 8%, Wholesale Trade 8%

NUMBER_OF_TAXPAYERS: 0 87%, nan 9%, 4 1%, 3 1%, 5 0%, 7 0%, 6 0%, 34 0%, 25 0%, 14 0%, 35 0%, 17 0%

GROUP_SORT_ORDER: 71 8%, 62 8%, 61 8%, 56 8%, 55 8%, 54 8%, 53 8%, 52 8%, 51 8%, 48 8%, 44 8%, 42 8%

CREDIT_TYPE_SORT_ORDER: 8 25%, 6 25%, 5 25%, 1 25%

NOTES: nan 87%, d/ 8%, 2/ 4%, 2/, d/ 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TAX_YEAR | other | 1 | 0 | 2022 2.0K |
| TAX_ARTICLE | other | 1 | 0 | 9A 2.0K |
| CREDIT_TYPE | category | 4 | 0 | Credit Carried Forward 500; Credit Used 500; Credit Claimed 500; Credit Earned 500 |
| CREDIT_NAME | category | 23 | 0 | Empire State Jobs Retenti 84; Empire State Film Product 84; Empire State Film Post Pr 84; Empire State Commercial P 84 |
| NAICS_DESCRIPTION | category | 21 | 0 | Arts, Entertainment, and  96; Health Care and Social As 96; Educational Services 96; Administrative and Suppor 96 |
| NUMBER_OF_TAXPAYERS | category | 30 | 0 | 0 1.7K; nan 178; 4 23; 3 13 |
| AMOUNT_OF_CREDIT | amount | 81 | 0 | 0 1.7K; nan 178; 43294 3; 357325 2 |
| PERCENT_OF_CREDIT | amount | 45 | 0 | 0 1.7K; nan 178; 100 52; 44.23407917 2 |
| MEDIAN_AMOUNT_OF_CREDIT | amount | 69 | 0 | 0 1.7K; nan 178; 5000 4; 12133 4 |
| MEAN_AMOUNT_OF_CREDIT | amount | 81 | 0 | 0 1.7K; nan 178; 10824 3; 71465 2 |
| GROUP_SORT_ORDER | category | 21 | 0 | 71 96; 62 96; 61 96; 56 96 |
| CREDIT_TYPE_SORT_ORDER | category | 4 | 0 | 8 500; 6 500; 5 500; 1 500 |
| NOTES | category | 4 | 0 | nan 1.7K; d/ 170; 2/ 76; 2/, d/ 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:42:06.87880 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | de3cd52d-9ae8-4f22-87be-5 2.0K |
| SRC_SHA256 | who | 1 | 0 | ec18cde193865220a0fdb2f2c 2.0K |
