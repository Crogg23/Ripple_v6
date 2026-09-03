# PORTAL_CKA_HOUSTON_OPEN_DAT_6082321C0C

rows 3.5K  columns 22  scan 3.3s

roles: audit 2, date 1, id 1, other 17, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 1; Census Tract 6716.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6712; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6709.04; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6721; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6717; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6723.05; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6723.05; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6734.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6731.09; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6740.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6720.04; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6710.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.10; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6710.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6714.02; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6711.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6716.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6720.03; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6709.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6721; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  1b2018e9efa3ace9ae4b88342a2b820a6d51ce1175f84f03c1a535d5ded47a95

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6709.04; For  2026:1
  Block Group 1; Census Tract 6710.01; For  2026:1
  Block Group 1; Census Tract 6710.02; For  2026:1
  Block Group 1; Census Tract 6712; Fort B  2026:1
  Block Group 1; Census Tract 6716.01; For  2026:1
  Block Group 1; Census Tract 6716.02; For  2026:1
  Block Group 1; Census Tract 6720.03; For  2026:1
  Block Group 1; Census Tract 6723.05; For  2026:1
  Block Group 1; Census Tract 6731.10; For  2026:1
  Block Group 1; Census Tract 6740.02; For  2026:1
  Block Group 2; Census Tract 6709.02; For  2026:1
  Block Group 2; Census Tract 6717; Fort B  2026:1
  Block Group 2; Census Tract 6721; Fort B  2026:1
  Block Group 2; Census Tract 6723.05; For  2026:1
  Block Group 2; Census Tract 6734.01; For  2026:1
  Block Group 3; Census Tract 6714.02; For  2026:1
  Block Group 3; Census Tract 6720.04; For  2026:1
  Block Group 3; Census Tract 6721; Fort B  2026:1
  Block Group 3; Census Tract 6731.09; For  2026:1
  Block Group 4; Census Tract 6711.02; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  1b2018e9efa3ace9ae4b88342a2b820a6d51ce11  2026:3.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B19001_001E | other | 1.2K | 0 | 571 19; 279 19; 907 19; 549 19 |
| B19001_002E | other | 228 | 0 | 0 1.2K; 13 57; 14 54; 21 54 |
| B19001_003E | other | 179 | 0 | 0 1.9K; 11 51; 13 48; 12 47 |
| B19001_004E | other | 165 | 0 | 0 1.9K; 10 61; 13 50; 14 49 |
| B19001_005E | other | 175 | 0 | 0 1.7K; 11 55; 14 53; 10 52 |
| B19001_006E | other | 163 | 0 | 0 1.7K; 15 50; 11 48; 10 47 |
| B19001_007E | other | 183 | 0 | 0 1.6K; 9 59; 11 58; 13 56 |
| B19001_008E | other | 184 | 0 | 0 1.6K; 9 58; 12 57; 15 55 |
| B19001_009E | other | 180 | 0 | 0 1.6K; 11 59; 13 52; 8 52 |
| B19001_010E | other | 179 | 0 | 0 1.7K; 10 57; 9 53; 14 49 |
| B19001_011E | other | 243 | 0 | 0 900; 16 55; 8 52; 19 51 |
| B19001_012E | other | 287 | 0 | 0 526; 42 49; 26 44; 17 43 |
| B19001_013E | other | 346 | 0 | 0 399; 41 37; 52 36; 49 35 |
| B19001_014E | other | 318 | 0 | 0 627; 11 41; 37 40; 19 40 |
| B19001_015E | other | 286 | 0 | 0 977; 13 56; 18 50; 16 48 |
| B19001_016E | other | 329 | 0 | 0 851; 16 40; 21 36; 12 36 |
| B19001_017E | other | 469 | 0 | 0 998; 13 45; 19 33; 16 31 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:31:21.05462 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 924f9687-8792-42eb-a212-7 3.5K |
| SRC_SHA256 | who | 1 | 0 | 1b2018e9efa3ace9ae4b88342 3.5K |
