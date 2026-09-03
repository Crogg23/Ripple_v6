# PORTAL_SOC_UTAH_OPEN_DATA_P_BF857F3B65

rows 118  columns 9  scan 3.2s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 142.3K | 64.50M | 892.73M | 1.14B | 17.74B |
| AVERAGE_MONTHLY_WAGE | 118 | 930 | 2.8K | 6.4K | 8.6K | 348.6K |

## who

SRC_SHA256 by rows
       118  5c77439b663dc09377213a5b34d72c1753a535baee5c2b2386aa84960b4d0e7f

SRC_SHA256 by dollars
      17.74B      118 rows  5c77439b663dc09377213a5b34d72c1753a535baee5c2b2386aa84960b4d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  5c77439b663dc09377213a5b34d72c1753a535ba  2026:17.74B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 113 | 0 | 201 2; 122719 2; 20872 2; 54681 2 |
| ESTABLISHMENTS | other | 113 | 0 | 144 2; 412 2; 1883 2; 439 2 |
| PAYROLL | amount | 115 | 0 | 1845012 2; 888911284 2; 258099892 2; 645484713 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 3060 3; 2414 2; 4122 2; 3935 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:51:52.93329 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2526d327-22f1-4ff7-9ea9-1 118 |
| SRC_SHA256 | who | 1 | 0 | 5c77439b663dc09377213a5b3 118 |
