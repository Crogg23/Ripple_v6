# PORTAL_CKA_ANALYZE_BOSTON_B6C7223760

rows 576  columns 30  scan 4.4s

roles: amount 3, audit 2, category 11, date 1, empty 2, other 8, who 4

## when

INGESTED_AT
  2026       576  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 576 | 0.01 | 1.08 | 159.46 | 392.18 | 6.0K |
| SHAPE_LENGTH | 576 | 0 | 0 | 0.12 | 0.56 | 6.20 |
| SHAPE_AREA | 576 | 0 | 0 | 0 | 0 | 0 |

## who

SITE_NAME by rows
         2  Lincoln Square
         1  St Michael's Cemetery
         1  Riverway IV
         1  Schraffts Centre Harborwalk
         1  Arborway I
         1  Fan Pier Harborwalk
         1  John W McCormack Memorial Park
         1  Dooley Playground
         1  Rogers Park
         1  Wilson Park
         1  Theresa Hynes Park
         1  Central Burying Ground
         1  Stony Brook Reservation I
         1  Fort Point Channel Harborwalk
         1  Chestnut Street
         1  Nancy Kafka Reserve
         1  Clarendon Street Playlot
         1  Bremen Street Park I
         1  Norman Leventhal Park
         1  Kennedy Playground

SITE_NAME by dollars
      392.18        1 rows  Franklin Park
      285.44        1 rows  Stony Brook Reservation I
      245.43        1 rows  Forest Hills Cemetery
      224.27        1 rows  Arnold Arboretum
      170.72        1 rows  Charles River Reservation
      169.89        1 rows  Thompson Island
      155.98        1 rows  George Wright Golf Course
      149.44        1 rows  Sawmill Brook/Brook Farm
      142.10        1 rows  Belle Isle Marsh Reservation
      141.63        1 rows  Stony Brook Reservation II
      129.12        1 rows  St Joseph's Cemetery
      125.05        1 rows  Mt. Hope Cemetery
      121.60        1 rows  Neponset River Reservation I
      102.12        1 rows  Chestnut Hill Reservation I
       97.74        1 rows  Jamaica Pond Park
       91.66        1 rows  Millennium Park I
          86        1 rows  Spectacle Island I
       79.31        1 rows  Mount Benedict Cemetery
       70.24        1 rows  Stony Brook Reservation III
       70.10        1 rows  Back Bay Fens

ALT_NAME by rows
       211  N/A
         2  Back Bay Fens
         2  Fenway Parkway
         2  Channel Center Park
         2  Back Bay Fens/Charlesgate
         2  East Boston Piers Park
         2  Spectacle Island
         2  Kennedy Greenway Parcel 23d, Chinatown Park
         2  Riverway parkway
         2  Dorchester Shores Reservation
         1  Melnea A. Cass Rink, Swimming Pool, and Spray Deck
         1  Fort Independence; Pleasure Bay, Harry McDonough Sailing Center
         1  Savin Hill Marsh; Dorchester Shores Reservation
         1  470 Atlantic Avenue Harborwalk
         1  John J. Ryan Playground; Charlestown Playground
         1  Viola Square
         1  Saratoga St. Play Area
         1  Wolcott Square
         1  North End Park
         1  Kennedy Greenway Parcels 14-17

ALT_NAME by dollars
        1.6K      211 rows  N/A
      170.72        1 rows  Charles River Esplanade, Herter Park, Daley Field
      149.44        1 rows  Camp Andrew
      111.52        2 rows  Spectacle Island
      102.12        1 rows  Chestnut Hill Reservoir
       97.74        1 rows  Pine Bank
       91.66        1 rows  Gardner Street Park
       70.10        1 rows  Includes Evans Way Park, Forsyth Park, Westland Avenue Gates
       63.83        1 rows  Zoo New England
       58.78        1 rows  Joe Moakley Park;  Joseph Moakley Park; Columbus Park
       48.71        1 rows  Mount Lebanon Cemetery
       47.70        1 rows  Fort Independence; Pleasure Bay, Harry McDonough Sailing Cen
       45.74        1 rows  The Common
       44.75        1 rows  Franklin Field
       42.83        1 rows  Daisy Field
       41.16        1 rows  Allandale Farm
       30.39        1 rows  Mill Pond Reservation
       27.40        1 rows  Kelly/Factory Hill (Lawler)/Bajko/Olsen
       25.31        1 rows  Orient Heights Beach
       24.68        1 rows  Arnold Arboretum III

