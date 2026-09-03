# PORTAL_CKA_HOUSTON_OPEN_DAT_AEFB1B6A56

rows 3.5K  columns 7  scan 2.5s

roles: audit 2, date 1, id 1, other 2, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 3; Census Tract 6715.01; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6709.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6716.02; Fort Bend County; Texas
         1  Block Group 5; Census Tract 6720.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6718; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6722.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6724.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6727.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6725; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6727.03; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6735.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6729.05; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6725; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6710.02; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6710.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6701.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6730.09; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6720.02; Fort Bend County; Texas
         1  Block Group 4; Census Tract 6715.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6711.02; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  1c664be9cc0d4bf4f553b48f951dc788fb7f80a21fd75fd52f574bcdac383f2d

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6701.01; For  2026:1
  Block Group 1; Census Tract 6711.02; For  2026:1
  Block Group 1; Census Tract 6718; Fort B  2026:1
  Block Group 1; Census Tract 6725; Fort B  2026:1
  Block Group 1; Census Tract 6729.05; For  2026:1
  Block Group 2; Census Tract 6709.02; For  2026:1
  Block Group 2; Census Tract 6710.02; For  2026:1
  Block Group 2; Census Tract 6716.02; For  2026:1
  Block Group 2; Census Tract 6722.02; For  2026:1
  Block Group 2; Census Tract 6727.01; For  2026:1
  Block Group 2; Census Tract 6735.01; For  2026:1
  Block Group 3; Census Tract 6710.01; For  2026:1
  Block Group 3; Census Tract 6715.01; For  2026:1
  Block Group 3; Census Tract 6724.02; For  2026:1
  Block Group 3; Census Tract 6727.03; For  2026:1
  Block Group 3; Census Tract 6730.09; For  2026:1
  Block Group 4; Census Tract 6715.01; For  2026:1
  Block Group 4; Census Tract 6720.02; For  2026:1
  Block Group 4; Census Tract 6725; Fort B  2026:1
  Block Group 5; Census Tract 6720.02; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  1c664be9cc0d4bf4f553b48f951dc788fb7f80a2  2026:3.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B19013_001E | other | 3.0K | 0 | - 324; 250000 75; 81875 16; 116932 16 |
| B25077_001E | other | 2.2K | 0 | - 617; 2000000 17; 167000 16; 225000 16 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:30:28.54024 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3cf2a4cf-559a-4a92-854a-1 3.5K |
| SRC_SHA256 | who | 1 | 0 | 1c664be9cc0d4bf4f553b48f9 3.5K |
