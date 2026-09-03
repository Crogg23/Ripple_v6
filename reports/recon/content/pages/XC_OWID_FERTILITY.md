# XC_OWID_FERTILITY

rows 19.4K  columns 7  scan 2.5s

roles: amount 1, audit 2, other 2, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_FERTILITY_RATE | 19.4K | 0.66 | 3.47 | 7.79 | 8.86 | 76.4K |

## who

ENTITY by rows
       133  Sweden
       108  Denmark
       103  Canada
       102  Spain
        92  Switzerland
        91  United States
        85  Finland
        84  Portugal
        78  France
        77  Japan
        77  Belgium
        77  Bulgaria
        74  Iceland
        74  Sint Maarten (Dutch part)
        74  Gambia
        74  Singapore
        74  Azerbaijan
        74  Gibraltar
        74  Senegal
        74  Saudi Arabia

ENTITY by dollars
      557.14       74 rows  Niger
      535.11       74 rows  Somalia
      529.12       74 rows  Yemen
      520.13       74 rows  Afghanistan
      510.82       74 rows  Mali
      502.31       74 rows  Burundi
      499.78       74 rows  Chad
      498.57       74 rows  Rwanda
      495.28       74 rows  Angola
      489.70       74 rows  Cote d'Ivoire
      487.87       74 rows  South Sudan
      485.70       74 rows  Uganda
      473.49       74 rows  Democratic Republic of Congo
      469.11       74 rows  Ethiopia
      468.60       74 rows  Malawi
      468.06       74 rows  Burkina Faso
      466.19       74 rows  Zambia
      465.56       74 rows  Palestine
      458.25       74 rows  Nigeria
      456.96       74 rows  Kenya

SRC_SHA256 by rows
     19.4K  4a1efe8bd6cc1165e3a09ad8bf1b615f97bcb4519678f8f90c6886a6de4402ac

SRC_SHA256 by dollars
       76.4K    19.4K rows  4a1efe8bd6cc1165e3a09ad8bf1b615f97bcb4519678f8f90c6886a6de44

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | who | 264 | 0 | Sweden 207; Spain 176; Switzerland 166; United States 165 |
| CODE | other | 257 | 387 | SWE 207; ESP 176; CHE 166; USA 165 |
| YEAR | other | 134 | 0 | 2023 259; 2022 259; 2021 259; 2020 259 |
| TOTAL_FERTILITY_RATE | amount | 6.6K | 0 | 1 167; 4.567 98; 6.942 98; 7.231 98 |
| INGESTED_AT | audit | 1 | 0 | 1782616851977494 19.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | d111dfbe-8d28-4912-bc5b-1 19.4K |
| SRC_SHA256 | who | 1 | 0 | 4a1efe8bd6cc1165e3a09ad8b 19.4K |
