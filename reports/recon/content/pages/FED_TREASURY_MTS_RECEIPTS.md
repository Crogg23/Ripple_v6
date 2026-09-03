# FED_TREASURY_MTS_RECEIPTS

rows 7.5K  columns 30  scan 4.7s

roles: amount 5, audit 2, category 9, date 1, id 2, other 9, who 2

## when

RECORD_DATE
  2015       528  ########################
  2016       649  #############################
  2017       664  ##############################
  2018       664  ##############################
  2019       664  ##############################
  2020       664  ##############################
  2021       664  ##############################
  2022       664  ##############################
  2023       664  ##############################
  2024       664  ##############################
  2025       664  ##############################
  2026       337  ###############

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CURRENT_MONTH_GROSS_RCPT_AMT | 5.4K | 2.8K | 3.93B | 438.95B | 946.12B | 227806.67B |
| CURRENT_MONTH_REFUND_AMT | 2.3K | 287.17 | 59.14M | 76.94B | 108.78B | 12372.91B |
| CURRENT_MONTH_NET_RCPT_AMT | 5.0K | 2.8K | 3.51B | 403.94B | 863.65B | 189010.43B |
| CURRENT_FYTD_REFUND_AMT | 2.4K | 2.9K | 286.01M | 346.20B | 451.22B | 79242.52B |
| PRIOR_FYTD_REFUND_AMT | 2.4K | 2.9K | 259.87M | 329.64B | 447.40B | 76554.35B |

## who

CLASSIFICATION_DESC by rows
       408  Federal Insurance Contributions Act Taxes
       408  Self-Employment Contributions Act Taxes
       303  Adjustments Attributable to Prior Years-FICA
       202  Adjustments Attributable to Prior Years-SECA
       136  Highway Trust Fund
       136  Total -- Other Retirement
       136  Black Lung Disability Trust Fund
       136  Total -- Individual Income Taxes
       136  Corporation Income Taxes
       136  Total -- Federal Old-Age and Survivors Insurance Trust Fund
       136  Total -- On-Budget
       136  Federal Old-Age and Survivors Insurance Trust Fund:
       136  Excise Taxes:
       136  Other Retirement:
       136  Unemployment Insurance:
       136  Miscellaneous Excise Taxes
       136  Total -- Receipts
       136  Railroad Unemployment Taxes
       136  Employment and General Retirement:
       136  Rail Pension and Supplemental Annuity

CLASSIFICATION_DESC by dollars
   50585.38B      136 rows  Total -- Receipts
   38891.18B      136 rows  Total -- On-Budget
   26509.24B      136 rows  Total -- Individual Income Taxes
   17303.77B      136 rows  Withheld
   15956.79B      136 rows  Total -- Social Insurance and Retirement Receipts
   15315.29B      136 rows  Total -- Employment and General Retirement
   14306.76B      408 rows  Federal Insurance Contributions Act Taxes
   11694.20B      136 rows  Total -- Off-Budget
    9879.43B      136 rows  Total -- Federal Old-Age and Survivors Insurance Trust Fund
    9205.18B      136 rows  Other
    4484.11B      136 rows  Corporation Income Taxes
    3556.49B      136 rows  Total -- Federal Hospital Insurance Trust Fund
    1814.77B      136 rows  Total -- Federal Disability Insurance Trust Fund
    1126.24B      136 rows  Total -- Excise Taxes
    1101.64B      136 rows  Total -- Miscellaneous Receipts
    1097.33B      136 rows  Customs Duties
     866.54B      408 rows  Self-Employment Contributions Act Taxes
     684.91B      136 rows  Deposit of Earnings, Federal Reserve System
     576.96B      136 rows  Total -- Unemployment Insurance
     489.28B      136 rows  Highway Trust Fund

SRC_SHA256 by rows
      7.5K  a3d1df1df615c80be7b894f763687ea3b1b852a4a882e3bc74aec9d7c91f8619

SRC_SHA256 by dollars
  227806.67B     7.5K rows  a3d1df1df615c80be7b894f763687ea3b1b852a4a882e3bc74aec9d7c91f

## who x when

