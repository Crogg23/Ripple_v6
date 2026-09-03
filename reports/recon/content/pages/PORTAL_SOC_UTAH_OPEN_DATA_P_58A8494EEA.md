# PORTAL_SOC_UTAH_OPEN_DATA_P_58A8494EEA

rows 5.0K  columns 13  scan 2.9s

roles: audit 2, category 7, date 1, other 1, who 3

## when

INGESTED_AT
  2026      5.0K  ##############################

## who

NAME by rows
        19  DEPT OF DEFENSE
         9  JACOBSEN CONSTRUCTION CO INC
         9  DUGWAY PROVING GROUND
         7  BUREAU OF THE CENSUS
         7  FARM SERVICE AGENCY
         6  NATURAL RESOURCES CONSERVATION SERV
         4  STATE FARM FIRE & CASUALTY CO
         4  BUREAU OF LAND MGMT
         4  OFFICE OF PERSONNEL MGMT
         2  MOUNTAIN PRIME HOMES
         2  BRIGHAM CITY OUTDOORS
         2  JGB LAW LLC
         2  BEEHIVE BROADBAND, LLC
         2  FOREST SERVICE
         2  FOOD SAFETY AND INSPECTION SERVICE
         2  COYOTE CHARRO II, INC.
         2  DAVIS PARK CAFE , LLC
         2  SECURE CAPITAL NETWORK, LLC
         2  CLEAR ADVANTAGE CONSULTING, LLC
         2  ROCKY MOUNTAIN CHOCOLATE FACTORY

NAICS by rows
       198  531210
       155  541611
       129  814110
       129  236115
       112  561730
       110  524210
        92  454390
        89  541110
        80  541613
        79  621111
        76  621210
        71  238221
        68  236118
        67  541511
        63  541618
        60  722511
        55  531390
        54  541219
        52  454111
        49  541690

SRC_SHA256 by rows
      5.0K  3b72c0474f53b4aee055691b5a663e213da59907d09b891fdaf19efaacd598cb

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  BEEHIVE BROADBAND, LLC                    2026:2
  BRIGHAM CITY OUTDOORS                     2026:2
  BUREAU OF LAND MGMT                       2026:4
  BUREAU OF THE CENSUS                      2026:7
  CLEAR ADVANTAGE CONSULTING, LLC           2026:2
  COYOTE CHARRO II, INC.                    2026:2
  DAVIS PARK CAFE , LLC                     2026:2
  DEPT OF DEFENSE                           2026:19
  DUGWAY PROVING GROUND                     2026:9
  FARM SERVICE AGENCY                       2026:7
  FOOD SAFETY AND INSPECTION SERVICE        2026:2
  FOREST SERVICE                            2026:2
  JACOBSEN CONSTRUCTION CO INC              2026:9
  JGB LAW LLC                               2026:2
  MOUNTAIN PRIME HOMES                      2026:2
  NATURAL RESOURCES CONSERVATION SERV       2026:6
  OFFICE OF PERSONNEL MGMT                  2026:4
  ROCKY MOUNTAIN CHOCOLATE FACTORY          2026:2
  SECURE CAPITAL NETWORK, LLC               2026:2
  STATE FARM FIRE & CASUALTY CO             2026:4

NAICS by INGESTED_AT  LOAD STAMP, not an event date
  236115                                    2026:129
  236118                                    2026:68
  238221                                    2026:71
  454111                                    2026:52
  454390                                    2026:92
  524210                                    2026:110
  531210                                    2026:198
  531390                                    2026:55
  541110                                    2026:89
  541219                                    2026:54
  541511                                    2026:67
  541611                                    2026:155
  541613                                    2026:80
  541618                                    2026:63
  541690                                    2026:49
  561730                                    2026:112
  621111                                    2026:79
  621210                                    2026:76
  722511                                    2026:60
  814110                                    2026:129

## what

COUNTYCODE: 49 38%, 11 17%, 53 11%, 57 11%, 5 5%, 43 5%, 21 3%, 47 2%, 45 2%, 51 2%, 13 2%, 3 2%

COUNTYNAME: Utah 38%, Davis 17%, Washington 11%, Weber 11%, Cache 5%, Summit 5%, Iron 3%, Uintah 2%, Tooele 2%, Wasatch 2%, Duchesne 2%, Box Elder 2%

EMPRANGE:  1-4 64%, 0 21%,  5-9 8%,  10-19 4%,  20-49 2%,  50-99 0%,  100-249 0%,  250-499 0%

EMPRANGECODE: B 64%, A 21%, C 8%, D 4%, E 2%, F 0%, G 0%, H 0%

OWNERSHIP: Private 98%, Federal 1%, Local 0%, State 0%

LOCATION_1: {"human_address": "{\"address\ 50%, {"human_address": "{\"address\ 50%

LOCATION_2: {"human_address": "{\"address\ 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 4.9K | 0 | STATE FARM FIRE & CASUALT 27; TAYLOR TIMES THREE LAWN C 25; TAYLOR MADE TILE, INC. 25; TAYLOR COMMERCIAL REAL ES 25 |
| COUNTYCODE | category | 28 | 0 | 49 1.8K; 11 816; 53 537; 57 515 |
| COUNTYNAME | category | 28 | 0 | Utah 1.8K; Davis 816; Washington 537; Weber 515 |
| PHONE | other | 3.7K | 227 | (801) 225-8474 95; (801) 852-2673 45; (801) 728-7070 42; (801) 621-0440 41 |
| EMPRANGE | category | 8 | 0 |  1-4 3.2K; 0 1.0K;  5-9 420;  10-19 223 |
| EMPRANGECODE | category | 8 | 0 | B 3.2K; A 1.0K; C 420; D 223 |
| NAICS | who | 534 | 0 | 531210 198; 541611 155; 236115 129; 814110 129 |
| OWNERSHIP | category | 4 | 0 | Private 4.9K; Federal 66; Local 21; State 1 |
| LOCATION_1 | category | 3 | 5.0K | {"human_address": "{\"add 1; {"human_address": "{\"add 1 |
| LOCATION_2 | category | 2 | 5.0K | {"human_address": "{\"add 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:48:03.82615 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 734996af-bfa2-483e-a1a3-a 5.0K |
| SRC_SHA256 | who | 1 | 0 | 3b72c0474f53b4aee055691b5 5.0K |
