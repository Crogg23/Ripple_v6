# PORTAL_CKA_HOUSTON_OPEN_DAT_405FBDB44A

rows 3.5K  columns 26  scan 2.9s

roles: audit 2, category 1, date 1, id 1, other 20, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 2; Census Tract 6708.03; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6704; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6723.05; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6716.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6709.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6716.01; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6720.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6729.06; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6728.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6731.07; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6732.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6731.07; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6729.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6706.03; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6705; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6701.01; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6731.09; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6713; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6715.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6708.04; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  4cb775fdaca6bfa2af13147ee2fda919c8439e27fce09a4d7dc3f4e39c7eea68

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6705; Fort B  2026:1
  Block Group 1; Census Tract 6708.04; For  2026:1
  Block Group 1; Census Tract 6709.02; For  2026:1
  Block Group 1; Census Tract 6713; Fort B  2026:1
  Block Group 1; Census Tract 6715.01; For  2026:1
  Block Group 1; Census Tract 6716.01; For  2026:1
  Block Group 1; Census Tract 6728.02; For  2026:1
  Block Group 1; Census Tract 6729.04; For  2026:1
  Block Group 2; Census Tract 6701.01; For  2026:1
  Block Group 2; Census Tract 6704; Fort B  2026:1
  Block Group 2; Census Tract 6706.03; For  2026:1
  Block Group 2; Census Tract 6708.03; For  2026:1
  Block Group 2; Census Tract 6720.04; For  2026:1
  Block Group 2; Census Tract 6723.05; For  2026:1
  Block Group 2; Census Tract 6729.06; For  2026:1
  Block Group 2; Census Tract 6731.07; For  2026:1
  Block Group 3; Census Tract 6716.01; For  2026:1
  Block Group 3; Census Tract 6731.07; For  2026:1
  Block Group 3; Census Tract 6732.02; For  2026:1
  Block Group 4; Census Tract 6731.09; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  4cb775fdaca6bfa2af13147ee2fda919c8439e27  2026:3.5K

## what

B03002_017E: 0 99%, 1 0%, 30 0%, 10 0%, 14 0%, 12 0%, 55 0%, 11 0%, 41 0%, 25 0%, 153 0%, 3 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B03002_001E | other | 2.1K | 0 | 1487 19; 2225 18; 1705 18; 2930 18 |
| B03002_002E | other | 1.8K | 0 | 0 26; 492 19; 1805 18; 1642 18 |
| B03002_003E | other | 1.3K | 0 | 0 224; 1609 18; 1853 18; 665 18 |
| B03002_004E | other | 989 | 0 | 0 614; 15 21; 17 21; 13 21 |
| B03002_005E | other | 67 | 0 | 0 3.2K; 6 25; 4 24; 7 20 |
| B03002_006E | other | 685 | 0 | 0 1.2K; 13 26; 12 25; 9 22 |
| B03002_007E | other | 53 | 0 | 0 3.4K; 13 6; 9 6; 2 5 |
| B03002_008E | other | 152 | 0 | 0 3.0K; 17 19; 10 17; 12 15 |
| B03002_009E | other | 364 | 0 | 0 1.2K; 19 40; 11 37; 10 37 |
| B03002_010E | other | 183 | 0 | 0 2.6K; 12 29; 9 24; 14 23 |
| B03002_011E | other | 308 | 0 | 0 1.4K; 11 44; 7 41; 10 41 |
| B03002_012E | other | 1.6K | 0 | 0 53; 678 19; 446 19; 281 19 |
| B03002_013E | other | 596 | 0 | 0 761; 18 28; 16 28; 12 25 |
| B03002_014E | other | 141 | 0 | 0 3.1K; 11 15; 17 13; 12 13 |
| B03002_015E | other | 205 | 0 | 0 2.8K; 8 22; 15 18; 10 16 |
| B03002_016E | other | 71 | 0 | 0 3.4K; 9 10; 10 8; 12 8 |
| B03002_017E | category | 27 | 0 | 0 3.5K; 1 2; 30 2; 10 2 |
| B03002_018E | other | 788 | 0 | 0 656; 25 26; 14 24; 11 21 |
| B03002_019E | other | 1.0K | 0 | 0 206; 53 20; 121 19; 65 18 |
| B03002_020E | other | 1.0K | 0 | 0 239; 59 20; 175 19; 138 18 |
| B03002_021E | other | 192 | 0 | 0 2.5K; 12 33; 14 27; 8 25 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:31:14.57750 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8b0c2cc9-ac21-4e88-8e31-1 3.5K |
| SRC_SHA256 | who | 1 | 0 | 4cb775fdaca6bfa2af13147ee 3.5K |
