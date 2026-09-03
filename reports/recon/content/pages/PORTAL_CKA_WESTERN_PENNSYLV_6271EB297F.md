# PORTAL_CKA_WESTERN_PENNSYLV_6271EB297F

rows 1.3K  columns 30  scan 3.0s

roles: amount 3, audit 2, date 1, id 1, other 23, who 1

## when

INGESTED_AT
  2026      1.3K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LONGITUDE | 1.3K | -80.31 | -79.98 | -79.71 | -79.68 | -104.4K |
| LATITUDE | 1.3K | 40.20 | 40.45 | 40.67 | 40.68 | 52.8K |
| C_12P | 1.3K | -1 | 266 | 950.96 | 999 | 426.4K |

## who

SRC_SHA256 by rows
      1.3K  5e5d08af1e522289d1ec9a0d052f7668f919f0a4324cb52041c2931893cca0b9

SRC_SHA256 by dollars
     -104.4K     1.3K rows  5e5d08af1e522289d1ec9a0d052f7668f919f0a4324cb52041c2931893cc

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LONGITUDE
  5e5d08af1e522289d1ec9a0d052f7668f919f0a4  2026:-104.4K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SENSOR_ID | id | 1.3K | 0 | 3931@1 7; 26521@1 7; 10540@1 7; 27461@1 7 |
| LONGITUDE | amount | 1.3K | 0 | -80.14961528 7; -79.83565874 7; -79.84994335 7; -79.93980354 7 |
| LATITUDE | amount | 1.3K | 0 | 40.55074267 7; 40.28092737 7; 40.28071653 7; 40.42256027 7 |
| C_1A | other | 216 | 0 | -1 147; 24 26; 1 26; 5 25 |
| C_2A | other | 158 | 0 | -1 166; 4 43; 2 41; 1 39 |
| C_3A | other | 150 | 0 | -1 174; 2 54; 1 49; 5 47 |
| C_4A | other | 177 | 0 | -1 161; 1 45; 2 41; 3 37 |
| C_5A | other | 262 | 0 | -1 134; 7 26; 4 25; 3 24 |
| C_6A | other | 461 | 0 | -1 124; 116 12; 46 11; 5 11 |
| C_7A | other | 637 | 0 | -1 122; 15 9; 59 8; 24 8 |
| C_8A | other | 673 | 0 | -1 121; 31 8; 48 8; 67 8 |
| C_9A | other | 670 | 0 | -1 123; 28 8; 132 7; 203 7 |
| C_10A | other | 657 | 0 | -1 122; 9 8; 349 7; 19 7 |
| C_11A | other | 638 | 0 | -1 120; 68 8; 31 8; 94 8 |
| C_12P | amount | 632 | 0 | -1 120; 25 9; 41 9; 18 9 |
| C_1P | other | 713 | 0 | 129 9; 202 9; 31 8; 41 8 |
| C_2P | other | 734 | 0 | 194 9; 765 8; 28 8; 31 8 |
| C_3P | other | 728 | 0 | 149 10; 97 8; 373 8; 121 8 |
| C_4P | other | 752 | 0 | 26 8; 795 8; 110 8; 36 8 |
| C_5P | other | 770 | 0 | 278 8; 37 8; 344 8; 446 8 |
| C_6P | other | 732 | 0 | 52 8; 49 8; 481 8; 125 8 |
| C_7P | other | 656 | 0 | -1 122; 419 8; 34 7; 427 7 |
| C_8P | other | 639 | 0 | -1 122; 79 8; 175 8; 750 7 |
| C_9P | other | 592 | 0 | -1 124; 278 9; 37 8; 45 8 |
| C_10P | other | 515 | 0 | -1 122; 7 10; 9 9; 15 9 |
| C_11P | other | 415 | 0 | -1 127; 55 11; 9 10; 22 10 |
| C_12A | other | 327 | 0 | -1 124; 1 18; 43 15; 11 14 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:52:19.23264 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | db9f0ee8-fa20-4fd4-86b1-b 1.3K |
| SRC_SHA256 | who | 1 | 0 | 5e5d08af1e522289d1ec9a0d0 1.3K |
