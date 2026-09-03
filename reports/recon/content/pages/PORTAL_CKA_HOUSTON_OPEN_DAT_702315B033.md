# PORTAL_CKA_HOUSTON_OPEN_DAT_702315B033

rows 1.1K  columns 15  scan 2.4s

roles: audit 2, category 5, date 1, id 2, other 3, who 3

## when

INGESTED_AT
  2026      1.1K  ##############################

## who

FULL_STREET_NAME by rows
       232  5825 KELLEY ST
        87  9826 ALDINE WESTFIELD RD
        43  6002 BONESS RD
        10  1005 ST. EMANUEL ST, Apt. 6
         8  1406 HAYS ST
         5  7200 CLAREWOOD DR
         3  6300 HILLCROFT , Apt. 620
         3  8802 PECAN PLACE DR
         3  14815 NEWTON FALLS LN
         3  6105 BEVERLY HILLS ST
         3  6413 SAM HOUSTON PKWY  W
         3  11726 BIRCH MEADOW DR
         3  8002 HARTFORD ST
         3  2323 VOSS RD S
         3  9218 MACMILLAN LN
         3  9212 RASMUS DR
         2  2615 CLEAR RIDGE DR
         2  6822 RIDGEWAY DR
         2  37 LYERLY ST
         2  8989 WESTHEIMER

COMPANY by rows
        70  SUNSET CAB COMPANY
        19  444 TAXI INC.
        17  METRO CAB / AMERICAN EAGLE TOWN CAR
        17  CITY CAB
        10  NATIONAL CAB COMPANY/ FOUR SEASONS CAB, LLC.
         6  YELLOW CAB/UNITED TRANSPORTATION SERVICES
         5  JR'S TAXI
         4  LIXSON EXECUTIVE TOWNCARS/LIXSON TRANSPORTATION COMPANY
         4  SLL TRANSPORTATION/INTEGRITY LIMOUSINE/SLL TRANSPORTATION & CHARTER SE
         4  UNION CAB COMPANY/GREEN CAB 
         3  DISCOUNT CAB COMPANY
         3  GOOD CAB
         3  444 TAXI, INC.
         3  CITY CHARTERS/HOUSTON EXECUTIVE LIMOUSINE/LIMOUSINES OF HOUSTON
         3  BEST CHOICE TOWN CAR
         3  IHOP CAB COMPANY
         3  MOCKINGBIRD CAB/ ALLBRIGHT TOWNCAR 
         2  CTI TRANSPORTATION/CORPORATE CUSTOM COACHES
         2  TAXIS FIESTA/EAGLE EXE TRANSPORTATION 
         2  GENESIS CORPORATE TRANSPORTATION/GENESIS LIVERY SERVICE

SRC_SHA256 by rows
      1.1K  560ecae6a473c8812cc42893c03bdf42caaeae8b6c5250f16e92c904b26efc35

## who x when

FULL_STREET_NAME by INGESTED_AT  LOAD STAMP, not an event date
  1005 ST. EMANUEL ST, Apt. 6               2026:10
  11726 BIRCH MEADOW DR                     2026:3
  1406 HAYS ST                              2026:8
  14815 NEWTON FALLS LN                     2026:3
  2323 VOSS RD S                            2026:3
  2615 CLEAR RIDGE DR                       2026:2
  37 LYERLY ST                              2026:2
  5825 KELLEY ST                            2026:232
  6002 BONESS RD                            2026:43
  6105 BEVERLY HILLS ST                     2026:3
  6300 HILLCROFT , Apt. 620                 2026:3
  6413 SAM HOUSTON PKWY  W                  2026:3
  6822 RIDGEWAY DR                          2026:2
  7200 CLAREWOOD DR                         2026:5
  8002 HARTFORD ST                          2026:3
  8802 PECAN PLACE DR                       2026:3
  8989 WESTHEIMER                           2026:2
  9212 RASMUS DR                            2026:3
  9218 MACMILLAN LN                         2026:3
  9826 ALDINE WESTFIELD RD                  2026:87