CLASSIFICATION_DESC by RECORD_DATE, dollars = CURRENT_MONTH_GROSS_RCPT_AMT
  Adjustments Attributable to Prior Years-  2016:14.81B 2017:5.20B 2018:6.47M 2019:9.70B 2020:12.19B 2021:3.87B 2022:27.61B 2023:42.23B 2024:27.33B 2025:19.16B 2026:21.87M
  Adjustments Attributable to Prior Years-  2016:5.72M 2017:20 2018:108.58M 2019:99.49M 2020:113.70M 2021:288.29M 2022:94.96M 2023:3.40B 2024:2.55B 2025:277.8K 2026:8.83B
  Black Lung Disability Trust Fund          2015:451.10M 2016:446.12M 2017:422.07M 2018:376.20M 2019:172.10M 2020:331.95M 2021:283.64M 2022:166.67M 2023:327.68M 2024:290.02M 2025:230.05M 2026:148.36M
  Corporation Income Taxes                  2015:362.81B 2016:338.63B 2017:329.05B 2018:248.80B 2019:290.34B 2020:273.91B 2021:444.53B 2022:480.02B 2023:500.00B 2024:525.91B 2025:459.08B 2026:231.02B
  Customs Duties                            2015:31.87B 2016:36.09B 2017:36.86B 2018:51.69B 2019:77.48B 2020:73.55B 2021:92.05B 2022:104.40B 2023:83.28B 2024:86.08B 2025:273.81B 2026:150.16B
  Employment and General Retirement:        2015:10 2016:12 2017:12 2018:12 2019:12 2020:12 2021:12 2022:12 2023:12 2024:12 2025:12 2026:6
  Excise Taxes:                             2015:10 2016:12 2017:12 2018:12 2019:12 2020:12 2021:12 2022:12 2023:12 2024:12 2025:12 2026:6
  Federal Insurance Contributions Act Taxe  2015:791.37B 2016:991.65B 2017:1054.44B 2018:1084.21B 2019:1133.45B 2020:1201.73B 2021:1229.34B 2022:1336.57B 2023:1450.96B 2024:1549.18B 2025:1611.51B 2026:872.37B
  Federal Old-Age and Survivors Insurance   2015:10 2016:12 2017:12 2018:12 2019:12 2020:12 2021:12 2022:12 2023:12 2024:12 2025:12 2026:6
  Highway Trust Fund                        2015:31.30B 2016:41.56B 2017:41.62B 2018:43.49B 2019:44.58B 2020:42.53B 2021:41.43B 2022:44.53B 2023:44.86B 2024:44.92B 2025:42.16B 2026:26.33B
  Miscellaneous Excise Taxes                2015:46.85B 2016:44.66B 2017:32.35B 2018:52.13B 2019:32.91B 2020:43.17B 2021:32.51B 2022:37.33B 2023:32.84B 2024:43.48B 2025:40.91B 2026:17.15B
  Other                                     2015:482.21B 2016:550.13B 2017:537.64B 2018:632.62B 2019:633.70B 2020:614.57B 2021:832.30B 2022:1164.24B 2023:887.42B 2024:915.21B 2025:1117.40B 2026:837.74B
  Other Retirement:                         2015:10 2016:12 2017:12 2018:12 2019:12 2020:12 2021:12 2022:12 2023:12 2024:12 2025:12 2026:6
  Rail Pension and Supplemental Annuity     2015:2.66B 2016:3.10B 2017:3.17B 2018:3.34B 2019:3.34B 2020:2.64B 2021:3.08B 2022:3.24B 2023:3.77B 2024:3.84B 2025:3.79B 2026:2.12B
  Railroad Unemployment Taxes               2015:86.38M 2016:119.08M 2017:128.58M 2018:135.29M 2019:128.25M 2020:58.12M 2021:148.34M 2022:324.59M 2023:307.28M 2024:96.53M 2025:33.78M 2026:17.21M
  Self-Employment Contributions Act Taxes   2015:52.70B 2016:61.51B 2017:65.47B 2018:65.05B 2019:67.56B 2020:70.29B 2021:71.57B 2022:77.57B 2023:79.32B 2024:90.32B 2025:90.12B 2026:75.07B
  Total -- Employment and General Retireme  2015:852.86B 2016:1077.36B 2017:1122.20B 2018:1139.80B 2019:1216.93B 2020:1288.95B 2021:1267.58B 2022:1445.12B 2023:1586.10B 2024:1672.37B 2025:1708.18B 2026:937.86B
  Total -- Excise Taxes                     2015:89.57B 2016:101.13B 2017:89.48B 2018:111.02B 2019:93.74B 2020:91.70B 2021:88.54B 2022:95.94B 2023:98.95B 2024:105.11B 2025:106.22B 2026:54.83B
  Total -- Federal Disability Insurance Tr  2015:94.17B 2016:154.60B 2017:164.34B 2018:166.25B 2019:137.45B 2020:143.01B 2021:139.98B 2022:158.42B 2023:176.74B 2024:185.04B 2025:189.14B 2026:105.64B
  Total -- Federal Hospital Insurance Trus  2015:199.49B 2016:249.82B 2017:257.66B 2018:264.33B 2019:281.28B 2020:299.07B 2021:298.18B 2022:348.21B 2023:362.34B 2024:391.23B 2025:397.95B 2026:206.95B
  Total -- Federal Old-Age and Survivors I  2015:554.58B 2016:667.72B 2017:694.88B 2018:703.40B 2019:792.60B 2020:842.57B 2021:824.17B 2022:932.60B 2023:1040.63B 2024:1089.63B 2025:1114.57B 2026:622.08B
  Total -- Individual Income Taxes          2015:1495.91B 2016:1801.39B 2017:1886.96B 2018:1934.63B 2019:1972.81B 2020:1813.06B 2021:2515.62B 2022:2868.18B 2023:2565.36B 2024:2716.30B 2025:3066.48B 2026:1872.55B
  Total -- Miscellaneous Receipts           2015:136.87B 2016:128.82B 2017:124.22B 2018:105.87B 2019:85.99B 2020:126.93B 2021:134.48B 2022:113.46B 2023:35.53B 2024:47.36B 2025:45.45B 2026:16.66B
  Total -- Off-Budget                       2015:648.75B 2016:822.32B 2017:859.22B 2018:869.65B 2019:930.05B 2020:985.58B 2021:964.15B 2022:1091.02B 2023:1217.38B 2024:1274.66B 2025:1303.71B 2026:727.71B
  Total -- On-Budget                        2015:2385.13B 2016:2734.44B 2017:2803.52B 2018:2795.42B 2019:2870.13B 2020:2754.69B 2021:3675.70B 2022:4114.83B 2023:3744.44B 2024:3965.92B 2025:4451.70B 2026:2595.24B
  Total -- Other Retirement                 2015:3.15B 2016:3.97B 2017:4.24B 2018:4.63B 2019:4.86B 2020:5.34B 2021:5.78B 2022:6.28B 2023:7.13B 2024:8.13B 2025:8.58B 2026:4.31B
  Total -- Receipts                         2015:3033.88B 2016:3556.76B 2017:3662.74B 2018:3665.07B 2019:3800.18B 2020:3740.28B 2021:4639.85B 2022:5205.85B 2023:4961.82B 2024:5240.58B 2025:5755.42B 2026:3322.96B
  Total -- Social Insurance and Retirement  2015:898.17B 2016:1129.54B 2017:1172.07B 2018:1189.31B 2019:1262.71B 2020:1341.28B 2021:1336.27B 2022:1509.76B 2023:1642.03B 2024:1728.83B 2025:1771.76B 2026:975.05B
  Unemployment Insurance:                   2015:10 2016:12 2017:12 2018:12 2019:12 2020:12 2021:12 2022:12 2023:12 2024:12 2025:12 2026:6
  Withheld                                  2015:1013.67B 2016:1251.23B 2017:1349.29B 2018:1301.97B 2019:1339.09B 2020:1198.47B 2021:1683.30B 2022:1703.92B 2023:1677.92B 2024:1801.07B 2025:1949.06B 2026:1034.79B

