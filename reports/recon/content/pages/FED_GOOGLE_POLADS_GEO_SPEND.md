# FED_GOOGLE_POLADS_GEO_SPEND

rows 1.3K  columns 26  scan 3.4s

roles: amount 12, audit 2, category 1, id 1, other 9, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SPEND_USD | 1.3K | 0 | 1.26M | 11.67M | 53.61M | 2.50B |
| SPEND_INR | 1.3K | 0 | 0 | 304.38M | 1.41B | 9.12B |
| SPEND_GBP | 1.3K | 0 | 0 | 0 | 12.24M | 12.24M |
| SPEND_NZD | 1.3K | 0 | 0 | 0 | 3.35M | 3.35M |
| SPEND_ILS | 1.3K | 0 | 0 | 0 | 9.68M | 9.68M |
| SPEND_AUD | 1.3K | 0 | 0 | 0 | 23.81M | 82.78M |

## who

SRC_SHA256 by rows
      1.3K  b4de0c2647cdab05b29b428ebcb961964315c6e19a53362939aad3c717dab3c0

SRC_SHA256 by dollars
       2.50B     1.3K rows  b4de0c2647cdab05b29b428ebcb961964315c6e19a53362939aad3c717da

## what

COUNTRY: US 87%, IN 3%, MX 2%, BR 2%, AR 2%, CL 1%, ZA 1%, AU 1%, NZ 0%, TW 0%, IL 0%, GB 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTRY | category | 12 | 0 | US 1.1K; IN 38; MX 32; BR 28 |
| COUNTRY_SUBDIVISION_PRIMARY | other | 202 | 18 | US-CA 157; US-TX 112; US-FL 83; US-NY 79 |
| COUNTRY_SUBDIVISION_SECONDARY | id | 1.3K | 0 | NC-10 (2026 redistricting 7; CA-22 (2022 redistricting 7; Chandigarh 7; TX-1 (2026 redistricting) 7 |
| SPEND_USD | amount | 1.1K | 0 | 0 163; 201900 6; 4463800 6; 135100 6 |
| SPEND_EUR | other | 1 | 0 | 0 1.3K |
| SPEND_INR | amount | 38 | 0 | 0 1.3K; 44088750 1; 1700000 1; 63499250 1 |
| SPEND_BGN | other | 1 | 0 | 0 1.3K |
| SPEND_CZK | other | 1 | 0 | 0 1.3K |
| SPEND_DKK | other | 1 | 0 | 0 1.3K |
| SPEND_HUF | other | 1 | 0 | 0 1.3K |
| SPEND_PLN | other | 1 | 0 | 0 1.3K |
| SPEND_RON | other | 1 | 0 | 0 1.3K |
| SPEND_SEK | other | 1 | 0 | 0 1.3K |
| SPEND_GBP | amount | 2 | 0 | 0 1.3K; 12240900 1 |
| SPEND_NZD | amount | 2 | 0 | 0 1.3K; 3351600 1 |
| SPEND_ILS | amount | 2 | 0 | 0 1.3K; 9680750 1 |
| SPEND_AUD | amount | 11 | 0 | 0 1.3K; 2970900 1; 22324200 1; 667350 1 |
| SPEND_TWD | amount | 2 | 0 | 0 1.3K; 42459000 1 |
| SPEND_BRL | amount | 29 | 0 | 0 1.3K; 2372500 1; 500 1; 901500 1 |
| SPEND_ARS | amount | 26 | 0 | 0 1.3K; 77715000 1; 246510000 1; 313830000 1 |
| SPEND_ZAR | amount | 10 | 0 | 0 1.3K; 225000 2; 285000 1; 15000 1 |
| SPEND_CLP | amount | 17 | 0 | 0 1.3K; 13800000 1; 59100000 1; 18400000 1 |
| SPEND_MXN | amount | 33 | 0 | 0 1.3K; 3827000 1; 2984000 1; 1895000 1 |
| INGESTED_AT | audit | 1 | 0 | 1785965602280091 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4141cf7d-a262-4c65-b58b-3 1.3K |
| SRC_SHA256 | who | 1 | 0 | b4de0c2647cdab05b29b428eb 1.3K |
