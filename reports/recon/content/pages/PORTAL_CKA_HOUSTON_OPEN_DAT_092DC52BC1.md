# PORTAL_CKA_HOUSTON_OPEN_DAT_092DC52BC1

rows 3.5K  columns 54  scan 2.9s

roles: audit 2, date 1, id 1, other 49, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 1; Census Tract 6721; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6702.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6716.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6707; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6729.03; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6710.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6713; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6727.03; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6720.03; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6730.08; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6720.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6731.09; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6724.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6720.04; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6704; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6701.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6719; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6730.08; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6708.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6704; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  7ac2a2d4079992d897bde1ff1e343afc924e8f5fdb7687c0b8fff338b7a588de

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6701.02; For  2026:1
  Block Group 1; Census Tract 6704; Fort B  2026:1
  Block Group 1; Census Tract 6708.01; For  2026:1
  Block Group 1; Census Tract 6713; Fort B  2026:1
  Block Group 1; Census Tract 6720.03; For  2026:1
  Block Group 1; Census Tract 6721; Fort B  2026:1
  Block Group 1; Census Tract 6724.02; For  2026:1
  Block Group 1; Census Tract 6727.03; For  2026:1
  Block Group 1; Census Tract 6730.08; For  2026:1
  Block Group 2; Census Tract 6716.02; For  2026:1
  Block Group 2; Census Tract 6719; Fort B  2026:1
  Block Group 2; Census Tract 6720.04; For  2026:1
  Block Group 2; Census Tract 6731.09; For  2026:1
  Block Group 3; Census Tract 6704; Fort B  2026:1
  Block Group 3; Census Tract 6707; Fort B  2026:1
  Block Group 3; Census Tract 6710.02; For  2026:1
  Block Group 3; Census Tract 6720.04; For  2026:1
  Block Group 3; Census Tract 6729.03; For  2026:1
  Block Group 3; Census Tract 6730.08; For  2026:1
  Block Group 4; Census Tract 6702.02; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  7ac2a2d4079992d897bde1ff1e343afc924e8f5f  2026:3.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B01001_001E | other | 2.1K | 0 | 1487 19; 2225 18; 1705 18; 2930 18 |
| B01001_002E | other | 1.5K | 0 | 1412 19; 990 19; 747 19; 614 19 |
| B01001_003E | other | 336 | 0 | 0 929; 16 37; 20 37; 24 35 |
| B01001_004E | other | 355 | 0 | 0 856; 36 36; 24 35; 20 35 |
| B01001_005E | other | 354 | 0 | 0 797; 16 36; 14 34; 12 33 |
| B01001_006E | other | 259 | 0 | 0 1.2K; 14 38; 21 36; 37 36 |
| B01001_007E | other | 203 | 0 | 0 1.7K; 17 43; 10 43; 13 41 |
| B01001_008E | other | 138 | 0 | 0 2.5K; 14 34; 17 33; 11 31 |
| B01001_009E | other | 149 | 0 | 0 2.5K; 15 34; 22 27; 14 27 |
| B01001_010E | other | 239 | 0 | 0 1.3K; 20 51; 16 49; 14 49 |
| B01001_011E | other | 329 | 0 | 0 695; 14 46; 16 45; 44 37 |
| B01001_012E | other | 331 | 0 | 0 641; 18 44; 35 41; 23 37 |
| B01001_013E | other | 322 | 0 | 0 622; 26 38; 28 38; 23 37 |
| B01001_014E | other | 328 | 0 | 0 626; 35 41; 24 41; 29 39 |
| B01001_015E | other | 298 | 0 | 0 696; 13 52; 25 40; 26 37 |
| B01001_016E | other | 285 | 0 | 0 726; 17 47; 11 41; 18 37 |
| B01001_017E | other | 262 | 0 | 0 712; 25 48; 22 45; 13 45 |
| B01001_018E | other | 165 | 0 | 0 1.6K; 11 73; 10 63; 12 55 |
| B01001_019E | other | 180 | 0 | 0 1.2K; 15 55; 20 55; 12 54 |
| B01001_020E | other | 143 | 0 | 0 1.7K; 9 67; 10 65; 12 64 |
| B01001_021E | other | 168 | 0 | 0 1.4K; 10 83; 13 79; 12 63 |
| B01001_022E | other | 188 | 0 | 0 1.1K; 19 63; 12 58; 14 57 |
| B01001_023E | other | 138 | 0 | 0 1.5K; 12 73; 9 69; 7 68 |
| B01001_024E | other | 112 | 0 | 0 2.1K; 9 77; 12 64; 10 64 |
| B01001_025E | other | 107 | 0 | 0 2.4K; 10 53; 12 51; 8 50 |
| B01001_026E | other | 1.5K | 0 | 1140 19; 977 19; 814 19; 1017 18 |
| B01001_027E | other | 336 | 0 | 0 963; 33 38; 25 35; 22 34 |
| B01001_028E | other | 339 | 0 | 0 824; 12 42; 23 38; 29 37 |
| B01001_029E | other | 343 | 0 | 0 865; 30 36; 15 33; 41 30 |
| B01001_030E | other | 245 | 0 | 0 1.2K; 16 46; 25 40; 21 37 |
| B01001_031E | other | 198 | 0 | 0 1.9K; 20 43; 14 40; 15 39 |
| B01001_032E | other | 142 | 0 | 0 2.6K; 11 29; 20 26; 14 26 |
| B01001_033E | other | 152 | 0 | 0 2.5K; 12 31; 14 28; 15 27 |
| B01001_034E | other | 247 | 0 | 0 1.3K; 23 39; 10 38; 26 37 |
| B01001_035E | other | 332 | 0 | 0 697; 16 40; 19 40; 24 37 |
| B01001_036E | other | 332 | 0 | 0 579; 28 39; 17 39; 18 38 |
| B01001_037E | other | 331 | 0 | 0 595; 18 44; 25 44; 22 40 |
| B01001_038E | other | 330 | 0 | 0 591; 27 40; 14 39; 12 36 |
| B01001_039E | other | 308 | 0 | 0 627; 18 45; 32 41; 20 41 |
| B01001_040E | other | 287 | 0 | 0 650; 25 44; 17 40; 12 40 |
| B01001_041E | other | 260 | 0 | 0 637; 17 53; 11 44; 13 44 |
| B01001_042E | other | 155 | 0 | 0 1.5K; 11 75; 12 59; 10 56 |
| B01001_043E | other | 186 | 0 | 0 1.1K; 14 60; 12 59; 20 55 |
| B01001_044E | other | 155 | 0 | 0 1.6K; 14 72; 10 70; 8 69 |
| B01001_045E | other | 166 | 0 | 0 1.3K; 14 71; 13 65; 11 64 |
| B01001_046E | other | 202 | 0 | 0 934; 12 64; 11 62; 18 59 |
| B01001_047E | other | 160 | 0 | 0 1.4K; 11 78; 12 62; 14 60 |
| B01001_048E | other | 134 | 0 | 0 1.9K; 9 76; 8 71; 11 70 |
| B01001_049E | other | 146 | 0 | 0 2.0K; 10 75; 8 60; 12 59 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:31:43.04847 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1851db4c-e618-4eca-a5f7-1 3.5K |
| SRC_SHA256 | who | 1 | 0 | 7ac2a2d4079992d897bde1ff1 3.5K |
