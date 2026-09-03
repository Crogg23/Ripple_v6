# FED_FRB_H15_SELECTED_RATES

rows 16.8K  columns 15  scan 4.3s

roles: amount 11, audit 2, date 1, who 1

## when

SERIES_DESCRIPTION
  1962       260  ##############################
  1963       261  ##############################
  1964       262  ##############################
  1965       261  ##############################
  1966       260  ##############################
  1967       260  ##############################
  1968       262  ##############################
  1969       261  ##############################
  1970       261  ##############################
  1971       261  ##############################
  1972       260  ##############################
  1973       261  ##############################
  1974       261  ##############################
  1975       261  ##############################
  1976       262  ##############################
  1977       260  ##############################
  1978       260  ##############################
  1979       261  ##############################
  1980       262  ##############################
  1981       261  ##############################
  1982       261  ##############################
  1983       260  ##############################
  1984       261  ##############################
  1985       261  ##############################
  1986       261  ##############################
  1987       261  ##############################
  1988       261  ##############################
  1989       260  ##############################
  1990       261  ##############################
  1991       261  ##############################
  1992       262  ##############################
  1993       261  ##############################
  1994       260  ##############################
  1995       260  ##############################
  1996       262  ##############################
  1997       261  ##############################
  1998       261  ##############################
  1999       261  ##############################
  2000       260  ##############################
  2001       261  ##############################
  2002       261  ##############################
  2003       261  ##############################
  2004       262  ##############################
  2005       260  ##############################
  2006       260  ##############################
  2007       261  ##############################
  2008       262  ##############################
  2009       261  ##############################
  2010       261  ##############################
  2011       260  ##############################
  2012       261  ##############################
  2013       261  ##############################
  2014       261  ##############################
  2015       261  ##############################
  2016       261  ##############################
  2017       260  ##############################
  2018       261  ##############################
  2019       261  ##############################
  2020       262  ##############################
  2021       261  ##############################
  2022       260  ##############################
  2023       260  ##############################
  2024       262  ##############################
  2025       261  ##############################
  2026       146  #################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_1_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | 6.2K | 0 | 1.02 | 5.54 | 6.02 | 10.7K |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_3_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | 11.2K | 0 | 3.93 | 13.12 | 17.01 | 43.0K |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_6_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | 11.2K | 0.02 | 4.04 | 13.82 | 17.43 | 44.8K |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_1_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | 16.1K | 0.04 | 4.90 | 15.04 | 17.31 | 78.6K |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_2_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | 12.5K | 0.09 | 4.62 | 14.93 | 16.95 | 62.1K |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_3_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | 16.1K | 0.10 | 4.99 | 14.45 | 16.59 | 84.5K |

## who

SRC_SHA256 by rows
     16.8K  6c08dd3c1253e680e7b86456f53814e09d1c75691a7395133edbc0bf62409cbc

SRC_SHA256 by dollars
       78.6K    16.8K rows  6c08dd3c1253e680e7b86456f53814e09d1c75691a7395133edbc0bf6240

## who x when

SRC_SHA256 by SERIES_DESCRIPTION, dollars = MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_1_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS
  6c08dd3c1253e680e7b86456f53814e09d1c7569  1962:771.89 1963:835.64 1964:961.77 1965:1.0K 1966:1.3K 1967:1.2K 1968:1.4K 1969:1.8K 1970:1.7K 1971:1.2K 1972:1.2K 1973:1.8K 1974:2.0K 1975:1.7K 1976:1.5K 1977:1.5K 1978:2.1K 1979:2.6K 1980:3.0K 1981:3.7K 1982:3.1K 1983:2.4K 1984:2.7K 1985:2.1K 1986:1.6K 1987:1.7K 1988:1.9K 1989:2.1K 1990:2.0K 1991:1.5K 1992:976.16 1993:858.61 1994:1.3K 1995:1.5K 1996:1.4K 1997:1.4K 1998:1.3K 1999:1.3K 2000:1.5K 2001:865.52 2002:500.47 2003:310.35 2004:471.92 2005:905.24 2006:1.2K 2007:1.1K 2008:458.53 2009:118.38 2010:79.73 2011:45.22 2012:43.71 2013:32.79 2014:30.28 2015:81 2016:153.58 2017:300.72 2018:580.38 2019:513.01 2020:92.90 2021:26.10 2022:696.33 2023:1.3K 2024:1.2K 2025:974.42 2026:520.68

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SERIES_DESCRIPTION | date | 17.1K | 0 | 2026-07-23 85; 2026-07-22 85; 2026-07-21 85; 2026-07-20 85 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_1_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 547 | 10.3K | 0.02 311; ND 272; 0.01 271; 0.04 223 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_3_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.2K | 5.1K | ND 491; 0.02 276; 0.05 237; 0.03 220 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_6_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.3K | 5.1K | ND 491; 0.06 214; 0.05 198; 0.07 183 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_1_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.5K | 1 | ND 719; 0.11 233; 0.12 214; 0.18 189 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_2_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.5K | 3.8K | ND 551; 0.27 138; 0.16 129; 0.14 115 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_3_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.5K | 1 | ND 719; 0.35 113; 0.34 104; 0.37 104 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_5_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.5K | 1 | ND 719; 3.72 92; 1.66 92; 1.62 92 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_7_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.5K | 2.0K | ND 634; 4.20 84; 2.14 83; 2.02 83 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_10_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.4K | 1 | ND 719; 4.19 111; 4.20 110; 4.29 95 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_20_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.3K | 1 | ND 2.4K; 4.21 104; 4.93 85; 4.20 85 |
| MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_30_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS | amount | 1.3K | 3.9K | ND 544; 3.00 83; 3.02 82; 3.03 79 |
| INGESTED_AT | audit | 1 | 0 | 1785098691291563 16.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | cd58594b-662a-410e-942b-2 16.8K |
| SRC_SHA256 | who | 1 | 0 | 6c08dd3c1253e680e7b86456f 16.8K |
