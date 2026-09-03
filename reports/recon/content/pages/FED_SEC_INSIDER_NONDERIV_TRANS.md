# FED_SEC_INSIDER_NONDERIV_TRANS

rows 2.67M  columns 31  scan 8.7s

roles: amount 4, audit 2, category 11, date 3, id 1, other 6, who 5

## when

TRANS_DATE
  1987         1  
  1994         1  
  1998         1  
  1999         1  
  2000         2  
  2001        12  
  2002        76  
  2003         2  
  2004         3  
  2005        15  
  2006        21  
  2007        34  
  2008        39  
  2009        41  
  2010       125  
  2011       242  
  2012       365  
  2013       412  
  2014       754  
  2015      2.0K  
  2016    133.0K  ###########
  2017    292.6K  ########################
  2018    304.5K  #########################
  2019    292.3K  ########################
  2020    310.9K  #########################
  2021    368.7K  ##############################
  2022    290.5K  ########################
  2023    281.9K  #######################
  2024    296.6K  ########################
  2025     97.6K  ########
  2026         2  
  2027         3  
  2028         4  
  2029         3  
  2030         6  
  2031         1  
  2032         1  
  2033         4  

DEEMED_EXECUTION_DATE
  2002         5  
  2008         1  
  2010         5  
  2011         5  
  2012        13  
  2013        17  
  2014        26  
  2015        54  
  2016      3.7K  ####################
  2017      5.4K  ##############################
  2018      5.0K  ############################
  2019      3.5K  ###################
  2020      3.4K  ###################
  2021      3.8K  #####################
  2022      3.1K  #################
  2023      3.0K  #################
  2024      2.7K  ###############
  2025       917  #####
  2027         1  
  2028         1  

_INGESTED_AT
  2026     2.67M  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TRANS_SHARES | 2.67M | 0 | 2.9K | 2.04M | 400.00B | 2473.35B |
| TRANS_PRICEPERSHARE | 2.50M | 0 | 18.67 | 1.0K | 400.00B | 406.99B |
| SHRS_OWND_FOLWNG_TRANS | 2.67M | 0 | 53.6K | 40.43M | 399.90B | 9421.65B |
| VALU_OWND_FOLWNG_TRANS | 754 | 0 | 244.8K | 222.85M | 344.67M | 5.74B |

## who

NATURE_OF_OWNERSHIP by rows
     37.1K  See footnote
     35.5K  See Footnote
     27.9K  By Trust
     23.3K  See Footnotes
     15.3K  See footnotes
      7.4K  By Spouse
      5.9K  by Trust
      4.5K  By CZI Holdings, LLC
      4.1K  Proportionate interest in shares held by Rankin Associates VI
      4.0K  Child's proportionate interest in shares held by Rankin Associates VI
      3.9K  -
      3.5K  By Chan Zuckerberg Initiative Foundation
      3.1K  By IRA
      2.8K  By Family Trust
      2.6K  By Mark Zuckerberg, Trustee Of The Mark Zuckerberg Trust Dated July 7,
      2.4K  Spouse's proportionate interest in shares held by Rankin Associates VI
      2.1K  By spouse
      2.1K  By LLC
      1.9K  Trust
      1.7K  By trust

NATURE_OF_OWNERSHIP by dollars
     942.81M    35.5K rows  See Footnote
     900.00M        8 rows  By Allied Physicians of California, A Professional Medical C
     614.61M      147 rows  Held through subsidiaries
     363.55M    23.3K rows  See Footnotes
     301.69M    15.3K rows  See footnotes
     193.54M       47 rows  By Groveland Capital LLC
     180.05M       50 rows  By The Prudential Insurance Company of America, a wholly-own
     162.97M      688 rows  By Subsidiary
      59.68M        7 rows  By Prudential Retirement Insurance and Annuity Company, a wh
      56.00M        7 rows  Held through subsidiary
      51.94M       21 rows  By SBI Incubation Co., Ltd.
      45.99M      114 rows  By Gregory E. Abel Revocable Trust
      20.13M        2 rows  By The Gibraltar Life Insurance Co., Ltd., a wholly-owned su
      19.64M        2 rows  By The Gibraltar Life Insurance Co., Ltd., a wholly owned su
      19.22M        6 rows  subsidiary
      17.58M        3 rows  By The Prudential Life Insurance Company Ltd., a wholly-owne
      14.99M        4 rows  By Prudential Arizona Reinsurance Term Company, a wholly-own
      14.81M        3 rows  By Prudential Annuities Life Assurance Corporation
      14.70M        4 rows  By holding
      13.13M    37.1K rows  See footnote

