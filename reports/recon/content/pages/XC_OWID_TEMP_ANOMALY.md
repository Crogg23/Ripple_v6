# XC_OWID_TEMP_ANOMALY

rows 531  columns 9  scan 3.0s

roles: amount 3, audit 2, category 2, other 1, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AVERAGE | 531 | -0.35 | 0.18 | 1.60 | 1.92 | 164.56 |
| LOWER_BOUND | 531 | -0.60 | 0.09 | 1.50 | 1.87 | 107.07 |
| UPPER_BOUND | 531 | -0.14 | 0.30 | 1.64 | 1.97 | 222.26 |

## who

SRC_SHA256 by rows
       531  aa920d646fe20b89b75229ad0fcfce49500cbd2a5f5cccaa92c7c9cbc07a73b8

SRC_SHA256 by dollars
      164.56      531 rows  aa920d646fe20b89b75229ad0fcfce49500cbd2a5f5cccaa92c7c9cbc07a

## what

ENTITY: World 33%, Southern Hemisphere 33%, Northern Hemisphere 33%

CODE: OWID_WRL 33%, OWID_SH 33%, OWID_NH 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | category | 3 | 0 | World 177; Southern Hemisphere 177; Northern Hemisphere 177 |
| CODE | category | 3 | 0 | OWID_WRL 177; OWID_SH 177; OWID_NH 177 |
| YEAR | other | 178 | 0 | 2026 3; 2025 3; 2024 3; 2023 3 |
| AVERAGE | amount | 540 | 0 | 1.3962804 3; 1.4137621 3; 1.5334455 3; 1.4737644 3 |
| LOWER_BOUND | amount | 529 | 0 | 1.2677863 3; 1.3743255 3; 1.4942731 3; 1.4368042 3 |
| UPPER_BOUND | amount | 534 | 0 | 1.5247746 3; 1.4531987 3; 1.5726179 3; 1.5107247 3 |
| INGESTED_AT | audit | 1 | 0 | 1782616839871243 531 |
| SOURCE_RUN_ID | audit | 1 | 0 | 615c8f28-3c07-4200-8c16-3 531 |
| SRC_SHA256 | who | 1 | 0 | aa920d646fe20b89b75229ad0 531 |
