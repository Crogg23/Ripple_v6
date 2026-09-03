# PORTAL_SOC_UTAH_OPEN_DATA_P_49602BAEC5

rows 118  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 136.3K | 64.50M | 847.51M | 1.08B | 16.60B |
| AVERAGE_MONTHLY_WAGE | 118 | 881 | 2.7K | 5.7K | 8.2K | 338.9K |

## who

SRC_SHA256 by rows
       118  6f361b6808f0c6f929668fdfc8a6244ba0a3fd0c986153e4799410cb6cc3e145

SRC_SHA256 by dollars
      16.60B      118 rows  6f361b6808f0c6f929668fdfc8a6244ba0a3fd0c986153e4799410cb6cc3

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  6f361b6808f0c6f929668fdfc8a6244ba0a3fd0c  2026:16.60B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 113 | 0 | 131 2; 119137 2; 20797 2; 51136 2 |
| ESTABLISHMENTS | other | 106 | 0 | 105 2; 30 2; 1764 2; 427 2 |
| PAYROLL | amount | 114 | 0 | 984150 2; 847509647 2; 241443573 2; 595007207 2 |
| AVERAGE_MONTHLY_WAGE | amount | 115 | 0 | 2504 2; 2371 2; 3870 2; 3879 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:38:52.78437 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 297fd5f6-c4d0-4ef0-b3d2-9 118 |
| SRC_SHA256 | who | 1 | 0 | 6f361b6808f0c6f929668fdfc 118 |
