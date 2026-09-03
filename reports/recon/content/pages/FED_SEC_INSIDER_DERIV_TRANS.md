# FED_SEC_INSIDER_DERIV_TRANS

rows 1.05M  columns 45  scan 7.4s

roles: amount 8, audit 2, category 10, date 5, empty 1, id 1, other 14, who 5

## when

TRANS_DATE
  2000         2  
  2001         2  
  2002         5  
  2003         2  
  2004         5  
  2005         4  
  2006        45  
  2007        70  
  2008       100  
  2009       109  
  2010       168  
  2011       158  
  2012       391  
  2013       593  
  2014      1.0K  
  2015      1.4K  
  2016     53.5K  ###########
  2017    122.5K  ##########################
  2018    119.4K  ##########################
  2019    116.6K  #########################
  2020    120.0K  ##########################
  2021    139.7K  ##############################
  2022    114.9K  #########################
  2023    113.0K  ########################
  2024    108.7K  #######################
  2025     36.6K  ########
  2026         2  
  2027         1  
  2028         7  
  2029         4  
  2030         6  
  2031         1  
  2033         3  
  2034         1  
  2035         1  

DEEMED_EXECUTION_DATE
  2006         8  
  2007         3  
  2008         4  
  2009         4  
  2010         5  
  2011         8  
  2012        39  #
  2013        29  
  2014        29  
  2015        48  #
  2016       868  #############
  2017      1.9K  ##############################
  2018      1.7K  ##########################
  2019      1.2K  ##################
  2020       883  ##############
  2021      1.0K  ################
  2022       740  ###########
  2023       659  ##########
  2024       716  ###########
  2025       285  ####
  2026         1  
  2027         3  
  2028         3  
  2029         1  
  2030         1  
  2031         2  
  2033         2  
  2034         1  

EXCERCISE_DATE
  1988       553  #
  1994         1  
  1995         1  
  1996         1  
  1997         2  
  1998       295  
  1999         4  
  2000        36  
  2001         7  
  2002        10  
  2003        18  
  2004        35  
  2005        17  
  2006       127  
  2007      1.0K  #
  2008      2.1K  ###
  2009      3.2K  ####
  2010      3.8K  #####
  2011      5.1K  #######
  2012      6.4K  #########
  2013      7.7K  ##########
  2014      8.6K  ############
  2015      9.8K  #############
  2016     15.6K  #####################
  2017     22.3K  ##############################
  2018     22.1K  ##############################
  2019     20.8K  ############################
  2020     21.1K  ############################
  2021     19.1K  ##########################
  2022     17.3K  #######################
  2023     15.2K  ####################
  2024     13.4K  ##################
  2025      8.3K  ###########
  2026      2.8K  ####
  2027      1.2K  ##
  2028       675  #
  2029       220  
  2030        73  
  2031        24  
  2032        16  
  2033        13  
  2034        12  
  2035        72  

EXPIRATION_DATE
  1988       550  
  1998       285  
  1999         2  
  2000        23  
  2002         3  
  2005         2  
  2006         6  
  2007         5  
  2008         6  
  2009         6  
  2010        11  
  2011        21  
  2012        13  
  2013        30  
  2014        54  
  2015        94  
  2016      3.3K  ##
  2017     13.7K  ##########
  2018     18.3K  #############
  2019     20.5K  ###############
  2020     23.9K  ##################
  2021     28.0K  #####################
  2022     31.0K  #######################
  2023     35.6K  ##########################
  2024     37.2K  ###########################
  2025     34.7K  ##########################
  2026     35.9K  ##########################
  2027     40.8K  ##############################
  2028     36.3K  ###########################
  2029     33.1K  ########################
  2030     28.5K  #####################
  2031     25.0K  ##################
  2032     21.6K  ################
  2033     17.4K  #############
  2034     14.0K  ##########
  2035      5.0K  ####

