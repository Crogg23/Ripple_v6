# FED_COURTLISTENER_DISCLOSURE_NON_INVESTMENT_INCOME

rows 15.3K  columns 11  scan 3.7s

roles: audit 2, category 1, date 3, id 1, other 2, who 3

## when

DATE_CREATED
  2021     13.6K  ##############################
  2022      1.7K  ####
  2023        29  

DATE_MODIFIED
  2021     13.6K  ##############################
  2022      1.7K  ####
  2023        29  

_INGESTED_AT
  2026     15.3K  ##############################

## who

INCOME_AMOUNT by rows
       150  S10.000.00
       111  $2,000.00
       110  S1.500.00
       100  $5,000.00
        99  S5.000.00
        99  $10,000.00
        95  S6.000.00)
        87  $6,000.00
        87  $3,000.00
        83  S4.000.00
        82  S2.000.00
        80  S3.000.00
        79  S15.000.00
        79  S1O.000.00
        76  $12,000.00
        69  $3,500.00
        61  $2,500.00
        60  $500.00
        60  $1,500.00
        58  S4.500.00

SOURCE_TYPE by rows
        45  Columbia Law School
        28  Self-employed (attorney)
        27  Tennessee Consolidated Retirement System
        24  California Judges Retirement System
        22  Vanderbilt University - teaching
        21  Washington State Department of Retirement Systems
        20  Judicial Retirement System of Texas
        19  Thomson Reuters, Eagan, MN - Royalties
        19  New York University School of Law
        19  Credit Card
        19  NEW YORK STATE RETIREMENT SYSTEM
        18  Georgetown University Law Center
        18  Tennessee Consolidated Retirement System Judicial Retirement
        18  State of Michigan Pension
        17  Northwestern Law School (teaching)
        17  Ohio Public Employees Retirement System
        17  State of Tennesssee Retirement Benefit
        17  Lecturer, The George Washington University Law School
        17  Practising Law Institute Book Royalties
        17  NEW YORK UNIVERSITY - TEACHING

_SRC_SHA256 by rows
     15.3K  42d1846b4f2c23f516d8c4302e213b3ab6c76ecd0a4babafad646da1f9ae5084

## who x when

INCOME_AMOUNT by DATE_CREATED
  $1,500.00                                 2021:43 2022:17
  $10,000.00                                2021:52 2022:46 2023:1
  $12,000.00                                2021:64 2022:11 2023:1
  $2,000.00                                 2021:99 2022:12
  $2,500.00                                 2021:51 2022:10
  $3,000.00                                 2021:45 2022:42
  $3,500.00                                 2021:54 2022:15
  $5,000.00                                 2021:75 2022:25
  $500.00                                   2021:59 2022:1
  $6,000.00                                 2021:60 2022:27
  S1.500.00                                 2021:110
  S10.000.00                                2021:150
  S15.000.00                                2021:79
  S1O.000.00                                2021:79
  S2.000.00                                 2021:82
  S3.000.00                                 2021:80
  S4.000.00                                 2021:83
  S4.500.00                                 2021:58
  S5.000.00                                 2021:99
  S6.000.00)                                2021:95

SOURCE_TYPE by DATE_CREATED
  California Judges Retirement System       2021:19 2022:5
  Columbia Law School                       2021:36 2022:9
  Credit Card                               2021:19
  Georgetown University Law Center          2021:17 2022:1
  Judicial Retirement System of Texas       2021:13 2022:7
  Lecturer, The George Washington Universi  2021:17
  NEW YORK STATE RETIREMENT SYSTEM          2021:17 2022:2
  NEW YORK UNIVERSITY - TEACHING            2021:16 2022:1
  New York University School of Law         2021:16 2022:3
  Northwestern Law School (teaching)        2021:13 2022:4
  Ohio Public Employees Retirement System   2021:15 2022:2
  Practising Law Institute Book Royalties   2021:16 2022:1
  Self-employed (attorney)                  2021:11 2022:17
  State of Michigan Pension                 2021:17 2022:1
  State of Tennesssee Retirement Benefit    2021:9 2022:8
  Tennessee Consolidated Retirement System  2021:27
  Tennessee Consolidated Retirement System  2021:17 2022:1
  Thomson Reuters, Eagan, MN - Royalties    2021:17 2022:2
  Vanderbilt University - teaching          2021:20 2022:2
  Washington State Department of Retiremen  2021:20 2022:1

## what

REDACTED: f 99%, t 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 15.3K | 0 | 42514 77; 42513 77; 42512 77; 42511 77 |
| DATE_CREATED | date | 15.5K | 0 | 2022-05-19 19:02:30.35697 77; 2022-05-19 19:02:22.15792 77; 2022-05-19 19:02:22.15781 77; 2022-05-19 16:13:17.06004 77 |
| DATE_MODIFIED | date | 14.9K | 0 | 2022-05-19 19:02:30.35700 77; 2022-05-19 19:02:22.15794 77; 2022-05-19 19:02:22.15785 77; 2022-05-19 16:13:17.06006 77 |
| DATE_RAW | other | 2.5K | 662 | 2020 1.1K; 2019 978; 2013 948; 2012 921 |
| SOURCE_TYPE | who | 6.7K | 285 | Fraser Stryker Deferred C 79; Judicial Retirement Syste 79; Penguin Random House LLC  79; Royalties, National Insti 78 |
| INCOME_AMOUNT | who | 8.8K | 204 | S10.000.00 162; S1.500.00 128; S5.000.00 116; S6.000.00) 113 |
| REDACTED | category | 2 | 0 | f 15.2K; t 124 |
| FINANCIAL_DISCLOSURE_ID | other | 10.1K | 0 | 33846 88; 33725 87; 33744 83; 30478 83 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:46.134 15.3K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 6f0a7bd5-e4ec-48fa-83cc-c 15.3K |
| _SRC_SHA256 | who | 1 | 0 | 42d1846b4f2c23f516d8c4302 15.3K |
