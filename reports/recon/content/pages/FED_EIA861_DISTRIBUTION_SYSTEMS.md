# FED_EIA861_DISTRIBUTION_SYSTEMS

rows 1.4K  columns 9  scan 2.6s

roles: amount 1, audit 2, date 1, other 4, state 1, who 1

## when

_INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| C_8_1 | 1.4K | 0 | 0 | 1.1K | 3.4K | 58.0K |

## who

_SRC_FILE by rows
      1.4K  Distribution_Systems_2024.xlsx

_SRC_FILE by dollars
       58.0K     1.4K rows  Distribution_Systems_2024.xlsx

## who x when

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date, dollars = C_8_1
  Distribution_Systems_2024.xlsx            2026:58.0K

## where

MS: TX 88, TN 87, WI 67, GA 59, NC 54, IN 46, KY 46, MN 46, AL 45, MO 45, WA 39, MS 39

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| C_2024 | other | 1 | 0 | 2024 1.4K |
| C_55 | other | 1.2K | 0 | 27000 14; 19160 10; 14354 10; 27058 9 |
| CITY_OF_ABERDEEN_MS | other | 1.2K | 0 | WAPA-- Western Area Power 14; Tri-County Electric Coop, 10; PacifiCorp 10; High West Energy, Inc 9 |
| MS | state | 51 | 0 | TX 88; TN 87; WI 67; GA 59 |
| C_8 | other | 316 | 0 | 1 35; 20 24; 36 21; 24 20 |
| C_8_1 | amount | 163 | 0 | 0 563; . 298; 1 17; 34 16 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:39:01.96605 1.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | e5dc2971-01a2-4b53-b4ad-1 1.4K |
| _SRC_FILE | who | 1 | 0 | Distribution_Systems_2024 1.4K |
