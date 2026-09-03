# PORTAL_ARC_LA_COUNTY_OPEN_D_86C98732BB

rows 146  columns 18  scan 4.1s

roles: amount 2, audit 2, category 4, date 1, other 6, who 4

## when

INGESTED_AT
  2026       146  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 146 | 32.58 | 34.02 | 35.38 | 36.33 | 5.0K |
| LONGITUDE | 146 | -120.44 | -118.30 | -117.06 | -116.93 | -17.3K |

## who

CONAME by rows
         2  Dmb Global Inc
         2  Proper Skateboarding Llc
         2  Rollerama
         2  Pacific Rink
         2  Skateland
         2  Warning Skate Shop
         2  Boarders Sports Inc
         2  Dwindle Distribution
         1  Bula Skate Co Llc
         1  Arena Development Group
         1  Excel Skateboard
         1  Buena Venture Llc
         1  San Pedro Surf & Sport
         1  Skatebording Stuff
         1  Skate Beach Inc
         1  Alliance Skate Park-lake Elsnr
         1  Girls Skateboards
         1  Track & Roller Repair Co
         1  Stoked Skateboards
         1  Holiday Skating Ctr

CONAME by dollars
       70.76        2 rows  Rollerama
       69.57        2 rows  Skateland
       68.18        2 rows  Boarders Sports Inc
       68.12        2 rows  Proper Skateboarding Llc
       68.08        2 rows  Dmb Global Inc
          68        2 rows  Warning Skate Shop
       67.84        2 rows  Dwindle Distribution
       67.62        2 rows  Pacific Rink
       36.33        1 rows  Roller Towne
       35.36        1 rows  Jett Rink Llc
       34.94        1 rows  Central Coast Sports Arena
       34.70        1 rows  Slow Ride Enterprises Inc
       34.60        1 rows  Pharmacy Boardshop Palmdale
       34.51        1 rows  Holiday Skating Ctr
       34.50        1 rows  Victor Valley Roller Derby
       34.45        1 rows  Power Play Skating Arena
       34.42        1 rows  661 Skate
       34.41        1 rows  Val Surf
       34.38        1 rows  Skate Fresh
       34.28        1 rows  Calling All Skaters

STATE_NAME by rows
       146  California

STATE_NAME by dollars
        5.0K      146 rows  California

CITY by rows
        26  Los Angeles
         7  Torrance
         5  Long Beach
         5  Venice
         4  Bakersfield
         4  El Segundo
         3  Redondo Beach
         3  Glendale
         3  San Pedro
         3  Hermosa Beach
         2  Ventura
         2  Northridge
         2  La Crescenta
         2  Santa Monica
         2  South Gate
         2  Sunland
         2  Bell
         2  Santa Clarita
         2  Culver City
         2  Malibu

CITY by dollars
      885.23       26 rows  Los Angeles
      236.84        7 rows  Torrance
      169.96        5 rows  Venice
      168.86        5 rows  Long Beach
      141.46        4 rows  Bakersfield
      135.67        4 rows  El Segundo
      102.45        3 rows  Glendale
      101.59        3 rows  Hermosa Beach
      101.52        3 rows  Redondo Beach
      101.17        3 rows  San Pedro
       69.01        2 rows  Victorville
       68.83        2 rows  Santa Clarita
       68.83        2 rows  Hesperia
       68.52        2 rows  Ventura
       68.51        2 rows  Sunland
       68.46        2 rows  Northridge
       68.44        2 rows  La Crescenta
       68.32        2 rows  Sherman Oaks
       68.04        2 rows  Malibu
       68.03        2 rows  Santa Monica

SRC_SHA256 by rows
       146  45c499dc1abb7bd3ed0f994665cc665944ee7ec3df039fa0799456062bf97f6a

