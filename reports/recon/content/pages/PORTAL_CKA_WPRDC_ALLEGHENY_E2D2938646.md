# PORTAL_CKA_WPRDC_ALLEGHENY_E2D2938646

rows 111  columns 36  scan 4.5s

roles: amount 3, audit 2, category 16, date 1, empty 7, other 4, who 4

## when

INGESTED_AT
  2026       111  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__LENGTH | 111 | 19.70 | 1.4K | 11.9K | 14.2K | 252.9K |
| AREASQFT | 110 | 0 | 9.4K | 131.2K | 1.81M | 3.64M |
| ROADWIDTH | 82 | 22 | 36.15 | 62.57 | 65 | 3.2K |

## who

STREETNAME by rows
         3  BAUSMAN ST
         3  SECOND AVE
         2  BRIGHTON RD
         2  FORBES AVE
         2  WEST LIBERTY AVE
         2  STANTON AVE
         2  PERRYSVILLE AVE
         2  BEECHWOOD BLVD
         2  BOGGS AVE
         2  NOBLESTOWN RD
         2  BIGELOW BLVD
         1  EAST ST
         1  MIFFLIN RD
         1  CENTRE AVE
         1  S BRADDOCK AVE
         1  EAST OHIO ST
         1  APPLE AVE
         1  10TH ST BYP
         1  WAGNER ST
         1  BLVD OF THE ALLIES

STREETNAME by dollars
       14.2K        1 rows  PENN AVE
       11.9K        1 rows  FIFTH AVE
       11.4K        1 rows  SAW MILL RUN BLVD
        9.5K        1 rows  CENTRE AVE
        9.0K        1 rows  LIBERTY AVE
        7.9K        2 rows  FORBES AVE
        7.5K        1 rows  E CARSON ST
        7.3K        1 rows  W CARSON ST
        6.4K        1 rows  BLVD OF THE ALLIES
        5.3K        1 rows  WASHINGTON BLVD
        5.1K        1 rows  BROWNSVILLE RD
        5.0K        3 rows  SECOND AVE
        4.8K        1 rows  SHADY AVE
        4.6K        1 rows  FRANKSTOWN AVE
        4.5K        1 rows  BUTLER ST
        4.4K        2 rows  BIGELOW BLVD
        4.1K        1 rows  CHARTIERS AVE
        4.0K        1 rows  BANKSVILLE RD
        3.9K        1 rows  MIFFLIN RD
        3.7K        1 rows  BECKS RUN RD

HOOD_LEFT by rows
        13  CENTRAL BUSINESS DISTRICT
         5  SQUIRREL HILL SOUTH
         5  MOUNT WASHINGTON
         4  NORTH SHORE
         3  LARIMER
         3  NORTH OAKLAND
         3  WEST END
         3  HAZELWOOD
         3  EAST LIBERTY
         3  HOMEWOOD WEST
         3  LINCOLN-LEMINGTON-BELMAR
         2  BROOKLINE
         2  SOUTHSIDE SLOPES
         2  PERRY NORTH
         2  CARRICK
         2  ELLIOTT
         2  HIGHLAND PARK
         2  BELTZHOOVER
         2  SHADYSIDE
         2  CENTRAL OAKLAND

HOOD_LEFT by dollars
       33.0K       13 rows  CENTRAL BUSINESS DISTRICT
       14.2K        1 rows  POINT BREEZE NORTH
       13.6K        3 rows  WEST END
       11.6K        3 rows  NORTH OAKLAND
       10.8K        2 rows  ELLIOTT
       10.5K        3 rows  LARIMER
        8.8K        3 rows  HOMEWOOD WEST
        8.7K        2 rows  SQUIRREL HILL NORTH
        7.7K        2 rows  SOUTHSIDE FLATS
        6.4K        2 rows  CARRICK
        6.3K        5 rows  MOUNT WASHINGTON
        6.1K        5 rows  SQUIRREL HILL SOUTH
        5.1K        2 rows  SOUTHSIDE SLOPES
        5.1K        3 rows  EAST LIBERTY
        5.1K        3 rows  LINCOLN-LEMINGTON-BELMAR
        5.0K        2 rows  BROOKLINE
        4.8K        1 rows  POINT BREEZE
        4.6K        2 rows  GREENFIELD
        4.5K        1 rows  CENTRAL LAWRENCEVILLE
        4.5K        2 rows  HAYS

