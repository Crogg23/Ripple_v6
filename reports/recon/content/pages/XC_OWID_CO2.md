# XC_OWID_CO2

rows 29.4K  columns 7  scan 2.2s

roles: audit 2, other 3, who 2

## who

ENTITY by rows
       275  Asia (excl. China and India)
       275  Oceania
       275  World
       275  New Zealand
       275  Australia
       275  High-income countries
       275  European Union (28)
       275  Asia
       275  Norway
       275  United Kingdom
       275  Europe (excl. EU-27)
       275  Europe
       275  Taiwan
       275  Europe (excl. EU-28)
       240  Canada
       240  North America (excl. USA)
       240  North America
       233  European Union (27)
       233  Germany
       225  Poland

SRC_SHA256 by rows
     29.4K  71620dbdbc25480e8dc6c6751c4e8f474fe2760d36905bbfa316ab5cf1acc948

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | who | 248 | 0 | World 350; United Kingdom 346; Taiwan 331; United States 298 |
| CODE | other | 229 | 3.3K | OWID_WRL 341; GBR 330; TWN 306; USA 281 |
| YEAR | other | 272 | 0 | 2024 247; 2023 247; 2022 247; 2021 247 |
| ANNUAL_CO_EMISSIONS | other | 22.0K | 0 | 0 1.1K; 3664 275; 10992 199; 7328 167 |
| INGESTED_AT | audit | 1 | 0 | 1782616832708260 29.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 728c082f-b2cd-4cde-a2d9-c 29.4K |
| SRC_SHA256 | who | 1 | 0 | 71620dbdbc25480e8dc6c6751 29.4K |
