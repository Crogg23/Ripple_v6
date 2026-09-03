# XC_JCS_MEDIANS

rows 102  columns 37  scan 3.7s

roles: amount 29, audit 2, category 2, other 2, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PRESIDENT | 98 | -0.50 | -0.32 | 0.69 | 0.69 | 3.69 |
| HOUSE_MEDIAN | 102 | -0.22 | -0.07 | 0.29 | 0.29 | -0.92 |
| SENATE_MEDIAN | 102 | -0.21 | 0 | 0.28 | 0.28 | -1.72 |
| SC_MEDIAN | 86 | -0.32 | 0.28 | 0.46 | 0.47 | 19.68 |
| CIRCUIT_MEDIAN1 | 86 | -0.37 | -0.27 | 0.53 | 0.53 | -11.07 |
| CIRCUIT_SD1 | 85 | 0.11 | 0.30 | 0.56 | 0.56 | 27.05 |

## who

UNNAMED_0 by rows
         1  69
         1  21
         1  51
         1  44
         1  85
         1  75
         1  83
         1  6
         1  86
         1  18
         1  42
         1  24
         1  99
         1  61
         1  31
         1  13
         1  30
         1  96
         1  45
         1  40

UNNAMED_0 by dollars
        0.29        1 rows  94
        0.29        1 rows  93
        0.28        1 rows  95
        0.28        1 rows  96
        0.27        1 rows  89
        0.27        1 rows  90
        0.26        1 rows  92
        0.26        1 rows  91
        0.26        1 rows  3
        0.26        1 rows  8
        0.26        1 rows  7
        0.26        1 rows  4
        0.23        1 rows  84
        0.23        1 rows  83
        0.21        1 rows  2
        0.21        1 rows  6
        0.21        1 rows  82
        0.21        1 rows  1
        0.21        1 rows  81
        0.21        1 rows  5

_SRC_SHA256 by rows
       102  bbe95c3dd282f4e203bbe3d6f23867550c5871e401933e5c4f359e59da517085

_SRC_SHA256 by dollars
       -0.92      102 rows  bbe95c3dd282f4e203bbe3d6f23867550c5871e401933e5c4f359e59da51

## what

CONGRESS: 118 8%, 117 8%, 116 8%, 115 8%, 114 8%, 113 8%, 112 8%, 111 8%, 110 8%, 109 8%, 108 8%, 107 8%

CIRCUIT_MEDIAN13: NA 58%, 0.557 19%, -0.358 14%, 0.692 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | who | 101 | 0 | 102 1; 101 1; 100 1; 99 1 |
| YEAR | other | 102 | 0 | 1924 2; 2024 1; 2023 1; 2022 1 |
| TERM | other | 89 | 0 | NA 14; 2023 1; 2022 1; 2021 1 |
| CONGRESS | category | 50 | 0 | 118 2; 117 2; 116 2; 115 2 |
| PRESIDENT | amount | 18 | 0 | -0.368000000715256 12; -0.358000010251999 8; 0.693000018596649 8; -0.437999993562698 8 |
| HOUSE_MEDIAN | amount | 46 | 0 | -0.13400000333786 6; -0.160999998450279 4; 0.157999992370605 4; -0.068000003695488 4 |
| SENATE_MEDIAN | amount | 49 | 0 | 0.0719999969005585 4; 0.221000000834465 4; -0.162000000476837 2; 0.0305000003427267 2 |
| SC_MEDIAN | amount | 84 | 0 | NA 16; 0.217386797070503 2; 0.417939573526382 2; 0.278232455253601 1 |
| CIRCUIT_MEDIAN1 | amount | 26 | 0 | NA 16; -0.294 10; -0.265 10; -0.299 8 |
| CIRCUIT_SD1 | amount | 29 | 0 | NA 17; 0.13 10; 0.143 8; 0.532 7 |
| CIRCUIT_MEDIAN2 | amount | 24 | 0 | -0.301 13; 0.419 12; -0.124 10; 0.4 10 |
| CIRCUIT_SD2 | amount | 48 | 0 | 0.396 10; 0.053 10; 0.286 7; 0.493 6 |
| CIRCUIT_MEDIAN3 | amount | 21 | 0 | 0.073 19; -0.108 15; NA 14; -0.551 11 |
| CIRCUIT_SD3 | amount | 48 | 0 | NA 15; 0.191 9; 0.269 4; 0.2 4 |
| CIRCUIT_MEDIAN4 | amount | 26 | 0 | 0.207 18; 0.262 11; NA 9; 0.472 8 |
| CIRCUIT_SD4 | amount | 40 | 0 | 0.375 17; NA 17; 0.383 5; 0.152 5 |
| CIRCUIT_MEDIAN5 | amount | 19 | 0 | NA 42; 0.414 19; -0.043 7; 0.391 5 |
| CIRCUIT_SD5 | amount | 40 | 0 | NA 42; 0.375 6; 0.297 5; 0.348 4 |
| CIRCUIT_MEDIAN6 | amount | 32 | 0 | -0.198 13; -0.069 10; 0.324 6; -0.262 6 |
| CIRCUIT_SD6 | amount | 50 | 0 | NA 9; 0.292 8; 0.308 6; 0.325 6 |
| CIRCUIT_MEDIAN7 | amount | 25 | 0 | 0.099 20; 0.261 10; 0.317 8; -0.115 8 |
| CIRCUIT_SD7 | amount | 40 | 0 | NA 14; 0.464 8; 0.348 5; 0.406 5 |
| CIRCUIT_MEDIAN8 | amount | 29 | 0 | 0.196 13; 0.337 12; 0.222 10; -0.11 7 |
| CIRCUIT_SD8 | amount | 44 | 0 | 0.263 10; NA 9; 0.257 8; 0.352 6 |
| CIRCUIT_MEDIAN9 | amount | 28 | 0 | -0.179 17; 0.162 12; NA 12; 0.096 10 |
| CIRCUIT_SD9 | amount | 50 | 0 | NA 12; 0.031 7; 0.451 5; 0.368 5 |
| CIRCUIT_MEDIAN10 | amount | 18 | 0 | 0.257 18; -0.196 11; 0.259 9; -0.201 8 |
| CIRCUIT_SD10 | amount | 38 | 0 | NA 10; 0.254 9; 0.222 7; 0.399 6 |
| CIRCUIT_MEDIAN11 | amount | 14 | 0 | NA 58; 0.399 9; 0.333 8; -0.118 7 |
| CIRCUIT_SD11 | amount | 25 | 0 | NA 58; 0.368 5; 0.308 5; 0.373 4 |
| CIRCUIT_MEDIAN12 | amount | 18 | 0 | -0.337 18; NA 14; -0.371 11; -0.358 9 |
| CIRCUIT_SD12 | amount | 42 | 0 | NA 15; 0.466 9; 0 7; 0.327 6 |
| CIRCUIT_MEDIAN13 | category | 4 | 0 | NA 59; 0.557 19; -0.358 14; 0.692 10 |
| CIRCUIT_SD13 | amount | 18 | 0 | NA 59; 0 7; 0.507 6; 0.526 5 |
| _INGESTED_AT | audit | 1 | 0 | 1782878874075360 102 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 03917ad5-cd60-4c70-8743-5 102 |
| _SRC_SHA256 | who | 1 | 0 | bbe95c3dd282f4e203bbe3d6f 102 |