SRC_SHA256 by RECORD_DATE, dollars = CURRENT_MONTH_GROSS_RCPT_AMT
  a3d1df1df615c80be7b894f763687ea3b1b852a4  2015:13478.20B 2016:16036.76B 2017:16559.13B 2018:16677.30B 2019:17290.39B 2020:17221.13B 2021:20637.40B 2022:23158.65B 2023:22449.37B 2024:23723.27B 2025:25749.83B 2026:14825.23B

## what

DATA_TYPE_CD: D 58%, T 24%, S 18%

RECORD_TYPE_CD: RSG 69%, SRS 26%, SL 5%

SEQUENCE_LEVEL_NBR: 2 34%, 4 29%, 3 22%, 1 15%

RECORD_FISCAL_YEAR: 2025 9%, 2024 9%, 2023 9%, 2022 9%, 2021 9%, 2020 9%, 2019 9%, 2018 9%, 2017 9%, 2016 9%, 2026 7%, 2015 5%

RECORD_FISCAL_QUARTER: 3 27%, 2 25%, 4 25%, 1 23%

RECORD_CALENDAR_YEAR: 2025 9%, 2024 9%, 2023 9%, 2022 9%, 2021 9%, 2020 9%, 2019 9%, 2018 9%, 2017 9%, 2016 9%, 2015 7%, 2026 4%

RECORD_CALENDAR_QUARTER: 2 27%, 1 25%, 3 25%, 4 23%

RECORD_CALENDAR_MONTH: 06 9%, 05 9%, 04 9%, 03 9%, 09 8%, 08 8%, 07 8%, 02 8%, 01 8%, 12 8%, 11 7%, 10 7%

