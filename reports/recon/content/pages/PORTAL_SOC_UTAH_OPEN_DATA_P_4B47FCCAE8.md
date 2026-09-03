# PORTAL_SOC_UTAH_OPEN_DATA_P_4B47FCCAE8

rows 5.0K  columns 12  scan 3.6s

roles: audit 2, category 6, date 1, other 1, who 3

## when

INGESTED_AT
  2026      5.0K  ##############################

## who

NAME by rows
        20  DEPT OF DEFENSE
        19  FOREST SERVICE
         9  JACOBSEN CONSTRUCTION CO INC
         8  BUREAU OF THE CENSUS
         8  NATURAL RESOURCES CONSERVATION SERV
         7  FARM SERVICE AGENCY
         6  DUGWAY PROVING GROUND
         4  OFFICE OF PERSONNEL MGMT
         4  TOOELE ARMY DEPOT
         4  STATE FARM FIRE & CASUALTY CO
         4  BUREAU OF LAND MGMT
         3  FOOD SAFETY AND INSPECTION SERVICE
         3  ANIMAL AND PLANT HEALTH INSPECTION
         2  SMALL BUSINESS ADMINISTRATION
         2  DRIVE LINE, LLC
         2  MAK HOLDINGS, LLC
         2  DEZIGNER TRENDS LTD
         2  MADBROOK DONUT COMPANY
         2  ROCKY MOUNTAIN CHOCOLATE FACTORY
         2  MATANDO, INC.

NAICS by rows
       196  531210
       154  541611
       144  814110
       115  236115
       103  524210
       103  561730
        95  454390
        82  541110
        80  621210
        75  621111
        72  541613
        68  541511
        65  238221
        65  236118
        58  541618
        58  722511
        56  722513
        56  454111
        53  541219
        53  484121

SRC_SHA256 by rows
      5.0K  eb4a070671011dcd7aca46c21c6eba28b45a9e11fd80381b83f22b4279057cd5

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  ANIMAL AND PLANT HEALTH INSPECTION        2026:3
  BUREAU OF LAND MGMT                       2026:4
  BUREAU OF THE CENSUS                      2026:8
  DEPT OF DEFENSE                           2026:20
  DEZIGNER TRENDS LTD                       2026:2
  DRIVE LINE, LLC                           2026:2
  DUGWAY PROVING GROUND                     2026:6
  FARM SERVICE AGENCY                       2026:7
  FOOD SAFETY AND INSPECTION SERVICE        2026:3
  FOREST SERVICE                            2026:19
  JACOBSEN CONSTRUCTION CO INC              2026:9
  MADBROOK DONUT COMPANY                    2026:2
  MAK HOLDINGS, LLC                         2026:2
  MATANDO, INC.                             2026:2
  NATURAL RESOURCES CONSERVATION SERV       2026:8
  OFFICE OF PERSONNEL MGMT                  2026:4
  ROCKY MOUNTAIN CHOCOLATE FACTORY          2026:2
  SMALL BUSINESS ADMINISTRATION             2026:2
  STATE FARM FIRE & CASUALTY CO             2026:4
  TOOELE ARMY DEPOT                         2026:4

NAICS by INGESTED_AT  LOAD STAMP, not an event date
  236115                                    2026:115
  236118                                    2026:65
  238221                                    2026:65
  454111                                    2026:56
  454390                                    2026:95
  484121                                    2026:53
  524210                                    2026:103
  531210                                    2026:196
  541110                                    2026:82
  541219                                    2026:53
  541511                                    2026:68
  541611                                    2026:154
  541613                                    2026:72
  541618                                    2026:58
  561730                                    2026:103
  621111                                    2026:75
  621210                                    2026:80
  722511                                    2026:58
  722513                                    2026:56
  814110                                    2026:144

## what

COUNTYCODE: 49 38%, 11 18%, 57 11%, 53 11%, 43 5%, 5 5%, 21 3%, 47 2%, 45 2%, 51 2%, 13 2%, 3 1%

COUNTYNAME: Utah 38%, Davis 18%, Weber 11%, Washington 11%, Summit 5%, Cache 5%, Iron 3%, Uintah 2%, Tooele 2%, Wasatch 2%, Duchesne 2%, Box Elder 1%

EMPRANGE:  1-4 61%, 0 22%,  5-9 9%,  10-19 5%,  20-49 2%,  50-99 0%,  100-249 0%,  250-499 0%

EMPRANGECODE: B 61%, A 22%, C 9%, D 5%, E 2%, F 0%, G 0%, H 0%

OWNERSHIP: Private 98%, Federal 2%, Local 0%, State 0%

LOCATION_1: {"human_address": "{\"address\ 25%, {"human_address": "{\"address\ 25%, {"human_address": "{\"address\ 25%, {"human_address": "{\"address\ 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 4.9K | 0 | TOOELE ARMY DEPOT 28; FOREST SERVICE 27; STATE FARM FIRE & CASUALT 26; DEPT OF DEFENSE 26 |
| COUNTYCODE | category | 28 | 0 | 49 1.8K; 11 833; 57 519; 53 497 |
| COUNTYNAME | category | 28 | 0 | Utah 1.8K; Davis 833; Weber 519; Washington 497 |
| PHONE | other | 3.7K | 255 | (801) 225-8474 104; (801) 561-3473 50; (801) 852-2673 47; (801) 728-7070 46 |
| EMPRANGE | category | 8 | 0 |  1-4 3.0K; 0 1.1K;  5-9 466;  10-19 244 |
| EMPRANGECODE | category | 8 | 0 | B 3.0K; A 1.1K; C 466; D 244 |
| NAICS | who | 548 | 0 | 531210 196; 541611 154; 814110 144; 236115 115 |
| OWNERSHIP | category | 4 | 0 | Private 4.9K; Federal 97; Local 21; State 2 |
| LOCATION_1 | category | 5 | 5.0K | {"human_address": "{\"add 1; {"human_address": "{\"add 1; {"human_address": "{\"add 1; {"human_address": "{\"add 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:46:43.85159 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 662015c4-1bb9-4e36-9b5b-b 5.0K |
| SRC_SHA256 | who | 1 | 0 | eb4a070671011dcd7aca46c21 5.0K |
