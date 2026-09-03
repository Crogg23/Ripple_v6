# PORTAL_CKA_INDIANA_DATA_HUB_83BA6435C2

rows 10.0K  columns 20  scan 3.9s

roles: amount 4, audit 2, category 4, date 2, other 8, who 1

## when

DATE
  2020      4.3K  ##########################
  2021      5.0K  ##############################
  2022       676  ####

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POSITIVE_TEST_RATE | 10.0K | 0 | 30 | 100 | 100 | 298.5K |
| POSITIVE_TEST_RATE_MOVING_AVG | 10.0K | 0 | 30.43 | 57.76 | 100 | 301.7K |
| ALL_TESTS_POSITIVE_TEST_RATE | 10.0K | 0 | 7.65 | 44.40 | 100 | 99.5K |
| ALL_TESTS_POSITIVE_TEST_RATE_MOVING_AVG | 10.0K | 0 | 7.45 | 33.32 | 100 | 91.1K |

## who

SRC_SHA256 by rows
     10.0K  f94002ddbc956c52d56cb82a95564741d6e0f89bcf1ff34d8f5babbdc9c839cb

SRC_SHA256 by dollars
      298.5K    10.0K rows  f94002ddbc956c52d56cb82a95564741d6e0f89bcf1ff34d8f5babbdc9c8

## who x when

SRC_SHA256 by DATE, dollars = POSITIVE_TEST_RATE
  f94002ddbc956c52d56cb82a95564741d6e0f89b  2020:144.8K 2021:130.0K 2022:23.7K

## what

LOCATION_ID: 18025 8%, 18023 8%, 18021 8%, 18019 8%, 18017 8%, 18015 8%, 18013 8%, 18011 8%, 18009 8%, 18007 8%, 18005 8%, 18003 8%

COVID_DEATHS: 0 83%, 1 12%, 2 3%, 3 1%, 4 1%, 5 0%, 6 0%, 7 0%, 9 0%, 8 0%, 11 0%

COVID_DEATHS_MOVING_AVG: 0 85%, 1 11%, 2 2%, 3 1%, 4 0%, 5 0%, 6 0%, 7 0%

COUNTY_NAME: Crawford 8%, Clinton 8%, Clay 8%, Clark 8%, Cass 8%, Carroll 8%, Brown 8%, Boone 8%, Blackford 8%, Benton 8%, Bartholomew 8%, Allen 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOCATION_ID | category | 14 | 0 | 18025 727; 18023 727; 18021 727; 18019 727 |
| DATE | date | 726 | 0 | 2021-08-27T00:00:00 50; 2021-08-26T00:00:00 50; 2021-08-25T00:00:00 50; 2021-08-24T00:00:00 50 |
| COVID_COUNT | other | 331 | 0 | 0 2.0K; 1 1.1K; 2 725; 3 545 |
| COVID_COUNT_MOVING_AVG | other | 331 | 0 | 0 1.3K; 1 1.3K; 2 840; 3 514 |
| COVID_DEATHS | category | 11 | 0 | 0 8.3K; 1 1.2K; 2 281; 3 108 |
| COVID_DEATHS_MOVING_AVG | category | 8 | 0 | 0 8.5K; 1 1.1K; 2 203; 3 81 |
| COVID_TESTS | other | 598 | 0 | 0 339; 2 326; 3 320; 4 319 |
| COVID_TESTS_MOVING_AVG | other | 577 | 0 | 12 306; 11 305; 4 301; 13 290 |
| POSITIVE_TEST_RATE | amount | 1.8K | 0 | 0.0 1.2K; 33.33 450; 50.0 428; 25.0 341 |
| POSITIVE_TEST_RATE_MOVING_AVG | amount | 3.1K | 0 | 0.0 241; 33.33 119; 25.0 81; 28.57 77 |
| COVID_TESTS_ADMINISTRATED | other | 1.2K | 0 | 0 266; 9 132; 4 130; 5 127 |
| COVID_TESTS_ADMINISTRATED_MOVING_AVG | other | 1.1K | 0 | 0 255; 20 102; 3 98; 42 92 |
| ALL_TESTS_POSITIVE_TEST_RATE | amount | 2.1K | 0 | 0.0 1.8K; 10.0 95; 11.11 91; 12.5 90 |
| COVID_POSITIVE_TESTS_ADMIN | other | 345 | 0 | 0 1.8K; 1 1.1K; 2 733; 3 561 |
| ALL_TESTS_POSITIVE_TEST_RATE_MOVING_AVG | amount | 2.4K | 0 | 0.0 400; 3.29 50; 1.09 50; 3.12 50 |
| COVID_COUNT_BY_SPECIMEN_COLLECTION_DATE | other | 328 | 0 | 0 2.0K; 1 1.1K; 2 736; 3 553 |
| COUNTY_NAME | category | 14 | 0 | Crawford 727; Clinton 727; Clay 727; Clark 727 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:51:33.61386 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | ec3301e6-5271-4fc2-96aa-6 10.0K |
| SRC_SHA256 | who | 1 | 0 | f94002ddbc956c52d56cb82a9 10.0K |
