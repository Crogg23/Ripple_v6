# FED_NTSB_AVIATION_INJURY

rows 179.2K  columns 10  scan 2.2s

roles: amount 1, audit 2, category 3, date 1, other 3

## when

LCHG_DATE
  2020    109.5K  ##############################
  2021      8.1K  ##
  2022     10.4K  ###
  2023      8.5K  ##
  2024     11.6K  ###
  2025     18.8K  #####
  2026     12.2K  ###

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| INJ_PERSON_COUNT | 156.6K | 0 | 0 | 11.24 | 497 | 260.6K |

## what

AIRCRAFT_KEY: 1 98%, 2 1%, 3 0%, 5 0%

INJ_PERSON_CATEGORY: Flig 71%, Pass 21%, Cabi 5%, LapC 3%

INJURY_LEVEL: TOTL 27%, NONE 23%, FATL 17%, MINR 17%, SERS 16%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| EV_ID | other | 29.9K | 0 | 20260625203249 925; 20260526203054 919; 20260324202693 910; 20260727203462 909 |
| AIRCRAFT_KEY | category | 4 | 0 | 1 176.5K; 2 2.7K; 3 33; 5 20 |
| INJ_PERSON_CATEGORY | category | 4 | 0 | Flig 127.7K; Pass 38.2K; Cabi 8.5K; LapC 4.7K |
| INJURY_LEVEL | category | 5 | 0 | TOTL 49.0K; NONE 41.1K; FATL 30.5K; MINR 29.6K |
| INJ_PERSON_COUNT | amount | 314 | 0 | 0.0 100.9K; 1.0 41.8K; nan 22.6K; 2.0 8.4K |
| LCHG_DATE | date | 9.3K | 0 | 2020-09-25 18:00:53 2.2K; 2020-09-25 18:01:38 2.1K; 2020-09-25 18:06:16 2.1K; 2020-09-25 17:59:24 2.0K |
| LCHG_USERID | other | 185 | 0 | None 108.4K; coln 30.9K; broda 5.6K; dobn 3.7K |
| INGESTED_AT | audit | 1 | 0 | 1786154107240125 179.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 767e3583-447f-4101-bd46-a 179.2K |
| SRC_SHA256 | other | 1 | 0 | 0cf30a610d18eb109035b8310 179.2K |
