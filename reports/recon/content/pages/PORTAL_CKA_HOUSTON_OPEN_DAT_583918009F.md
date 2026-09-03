# PORTAL_CKA_HOUSTON_OPEN_DAT_583918009F

rows 3.5K  columns 12  scan 2.8s

roles: audit 2, date 1, id 1, other 7, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## who

NAME by rows
         1  Block Group 1; Census Tract 6734.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6706.03; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6727.02; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6718; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6714.01; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6718; Fort Bend County; Texas
         1  Block Group 5; Census Tract 6720.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6726.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6720.04; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6727.01; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6730.10; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6729.01; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6722.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6730.06; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6709.04; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6701.01; Fort Bend County; Texas
         1  Block Group 3; Census Tract 6729.06; Fort Bend County; Texas
         1  Block Group 1; Census Tract 6714.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6720.02; Fort Bend County; Texas
         1  Block Group 2; Census Tract 6712; Fort Bend County; Texas

SRC_SHA256 by rows
      3.5K  181a4316cf2771abe993620b283fd822aa9692b5d4f505f1547cb2e887b079ae

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Block Group 1; Census Tract 6714.01; For  2026:1
  Block Group 1; Census Tract 6714.02; For  2026:1
  Block Group 1; Census Tract 6718; Fort B  2026:1
  Block Group 1; Census Tract 6729.01; For  2026:1
  Block Group 1; Census Tract 6730.10; For  2026:1
  Block Group 1; Census Tract 6734.01; For  2026:1
  Block Group 2; Census Tract 6701.01; For  2026:1
  Block Group 2; Census Tract 6712; Fort B  2026:1
  Block Group 2; Census Tract 6718; Fort B  2026:1
  Block Group 2; Census Tract 6720.02; For  2026:1
  Block Group 2; Census Tract 6720.04; For  2026:1
  Block Group 2; Census Tract 6722.02; For  2026:1
  Block Group 2; Census Tract 6726.02; For  2026:1
  Block Group 2; Census Tract 6730.06; For  2026:1
  Block Group 3; Census Tract 6706.03; For  2026:1
  Block Group 3; Census Tract 6709.04; For  2026:1
  Block Group 3; Census Tract 6727.01; For  2026:1
  Block Group 3; Census Tract 6727.02; For  2026:1
  Block Group 3; Census Tract 6729.06; For  2026:1
  Block Group 5; Census Tract 6720.02; For  2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  181a4316cf2771abe993620b283fd822aa9692b5  2026:3.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_ID | id | 3.5K | 0 | 483396947002 18; 483396947001 18; 483396946032 18; 483396946031 18 |
| NAME | who | 3.5K | 0 | Block Group 2; Census Tra 18; Block Group 1; Census Tra 18; Block Group 2; Census Tra 18; Block Group 1; Census Tra 18 |
| B23025_001E | other | 1.8K | 0 | 1454 19; 1359 19; 2072 18; 1264 18 |
| B23025_002E | other | 1.5K | 0 | 708 19; 0 19; 1039 19; 637 19 |
| B23025_003E | other | 1.5K | 0 | 685 19; 708 19; 0 19; 794 19 |
| B23025_004E | other | 1.5K | 0 | 861 19; 859 19; 945 19; 774 19 |
| B23025_005E | other | 302 | 0 | 0 695; 20 43; 14 42; 9 41 |
| B23025_006E | other | 67 | 0 | 0 3.4K; 10 5; 15 5; 14 5 |
| B23025_007E | other | 1.0K | 0 | 398 21; 0 20; 769 19; 659 19 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:31:07.54815 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2c6dce38-3818-4fbf-8e2a-6 3.5K |
| SRC_SHA256 | who | 1 | 0 | 181a4316cf2771abe993620b2 3.5K |
