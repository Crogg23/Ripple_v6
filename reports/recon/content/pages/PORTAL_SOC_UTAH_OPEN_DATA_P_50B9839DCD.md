# PORTAL_SOC_UTAH_OPEN_DATA_P_50B9839DCD

rows 117  columns 9  scan 3.0s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 12.3K | 84.62M | 1.30B | 1.47B | 24.14B |
| AVERAGE_MONTHLY_WAGE | 117 | 1.2K | 3.6K | 10.6K | 11.7K | 452.5K |

## who

SRC_SHA256 by rows
       117  629312ed69a39a388315f81ba0696a574a81c2bb4334066ef0126d992bd86111

SRC_SHA256 by dollars
      24.14B      117 rows  629312ed69a39a388315f81ba0696a574a81c2bb4334066ef0126d992bd8

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  629312ed69a39a388315f81ba0696a574a81c2bb  2026:24.14B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 108 | 0 | 30 2; 148659 2; 18996 2; 70438 2 |
| ESTABLISHMENTS | other | 106 | 0 | 40 2; 2255 2; 539 2; 11338 2 |
| PAYROLL | amount | 114 | 0 | 323033 2; 1141159194 2; 417517120 2; 1082940089 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 3589 2; 2559 2; 7326 2; 5125 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:45:08.41293 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | a7a26fb5-f85f-4688-950e-8 117 |
| SRC_SHA256 | who | 1 | 0 | 629312ed69a39a388315f81ba 117 |
