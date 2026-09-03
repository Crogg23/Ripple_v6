# PORTAL_CKA_OPEN_DATA_SA_9DCA88D285

rows 617  columns 27  scan 4.6s

roles: amount 4, audit 2, category 9, date 5, empty 2, other 4, who 2

## when

SCHEDULE_START
  2023         1  
  2025        21  #########
  2026        74  ##############################

SCHEDULE_FINISH
  2023         1  
  2025        15  ######
  2026        80  ##############################

ACTUAL_START
  2023         1  #
  2025        21  ###########
  2026        56  ##############################

ACTUAL_FINISH
  2023         1  #
  2025        19  ##########
  2026        56  ##############################

INGESTED_AT
  2026       617  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ESTIMATED_TOTAL_COST | 617 | 206.44 | 13.5K | 165.2K | 436.4K | 17.50M |
| INSIDE_X | 617 | 2.03M | 2.12M | 2.19M | 2.20M | 1.31B |
| INSIDE_Y | 617 | 13.63M | 13.74M | 13.79M | 13.79M | 8.47B |
| SHAPE__LENGTH | 617 | 22.36 | 1.9K | 14.0K | 16.1K | 1.74M |

## who

NAME by rows
        26  LEON CREEK
        17  Salado Creek
        15  SALADO CREEK
        12  UNNAMED NATURAL CREEK OF SALADO CREEK
        10  San Antonio River
         9  Leon Creek
         8  ROSILLO CREEK
         8  Culebra Creek
         7  Alazan Creek
         7  SLICK RANCH CREEK
         7  San Antonio River Above Medina
         7  Huebner Creek
         6  OLMOS CREEK LOWER
         6  LORENCE CREEK
         6  Maverick Creek
         6  East Elm Creek
         6  FRENCH CREEK
         5  Panther Springs Creek Upper
         5  French Creek Tributary A
         5  Zarzamora Creek

NAME by dollars
      741.5K        5 rows  Zarzamora Creek
      632.3K       26 rows  LEON CREEK
      561.6K        2 rows  Olmos Creek
      513.9K        7 rows  Alazan Creek
      502.0K       17 rows  Salado Creek
      494.4K       15 rows  SALADO CREEK
      393.1K        8 rows  ROSILLO CREEK
      358.2K        2 rows  Edgemont at O'Connor
      356.3K        9 rows  Leon Creek
      354.9K        3 rows  Indian Creek
      339.7K        4 rows  Apache Creek
      277.8K        2 rows  4242 E Southcross Blvd
      269.0K        3 rows  Floyd Curl Channel
      265.3K        4 rows  Desilu Channel
      201.2K        8 rows  Culebra Creek
      190.3K        1 rows  Gun Smoke Channel
      170.7K        2 rows  Stoneshire Channel
      169.3K        3 rows  Mud Creek
      166.3K        1 rows  13044 Nacogdoches Rd
      155.9K        2 rows  8406 Romney

SRC_SHA256 by rows
       617  9d3b4ef6885addc6e39969e44b4c2e7957318fdec1b0b490cc7ae7435d61f579

SRC_SHA256 by dollars
      17.50M      617 rows  9d3b4ef6885addc6e39969e44b4c2e7957318fdec1b0b490cc7ae7435d61

## who x when

NAME by SCHEDULE_START, dollars = ESTIMATED_TOTAL_COST
  Apache Creek                              2026:177.1K
  Culebra Creek                             2026:161.6K
  Huebner Creek                             2026:55.9K
  LEON CREEK                                2026:138.5K
  Leon Creek                                2026:37.7K
  OLMOS CREEK LOWER                         2025:61.4K 2026:11.9K
  ROSILLO CREEK                             2025:228.0K 2026:165.1K
  SLICK RANCH CREEK                         2026:116.7K
  Salado Creek                              2023:37.5K
  San Antonio River Above Medina            2026:26.7K
  Zarzamora Creek                           2026:114.6K

SRC_SHA256 by SCHEDULE_START, dollars = ESTIMATED_TOTAL_COST
  9d3b4ef6885addc6e39969e44b4c2e7957318fde  2023:37.5K 2025:1.02M 2026:2.48M

## what

SEGMENT_COUNT: 1 87%, 2 8%, 3 2%, 4 1%, 8 0%, 7 0%, 9 0%, 5 0%, 19 0%

FISCAL_YEAR: 2029 27%, 2030 25%, 2028 17%, 2026 15%, 2027 15%

CHANNEL_TYPE: Natural Creek 77%, Improved Channel 23%

PROJECT_TYPE: Debris Removal 77%, Restoration 23%