PROTECTION by rows
       248  A97
        28  N/A
        18  A97/LWCF
        17  A97/CPA
        16  Ch91/WPA
        12  A97/WPA
        10  Ch114S17
         9  A97/CR
         8  Ch114S17/A97
         8  A97/USH
         7  A97/Ch91/WPA/CPA
         6  A97/Acts2008Ch306/CAT Mit/RFK
         6  A97/PARC
         6  A97/NRHP
         5  A97/LWCF/USH
         5  A97/Ch91/WPA
         5  Ch91
         5  A97/GPOD
         5  CAT Mit
         4  A97/WPA/Ch91

PROTECTION by dollars
        1.1K      248 rows  A97
      448.44       10 rows  Ch114S17
      392.18        1 rows  A97/WPA/NRHP/CPA/LWCF
      285.44        1 rows  A97/Wetlands
      246.06        2 rows  Ch114S17/NRHP
      224.27        1 rows  A97/GPOD/WPA/CPA
      218.29        7 rows  A97/Ch91/WPA/CPA
      214.21       17 rows  A97/CPA
      183.70        2 rows  A97/WPA/ACEC
      177.08        9 rows  A97/CR
      175.31       12 rows  A97/WPA
      149.44        1 rows  A97/NRHP/WPA/CPA
      149.13        3 rows  Ch114S17/A97/CPA
      142.10        1 rows  A97/LWCF/WPA/Ch91/ACEC/CPA
      115.49        3 rows  A97/NRHP/WPA
      113.62       18 rows  A97/LWCF
       94.94        5 rows  A97/Ch91/WPA
       91.66        1 rows  SURF/WPA/A97
       82.74        2 rows  A97/ACEC/WPA
       81.96        4 rows  A97/UPARR

SRC_SHA256 by rows
       576  f662d0d30c985cf9d5f89bb1d32f4a9bf8c7d637be21b1ca288170841b1d11e3

SRC_SHA256 by dollars
        6.0K      576 rows  f662d0d30c985cf9d5f89bb1d32f4a9bf8c7d637be21b1ca288170841b1d

## who x when

SITE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  Arborway I                                2026:16.78
  Arnold Arboretum                          2026:224.27
  Belle Isle Marsh Reservation              2026:142.10
  Bremen Street Park I                      2026:17.79
  Central Burying Ground                    2026:1.49
  Charles River Reservation                 2026:170.72
  Chestnut Street                           2026:1.04
  Clarendon Street Playlot                  2026:0.32
  Dooley Playground                         2026:0.54
  Fan Pier Harborwalk                       2026:1.66
  Forest Hills Cemetery                     2026:245.43
  Fort Point Channel Harborwalk             2026:1.41
  Franklin Park                             2026:392.18
  George Wright Golf Course                 2026:155.98
  John W McCormack Memorial Park            2026:0.12
  Kennedy Playground                        2026:0.23
  Lincoln Square                            2026:0.27
  Nancy Kafka Reserve                       2026:0.71
  Norman Leventhal Park                     2026:1.54
  Riverway IV                               2026:1.92
  Rogers Park                               2026:8.18
  Sawmill Brook/Brook Farm                  2026:149.44
  Schraffts Centre Harborwalk               2026:1.01
  St Joseph's Cemetery                      2026:129.12
  St Michael's Cemetery                     2026:46.03
  Stony Brook Reservation I                 2026:285.44
  Stony Brook Reservation II                2026:141.63
  Theresa Hynes Park                        2026:0.42
  Thompson Island                           2026:169.89
  Wilson Park                               2026:0.10

