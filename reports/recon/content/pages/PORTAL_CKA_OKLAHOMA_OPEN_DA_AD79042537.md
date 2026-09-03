# PORTAL_CKA_OKLAHOMA_OPEN_DA_AD79042537

rows 410  columns 14  scan 3.4s

roles: amount 4, audit 2, category 4, date 1, other 3, who 1

## when

INGESTED_AT
  2026       410  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 410 | 0 | 36.19 | 36.95 | 37.55 | 14.6K |
| LONGITUDE | 410 | -102.21 | -98 | 1.82 | 97.52 | -38.8K |
| TOP_OF_TOWER_AGL_HEIGHT_FEET | 410 | 2 | 197 | 851.49 | 2.0K | 88.0K |
| TOP_OF_TOWER_MSL_HEIGHT_FEET | 410 | 4 | 1.7K | 3.9K | 28.9K | 806.6K |

## who

SRC_SHA256 by rows
       410  6e4e29f961f6809612f255150280e4e2c22f63154512b6a373096d474989eb3d

SRC_SHA256 by dollars
       88.0K      410 rows  6e4e29f961f6809612f255150280e4e2c22f63154512b6a373096d474989

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOP_OF_TOWER_AGL_HEIGHT_FEET
  6e4e29f961f6809612f255150280e4e2c22f6315  2026:88.0K

## what

COUNTY: Garfield 13%, Caddo 11%, Woodward 10%, Noble 10%, Texas 10%, Johnston 8%, Dewey 8%, Grant 6%, Grady 6%, Kay 6%, Ellis 6%, Woods 6%

ALTERNATING_BANDS: Yes 99%, No 1%

MARKER_BALLS: Yes 96%, No 4%

SAFETY_SLEEVES: Yes 97%, No 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TOWER_NUMBER | other | 404 | 0 | Woodward-028 3; Nowata-009 3; Nowata-008 3; Nowata-007 3 |
| COUNTY | category | 48 | 0 | Garfield 32; Caddo 27; Woodward 25; Noble 25 |
| LATITUDE | amount | 370 | 0 | 0.0 4; 35.0 4; 36.50095 4; 36.1888 3 |
| LONGITUDE | amount | 383 | 0 | 0.0 6; -98.588619 4; -97.451133 4; -95.0 3 |
| MAP | other | 381 | 0 | https://www.google.com/ma 4; https://www.google.com/ma 4; https://www.google.com/ma 3; https://www.google.com/ma 3 |
| LOCATION_DESCRIPTION | other | 411 | 0 | (N 36 18 37.4400\, W 99 2 3; (N 36 56 13.5384\, W 95 3 3; (N 36 41 44.9196\, E 95 4 3; (N 36 41 13.9596\, E 95 4 3 |
| TOP_OF_TOWER_AGL_HEIGHT_FEET | amount | 34 | 0 | 197 182; 198 56; 200 56; 196 41 |
| TOP_OF_TOWER_MSL_HEIGHT_FEET | amount | 335 | 0 | 1427 5; 1399 4; 392 4; 1401 4 |
| ALTERNATING_BANDS | category | 2 | 0 | Yes 407; No 3 |
| MARKER_BALLS | category | 2 | 0 | Yes 394; No 16 |
| SAFETY_SLEEVES | category | 2 | 0 | Yes 396; No 14 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:41:27.76892 410 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5661331c-c226-4168-a5c0-9 410 |
| SRC_SHA256 | who | 1 | 0 | 6e4e29f961f6809612f255150 410 |
