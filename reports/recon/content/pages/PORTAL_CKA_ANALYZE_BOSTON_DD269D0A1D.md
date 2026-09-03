# PORTAL_CKA_ANALYZE_BOSTON_DD269D0A1D

rows 10.0K  columns 39  scan 4.2s

roles: amount 3, audit 2, category 22, date 1, id 2, other 7, who 3

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FT_COST | 10.0K | -1 | 0.11 | 0.56 | 1.40 | 438.34 |
| TF_COST | 10.0K | -1 | 0.09 | 0.55 | 1.40 | -1.7K |
| SHAPE_LENGTH | 10.0K | 0 | 0 | 0 | 0.02 | 0.24 |

## who

ST_NAME by rows
       189  Washington
       140  Centre
        92  Dorchester
        64  Commonwealth
        64  River
        63  Harvard
        52  Beacon
        50  Adams
        47  Park
        45  Milton
        45  Gallivan
        41  Harrison
        40  Saratoga
        40  VFW
        40  Bennington
        40  Norfolk
        39  Warren
        39  Neponset
        38  Shawmut
        37  Dudley

ST_NAME by dollars
       12.93      189 rows  Washington
        6.41       47 rows  Park
        4.68       34 rows  Chestnut
        4.01       39 rows  Warren
        4.01       35 rows  Corey
        3.85       40 rows  Norfolk
        3.77       37 rows  Lagrange
        3.72       45 rows  Milton
        3.59       24 rows  West Roxbury
        3.38       29 rows  South
        3.32       21 rows  Third
        3.23       21 rows  Beech
        3.18       20 rows  Fourth
        3.06       38 rows  Shawmut
        3.05       14 rows  Temple
        2.94       20 rows  West
        2.93       15 rows  Sixth
        2.90       64 rows  River
        2.90       11 rows  William J Day
        2.80       21 rows  Cottage

ALTERNATE_NAME by rows
        32  RAMP
        12  ALLSTON TOLL PLAZA
         9  RAMP - RT 1A / RT 90 W TO AIRPORT ROAD
         8  RAMP - SOLDIERS FIELD ROAD WB 
         7  LEVERETT CONNECTOR
         7  RAMP - AIRPORT ROAD TO RT 90 E
         6  LEVERETT CIRCLE CONNECTOR
         5  RT 90 E HOV LANE
         5  RAMP - WESTERN AVENUE TO SOLDIERS FIELD ROAD
         5  RAMP - LEVERETT CONNECTOR TO NASHUA STREET
         5  CHARLESGATE OVERPASS
         4  RAMP - TO RT 93 N
         3  RAMP - BROADWAY TO RT 90 W
         3  RAMP - ALBANY STREET TO RT 90 W
         3  RAMP - RT 90 W TO RT 93 S
         3  RAMP - RT 90 W TO RT 93
         3  MAURICE TOBIN BRIDGE
         3  RAMP - RT 93 N TO RT 90 E
         2  RAMP - RT 93 S TO COLUMBIA ROAD
         2  RAMP - RT 93 N TO RT 90 W

ALTERNATE_NAME by dollars
        4.07       32 rows  RAMP
        1.41        2 rows  RAMP - RT 93 S TO MASSACHUSETTS AVENUE CONNECTOR
        1.38        9 rows  RAMP - RT 1A / RT 90 W TO AIRPORT ROAD
        1.21        3 rows  RAMP - RT 93 N TO RT 90 E
        1.14        8 rows  RAMP - SOLDIERS FIELD ROAD WB 
        1.01        1 rows  RAMP - ALBANY STREET TO RT 93 S
        0.69        3 rows  RAMP - ALBANY STREET TO RT 90 W
        0.68        5 rows  RAMP - WESTERN AVENUE TO SOLDIERS FIELD ROAD
        0.64        1 rows  RAMP - MASSACHUSETTS AVENUE CONNECTOR TO FRONTAGE RD
        0.62        2 rows  RAMP - RT 90 E TO HOTEL DRIVE
        0.61        1 rows  RAMP - RT 93 N TO COLUMBIA ROAD
        0.59        2 rows  RAMP - RT 90 E TO AIRPORT ROAD
        0.46        5 rows  RAMP - LEVERETT CONNECTOR TO NASHUA STREET
        0.44        1 rows  RAMP - SOUTH BOSTON HAUL ROAD TO RT 90 W
        0.43        1 rows  RAMP - NEPTUNE ROAD TO RT 1A S
        0.39        1 rows  RAMP - WILLIAM T MORRISSEY BOULEVARD
        0.38        2 rows  RAMP - RT 93 N TO RT 90 W
        0.34        1 rows  RAMP - AIRPORT ROAD TO HOTEL DRIVE
        0.34        1 rows  RAMP - MASSACHUSETTS AVENUE TO RT 90 W
        0.29        1 rows  RAMP - FREEPORT STREET TO RT 93 S

