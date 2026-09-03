# XC_OWID_REFUGEES

rows 7.4K  columns 8  scan 1.9s

roles: audit 2, category 1, other 3, who 2

## who

ENTITY by rows
        74  Unknown Origin
        65  Angola
        64  Rwanda
        62  Guinea-Bissau
        62  Sudan
        61  Mozambique
        61  Democratic Republic of Congo
        61  Tibetan
        60  Albania
        59  Malawi
        59  South Africa
        58  Namibia
        58  Hungary
        58  Ethiopia
        57  Vietnam
        56  Russia
        55  Burundi
        54  China
        53  Serbia and Kosovo
        53  Bulgaria

SRC_SHA256 by rows
      7.4K  5ea8e1713a805c174503e81a1744bf270a4b99e03dd82541c3b9408ff6a8c830

## what

WORLD_REGION_ACCORDING_TO_OWID: Africa 33%, Asia 25%, Europe 19%, North America 12%, South America 7%, Oceania 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | who | 216 | 0 | Unknown Origin 77; Angola 65; Rwanda 64; Vietnam 62 |
| CODE | other | 212 | 233 | AGO 65; RWA 64; VNM 62; SDN 62 |
| YEAR | other | 75 | 0 | 2024 207; 2022 206; 2023 205; 2021 204 |
| REFUGEES_BY_COUNTRY_OF_ORIGIN | other | 4.2K | 0 | 5 297; 0 195; 10 77; 6 61 |
| WORLD_REGION_ACCORDING_TO_OWID | category | 7 | 233 | Africa 2.4K; Asia 1.8K; Europe 1.4K; North America 853 |
| INGESTED_AT | audit | 1 | 0 | 1782616848204728 7.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 220b0d57-1b8d-41e2-84ef-f 7.4K |
| SRC_SHA256 | who | 1 | 0 | 5ea8e1713a805c174503e81a1 7.4K |
