# FED_TREASURY_DTS_DEPOSITS

rows 478.1K  columns 20  scan 5.8s

roles: amount 3, audit 2, category 9, date 2, other 3, who 2

## when

RECORD_DATE
  2005      3.3K  ##
  2006     13.6K  #########
  2007     13.6K  #########
  2008     14.2K  #########
  2009     15.0K  ##########
  2010     15.3K  ##########
  2011     15.2K  ##########
  2012     15.0K  ##########
  2013     15.0K  ##########
  2014     14.8K  ##########
  2015     15.2K  ##########
  2016     15.1K  ##########
  2017     15.1K  ##########
  2018     15.2K  ##########
  2019     15.5K  ##########
  2020     23.8K  ################
  2021     37.4K  #########################
  2022     42.5K  ############################
  2023     44.8K  #############################
  2024     45.6K  ##############################
  2025     45.6K  ##############################
  2026     27.4K  ##################

_INGESTED_AT
  2026    478.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TRANSACTION_FYTD_AMT | 478.1K | -88.5K | 7.0K | 6.96M | 36.92M | 130.83B |
| TRANSACTION_MTD_AMT | 478.1K | -62.0K | 510 | 582.9K | 3.69M | 11.28B |
| TRANSACTION_TODAY_AMT | 478.1K | -41.3K | 43 | 56.1K | 582.6K | 1.06B |

## who

TRANSACTION_CATG by rows
     26.0K  Other Withdrawals
     10.8K  Other Deposits
      8.4K  Justice Department programs
      8.4K  Housing and Urban Development programs
      7.7K  Deposits by States
      7.6K  Commodity Credit Corporation programs
      7.1K  Education Department programs
      7.1K  Energy Department programs
      5.2K  Interest on Treasury Securities
      5.2K  Federal Reserve Earnings
      5.2K  Federal Salaries (EFT)
      4.5K  Postal Service Money Orders and Other
      4.5K  Postal Service
      4.5K  Defense Vendor Payments (EFT)
      4.4K  Individual Income and Employment Taxes, Not Withheld
      4.4K  Estate and Gift Taxes
      4.3K  Public Debt Cash Redemp. (Table III-B)
      4.3K  Public Debt Cash Issues (Table III-B)
      4.2K  Federal Employees Insurance Payments
      4.2K  Transfers from Depositaries

TRANSACTION_CATG by dollars
      20.71B     4.3K rows  Public Debt Cash Issues (Table III-B)
      18.32B     4.3K rows  Public Debt Cash Redemp. (Table III-B)
      13.22B      979 rows  Public Debt Cash Issues (Table IIIB)
      12.52B      979 rows  Public Debt Cash Redemp. (Table IIIB)
       3.77B     2.6K rows  Cash FTD's Received (Table IV)
       1.85B     4.0K rows  Transfers to Federal Reserve Account (Table V)
       1.85B     4.2K rows  Transfers from Depositaries
       1.82B     3.5K rows  FTD's Received (Table IV)
       1.54B      874 rows  Taxes - Withheld Individual/FICA
       1.50B      365 rows  Sub-Total Withdrawals
       1.43B     4.0K rows  Social Security Benefits (EFT)
       1.19B      365 rows  Sub-Total Deposits
       1.10B    26.0K rows  Other Withdrawals
     843.37M     4.4K rows  Individual Income and Employment Taxes, Not Withheld
     808.02M     1.3K rows  SSA - Benefits Payments
     777.54M     4.5K rows  Defense Vendor Payments (EFT)
     727.70M     5.2K rows  Interest on Treasury Securities
     575.11M     2.3K rows  Medicare
     568.35M     4.0K rows  Transfers from Federal Reserve Account (Table V)
     568.35M     4.2K rows  Transfers to Depositaries

TRANSACTION_CATG_DESC by rows
      4.5K  Unclassified
      4.3K  Thrift Savings Plan Transfer
      4.0K  Supplemental Security Income
      3.8K  Unemployment
      1.8K  Medicare Premiums
      1.7K  Federal Housing Admin: Note Sales
      1.5K  TARP
      1.5K  Emergency Prep & Response (DHS)
      1.4K  Interior
      1.3K  Agency for Internat'l Development
      1.3K  Federal Transit Admin.
      1.1K  State Department
       952  Agriculture
       912  IRS Tax Refunds Business (EFT)
       692  Transportation Security Admin. (DHS)
       689  IRS Tax Refunds Individual (EFT)
       677  Federal Crop Ins. Corp.
       646  Deposit Insurance Fund
       593  Defense Finance & Accounting Service
       542  Federal Aviation Administration

