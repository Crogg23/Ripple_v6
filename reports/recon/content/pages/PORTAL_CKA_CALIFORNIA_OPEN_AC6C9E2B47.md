# PORTAL_CKA_CALIFORNIA_OPEN_AC6C9E2B47

rows 10.0K  columns 22  scan 4.5s

roles: amount 4, audit 2, category 7, date 1, id 3, other 3, who 3

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 10.0K | 32.55 | 33.68 | 34.44 | 36.56 | 337.1K |
| LONGITUDE | 10.0K | -121.75 | -117.15 | -114.54 | -114.13 | -1.17M |
| GSE | 10.0K | -211 | 822.32 | 4.5K | 7.3K | 12.08M |
| RPE | 10.0K | -211 | 822.32 | 4.5K | 7.3K | 12.08M |

## who

WELL_NAME by rows
         5  MW-4
         5  Private
         5  MW-2
         4  MW-3
         4  MW-1
         4  Well 5
         3  Well 7
         3  WELL 04
         3  MW-11
         2  WELL 18
         2  02N21W07Q01S
         2  MW-26
         2  02N21W31P02S
         2  MW-20
         2  35E1
         2  01N21W16A04S
         2  MW-21
         2  MW-17
         2  MW-5
         2  Well 2

WELL_NAME by dollars
      172.07        5 rows  Private
      168.26        5 rows  MW-4
      167.82        5 rows  MW-2
      134.96        4 rows  MW-1
      134.95        4 rows  Well 5
      134.85        4 rows  MW-3
      102.88        3 rows  WELL 04
      101.54        3 rows  MW-11
      101.01        3 rows  Well 7
       68.78        2 rows  35E1
       68.67        2 rows  WELL 18
       68.67        2 rows  WELL 32
       68.52        2 rows  02N21W07Q01S
       68.50        2 rows  02N21W19B02S
       68.50        2 rows  02N21W19A03S
       68.48        2 rows  02N21W20F02S
       68.48        2 rows  02N22W24P01S
       68.48        2 rows  02N21W20M06S
       68.46        2 rows  Monte Vista Well
       68.46        2 rows  02N23W25G02S

BASIN_NAME by rows
       626  Coastal Plain Of Orange County
       596  Temecula Valley
       513  San Jacinto
       463  Oxnard
       366  Palo Verde Mesa
       351  Upper Mojave River Valley
       321  San Bernardino
       277  Yuma Valley
       251  Lower San Luis Rey Valley
       221  Cahuilla Valley
       183  Upper San Luis Rey Valley
       168  Fillmore
       155  Yucaipa
       145  Palo Verde Valley
       135  Indio
       133  Las Posas Valley
       103  Piru
       100  Central
        98  Ames Valley
        94  Rialto-Colton

BASIN_NAME by dollars
       21.1K      626 rows  Coastal Plain Of Orange County
       20.0K      596 rows  Temecula Valley
       17.3K      513 rows  San Jacinto
       15.8K      463 rows  Oxnard
       12.3K      366 rows  Palo Verde Mesa
       12.1K      351 rows  Upper Mojave River Valley
       10.9K      321 rows  San Bernardino
        9.1K      277 rows  Yuma Valley
        8.4K      251 rows  Lower San Luis Rey Valley
        7.4K      221 rows  Cahuilla Valley
        6.1K      183 rows  Upper San Luis Rey Valley
        5.8K      168 rows  Fillmore
        5.3K      155 rows  Yucaipa
        4.9K      145 rows  Palo Verde Valley
        4.6K      133 rows  Las Posas Valley
        4.5K      135 rows  Indio
        3.5K      103 rows  Piru
        3.4K      100 rows  Central
        3.4K       98 rows  Ames Valley
        3.2K       94 rows  Rialto-Colton

SRC_SHA256 by rows
     10.0K  7ca7a11206821221a028b6c82daea525b0dd7a74911be0533062c5fbb60da7af

SRC_SHA256 by dollars
      337.1K    10.0K rows  7ca7a11206821221a028b6c82daea525b0dd7a74911be0533062c5fbb60d

## who x when

WELL_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  01N21W16A04S                              2026:68.36
  02N21W07Q01S                              2026:68.52
  02N21W19A03S                              2026:68.50
  02N21W19B02S                              2026:68.50
  02N21W20F02S                              2026:68.48
  02N21W20M06S                              2026:68.48
  02N21W31P02S                              2026:68.42
  02N22W24P01S                              2026:68.48
  02N23W25G02S                              2026:68.46
  35E1                                      2026:68.78
  MW-1                                      2026:134.96
  MW-11                                     2026:101.54
  MW-17                                     2026:67.51
  MW-2                                      2026:167.82
  MW-20                                     2026:67.51
  MW-21                                     2026:67.52
  MW-26                                     2026:67.52
  MW-3                                      2026:134.85
  MW-4                                      2026:168.26
  MW-5                                      2026:67.54
  Monte Vista Well                          2026:68.46
  Private                                   2026:172.07
  WELL 04                                   2026:102.88
  WELL 18                                   2026:68.67
  WELL 32                                   2026:68.67
  Well 2                                    2026:68.42
  Well 5                                    2026:134.95
  Well 7                                    2026:101.01