HOOD_RIGHT by rows
        13  CENTRAL BUSINESS DISTRICT
         6  SQUIRREL HILL SOUTH
         4  EAST LIBERTY
         4  MOUNT WASHINGTON
         4  LINCOLN-LEMINGTON-BELMAR
         4  HAZELWOOD
         3  NORTH SHORE
         3  CENTRAL NORTHSIDE
         3  CARRICK
         3  ELLIOTT
         3  NORTH OAKLAND
         2  BANKSVILLE
         2  SQUIRREL HILL NORTH
         2  HOMEWOOD WEST
         2  SHADYSIDE
         2  WEST END
         2  FRIENDSHIP
         2  SHERADEN
         2  LARIMER
         2  CENTRAL LAWRENCEVILLE

HOOD_RIGHT by dollars
       33.0K       13 rows  CENTRAL BUSINESS DISTRICT
       14.2K        1 rows  POINT BREEZE
       12.4K        2 rows  WEST END
       12.3K        6 rows  SQUIRREL HILL SOUTH
       12.0K        3 rows  ELLIOTT
       11.6K        3 rows  NORTH OAKLAND
       10.4K        4 rows  LINCOLN-LEMINGTON-BELMAR
        7.7K        2 rows  SOUTHSIDE FLATS
        7.2K        2 rows  SQUIRREL HILL NORTH
        7.0K        2 rows  SHERADEN
        6.8K        3 rows  CARRICK
        6.3K        4 rows  HAZELWOOD
        6.0K        4 rows  EAST LIBERTY
        5.7K        2 rows  HOMEWOOD WEST
        5.2K        2 rows  LARIMER
        5.1K        2 rows  SOUTHSIDE SLOPES
        4.9K        2 rows  BANKSVILLE
        4.8K        2 rows  CENTRAL LAWRENCEVILLE
        4.2K        1 rows  CRAWFORD-ROBERTS
        3.9K        1 rows  NEW HOMESTEAD

SRC_SHA256 by rows
       111  af17a1ba2ac61e7953d2ca60372c0f8bf5f6c9670da2ed34115d6910da6f8e52

SRC_SHA256 by dollars
      252.9K      111 rows  af17a1ba2ac61e7953d2ca60372c0f8bf5f6c9670da2ed34115d6910da6f

## who x when

STREETNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__LENGTH
  10TH ST BYP                               2026:825.26
  APPLE AVE                                 2026:725.17
  BAUSMAN ST                                2026:3.3K
  BEECHWOOD BLVD                            2026:3.3K
  BIGELOW BLVD                              2026:4.4K
  BLVD OF THE ALLIES                        2026:6.4K
  BOGGS AVE                                 2026:843.01
  BRIGHTON RD                               2026:2.2K
  BROWNSVILLE RD                            2026:5.1K
  CENTRE AVE                                2026:9.5K
  E CARSON ST                               2026:7.5K
  EAST OHIO ST                              2026:836.22
  EAST ST                                   2026:952.25
  FIFTH AVE                                 2026:11.9K
  FORBES AVE                                2026:7.9K
  FRANKSTOWN AVE                            2026:4.6K
  LIBERTY AVE                               2026:9.0K
  MIFFLIN RD                                2026:3.9K
  NOBLESTOWN RD                             2026:3.0K
  PENN AVE                                  2026:14.2K
  PERRYSVILLE AVE                           2026:3.4K
  S BRADDOCK AVE                            2026:3.3K
  SAW MILL RUN BLVD                         2026:11.4K
  SECOND AVE                                2026:5.0K
  SHADY AVE                                 2026:4.8K
  STANTON AVE                               2026:1.8K
  W CARSON ST                               2026:7.3K
  WAGNER ST                                 2026:387.52
  WASHINGTON BLVD                           2026:5.3K
  WEST LIBERTY AVE                          2026:3.6K

