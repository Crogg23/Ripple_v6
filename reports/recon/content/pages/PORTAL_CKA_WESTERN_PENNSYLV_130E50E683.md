# PORTAL_CKA_WESTERN_PENNSYLV_130E50E683

rows 10.0K  columns 12  scan 4.4s

roles: amount 1, audit 2, category 5, date 2, other 1, who 2

## when

MONTH_START
  2022       263  ###
  2023      2.9K  ##############################
  2024      2.9K  ##############################
  2025      2.9K  ##############################
  2026       976  ##########

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AVG_RIDERS | 10.0K | -0.83 | 636.28 | 5.2K | 8.0K | 10.00M |

## who

ROUTE_FULL_NAME by rows
       124  27 - FAIRYWOOD
       124  1 - FREEPORT ROAD
       124  17 - SHADELAND
       124  12 - MCKNIGHT
       124  13 - BELLEVUE
       124  24 - WEST PARK
       124  11 - FINEVIEW
       124  16 - BRIGHTON
       124  15 - CHARLES
       124  29 - ROBINSON
       124  28X - AIRPORT FLYER
       124  20 - KENNEDY
       124  38 - GREEN TREE
       124  14 - OHIO VALLEY
       124  21 - CORAOPOLIS
       124  22 - MCCOY
       124  31 - BRIDGEVILLE
       124  26 - CHARTIERS
       124  2 - MOUNT ROYAL
       124  39 - BROOKLINE

ROUTE_FULL_NAME by dollars
      503.3K      121 rows  RED - Castle Shannon via Beechview
      488.0K      123 rows  51 - CARRICK
      450.8K      123 rows  61C - MCKEESPORT-HOMESTEAD
      414.9K      123 rows  P1 - EAST BUSWAY-ALL STOPS
      367.3K      123 rows  61A - NORTH BRADDOCK
      320.4K      123 rows  71B - HIGHLAND PARK
      305.3K      123 rows  82 - LINCOLN
      301.9K      123 rows  61B - BRADDOCK-SWISSVALE
      298.1K      123 rows  71C - POINT BREEZE
      264.5K      123 rows  61D - MURRAY
      249.9K      123 rows  BLUE - SouthHills Village via Overbrook
      243.2K      123 rows  71A - NEGLEY
      243.1K      123 rows  54 - NORTH SIDE-OAKLAND-SOUTH SIDE
      228.5K      123 rows  SLVR - Libary via Overbrook
      220.6K      123 rows  75 - ELLSWORTH
      191.2K      124 rows  16 - BRIGHTON
      184.8K      123 rows  59 - MON VALLEY
      183.3K      123 rows  86 - LIBERTY
      178.2K      123 rows  71D - HAMILTON
      175.0K      123 rows  64 - LAWRENCEVILLE - WATERFRONT

SRC_SHA256 by rows
     10.0K  291d7f3a79c4ce4bdf14985c5d9c71f75740c6bce02f3b60b178206cf1368130

SRC_SHA256 by dollars
      10.00M    10.0K rows  291d7f3a79c4ce4bdf14985c5d9c71f75740c6bce02f3b60b178206cf136

## who x when