_INGESTED_AT
  2026     1.05M  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CONV_EXERCISE_PRICE | 565.0K | 0 | 7.70 | 342.89 | 400.00B | 400.22B |
| TRANS_SHARES | 1.05M | 0 | 6.1K | 3.26M | 400.00B | 795.71B |
| TRANS_TOTAL_VALUE | 3.5K | 0 | 185.0K | 380.00M | 2.00B | 51.02B |
| TRANS_PRICEPERSHARE | 920.6K | 0 | 0 | 185.54 | 400.00B | 429.34B |
| UNDLYNG_SEC_SHARES | 1.05M | 0 | 6.3K | 4.96M | 399.90B | 1215.42B |
| UNDLYNG_SEC_VALUE | 383 | 0 | 25.0K | 29.73M | 1.09B | 1.70B |

## who

NATURE_OF_OWNERSHIP by rows
      9.0K  See footnote
      7.4K  See Footnote
      5.8K  See Footnotes
      3.2K  See footnotes
      2.6K  By Trust
      2.2K  By Deferred Compensation Plan
      1.4K  By Spouse
       620  By CZI Holdings, LLC
       514  Proportionate limited partnership interest in shares held by Rankin As
       483  See Note 2
       478  Deferred Compensation Plan
       457  By Benefit Plan
       435  CEO OF BENEFICIAL OWNER FOMO WORLDWIDE, INC.
       422  By QH Hungary Holdings Limited
       405  By spouse
       391  See Note
       375  See Explanation of Responses
       373  By LLC
       326  Non Qualified Retirement Savings Plan
       318  By Mark Zuckerberg, Trustee Of The Mark Zuckerberg Trust Dated July 7,

