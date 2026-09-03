# PORTAL_CKA_WPRDC_ALLEGHENY_FC8733F36B

rows 1.3K  columns 18  scan 3.8s

roles: audit 2, category 4, date 1, id 7, other 2, who 3

## when

INGESTED_AT
  2026      1.3K  ##############################

## who

NAME by rows
       402  PITTSBURGH
        50  PENN HILLS
        38  MOUNT LEBANON
        34  SHALER
        33  ROSS
        32  MCKEESPORT
        28  BETHEL PARK
        25  MONROEVILLE
        21  MCCANDLESS
        21  PLUM
        21  WEST MIFFLIN
        20  BALDWIN
        18  UPPER ST. CLAIR
        18  SCOTT
        17  WILKINSBURG
        16  MOON
        16  WHITEHALL
        13  HAMPTON
        13  NORTH VERSAILLES
        13  SOUTH PARK

LABEL by rows
       402  Pittsburgh
        50  Penn Hills Municipality
        38  Mount Lebanon Township
        34  Shaler Township
        33  Ross Township
        32  McKeesport
        28  Bethel Park Municipality
        25  Monroeville Municipality
        21  Plum Borough
        21  West Mifflin Borough
        21  McCandless Township
        18  Baldwin Borough
        18  Scott Township
        18  Upper St. Clair Municipality
        17  Wilkinsburg Borough
        16  Whitehall Borough
        16  Moon Township
        13  North Versailles Township
        13  Hampton Township
        13  South Park Township

SRC_SHA256 by rows
      1.3K  d0e2b1234222c937c1248861e0e23095d6f910288d6df26b04a2a09bb24af746

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  BALDWIN                                   2026:20
  BETHEL PARK                               2026:28
  HAMPTON                                   2026:13
  MCCANDLESS                                2026:21
  MCKEESPORT                                2026:32
  MONROEVILLE                               2026:25
  MOON                                      2026:16
  MOUNT LEBANON                             2026:38
  NORTH VERSAILLES                          2026:13
  PENN HILLS                                2026:50
  PITTSBURGH                                2026:402
  PLUM                                      2026:21
  ROSS                                      2026:33
  SCOTT                                     2026:18
  SHALER                                    2026:34
  SOUTH PARK                                2026:13
  UPPER ST. CLAIR                           2026:18
  WEST MIFFLIN                              2026:21
  WHITEHALL                                 2026:16
  WILKINSBURG                               2026:17

LABEL by INGESTED_AT  LOAD STAMP, not an event date
  Baldwin Borough                           2026:18
  Bethel Park Municipality                  2026:28
  Hampton Township                          2026:13
  McCandless Township                       2026:21
  McKeesport                                2026:32
  Monroeville Municipality                  2026:25
  Moon Township                             2026:16
  Mount Lebanon Township                    2026:38
  North Versailles Township                 2026:13
  Penn Hills Municipality                   2026:50
  Pittsburgh                                2026:402
  Plum Borough                              2026:21
  Ross Township                             2026:33
  Scott Township                            2026:18
  Shaler Township                           2026:34
  South Park Township                       2026:13
  Upper St. Clair Municipality              2026:18
  West Mifflin Borough                      2026:21
  Whitehall Borough                         2026:16
  Wilkinsburg Borough                       2026:17

## what

DISTRICT_1: 1 22%, 2 20%, 3 14%, 4 10%, 5 7%, 6 6%, 7 5%, 0 4%, 8 4%, 9 3%, 10 3%, 11 2%

ROTATEMAP: 0 54%, 90 46%

TYPE: CITY 34%, BOROUGH 29%, TOWNSHIP 27%, MUNICIPALI 9%

WARD_1: 0 39%, 1 10%, 3 9%, 2 9%, 4 7%, 5 6%, 7 5%, 14 4%, 6 4%, 19 4%, 8 3%, 9 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DISTRICT_1 | category | 42 | 0 | 1 259; 2 236; 3 163; 4 111 |
| LABEL | who | 130 | 0 | Pittsburgh 402; Penn Hills Municipality 50; Mount Lebanon Township 38; Shaler Township 34 |
| MUNICODE_1 | other | 128 | 0 | 188 402; 185 50; 173 38; 202 34 |
| MWD_NOPA_1 | id | 1.3K | 26 | 12401 8; 16673 7; 16661 7; 16612 7 |
| MWD_PAD_1 | id | 1.3K | 0 | 1660703 7; 1660601 7; 1660102 7; 1660602 7 |
| MUNI_WAR_1 | id | 1.3K | 0 | Mccandless Ward 7 Dist 3 7; Mccandless Ward 6 Dist 1 7; Mccandless Ward 1 Dist 2 7; Mccandless Ward 6 Dist 2 7 |
| NAME | who | 127 | 0 | PITTSBURGH 402; PENN HILLS 50; MOUNT LEBANON 38; SHALER 34 |
| OBJECTID | id | 1.3K | 0 | 2170 7; 2169 7; 2168 7; 2167 7 |
| OPA_MUNI_1 | other | 131 | 0 | 100 402; 934 50; 926 38; 944 34 |
| PSEUD4_12 | id | 1.3K | 26 | 0128 8; 0336 7; 0331 7; 0317 7 |
| PSEUDONU_5 | id | 1.3K | 0 | 0 32; 128 8; 336 7; 331 7 |
| ROTATEMAP | category | 2 | 0 | 0 722; 90 605 |
| TYPE | category | 4 | 0 | CITY 456; BOROUGH 391; TOWNSHIP 359; MUNICIPALI 121 |
| WARD_1 | category | 33 | 0 | 0 423; 1 103; 3 96; 2 94 |
| GEOMETRY | id | 1.3K | 0 | POLYGON ((585556.53706188 7; POLYGON ((583895.43970179 7; POLYGON ((584875.08288642 7; POLYGON ((584509.14494213 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:52:56.95169 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5a411711-4caf-4aeb-a85a-7 1.3K |
| SRC_SHA256 | who | 1 | 0 | d0e2b1234222c937c1248861e 1.3K |
