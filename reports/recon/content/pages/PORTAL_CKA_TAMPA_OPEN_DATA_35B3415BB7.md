# PORTAL_CKA_TAMPA_OPEN_DATA_35B3415BB7

rows 4.8K  columns 13  scan 3.2s

roles: amount 1, audit 2, category 2, date 2, empty 2, id 1, other 2, who 2

## when

DATE
  2020       446  ##############
  2021       572  #################
  2022       627  ###################
  2023       981  ##############################
  2024       951  #############################
  2025       839  ##########################
  2026       351  ###########

INGESTED_AT
  2026      4.8K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 4.8K | 0 | 0 | 28 | 177 | 8.7K |

## who

C_ORGANIZATION by rows
      4.8K  Human Resources

C_ORGANIZATION by dollars
        8.7K     4.8K rows  Human Resources

SRC_SHA256 by rows
      4.8K  d5b4970e53b0a6e475c681edf50c47092cfa845287506e4806bc0550bab6f9b0

SRC_SHA256 by dollars
        8.7K     4.8K rows  d5b4970e53b0a6e475c681edf50c47092cfa845287506e4806bc0550bab6

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Human Resources                           2020:1.5K 2021:1.5K 2022:2.0K 2023:1.5K 2024:1.0K 2025:771 2026:366

SRC_SHA256 by DATE, dollars = VALUE
  d5b4970e53b0a6e475c681edf50c47092cfa8452  2020:1.5K 2021:1.5K 2022:2.0K 2023:1.5K 2024:1.0K 2025:771 2026:366

## what

CHARTNAME: HR Hires by Dept by Month 50%, HR Terminations by Dept by Mon 39%, HR Terms within 180 Days by De 11%

CATEGORY: P&R-Parks & Recreation Dept 9%, SW-Solid Waste Dept 9%, MOB-Mobility Dept 9%, TPD-Police Dept 9%, HR-Human Resources Dept 8%, TFR-Fire Rescue Dept 8%, LAM-Logistics and Asset Manage 8%, WTR-Water Dept 8%, WW-Wastewater Dept 8%, LEGAL-Legal Dept 8%, CC&T-Convention Center & Touri 8%, NCA-Neighborhood & Community A 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 4.9K | 0 | 21064 24; 21063 24; 21062 24; 21061 24 |
| C_ORGANIZATION | who | 1 | 0 | Human Resources 4.8K |
| CHARTNAME | category | 3 | 0 | HR Hires by Dept by Month 2.4K; HR Terminations by Dept b 1.8K; HR Terms within 180 Days  546 |
| DESCRIPTION | empty | 1 | 4.8K |  |
| CATEGORY | category | 35 | 0 | P&R-Parks & Recreation De 171; SW-Solid Waste Dept 168; MOB-Mobility Dept 167; TPD-Police Dept 166 |
| SUMMARY | other | 1 | 0 | Total 4.8K |
| TYPEDATA | other | 1 | 0 | Date 4.8K |
| DATE | date | 99 | 0 | 12/01/2024 00:00:00 103; 03/01/2024 00:00:00 103; 12/01/2023 00:00:00 103; 09/01/2024 00:00:00 101 |
| PERIOD | empty | 1 | 4.8K |  |
| VALUE | amount | 63 | 0 | 0.000 2.9K; 1.000 793; 2.000 372; 3.000 189 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:33:09.12971 4.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5b20f770-85dd-437c-920c-f 4.8K |
| SRC_SHA256 | who | 1 | 0 | d5b4970e53b0a6e475c681edf 4.8K |