NATURE_OF_OWNERSHIP by dollars
       3.46B     7.4K rows  See Footnote
       2.00B        3 rows  Held through SLA Maverick Holdings, L.P.
       1.85B     9.0K rows  See footnote
       1.65B     3.2K rows  See footnotes
       1.59B        1 rows  Held through SLA CM Maverick Holdings, L.P.(
       1.27B        6 rows  Held through SLP IV Star Holdings, L.P.
       1.26B        2 rows  Held through a wholly-owned subsidiary
     894.71M        3 rows  Held through SLP IV Mustang Holdings II, L.P.
     467.44M        5 rows  Held through SLP IV Seal II Holdings, L.P.
     467.44M        5 rows  Held through SLP IV Seal Holdings, L.P.
     443.48M     5.8K rows  See Footnotes
     376.00M        1 rows  Held through SLP VI Union Holdings, L.P.
     376.00M        1 rows  Held through SLP VI Union Holdings II, L.P.
     209.75M      121 rows  Footnote
     188.00M        1 rows  Held through SLA Union Holdings L.P.
     150.00M        1 rows  Held through SLA Zurich Holdings, L.P.
     125.00M        3 rows  See footnote 1.
     120.00M       65 rows  Sequoia Capital Fund, LP
     100.00M        5 rows  Color Up, LLC
     100.00M        1 rows  By MGG Investment Group LP

NATURE_OF_OWNERSHIP_FN by rows
     11.8K  F2
      6.9K  F3
      5.1K  F1
      4.0K  F4
      2.8K  F5
      1.8K  F6
      1.2K  F2, F3
      1.2K  F7
       900  F8
       774  F3, F2
       761  F3, F4
       659  F9
       567  F4, F3
       506  F2, F1
       458  F10
       384  F11
       337  F5, F4
       335  F1, F2
       252  F4, F5
       249  F12

NATURE_OF_OWNERSHIP_FN by dollars
       4.16B     5.1K rows  F1
       2.18B      506 rows  F2, F1
       1.64B     1.2K rows  F2, F3
       1.31B     6.9K rows  F3
     981.77M    11.8K rows  F2
     527.03M     1.2K rows  F7
     505.52M      112 rows  F15
     472.97M       12 rows  F6, F7, F8
     376.00M        1 rows  F1, F4, F2, F6
     376.00M        1 rows  F1, F4, F6, F3
     301.56M     4.0K rows  F4
     299.52M      127 rows  F6, F7
     284.71M        1 rows  F6, F9, F8
     284.71M        9 rows  F9, F7, F8
     274.61M     2.8K rows  F5
     210.02M       82 rows  F17
     194.78M     1.8K rows  F6
     188.00M        1 rows  F1, F5, F6
     182.72M       11 rows  F11, F12
     182.72M        3 rows  F10, F12

DIRECT_INDIRECT_OWNERSHIP_FN by rows
      2.7K  F2
      2.2K  F3
      1.3K  F1
       803  F4
       353  F5
       299  F7
       270  F6
       206  F8
       194  F2, F3
       129  F3, F4
        98  F2, F1
        95  F9
        86  F3, F2
        85  F12
        75  F10
        67  F11
        66  F1, F2
        56  F15
        53  F14
        36  F4, F3

DIRECT_INDIRECT_OWNERSHIP_FN by dollars
     188.34M     2.7K rows  F2
     159.35M      353 rows  F5
     156.02M      270 rows  F6
      99.15M     1.3K rows  F1
      47.58M      129 rows  F3, F4
      35.00M       86 rows  F3, F2
      30.00M        1 rows  F3, F1, F2, F4
      27.53M       25 rows  F6, F5
      26.40M        1 rows  F9, F8, F10
      25.34M      803 rows  F4
      24.56M      299 rows  F7
      23.67M       66 rows  F1, F2
      18.08M     2.2K rows  F3
       7.08M        1 rows  F7, F10
       6.53M        6 rows  F2, F6, F5, F1
       5.89M       98 rows  F2, F1
       5.58M        1 rows  F5, F10
       2.36M        1 rows  F4, F10
       2.08M        2 rows  F6, F10
      150.0K       12 rows  F5, F6

SECURITY_TITLE by rows
    213.4K  Restricted Stock Units
     75.5K  Stock Option (Right to Buy)
     55.8K  Restricted Stock Unit
     50.3K  Stock Option (right to buy)
     37.4K  Class B Common Stock
     30.1K  Employee Stock Option (right to buy)
     27.3K  Employee Stock Option (Right to Buy)
     18.6K  Stock Option
     17.7K  Phantom Stock
     17.6K  Non-Qualified Stock Option (right to buy)
     16.7K  Phantom Stock Units
     12.4K  Stock Options
     12.2K  Deferred Stock Units
     11.0K  Stock Options (Right to Buy)
      9.4K  Restricted Share Units
      7.7K  Dividend Equivalent Rights
      6.2K  Stock Appreciation Right
      5.8K  Performance Stock Units
      5.7K  Stock Appreciation Rights
      5.5K  Non-qualified Stock Option (Right to Buy)

SECURITY_TITLE by dollars
     400.00B        1 rows  FL ADR No. HCCZT-IBN00001 Payable through FRB Fiscal Agent
       3.59B        4 rows  1.75% Convertible Senior Notes due 2024
       1.84B        6 rows  0.50% Exch. Sr. Debentures due 2050 (obligation to sell)
       1.56B        2 rows  3.125% Exch. Senior Debentures due 2053 (obligation to sell)
       1.15B        1 rows  2.375% Exch. Sr. Debentures due 2053 (obligation to sell)
       1.13B        3 rows  2.000% Convertible Senior Notes due 2022
       1.03B        1 rows  Exchangeable Senior Notes due 2026
     940.00M        3 rows  2.00% Convertible Senior Notes due 2027
     934.87M        8 rows  2.500% Convertible Senior Notes due 2022
     894.71M        4 rows  2.0% Convertible Senior Notes due 2020
     860.00M        3 rows  3.125% Exch. Senior Debentures due 2054 (obligation to sell)
     827.01M        3 rows  1.25% Exch. Senior Debentures due 2050 (obligation to sell)
     822.99M        1 rows  1.25% Exch.Senior Debentures due 2050 (obligation to sell)
     772.48M        4 rows  2.00% Convertible Senior Notes due 2022
     723.76M       11 rows  Second Amended and Restated Convertible Promissory Note
     655.90M        3 rows  0.50% Exch. Senior Debentures due 2051 (obligation to sell)
     603.75M        3 rows  2.75% Exch. Sr. Debentures due 2049 (obligation to sell)
     575.00M        1 rows  2.75% Exch.Senior Debentures due 2050 (obligation to sell)
     575.00M        1 rows  2.75% Exchangeable Sr. Dbnt. due 2050 (obligation to sell)
     500.00M        2 rows  2.00% Convertible Senior Notes due 2021

## who x when

NATURE_OF_OWNERSHIP by TRANS_DATE, dollars = TRANS_PRICEPERSHARE
  By Benefit Plan                           2016:1.7K 2017:1.8K 2018:1.6K 2019:1.9K 2020:1.5K 2021:1.4K 2022:1.0K 2023:853.33 2024:1.0K 2025:237.30
  By CZI Holdings, LLC                      2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2023:0 2024:0 2025:0
  By Deferred Compensation Plan             2016:2.3K 2017:3.5K 2018:3.7K 2019:4.1K 2020:4.1K 2021:4.1K 2022:3.0K 2023:2.7K 2024:2.8K 2025:664.16
  By LLC                                    2016:2.50 2017:100.1K 2018:705 2019:234.13 2020:17.76 2021:0 2022:34.79 2023:5.35M 2024:15.38 2025:45.81
  By Mark Zuckerberg, Trustee Of The Mark   2016:0 2017:0 2020:0 2021:0 2023:0 2024:0
  By QH Hungary Holdings Limited            2020:5 2021:12 2022:0 2023:6 2024:137 2025:135
  By Spouse                                 2015:0 2016:362.02 2017:630.11 2018:815.4K 2019:271.82 2020:340.23 2021:193.48 2022:96.32 2023:1.2K 2024:128.9K 2025:84.43
  By Trust                                  2008:0 2011:0 2015:0 2016:2.4K 2017:737.4K 2018:4.0K 2019:5.7K 2020:5.3K 2021:5.8K 2022:1.3K 2023:2.15M 2024:289.2K 2025:25
  By spouse                                 2014:0 2015:8 2016:3.0K 2017:50.0K 2018:61.21 2019:108.16 2020:69.56 2021:22.46 2022:19.87 2023:0.04 2024:15.75 2025:18.22
  CEO OF BENEFICIAL OWNER FOMO WORLDWIDE,   2021:580 2022:280.80 2023:29.19
  Deferred Compensation Plan                2016:2.6K 2017:6.9K 2018:5.4K 2019:4.0K 2020:4.0K 2021:6.4K 2022:6.5K 2023:4.9K 2024:5.6K 2025:1.5K
  Footnote                                  2016:27.65 2017:4 2018:0.10 2020:0 2021:402.69 2022:85.58M 2023:124.18M 2024:1
  Held through SLA CM Maverick Holdings, L  2024:1.59B
  Held through SLA Maverick Holdings, L.P.  2019:2.00B
  Held through SLP IV Mustang Holdings II,  2018:368.86M 2019:525.86M
  Held through SLP IV Seal Holdings, L.P.   2020:284.71M 2021:182.72M
  Held through SLP IV Seal II Holdings, L.  2020:284.71M 2021:182.72M
  Held through SLP IV Star Holdings, L.P.   2016:500.00M 2020:772.48M
  Held through SLP VI Union Holdings II, L  2022:376.00M
  Held through SLP VI Union Holdings, L.P.  2022:376.00M
  Held through a wholly-owned subsidiary    2020:1 2023:1.26B
  Non Qualified Retirement Savings Plan     2018:3.8K 2019:3.4K 2020:3.3K 2021:4.1K 2022:7.3K 2023:4.1K 2024:3.9K 2025:1.3K
  Proportionate limited partnership intere  2017:0 2018:0 2019:0 2020:103 2021:11.53 2022:0
  See Explanation of Responses              2013:62.04 2016:0 2017:220.59 2018:316.14 2019:32.50 2020:40.80 2021:1.50 2022:6.18 2023:54.66 2024:30 2025:4
  See Footnote                              2014:20.50 2015:2 2016:10.08M 2017:7.48M 2018:88.69M 2019:46.25M 2020:1.42B 2021:1.31B 2022:337.97M 2023:46.50M 2024:186.03M 2025:10.75M
  See Footnotes                             2014:2 2015:0 2016:6.32M 2017:1.15M 2018:7.59M 2019:22.83M 2020:713.4K 2021:9.18M 2022:1.01M 2023:119.40M 2024:51.51M 2025:223.79M
  See Note                                  2012:0 2013:0 2014:0 2015:0 2016:608.4K 2017:92.7K 2018:3.25M 2019:0 2021:592.47 2022:0 2023:32.00M 2024:0 2025:4
  See Note 2                                2016:0 2017:0 2018:11.41 2019:132.46 2020:58.32 2021:0 2022:1.90 2023:25 2024:0
  See footnote                              2010:11.27 2011:6.50 2012:0 2013:0 2014:0.76 2015:5.00M 2016:24.95M 2017:54.87M 2018:46.99M 2019:25.78M 2020:38.14M 2021:44.92M 2022:317.06M 2023:647.72M 2024:509.62M 2025:130.00M
  See footnotes                             2015:930.0K 2016:504.1K 2017:172.22M 2018:16.6K 2019:24.56M 2020:1.35B 2021:4.09M 2022:98.59M 2023:9.7K 2024:3.4K 2025:1.1K

NATURE_OF_OWNERSHIP_FN by TRANS_DATE, dollars = TRANS_PRICEPERSHARE
  F1                                        2013:62.04 2014:1.01M 2015:30 2016:781.2K 2017:577.8K 2018:389.96M 2019:575.53M 2020:45.94M 2021:1.36B 2022:174.08M 2023:6.4K 2024:1.59B 2025:22.02M
  F1, F2                                    2016:101.22 2020:0 2021:4.77M 2022:19.50M 2023:0.25 2024:134.89 2025:70.56
  F1, F4, F2, F6                            2022:376.00M
  F1, F4, F6, F3                            2022:376.00M
  F1, F5, F6                                2022:188.00M
  F10                                       2010:11.27 2011:6.50 2013:0 2014:0 2016:0 2017:2.0K 2018:10.0K 2019:20 2020:302.9K 2021:19.38 2022:26 2023:487.28 2024:627.73 2025:0
  F11                                       2012:0 2013:0 2014:0 2015:0 2016:1.2K 2017:205.34 2018:0 2019:0 2020:633.70 2021:1.27M 2022:1.43 2023:0 2024:0 2025:0
  F11, F12                                  2018:1 2021:182.72M 2023:578.80 2024:0
  F12                                       2013:0 2014:0 2015:0 2016:0 2017:0 2018:270.81 2019:272.60 2020:406.42 2021:0.01 2022:438.43 2023:106 2024:1.80 2025:3
  F15                                       2014:0 2015:0 2016:0 2017:521.5K 2018:0 2019:0 2020:0 2021:15.19 2022:0 2023:0 2024:505.00M 2025:2
  F17                                       2014:0 2015:0 2016:0 2017:21.5K 2018:0 2019:0 2020:10.00M 2021:15.19 2022:0 2023:200.00M 2024:0 2025:0
  F2                                        2008:0 2011:0 2013:0 2014:20.50 2015:13.24 2016:25.57M 2017:313.4K 2018:26.23M 2019:4.30M 2020:737.5K 2021:26.72M 2022:273.32M 2023:596.75M 2024:9.69M 2025:18.15M
  F2, F1                                    2015:930.0K 2016:6.81M 2017:45.13M 2018:125.00M 2019:2.00B 2020:78.28 2021:3.26 2022:0.52 2023:114.82 2024:67.72 2025:8.77
  F2, F3                                    2016:0 2017:2.3K 2018:0 2019:35.52 2020:1.63B 2021:155.04 2022:4.90 2023:22.16 2024:6.00M 2025:2.50M
  F3                                        2012:0 2014:0.76 2015:2 2016:13.61M 2017:9.57M 2018:19.70M 2019:20.49M 2020:854.18M 2021:66.78M 2022:252.18M 2023:58.04M 2024:18.76M 2025:177.4K
  F3, F2                                    2016:608.18 2017:0 2018:251.31 2020:11.10 2021:2.0K 2022:54.41 2023:150.00M 2024:1.0K 2025:143.27
  F3, F4                                    2016:566.09 2017:1.55M 2018:1.19M 2019:767.7K 2020:3.94M 2021:25.59M 2022:3.0K 2023:1.1K 2024:3.46 2025:26.25
  F4                                        2015:1.0K 2016:416.4K 2017:11.75M 2018:44.37M 2019:22.33M 2020:58.89M 2021:6.4K 2022:74.69M 2023:66.50M 2024:22.60M 2025:886.52
  F4, F3                                    2020:845.3K 2021:3.0K 2022:3.1K 2023:60.95 2024:8.21 2025:40.40
  F4, F5                                    2016:113.13 2017:7.23M 2018:2.34M 2020:8 2021:588.3K 2022:22.3K 2023:6.7K 2024:1.6K 2025:1.0K
  F5                                        2015:0.01 2016:12.5K 2017:4.57M 2018:32.11M 2019:1.8K 2020:450.4K 2021:3.3K 2022:72.62M 2023:21.85M 2024:8.04M 2025:134.96M
  F5, F4                                    2018:2.56M 2019:2.83M 2020:9.6K 2021:6.1K 2022:6.7K 2023:6.7K 2024:2.2K 2025:752.33
  F6                                        2012:0 2013:0 2015:0.01 2016:408.2K 2017:2.95M 2018:425.50 2019:1.7K 2020:51.5K 2021:2.6K 2022:140.02M 2023:49.85M 2024:710.3K 2025:792.0K
  F6, F7                                    2018:0 2019:0 2020:299.52M 2021:0 2022:0 2023:1.0K 2024:0
  F6, F7, F8                                2019:0 2020:472.97M 2021:0 2022:0 2023:0 2024:2
  F6, F9, F8                                2020:284.71M
  F7                                        2013:0 2015:20 2016:500.41M 2017:1.37M 2018:470.07 2019:1.5K 2020:20.00M 2021:5.00M 2022:1.2K 2023:241.6K 2024:1.1K 2025:278.50
  F8                                        2012:0 2013:0 2014:2 2016:2.0K 2017:972.5K 2018:10.1K 2019:100.00M 2020:4.70M 2021:1.21M 2022:598.82 2023:347.24 2024:297.41 2025:429.38
  F9                                        2013:0 2014:0 2016:0 2017:246.72 2018:1.00M 2019:21.61 2020:22.33 2021:164.10 2022:608.68 2023:824.59 2024:92.17 2025:0
  F9, F7, F8                                2018:0 2020:284.71M

## what

DEEMED_EXECUTION_DATE_FN: F1 57%, F2 19%, F3 11%, F7 5%, F4 2%, F6 2%, F5 1%, F4, F5 1%, F8 1%, F7, F6 1%, F2, F1 1%

TRANS_FORM_TYPE: 4 98%, 5 2%

TRANS_CODE: A 44%, M 40%, D 5%, C 4%, J 3%, P 1%, G 1%, X 1%, S 0%, F 0%, I 0%, U 0%

EQUITY_SWAP_INVOLVED: 0 92%, false 8%, 1 0%, true 0%

TRANS_TIMELINESS: E 87%, L 13%

TRANS_TIMELINESS_FN: F1 56%, F2 13%, F4 10%, F3 10%, F5 6%, F15 4%, F12 1%

TRANS_ACQUIRED_DISP_CD: D 51%, A 49%

UNDLYNG_SEC_VALUE_FN: F1 20%, F3 19%, F2 15%, F5 11%, F4 9%, F2, F1 6%, F6 5%, F3, F2, F1 5%, F2, F3 3%, F7 3%, F3, F1, F2, F4 3%

VALU_OWND_FOLWNG_TRANS_FN: F1 25%, F2 16%, F4 15%, F3 10%, F2, F1 10%, F7 6%, F5 6%, F6 3%, F2, F3 3%, F3, F2 3%, F9 2%

DIRECT_INDIRECT_OWNERSHIP: D 93%, I 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACCESSION_NUMBER | other | 655.4K | 0 | 0001104659-23-018835 788; 0001209191-23-009246 788; 0001209191-23-007653 786; 0001209191-23-007655 784 |
| DERIV_TRANS_SK | id | 1.08M | 0 | 2736749 779; 2936100 779; 3032266 779; 3032265 779 |
| SECURITY_TITLE | who | 9.9K | 0 | Restricted Stock Units 213.4K; Stock Option (Right to Bu 75.5K; Restricted Stock Unit 55.8K; Stock Option (right to bu 50.3K |
| SECURITY_TITLE_FN | other | 277 | 963.9K | F1 41.8K; F2 12.3K; F3 10.0K; F4 6.3K |
| CONV_EXERCISE_PRICE | amount | 13.2K | 484.2K | 0.0 128.5K; 11.5 2.9K; 10.0 1.6K; 2.0 1.6K |
| CONV_EXERCISE_PRICE_FN | other | 675 | 491.1K | F1 294.5K; F2 100.7K; F3 56.7K; F4 30.3K |
| TRANS_DATE | date | 4.0K | 0 | 01-MAR-2023 3.0K; 01-MAR-2024 2.9K; 01-MAR-2021 2.5K; 01-MAR-2022 2.5K |
| TRANS_DATE_FN | other | 86 | 1.04M | F1 4.7K; F2 1.7K; F3 892; F4 516 |
| DEEMED_EXECUTION_DATE | date | 1.7K | 1.04M | 20-FEB-2017 82; 17-NOV-2017 75; 01-MAR-2017 70; 02-MAY-2022 60 |
| DEEMED_EXECUTION_DATE_FN | category | 38 | 1.05M | F1 432; F2 146; F3 87; F7 35 |
| TRANS_FORM_TYPE | category | 3 | 1 | 4 1.03M; 5 17.2K |
| TRANS_CODE | category | 19 | 1 | A 461.2K; M 423.8K; D 52.3K; C 46.2K |
| EQUITY_SWAP_INVOLVED | category | 5 | 1 | 0 964.1K; false 82.2K; 1 2.7K; true 72 |
| EQUITY_SWAP_TRANS_CD_FN | other | 440 | 927.4K | F1 59.8K; F2 27.5K; F3 9.3K; F4 6.2K |
| TRANS_TIMELINESS | category | 3 | 1.04M | E 8.2K; L 1.2K |
| TRANS_TIMELINESS_FN | category | 8 | 1.05M | F1 52; F2 12; F4 9; F3 9 |
| TRANS_SHARES | amount | 149.9K | 3.5K | 10000.0 15.3K; 5000.0 12.0K; 20000.0 8.9K; 25000.0 8.5K |
| TRANS_SHARES_FN | other | 430 | 958.3K | F2 27.6K; F1 23.5K; F3 12.6K; F4 8.5K |
| TRANS_TOTAL_VALUE | amount | 1.4K | 1.05M | 100000.0 117; 50000.0 97; 1000000.0 78; 500000.0 62 |
| TRANS_TOTAL_VALUE_FN | other | 51 | 1.05M | F2 156; F1 139; F3 87; F4 64 |
| TRANS_PRICEPERSHARE | amount | 13.4K | 128.5K | 0.0 775.3K; 0.1 952; 0.01 916; 0.25 795 |
| TRANS_PRICEPERSHARE_FN | other | 661 | 873.0K | F1 53.0K; F2 36.1K; F3 26.0K; F4 17.4K |
| TRANS_ACQUIRED_DISP_CD | category | 2 | 0 | D 535.0K; A 514.2K |
| TRANS_ACQUIRED_DISP_CD_FN | empty | 1 | 1.05M |  |
| EXCERCISE_DATE | date | 6.8K | 820.1K | 01-MAR-2023 860; 31-DEC-2019 856; 01-MAR-2018 769; 01-MAR-2019 710 |
| EXCERCISE_DATE_FN | other | 864 | 152.2K | F2 221.2K; F1 200.6K; F3 164.1K; F4 101.3K |
| EXPIRATION_DATE | date | 7.1K | 543.9K | 01-MAR-2027 1.6K; 15-FEB-2028 1.5K; 15-FEB-2027 1.4K; 01-JAN-2025 1.3K |
| EXPIRATION_DATE_FN | other | 516 | 486.4K | F2 140.2K; F3 117.1K; F1 105.9K; F4 68.1K |
| UNDLYNG_SEC_TITLE | who | 1.6K | 0 | Common Stock 705.4K; Class A Common Stock 124.1K; Common Shares 27.5K; Ordinary Shares 22.0K |
| UNDLYNG_SEC_TITLE_FN | other | 186 | 1.04M | F1 4.0K; F2 2.9K; F3 1.1K; F4 717 |
| UNDLYNG_SEC_SHARES | amount | 150.6K | 3.6K | 10000.0 15.0K; 5000.0 11.6K; 20000.0 8.7K; 25000.0 8.4K |
| UNDLYNG_SEC_SHARES_FN | other | 307 | 1.02M | F1 7.8K; F2 7.7K; F3 5.1K; F4 3.5K |
| UNDLYNG_SEC_VALUE | amount | 191 | 1.05M | 5000.0 25; 20000.0 23; 0.0 19; 12500.0 15 |
| UNDLYNG_SEC_VALUE_FN | category | 22 | 1.05M | F1 19; F3 18; F2 14; F5 10 |
| SHRS_OWND_FOLWNG_TRANS | amount | 237.7K | 2.6K | 0.0 238.2K; 10000.0 5.2K; 20000.0 4.5K; 50000.0 4.5K |
| SHRS_OWND_FOLWNG_TRANS_FN | other | 357 | 983.7K | F3 16.8K; F2 12.8K; F4 11.4K; F5 6.0K |
| VALU_OWND_FOLWNG_TRANS | amount | 1.0K | 1.05M | 0.0 553; 100000.0 53; 50000.0 47; 1000000.0 44 |
| VALU_OWND_FOLWNG_TRANS_FN | category | 33 | 1.05M | F1 83; F2 53; F4 49; F3 32 |
| DIRECT_INDIRECT_OWNERSHIP | category | 2 | 0 | D 975.6K; I 73.5K |
| DIRECT_INDIRECT_OWNERSHIP_FN | who | 363 | 1.04M | F2 2.7K; F3 2.2K; F1 1.3K; F4 803 |
| NATURE_OF_OWNERSHIP | who | 6.3K | 975.6K | See footnote 9.0K; See Footnote 7.4K; See Footnotes 5.8K; See footnotes 3.2K |
| NATURE_OF_OWNERSHIP_FN | who | 1.7K | 996.7K | F2 11.8K; F3 6.9K; F1 5.1K; F4 4.0K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-24 02:31:15.000 1.05M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 103fdf61-1806-44af-9610-f 1.05M |
| _SRC_SHA256 | other | 1 | 0 | manifest_members:35:DERIV 1.05M |
