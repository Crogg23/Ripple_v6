# PORTAL_ARC_LA_COUNTY_OPEN_D_E68DDAB268

rows 167  columns 28  scan 4.3s

roles: amount 1, audit 2, category 11, date 1, empty 1, other 9, who 4

## when

INGESTED_AT
  2026       167  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 167 | 93.59 | 100 | 100 | 100 | 16.7K |

## who

CONAME by rows
         2  BELVEDERE CHILDREN'S CTR
         2  LOS ANGELES UNIFIED SCH DIST
         2  ASCENSION CATHOLIC SCHOOL
         1  ST TURIBIUS SCHOOL
         1  TRINITY STREET SCHOOL
         1  KING DREW MED MAGNET HIGH SCH
         1  CALLYBEAN ACADEMY
         1  UNIFIED SCHOOL INC
         1  RAMONA OPPORTUNITY HIGH SCHOOL
         1  HIGH SCHOOL FOR THE ARTS-LA
         1  ACCELERATED SCHOOL
         1  DOROTHY F KIRBY SCHOOL
         1  ONE HUNDRED SEVENTH STREET
         1  JOHN ADAMS MIDDLE SCHOOL
         1  WEST ATHENS ELEMENTARY SCHOOL
         1  CARVER MIDDLE SCHOOL
         1  TWENTIETH STREET ELEMENTARY
         1  AMANECER PRIMARY CTR
         1  VERBUM DEI HIGH SCHOOL
         1  SEVENTH STREET ELEMENTARY SCHL

CONAME by dollars
         200        2 rows  ASCENSION CATHOLIC SCHOOL
         200        2 rows  BELVEDERE CHILDREN'S CTR
         200        2 rows  LOS ANGELES UNIFIED SCH DIST
         100        1 rows  BANDINI STREET ELEMENTARY SCH
         100        1 rows  99TH STREET ELEMENTARY SCHOOL
         100        1 rows  RAMONA OPPORTUNITY HIGH SCHOOL
         100        1 rows  EAST LOS ANGELES RENAISSANCE
         100        1 rows  YOUTH BUILD CHARTER SCHOOL-CA
         100        1 rows  WADSWORTH AVENUE ELEMENTARY
         100        1 rows  PDL R-CITY TERRACE
         100        1 rows  ROBERT HILL LANE ELEMENTARY
         100        1 rows  ANIMO RALPH BUNCHE CHARTER
         100        1 rows  SEVENTH STREET ELEMENTARY SCHL
         100        1 rows  KIPP IIUMINAR ACADEMY SITE 2
         100        1 rows  ROSEWOOD PARK ELEMENTARY SCH
         100        1 rows  BELEVEDERE MIDDLE SCHOOL
         100        1 rows  KENNEDY ROBERT F ELEMENTARY
         100        1 rows  FIFTEENTH STREET ELEMENTARY
         100        1 rows  WEST ATHENS ELEMENTARY SCHOOL
         100        1 rows  CITY TERRACE ELEMENTARY SCHOOL

STATE_NAME by rows
       167  California

STATE_NAME by dollars
       16.7K      167 rows  California

SOURCE by rows
       167  INFOGROUP

SOURCE by dollars
       16.7K      167 rows  INFOGROUP

SRC_SHA256 by rows
       167  5bef21d94103a5880492e492c1a8a1393b5b76a1b1f86e947f3941a55892adae

SRC_SHA256 by dollars
       16.7K      167 rows  5bef21d94103a5880492e492c1a8a1393b5b76a1b1f86e947f3941a55892

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  99TH STREET ELEMENTARY SCHOOL             2026:100
  ACCELERATED SCHOOL                        2026:100
  AMANECER PRIMARY CTR                      2026:100
  ANIMO RALPH BUNCHE CHARTER                2026:100
  ASCENSION CATHOLIC SCHOOL                 2026:200
  BANDINI STREET ELEMENTARY SCH             2026:100
  BELVEDERE CHILDREN'S CTR                  2026:200
  CALLYBEAN ACADEMY                         2026:100
  CARVER MIDDLE SCHOOL                      2026:100
  DOROTHY F KIRBY SCHOOL                    2026:100
  EAST LOS ANGELES RENAISSANCE              2026:100
  HIGH SCHOOL FOR THE ARTS-LA               2026:100
  JOHN ADAMS MIDDLE SCHOOL                  2026:100
  KING DREW MED MAGNET HIGH SCH             2026:100
  KIPP IIUMINAR ACADEMY SITE 2              2026:100
  LOS ANGELES UNIFIED SCH DIST              2026:200
  ONE HUNDRED SEVENTH STREET                2026:100
  PDL R-CITY TERRACE                        2026:100
  RAMONA OPPORTUNITY HIGH SCHOOL            2026:100
  ROBERT HILL LANE ELEMENTARY               2026:100
  ROSEWOOD PARK ELEMENTARY SCH              2026:100
  SEVENTH STREET ELEMENTARY SCHL            2026:100
  ST TURIBIUS SCHOOL                        2026:100
  TRINITY STREET SCHOOL                     2026:100
  TWENTIETH STREET ELEMENTARY               2026:100
  UNIFIED SCHOOL INC                        2026:100
  VERBUM DEI HIGH SCHOOL                    2026:100
  WADSWORTH AVENUE ELEMENTARY               2026:100
  WEST ATHENS ELEMENTARY SCHOOL             2026:100
  YOUTH BUILD CHARTER SCHOOL-CA             2026:100

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:16.7K

