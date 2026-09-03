# PORTAL_CKA_OPEN_DATA_SA_38DF78BD6D

rows 115  columns 13  scan 4.3s

roles: amount 3, audit 2, category 4, date 2, other 2, who 1

## when

CREATED_DATE
  2025       115  ##############################

INGESTED_AT
  2026       115  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SQMILES | 115 | 0.34 | 2.87 | 25.34 | 41.92 | 506.68 |
| SHAPE__AREA | 115 | 0 | 0 | 0.01 | 0.01 | 0.03 |
| SHAPE__LENGTH | 115 | 0.05 | 0.13 | 0.96 | 0.98 | 21.04 |

## who

SRC_SHA256 by rows
       115  004dca69f7af54b6aa5752d8719c79e03562cdaa5c2fd788b88f3108d50157b5

SRC_SHA256 by dollars
      506.68      115 rows  004dca69f7af54b6aa5752d8719c79e03562cdaa5c2fd788b88f3108d501

## who x when

SRC_SHA256 by CREATED_DATE, dollars = SQMILES
  004dca69f7af54b6aa5752d8719c79e03562cdaa  2025:506.68

## what

SUBSTN: SOUTH 17%, WEST 17%, NORTH 17%, PRUE 17%, EAST 16%, CENTRAL 9%, DOWNTOWN 7%

SECTION: 62 10%, 33 9%, 73 9%, 31 9%, 52 9%, 51 9%, 23 9%, 61 8%, 53 8%, 43 8%, 63 8%, 72 8%

SUBCODE: S 17%, W 17%, N 17%, P 17%, E 16%, C 9%, D 7%

WEBSITE: https://www.sanantonio.gov/SAP 17%, https://www.sanantonio.gov/SAP 17%, https://www.sanantonio.gov/SAP 17%, https://www.sanantonio.gov/SAP 17%, https://www.sanantonio.gov/SAP 16%, https://www.sanantonio.gov/SAP 16%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 114 | 0 | 115 1; 114 1; 113 1; 112 1 |
| SUBSTN | category | 7 | 0 | SOUTH 20; WEST 20; NORTH 20; PRUE 19 |
| SECTION | category | 19 | 0 | 62 8; 33 7; 73 7; 31 7 |
| DISTRICT | other | 116 | 0 | 6130 1; 6250 1; 6150 1; 6160 1 |
| SUBCODE | category | 7 | 0 | S 20; W 20; N 20; P 19 |
| SQMILES | amount | 117 | 0 | 0.53483231 1; 2.95958817 1; 3.25136496 1; 41.91626964 1 |
| WEBSITE | category | 6 | 0 | https://www.sanantonio.go 20; https://www.sanantonio.go 20; https://www.sanantonio.go 20; https://www.sanantonio.go 19 |
| CREATED_DATE | date | 1 | 0 | 11/17/2025 8:24:25 PM 115 |
| SHAPE__AREA | amount | 117 | 0 | 0.000128738982084542 1; 0.000712252961648119 1; 0.000782497210138899 1; 0.0100819715107718 1 |
| SHAPE__LENGTH | amount | 114 | 0 | 0.0485842283076662 1; 0.113368027607016 1; 0.115902996237608 1; 0.973901245811474 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:33:09.60018 115 |
| SOURCE_RUN_ID | audit | 1 | 0 | ea19c6d9-686d-444b-be8d-9 115 |
| SRC_SHA256 | who | 1 | 0 | 004dca69f7af54b6aa5752d87 115 |
