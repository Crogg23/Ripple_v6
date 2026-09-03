# PORTAL_SOC_UTAH_OPEN_DATA_P_447082E18E

rows 117  columns 9  scan 2.9s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 108.4K | 60.59M | 666.43M | 1.07B | 15.33B |
| AVERAGE_MONTHLY_WAGE | 117 | 848 | 2.6K | 5.6K | 6.1K | 314.0K |

## who

SRC_SHA256 by rows
       117  180835666af4f538d0170d7721dffdea1ea7f343b004c3d8dce0bdea2851e109

SRC_SHA256 by dollars
      15.33B      117 rows  180835666af4f538d0170d7721dffdea1ea7f343b004c3d8dce0bdea2851

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  180835666af4f538d0170d7721dffdea1ea7f343  2026:15.33B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 113 | 0 | 136 2; 101469 2; 22139 2; 50153 2 |
| ESTABLISHMENTS | other | 108 | 0 | 105 2; 158 2; 73 2; 1578 2 |
| PAYROLL | amount | 112 | 0 | 1079521 2; 657591788 2; 239831780 2; 566769921 2 |
| AVERAGE_MONTHLY_WAGE | amount | 113 | 0 | 2646 2; 2160 2; 3611 2; 3767 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:38:18.55981 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 91821b25-c50d-47b9-b844-1 117 |
| SRC_SHA256 | who | 1 | 0 | 180835666af4f538d0170d772 117 |
