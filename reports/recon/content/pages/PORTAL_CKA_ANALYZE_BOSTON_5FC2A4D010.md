# PORTAL_CKA_ANALYZE_BOSTON_5FC2A4D010

rows 295  columns 33  scan 3.8s

roles: amount 2, audit 2, category 20, date 1, other 6, who 3

## when

INGESTED_AT
  2026       295  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 295 | 0 | 0 | 0.07 | 0.12 | 1.61 |
| SHAPE_AREA | 295 | 0 | 0 | 0 | 0 | 0 |

## who

PARK_NAME by rows
         1  Little Scobie Playground
         1  Crawford Street Playground
         1  George Wright Golf Course
         1  Brighton Common
         1  LoPresti Park
         1  Byrne Playground
         1  Doherty Playground
         1  Ringgold Park
         1  East Boston Memorial Park
         1  Roslindale Wetlands Urban Wild
         1  Ceylon Park
         1  Ryan Playground
         1  Fidelis Way Park
         1  Hemenway Playground
         1  Cuneo Park
         1  Barry Playground
         1  Winthrop Square
         1  Martin/Hilltop Playground
         1  Leo F. McCarthy Playground
         1  Doherty/Gibson Playground

PARK_NAME by dollars
        0.12        1 rows  Franklin Park (excludes Playgrounds)
        0.09        1 rows  Allandale Woods
        0.07        1 rows  Back Bay Fens
        0.07        1 rows  Arnold Arboretum
        0.05        1 rows  George Wright Golf Course
        0.05        1 rows  Commonwealth Avenue Mall
        0.04        1 rows  Millennium Park
        0.04        1 rows  Riverway
        0.04        1 rows  Mt. Hope Cemetery
        0.04        1 rows  Spectacle Island
        0.03        1 rows  Jamaica Pond Park
        0.03        1 rows  Olmsted Park
        0.03        1 rows  Fairview Cemetery
        0.03        1 rows  East Boston Memorial Park
        0.02        1 rows  Dorchester Park
        0.02        1 rows  Roslindale Wetlands Urban Wild
        0.02        1 rows  Bussey Brook Meadow
        0.02        1 rows  Hunt Playground
        0.02        1 rows  Boston Common
        0.02        1 rows  Harambee Park

ALT_NAME by rows
         1  Savin Hill Playground
         1  Chester Park
         1  Terrace Park
         1  West 1st West 2nd Street
         1  The Meadow
         1  Warren Gardens-Gendrot Trust
         1  Moreland Green
         1  London & Decatur St Park II
         1  Pine Bank
         1  Alvah Kittredge Park
         1  Brighton Square, Wilson Square
         1  Chiswick Park;  Andrew Jackson Davis Jr Tot Lot
         1  Townsend Street Plaza
         1  Franklin Field
         1  Waterfront Park
         1  Rev James K Allen Park, James F Donovan Park, Dorchester Square or Com
         1  Allis Chalmers UW, Area 1
         1  Rutherford Union Playground
         1  Copley Square
         1  M Street Plgd

ALT_NAME by dollars
        0.07        1 rows  Includes Evans Way Park, Forsyth Park, Westland Avenue Gates
        0.05        1 rows  Commonwealth Ave Mall (east of Charlesgate)
        0.04        1 rows  Gardner Street Park
        0.04        1 rows  contains Back Bay Yard, "Sears Lot" aka "Sears Rotary"
        0.04        1 rows  Spectacle Island
        0.03        1 rows  Pine Bank
        0.03        1 rows  Satori Stadium
        0.03        1 rows  Daisy Field
        0.02        1 rows  Almont Park
        0.02        1 rows  East Boston Greenway
        0.02        1 rows  Arnold Arboretum III
        0.02        1 rows  Mother Brook II
        0.02        1 rows  Franklin Field
        0.02        1 rows  Joe Moakley Park;  Joseph Moakley Park; Columbus Park
        0.02        1 rows  The Common
        0.01        1 rows  Washington Park
        0.01        1 rows  M Street Plgd
        0.01        1 rows  John J. Ryan Playground; Charlestown Playground
        0.01        1 rows  Beechmont Footpath
        0.01        1 rows  Townfield

