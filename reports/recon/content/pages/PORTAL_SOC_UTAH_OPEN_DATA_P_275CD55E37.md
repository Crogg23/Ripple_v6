# PORTAL_SOC_UTAH_OPEN_DATA_P_275CD55E37

rows 118  columns 9  scan 3.4s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 215.7K | 60.60M | 759.78M | 1.04B | 15.37B |
| AVERAGE_MONTHLY_WAGE | 118 | 799 | 2.8K | 6.0K | 6.8K | 337.7K |

## who

SRC_SHA256 by rows
       118  142389d07a59205713c3b5d3ab885dc4046b3e68e5802a930ded86f2054993ab

SRC_SHA256 by dollars
      15.37B      118 rows  142389d07a59205713c3b5d3ab885dc4046b3e68e5802a930ded86f20549

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  142389d07a59205713c3b5d3ab885dc4046b3e68  2026:15.37B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 100 2; 5507 2; 121277 2; 20442 2 |
| ESTABLISHMENTS | other | 108 | 0 | 48 3; 87 2; 1655 2; 417 2 |
| PAYROLL | amount | 113 | 0 | 1394944 2; 759780771 2; 234712227 2; 551370214 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 4650 2; 2088 2; 1576 2; 3827 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:48:42.26749 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 981c14fc-465e-4544-b9f5-9 118 |
| SRC_SHA256 | who | 1 | 0 | 142389d07a59205713c3b5d3a 118 |
