# PORTAL_CKA_ANALYZE_BOSTON_941E6C1D15

rows 26  columns 12  scan 2.8s

roles: amount 3, audit 2, category 5, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        26  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LIBRARIES | 25 | 1 | 14 | 27.76 | 28 | 362 |
| POINT_X | 26 | -71.17 | -71.08 | -71.03 | -71.03 | -1.8K |
| POINT_Y | 26 | 42.26 | 42.33 | 42.38 | 42.38 | 1.1K |

## who

SRC_SHA256 by rows
        26  dc0cb5fdd4178d0ce29f61820ba3ca3ebc46898f4adc95167fb573db4dff203b

SRC_SHA256 by dollars
       -1.8K       26 rows  dc0cb5fdd4178d0ce29f61820ba3ca3ebc46898f4adc95167fb573db4dff

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  dc0cb5fdd4178d0ce29f61820ba3ca3ebc46898f  2026:-1.8K

## what

DISTRICT: DORCHESTER 24%, BRIGHTON 14%, ROXBURY 10%, MATTAPAN 10%, JAMAICA PLAIN 10%, CHINATOWN 5%,  SOUTH BOSTON 5%, WEST ROXBURY 5%, MISSION HILL 5%, ROSLINDALE 5%, EAST BOSTON 5%, CHARLESTOWN 5%

ST_ADDRESS: 2 Boylston St 8%, 646 East Broadway 8%, 1961 Centre St 8%, 1497 Tremont St 8%, 41 Geneva Ave 8%, 2044 Columbus Av 8%, 4246 Washington St 8%, 1350 Blue Hill Avenue 8%, 30 South St 8%, 365 Bremen St 8%, 500 Columbia Rd 8%, 27 Richmond St 8%

BRANCH: Chinatown 8%, South Boston 8%, West Roxbury 8%, Parker Hill 8%, Grove Hall 8%, Egleston Square 8%, Roslindale 8%, Mattapan 8%, Jamaica Plain 8%, East Boston 8%, Uphams Corner 8%, Lower Mills 8%

ZIPCODE: 02116 11%, 02119 11%, 02130 11%, 02124 11%, 02122 11%, 02135 11%, 02127 6%, 02132 6%, 02120 6%, 02121 6%, 02131 6%, 02126 6%

SHAPE_WKT: POINT (-71.063135877999969 42. 8%, POINT (-71.038718008999979 42. 8%, POINT (-71.157449492999945 42. 8%, POINT (-71.099078858999974 42. 8%, POINT (-71.081193170999939 42. 8%, POINT (-71.095631586999957 42. 8%, POINT (-71.128653960999941 42. 8%, POINT (-71.093139234999967 42. 8%, POINT (-71.11487789399996 42.3 8%, POINT (-71.028576660999988 42. 8%, POINT (-71.067534205999948 42. 8%, POINT (-71.06850832799995 42.2 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | empty | 1 | 26 |  |
| LIBRARIES | amount | 26 | 1 | 28.000000000000000 1; 27.000000000000000 1; 25.000000000000000 1; 24.000000000000000 1 |
| DISTRICT | category | 17 | 0 | DORCHESTER 5; BRIGHTON 3; ROXBURY 2; MATTAPAN 2 |
| ST_ADDRESS | category | 26 | 0 | 2 Boylston St 1; 646 East Broadway 1; 1961 Centre St 1; 1497 Tremont St 1 |
| BRANCH | category | 26 | 0 | Chinatown 1; South Boston 1; West Roxbury 1; Parker Hill 1 |
| ZIPCODE | category | 20 | 0 | 02116 2; 02119 2; 02130 2; 02124 2 |
| SHAPE_WKT | category | 26 | 0 | POINT (-71.06313587799996 1; POINT (-71.03871800899997 1; POINT (-71.15744949299994 1; POINT (-71.09907885899997 1 |
| POINT_X | amount | 26 | 0 | -71.063135877999969 1; -71.038718008999979 1; -71.157449492999945 1; -71.099078858999974 1 |
| POINT_Y | amount | 26 | 0 | 42.352131293000070 1; 42.335827368000025 1; 42.283387090000076 1; 42.332452701000079 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:18:51.77687 26 |
| SOURCE_RUN_ID | audit | 1 | 0 | fb6e5b84-e0f5-4579-9758-3 26 |
| SRC_SHA256 | who | 1 | 0 | dc0cb5fdd4178d0ce29f61820 26 |
