# PORTAL_CKA_ANALYZE_BOSTON_E4C004D662

rows 10.0K  columns 31  scan 5.3s

roles: amount 2, audit 2, category 14, date 4, empty 2, id 1, other 3, who 4

## when

OPEN_DATE
  2025      2.1K  ########
  2026      7.9K  ##############################

CLOSE_DATE
  2025      1.9K  #########
  2026      6.8K  ##############################

TARGET_CLOSE_DATE
  2025      2.1K  ########
  2026      7.9K  ##############################
  2027        27  

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LONGITUDE | 10.0K | -76.99 | -71.08 | -71.01 | -71 | -709.3K |
| LATITUDE | 10.0K | 38.90 | 42.33 | 42.39 | 42.43 | 422.3K |

## who

SERVICE_NAME by rows
      2.9K  Domestic Animal Issue
      1.6K  Wild Animal Issue
       634  Park Groundskeeping
       622  Litter & Debris
       368  Broken Park Equipment
       250  Missed Waste Pick-up
       241  Lost Pet
       225  Trash Placed Out Early
       217  Dead Animal General
       217  Pruning Request
       206  Illegal Dumping or Disposal
       202  Street Light Outage
       198  Park Litter & Debris
       197  Sidewalk Repair
       183  Improper Trash Storage
       163  Fallen Tree or Branches
       155  Pothole
       144  Overflowing Trash
       121  Park Overflowing Trash Can
       115  Illegally Blocked Sidewalk

SERVICE_NAME by dollars
      -71.06        1 rows  Snow Plowing
      -71.06        1 rows  News Boxes
      -71.06        1 rows  PWD General
      -71.06        1 rows  Bridge Maintenance
      -71.06        1 rows  Unshoveled Sidewalk
      -71.06        1 rows  Emergency Responder Snow Plowing
      -71.06        1 rows  Dropped Personal Item
     -142.08        2 rows  Fences/Guardrails/Bollards
     -142.21        2 rows  Municipal Lots
     -284.38        4 rows  Utility Casting Repair
     -355.39        5 rows  Illegal Yard Parking
     -355.63        5 rows  Lane Divider
     -497.90        7 rows  Request New Public Waste Receptacle
     -568.77        8 rows  Cemetery Maintenance
     -781.77       11 rows  Code Enforcement Collection
     -853.19       12 rows  Locked Gates
       -1.3K       19 rows  Park Suggestions
       -1.3K       18 rows  Broken Public Waste Receptacle
       -1.6K       23 rows  Unauthorized Signage
       -1.8K       25 rows  Unauthorized Vending

STREET_NAME by rows
       343  Washington St
       158  Commonwealth Ave
       145  Tremont St
       113  Shawmut Ave
       112  Massachusetts Ave
       101  Boylston St
        91  Dorchester Ave
        91  Beacon St
        76  Centre St
        68  Columbus Ave
        68  River St
        63  Atlantic Ave
        59  Hyde Park Ave
        57  Blue Hill Ave
        56  Clarendon St
        54  South St
        52  Commercial St
        50  Columbia Rd
        48  Saratoga St
        45  W Rutland Sq

STREET_NAME by dollars
         -71        1 rows  Annavoy St
         -71        1 rows  Blackinton St
         -71        1 rows  Beachview Rd
         -71        1 rows  Barnes Ave & Saint Edward Rd
      -71.01        1 rows  Bennington St & Westbrook St
      -71.01        1 rows  Faywood Ave & Orient Ave
      -71.01        1 rows  Crestway Rd
      -71.01        1 rows  Vallar Rd
      -71.01        1 rows  Thurston St
      -71.01        1 rows  Antrim St
      -71.01        1 rows  Brandywyne Dr & Saratoga St
      -71.02        1 rows  Chelsea St & Curtis St
      -71.02        1 rows  E Broadway & William J Day Blvd
      -71.02        1 rows  Farragut Rd & Columbia Rd
      -71.02        1 rows  Swift St & Frankfort St
      -71.02        1 rows  E First St & William J Day Blvd
      -71.02        1 rows  Chaucer St
      -71.02        1 rows  Cowper St
      -71.02        1 rows  Moore St
      -71.02        1 rows  Horace St

