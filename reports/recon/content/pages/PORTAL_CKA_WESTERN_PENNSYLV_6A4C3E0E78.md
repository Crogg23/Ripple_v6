# PORTAL_CKA_WESTERN_PENNSYLV_6A4C3E0E78

rows 1.0K  columns 39  scan 6.1s

roles: amount 11, audit 2, category 12, date 4, id 1, other 2, who 8

## when

INSPECTION_DATE
  2021       112  ######
  2022       600  ##############################
  2023       197  ##########
  2024        91  #####

INSPECTION_END
  2021       109  #####
  2022       600  ##############################
  2023       195  ##########
  2024        95  #####

ABATED_DATE
  2021        87  #####
  2022       503  ##############################
  2023       237  ##############
  2024       125  #######
  2025        13  #

INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FACILITY_LATITUDE | 935 | 40.24 | 40.44 | 40.66 | 40.67 | 37.8K |
| FACILITY_LONGITUDE | 935 | -80.27 | -80 | -79.72 | -79.71 | -74.8K |
| FREE_CHLORINE_SHALLOW | 793 | 0 | 3 | 14 | 32 | 2.6K |
| FREE_CHLORINE_DEEP | 374 | 0 | 3 | 12.54 | 26 | 1.2K |
| COMBINED_CHLORINE_SHALLOW | 798 | 0 | 0 | 3 | 10.04 | 166.64 |
| COMBINED_CHLORINE_DEEP | 372 | 0 | 0 | 3 | 10.04 | 101.14 |

## who

FACILITY_NAME by rows
         9  RIVERS CLUB MEN'S SPA
         9  HOME 2 SUITES POOL
         8  COMFORT INN & SUITES NORTH SHORE - POOL
         7  HAMPTON INN MONROEVILLE POOL
         6  COMFORT INN SUITES - POOL
         6  LA FITNESS NORTH HILLS POOL
         5  SPRINGHILL SUITES NORTH SHORE POOL
         5  LA FITNESS NORTH HILLS SPA
         5  DOUBLETREE BY HILTON PGH CRANBERRY POOL
         5  LA FITNESS POOL - COLLIER
         5  SPRINGHILL SUITES MONROEVILLE POOL
         5  GOLDFISH SWIM SCHOOL
         5  KAUFMANNS GRAND ON 5TH POOL
         4  BAIERL FAMILY YMCA  POOL - INDOOR
         4  MCKNIGHT HOTEL - POOL
         4  PARK WEST 205 APARTMENT POOL
         4  GLASSHOUSE OF PITTSBURGH POOL 
         4  STAYBRIDGE SUITES CRANBERRY POOL
         4  COURTYARD BY MARRIOTT WEST HOMESTEAD - SPA
         4  CAMBRIA SUITES PGH @ PPG PAINTS ARENA POOL

FACILITY_NAME by dollars
      365.04        9 rows  HOME 2 SUITES POOL
      363.96        9 rows  RIVERS CLUB MEN'S SPA
      323.60        8 rows  COMFORT INN & SUITES NORTH SHORE - POOL
      283.08        7 rows  HAMPTON INN MONROEVILLE POOL
      243.36        6 rows  LA FITNESS NORTH HILLS POOL
         243        6 rows  COMFORT INN SUITES - POOL
      203.35        5 rows  DOUBLETREE BY HILTON PGH CRANBERRY POOL
      202.84        5 rows  GOLDFISH SWIM SCHOOL
      202.80        5 rows  LA FITNESS NORTH HILLS SPA
      202.25        5 rows  SPRINGHILL SUITES NORTH SHORE POOL
      202.20        5 rows  KAUFMANNS GRAND ON 5TH POOL
      202.20        5 rows  SPRINGHILL SUITES MONROEVILLE POOL
      201.85        5 rows  LA FITNESS POOL - COLLIER
      162.64        4 rows  STAYBRIDGE SUITES CRANBERRY POOL
      162.44        4 rows  POLO FIELDS AT HAMPTON POOL
      162.44        4 rows  BAIERL FAMILY YMCA  POOL - INDOOR
      162.28        4 rows  FAIRFIELD INN & SUITES BY MARRIOTT-MCCANDLESS POOL
      162.16        4 rows  CHARLEMAGNE II POOL
      162.16        4 rows  HOLIDAY INN EXPRESS HARMAR / POOL
      162.04        4 rows  CASCADES POOL

