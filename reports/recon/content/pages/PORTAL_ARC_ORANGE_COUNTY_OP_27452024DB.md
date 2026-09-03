# PORTAL_ARC_ORANGE_COUNTY_OP_27452024DB

rows 59  columns 29  scan 3.1s

roles: amount 3, audit 2, category 10, date 3, empty 5, other 3, who 4

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
| PROGRAM_ELEMENT | 58 | 33.72 | 33.74 | 33.91 | 33.94 | 2.0K |
| GIS_LATITUDE | 58 | -118.07 | -117.98 | -117.65 | -117.64 | -6.8K |

## who

NAME by rows
         1  Do's Auto Body & Repair
         1  Reliable Transmission Service
         1  Deluxe Auto
         1  Nieto & Sons Trucking, Inc.
         1  Budget Trac rental/ Avis Rental Care system
         1  Dynamic Auto Repair
         1  Beach Cities RV  Balout Auto Sales
         1  Bolsa Transmission
         1  Rawhide Pony Rides
         1  UNOCAL #5372 / Circle K
         1  Irvine Lake (Includes Café)
         1  Baladi Poultry Farm
         1  David L. Baker Memorial Golf Center
         1  Marlex Stucco / ParexUSA
         1  Tommy / Body & Paint 
         1  Chevron Station
         1  Clean Wave Express Car Wash
         1  Rossmoor Arco 81782
         1  Pro Tire & Auto Service
         1  Clutches Unlimited

NAME by dollars
       33.94        1 rows  Nieto & Sons Trucking, Inc.
       33.88        1 rows  Marlex Stucco / ParexUSA
       33.87        1 rows  Canyon RV Park @ Featherly Park
       33.87        1 rows  Green River Golf Course - Western Side
       33.86        1 rows  UNOCAL #5372 / Circle K
       33.86        1 rows  Anaheim Hills Tire (Goodyear)
       33.83        1 rows  Chevron Station
       33.80        1 rows  D&F Auto
       33.80        1 rows  Irvine Ranch Outdoor Education Center
       33.80        1 rows  Rossmoor Arco 81782
       33.80        1 rows  Rawhide Pony Rides
       33.80        1 rows  C&A Auto Repair
       33.80        1 rows  Peacock Hill Equestrian Center
       33.80        1 rows  Ruben's Tires & Wheels
       33.80        1 rows  Hi Tech Automotive
       33.80        1 rows  Clean Wave Express Car Wash
       33.77        1 rows  River View Golf Course (and Snack Shop)
       33.77        1 rows  Irvine Lake (Includes Café)
       33.76        1 rows  Santiago Event Center and RV Park
       33.75        1 rows  Rancho Silverado Stables / OC Polo

CREATOR by rows
        59  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
        2.0K       59 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
        59  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
        2.0K       59 rows  vickie.bach@ocpw.ocgov.com_OCPW

SRC_SHA256 by rows
        59  bf179760fe5b0bacbe9524c1758ad5acc67d77697f9519ec92a317e620c8ffea

SRC_SHA256 by dollars
        2.0K       59 rows  bf179760fe5b0bacbe9524c1758ad5acc67d77697f9519ec92a317e620c8

## who x when

NAME by CREATIONDATE, dollars = PROGRAM_ELEMENT
  Anaheim Hills Tire (Goodyear)             2025:33.86
  Baladi Poultry Farm                       2025:33.75
  Beach Cities RV  Balout Auto Sales        2025:33.74
  Bolsa Transmission                        2025:33.74
  Budget Trac rental/ Avis Rental Care sys  2025:33.74
  C&A Auto Repair                           2025:33.80
  Canyon RV Park @ Featherly Park           2025:33.87
  Chevron Station                           2025:33.83
  Clean Wave Express Car Wash               2025:33.80
  Clutches Unlimited                        2025:33.74
  D&F Auto                                  2025:33.80
  David L. Baker Memorial Golf Center       2025:33.73
  Deluxe Auto                               2025:33.74
  Do's Auto Body & Repair                   2025:33.74
  Dynamic Auto Repair                       2025:33.75
  Green River Golf Course - Western Side    2025:33.87
  Hi Tech Automotive                        2025:33.80
  Irvine Lake (Includes Café)               2025:33.77
  Irvine Ranch Outdoor Education Center     2025:33.80
  Marlex Stucco / ParexUSA                  2025:33.88
  Nieto & Sons Trucking, Inc.               2025:33.94
  Peacock Hill Equestrian Center            2025:33.80
  Pro Tire & Auto Service                   2025:33.74
  Rawhide Pony Rides                        2025:33.80
  Reliable Transmission Service             2025:33.74
  River View Golf Course (and Snack Shop)   2025:33.77
  Rossmoor Arco 81782                       2025:33.80
  Ruben's Tires & Wheels                    2025:33.80
  Tommy / Body & Paint                      2025:33.75
  UNOCAL #5372 / Circle K                   2025:33.86

