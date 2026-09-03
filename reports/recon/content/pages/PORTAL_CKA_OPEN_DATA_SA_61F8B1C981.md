# PORTAL_CKA_OPEN_DATA_SA_61F8B1C981

rows 337  columns 12  scan 4.2s

roles: amount 2, audit 2, category 1, date 1, other 3, who 4

## when

INGESTED_AT
  2026       337  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 337 | 3.9K | 381.3K | 41.04M | 503.90M | 1.32B |
| SHAPE__LENGTH | 337 | 252.08 | 3.0K | 132.3K | 361.6K | 3.35M |

## who

PARK_NAME by rows
         1  Healy Murphy Park
         1  Barbara Drive Park
         1  Benavides Park
         1  Northridge Park
         1  Lackland Terrace Park
         1  Blue Grass Lawn Park
         1  Camino Santa Maria Park
         1  Kennedy Park
         1  Hemisfair Park
         1  King Park
         1  Spanish Governors Palace
         1  Olmos Basin Park
         1  Kelly Area Park
         1  Garza Park
         1  Ridgeview Elementary School Park
         1  Shadwell Park
         1  River Walk
         1  Lee's Creek Park
         1  Cathedral Rock Park
         1  Beitel Creek Greenway

PARK_NAME by dollars
     503.90M        1 rows  Government Canyon State Park
      50.12M        1 rows  Rancho Diana Natural Area
      46.53M        1 rows  Leon Creek Greenway
      42.55M        1 rows  McAllister Park
      38.35M        1 rows  Salado Creek Greenway
      28.42M        1 rows  Scenic Canyon Natural Areas
      26.53M        1 rows  Friedrich Natural Area
      25.27M        1 rows  Southside Lions Park
      22.83M        1 rows  Medina River Natural Area
      21.58M        1 rows  Pearsall Park
      20.26M        1 rows  Olmos Basin Park
      18.53M        1 rows  Eisenhower Natural Area
      16.44M        1 rows  Medina River Greenway
      14.51M        1 rows  King Park
      14.37M        1 rows  Phil Hardberger Natural Area
      14.06M        1 rows  Calaveras Lake Park
      12.83M        1 rows  O P Schnabel Park
      12.39M        1 rows  Panther Springs Natural Area
      11.09M        1 rows  Brackenridge Park
      10.70M        1 rows  Stone Oak Natural Areas

ALT_PARK_NAME by rows
         2  Leon Creek Greenway North
         1  Nicholas Copernicus
         1  John F Kennedy
         1  Camino Santa Maria/Woodlawn
         1  Caracol Creek
         1  Al Forge
         1  Levi Strauss
         1  Rainbow Hills
         1  Riverside Golf Course
         1  Market Square
         1  Fox Trailhead
         1  Rodriguez
         1  W W McAllister
         1  Blue Grass Lawn Park
         1  Cedar Creek Golf Course
         1  Brackenridge
         1  Sunset Hills
         1  Morrison Kallison
         1  Robert B Dawson
         1  Escobar Field

ALT_PARK_NAME by dollars
     503.90M        1 rows  Government Canyon
      50.12M        1 rows  Rancho Diana
      48.10M        2 rows  Leon Creek Greenway North
      42.55M        1 rows  W W McAllister
      38.35M        1 rows  McNeill
      28.42M        1 rows  Scenic Canyon
      26.53M        1 rows  Emile and Albert Friedrich
      25.27M        1 rows  Southside Lions
      22.83M        1 rows  Medina River Natural Area
      21.58M        1 rows  Pearsall
      20.26M        1 rows  Olmos Basin
      18.53M        1 rows  Dwight D. Eisenhower
      16.44M        1 rows  Medina River Greenway
      14.51M        1 rows  Martin Luther King
      14.37M        1 rows  Hardberger East & West
      14.06M        1 rows  Calaveras Lake
      12.83M        1 rows  O P Schnabel
      12.39M        1 rows  Panther Springs
      11.09M        1 rows  Brackenridge
      10.70M        1 rows  Stone Oak

STREET_NAME by rows
         5  W Commerce St
         4  E Commerce St
         3  Mission Rd
         3  NE 410
         3  Cincinnati Ave
         3  Wilderness Oak
         2  Tampico St
         2  Bandera Rd
         2  W Thompson Place
         2  Poteet Jourdanton Fwy
         2  Jones Maltsberger Rd
         2  Broadway
         2  Mission Grande
         2  Spring Time Dr
         2  Martin Luther King Dr
         2  Babcock Rd
         2  S Ellison Dr
         2  E Sunshine Dr
         2  Catalpa Ave
         2  San Pedro Ave

STREET_NAME by dollars
     503.90M        1 rows  Galm Rd
      60.19M        2 rows  Menchaca Rd
      46.53M        1 rows  N 1604 W
      45.60M        2 rows  Jones Maltsberger Rd
      39.27M        2 rows  Poteet Jourdanton Fwy
      38.35M        1 rows  North Loop Rd
      28.42M        1 rows  Scenic Loop Rd
      26.53M        1 rows  Milsa Dr
      25.27M        1 rows  Hiawatha
      21.58M        1 rows  Old Pearsall Rd
      20.26M        1 rows  Devine Rd
      18.53M        1 rows  NW Military Hwy
      17.89M        2 rows  Applewhite Rd
      14.57M        2 rows  Martin Luther King Dr
      14.37M        1 rows  Blanco Rd
      14.06M        1 rows  Bernhardt Rd
      13.17M        3 rows  Wilderness Oak
      12.85M        2 rows  Bandera Rd
      11.48M        2 rows  Stone Oak Pkwy
      11.46M        5 rows  W Commerce St