CASE_TOPIC by rows
      2.9K  Domestic Animal Issue
      1.6K  Wild Animal Issue
       634  Park Groundskeeping
       622  Litter & Debris
       368  Broken Park Equipment
       250  Missed Waste Pick-up
       241  Lost Pet
       225  Trash Placed Out Early
       217  Dead Animal General
       217  Pruning Request
       206  Illegal Dumping or Disposal
       202  Street Light Outage
       198  Park Litter & Debris
       197  Sidewalk Repair
       183  Improper Trash Storage
       163  Fallen Tree or Branches
       155  Pothole
       144  Overflowing Trash
       121  Park Overflowing Trash Can
       115  Illegally Blocked Sidewalk

CASE_TOPIC by dollars
      -71.06        1 rows  News Boxes
      -71.06        1 rows  Bridge Maintenance
      -71.06        1 rows  Snow Plowing
      -71.06        1 rows  Unshoveled Sidewalk
      -71.06        1 rows  PWD General
      -71.06        1 rows  Emergency Responder Snow Plowing
      -71.06        1 rows  Dropped Personal Item
     -142.08        2 rows  Fences/Guardrails/Bollards
     -142.21        2 rows  Municipal Lots
     -284.38        4 rows  Utility Casting Repair
     -355.39        5 rows  Illegal Yard Parking
     -355.63        5 rows  Lane Divider
     -497.90        7 rows  Request New Public Waste Receptacle
     -568.77        8 rows  Cemetery Maintenance
     -781.77       11 rows  Code Enforcement Collection
     -853.19       12 rows  Locked Gates
       -1.3K       19 rows  Park Suggestions
       -1.3K       18 rows  Broken Public Waste Receptacle
       -1.6K       23 rows  Unauthorized Signage
       -1.8K       25 rows  Unauthorized Vending

SRC_SHA256 by rows
     10.0K  296ec25f96376aa46abd0aa37c61de0a7c1d9e2eb93d60b7be90ebe36283f560

SRC_SHA256 by dollars
     -709.3K    10.0K rows  296ec25f96376aa46abd0aa37c61de0a7c1d9e2eb93d60b7be90ebe36283

## who x when

SERVICE_NAME by OPEN_DATE, dollars = LONGITUDE
  Bridge Maintenance                        2026:-71.06
  Broken Park Equipment                     2026:-26.1K
  Dead Animal General                       2026:-15.4K
  Domestic Animal Issue                     2025:-90.5K 2026:-113.0K
  Dropped Personal Item                     2026:-71.06
  Emergency Responder Snow Plowing          2026:-71.06
  Fallen Tree or Branches                   2026:-11.6K
  Fences/Guardrails/Bollards                2026:-142.08
  Illegal Dumping or Disposal               2026:-14.6K
  Illegally Blocked Sidewalk                2026:-8.2K
  Improper Trash Storage                    2026:-13.0K
  Litter & Debris                           2026:-44.2K
  Lost Pet                                  2025:-10.3K 2026:-6.8K
  Missed Waste Pick-up                      2026:-17.8K
  Municipal Lots                            2026:-142.21
  News Boxes                                2026:-71.06
  Overflowing Trash                         2026:-10.2K
  PWD General                               2026:-71.06
  Park Groundskeeping                       2025:-71.07 2026:-45.0K
  Park Litter & Debris                      2026:-14.1K
  Park Overflowing Trash Can                2026:-8.6K
  Pothole                                   2026:-11.0K
  Pruning Request                           2025:-142.11 2026:-15.3K
  Sidewalk Repair                           2026:-14.0K
  Snow Plowing                              2026:-71.06
  Street Light Outage                       2025:-781.93 2026:-13.5K
  Trash Placed Out Early                    2026:-16.0K
  Unshoveled Sidewalk                       2026:-71.06
  Utility Casting Repair                    2026:-284.38
  Wild Animal Issue                         2025:-46.6K 2026:-63.3K