NATURE_OF_OWNERSHIP_FN by rows
     57.4K  F2
     47.0K  F3
     46.9K  F1
     15.4K  F4
      9.4K  F5
      6.2K  F6
      4.9K  F2, F3
      4.6K  F2, F1
      4.3K  F7
      3.4K  F8
      3.3K  F3, F2
      2.8K  F3, F4
      2.7K  F9
      2.4K  F10
      2.3K  F1, F2
      2.1K  F11
      1.8K  F13
      1.6K  F4, F3
      1.4K  F12
      1.3K  F2, F3, F1

NATURE_OF_OWNERSHIP_FN by dollars
       1.44B    57.4K rows  F2
       1.20B    46.9K rows  F1
     287.13M     4.6K rows  F2, F1
     251.88M    47.0K rows  F3
     124.80M      829 rows  F4, F5
      94.39M     4.9K rows  F2, F3
      68.64M    15.4K rows  F4
      36.45M     9.4K rows  F5
      30.06M     1.6K rows  F4, F3
      13.88M     4.3K rows  F7
      12.68M     3.3K rows  F3, F2
      11.46M     6.2K rows  F6
       7.37M     3.4K rows  F8
       6.82M     1.8K rows  F13
       6.77M     2.1K rows  F11
       5.46M     1.2K rows  F14
       5.35M     2.7K rows  F9
       4.60M     1.2K rows  F15
       4.51M     1.4K rows  F12
       4.23M     2.4K rows  F10

DIRECT_INDIRECT_OWNERSHIP_FN by rows
     16.7K  F2
     16.1K  F1
      9.1K  F3
      2.7K  F4
      1.6K  F2, F1
      1.4K  F5
       984  F2, F3
       808  F6
       678  F1, F2
       646  F3, F2
       497  F7
       481  F9
       362  F3, F4
       324  F8
       192  F12
       186  F2, F3, F1
       133  F10
       117  F6, F5
       117  F3, F2, F4
       116  F11

DIRECT_INDIRECT_OWNERSHIP_FN by dollars
     190.33M    16.7K rows  F2
     149.66M    16.1K rows  F1
     124.76M       62 rows  F4, F5
      84.82M      984 rows  F2, F3
      41.74M     9.1K rows  F3
      30.00M       72 rows  F4, F3
      29.45M     2.7K rows  F4
      12.36M        3 rows  F7, F1
       6.01M      646 rows  F3, F2
       5.03M      324 rows  F8
       3.42M        6 rows  F7, F2
       1.97M        3 rows  F3, F7
       1.92M        4 rows  F6, F4
       1.22M      808 rows  F6
      854.0K     1.6K rows  F2, F1
      263.5K        5 rows  F5, F4, F6, F2, F3
       91.1K       37 rows  F7, F6
       76.2K        6 rows  F7, F5
       41.7K     1.4K rows  F5
       33.3K      497 rows  F7

SECURITY_TITLE by rows
     1.70M  Common Stock
    351.3K  Class A Common Stock
     57.1K  Common Shares
     38.5K  Ordinary Shares
     26.7K  COMMON STOCK
     26.1K  Common Stock, par value $0.01 per share
     18.2K  Common stock
     17.2K  Common
     14.7K  Class A common stock
     12.6K  Class B Common Stock
     11.7K  Common Stock, $0.01 par value
     10.7K  Common Stock, par value $0.001 per share
      9.4K  common stock
      8.4K  Common Units
      8.1K  Common Stock, par value $0.01
      7.7K  Common Stock, par value $.01 per share
      7.7K  Common Stock, par value $0.001
      6.8K  Class C Capital Stock
      5.6K  Common Stock, $0.001 par value
      5.3K  Common stock, par value $0.01 per share

