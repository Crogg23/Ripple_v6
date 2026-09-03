# PORTAL_SOC_UTAH_OPEN_DATA_P_0028F23236

rows 117  columns 9  scan 2.7s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 137.0K | 58.42M | 786.02M | 1.04B | 15.48B |
| AVERAGE_MONTHLY_WAGE | 117 | 855 | 2.6K | 5.5K | 5.6K | 322.1K |

## who

SRC_SHA256 by rows
       117  adc059e3e1b0d96896634d0ec6db367fae3ed74083cafb9213be23eb2c5394b3

SRC_SHA256 by dollars
      15.48B      117 rows  adc059e3e1b0d96896634d0ec6db367fae3ed74083cafb9213be23eb2c53

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  adc059e3e1b0d96896634d0ec6db367fae3ed740  2026:15.48B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 57 2; 115586 2; 20886 2; 49483 2 |
| ESTABLISHMENTS | other | 106 | 0 | 67 3; 420 2; 1595 2; 429 2 |
| PAYROLL | amount | 114 | 0 | 658736 2; 786022902 2; 228576477 2; 549543214 2 |
| AVERAGE_MONTHLY_WAGE | amount | 113 | 0 | 3852 2; 1073 2; 2267 2; 3648 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:39:17.43784 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 22e85774-b42c-4319-9db7-5 117 |
| SRC_SHA256 | who | 1 | 0 | adc059e3e1b0d96896634d0ec 117 |
