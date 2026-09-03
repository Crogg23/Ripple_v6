# PORTAL_SOC_UTAH_OPEN_DATA_P_294FE280EF

rows 604  columns 13  scan 3.1s

roles: audit 2, category 6, date 1, other 2, who 3

## when

INGESTED_AT
  2026       604  ##############################

## who

NAME by rows
         3  WALGREENS
         2  WASATCH HOUSE CLEANING, LLC
         2  DAVIS COUNTY SCHOOL DISTRICT
         2  KAYSVILLE CITY
         1  LAW OFFICES OF JASON F BARNES
         1  RESTORE MEDICAL, LLC
         1  OAKCOINS INC
         1  SCOTT HIRSCHI INSURANCE AGENCY
         1  BUILD TECH INC
         1  RON DAVENPORT PC
         1  ROBERT D MILLER INSURANCE INC
         1  THE PAW SPA
         1  KAYSVILLE CITY RECREATION
         1  CENTERLINE DEVELOPMENT LLC
         1  US POSTAL SERVICE
         1  WINGERS KAYSVILLE
         1  BIKERS EDGE
         1  CRESCENDO BIOSCIENCE INC
         1  DREW STORM PRODUCTIONS, INC.
         1  IN THE LOOP INC

NAICS by rows
        20  611110
        16  524210
        16  621210
        16  531210
        15  722513
        13  541611
        13  236115
        12  238221
        12  541511
        11  454390
         9  624120
         9  236118
         8  541110
         8  812112
         8  541219
         8  541618
         8  541211
         8  561730
         7  236220
         6  454111

SRC_SHA256 by rows
       604  a9e5f09d25fcf89afa981665c91d2708d175693e5fe74166e3ad23c8238073b0

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  BIKERS EDGE                               2026:1
  BUILD TECH INC                            2026:1
  CENTERLINE DEVELOPMENT LLC                2026:1
  CRESCENDO BIOSCIENCE INC                  2026:1
  DAVIS COUNTY SCHOOL DISTRICT              2026:2
  DREW STORM PRODUCTIONS, INC.              2026:1
  IN THE LOOP INC                           2026:1
  KAYSVILLE CITY                            2026:2
  KAYSVILLE CITY RECREATION                 2026:1
  LAW OFFICES OF JASON F BARNES             2026:1
  OAKCOINS INC                              2026:1
  RESTORE MEDICAL, LLC                      2026:1
  ROBERT D MILLER INSURANCE INC             2026:1
  RON DAVENPORT PC                          2026:1
  SCOTT HIRSCHI INSURANCE AGENCY            2026:1
  THE PAW SPA                               2026:1
  US POSTAL SERVICE                         2026:1
  WALGREENS                                 2026:3
  WASATCH HOUSE CLEANING, LLC               2026:2
  WINGERS KAYSVILLE                         2026:1

NAICS by INGESTED_AT  LOAD STAMP, not an event date
  236115                                    2026:13
  236118                                    2026:9
  236220                                    2026:7
  238221                                    2026:12
  454111                                    2026:6
  454390                                    2026:11
  524210                                    2026:16
  531210                                    2026:16
  541110                                    2026:8
  541211                                    2026:8
  541219                                    2026:8
  541511                                    2026:12
  541611                                    2026:13
  541618                                    2026:8
  561730                                    2026:8
  611110                                    2026:20
  621210                                    2026:16
  624120                                    2026:9
  722513                                    2026:15
  812112                                    2026:8

## what

COUNTYCODE: 11 99%, 57 1%, 29 0%

COUNTYNAME: Davis 99%, Weber 1%, Morgan 0%

EMPRANGE:  1-4 48%,  5-9 15%, 0 12%,  10-19 11%,  20-49 8%,  50-99 4%,  100-249 1%,  250-499 0%

EMPRANGECODE: B 48%, C 15%, A 12%, D 11%, E 8%, F 4%, G 1%, H 0%

OWNERSHIP: Private 95%, Local 5%, State 0%, Federal 0%

LOCATION_2: nan 95%, {"human_address": "{\"address\ 1%, {"human_address": "{\"address\ 1%, {"human_address": "{\"address\ 1%, {"human_address": "{\"address\ 1%, {"human_address": "{\"address\ 0%, {"human_address": "{\"address\ 0%, {"human_address": "{\"address\ 0%, {"human_address": "{\"address\ 0%, {"human_address": "{\"address\ 0%, {"latitude": "41.044148", "lon 0%, {"human_address": "{\"address\ 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 585 | 0 | BICIN SALES INC 4; ADVENT SYSTEMS INC 4; 1800 VENDING INC 4; DAVIS COUNTY SCHOOL DISTR 4 |
| COUNTYCODE | category | 3 | 0 | 11 599; 57 4; 29 1 |
| COUNTYNAME | category | 3 | 0 | Davis 599; Weber 4; Morgan 1 |
| PHONE | other | 503 | 0 | nan 53; (801) 444-3710 12; (801) 732-1090 9; (801) 359-4699 5 |
| EMPRANGE | category | 8 | 0 |  1-4 292;  5-9 92; 0 71;  10-19 69 |
| EMPRANGECODE | category | 8 | 0 | B 292; C 92; A 71; D 69 |
| NAICS | who | 227 | 0 | 611110 20; 621210 16; 524210 16; 531210 16 |
| OWNERSHIP | category | 4 | 0 | Private 572; Local 30; State 1; Federal 1 |
| LOCATION_1 | other | 564 | 0 | {"human_address": "{\"add 6; {"latitude": "41.02629",  4; {"latitude": "41.008679", 4; {"latitude": "41.040388", 4 |
| LOCATION_2 | category | 37 | 0 | nan 551; {"human_address": "{\"add 7; {"human_address": "{\"add 4; {"human_address": "{\"add 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:52:03.43749 604 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7c4f2873-1b93-4d58-b80b-0 604 |
| SRC_SHA256 | who | 1 | 0 | a9e5f09d25fcf89afa981665c 604 |