ALT_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  470 Atlantic Avenue Harborwalk            2026:0.18
  Back Bay Fens                             2026:1.44
  Back Bay Fens/Charlesgate                 2026:2.40
  Camp Andrew                               2026:149.44
  Channel Center Park                       2026:1.38
  Charles River Esplanade, Herter Park, Da  2026:170.72
  Chestnut Hill Reservoir                   2026:102.12
  Dorchester Shores Reservation             2026:5.97
  East Boston Piers Park                    2026:10.57
  Fenway Parkway                            2026:7.52
  Fort Independence; Pleasure Bay, Harry M  2026:47.70
  Gardner Street Park                       2026:91.66
  Includes Evans Way Park, Forsyth Park, W  2026:70.10
  Joe Moakley Park;  Joseph Moakley Park;   2026:58.78
  John J. Ryan Playground; Charlestown Pla  2026:8.78
  Kennedy Greenway Parcel 23d, Chinatown P  2026:0.79
  Kennedy Greenway Parcels 14-17            2026:4.71
  Melnea A. Cass Rink, Swimming Pool, and   2026:2.58
  Mount Lebanon Cemetery                    2026:48.71
  N/A                                       2026:1.6K
  North End Park                            2026:0.61
  Pine Bank                                 2026:97.74
  Riverway parkway                          2026:2.81
  Saratoga St. Play Area                    2026:0.23
  Savin Hill Marsh; Dorchester Shores Rese  2026:9.66
  Spectacle Island                          2026:111.52
  The Common                                2026:45.74
  Viola Square                              2026:0.12
  Wolcott Square                            2026:0.07
  Zoo New England                           2026:63.83

## what

OWNERSHIP: City of Boston 64%, Commonwealth of Massachusetts 18%, Private 10%, Massport 2%, MassDOT 2%, BRA 1%, United States of America 1%, MBTA 1%, BWSC 0%, Town of Brookline 0%

TYPECODE: 3 46%, 1 22%, 2 13%, 6 8%, 4 6%, 5 4%, 7 1%

DISTRICT: Dorchester 16%, Jamaica Plain 11%, Central Boston 11%, Roxbury 10%, Allston-Brighton 8%, East Boston 8%, Hyde Park 8%, South Boston 7%, West Roxbury 6%, Roslindale 6%, South End 6%, Charlestown 5%

ZONAGG: Open Space District 44%, Residential District 30%, Special District 8%, Commercial/Office/Business Dis 8%, Industrial District 5%, Conservation Protection Subdis 3%, Institutional District 2%

TYPELONG: Parks, Playgrounds & Athletic  46%, Malls, Squares & Plazas 22%, Parkways, Reservations & Beach 13%, Urban Wilds 8%, Cemeteries & Burying Grounds 6%, Community Gardens 4%, Open Land 1%

OS_OWN_JUR: BPRD 58%, DCR 19%, BCC 6%, Private 6%, PWD 3%, Massport 2%, RFK Greenway Conservancy 2%, BPS 1%, MBTA 1%, BRA 1%, MA EOEEA 1%, TTOR 1%

OS_MNGMNT: BPRD 61%, NULL 14%, DCR 9%, Private 8%, Massport 3%, Private+BPRD 1%, BCYF 1%, TTOR 1%, National Park Service 1%, Mass Audubon Society 1%, BRA 1%, BPRD + Private 0%

POS: X 85%, N 15%

PA: X 93%, L 4%, N 2%, A 1%

AGNCYJURIS: BPRD 76%, BCC 7%, DCR 7%, Massport 3%, PWD 2%, BPS 1%, BRA 0%, Private 0%, BCYF 0%, NPS 0%

