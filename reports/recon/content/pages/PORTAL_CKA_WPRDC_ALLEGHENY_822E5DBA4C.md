# PORTAL_CKA_WPRDC_ALLEGHENY_822E5DBA4C

rows 1.0K  columns 24  scan 8.9s

roles: amount 3, audit 2, category 10, date 2, id 1, other 3, who 4

## when

START_DATE
  2017       269  ############################
  2018       290  ##############################
  2019       251  ##########################
  2020       192  ####################

INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| BUDGETED_AMOUNT | 998 | 1.0K | 115.0K | 4.00M | 15.07M | 426.42M |
| LATITUDE | 500 | 40.37 | 40.44 | 40.48 | 40.49 | 20.2K |
| LONGITUDE | 500 | -80.08 | -79.98 | -79.89 | -79.87 | -40.0K |

## who

NAME by rows
       110  CITY COUNCIL'S UNSPECIFIED LOCAL OPTION
        82  CAPITAL EQUIPMENT ACQUISITION
        67  PARK RECONSTRUCTION
        56  SPORT FACILITY IMPROVEMENTS
        56  COMPLETE STREETS
        50  PLAY AREA IMPROVEMENTS
        38  FACILITY IMPROVEMENTS - PUBLIC SAFETY FACILITIES
        23  FACILITY IMPROVEMENTS - RECREATION AND SENIOR CENTERS
        18  STREET RESURFACING
        17  FACILITY IMPROVEMENTS - CITY FACILITIES
        17  ECONOMIC DEVELOPMENT AND HOUSING
        17  SLOPE FAILURE REMEDIATION
        16  FACILITY IMPROVEMENTS - SPORT FACILITIES
        16  PARK RECONSTRUCTION - REGIONAL ASSET DISTRICT PARKS
        15  ADA COMPLIANCE
        15  STEP REPAIR AND REPLACEMENT
        15  FACILITY IMPROVEMENTS
        13  RAMP AND PUBLIC SIDEWALK
        13  STREETSCAPE AND INTERSECTION RECONSTRUCTION
        13  COMMUNITY-BASED ORGANIZATIONS

NAME by dollars
      65.15M       18 rows  STREET RESURFACING
      24.40M       82 rows  CAPITAL EQUIPMENT ACQUISITION
      24.39M       56 rows  COMPLETE STREETS
      18.30M       67 rows  PARK RECONSTRUCTION
      17.37M        4 rows  ADVANCED TRANSPORTATION AND CONGESTION MANAGEMENT TECHNOLOGI
      15.13M       38 rows  FACILITY IMPROVEMENTS - PUBLIC SAFETY FACILITIES
      14.63M        3 rows  SMALLMAN STREET RECONSTRUCTION
      14.50M        4 rows  FOUR MILE RUN
      14.00M        1 rows  LED STREETLIGHT UPGRADE
      11.70M       17 rows  SLOPE FAILURE REMEDIATION
      11.69M       17 rows  FACILITY IMPROVEMENTS - CITY FACILITIES
      10.96M       17 rows  ECONOMIC DEVELOPMENT AND HOUSING
      10.08M       23 rows  FACILITY IMPROVEMENTS - RECREATION AND SENIOR CENTERS
       8.35M       13 rows  STREETSCAPE AND INTERSECTION RECONSTRUCTION
       8.12M        5 rows  REMEDIATION OF CONDEMNED BUILDINGS
       6.81M        7 rows  WEST OHIO STREET BRIDGE (TIP)
       6.47M       10 rows  FLOOD CONTROL PROJECTS
       5.97M        7 rows  URBAN REDEVELOPMENT AUTHORITY PERSONNEL
       5.71M       16 rows  PARK RECONSTRUCTION - REGIONAL ASSET DISTRICT PARKS
       5.27M       10 rows  BRIDGE UPGRADES

TRACT by rows
        24  42003170200
        23  42003562600
        22  42003562700
        17  42003020100
        14  42003160800
        13  42003240600
        13  42003562400
        12  42003040900
         9  42003151700
         9  42003060300
         9  42003020300
         9  42003080400
         9  42003290400
         8  42003060500
         8  42003250300
         8  42003281500
         7  42003191400
         7  42003191700
         7  42003250900
         7  42003262000

