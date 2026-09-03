# FED_TREASURY_AVG_INTEREST_RATES

rows 5.0K  columns 14  scan 3.0s

roles: amount 1, audit 2, category 9, date 1, who 1

## when

RECORD_DATE
  2001       190  ############################
  2002       189  ############################
  2003       184  ###########################
  2004       183  ###########################
  2005       202  ##############################
  2006       180  ##########################
  2007       180  ##########################
  2008       185  ###########################
  2009       191  ############################
  2010       195  #############################
  2011       204  ##############################
  2012       192  ############################
  2013       192  ############################
  2014       204  ##############################
  2015       204  ##############################
  2016       204  ##############################
  2017       195  #############################
  2018       192  ############################
  2019       192  ############################
  2020       200  #############################
  2021       204  ##############################
  2022       204  ##############################
  2023       204  ##############################
  2024       204  ##############################
  2025       204  ##############################
  2026        83  ############

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AVG_INTEREST_RATE_AMT | 4.9K | 0 | 3.25 | 8.27 | 10.25 | 17.9K |

## who

_SRC_SHA256 by rows
      5.0K  7fe37899bd0d15e7655b1290f0ca1d8d7f992e12b6e85f96be0499b80db3f9d1

_SRC_SHA256 by dollars
       17.9K     5.0K rows  7fe37899bd0d15e7655b1290f0ca1d8d7f992e12b6e85f96be0499b80db3

## who x when

_SRC_SHA256 by RECORD_DATE, dollars = AVG_INTEREST_RATE_AMT
  7fe37899bd0d15e7655b1290f0ca1d8d7f992e12  2001:1.1K 2002:1.0K 2003:900.29 2004:830.72 2005:881.02 2006:914.78 2007:920.66 2008:846.42 2009:705.12 2010:666.16 2011:664.77 2012:626.85 2013:591.59 2014:566.65 2015:536.18 2016:533.13 2017:558.94 2018:594.82 2019:600.63 2020:513.38 2021:469.62 2022:596.24 2023:664.83 2024:673.55 2025:640.29 2026:264.89

## what

SECURITY_TYPE_DESC: Non-marketable 53%, Marketable 41%, Interest-bearing Debt 6%

SECURITY_DESC: Treasury Bills 8%, Total Interest-bearing Debt 8%, Total Non-marketable 8%, Government Account Series 8%, United States Savings Securiti 8%, State and Local Government Ser 8%, Domestic Series 8%, Treasury Bonds 8%, Treasury Notes 8%, Foreign Series 8%, Total Marketable 8%, United States Savings Inflatio 8%

SRC_LINE_NBR: 1 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%

RECORD_FISCAL_YEAR: 2011 8%, 2015 8%, 2016 8%, 2021 8%, 2022 8%, 2023 8%, 2024 8%, 2025 8%, 2005 8%, 2014 8%, 2017 8%, 2020 8%

RECORD_FISCAL_QUARTER: 2 26%, 3 25%, 1 25%, 4 25%

RECORD_CALENDAR_YEAR: 2011 8%, 2014 8%, 2015 8%, 2016 8%, 2021 8%, 2022 8%, 2023 8%, 2024 8%, 2025 8%, 2005 8%, 2020 8%, 2010 8%

RECORD_CALENDAR_QUARTER: 1 26%, 2 25%, 4 25%, 3 25%

RECORD_CALENDAR_MONTH: 03 9%, 05 9%, 02 9%, 04 9%, 01 8%, 11 8%, 10 8%, 06 8%, 08 8%, 09 8%, 07 8%, 12 8%

RECORD_CALENDAR_DAY: 31 58%, 30 33%, 28 7%, 29 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RECORD_DATE | date | 307 | 0 | 2001-03-31 33; 2001-04-30 33; 2001-05-31 33; 2001-06-30 33 |
| SECURITY_TYPE_DESC | category | 3 | 0 | Non-marketable 2.6K; Marketable 2.0K; Interest-bearing Debt 305 |
| SECURITY_DESC | category | 22 | 0 | Treasury Bills 305; Total Interest-bearing De 305; Total Non-marketable 305; Government Account Series 305 |
| AVG_INTEREST_RATE_AMT | amount | 2.7K | 0 | 5.000 129; 7.312 103; 0.000 75; 4.652 68 |
| SRC_LINE_NBR | category | 17 | 0 | 1 305; 15 305; 14 305; 13 305 |
| RECORD_FISCAL_YEAR | category | 26 | 0 | 2011 204; 2015 204; 2016 204; 2021 204 |
| RECORD_FISCAL_QUARTER | category | 4 | 0 | 2 1.3K; 3 1.3K; 1 1.2K; 4 1.2K |
| RECORD_CALENDAR_YEAR | category | 26 | 0 | 2011 204; 2014 204; 2015 204; 2016 204 |
| RECORD_CALENDAR_QUARTER | category | 4 | 0 | 1 1.3K; 2 1.3K; 4 1.2K; 3 1.2K |
| RECORD_CALENDAR_MONTH | category | 12 | 0 | 03 424; 05 423; 02 422; 04 422 |
| RECORD_CALENDAR_DAY | category | 4 | 0 | 31 2.9K; 30 1.6K; 28 326; 29 96 |
| _INGESTED_AT | audit | 1 | 0 | 1781655965582501 5.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 4046bcc7-4501-46e9-878d-5 5.0K |
| _SRC_SHA256 | who | 1 | 0 | 7fe37899bd0d15e7655b1290f 5.0K |
