# PORTAL_SOC_UTAH_OPEN_DATA_P_645B93D1C3

rows 117  columns 9  scan 3.1s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 26.8K | 86.84M | 1.43B | 1.50B | 24.70B |
| AVERAGE_MONTHLY_WAGE | 117 | 1.1K | 3.6K | 8.4K | 9.2K | 441.0K |

## who

SRC_SHA256 by rows
       117  d5160eeeabad8837613733cf38b3acecc282e2f43398e2f351509c0568abee68

SRC_SHA256 by dollars
      24.70B      117 rows  d5160eeeabad8837613733cf38b3acecc282e2f43398e2f351509c0568ab

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  d5160eeeabad8837613733cf38b3acecc282e2f4  2026:24.70B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 38 2; 148024 2; 18730 2; 70344 2 |
| ESTABLISHMENTS | other | 106 | 0 | 532 3; 45 2; 683 2; 2259 2 |
| PAYROLL | amount | 110 | 0 | 445316 2; 1199814930 2; 349481424 2; 1234142978 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 3906 2; 2702 2; 6220 2; 5848 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:47:27.08086 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0cb8aea2-9b7f-4550-a584-1 117 |
| SRC_SHA256 | who | 1 | 0 | d5160eeeabad8837613733cf3 117 |