SECURITY_TITLE by dollars
     400.00B        1 rows  FL ADR No. 201805189210
       4.10B    1.70M rows  Common Stock
     600.09M     3.1K rows  Class A Ordinary Shares
     234.86M   351.3K rows  Class A Common Stock
     100.50M        3 rows  LISA MICHELLE PARKER (PA) ADR, Preferred Stock
     100.00M        1 rows  FL ADR No. HCCZT-IBN00001
      79.85M        5 rows  3.00% Series B Senior Secured Notes due July 22, 2026
      70.62M        9 rows  Floating Rate Senior Note, Series A Note, Due Sep. 18, 2023
      64.00M        4 rows  3.18% Senior Notes, Series N, due December 13, 2024
      60.00M        3 rows  7.10% Series I Senior Secured Notes due December 6, 2027
      59.00M        3 rows  6.81% Series M Senior Secured Notes due August 4, 2030
      50.00M        2 rows  7.40% Series R Senior Secured Notes due January 20, 2034
      49.00M        3 rows  6.77% Series L Senior Secured Notes due August 4, 2028
      42.12M        3 rows  Units of Limited Liability Company Interests, $10.00 per Uni
      41.93M        6 rows  3.33% Senior Notes, Series PP, due September 25, 2027
      41.40M    57.1K rows  Common Shares
      41.29M        1 rows  3.71% Series V Senior Unsecured Notes due May 26, 2016
      40.00M        1 rows  7.10% Series J Senior Secured Notes due December 6, 2029
      39.05M       27 rows  Series C Mandatory Redeemable Preferred Shares
      39.00M        2 rows  7.23% Series Q Senior Secured Notes due January 20, 2031

## who x when

