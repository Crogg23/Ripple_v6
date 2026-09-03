# PORTAL_ARC_ORANGE_COUNTY_OP_41E4E2185F

rows 66  columns 22  scan 3.6s

roles: amount 2, audit 2, category 11, date 1, other 5, who 2

## when

INGESTED_AT
  2026        66  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITIUDE | 66 | 33.64 | 33.75 | 33.93 | 33.94 | 2.2K |
| LONGITUDE | 66 | -118.07 | -117.97 | -117.65 | -117.64 | -7.8K |

## who

BUSINESS_NAME by rows
         1  C&A Auto Repair
         1  David L. Baker Memorial Golf Center
         1  Reliable Transmission Service
         1  Midway City Feed
         1  Pro Tire & Auto Service
         1  Bolsa Auto Center
         1  RPM Carburetor Specialist
         1  Plantenders Nursery
         1  OC Auto Center
         1  D&F Auto
         1  Jake's Auto & RV Repair
         1  Ruben's Tires and Wheels
         1  Rawhide Pony Rides
         1  Giracci Farms Stables
         1  H & N Automotive
         1  Nieto & Sons Trucking, Inc.
         1  Green River Golf Course
         1  Midway Collision Repair
         1  Clutches Unlimited
         1  MD Transmission

BUSINESS_NAME by dollars
       33.94        1 rows  Nieto & Sons Trucking, Inc.
       33.93        1 rows  Brea Power LFG LLC
       33.88        1 rows  Yorba Linda Country Club
       33.87        1 rows  Green River Golf Course
       33.87        1 rows  Canyon RV Park
       33.86        1 rows  UNOCAL #5372 / Circle K
       33.86        1 rows  Anaheim Hills Tire
       33.84        1 rows  K&A Property Management
       33.84        1 rows  Action Recycling
       33.84        1 rows  R.J. Noble Company
       33.83        1 rows  Chevron Station
       33.80        1 rows  Clean Wave Express Car Wash
       33.80        1 rows  Rawhide Pony Rides
       33.80        1 rows  Irvine Ranch Outdoor Education Center
       33.80        1 rows  C&A Auto Repair
       33.80        1 rows  Hi Tech Automotive
       33.80        1 rows  Ruben's Tires and Wheels
       33.80        1 rows  Peacock Hill Equestrian Center
       33.80        1 rows  Rossmoor Arco 81782
       33.80        1 rows  D&F Auto

SRC_SHA256 by rows
        66  e10c2539d05ffd2773fe12c8d4efe5072ae57f98b8aafdf18a80bd0b09312db4

SRC_SHA256 by dollars
        2.2K       66 rows  e10c2539d05ffd2773fe12c8d4efe5072ae57f98b8aafdf18a80bd0b0931

## who x when

BUSINESS_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITIUDE
  Action Recycling                          2026:33.84
  Anaheim Hills Tire                        2026:33.86
  Bolsa Auto Center                         2026:33.75
  Brea Power LFG LLC                        2026:33.93
  C&A Auto Repair                           2026:33.80
  Canyon RV Park                            2026:33.87
  Chevron Station                           2026:33.83
  Clean Wave Express Car Wash               2026:33.80
  Clutches Unlimited                        2026:33.74
  D&F Auto                                  2026:33.80
  David L. Baker Memorial Golf Center       2026:33.73
  Giracci Farms Stables                     2026:33.73
  Green River Golf Course                   2026:33.87
  H & N Automotive                          2026:33.74
  Jake's Auto & RV Repair                   2026:33.74
  K&A Property Management                   2026:33.84
  MD Transmission                           2026:33.75
  Midway City Feed                          2026:33.75
  Midway Collision Repair                   2026:33.74
  Nieto & Sons Trucking, Inc.               2026:33.94
  OC Auto Center                            2026:33.74
  Plantenders Nursery                       2026:33.73
  Pro Tire & Auto Service                   2026:33.74
  R.J. Noble Company                        2026:33.84
  RPM Carburetor Specialist                 2026:33.74
  Rawhide Pony Rides                        2026:33.80
  Reliable Transmission Service             2026:33.74
  Ruben's Tires and Wheels                  2026:33.80
  UNOCAL #5372 / Circle K                   2026:33.86
  Yorba Linda Country Club                  2026:33.88

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITIUDE
  e10c2539d05ffd2773fe12c8d4efe5072ae57f98  2026:2.2K

## what

FACILITY_TYPE: Commercial 89%, Industrial 11%

WDID: 8 30I030132 17%, 8 30I024641 17%, 8 30I025442 17%, 8 30I026433 17%, 8 30I024034 17%, 8 30I002062 17%

