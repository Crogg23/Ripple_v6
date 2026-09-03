# PORTAL_SOC_UTAH_OPEN_DATA_P_55B6E45F3F

rows 118  columns 9  scan 3.9s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 155.0K | 66.48M | 951.02M | 1.21B | 18.67B |
| AVERAGE_MONTHLY_WAGE | 118 | 910 | 3.1K | 7.5K | 8.4K | 374.8K |

## who

SRC_SHA256 by rows
       118  6d7dd9275ccf295a54cc624c31a8f5bc9ec6b3112cb38e835e45e092a959b5b6

SRC_SHA256 by dollars
      18.67B      118 rows  6d7dd9275ccf295a54cc624c31a8f5bc9ec6b3112cb38e835e45e092a959

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  6d7dd9275ccf295a54cc624c31a8f5bc9ec6b311  2026:18.67B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 109 | 0 | 152 2; 126005 2; 20966 2; 52783 2 |
| ESTABLISHMENTS | other | 109 | 0 | 21 3; 126 2; 30 2; 1853 2 |
| PAYROLL | amount | 114 | 0 | 1617009 2; 864040782 2; 277393346 2; 751754857 2 |
| AVERAGE_MONTHLY_WAGE | amount | 113 | 0 | 3546 2; 2286 2; 4410 2; 4747 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:16.50187 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 03cc52b2-b22c-4a4f-bfa9-8 118 |
| SRC_SHA256 | who | 1 | 0 | 6d7dd9275ccf295a54cc624c3 118 |
