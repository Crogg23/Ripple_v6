# XC_OWID_FOSSIL_SHARE

rows 6.4K  columns 7  scan 2.7s

roles: amount 1, audit 2, other 2, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FOSSIL_FUELS | 6.4K | 13.87 | 90.36 | 100 | 100 | 549.0K |

## who

ENTITY by rows
        60  Denmark
        60  China
        60  Cyprus
        60  Japan
        60  Canada
        60  United Kingdom
        60  Singapore
        60  Colombia
        60  Belgium
        60  Other South America (EI)
        60  Oceania
        60  Europe (EI)
        60  New Zealand
        60  CIS (EI)
        60  Other Asia Pacific (EI)
        60  Austria
        60  Iceland
        60  Indonesia
        60  United Arab Emirates
        60  Trinidad and Tobago

ENTITY by dollars
        6.0K       60 rows  Kuwait
        6.0K       60 rows  Saudi Arabia
        6.0K       60 rows  Qatar
        6.0K       60 rows  Oman
        6.0K       60 rows  Trinidad and Tobago
        6.0K       60 rows  Hong Kong
        6.0K       60 rows  Singapore
        6.0K       60 rows  Other Northern Africa (EI)
        6.0K       60 rows  United Arab Emirates
        6.0K       60 rows  Israel
        5.9K       60 rows  Algeria
        5.9K       60 rows  Middle East (EI)
        5.9K       60 rows  Cyprus
        5.9K       60 rows  Poland
        5.9K       60 rows  South Africa
        5.9K       60 rows  Luxembourg
        5.8K       60 rows  Iran
        5.8K       60 rows  Iraq
        5.8K       60 rows  Other Middle East (EI)
        5.8K       60 rows  Netherlands

SRC_SHA256 by rows
      6.4K  daa0f183831840e63a46a6214071bf41a277031c19ae566cd29f4528898183ca

SRC_SHA256 by dollars
      549.0K     6.4K rows  daa0f183831840e63a46a6214071bf41a277031c19ae566cd29f45288981

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | who | 112 | 0 | World 60; Western Africa (EI) 60; Vietnam 60; Venezuela 60 |
| CODE | other | 93 | 1.2K | OWID_WRL 60; VNM 60; VEN 60; OWID_UMC 60 |
| YEAR | other | 60 | 0 | 2024 111; 2023 111; 2022 111; 2021 111 |
| FOSSIL_FUELS | amount | 6.0K | 0 | 100 370; 81.25719 31; 82.14785 31; 82.57288 31 |
| INGESTED_AT | audit | 1 | 0 | 1782616864369314 6.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8b8b615c-9712-4092-9f5e-e 6.4K |
| SRC_SHA256 | who | 1 | 0 | daa0f183831840e63a46a6214 6.4K |
