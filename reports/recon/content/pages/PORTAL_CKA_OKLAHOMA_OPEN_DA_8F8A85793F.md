# PORTAL_CKA_OKLAHOMA_OPEN_DA_8F8A85793F

rows 347  columns 14  scan 5.6s

roles: amount 1, audit 2, category 2, date 3, other 4, who 3

## when

PURCHASE_DATE
  2024       347  ##############################

POST_DATE
  2024       347  ##############################

INGESTED_AT
  2026       347  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 330 | 3.79 | 108.98 | 2.4K | 4.5K | 105.8K |

## who

LAST_NAME by rows
        33  Hartsfield
        22  Kafka
        17  Wheeler
        17  Crenshaw
        15  Smith
        13  Card
        13  Toombs
        11  Dezort
        11  Allred
         9  Pratt
         9  Dunlap
         8  Carman
         8  White
         8  Cripe
         8  Ingram
         7  Luddington
         7  Hall
         6  Matt
         6  Brown
         6  Simmons

LAST_NAME by dollars
        8.2K        5 rows  Bentley
        7.4K       33 rows  Hartsfield
        5.7K        4 rows  Ashton
        5.5K       11 rows  Allred
        5.0K       15 rows  Smith
        5.0K       13 rows  Toombs
        5.0K        5 rows  Boso
        4.7K       11 rows  Dezort
        4.0K        5 rows  Mitchell
        4.0K       22 rows  Kafka
        4.0K        7 rows  Hall
        3.9K       13 rows  Card
        3.0K       17 rows  Crenshaw
        2.6K       17 rows  Wheeler
        2.6K        3 rows  Woodfork
        2.0K        3 rows  Lane
        2.0K        9 rows  Pratt
        1.9K        8 rows  Ingram
        1.7K        7 rows  Luddington
        1.7K        6 rows  Underwood

MCC_DESCRIPTION by rows
       137  BOOK STORES
        18  GROCERY STORES, SUPERMARKETS
        12  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
        12  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
         9  EMBASSY SUITES
         9  HARDWARE STORES
         8  ADVERTISING SERVICES
         8  CHARITABLE AND SOCIAL SERVICE ORGANIZATI
         8  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
         7  LARGE DIGITAL GOODS MERCHANT
         7  POSTAGE STAMPS
         7  LODGING, HOTELS, MOTELS, RESORTS
         6  MISCELLANEOUS AUTOMOTIVE DEALERS
         6  MISCELLANEOUS AND RETAIL STORES
         6  WYNDHAM
         5  BEST WESTERN HOTELS
         4  COMPUTER SOFTWARE STORES
         4  TOLLS, ROAD AND BRIDGE FEES
         4  VARIETY STORES
         4  COMPUTERS,COMPUTER PERIPHERAL EQUIPMENT,

MCC_DESCRIPTION by dollars
       27.4K      137 rows  BOOK STORES
        7.4K        7 rows  LODGING, HOTELS, MOTELS, RESORTS
        6.4K        2 rows  DURABLE GOODS,NOT ELSEWHERE CLASSIFIED
        6.2K       12 rows  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
        5.6K        9 rows  EMBASSY SUITES
        4.8K        6 rows  MISCELLANEOUS AUTOMOTIVE DEALERS
        3.8K        2 rows  TELECOMMUNICATION EQUIPMENT INCLUDING TE
        3.2K        6 rows  MISCELLANEOUS AND RETAIL STORES
        2.7K        8 rows  CHARITABLE AND SOCIAL SERVICE ORGANIZATI
        2.6K       18 rows  GROCERY STORES, SUPERMARKETS
        2.4K        5 rows  BEST WESTERN HOTELS
        2.2K        8 rows  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
        2.2K        4 rows  HOME SUPPLY WAREHOUSE STORES
        1.9K        2 rows  HILTON INTERNATIONAL
        1.6K        1 rows  SPORTING GOODS STORES
        1.6K       12 rows  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
        1.6K        1 rows  SHOE STORES
        1.5K        9 rows  HARDWARE STORES
        1.3K        3 rows  RESIDENCE INN
        1.3K        2 rows  FAST FOOD RESTAURANTS

SRC_SHA256 by rows
       347  c5e8f13e158ff8ce43879f5919224317a8e1ede6ed4b1bba517cb40cbbc240f2

SRC_SHA256 by dollars
      105.8K      347 rows  c5e8f13e158ff8ce43879f5919224317a8e1ede6ed4b1bba517cb40cbbc2

## who x when