NATURE_OF_OWNERSHIP by TRANS_DATE, dollars = TRANS_PRICEPERSHARE
  -                                         2010:11.43 2017:21.25 2018:3.8K 2019:2.9K 2020:3.9K 2021:2.2K 2022:4.3K 2023:15.7K 2024:13.7K 2025:2.7K
  By Allied Physicians of California, A Pr  2018:0 2019:900.00M 2022:0
  By CZI Holdings, LLC                      2016:4.7K 2017:16.2K 2018:110.1K 2019:55.1K 2020:67.5K 2021:473.9K 2023:0 2024:331.5K 2025:325.0K
  By Chan Zuckerberg Initiative Foundation  2020:65.8K 2021:448.4K 2023:89.3K 2024:569.0K 2025:233.3K
  By Family Trust                           2001:0 2014:0 2015:1 2016:2.0K 2017:15.2K 2018:10.4K 2019:9.7K 2020:15.1K 2021:17.5K 2022:24.1K 2023:54.9K 2024:82.2K 2025:2.8K
  By Gregory E. Abel Revocable Trust        2021:276.82 2022:45.99M
  By Groveland Capital LLC                  2016:272.81 2017:193.54M 2018:55.94
  By IRA                                    2007:34.23 2014:1 2015:30.27 2016:4.0K 2017:5.9K 2018:6.5K 2019:5.9K 2020:6.9K 2021:57.5K 2022:5.4K 2023:4.0K 2024:3.9K 2025:1.1K
  By LLC                                    2009:0 2015:73.25 2016:485.95 2017:2.2K 2018:4.9K 2019:9.3K 2020:9.8K 2021:104.9K 2022:6.3K 2023:5.9K 2024:5.1K 2025:1.6K
  By Mark Zuckerberg, Trustee Of The Mark   2016:0 2017:0 2020:30.5K 2021:436.6K 2023:83.1K 2024:233.9K
  By Prudential Retirement Insurance and A  2017:30.00M 2020:29.68M
  By SBI Incubation Co., Ltd.               2014:8.15 2015:5.72 2016:1.90M 2017:50.04M
  By Spouse                                 2001:44.76 2010:0 2011:0 2012:0 2013:26.66 2014:0 2015:169.48 2016:9.0K 2017:12.6K 2018:16.9K 2019:18.7K 2020:109.8K 2021:47.5K 2022:24.4K 2023:34.1K 2024:63.5K 2025:13.4K
  By Subsidiary                             2016:22.77M 2017:25.43M 2018:77.70M 2019:1.75M 2020:34.09M 2021:100.0K 2022:71.3K 2023:911.5K 2024:151.2K
  By The Gibraltar Life Insurance Co., Ltd  2017:12.00M 2020:8.13M
  By The Prudential Insurance Company of A  2017:15.00M 2018:23.00M 2020:76.16M 2021:20.00M 2022:400.1K 2024:45.50M
  By Trust                                  2007:0 2010:64.74 2011:38.98 2012:20.10 2013:117.79 2014:151.79 2015:488.74 2016:35.1K 2017:70.1K 2018:83.5K 2019:109.4K 2020:454.5K 2021:952.7K 2022:937.2K 2023:707.8K 2024:890.5K 2025:300.8K
  By spouse                                 2008:5.72 2012:75.86 2013:0 2014:446.29 2015:731.91 2016:3.6K 2017:10.8K 2018:4.9K 2019:7.36M 2020:11.4K 2021:66.2K 2022:8.4K 2023:13.6K 2024:8.4K 2025:1.5K
  By trust                                  2011:0 2014:0 2015:277.17 2016:1.8K 2017:4.3K 2018:3.3K 2019:6.4K 2020:8.9K 2021:4.6K 2022:2.6K 2023:4.5K 2024:3.7K 2025:273.80
  Child's proportionate interest in shares  2017:0 2018:155.9K 2019:85.8K 2021:0
  Held through subsidiaries                 2008:12.85M 2015:68.93M 2016:90.06M 2018:6.93M 2019:200.0K 2020:153.68M 2022:100.00M 2023:168.67M 2024:13.29M
  Held through subsidiary                   2016:5.00M 2023:51.00M 2025:75
  Proportionate interest in shares held by  2017:0 2018:161.8K 2019:86.5K 2021:55.50
  See Footnote                              2008:6.25 2011:88.05 2012:94.97 2013:56.85 2014:346.92 2015:156.19 2016:305.3K 2017:525.70M 2018:224.2K 2019:69.1K 2020:293.3K 2021:406.30M 2022:9.56M 2023:65.4K 2024:278.7K 2025:23.7K
  See Footnotes                             2002:3.09 2006:0 2007:14.04 2008:7 2009:0 2011:32.87 2012:51.7K 2013:736.82 2014:889.53 2015:1.2K 2016:35.1K 2017:8.48M 2018:108.79M 2019:51.2K 2020:124.80M 2021:608.2K 2022:32.54M 2023:50.8K 2024:87.13M 2025:1.01M
  See footnote                              2011:1.1K 2012:2.1K 2013:0 2014:16.59 2015:36.60 2016:56.4K 2017:223.6K 2018:113.3K 2019:733.8K 2020:5.76M 2021:1.08M 2022:1.32M 2023:3.36M 2024:410.6K 2025:67.9K
  See footnotes                             2015:0 2016:12.9K 2017:114.30M 2018:55.72M 2019:68.7K 2020:83.2K 2021:2.01M 2022:67.4K 2023:28.4K 2024:129.39M 2025:5.6K 2027:5.75
  Spouse's proportionate interest in share  2017:0 2018:93.8K 2019:51.5K 2020:0 2021:166.50
  Trust                                     2015:0.06 2016:3.2K 2017:7.1K 2018:5.3K 2019:6.1K 2020:6.4K 2021:33.1K 2022:3.9K 2023:4.4K 2024:10.1K 2025:3.6K
  by Trust                                  2013:74.46 2014:80.47 2015:84.72 2016:17.2K 2017:36.8K 2018:52.8K 2019:54.5K 2020:87.2K 2021:424.3K 2022:355.8K 2023:32.2K 2024:84.5K 2025:33.2K

