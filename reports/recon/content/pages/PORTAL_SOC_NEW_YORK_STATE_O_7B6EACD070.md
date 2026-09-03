# PORTAL_SOC_NEW_YORK_STATE_O_7B6EACD070

rows 2.0K  columns 13  scan 2.8s

roles: audit 2, category 2, date 1, id 1, other 4, who 4

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

SALES_TAX_YEAR by rows
      2.0K  2025 - 2026

SELLING_PERIOD by rows
      2.0K  December - February

DESCRIPTION by rows
         7  Other Crop Farming
         7  Other Fabricated Metal Product Manufacturing
         7  Bakeries and Tortilla Manufacturing
         7  Hunting and Trapping
         7  Electric Lighting Equipment Manufacturing
         7  Commercial and Service Industry Machinery Manufacturing
         7  Other Miscellaneous Manufacturing
         7  Office Furniture (including Fixtures) Manufacturing
         7  Apparel, Piece Goods, and Notions Merchant Wholesalers
         7  Grain and Oilseed Milling
         7  Nonresidential Building Construction
         7  Electric Power Generation, Transmission and Distribution
         7  Oil and Gas Extraction
         7  Petroleum and Petroleum Products Merchant Wholesalers
         7  Iron and Steel Mills and Ferroalloy Manufacturing
         7  Timber Tract Operations
         7  Metal and Mineral (except Petroleum) Merchant Wholesalers
         7  Sugar and Confectionery Product Manufacturing
         7  Resin, Synthetic Rubber, and Artificial and Synthetic Fibers and Filam
         7  Oilseed and Grain Farming

SRC_SHA256 by rows
      2.0K  14cd3b4e3ff6620901704127fd792c23a0218f92fe2675d76746675823b88ee6

## who x when

SALES_TAX_YEAR by INGESTED_AT  LOAD STAMP, not an event date
  2025 - 2026                               2026:2.0K

SELLING_PERIOD by INGESTED_AT  LOAD STAMP, not an event date
  December - February                       2026:2.0K

## what

JURISDICTION: CATTARAUGUS 15%, BROOME 15%, ALLEGANY 15%, ALBANY 15%, MCTD 15%, NY STATE 15%, CAYUGA 7%

JURISDICTION_SORT_ORDER: 6 15%, 5 15%, 4 15%, 3 15%, 2 15%, 1 15%, 7 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATUS | other | 1 | 0 | P 2.0K |
| SALES_TAX_YEAR | who | 1 | 0 | 2025 - 2026 2.0K |
| SELLING_PERIOD | who | 1 | 0 | December - February 2.0K |
| SALES_TAX_QUARTER | other | 1 | 0 | 4 2.0K |
| JURISDICTION | category | 7 | 0 | CATTARAUGUS 309; BROOME 309; ALLEGANY 309; ALBANY 309 |
| NAICS_INDUSTRY_GROUP | other | 308 | 0 | 4441 10; 4413 10; 4412 10; 4411 10 |
| DESCRIPTION | who | 310 | 0 | Building Material and Sup 10; Automotive Parts, Accesso 10; Other Motor Vehicle Deale 10; Automobile Dealers 10 |
| TAXABLE_SALES_AND_PURCHASES | other | 1.8K | 0 | nan 132; 5399 11; 17336478 10; 4288334 10 |
| JURISDICTION_SORT_ORDER | category | 7 | 0 | 6 309; 5 309; 4 309; 3 309 |
| ROW_UPDATE_INDICATOR | id | 2.0K | 0 | 7202644441 10; 7202644413 10; 7202644412 10; 7202644411 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:43:10.03087 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | f2a8ff01-2514-4d5b-8933-0 2.0K |
| SRC_SHA256 | who | 1 | 0 | 14cd3b4e3ff6620901704127f 2.0K |
