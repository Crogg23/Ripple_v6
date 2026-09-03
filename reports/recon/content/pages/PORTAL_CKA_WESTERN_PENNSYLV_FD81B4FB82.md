# PORTAL_CKA_WESTERN_PENNSYLV_FD81B4FB82

rows 1.2K  columns 19  scan 3.8s

roles: amount 2, audit 2, category 7, date 3, id 1, other 2, who 3

## when

ASSIGNMENT_DATE
  2017       357  #################
  2018       648  ##############################
  2019       151  #######
  2020        25  #
  2021         9  
  2022         4  

LAST_UPDATED_DATE
  2021         3  
  2022      1.2K  ##############################

INGESTED_AT
  2026      1.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 1.2K | -80.08 | -79.97 | -79.89 | -79.88 | -95.5K |
| Y | 1.2K | 40.36 | 40.45 | 40.49 | 40.49 | 48.3K |

## who

NEIGHBORHOOD by rows
        76  Shadyside
        68  East Liberty
        63  Squirrel Hill South
        58  Bloomfield
        53  North Shore
        51  South Side Flats
        42  Strip District
        38  Carrick
        34  Central Oakland
        29  Lower Lawrenceville
        29  Middle Hill
        29  Central Lawrenceville
        28  Bluff
        28  Homewood South
        26  East Allegheny
        25  Mount Washington
        24  Brighton Heights
        22  Squirrel Hill North
        21  Crawford-Roberts
        20  Larimer

NEIGHBORHOOD by dollars
      -79.91        1 rows  Swisshelm Park
      -79.98        1 rows  Mt. Oliver
      -79.98        1 rows  St. Clair
      -79.98        1 rows  Bedford Dwellings
      -80.01        1 rows  Northview Heights
      -80.02        1 rows  South Shore
      -80.07        1 rows  East Carnegie
      -80.07        1 rows  Oakwood
      -80.08        1 rows  Windgap
     -159.76        2 rows  East Hills
     -159.79        2 rows  Point Breeze North
     -159.81        2 rows  Homewood West
     -159.87        2 rows  Stanton Heights
     -160.08        2 rows  Banksville
     -239.91        3 rows  Arlington
     -239.97        3 rows  Spring Garden
        -240        3 rows  Beltzhoover
     -240.01        3 rows  Fineview
     -240.06        3 rows  Duquesne Heights
     -319.58        4 rows  Homewood North

STATE by rows
      1.2K  Pennsylvania

STATE by dollars
      -95.5K     1.2K rows  Pennsylvania

SRC_SHA256 by rows
      1.2K  005f935433604b3ee25ef44d2173989ebb13f11eb7edf6d4e833f586958eb7b7

SRC_SHA256 by dollars
      -95.5K     1.2K rows  005f935433604b3ee25ef44d2173989ebb13f11eb7edf6d4e833f586958e

## who x when

NEIGHBORHOOD by ASSIGNMENT_DATE, dollars = X
  Bedford Dwellings                         2018:-79.98
  Bloomfield                                2017:-559.58 2018:-3.8K 2019:-239.84
  Bluff                                     2017:-799.89 2018:-1.4K
  Brighton Heights                          2017:-1.6K 2018:-320.15
  Carrick                                   2017:-1.6K 2018:-1.3K 2019:-159.97
  Central Lawrenceville                     2018:-879.49 2019:-1.4K
  Central Oakland                           2017:-399.76 2018:-2.0K 2020:-319.84
  Crawford-Roberts                          2017:-79.98 2018:-1.4K 2020:-159.96
  East Allegheny                            2017:-2.0K 2018:-80
  East Carnegie                             2017:-80.07
  East Hills                                2018:-159.76
  East Liberty                              2017:-559.45 2018:-3.7K 2019:-559.44 2020:-639.36
  Homewood South                            2018:-1.6K 2019:-639.20
  Larimer                                   2017:-79.92 2018:-1.1K 2021:-399.56
  Lower Lawrenceville                       2018:-799.63 2019:-1.4K 2020:-159.93
  Middle Hill                               2018:-2.3K
  Mount Washington                          2017:-960.12 2018:-1.0K
  Mt. Oliver                                2017:-79.98
  North Shore                               2018:-4.2K 2022:-80.02
  Northview Heights                         2017:-80.01
  Oakwood                                   2018:-80.07
  Shadyside                                 2017:-1.6K 2018:-1.4K 2019:-2.7K 2020:-319.68
  South Shore                               2017:-80.02
  South Side Flats                          2017:-2.5K 2018:-1.6K
  Squirrel Hill North                       2018:-1.4K 2019:-79.93 2020:-239.79
  Squirrel Hill South                       2018:-3.6K 2019:-1.4K
  St. Clair                                 2018:-79.98
  Strip District                            2018:-3.3K 2022:-79.98
  Swisshelm Park                            2019:-79.91
  Windgap                                   2017:-80.08