FACILITY_MUNICIPALITY_NAME by rows
       267  Pittsburgh
        54  Monroeville
        50  McCandless
        36  Ross Township
        32  Moon Township
        28  Bethel Park
        26  Collier Township
        26  West Homestead
        25  Penn Hills
        24  O'Hara Township
        21  Robinson Township
        19  Green Tree
        19  South Fayette Township
        18  Hampton Township
        17  Pine Township
        16  Mount Lebanon
        16  Plum
        15  Scott Township
        15  Upper St Clair Township
        15  Marshall Township

FACILITY_MUNICIPALITY_NAME by dollars
       10.0K      267 rows  Pittsburgh
        1.8K       54 rows  Monroeville
        1.7K       50 rows  McCandless
        1.3K       36 rows  Ross Township
        1.2K       32 rows  Moon Township
        1.1K       26 rows  West Homestead
        1.0K       28 rows  Bethel Park
        1.0K       25 rows  Penn Hills
      971.94       24 rows  O'Hara Township
      928.86       26 rows  Collier Township
         768       19 rows  Green Tree
      766.69       19 rows  South Fayette Township
      690.80       17 rows  Pine Township
      690.02       18 rows  Hampton Township
      687.53       21 rows  Robinson Township
      646.12       16 rows  Mount Lebanon
      607.35       16 rows  Plum
      606.48       15 rows  Wilkins Township
      605.83       15 rows  Scott Township
      569.19       15 rows  Marshall Township

FACILITY_ID by rows
         9  1944
         8  9097
         7  7026
         6  1233
         6  7735
         5  739
         5  1234
         5  1399
         5  3922
         5  7261
         5  1016
         5  9717
         4  2366
         4  10522
         4  2002
         4  8956
         4  1972
         4  748
         4  2507
         4  1410

FACILITY_ID by dollars
      363.96        9 rows  1944
      323.60        8 rows  9097
      283.08        7 rows  7026
      243.36        6 rows  1233
         243        6 rows  7735
      203.35        5 rows  3922
      202.80        5 rows  1234
      202.80        5 rows  1399
      202.25        5 rows  739
      202.20        5 rows  9717
      202.20        5 rows  7261
      201.85        5 rows  1016
      162.44        4 rows  855
      162.44        4 rows  167
      162.28        4 rows  5802
      162.24        4 rows  10522
      162.16        4 rows  2234
      162.16        4 rows  2298
      162.04        4 rows  2308
         162        4 rows  1097

FACILITY_ADDRESS by rows
        20  1000 SANDCASTLE DRIVE
        15  5738 FORBES AVENUE
        12  301 GRANT STREET
        11  8700 DUNCAN AVENUE
         9  8630 DUNCAN AVENUE
         8  820 E OHIO STREET
         8  1000 HIGBEE DRIVE
         8  4575 MCKNIGHT ROAD
         8  625 BLACKBURN ROAD
         7  699 RODI ROAD
         7  100 VILLAGE CLUB DRIVE
         7  3000 MOSSIDE BOULEVARD
         6  600 COMMONWEALTH PLACE
         6  517 TWIN OAK DRIVE
         6   VERONA ROAD
         6  2200 GOLDEN MILE HIGHWAY
         6  1155 WASHINGTON PIKE
         6  401 W WATERFRONT DRIVE
         6  180 GAMMA  DRIVE
         6  435 FREEMONT STREET

