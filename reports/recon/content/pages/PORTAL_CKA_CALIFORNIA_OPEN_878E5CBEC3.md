# PORTAL_CKA_CALIFORNIA_OPEN_878E5CBEC3

rows 7.0K  columns 13  scan 2.3s

roles: audit 2, category 9, date 1, id 1, who 1

## when

INGESTED_AT
  2026      7.0K  ##############################

## who

SRC_SHA256 by rows
      7.0K  b7949131e8f81223035cac938b73ef84af1054fac09248136c08962d2c8f96f0

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  b7949131e8f81223035cac938b73ef84af1054fa  2026:7.0K

## what

TEST_NAME: Chronic Wasting Disease - IHC 63%, Chronic Wasting Disease - cELI 37%

RESULT: Negative 96%, No Result 2%, Pending 2%, Positive 0%

SEX: Male 83%, Female 14%, Unknown 3%, Not Recorded 0%

AGE: Adult 56%, Unknown 34%, 2nd Year 8%, 1st Year 2%, Sub-adult 0%

HUNT_ZONE: A (South Unit 110) 15%, C4 12%, D5 10%, B2 9%, B1 9%, X12 8%, D7 8%, A (North Unit 160) 7%, D6 7%, X9a 6%, D8 5%, D3 4%

YEAR: 2004 12%, 2003 9%, 2002 9%, 2007 9%, 2008 9%, 2023 9%, 2005 8%, 2006 8%, 2022 8%, 2001 7%, 2020 7%, 2021 7%

DSU: DSU 2 24%, DSU 4 23%, DSU 5 19%, DSU 1 18%, DSU 3 16%, NA 0%

SAMPLE_TYPE: Hunter Harvest 79%, Roadkill 9%, Clinical Suspect 7%, All Other Mortality 3%, Not Recorded 2%, Mortality/Non-CWD Suspect 0%

SPECIES: Native Deer 92%, Native Elk 7%, Other 1%, NA 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 6.9K | 0 | 6950 35; 6949 35; 6948 35; 6947 35 |
| TEST_NAME | category | 2 | 0 | Chronic Wasting Disease - 4.4K; Chronic Wasting Disease - 2.6K |
| RESULT | category | 4 | 0 | Negative 6.6K; No Result 168; Pending 133; Positive 2 |
| SEX | category | 5 | 5 | Male 5.7K; Female 984; Unknown 221; Not Recorded 3 |
| AGE | category | 6 | 3 | Adult 3.9K; Unknown 2.3K; 2nd Year 558; 1st Year 129 |
| HUNT_ZONE | category | 50 | 0 | A (South Unit 110) 735; C4 599; D5 508; B2 413 |
| YEAR | category | 26 | 0 | 2004 659; 2003 502; 2002 484; 2007 482 |
| DSU | category | 6 | 0 | DSU 2 1.7K; DSU 4 1.6K; DSU 5 1.3K; DSU 1 1.2K |
| SAMPLE_TYPE | category | 6 | 0 | Hunter Harvest 5.5K; Roadkill 632; Clinical Suspect 460; All Other Mortality 197 |
| SPECIES | category | 4 | 0 | Native Deer 6.4K; Native Elk 475; Other 53; NA 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:35:58.39685 7.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 6ddb8646-8d4d-4cd1-b016-d 7.0K |
| SRC_SHA256 | who | 1 | 0 | b7949131e8f81223035cac938 7.0K |
