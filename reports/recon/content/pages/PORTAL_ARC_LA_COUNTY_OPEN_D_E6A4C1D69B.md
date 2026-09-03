# PORTAL_ARC_LA_COUNTY_OPEN_D_E6A4C1D69B

rows 2.0K  columns 28  scan 5.2s

roles: amount 1, audit 2, category 7, date 1, id 3, other 6, who 9

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 2.0K | 85 | 100 | 100 | 100 | 199.9K |

## who

CONAME by rows
         9  CVS/PHARMACY
         6  7-ELEVEN
         5  MERRILL LYNCH WEALTH MGMT
         5  MACY'S
         5  PEP BOYS
         5  U.S. BANK BRANCH
         4  FIRESTONE COMPLETE AUTO CARE
         4  MOTEL 6
         4  MC DONALD'S
         4  DEL TACO
         3  STATER BROS MARKETS
         3  RALPHS
         2  HIRSCH PIPE & SUPPLY CO
         2  CHASE
         2  PAUL HASTINGS LLP
         2  CALIFORNIA WATER SVC CO
         2  DENNY'S
         2  O'MELVENY & MYERS LLP
         2  HARRINGTON INDUSTRIAL PLASTICS
         2  AMERICAN TIRE DEPOT

CONAME by dollars
         900        9 rows  CVS/PHARMACY
         600        6 rows  7-ELEVEN
         500        5 rows  MERRILL LYNCH WEALTH MGMT
         500        5 rows  PEP BOYS
         500        5 rows  U.S. BANK BRANCH
      428.52        5 rows  MACY'S
         400        4 rows  DEL TACO
         400        4 rows  MC DONALD'S
         400        4 rows  FIRESTONE COMPLETE AUTO CARE
         400        4 rows  MOTEL 6
         300        3 rows  RALPHS
         300        3 rows  STATER BROS MARKETS
         200        2 rows  UNITED RENTALS
         200        2 rows  PEPSI BEVERAGES CO
         200        2 rows  UNION BANK
         200        2 rows  ALBERTSONS
         200        2 rows  HOLIDAY INN
         200        2 rows  ROUND TABLE PIZZA
         200        2 rows  GIBSON DUNN & CRUTCHER LLP
         200        2 rows  GOODWILL

STATE_NAME by rows
      2.0K  California

STATE_NAME by dollars
      199.9K     2.0K rows  California

NAICS by rows
        60  72251117
        58  72111002
        53  62311016
        36  81111104
        34  53111002
        33  62211002
        31  33271002
        25  54111002
        21  52211002
        21  62311002
        21  44111001
        20  72251301
        19  33641301
        17  44511003
        17  53121003
        17  62331206
        16  81211202
        15  62331101
        15  81232002
        14  44611009

NAICS by dollars
        6.0K       60 rows  72251117
        5.8K       58 rows  72111002
        5.3K       53 rows  62311016
        3.6K       36 rows  81111104
        3.4K       34 rows  53111002
        3.3K       33 rows  62211002
        3.1K       31 rows  33271002
        2.5K       25 rows  54111002
        2.1K       21 rows  44111001
        2.1K       21 rows  62311002
        2.1K       21 rows  52211002
        2.0K       20 rows  72251301
        1.9K       19 rows  33641301
        1.7K       17 rows  62331206
        1.7K       17 rows  44511003
        1.7K       17 rows  53121003
        1.6K       16 rows  81211202
        1.5K       15 rows  62331101
        1.5K       15 rows  81232002
        1.4K       14 rows  44531004

SIC by rows
        75  581208
        58  701101
        53  805101
        36  753801
        34  651303
        33  806202
        31  359903
        25  811103
        21  602101
        21  805902
        21  551102
        19  372801
        17  541105
        17  653118
        17  836105
        16  723106
        15  721201
        15  805904
        14  591205
        14  592102

