# PORTAL_CKA_ANALYZE_BOSTON_EB235CDC7A

rows 1.3K  columns 16  scan 5.5s

roles: amount 2, audit 2, category 6, date 1, id 1, other 2, who 3

## when

INGESTED_AT
  2026      1.3K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 1.3K | -71.18 | -71.08 | -71.01 | -70.96 | -93.4K |
| POINT_Y | 1.3K | 42.24 | 42.33 | 42.39 | 42.39 | 55.6K |

## who

PARK_NAME by rows
        40  Moakley Park
        36  Harambee Park
        34  Franklin Park
        33  Smith Playground
        26  Malcolm X Park
        23  Hunt Playground
        23  Boston Common
        23  Back Bay Fens
        23  Arnold Arboretum
        21  LoPresti Park
        21  East Boston Memorial Park I
        18  English H.S. Athletic Fields
        17  Walsh Playground
        16  Doherty/Gibson Playground
        16  Cassidy Playground
        16  Jamaica Pond Park
        16  Ross Playground
        15  Garvey Playground
        15  Ronan Park
        15  Titus Sparrow Park

PARK_NAME by dollars
      -71.02        1 rows  McLean Playground
      -71.03        1 rows  Putnam Square
      -71.03        1 rows  Day Square
      -71.03        1 rows  East Boston Memorial Park III
      -71.04        1 rows  Devine Memorial Rink Grounds
      -71.04        1 rows  Maverick Square
      -71.04        1 rows  Daniel E. O'Connor Park
      -71.05        1 rows  Mirabella Pool
      -71.05        1 rows  Polcari Park
      -71.05        1 rows  Foster Street Play Area
      -71.06        1 rows  Allen Park
      -71.06        1 rows  Coppens Square
      -71.06        1 rows  Cook Street Play Area
      -71.06        1 rows  Hayes Square
      -71.06        1 rows  Angell Memorial Square
      -71.06        1 rows  Copp's Hill Burying Ground
      -71.06        1 rows  Deer Street Park
      -71.06        1 rows  Winthrop Square
      -71.06        1 rows  Thompson Square II
      -71.06        1 rows  Tai Tung Park

ASSET_DETA by rows
       178  Full
       162  N/A
       140  UA
       127  Approved Portable Toilet Site
       104  Post-and-ring
        99  Bottle Filler,Drinking
        73  Inverted U
        60  Drinking
        37  Combo
        36  Softball
        31  Hydraulic
        25  Electrical
        24  Half
        24  Little League
        23  Mechanical
        22  Unlit 
        21  Baseball
        20  Pet,Bottle Filler,Drinking
        10  Permanent Structure
         8  Wave

ASSET_DETA by dollars
      -71.03        1 rows  Mechnical
      -71.05        1 rows  Hydraulic (table)
      -71.05        1 rows  Schoolyard
      -71.05        1 rows  Bottle Filler, Drinking
      -71.05        1 rows  Lacrosse
      -71.06        1 rows  George Thorndike Angell Memorial
      -71.06        1 rows  BottleFiller,Drinking
      -71.06        1 rows  Pet
      -71.06        1 rows  Lyman Memorial Fountain
      -71.06        1 rows  Brewer Fountain
      -71.07        1 rows  George Robert White Memorial
      -71.07        1 rows  Drinking, Pet
      -71.07        1 rows  Boy and Bird Fountain
      -71.07        1 rows  Bagheera Fountain
      -71.07        1 rows  Statler Fountain
      -71.07        1 rows  Triton Babies Fountain
      -71.07        1 rows  Small Child Fountain
      -71.07        1 rows  Ether Fountain
      -71.08        1 rows  Skate dot
      -71.08        1 rows  bucket swing

SRC_SHA256 by rows
      1.3K  a6ffb4063a81e1b200176f915c2e481848e13c55152af5ba048a61a0a3ba9e22

SRC_SHA256 by dollars
      -93.4K     1.3K rows  a6ffb4063a81e1b200176f915c2e481848e13c55152af5ba048a61a0a3ba

## who x when

PARK_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  Arnold Arboretum                          2026:-1.6K
  Back Bay Fens                             2026:-1.6K
  Boston Common                             2026:-1.6K
  Cassidy Playground                        2026:-1.1K
  Daniel E. O'Connor Park                   2026:-71.04
  Day Square                                2026:-71.03
  Devine Memorial Rink Grounds              2026:-71.04
  Doherty/Gibson Playground                 2026:-1.1K
  East Boston Memorial Park I               2026:-1.5K
  East Boston Memorial Park III             2026:-71.03
  English H.S. Athletic Fields              2026:-1.3K
  Foster Street Play Area                   2026:-71.05
  Franklin Park                             2026:-2.4K
  Garvey Playground                         2026:-1.1K
  Harambee Park                             2026:-2.6K
  Hunt Playground                           2026:-1.6K
  Jamaica Pond Park                         2026:-1.1K
  LoPresti Park                             2026:-1.5K
  Malcolm X Park                            2026:-1.8K
  Maverick Square                           2026:-71.04
  McLean Playground                         2026:-71.02
  Mirabella Pool                            2026:-71.05
  Moakley Park                              2026:-2.8K
  Polcari Park                              2026:-71.05
  Putnam Square                             2026:-71.03
  Ronan Park                                2026:-1.1K
  Ross Playground                           2026:-1.1K
  Smith Playground                          2026:-2.3K
  Titus Sparrow Park                        2026:-1.1K
  Walsh Playground                          2026:-1.2K

