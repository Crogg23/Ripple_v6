# PORTAL_SOC_COLORADO_INFORMA_0637BE3AAC

rows 2.0K  columns 15  scan 2.0s

roles: audit 2, category 9, date 1, other 3, who 1

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

SRC_SHA256 by rows
      2.0K  f30779adf9b363471d4d30b709329087603f49771fdcefe41091e34fda445654

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  f30779adf9b363471d4d30b709329087603f4977  2026:2.0K

## what

MONTH: 2 19%, 3 19%, 4 19%, 5 19%, 6 19%, 1 6%, 7 0%

YEAR: 2025.0 100%, 2025 0%

SEQUENCENUMBER: 27.0 8%, 26.0 8%, 25.0 8%, 24.0 8%, 23.0 8%, 22.0 8%, 21.0 8%, 20.0 8%, 19.0 8%, 18.0 8%, 17.0 8%, 16.0 8%

NAICS: 61 8%, 722 8%, 721 8%, 71 8%, 62 8%, 56 8%, 54 8%, 53 8%, 52 8%, 51 8%, 48-49 8%, 459 8%

INDUSTRY: Educational Services 8%, Food Services and Drinking Pla 8%, Accommodation 8%, Arts Entertainment and Recreat 8%, Health Care and Social Assista 8%, Administrative and Support and 8%, Professional Scientific and Te 8%, Real Estate and Rental and Lea 8%, Finance and Insurance 8%, Information 8%, Transportation and Warehousing 8%, Sporting Goods Hobby Musical I 8%

CITY: Arvada 9%, Boulder 9%, Aurora 9%, Centennial 9%, Westminster 8%, Thornton 8%, Pueblo 8%, Longmont 8%, Lakewood 8%, Greeley 8%, Fort Collins 8%, Denver 8%

RETAILSALESBLANKCODE: nan 91%, NR 9%

NUMBEROFRETAILERSBLANKCODE: nan 100%, NR 0%

NUMBEROFRETURNSBLANKCODE: nan 100%, NR 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MONTH | category | 7 | 0 | 2 377; 3 377; 4 377; 5 377 |
| YEAR | category | 2 | 0 | 2025.0 2.0K; 2025 1 |
| SEQUENCENUMBER | category | 30 | 0 | 27.0 69; 26.0 69; 25.0 69; 24.0 69 |
| NAICS | category | 29 | 0 | 61 70; 722 69; 721 69; 71 69 |
| INDUSTRY | category | 29 | 0 | Educational Services 70; Food Services and Drinkin 69; Accommodation 69; Arts Entertainment and Re 69 |
| CITY | category | 13 | 0 | Arvada 175; Boulder 174; Aurora 174; Centennial 172 |
| NUMBEROFRETAILERS | other | 893 | 0 | 17 20; 10 19; 11 19; 5 19 |
| NUMBEROFRETURNS | other | 948 | 0 | 10 20; 27 20; 28 18; 23 17 |
| RETAILSALES | other | 1.8K | 0 | nan 179; 18056927 10; 3155372 10; 6107398 10 |
| RETAILSALESBLANKCODE | category | 2 | 0 | nan 1.8K; NR 179 |
| NUMBEROFRETAILERSBLANKCODE | category | 2 | 0 | nan 2.0K; NR 2 |
| NUMBEROFRETURNSBLANKCODE | category | 2 | 0 | nan 2.0K; NR 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:45:16.22132 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | b2ee5cfe-b052-4fb3-a4b6-b 2.0K |
| SRC_SHA256 | who | 1 | 0 | f30779adf9b363471d4d30b70 2.0K |