TRACT by dollars
      11.30M        4 rows  42003151600
       8.91M       24 rows  42003170200
       8.78M       22 rows  42003562700
       8.21M       17 rows  42003020100
       7.23M       23 rows  42003562600
       5.61M        6 rows  42003140300
       5.26M        9 rows  42003020300
       4.44M        5 rows  42003141400
       4.40M        4 rows  42003130300
       4.11M       14 rows  42003160800
       4.07M        5 rows  42003980100
       3.65M        7 rows  42003262000
       3.48M       12 rows  42003040900
       2.97M        4 rows  42003202300
       2.90M        2 rows  42003300100
       2.54M       13 rows  42003562400
       2.39M        4 rows  42003981800
       2.26M        6 rows  42003980400
       2.16M       13 rows  42003240600
       2.14M        8 rows  42003250300

NEIGHBORHOOD by rows
        28  South Side Flats
        20  South Side Slopes
        19  Elliott
        17  Central Business District
        17  Brookline
        16  Bloomfield
        15  Allegheny Center
        14  Shadyside
        14  Carrick
        13  Squirrel Hill South
        13  Troy Hill
        13  Strip District
        13  Greenfield
        12  Highland Park
        12  Beltzhoover
        11  Squirrel Hill North
        11  Beechview
        10  Brighton Heights
        10  Mount Washington
         9  Hazelwood

NEIGHBORHOOD by dollars
      13.05M       13 rows  Greenfield
       9.05M       28 rows  South Side Flats
       8.21M       17 rows  Central Business District
       6.81M        7 rows  Allegheny West
       6.68M       19 rows  Elliott
       6.49M       11 rows  Squirrel Hill North
       6.26M       13 rows  Strip District
       6.04M       12 rows  Highland Park
       5.83M       20 rows  South Side Slopes
       4.44M        6 rows  Homewood South
       4.10M        4 rows  Swisshelm Park
       3.65M        7 rows  Spring Hill-City View
       3.15M        9 rows  Lincoln-Lemington-Belmar
       2.97M        4 rows  Banksville
       2.94M       11 rows  Beechview
       2.90M        2 rows  Knoxville
       2.72M        8 rows  Central Oakland
       2.51M       12 rows  Beltzhoover
       2.43M       14 rows  Carrick
       2.34M        9 rows  Central Northside

SRC_SHA256 by rows
      1.0K  5724380d35778bab7e10f8d604afef31ef8f11e8c263766277da6cb7f5f22d6b

SRC_SHA256 by dollars
     426.42M     1.0K rows  5724380d35778bab7e10f8d604afef31ef8f11e8c263766277da6cb7f5f2

## who x when

NAME by START_DATE, dollars = BUDGETED_AMOUNT
  ADA COMPLIANCE                            2017:33.0K 2018:40.0K 2019:40.0K 2020:50.0K
  ADVANCED TRANSPORTATION AND CONGESTION M  2018:2.57M 2019:11.31M 2020:3.49M
  BRIDGE UPGRADES                           2019:875.0K 2020:4.40M
  CAPITAL EQUIPMENT ACQUISITION             2017:5.00M 2018:8.79M 2019:5.00M 2020:5.61M
  CITY COUNCIL'S UNSPECIFIED LOCAL OPTION   2017:805.5K 2018:754.5K 2019:850.0K 2020:760.0K
  COMMUNITY-BASED ORGANIZATIONS             2017:600.0K 2018:650.0K 2019:700.0K 2020:500.0K
  COMPLETE STREETS                          2018:1.05M 2019:5.62M 2020:17.72M
  ECONOMIC DEVELOPMENT AND HOUSING          2017:3.20M 2018:4.23M 2019:3.53M
  FACILITY IMPROVEMENTS                     2017:3.11M 2018:475.0K 2019:390.0K
  FACILITY IMPROVEMENTS - CITY FACILITIES   2018:3.04M 2019:3.52M 2020:5.13M
  FACILITY IMPROVEMENTS - PUBLIC SAFETY FA  2018:2.45M 2019:5.39M 2020:7.30M
  FACILITY IMPROVEMENTS - RECREATION AND S  2018:974.2K 2019:4.86M 2020:4.24M
  FACILITY IMPROVEMENTS - SPORT FACILITIES  2018:864.3K 2019:798.5K 2020:610.0K
  FLOOD CONTROL PROJECTS                    2018:2.85M 2019:3.55M 2020:70.0K
  FOUR MILE RUN                             2018:4.00M 2019:10.50M
  LED STREETLIGHT UPGRADE                   2019:14.00M
  PARK RECONSTRUCTION                       2017:540.8K 2018:5.39M 2019:3.72M 2020:8.66M
  PARK RECONSTRUCTION - REGIONAL ASSET DIS  2017:465.0K 2018:1.21M 2019:1.74M 2020:2.30M
  PLAY AREA IMPROVEMENTS                    2017:455.9K 2018:1.32M 2019:1.49M 2020:430.0K
  RAMP AND PUBLIC SIDEWALK                  2017:200.0K 2018:550.0K 2019:700.0K 2020:600.0K
  REMEDIATION OF CONDEMNED BUILDINGS        2018:1.70M 2019:2.62M 2020:3.80M
  SLOPE FAILURE REMEDIATION                 2017:550.0K 2018:2.25M 2019:6.80M 2020:2.10M
  SMALLMAN STREET RECONSTRUCTION            2018:11.90M 2019:2.73M
  SPORT FACILITY IMPROVEMENTS               2017:1.01M 2018:546.8K 2019:223.5K
  STEP REPAIR AND REPLACEMENT               2017:385.0K 2018:635.0K 2019:735.0K 2020:590.0K
  STREET RESURFACING                        2017:14.88M 2018:16.02M 2019:18.57M 2020:15.68M
  STREETSCAPE AND INTERSECTION RECONSTRUCT  2017:395.0K 2018:7.96M
  URBAN REDEVELOPMENT AUTHORITY PERSONNEL   2017:2.16M 2018:2.16M 2019:1.15M 2020:500.0K
  WEST OHIO STREET BRIDGE (TIP)             2017:2.61M 2018:394.2K 2019:256.0K 2020:3.55M

