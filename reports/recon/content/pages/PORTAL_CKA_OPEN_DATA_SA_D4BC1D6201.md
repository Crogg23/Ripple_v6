# PORTAL_CKA_OPEN_DATA_SA_D4BC1D6201

rows 101  columns 5  scan 2.1s

roles: audit 2, date 1, other 2, who 1

## when

INGESTED_AT
  2026       101  ##############################

## who

SRC_SHA256 by rows
       101  0b3ca8b39ac0e89a518177f1a73fe379814931adb1013e6a09c9c802f4edd534

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  0b3ca8b39ac0e89a518177f1a73fe379814931ad  2026:101

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ZIPCODE | other | 102 | 0 | 78238 1; 78003 1; 78006 1; 78284 1 |
| ESTABLISHMENTS | other | 96 | 0 | 10 2; 77 2; 82 2; 12 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:31:55.54890 101 |
| SOURCE_RUN_ID | audit | 1 | 0 | b8e9d5ce-d2e0-4d4e-bf67-4 101 |
| SRC_SHA256 | who | 1 | 0 | 0b3ca8b39ac0e89a518177f1a 101 |