FACILITY_ADDRESS by dollars
         808       20 rows  1000 SANDCASTLE DRIVE
      606.60       15 rows  5738 FORBES AVENUE
      485.28       12 rows  301 GRANT STREET
      446.16       11 rows  8700 DUNCAN AVENUE
      365.04        9 rows  8630 DUNCAN AVENUE
      324.32        8 rows  625 BLACKBURN ROAD
         324        8 rows  4575 MCKNIGHT ROAD
      323.60        8 rows  820 E OHIO STREET
      322.72        8 rows  1000 HIGBEE DRIVE
      284.41        7 rows  100 VILLAGE CLUB DRIVE
      283.08        7 rows  3000 MOSSIDE BOULEVARD
      283.08        7 rows  699 RODI ROAD
         243        6 rows  180 GAMMA  DRIVE
      242.94        6 rows   VERONA ROAD
      242.88        6 rows  517 TWIN OAK DRIVE
      242.76        6 rows  2200 GOLDEN MILE HIGHWAY
      242.64        6 rows  600 COMMONWEALTH PLACE
      242.46        6 rows  401 W WATERFRONT DRIVE
      242.22        6 rows  1155 WASHINGTON PIKE
      241.80        6 rows  435 FREEMONT STREET

## who x when

FACILITY_NAME by INSPECTION_DATE, dollars = FACILITY_LATITUDE
  BAIERL FAMILY YMCA  POOL - INDOOR         2022:81.22 2023:81.22
  CAMBRIA SUITES PGH @ PPG PAINTS ARENA PO  2022:121.32 2023:40.44
  CASCADES POOL                             2022:81.02 2023:40.51 2024:40.51
  CHARLEMAGNE II POOL                       2022:121.62 2023:40.54
  COMFORT INN & SUITES NORTH SHORE - POOL   2021:40.45 2022:161.80 2023:40.45 2024:80.90
  COMFORT INN SUITES - POOL                 2021:40.50 2022:81 2023:121.50
  COURTYARD BY MARRIOTT WEST HOMESTEAD - S  2022:80.82 2023:80.82
  DOUBLETREE BY HILTON PGH CRANBERRY POOL   2021:40.67 2022:122.01 2024:40.67
  FAIRFIELD INN & SUITES BY MARRIOTT-MCCAN  2021:81.14 2022:40.57 2023:40.57
  GLASSHOUSE OF PITTSBURGH POOL             2022:121.29 2023:40.43
  GOLDFISH SWIM SCHOOL                      2021:40.62 2022:162.22
  HAMPTON INN MONROEVILLE POOL              2021:40.44 2022:121.32 2023:80.88 2024:40.44
  HOLIDAY INN EXPRESS HARMAR / POOL         2022:81.08 2023:40.54 2024:40.54
  HOME 2 SUITES POOL                        2021:81.12 2022:121.68 2023:162.24
  KAUFMANNS GRAND ON 5TH POOL               2022:121.32 2023:80.88
  LA FITNESS NORTH HILLS POOL               2021:40.56 2022:121.68 2023:40.56 2024:40.56
  LA FITNESS NORTH HILLS SPA                2021:40.56 2022:121.68 2024:40.56
  LA FITNESS POOL - COLLIER                 2021:40.37 2022:121.11 2024:40.37
  MCKNIGHT HOTEL - POOL                     2021:40.50 2022:40.50 2023:81
  PARK WEST 205 APARTMENT POOL              2022:80.86 2023:40.43 2024:40.43
  POLO FIELDS AT HAMPTON POOL               2022:162.44
  RIVERS CLUB MEN'S SPA                     2021:80.88 2022:242.64 2023:40.44
  SPRINGHILL SUITES MONROEVILLE POOL        2021:80.88 2022:121.32
  SPRINGHILL SUITES NORTH SHORE POOL        2021:40.45 2023:80.90 2024:80.90
  STAYBRIDGE SUITES CRANBERRY POOL          2021:81.32 2023:81.32

