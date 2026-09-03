# PORTAL_ARC_HARRIS_COUNTY_OP_FCFE62D3BE

rows 18  columns 21  scan 3.7s

roles: amount 6, audit 2, category 12, date 1, who 1

## when

INGESTED_AT
  2026        18  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FID_1 | 8 | 9 | 626.50 | 658.86 | 659 | 3.3K |
| SHAPE__ARE | 8 | 18.25M | 412.71M | 855.82M | 860.29M | 3.31B |
| SHAPE__LEN | 8 | 31.2K | 126.7K | 200.3K | 204.2K | 942.8K |
| SHAPE_LENG | 18 | 10.5K | 192.1K | 401.4K | 401.4K | 3.63M |
| SHAPE__AREA | 18 | 5.1K | 646.79M | 3.16B | 3.16B | 17.58B |
| SHAPE__LENGTH | 18 | 10.5K | 192.1K | 401.4K | 401.4K | 3.63M |

## who

SRC_SHA256 by rows
        18  86df0b03eda25fc0c7a433e9f1a87958c572889b723a4335fea73670296e7344

SRC_SHA256 by dollars
       3.63M       18 rows  86df0b03eda25fc0c7a433e9f1a87958c572889b723a4335fea73670296e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENG
  86df0b03eda25fc0c7a433e9f1a87958c572889b  2026:3.63M

## what

FID: 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%

GEOID20: nan 56%, 4828740 6%, 4816110 6%, 4844430 6%, 4842960 6%, 4819650 6%, 4841100 6%, 4823640 6%, 4841350 6%

NAME20: nan 56%, Magnolia Independent School Di 6%, Cypress-Fairbanks Independent  6%, Waller Independent School Dist 6%, Tomball Independent School Dis 6%, Fort Bend Independent School D 6%, Spring Branch Independent Scho 6%, Houston Independent School Dis 6%, Stafford Municipal School Dist 6%

SDLEA: nan 56%, 28740 6%, 16110 6%, 44430 6%, 42960 6%, 19650 6%, 41100 6%, 23640 6%, 41350 6%

NAME: Magnolia ISD 17%, Fort Bend ISD 11%, Houston ISD 11%, Katy ISD 11%, Stafford MSD 11%, Cypress-Fairbanks ISD 11%, Spring Branch ISD 11%, Alief ISD 6%, Waller ISD 6%, Tomball ISD 6%

NAME2: Magnolia 17%, Fort Bend 11%, Houston 11%, Katy 11%, Stafford MSD 11%, Cypress-Fairbanks 11%, Spring Branch 11%, Alief 6%, Waller 6%, Tomball 6%

DISTRICT_N: 170906 17%, 79907 11%, 101912 11%, 101914 11%, 79910 11%, 101907 11%, 101920 11%, 101903 6%, 237904 6%, 101921 6%

DISTRICT: 170-906 17%, 079-907 11%, 101-912 11%, 101-914 11%, 079-910 11%, 101-907 11%, 101-920 11%, 101-903 6%, 237-904 6%, 101-921 6%

DISTRICT_C: 170906 17%, 079907 11%, 101912 11%, 101914 11%, 079910 11%, 101907 11%, 101920 11%, 101903 6%, 237904 6%, 101921 6%

NCES_DISTR: 4828740 17%, 4819650 11%, 4823640 11%, 4825170 11%, 4841350 11%, 4816110 11%, 4841100 11%, 4807830 6%, 4844430 6%, 4842960 6%

COLOR: 2 28%, 3 28%, 4 17%, 6 17%, 7 11%

GEOMETRY: {"type": "MultiPolygon", "coor 11%, {"type": "MultiPolygon", "coor 11%, {"type": "Polygon", "coordinat 11%, {"type": "Polygon", "coordinat 11%, {"type": "MultiPolygon", "coor 11%, {"type": "MultiPolygon", "coor 11%, {"type": "MultiPolygon", "coor 11%, {"type": "Polygon", "coordinat 6%, {"type": "Polygon", "coordinat 6%, {"type": "Polygon", "coordinat 6%, {"type": "MultiPolygon", "coor 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 18 | 0 | 20 1; 19 1; 18 1; 17 1 |
| FID_1 | amount | 9 | 0 | nan 10; 659.0 1; 657.0 1; 656.0 1 |
| GEOID20 | category | 9 | 0 | nan 10; 4828740 1; 4816110 1; 4844430 1 |
| NAME20 | category | 9 | 0 | nan 10; Magnolia Independent Scho 1; Cypress-Fairbanks Indepen 1; Waller Independent School 1 |
| SDLEA | category | 9 | 0 | nan 10; 28740 1; 16110 1; 44430 1 |
| NAME | category | 10 | 0 | Magnolia ISD 3; Fort Bend ISD 2; Houston ISD 2; Katy ISD 2 |
| NAME2 | category | 10 | 0 | Magnolia 3; Fort Bend 2; Houston 2; Katy 2 |
| DISTRICT_N | category | 10 | 0 | 170906 3; 79907 2; 101912 2; 101914 2 |
| DISTRICT | category | 10 | 0 | 170-906 3; 079-907 2; 101-912 2; 101-914 2 |
| DISTRICT_C | category | 10 | 0 | 170906 3; 079907 2; 101912 2; 101914 2 |
| NCES_DISTR | category | 10 | 0 | 4828740 3; 4819650 2; 4823640 2; 4825170 2 |
| COLOR | category | 5 | 0 | 2 5; 3 5; 4 3; 6 3 |
| SHAPE__ARE | amount | 9 | 0 | nan 10; 387675446.988 1; 487361428.086 1; 796371094.99 1 |
| SHAPE__LEN | amount | 9 | 0 | nan 10; 135745.44773 1; 117575.725889 1; 148146.469041 1 |
| SHAPE_LENG | amount | 11 | 0 | 96126.8595627 2; 401430.370346 2; 339044.320002 2; 23083.3064703 2 |
| SHAPE__AREA | amount | 11 | 0 | 745881.765625 2; 1493736516.4335938 2; 3158437418.9453125 2; 1251366.0546875 2 |
| SHAPE__LENGTH | amount | 11 | 0 | 96126.85956272129 2; 401430.37034581706 2; 339044.32000169717 2; 23083.306470312928 2 |
| GEOMETRY | category | 11 | 0 | {"type": "MultiPolygon",  2; {"type": "MultiPolygon",  2; {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:28.88546 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | e285087d-923e-400d-a724-b 18 |
| SRC_SHA256 | who | 1 | 0 | 86df0b03eda25fc0c7a433e9f 18 |