STREET_NAM: Bolsa 22%, Jackson 16%, Beach 10%, Adams 10%, Katella 8%, Silverado Canyon 6%, Irvine Park 6%, E. Lincoln 4%, Baker Canyon 4%, Esperanza 4%, Santiago Canyon 4%, Los Alamitos 4%

STREET_TYP: Ave. 36%, Rd. 26%, St. 24%, Blvd. 12%, Dr. 2%

CITY: Midway City 48%, Silverado 12%, Orange 9%, Anaheim 9%, Yorba Linda 5%, Brea 3%, Santa Ana 3%, Rossmoor 3%, Fountain Valley 3%, Irvine 2%, Costa Mesa 2%, Santiago Canyon 2%

ZIP: 92655 50%, 92676 15%, 92804 8%, 92865 5%, 92886 5%, 92869 5%, 90720 3%, 92708 3%, 92602 2%, 92823 2%, 92627 2%, 92707 2%

WATERSHED: Anaheim Bay-Huntington Harbor 56%, Santa Ana River 33%, San Gabriel River-Coyote Creek 8%, Newport Bay 3%

PRIORITY: Low 62%, Medium 20%, High 18%

INSPECTION: Permit Term 62%, Every 2 Years 20%, Annually 18%

SIC_DESCRIPTION: General automotive repair 27%, Misc. amusement and recreation 13%, Motor vehicle dealers 9%, Paint shops, body and upholste 9%, Gasoline Service Stations 7%, Tires and tubes 7%, Public golf courses 7%, Local trucking without storage 4%, Electricity production 4%, Horses and other equines 4%, Ornamental floriculture and nu 4%, Membership sports and recreati 4%

SIC_CODE: 7538.0 28%, nan 13%, 7999.0 11%, 5511.0 7%, 7532.0 7%, 7997.0 6%, 5541.0 6%, 5014.0 6%, 7992.0 6%, 4212.0 4%, 4911.0 4%, 7521.0 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 67 | 0 | 66 1; 65 1; 64 1; 63 1 |
| FACILITY_TYPE | category | 2 | 0 | Commercial 59; Industrial 7 |
| REGION | other | 1 | 0 | SAR 66 |
| WDID | category | 7 | 60 | 8 30I030132 1; 8 30I024641 1; 8 30I025442 1; 8 30I026433 1 |
| BUSINESS_NAME | who | 67 | 0 | K&A Property Management 1; Baker Canyon Green Recycl 1; Action Recycling 1; Bowerman Power LFG LLC 1 |
| STREET_NUM | other | 58 | 0 | 9041.0 4; nan 2; 1.0 2; 15132.0 2 |
| STREET_NAM | category | 29 | 0 | Bolsa 11; Jackson 8; Beach 5; Adams 5 |
| STREET_TYP | category | 5 | 0 | Ave. 24; Rd. 17; St. 16; Blvd. 8 |
| CITY | category | 13 | 0 | Midway City 31; Silverado 8; Orange 6; Anaheim 6 |
| ZIP | category | 16 | 0 | 92655 31; 92676 9; 92804 5; 92865 3 |
| WATERSHED | category | 4 | 0 | Anaheim Bay-Huntington Ha 37; Santa Ana River 22; San Gabriel River-Coyote  5; Newport Bay 2 |
| LATITIUDE | amount | 66 | 0 | 33.745017 2; 33.835593 1; 33.765609 1; 33.837309 1 |
| LONGITUDE | amount | 66 | 0 | -117.983478 2; -117.858157 1; -117.659542 1; -117.844585 1 |
| PRIORITY | category | 3 | 0 | Low 41; Medium 13; High 12 |
| INSPECTION | category | 3 | 0 | Permit Term 41; Every 2 Years 13; Annually 12 |
| INVENTORY_ID | other | 67 | 0 | nan 1; SAR_Exist_Dev_159 1; SAR_Exist_Dev_69 1; SAR_Exist_Dev_10 1 |
| SIC_DESCRIPTION | category | 30 | 0 | General automotive repair 12; Misc. amusement and recre 6; Motor vehicle dealers 4; Paint shops, body and uph 4 |
| SIC_CODE | category | 23 | 0 | 7538.0 15; nan 7; 7999.0 6; 5511.0 4 |
| GEOMETRY | other | 66 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:08.12311 66 |
| SOURCE_RUN_ID | audit | 1 | 0 | d56eb9f1-98ae-4e5a-bd7c-9 66 |
| SRC_SHA256 | who | 1 | 0 | e10c2539d05ffd2773fe12c8d 66 |