STREET_NAME by OPEN_DATE, dollars = LONGITUDE
  Annavoy St                                2025:-71
  Antrim St                                 2026:-71.01
  Atlantic Ave                              2025:-1.6K 2026:-2.8K
  Barnes Ave & Saint Edward Rd              2026:-71
  Beachview Rd                              2026:-71
  Beacon St                                 2025:-995.30 2026:-5.5K
  Bennington St & Westbrook St              2025:-71.01
  Blackinton St                             2026:-71
  Blue Hill Ave                             2025:-1.1K 2026:-3.0K
  Boylston St                               2025:-1.7K 2026:-5.5K
  Centre St                                 2025:-1.2K 2026:-4.2K
  Clarendon St                              2025:-355.37 2026:-3.6K
  Columbia Rd                               2025:-710.54 2026:-2.8K
  Columbus Ave                              2025:-426.51 2026:-4.4K
  Commercial St                             2025:-497.39 2026:-3.2K
  Commonwealth Ave                          2025:-1.8K 2026:-9.4K
  Crestway Rd                               2026:-71.01
  Dorchester Ave                            2025:-994.88 2026:-5.5K
  Faywood Ave & Orient Ave                  2026:-71.01
  Hyde Park Ave                             2025:-1.1K 2026:-3.1K
  Massachusetts Ave                         2025:-995.07 2026:-7.0K
  River St                                  2025:-1.4K 2026:-3.4K
  Saratoga St                               2025:-497.15 2026:-2.9K
  Shawmut Ave                               2025:-639.63 2026:-7.4K
  South St                                  2025:-640.13 2026:-3.2K
  Thurston St                               2026:-71.01
  Tremont St                                2025:-1.8K 2026:-8.5K
  Vallar Rd                                 2025:-71.01
  W Rutland Sq                              2025:-497.56 2026:-2.7K
  Washington St                             2025:-5.6K 2026:-18.6K

## what