TRACT by START_DATE, dollars = BUDGETED_AMOUNT
  42003020100                               2017:1.25M 2018:5.73M 2019:1.22M
  42003020300                               2017:2.5K 2019:3.65M 2020:1.60M
  42003040900                               2017:806.0K 2018:2.06M 2019:125.6K 2020:480.0K
  42003060300                               2017:489.0K 2019:205.2K 2020:150.0K
  42003060500                               2017:55.0K 2018:5.0K 2019:850.0K 2020:440.0K
  42003080400                               2017:12.5K 2018:399.7K 2019:155.0K
  42003130300                               2019:1.40M 2020:3.00M
  42003140300                               2017:2.5K 2018:4.07M 2019:140.0K 2020:1.39M
  42003141400                               2018:4.10M 2019:345.0K
  42003151600                               2018:800.0K 2019:10.50M
  42003151700                               2017:885.0K 2018:605.2K 2019:257.5K
  42003160800                               2017:208.2K 2018:343.0K 2019:405.2K 2020:3.15M
  42003170200                               2017:40.4K 2018:1.86M 2019:4.21M 2020:2.80M
  42003191400                               2018:336.9K 2019:900.0K 2020:150.0K
  42003191700                               2017:170.0K 2018:110.4K
  42003202300                               2017:2.92M 2018:48.0K
  42003240600                               2017:97.7K 2018:131.2K 2019:380.2K 2020:1.55M
  42003250300                               2017:150.0K 2018:39.4K 2019:808.0K 2020:1.14M
  42003250900                               2018:785.0K 2019:1.02M
  42003262000                               2017:561.2K 2018:1.50M 2019:1.59M
  42003281500                               2017:187.3K 2018:187.3K
  42003290400                               2017:385.0K 2018:593.5K 2019:800.0K
  42003300100                               2019:2.00M 2020:900.0K
  42003562400                               2017:45.0K 2018:1.53M 2019:960.0K
  42003562600                               2017:86.4K 2018:789.4K 2019:3.21M 2020:3.15M
  42003562700                               2017:2.80M 2018:1.94M 2019:489.4K 2020:3.55M
  42003980100                               2017:558.2K 2018:57.3K 2020:3.45M
  42003980400                               2017:1.60M 2018:425.0K 2020:237.5K
  42003981800                               2018:61.7K 2019:2.33M

## what

AREA: Facility Improvement 34%, Engineering and Construction 28%, Administration/Sub-Award 21%, Vehicles and Equipment 8%, Neighborhood and Community Dev 7%, Public Safety 2%