RECORD_CALENDAR_DAY: 31 58%, 30 34%, 28 6%, 29 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RECORD_DATE | date | 133 | 0 | 2026-06-30 57; 2025-09-30 57; 2025-08-31 57; 2025-07-31 57 |
| PARENT_ID | other | 1.6K | 1.1K | 58739505 36; 58739579 35; 58739456 35; 58739460 35 |
| CLASSIFICATION_ID | id | 7.4K | 0 | 58739595 38; 58739592 38; 58739571 38; 58739569 38 |
| CLASSIFICATION_DESC | who | 51 | 0 | Self-Employment Contribut 408; Federal Insurance Contrib 408; Adjustments Attributable  303; Adjustments Attributable  202 |
| CURRENT_MONTH_GROSS_RCPT_AMT | amount | 5.6K | 1.9K | 2366843375.96 28; 8234257420.92 28; 1702864.35 28; 754613541.90 28 |
| CURRENT_MONTH_REFUND_AMT | amount | 1.9K | 5.1K | 20869388.61 13; 68040147202.30 13; 2515344.34 13; 44897000.00 13 |
| CURRENT_MONTH_NET_RCPT_AMT | amount | 5.1K | 2.3K | 2203882904.32 26; 7705552298.15 26; 1702864.35 26; 754613541.90 26 |
| CURRENT_FYTD_GROSS_RCPT_AMT | other | 5.7K | 1.5K | '-45010469.12 32; '-281603489.53 32; '-284135555.98 32; '-920556362.17 32 |
| CURRENT_FYTD_REFUND_AMT | amount | 1.9K | 5.0K | 3309850000.00 23; 562050000.00 23; 2609701.51 18; 3871900000.00 14 |
| CURRENT_FYTD_NET_RCPT_AMT | other | 5.2K | 1.9K | '-45010469.12 30; '-281603489.53 30; '-284135555.98 30; '-920556362.17 30 |
| PRIOR_FYTD_GROSS_RCPT_AMT | id | 5.7K | 1.5K | 522164240.13 32; 3058827707.10 32; '-904957134.66 32; '-5338801962.56 32 |
| PRIOR_FYTD_REFUND_AMT | amount | 1.9K | 5.0K | 562050000.00 24; 3309850000.00 24; 2609701.51 16; 3871900000.00 16 |
| PRIOR_FYTD_NET_RCPT_AMT | other | 5.2K | 1.9K | 522164240.13 30; 3058827707.10 30; '-904957134.66 30; '-5338801962.56 30 |
| TABLE_NBR | other | 1 | 0 | 4 7.5K |
| SRC_LINE_NBR | other | 57 | 0 | 48 136; 47 136; 39 136; 38 136 |
| PRINT_ORDER_NBR | other | 57 | 0 | 48 136; 47 136; 39 136; 38 136 |
| LINE_CODE_NBR | other | 56 | 0 | 350 136; 314 136; 284 136; 279 136 |
| DATA_TYPE_CD | category | 3 | 0 | D 4.4K; T 1.8K; S 1.4K |
| RECORD_TYPE_CD | category | 3 | 0 | RSG 5.2K; SRS 1.9K; SL 408 |
| SEQUENCE_LEVEL_NBR | category | 4 | 0 | 2 2.6K; 4 2.2K; 3 1.6K; 1 1.1K |
| SEQUENCE_NUMBER_CD | other | 57 | 0 | 5 136; 4.5 136; 3.3.2 136; 3.3.1 136 |
| RECORD_FISCAL_YEAR | category | 12 | 0 | 2025 664; 2024 664; 2023 664; 2022 664 |
| RECORD_FISCAL_QUARTER | category | 4 | 0 | 3 2.0K; 2 1.9K; 4 1.9K; 1 1.7K |
| RECORD_CALENDAR_YEAR | category | 12 | 0 | 2025 664; 2024 664; 2023 664; 2022 664 |
| RECORD_CALENDAR_QUARTER | category | 4 | 0 | 2 2.0K; 1 1.9K; 3 1.9K; 4 1.7K |
| RECORD_CALENDAR_MONTH | category | 12 | 0 | 06 681; 05 666; 04 666; 03 666 |
| RECORD_CALENDAR_DAY | category | 4 | 0 | 31 4.4K; 30 2.5K; 28 448; 29 165 |
| INGESTED_AT | audit | 1 | 0 | 1785098772488253 7.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8b90390e-ce60-4679-934f-f 7.5K |
| SRC_SHA256 | who | 1 | 0 | a3d1df1df615c80be7b894f76 7.5K |