NATURE_OF_OWNERSHIP_FN by TRANS_DATE, dollars = TRANS_PRICEPERSHARE
  F1                                        2009:0 2010:0 2011:88.05 2012:86.32 2013:112.4K 2014:313.98 2015:202.5K 2016:7.57M 2017:526.33M 2018:244.2K 2019:28.52M 2020:1.51M 2021:401.02M 2022:48.17M 2023:54.31M 2024:130.19M 2025:1.28M 2026:0.25
  F1, F2                                    2011:0 2013:9.85 2016:9.6K 2018:0 2019:13.23 2020:61.98 2021:9.5K 2022:11.4K 2023:115.6K 2024:7.3K 2025:4.2K
  F10                                       2016:3.89M 2017:10.4K 2018:15.9K 2019:14.6K 2020:31.2K 2021:126.5K 2022:5.4K 2023:23.7K 2024:100.3K 2025:8.0K
  F11                                       2013:0 2015:3.19M 2016:3.22M 2017:2.6K 2018:13.6K 2019:7.2K 2020:33.4K 2021:137.4K 2022:9.8K 2023:17.1K 2024:119.4K 2025:8.4K
  F12                                       2014:0.08 2016:4.26M 2017:10.0K 2018:9.5K 2019:16.8K 2020:19.6K 2021:97.4K 2022:7.0K 2023:12.3K 2024:68.5K 2025:3.0K
  F13                                       2015:6.53M 2016:141.06 2017:10.6K 2018:9.7K 2019:7.4K 2020:21.0K 2021:144.5K 2022:5.0K 2023:7.9K 2024:73.9K 2025:9.0K
  F14                                       2016:5.22M 2017:1.5K 2018:10.2K 2019:10.4K 2020:27.1K 2021:90.3K 2022:4.5K 2023:5.3K 2024:66.2K 2025:26.4K
  F15                                       2016:4.32M 2017:3.5K 2018:1.8K 2019:10.6K 2020:26.1K 2021:135.1K 2022:920.41 2023:11.0K 2024:79.5K 2025:6.2K
  F2                                        2000:13 2005:0 2008:12.85M 2009:46.60 2010:2.16 2011:1.2K 2012:2.1K 2013:45.63 2014:7.90 2015:41.29M 2016:51.89M 2017:200.03M 2018:7.48M 2019:900.71M 2020:25.84M 2021:7.11M 2022:63.61M 2023:109.92M 2024:14.16M 2025:146.4K
  F2, F1                                    2014:66.22 2015:62.19 2016:215.04 2017:122.71M 2018:164.29M 2019:19.3K 2020:76.4K 2021:4.7K 2022:11.1K 2023:4.7K 2024:8.2K 2025:1.5K
  F2, F3                                    2006:0 2007:6.37 2008:7 2010:0 2016:153.13 2017:9.8K 2018:359.64 2019:215.0K 2020:18.9K 2021:40.0K 2022:35.98M 2023:4.7K 2024:57.12M 2025:1.01M
  F2, F3, F1                                2012:25.0K 2014:101.24 2015:499.95 2016:225.02 2017:2.9K 2018:720.66 2019:2.7K 2020:6.4K 2021:6.3K 2022:986.97 2023:617.52 2024:726.45 2025:206.01
  F3                                        2010:64.74 2012:9.23 2013:40.14 2014:101.68 2015:78.78 2016:264.6K 2017:61.87M 2018:77.51M 2019:242.1K 2020:9.32M 2021:810.8K 2022:40.29M 2023:59.82M 2024:1.31M 2025:443.0K 2027:17.71
  F3, F2                                    2016:7.8K 2017:100.2K 2018:10.6K 2019:74.57 2020:49.4K 2021:10.8K 2022:12.46M 2023:22.5K 2024:16.1K 2025:9.6K
  F3, F4                                    2013:5.67 2016:2.4K 2017:2.8K 2018:4.2K 2019:4.9K 2020:14.5K 2021:26.3K 2022:9.0K 2023:2.8K 2024:1.4K 2025:151.93
  F4                                        2008:6.25 2010:1 2014:1 2015:146.21 2016:17.40M 2017:99.3K 2018:49.5K 2019:51.0K 2020:50.55M 2021:126.1K 2022:45.9K 2023:226.3K 2024:70.7K 2025:20.0K
  F4, F3                                    2020:0 2021:51.5K 2022:5.5K 2023:2.9K 2024:30.00M 2025:474.19
  F4, F5                                    2016:1.1K 2017:2.0K 2018:2.7K 2020:124.76M 2021:19.3K 2022:1.9K 2023:10.7K 2024:474.26 2025:83.77
  F5                                        2010:0 2011:0 2012:24 2013:90.24 2014:513.73 2015:5.60M 2016:1.59M 2017:39.5K 2018:29.3K 2019:45.3K 2020:28.76M 2021:80.0K 2022:24.5K 2023:203.8K 2024:75.0K 2025:4.4K
  F6                                        2013:12.43 2015:102.0K 2016:2.16M 2017:37.3K 2018:34.0K 2019:36.9K 2020:8.93M 2021:50.7K 2022:11.3K 2023:14.4K 2024:74.3K 2025:5.8K
  F7                                        2008:19.79 2015:1 2016:107.0K 2017:14.4K 2018:37.7K 2019:40.8K 2020:13.04M 2021:56.2K 2022:14.2K 2023:489.7K 2024:57.4K 2025:24.4K
  F8                                        2015:6.98M 2016:105.4K 2017:9.1K 2018:28.9K 2019:25.1K 2020:46.0K 2021:79.3K 2022:9.5K 2023:22.3K 2024:62.4K 2025:5.5K
  F9                                        2015:5.04M 2016:3.9K 2017:7.2K 2018:21.5K 2019:20.5K 2020:46.4K 2021:104.5K 2022:11.4K 2023:27.2K 2024:58.9K 2025:12.0K