SRC_SHA256 by rows
     10.0K  ae8c629b22b778755f5ae3c8ed4194d7a77be7b1cf2720a0336107325d141dd9

SRC_SHA256 by dollars
      438.34    10.0K rows  ae8c629b22b778755f5ae3c8ed4194d7a77be7b1cf2720a0336107325d14

## who x when

ST_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = FT_COST
  Adams                                     2026:1.42
  Beacon                                    2026:-0.96
  Beech                                     2026:3.23
  Bennington                                2026:1.44
  Centre                                    2026:-5.94
  Chestnut                                  2026:4.68
  Commonwealth                              2026:-11.66
  Corey                                     2026:4.01
  Dorchester                                2026:-6.09
  Dudley                                    2026:-0.28
  Fourth                                    2026:3.18
  Gallivan                                  2026:2.56
  Harrison                                  2026:2.26
  Harvard                                   2026:2.50
  Lagrange                                  2026:3.77
  Milton                                    2026:3.72
  Neponset                                  2026:2.58
  Norfolk                                   2026:3.85
  Park                                      2026:6.41
  River                                     2026:2.90
  Saratoga                                  2026:-1.02
  Shawmut                                   2026:3.06
  South                                     2026:3.38
  Temple                                    2026:3.05
  Third                                     2026:3.32
  VFW                                       2026:0.50
  Warren                                    2026:4.01
  Washington                                2026:12.93
  West                                      2026:2.94
  West Roxbury                              2026:3.59

ALTERNATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = FT_COST
  ALLSTON TOLL PLAZA                        2026:-4.31
  CHARLESGATE OVERPASS                      2026:-3.83
  LEVERETT CIRCLE CONNECTOR                 2026:-3.82
  LEVERETT CONNECTOR                        2026:-3.70
  MAURICE TOBIN BRIDGE                      2026:0.22
  RAMP                                      2026:4.07
  RAMP - AIRPORT ROAD TO HOTEL DRIVE        2026:0.34
  RAMP - AIRPORT ROAD TO RT 90 E            2026:-0.18
  RAMP - ALBANY STREET TO RT 90 W           2026:0.69
  RAMP - ALBANY STREET TO RT 93 S           2026:1.01
  RAMP - BROADWAY TO RT 90 W                2026:-1.91
  RAMP - LEVERETT CONNECTOR TO NASHUA STRE  2026:0.46
  RAMP - MASSACHUSETTS AVENUE CONNECTOR TO  2026:0.64
  RAMP - NEPTUNE ROAD TO RT 1A S            2026:0.43
  RAMP - RT 1A / RT 90 W TO AIRPORT ROAD    2026:1.38
  RAMP - RT 90 E TO AIRPORT ROAD            2026:0.59
  RAMP - RT 90 E TO HOTEL DRIVE             2026:0.62
  RAMP - RT 90 W TO RT 93                   2026:-0.22
  RAMP - RT 90 W TO RT 93 S                 2026:-0.80
  RAMP - RT 93 N TO COLUMBIA ROAD           2026:0.61
  RAMP - RT 93 N TO RT 90 E                 2026:1.21
  RAMP - RT 93 N TO RT 90 W                 2026:0.38
  RAMP - RT 93 S TO COLUMBIA ROAD           2026:-0.94
  RAMP - RT 93 S TO MASSACHUSETTS AVENUE C  2026:1.41
  RAMP - SOLDIERS FIELD ROAD WB             2026:1.14
  RAMP - SOUTH BOSTON HAUL ROAD TO RT 90 W  2026:0.44
  RAMP - TO RT 93 N                         2026:-2.45
  RAMP - WESTERN AVENUE TO SOLDIERS FIELD   2026:0.68
  RAMP - WILLIAM T MORRISSEY BOULEVARD      2026:0.39
  RT 90 E HOV LANE                          2026:-3.98

