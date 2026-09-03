# PORTAL_ARC_ORANGE_COUNTY_OP_75EFFF54D5

rows 59  columns 30  scan 3.4s

roles: amount 3, audit 2, category 13, date 3, empty 2, other 4, who 4

## when

CREATIONDATE
  2025        59  ##############################

EDITDATE
  2025        59  ##############################

INGESTED_AT
  2026        59  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PHONE | 14 | 6.57B | 7.15B | 9.21B | 9.52B | 101.86B |
| GIS_LATITUDE | 58 | 33.72 | 33.74 | 33.91 | 33.94 | 2.0K |
| GIS_LONGITUDE | 58 | -118.07 | -117.98 | -117.65 | -117.64 | -6.8K |

## who

NAME by rows
         1  TA -Tatung Distribution Auto Parts
         1  Anaheim Hills Tire (Goodyear)
         1  Joe's Towing
         1  Giracci Farms Stables
         1  Peltzer Pines
         1  C&A Auto Repair
         1  Banh Collision Center
         1  Baladi Poultry Farm
         1  Tommy / Body & Paint 
         1  Canyon RV Park @ Featherly Park
         1  Reliable Transmission Service
         1  Budget Trac rental/ Avis Rental Care system
         1  Bolsa Transmission
         1  Dynamic Auto Repair
         1  Irvine Ranch Outdoor Education Center
         1  D&F Auto
         1  UNOCAL #5372 / Circle K
         1  Midway Collision Repair
         1  Nieto & Sons Trucking, Inc.
         1  David L. Baker Memorial Golf Center

NAME by dollars
       33.94        1 rows  Nieto & Sons Trucking, Inc.
       33.88        1 rows  Marlex Stucco / ParexUSA
       33.87        1 rows  Canyon RV Park @ Featherly Park
       33.87        1 rows  Green River Golf Course - Western Side
       33.86        1 rows  Anaheim Hills Tire (Goodyear)
       33.86        1 rows  UNOCAL #5372 / Circle K
       33.83        1 rows  Chevron Station
       33.80        1 rows  Peacock Hill Equestrian Center
       33.80        1 rows  Hi Tech Automotive
       33.80        1 rows  D&F Auto
       33.80        1 rows  Clean Wave Express Car Wash
       33.80        1 rows  Rawhide Pony Rides
       33.80        1 rows  C&A Auto Repair
       33.80        1 rows  Rossmoor Arco 81782
       33.80        1 rows  Irvine Ranch Outdoor Education Center
       33.80        1 rows  Ruben's Tires & Wheels
       33.77        1 rows  Irvine Lake (Includes Café)
       33.77        1 rows  River View Golf Course (and Snack Shop)
       33.76        1 rows  Santiago Event Center and RV Park
       33.75        1 rows  Dynamic Auto Repair

CREATOR by rows
        59  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
        2.0K       59 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
        59  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
        2.0K       59 rows  vickie.bach@ocpw.ocgov.com_OCPW

SRC_SHA256 by rows
        59  d2aa321ab128487f161e4b946db6fb3e13ff885007e5af2409eb84beed0bea01

SRC_SHA256 by dollars
        2.0K       59 rows  d2aa321ab128487f161e4b946db6fb3e13ff885007e5af2409eb84beed0b

## who x when

NAME by CREATIONDATE, dollars = GIS_LATITUDE
  Anaheim Hills Tire (Goodyear)             2025:33.86
  Baladi Poultry Farm                       2025:33.75
  Banh Collision Center                     2025:33.74
  Bolsa Transmission                        2025:33.74
  Budget Trac rental/ Avis Rental Care sys  2025:33.74
  C&A Auto Repair                           2025:33.80
  Canyon RV Park @ Featherly Park           2025:33.87
  Chevron Station                           2025:33.83
  Clean Wave Express Car Wash               2025:33.80
  D&F Auto                                  2025:33.80
  David L. Baker Memorial Golf Center       2025:33.73
  Dynamic Auto Repair                       2025:33.75
  Giracci Farms Stables                     2025:33.73
  Green River Golf Course - Western Side    2025:33.87
  Hi Tech Automotive                        2025:33.80
  Irvine Lake (Includes Café)               2025:33.77
  Irvine Ranch Outdoor Education Center     2025:33.80
  Joe's Towing                              2025:33.74
  Marlex Stucco / ParexUSA                  2025:33.88
  Midway Collision Repair                   2025:33.74
  Nieto & Sons Trucking, Inc.               2025:33.94
  Peacock Hill Equestrian Center            2025:33.80
  Peltzer Pines                             2025:33.75
  Rawhide Pony Rides                        2025:33.80
  Reliable Transmission Service             2025:33.74
  Rossmoor Arco 81782                       2025:33.80
  Ruben's Tires & Wheels                    2025:33.80
  TA -Tatung Distribution Auto Parts        2025:33.74
  Tommy / Body & Paint                      2025:33.75
  UNOCAL #5372 / Circle K                   2025:33.86

