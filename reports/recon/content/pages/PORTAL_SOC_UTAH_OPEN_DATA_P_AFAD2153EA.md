# PORTAL_SOC_UTAH_OPEN_DATA_P_AFAD2153EA

rows 118  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 193.1K | 68.35M | 938.46M | 1.27B | 19.24B |
| AVERAGE_MONTHLY_WAGE | 118 | 980 | 3.0K | 7.6K | 7.8K | 381.6K |

## who

SRC_SHA256 by rows
       118  5d268649194859f1514940be3b33f056ee16ae6d6391bc1d42e66538cb44359b

SRC_SHA256 by dollars
      19.24B      118 rows  5d268649194859f1514940be3b33f056ee16ae6d6391bc1d42e66538cb44

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  5d268649194859f1514940be3b33f056ee16ae6d  2026:19.24B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 115 | 0 | 244 2; 129416 2; 19075 2; 58857 2 |
| ESTABLISHMENTS | other | 110 | 0 | 198 3; 1960 2; 456 2; 9634 2 |
| PAYROLL | amount | 112 | 0 | 2181851 2; 866187427 2; 278228927 2; 737636839 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 2981 2; 2231 2; 4862 2; 4178 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:21.30458 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | bdda9d07-93e0-471f-88ce-a 118 |
| SRC_SHA256 | who | 1 | 0 | 5d268649194859f1514940be3 118 |
