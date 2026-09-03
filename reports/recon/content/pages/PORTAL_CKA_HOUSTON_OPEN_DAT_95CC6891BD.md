# PORTAL_CKA_HOUSTON_OPEN_DAT_95CC6891BD

rows 3.5K  columns 10  scan 2.4s

roles: audit 2, date 1, id 1, other 5, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 3; Census Tract 6704; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6709.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.09; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6709.04; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6708.03; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6710.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6712; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6728.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6714.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6729.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6735.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.08; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6726.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6731.12; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6710.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6701.01; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6731.09; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6709.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6729.07; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6717; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  4ccb6e1832e277df9c88c152139a57697bae9c39023b8e07770774a90b318c6e

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6701.01; For  2026:1
  Block Group 1; Census Tract 6708.03; For  2026:1
  Block Group 1; Census Tract 6709.02; For  2026:1
  Block Group 1; Census Tract 6714.02; For  2026:1
  Block Group 1; Census Tract 6717; Fort B  2026:1
  Block Group 1; Census Tract 6729.04; For  2026:1
  Block Group 1; Census Tract 6729.07; For  2026:1
  Block Group 1; Census Tract 6731.08; For  2026:1
  Block Group 1; Census Tract 6731.09; For  2026:1
  Block Group 2; Census Tract 6709.02; For  2026:1
  Block Group 2; Census Tract 6709.04; For  2026:1
  Block Group 2; Census Tract 6728.02; For  2026:1
  Block Group 2; Census Tract 6731.12; For  2026:1
  Block Group 2; Census Tract 6735.02; For  2026:1
  Block Group 3; Census Tract 6704; Fort B  2026:1
  Block Group 3; Census Tract 6712; Fort B  2026:1
  Block Group 4; Census Tract 6710.01; For  2026:1
  Block Group 4; Census Tract 6710.02; For  2026:1
  Block Group 4; Census Tract 6726.04; For  2026:1
  Block Group 4; Census Tract 6731.09; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  4ccb6e1832e277df9c88c152139a57697bae9c39  2026:3.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B25002_001E | other | 1.2K | 0 | 652 19; 1050 19; 1823 19; 498 19 |
| B25002_002E | other | 1.2K | 0 | 571 19; 279 19; 907 19; 549 19 |
| B25002_003E | other | 280 | 0 | 0 1.0K; 58 35; 22 34; 21 34 |
| B25003_002E | other | 972 | 0 | 0 296; 870 17; 526 17; 825 17 |
| B25003_003E | other | 832 | 0 | 0 220; 54 20; 21 19; 15 19 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:31:34.96490 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8547304d-d11e-4c72-99c7-7 3.5K |
| SRC_SHA256 | who | 1 | 0 | 4ccb6e1832e277df9c88c1521 3.5K |
