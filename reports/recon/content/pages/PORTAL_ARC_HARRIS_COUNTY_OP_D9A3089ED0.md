# PORTAL_ARC_HARRIS_COUNTY_OP_D9A3089ED0

rows 125  columns 47  scan 4.2s

roles: amount 5, audit 2, category 21, date 4, empty 5, other 8, who 3

## when

VAL_DATE
  2021        94  ##############################
  2022         6  ##

CREATIONDATE
  2026       125  ##############################

EDITDATE
  2026       125  ##############################

INGESTED_AT
  2026       125  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POPULATION | 123 | -999 | 15 | 199.12 | 202 | -17.2K |
| LATITUDE | 124 | 29.50 | 29.68 | 29.93 | 29.93 | 3.7K |
| LONGITUDE | 124 | -95.49 | -95.18 | -94.92 | -94.92 | -11.8K |
| TOT_RES | 123 | -999 | 15 | 199.12 | 202 | -17.2K |
| BEDS | 123 | -999 | 30 | 200 | 202 | 6.7K |

## who

NAME by rows
         2  THE PINE TREE OF PASADENA LLC
         2  SERENITY GARDENS
         2  EFE ASSISTED LIVING CENTER INC
         2  THE COTTAGES AT CLEAR LAKE I I
         2  MRC THE CROSSINGS
         2  GENOA ASSISTED LIVING
         1  LOVING IN CARING ARMS
         1  FOCUSED CARE AT BAYTOWN
         1  FOCUSED CARE AT PASADENA
         1  LIGHT HEART MEMORY CARE  PASADENA
         1  SWAN MANOR ALF
         1  GRACEFULLY FOUND CARE HOME
         1  SYLVAN SHORES HEALTH AND WELLNESS
         1  BRIGHTWAY PERSONAL CARE
         1  BROOKDALE PEARLAND
         1  SWEET HOME
         1  MEMORY CARE SUITES
         1  ASHFORD GARDENS
         1  BAY RIDGE HEALTHCARE CENTER
         1  THE SUITES PASADENA

NAME by dollars
       59.36        2 rows  THE PINE TREE OF PASADENA LLC
       59.28        2 rows  EFE ASSISTED LIVING CENTER INC
       59.24        2 rows  GENOA ASSISTED LIVING
       59.20        2 rows  SERENITY GARDENS
       59.04        2 rows  MRC THE CROSSINGS
          59        2 rows  THE COTTAGES AT CLEAR LAKE I I
       29.93        1 rows  BRIGHTWAY PERSONAL CARE
       29.93        1 rows  CANYON RIDGE PERSONAL CARE HOME LLC
       29.93        1 rows  BRIGHT STAR HEALTH NETWORK MANAGEMENT SERVICES INC
       29.92        1 rows  BRIGHTWAY PERSONAL CARE I I
       29.92        1 rows  AVIR AT VETERANS MEMORIAL
       29.91        1 rows  LOVING IN CARING ARMS
       29.88        1 rows  HOUSE OF HEARTS ASSISTED LIVING, LLC
       29.87        1 rows  ASHFORD GARDENS
       29.87        1 rows  K AND R AMAZING PERSONAL CARE HOME INCORPORATED
       29.87        1 rows  MINGO PERSONAL HOME
       29.87        1 rows  MINGO'S PERSONAL CARE HOME INC
       29.86        1 rows  NIXON ASSISTED LIVING TOO
       29.86        1 rows  CARADAY OF HOUSTON
       29.86        1 rows  SUBJECTIVE HOME CARE

CREATOR by rows
       125  JGuerraPct2

CREATOR by dollars
        3.7K      125 rows  JGuerraPct2

SRC_SHA256 by rows
       125  19c375e9795d5b60c570aba6a22a579b47b6d19406858973fc72f33c29eb7456

SRC_SHA256 by dollars
        3.7K      125 rows  19c375e9795d5b60c570aba6a22a579b47b6d19406858973fc72f33c29eb

## who x when

