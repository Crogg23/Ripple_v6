# PORTAL_SOC_CONNECTICUT_OPEN_DEA6C4224A

rows 4  columns 26  scan 5.2s

roles: amount 4, audit 2, category 13, date 2, other 3, who 3

## when

CONTRACT_EXECUTION_DATE
  2024         2  ##############################
  2025         2  ##############################

INGESTED_AT
  2026         4  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LOAN_AMOUNT | 4 | 200.0K | 490.0K | 500.0K | 500.0K | 1.68M |
| TOTAL_ASSISTANCE | 4 | 200.0K | 490.0K | 500.0K | 500.0K | 1.68M |
| TOTAL_PROJECT_COST | 4 | 240.0K | 600.0K | 696.5K | 699.5K | 2.14M |
| AMOUNT_LEVERAGED | 4 | 40.0K | 110.0K | 197.1K | 199.5K | 459.5K |

## who

FUNDING_SOURCE by rows
         4  Cannabusiness Revolving Loan Program

FUNDING_SOURCE by dollars
       1.68M        4 rows  Cannabusiness Revolving Loan Program

STATUTORY_REFERENCE by rows
         4  CGS Secs. 21a-421h and 21a-421i(b)

STATUTORY_REFERENCE by dollars
       1.68M        4 rows  CGS Secs. 21a-421h and 21a-421i(b)

SRC_SHA256 by rows
         4  ae57c2fcacf1f3bd31d0e796c268ee7849cd94413f4b3257398a86bdc74f0db7

SRC_SHA256 by dollars
       1.68M        4 rows  ae57c2fcacf1f3bd31d0e796c268ee7849cd94413f4b3257398a86bdc74f

## who x when

FUNDING_SOURCE by CONTRACT_EXECUTION_DATE, dollars = LOAN_AMOUNT
  Cannabusiness Revolving Loan Program      2024:1.00M 2025:680.0K

STATUTORY_REFERENCE by CONTRACT_EXECUTION_DATE, dollars = LOAN_AMOUNT
  CGS Secs. 21a-421h and 21a-421i(b)        2024:1.00M 2025:680.0K

## what

COMPANY_NAME: Connecticut Cannabis Courier I 25%, Lorrain's CT LLC 25%, Connecticut Social Equity LLC 25%, Dutch LLC 25%

COMPANY_ADDRESS: 101 Merritt 7 25%, 724 Honey Spot Road 25%, 221 Old Cidar Mill Road 25%, 643 Riverside Avenue 25%

MUNICIPALITY: Norwalk 25%, Stratford 25%, Southington 25%, Torrington 25%

COUNTY: Fairfield 50%, Hartford 25%, Litchfield 25%

LEGISLATIVE_DISTRICT: CT-001 50%, CT-004 25%, CT-003 25%

ZIP_CODE: 06851 25%, 06615 25%, 06489 25%, 06790 25%

BUSINESS_INDUSTRY: Manufacturing 50%, Perishable Prepared Food Manuf 25%, Other Manufacturing 25%

NAICS_CODE: 339999 50%, 311911 25%, 311919 25%

MINORITY_WOMAN_VETERAN: Minority/Woman 50%, N/A 50%

PER_APPLICATION_EXISTING: 0 50%, 12 25%, 14 25%

PER_APPLICATION_FULL_TIME: 10 25%, 6 25%, 8 25%, 3-6 25%

PER_APPLICATION_EXISTING_1: 0 75%, 2 25%

PER_APPLICATION_PART_TIME: 5-10 25%, 2 25%, 0 25%, 3-6 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FISCAL_YEAR | other | 1 | 0 | 2025 4 |
| COMPANY_NAME | category | 4 | 0 | Connecticut Cannabis Cour 1; Lorrain's CT LLC 1; Connecticut Social Equity 1; Dutch LLC 1 |
| COMPANY_ADDRESS | category | 4 | 0 | 101 Merritt 7 1; 724 Honey Spot Road 1; 221 Old Cidar Mill Road 1; 643 Riverside Avenue 1 |
| MUNICIPALITY | category | 4 | 0 | Norwalk 1; Stratford 1; Southington 1; Torrington 1 |
| COUNTY | category | 3 | 0 | Fairfield 2; Hartford 1; Litchfield 1 |
| LEGISLATIVE_DISTRICT | category | 3 | 0 | CT-001 2; CT-004 1; CT-003 1 |
| STATE | other | 1 | 0 | CT 4 |
| ZIP_CODE | category | 4 | 0 | 06851 1; 06615 1; 06489 1; 06790 1 |
| BUSINESS_INDUSTRY | category | 3 | 0 | Manufacturing 2; Perishable Prepared Food  1; Other Manufacturing 1 |
| NAICS_CODE | category | 3 | 0 | 339999 2; 311911 1; 311919 1 |
| MINORITY_WOMAN_VETERAN | category | 2 | 0 | Minority/Woman 2; N/A 2 |
| CONTRACT_EXECUTION_DATE | date | 4 | 0 | 2025-05-15T00:00:00.000 1; 2025-03-17T00:00:00.000 1; 2024-12-10T00:00:00.000 1; 2024-12-19T00:00:00.000 1 |
| GRANT_AMOUNT | other | 1 | 0 | 0 4 |
| LOAN_AMOUNT | amount | 3 | 0 | 500000 2; 200000 1; 480000 1 |
| TOTAL_ASSISTANCE | amount | 3 | 0 | 500000 2; 200000 1; 480000 1 |
| TOTAL_PROJECT_COST | amount | 3 | 0 | 600000 2; 240000 1; 699500 1 |
| AMOUNT_LEVERAGED | amount | 4 | 0 | 40000 1; 120000 1; 100000 1; 199500 1 |
| FUNDING_SOURCE | who | 1 | 0 | Cannabusiness Revolving L 4 |
| STATUTORY_REFERENCE | who | 1 | 0 | CGS Secs. 21a-421h and 21 4 |
| PER_APPLICATION_EXISTING | category | 3 | 0 | 0 2; 12 1; 14 1 |
| PER_APPLICATION_FULL_TIME | category | 4 | 0 | 10 1; 6 1; 8 1; 3-6 1 |
| PER_APPLICATION_EXISTING_1 | category | 2 | 0 | 0 3; 2 1 |
| PER_APPLICATION_PART_TIME | category | 4 | 0 | 5-10 1; 2 1; 0 1; 3-6 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:47:11.79791 4 |
| SOURCE_RUN_ID | audit | 1 | 0 | 33a3fb1d-6c12-42df-90d9-0 4 |
| SRC_SHA256 | who | 1 | 0 | ae57c2fcacf1f3bd31d0e796c 4 |