HOOD_LEFT by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__LENGTH
  BELTZHOOVER                               2026:2.2K
  BROOKLINE                                 2026:5.0K
  CARRICK                                   2026:6.4K
  CENTRAL BUSINESS DISTRICT                 2026:33.0K
  CENTRAL LAWRENCEVILLE                     2026:4.5K
  CENTRAL OAKLAND                           2026:1.6K
  EAST LIBERTY                              2026:5.1K
  ELLIOTT                                   2026:10.8K
  GREENFIELD                                2026:4.6K
  HAYS                                      2026:4.5K
  HAZELWOOD                                 2026:4.2K
  HIGHLAND PARK                             2026:2.8K
  HOMEWOOD WEST                             2026:8.8K
  LARIMER                                   2026:10.5K
  LINCOLN-LEMINGTON-BELMAR                  2026:5.1K
  MOUNT WASHINGTON                          2026:6.3K
  NORTH OAKLAND                             2026:11.6K
  NORTH SHORE                               2026:2.8K
  PERRY NORTH                               2026:3.4K
  POINT BREEZE                              2026:4.8K
  POINT BREEZE NORTH                        2026:14.2K
  SHADYSIDE                                 2026:2.8K
  SOUTHSIDE FLATS                           2026:7.7K
  SOUTHSIDE SLOPES                          2026:5.1K
  SQUIRREL HILL NORTH                       2026:8.7K
  SQUIRREL HILL SOUTH                       2026:6.1K
  WEST END                                  2026:13.6K

## what

CATEGORY: PED/VRU 33%, VRU 23%, BIC 13%, PED/BIC/VRU 13%, BIC/VRU 7%, PED/BIC 7%, PED 3%

COUNT_BICYCLECRASH: 0 57%, 1 22%, 2 9%, 3 5%, 4 2%, 7 2%, 5 2%, 8 1%, 10 1%

COUNT_FATALCRASH: 0 72%, 1 16%, 2 6%, 3 3%, 7 1%, 5 1%, 4 1%

COUNT_PEDESTRIANCRASH: 0 31%, 3 15%, 4 11%, 1 10%, 2 9%, 8 6%, 11 4%, 5 4%, 7 3%, 9 2%, 6 2%, 40 2%

COUNT_SUSPECTEDSERIOUSCRASH: 1 24%, 0 20%, 3 17%, 2 13%, 4 8%, 5 7%, 6 4%, 16 2%, 7 2%, 8 2%, 13 1%, 9 1%

CDBG: Y 67%, N 33%

COUNCIL201: 6 21%, 9 16%, 3 12%, 2 12%, 5 11%, 1 9%, 4 7%, 8 7%, 7 5%

COUNCIL2_1: 6 21%, 9 14%, 5 13%, 2 12%, 3 11%, 1 9%, 4 8%, 8 7%, 7 5%

COUNCIL_LT: 1 17%, 9 17%, 2 14%, 6 14%, 3 13%, 5 11%, 7 5%, 8 5%, 4 5%

COUNCIL_RT: 1 17%, 9 16%, 2 16%, 6 13%, 5 13%, 3 9%, 4 6%, 8 5%, 7 5%

DOMI_CLASS: Collector 50%, Minor Arterial 36%, Local 7%, Principal Arterial 7%

NO_LANES: 2 59%, 0 24%, 4 10%, 3 5%, 1 2%

NUM_LANES: 2 59%, 0 23%, 4 11%, 3 5%, 1 2%

ROADCLASS: Primary 71%, NULL 28%, Secondary 1%

RSROADCLAS: PRIMARY 92%, SECONDARY 7%, PRIMART 1%

