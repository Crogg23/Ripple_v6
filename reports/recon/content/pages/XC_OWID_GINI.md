# XC_OWID_GINI

rows 2.4K  columns 8  scan 2.2s

roles: amount 1, audit 2, category 1, other 2, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GINI_COEFFICIENT | 2.4K | 0.18 | 0.35 | 0.60 | 0.71 | 893.09 |

## who

ENTITY by rows
        62  United States
        54  United Kingdom
        46  Canada
        40  Brazil
        39  Luxembourg
        39  Costa Rica
        38  Italy
        36  Argentina (urban)
        33  France
        33  Indonesia
        32  Honduras
        32  Germany
        32  Spain
        30  Thailand
        30  Panama
        30  Dominican Republic
        29  Sweden
        29  El Salvador
        29  Georgia
        28  Peru

ENTITY by dollars
       24.08       62 rows  United States
       22.39       40 rows  Brazil
       18.50       39 rows  Costa Rica
       17.57       54 rows  United Kingdom
       17.02       32 rows  Honduras
       16.35       36 rows  Argentina (urban)
       15.99       30 rows  Panama
       15.18       46 rows  Canada
       14.12       26 rows  Colombia
       13.94       30 rows  Dominican Republic
       13.91       28 rows  Paraguay
       13.22       29 rows  El Salvador
       13.05       28 rows  Peru
       12.87       38 rows  Italy
       12.66       26 rows  Ecuador
       12.40       25 rows  Bolivia
       12.01       39 rows  Luxembourg
       11.82       30 rows  Thailand
       11.14       33 rows  Indonesia
       11.05       32 rows  Spain

SRC_SHA256 by rows
      2.4K  8fcebbf5505b7e0a2c7e831785cdc2800cb402b00e64cf55ebb386065c59a168

SRC_SHA256 by dollars
      893.09     2.4K rows  8fcebbf5505b7e0a2c7e831785cdc2800cb402b00e64cf55ebb386065c59

## what

WORLD_REGION_ACCORDING_TO_OWID: Europe 42%, Asia 21%, North America 14%, Africa 12%, South America 10%, Oceania 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | who | 184 | 0 | United States 62; United Kingdom 54; Canada 46; Brazil 40 |
| CODE | other | 172 | 109 | USA 62; GBR 54; CAN 46; BRA 40 |
| YEAR | other | 63 | 0 | 2018 96; 2015 88; 2012 88; 2010 86 |
| GINI_COEFFICIENT | amount | 2.4K | 0 | 0.5025644898414612 12; 0.4433708190917969 12; 0.4315357506275177 12; 0.5148494839668274 12 |
| WORLD_REGION_ACCORDING_TO_OWID | category | 7 | 109 | Europe 957; Asia 471; North America 320; Africa 269 |
| INGESTED_AT | audit | 1 | 0 | 1782616844119000 2.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | da679e90-c70b-410b-bbc9-2 2.4K |
| SRC_SHA256 | who | 1 | 0 | 8fcebbf5505b7e0a2c7e83178 2.4K |
