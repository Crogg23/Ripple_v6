# PORTAL_SOC_UTAH_OPEN_DATA_P_2FDF78BD22

rows 117  columns 9  scan 2.7s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 132.4K | 61.71M | 819.09M | 1.09B | 16.61B |
| AVERAGE_MONTHLY_WAGE | 117 | 761 | 2.8K | 6.4K | 7.5K | 340.6K |

## who

SRC_SHA256 by rows
       117  3a806c51373a561fe8758b83a19b4c1dabdbd113074c1985fb92e57833f4fbdd

SRC_SHA256 by dollars
      16.61B      117 rows  3a806c51373a561fe8758b83a19b4c1dabdbd113074c1985fb92e57833f4

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  3a806c51373a561fe8758b83a19b4c1dabdbd113  2026:16.61B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 109 | 0 | 161 2; 120683 2; 21111 2; 50168 2 |
| ESTABLISHMENTS | other | 108 | 0 | 328 3; 112 2; 1641 2; 429 2 |
| PAYROLL | amount | 112 | 0 | 1409263 2; 763561250 2; 250459976 2; 649479650 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 2918 2; 2109 2; 3955 2; 4315 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:37:59.32189 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 17d5cc5a-371c-4ec1-978f-9 117 |
| SRC_SHA256 | who | 1 | 0 | 3a806c51373a561fe8758b83a 117 |