STATUS: Planned 77%, Completed 12%, In Progress 9%, Canceled 2%

ASSET_TYPE: Non-Asset 60%, Facility 9%, Park 8%, Playground 5%, Bridge 4%, Court 3%, Signalized Intersection 3%, Sidewalk 2%, Pavement 2%, Playing Field 2%, Retaining Wall 1%, Step 1%

FISCAL_YEAR: 2018 29%, 2017 27%, 2019 25%, 2020 19%

INACTIVE: False 100%

COUNCIL_DISTRICT: 3 16%, 1 14%, 7 13%, 6 13%, 2 12%, 4 10%, 5 10%, 9 7%, 8 5%

WARD: 20 14%, 17 14%, 14 11%, 19 11%, 22 8%, 15 8%, 6 7%, 4 7%, 18 7%, 12 7%, 8 7%

PUBLIC_WORKS_DIVISION: 3 32%, 5 22%, 2 20%, 1 18%, 6 7%, 0 0%

PLI_DIVISION: 20 14%, 17 14%, 14 11%, 19 11%, 22 8%, 15 8%, 6 7%, 4 7%, 18 7%, 12 7%, 8 7%

POLICE_ZONE: 3 20%, 4 19%, 1 19%, 6 15%, 2 14%, 5 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 1.0K | 0 | 2131381374 6; 1225751234 6; 1807693253 5; 1216752652 5 |
| NAME | who | 106 | 3 | CITY COUNCIL'S UNSPECIFIE 110; CAPITAL EQUIPMENT ACQUISI 82; PARK RECONSTRUCTION 67; COMPLETE STREETS 56 |
| TASK_DESCRIPTION | other | 844 | 8 | CITY COUNCIL CDBG ULO 13; Pittsburgh Action Against 8; CRITICAL SIDEWALK GAPS 7; DEMOLITION OF CITY-OWNED  7 |
| AREA | category | 7 | 3 | Facility Improvement 343; Engineering and Construct 282; Administration/Sub-Award 211; Vehicles and Equipment 83 |
| BUDGETED_AMOUNT | amount | 349 | 4 | 100000.0 64; 200000.0 45; 2500.0 39; 150000.0 37 |
| STATUS | category | 4 | 0 | Planned 768; Completed 124; In Progress 94; Canceled 16 |
| ASSET_ID | other | 262 | 588 | West Ohio Street Bridge 7; Southside Park 7; City-County Building 7; Thaddeus Stevens Elementa 6 |
| ASSET_TYPE | category | 15 | 0 | Non-Asset 588; Facility 92; Park 82; Playground 48 |
| FISCAL_YEAR | category | 4 | 0 | 2018 290; 2017 269; 2019 251; 2020 192 |
| START_DATE | date | 49 | 0 | 2017-02-08 229; 2020-09-24 186; 2018-02-12 170; 2019-03-20 105 |
| INACTIVE | category | 2 | 586 | False 416 |
| NEIGHBORHOOD | who | 75 | 503 | South Side Flats 28; South Side Slopes 20; Elliott 19; Central Business District 17 |
| COUNCIL_DISTRICT | category | 10 | 504 | 3 79; 1 68; 7 66; 6 63 |
| WARD | category | 34 | 503 | 20 38; 17 38; 14 31; 19 30 |
| TRACT | who | 104 | 502 | 42003170200 24; 42003562600 23; 42003562700 22; 42003020100 17 |
| PUBLIC_WORKS_DIVISION | category | 7 | 503 | 3 162; 5 108; 2 100; 1 91 |
| PLI_DIVISION | category | 34 | 503 | 20 38; 17 38; 14 31; 19 30 |
| POLICE_ZONE | category | 7 | 504 | 3 99; 4 94; 1 94; 6 73 |
| FIRE_ZONE | other | 83 | 503 | 4-24 25; 1-17 23; 1-6 16; 4-26 15 |
| LATITUDE | amount | 346 | 502 | 40.44247859 7; 40.45161859 7; 40.42127838 7; 40.47781114 7 |
| LONGITUDE | amount | 356 | 502 | -80.04007969 7; -80.01067255 7; -79.97805508 7; -79.91531831 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:48:46.58303 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | ed568166-33c2-4ea3-ad5e-0 1.0K |
| SRC_SHA256 | who | 1 | 0 | 5724380d35778bab7e10f8d60 1.0K |