CREATOR by CREATIONDATE, dollars = PROGRAM_ELEMENT
  vickie.bach@ocpw.ocgov.com_OCPW           2025:2.0K

## what

FACILITY_ID: nan 76%, OPEN 24%

CITY: Midway City 53%, Silverado 12%, Anaheim 8%, Orange 7%, Yorba Linda 5%, Fountain Valley 3%, Rossmoor 3%, Santa Ana 2%, Santiago Canyon 2%, Brea 2%, Corona 2%, nan 2%

ZIP: N 93%, N (WQ12-0011 Archery range) 3%, Y (WQ11-0016 Maintenance Facil 2%, nan 2%

PE: Low (Once per Permit Term) 56%, nan 24%, Medium (Once Every 2 Years) 19%, 10% High; 20% Medium; 70% Low 2%

EXISTING_DEVELOPMENT: nan 64%, NO 24%, X 12%

MOBILE_BUSINESS: nan 64%, X 29%, OC Parks 7%

NAICS_ICS: nan 76%, N/A 24%

NOI_WDID: nan 53%, N/A 24%, X 12%, No appt required 3%, JL 3%, 20-Jun 2%, 25-Jun 2%, 26-Jun 2%

POLLUTANTS_IDENTIFICATION: nan 76%, N/A 24%

ADJACENCY_TO_ESA__Y_N: nan 76%, N/A 24%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 59 | 0 | 59 1; 58 1; 57 1; 56 1 |
| FACILITY_ID | category | 2 | 0 | nan 45; OPEN 14 |
| OPERATIONAL_STATUS | empty | 1 | 59 |  |
| NAME | who | 58 | 0 | Canyon RV Park @ Featherl 1; Specialized Tree Works an 1; Rancho Silverado Stables  1; Plantenders Nursery 1 |
| ADDRESS | other | 56 | 0 | 1  Irvine Park Road Orang 2; 8331  Bolsa Avenue Midway 2; 9041 #B Katella Avenue An 2; 24001  Santa Ana Canyon R 1 |
| CITY | category | 12 | 0 | Midway City 31; Silverado 7; Anaheim 5; Orange 4 |
| ZIP | category | 4 | 0 | N 55; N (WQ12-0011 Archery rang 2; Y (WQ11-0016 Maintenance  1; nan 1 |
| INSPECTION_DATE | empty | 1 | 59 |  |
| PHONE | amount | 14 | 0 | nan 45; 7148995555.0 2; 7146370210.0 1; 7146499251.0 1 |
| PE | category | 4 | 0 | Low (Once per Permit Term 33; nan 14; Medium (Once Every 2 Year 11; 10% High; 20% Medium; 70% 1 |
| PROGRAM_ELEMENT | amount | 54 | 0 | 33.803542 4; 33.74156 2; 33.745017 2; 33.868232 1 |
| GIS_LATITUDE | amount | 53 | 0 | -117.974901 4; -117.987416 2; -117.983478 2; -117.714938 1 |
| GIS_LONGITUDE | empty | 1 | 59 |  |
| EXISTING_DEVELOPMENT | category | 3 | 0 | nan 38; NO 14; X 7 |
| MOBILE_BUSINESS | category | 3 | 0 | nan 38; X 17; OC Parks 4 |
| NAICS_ICS | category | 2 | 0 | nan 45; N/A 14 |
| NOI_WDID | category | 8 | 0 | nan 31; N/A 14; X 7; No appt required 2 |
| POLLUTANTS_IDENTIFICATION | category | 2 | 0 | nan 45; N/A 14 |
| ADJACENCY_TO_ESA__Y_N | category | 2 | 0 | nan 45; N/A 14 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | empty | 1 | 59 |  |
| FIELD20 | empty | 1 | 59 |  |
| GLOBALID | other | 58 | 0 | 661ab11f-4495-4312-a751-d 1; 330c4e79-4f9e-4b24-8c3d-9 1; 82deaee5-6dbe-4c8d-93ab-2 1; 79bb43b4-6716-4214-baf7-4 1 |
| CREATIONDATE | date | 1 | 0 | 1755810816452 59 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 59 |
| EDITDATE | date | 1 | 0 | 1755810816452 59 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 59 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:50.28900 59 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4728ec8e-1285-4e34-849a-9 59 |
| SRC_SHA256 | who | 1 | 0 | bf179760fe5b0bacbe9524c17 59 |
