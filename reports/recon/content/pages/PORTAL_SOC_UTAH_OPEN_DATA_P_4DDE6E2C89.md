# PORTAL_SOC_UTAH_OPEN_DATA_P_4DDE6E2C89

rows 116  columns 9  scan 2.9s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 268.9K | 79.45M | 1.17B | 1.29B | 21.47B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.2K | 7.4K | 8.1K | 387.4K |

## who

SRC_SHA256 by rows
       116  521bfff1bb66f63d01041111b358708294e712808fd32bc7726aa342d0382a59

SRC_SHA256 by dollars
      21.47B      116 rows  521bfff1bb66f63d01041111b358708294e712808fd32bc7726aa342d038

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  521bfff1bb66f63d01041111b358708294e71280  2026:21.47B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 110 | 0 | 46 2; 132273 2; 19511 2; 65451 2 |
| ESTABLISHMENTS | other | 105 | 0 | 45 3; 2126 2; 485 2; 10633 2 |
| PAYROLL | amount | 110 | 0 | 400556 2; 1141519009 2; 282745655 2; 961301618 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 2903 2; 2877 2; 4831 2; 4896 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:45:36.46668 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | b14b450f-ce1a-45a6-841e-7 116 |
| SRC_SHA256 | who | 1 | 0 | 521bfff1bb66f63d01041111b 116 |