NAME by VAL_DATE, dollars = LATITUDE
  ASHFORD GARDENS                           2021:29.87
  AVIR AT VETERANS MEMORIAL                 2021:29.92
  BAY RIDGE HEALTHCARE CENTER               2021:29.67
  BRIGHT STAR HEALTH NETWORK MANAGEMENT SE  2021:29.93
  BRIGHTWAY PERSONAL CARE                   2021:29.93
  BRIGHTWAY PERSONAL CARE I I               2021:29.92
  BROOKDALE PEARLAND                        2021:29.57
  CANYON RIDGE PERSONAL CARE HOME LLC       2021:29.93
  EFE ASSISTED LIVING CENTER INC            2021:59.28
  FOCUSED CARE AT BAYTOWN                   2021:29.75
  FOCUSED CARE AT PASADENA                  2021:29.66
  GENOA ASSISTED LIVING                     2021:29.62
  GRACEFULLY FOUND CARE HOME                2022:29.69
  HOUSE OF HEARTS ASSISTED LIVING, LLC      2021:29.88
  LOVING IN CARING ARMS                     2021:29.91
  MINGO'S PERSONAL CARE HOME INC            2021:29.87
  MRC THE CROSSINGS                         2021:59.04
  NIXON ASSISTED LIVING TOO                 2021:29.86
  SERENITY GARDENS                          2021:29.53 2022:29.67
  SWAN MANOR ALF                            2021:29.74
  SWEET HOME                                2021:29.78
  SYLVAN SHORES HEALTH AND WELLNESS         2021:29.65
  THE COTTAGES AT CLEAR LAKE I I            2021:29.50
  THE PINE TREE OF PASADENA LLC             2021:59.36
  THE SUITES PASADENA                       2021:29.64

CREATOR by VAL_DATE, dollars = LATITUDE
  JGuerraPct2                               2021:2.8K 2022:178.15

## what

CITY: HOUSTON 47%, PASADENA 12%, BAYTOWN 10%, LEAGUE CITY 9%, FRIENDSWOOD 7%, WEBSTER 4%, LA PORTE 3%, PEARLAND 3%, HIGHLANDS 2%, DEER PARK 2%, CLEAR LAKE 1%, EL LAGO 1%

ZIP: 77573 15%, 77016 12%, 77546 12%, 77521 11%, 77598 7%, 77503 7%, 77504 7%, 77089 7%, 77062 7%, 77520 5%, 77571 5%, 77505 5%

ZIP4: NOT AVAILABLE 94%, nan 2%, 1010 1%, 3765 1%, 6060 1%, 2920 1%, 3236 1%

TYPE: ASSISTED LIVING 70%, NURSING HOME 30%

STATUS: OPEN 97%, CLOSED 3%

COUNTY: HARRIS 85%, GALVESTON 13%, BRAZORIA 2%, nan 1%

COUNTYFIPS: 48201 86%, 48167 13%, 48039 2%

COUNTRY: USA 82%, US 18%

NAICS_CODE: 623312 69%, 623110 30%, nan 2%