TRANSACTION_CATG_DESC by dollars
     766.53M     4.5K rows  Unclassified
      92.03M      689 rows  IRS Tax Refunds Individual (EFT)
      88.65M     4.3K rows  Thrift Savings Plan Transfer
      71.40M     3.8K rows  Unemployment
      68.68M     1.5K rows  TARP
      27.14M     1.8K rows  Medicare Premiums
      22.07M      912 rows  IRS Tax Refunds Business (EFT)
      18.40M      439 rows  Military Active Duty Pay (EFT)
      15.91M     1.7K rows  Federal Housing Admin: Note Sales
      14.22M     1.5K rows  Emergency Prep & Response (DHS)
      13.15M      380 rows  Veterans Benefits (EFT)
      10.66M     1.3K rows  Agency for Internat'l Development
       8.32M     1.4K rows  Interior
       7.98M      339 rows  Supple. Security Income Benefits (EFT)
       7.61M     4.0K rows  Supplemental Security Income
       7.54M     1.3K rows  Federal Transit Admin.
       7.37M      646 rows  Deposit Insurance Fund
       7.21M      268 rows  Military Retirement (EFT)
       6.57M      952 rows  Agriculture
       6.47M      200 rows  Civil Service Retirement (EFT)

## who x when

TRANSACTION_CATG by RECORD_DATE, dollars = TRANSACTION_FYTD_AMT
  Cash FTD's Received (Table IV)            2012:15.49M 2013:292.44M 2014:313.94M 2015:340.63M 2016:348.27M 2017:359.50M 2018:366.06M 2019:373.05M 2020:373.01M 2021:429.37M 2022:520.40M 2023:36.42M
  Commodity Credit Corporation programs     2005:850.6K 2006:7.71M 2007:6.40M 2008:5.91M 2009:5.04M 2010:4.55M 2011:4.51M 2012:3.94M 2013:4.10M 2014:3.41M 2015:3.08M 2016:3.74M 2017:4.27M 2018:4.11M 2019:5.12M 2020:5.16M
  Defense Vendor Payments (EFT)             2005:2.13M 2006:36.57M 2007:38.42M 2008:43.97M 2009:48.04M 2010:49.88M 2011:49.60M 2012:47.17M 2013:43.30M 2014:39.52M 2015:37.40M 2016:36.52M 2017:35.05M 2018:38.63M 2019:43.40M 2020:47.26M 2021:46.13M 2022:49.18M 2023:45.37M
  Deposits by States                        2005:233.1K 2006:4.75M 2007:4.53M 2008:4.38M 2009:4.16M 2010:4.85M 2011:6.47M 2012:7.35M 2013:6.40M 2014:6.09M 2015:5.69M 2016:5.39M 2017:5.01M 2018:4.76M 2019:4.57M 2020:4.15M 2021:232.3K
  Education Department programs             2005:899.2K 2006:15.33M 2007:13.60M 2008:14.11M 2009:24.03M 2010:32.68M 2011:34.08M 2012:31.17M 2013:29.54M 2014:29.32M 2015:30.30M 2016:30.37M 2017:30.45M 2018:30.59M 2019:29.85M
  Energy Department programs                2005:282.6K 2006:4.52M 2007:4.32M 2008:4.48M 2009:4.76M 2010:5.44M 2011:6.35M 2012:6.05M 2013:5.25M 2014:5.09M 2015:5.07M 2016:5.10M 2017:5.17M 2018:5.44M 2019:5.51M
  Estate and Gift Taxes                     2005:196.0K 2006:3.36M 2007:3.38M 2008:3.78M 2009:3.24M 2010:2.21M 2011:968.6K 2012:1.73M 2013:2.40M 2014:2.39M 2015:2.48M 2016:2.75M 2017:2.72M 2018:2.84M 2019:2.11M 2020:2.12M 2021:2.90M 2022:3.48M 2023:225.2K
  FTD's Received (Table IV)                 2005:13.45M 2006:252.87M 2007:270.19M 2008:278.05M 2009:250.34M 2010:248.11M 2011:256.14M 2012:248.49M
  Federal Employees Insurance Payments      2005:359.0K 2006:6.16M 2007:6.69M 2008:7.22M 2009:7.62M 2010:7.99M 2011:8.44M 2012:8.71M 2013:8.88M 2014:9.17M 2015:9.71M 2016:9.59M 2017:9.64M 2018:9.97M 2019:10.68M 2020:10.95M 2021:11.37M 2022:3.81M
  Federal Reserve Earnings                  2005:165.7K 2006:3.65M 2007:3.81M 2008:4.59M 2009:4.04M 2010:9.43M 2011:10.61M 2012:9.89M 2013:9.69M 2014:12.55M 2015:11.90M 2016:15.85M 2017:10.38M 2018:9.20M 2019:6.74M 2020:9.37M 2021:11.45M 2022:14.08M 2023:117.9K 2024:333.9K 2025:681.4K 2026:673.7K
  Federal Salaries (EFT)                    2005:1.15M 2006:18.94M 2007:19.31M 2008:20.46M 2009:22.54M 2010:22.66M 2011:22.70M 2012:22.15M 2013:21.67M 2014:21.08M 2015:21.16M 2016:21.86M 2017:22.14M 2018:23.09M 2019:24.22M 2020:25.52M 2021:26.86M 2022:26.64M 2023:27.43M 2024:29.71M 2025:30.91M 2026:21.16M
  Housing and Urban Development programs    2005:481.8K 2006:7.38M 2007:7.91M 2008:8.10M 2009:7.75M 2010:9.80M 2011:10.44M 2012:10.13M 2013:10.96M 2014:10.93M 2015:10.15M 2016:9.99M 2017:9.59M 2018:9.32M 2019:9.83M 2020:9.76M 2021:9.98M 2022:3.53M
  Individual Income and Employment Taxes,   2005:729.2K 2006:44.84M 2007:50.72M 2008:53.53M 2009:39.95M 2010:34.51M 2011:38.49M 2012:38.96M 2013:48.25M 2014:51.16M 2015:57.55M 2016:55.16M 2017:52.26M 2018:56.14M 2019:55.23M 2020:39.74M 2021:53.77M 2022:69.60M 2023:2.79M
  Interest on Treasury Securities           2005:1.05M 2006:18.62M 2007:21.01M 2008:22.11M 2009:21.30M 2010:22.61M 2011:25.48M 2012:27.53M 2013:27.97M 2014:27.17M 2015:28.76M 2016:29.99M 2017:30.68M 2018:33.45M 2019:37.51M 2020:39.20M 2021:36.93M 2022:36.94M 2023:47.24M 2024:61.27M 2025:73.71M 2026:57.18M
  Justice Department programs               2005:145.4K 2006:2.47M 2007:2.32M 2008:2.14M 2009:2.63M 2010:3.19M 2011:3.64M 2012:3.24M 2013:3.10M 2014:4.78M 2015:4.94M 2016:4.12M 2017:4.52M 2018:3.51M 2019:4.33M 2020:4.75M 2021:4.02M 2022:1.05M
  Other Deposits                            2005:38.0K 2006:835.1K 2007:1.13M 2008:3.11M 2009:6.98M 2010:22.10M 2011:10.36M 2012:7.05M 2013:12.02M 2014:6.88M 2015:8.55M 2016:7.40M 2017:7.13M 2018:8.87M 2019:8.28M 2020:9.56M 2021:6.45M 2022:4.71M 2023:75.6K
  Other Withdrawals                         2005:3.11M 2006:55.22M 2007:56.28M 2008:71.11M 2009:131.48M 2010:87.75M 2011:78.32M 2012:73.93M 2013:48.46M 2014:42.98M 2015:43.47M 2016:45.02M 2017:48.90M 2018:49.53M 2019:50.81M 2020:50.06M 2021:58.66M 2022:47.10M 2023:53.44M
  Postal Service                            2005:792.9K 2006:12.98M 2007:13.13M 2008:13.19M 2009:12.16M 2010:11.67M 2011:11.55M 2012:11.37M 2013:11.38M 2014:11.50M 2015:11.67M 2016:11.83M 2017:11.63M 2018:11.73M 2019:11.94M 2020:12.16M 2021:12.67M 2022:12.46M 2023:11.67M
  Postal Service Money Orders and Other     2005:390.8K 2006:6.50M 2007:6.42M 2008:6.26M 2009:5.73M 2010:5.43M 2011:5.33M 2012:5.17M 2013:5.10M 2014:4.99M 2015:5.06M 2016:5.11M 2017:5.18M 2018:5.22M 2019:5.41M 2020:5.42M 2021:5.49M 2022:5.49M 2023:5.35M
  Public Debt Cash Issues (Table III-B)     2005:33.35M 2006:565.24M 2007:572.37M 2008:685.99M 2009:1.15B 2010:1.05B 2011:1.03B 2012:997.96M 2013:1.06B 2014:948.69M 2015:923.28M 2016:1.03B 2017:1.13B 2018:1.28B 2019:1.50B 2020:2.19B 2021:2.66B 2022:1.90B
  Public Debt Cash Issues (Table IIIB)      2022:391.76M 2023:2.48B 2024:3.67B 2025:3.90B 2026:2.79B
  Public Debt Cash Redemp. (Table III-B)    2005:28.91M 2006:530.48M 2007:548.78M 2008:618.27M 2009:932.18M 2010:877.11M 2011:892.24M 2012:840.69M 2013:938.36M 2014:864.90M 2015:846.68M 2016:923.18M 2017:1.07B 2018:1.14B 2019:1.38B 2020:1.74B 2021:2.45B 2022:1.69B
  Public Debt Cash Redemp. (Table IIIB)     2022:362.31M 2023:2.31B 2024:3.46B 2025:3.74B 2026:2.65B
  SSA - Benefits Payments                   2021:56.71M 2022:136.04M 2023:150.66M 2024:163.34M 2025:176.64M 2026:124.63M
  Social Security Benefits (EFT)            2005:3.69M 2006:56.01M 2007:59.53M 2008:64.13M 2009:71.14M 2010:74.60M 2011:78.10M 2012:84.29M 2013:92.19M 2014:98.21M 2015:103.36M 2016:106.27M 2017:108.34M 2018:111.22M 2019:117.38M 2020:124.96M 2021:71.92M
  Sub-Total Deposits                        2022:565.89M 2023:625.27M
  Sub-Total Withdrawals                     2022:677.67M 2023:820.47M
  Taxes - Withheld Individual/FICA          2023:373.13M 2024:415.94M 2025:439.06M 2026:310.44M
  Transfers from Depositaries               2005:15.63M 2006:310.93M 2007:388.98M 2008:431.05M 2009:233.18M 2010:174.54M 2011:176.02M 2012:121.80M 2013:0 2014:0 2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0
  Transfers to Federal Reserve Account (Ta  2005:15.63M 2006:310.93M 2007:388.98M 2008:431.05M 2009:233.18M 2010:174.54M 2011:176.02M 2012:121.80M 2013:0 2014:0 2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0

TRANSACTION_CATG_DESC by RECORD_DATE, dollars = TRANSACTION_FYTD_AMT
  Agency for Internat'l Development         2005:13.0K 2006:177.1K 2007:131.6K 2008:199.6K 2009:321.9K 2010:513.5K 2011:560.7K 2012:505.0K 2013:432.2K 2014:499.8K 2015:679.3K 2016:552.7K 2017:661.1K 2018:842.5K 2019:763.7K 2020:881.7K 2021:1.28M 2022:1.64M
  Agriculture                               2008:7.8K 2009:252.9K 2010:247.6K 2011:271.4K 2012:213.2K 2013:434.8K 2014:367.9K 2015:506.8K 2016:453.5K 2017:590.0K 2018:733.0K 2019:860.3K 2020:1.63M
  Civil Service Retirement (EFT)            2005:22.0K 2006:295.1K 2007:310.5K 2008:324.2K 2009:344.5K 2010:357.5K 2011:358.8K 2012:373.4K 2013:392.9K 2014:406.9K 2015:418.1K 2016:422.6K 2017:424.0K 2018:436.6K 2019:454.8K 2020:465.9K 2021:470.3K 2022:186.8K
  Defense Finance & Accounting Service      2005:8.9K 2006:196.0K 2007:165.9K 2008:179.3K 2009:157.1K 2010:99.3K 2011:107.6K 2012:150.6K 2013:156.6K 2014:116.4K 2015:122.6K 2016:113.8K 2017:78.9K 2018:66.0K 2019:70.3K 2020:51.8K 2021:44.3K 2022:63.2K 2023:69.8K
  Deposit Insurance Fund                    2008:70.2K 2009:2.53M 2010:2.79M 2011:581.8K 2012:327.9K 2013:238.8K 2014:180.0K 2015:184.0K 2016:116.6K 2017:96.4K 2018:158.2K 2019:55.5K 2020:38.4K
  Emergency Prep & Response (DHS)           2005:467.1K 2006:3.93M 2007:256.3K 2008:357.1K 2009:836.5K 2010:320.7K 2011:405.6K 2012:526.4K 2013:1.52M 2014:316.4K 2015:145.7K 2016:411.4K 2017:918.0K 2018:2.47M 2019:1.06M 2020:280.4K
  Federal Aviation Administration           2005:8.2K 2006:127.6K 2007:120.9K 2008:107.8K 2009:160.1K 2010:157.9K 2011:154.2K 2012:130.7K 2013:142.9K 2014:176.6K 2015:103.3K 2016:129.1K 2017:129.5K 2018:164.1K 2019:211.2K 2020:180.8K
  Federal Crop Ins. Corp.                   2006:14.5K 2007:16.5K 2008:60.5K 2009:351.9K 2010:84.2K 2011:323.8K 2012:374.3K 2013:1.22M 2014:379.1K 2015:291.4K 2016:33.9K 2017:51.2K 2018:78.9K 2019:606.7K 2020:306.0K
  Federal Housing Admin: Note Sales         2005:3.1K 2006:22.2K 2007:20.8K 2008:46.1K 2009:658.7K 2010:1.01M 2011:721.6K 2012:885.2K 2013:1.92M 2014:1.28M 2015:1.32M 2016:1.35M 2017:1.06M 2018:718.7K 2019:849.4K 2020:1.31M 2021:1.96M 2022:760.8K
  Federal Transit Admin.                    2005:2.7K 2006:95.2K 2007:109.4K 2008:175.1K 2009:496.4K 2010:690.9K 2011:562.2K 2012:513.2K 2013:533.6K 2014:619.3K 2015:591.0K 2016:518.6K 2017:612.0K 2018:638.2K 2019:727.9K 2020:651.7K
  IRS Tax Refunds Business (EFT)            2005:56.6K 2006:561.3K 2007:649.7K 2008:2.14M 2009:5.92M 2010:7.72M 2011:3.70M 2012:1.33M
  IRS Tax Refunds Individual (EFT)          2005:6.7K 2006:4.86M 2007:8.58M 2008:13.27M 2009:14.72M 2010:15.97M 2011:15.12M 2012:19.50M
  Interior                                  2006:442.6K 2007:620.8K 2008:653.8K 2009:565.4K 2010:731.4K 2011:745.0K 2012:521.4K 2013:432.1K 2014:385.4K 2015:445.8K 2016:560.0K 2017:442.0K 2018:472.7K 2019:523.0K 2020:780.4K 2021:681
  Medicare Premiums                         2008:1.06M 2009:1.21M 2010:1.23M 2011:1.60M 2012:1.77M 2013:1.73M 2014:2.04M 2015:3.46M 2016:2.72M 2017:3.43M 2018:2.90M 2019:3.59M 2020:392.1K
  Military Active Duty Pay (EFT)            2005:55.4K 2006:809.9K 2007:789.4K 2008:900.4K 2009:965.6K 2010:1.02M 2011:1.17M 2012:988.2K 2013:1.03M 2014:1.07M 2015:980.5K 2016:1.03M 2017:972.5K 2018:953.2K 2019:1.08M 2020:1.10M 2021:1.15M 2022:1.23M 2023:1.10M
  Military Retirement (EFT)                 2005:17.4K 2006:236.0K 2007:250.7K 2008:264.2K 2009:285.6K 2010:296.5K 2011:348.1K 2012:402.6K 2013:427.9K 2014:478.7K 2015:447.6K 2016:424.5K 2017:418.4K 2018:456.4K 2019:485.9K 2020:496.2K 2021:480.0K 2022:496.1K 2023:496.4K
  State Department                          2005:4.1K 2006:58.8K 2007:60.2K 2008:135.6K 2009:226.0K 2010:158.6K 2011:299.9K 2012:355.7K 2013:251.2K 2014:226.1K 2015:281.1K 2016:430.5K 2017:323.7K 2018:294.6K 2019:462.7K 2020:1.11M 2021:1.22M 2022:440.5K
  Supple. Security Income Benefits (EFT)    2005:10.3K 2006:138.4K 2007:140.5K 2008:166.5K 2009:346.1K 2010:411.2K 2011:477.1K 2012:488.7K 2013:622.8K 2014:674.0K 2015:685.6K 2016:718.0K 2017:640.8K 2018:622.5K 2019:703.7K 2020:710.8K 2021:427.8K
  Supplemental Security Income              2005:24.8K 2006:525.3K 2007:537.2K 2008:556.0K 2009:522.9K 2010:483.3K 2011:571.3K 2012:524.4K 2013:517.9K 2014:515.1K 2015:441.8K 2016:436.2K 2017:452.4K 2018:428.1K 2019:423.2K 2020:418.0K 2021:232.3K
  TARP                                      2008:1.59M 2009:30.49M 2010:19.52M 2011:7.40M 2012:2.76M 2013:5.45M 2014:1.19M 2015:127.2K 2016:55.0K 2017:50.5K 2018:18.0K 2019:13.5K 2020:6.4K 2021:4.7K 2022:361
  Thrift Savings Plan Transfer              2005:79.0K 2006:1.39M 2007:2.02M 2008:1.76M 2009:1.93M 2010:1.66M 2011:2.50M 2012:2.76M 2013:3.99M 2014:3.85M 2015:5.09M 2016:4.95M 2017:6.45M 2018:8.80M 2019:7.79M 2020:14.40M 2021:11.87M 2022:7.36M
  Transportation Security Admin. (DHS)      2005:15.6K 2006:241.4K 2007:250.6K 2008:251.5K
  Unclassified                              2005:2.32M 2006:41.73M 2007:42.13M 2008:48.45M 2009:73.13M 2010:52.26M 2011:48.39M 2012:43.63M 2013:36.51M 2014:32.90M 2015:33.35M 2016:34.55M 2017:36.22M 2018:35.21M 2019:35.33M 2020:33.25M 2021:45.84M 2022:39.53M 2023:51.81M
  Unemployment                              2005:208.3K 2006:4.23M 2007:4.00M 2008:3.83M 2009:3.64M 2010:4.37M 2011:5.90M 2012:6.82M 2013:5.88M 2014:5.57M 2015:5.25M 2016:4.95M 2017:4.56M 2018:4.33M 2019:4.15M 2020:3.73M
  Veterans Benefits (EFT)                   2005:13.1K 2006:177.1K 2007:172.1K 2008:206.3K 2009:315.9K 2010:310.6K 2011:1.26M 2012:863.5K 2013:1.26M 2014:1.39M 2015:1.31M 2016:1.56M 2017:1.48M 2018:1.12M 2019:1.69M 2020:33.5K

## what

ACCOUNT_TYPE: Federal Reserve Account 53%, Treasury General Account (TGA) 45%, Tax and Loan Note Accounts 1%, Short-Term Cash Investments 1%, Treasury General Account Total 0%, Treasury General Account Total 0%, Other Withdrawals 0%

RECORD_CALENDAR_DAY: 03 8%, 06 8%, 22 8%, 23 8%, 24 8%, 13 8%, 27 8%, 15 8%, 08 8%, 07 8%, 09 8%, 28 8%

RECORD_CALENDAR_MONTH: 03 9%, 07 9%, 04 9%, 06 9%, 05 9%, 08 9%, 12 8%, 10 8%, 01 8%, 09 8%, 11 8%, 02 8%

RECORD_CALENDAR_QUARTER: 2 26%, 3 25%, 1 25%, 4 24%

RECORD_CALENDAR_YEAR: 2025 13%, 2024 13%, 2023 13%, 2022 12%, 2021 11%, 2026 8%, 2020 7%, 2019 5%, 2010 4%, 2011 4%, 2018 4%, 2015 4%

RECORD_FISCAL_QUARTER: 3 26%, 4 25%, 2 25%, 1 24%

RECORD_FISCAL_YEAR: 2025 13%, 2024 13%, 2023 13%, 2022 12%, 2026 11%, 2021 10%, 2020 6%, 2019 4%, 2011 4%, 2010 4%, 2015 4%, 2018 4%

TRANSACTION_TYPE: Withdrawals 59%, Deposits 41%

_SRC_SHA256: 7124ade3d968e0a1 8%, 8223c1a4c51fefe9 8%, ef80937b9b999c1d 8%, f3766f4e1b64d9b7 8%, 846fa25ee4c20ad6 8%, 647ee4456a0109c6 8%, 0b58da18ccbe2336 8%, 457d6ba73f9b097a 8%, 9309f4d8eef5168e 8%, 1b4038d94e8c059c 8%, e19291417fbdfee7 8%, 61f1170a6ebffa4e 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACCOUNT_TYPE | category | 7 | 0 | Federal Reserve Account 252.9K; Treasury General Account  213.0K; Tax and Loan Note Account 5.3K; Short-Term Cash Investmen 4.8K |
| RECORD_CALENDAR_DAY | category | 31 | 0 | 03 16.3K; 06 16.2K; 22 16.1K; 23 16.0K |
| RECORD_CALENDAR_MONTH | category | 12 | 0 | 03 42.6K; 07 42.1K; 04 41.5K; 06 41.2K |
| RECORD_CALENDAR_QUARTER | category | 4 | 0 | 2 123.8K; 3 120.4K; 1 117.3K; 4 116.6K |
| RECORD_CALENDAR_YEAR | category | 22 | 0 | 2025 45.6K; 2024 45.6K; 2023 44.8K; 2022 42.5K |
| RECORD_DATE | date | 5.2K | 0 | 2017-03-31 1.4K; 2017-04-03 1.4K; 2017-04-13 1.4K; 2017-03-30 1.4K |
| RECORD_FISCAL_QUARTER | category | 4 | 0 | 3 123.8K; 4 120.4K; 2 117.3K; 1 116.6K |
| RECORD_FISCAL_YEAR | category | 21 | 0 | 2025 45.8K; 2024 45.4K; 2023 44.1K; 2022 41.7K |
| SRC_LINE_NBR | other | 186 | 0 | 14 5.2K; 13 5.2K; 4 5.2K; 8 5.2K |
| TABLE_NBR | other | 1 | 0 | II 478.1K |
| TABLE_NM | other | 1 | 0 | Deposits and Withdrawals  478.1K |
| TRANSACTION_CATG | who | 517 | 2.2K | Other Withdrawals 26.0K; Other Deposits 10.8K; Housing and Urban Develop 8.4K; Justice Department progra 8.4K |
| TRANSACTION_CATG_DESC | who | 120 | 433.6K | Unclassified 4.5K; Thrift Savings Plan Trans 4.3K; Supplemental Security Inc 4.0K; Unemployment 3.8K |
| TRANSACTION_FYTD_AMT | amount | 123.1K | 0 | 0 18.7K; 3904 2.3K; 18260 2.3K; 18358 2.3K |
| TRANSACTION_MTD_AMT | amount | 51.4K | 0 | 0 37.5K; 1 6.5K; 2 4.2K; 3 3.4K |
| TRANSACTION_TODAY_AMT | amount | 18.4K | 0 | 0 78.8K; 1 22.1K; 2 13.7K; 3 10.1K |
| TRANSACTION_TYPE | category | 2 | 0 | Withdrawals 279.7K; Deposits 198.4K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-11T14:21:00.83917 478.1K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 412b389e-797f-4241-a166-c 478.1K |
| _SRC_SHA256 | category | 48 | 0 | 7124ade3d968e0a1 10.0K; 8223c1a4c51fefe9 10.0K; ef80937b9b999c1d 10.0K; f3766f4e1b64d9b7 10.0K |
