# PORTAL_CKA_TAMPA_OPEN_DATA_662D0D6BCB

rows 694  columns 13  scan 3.0s

roles: amount 1, audit 2, category 3, date 2, empty 2, other 3, who 1

## when

DATE
  2018         8  ##
  2019        72  ####################
  2020        77  ######################
  2021        96  ###########################
  2022        96  ###########################
  2023        95  ###########################
  2024        97  ###########################
  2025       107  ##############################
  2026        46  #############

INGESTED_AT
  2026       694  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 694 | 0 | 56.45 | 49.3K | 269.4K | 1.22M |

## who

SRC_SHA256 by rows
       694  f60b5c796a53079278841aba29b867148fdad69cfbe7187ae3f35d5061f7b3a0

SRC_SHA256 by dollars
       1.22M      694 rows  f60b5c796a53079278841aba29b867148fdad69cfbe7187ae3f35d5061f7

## who x when

SRC_SHA256 by DATE, dollars = VALUE
  f60b5c796a53079278841aba29b867148fdad69c  2018:649.83 2019:3.5K 2020:3.7K 2021:4.6K 2022:4.5K 2023:4.5K 2024:75.8K 2025:850.7K 2026:273.0K

## what

CHARTNAME: Water Percent New Meters 13%, Water Percent Meter Accuracy 13%, Water Percent of Abandoned Cal 13%, Water Percent Meters Read 13%, Water Call Center Wait Time 13%, Water Odor Threshold 13%, Cumulative miles of pipe this  10%, Water Available Permitted Capa 10%, Water Engineering Construction 3%

CATEGORY: Install Percent 13%, Pct Meter Accuracy 13%, Pct of Abandoned Calls 13%, Pct Meters Read 13%, Avg Wait Time 13%, Threshold Odor 13%, Miles 10%, Running Average (MGD) 10%, Cost Savings Per Month 3%

SUMMARY: Percent 52%, Total 35%, Average 13%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 682 | 0 | 21323 4; 21322 4; 21148 4; 21147 4 |
| C_ORGANIZATION | other | 1 | 0 | Water 694 |
| CHARTNAME | category | 9 | 0 | Water Percent New Meters 92; Water Percent Meter Accur 90; Water Percent of Abandone 89; Water Percent Meters Read 89 |
| DESCRIPTION | empty | 1 | 694 |  |
| CATEGORY | category | 9 | 0 | Install Percent 92; Pct Meter Accuracy 90; Pct of Abandoned Calls 89; Pct Meters Read 89 |
| SUMMARY | category | 3 | 0 | Percent 360; Total 245; Average 89 |
| TYPEDATA | other | 1 | 0 | Date 694 |
| DATE | date | 154 | 0 | 2025-03-01T00:00:00 8; 2024-12-01T00:00:00 8; 2024-11-01T00:00:00 8; 2021-09-01T00:00:00 8 |
| PERIOD | empty | 1 | 694 |  |
| VALUE | amount | 463 | 0 | 0.0 59; 1.0 9; 1.1 9; 99.79 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:22:46.78506 694 |
| SOURCE_RUN_ID | audit | 1 | 0 | e980a1a6-406f-4766-934f-5 694 |
| SRC_SHA256 | who | 1 | 0 | f60b5c796a53079278841aba2 694 |
