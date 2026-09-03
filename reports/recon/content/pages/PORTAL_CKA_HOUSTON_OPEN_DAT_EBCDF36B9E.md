# PORTAL_CKA_HOUSTON_OPEN_DAT_EBCDF36B9E

rows 3.5K  columns 32  scan 2.9s

roles: audit 2, category 6, date 1, id 1, other 21, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 2; Census Tract 6728.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6706.03; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6716.01; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6716.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6707; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6720.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6723.03; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6729.03; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6725; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6732.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.07; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6727.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6719; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6709.03; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6704; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6731.13; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6712; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6712; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6712; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  af6c44aaa8ff036c159b4c6c51c89899d8b2bbd848c74984a3956145957ea48a

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6704; Fort B  2026:1
  Block Group 1; Census Tract 6706.03; For  2026:1
  Block Group 1; Census Tract 6709.03; For  2026:1
  Block Group 1; Census Tract 6712; Fort B  2026:1
  Block Group 1; Census Tract 6725; Fort B  2026:1
  Block Group 1; Census Tract 6727.02; For  2026:1
  Block Group 1; Census Tract 6729.03; For  2026:1
  Block Group 1; Census Tract 6731.04; For  2026:1
  Block Group 1; Census Tract 6731.07; For  2026:1
  Block Group 2; Census Tract 6712; Fort B  2026:1
  Block Group 2; Census Tract 6716.01; For  2026:1
  Block Group 2; Census Tract 6716.02; For  2026:1
  Block Group 2; Census Tract 6723.03; For  2026:1
  Block Group 2; Census Tract 6728.01; For  2026:1
  Block Group 2; Census Tract 6732.01; For  2026:1
  Block Group 3; Census Tract 6707; Fort B  2026:1
  Block Group 3; Census Tract 6712; Fort B  2026:1
  Block Group 3; Census Tract 6719; Fort B  2026:1
  Block Group 3; Census Tract 6720.02; For  2026:1
  Block Group 3; Census Tract 6731.13; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  af6c44aaa8ff036c159b4c6c51c89899d8b2bbd8  2026:3.5K

## what

B25063_003E: 0 100%, 17 0%, 10 0%, 13 0%, 9 0%, 27 0%, 36 0%, 11 0%, 76 0%, 79 0%, 28 0%, 25 0%

B25063_004E: 0 100%, 12 0%, 29 0%, 18 0%, 16 0%, 27 0%, 40 0%, 7 0%, 47 0%, 71 0%, 21 0%, 64 0%

B25063_005E: 0 100%, 16 0%, 23 0%, 13 0%, 6 0%, 103 0%, 25 0%, 48 0%, 31 0%, 26 0%, 92 0%, 5 0%

B25063_006E: 0 99%, 23 0%, 22 0%, 5 0%, 13 0%, 29 0%, 12 0%, 9 0%, 55 0%, 17 0%, 3 0%, 53 0%

B25063_008E: 0 99%, 12 0%, 10 0%, 8 0%, 42 0%, 35 0%, 22 0%, 85 0%, 7 0%, 15 0%, 32 0%, 11 0%

B25063_011E: 0 99%, 22 0%, 13 0%, 7 0%, 14 0%, 10 0%, 20 0%, 12 0%, 11 0%, 36 0%, 34 0%, 19 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B25063_001E | other | 832 | 0 | 0 220; 54 20; 21 19; 15 19 |
| B25063_002E | other | 821 | 0 | 0 262; 17 21; 72 20; 15 20 |
| B25063_003E | category | 27 | 0 | 0 3.5K; 17 3; 10 2; 13 2 |
| B25063_004E | category | 18 | 0 | 0 3.5K; 12 3; 29 3; 18 2 |
| B25063_005E | category | 23 | 0 | 0 3.5K; 16 2; 23 1; 13 1 |
| B25063_006E | category | 50 | 0 | 0 3.5K; 23 4; 22 4; 5 4 |
| B25063_007E | other | 60 | 0 | 0 3.4K; 17 7; 15 5; 27 5 |
| B25063_008E | category | 48 | 0 | 0 3.4K; 12 9; 10 6; 8 5 |
| B25063_009E | other | 58 | 0 | 0 3.4K; 12 6; 13 5; 15 5 |
| B25063_010E | other | 55 | 0 | 0 3.4K; 10 6; 25 5; 24 4 |
| B25063_011E | category | 45 | 0 | 0 3.4K; 22 5; 13 4; 7 4 |
| B25063_012E | other | 57 | 0 | 0 3.4K; 13 8; 8 5; 17 5 |
| B25063_013E | other | 56 | 0 | 0 3.4K; 11 8; 15 6; 14 4 |
| B25063_014E | other | 61 | 0 | 0 3.4K; 13 8; 14 7; 25 7 |
| B25063_015E | other | 70 | 0 | 0 3.3K; 15 11; 24 9; 21 9 |
| B25063_016E | other | 79 | 0 | 0 3.3K; 11 12; 12 10; 8 9 |
| B25063_017E | other | 97 | 0 | 0 3.2K; 10 17; 9 12; 28 12 |
| B25063_018E | other | 170 | 0 | 0 2.8K; 14 20; 22 18; 13 17 |
| B25063_019E | other | 202 | 0 | 0 2.6K; 14 22; 10 21; 19 18 |
| B25063_020E | other | 332 | 0 | 0 1.7K; 13 26; 14 25; 39 24 |
| B25063_021E | other | 320 | 0 | 0 1.6K; 12 39; 10 26; 16 26 |
| B25063_022E | other | 401 | 0 | 0 1.3K; 12 32; 18 31; 19 29 |
| B25063_023E | other | 256 | 0 | 0 2.0K; 13 34; 15 34; 12 33 |
| B25063_024E | other | 158 | 0 | 0 2.8K; 11 23; 9 22; 20 21 |
| B25063_025E | other | 98 | 0 | 0 3.2K; 11 16; 16 14; 10 13 |
| B25063_026E | other | 112 | 0 | 0 3.1K; 12 18; 10 14; 11 12 |
| B25063_027E | other | 112 | 0 | 0 2.6K; 14 34; 10 33; 8 33 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:30:52.25089 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 28d193cf-4512-4a5f-9ad5-f 3.5K |
| SRC_SHA256 | who | 1 | 0 | af6c44aaa8ff036c159b4c6c5 3.5K |