WATERSHED: Salado 28%, Leon 26%, San Antonio 14%, SW 10%, NW 10%, NE 9%, SE 2%

COUNCIL_DISTRICT: 8 18%, 9 13%, 10 13%, 2 13%, 6 12%, 3 10%, 7 8%, 4 8%, 1 3%, 5 2%

PERCENT_COMPLETE: 100 97%, 50 1%, 40 1%

PROJECT_MANAGER: Maria Diaz 69%, Xavier Gonzales 16%, Luis Garcia 6%, Daniel Villasenor 6%, Xavier Gonzlaes 2%, Xavier Gonzalez 1%

CONTACT: Maria Diaz: (210) 207-5030 68%, David Gonzales: (210) 207-0709 31%, 0 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 603 | 0 | 617 4; 616 4; 615 4; 614 4 |
| PROJECTID | other | 609 | 0 | 4736 4; 4735 4; 4734 4; 4733 4 |
| SEGMENT_COUNT | category | 9 | 0 | 1 536; 2 50; 3 15; 4 6 |
| FISCAL_YEAR | category | 5 | 0 | 2029 167; 2030 157; 2028 107; 2026 95 |
| CHANNEL_TYPE | category | 2 | 0 | Natural Creek 474; Improved Channel 143 |
| PROJECT_CATEGORY | empty | 1 | 617 |  |
| PROJECT_TYPE | category | 2 | 0 | Debris Removal 474; Restoration 143 |
| NAME | who | 359 | 0 | LEON CREEK 26; Salado Creek 17; SALADO CREEK 15; UNNAMED NATURAL CREEK OF  12 |
| UPPER_LIMIT | other | 514 | 0 | Edgemont Dr 5; Dover Ridge 5; Judson Rd 5; Nacogdoches Rd 4 |
| LOWER_LIMIT | other | 476 | 0 | LEON CREEK 9; SALADO CREEK 8; N Loop 1604 W Access Rd 6; Ray Ellison Blvd 5 |
| WATERSHED | category | 8 | 318 | Salado 85; Leon 79; San Antonio 42; SW 31 |
| COUNCIL_DISTRICT | category | 10 | 0 | 8 113; 9 81; 10 78; 2 78 |
| ESTIMATED_TOTAL_COST | amount | 418 | 0 | 24005.0537 6; 24242.4242 6; 39014.3737 6; 8662.8165 6 |
| SCHEDULE_START | date | 81 | 521 | 10/1/2025 6:00:00 AM 5; 9/1/2026 6:00:00 AM 3; 2/11/2026 6:00:00 AM 2; 6/2/2026 6:00:00 AM 2 |
| SCHEDULE_FINISH | date | 83 | 521 | 11/21/2025 6:00:00 AM 3; 9/30/2026 6:00:00 AM 3; 5/20/2026 6:00:00 AM 3; 7/10/2026 6:00:00 AM 2 |
| ACTUAL_START | date | 72 | 539 | 10/7/2025 6:00:00 AM 2; 1/22/2026 6:00:00 AM 2; 3/18/2026 6:00:00 AM 2; 4/1/2026 6:00:00 AM 2 |
| ACTUAL_FINISH | date | 63 | 541 | 5/26/2026 6:00:00 AM 3; 3/30/2026 6:00:00 AM 3; 2/26/2026 6:00:00 AM 2; 11/21/2025 6:00:00 AM 2 |
| PERCENT_COMPLETE | category | 4 | 539 | 100 76; 50 1; 40 1 |
| PROJECT_MANAGER | category | 7 | 521 | Maria Diaz 66; Xavier Gonzales 15; Luis Garcia 6; Daniel Villasenor 6 |
| CONTACT | category | 4 | 521 | Maria Diaz: (210) 207-503 65; David Gonzales: (210) 207 30; 0 1 |
| CLASSIFICATION | empty | 1 | 617 |  |
| INSIDE_X | amount | 555 | 0 | 2151438.26634714 4; 2161558.05799676 4; 2163479.82754713 4; 2144184.61814701 4 |
| INSIDE_Y | amount | 569 | 0 | 13744053.6030148 4; 13750407.5226146 4; 13753975.2733699 4; 13754295.5891839 4 |
| SHAPE__LENGTH | amount | 560 | 0 | 865.662912419451 4; 3468.38696634361 4; 5730.6625376786 4; 1211.7749790374 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:44:40.04103 617 |
| SOURCE_RUN_ID | audit | 1 | 0 | b3b62177-3d14-4024-a44e-3 617 |
| SRC_SHA256 | who | 1 | 0 | 9d3b4ef6885addc6e39969e44 617 |
