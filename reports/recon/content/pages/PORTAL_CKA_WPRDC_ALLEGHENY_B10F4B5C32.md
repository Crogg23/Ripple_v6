# PORTAL_CKA_WPRDC_ALLEGHENY_B10F4B5C32

rows 5.5K  columns 13  scan 3.8s

roles: amount 2, audit 2, category 4, date 2, other 2, who 2

## when

MONTH_START
  2024      1.4K  ###############
  2025      2.9K  ##############################
  2026      1.2K  ############

INGESTED_AT
  2026      5.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| OTP_PCT | 5.5K | 0.21 | 0.68 | 0.92 | 0.99 | 3.7K |
| COUNT_TOTAL | 5.5K | 12 | 1.8K | 25.3K | 33.8K | 22.12M |

## who

ROUTE_FULL_NAME by rows
        69  55 - GLASSPORT
        69  20 - KENNEDY
        69  11 - FINEVIEW
        69  8 - PERRYSVILLE
        69  60 - MCKEESPORT - WALNUT
        69  86 - LIBERTY
        69  71A - NEGLEY
        69  39 - BROOKLINE
        69  1 - FREEPORT ROAD
        69  57 - HAZELWOOD
        69  4 - TROY HILL
        69  6 - SPRING HILL
        69  79 - EAST HILLS
        69  87 - FRIENDSHIP
        69  64 - LAWRENCEVILLE - WATERFRONT
        69  27 - FAIRYWOOD
        69  61A - NORTH BRADDOCK
        69  83 - BEDFORD HILL
        69  59 - MON VALLEY
        69  2 - MOUNT ROYAL

ROUTE_FULL_NAME by dollars
      899.5K       69 rows  51 - CARRICK
      786.1K       69 rows  61A - NORTH BRADDOCK
      685.9K       69 rows  91 - BUTLER STREET
      594.5K       69 rows  P1 - EAST BUSWAY-ALL STOPS
      575.9K       69 rows  75 - ELLSWORTH
      548.0K       69 rows  61C - MCKEESPORT-HOMESTEAD
      543.4K       69 rows  61B - BRADDOCK-SWISSVALE
      516.3K       69 rows  16 - BRIGHTON
      510.8K       69 rows  71C - POINT BREEZE
      462.0K       69 rows  82 - LINCOLN
      459.9K       69 rows  71D - HAMILTON
      452.9K       69 rows  54 - NORTH SIDE-OAKLAND-SOUTH SIDE
      450.8K       69 rows  61D - MURRAY
      442.0K       63 rows  RED - Castle Shannon via Beechview
      434.2K       69 rows  64 - LAWRENCEVILLE - WATERFRONT
      430.7K       69 rows  59 - MON VALLEY
      413.6K       69 rows  1 - FREEPORT ROAD
      352.6K       69 rows  71B - HIGHLAND PARK
      348.5K       69 rows  71A - NEGLEY
      343.9K       69 rows  13 - BELLEVUE

SRC_SHA256 by rows
      5.5K  9d19d763a6bd70517505d32bc0e186a59a26b9c1e3dc6692f6a5c2982ffc3bd1

SRC_SHA256 by dollars
      22.12M     5.5K rows  9d19d763a6bd70517505d32bc0e186a59a26b9c1e3dc6692f6a5c2982ffc

## who x when