REGION: INFO_Reallocation From Dept 40%, PARK_Maintenance_Region 1 11%, PARK_Maintenance_Region 4 10%, PARK_Maintenance_Region 2 9%, PARK_Maintenance_Region 6 7%, PARK_Maintenance_Region 5 7%, PARK_Urban_Wild 7%, PARK_Maintenance_Region 3 6%, PARK_Cemetery Maintenance Requ 3%, PARK_Trades_Only 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SITE_NAME | who | 564 | 0 | Lincoln Square 4; Al Festa Little League Fi 3; Dorchester Park Access Ea 3; Richmond St Entrance to D 3 |
| OWNERSHIP | category | 9 | 0 | City of Boston 371; Commonwealth of Massachus 102; Private 59; Massport 14 |
| PROTECTION | who | 135 | 0 | A97 248; N/A 28; A97/LWCF 18; A97/CPA 17 |
| TYPECODE | category | 7 | 0 | 3 265; 1 126; 2 76; 6 45 |
| DISTRICT | category | 17 | 0 | Dorchester 80; Jamaica Plain 56; Central Boston 54; Roxbury 49 |
| ACRES | amount | 579 | 0 | 0.381100730000000 4; 1.074506330000000 3; 0.411817360000000 3; 0.059830820000000 3 |
| ADDRESS | other | 496 | 52 | 174 W Second St 4; 160 Florence Street 4; 135-141 A Street 4; 230 Shawmut Avenue 4 |
| ZONAGG | category | 7 | 0 | Open Space District 254; Residential District 170; Special District 48; Commercial/Office/Busines 45 |
| TYPELONG | category | 7 | 0 | Parks, Playgrounds & Athl 265; Malls, Squares & Plazas 126; Parkways, Reservations &  76; Urban Wilds 45 |
| OS_OWN_JUR | category | 27 | 0 | BPRD 319; DCR 103; BCC 35; Private 33 |
| OS_MNGMNT | category | 32 | 0 | BPRD 338; NULL 78; DCR 52; Private 46 |
| POS | category | 2 | 0 | X 488; N 88 |
| PA | category | 4 | 0 | X 535; L 23; N 14; A 4 |
| ALT_NAME | who | 229 | 132 | N/A 211; Channel Center Park 3; Jim Napolitano Field, Gra 2; Dorchester Park II 2 |
| AGNCYJURIS | category | 21 | 162 | BPRD 308; BCC 30; DCR 28; Massport 14 |
| PARK_ID | other | 304 | 278 | 335 3; 013 2; 124 2; 356 2 |
| REGION | category | 10 | 0 | INFO_Reallocation From De 228; PARK_Maintenance_Region 1 62; PARK_Maintenance_Region 4 56; PARK_Maintenance_Region 2 50 |
| OS_ID | other | 581 | 0 | 9110 3; 8231 3; 8230 3; 1035 3 |
| F_100FTRULE | other | 1 | 0 | YES 576 |
| ZIPCODE | other | 60 | 20 | 02130 43; 02136 41; 02128 39; 02119 32 |
| PARCELNUMBER | other | 374 | 159 | ROW 29; 1812162000,1812161000 3; 0601265000,0601258000 3; 0504175000 3 |
| YEARACQUIRED | other | 102 | 3 | 0 366; 1991 15; 1897 7; 2025 7 |
| STAREA | empty | 1 | 576 |  |
| STLENGTH | empty | 1 | 576 |  |
| SHAPE_LENGTH | amount | 577 | 0 | 0.002942517442753 3; 0.002248851801031 3; 0.000980659410844 3; 0.010717782200484 3 |
| SHAPE_AREA | amount | 578 | 0 | 0.000000475362667 3; 0.000000181898217 3; 0.000000027093410 3; 0.000001926355147 3 |
| SHAPE_WKT | other | 160 | 418 | MULTIPOLYGON (((-71.02035 1; MULTIPOLYGON (((-71.06396 1; MULTIPOLYGON (((-71.06563 1; MULTIPOLYGON (((-71.13514 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:43:23.49317 576 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0f7ee4d8-b29d-4a78-8ee7-7 576 |
| SRC_SHA256 | who | 1 | 0 | f662d0d30c985cf9d5f89bb1d 576 |
