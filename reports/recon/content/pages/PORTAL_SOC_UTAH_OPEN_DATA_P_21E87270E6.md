# PORTAL_SOC_UTAH_OPEN_DATA_P_21E87270E6

rows 118  columns 9  scan 2.6s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 149.8K | 63.28M | 770.86M | 1.05B | 16.03B |
| AVERAGE_MONTHLY_WAGE | 118 | 875 | 2.6K | 6.9K | 7.2K | 344.4K |

## who

SRC_SHA256 by rows
       118  c5e823c0e36ec4b058759d02155ce9ee41d02db18c88faae2d71ef4f553d1c26

SRC_SHA256 by dollars
      16.03B      118 rows  c5e823c0e36ec4b058759d02155ce9ee41d02db18c88faae2d71ef4f553d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  c5e823c0e36ec4b058759d02155ce9ee41d02db1  2026:16.03B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 113 | 0 | 126 2; 123456 2; 20828 2; 50539 2 |
| ESTABLISHMENTS | other | 108 | 0 | 327 3; 93 2; 1726 2; 433 2 |
| PAYROLL | amount | 114 | 0 | 879540 2; 770864765 2; 253924552 2; 578533692 2 |
| AVERAGE_MONTHLY_WAGE | amount | 114 | 0 | 2327 2; 2081 2; 4064 2; 3816 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:37:07.16566 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | bb1ddff0-db58-4368-8513-6 118 |
| SRC_SHA256 | who | 1 | 0 | c5e823c0e36ec4b058759d021 118 |
