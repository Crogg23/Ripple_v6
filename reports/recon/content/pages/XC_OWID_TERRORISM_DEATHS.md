# XC_OWID_TERRORISM_DEATHS

rows 10.5K  columns 8  scan 2.1s

roles: audit 2, category 1, other 3, who 2

## who

ENTITY by rows
        51  Angola
        51  Barbados
        51  Cyprus
        51  Saint Lucia
        51  Honduras
        51  Jordan
        51  Kenya
        51  Ecuador
        51  Gambia
        51  Malawi
        51  South Sudan
        51  Malaysia
        51  India
        51  Jamaica
        51  Nepal
        51  Kuwait
        51  Myanmar
        51  Iran
        51  Brazil
        51  Algeria

SRC_SHA256 by rows
     10.5K  c209d180ec2d4a42593db03aff7d27d81e9612e9fac5ae2d4e0b5aaa04541b41

## what

WORLD_REGION_ACCORDING_TO_OWID: Africa 29%, Asia 25%, Europe 21%, North America 13%, South America 8%, Oceania 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | who | 224 | 0 | Zimbabwe 81; Zambia 81; Zaire 81; Yemen Arab Republic 81 |
| CODE | other | 204 | 912 | ZWE 70; ZMB 67; OWID_YAR 51; YEM 51 |
| YEAR | other | 51 | 0 | 2020 216; 2019 216; 2018 216; 2017 216 |
| FATALITIES | other | 842 | 0 | 0 6.9K; 1 496; 2 277; 3 160 |
| WORLD_REGION_ACCORDING_TO_OWID | category | 7 | 1.3K | Africa 2.6K; Asia 2.3K; Europe 1.9K; North America 1.2K |
| INGESTED_AT | audit | 1 | 0 | 1782616860066605 10.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4326f7b7-eab2-4422-8ef3-2 10.5K |
| SRC_SHA256 | who | 1 | 0 | c209d180ec2d4a42593db03af 10.5K |