STATE by ASSIGNMENT_DATE, dollars = X
  Pennsylvania                              2017:-28.6K 2018:-51.8K 2019:-12.1K 2020:-2.0K 2021:-719.20 2022:-320.01

## what

RECEPTACLE_MODEL_ID: 74 100%, 105 0%

GROUP_NAME: 2nd Division 32%, 1st Division 23%, 3rd Division 22%, 4th Division 12%, 5th Division 8%, Frick Park 3%, Eastern Parks Division 1%, Northeastern Parks Division 0%, Schenley Parks Division 0%, Western Parks Division 0%

CITY: Pittsburgh 100%, Carnegie 0%

ZIP: 15212 17%, 15206 15%, 15219 11%, 15217 10%, 15201 7%, 15213 7%, 15224 6%, 15210 6%, 15232 6%, 15203 6%, 15208 4%, 15222 4%

DPW_DIVISION: 3 33%, 2 32%, 1 14%, 5 11%, 6 10%

COUNCIL_DISTRICT: 7 18%, 1 16%, 9 13%, 6 12%, 5 11%, 3 10%, 8 8%, 2 7%, 4 5%

WARD: 14 15%, 22 11%, 7 10%, 8 10%, 11 9%, 4 8%, 19 7%, 6 7%, 5 6%, 20 6%, 9 6%, 17 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CONTAINER_ID | id | 1.2K | 0 | 1339 6; 1338 6; 1337 6; 1336 6 |
| RECEPTACLE_MODEL_ID | category | 2 | 0 | 74 1.2K; 105 4 |
| ASSIGNMENT_DATE | date | 112 | 0 | 2019-03-19T08:03:00 24; 2017-09-19T12:22:47 24; 2017-09-21T16:27:32 23; 2019-03-19T08:02:59 22 |
| LAST_UPDATED_DATE | date | 1.1K | 0 | 2022-12-31T01:44:20 8; 2022-12-31T01:51:20 8; 2022-12-31T01:55:20 8; 2022-12-31T01:58:19 7 |
| GROUP_NAME | category | 10 | 0 | 2nd Division 377; 1st Division 270; 3rd Division 261; 4th Division 141 |
| ADDRESS | other | 1.1K | 0 | 1796 Mcbride Street 9; 175 Granville Street 7; 3701 Forbes Ave 7; 803 Ernie Street 7 |
| CITY | category | 2 | 0 | Pittsburgh 1.2K; Carnegie 1 |
| STATE | who | 1 | 0 | Pennsylvania 1.2K |
| ZIP | category | 26 | 0 | 15212 166; 15206 149; 15219 112; 15217 99 |
| NEIGHBORHOOD | who | 81 | 1 | Shadyside 76; East Liberty 68; Squirrel Hill South 63; Bloomfield 58 |
| DPW_DIVISION | category | 6 | 1 | 3 399; 2 379; 1 164; 5 128 |
| COUNCIL_DISTRICT | category | 10 | 1 | 7 213; 1 189; 9 156; 6 142 |
| WARD | category | 32 | 1 | 14 108; 22 82; 7 76; 8 71 |
| FIRE_ZONE | other | 85 | 0 | 3-6 58; 1-7 56; 2-1 54; 4-24 49 |
| X | amount | 1.2K | 0 | -79.91914 7; -79.91296 6; -79.91043 6; -79.9104156 6 |
| Y | amount | 1.2K | 0 | 40.43013 7; 40.46379 6; 40.46688 6; 40.46166949 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:51:17.19929 1.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 83af74a5-e880-47e7-8ac4-6 1.2K |
| SRC_SHA256 | who | 1 | 0 | 005f935433604b3ee25ef44d2 1.2K |
