# PORTAL_CKA_TAMPA_OPEN_DATA_33F54DB74C

rows 1.6K  columns 13  scan 3.6s

roles: amount 1, audit 2, category 5, date 2, empty 1, id 1, who 2

## when

DATE
  2019        87  ###########
  2020       213  ############################
  2021       232  ##############################
  2022       232  ##############################
  2023       231  ##############################
  2024       231  ##############################
  2025       232  ##############################
  2026       113  ###############

INGESTED_AT
  2026      1.6K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 1.6K | 0 | 24.3K | 1.05M | 1.49M | 228.72M |

## who

C_ORGANIZATION by rows
      1.6K  Solid Waste Department

C_ORGANIZATION by dollars
     228.72M     1.6K rows  Solid Waste Department

SRC_SHA256 by rows
      1.6K  ea41e9aae56a97e45cf8f58783e2155ed93b6298a3eb62fcf48a4cff8495b744

SRC_SHA256 by dollars
     228.72M     1.6K rows  ea41e9aae56a97e45cf8f58783e2155ed93b6298a3eb62fcf48a4cff8495

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Solid Waste Department                    2019:15.81M 2020:27.13M 2021:30.13M 2022:39.96M 2023:41.74M 2024:30.35M 2025:27.77M 2026:15.83M

SRC_SHA256 by DATE, dollars = VALUE
  ea41e9aae56a97e45cf8f58783e2155ed93b6298  2019:15.81M 2020:27.13M 2021:30.13M 2022:39.96M 2023:41.74M 2024:30.35M 2025:27.77M 2026:15.83M

## what

CHARTNAME: Solid Waste Number of Active A 19%, Solid Waste Carbon Emissions R 17%, Solid Waste Fuel Savings 17%, Solid Waste McKay Bay Equivale 15%, Solid Waste McKay Bay Homes Po 5%, Solid Waste McKay Bay Homes Po 5%, Solid Waste Recycling Tonnage  5%, Solid Waste Percent On Time Re 5%, Solid Waste Percent On Time Co 5%, Solid Waste Code Enforcement V 4%, Solid Waste Resource Managemen 2%, Solid Waste Recycling Tonnage  1%

CATEGORY: Percent On Time 14%, REDUCTION 8%, CNG 8%, DIESEL 8%, EQUIVALENT DIESEL COST 8%, CNG COST SAVINGS 8%, ACTUAL CNG COST 8%, Revenue 7%, Homes Powered 7%, COAL EQUIVALENT TONS 7%, OIL EQUIVALENT BARRELS 7%, WASTE TONS PROCESSED 7%

SUMMARY: Total 95%, Percent 5%

TYPEDATA: Date 98%, Period 2%

PERIOD: 2026 10%, 2025 10%, 2024 10%, 2023 10%, 2022 10%, 2021 10%, 2020 10%, 2018 10%, 2019 10%, FY-2026 3%, FY-2025 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 1.6K | 0 | 21343 8; 21342 8; 21341 8; 21340 8 |
| C_ORGANIZATION | who | 1 | 0 | Solid Waste Department 1.6K |
| CHARTNAME | category | 12 | 0 | Solid Waste Number of Act 304; Solid Waste Carbon Emissi 267; Solid Waste Fuel Savings 264; Solid Waste McKay Bay Equ 243 |
| DESCRIPTION | empty | 1 | 1.6K |  |
| CATEGORY | category | 22 | 0 | Percent On Time 151; REDUCTION 89; CNG 89; DIESEL 89 |
| SUMMARY | category | 2 | 0 | Total 1.5K; Percent 75 |
| TYPEDATA | category | 2 | 0 | Date 1.5K; Period 36 |
| DATE | date | 117 | 0 | 02/01/2026 00:00:00 20; 03/01/2026 00:00:00 19; 01/01/2026 00:00:00 19; 12/01/2025 00:00:00 19 |
| PERIOD | category | 19 | 1.5K | 2026 3; 2025 3; 2024 3; 2023 3 |
| VALUE | amount | 1.3K | 0 | 99.980 43; 99.990 33; 99.970 32; 0.000 29 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:26:36.48675 1.6K |
| SOURCE_RUN_ID | audit | 1 | 0 | d4b2e2a0-3f1e-4125-b2e7-3 1.6K |
| SRC_SHA256 | who | 1 | 0 | ea41e9aae56a97e45cf8f5878 1.6K |
