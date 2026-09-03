# PORTAL_SOC_UTAH_OPEN_DATA_P_6223211050

rows 117  columns 9  scan 3.7s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 174.5K | 61.76M | 714.99M | 1.04B | 15.37B |
| AVERAGE_MONTHLY_WAGE | 117 | 868 | 2.7K | 5.1K | 6.0K | 318.0K |

## who

SRC_SHA256 by rows
       117  17b6fd8a833e5da49885b0dcfa57efe518d10584a39fb9ef4b833790e72a3fce

SRC_SHA256 by dollars
      15.37B      117 rows  17b6fd8a833e5da49885b0dcfa57efe518d10584a39fb9ef4b833790e72a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  17b6fd8a833e5da49885b0dcfa57efe518d10584  2026:15.37B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 114 | 0 | 112 2; 102820 2; 20983 2; 49079 2 |
| ESTABLISHMENTS | other | 108 | 0 | 88 2; 1627 2; 421 2; 7361 2 |
| PAYROLL | amount | 112 | 0 | 943141 2; 682288209 2; 219260608 2; 534805257 2 |
| AVERAGE_MONTHLY_WAGE | amount | 109 | 0 | 2807 2; 3305 2; 2212 2; 3483 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:44:41.89989 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 557c617c-bda8-4af4-bab3-c 117 |
| SRC_SHA256 | who | 1 | 0 | 17b6fd8a833e5da49885b0dcf 117 |
