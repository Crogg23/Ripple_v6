# PORTAL_CKA_HOUSTON_OPEN_DAT_501EE45DC7

rows 3.5K  columns 30  scan 4.4s

roles: audit 2, category 2, date 1, id 1, other 23, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 1; Census Tract 6731.11; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6704; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6724.01; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6715.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6705; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6715.01; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6720.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6730.09; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6728.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6730.10; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6718; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6729.03; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.06; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6706.03; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6702.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6734.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6708.04; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6711.02; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6710.02; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  074442f6044647663325f35769674c7df1e685a149afcdd84b878ee9e0927667

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6704; Fort B  2026:1
  Block Group 1; Census Tract 6705; Fort B  2026:1
  Block Group 1; Census Tract 6708.04; For  2026:1
  Block Group 1; Census Tract 6718; Fort B  2026:1
  Block Group 1; Census Tract 6724.01; For  2026:1
  Block Group 1; Census Tract 6730.10; For  2026:1
  Block Group 1; Census Tract 6731.04; For  2026:1
  Block Group 1; Census Tract 6731.06; For  2026:1
  Block Group 1; Census Tract 6731.11; For  2026:1
  Block Group 2; Census Tract 6706.03; For  2026:1
  Block Group 2; Census Tract 6715.01; For  2026:1
  Block Group 2; Census Tract 6728.02; For  2026:1
  Block Group 2; Census Tract 6729.03; For  2026:1
  Block Group 2; Census Tract 6734.02; For  2026:1
  Block Group 3; Census Tract 6702.02; For  2026:1
  Block Group 3; Census Tract 6715.01; For  2026:1
  Block Group 3; Census Tract 6730.09; For  2026:1
  Block Group 4; Census Tract 6710.02; For  2026:1
  Block Group 4; Census Tract 6711.02; For  2026:1
  Block Group 4; Census Tract 6720.02; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  074442f6044647663325f35769674c7df1e685a1  2026:3.5K

## what

B15003_003E: 0 99%, 9 0%, 10 0%, 13 0%, 8 0%, 24 0%, 19 0%, 25 0%, 53 0%, 21 0%, 7 0%, 4 0%

B15003_004E: 0 99%, 14 0%, 11 0%, 7 0%, 12 0%, 33 0%, 8 0%, 6 0%, 23 0%, 13 0%, 21 0%, 18 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B15003_001E | other | 1.7K | 0 | 1171 19; 1296 19; 862 19; 1741 18 |
| B15003_002E | other | 271 | 0 | 0 1.4K; 13 47; 11 39; 8 38 |
| B15003_003E | category | 37 | 0 | 0 3.5K; 9 5; 10 4; 13 3 |
| B15003_004E | category | 42 | 0 | 0 3.4K; 14 4; 11 4; 7 4 |
| B15003_005E | other | 76 | 0 | 0 3.4K; 26 9; 15 7; 17 7 |
| B15003_006E | other | 100 | 0 | 0 3.2K; 12 9; 15 8; 22 8 |
| B15003_007E | other | 114 | 0 | 0 3.0K; 8 18; 14 16; 7 15 |
| B15003_008E | other | 85 | 0 | 0 3.1K; 14 13; 12 13; 22 13 |
| B15003_009E | other | 121 | 0 | 0 3.0K; 18 18; 26 18; 10 16 |
| B15003_010E | other | 231 | 0 | 0 2.2K; 15 29; 11 28; 8 23 |
| B15003_011E | other | 100 | 0 | 0 3.0K; 12 19; 3 18; 6 17 |
| B15003_012E | other | 145 | 0 | 0 2.5K; 12 32; 9 25; 13 23 |
| B15003_013E | other | 202 | 0 | 0 2.1K; 13 28; 10 27; 8 26 |
| B15003_014E | other | 150 | 0 | 0 2.3K; 8 38; 13 34; 19 33 |
| B15003_015E | other | 163 | 0 | 0 2.2K; 12 40; 13 38; 15 35 |
| B15003_016E | other | 215 | 0 | 0 1.6K; 14 52; 13 49; 9 44 |
| B15003_017E | other | 634 | 0 | 0 85; 133 20; 39 20; 62 20 |
| B15003_018E | other | 262 | 0 | 0 977; 11 52; 18 51; 24 47 |
| B15003_019E | other | 328 | 0 | 0 556; 25 41; 12 40; 10 36 |
| B15003_020E | other | 514 | 0 | 0 146; 98 25; 50 24; 63 24 |
| B15003_021E | other | 368 | 0 | 0 450; 24 38; 43 36; 23 35 |
| B15003_022E | other | 814 | 0 | 0 156; 113 20; 11 20; 23 19 |
| B15003_023E | other | 506 | 0 | 0 651; 21 35; 23 34; 14 30 |
| B15003_024E | other | 244 | 0 | 0 1.8K; 9 43; 15 40; 14 37 |
| B15003_025E | other | 210 | 0 | 0 2.0K; 11 46; 13 41; 8 41 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:31:27.83160 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0a36875d-08bd-45b0-b61b-1 3.5K |
| SRC_SHA256 | who | 1 | 0 | 074442f6044647663325f3576 3.5K |