SIC by dollars
        7.5K       75 rows  581208
        5.8K       58 rows  701101
        5.3K       53 rows  805101
        3.6K       36 rows  753801
        3.4K       34 rows  651303
        3.3K       33 rows  806202
        3.1K       31 rows  359903
        2.5K       25 rows  811103
        2.1K       21 rows  551102
        2.1K       21 rows  805902
        2.1K       21 rows  602101
        1.9K       19 rows  372801
        1.7K       17 rows  836105
        1.7K       17 rows  653118
        1.7K       17 rows  541105
        1.6K       16 rows  723106
        1.5K       15 rows  805904
        1.5K       15 rows  721201
        1.4K       14 rows  591205
        1.4K       14 rows  592102

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  7-ELEVEN                                  2026:600
  ALBERTSONS                                2026:200
  AMERICAN TIRE DEPOT                       2026:200
  CALIFORNIA WATER SVC CO                   2026:200
  CHASE                                     2026:200
  CVS/PHARMACY                              2026:900
  DEL TACO                                  2026:400
  DENNY'S                                   2026:200
  FIRESTONE COMPLETE AUTO CARE              2026:400
  GIBSON DUNN & CRUTCHER LLP                2026:200
  GOODWILL                                  2026:200
  HARRINGTON INDUSTRIAL PLASTICS            2026:200
  HIRSCH PIPE & SUPPLY CO                   2026:200
  HOLIDAY INN                               2026:200
  MACY'S                                    2026:428.52
  MC DONALD'S                               2026:400
  MERRILL LYNCH WEALTH MGMT                 2026:500
  MOTEL 6                                   2026:400
  O'MELVENY & MYERS LLP                     2026:200
  PAUL HASTINGS LLP                         2026:200
  PEP BOYS                                  2026:500
  PEPSI BEVERAGES CO                        2026:200
  RALPHS                                    2026:300
  ROUND TABLE PIZZA                         2026:200
  STATER BROS MARKETS                       2026:300
  U.S. BANK BRANCH                          2026:500
  UNION BANK                                2026:200
  UNITED RENTALS                            2026:200

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:199.9K

## what

HDBRCH: 2 65%, 3 21%, 1 14%

PUBPRV: 2 92%, 1 8%

ISCODE: C 23%, D 16%, B 12%, 3 10%, E 10%, F 8%, V 6%, e 4%, M 4%, I 3%, 5 2%

SQFTCODE: 8 27%, 7 17%, 6 12%, 3 11%, 2 9%, 1 9%, 4 8%, 5 7%

LOC_NAME: PointAddress 75%, Subaddress 16%, StreetAddress 8%, Postal 0%, PostalExt 0%, StreetName 0%

STATUS: M 99%, T 1%

REC_TYPE: 0 100%, 1 0%, 2 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| LOCNUM | id | 2.0K | 0 | 100125731 10; 100125608 10; 100125582 10; 100125293 10 |
| CONAME | who | 1.9K | 0 | 7-ELEVEN 12; UNION BANK 11; RALPHS 11; TICKET MANIA 10 |
| STREET | who | 1.1K | 3 | HARBOR BLVD 45; E COAST HWY 37; NEWPORT BLVD 33; E 17TH ST 28 |
| CITY | who | 156 | 0 | COSTA MESA 340; LOS ANGELES 180; FULLERTON 94; BREA 89 |
| STATE | other | 1 | 0 | CA 2.0K |
| STATE_NAME | who | 1 | 0 | California 2.0K |
| ZIP | other | 314 | 0 | 92627 209; 92626 130; 92821 87; 92831 74 |
| ZIP4 | other | 1.5K | 17 | 4609 12; 2307 12; 3627 12; 2907 12 |
| NAICS | who | 785 | 0 | 72251117 60; 72111002 58; 62311016 55; 53111002 37 |
| SIC | who | 769 | 0 | 581208 75; 701101 58; 805101 55; 651303 37 |
| SALESVOL | other | 1.3K | 0 | 0 319; 171 21; 483 16; 559 13 |
| HDBRCH | category | 4 | 1.4K | 2 389; 3 127; 1 84 |
| ULTNUM | who | 402 | 0 | 000000000 1.4K; 400857322 12; 488940388 12; 811308949 11 |
| PUBPRV | category | 3 | 1.7K | 2 244; 1 20 |
| EMPNUM | other | 187 | 0 | 2 107; 3 94; 1 91; 100 79 |
| FRNCOD | other | 102 | 1.7K | M 22; K 16; P 14; EFH 12 |
| ISCODE | category | 25 | 1.8K | C 46; D 33; B 23; 3 21 |
| SQFTCODE | category | 8 | 0 | 8 548; 7 339; 6 233; 3 229 |
| LOC_NAME | category | 6 | 0 | PointAddress 1.5K; Subaddress 318; StreetAddress 160; Postal 7 |
| STATUS | category | 2 | 0 | M 2.0K; T 23 |
| SCORE | amount | 14 | 0 | 100.0 2.0K; 99.890625 15; 85.0 4; 98.0 3 |
| SOURCE | who | 1 | 0 | Data Axle 2.0K |
| REC_TYPE | category | 3 | 0 | 0 2.0K; 1 3; 2 3 |
| GEOMETRY | id | 1.9K | 0 | {"type": "Point", "coordi 11; {"type": "Point", "coordi 11; {"type": "Point", "coordi 11; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:37:00.83552 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 07446fe3-39e6-4872-8cf0-8 2.0K |
| SRC_SHA256 | who | 1 | 0 | 5110b9a2af4df87ad1f494f73 2.0K |
