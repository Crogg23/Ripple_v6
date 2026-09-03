# PORTAL_CKA_TAMPA_OPEN_DATA_E00E42A7E9

rows 43  columns 13  scan 3.6s

roles: amount 1, audit 2, category 4, date 2, empty 1, other 1, who 3

## when

DATE
  2021        30  ##############################
  2022         1  #
  2023         2  ##
  2024         6  ######
  2025         3  ###
  2026         1  #

INGESTED_AT
  2026        43  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 43 | 66 | 229 | 3.2K | 3.4K | 31.4K |

## who

C_ORGANIZATION by rows
        43  City Clerk (Archives)

C_ORGANIZATION by dollars
       31.4K       43 rows  City Clerk (Archives)

TYPEDATA by rows
        43  Period

TYPEDATA by dollars
       31.4K       43 rows  Period

SRC_SHA256 by rows
        43  36378f72ac01844d5dc391c89344b71a17f58751677eb1a7dffde2495bb0dea5

SRC_SHA256 by dollars
       31.4K       43 rows  36378f72ac01844d5dc391c89344b71a17f58751677eb1a7dffde2495bb0

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  City Clerk (Archives)                     2021:13.8K 2022:460 2023:2.2K 2024:7.3K 2025:4.2K 2026:3.4K

TYPEDATA by DATE, dollars = VALUE
  Period                                    2021:13.8K 2022:460 2023:2.2K 2024:7.3K 2025:4.2K 2026:3.4K

## what

ID: 19384 8%, 17701 8%, 17700 8%, 16890 8%, 13105 8%, 13104 8%, 13103 8%, 13102 8%, 13101 8%, 13100 8%, 8485 8%, 8484 8%

CHARTNAME: All Data 65%, Public Record Requests 35%

CATEGORY: Public Record Requests 35%, Resolutions 35%, Ordinances 30%

PERIOD: 2022 11%, 2024 8%, 2023 8%, 2020 8%, 2019 8%, 2018 8%, 2017 8%, 2016 8%, 2015 8%, 2014 8%, 2013 8%, 2012 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | category | 43 | 0 | 19384 1; 17701 1; 17700 1; 16890 1 |
| C_ORGANIZATION | who | 1 | 0 | City Clerk (Archives) 43 |
| CHARTNAME | category | 2 | 0 | All Data 28; Public Record Requests 15 |
| DESCRIPTION | empty | 1 | 43 |  |
| CATEGORY | category | 3 | 0 | Public Record Requests 15; Resolutions 15; Ordinances 13 |
| SUMMARY | other | 1 | 0 | Total 43 |
| TYPEDATA | who | 1 | 0 | Period 43 |
| DATE | date | 20 | 0 | 2021-04-22T16:16:00 5; 2021-04-22T17:01:00 4; 2021-04-22T16:10:00 4; 2024-04-25T08:41:00 3 |
| PERIOD | category | 15 | 0 | 2022 4; 2024 3; 2023 3; 2020 3 |
| VALUE | amount | 41 | 0 | 1128 2; 152 2; 3369 1; 136 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:12:10.61173 43 |
| SOURCE_RUN_ID | audit | 1 | 0 | 818fcac8-9e5d-4600-9895-3 43 |
| SRC_SHA256 | who | 1 | 0 | 36378f72ac01844d5dc391c89 43 |
