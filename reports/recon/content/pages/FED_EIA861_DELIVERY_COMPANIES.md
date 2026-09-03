# FED_EIA861_DELIVERY_COMPANIES

rows 9  columns 27  scan 3.6s

roles: amount 4, audit 2, category 20, date 1, who 1

## when

_INGESTED_AT
  2026         9  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| REVENUES | 7 | 0 | 204.0K | 2.37M | 2.42M | 5.01M |
| REVENUES_1 | 7 | 4.0K | 175.1K | 1.78M | 1.83M | 3.63M |
| REVENUES_2 | 7 | 2.1K | 43.0K | 642.7K | 651.0K | 1.35M |
| REVENUES_4 | 7 | 6.1K | 415.0K | 4.80M | 4.91M | 9.99M |

## who

_SRC_FILE by rows
         9  Delivery_Companies_2024.xlsx

_SRC_FILE by dollars
       5.01M        9 rows  Delivery_Companies_2024.xlsx

## who x when

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date, dollars = REVENUES
  Delivery_Companies_2024.xlsx              2026:5.01M

## what

UNNAMED_0: 2024 78%, This data should not be added  11%, Data Year 11%

UNNAMED_1: 44372 12%, 40051 12%, 20404 12%, 13830 12%, 11292 12%, 8901 12%, 3278 12%, Utility Number 12%

UNNAMED_2: Oncor Electric Delivery Compan 12%, Texas-New Mexico Power Co 12%, AEP Texas North Company 12%, Nueces Electric Cooperative 12%, City of Lubbock - (TX) 12%, CenterPoint Energy 12%, AEP Texas Central Company 12%, Utility Name 12%

UNNAMED_3: C 88%, Part 12%

UNNAMED_4: Delivery 88%, Service Type 12%

UNNAMED_5: O 88%, Data Type
O = Observed
I = Imp 12%

UNNAMED_6: TX 88%, State 12%

UNNAMED_7: Investor Owned 62%, Cooperative 12%, Municipal 12%, Ownership 12%

UNNAMED_8: ERCO 88%, BA Code 12%

SALES: 46669589 12%, 3223123 12%, 1896215 12%, 0 12%, 795850 12%, 32768523 12%, 10660737 12%, Megawatthours 12%

CUSTOMERS: 3477215 12%, 233056 12%, 157455 12%, 0 12%, 90455 12%, 2485470 12%, 784148 12%, Count 12%

SALES_1: 49826500 12%, 5674061 12%, 6128780 12%, 77195 12%, 1104490 12%, 28202435 12%, 10152977 12%, Megawatthours 12%

CUSTOMERS_1: 523112 12%, 43845 12%, 37485 12%, 1230 12%, 14616 12%, 324291 12%, 124961 12%, Count 12%

SALES_2: 65686094 12%, 8231633 12%, 2951868 12%, 154797 12%, 73414 12%, 44983552 12%, 10368769 12%, Megawatthours 12%

CUSTOMERS_2: 10645 12%, 102 12%, 5189 12%, 15 12%, 9 12%, 2058 12%, 7022 12%, Count 12%

REVENUES_3: . 38%, 0 25%, 5207.8 12%, 1771.7 12%, Thousand Dollars 12%

SALES_3: . 38%, 0 25%, 156924 12%, 59166 12%, Megawatthours 12%

CUSTOMERS_3: . 38%, 1 25%, 0 25%, Count 12%

SALES_4: 162339107 12%, 17128817 12%, 10976863 12%, 231992 12%, 1973754 12%, 106013676 12%, 31182483 12%, Megawatthours 12%

CUSTOMERS_4: 4010973 12%, 277003 12%, 200129 12%, 1245 12%, 105080 12%, 2811820 12%, 916131 12%, Count 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | category | 3 | 0 | 2024 7; This data should not be a 1; Data Year 1 |
| UNNAMED_1 | category | 8 | 1 | 44372 1; 40051 1; 20404 1; 13830 1 |
| UNNAMED_2 | category | 8 | 1 | Oncor Electric Delivery C 1; Texas-New Mexico Power Co 1; AEP Texas North Company 1; Nueces Electric Cooperati 1 |
| UNNAMED_3 | category | 2 | 1 | C 7; Part 1 |
| UNNAMED_4 | category | 2 | 1 | Delivery 7; Service Type 1 |
| UNNAMED_5 | category | 2 | 1 | O 7; Data Type
O = Observed
I  1 |
| UNNAMED_6 | category | 2 | 1 | TX 7; State 1 |
| UNNAMED_7 | category | 4 | 1 | Investor Owned 5; Cooperative 1; Municipal 1; Ownership 1 |
| UNNAMED_8 | category | 2 | 1 | ERCO 7; BA Code 1 |
| REVENUES | amount | 8 | 1 | 2421736.9 1; 204020 1; 103134.5 1; 0 1 |
| SALES | category | 8 | 1 | 46669589 1; 3223123 1; 1896215 1; 0 1 |
| CUSTOMERS | category | 7 | 1 | 3477215 1; 233056 1; 157455 1; 0 1 |
| REVENUES_1 | amount | 8 | 1 | 1829429.9 1; 175093 1; 87962.1 1; 4002.2 1 |
| SALES_1 | category | 8 | 1 | 49826500 1; 5674061 1; 6128780 1; 77195 1 |
| CUSTOMERS_1 | category | 8 | 1 | 523112 1; 43845 1; 37485 1; 1230 1 |
| REVENUES_2 | amount | 8 | 1 | 650976 1; 35882 1; 42967.8 1; 2138.5 1 |
| SALES_2 | category | 8 | 1 | 65686094 1; 8231633 1; 2951868 1; 154797 1 |
| CUSTOMERS_2 | category | 8 | 1 | 10645 1; 102 1; 5189 1; 15 1 |
| REVENUES_3 | category | 5 | 1 | . 3; 0 2; 5207.8 1; 1771.7 1 |
| SALES_3 | category | 5 | 1 | . 3; 0 2; 156924 1; 59166 1 |
| CUSTOMERS_3 | category | 3 | 1 | . 3; 1 2; 0 2; Count 1 |
| REVENUES_4 | amount | 8 | 1 | 4907350.6 1; 414995 1; 234064.4 1; 6140.7 1 |
| SALES_4 | category | 8 | 1 | 162339107 1; 17128817 1; 10976863 1; 231992 1 |
| CUSTOMERS_4 | category | 8 | 1 | 4010973 1; 277003 1; 200129 1; 1245 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:54.09460 9 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 917cee52-7348-4d9f-9b96-4 9 |
| _SRC_FILE | who | 1 | 0 | Delivery_Companies_2024.x 9 |