ASSIGNED_DEPARTMENT: Animal Care & Control 47%, Public Works Department (PWD) 29%, Parks & Recreation 23%, Boston 311 1%, Boston Transportation Departme 0%, City of Boston Property Manage 0%, Eversource 0%, Boston Public Health Commissio 0%, Boston Fire Department (BFD) 0%, MBTA (Mass Bay Transit Authori 0%

ASSIGNED_TEAM: Animal control staff 49%, Parks Operations 14%, PWD Code Enforcement (BEAM) 12%, PWD Highway (BEAM) 11%, PWD Waste Reduction 3%, Urban Forestry (BEAM) 3%, Urban Forestry 3%, PWD Street Lighting (BEAM) 1%, PWD Street Lighting 1%, Parks Maintenance (BEAM) 1%, BPRD Parks (BEAM) 1%, BPRD Parks Trades (BEAM) 1%

CASE_STATUS: Closed 88%, In progress 12%, Needs Reallocation 0%, Create 0%, Submit 0%, Apply 0%

CLOSURE_REASON: Resolved 81%, Noted 14%, Transitioned 3%, Resolved successfully 3%

ON_TIME: ONTIME 76%, OVERDUE 24%

REPORT_SOURCE: Call 56%, BOS311 44%, Email 0%

ZIP_CODE: 02118 12%, 02124 10%, 02116 10%, 02130 10%, 02128 9%, 02127 9%, 02135 8%, 02132 7%, 02125 7%, 02131 6%, 02122 6%, 02119 6%

NEIGHBORHOOD: Dorchester 21%, South End 11%, Roxbury 10%, Jamaica Plain 9%, South Boston 8%, East Boston 8%, Brighton 7%, West Roxbury 6%, Back Bay 5%, Roslindale 5%, Beacon Hill 5%, Hyde Park 5%

PUBLIC_WORKS_DISTRICT: 1C 19%, 3 11%, 4 9%, 2 9%, 1B 8%, 5 8%, 9 7%, 7B 7%, 10B 6%, 7A 6%, 10A 6%, 6A 4%

CITY_COUNCIL_DISTRICT: 1 14%, 2 14%, 3 12%, 6 12%, 8 11%, 7 10%, 4 9%, 5 9%, 9 8%, 0 0%

FIRE_DISTRICT: 4 18%, 3 13%, 9 11%, 7 11%, 10 9%, 8 9%, 11 8%, 6 8%, 12 7%, 1 6%, 0 0%

POLICE_DISTRICT: D4 17%, C11 11%, A1 11%, B2 9%, D14 8%, E5 8%, C6 8%, E13 7%, B3 7%, A7 6%, E18 5%, A15 3%

WARD: 03 14%, 05 12%, 18 11%, 20 10%, 01 9%, 04 7%, 22 7%, 06 6%, 19 6%, 17 6%, 16 6%, 08 6%

PRECINCT: 01 12%, 02 11%, 03 10%, 07 10%, 06 10%, 04 9%, 05 8%, 08 8%, 09 7%, 10 6%, 11 4%, 12 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CASE_ID | id | 9.8K | 0 | BCS-00204973 50; BCS-00208645 50; BCS-00213078 50; BCS-00212336 50 |
| OPEN_DATE | date | 10.0K | 0 | 2026-05-09 10:43:28.38683 50; 2026-05-16 19:23:32.71891 50; 2026-05-23 17:59:49.089+0 50; 2026-05-22 09:21:31.64927 50 |
| CASE_TOPIC | who | 56 | 20 | Domestic Animal Issue 2.9K; Wild Animal Issue 1.6K; Park Groundskeeping 634; Litter & Debris 622 |
| SERVICE_NAME | who | 56 | 20 | Domestic Animal Issue 2.9K; Wild Animal Issue 1.6K; Park Groundskeeping 634; Litter & Debris 622 |
| ASSIGNED_DEPARTMENT | category | 11 | 89 | Animal Care & Control 4.7K; Public Works Department ( 2.8K; Parks & Recreation 2.3K; Boston 311 58 |
| ASSIGNED_TEAM | category | 37 | 89 | Animal control staff 4.7K; Parks Operations 1.3K; PWD Code Enforcement (BEA 1.1K; PWD Highway (BEAM) 1.0K |
| CASE_STATUS | category | 6 | 0 | Closed 8.8K; In progress 1.2K; Needs Reallocation 22; Create 6 |
| CLOSURE_REASON | category | 5 | 1.2K | Resolved 7.1K; Noted 1.2K; Transitioned 236; Resolved successfully 235 |
| CLOSURE_COMMENTS | other | 1.7K | 7.6K | Property has been cited 62; violation has been issued 45; A new tree was planted at 31; Thank you for your submis 27 |
| CLOSE_DATE | date | 8.7K | 1.2K | 2026-05-21 13:34:03+00 44; 2026-05-19 11:34:03+00 44; 2026-05-25 07:15:06+00 44; 2026-05-26 12:42:04+00 44 |
| TARGET_CLOSE_DATE | date | 10.0K | 20 | 2026-05-11 10:43:28.38683 50; 2026-05-18 19:23:32.71891 50; 2026-05-26 17:59:49.089+0 50; 2026-05-24 09:21:54.58430 50 |
| ON_TIME | category | 2 | 0 | ONTIME 7.5K; OVERDUE 2.5K |
| REPORT_SOURCE | category | 3 | 0 | Call 5.6K; BOS311 4.4K; Email 1 |
| FULL_ADDRESS | other | 7.4K | 35 | 230 Shawmut Ave, Boston,  63; 1530 Washington St, Bosto 62; 300 Gardner St, Boston, M 56; 64 Sleeper St, Boston, MA 55 |
| STREET_NUMBER | other | 1.2K | 1.3K | 10 129; 1 128; 20 109; 75 103 |
| STREET_NAME | who | 2.3K | 121 | Washington St 343; Commonwealth Ave 158; Tremont St 145; Shawmut Ave 113 |
| ZIP_CODE | category | 34 | 77 | 02118 779; 02124 703; 02116 668; 02130 645 |
| NEIGHBORHOOD | category | 26 | 76 | Dorchester 1.7K; South End 866; Roxbury 751; Jamaica Plain 679 |
| PUBLIC_WORKS_DISTRICT | category | 17 | 78 | 1C 1.7K; 3 941; 4 814; 2 751 |
| CITY_COUNCIL_DISTRICT | category | 11 | 39 | 1 1.4K; 2 1.4K; 3 1.2K; 6 1.2K |
| FIRE_DISTRICT | category | 12 | 39 | 4 1.8K; 3 1.3K; 9 1.1K; 7 1.1K |
| POLICE_DISTRICT | category | 13 | 77 | D4 1.7K; C11 1.1K; A1 1.1K; B2 862 |
| WARD | category | 23 | 73 | 03 940; 05 834; 18 728; 20 651 |
| PRECINCT | category | 24 | 73 | 01 1.0K; 02 901; 03 878; 07 873 |
| SUBMITTED_PHOTO | empty | 1 | 10.0K |  |
| CLOSED_PHOTO | empty | 1 | 10.0K |  |
| LONGITUDE | amount | 7.8K | 22 | -71.066871 62; -71.0727075 60; -71.1810315 59; -71.0491275 55 |
| LATITUDE | amount | 7.4K | 22 | 42.343497 62; 42.338952 61; 42.28218 59; 42.353199 55 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:32:47.30450 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | f89124fe-66e4-44de-b3bd-3 10.0K |
| SRC_SHA256 | who | 1 | 0 | 296ec25f96376aa46abd0aa37 10.0K |