SRC_SHA256 by dollars
        5.0K      146 rows  45c499dc1abb7bd3ed0f994665cc665944ee7ec3df039fa0799456062bf9

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  661 Skate                                 2026:34.42
  Alliance Skate Park-lake Elsnr            2026:33.69
  Arena Development Group                   2026:34.02
  Boarders Sports Inc                       2026:68.18
  Buena Venture Llc                         2026:34.26
  Bula Skate Co Llc                         2026:32.77
  Central Coast Sports Arena                2026:34.94
  Dmb Global Inc                            2026:68.08
  Dwindle Distribution                      2026:67.84
  Excel Skateboard                          2026:33.99
  Girls Skateboards                         2026:33.82
  Holiday Skating Ctr                       2026:34.51
  Jett Rink Llc                             2026:35.36
  Pacific Rink                              2026:67.62
  Pharmacy Boardshop Palmdale               2026:34.60
  Power Play Skating Arena                  2026:34.45
  Proper Skateboarding Llc                  2026:68.12
  Roller Towne                              2026:36.33
  Rollerama                                 2026:70.76
  San Pedro Surf & Sport                    2026:33.72
  Skate Beach Inc                           2026:33.16
  Skate Fresh                               2026:34.38
  Skatebording Stuff                        2026:33.99
  Skateland                                 2026:69.57
  Slow Ride Enterprises Inc                 2026:34.70
  Stoked Skateboards                        2026:33.85
  Track & Roller Repair Co                  2026:34.03
  Val Surf                                  2026:34.41
  Victor Valley Roller Derby                2026:34.50
  Warning Skate Shop                        2026:68

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  California                                2026:5.0K

## what

NAICS: 45111044 45%, 71394025 36%, 45111045 6%, 61162017 3%, 71399028 2%, 45111057 2%, 45231906 1%, 71219004 1%, 33992022 1%, 44811006 1%, 71394015 1%, 53228401 1%

SIC: 594116 45%, 799901 36%, 594117 6%, 799962 3%, 799994 2%, 594112 2%, 539901 1%, 799951 1%, 394933 1%, 561101 1%, 799701 1%, 799909 1%

EMPNUM: 3 46%, 2 16%, 1 7%, 7 6%, 4 5%, 10 5%, 5 4%, 15 3%, 30 2%, 40 1%, 8 1%, 20 1%

CATEGORY: Skate Shops 44%, Skating Rinks 34%, Skate - Other 21%, Roller Skate Shops 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 145 | 0 | 728 1; 727 1; 726 1; 725 1 |
| CONAME | who | 136 | 0 | Skateland 2; Rollerama 2; Pacific Rink 2; Proper Skateboarding Llc 2 |
| ADDR | other | 129 | 0 | Ocean Front Walk 4; S Vermont Ave 4; Mesa Verde Ave 2; Parthenia St 2 |
| CITY | who | 79 | 0 | Los Angeles 26; Torrance 7; Long Beach 5; Venice 5 |
| STATE_NAME | who | 1 | 0 | California 146 |
| ZIP | other | 120 | 0 | 90291 5; 90245 4; 90036 3; 90502 3 |
| NAICS | category | 23 | 0 | 45111044 61; 71394025 48; 45111045 8; 61162017 4 |
| SIC | category | 23 | 0 | 594116 61; 799901 48; 594117 8; 799962 4 |
| EMPNUM | category | 23 | 0 | 3 61; 2 22; 1 10; 7 8 |
| SALESVOL | other | 53 | 0 | 558000 37; 317000 17; 372000 15; 186000 9 |
| DESC | other | 142 | 0 | Pacific Rink, Torrance, C 2; Proper Skateboarding Llc, 2; Dwindle Distribution, El  2; Dmb Global Inc, Los Angel 2 |
| LATITUDE | amount | 142 | 0 | 34.063928999997906 2; 33.913431000231405 2; 34.04471400027589 2; 33.9288779203057 2 |
| LONGITUDE | amount | 140 | 0 | -118.343209500164 2; -118.37929049973901 2; -118.29137850041 2; -118.172483400318 2 |
| CATEGORY | category | 4 | 0 | Skate Shops 64; Skating Rinks 49; Skate - Other 31; Roller Skate Shops 2 |
| GEOMETRY | other | 139 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:20:28.63810 146 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1487573e-c0a1-45ec-ad30-3 146 |
| SRC_SHA256 | who | 1 | 0 | 45c499dc1abb7bd3ed0f99466 146 |
