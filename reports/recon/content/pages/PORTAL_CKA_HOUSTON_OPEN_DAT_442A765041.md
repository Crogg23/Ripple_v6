# PORTAL_CKA_HOUSTON_OPEN_DAT_442A765041

rows 3.5K  columns 6  scan 3.3s

roles: audit 2, date 1, id 1, other 1, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 2; Census Tract 6736; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6705; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6711.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6720.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6716.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6721; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6727.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6731.13; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6727.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6739.04; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6730.09; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6729.03; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6731.03; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6711.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6706.04; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6701.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6730.08; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6717; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6711.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6708.03; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  7928a3a1779bffac69a6af10d58ed2eedcb5bab33fffdfeeb92e2275f4723c93

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6701.01; For  2026:1
  Block Group 1; Census Tract 6706.04; For  2026:1
  Block Group 1; Census Tract 6708.03; For  2026:1
  Block Group 1; Census Tract 6711.01; For  2026:1
  Block Group 1; Census Tract 6711.02; For  2026:1
  Block Group 1; Census Tract 6721; Fort B  2026:1
  Block Group 1; Census Tract 6731.03; For  2026:1
  Block Group 2; Census Tract 6705; Fort B  2026:1
  Block Group 2; Census Tract 6711.02; For  2026:1
  Block Group 2; Census Tract 6716.01; For  2026:1
  Block Group 2; Census Tract 6717; Fort B  2026:1
  Block Group 2; Census Tract 6720.04; For  2026:1
  Block Group 2; Census Tract 6729.03; For  2026:1
  Block Group 2; Census Tract 6736; Fort B  2026:1
  Block Group 3; Census Tract 6727.01; For  2026:1
  Block Group 3; Census Tract 6727.02; For  2026:1
  Block Group 3; Census Tract 6730.08; For  2026:1
  Block Group 3; Census Tract 6730.09; For  2026:1
  Block Group 3; Census Tract 6731.13; For  2026:1
  Block Group 3; Census Tract 6739.04; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  7928a3a1779bffac69a6af10d58ed2eedcb5bab3  2026:3.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B25064_001E | other | 1.3K | 0 | - 1.0K; 3500 26; 1435 14; 1612 14 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:30:45.43524 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | c81a0b82-1f46-423a-8fcd-b 3.5K |
| SRC_SHA256 | who | 1 | 0 | 7928a3a1779bffac69a6af10d 3.5K |
