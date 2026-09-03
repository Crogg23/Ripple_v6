# PORTAL_ARC_ORANGE_COUNTY_OP_BFABCC10A2

rows 72  columns 30  scan 3.5s

roles: amount 2, audit 2, category 6, date 3, empty 4, other 8, who 6

## when

CREATIONDATE
  2025        72  ##############################

EDITDATE
  2025        72  ##############################

INGESTED_AT
  2026        72  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GIS_LATITUDE | 72 | 33.52 | 33.56 | 33.69 | 33.69 | 2.4K |
| GIS_LONGITUDE | 72 | -117.65 | -117.63 | -117.53 | -117.51 | -8.5K |

## who

NAME by rows
         2  NEKTER JUICE BAR
         2  STARBUCKS COFFEE COMPANY
         1  BASKIN ROBBINS ICE CREAM
         1  QUEST SJC
         1  PRESERVE RESTURANT
         1  PICK UP STIX
         1  ONIGURU
         1  THAI FIX
         1  24 HOUR FITNESS
         1  MANIOTO'S BAKERY
         1  COSMOS ITALIAN KITCHEN
         1  TACO BELL #19895
         1  LOLAS CAFE
         1  SAV-ON PHARMACY # 9552
         1  GELSONS MARKETS
         1  JOES RESTAURANT AND BAR
         1  IN N OUT
         1  BURGER KING #13906
         1  BRUEGGERS BAGEL BAKERY
         1  STARBUCKS COFFEE #6603

NAME by dollars
       67.09        2 rows  NEKTER JUICE BAR
       67.08        2 rows  STARBUCKS COFFEE COMPANY
       33.69        1 rows  RANCHO LAS LOMAS
       33.69        1 rows  COOKS CORNER
       33.66        1 rows  ROSE CANYON CANTINA
       33.66        1 rows  TRABUCO GENERAL STORE
       33.66        1 rows  TRABUCO OAKS STEAKHOUSE
       33.63        1 rows  COTO VALLEY COUNTRY CLUB
       33.61        1 rows  LAZY W RANCH
       33.60        1 rows  COTO DE CAZA GOLF & RACQUET CLUB
       33.60        1 rows  PRESERVE RESTURANT
       33.58        1 rows  MESA FOOD & LIQUOR
       33.58        1 rows  STARBUCKS COFFEE #9288
       33.58        1 rows  JACK IN THE BOX #3387
       33.58        1 rows  TACO BELL #19895
       33.58        1 rows  WENDIS DONUTS
       33.58        1 rows  COSMOS ITALIAN KITCHEN
       33.58        1 rows  PICK UP STIX
       33.57        1 rows  THAI FIX
       33.57        1 rows  JOES RESTAURANT AND BAR

EXISTING_DEVELOPMENTS by rows
        72  Commercial Facilities

EXISTING_DEVELOPMENTS by dollars
        2.4K       72 rows  Commercial Facilities

CREATOR by rows
        72  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
        2.4K       72 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
        72  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
        2.4K       72 rows  vickie.bach@ocpw.ocgov.com_OCPW

## who x when

NAME by CREATIONDATE, dollars = GIS_LATITUDE
  24 HOUR FITNESS                           2025:33.56
  BASKIN ROBBINS ICE CREAM                  2025:33.56
  BRUEGGERS BAGEL BAKERY                    2025:33.56
  BURGER KING #13906                        2025:33.56
  COOKS CORNER                              2025:33.69
  COSMOS ITALIAN KITCHEN                    2025:33.58
  COTO DE CAZA GOLF & RACQUET CLUB          2025:33.60
  COTO VALLEY COUNTRY CLUB                  2025:33.63
  GELSONS MARKETS                           2025:33.52
  IN N OUT                                  2025:33.52
  JOES RESTAURANT AND BAR                   2025:33.57
  LAZY W RANCH                              2025:33.61
  LOLAS CAFE                                2025:33.56
  MANIOTO'S BAKERY                          2025:33.52
  MESA FOOD & LIQUOR                        2025:33.58
  NEKTER JUICE BAR                          2025:67.09
  ONIGURU                                   2025:33.56
  PICK UP STIX                              2025:33.58
  PRESERVE RESTURANT                        2025:33.60
  QUEST SJC                                 2025:33.56
  RANCHO LAS LOMAS                          2025:33.69
  ROSE CANYON CANTINA                       2025:33.66
  SAV-ON PHARMACY # 9552                    2025:33.56
  STARBUCKS COFFEE #6603                    2025:33.56
  STARBUCKS COFFEE #9288                    2025:33.58
  STARBUCKS COFFEE COMPANY                  2025:67.08
  TACO BELL #19895                          2025:33.58
  THAI FIX                                  2025:33.57
  TRABUCO GENERAL STORE                     2025:33.66
  TRABUCO OAKS STEAKHOUSE                   2025:33.66