ROUTE_FULL_NAME by MONTH_START, dollars = AVG_RIDERS
  1 - FREEPORT ROAD                         2022:4.2K 2023:42.5K 2024:40.2K 2025:42.1K 2026:14.1K
  11 - FINEVIEW                             2022:846.88 2023:9.3K 2024:7.7K 2025:7.5K 2026:2.6K
  12 - MCKNIGHT                             2022:3.6K 2023:32.4K 2024:31.1K 2025:32.4K 2026:10.8K
  13 - BELLEVUE                             2022:3.6K 2023:37.3K 2024:34.6K 2025:35.2K 2026:11.9K
  14 - OHIO VALLEY                          2022:1.6K 2023:15.7K 2024:13.1K 2025:13.2K 2026:4.2K
  15 - CHARLES                              2022:2.0K 2023:19.9K 2024:18.1K 2025:20.4K 2026:6.6K
  16 - BRIGHTON                             2022:5.5K 2023:57.5K 2024:54.9K 2025:55.7K 2026:17.6K
  17 - SHADELAND                            2022:1.9K 2023:21.0K 2024:19.7K 2025:20.4K 2026:6.7K
  2 - MOUNT ROYAL                           2022:969.56 2023:9.5K 2024:8.9K 2025:8.6K 2026:2.8K
  20 - KENNEDY                              2022:599.35 2023:7.1K 2024:7.6K 2025:7.8K 2026:2.5K
  21 - CORAOPOLIS                           2022:2.1K 2023:22.5K 2024:22.0K 2025:23.0K 2026:7.5K
  22 - MCCOY                                2022:1.1K 2023:12.7K 2024:12.7K 2025:14.3K 2026:4.6K
  24 - WEST PARK                            2022:2.6K 2023:28.7K 2024:29.4K 2025:30.0K 2026:9.8K
  26 - CHARTIERS                            2022:1.4K 2023:14.9K 2024:15.6K 2025:16.7K 2026:5.3K
  27 - FAIRYWOOD                            2022:1.7K 2023:18.0K 2024:18.5K 2025:19.4K 2026:5.9K
  28X - AIRPORT FLYER                       2022:4.8K 2023:46.5K 2024:44.0K 2025:45.1K 2026:13.4K
  29 - ROBINSON                             2022:1.8K 2023:18.0K 2024:17.2K 2025:19.0K 2026:6.1K
  31 - BRIDGEVILLE                          2022:2.6K 2023:26.7K 2024:24.1K 2025:24.4K 2026:7.6K
  38 - GREEN TREE                           2022:961.17 2023:10.9K 2024:11.7K 2025:12.8K 2026:3.9K
  39 - BROOKLINE                            2022:985.02 2023:12.5K 2024:12.8K 2025:14.6K 2026:4.3K
  51 - CARRICK                              2022:10.0K 2023:142.6K 2024:144.0K 2025:142.8K 2026:48.6K
  61A - NORTH BRADDOCK                      2022:6.4K 2023:99.8K 2024:106.1K 2025:112.9K 2026:42.1K
  61B - BRADDOCK-SWISSVALE                  2022:5.1K 2023:81.2K 2024:88.8K 2025:94.1K 2026:32.7K
  61C - MCKEESPORT-HOMESTEAD                2022:8.8K 2023:130.4K 2024:126.6K 2025:137.3K 2026:47.8K
  61D - MURRAY                              2022:7.0K 2023:97.1K 2024:69.0K 2025:67.8K 2026:23.6K
  71B - HIGHLAND PARK                       2022:5.1K 2023:89.6K 2024:95.6K 2025:98.1K 2026:31.9K
  71C - POINT BREEZE                        2022:7.1K 2023:103.4K 2024:77.1K 2025:83.1K 2026:27.4K
  82 - LINCOLN                              2022:6.4K 2023:90.2K 2024:89.0K 2025:89.8K 2026:30.0K
  P1 - EAST BUSWAY-ALL STOPS                2022:8.3K 2023:123.9K 2024:116.9K 2025:124.8K 2026:41.0K
  RED - Castle Shannon via Beechview        2022:11.9K 2023:169.6K 2024:130.3K 2025:142.9K 2026:48.7K

SRC_SHA256 by MONTH_START, dollars = AVG_RIDERS
  291d7f3a79c4ce4bdf14985c5d9c71f75740c6bc  2022:218.8K 2023:3.03M 2024:2.85M 2025:2.92M 2026:982.9K

## what

CURRENT_GARAGE: East Liberty 28%, West Mifflin 24%, Ross 21%, Collier 21%, South Hills Village 4%, Incline 1%, NULL 0%

MODE: Bus 95%, Rail 4%, Incline 1%

DATE_KEY: 202604 8%, 202406 8%, 202407 8%, 202303 8%, 202308 8%, 202408 8%, 202411 8%, 202505 8%, 202507 8%, 202510 8%, 202310 8%, 202403 8%

DAY_TYPE: WEEKDAY 41%, SAT. 30%, SUN. 29%

DAY_COUNT: 4 30%, 5 26%, 22 16%, 21 10%, 20 10%, 23 4%, 6 4%, 19 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ROUTE | other | 107 | 0 | 39 124; 38 124; 36 124; 31 124 |
| ROUTE_FULL_NAME | who | 102 | 0 | 39 - BROOKLINE 124; 38 - GREEN TREE 124; 36 - BANKSVILLE 124; 31 - BRIDGEVILLE 124 |
| CURRENT_GARAGE | category | 7 | 0 | East Liberty 2.8K; West Mifflin 2.4K; Ross 2.1K; Collier 2.1K |
| MODE | category | 3 | 0 | Bus 9.5K; Rail 404; Incline 112 |
| MONTH_START | date | 41 | 0 | 4/1/2026 250; 6/1/2024 247; 7/1/2024 247; 3/1/2023 245 |
| DATE_KEY | category | 42 | 0 | 202604 250; 202406 247; 202407 247; 202303 245 |
| DAY_TYPE | category | 3 | 0 | WEEKDAY 4.1K; SAT. 3.0K; SUN. 2.9K |
| AVG_RIDERS | amount | 8.5K | 0 | 351.0 51; 198.0 50; 211.75 50; 97.25 50 |
| DAY_COUNT | category | 8 | 0 | 4 3.0K; 5 2.6K; 22 1.6K; 21 990 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:44:51.87281 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | b60b2ce8-1bf5-4568-a7a1-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | 291d7f3a79c4ce4bdf14985c5 10.0K |