## what

TRANS_DATE_FN: F1 78%, F2 12%, F3 4%, F4 2%, F5 1%, F2, F1 1%, F6 1%, F1, F2 0%, F7 0%, F8 0%, F13 0%

DEEMED_EXECUTION_DATE_FN: F1 82%, F2 12%, F3 3%, F4 1%, F5 0%, F2, F1 0%, F1, F4 0%, 4 0%, F6 0%, F8 0%, F7 0%

TRANS_FORM_TYPE: 4 97%, 5 3%, F 0%

TRANS_CODE: S 28%, A 21%, F 16%, M 15%, P 11%, J 3%, G 3%, D 2%, C 2%, L 0%, X 0%, U 0%

EQUITY_SWAP_INVOLVED: 0 92%, false 8%, 1 0%, true 0%

TRANS_TIMELINESS: E 91%, L 9%

TRANS_TIMELINESS_FN: F1 81%, F2 11%, F3 5%, F4 1%, F7 1%, F5 0%, F6 0%, 1621.0 0%

TRANS_ACQUIRED_DISP_CD: A 51%, D 49%

TRANS_ACQUIRED_DISP_CD_FN: F1 71%, F2 17%, F3 6%, F4 3%, F5 2%, F6 1%, F1, F2 0%, F3, F1 0%, F2, F1 0%, F7 0%, F1, F3 0%

VALU_OWND_FOLWNG_TRANS_FN: F2 67%, F1 26%, F3 4%, F7 1%, F10, F11 1%, F2, F1 1%, D 1%, F5 1%

