# PORTAL_CKA_TAMPA_OPEN_DATA_08860F4F6E

rows 3.0K  columns 13  scan 2.8s

roles: amount 1, audit 2, category 5, date 2, empty 1, other 2, who 1

## when

DATE
  2018         5  
  2019       211  #############
  2020       328  ####################
  2021       404  ########################
  2022       496  ##############################
  2023       467  ############################
  2024       458  ############################
  2025       458  ############################
  2026       206  ############

INGESTED_AT
  2026      3.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 3.0K | -135 | 25 | 73.6K | 1.68M | 13.61M |

## who

SRC_SHA256 by rows
      3.0K  5835c8fb8ab3f4ce827732ddd25110db8e7ca9ea4f4c0b4720278a29cc735b60

SRC_SHA256 by dollars
      13.61M     3.0K rows  5835c8fb8ab3f4ce827732ddd25110db8e7ca9ea4f4c0b4720278a29cc73

## who x when

SRC_SHA256 by DATE, dollars = VALUE
  5835c8fb8ab3f4ce827732ddd25110db8e7ca9ea  2018:397.94 2019:174.8K 2020:379.2K 2021:994.4K 2022:2.67M 2023:3.38M 2024:2.25M 2025:3.03M 2026:727.4K

## what

C_ORGANIZATION: Mobility 91%, Mobility (Public Works and Uti 9%

CHARTNAME: Mobility Transportation Cut Ou 18%, Mobility Street Miles Resurfac 13%, Mobility Stormwater Active/Pla 12%, Mobility Stormwater Spray/Mow  6%, Mobility Stormwater Pipes Insp 6%, Mobility Stormwater Ditches In 6%, Mobility Stormwater Inlets Ins 6%, Mobility Stormwater Street Swe 6%, Mobility Transportation Edge O 6%, Mobility Transportation Nuisan 6%, Mobility Transportation Pothol 6%, Mobility Transportation Refurb 6%

CATEGORY: Total 17%, Each 15%, Sq. Ft. 14%, Miles Maintained & Inspected 11%, DAYS 5%, Inlets Inspected 5%, Days Ahead of Goal 5%, Square Feet Repaired 5%, REPAIRS 5%, Number Repaired 5%, Markings Refurbished 5%, Number of Signs 5%

TYPEDATA: Date 99%, Period 1%

PERIOD: 2020 17%, FY-2023 13%, FY-2022 13%, FY-2021 13%, FY-2026 9%, FY-2025 9%, FY-2024 9%, YTD  2026 4%, 2025 4%, 2024 4%, 2023 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 2.7K | 0 | 21268 16; 21266 16; 21265 16; 21261 16 |
| C_ORGANIZATION | category | 2 | 0 | Mobility 2.8K; Mobility (Public Works an 263 |
| CHARTNAME | category | 47 | 0 | Mobility Transportation C 262; Mobility Street Miles Res 184; Mobility Stormwater Activ 176; Mobility Stormwater Spray 92 |
| DESCRIPTION | empty | 2 | 3.0K |  |
| CATEGORY | category | 41 | 0 | Total 290; Each 254; Sq. Ft. 234; Miles Maintained & Inspec 180 |
| SUMMARY | other | 1 | 0 | Total 3.0K |
| TYPEDATA | category | 2 | 0 | Date 3.0K; Period 30 |
| DATE | date | 136 | 0 | 04/01/2022 00:00:00 46; 09/01/2022 00:00:00 45; 11/01/2021 00:00:00 44; 06/01/2022 00:00:00 43 |
| PERIOD | category | 19 | 3.0K | 2020 4; FY-2023 3; FY-2022 3; FY-2021 3 |
| VALUE | amount | 1.3K | 0 | 0.000 283; 1.000 100; 28.000 94; 2.000 87 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:29:29.38232 3.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c4368d4c-751b-400f-bf3e-0 3.0K |
| SRC_SHA256 | who | 1 | 0 | 5835c8fb8ab3f4ce827732ddd 3.0K |