ASSET_DETA by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  Approved Portable Toilet Site             2026:-9.0K
  Baseball                                  2026:-1.5K
  Bottle Filler, Drinking                   2026:-71.05
  Bottle Filler,Drinking                    2026:-7.0K
  BottleFiller,Drinking                     2026:-71.06
  Brewer Fountain                           2026:-71.06
  Combo                                     2026:-2.6K
  Drinking                                  2026:-4.3K
  Electrical                                2026:-1.8K
  Full                                      2026:-12.7K
  George Thorndike Angell Memorial          2026:-71.06
  Half                                      2026:-1.7K
  Hydraulic                                 2026:-2.2K
  Hydraulic (table)                         2026:-71.05
  Inverted U                                2026:-5.2K
  Lacrosse                                  2026:-71.05
  Little League                             2026:-1.7K
  Lyman Memorial Fountain                   2026:-71.06
  Mechanical                                2026:-1.6K
  Mechnical                                 2026:-71.03
  N/A                                       2026:-11.5K
  Permanent Structure                       2026:-710.81
  Pet                                       2026:-71.06
  Pet,Bottle Filler,Drinking                2026:-1.4K
  Post-and-ring                             2026:-7.4K
  Schoolyard                                2026:-71.05
  Softball                                  2026:-2.6K
  UA                                        2026:-10.0K
  Unlit                                     2026:-1.6K
  Wave                                      2026:-568.86

## what

PLAY_NAME: N/A 99%, Tadpole Playground 0%, El Parquesito 0%, Tiffany Moore 0%, Dottie Curran 0%, Court Area 0%, Main Playground 0%, Harambee Park (Talbot Ave) 0%, Dennis 'DJ' Simmonds Playgroun 0%, Frog Pond 0%, Kelleher Rose Garden 0%, Wilson Field 0%

NEIGHBOR: Dorchester 18%, Roxbury 16%, Allston-Brighton 11%, Jamaica Plain 10%, East Boston 9%, South Boston 7%, Central Boston 5%, South End 5%, Mattapan 5%, West Roxbury 5%, Hyde Park 4%, Roslindale 4%

ASSET: Drinking Fountain 17%, Bike Rack 15%, Restroom 11%, Playground 11%, Athletic Field 11%, Basketball 11%, Spray Play 7%, Tennis 6%, Flagpole 5%, Ornamental Fountain 3%, Parking Lot 3%, Fitness Equipment 1%

ASSET_USE2: N/A 61%, Natural Turf 8%, N 7%, Y 7%, A 5%, B 3%, UA 3%, Artificial Turf 2%, Aluminum  2%, C 1%, Fiberglass  0%, D 0%

ASSET_USE3: N/A 73%, 90 9%, UA 9%, 0 3%, USA 5X8 3%, 45 1%, Scoreboard 1%, Stalls: 2 0%, USA 6X10 0%, Pad Capacity: 3 0%, Pad Capacity: 2 0%, Pad Capacity: 1 0%

AGE: N/A 89%, 2-5,5-12 8%, 5-12 1%, 2-5 1%, 0-2,2-5,5-12 1%, UA 0%, 2-12 0%, 2-5 & 5-12 0%, 2-5, 5-12 0%, 0-2,2-5 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PARK_NAME | who | 220 | 1 | Moakley Park 40; Harambee Park 36; Franklin Park 34; Smith Playground 33 |
| PLAY_NAME | category | 20 | 0 | N/A 1.3K; Tadpole Playground 2; El Parquesito 2; Tiffany Moore 2 |
| NEIGHBOR | category | 19 | 1 | Dorchester 212; Roxbury 189; Allston-Brighton 123; Jamaica Plain 116 |
| OS_ID | other | 217 | 0 | 200 40; 142 36; 124 34; 284 33 |
| ASSET | category | 24 | 0 | Drinking Fountain 216; Bike Rack 186; Restroom 144; Playground 144 |
| ASSET_DETA | who | 67 | 0 | Full 178; N/A 162; UA 140; Approved Portable Toilet  127 |
| ASSET_USE1 | other | 63 | 0 | N/A 758; 2 183; 1 114; Spray 82 |
| ASSET_USE2 | category | 26 | 0 | N/A 792; Natural Turf 103; N 93; Y 93 |
| ASSET_USE3 | category | 25 | 1 | N/A 947; 90 122; UA 117; 0 38 |
| AGE | category | 10 | 0 | N/A 1.2K; 2-5,5-12 103; 5-12 14; 2-5 13 |
| SHAPE_WKT | id | 1.3K | 0 | POINT (-71.05183053999996 7; POINT (-71.11763976199995 7; POINT (-71.08513811599993 7; POINT (-71.11196940199994 7 |
| POINT_X | amount | 1.3K | 0 | -71.051830539999969 7; -71.117639761999953 7; -71.085138115999939 7; -71.111969401999943 7 |
| POINT_Y | amount | 1.3K | 0 | 42.326592306000066 7; 42.315528549000078 7; 42.291056210000079 7; 42.263295346000064 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:52:26.29499 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | c1e1a100-cfdf-4479-8b1e-9 1.3K |
| SRC_SHA256 | who | 1 | 0 | a6ffb4063a81e1b200176f915 1.3K |
