# PORTAL_SOC_UTAH_OPEN_DATA_P_F6E04B3D02

rows 116  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 407.8K | 82.82M | 1.16B | 1.50B | 24.07B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.5K | 8.5K | 8.7K | 418.1K |

## who

SRC_SHA256 by rows
       116  1d2ac684e03c4a2a76d8f02e903169617507e1bc4e4babe04a643bdd073e4926

SRC_SHA256 by dollars
      24.07B      116 rows  1d2ac684e03c4a2a76d8f02e903169617507e1bc4e4babe04a643bdd073e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  1d2ac684e03c4a2a76d8f02e903169617507e1bc  2026:24.07B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 114 2; 133868 2; 20622 2; 66741 2 |
| ESTABLISHMENTS | other | 107 | 0 | 122 2; 32 2; 164 2; 2060 2 |
| PAYROLL | amount | 113 | 0 | 1428160 2; 1044870191 2; 334134638 2; 1069104485 2 |
| AVERAGE_MONTHLY_WAGE | amount | 107 | 0 | 4176 2; 4360 2; 2602 2; 5401 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:49:05.47160 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 56554092-06c1-46e0-b887-d 116 |
| SRC_SHA256 | who | 1 | 0 | 1d2ac684e03c4a2a76d8f02e9 116 |