SRC_SHA256 by rows
       337  6d30716865bbdf5f0e59be55f404d104c18bb84b276d330e896bc61531706aec

SRC_SHA256 by dollars
       1.32B      337 rows  6d30716865bbdf5f0e59be55f404d104c18bb84b276d330e896bc6153170

## who x when

PARK_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Barbara Drive Park                        2026:318.3K
  Beitel Creek Greenway                     2026:1.03M
  Benavides Park                            2026:342.6K
  Blue Grass Lawn Park                      2026:22.5K
  Camino Santa Maria Park                   2026:10.5K
  Cathedral Rock Park                       2026:2.62M
  Friedrich Natural Area                    2026:26.53M
  Garza Park                                2026:1.10M
  Government Canyon State Park              2026:503.90M
  Healy Murphy Park                         2026:45.7K
  Hemisfair Park                            2026:1.36M
  Kelly Area Park                           2026:154.9K
  Kennedy Park                              2026:1.74M
  King Park                                 2026:14.51M
  Lackland Terrace Park                     2026:333.3K
  Lee's Creek Park                          2026:341.9K
  Leon Creek Greenway                       2026:46.53M
  McAllister Park                           2026:42.55M
  Medina River Natural Area                 2026:22.83M
  Northridge Park                           2026:201.5K
  Olmos Basin Park                          2026:20.26M
  Pearsall Park                             2026:21.58M
  Rancho Diana Natural Area                 2026:50.12M
  Ridgeview Elementary School Park          2026:158.9K
  River Walk                                2026:1.61M
  Salado Creek Greenway                     2026:38.35M
  Scenic Canyon Natural Areas               2026:28.42M
  Shadwell Park                             2026:93.6K
  Southside Lions Park                      2026:25.27M
  Spanish Governors Palace                  2026:18.7K

ALT_PARK_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Al Forge                                  2026:125.5K
  Blue Grass Lawn Park                      2026:22.5K
  Brackenridge                              2026:11.09M
  Camino Santa Maria/Woodlawn               2026:10.5K
  Caracol Creek                             2026:1.63M
  Cedar Creek Golf Course                   2026:7.53M
  Dwight D. Eisenhower                      2026:18.53M
  Emile and Albert Friedrich                2026:26.53M
  Escobar Field                             2026:96.7K
  Fox Trailhead                             2026:1.45M
  Government Canyon                         2026:503.90M
  John F Kennedy                            2026:1.74M
  Leon Creek Greenway North                 2026:48.10M
  Levi Strauss                              2026:839.9K
  Market Square                             2026:296.4K
  McNeill                                   2026:38.35M
  Medina River Natural Area                 2026:22.83M
  Morrison Kallison                         2026:675.1K
  Nicholas Copernicus                       2026:937.7K
  Olmos Basin                               2026:20.26M
  Pearsall                                  2026:21.58M
  Rainbow Hills                             2026:524.9K
  Rancho Diana                              2026:50.12M
  Riverside Golf Course                     2026:8.00M
  Robert B Dawson                           2026:192.0K
  Rodriguez                                 2026:1.74M
  Scenic Canyon                             2026:28.42M
  Southside Lions                           2026:25.27M
  Sunset Hills                              2026:83.5K
  W W McAllister                            2026:42.55M

## what

PARK_TYPE: Neighborhood Park 54%, Community Park 9%, Special Use Facility 9%, Large Urban Park 7%, Natural Area 6%, Greenway 4%, Historic Resource 4%, Historical Facility 3%, Urban Space 2%, Sports Complex 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 339 | 0 | 337 2; 336 2; 335 2; 334 2 |
| PARK_ID | other | 338 | 0 | 398 2; 397 2; 396 2; 395 2 |
| PARK_NAME | who | 340 | 0 | Tobin Library Park 2; Schaefer Library Park 2; Mission Library Park 2; Memorial Library Park 2 |
| ALT_PARK_NAME | who | 271 | 71 | Westside Creeks 2; French Creek Park 2; Leon Creek Greenway North 2; Alazan Creek 2 |
| STREET_NUMBER | other | 281 | 7 | 100 7; 500 6; 300 5; 600 4 |
| STREET_NAME | who | 292 | 0 | W Commerce St 5; E Commerce St 4; Cincinnati Ave 4; Roosevelt Ave 3 |
| PARK_TYPE | category | 11 | 44 | Neighborhood Park 159; Community Park 27; Special Use Facility 25; Large Urban Park 21 |
| SHAPE__AREA | amount | 336 | 0 | 6467.1328125 2; 7122.669921875 2; 40499.439453125 2; 3863.23393797874 2 |
| SHAPE__LENGTH | amount | 336 | 0 | 326.308773710826 2; 348.090544137149 2; 900.311476276324 2; 252.084829052489 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:39:39.43396 337 |
| SOURCE_RUN_ID | audit | 1 | 0 | 11aaf583-3a0d-4905-8835-0 337 |
| SRC_SHA256 | who | 1 | 0 | 6d30716865bbdf5f0e59be55f 337 |