CREATOR by CREATIONDATE, dollars = GIS_LATITUDE
  vickie.bach@ocpw.ocgov.com_OCPW           2025:2.0K

## what

FACILITY_ID: nan 93%, OC Parks 7%

OPERATIONAL_STATUS: nan 76%, OPEN 24%

CITY: Midway City 53%, Silverado 12%, Anaheim 8%, Orange 7%, Yorba Linda 5%, Fountain Valley 3%, Rossmoor 3%, Santa Ana 2%, Santiago Canyon 2%, Brea 2%, Corona 2%, nan 2%

ZIP: Commercial 75%, 92655 8%, 92804 8%, 92887 2%, 92676 2%, 92706 2%, 92880 2%, nan 2%

INSPECTION_DATE: N 93%, N (WQ12-0011 Archery range) 3%, Y (WQ11-0016 Maintenance Facil 2%, nan 2%

PROGRAM_ELEMENT: Low (Once per Permit Term) 56%, nan 24%, Medium (Once Every 2 Years) 19%, 10% High; 20% Medium; 70% Low 2%

EXISTING_DEVELOPMENT: X 42%, nan 29%, Commercial Facilities 24%, OC Parks 5%

MOBILE_BUSINESS: nan 64%, NO 24%, X 12%

NAICS_ICS: nan 64%, X 29%, OC Parks 7%

NOI_WDID: nan 76%, N/A 24%

POLLUTANTS_IDENTIFICATION: nan 53%, N/A 24%, X 12%, No appt required 3%, JL 3%, 20-Jun 2%, 25-Jun 2%, 26-Jun 2%

ADJACENCY_TO_ESA__Y_N: nan 76%, N/A 24%

WATER_BODY_SEGMENT_IMPAIRED__Y: nan 76%, N/A 24%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 59 | 0 | 59 1; 58 1; 57 1; 56 1 |
| FACILITY_ID | category | 2 | 0 | nan 55; OC Parks 4 |
| OPERATIONAL_STATUS | category | 2 | 0 | nan 45; OPEN 14 |
| NAME | who | 58 | 0 | Canyon RV Park @ Featherl 1; Specialized Tree Works an 1; Rancho Silverado Stables  1; Plantenders Nursery 1 |
| ADDRESS | other | 56 | 0 | 1  Irvine Park Road Orang 2; 8331  Bolsa Avenue Midway 2; 9041 #B Katella Avenue An 2; 24001  Santa Ana Canyon R 1 |
| CITY | category | 12 | 0 | Midway City 31; Silverado 7; Anaheim 5; Orange 4 |
| ZIP | category | 8 | 0 | Commercial 44; 92655 5; 92804 5; 92887 1 |
| INSPECTION_DATE | category | 4 | 0 | N 55; N (WQ12-0011 Archery rang 2; Y (WQ11-0016 Maintenance  1; nan 1 |
| PHONE | amount | 14 | 0 | nan 45; 7148995555.0 2; 7146370210.0 1; 7146499251.0 1 |
| PE | empty | 1 | 59 |  |
| PROGRAM_ELEMENT | category | 4 | 0 | Low (Once per Permit Term 33; nan 14; Medium (Once Every 2 Year 11; 10% High; 20% Medium; 70% 1 |
| GIS_LATITUDE | amount | 54 | 0 | 33.803542 4; 33.74156 2; 33.745017 2; 33.868232 1 |
| GIS_LONGITUDE | amount | 53 | 0 | -117.974901 4; -117.987416 2; -117.983478 2; -117.714938 1 |
| EXISTING_DEVELOPMENT | category | 4 | 0 | X 25; nan 17; Commercial Facilities 14; OC Parks 3 |
| MOBILE_BUSINESS | category | 3 | 0 | nan 38; NO 14; X 7 |
| NAICS_ICS | category | 3 | 0 | nan 38; X 17; OC Parks 4 |
| NOI_WDID | category | 2 | 0 | nan 45; N/A 14 |
| POLLUTANTS_IDENTIFICATION | category | 8 | 0 | nan 31; N/A 14; X 7; No appt required 2 |
| ADJACENCY_TO_ESA__Y_N | category | 2 | 0 | nan 45; N/A 14 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | category | 2 | 0 | nan 45; N/A 14 |
| FIELD20 | empty | 1 | 59 |  |
| GLOBALID | other | 59 | 0 | fd6b0f6f-04cb-4209-9343-2 1; b49b1c78-1a67-4225-8746-4 1; 6f424823-dd48-4db6-9ecd-7 1; c0e32669-62a4-4670-8c9b-f 1 |
| CREATIONDATE | date | 1 | 0 | 1755810814983 59 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 59 |
| EDITDATE | date | 1 | 0 | 1755810814983 59 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 59 |
| GEOMETRY | other | 53 | 0 | {"type": "Point", "coordi 4; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:39.64137 59 |
| SOURCE_RUN_ID | audit | 1 | 0 | b7381c2e-fb2d-48dc-910c-5 59 |
| SRC_SHA256 | who | 1 | 0 | d2aa321ab128487f161e4b946 59 |
