# PORTAL_SOC_UTAH_OPEN_DATA_P_6679F2DEDB

rows 118  columns 9  scan 3.3s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 165.9K | 60.18M | 816.87M | 1.04B | 15.72B |
| AVERAGE_MONTHLY_WAGE | 118 | 841 | 2.6K | 6.3K | 7.7K | 331.9K |

## who

SRC_SHA256 by rows
       118  c77bc832715f588b5e1f1dd62e3d7fd42a52e1d41fe51af54f29d747aa6c9c60

SRC_SHA256 by dollars
      15.72B      118 rows  c77bc832715f588b5e1f1dd62e3d7fd42a52e1d41fe51af54f29d747aa6c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  c77bc832715f588b5e1f1dd62e3d7fd42a52e1d4  2026:15.72B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 114 | 0 | 94 2; 116852 2; 20368 2; 50003 2 |
| ESTABLISHMENTS | other | 108 | 0 | 86 3; 1658 2; 419 2; 7513 2 |
| PAYROLL | amount | 112 | 0 | 966478 2; 816873269 2; 227991768 2; 561810850 2 |
| AVERAGE_MONTHLY_WAGE | amount | 113 | 0 | 3427 2; 2330 2; 3731 2; 3745 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:48:24.93692 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 526b2aba-f56e-41cc-b060-4 118 |
| SRC_SHA256 | who | 1 | 0 | c77bc832715f588b5e1f1dd62 118 |