FACILITY_MUNICIPALITY_NAME by INSPECTION_DATE, dollars = FACILITY_LATITUDE
  Bethel Park                               2022:645.36 2023:322.67 2024:80.68
  Collier Township                          2021:121.13 2022:565.39 2023:121.17 2024:121.17
  Green Tree                                2021:202.10 2022:404.22 2023:80.84 2024:80.84
  Hampton Township                          2021:81.16 2022:487.11 2023:81.16 2024:40.59
  Marshall Township                         2021:162.63 2022:243.94 2023:121.95 2024:40.67
  McCandless                                2021:283.95 2022:933.13 2023:405.66 2024:81.12
  Monroeville                               2021:242.63 2022:1.2K 2023:323.41 2024:40.44
  Moon Township                             2021:80.97 2022:688.61 2023:405.16
  Mount Lebanon                             2021:121.15 2022:323.05 2023:40.39 2024:161.53
  O'Hara Township                           2021:40.50 2022:607.46 2023:323.98
  Penn Hills                                2022:688.19 2023:242.91 2024:80.96
  Pine Township                             2021:162.54 2022:365.68 2023:81.29 2024:81.29
  Pittsburgh                                2021:1.9K 2022:4.9K 2023:1.9K 2024:1.3K
  Plum                                      2022:526.36 2024:80.99
  Robinson Township                         2021:80.88 2022:404.46 2023:80.86 2024:121.33
  Ross Township                             2021:81 2022:891.61 2023:283.66 2024:81.06
  Scott Township                            2021:121.17 2022:323.09 2023:121.18 2024:40.39
  South Fayette Township                    2021:80.76 2022:443.88 2023:121.02 2024:121.03
  Upper St Clair Township                   2022:403.26 2023:80.65 2024:80.62
  West Homestead                            2022:646.44 2023:404.02
  Wilkins Township                          2021:161.73 2022:242.59 2023:202.16

## what

FACILITY_ADDRESS_2:  #411 31%, Building & Grounds Dept 14%, Ste 411 10%, Managers Office 7%, #114 7%, Rt#286 7%, Po Box  12420 7%, 4th Floor 7%, 2622 3%, #T4 3%, PO Box 7735 3%

FACILITY_STATE: PA 100%

VENUE_TYPE: POOLS (OUTDOOR) 34%, POOLS (INDOOR) 25%, POOL (CONDO OUTDOOR) 11%, POOLS (SCHOOLS) 10%, SPA/HOT TUB (INDOOR) 8%, WADING POOL SYSTEM 7%, POOL (CONDO INDOOR) 2%, WATER SLIDE POOLS 1%, SPA/HOT TUB (OUTDOOR) 1%

INSPECTION_PURPOSE: INITIAL INSPECTION 66%, FOLLOW UP INSPECTION 34%

INSPECTION_PASSED: True 72%, False 28%

INSPECTION_NUMBER: 1 66%, 2 22%, 3 7%, 4 3%, 5 1%, 6 1%, 9 0%, 10 0%, 8 0%, 7 0%

INSPECTOR_NAME: NOBBS SCOTT 22%, MURPHY COLLEEN 16%, MANOWN MARYANN 12%, FREEMAN MICHELE 8%, WILSON ANGELA 8%, CONLEY FAON 7%, LAURIA D. ANTHONY 7%, WOLFE CURRIER 6%, ANDERSON IAN 5%, ZIRNGIBL BARBARA 3%, NABLO MARIAH 3%, MUSA AMINATA 2%

CYANURIC_ACID: <30 36%, <50 24%, 0 18%, 50 4%, 30 4%, 40 4%, 45 3%, 35 3%, 30 > 1%, >50 1%, 0-30 1%

MAIN_DRAIN_VISIBLE: True 99%, False 1%

SAFETY_EQUIPMENT: True 52%, False 48%

PH_BALANCE: True 92%, False 8%