NAICS_DESC: ASSISTED LIVING FACILITIES FOR 70%, NURSING CARE FACILITIES (SKILL 30%, nan 1%

SOURCE: https://hhs.texas.gov/doing-bu 75%, https://www.hhs.texas.gov/prov 17%, https://apps.hhs.texas.gov/pro 3%, nan 2%, https://www.hhs.texas.gov/prov 2%, https://apps.hhs.texas.gov/pro 2%

SOURCEDATE: 4/10/2021 92%, 2/7/2022 6%, nan 2%

VAL_METHOD: IMAGERY/OTHER 78%, GEOCODE 18%, UNVERIFIED 2%, nan 2%

WEBSITE: NOT AVAILABLE 97%, nan 2%, https://www.mrcthecrossings.or 2%

TOT_STAFF: -999.0 98%, nan 2%

EXCESS_BED: -999.0 98%, nan 2%

OWNERSHIP: LIMITED LIABILITY COMPANY (LLC 29%, NOT AVAILABLE 22%, FOR-PROFIT CORPORATION 14%, LIMITED PARTNERSHIP 8%, NONPROFIT ORGANIZATION 6%, HOSPITAL DISTRICT/AUTHORITY 6%, SOLE PROPRIETOR 6%, LIMITED LIABILITY COMPANY 5%, SOLE PROPRIETORSHIP 2%, nan 1%, WJ HEALTHCARE LLC 1%, GENERAL PARTNERSHIP 1%

MEDICAIDID: NOT AVAILABLE 98%, nan 2%

MEDICAREID: NOT AVAILABLE 98%, nan 2%

SOURCETYPE: ASSISTED LIVING 52%, NURSING 26%, Point 18%, nan 2%, NURSING HOME 2%

EDITOR: JGuerraPct2 88%, camerondavis1 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | other | 125 | 0 | 127 1; 126 1; 125 1; 124 1 |
| ID | other | 127 | 0 | nan 1; 111658 1; 481431 1; 481549 1 |
| NAME | who | 116 | 0 | THE PINE TREE OF PASADENA 2; SERENITY GARDENS 2; EFE ASSISTED LIVING CENTE 2; GENOA ASSISTED LIVING 2 |
| ADDRESS | other | 114 | 0 | 15403 HOPE VILLAGE RD 4; 450 LANDING BLVD 3; 10222 ALLWOOD ST 2; 2711 MCDANIEL 2 |
| CITY | category | 12 | 0 | HOUSTON 59; PASADENA 15; BAYTOWN 12; LEAGUE CITY 11 |
| STATE | other | 1 | 0 | TX 125 |
| ZIP | category | 40 | 0 | 77573 11; 77016 9; 77546 9; 77521 8 |
| ZIP4 | category | 7 | 0 | NOT AVAILABLE 118; nan 2; 1010 1; 3765 1 |
| TELEPHONE | other | 101 | 0 | NOT AVAILABLE 7; (281) 282-0770 4; (281) 482-7926 4; (281) 316-4281 4 |
| TYPE | category | 2 | 0 | ASSISTED LIVING 88; NURSING HOME 37 |
| STATUS | category | 2 | 0 | OPEN 121; CLOSED 4 |
| POPULATION | amount | 49 | 0 | -999.0 24; 9.0 14; 120.0 12; 8.0 6 |
| COUNTY | category | 4 | 0 | HARRIS 106; GALVESTON 16; BRAZORIA 2; nan 1 |
| COUNTYFIPS | category | 3 | 0 | 48201 107; 48167 16; 48039 2 |
| COUNTRY | category | 2 | 0 | USA 102; US 23 |
| LATITUDE | amount | 127 | 0 | nan 1; 29.534545 1; 29.932134973000075 1; 29.93210343800007 1 |
| LONGITUDE | amount | 126 | 0 | nan 1; -95.117973 1; -95.48679707799994 1; -95.48256682099998 1 |
| NAICS_CODE | category | 3 | 0 | 623312 86; 623110 37; nan 2 |
| NAICS_DESC | category | 3 | 0 | ASSISTED LIVING FACILITIE 87; NURSING CARE FACILITIES ( 37; nan 1 |
| SOURCE | category | 6 | 0 | https://hhs.texas.gov/doi 94; https://www.hhs.texas.gov 21; https://apps.hhs.texas.go 4; nan 2 |
| SOURCEDATE | category | 4 | 23 | 4/10/2021 94; 2/7/2022 6; nan 2 |
| VAL_METHOD | category | 4 | 0 | IMAGERY/OTHER 97; GEOCODE 23; UNVERIFIED 3; nan 2 |
| VAL_DATE | date | 6 | 23 | 4/10/2021 83; 4/19/2021 7; 2/7/2022 6; 4/20/2021 4 |
| WEBSITE | category | 3 | 0 | NOT AVAILABLE 121; nan 2; https://www.mrcthecrossin 2 |
| TOT_RES | amount | 49 | 0 | -999.0 24; 9.0 14; 120.0 12; 8.0 6 |
| TOT_STAFF | category | 2 | 0 | -999.0 123; nan 2 |
| BEDS | amount | 52 | 0 | 9.0 17; 120.0 13; 8.0 11; 16.0 9 |
| EXCESS_BED | category | 2 | 0 | -999.0 123; nan 2 |
| OWNERSHIP | category | 12 | 0 | LIMITED LIABILITY COMPANY 36; NOT AVAILABLE 27; FOR-PROFIT CORPORATION 18; LIMITED PARTNERSHIP 10 |
| MEDICAIDID | category | 2 | 0 | NOT AVAILABLE 123; nan 2 |
| MEDICAREID | category | 2 | 0 | NOT AVAILABLE 123; nan 2 |
| STATE_LIC | other | 96 | 0 | NOT AVAILABLE 29; nan 2; 148116 1; 145343 1 |
| SOURCETYPE | category | 5 | 0 | ASSISTED LIVING 65; NURSING 33; Point 23; nan 2 |
| GENERATOR_ONSITE | empty | 1 | 125 |  |
| SELF_SUFFICIENT_ELECTRICITY | empty | 1 | 125 |  |
| IN_100_YR_FLOODPLAIN | empty | 1 | 125 |  |
| IN_500_YR_FLOODPLAIN | empty | 1 | 125 |  |
| IN_SURGE_SLOSH_AREA | empty | 1 | 125 |  |
| GLOBALID | other | 125 | 0 | 933884c3-9888-4a78-b397-b 1; 8b300701-57e4-40b9-b9a5-2 1; 2d35ce85-8c26-4acb-800e-5 1; d3a7f7e2-d052-4055-9a43-5 1 |
| CREATIONDATE | date | 1 | 0 | 1768918780879 125 |
| CREATOR | who | 1 | 0 | JGuerraPct2 125 |
| EDITDATE | date | 16 | 0 | 1768918780879 110; 1773677766869 1; 1773677472934 1; 1773673873220 1 |
| EDITOR | category | 2 | 0 | JGuerraPct2 110; camerondavis1 15 |
| GEOMETRY | other | 127 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:19:56.55912 125 |
| SOURCE_RUN_ID | audit | 1 | 0 | 983c497a-6592-4d0f-a073-1 125 |
| SRC_SHA256 | who | 1 | 0 | 19c375e9795d5b60c570aba6a 125 |
