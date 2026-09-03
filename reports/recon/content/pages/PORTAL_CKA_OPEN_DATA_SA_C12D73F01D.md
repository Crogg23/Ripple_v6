# PORTAL_CKA_OPEN_DATA_SA_C12D73F01D

rows 5.0K  columns 11  scan 3.7s

roles: amount 2, audit 2, category 3, date 1, id 2, who 2

## when

INGESTED_AT
  2026      5.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TRAILMILES | 5.0K | 0 | 0.03 | 0.95 | 4.06 | 401.82 |
| SHAPE__LENGTH | 5.0K | 0.15 | 131.63 | 5.0K | 21.4K | 2.10M |

## who

TRAILNAME by rows
       197  McAllister Park Trail
       185  S River Walk
       143  OP Schnabel Park Trail
        95  San Jose Burial Park Trail
        77  Salado Creek Greenway North
        75  Olmos Basin Golf Course Park Sidewalk
        73  Comanche Lookout Park Trail
        72  Riverside Golf Course Park Trail
        67  Leon Creek Greenway North Park Trail
        63  Collins Gardens Park Sidewalk
        57  Botanical Garden Park Trail
        57  Salado Creek Greenway South
        51  N River Walk
        48  McAllister Blue Loop
        48  Apache Creek Loop
        44  San Pedro Springs Park Trail
        41  Historic City Cemeteries Park Trail
        38  San Pedro Springs Park Sidewalk
        38  McAllister Park Road
        37  Apache Creek Park Connector

TRAILNAME by dollars
      115.4K       77 rows  Salado Creek Greenway North
       89.5K      185 rows  S River Walk
       85.0K       67 rows  Leon Creek Greenway North Park Trail
       63.4K      197 rows  McAllister Park Trail
       59.5K       20 rows  Medina River Greenway Park Trail
       44.6K       57 rows  Salado Creek Greenway South
       33.2K       48 rows  McAllister Blue Loop
       31.2K       75 rows  Olmos Basin Golf Course Park Sidewalk
       28.3K      143 rows  OP Schnabel Park Trail
       28.1K       72 rows  Riverside Golf Course Park Trail
       25.6K        7 rows  Black Hill Loop
       24.7K        7 rows  Lytles Loop
       23.7K        5 rows  Medina River Greenway Espada Connection
       23.4K       51 rows  N River Walk
       23.3K        7 rows  Sendero Balcones
       23.0K       32 rows  Stone Oak South Trail
       22.0K       17 rows  Mission Trail
       21.1K       95 rows  San Jose Burial Park Trail
       21.1K       38 rows  McAllister Park Road
       21.0K        8 rows  Joe Johnston Route

SRC_SHA256 by rows
      5.0K  e08d29b0f1556cb09984b37ebbd0668ed0f752865bfd40f8f09b4e2a74ca7d78

SRC_SHA256 by dollars
       2.10M     5.0K rows  e08d29b0f1556cb09984b37ebbd0668ed0f752865bfd40f8f09b4e2a74ca

## who x when

TRAILNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__LENGTH
  Apache Creek Loop                         2026:19.5K
  Apache Creek Park Connector               2026:4.8K
  Black Hill Loop                           2026:25.6K
  Botanical Garden Park Trail               2026:9.5K
  Collins Gardens Park Sidewalk             2026:8.5K
  Comanche Lookout Park Trail               2026:10.7K
  Historic City Cemeteries Park Trail       2026:8.7K
  Joe Johnston Route                        2026:21.0K
  Leon Creek Greenway North Park Trail      2026:85.0K
  Lytles Loop                               2026:24.7K
  McAllister Blue Loop                      2026:33.2K
  McAllister Park Road                      2026:21.1K
  McAllister Park Trail                     2026:63.4K
  Medina River Greenway Espada Connection   2026:23.7K
  Medina River Greenway Park Trail          2026:59.5K
  Mission Trail                             2026:22.0K
  N River Walk                              2026:23.4K
  OP Schnabel Park Trail                    2026:28.3K
  Olmos Basin Golf Course Park Sidewalk     2026:31.2K
  Riverside Golf Course Park Trail          2026:28.1K
  S River Walk                              2026:89.5K
  Salado Creek Greenway North               2026:115.4K
  Salado Creek Greenway South               2026:44.6K
  San Jose Burial Park Trail                2026:21.1K
  San Pedro Springs Park Sidewalk           2026:4.3K
  San Pedro Springs Park Trail              2026:8.2K
  Sendero Balcones                          2026:23.3K
  Stone Oak South Trail                     2026:23.0K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__LENGTH
  e08d29b0f1556cb09984b37ebbd0668ed0f75286  2026:2.10M

## what

TRAILTYPE: Trail 59%, Sidewalk 23%, Connector 12%, Park Road 4%, Bridge 2%

TRAILSUBTYPE: Concrete 62%, Natural 16%, Asphalt 14%, Aggregate 6%, Unknown 1%, Pavers 1%, Wood 0%, Rubberized 0%, Mulch 0%

TRAILSOURCE: Imagery 72%, Parks Staff 14%, MPO 7%, COSA ITSD GIS Public Safety 4%, AsBuilt Planset 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 5.0K | 0 | 4976 25; 4975 25; 4974 25; 4973 25 |
| TRAIL_ID | id | 4.9K | 0 | TR_004888 25; TR_002939 25; TR_003360 25; TR_003426 25 |
| TRAILTYPE | category | 5 | 0 | Trail 3.0K; Sidewalk 1.1K; Connector 600; Park Road 197 |
| TRAILSUBTYPE | category | 10 | 1 | Concrete 3.1K; Natural 785; Asphalt 699; Aggregate 295 |
| TRAILNAME | who | 569 | 0 | McAllister Park Trail 197; S River Walk 185; OP Schnabel Park Trail 143; San Jose Burial Park Trai 95 |
| TRAILMILES | amount | 5.0K | 1 | 0.0139 25; 0.63916717 25; 0.07381022 25; 0.10550765 25 |
| TRAILSOURCE | category | 6 | 9 | Imagery 3.6K; Parks Staff 684; MPO 353; COSA ITSD GIS Public Safe 221 |
| SHAPE__LENGTH | amount | 5.0K | 0 | 73.4383663156083 25; 3374.80263966839 25; 389.717975474395 25; 557.080400132624 25 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:08:21.21848 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 663e1458-17d6-474c-9a8d-b 5.0K |
| SRC_SHA256 | who | 1 | 0 | e08d29b0f1556cb09984b37eb 5.0K |
