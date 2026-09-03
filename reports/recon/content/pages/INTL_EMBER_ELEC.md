# INTL_EMBER_ELEC

rows 369.3K  columns 21  scan 3.8s

roles: amount 3, audit 2, category 13, other 2, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 360.8K | -93.35 | 0.20 | 1.1K | 31.7K | 24.78M |
| YOY_ABSOLUTE_CHANGE | 265.9K | -500 | 0 | 55.12 | 1.5K | 515.8K |
| YOY___CHANGE | 170.2K | -51.3K | 0.70 | 168.33 | 24.0K | 1.86M |

## who

COUNTRY_OR_REGION by rows
      1.7K  Latin America and Caribbean
      1.7K  Colombia
      1.7K  Sweden
      1.7K  Portugal
      1.7K  G20
      1.7K  Belarus
      1.7K  Armenia
      1.7K  Austria
      1.7K  Ethiopia
      1.7K  Denmark
      1.7K  Turkey
      1.7K  France
      1.7K  Spain
      1.7K  Chile
      1.7K  Norway
      1.7K  Nigeria
      1.7K  Poland
      1.7K  Latvia
      1.7K  Moldova
      1.7K  Mongolia

COUNTRY_OR_REGION by dollars
       4.28M     1.7K rows  World
       3.56M     1.7K rows  G20
       1.94M     1.7K rows  OECD
       1.83M     1.7K rows  Asia
       1.39M     1.7K rows  G7
       1.02M     1.6K rows  China
      908.7K     1.7K rows  Europe
      874.9K     1.7K rows  North America
      765.6K     1.7K rows  United States of America
      517.3K     1.7K rows  EU
      300.8K     1.7K rows  Latin America and Caribbean
      249.5K     1.6K rows  India
      241.1K     1.7K rows  Middle East
      221.2K     1.6K rows  Japan
      210.3K     1.6K rows  Russian Federation (the)
      183.4K     1.7K rows  ASEAN
      164.2K     1.7K rows  Africa
      129.2K     1.7K rows  Germany
      124.3K     1.6K rows  Canada
      115.2K     1.6K rows  Brazil

## what

DATE: 2020 8%, 2021 8%, 2022 8%, 2019 8%, 2017 8%, 2018 8%, 2015 8%, 2016 8%, 2014 8%, 2013 8%, 2012 8%, 2023 8%

AREA_TYPE: Country or economy 94%, Region 6%

CONTINENT: Africa 25%, Asia 22%, Europe 19%, North America 15%, Oceania 7%, South America 7%, nan 6%

EMBER_REGION: Africa 25%, Latin America and Caribbean 20%, Europe 19%, Asia 15%, Oceania 7%, Middle East 6%, nan 6%, North America 1%

EU: 0.0 82%, 1.0 12%, nan 6%

OECD: 0.0 77%, 1.0 17%, nan 6%

G20: 0.0 86%, 1.0 8%, nan 6%

G7: 0.0 91%, nan 6%, 1.0 3%

ASEAN: 0.0 89%, nan 6%, 1.0 5%

CATEGORY: Electricity generation 47%, Power sector emissions 26%, Capacity 22%, Electricity demand 3%, Electricity imports 2%

SUBCATEGORY: Fuel 54%, Aggregate fuel 37%, Total 3%, CO2 intensity 2%, Demand 2%, Demand per capita 2%, Electricity imports 2%

VARIABLE: Fossil 8%, Gas and Other Fossil 8%, Hydro, Bioenergy and Other Ren 8%, Renewables 8%, Wind and Solar 8%, Clean 8%, Other Fossil 8%, Solar 8%, Bioenergy 8%, Hydro 8%, Coal 8%, Gas 8%

UNIT: TWh 27%, mtCO2 24%, % 23%, GW 22%, gCO2/kWh 2%, MWh 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTRY_OR_REGION | who | 223 | 0 | World 1.7K; Uzbekistan 1.7K; Uruguay 1.7K; United States of America 1.7K |
| ISO_3_CODE | other | 217 | 0 | nan 22.1K; UZB 1.7K; URY 1.7K; USA 1.7K |
| DATE | category | 26 | 0 | 2020 14.7K; 2021 14.7K; 2022 14.7K; 2019 14.7K |
| AREA_TYPE | category | 2 | 0 | Country or economy 347.2K; Region 22.1K |
| CONTINENT | category | 7 | 0 | Africa 91.7K; Asia 80.4K; Europe 69.8K; North America 54.8K |
| EMBER_REGION | category | 8 | 0 | Africa 91.7K; Latin America and Caribbe 74.2K; Europe 71.5K; Asia 56.0K |
| EU | category | 3 | 0 | 0.0 301.4K; 1.0 45.7K; nan 22.1K |
| OECD | category | 3 | 0 | 0.0 283.4K; 1.0 63.7K; nan 22.1K |
| G20 | category | 3 | 0 | 0.0 316.6K; 1.0 30.6K; nan 22.1K |
| G7 | category | 3 | 0 | 0.0 335.5K; nan 22.1K; 1.0 11.7K |
| ASEAN | category | 3 | 0 | 0.0 330.4K; nan 22.1K; 1.0 16.8K |
| CATEGORY | category | 5 | 0 | Electricity generation 173.9K; Power sector emissions 95.6K; Capacity 82.6K; Electricity demand 11.5K |
| SUBCATEGORY | category | 7 | 0 | Fuel 198.1K; Aggregate fuel 136.8K; Total 11.5K; CO2 intensity 5.7K |
| VARIABLE | category | 21 | 0 | Fossil 22.8K; Gas and Other Fossil 22.8K; Hydro, Bioenergy and Othe 22.8K; Renewables 22.8K |
| UNIT | category | 6 | 0 | TWh 101.3K; mtCO2 89.8K; % 84.1K; GW 82.6K |
| VALUE | amount | 27.2K | 0 | 0.0 128.7K; 0.01 9.9K; nan 8.4K; 0.02 5.3K |
| YOY_ABSOLUTE_CHANGE | amount | 9.6K | 0 | 0.0 133.5K; nan 103.4K; 0.01 12.8K; 0.02 6.2K |
| YOY___CHANGE | amount | 10.8K | 0 | nan 199.1K; 0.0 41.2K; 100.0 1.4K; 50.0 1.2K |
| _INGESTED_AT | audit | 1 | 0 | 1781748320650396 369.3K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 4fd2ff85-133d-41ef-8b0c-1 369.3K |
| _SRC_SHA256 | other | 1 | 0 | 0767d48e77d841df5493eb4cb 369.3K |
