# PORTAL_SOC_UTAH_OPEN_DATA_P_7DACFB4113

rows 116  columns 9  scan 3.4s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 293.7K | 79.80M | 1.22B | 1.28B | 21.21B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.3K | 6.3K | 6.4K | 389.8K |

## who

SRC_SHA256 by rows
       116  1bb702ba3313e06f5702baa59c75793285a3cac7df378ae20d97d37b5b6979ee

SRC_SHA256 by dollars
      21.21B      116 rows  1bb702ba3313e06f5702baa59c75793285a3cac7df378ae20d97d37b5b69

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  1bb702ba3313e06f5702baa59c75793285a3cac7  2026:21.21B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 47 2; 120210 2; 19449 2; 64449 2 |
| ESTABLISHMENTS | other | 108 | 0 | 46 2; 34 2; 155 2; 2149 2 |
| PAYROLL | amount | 113 | 0 | 461633 2; 979863540 2; 291559349 2; 897075161 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 3274 2; 2717 2; 4997 2; 4640 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:44:04.73781 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | db8829d4-1a4b-4497-be4d-3 116 |
| SRC_SHA256 | who | 1 | 0 | 1bb702ba3313e06f5702baa59 116 |