## what

PRE_DIR: E 41%, W 36%, N 17%, S 6%

ST_TYPE: ST 66%, AVE 13%, RD 11%, PL 2%, TER 2%, WAY 1%, PKWY 1%, BLVD 1%, CT 1%, DR 1%, PARK 1%

SUF_DIR: S 31%, N 30%, W 23%, E 16%

CFCC: A41 65%, A31 25%, A35 3%, A60 2%, A63 2%, A73 1%, A70 1%, A15 1%, A21 0%, A25 0%, A62 0%, A40 0%

SPEEDLIMIT: 20 53%, 25 25%, 15 14%, 30 3%, 35 3%, 1 1%, 5 1%, 65 0%, 10 0%, 55 0%, 45 0%, 3 0%

ONEWAY: FT 97%, N 3%

F_ZLEV: 0 98%, 1 2%, -1 1%, 2 0%, -2 0%, 3 0%

T_ZLEV: 0 98%, 1 2%, -1 0%, 2 0%, 3 0%, -2 0%

FT_DIR: W 30%, N 25%, S 25%, E 20%

TF_DIR: S 41%, N 38%, W 12%, E 9%

SHIELD: S 68%, I 19%, U 14%

HWY_NUM: 203 19%, 93 14%, 20 14%, 28 11%, 145 10%, 3A 7%, 2 7%, 90 7%, 30 4%, 1A 4%, 9 3%

MUN_L: BOSTON 100%, BROOKLINE 0%, SOMERVILLE 0%, NEWTON 0%

MUN_R: BOSTON 100%, BROOKLINE 0%, MILTON 0%, SOMERVILLE 0%

NBHD_L: DORCHESTER 21%, BOSTON 12%, BRIGHTON 10%, WEST ROXBURY 10%, ROXBURY 9%, HYDE PARK 8%, SOUTH BOSTON 7%, JAMAICA PLAIN 6%, ROSLINDALE 6%, EAST BOSTON 6%, MATTAPAN 3%, CHARLESTOWN 3%

NBHD_R: DORCHESTER 21%, BOSTON 12%, BRIGHTON 10%, WEST ROXBURY 10%, ROXBURY 9%, HYDE PARK 8%, SOUTH BOSTON 7%, JAMAICA PLAIN 6%, ROSLINDALE 6%, EAST BOSTON 6%, MATTAPAN 3%, CHARLESTOWN 3%

COUNTY00_L: 25025 100%, 25021 0%, 25017 0%

COUNTY00_R: 25025 100%, 25021 0%, 25017 0%

MCD00_L: 7000 100%, 9175 0%, 45560 0%, 62535 0%

MCD00_R: 7000 100%, 9175 0%, 16495 0%, 41690 0%, 62535 0%

ZIP_L: 02118 87%, 02124 13%

