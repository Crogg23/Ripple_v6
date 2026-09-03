# PORTAL_CKA_WPRDC_ALLEGHENY_8DDE33B4BE

rows 253  columns 14  scan 3.7s

roles: audit 2, category 1, date 1, other 7, who 4

## when

INGESTED_AT
  2026       253  ##############################

## who

FACILITY by rows
         2  ACHD-Arsenal Health Center
         2  Pittsburgh Public Works 3rd Division
         1  Nova House
         1  Thornburg Borough Building
         1  Stowe Township Building
         1  Castle Shannon Borough Building
         1  Manchester Storage Building
         1  South Park Township Building
         1  Bradford Woods Borough Building
         1  West Elizabeth Borough Building
         1  Edgeworth Borough Building
         1  North Fayette Township Building
         1  Oakdale Borough Building
         1  PW - Dx 2
         1  DHS @ Smithfield
         1  Liberty Borough Building
         1  West Deer Township Building
         1  Allegheny County Jail
         1  Leetsdale Borough
         1  West Mifflin Borough Building

FACILITY_C by rows
         1  B204
         1  CH
         1  ACHD
         1  K-R
         1  B149
         1  NOVA
         1  B220
         1  B007
         1  B276
         1  CCB
         1  B318
         1  B104
         1  B004
         1  WRC
         1  K-Mc
         1  ACHD-NH
         1  B267
         1  B314
         1  ACHD-Ars
         1  B157

CITY by rows
       153  Pittsburgh
         9  Sewickley
         6  McKeesport
         4  Elizabeth
         4  Allison Park
         3  Turtle Creek
         3  Tarentum
         3  Carnegie
         3  Homestead
         2  Wilmerding
         2  Oakdale
         2  Wexford
         2  West Mifflin
         2  Gibsonia
         2  Clairton
         2  Cheswick
         2  Bethel Park
         2  Coraopolis
         2  East Pittsburgh
         2  McKees Rocks

SRC_SHA256 by rows
       253  2cb76159b22f7d689e5945679f2e32805866618ed051af82aca24f54433ca1d8

## who x when

FACILITY by INGESTED_AT  LOAD STAMP, not an event date
  ACHD-Arsenal Health Center                2026:2
  Allegheny County Jail                     2026:1
  Bradford Woods Borough Building           2026:1
  Castle Shannon Borough Building           2026:1
  DHS @ Smithfield                          2026:1
  Edgeworth Borough Building                2026:1
  Leetsdale Borough                         2026:1
  Liberty Borough Building                  2026:1
  Manchester Storage Building               2026:1
  North Fayette Township Building           2026:1
  Nova House                                2026:1
  Oakdale Borough Building                  2026:1
  PW - Dx 2                                 2026:1
  Pittsburgh Public Works 3rd Division      2026:2
  South Park Township Building              2026:1
  Stowe Township Building                   2026:1
  Thornburg Borough Building                2026:1
  West Deer Township Building               2026:1
  West Elizabeth Borough Building           2026:1
  West Mifflin Borough Building             2026:1

FACILITY_C by INGESTED_AT  LOAD STAMP, not an event date
  ACHD                                      2026:1
  ACHD-Ars                                  2026:1
  ACHD-NH                                   2026:1
  B004                                      2026:1
  B007                                      2026:1
  B104                                      2026:1
  B149                                      2026:1
  B157                                      2026:1
  B204                                      2026:1
  B220                                      2026:1
  B267                                      2026:1
  B276                                      2026:1
  B314                                      2026:1
  B318                                      2026:1
  CCB                                       2026:1
  CH                                        2026:1
  K-Mc                                      2026:1
  K-R                                       2026:1
  NOVA                                      2026:1
  WRC                                       2026:1

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
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:37:46.28164 253 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1fd86917-ec47-4fae-bee7-c 253 |
| SRC_SHA256 | who | 1 | 0 | 2cb76159b22f7d689e5945679 253 |
