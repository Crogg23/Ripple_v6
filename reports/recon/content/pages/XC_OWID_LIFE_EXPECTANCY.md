# XC_OWID_LIFE_EXPECTANCY

rows 21.6K  columns 7  scan 3.5s

roles: amount 1, audit 2, other 2, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LIFE_EXPECTANCY | 21.6K | 10.99 | 64.48 | 82.69 | 86.37 | 1.34M |

## who

ENTITY by rows
       273  Sweden
       242  United Kingdom
       208  France
       190  Denmark
       186  Iceland
       178  Norway
       178  Belgium
       174  Netherlands
       159  Finland
       152  Italy
       148  Switzerland
       143  Jamaica
       125  United States
       123  Luxembourg
       121  Mexico
       119  Spain
       112  Canada
       109  England and Wales
       106  Australia
       100  Russia

ENTITY by dollars
       14.9K      273 rows  Sweden
       13.1K      242 rows  United Kingdom
       11.7K      208 rows  France
       11.6K      190 rows  Denmark
       11.5K      178 rows  Norway
       11.0K      186 rows  Iceland
       10.7K      174 rows  Netherlands
       10.5K      178 rows  Belgium
        9.7K      148 rows  Switzerland
        9.5K      159 rows  Finland
        9.1K      152 rows  Italy
        8.4K      125 rows  United States
        8.1K      123 rows  Luxembourg
        7.8K      112 rows  Canada
        7.8K      143 rows  Jamaica
        7.7K      119 rows  Spain
        7.7K      106 rows  Australia
        6.4K       93 rows  Japan
        6.4K      121 rows  Mexico
        6.3K       89 rows  Greece

SRC_SHA256 by rows
     21.6K  aef7addd2b324f091ea601c417ecc8be56e0bc784738d82851292d8e81df60e9

SRC_SHA256 by dollars
       1.34M    21.6K rows  aef7addd2b324f091ea601c417ecc8be56e0bc784738d82851292d8e81df

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | who | 268 | 0 | Sweden 347; United Kingdom 316; Switzerland 222; France 208 |
| CODE | other | 249 | 1.3K | SWE 347; GBR 316; CHE 222; FRA 208 |
| YEAR | other | 313 | 0 | 2023 261; 2022 261; 2021 261; 2020 261 |
| LIFE_EXPECTANCY | amount | 20.8K | 0 | 62.7748 108; 62.3601 108; 60.1347 108; 61.53 108 |
| INGESTED_AT | audit | 1 | 0 | 1782616868814672 21.6K |
| SOURCE_RUN_ID | audit | 1 | 0 | 32e7c8da-f038-4f15-a617-2 21.6K |
| SRC_SHA256 | who | 1 | 0 | aef7addd2b324f091ea601c41 21.6K |
