# FED_GOOGLE_POLADS_ADVERTISER_STATS

rows 21.2K  columns 29  scan 3.9s

roles: amount 13, audit 2, category 1, empty 1, id 1, other 9, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_CREATIVES | 21.2K | 1 | 6 | 706.25 | 274.6K | 1.56M |
| SPEND_USD | 21.2K | 0 | 2.0K | 1.64M | 100.72M | 2.50B |
| SPEND_INR | 21.2K | 0 | 0 | 232.1K | 2.46B | 9.12B |
| SPEND_GBP | 21.2K | 0 | 0 | 0 | 3.67M | 12.04M |
| SPEND_NZD | 21.2K | 0 | 0 | 0 | 1.00M | 3.35M |
| SPEND_ILS | 21.2K | 0 | 0 | 0 | 1.36M | 9.68M |

## who

ADVERTISER_NAME by rows
        12  Inmo Khang
         7  MAXWELL RYMER
         6  Nancy Liu
         5  Lovead Limited
         4  CIATTARELLI FOR GOVERNOR
         4  Nicholas Perhai
         3  Georgia Blue PAC, Inc.
         3  CATHY MCMORRIS RODGERS FOR CONGRESS
         3  MAGGIE FOR NH
         3  Friends for Kathy Hochul
         3  US House of Representatives
         3  Iowa Democratic Party
         3  Ryan O'Daniel
         3  LALOTA FOR CONGRESS
         3  PETER MEIJER FOR CONGRESS
         3  COLLINS FOR CONGRESS
         3  BECKER FOR CONGRESS
         3  DAN SCHWARTZ FOR CONGRESS
         3  SAM BROWN FOR NEVADA
         3  NIDA FOR NC

ADVERTISER_NAME by dollars
      274.6K        1 rows  Bharatiya Janata Party
       64.1K        1 rows  MIKE BLOOMBERG 2020 INC
       62.8K        1 rows  BIDEN FOR PRESIDENT
       38.1K        1 rows  KEVIN COMBS
       34.2K        1 rows  Money Metals Exchange LLC
       27.0K        1 rows  TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE
       23.0K        1 rows  DONALD J. TRUMP FOR PRESIDENT, INC.
       17.5K        1 rows  The Labour Party
       17.4K        1 rows  Sprizzy Media LLC
       14.0K        1 rows  HARRIS FOR PRESIDENT
       12.2K        1 rows  TILAK SHARMA
       12.2K        1 rows  JEXAN LLC
       10.0K        1 rows  Populus Empowerment Network Private Limited
        9.1K        1 rows  NRSC
        9.1K        1 rows  FF PAC
        8.7K        1 rows  MARKETFUEL SUBSCRIPTION SERVICES
        8.7K        1 rows  INDIAN PAC CONSULTING PRIVATE LIMITED
        8.2K        1 rows  PROGRESSNOW
        7.5K        1 rows  Juntos por el Cambio
        7.3K        1 rows  Indian National Congress

SRC_SHA256 by rows
     21.2K  b4de0c2647cdab05b29b428ebcb961964315c6e19a53362939aad3c717dab3c0

SRC_SHA256 by dollars
       1.56M    21.2K rows  b4de0c2647cdab05b29b428ebcb961964315c6e19a53362939aad3c717da

## what

REGIONS: US 76%, BR 10%, IN 4%, AR 4%, AU 2%, CL 1%, GB 1%, IL 1%, MX 1%, TW 1%, NZ 0%, ZA 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ADVERTISER_ID | id | 20.8K | 0 | AR18406687078403276801 107; AR14600099190781509633 107; AR08011618551263657985 107; AR12651855931726888961 107 |
| ADVERTISER_NAME | who | 20.6K | 0 | SHEDD FOR ATTORNEY GENERA 107; PRO - Propuesta Republica 107; ESTHER FOR CONGRESS 107; METACORP MEDIA PRIVATE LI 107 |
| PUBLIC_IDS_LIST | other | 13.8K | 6.3K | EIN ID 53-6002523 114; Registered in US-CA  92; Registered in US-NJ  76; Registered in US-GA  76 |
| REGIONS | category | 13 | 0 | US 16.1K; BR 2.1K; IN 880; AR 843 |
| ELECTIONS | empty | 0 | 21.2K |  |
| TOTAL_CREATIVES | amount | 672 | 0 | 1 3.3K; 2 2.4K; 3 1.8K; 4 1.4K |
| SPEND_USD | amount | 2.5K | 0 | 0 5.2K; 100 1.2K; 200 438; 300 386 |
| SPEND_EUR | other | 1 | 0 | 0 21.2K |
| SPEND_INR | amount | 415 | 0 | 0 20.3K; 250 153; 500 41; 750 34 |
| SPEND_BGN | other | 1 | 0 | 0 21.2K |
| SPEND_CZK | other | 1 | 0 | 0 21.2K |
| SPEND_DKK | other | 1 | 0 | 0 21.2K |
| SPEND_HUF | other | 1 | 0 | 0 21.2K |
| SPEND_PLN | other | 1 | 0 | 0 21.2K |
| SPEND_RON | other | 1 | 0 | 0 21.2K |
| SPEND_SEK | other | 1 | 0 | 0 21.2K |
| SPEND_GBP | amount | 80 | 0 | 0 21.1K; 50 23; 100 8; 300 7 |
| SPEND_NZD | amount | 40 | 0 | 0 21.1K; 200 9; 1000 7; 400 4 |
| SPEND_ILS | amount | 74 | 0 | 0 21.1K; 250 12; 1500 8; 1250 6 |
| SPEND_AUD | amount | 215 | 0 | 0 20.7K; 150 29; 3750 21; 6300 17 |
| SPEND_TWD | amount | 58 | 0 | 0 21.1K; 3000 24; 9000 7; 27000 5 |
| SPEND_BRL | amount | 298 | 0 | 0 19.1K; 500 302; 1000 161; 5000 103 |
| SPEND_ARS | amount | 344 | 0 | 0 20.4K; 15000 102; 45000 30; 30000 29 |
| SPEND_ZAR | amount | 10 | 0 | 0 21.2K; 15000 3; 30000 2; 360000 1 |
| SPEND_CLP | amount | 120 | 0 | 0 21.0K; 50000 18; 400000 7; 350000 7 |
| SPEND_MXN | amount | 88 | 0 | 0 21.1K; 1000 8; 4000 5; 2000 5 |
| INGESTED_AT | audit | 1 | 0 | 1785965602280091 21.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4141cf7d-a262-4c65-b58b-3 21.2K |
| SRC_SHA256 | who | 1 | 0 | b4de0c2647cdab05b29b428eb 21.2K |
