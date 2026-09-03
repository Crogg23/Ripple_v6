# INTL_FAO_FAOSTAT

rows 69  columns 11  scan 3.4s

roles: audit 2, date 1, other 5, who 3

## when

DATEUPDATE
  1991         1  #
  2014         1  #
  2016         1  #
  2020         1  #
  2021         3  ###
  2022         1  #
  2023         1  #
  2024         1  #
  2025        35  ##############################
  2026        24  #####################

## who

DATASETNAME by rows
         1  Discontinued archives and data series: Producer Prices (old series)
         1  Food Balances: Commodity Balances (non-food) (-2013, old methodology)
         1  Land, Inputs and Sustainability: Fertilizers by Nutrient
         1  Prices: Deflators
         1  Food Balances: Supply Utilization Accounts (2010-)
         1  Cost and Affordability of a Healthy Diet: Cost and Affordability of a 
         1  Prices: Consumer Price Indices
         1  Land, Inputs and Sustainability: Livestock Manure
         1  Macro-Economic Indicators: Capital Stock
         1  Food Value Chain: Value shares by industry and primary factors
         1  Gender: Suite of Gender Indicators
         1  Production: Value of Agricultural Production
         1  Land, Inputs and Sustainability: Livestock Patterns
         1  Discontinued archives and data series: Machinery Archive
         1  Discontinued archives and data series: Food Aid Shipments (WFP)
         1  Food Balances: Commodity Balances (non-food) (2010-)
         1  Land, Inputs and Sustainability: Pesticides Trade
         1  Food and Diet: Availability (based on supply utilization accounts)
         1  Prices: Producer Prices
         1  Food Balances: Food Balances (-2013, old methodology and population)

FILEROWS by rows
         1  312259
         1  161088
         1  168405
         1  1184986
         1  11615212
         1  2191084
         1  428963
         1  2500090
         1  1166330
         1  146834
         1  590512
         1  17270631
         1  2829802
         1  4209110
         1  104860
         1  13020275
         1  52410630
         1  256389
         1  743139
         1  198208

_SRC_SHA256 by rows
        69  dc9e534f0b5698d94b789645a852cdf6cc2589f76db0c55aaff43cda7b433f9a

## who x when

DATASETNAME by DATEUPDATE
  Cost and Affordability of a Healthy Diet  2025:1
  Discontinued archives and data series: F  2016:1
  Discontinued archives and data series: M  2021:1
  Discontinued archives and data series: P  1991:1
  Food Balances: Commodity Balances (non-f  2021:1
  Food Balances: Commodity Balances (non-f  2026:1
  Food Balances: Food Balances (-2013, old  2023:1
  Food Balances: Supply Utilization Accoun  2025:1
  Food Value Chain: Value shares by indust  2024:1
  Food and Diet: Availability (based on su  2025:1
  Gender: Suite of Gender Indicators        2026:1
  Land, Inputs and Sustainability: Fertili  2025:1
  Land, Inputs and Sustainability: Livesto  2025:1
  Land, Inputs and Sustainability: Livesto  2025:1
  Land, Inputs and Sustainability: Pestici  2025:1
  Macro-Economic Indicators: Capital Stock  2025:1
  Prices: Consumer Price Indices            2026:1
  Prices: Deflators                         2025:1
  Prices: Producer Prices                   2026:1
  Production: Value of Agricultural Produc  2026:1

FILEROWS by DATEUPDATE
  104860                                    2025:1
  11615212                                  2025:1
  1166330                                   2025:1
  1184986                                   2021:1
  13020275                                  2025:1
  146834                                    2021:1
  161088                                    2024:1
  168405                                    2026:1
  17270631                                  2025:1
  198208                                    2025:1
  2191084                                   2025:1
  2500090                                   2025:1
  256389                                    2026:1
  2829802                                   2022:1
  312259                                    2025:1
  4209110                                   2025:1
  428963                                    2025:1
  52410630                                  2025:1
  590512                                    2026:1
  743139                                    2025:1

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATASETCODE | other | 69 | 0 | WCAD 1; TM 1; TI 1; TCLI 1 |
| DATASETNAME | who | 70 | 0 | World Census of Agricultu 1; Trade: Detailed trade mat 1; Trade: Trade Indices 1; Trade: Crops and livestoc 1 |
| TOPIC | other | 54 | 12 | FAO strives to provide da 2; FAO strives to provide da 2; Most crop and livestock p 2; Data is disseminated for  2 |
| DATASETDESCRIPTION | other | 66 | 3 | The food and agricultural 3; The FAOSTAT Employment in 2; Food Balance Sheet presen 2; Data from censuses of agr 1 |
| DATEUPDATE | date | 39 | 0 | 2025-10-28T00:00:00 14; 2025-12-23T00:00:00 4; 2026-06-17T00:00:00 3; 2021-12-03T00:00:00 3 |
| FILELOCATION | other | 68 | 0 | https://bulks-faostat.fao 1; https://bulks-faostat.fao 1; https://bulks-faostat.fao 1; https://bulks-faostat.fao 1 |
| FILESIZE | other | 70 | 0 | 378KB 1; 410792KB 1; 66519KB 1; 834KB 1 |
| FILEROWS | who | 70 | 0 | 28565 1; 52410630 1; 10406391 1; 116294 1 |
| _INGESTED_AT | audit | 1 | 0 | 1783286097037588 69 |
| _SOURCE_RUN_ID | audit | 1 | 0 | c655b9e7-00d9-461b-be12-4 69 |
| _SRC_SHA256 | who | 1 | 0 | dc9e534f0b5698d94b789645a 69 |