## what

CITY: LOS ANGELES 81%, SAN PEDRO 10%, MONTEREY PARK 3%, MONTEBELLO 2%, COMMERCE 2%, COMPTON 1%

ZIP: 90011 19%, 90063 13%, 90022 13%, 90059 8%, 90061 8%, 90731 8%, 90003 6%, 90023 6%, 90007 6%, 90044 4%, 91754 4%, 90732 4%

NAICS: 61111007 86%, 62441006 14%

SIC: 821103 86%, 835102 14%

SALESVOL: 0 89%, 190 3%, 423 1%, 85 1%, 212 1%, 570 1%, 317 1%, 634 1%, 127 1%, 169 1%, 43 1%, 296 1%

HDBRCH: 2 100%

ULTNUM: 000000000 99%, 597899889 1%

FRNCOD: EKN 48%, NS 14%, JN 7%, 0 6%, S 4%, E 4%, GNS 3%, JNS0 3%, J 3%, EJN 3%, EKN0 3%

ISCODE: C 37%, D 31%, A 17%, B 15%

SQFTCODE: 7 34%, 8 26%, 4 10%, 6 10%, 3 7%, 5 5%, 1 5%, 2 4%

LOC_NAME: PointAddress 74%, StreetAddress 25%, PostalExt 1%, Subaddress 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 167 | 0 | 167 1; 166 1; 165 1; 164 1 |
| LOCNUM | other | 167 | 0 | 977937523 1; 977936129 1; 977935626 1; 977935360 1 |
| CONAME | who | 164 | 0 | BELVEDERE CHILDREN'S CTR 2; LOS ANGELES UNIFIED SCH D 2; ASCENSION CATHOLIC SCHOOL 2; EAST LOS ANGELES COUNTY C 1 |
| STREET | other | 114 | 0 | S MAIN ST 5; AVALON BLVD 5; E 1ST ST 5; S EASTMAN AVE 4 |
| CITY | category | 6 | 0 | LOS ANGELES 136; SAN PEDRO 16; MONTEREY PARK 5; MONTEBELLO 4 |
| STATE | other | 1 | 0 | CA 167 |
| STATE_NAME | who | 1 | 0 | California 167 |
| ZIP | category | 21 | 0 | 90011 27; 90063 19; 90022 19; 90059 12 |
| ZIP4 | other | 148 | 2 | 1929 3; 3422 3; 1220 2; 1022 2 |
| NAICS | category | 2 | 0 | 61111007 144; 62441006 23 |
| SIC | category | 2 | 0 | 821103 144; 835102 23 |
| SALESVOL | category | 18 | 0 | 0 144; 190 5; 423 2; 85 2 |
| HDBRCH | category | 2 | 166 | 2 1 |
| ULTNUM | category | 2 | 0 | 000000000 166; 597899889 1 |
| PUBPRV | empty | 1 | 167 |  |
| EMPNUM | other | 63 | 0 | 9 19; 20 8; 100 7; 50 7 |
| FRNCOD | category | 38 | 35 | EKN 46; NS 13; JN 7; 0 6 |
| ISCODE | category | 5 | 102 | C 24; D 20; A 11; B 10 |
| SQFTCODE | category | 8 | 0 | 7 56; 8 43; 4 17; 6 16 |
| LOC_NAME | category | 4 | 0 | PointAddress 124; StreetAddress 41; PostalExt 1; Subaddress 1 |
| STATUS | other | 1 | 0 | M 167 |
| SCORE | amount | 3 | 0 | 100.0 165; 93.59375 1; 99.515625 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 167 |
| REC_TYPE | other | 1 | 0 | 0 167 |
| GEOMETRY | other | 149 | 0 | {"type": "Point", "coordi 3; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:20:47.05754 167 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7e662d4c-936a-4e48-8b4e-4 167 |
| SRC_SHA256 | who | 1 | 0 | 5bef21d94103a5880492e492c 167 |
