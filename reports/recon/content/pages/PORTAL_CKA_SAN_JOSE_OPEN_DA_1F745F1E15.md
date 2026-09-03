# PORTAL_CKA_SAN_JOSE_OPEN_DA_1F745F1E15

rows 581  columns 13  scan 3.4s

roles: amount 2, audit 2, category 2, date 1, empty 2, other 3, who 2

## when

INGESTED_AT
  2026       581  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 581 | 172.91 | 4.1K | 46.7K | 96.9K | 4.52M |
| SHAPE_AREA | 581 | 1.3K | 522.2K | 43.18M | 111.61M | 1.52B |

## who

FACILITYID by rows
         1  156
         1  35
         1  49
         1  66
         1  57
         1  23
         1  78
         1  128
         1  90
         1  143
         1  105
         1  146
         1  117
         1  109
         1  41
         1  15
         1  147
         1  58
         1  48
         1  46

FACILITYID by dollars
       96.9K        1 rows  464
       93.5K        1 rows  118
       89.3K        1 rows  123
       82.2K        1 rows  114
       55.5K        1 rows  93
       46.8K        1 rows  36
       46.7K        1 rows  411
       46.2K        1 rows  449
       42.1K        1 rows  171
       41.2K        1 rows  92
       40.6K        1 rows  65
       39.7K        1 rows  260
       39.5K        1 rows  369
       37.9K        1 rows  90
       37.8K        1 rows  524
       37.1K        1 rows  136
       35.5K        1 rows  119
       35.4K        1 rows  34
       35.1K        1 rows  534
       33.2K        1 rows  73

SRC_SHA256 by rows
       581  959c7f285e5c2720c884b62f1c17d43d8485df05fd92212cb3919208074be780

SRC_SHA256 by dollars
       4.52M      581 rows  959c7f285e5c2720c884b62f1c17d43d8485df05fd92212cb3919208074b

## who x when

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  105                                       2026:5.2K
  109                                       2026:26.7K
  114                                       2026:82.2K
  117                                       2026:24.8K
  118                                       2026:93.5K
  123                                       2026:89.3K
  128                                       2026:14.3K
  143                                       2026:8.6K
  146                                       2026:6.1K
  147                                       2026:3.7K
  15                                        2026:3.2K
  156                                       2026:2.1K
  171                                       2026:42.1K
  23                                        2026:671.86
  35                                        2026:3.8K
  36                                        2026:46.8K
  41                                        2026:620.60
  411                                       2026:46.7K
  449                                       2026:46.2K
  46                                        2026:703.32
  464                                       2026:96.9K
  48                                        2026:16.0K
  49                                        2026:8.9K
  57                                        2026:3.8K
  58                                        2026:7.3K
  66                                        2026:1.3K
  78                                        2026:1.1K
  90                                        2026:37.9K
  92                                        2026:41.2K
  93                                        2026:55.5K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  959c7f285e5c2720c884b62f1c17d43d8485df05  2026:4.52M

## what

SOURCE: Serpentinite Rock 58%, Ultramafic Rock 42%

CONFIDENCELEVEL: Definite 68%, Likely 32%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 571 | 0 | 581 3; 580 3; 579 3; 578 3 |
| FACILITYID | who | 571 | 0 | 566 3; 565 3; 564 3; 563 3 |
| INTID | other | 571 | 0 | 566 3; 565 3; 564 3; 563 3 |
| NATURALASBESTOS | other | 1 | 0 | Yes 581 |
| SOURCE | category | 2 | 0 | Serpentinite Rock 337; Ultramafic Rock 244 |
| CONFIDENCELEVEL | category | 2 | 0 | Definite 396; Likely 185 |
| LASTUPDATE | empty | 1 | 581 |  |
| NOTES | empty | 1 | 581 |  |
| SHAPE_LENGTH | amount | 584 | 0 | 2003.62358318749 3; 6374.0134613552 3; 945.740912869956 3; 1165.95285654583 3 |
| SHAPE_AREA | amount | 586 | 0 | 206871.867669962 3; 773401.138720872 3; 44421.3558892433 3; 84523.173704317 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:43:28.91282 581 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0a3fa688-78dd-4991-afb2-b 581 |
| SRC_SHA256 | who | 1 | 0 | 959c7f285e5c2720c884b62f1 581 |
