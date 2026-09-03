# PORTAL_CKA_ANALYZE_BOSTON_0CED34C7C1

rows 13  columns 17  scan 3.6s

roles: amount 4, audit 2, category 9, date 1, who 2

## when

INGESTED_AT
  2026        13  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 13 | -71.15 | -71.09 | -71.03 | -71.03 | -924.12 |
| POINT_Y | 13 | 42.26 | 42.33 | 42.38 | 42.38 | 550.25 |
| FT_SQFT | 11 | 6.9K | 8.7K | 176.1K | 194.0K | 291.0K |
| STORY_HT | 12 | 1.50 | 2 | 4.89 | 5 | 31.50 |

## who

CITY by rows
        13  Boston

CITY by dollars
     -924.12       13 rows  Boston

SRC_SHA256 by rows
        13  d2984d08b14fe7788845e3eadbd0bb856bfe4ba88a7a62dcc909aad5ac1b6c5f

SRC_SHA256 by dollars
     -924.12       13 rows  d2984d08b14fe7788845e3eadbd0bb856bfe4ba88a7a62dcc909aad5ac1b

## who x when

CITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  Boston                                    2026:-924.12

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  d2984d08b14fe7788845e3eadbd0bb856bfe4ba8  2026:-924.12

## what

BLDG_ID: Bos_1600673000_B0 8%, Bos_1404623000_B0 8%, Bos_1102261000_B0 8%, Bos_1201261000_B0 8%, Bos_0902771010_B0 8%, Bos_0801170010_B0 8%, Bos_0600118000_B0 8%, Bos_0202644020_B0 8%, Bos_2202387000_B0 8%, Bos_0302626000_B0 8%, Bos_0103711003_B0 8%, Bos_2005719000_B0 8%

BID: 189445 8%, 186089 8%, 180965 8%, 176508 8%, 163892 8%, 162100 8%, 154919 8%, 148316 8%, 145004 8%, 136171 8%, 222774 8%, 112112 8%

ADDRESS: 40 Gibson St 8%, 1165 Blue Hill Ave 8%, 3345 Washington St 8%, 2400 Washington St 8%, 1 Schroeder Plz 8%, 650 Harrison Ave 8%, 101 W Broadway 8%, 20 Vine St 8%, 301 Washington St 8%, 40 Sudbury St 8%, 300 E Eagle St 8%, 1708 Centre St 8%

NAME: District C-11 Police Station 8%, District B-3 Police Station 8%, District E-13 Police Station 8%, District B-2 Police Station 8%, Boston Police Headquarters 8%, District D-4 Police Station 8%, District C-6 Police Station 8%, District A-15 Police Station 8%, District D-14 Police Station 8%, District A-1 Police Station 8%, District A-7 Police Station 8%, District E-5 Police Station 8%

NEIGHBORHOOD: Roxbury 15%, Boston 15%, Dorchester 8%, Mattapan 8%, Jamaica Plain 8%, South Boston 8%, Charlestown 8%, Brighton 8%, East Boston 8%, West Roxbury 8%, Hyde Park 8%

ZIP: 02122 8%, 02124 8%, 02130 8%, 02119 8%, 02120 8%, 02118 8%, 02127 8%, 02129 8%, 02135 8%, 02114 8%, 02128 8%, 02132 8%

PARCEL_ID: 1600673000 8%, 1404623000 8%, 1102261000 8%, 1201261000 8%, 0902771010 8%, 0801170010 8%, 0600118000 8%, 0202644020 8%, 2202387000 8%, 0302626000 8%, 0103711003 8%, 2005719000 8%

DISTRICT: C11 9%, B3 9%, E13 9%, B2 9%, D4 9%, C6 9%, A15 9%, D14 9%, A1 9%, A7 9%, E5 9%

SHAPE_WKT: POINT (-71.059164332999956 42. 8%, POINT (-71.091701393999983 42. 8%, POINT (-71.104638613999953 42. 8%, POINT (-71.085683750999976 42. 8%, POINT (-71.090746919999958 42. 8%, POINT (-71.069239163999953 42. 8%, POINT (-71.054935696999962 42. 8%, POINT (-71.056046539999954 42. 8%, POINT (-71.15057769799995 42.3 8%, POINT (-71.060306675999982 42. 8%, POINT (-71.028134977999969 42. 8%, POINT (-71.148367137999969 42. 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BLDG_ID | category | 13 | 0 | Bos_1600673000_B0 1; Bos_1404623000_B0 1; Bos_1102261000_B0 1; Bos_1201261000_B0 1 |
| BID | category | 13 | 0 | 189445 1; 186089 1; 180965 1; 176508 1 |
| ADDRESS | category | 13 | 0 | 40 Gibson St 1; 1165 Blue Hill Ave 1; 3345 Washington St 1; 2400 Washington St 1 |
| POINT_X | amount | 13 | 0 | -71.059164332999956 1; -71.091701393999983 1; -71.104638613999953 1; -71.085683750999976 1 |
| POINT_Y | amount | 13 | 0 | 42.298056843000040 1; 42.284720271000026 1; 42.309713783000063 1; 42.328376723000076 1 |
| NAME | category | 13 | 0 | District C-11 Police Stat 1; District B-3 Police Stati 1; District E-13 Police Stat 1; District B-2 Police Stati 1 |
| NEIGHBORHOOD | category | 11 | 0 | Roxbury 2; Boston 2; Dorchester 1; Mattapan 1 |
| CITY | who | 1 | 0 | Boston 13 |
| ZIP | category | 13 | 0 | 02122 1; 02124 1; 02130 1; 02119 1 |
| FT_SQFT | amount | 12 | 2 | 15338.000000000000000 1; 9740.000000000000000 1; 8312.000000000000000 1; 10809.000000000000000 1 |
| STORY_HT | amount | 6 | 1 | 2.000000000000000 6; 3.000000000000000 3; 1.500000000000000 1; 4.000000000000000 1 |
| PARCEL_ID | category | 13 | 0 | 1600673000 1; 1404623000 1; 1102261000 1; 1201261000 1 |
| DISTRICT | category | 13 | 1 | C11 1; B3 1; E13 1; B2 1 |
| SHAPE_WKT | category | 13 | 0 | POINT (-71.05916433299995 1; POINT (-71.09170139399998 1; POINT (-71.10463861399995 1; POINT (-71.08568375099997 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:14:30.88369 13 |
| SOURCE_RUN_ID | audit | 1 | 0 | 88123d47-fc0e-4c17-afe0-a 13 |
| SRC_SHA256 | who | 1 | 0 | d2984d08b14fe7788845e3ead 13 |
