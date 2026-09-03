# PORTAL_CKA_OPEN_DATA_SA_E90902C24C

rows 10.0K  columns 11  scan 2.7s

roles: amount 3, audit 2, category 3, date 1, id 2, who 1

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SQMILES | 10.0K | 0 | 0 | 0.04 | 1.16 | 27.13 |
| SHAPE__AREA | 10.0K | 10.94 | 16.5K | 1.13M | 32.46M | 935.06M |
| SHAPE__LENGTH | 10.0K | 25.29 | 569.65 | 6.2K | 29.3K | 9.33M |

## who

SRC_SHA256 by rows
     10.0K  7efc4a8e7b53d7ecf5f50b81e1e47222db004fd0721d8dffb896fef02a475624

SRC_SHA256 by dollars
       27.13    10.0K rows  7efc4a8e7b53d7ecf5f50b81e1e47222db004fd0721d8dffb896fef02a47

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SQMILES
  7efc4a8e7b53d7ecf5f50b81e1e47222db004fd0  2026:27.13

## what

NAME: Level 3 79%, Level 2 14%, Level 1 7%

COLOR: Leaf Green 92%, Red 8%, Yellow 1%

NAME2: Downtown 28%, Greater Airport Area 21%, Medical Center 13%, Fort Sam Houston 9%, Stone Oak 8%, UTSA 6%, NE I-35 and Loop 410 5%, Port San Antonio 5%, Highway 151 and Loop 1604 2%, Texas AM - San Antonio 2%, Rolling Oaks 1%, Near Northeast 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| NAME | category | 3 | 0 | Level 3 7.9K; Level 2 1.4K; Level 1 716 |
| COLOR | category | 4 | 1.4K | Leaf Green 7.9K; Red 657; Yellow 59 |
| NAME2 | category | 14 | 0 | Downtown 2.8K; Greater Airport Area 2.1K; Medical Center 1.3K; Fort Sam Houston 923 |
| SQMILES | amount | 9.6K | 0 | 2.8E-06 59; 0.00180088 50; 0.00011679 50; 0.00227249 50 |
| GLOBALID | id | 10.2K | 0 | 40672fdf-6b82-411f-8a12-2 50; 64d14c26-8d2d-4ac5-bb55-0 50; d1c44280-284d-4566-ac01-c 50; 331645e1-1b78-4e29-9d65-c 50 |
| SHAPE__AREA | amount | 10.0K | 0 | 50205.57421875 50; 3255.873046875 50; 63353.064453125 50; 4836.142578125 50 |
| SHAPE__LENGTH | amount | 9.9K | 0 | 891.353828114456 50; 247.646266926373 50; 1224.92594689481 50; 332.472524272521 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:36:37.90941 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3e02b959-e1cc-4c30-b091-0 10.0K |
| SRC_SHA256 | who | 1 | 0 | 7efc4a8e7b53d7ecf5f50b81e 10.0K |