DIRECT_INDIRECT_OWNERSHIP: D 83%, I 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACCESSION_NUMBER | other | 1.33M | 0 | 0001209191-21-058512 2.1K; 0001209191-21-058517 2.1K; 0001209191-21-058521 2.1K; 0001209191-21-058527 2.1K |
| NONDERIV_TRANS_SK | id | 2.70M | 0 | 5868739 2.1K; 5868738 2.1K; 5868887 2.1K; 5868888 2.1K |
| SECURITY_TITLE | who | 4.6K | 0 | Common Stock 1.70M; Class A Common Stock 351.3K; Common Shares 57.1K; Ordinary Shares 38.5K |
| SECURITY_TITLE_FN | who | 259 | 2.58M | F1 67.0K; F2 8.1K; F2, F1 3.5K; F3 3.3K |
| TRANS_DATE | date | 4.6K | 1 | 01-MAR-2021 6.5K; 01-MAR-2024 6.5K; 01-MAR-2022 5.7K; 01-MAR-2023 5.7K |
| TRANS_DATE_FN | category | 49 | 2.66M | F1 13.0K; F2 2.0K; F3 662; F4 397 |
| DEEMED_EXECUTION_DATE | date | 2.5K | 2.64M | 16-AUG-2022 188; 04-JAN-2025 121; 15-AUG-2022 107; 04-JAN-2024 107 |
| DEEMED_EXECUTION_DATE_FN | category | 13 | 2.67M | F1 1.1K; F2 159; F3 39; F4 19 |
| TRANS_FORM_TYPE | category | 4 | 1 | 4 2.58M; 5 90.6K; F 1 |
| TRANS_CODE | category | 20 | 1 | S 751.4K; A 548.5K; F 421.1K; M 395.1K |
| EQUITY_SWAP_INVOLVED | category | 5 | 2 | 0 2.46M; false 213.0K; 1 1.8K; true 50 |
| EQUITY_SWAP_TRANS_CD_FN | other | 353 | 2.00M | F1 493.1K; F2 86.6K; F3 36.5K; F4 13.7K |
| TRANS_TIMELINESS | category | 3 | 2.63M | E 41.8K; L 4.3K |
| TRANS_TIMELINESS_FN | category | 9 | 2.67M | F1 583; F2 79; F3 38; F4 9 |
| TRANS_SHARES | amount | 208.5K | 0 | 10000.0 33.3K; 5000.0 32.7K; 100.0 32.6K; 1000.0 31.8K |
| TRANS_SHARES_FN | other | 351 | 1.94M | F1 521.6K; F2 113.5K; F3 47.8K; F4 19.5K |
| TRANS_PRICEPERSHARE | amount | 80.7K | 177.8K | 0.0 651.3K; 10.0 4.1K; 25.0 4.0K; 2.75 3.8K |
| TRANS_PRICEPERSHARE_FN | other | 713 | 1.82M | F1 300.0K; F2 198.5K; F3 103.0K; F4 66.2K |
| TRANS_ACQUIRED_DISP_CD | category | 3 | 1 | A 1.35M; D 1.32M |
| TRANS_ACQUIRED_DISP_CD_FN | category | 50 | 2.66M | F1 9.5K; F2 2.3K; F3 762; F4 362 |
| SHRS_OWND_FOLWNG_TRANS | amount | 937.5K | 754 | 0.0 86.2K; 5000.0 5.0K; 13583.0 3.2K; 629303.0 2.0K |
| SHRS_OWND_FOLWNG_TRANS_FN | other | 943 | 2.34M | F2 148.6K; F1 86.0K; F3 40.2K; F4 11.3K |
| VALU_OWND_FOLWNG_TRANS | amount | 572 | 2.67M | 0.0 54; 3125.0 28; 5000.0 22; 1250.0 19 |
| VALU_OWND_FOLWNG_TRANS_FN | category | 9 | 2.67M | F2 92; F1 36; F3 5; F7 1 |
| DIRECT_INDIRECT_OWNERSHIP | category | 3 | 1 | D 2.21M; I 461.2K |
| DIRECT_INDIRECT_OWNERSHIP_FN | who | 884 | 2.61M | F2 16.7K; F1 16.1K; F3 9.1K; F4 2.7K |
| NATURE_OF_OWNERSHIP | who | 21.3K | 2.21M | See footnote 37.1K; See Footnote 35.5K; By Trust 27.9K; See Footnotes 23.3K |
| NATURE_OF_OWNERSHIP_FN | who | 3.6K | 2.40M | F2 57.4K; F3 47.0K; F1 46.9K; F4 15.4K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-24 02:30:07.000 2.67M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 8475bcc4-c7ad-4134-a69a-2 2.67M |
| _SRC_SHA256 | other | 1 | 0 | manifest_members:35:NONDE 2.67M |
