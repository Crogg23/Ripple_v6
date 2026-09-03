# PORTAL_CKA_WPRDC_ALLEGHENY_3CED3B9382

rows 48  columns 26  scan 4.3s

roles: amount 11, audit 2, category 11, date 2, who 1

## when

TREASURY_SALE_DATE
  2026        48  ##############################

INGESTED_AT
  2026        48  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_TAX_DUE | 48 | 27.42 | 6.0K | 290.2K | 411.5K | 1.46M |
| CITY_TAX_DUE | 48 | 26.22 | 1.3K | 83.8K | 130.8K | 317.4K |
| COUNTY_TAX_DUE | 48 | 0 | 1.6K | 71.4K | 95.1K | 335.1K |
| SCHOOL_TAX_DUE | 48 | 0 | 953.50 | 128.8K | 182.4K | 523.1K |
| LIBRARY_TAX_DUE | 48 | 0.10 | 26.29 | 7.7K | 12.7K | 17.0K |
| PWSA_TAX_DUE | 48 | 0 | 546.02 | 45.0K | 74.7K | 146.0K |

## who

SRC_SHA256 by rows
        48  5d89171997369474787ce5c314b4df3607797549671e4d6b6951c23957def7b4

SRC_SHA256 by dollars
       1.46M       48 rows  5d89171997369474787ce5c314b4df3607797549671e4d6b6951c23957de

## who x when

SRC_SHA256 by TREASURY_SALE_DATE, dollars = TOTAL_TAX_DUE
  5d89171997369474787ce5c314b4df3607797549  2026:1.46M

## what

PIN: 0027B00283000000 8%, 0009M00154000300 8%, 0045B00189000000 8%, 0046K00210000000 8%, 0046K00209000000 8%, 0013N00113000000 8%, 0033B00005000000 8%, 0035D00117000000 8%, 0012F00127000000 8%, 0003D00050000000 8%, 0013G00050000000 8%, 0014K00169000000 8%

ADDRESS: EWING ST, PITTSBURGH, PA 15224 32%, LAFAYETTE AVE, PITTSBURGH, PA  9%, CHALFONT ST, PITTSBURGH, PA 15 9%, 1217 CHARTIERS AVE, PITTSBURGH 9%, 3060 MERWYN AVE, PITTSBURGH, P 9%, CHEROKEE ST, PITTSBURGH, PA 15 5%, 1848 ARCENA ST, PITTSBURGH, PA 5%, 2800 MCDOWELL ST, PITTSBURGH,  5%, 480 DAWES ST, PITTSBURGH, PA 1 5%, 339 MATHEWS AVE, PITTSBURGH, P 5%, 1506 ORANGEWOOD AVE, PITTSBURG 5%, 1925 E CARSON ST, PITTSBURGH,  5%

TREASURY_SALE_FLAG: Y 65%, N 35%

NEIGHBORHOOD_NAME: Sheraden 23%, Lower Lawrenceville 18%, Crafton Heights 13%, Lincoln-Lemington-Belmar 10%, Perry South 5%, Knoxville 5%, South Side Flats 5%, Beltzhoover 5%, Hazelwood 5%, Elliott 5%, Upper Hill 3%, Crawford-Roberts 3%

COUNCIL_DISTRICT: 2 33%, 3 19%, 7 17%, 9 15%, 6 10%, 5 4%, 4 2%

WARD: 20 29%, 9 18%, 12 9%, 18 7%, 13 7%, 28 7%, 26 4%, 16 4%, 30 4%, 17 4%, 15 4%, 5 2%

POLICE_ZONE: 6 35%, 2 19%, 3 19%, 5 17%, 1 6%, 4 4%

FIRE_ZONE: 1-16 22%, 3-6 20%, 3-18 10%, 1-17 10%, 1-18 8%, 1-10 5%, 4-24 5%, 4-16 5%, 3-17 5%, 2-13 5%, 2-22 2%, 2-1 2%

DPW_STREETS: 5 38%, 1 21%, 4 17%, 2 17%, 3 8%

DPW_ENVIRO: Northern 40%, Central 21%, Southern 21%, Eastern 19%

DPW_PARKS: Emerald 35%, Highland 25%, McKinley 19%, Frick 10%, Riverview 6%, Schenley 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PIN | category | 48 | 0 | 0027B00283000000 1; 0009M00154000300 1; 0045B00189000000 1; 0046K00210000000 1 |
| ADDRESS | category | 38 | 0 | EWING ST, PITTSBURGH, PA  7; LAFAYETTE AVE, PITTSBURGH 2; CHALFONT ST, PITTSBURGH,  2; 1217 CHARTIERS AVE, PITTS 2 |
| TREASURY_SALE_DATE | date | 1 | 0 | 2026-06-05 48 |
| TREASURY_SALE_FLAG | category | 2 | 0 | Y 31; N 17 |
| TOTAL_TAX_DUE | amount | 47 | 0 | 512.69 2; 50135.84 1; 14835.01 1; 7245.96 1 |
| CITY_TAX_DUE | amount | 47 | 0 | 26.22 2; 10792.48 1; 2418.0 1; 564.2 1 |
| COUNTY_TAX_DUE | amount | 41 | 0 | 0.0 8; 12645.71 1; 2378.46 1; 811.51 1 |
| SCHOOL_TAX_DUE | amount | 40 | 0 | 0.0 9; 22962.35 1; 1838.17 1; 29.19 1 |
| LIBRARY_TAX_DUE | amount | 46 | 0 | 11.49 2; 0.1 2; 149.74 1; 75.0 1 |
| PWSA_TAX_DUE | amount | 29 | 0 | 0.0 15; 486.17 5; 3561.91 1; 7975.38 1 |
| PARKS_TAX_DUE | amount | 43 | 0 | 6.0 4; 0.0 2; 0.2 2; 23.65 1 |
| DEMO_COST_DUE | amount | 5 | 0 | 0 44; 49950 1; 52000 1; 7300 1 |
| CLEAN_LIEN_DUE | amount | 13 | 0 | 0.0 36; 498.0 1; 400.53 1; 814.67 1 |
| LATITUDE | amount | 47 | 0 | 40.4514668867115 1; 40.44717967938591 1; 40.47068329192621 1; 40.465411710639145 1 |
| LONGITUDE | amount | 48 | 0 | -79.96142832893905 1; -79.984198720795 1; -80.02648118068127 1; -80.0094995954473 1 |
| NEIGHBORHOOD_NAME | category | 21 | 0 | Sheraden 9; Lower Lawrenceville 7; Crafton Heights 5; Lincoln-Lemington-Belmar 4 |
| COUNCIL_DISTRICT | category | 7 | 0 | 2 16; 3 9; 7 8; 9 7 |
| WARD | category | 15 | 0 | 20 13; 9 8; 12 4; 18 3 |
| POLICE_ZONE | category | 6 | 0 | 6 17; 2 9; 3 9; 5 8 |
| FIRE_ZONE | category | 20 | 0 | 1-16 9; 3-6 8; 3-18 4; 1-17 4 |
| DPW_STREETS | category | 5 | 0 | 5 18; 1 10; 4 8; 2 8 |
| DPW_ENVIRO | category | 4 | 0 | Northern 19; Central 10; Southern 10; Eastern 9 |
| DPW_PARKS | category | 6 | 0 | Emerald 17; Highland 12; McKinley 9; Frick 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:23:38.50727 48 |
| SOURCE_RUN_ID | audit | 1 | 0 | a20893d6-564d-49b5-95f5-5 48 |
| SRC_SHA256 | who | 1 | 0 | 5d89171997369474787ce5c31 48 |
