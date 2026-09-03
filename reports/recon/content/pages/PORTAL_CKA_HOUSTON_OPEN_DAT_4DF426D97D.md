# PORTAL_CKA_HOUSTON_OPEN_DAT_4DF426D97D

rows 3.5K  columns 32  scan 2.9s

roles: audit 2, date 1, id 1, other 27, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 2; Census Tract 6718; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6701.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6710.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6709.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6723.04; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6711.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6714.02; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6725; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6714.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6730.08; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.05; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6730.10; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6723.06; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6712; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6701.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6701.01; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6730.10; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6730.09; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6703; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6702.01; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  793e7a8851b0cbaa2ad9ef31702f219b731b8c5541fe66e33a2ac7dbc2f5aa5d

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6701.02; For  2026:1
  Block Group 1; Census Tract 6702.01; For  2026:1
  Block Group 1; Census Tract 6710.01; For  2026:1
  Block Group 1; Census Tract 6712; Fort B  2026:1
  Block Group 1; Census Tract 6714.02; For  2026:1
  Block Group 1; Census Tract 6723.06; For  2026:1
  Block Group 1; Census Tract 6730.10; For  2026:1
  Block Group 1; Census Tract 6731.05; For  2026:1
  Block Group 2; Census Tract 6701.01; For  2026:1
  Block Group 2; Census Tract 6703; Fort B  2026:1
  Block Group 2; Census Tract 6718; Fort B  2026:1
  Block Group 2; Census Tract 6723.04; For  2026:1
  Block Group 2; Census Tract 6730.10; For  2026:1
  Block Group 3; Census Tract 6701.01; For  2026:1
  Block Group 3; Census Tract 6709.04; For  2026:1
  Block Group 3; Census Tract 6730.08; For  2026:1
  Block Group 3; Census Tract 6730.09; For  2026:1
  Block Group 4; Census Tract 6711.02; For  2026:1
  Block Group 4; Census Tract 6714.02; For  2026:1
  Block Group 4; Census Tract 6725; Fort B  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  793e7a8851b0cbaa2ad9ef31702f219b731b8c55  2026:3.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B25075_001E | other | 972 | 0 | 0 296; 870 17; 526 17; 825 17 |
| B25075_002E | other | 100 | 0 | 0 3.0K; 10 29; 13 25; 12 25 |
| B25075_003E | other | 68 | 0 | 0 3.3K; 12 11; 10 10; 9 9 |
| B25075_004E | other | 68 | 0 | 0 3.3K; 14 17; 9 13; 8 12 |
| B25075_005E | other | 69 | 0 | 0 3.3K; 10 14; 13 13; 9 12 |
| B25075_006E | other | 58 | 0 | 0 3.3K; 11 13; 12 11; 17 10 |
| B25075_007E | other | 65 | 0 | 0 3.3K; 5 12; 4 10; 8 10 |
| B25075_008E | other | 52 | 0 | 0 3.4K; 11 10; 12 9; 17 8 |
| B25075_009E | other | 73 | 0 | 0 3.3K; 9 17; 8 14; 13 13 |
| B25075_010E | other | 77 | 0 | 0 3.2K; 8 18; 12 16; 13 11 |
| B25075_011E | other | 78 | 0 | 0 3.2K; 9 16; 16 14; 15 13 |
| B25075_012E | other | 77 | 0 | 0 3.3K; 14 13; 10 12; 12 11 |
| B25075_013E | other | 88 | 0 | 0 3.1K; 10 19; 13 19; 12 17 |
| B25075_014E | other | 95 | 0 | 0 3.0K; 6 23; 13 19; 10 19 |
| B25075_015E | other | 162 | 0 | 0 2.5K; 9 36; 8 36; 12 33 |
| B25075_016E | other | 140 | 0 | 0 2.5K; 12 33; 11 32; 15 30 |
| B25075_017E | other | 187 | 0 | 0 2.1K; 11 43; 16 35; 9 34 |
| B25075_018E | other | 187 | 0 | 0 2.1K; 12 37; 13 36; 11 35 |
| B25075_019E | other | 329 | 0 | 0 1.3K; 11 39; 9 37; 16 35 |
| B25075_020E | other | 313 | 0 | 0 1.4K; 9 38; 12 37; 8 32 |
| B25075_021E | other | 424 | 0 | 0 1.2K; 12 37; 14 33; 18 31 |
| B25075_022E | other | 330 | 0 | 0 1.9K; 21 29; 15 28; 14 28 |
| B25075_023E | other | 336 | 0 | 0 2.1K; 14 29; 15 27; 9 26 |
| B25075_024E | other | 201 | 0 | 0 2.7K; 14 24; 13 19; 18 19 |
| B25075_025E | other | 165 | 0 | 0 3.0K; 9 16; 11 16; 7 15 |
| B25075_026E | other | 93 | 0 | 0 3.2K; 10 15; 13 11; 12 11 |
| B25075_027E | other | 112 | 0 | 0 3.2K; 11 16; 9 14; 8 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:30:59.20968 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | d7a61b2e-8d0e-43fe-a98e-7 3.5K |
| SRC_SHA256 | who | 1 | 0 | 793e7a8851b0cbaa2ad9ef317 3.5K |
