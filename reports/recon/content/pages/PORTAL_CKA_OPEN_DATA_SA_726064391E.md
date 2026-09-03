# PORTAL_CKA_OPEN_DATA_SA_726064391E

rows 292  columns 26  scan 5.3s

roles: amount 4, audit 2, category 7, date 5, empty 2, other 6, who 1

## when

SCHEDULE_START
  2024        12  #####
  2025        67  ##############################
  2026        64  #############################

SCHEDULE_FINISH
  2024        12  #####
  2025        67  ##############################
  2026        64  #############################

ACTUAL_START
  2024        12  #####
  2025        71  ##############################
  2026        34  ##############

ACTUAL_FINISH
  2024        12  #####
  2025        71  ##############################
  2026        34  ##############

INGESTED_AT
  2026       292  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ESTIMATED_TOTAL_COST | 292 | 4.1K | 23.1K | 118.2K | 681.0K | 9.14M |
| INSIDE_X | 292 | 2.07M | 2.12M | 2.16M | 2.17M | 620.67M |
| INSIDE_Y | 292 | 13.67M | 13.73M | 13.76M | 13.76M | 4.01B |
| SHAPE__LENGTH | 292 | 126.99 | 595.01 | 1.7K | 2.1K | 197.6K |

## who

SRC_SHA256 by rows
       292  3bea0a849affd9476b1563f24833ca30577e89b3677788a87f2136610f5cd5f3

SRC_SHA256 by dollars
       9.14M      292 rows  3bea0a849affd9476b1563f24833ca30577e89b3677788a87f2136610f5c

## who x when

SRC_SHA256 by SCHEDULE_START, dollars = ESTIMATED_TOTAL_COST
  3bea0a849affd9476b1563f24833ca30577e89b3  2024:257.9K 2025:1.48M 2026:1.51M

## what

PROJECT_CATEGORY: IMP Alley 91%, NSA-IMP 9%

FISCAL_YEAR: 2026 27%, 2025 22%, 2030 15%, 2029 14%, 2028 13%, 2027 9%

COUNCIL_DISTRICT: 1 29%, 9 12%, 10 11%, 8 11%, 3 10%, 2 8%, 7 8%, 5 8%, 4 4%, 6 1%

APPLICATION: SA - Single Course Treatment 100%, Earthen Alley - Regrading 0%

COMPLETE: 95 100%

PROJECT_MANAGER: Robert Morales 83%, Gustavo Aguilera 17%

CONTACT: Maria Zertuche: 210-207-5069 44%, Maria Zertuche: (210) 207-5069 38%, Joe Hinojosa: (210) 207-2799 17%, 0 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 292 | 0 | 292 2; 291 2; 290 2; 289 2 |
| SMPPROJECTID | other | 293 | 0 | 50108 2; 50103 2; 50093 2; 50091 2 |
| SEGMENT_COUNT | other | 1 | 0 | 1 292 |
| PROJECT_CATEGORY | category | 2 | 0 | IMP Alley 267; NSA-IMP 25 |
| PROJECT_TYPE | empty | 1 | 292 |  |
| FISCAL_YEAR | category | 6 | 0 | 2026 79; 2025 64; 2030 45; 2029 40 |
| COUNCIL_DISTRICT | category | 10 | 0 | 1 84; 9 35; 10 32; 8 31 |
| PROJECT_STREET | other | 289 | 0 | A-50108 2; A-50103 2; A-50093 2; A-50091 2 |
| IN_BETWEEN | other | 240 | 0 | Saunders & W Cesar Chavez 6; Buena Vista St & Monterey 5; Sage Trl & Winding Crk 3; Knights Wood & Voelcker R 3 |
| STREET_FROM | other | 220 | 0 | Budding Blvd 5; St Cloud 4; Whiting 4; Kampmann Blvd 4 |
| APPLICATION | category | 3 | 24 | SA - Single Course Treatm 267; Earthen Alley - Regrading 1 |
| ESTIMATED_TOTAL_COST | amount | 287 | 0 | 55540.6735 2; 9497.0078 2; 27475.0393604899 2; 59788.3739392731 2 |
| SCHEDULE_START | date | 91 | 149 | 4/1/2026 6:00:00 AM 25; 3/31/2026 6:00:00 AM 5; 9/1/2025 6:00:00 AM 4; 3/23/2026 6:00:00 AM 3 |
| SCHEDULE_FINISH | date | 83 | 149 | 9/30/2026 6:00:00 AM 26; 3/20/2026 6:00:00 AM 5; 4/17/2026 6:00:00 AM 5; 9/30/2025 6:00:00 AM 5 |
| ACTUAL_START | date | 98 | 175 | 1/28/2026 6:00:00 AM 3; 3/31/2026 6:00:00 AM 3; 3/24/2026 6:00:00 AM 3; 8/16/2025 6:00:00 AM 3 |
| ACTUAL_FINISH | date | 104 | 175 | 1/30/2026 6:00:00 AM 3; 1/23/2025 6:00:00 AM 2; 12/11/2025 6:00:00 AM 2; 4/16/2026 6:00:00 AM 2 |
| COMPLETE | category | 2 | 178 | 95 114 |
| PROJECT_MANAGER | category | 3 | 150 | Robert Morales 118; Gustavo Aguilera 24 |
| CONTACT | category | 5 | 149 | Maria Zertuche: 210-207-5 63; Maria Zertuche: (210) 207 54; Joe Hinojosa: (210) 207-2 24; 0 2 |
| CLASSIFICATION | empty | 1 | 292 |  |
| INSIDE_X | amount | 291 | 0 | 2067375.94805714 2; 2115142.61496178 2; 2118179.3799673 2; 2118009.66160311 2 |
| INSIDE_Y | amount | 290 | 0 | 13731521.8699149 2; 13735454.3122541 2; 13755480.3046623 2; 13754901.7467747 2 |
| SHAPE__LENGTH | amount | 288 | 0 | 935.815818554351 2; 364.748518483055 2; 403.356244951982 2; 802.519600140975 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:38:41.85101 292 |
| SOURCE_RUN_ID | audit | 1 | 0 | c9647b9c-8a43-4407-bac6-5 292 |
| SRC_SHA256 | who | 1 | 0 | 3bea0a849affd9476b1563f24 292 |