EXISTING_DEVELOPMENTS by CREATIONDATE, dollars = GIS_LATITUDE
  Commercial Facilities                     2025:2.4K

## what

OPERATIONAL_STATUS: OPEN 90%, NEW 10%

CITY: LADERA RANCH 57%, RANCHO MISSION VIEJO 18%, LAS FLORES 10%, TRABUCO CANYON 6%, COTO DE CAZA 4%, SAN JUAN CAPISTRANO 3%, SILVERADO  1%, MISSION VIEJO 1%

ZIP: 92694 72%, 92679 10%, 92688 8%, 92675 4%, 92676 1%, 92678 1%, 92649 1%, 92651 1%

PE: 0111 24%, 0132 20%, 0133 14%, 0134 12%, 0112 7%, 0113 5%, 0308 5%, 0131 3%, 0391 3%, 0115 3%, 0135 3%

PROGRAM_ELEMENT: RESTAURANT UNDER 31 PERSONS -  24%, RESTAURANT 31-60 PERSONS - COM 20%, RESTAURANT 61-100 PERSONS - CO 14%, RESTAURANT 101-150 PERSONS - C 12%, RESTAURANT 31-60 PERSONS - NON 7%, RESTAURANT 61-100 PERSONS - NO 5%, FOOD MARKET W/ 2+ PREP AREAS 3 5%, RESTAURANT UNDER 31 PERSONS -  3%, FOOD MARKET - PACKAGED FOOD 1- 3%, RESTAURANT 151-200 PERSONS - N 3%, RESTAURANT 151-200 PERSONS - C 3%

MOBILE_BUSINESS: No 79%, NO 21%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 72 | 0 | 72 1; 71 1; 70 1; 69 1 |
| FACILITY_ID | who | 67 | 7 | FA0057365 1; FA0043615 1; FA0017684 1; FA0012416 1 |
| OPERATIONAL_STATUS | category | 2 | 0 | OPEN 65; NEW 7 |
| NAME | who | 69 | 0 | NEKTER JUICE BAR 2; STARBUCKS COFFEE COMPANY 2; RANCHO LAS LOMAS 1; STARBUCKS COFFEE #9288 1 |
| ADDRESS | other | 70 | 0 | 25291 VISTA DEL VERDE  2; 30731 GATEWAY PL 2; 19191 LAWRENCE CYN 1; 28562 OSO PKWY STE F 1 |
| CITY | category | 8 | 0 | LADERA RANCH 41; RANCHO MISSION VIEJO 13; LAS FLORES 7; TRABUCO CANYON 4 |
| ZIP | category | 8 | 0 | 92694 52; 92679 7; 92688 6; 92675 3 |
| INSPECTION_DATE | other | 1 | 0 | N/A 72 |
| PHONE | other | 71 | 0 | 9498584100 2; 9498883080 1; 9496359215 1; 9498888155 1 |
| PE | category | 19 | 5 | 0111 14; 0132 12; 0133 8; 0134 7 |
| PROGRAM_ELEMENT | category | 19 | 5 | RESTAURANT UNDER 31 PERSO 14; RESTAURANT 31-60 PERSONS  12; RESTAURANT 61-100 PERSONS 8; RESTAURANT 101-150 PERSON 7 |
| GIS_LATITUDE | amount | 70 | 0 | 33.52197 2; 33.5601 2; 33.689023 1; 33.5829976490935 1 |
| GIS_LONGITUDE | amount | 71 | 0 | -117.628751 2; -117.6462 2; -117.624283 1; -117.632436727555 1 |
| EXISTING_DEVELOPMENTS | who | 1 | 0 | Commercial Facilities 72 |
| MOBILE_BUSINESS | category | 2 | 0 | No 57; NO 15 |
| NAICS_ICS | empty | 1 | 72 |  |
| NOI_WDID | other | 1 | 0 | N/A 72 |
| POLLUTANTS_IDENTIFICATION | empty | 1 | 72 |  |
| ADJACENCY_TO_ESA__Y_N | other | 1 | 0 | N/A 72 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | other | 1 | 0 | N/A 72 |
| COL_T | empty | 1 | 72 |  |
| COL_U | empty | 1 | 72 |  |
| GLOBALID | other | 73 | 0 | ca37a96f-cc77-4c5e-8ace-3 1; b3353350-8cbb-46c2-95be-7 1; 227c1240-e1e8-4926-a482-f 1; 35327eb2-34af-423c-8a23-4 1 |
| CREATIONDATE | date | 1 | 0 | 1755810816155 72 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 72 |
| EDITDATE | date | 1 | 0 | 1755810816155 72 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 72 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:31.09897 72 |
| SOURCE_RUN_ID | audit | 1 | 0 | e79d6abe-e3cc-4831-bab8-c 72 |
| SRC_SHA256 | who | 1 | 0 | e94c2ac98e7508bd2e7408fab 72 |
