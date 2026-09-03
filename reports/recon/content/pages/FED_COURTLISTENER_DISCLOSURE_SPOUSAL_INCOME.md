# FED_COURTLISTENER_DISCLOSURE_SPOUSAL_INCOME

rows 20.2K  columns 10  scan 3.2s

roles: audit 2, category 1, date 3, id 1, other 2, who 2

## when

DATE_CREATED
  2021     17.5K  ##############################
  2022      2.7K  #####
  2023        18  

DATE_MODIFIED
  2021     17.5K  ##############################
  2022      2.7K  #####
  2023        18  

_INGESTED_AT
  2026     20.2K  ##############################

## who

SOURCE_TYPE by rows
       171  Self-employed attorney
       117  self-employed attorney
        73  Credit Card
        55  Dreyfus Strategic World Investment Fund - Director Fees
        39  Self-Employed Attomey
        35  Self-employed Attorney
        32  Oregon Public Employees Retirement System
        31  Self-employed (attorney)
        29  Self-employed lawyer
        29  Self-employed (attomey)
        26  Self-employed artist
        22  Self-Employed Attorney
        21  Teachers Retirement System of Georgia
        20  Interventional Consultants, LLC
        20  Northwestern Medical Faculty Foundation
        19  Self-employed writer
        17  self-employed - soft tissue therapies
        17  Self-employed, dietitian consultant
        17  State of New Jersey
        17  Northwestern University Salary

_SRC_SHA256 by rows
     20.2K  a934538c22514fc704e45a8cfea3fcc3b6f09eecbfa2f116282cdb7bd21b9f24

## who x when

SOURCE_TYPE by DATE_CREATED
  Credit Card                               2021:73
  Dreyfus Strategic World Investment Fund   2021:49 2022:6
  Interventional Consultants, LLC           2021:15 2022:5
  Northwestern Medical Faculty Foundation   2021:15 2022:5
  Northwestern University Salary            2021:16 2022:1
  Oregon Public Employees Retirement Syste  2021:26 2022:6
  Self-Employed Attomey                     2021:39
  Self-Employed Attorney                    2021:15 2022:7
  Self-employed (attomey)                   2021:29
  Self-employed (attorney)                  2021:12 2022:19
  Self-employed Attorney                    2021:34 2022:1
  Self-employed artist                      2021:19 2022:7
  Self-employed attorney                    2021:145 2022:26
  Self-employed lawyer                      2021:28 2022:1
  Self-employed writer                      2021:15 2022:4
  Self-employed, dietitian consultant       2021:17
  State of New Jersey                       2021:15 2022:2
  Teachers Retirement System of Georgia     2021:20 2022:1
  self-employed - soft tissue therapies     2021:14 2022:3
  self-employed attorney                    2021:93 2022:24

_SRC_SHA256 by DATE_CREATED
  a934538c22514fc704e45a8cfea3fcc3b6f09eec  2021:17.5K 2022:2.7K 2023:18

## what

REDACTED: f 97%, t 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 20.7K | 0 | 61808 101; 61807 101; 61806 101; 61805 101 |
| DATE_CREATED | date | 20.3K | 0 | 2022-05-19 19:02:22.18930 101; 2022-05-19 19:02:22.18923 101; 2022-05-19 19:02:22.18913 101; 2022-05-19 16:13:10.68840 101 |
| DATE_MODIFIED | date | 20.1K | 0 | 2022-05-19 19:02:22.18931 101; 2022-05-19 19:02:22.18925 101; 2022-05-19 19:02:22.18917 101; 2022-05-19 16:13:10.68841 101 |
| SOURCE_TYPE | who | 8.7K | 226 | Self-employed attorney 173; self-employed attorney 130; Self-employed (attorney) 105; ( 102 |
| DATE_RAW | other | 2.3K | 397 | 2020 1.9K; 2019 1.6K; 2018 1.3K; 2016 1.3K |
| REDACTED | category | 2 | 0 | f 19.6K; t 611 |
| FINANCIAL_DISCLOSURE_ID | other | 13.8K | 0 | 33722 123; 33047 118; 33760 115; 33565 111 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:51.940 20.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 4ed846f8-f4fa-43b9-b982-4 20.2K |
| _SRC_SHA256 | who | 1 | 0 | a934538c22514fc704e45a8cf 20.2K |