SRC_SHA256 by rows
       295  168e1cb2d808009ccce44b82bfb72d756c235c829ecf18e54f255f6e4d99acfb

SRC_SHA256 by dollars
        1.61      295 rows  168e1cb2d808009ccce44b82bfb72d756c235c829ecf18e54f255f6e4d99

## who x when

PARK_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Allandale Woods                           2026:0.09
  Arnold Arboretum                          2026:0.07
  Back Bay Fens                             2026:0.07
  Barry Playground                          2026:0.01
  Brighton Common                           2026:0
  Byrne Playground                          2026:0
  Ceylon Park                               2026:0.01
  Commonwealth Avenue Mall                  2026:0.05
  Crawford Street Playground                2026:0.01
  Cuneo Park                                2026:0
  Doherty Playground                        2026:0.01
  Doherty/Gibson Playground                 2026:0.01
  East Boston Memorial Park                 2026:0.03
  Fidelis Way Park                          2026:0.01
  Franklin Park (excludes Playgrounds)      2026:0.12
  George Wright Golf Course                 2026:0.05
  Hemenway Playground                       2026:0.01
  Jamaica Pond Park                         2026:0.03
  Leo F. McCarthy Playground                2026:0
  Little Scobie Playground                  2026:0
  LoPresti Park                             2026:0.01
  Martin/Hilltop Playground                 2026:0
  Millennium Park                           2026:0.04
  Mt. Hope Cemetery                         2026:0.04
  Ringgold Park                             2026:0
  Riverway                                  2026:0.04
  Roslindale Wetlands Urban Wild            2026:0.02
  Ryan Playground                           2026:0.01
  Spectacle Island                          2026:0.04
  Winthrop Square                           2026:0

