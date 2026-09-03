# FED_COURTLISTENER_DISCLOSURE_AGREEMENTS

rows 10.0K  columns 10  scan 3.4s

roles: audit 2, category 1, date 3, id 1, other 2, who 2

## when

DATE_CREATED
  2021      8.8K  ##############################
  2022      1.2K  ####
  2023         8  

DATE_MODIFIED
  2021      8.8K  ##############################
  2022      1.2K  ####
  2023         7  
  2024         1  

_INGESTED_AT
  2026     10.0K  ##############################

## who

PARTIES_AND_TERMS by rows
        24  LexisNexis: payment for work as author on updates of Moore's Federal P
        17  Johnson & Johnson Employee Savings Plan
        17  Pennsylvania State Employees Retirement Plan - pension received each m
        16  Johnson & Johnson Pension Plan
        16  State of Texas Retirement Plan, no control
        16  Contract with Greenwood Press as co-author for book (published 2006)
        15  New York State Retirement Plans
        15  New York State Retirement System, currently receiving pension
        15  State of Michigan 48th District Court Pension Fund
        15  University of California Pension (vested; no control)
        14  Berrien County Pension calculated based on years of service-Commenced 
        14  State of Texas Retirement Plan
        14  State of Nebraska Deferred Compensation Plan
        14  Department of Retirement Systems - State Pension
        14  CHESAPEAKE APP. (RedSky) LAND, LLC - 10 YEAR OIL AND GAS LEASE. DELAY 
        14  WI Department of Employee Trust Funds (retirement account), no control
        14  Arizona Elected Officials Retirement Plan (pension plan from prior emp
        13  Crowell & Moring LLP Retirement Plan with former law firm - no contrib
        13  Carlton Fields Profit Sharing Plan with former law firm - self directe
        13  TIAA-CREF (former law professor)

_SRC_SHA256 by rows
     10.0K  200c4974d058acac98030303416095b0143545ec0cf81752bfc391e88f199309

## who x when

PARTIES_AND_TERMS by DATE_CREATED
  Arizona Elected Officials Retirement Pla  2021:13 2022:1
  Berrien County Pension calculated based   2021:10 2022:4
  CHESAPEAKE APP. (RedSky) LAND, LLC - 10   2021:9 2022:5
  Carlton Fields Profit Sharing Plan with   2021:13
  Contract with Greenwood Press as co-auth  2021:15 2022:1
  Crowell & Moring LLP Retirement Plan wit  2021:9 2022:4
  Department of Retirement Systems - State  2021:13 2022:1
  Johnson & Johnson Employee Savings Plan   2021:14 2022:3
  Johnson & Johnson Pension Plan            2021:13 2022:3
  LexisNexis: payment for work as author o  2021:20 2022:4
  New York State Retirement Plans           2021:14 2022:1
  New York State Retirement System, curren  2021:9 2022:6
  Pennsylvania State Employees Retirement   2021:16 2022:1
  State of Michigan 48th District Court Pe  2021:14 2022:1
  State of Nebraska Deferred Compensation   2021:13 2022:1
  State of Texas Retirement Plan            2021:13 2022:1
  State of Texas Retirement Plan, no contr  2021:16
  TIAA-CREF (former law professor)          2021:12 2022:1
  University of California Pension (vested  2021:14 2022:1
  WI Department of Employee Trust Funds (r  2021:12 2022:2

_SRC_SHA256 by DATE_CREATED
  200c4974d058acac98030303416095b0143545ec  2021:8.8K 2022:1.2K 2023:8

## what

REDACTED: f 99%, t 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 10.2K | 0 | 25171 51; 25170 51; 25169 51; 25168 51 |
| DATE_CREATED | date | 10.1K | 0 | 2022-05-19 19:02:30.28618 51; 2022-05-19 19:02:22.07381 51; 2022-05-19 16:13:16.98295 51; 2022-05-19 16:13:07.28915 51 |
| DATE_MODIFIED | date | 10.0K | 0 | 2022-05-19 19:02:30.28620 51; 2022-05-19 19:02:22.07383 51; 2022-05-19 16:13:16.98298 51; 2022-05-19 16:13:07.28919 51 |
| DATE_RAW | other | 2.0K | 665 | 2003 262; 2004 236; 2013 236; 2012 223 |
| PARTIES_AND_TERMS | who | 5.0K | 50 | LexisNexis: payment for w 54; Fraser Stryker PC LLO - D 53; State of Texas Employee R 53; New York State Retirement 53 |
| REDACTED | category | 2 | 0 | f 9.9K; t 145 |
| FINANCIAL_DISCLOSURE_ID | other | 6.8K | 0 | 33633 59; 34023 56; 33965 56; 33935 56 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:40.793 10.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | df7abce6-b7c2-4588-a4ef-2 10.0K |
| _SRC_SHA256 | who | 1 | 0 | 200c4974d058acac980303034 10.0K |
