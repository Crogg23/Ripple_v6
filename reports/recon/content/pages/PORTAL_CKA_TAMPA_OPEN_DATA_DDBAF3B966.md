# PORTAL_CKA_TAMPA_OPEN_DATA_DDBAF3B966

rows 88  columns 13  scan 2.8s

roles: amount 1, audit 2, category 5, date 2, empty 1, other 2, who 1

## when

DATE
  2015         1  ##
  2016         1  ##
  2017         1  ##
  2018         1  ##
  2019         1  ##
  2020         1  ##
  2021         9  ###############
  2022        13  ######################
  2023        12  ####################
  2024        13  ######################
  2025        18  ##############################
  2026        17  ############################

INGESTED_AT
  2026        88  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 88 | 0 | 95.75 | 807.3K | 813.0K | 8.50M |

## who

SRC_SHA256 by rows
        88  e32b00041494d1a61a4d91e52e849839b0ca7fc522677b998ad1d9bb3f503434

SRC_SHA256 by dollars
       8.50M       88 rows  e32b00041494d1a61a4d91e52e849839b0ca7fc522677b998ad1d9bb3f50

## who x when

SRC_SHA256 by DATE, dollars = VALUE
  e32b00041494d1a61a4d91e52e849839b0ca7fc5  2015:720.0K 2016:740.0K 2017:745.0K 2018:760.0K 2019:784.5K 2020:761.7K 2021:775.7K 2022:788.3K 2023:798.5K 2024:807.6K 2025:815.7K 2026:2.3K

## what

C_ORGANIZATION: Logistics & Asset Management ( 60%, Neighborhood Empowerment 16%, Development & Growth Mgmt 12%, City of Tampa 7%, Planning & Development (Develo 5%

CHARTNAME: Percent of Vehicles Available  60%, Mayor's Strategic Initiatives  16%, Mayor's Strategic Initiatives  12%, Mayor's Strategic Initiatives  5%, Mayor's Strategic Initiatives  3%, Mayor's Strategic Initiatives  3%

DESCRIPTION: Workforce Development; T3 Init 48%, Development and Growth Mgmt; H 38%, T3 Initiative 14%

CATEGORY: Percent of Vehicles 60%, Job Trends 12%, Started 9%, Not Started 9%, Completed 8%, Goal 1%

SUMMARY: Percent 60%, Total 40%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 88 | 0 | 21306 1; 21151 1; 21150 1; 21149 1 |
| C_ORGANIZATION | category | 5 | 0 | Logistics & Asset Managem 53; Neighborhood Empowerment 14; Development & Growth Mgmt 11; City of Tampa 6 |
| CHARTNAME | category | 6 | 0 | Percent of Vehicles Avail 53; Mayor's Strategic Initiat 14; Mayor's Strategic Initiat 11; Mayor's Strategic Initiat 4 |
| DESCRIPTION | category | 4 | 59 | Workforce Development; T3 14; Development and Growth Mg 11; T3 Initiative 4 |
| CATEGORY | category | 6 | 0 | Percent of Vehicles 53; Job Trends 11; Started 8; Not Started 8 |
| SUMMARY | category | 2 | 0 | Percent 53; Total 35 |
| TYPEDATA | other | 1 | 0 | Date 88 |
| DATE | date | 72 | 0 | 07/02/2026 12:30:27 8; 06/10/2026 00:00:00 3; 10/15/2025 00:00:00 3; 03/02/2021 00:00:00 3 |
| PERIOD | empty | 1 | 88 |  |
| VALUE | amount | 70 | 0 | 100.000 9; 89.380 7; 0.000 3; 99.700 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:14:47.07806 88 |
| SOURCE_RUN_ID | audit | 1 | 0 | 26ef1765-91d1-495a-a999-4 88 |
| SRC_SHA256 | who | 1 | 0 | e32b00041494d1a61a4d91e52 88 |