LAST_NAME by PURCHASE_DATE, dollars = AMOUNT
  Allred                                    2024:5.5K
  Ashton                                    2024:5.7K
  Bentley                                   2024:8.2K
  Boso                                      2024:5.0K
  Brown                                     2024:1.4K
  Card                                      2024:3.9K
  Carman                                    2024:501.62
  Crenshaw                                  2024:3.0K
  Cripe                                     2024:842.67
  Dezort                                    2024:4.7K
  Dunlap                                    2024:481.83
  Hall                                      2024:4.0K
  Hartsfield                                2024:7.4K
  Ingram                                    2024:1.9K
  Kafka                                     2024:4.0K
  Lane                                      2024:2.0K
  Luddington                                2024:1.7K
  Matt                                      2024:1.4K
  Mitchell                                  2024:4.0K
  Pratt                                     2024:2.0K
  Simmons                                   2024:468.19
  Smith                                     2024:5.0K
  Toombs                                    2024:5.0K
  Underwood                                 2024:1.7K
  Wheeler                                   2024:2.6K
  White                                     2024:1.2K
  Woodfork                                  2024:2.6K

MCC_DESCRIPTION by PURCHASE_DATE, dollars = AMOUNT
  ADVERTISING SERVICES                      2024:115
  BEST WESTERN HOTELS                       2024:2.4K
  BOOK STORES                               2024:27.4K
  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI  2024:6.2K
  CHARITABLE AND SOCIAL SERVICE ORGANIZATI  2024:2.7K
  COMPUTER SOFTWARE STORES                  2024:1.1K
  COMPUTERS,COMPUTER PERIPHERAL EQUIPMENT,  2024:666.19
  DURABLE GOODS,NOT ELSEWHERE CLASSIFIED    2024:6.4K
  EMBASSY SUITES                            2024:5.6K
  FAST FOOD RESTAURANTS                     2024:1.3K
  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI  2024:1.6K
  GROCERY STORES, SUPERMARKETS              2024:2.6K
  HARDWARE STORES                           2024:1.5K
  HILTON INTERNATIONAL                      2024:1.9K
  HOME SUPPLY WAREHOUSE STORES              2024:2.2K
  LARGE DIGITAL GOODS MERCHANT              2024:284.54
  LODGING, HOTELS, MOTELS, RESORTS          2024:7.4K
  MISCELLANEOUS AND RETAIL STORES           2024:3.2K
  MISCELLANEOUS AUTOMOTIVE DEALERS          2024:4.8K
  POSTAGE STAMPS                            2024:1.2K
  RESIDENCE INN                             2024:1.3K
  SHOE STORES                               2024:1.6K
  SPORTING GOODS STORES                     2024:1.6K
  TELECOMMUNICATION EQUIPMENT INCLUDING TE  2024:3.8K
  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D  2024:2.2K
  TOLLS, ROAD AND BRIDGE FEES               2024:71.71
  VARIETY STORES                            2024:569.18
  WYNDHAM                                   2024:569.90

## what

BUSINESS_UNIT: WOODWARD COUNTY 20%, PITTSBURG COUNTY 16%, BRYAN COUNTY OK 13%, GRANT COUNTY OKLAHOMA 11%, LINCOLN COUNTY OK 8%, CLEVELAND COUNTY 6%, OKLAHOMA COUNTY 6%, WAGONER COUNTY OK 5%, MCINTOSH COUNTY 5%, JACKSON COUNTY OK 4%, COUNTY OF JOHNSTON 4%, CHEROKEE COUNTY 2%

CH_INITIAL: C 18%, B 17%, S 14%, K 10%, M 9%, L 7%, J 7%, D 6%, T 4%, W 3%, A 3%, P 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CALENDAR_YEAR | other | 1 | 0 | 2024 347 |
| MONTH | other | 1 | 0 | 7 347 |
| BUSINESS_UNIT | category | 16 | 0 | WOODWARD COUNTY 65; PITTSBURG COUNTY 52; BRYAN COUNTY OK 43; GRANT COUNTY OKLAHOMA 38 |
| LAST_NAME | who | 65 | 1 | Hartsfield 33; Kafka 22; Crenshaw 17; Wheeler 17 |
| CH_INITIAL | category | 16 | 1 | C 60; B 57; S 47; K 34 |
| ITEM_DESCRIPTION | other | 281 | 0 | SECRETARY OF STATE - Purc 8; AMAZON MKTPLACE PMTS - Cr 8; IAAO ORG - Purchase 5; WM SUPERCENTER #975 - Pur 4 |
| AMOUNT | amount | 310 | 0 | $10.00  9; $99.99  4; $10.40  4; $20.80  3 |
| MERCHANT | other | 277 | 0 | SECRETARY OF STATE 8; AMAZON MKTPLACE PMTS 8; IAAO ORG 5; WM SUPERCENTER #975 4 |
| PURCHASE_DATE | date | 35 | 0 | 7/18/2024 25; 7/19/2024 22; 7/3/2024 20; 7/1/2024 20 |
| POST_DATE | date | 23 | 0 | 7/22/2024 29; 7/15/2024 24; 7/4/2024 23; 7/19/2024 23 |
| MCC_DESCRIPTION | who | 61 | 0 | BOOK STORES 137; GROCERY STORES, SUPERMARK 18; GOVERNMENT SERVICES NOT E 12; BUSINESS SERVICES NOT ELS 12 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:19:45.41465 347 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2a1c4ee7-1d07-4c59-a75b-9 347 |
| SRC_SHA256 | who | 1 | 0 | c5e8f13e158ff8ce43879f591 347 |
