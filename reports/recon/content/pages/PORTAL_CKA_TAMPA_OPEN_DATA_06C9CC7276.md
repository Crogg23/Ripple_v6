# PORTAL_CKA_TAMPA_OPEN_DATA_06C9CC7276

rows 221  columns 13  scan 3.4s

roles: amount 1, audit 2, category 6, date 2, other 1, who 2

## when

DATE
  2023        48  ###################
  2024        48  ###################
  2025        48  ###################
  2026        77  ##############################

INGESTED_AT
  2026       221  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 221 | -6 | 1.2K | 517.27M | 649.63M | 3.75B |

## who

C_ORGANIZATION by rows
       221  Purchasing

C_ORGANIZATION by dollars
       3.75B      221 rows  Purchasing

SRC_SHA256 by rows
       221  fa2d7ca8076247121b5b8648f7a69d3e70ab0fec18dbbb8d46865580437bdcc8

SRC_SHA256 by dollars
       3.75B      221 rows  fa2d7ca8076247121b5b8648f7a69d3e70ab0fec18dbbb8d46865580437b

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Purchasing                                2023:68.4K 2024:70.7K 2025:68.4K 2026:3.75B

SRC_SHA256 by DATE, dollars = VALUE
  fa2d7ca8076247121b5b8648f7a69d3e70ab0fec  2023:68.4K 2024:70.7K 2025:68.4K 2026:3.75B

## what

CHARTNAME: Warehouse Inventory Issues 76%, Spend by Source 9%, Purchasing Report by Review Ty 6%, Purchasing Report by Review Ty 5%, Inventory Fulfillment by Wareh 2%, REQ to PO Timing 1%

DESCRIPTION: Warehouse Inventory Issues 76%, Spend by Source 9%, Purchasing Report by Review Ty 6%, Purchasing Report by Review Ty 5%, Inventory Fulfillment by Wareh 2%, REQ to PO Timing 1%

CATEGORY: WW1 20%, WT1 20%, MS1 20%, FD1 20%, Purchasing Processing 3%, Buyer Review 3%, Posting Time 2%, Opening To Award 2%, Traditional Solicitation 2%, Sheltered Solicitation 2%, Non Competitive 2%, Cooperative 2%

SUMMARY: Total 85%, Average 13%, Percent 2%

TYPEDATA: Date 77%, Period 23%

PERIOD: FY-21 22%, FY-20 22%, FY-22 13%, 2026 9%, 2025 9%, 2024 9%, 2023 9%, 2022 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 168 | 0 | 3 5; 2 5; 1 5; 4 4 |
| C_ORGANIZATION | who | 1 | 0 | Purchasing 221 |
| CHARTNAME | category | 6 | 0 | Warehouse Inventory Issue 168; Spend by Source 20; Purchasing Report by Revi 14; Purchasing Report by Revi 12 |
| DESCRIPTION | category | 6 | 0 | Warehouse Inventory Issue 168; Spend by Source 20; Purchasing Report by Revi 14; Purchasing Report by Revi 12 |
| CATEGORY | category | 16 | 0 | WW1 43; WT1 43; MS1 43; FD1 43 |
| SUMMARY | category | 3 | 0 | Total 188; Average 29; Percent 4 |
| TYPEDATA | category | 2 | 0 | Date 171; Period 50 |
| DATE | date | 45 | 0 | 07/02/2026 12:31:12 46; 12/01/2025 00:00:00 4; 12/01/2024 00:00:00 4; 12/01/2023 00:00:00 4 |
| PERIOD | category | 9 | 175 | FY-21 10; FY-20 10; FY-22 6; 2026 4 |
| VALUE | amount | 206 | 0 | 374.00 3; 420.00 3; 15.00 3; 100.00 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:17:34.79088 221 |
| SOURCE_RUN_ID | audit | 1 | 0 | 64458928-3335-4e3f-aa94-3 221 |
| SRC_SHA256 | who | 1 | 0 | fa2d7ca8076247121b5b8648f 221 |