COMPANY by INGESTED_AT  LOAD STAMP, not an event date
  444 TAXI INC.                             2026:19
  444 TAXI, INC.                            2026:3
  BEST CHOICE TOWN CAR                      2026:3
  CITY CAB                                  2026:17
  CITY CHARTERS/HOUSTON EXECUTIVE LIMOUSIN  2026:3
  CTI TRANSPORTATION/CORPORATE CUSTOM COAC  2026:2
  DISCOUNT CAB COMPANY                      2026:3
  GENESIS CORPORATE TRANSPORTATION/GENESIS  2026:2
  GOOD CAB                                  2026:3
  IHOP CAB COMPANY                          2026:3
  JR'S TAXI                                 2026:5
  LIXSON EXECUTIVE TOWNCARS/LIXSON TRANSPO  2026:4
  METRO CAB / AMERICAN EAGLE TOWN CAR       2026:17
  MOCKINGBIRD CAB/ ALLBRIGHT TOWNCAR        2026:3
  NATIONAL CAB COMPANY/ FOUR SEASONS CAB,   2026:10
  SLL TRANSPORTATION/INTEGRITY LIMOUSINE/S  2026:4
  SUNSET CAB COMPANY                        2026:70
  TAXIS FIESTA/EAGLE EXE TRANSPORTATION     2026:2
  UNION CAB COMPANY/GREEN CAB               2026:4
  YELLOW CAB/UNITED TRANSPORTATION SERVICE  2026:6

## what

APPLICATION_DESCRIPTION: Taxi 52%, Limo 29%, School Bus 10%, Charter/SS 7%, SGT 1%, Pedicab 0%, Jitney 0%, Low Speed Shuttle 0%

STATUS: Active 65%, ISS 35%

CITY_NAME: Houston 91%, Humble 5%, Sugarland 1%, Pearland  1%, STAFFORD 1%, Katy 1%, League City  1%, The Woodlands 0%, Conroe  0%, MANVEL 0%, Richmond 0%

ACTIVE_VEHICLE_COUNT: 1 59%, 2 11%, 3 8%, 5 5%, 4 5%, 6 4%, 8 2%, 7 2%, 10 1%, 9 1%, 11 1%

ALL_VEHICLE_COUNT: 1 51%, 2 16%, 3 8%, 4 5%, 5 4%, 6 4%, 7 3%, 8 2%, 10 2%, 9 2%, 12 1%, 11 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TRANSPORTATION_ID | id | 1.0K | 0 | 964 6; 5920 6; 2885 6; 2490 6 |
| APPLICATION_DESCRIPTION | category | 8 | 0 | Taxi 553; Limo 310; School Bus 105; Charter/SS 72 |
| DBA_ALIAS | id | 1.0K | 15 | COMPASS TRANSPORTATION CO 6; COMPASS TOWNCAR 6; LONE STAR BIKE CABS 6; READY 2 ROLL 6 |
| COMPANY | who | 569 | 242 | SUNSET CAB COMPANY 70; 444 TAXI INC. 22; CITY CAB 20; METRO CAB / AMERICAN EAGL 17 |
| STATUS | category | 2 | 0 | Active 684; ISS 372 |
| HLL_CSS_NUMBER | other | 459 | 590 | HLL 630 3; SGT 507 3; HLL 708 3; CSS 172 3 |
| FULL_STREET_NAME | who | 529 | 53 | 5825 KELLEY ST 232; 9826 ALDINE WESTFIELD RD 87; 6002 BONESS RD 45; 1005 ST. EMANUEL ST, Apt. 10 |
| CITY_NAME | category | 27 | 54 | Houston 892; Humble 46; Sugarland 13; Pearland  6 |
| ZIPCODE | other | 134 | 53 | 77026 234; 77093 97; 77396 48; 77083 34 |
| ACTIVE_VEHICLE_COUNT | category | 35 | 36 | 1 575; 2 106; 3 82; 5 53 |
| ALL_VEHICLE_COUNT | category | 46 | 0 | 1 500; 2 159; 3 80; 4 48 |
| SHORT_DESC | other | 878 | 0 | SCHOOL BUS 83; CHARTER COMPANY 66; TAXICAB 8; SGT COMPANY 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:49:22.28102 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | a7e82d10-c3df-498c-ae73-a 1.1K |
| SRC_SHA256 | who | 1 | 0 | 560ecae6a473c8812cc42893c 1.1K |
