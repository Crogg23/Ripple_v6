# PORTAL_CKA_TAMPA_OPEN_DATA_7B31B708C9

rows 104  columns 26  scan 5.1s

roles: amount 1, audit 2, category 5, date 8, empty 3, other 5, who 3

## when

DATE
  2019        13  ###########
  2020        11  ##########
  2021        34  ##############################
  2022        16  ##############
  2023         7  ######
  2024        12  ###########
  2025         8  #######
  2026         3  ###

CUSTOM_DATE_1
  2026       104  ##############################

CUSTOM_DATE_2
  2026       104  ##############################

CUSTOM_DATE_3
  2026       104  ##############################

LAST_UPDATE
  2021        58  ##############################
  2022        15  ########
  2023         8  ####
  2024        12  ######
  2025         8  ####
  2026         3  ##

LAST_UPDATE_COT
  2026       104  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 104 | 0 | 42.7K | 1.18M | 1.46M | 15.57M |

## who

ORGANZIATION by rows
       104  Development & Growth Mgmt

ORGANZIATION by dollars
      15.57M      104 rows  Development & Growth Mgmt

AUTOMATION by rows
       104  Manual

AUTOMATION by dollars
      15.57M      104 rows  Manual

SRC_SHA256 by rows
       104  d219202833458c386975c8c127d6e84a375211b7016b030fb6fbfd9ac5938ba3

SRC_SHA256 by dollars
      15.57M      104 rows  d219202833458c386975c8c127d6e84a375211b7016b030fb6fbfd9ac593

## who x when

ORGANZIATION by DATE, dollars = VALUE
  Development & Growth Mgmt                 2019:1.13M 2020:867.0K 2021:3.47M 2022:1.71M 2023:1.26M 2024:2.15M 2025:4.03M 2026:950.0K

AUTOMATION by DATE, dollars = VALUE
  Manual                                    2019:1.13M 2020:867.0K 2021:3.47M 2022:1.71M 2023:1.26M 2024:2.15M 2025:4.03M 2026:950.0K

## what

CHARTNAME: Owner Occupied Rehab Payments  30%, YTD Quarterly Closing Amount 26%, YTD Quarterly Closing Units 26%, Owner Occupied Rehab by Quarte 18%

DESCRIPTION: Housing and Community Developm 30%, Development & Growth Mgmt; Tot 26%, Total Clients by Fiscal Year a 26%, Housing and Community Developm 18%

CATEGORY: Payments 30%, Amount 26%, Clients 26%, Units 18%

PERIOD: 2025/Q3 9%, 2025/Q2 9%, 2025/Q1 9%, 2024/Q3 9%, 2024/Q2 9%, 2024/Q1 9%, 2023/Q4 9%, 2023/Q3 9%, 2023/Q2 9%, 2023/Q1 9%, 2022/Q4 9%

DATA_TYPE: Integer 69%, Decimal 31%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 102 | 0 | 20610 1; 20609 1; 20608 1; 17490 1 |
| ORGANZIATION | who | 1 | 0 | Development & Growth Mgmt 104 |
| CHARTNAME | category | 4 | 0 | Owner Occupied Rehab Paym 31; YTD Quarterly Closing Amo 27; YTD Quarterly Closing Uni 27; Owner Occupied Rehab by Q 19 |
| DESCRIPTION | category | 4 | 0 | Housing and Community Dev 31; Development & Growth Mgmt 27; Total Clients by Fiscal Y 27; Housing and Community Dev 19 |
| CATEGORY | category | 4 | 0 | Payments 31; Amount 27; Clients 27; Units 19 |
| SUMMARY | other | 1 | 0 | Total 104 |
| PERIOD | category | 48 | 31 | 2025/Q3 2; 2025/Q2 2; 2025/Q1 2; 2024/Q3 2 |
| DATE | date | 83 | 0 | 03/08/2021 08:50:00 4; 02/28/2021 11:11:00 4; 05/10/2022 00:00:00 3; 03/08/2021 08:49:00 3 |
| DATA_TYPE | category | 2 | 0 | Integer 72; Decimal 32 |
| VALUE | amount | 72 | 0 | 7.00 4; 13.00 4; 5.00 4; 21.00 3 |
| AUTOMATION | who | 1 | 0 | Manual 104 |
| CUSTOM_TEXT_1 | empty | 1 | 104 |  |
| CUSTOM_TEXT_2 | empty | 1 | 104 |  |
| CUSTOM_TEXT_3 | empty | 1 | 104 |  |
| CUSTOM_NUMBER_1 | other | 1 | 0 | 0 104 |
| CUSTOM_NUMBER_2 | other | 1 | 0 | 0 104 |
| CUSTOM_NUMBER_3 | other | 1 | 0 | 0 104 |
| CUSTOM_DATE_1 | date | 1 | 0 | 07/02/2026 12:30:36 104 |
| CUSTOM_DATE_2 | date | 1 | 0 | 07/02/2026 12:30:36 104 |
| CUSTOM_DATE_3 | date | 1 | 0 | 07/02/2026 12:30:36 104 |
| LAST_UPDATE | date | 65 | 0 | 03/08/2021 08:50:00 4; 02/28/2021 11:11:00 4; 02/25/2021 12:23:00 4; 02/25/2021 12:22:00 4 |
| LAST_UPDATE_COT | date | 1 | 0 | 07/02/2026 12:30:36 104 |
| LAST_UPDATE_OGI | date | 1 | 0 | 07/02/2026 12:30:36 104 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:15:15.90290 104 |
| SOURCE_RUN_ID | audit | 1 | 0 | 55b4efd0-4167-478c-b6be-0 104 |
| SRC_SHA256 | who | 1 | 0 | d219202833458c386975c8c12 104 |