ALT_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Allis Chalmers UW, Area 1                 2026:0.01
  Almont Park                               2026:0.02
  Alvah Kittredge Park                      2026:0
  Arnold Arboretum III                      2026:0.02
  Brighton Square, Wilson Square            2026:0
  Chester Park                              2026:0.01
  Chiswick Park;  Andrew Jackson Davis Jr   2026:0
  Commonwealth Ave Mall (east of Charlesga  2026:0.05
  Copley Square                             2026:0
  Daisy Field                               2026:0.03
  East Boston Greenway                      2026:0.02
  Franklin Field                            2026:0.02
  Gardner Street Park                       2026:0.04
  Includes Evans Way Park, Forsyth Park, W  2026:0.07
  London & Decatur St Park II               2026:0
  M Street Plgd                             2026:0.01
  Moreland Green                            2026:0
  Pine Bank                                 2026:0.03
  Rev James K Allen Park, James F Donovan   2026:0
  Rutherford Union Playground               2026:0
  Satori Stadium                            2026:0.03
  Savin Hill Playground                     2026:0.01
  Spectacle Island                          2026:0.04
  Terrace Park                              2026:0
  The Meadow                                2026:0
  Townsend Street Plaza                     2026:0
  Warren Gardens-Gendrot Trust              2026:0
  Waterfront Park                           2026:0.01
  West 1st West 2nd Street                  2026:0
  contains Back Bay Yard, "Sears Lot" aka   2026:0.04

## what

STATUS: ❌ Not completed yet 41%, ✔ Done 41%, ⚠ Active project 16%, ! Priority 2%

NEIGHBORHOOD: Dorchester 17%, Roxbury 15%, Jamaica Plain 10%, Allston-Brighton 8%, Central Boston 8%, South End 8%, East Boston 8%, Hyde Park 6%, South Boston 6%, Charlestown 5%, West Roxbury 5%, Back Bay/Beacon Hill 4%

INCLUSION: Y 100%

BENCHES_WHEELCHAIR: Y 100%

TABLE_WHEELCHAIR: Y 100%

DRINKING_FOUNTAIN: Y 100%

SPRAY_PLAY: Yes 100%

BENCHES_ALONG_PATH: Y 100%

SHADED_SEATING: Y 100%

SHADE_TYPE: Tree shade 78%, Tree shade, Shade shelter 16%, Shade shelter 6%

BATHROOM: Portable toilet 75%, Accessible portable toilet 17%, Bathroom 8%

ACCESSIBLE_PLAY: No playground at this park 42%, Play panels, Transfer station 19%, Play panels 12%, Molded bucket seat swing 4%, Stair-free access all levels,  4%, Molded bucket seat swing, Play 4%, Molded bucket seat swing, Play 3%, Molded bucket seat swing, Tran 3%, Play panels, Transfer station, 3%, Play panels, Transfer station, 2%, Ground level play 2%

SENSORY_PLAY: Dish swing 23%, Musical play 23%, Dish swing, Musical play 14%, Dish swing, Musical play, Sens 11%, Sensory panel 11%, Dish swing, Sensory panel 7%, Dish swing, OmniSpin spinner 4%, Roller slide 2%, Musical play, Sensory panel, R 2%, OmniSpin spinner, Musical play 2%, Roller table, Musical play, Di 2%

OTHER_INCLUSIVE: Accessible game table 31%, Accessible field viewing area 12%, Accessible basketball viewing  6%, Historical plaque viewing area 6%, Pier viewing area 6%, Tennis/pickleball wall 6%, Accessible game table, Accessi 6%, Accessible community garden, S 6%, Accessible fishing platform 6%, Tic-tac-toe panel 6%, Accessible basketball viewing  6%

COMMUNICATION: Braille 50%, Spanish 33%, Somali 17%

PARKING_TYPE: On street 79%, On street (permitted) 10%, Parking lot (accessible) 4%, On street, Parking lot 3%, On street, Parking lot (access 2%, On street (accessible) 2%, Parking lot 1%

NEAR_BUS: Blue Hill Ave @ Ingleside St,  9%, Blue Hill Ave @ Mattapan St, 0 9%, 247 Norfolk St opp Capen St, 0 9%, Alwin St @ Stonehill Rd, 308 f 9%, Western Ave opp Riverdale St,  9%, Dorchester Ave @ Howes St, 125 9%, River St @ Reddy Ave, 0.5 mile 9%, Melnea Cass Blvd @ Washington  9%, 3867 Washington St opp Tollgat 9%, Meridian St @ Havre St, 0.2 mi 9%, Boardman St @ Ashley St, 171 f 9%

NEAR_TRAIN: Upham's Corner, 0.5 mi 11%, Boston Landing, Boston, MA 021 11%, Fairmount , 1 mile 11%, Jackson Square, 0.7 miles 11%, Jackson Square , 0.7 miles 11%, Washington St @ Firth Rd, 0.3  11%, Talbot Ave, 0.4 miles 11%, Fields Corner, 1.3 miles 11%, Ruggles, 0.4 miles 11%

DISSOLVED_OS_DISTRICT: Dorchester 17%, Roxbury 15%, Jamaica Plain 10%, Central Boston 8%, Allston-Brighton 8%, East Boston 8%, South End 8%, South Boston 6%, Roslindale 5%, Hyde Park 5%, Charlestown 5%, West Roxbury 5%

DISSOLVED_OS_ZIP_CODE: 02119 12%, 02130 11%, 02128 10%, 02118 10%, 02124 8%, 02136 8%, 02135 7%, 02121 7%, 02125 7%, 02129 7%, 02127 6%, 02132 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATUS | category | 4 | 0 | ❌ Not completed yet 121; ✔ Done 120; ⚠ Active project 47; ! Priority 7 |
| POLYGON_ID | other | 295 | 0 | 124 2; 10000 2; 10002 2; 10001 2 |
| PARK_NAME | who | 294 | 0 | Franklin Park (excludes P 2; American Legion Play Area 2; Tiffany Moore Tot Lot (Fr 2; El Parquesito de la Herma 2 |
| ALT_NAME | who | 108 | 187 | West and Austin Street Ro 1; Spectacle Island 1; Lakeside 1; Melrose Park 1 |
| PARK_ADDRESS | other | 292 | 3 | 25 Pierpont Road 2; 85 American Legion Hwy 2; 155 Seaver Street 2; 450 Walnut Avenue 2 |
| NEIGHBORHOOD | category | 18 | 1 | Dorchester 44; Roxbury 40; Jamaica Plain 25; Allston-Brighton 22 |
| INCLUSION | category | 2 | 277 | Y 18 |
| STAIR_FREE | other | 113 | 157 | Playground 11; Seating area 7; Playground, Fitness equip 3; Basketball court, Playgro 3 |
| BENCHES_WHEELCHAIR | category | 2 | 172 | Y 123 |
| TABLE_WHEELCHAIR | category | 2 | 212 | Y 83 |
| DRINKING_FOUNTAIN | category | 2 | 204 | Y 91 |
| SPRAY_PLAY | category | 2 | 236 | Yes 59 |
| BENCHES_ALONG_PATH | category | 2 | 236 | Y 59 |
| SHADED_SEATING | category | 2 | 175 | Y 120 |
| SHADE_TYPE | category | 4 | 175 | Tree shade 94; Tree shade, Shade shelter 19; Shade shelter 7 |
| BATHROOM | category | 4 | 283 | Portable toilet 9; Accessible portable toile 2; Bathroom 1 |
| ACCESSIBLE_PLAY | category | 43 | 166 | No playground at this par 39; Play panels, Transfer sta 18; Play panels 11; Molded bucket seat swing 4 |
| SENSORY_PLAY | category | 17 | 234 | Dish swing 13; Musical play 13; Dish swing, Musical play 8; Dish swing, Musical play, 6 |
| OTHER_INCLUSIVE | category | 13 | 278 | Accessible game table 5; Accessible field viewing  2; Accessible basketball vie 1; Historical plaque viewing 1 |
| COMMUNICATION | category | 4 | 289 | Braille 3; Spanish 2; Somali 1 |
| PARKING_TYPE | category | 8 | 190 | On street 83; On street (permitted) 10; Parking lot (accessible) 4; On street, Parking lot 3 |
| NEAR_BUS | category | 42 | 254 | Blue Hill Ave @ Ingleside 1; Blue Hill Ave @ Mattapan  1; 247 Norfolk St opp Capen  1; Alwin St @ Stonehill Rd,  1 |
| NEAR_TRAIN | category | 10 | 286 | Upham's Corner, 0.5 mi 1; Boston Landing, Boston, M 1; Fairmount , 1 mile 1; Jackson Square, 0.7 miles 1 |
| DISSOLVED_OS_ADDRESS | other | 294 | 1 | 25 Pierpont Road 
155 Sea 2; 85 American Legion Hwy 2; 155 Seaver Street 2; 3131 Washington Street 2 |
| DISSOLVED_OS | other | 295 | 0 | Franklin Park (excludes P 2; American Legion Play Area 2; Tiffany Moore Tot Lot (Fr 2; El Parquesito (Franklin P 2 |
| DISSOLVED_OS_DISTRICT | category | 17 | 0 | Dorchester 44; Roxbury 40; Jamaica Plain 25; Central Boston 22 |
| DISSOLVED_OS_ZIP_CODE | category | 39 | 1 | 02119 25; 02130 23; 02128 20; 02118 20 |
| SHAPE_LENGTH | amount | 298 | 0 | 0.121455742372905 2; 0.005541213722539 2; 0.002719640591001 2; 0.001937946366284 2 |
| SHAPE_AREA | amount | 301 | 0 | 0.000171304382507 2; 0.000001319306829 2; 0.000000445923331 2; 0.000000241585785 2 |
| SHAPE_WKT | other | 99 | 198 | MULTIPOLYGON (((-71.09206 1; MULTIPOLYGON (((-71.09728 1; MULTIPOLYGON (((-71.15941 1; MULTIPOLYGON (((-71.04047 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:38:47.75185 295 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9d92c8d8-f582-4af7-9b38-6 295 |
| SRC_SHA256 | who | 1 | 0 | 168e1cb2d808009ccce44b82b 295 |