ZIP_R: 02118 87%, 02126 13%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SEGMENT_ID | id | 10.2K | 0 | 15196 50; 8316 50; 8315 50; 8314 50 |
| L_F_ADD | other | 819 | 1.5K | 2 2.0K; 1 196; 100 99; 32 95 |
| L_T_ADD | other | 816 | 1.5K | 98 607; 1 410; 198 231; 2 204 |
| R_F_ADD | other | 973 | 1.2K | 1 2.0K; 2 194; 101 115; 21 105 |
| R_T_ADD | other | 958 | 1.2K | 99 625; 2 428; 199 238; 1 189 |
| STREET_ID | other | 3.3K | 0 | -1 216; 767 121; 4354 107; 4357 86 |
| PRE_DIR | category | 5 | 9.7K | E 131; W 114; N 56; S 20 |
| ST_NAME | who | 2.7K | 178 | Washington 216; Centre 143; Dorchester 98; River 86 |
| ST_TYPE | category | 29 | 349 | ST 6.3K; AVE 1.3K; RD 1.0K; PL 191 |
| SUF_DIR | category | 5 | 9.9K | S 19; N 18; W 14; E 10 |
| ALTERNATE_NAME | who | 51 | 9.8K | RAMP 32; ALLSTON TOLL PLAZA 12; RAMP - RT 1A / RT 90 W TO 9; RAMP - SOLDIERS FIELD ROA 8 |
| CFCC | category | 20 | 36 | A41 6.4K; A31 2.4K; A35 339; A60 168 |
| SPEEDLIMIT | category | 14 | 0 | 20 5.3K; 25 2.5K; 15 1.4K; 30 282 |
| ONEWAY | category | 3 | 6.2K | FT 3.7K; N 104 |
| F_ZLEV | category | 6 | 0 | 0 9.8K; 1 173; -1 54; 2 9 |
| T_ZLEV | category | 6 | 0 | 0 9.8K; 1 175; -1 50; 2 8 |
| FT_COST | amount | 2.9K | 29 | -1.0 942; 0.0 65; 0.116 55; 0.017 52 |
| TF_COST | amount | 1.7K | 29 | -1.0 2.8K; 0.0 65; 0.116 48; 0.011 45 |
| FT_DIR | category | 5 | 10.0K | W 6; N 5; S 5; E 4 |
| TF_DIR | category | 5 | 10.0K | S 14; N 13; W 4; E 3 |
| SHIELD | category | 4 | 9.7K | S 185; I 52; U 37 |
| HWY_NUM | category | 18 | 9.7K | 203 48; 93 35; 20 35; 28 28 |
| MUN_L | category | 4 | 0 | BOSTON 10.0K; BROOKLINE 2; SOMERVILLE 2; NEWTON 1 |
| MUN_R | category | 4 | 0 | BOSTON 10.0K; BROOKLINE 6; MILTON 1; SOMERVILLE 1 |
| NBHD_L | category | 12 | 0 | DORCHESTER 2.1K; BOSTON 1.2K; BRIGHTON 1.0K; WEST ROXBURY 957 |
| NBHD_R | category | 13 | 0 | DORCHESTER 2.1K; BOSTON 1.2K; BRIGHTON 1.0K; WEST ROXBURY 970 |
| STATE00_L | other | 1 | 0 | MA 10.0K |
| STATE00_R | other | 1 | 0 | MA 10.0K |
| COUNTY00_L | category | 3 | 0 | 25025 10.0K; 25021 2; 25017 2 |
| COUNTY00_R | category | 3 | 0 | 25025 10.0K; 25021 8; 25017 2 |
| MCD00_L | category | 4 | 0 | 7000 10.0K; 9175 1; 45560 1; 62535 1 |
| MCD00_R | category | 5 | 0 | 7000 10.0K; 9175 6; 16495 1; 41690 1 |
| ZIP_L | category | 3 | 10.0K | 02118 13; 02124 2 |
| ZIP_R | category | 3 | 10.0K | 02118 13; 02126 2 |
| SHAPE_LENGTH | amount | 9.7K | 0 | 0.000484251482397 50; 0.000252798790258 50; 0.000491935559289 50; 0.000383686127289 50 |
| SHAPE_WKT | id | 9.6K | 291 | MULTILINESTRING ((-71.051 49; MULTILINESTRING ((-71.052 49; MULTILINESTRING ((-71.053 49; MULTILINESTRING ((-71.053 49 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:35:07.67097 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5ab8d056-c5af-4ad1-a3d0-5 10.0K |
| SRC_SHA256 | who | 1 | 0 | ae8c629b22b778755f5ae3c8e 10.0K |
