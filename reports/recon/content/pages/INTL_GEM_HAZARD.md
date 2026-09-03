# INTL_GEM_HAZARD

rows 12  columns 12  scan 2.4s

roles: audit 2, category 3, empty 4, other 1, who 2

## who

MODEL_VERSION by rows
        12  2023.1

_SRC_SHA256 by rows
        12  f09014583005ab506c4a9d27a7d7c21b0eab62ff9df0eb43f201fb1454e3365f

## what

COUNTRY: New Zealand 8%, India 8%, China 8%, Japan 8%, Southeast Asia 8%, Middle East 8%, Africa 8%, South America 8%, United States 8%, Europe 8%, Canada 8%, Australia 8%

HAZARD_MODEL_ID: NZL 8%, IND 8%, CHN 8%, JPN 8%, SEA 8%, MIE 8%, AFR 8%, SAM 8%, USA 8%, EUR 8%, CAN 8%, AUS 8%

DOI: 10.13117/NZLSHA23 8%, 10.13117/INDSHA23 8%, 10.13117/CHNSHA23 8%, 10.13117/JPNSHA23 8%, 10.13117/SEASHA23 8%, 10.13117/MIESHA23 8%, 10.13117/AFRSHA23 8%, 10.13117/SAMSHA23 8%, 10.13117/USASHA23 8%, 10.13117/EURSHA23 8%, 10.13117/CANSHA23 8%, 10.13117/AUSSHA23 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MODEL_VERSION | who | 1 | 0 | 2023.1 12 |
| COUNTRY | category | 12 | 0 | New Zealand 1; India 1; China 1; Japan 1 |
| FIPS | empty | 1 | 12 |  |
| LATITUDE | empty | 1 | 12 |  |
| LONGITUDE | empty | 1 | 12 |  |
| PGA_10PCT_50YR | empty | 1 | 12 |  |
| VS30 | other | 1 | 0 | 760 12 |
| HAZARD_MODEL_ID | category | 12 | 0 | NZL 1; IND 1; CHN 1; JPN 1 |
| DOI | category | 12 | 0 | 10.13117/NZLSHA23 1; 10.13117/INDSHA23 1; 10.13117/CHNSHA23 1; 10.13117/JPNSHA23 1 |
| _INGESTED_AT | audit | 1 | 0 | 1783023199761374 12 |
| _SOURCE_RUN_ID | audit | 1 | 0 | e181bc64-922a-471a-a2ab-4 12 |
| _SRC_SHA256 | who | 1 | 0 | f09014583005ab506c4a9d27a 12 |
