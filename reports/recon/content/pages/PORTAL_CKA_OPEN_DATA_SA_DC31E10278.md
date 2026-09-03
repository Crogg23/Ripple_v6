# PORTAL_CKA_OPEN_DATA_SA_DC31E10278

rows 40  columns 9  scan 2.6s

roles: amount 3, audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026        40  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 40 | 393.84 | 2.1K | 26.7K | 28.5K | 187.8K |
| SHAPE__AREA | 40 | 2.12M | 11.10M | 143.48M | 153.36M | 1.01B |
| SHAPE__LENGTH | 40 | 6.9K | 20.2K | 196.6K | 197.3K | 2.00M |

## who

SRC_SHA256 by rows
        40  de83edd8e71eb2b9c684109fd010b2fa401d0341cd186e675d5db8462c4982a4

SRC_SHA256 by dollars
      187.8K       40 rows  de83edd8e71eb2b9c684109fd010b2fa401d0341cd186e675d5db8462c49

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  de83edd8e71eb2b9c684109fd010b2fa401d0341  2026:187.8K

## what

OBJECTID: 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%

NAME: Alamo Heights 8%, Terrell Hills 8%, Devine 8%, Natalia 8%, Castroville 8%, Elmendorf 8%, Converse 8%, Live Oak 8%, Garden Ridge 8%, Shavano Park 8%, Fair Oaks Ranch 8%, Helotes 8%

SQMILES: 2 30%, 1 19%, 3 11%, 6 8%, 5 5%, 7 5%, 4 5%, 10 5%, 9 3%, 12 3%, 32 3%, 45 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 40 | 0 | 40 1; 39 1; 38 1; 37 1 |
| NAME | category | 40 | 0 | Alamo Heights 1; Terrell Hills 1; Devine 1; Natalia 1 |
| ACRES | amount | 39 | 0 | 1181.06776409 1; 1025.39894007 1; 2057.72991851 1; 728.25915954 1 |
| SQMILES | category | 15 | 0 | 2 11; 1 7; 3 4; 6 3 |
| SHAPE__AREA | amount | 40 | 0 | 6331038.30859375 1; 5495973.921875 1; 10958497.1328125 1; 3881437.33203125 1 |
| SHAPE__LENGTH | amount | 40 | 0 | 11185.5625965968 1; 9717.98641774981 1; 20450.2660148347 1; 15812.0591171642 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:21:02.98451 40 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3f498843-7ad4-4236-90e9-4 40 |
| SRC_SHA256 | who | 1 | 0 | de83edd8e71eb2b9c684109fd 40 |
