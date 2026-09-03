# PORTAL_SOC_COLORADO_INFORMA_502999772D

rows 984  columns 13  scan 3.7s

roles: amount 2, audit 2, category 4, date 1, other 3, who 2

## when

INGESTED_AT
  2026       984  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ANNUAL_PAYROLL_1_000_PAYANN | 984 | 88 | 156.3K | 16.00M | 142.46M | 1.13B |
| FIRST_QUARTER_PAYROLL_1_000 | 984 | 6 | 38.4K | 4.17M | 36.18M | 287.78M |

## who

GEOGRAPHIC_AREA_NAME_NAME by rows
       984  Colorado

GEOGRAPHIC_AREA_NAME_NAME by dollars
       1.13B      984 rows  Colorado

SRC_SHA256 by rows
       984  8bea662b89fd664c99aba77ea42b003f4e771a6846266d6384285149f9bd1903

SRC_SHA256 by dollars
       1.13B      984 rows  8bea662b89fd664c99aba77ea42b003f4e771a6846266d6384285149f9bd

## who x when

GEOGRAPHIC_AREA_NAME_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = ANNUAL_PAYROLL_1_000_PAYANN
  Colorado                                  2026:1.13B

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ANNUAL_PAYROLL_1_000_PAYANN
  8bea662b89fd664c99aba77ea42b003f4e771a68  2026:1.13B

## what

C_2017_NAICS_CODE_NAICS2017: 00 11%, 62 10%, 56 9%, 54 8%, 52 8%, 72 8%, 81 8%, 44-45 8%, 42 8%, 71 8%, 55 7%, 51 7%

MEANING_OF_NAICS_CODE: Total for all sectors 11%, Health care and social assista 10%, Administrative and support and 9%, Professional, scientific, and  8%, Finance and insurance 8%, Accommodation and food service 8%, Other services (except public  8%, Retail trade 8%, Wholesale trade 8%, Arts, entertainment, and recre 8%, Management of companies and en 7%, Information 7%

MEANING_OF_LEGAL_FORM_OF: All establishments 19%, C-corporations and other corpo 18%, Partnerships 16%, S-corporations 15%, Non-profit 13%, Individual proprietorships 12%, Other noncorporate legal forms 5%, Government 1%

MEANING_OF_EMPLOYMENT_SIZE: All establishments 15%, Establishments with less than  14%, Establishments with 5 to 9 emp 12%, Establishments with 10 to 19 e 12%, Establishments with 20 to 49 e 11%, Establishments with 50 to 99 e 11%, Establishments with 100 to 249 10%, Establishments with 250 to 499 7%, Establishments with 500 to 999 5%, Establishments with 1,000 empl 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEOGRAPHIC_AREA_NAME_NAME | who | 1 | 0 | Colorado 984 |
| C_2017_NAICS_CODE_NAICS2017 | category | 21 | 0 | 00 74; 62 64; 56 57; 54 54 |
| MEANING_OF_NAICS_CODE | category | 20 | 0 | Total for all sectors 74; Health care and social as 64; Administrative and suppor 57; Professional, scientific, 54 |
| MEANING_OF_LEGAL_FORM_OF | category | 8 | 0 | All establishments 191; C-corporations and other  179; Partnerships 155; S-corporations 152 |
| MEANING_OF_EMPLOYMENT_SIZE | category | 10 | 0 | All establishments 143; Establishments with less  136; Establishments with 5 to  123; Establishments with 10 to 115 |
| YEAR_YEAR | other | 1 | 0 | 2019 984 |
| NUMBER_OF_ESTABLISHMENTS | other | 464 | 0 | 3 39; 4 35; 10 23; 6 20 |
| ANNUAL_PAYROLL_1_000_PAYANN | amount | 964 | 0 | 88 6; 262734 6; 120278 6; 111 5 |
| FIRST_QUARTER_PAYROLL_1_000 | amount | 958 | 0 | 6 6; 119 6; 64100 6; 26555 6 |
| NUMBER_OF_EMPLOYEES_EMP | other | 914 | 0 | 1 6; 10 6; 57 6; 51 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:42:53.85424 984 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2934627e-0d32-4afe-9abe-d 984 |
| SRC_SHA256 | who | 1 | 0 | 8bea662b89fd664c99aba77ea 984 |