SPEEDLIMIT: 25 84%, 35 14%, 15 2%, 30 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CATEGORY | category | 8 | 81 | PED/VRU 10; VRU 7; BIC 4; PED/BIC/VRU 4 |
| COMPLETE_STREETS | empty | 1 | 111 |  |
| COUNT_ALLCRASH | other | 78 | 0 | 43 4; 50 3; 22 3; 18 3 |
| COUNT_BICYCLECRASH | category | 9 | 0 | 0 63; 1 24; 2 10; 3 6 |
| COUNT_FATALCRASH | category | 7 | 0 | 0 80; 1 18; 2 7; 3 3 |
| COUNT_INJURYCRASH | other | 55 | 0 | 16 6; 11 6; 6 6; 15 5 |
| COUNT_PEDESTRIANCRASH | category | 22 | 0 | 0 30; 3 15; 4 11; 1 10 |
| COUNT_SUSPECTEDSERIOUSCRASH | category | 18 | 0 | 1 25; 0 21; 3 18; 2 14 |
| FATAL22 | empty | 1 | 111 |  |
| FIELD | empty | 1 | 111 |  |
| NUM_PROJECTS | empty | 1 | 111 |  |
| OBJECTID_1 | other | 110 | 0 | 112 1; 111 1; 110 1; 109 1 |
| SHAPE__LENGTH | amount | 112 | 0 | 1123.1388549662652 2; 2946.0537946132367 1; 275.77026520544456 1; 1048.576069539844 1 |
| SIDEWALK | empty | 1 | 111 |  |
| TRAFFIC_CALMING | empty | 1 | 111 |  |
| TRAFFIC_SIGNALS | empty | 1 | 111 |  |
| AREASQFT | amount | 81 | 1 | 0.0 30; 98269.8251268 2; 10803.2657114 1; 12312.0181257 1 |
| CDBG | category | 2 | 0 | Y 74; N 37 |
| COUNCIL201 | category | 9 | 0 | 6 23; 9 18; 3 13; 2 13 |
| COUNCIL2_1 | category | 9 | 0 | 6 23; 9 16; 5 14; 2 13 |
| COUNCIL_LT | category | 9 | 0 | 1 19; 9 19; 2 16; 6 15 |
| COUNCIL_RT | category | 9 | 0 | 1 19; 9 18; 2 18; 6 14 |
| DOMI_CLASS | category | 4 | 0 | Collector 55; Minor Arterial 40; Local 8; Principal Arterial 8 |
| HOOD_LEFT | who | 58 | 0 | CENTRAL BUSINESS DISTRICT 13; MOUNT WASHINGTON 5; SQUIRREL HILL SOUTH 5; NORTH SHORE 4 |
| HOOD_RIGHT | who | 57 | 0 | CENTRAL BUSINESS DISTRICT 13; SQUIRREL HILL SOUTH 6; LINCOLN-LEMINGTON-BELMAR 4; EAST LIBERTY 4 |
| NO_LANES | category | 5 | 0 | 2 65; 0 27; 4 11; 3 6 |
| NUM_LANES | category | 5 | 0 | 2 66; 0 25; 4 12; 3 6 |
| ROADCLASS | category | 3 | 0 | Primary 79; NULL 31; Secondary 1 |
| ROADWIDTH | amount | 43 | 29 | 36.0 14; 30.0 7; 40.0 6; 36.5 4 |
| RSROADCLAS | category | 4 | 36 | PRIMARY 69; SECONDARY 5; PRIMART 1 |
| SPEEDLIMIT | category | 5 | 1 | 25 92; 35 15; 15 2; 30 1 |
| STREETNAME | who | 99 | 0 | BAUSMAN ST 3; SECOND AVE 3; PERRYSVILLE AVE 2; STANTON AVE 2 |
| GEOMETRY | other | 108 | 0 | LINESTRING (584329.922493 2; LINESTRING (585807.928403 1; LINESTRING (584228.817481 1; LINESTRING (593586.503350 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:32:32.08978 111 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7a6d88b8-c4ce-444c-b4bb-b 111 |
| SRC_SHA256 | who | 1 | 0 | af17a1ba2ac61e7953d2ca603 111 |
