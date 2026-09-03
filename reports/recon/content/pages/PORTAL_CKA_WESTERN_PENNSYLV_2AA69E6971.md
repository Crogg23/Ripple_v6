# PORTAL_CKA_WESTERN_PENNSYLV_2AA69E6971

rows 253  columns 14  scan 3.5s

roles: audit 2, category 1, date 1, other 7, who 4

## when

INGESTED_AT
  2026       253  ##############################

## who

FACILITY by rows
         2  Pittsburgh Public Works 3rd Division
         2  ACHD-Arsenal Health Center
         1  Churchill Borough Building
         1  McKees Rocks Borough Building
         1  Glassport Borough Building
         1  ACHD-Clack Health Center
         1  ACHD-Carnegie
         1  Marshall Township Building
         1  Municipal Courts Building
         1  Frazer Township Building
         1  DHS-CRO
         1  Crafton Borough Building
         1  Oakdale Borough Building
         1  Aspinwall Borough Building
         1  Buncher Building
         1  Leet Township Building
         1  Kane-McKeesport
         1  Braddock Borough Building
         1  Shuman Juvenile Detention Center
         1  Sewickley Hills Borough Building

FACILITY_C by rows
         1  RCW
         1  B157
         1  DHS-MVO
         1  L-FPC
         1  S&S
         1  B210
         1  DHS-NRO
         1  LEX
         1  DHS-CRO
         1  PW-2
         1  B276
         1  B039
         1  FrB
         1  ACAD
         1  DHS-WSC
         1  CH
         1  B281
         1  COB
         1  B159
         1  ACHD-Sss

CITY by rows
       153  Pittsburgh
         9  Sewickley
         6  McKeesport
         4  Elizabeth
         4  Allison Park
         3  Carnegie
         3  Tarentum
         3  Turtle Creek
         3  Homestead
         2  Wexford
         2  Clairton
         2  West Mifflin
         2  Gibsonia
         2  Coraopolis
         2  Wilmerding
         2  Oakdale
         2  East Pittsburgh
         2  McKees Rocks
         2  Cheswick
         2  Bethel Park

SRC_SHA256 by rows
       253  2cb76159b22f7d689e5945679f2e32805866618ed051af82aca24f54433ca1d8

## who x when

FACILITY by INGESTED_AT  LOAD STAMP, not an event date
  ACHD-Arsenal Health Center                2026:2
  ACHD-Carnegie                             2026:1
  ACHD-Clack Health Center                  2026:1
  Aspinwall Borough Building                2026:1
  Braddock Borough Building                 2026:1
  Buncher Building                          2026:1
  Churchill Borough Building                2026:1
  Crafton Borough Building                  2026:1
  DHS-CRO                                   2026:1
  Frazer Township Building                  2026:1
  Glassport Borough Building                2026:1
  Kane-McKeesport                           2026:1
  Leet Township Building                    2026:1
  Marshall Township Building                2026:1
  McKees Rocks Borough Building             2026:1
  Municipal Courts Building                 2026:1
  Oakdale Borough Building                  2026:1
  Pittsburgh Public Works 3rd Division      2026:2
  Sewickley Hills Borough Building          2026:1
  Shuman Juvenile Detention Center          2026:1

FACILITY_C by INGESTED_AT  LOAD STAMP, not an event date
  ACAD                                      2026:1
  ACHD-Sss                                  2026:1
  B039                                      2026:1
  B157                                      2026:1
  B159                                      2026:1
  B210                                      2026:1
  B276                                      2026:1
  B281                                      2026:1
  CH                                        2026:1
  COB                                       2026:1
  DHS-CRO                                   2026:1
  DHS-MVO                                   2026:1
  DHS-NRO                                   2026:1
  DHS-WSC                                   2026:1
  FrB                                       2026:1
  L-FPC                                     2026:1
  LEX                                       2026:1
  PW-2                                      2026:1
  RCW                                       2026:1
  S&S                                       2026:1

## what

CLASS: Allegheny County 43%, City of Pittsburgh 40%, Pittsburgh Public Works 14%, State 1%, Pittsburgh Environmental 1%, PIttsburgh Parks 1%, Pittsburgh Parks 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ADDRESS | other | 242 | 1 | 601 Thorn St 3; 10 29 1/2 St 3; Service Rd 3; Orangewood Ave 2 |
| CITY | who | 63 | 0 | Pittsburgh 153; Sewickley 9; McKeesport 6; Elizabeth 4 |
| CLASS | category | 8 | 130 | Allegheny County 53; City of Pittsburgh 49; Pittsburgh Public Works 17; State 1 |
| FACILITY | who | 252 | 0 | Vanucci Storage Building 2; General Services Motorpoo 2; City County Building 2; Asphalt Plant 2 |
| FACILITY_C | who | 103 | 152 | B314 1; B538 1; CCB 1; BB 1 |
| FID | other | 252 | 0 | 253 2; 252 2; 251 2; 250 2 |
| MUNICODE | other | 132 | 53 | 100 71; 917 1; 854 1; 859 1 |
| PERIMETER | other | 1 | 0 | 0 253 |
| PUBLICBL_I | other | 143 | 0 | 5 5; 3 4; 12 4; 4 4 |
| ZIPCODE | other | 91 | 0 | 15219 18; 15222 16; 15217 11; 15206 9 |
| GEOMETRY | other | 247 | 0 | POINT (569414.97160632605 3; POINT (588323.12743985909 3; POINT (583301.38031409296 2; POINT (585088.76753676892 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:37:52.86584 253 |
| SOURCE_RUN_ID | audit | 1 | 0 | f9daa940-8110-4c4a-9803-c 253 |
| SRC_SHA256 | who | 1 | 0 | 2cb76159b22f7d689e5945679 253 |