BASIN_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  Ames Valley                               2026:3.4K
  Cahuilla Valley                           2026:7.4K
  Central                                   2026:3.4K
  Coastal Plain Of Orange County            2026:21.1K
  Fillmore                                  2026:5.8K
  Indio                                     2026:4.5K
  Las Posas Valley                          2026:4.6K
  Lower San Luis Rey Valley                 2026:8.4K
  Oxnard                                    2026:15.8K
  Palo Verde Mesa                           2026:12.3K
  Palo Verde Valley                         2026:4.9K
  Piru                                      2026:3.5K
  Rialto-Colton                             2026:3.2K
  San Bernardino                            2026:10.9K
  San Jacinto                               2026:17.3K
  Temecula Valley                           2026:20.0K
  Upper Mojave River Valley                 2026:12.1K
  Upper San Luis Rey Valley                 2026:6.1K
  Yucaipa                                   2026:5.3K
  Yuma Valley                               2026:9.1K

## what

CONTINUOUS_DATA_STATION_NUMBER: 04S05E08N001S 25%, 06S07E04B002S 25%, 10S06E08A002S 25%, 10S06E08A003S 25%

GSE_METHOD: Unknown 78%, Digital Elevation Model 7%, Surveyed to a benchmark 6%, GPS 6%, Other 2%, USGS quad 1%, GPS with WAAS 0%, Digital aerial photo 0%

GSE_ACC: Unknown 78%, 0.1 ft. 12%, 2.5 ft. 4%, 10 ft. 3%, 5 ft. 2%, 50 ft. 0%, 20 ft. 0%, > 50 ft. 0%

COUNTY_NAME: Riverside 28%, San Diego 25%, San Bernardino 16%, Ventura 12%, Orange 6%, Imperial 5%, Los Angeles 4%, Santa Barbara 2%, Butte 0%, Alameda 0%, Monterey 0%

WELL_USE: Unknown 75%, Observation 13%, Irrigation 6%, Residential 3%, Public Supply 2%, Other 1%, Industrial 0%, Stockwatering 0%

WELL_TYPE: Unknown 72%, Single Well 23%, Part of a nested/multi-complet 5%

MONITORING_PROGRAM: VOLUNTARY 80%, SGMA 19%, CASGEM 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SITE_CODE | id | 10.0K | 0 | 344439N1168257W001 50; 344438N1196650W001 50; 344438N1196618W001 50; 344438N1196263W001 50 |
| STN_ID | id | 10.0K | 0 | 3575 50; 61079 50; 61078 50; 61082 50 |
| SWN | id | 8.9K | 1.0K | 04N01E12R001S 46; 04N27W08E004S 46; 04N27W08E001S 46; 04N02W12N002S 45 |
| WELL_NAME | who | 10.0K | 0 | Private 51; 04N01E12R001S 50; 1-36 50; 1-35 50 |
| CONTINUOUS_DATA_STATION_NUMBER | category | 5 | 10.0K | 04S05E08N001S 1; 06S07E04B002S 1; 10S06E08A002S 1; 10S06E08A003S 1 |
| LATITUDE | amount | 5.7K | 0 | 34.4419 60; 34.4275 59; 34.4369 57; 34.43144 57 |
| LONGITUDE | amount | 6.4K | 0 | -117.24214 57; -117.23756 57; -116.9534 55; -117.38815 55 |
| GSE | amount | 7.6K | 0 | 0.0 80; 2867.865 57; 2910.796 57; 3411.58 55 |
| RPE | amount | 7.7K | 0 | 0.0 80; 2867.865 57; 2910.796 57; 3411.58 55 |
| GSE_METHOD | category | 8 | 0 | Unknown 7.8K; Digital Elevation Model 653; Surveyed to a benchmark 616; GPS 550 |
| GSE_ACC | category | 8 | 0 | Unknown 7.8K; 0.1 ft. 1.2K; 2.5 ft. 401; 10 ft. 325 |
| BASIN_CODE | other | 109 | 2.3K | 8-001 626; 9-005 596; 8-005 513; 4-004.02 463 |
| BASIN_NAME | who | 108 | 2.3K | Coastal Plain Of Orange C 626; Temecula Valley 596; San Jacinto 513; Oxnard 463 |
| COUNTY_NAME | category | 11 | 0 | Riverside 2.8K; San Diego 2.5K; San Bernardino 1.6K; Ventura 1.2K |
| WELL_DEPTH | other | 726 | 7.4K | 400 41; 200 39; 300 34; 1100 30 |
| WELL_USE | category | 8 | 0 | Unknown 7.5K; Observation 1.3K; Irrigation 601; Residential 329 |
| WELL_TYPE | category | 3 | 0 | Unknown 7.2K; Single Well 2.3K; Part of a nested/multi-co 504 |
| WCR_NO | other | 621 | 9.2K | Unknown 60; E0105264 14; NA 13; E0091033 12 |
| MONITORING_PROGRAM | category | 3 | 0 | VOLUNTARY 8.0K; SGMA 1.9K; CASGEM 94 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:56:39.77733 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | ce258edd-94f8-4be2-aa6f-d 10.0K |
| SRC_SHA256 | who | 1 | 0 | 7ca7a11206821221a028b6c82 10.0K |
