# PORTAL_SOC_UTAH_OPEN_DATA_P_27F4752A1B

rows 117  columns 9  scan 2.7s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 7.3K | 84.96M | 1.30B | 1.44B | 23.90B |
| AVERAGE_MONTHLY_WAGE | 117 | 815 | 3.6K | 7.4K | 8.0K | 420.8K |

## who

SRC_SHA256 by rows
       117  b7a9f6524963d2bf6b4e605b8467dee1ee5f8b619e36cd10bea42fcbf3b10b9f

SRC_SHA256 by dollars
      23.90B      117 rows  b7a9f6524963d2bf6b4e605b8467dee1ee5f8b619e36cd10bea42fcbf3b1

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  b7a9f6524963d2bf6b4e605b8467dee1ee5f8b61  2026:23.90B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 54 2; 130348 2; 19368 2; 72953 2 |
| ESTABLISHMENTS | other | 110 | 0 | 34 3; 2310 2; 568 2; 11821 2 |
| PAYROLL | amount | 110 | 0 | 628513 2; 1070571551 2; 323707385 2; 1080874215 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 3880 2; 2738 2; 5571 2; 4939 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:39:34.30689 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 980008c0-0f55-4869-9a70-b 117 |
| SRC_SHA256 | who | 1 | 0 | b7a9f6524963d2bf6b4e605b8 117 |