ROUTE_FULL_NAME by MONTH_START, dollars = COUNT_TOTAL
  1 - FREEPORT ROAD                         2024:153.6K 2025:208.5K 2026:51.5K
  11 - FINEVIEW                             2024:18.9K 2025:40.1K 2026:14.3K
  16 - BRIGHTON                             2024:139.0K 2025:269.9K 2026:107.5K
  2 - MOUNT ROYAL                           2024:41.8K 2025:73.8K 2026:27.5K
  20 - KENNEDY                              2024:60.3K 2025:86.6K 2026:21.2K
  27 - FAIRYWOOD                            2024:54.1K 2025:78.7K 2026:20.9K
  39 - BROOKLINE                            2024:57.7K 2025:101.1K 2026:31.7K
  4 - TROY HILL                             2024:26.9K 2025:57.4K 2026:22.9K
  51 - CARRICK                              2024:236.7K 2025:472.9K 2026:189.8K
  55 - GLASSPORT                            2024:76.2K 2025:121.0K 2026:36.6K
  57 - HAZELWOOD                            2024:59.7K 2025:113.2K 2026:45.6K
  59 - MON VALLEY                           2024:135.5K 2025:224.9K 2026:70.2K
  6 - SPRING HILL                           2024:76.5K 2025:115.5K 2026:33.7K
  60 - MCKEESPORT - WALNUT                  2024:11.6K 2025:21.9K 2026:8.3K
  61A - NORTH BRADDOCK                      2024:213.0K 2025:405.6K 2026:167.5K
  61B - BRADDOCK-SWISSVALE                  2024:148.0K 2025:278.1K 2026:117.3K
  61C - MCKEESPORT-HOMESTEAD                2024:148.7K 2025:283.8K 2026:115.5K
  64 - LAWRENCEVILLE - WATERFRONT           2024:118.3K 2025:228.3K 2026:87.6K
  71A - NEGLEY                              2024:93.5K 2025:184.9K 2026:70.1K
  71C - POINT BREEZE                        2024:139.4K 2025:265.3K 2026:106.0K
  71D - HAMILTON                            2024:125.7K 2025:237.6K 2026:96.6K
  75 - ELLSWORTH                            2024:156.8K 2025:304.6K 2026:114.6K
  79 - EAST HILLS                           2024:57.1K 2025:116.4K 2026:47.7K
  8 - PERRYSVILLE                           2024:115.1K 2025:165.0K 2026:47.8K
  82 - LINCOLN                              2024:137.6K 2025:239.1K 2026:85.3K
  83 - BEDFORD HILL                         2024:69.2K 2025:137.5K 2026:54.4K
  86 - LIBERTY                              2024:76.9K 2025:159.1K 2026:61.8K
  87 - FRIENDSHIP                           2024:70.6K 2025:137.5K 2026:55.2K
  91 - BUTLER STREET                        2024:185.6K 2025:360.0K 2026:140.4K
  P1 - EAST BUSWAY-ALL STOPS                2024:163.1K 2025:308.1K 2026:123.3K

SRC_SHA256 by MONTH_START, dollars = COUNT_TOTAL
  9d19d763a6bd70517505d32bc0e186a59a26b9c1  2024:6.39M 2025:11.47M 2026:4.26M

## what

CURRENT_GARAGE: East Liberty 28%, West Mifflin 25%, Ross 22%, Collier 21%, South Hills Village 4%

MODE: Bus 96%, Light Rail 4%

DATEKEY: 202604 9%, 202407 8%, 202408 8%, 202410 8%, 202411 8%, 202412 8%, 202501 8%, 202502 8%, 202503 8%, 202504 8%, 202505 8%, 202506 8%

DAY_TYPE: WEEKDAY 41%, SAT. 30%, SUN. 29%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ROUTE | other | 105 | 0 | Y49 69; Y46 69; SLVR 69; P68 69 |
| ROUTE_FULL_NAME | who | 102 | 0 | Y49 - PROSPECT FLYER 69; Y46 - ELIZABETH FLYER 69; SLVR - Libary via Overbro 69; P68 - BRADDOCK HILLS FLYE 69 |
| CURRENT_GARAGE | category | 5 | 0 | East Liberty 1.6K; West Mifflin 1.4K; Ross 1.2K; Collier 1.2K |
| MODE | category | 2 | 0 | Bus 5.3K; Light Rail 246 |
| MONTH_START | date | 22 | 0 | 4/1/2026 247; 7/1/2024 244; 8/1/2024 244; 10/1/2024 241 |
| DATEKEY | category | 23 | 0 | 202604 247; 202407 244; 202408 244; 202410 241 |
| DAY_TYPE | category | 3 | 0 | WEEKDAY 2.3K; SAT. 1.7K; SUN. 1.6K |
| OTP_PCT | amount | 3.1K | 0 | 0.6877 29; 0.7447 28; 0.643 28; 0.7505 28 |
| COUNT_ONTIME | other | 3.2K | 0 | 840 31; 914 29; 606 29; 1851 29 |
| COUNT_TOTAL | amount | 3.7K | 0 | 1793 29; 1354 29; 1508 29; 652 29 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:34:57.77827 5.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0ff94822-0d41-4927-a536-f 5.5K |
| SRC_SHA256 | who | 1 | 0 | 9d19d763a6bd70517505d32bc 5.5K |
