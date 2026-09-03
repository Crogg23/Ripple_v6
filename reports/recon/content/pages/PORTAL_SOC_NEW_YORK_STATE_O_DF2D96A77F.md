# PORTAL_SOC_NEW_YORK_STATE_O_DF2D96A77F

rows 2.0K  columns 13  scan 3.4s

roles: amount 2, audit 2, category 3, date 1, other 4, who 2

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_WAGE | 2.0K | 19.8K | 82.97M | 43.80B | 978.63B | 6219.25B |
| ANNUAL_AVERAGE_SALARY | 2.0K | 11.7K | 74.5K | 291.5K | 547.2K | 169.78M |

## who

NAICS_TITLE by rows
        24  Management of Companies and Enterprises
        24  Administration of Economic Programs
        22  Justice, Public Order, and Safety Activi
        18  Professional and Technical Services
        17  Total, All Industries
        16  Educational Services
        16  Public Administration
        16  Executive, Legislative, & Gen Government
        16  Warehousing and Storage
        15  Unclassified
        14  Administration of Human Resource Program
        12  Transportation and Warehousing
        12  Printing and Related Support Activities
        12  Electronic Markets and Agents/Brokers
        11  Elementary and Secondary Schools
        11  Health Care and Social Assistance
        11  Transit and Ground Passenger Transport
        11  Amusement, Gambling & Recreation Ind
        11  Food Services and Drinking Places
        11  Restaurants and Other Eating Places

NAICS_TITLE by dollars
    2140.98B       17 rows  Total, All Industries
     239.81B       18 rows  Professional and Technical Services
     239.77B        6 rows  Financial Investment & Related Activity
     184.80B       16 rows  Public Administration
     182.48B        8 rows  Finance and Insurance
     172.58B       24 rows  Management of Companies and Enterprises
     167.33B       16 rows  Educational Services
     150.84B       11 rows  Health Care and Social Assistance
     123.54B        6 rows  Security & Commodity Investment Activity
     114.81B        6 rows  Other Financial Investment Activities
      74.83B        8 rows  Wholesale Trade
      58.86B        8 rows  Hospitals
      58.37B       10 rows  Information
      54.73B        8 rows  Depository Credit Intermediation
      52.79B        8 rows  General Medical and Surgical Hospitals
      50.29B        6 rows  Ambulatory Health Care Services
      49.88B       11 rows  Elementary and Secondary Schools
      49.80B        8 rows  Legal Services
      49.70B       11 rows  Food Services and Drinking Places
      47.78B        9 rows  Social Assistance

SRC_SHA256 by rows
      2.0K  075e431361daea0ae5cd3e0fd3d1322971f6b99cee4aef3fd7bcc36a331162ae

SRC_SHA256 by dollars
    6219.25B     2.0K rows  075e431361daea0ae5cd3e0fd3d1322971f6b99cee4aef3fd7bcc36a3311

## who x when

NAICS_TITLE by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_WAGE
  Administration of Economic Programs       2026:35.98B
  Administration of Human Resource Program  2026:15.54B
  Ambulatory Health Care Services           2026:50.29B
  Amusement, Gambling & Recreation Ind      2026:8.12B
  Depository Credit Intermediation          2026:54.73B
  Educational Services                      2026:167.33B
  Electronic Markets and Agents/Brokers     2026:8.11B
  Elementary and Secondary Schools          2026:49.88B
  Executive, Legislative, & Gen Government  2026:39.75B
  Finance and Insurance                     2026:182.48B
  Financial Investment & Related Activity   2026:239.77B
  Food Services and Drinking Places         2026:49.70B
  General Medical and Surgical Hospitals    2026:52.79B
  Health Care and Social Assistance         2026:150.84B
  Hospitals                                 2026:58.86B
  Information                               2026:58.37B
  Justice, Public Order, and Safety Activi  2026:25.70B
  Management of Companies and Enterprises   2026:172.58B
  Other Financial Investment Activities     2026:114.81B
  Printing and Related Support Activities   2026:2.25B
  Professional and Technical Services       2026:239.81B
  Public Administration                     2026:184.80B
  Restaurants and Other Eating Places       2026:41.66B
  Security & Commodity Investment Activity  2026:123.54B
  Total, All Industries                     2026:2140.98B
  Transit and Ground Passenger Transport    2026:34.37B
  Transportation and Warehousing            2026:35.77B
  Unclassified                              2026:14.89B
  Warehousing and Storage                   2026:12.61B
  Wholesale Trade                           2026:74.83B

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_WAGE
  075e431361daea0ae5cd3e0fd3d1322971f6b99c  2026:6219.25B

## what

AREA_TYPE: County 57%, State 43%

AREA: New York State 43%, Albany County 25%, Bronx County 20%, Allegany County 11%

OWNERSHIP: Private 47%, Total, All Ownerships 37%, Federal Government 7%, Local Government 4%, State Government 3%, Total, All Government 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA_TYPE | category | 2 | 0 | County 1.1K; State 858 |
| AREA | category | 4 | 0 | New York State 858; Albany County 504; Bronx County 410; Allegany County 228 |
| OWNERSHIP | category | 6 | 0 | Private 936; Total, All Ownerships 746; Federal Government 137; Local Government 77 |
| NAICS | other | 387 | 0 | 00 19; 92 18; 9261 14; 926 14 |
| NAICS_TITLE | who | 361 | 0 | Management of Companies a 26; Administration of Economi 26; Justice, Public Order, an 24; Professional and Technica 20 |
| YEAR | other | 1 | 0 | 2025 2.0K |
| ESTABLISHMENTS | other | 511 | 0 | 4 61; 5 60; 6 53; 3 50 |
| AVERAGE_EMPLOYMENT | other | 943 | 0 | 84 18; 25 17; 2283 14; 58 14 |
| TOTAL_WAGE | amount | 1.1K | 0 | 307796642 14; 133530168 13; 2303706 13; 20010551 13 |
| ANNUAL_AVERAGE_SALARY | amount | 1.1K | 0 | 134821 14; 31996 13; 238221 13; 68583 12 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:42:59.38192 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | a33e491e-9e55-4c1e-9a24-9 2.0K |
| SRC_SHA256 | who | 1 | 0 | 075e431361daea0ae5cd3e0fd 2.0K |
