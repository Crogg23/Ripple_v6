# PORTAL_SOC_COLORADO_INFORMA_6BE19A7323

rows 2.0K  columns 15  scan 1.5s

roles: audit 2, category 6, date 1, id 3, other 3, who 1

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

SRC_SHA256 by rows
      2.0K  afd99db76ea17c81060fe4928efb879788dc3aa5629f34dda4bb16b05de26357

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  afd99db76ea17c81060fe4928efb879788dc3aa5  2026:2.0K

## what

YEAR: 2020.0 19%, 2019.0 19%, 2018.0 19%, 2017.0 19%, 2016.0 19%, 2021.0 4%, 2025 0%

MONTH: 2 10%, 1 10%, 3 9%, 5 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 4 8%

INDUSTRY: Health and Personal Care Store 8%, Food and Beverage Stores 8%, Building Material and Garden E 8%, Electronics and Appliance Stor 8%, Furniture and Home Furnishings 8%, Motor Vehicle and Parts Dealer 8%, Wholesale Trade 8%, Manufacturing 8%, Construction 8%, Utilities 8%, Mining Quarrying and Oil and G 8%, Agriculture Forestry Fishing a 8%

NAICS: 446 8%, 445 8%, 444 8%, 443 8%, 442 8%, 441 8%, 42 8%, 31-33 8%, 23 8%, 22 8%, 21 8%, 11 8%

SEQUENCENUMBER: 13.0 8%, 12.0 8%, 11.0 8%, 10.0 8%, 9.0 8%, 8.0 8%, 7.0 8%, 6.0 8%, 5.0 8%, 4.0 8%, 3.0 8%, 2.0 8%

RETAILSALESBLANKCODE: nan 100%, NR 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 7 | 0 | 2020.0 384; 2019.0 384; 2018.0 384; 2017.0 384 |
| MONTH | category | 12 | 0 | 2 192; 1 192; 3 173; 5 163 |
| INDUSTRY | category | 33 | 0 | Health and Personal Care  63; Food and Beverage Stores 63; Building Material and Gar 63; Electronics and Appliance 63 |
| NUMBER_OF_RETURNS | other | 1.9K | 0 | 26422 10; 7482 10; 11146 10; 8821 10 |
| NUMBER_OF_RETAILERS | other | 315 | 0 | nan 1.7K; 662 3; 387 3; 250 3 |
| GROSS_SALES | id | 2.0K | 0 | 736969000 10; 1699327000 10; 862897000 10; 495082000 10 |
| RETAIL_SALES | id | 2.0K | 0 | nan 12; 706581000 10; 1674291000 10; 771034000 10 |
| STATE_NET_TAXABLE_SALES | id | 2.0K | 0 | 177909000 10; 569585000 10; 682136000 10; 204647000 10 |
| STATE_SALES_TAX | other | 1.5K | 0 | nan 468; 5883000 9; 253000 8; 8057000 8 |
| NAICS | category | 33 | 0 | 446 63; 445 63; 444 63; 443 63 |
| SEQUENCENUMBER | category | 35 | 0 | 13.0 63; 12.0 63; 11.0 63; 10.0 63 |
| RETAILSALESBLANKCODE | category | 2 | 0 | nan 2.0K; NR 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:43:04.44161 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 44b257b0-ef73-4096-946f-c 2.0K |
| SRC_SHA256 | who | 1 | 0 | afd99db76ea17c81060fe4928 2.0K |
