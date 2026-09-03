# PORTAL_CKA_OPEN_DATA_SA_146EBE0CC0

rows 816  columns 30  scan 4.1s

roles: amount 4, audit 2, category 10, date 5, empty 1, other 8, who 1

## when

SCHEDULE_START
  2024        41  ##########
  2025       128  ##############################
  2026       126  ##############################

SCHEDULE_FINISH
  2024        24  #####
  2025       132  ############################
  2026       139  ##############################

ACTUAL_START
  2024        41  ##########
  2025       129  ##############################
  2026        64  ###############

ACTUAL_FINISH
  2024        27  ######
  2025       131  ##############################
  2026        58  #############

INGESTED_AT
  2026       816  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ESTIMATED_TOTAL_COST | 816 | 2.0K | 76.2K | 307.2K | 784.7K | 75.18M |
| PROJECT_LENGTH | 816 | 56.43 | 1.7K | 7.2K | 11.0K | 1.62M |
| X | 816 | 2.06M | 2.12M | 2.17M | 2.17M | 1.73B |
| Y | 816 | 13.66M | 13.71M | 13.76M | 13.78M | 11.19B |

## who

SRC_SHA256 by rows
       816  618ad333ce22d943a643f5f6ed5d9f983e242ec219a51bfa138e6de4f343d272

SRC_SHA256 by dollars
      75.18M      816 rows  618ad333ce22d943a643f5f6ed5d9f983e242ec219a51bfa138e6de4f343

## who x when

SRC_SHA256 by SCHEDULE_START, dollars = ESTIMATED_TOTAL_COST
  618ad333ce22d943a643f5f6ed5d9f983e242ec2  2024:5.35M 2025:12.95M 2026:10.88M

## what

SEGMENT_COUNT: 2 30%, 4 18%, 3 13%, 5 10%, 1 9%, 6 7%, 8 4%, 7 3%, 9 2%, 10 1%, 11 1%, 12 1%

PROJECT_CATEGORY: SW Repair 53%, IMP Sidewalk 47%

COUNCIL_DISTRICT: 1 12%, 3 12%, 5 12%, 7 11%, 4 11%, 6 11%, 2 10%, 10 7%, 8 7%, 9 6%, 0 0%

SIDE_OF_STREET: Both Sides 76%, West Side 7%, East Side 6%, North Side 6%, South Side 5%

FISCAL_YEAR: 2025 20%, 2029 17%, 2026 17%, 2028 16%, 2027 16%, 2030 14%

PERCENT_COMPLETE: 100 81%, 0 7%, 1 2%, 2 2%, 99 2%, 5 1%, 90 1%, 65 1%, 92 1%, 95 1%, 15 0%

PROJECT_TYPE: Sidewalk Reconstruction 55%, Sidewalks 45%

PROJECT_MANAGER: Harry Trumble 16%, Haralampos Trumble 15%, 151385 15%, 154817 14%, 159039 10%, 154360 9%, 140085 7%, 154811 7%, 157496 6%, 154336 1%, Jose 0%

CONTACT: Erick Wildestorm: (210) 461-15 39%, Keith Schoonmaker: (210) 303-4 29%, Maria Zertuche: (210) 207-5069 17%, Maria Zertuche: 210-207-5069 15%, 0 0%

PROJECT_STATUS: Complete 56%, Construction 13%, Planning 10%, Punchlists 7%, Warrantee 5%, Precon 4%, Pending Final 3%, Pending Final Walk 0%, Pending Construction 0%, Completed 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 798 | 0 | 816 5; 815 5; 814 5; 813 5 |
| SWPROJECTID | other | 809 | 0 | 4124 5; 4076 5; 4070 5; 4069 5 |
| SEGMENT_COUNT | category | 21 | 0 | 2 243; 4 145; 3 107; 5 77 |
| PROJECT_CATEGORY | category | 2 | 0 | SW Repair 434; IMP Sidewalk 382 |
| COUNCIL_DISTRICT | category | 11 | 0 | 1 102; 3 95; 5 95; 7 93 |
| PROJECT_STREET | other | 721 | 1 | Lands Run 7; Oakline Dr 5; Westchester 5; Mission Vista 5 |
| FROM_STREET | other | 544 | 0 | Cul-de-sac 36; S Presa St 10; Dead End 10; Dewhurst Rd 9 |
| TO_STREET | other | 523 | 1 | Cul-de-sac 57; Dead End 27; City Limits 14; Semlinger Rd 9 |
| SIDE_OF_STREET | category | 5 | 0 | Both Sides 619; West Side 59; East Side 48; North Side 46 |
| ESTIMATED_TOTAL_COST | amount | 766 | 0 | 25944 6; 25309.5 6; 64860 5; 102274.7869 5 |
| FISCAL_YEAR | category | 6 | 0 | 2025 160; 2029 140; 2026 135; 2028 133 |
| SCORE | other | 86 | 0 | 30 83; 20 79; 17 76; 7 65 |
| SCHEDULE_START | date | 153 | 521 | 9/2/2025 6:00:00 AM 8; 10/20/2025 6:00:00 AM 6; 6/15/2026 6:00:00 AM 6; 10/6/2025 6:00:00 AM 5 |
| SCHEDULE_FINISH | date | 200 | 521 | 9/30/2026 6:00:00 AM 6; 10/1/2025 6:00:00 AM 6; 12/23/2025 6:00:00 AM 5; 6/22/2026 6:00:00 AM 4 |
| ACTUAL_START | date | 134 | 582 | 10/6/2025 6:00:00 AM 7; 9/2/2025 6:00:00 AM 6; 7/28/2025 6:00:00 AM 6; 8/18/2025 6:00:00 AM 6 |
| ACTUAL_FINISH | date | 146 | 600 | 8/15/2025 6:00:00 AM 10; 3/27/2026 6:00:00 AM 4; 11/22/2024 6:00:00 AM 4; 9/25/2025 6:00:00 AM 4 |
| PERCENT_COMPLETE | category | 18 | 553 | 100 209; 0 19; 1 6; 2 6 |
| PROJECT_TYPE | category | 3 | 521 | Sidewalk Reconstruction 162; Sidewalks 133 |
| PROJECT_MANAGER | category | 13 | 521 | Harry Trumble 48; Haralampos Trumble 44; 151385 43; 154817 41 |
| CONTACT | category | 6 | 521 | Erick Wildestorm: (210) 4 114; Keith Schoonmaker: (210)  87; Maria Zertuche: (210) 207 49; Maria Zertuche: 210-207-5 44 |
| PROJECT_LENGTH | amount | 819 | 0 | 10983.84 5; 1096.23 5; 2666.01 5; 994.32 5 |
| SIDEWALK_INSTALLED_FT | other | 662 | 0 | 500 15; 1000 11; 1200 8; 600 8 |
| PROJECT_STATUS | category | 11 | 569 | Complete 139; Construction 33; Planning 25; Punchlists 17 |
| CLASSIFICATION | empty | 1 | 816 |  |
| ORIG_FID | other | 798 | 0 | 800 5; 799 5; 798 5; 797 5 |
| X | amount | 813 | 0 | 2139815.92265214 5; 2144031.28725289 5; 2146452.86672731 5; 2161492.73166063 5 |
| Y | amount | 797 | 0 | 13755398.5690974 5; 13737694.3292435 5; 13668991.2727522 5; 13754676.5433105 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:23:24.16382 816 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0b19ecee-d44b-488c-9090-b 816 |
| SRC_SHA256 | who | 1 | 0 | 618ad333ce22d943a643f5f6e 816 |