NO_IMMINENT_HEALTH_HAZARDS: True 96%, False 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INSPECTION_ID | id | 1.0K | 0 | 214560 5; 214555 5; 214509 5; 214502 5 |
| FACILITY_ID | who | 532 | 0 | 1944 9; 9097 8; 10522 8; 2308 7 |
| FACILITY_NAME | who | 518 | 0 | RIVERS CLUB MEN'S SPA 9; HOME 2 SUITES POOL 9; COMFORT INN & SUITES NORT 8; CASCADES POOL 7 |
| FACILITY_ADDRESS | who | 433 | 0 | 1000 SANDCASTLE DRIVE 20; 5738 FORBES AVENUE 15; 301 GRANT STREET 12; 8700 DUNCAN AVENUE 11 |
| FACILITY_ADDRESS_2 | category | 13 | 970 |  #411 9; Building & Grounds Dept 4; Ste 411 3; Managers Office 2 |
| FACILITY_MUNICIPALITY_NAME | who | 76 | 2 | Pittsburgh 267; Monroeville 54; McCandless 50; Ross Township 36 |
| FACILITY_CITY | who | 70 | 0 | PITTSBURGH 440; Pittsburgh 121; MONROEVILLE 41; SEWICKLEY 27 |
| FACILITY_COUNTY | who | 1 | 0 | Allegheny County 1.0K |
| FACILITY_STATE | category | 2 | 2 | PA 998 |
| FACILITY_POSTAL_CODE | who | 75 | 2 | 15237 86; 15146 54; 15219 53; 15108 45 |
| FACILITY_LATITUDE | amount | 397 | 65 | 40.397805 20; 40.437657 15; 40.437999 12; 40.562811 11 |
| FACILITY_LONGITUDE | amount | 391 | 65 | -79.9272225 20; -79.9239015 15; -79.998606 12; -80.026578 11 |
| VENUE_TYPE | category | 9 | 0 | POOLS (OUTDOOR) 340; POOLS (INDOOR) 254; POOL (CONDO OUTDOOR) 113; POOLS (SCHOOLS) 102 |
| INSPECTION_DATE | date | 919 | 0 | 2023-06-27T11:00:00 9; 2024-06-17T11:30:00 6; 2024-03-27T15:30:00 6; 2023-08-22T11:00:00 6 |
| INSPECTION_END | date | 960 | 1 | 2023-07-03T15:00:00 7; 2024-06-24T13:30:00 6; 2023-07-25T14:30:00 6; 2023-07-24T13:10:00 6 |
| INSPECTION_PURPOSE | category | 2 | 0 | INITIAL INSPECTION 662; FOLLOW UP INSPECTION 338 |
| INSPECTION_PASSED | category | 2 | 0 | True 716; False 284 |
| INSPECTION_NUMBER | category | 10 | 0 | 1 662; 2 219; 3 70; 4 27 |
| INSPECTOR_NAME | category | 22 | 0 | NOBBS SCOTT 206; MURPHY COLLEEN 150; MANOWN MARYANN 116; FREEMAN MICHELE 79 |
| FREE_CHLORINE_SHALLOW | amount | 60 | 207 | 3.0 72; 4.0 58; 2.0 54; 2.4 45 |
| FREE_CHLORINE_DEEP | amount | 55 | 626 | 3.0 37; 2.0 24; 4.0 23; 2.2 20 |
| COMBINED_CHLORINE_SHALLOW | amount | 21 | 202 | 0.0 475; 0.2 205; 0.4 31; 0.6 29 |
| COMBINED_CHLORINE_DEEP | amount | 20 | 628 | 0.0 220; 0.2 106; 0.4 11; 3.0 8 |
| FREE_BROMINE_SHALLOW | amount | 31 | 847 | 0.0 104; 6.0 8; 10.0 5; 3.0 4 |
| FREE_BROMINE_DEEP | amount | 5 | 892 | 0.0 104; 3.0 2; 7.6 1; 5.8 1 |
| PH_VALUE_SHALLOW | amount | 19 | 165 | 7.4 351; 7.2 179; 7.6 154; 7.8 60 |
| PH_VALUE_DEEP | amount | 17 | 623 | 7.4 154; 7.2 77; 7.6 73; 7.8 22 |
| CYANURIC_ACID | category | 32 | 683 | <30 99; <50 66; 0 50; 50 12 |
| TURNOVER | amount | 174 | 259 | 60.0 38; 80.0 36; 70.0 35; 50.0 35 |
| ENCLOSURE | other | 1 | 0 | True 1.0K |
| MAIN_DRAIN_VISIBLE | category | 2 | 0 | True 991; False 9 |
| SAFETY_EQUIPMENT | category | 2 | 0 | True 520; False 480 |
| DISINFECTANT_LEVEL | other | 1 | 0 | True 1.0K |
| PH_BALANCE | category | 2 | 0 | True 925; False 75 |
| NO_IMMINENT_HEALTH_HAZARDS | category | 2 | 0 | True 957; False 43 |
| ABATED_DATE | date | 335 | 35 | 2022-07-14 28; 2022-08-16 22; 2022-08-10 20; 2022-07-25 19 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:48:22.23957 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9bc40c89-3d83-4ada-80b5-f 1.0K |
| SRC_SHA256 | who | 1 | 0 | 92e6188a2a9b578ddc841681c 1.0K |
