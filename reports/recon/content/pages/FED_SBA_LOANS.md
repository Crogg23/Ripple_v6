# FED_SBA_LOANS

rows 2.17M  columns 55  scan 10.6s

roles: amount 3, audit 2, category 11, date 5, other 14, state 5, who 15

## when

ASOFDATE
  2026     2.17M  ##############################

APPROVALDATE
  1990      4.3K  #
  1991     20.7K  ######
  1992     25.8K  #######
  1993     31.0K  ########
  1994     47.2K  #############
  1995     55.2K  ###############
  1996     53.5K  ###############
  1997     49.3K  #############
  1998     47.0K  #############
  1999     49.3K  #############
  2000     47.4K  #############
  2001     49.6K  ##############
  2002     60.8K  #################
  2003     79.4K  ######################
  2004     94.2K  ##########################
  2005    103.3K  ############################
  2006    109.9K  ##############################
  2007    107.6K  #############################
  2008     65.5K  ##################
  2009     51.8K  ##############
  2010     62.4K  #################
  2011     52.1K  ##############
  2012     54.4K  ###############
  2013     53.2K  ###############
  2014     61.2K  #################
  2015     70.2K  ###################
  2016     69.3K  ###################
  2017     70.6K  ###################
  2018     63.3K  #################
  2019     57.3K  ################
  2020     46.5K  #############
  2021     62.6K  #################
  2022     59.6K  ################
  2023     64.8K  ##################
  2024     81.8K  ######################
  2025     74.6K  ####################
  2026     17.9K  #####

FIRSTDISBURSEMENTDATE
  1987         1  
  1990       277  
  1991     15.3K  #####
  1992     21.4K  #######
  1993     24.4K  #######
  1994     34.3K  ##########
  1995     50.6K  ###############
  1996     42.6K  #############
  1997     45.9K  ##############
  1998     39.4K  ############
  1999     44.0K  #############
  2000     43.6K  #############
  2001     41.3K  #############
  2002     50.4K  ###############
  2003     65.7K  ####################
  2004     79.8K  ########################
  2005     89.2K  ###########################
  2006     98.3K  ##############################
  2007     95.2K  #############################
  2008     65.6K  ####################
  2009     45.5K  ##############
  2010     48.3K  ###############
  2011     49.4K  ###############
  2012     46.2K  ##############
  2013     47.5K  ##############
  2014     53.3K  ################
  2015     59.2K  ##################
  2016     61.3K  ###################
  2017     63.6K  ###################
  2018     58.5K  ##################
  2019     51.5K  ################
  2020     41.5K  #############
  2021     54.2K  #################
  2022     53.4K  ################
  2023     55.6K  #################
  2024     64.8K  ####################
  2025     59.9K  ##################
  2026      8.4K  ###
  2028         1  

PAIDINFULLDATE
  2005    316.4K  ##############################
  2006     52.3K  #####
  2007     49.8K  #####
  2008     44.3K  ####
  2009     34.1K  ###
  2010     33.0K  ###
  2011     41.6K  ####
  2012     52.9K  #####
  2013     49.6K  #####
  2014     51.2K  #####
  2015     49.7K  #####
  2016     49.2K  #####
  2017     52.4K  #####
  2018     53.5K  #####
  2019     53.0K  #####
  2020     43.4K  ####
  2021     57.8K  #####
  2022     59.9K  ######
  2023     47.0K  ####
  2024     45.5K  ####
  2025     40.5K  ####
  2026      6.2K  #

CHARGEOFFDATE
  1991         6  
  1992       112  
  1993       358  
  1994       629  #
  1995       882  #
  1996      2.0K  ##
  1997      3.0K  ##
  1998      3.6K  ###
  1999      4.4K  ####
  2000      3.9K  ###
  2001      4.1K  ###
  2002      4.9K  ####
  2003      5.0K  ####
  2004      2.5K  ##
  2005      3.4K  ###
  2006     12.6K  ##########
  2007      8.2K  #######
  2008     20.1K  #################
  2009     21.1K  #################
  2010     36.5K  ##############################
  2011     21.9K  ##################
  2012     13.1K  ###########
  2013      9.9K  ########
  2014      8.9K  #######
  2015     11.5K  #########
  2016      7.8K  ######
  2017      5.3K  ####
  2018      5.7K  #####
  2019      4.8K  ####
  2020      3.5K  ###
  2021      4.0K  ###
  2022      4.5K  ####
  2023      3.6K  ###
  2024      3.7K  ###
  2025      4.8K  ####
  2026      1.2K  #

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| THIRDPARTYDOLLARS | 120.8K | 32.0K | 650.0K | 7.33M | 30.30M | 135.14B |
| GROSSCHARGEOFFAMOUNT | 2.17M | 0 | 0 | 338.7K | 6.91M | 29.79B |
| INITIALINTERESTRATE | 956.4K | 0 | 6.75 | 14.00 | 56 | 7.09M |

## who

BORRNAME by rows
      1.4K  SUBWAY
       556  QUIZNO'S SUBS
       506  COLD STONE CREAMERY
       438  QUIZNO'S
       426  DAIRY QUEEN
       424  THE UPS STORE
       379  DOMINO'S PIZZA
       373  DUNKIN DONUTS
       325  QUIZNO'S CLASSIC SUBS
       322  DAYS INN
       314  MAIL BOXES ETC
       313  MATCO TOOLS
       312  SUPER 8 MOTEL
       294  HOLIDAY INN EXPRESS
       282  PLAY IT AGAIN SPORTS
       244  COMFORT INN
       218  SCHLOTZSKY'S DELI
       214  CURVES FOR WOMEN
       209  MINUTEMAN PRESS
       198  CICI'S PIZZA

BORRNAME by dollars
      24.97M      322 rows  DAYS INN
      24.86M      294 rows  HOLIDAY INN EXPRESS
      21.99M      244 rows  COMFORT INN
      21.82M      506 rows  COLD STONE CREAMERY
      19.14M      108 rows  QUALITY INN
      16.27M       74 rows  COMFORT SUITES
      12.02M       89 rows  BEST WESTERN
      11.78M       40 rows  HOLIDAY INN
      10.48M       94 rows  RAMADA INN
      10.13M       56 rows  MICROTEL INN & SUITES
      10.08M      218 rows  SCHLOTZSKY'S DELI
       9.41M      312 rows  SUPER 8 MOTEL
       9.34M      556 rows  QUIZNO'S SUBS
       9.25M      156 rows  PLANET BEACH
       9.17M      144 rows  ECONO LODGE
       8.52M       61 rows  SLEEP INN
       7.96M       51 rows  COUNTRY INN & SUITES
       7.91M      110 rows  SUPER 8
       7.90M      123 rows  HUNTINGTON LEARNING CENTER
       7.34M       46 rows  COMFORT INN & SUITES

FRANCHISENAME by rows
      4.9K  SUBWAY SANDWICH SHOP                    
      2.6K  QUIZNOS                                 
      1.5K  DAIRY QUEEN                             
      1.3K  MAIL BOXES ETC. USA                     
      1.2K  DUNKIN DONUTS                           
      1.1K  The UPS Store 
      1.1K  SUPER 8 MOTEL                           
      1.1K  DAYS INN                                
       937  COLD STONE CREAMERY, INC.               
       887  BEST WESTERN INN
       767  TEMPORARY FRANCHISES                    
       743  DOMINO'S PIZZA                          
       698  HOLIDAY INN EXPRESS                     
       679  COMFORT INN                             
       676  MATCO TOOLS (RENT TOOLS)                
       663  BLIMPIE
       663  SUBWAY
       621  Subway
       561  Quality Inn by Choice Hotels /Quality Inn & Suites by Choice Hotels
       551  ACE HARDWARE                            

FRANCHISENAME by dollars
     123.12M     1.1K rows  DAYS INN                                
     118.88M      500 rows  CHOICE HOTELS INTERNATIONAL INC.        
      82.54M      698 rows  HOLIDAY INN EXPRESS                     
      77.21M     1.1K rows  SUPER 8 MOTEL                           
      75.53M      679 rows  COMFORT INN                             
      69.54M      887 rows  BEST WESTERN INN
      67.26M      488 rows  RAMADA INN                              
      65.37M     2.6K rows  QUIZNOS                                 
      55.86M      304 rows  QUALITY INN                             
      53.31M      937 rows  COLD STONE CREAMERY, INC.               
      36.72M      281 rows  HOWARD JOHNSON                          
      33.57M      446 rows  ECONO LODGE MOTEL                       
      30.90M      202 rows  MICROTEL                                
      30.55M      238 rows  HOLIDAY INN                             
      30.14M      165 rows  LA QUINTA INN                           
      28.01M     4.9K rows  SUBWAY SANDWICH SHOP                    
      27.16M      311 rows  TRAVELODGE                              
      26.88M     1.5K rows  DAIRY QUEEN                             
      23.82M      316 rows  PLANET BEACH                            
      23.71M     1.2K rows  DUNKIN DONUTS                           

THIRDPARTYLENDER_NAME by rows
      5.5K  JPMorgan Chase Bank, National Association
      3.5K  Bank of America, National Association
      2.9K  Zions Bank, A Division of
      2.8K  Wells Fargo Bank National Association
      1.7K  BMO Bank National Association
      1.5K  First-Citizens Bank & Trust Company
      1.3K  Truist Bank
      1.2K  The Huntington National Bank
      1.2K  U.S. Bank, National Association
      1.2K  Glacier Bank
      1.0K  PNC Bank, National Association
       989  Columbia Bank
       983  Regions Bank
       974  KeyBank National Association
       936  City National Bank
       916  Old National Bank
       864  SouthState Bank, National Association
       857  Fifth Third Bank
       830  Rockland Trust Company
       825  Eastern Bank

THIRDPARTYLENDER_NAME by dollars
      10.57M     2.8K rows  Wells Fargo Bank National Association
       9.15M     5.5K rows  JPMorgan Chase Bank, National Association
       8.92M     2.9K rows  Zions Bank, A Division of
       8.70M     3.5K rows  Bank of America, National Association
       8.34M      538 rows  First Interstate Bank
       7.99M     1.3K rows  Truist Bank
       7.17M      249 rows  NBT Bank, National Association
       6.95M      916 rows  Old National Bank
       6.36M     1.2K rows  The Huntington National Bank
       6.17M      447 rows  Oriental Bank
       6.01M      864 rows  SouthState Bank, National Association
       5.66M      466 rows  Ameris Bank
       5.16M      632 rows  Pinnacle Bank
       4.83M      108 rows  The Cape Cod Five Cents Savings Bank
       4.79M      983 rows  Regions Bank
       4.55M      541 rows  Western Alliance Bank
       4.49M        1 rows  MountainOne Financial, MHC.
       4.44M       35 rows  Legacy Bank
       4.28M      310 rows  Centennial Bank
       4.20M      330 rows  First Financial Bank

BANKNAME by rows
    131.1K  Wells Fargo Bank National Association
    107.3K  Bank of America, National Association
    100.6K  The Huntington National Bank
     96.0K  JPMorgan Chase Bank, National Association
     86.6K  U.S. Bank, National Association
     60.2K  PNC Bank, National Association
     49.8K  Citizens Bank, National Association
     46.9K  TD Bank, National Association
     45.8K  Manufacturers and Traders Trust Company
     39.5K  Bank of Hope
     31.2K  Zions Bank, A Division of
     29.5K  Readycap Lending, LLC
     26.9K  KeyBank National Association
     24.9K  Truist Bank
     24.0K  Columbia Bank
     23.7K  Fifth Third Bank
     22.8K  Capital One, National Association
     19.0K  Northeast Bank
     17.5K  BMO Bank National Association
     17.5K  Live Oak Banking Company

BANKNAME by dollars
       1.77B   131.1K rows  Wells Fargo Bank National Association
       1.42B    29.5K rows  Readycap Lending, LLC
     952.41M    96.0K rows  JPMorgan Chase Bank, National Association
     948.10M   107.3K rows  Bank of America, National Association
     763.09M    23.7K rows  Fifth Third Bank
     732.98M    60.2K rows  PNC Bank, National Association
     669.40M    86.6K rows  U.S. Bank, National Association
     612.76M   100.6K rows  The Huntington National Bank
     588.91M    39.5K rows  Bank of Hope
     541.02M    11.5K rows  Popular Bank
     522.80M     9.0K rows  Business Loan Center, LLC
     382.12M    46.9K rows  TD Bank, National Association
     380.61M    31.2K rows  Zions Bank, A Division of
     339.04M    19.0K rows  Northeast Bank
     339.03M    22.8K rows  Capital One, National Association
     335.46M    24.9K rows  Truist Bank
     332.85M    49.8K rows  Citizens Bank, National Association
     301.58M     6.6K rows  GE Capital Small Business Finance Corporation
     299.14M    24.0K rows  Columbia Bank
     281.68M    45.8K rows  Manufacturers and Traders Trust Company

## who x when

BORRNAME by FIRSTDISBURSEMENTDATE, dollars = GROSSCHARGEOFFAMOUNT
  BEST WESTERN                              1993:0 1994:204.2K 1995:0 1996:0 1997:561.1K 1998:638.0K 1999:1.52M 2000:0 2001:0 2002:0 2003:411.3K 2004:1.18M 2005:829.6K 2006:734.8K 2007:1.15M 2008:1.49M 2009:1.95M 2010:1.36M 2021:0
  CICI'S PIZZA                              1992:0 1993:0 1994:0 1995:106.4K 1996:426.2K 1997:334.4K 1998:458.8K 1999:343.8K 2000:711.8K 2001:198.9K 2002:0 2003:882.5K 2004:221.3K 2005:784.2K 2006:429.2K 2007:758.5K 2008:251.0K 2009:0 2010:473.4K
  COLD STONE CREAMERY                       1995:0 1996:0 1997:0 1998:0 1999:314.1K 2000:0 2001:0 2002:48.1K 2003:1.06M 2004:4.24M 2005:6.35M 2006:8.57M 2007:1.10M 2008:145.0K 2009:0 2024:0
  COMFORT INN                               1991:0 1992:0 1993:0 1994:0 1995:0 1996:0 1997:635.2K 1998:527.0K 1999:0 2000:0 2001:0 2002:616.4K 2003:0 2004:869.4K 2005:1.44M 2006:3.39M 2007:2.45M 2008:9.08M 2009:2.98M 2023:0
  COMFORT SUITES                            1991:0 1995:0 1996:533.0K 1997:0 1998:0 1999:0 2000:437.4K 2001:0 2002:0 2003:0 2004:512.2K 2005:1.30M 2006:4.04M 2007:5.71M 2008:0 2009:3.73M 2010:0 2014:0 2021:0 2023:0
  COUNTRY INN & SUITES                      1995:0 1997:0 1998:0 1999:0 2000:1.32M 2001:0 2002:0 2003:0 2004:0 2005:953.8K 2006:0 2007:2.60M 2008:3.09M 2009:0 2010:0 2011:0 2013:0
  CURVES FOR WOMEN                          1996:0 1997:0 1998:0 1999:23.9K 2000:0 2001:0 2002:37.6K 2003:30.6K 2004:327.1K 2005:271.5K 2006:133.0K 2007:0
  DAIRY QUEEN                               1991:262.6K 1992:66.0K 1993:0 1994:0 1995:0 1996:619.4K 1997:551.8K 1998:388.3K 1999:542.0K 2000:504.4K 2001:262.8K 2002:1.09M 2003:24.3K 2004:109.7K 2005:0 2006:706.0K 2007:552.4K 2008:0 2009:0 2013:0 2017:0 2024:0 2025:0
  DAYS INN                                  1991:0 1992:0 1993:0 1994:6.2K 1995:1.29M 1996:1.13M 1997:2.70M 1998:2.33M 1999:1.50M 2000:1.00M 2001:1.31M 2002:1.21M 2003:220.7K 2004:2.55M 2005:2.28M 2006:1.38M 2007:2.86M 2008:2.42M 2009:0 2010:780.5K 2011:0 2019:0 2021:0 2023:0 2026:0
  DOMINO'S PIZZA                            1991:0 1992:329.9K 1993:79.2K 1994:183.5K 1995:196.6K 1996:0 1997:181.9K 1998:108.8K 1999:70.1K 2000:111.8K 2001:0 2002:167.4K 2003:111.7K 2004:163.0K 2005:2.80M 2006:584.0K 2007:627.9K 2008:340.9K 2009:0 2010:0 2014:0 2020:0
  DUNKIN DONUTS                             1991:0 1992:0 1993:0 1994:0 1995:125.9K 1996:0 1997:179.5K 1998:0 1999:421.5K 2000:511.9K 2001:0 2002:193.9K 2003:1.14M 2004:600.5K 2005:1.10M 2006:0 2007:0 2008:0 2009:0 2010:0 2011:0 2012:0 2015:0 2022:0
  ECONO LODGE                               1991:0 1992:0 1993:0 1994:0 1995:0 1996:0 1997:1.04M 1998:1.47M 1999:0 2000:719.85 2001:0 2002:0 2003:404.2K 2004:711.3K 2005:1.46M 2006:1.43M 2007:1.16M 2008:0 2009:0 2010:1.49M 2022:0
  HOLIDAY INN                               1991:0 1992:0 1993:0 1994:1.53M 1997:0 1998:1.78M 1999:0 2000:1.39M 2001:1.80M 2002:51.7K 2004:0 2006:3.03M 2008:0 2009:2.20M 2011:0
  HOLIDAY INN EXPRESS                       1991:0 1993:0 1994:0 1995:850.4K 1996:0 1997:0 1998:0 1999:489.3K 2000:0 2001:0 2002:971.9K 2003:994.5K 2004:0 2005:4.57M 2006:3.60M 2007:1.55M 2008:7.82M 2009:3.23M 2010:795.6K 2011:0 2012:0 2013:0
  MAIL BOXES ETC                            1992:30.6K 1993:0 1994:0 1995:96.7K 1996:118.9K 1997:69.6K 1998:115.6K 1999:678.2K 2000:376.4K 2001:1.12M 2002:1.03M 2003:37.5K 2004:22.7K 2005:0
  MATCO TOOLS                               1991:16.7K 1992:51.6K 1993:0 1994:0 1995:30.1K 1996:20.5K 1997:266.3K 1998:349.8K 1999:119.7K 2000:312.6K 2001:336.0K 2002:1.73M 2003:1.25M 2004:285.6K 2005:49.3K 2006:0 2007:0 2008:0 2009:0
  MICROTEL INN & SUITES                     1998:0 1999:0 2000:981.7K 2001:427.6K 2002:572.7K 2003:0 2004:0 2005:939.1K 2006:1.06M 2007:2.61M 2008:2.28M 2009:1.27M 2010:0
  MINUTEMAN PRESS                           1991:28.1K 1992:42.7K 1993:0 1994:0 1995:187.4K 1996:178.2K 1997:160.5K 1998:111.0K 1999:515.8K 2000:262.3K 2001:0 2002:208.7K 2003:506.8K 2004:118.7K 2005:288.7K 2006:121.8K 2007:232.5K 2009:12.0K
  PLANET BEACH                              2000:0 2001:243.6K 2002:124.6K 2003:1.26M 2004:361.7K 2005:945.1K 2006:1.51M 2007:2.26M 2008:2.09M 2009:251.8K 2010:194.9K
  PLAY IT AGAIN SPORTS                      1991:9.7K 1992:15.7K 1993:134.4K 1994:151.7K 1995:175.1K 1996:207.2K 1997:83.7K 1998:0 1999:199.3K 2000:210.5K 2001:67.0K 2002:173.3K 2003:168.9K 2004:127.3K 2005:175.4K 2006:0 2007:50.7K 2008:169.0K 2009:157.8K
  QUALITY INN                               1991:0 1992:0 1993:0 1994:898.5K 1996:0 1997:265.7K 1998:0 1999:1.54M 2000:0 2001:0 2002:0 2003:0 2004:1.22M 2005:3.30M 2006:2.14M 2007:2.76M 2008:6.51M 2009:0 2010:507.7K 2011:0 2013:0 2018:0 2021:0 2022:0
  QUIZNO'S                                  1994:0 1995:0 1996:224.2K 1997:218.9K 1998:72.0K 1999:46.2K 2000:0 2001:722.0K 2002:185.8K 2003:955.1K 2004:840.2K 2005:1.13M 2006:1.09M 2007:404.5K 2008:303.4K 2009:0
  QUIZNO'S CLASSIC SUBS                     1993:0 1994:77.6K 1995:166.5K 1996:21.2K 1997:513.5K 1998:428.8K 1999:785.4K 2000:357.2K 2001:113.3K 2002:1.15M 2003:587.9K 2004:207.7K 2005:208.5K
  QUIZNO'S SUBS                             1998:82.1K 1999:0 2000:458.6K 2001:200.5K 2002:442.7K 2003:890.7K 2004:2.49M 2005:3.63M 2006:389.6K 2007:509.4K 2008:134.2K 2009:108.2K
  RAMADA INN                                1990:0 1992:0 1993:0 1994:0 1995:0 1996:0 1997:0 1998:0 1999:1.18M 2000:0 2001:441.3K 2002:0 2003:1.02M 2004:1.13M 2005:1.22M 2006:2.12M 2007:1.53M 2008:1.85M 2016:0
  SCHLOTZSKY'S DELI                         1992:0 1993:0 1994:0 1995:992.2K 1996:1.36M 1997:3.52M 1998:737.2K 1999:2.06M 2000:1.11M 2001:0 2002:244.6K 2003:0 2004:55.6K 2005:0 2006:0 2007:0 2008:0
  SLEEP INN                                 1994:0 1996:0 1997:0 1998:0 1999:700.1K 2000:0 2001:0 2002:0 2004:0 2005:2.06M 2006:2.85M 2007:0 2008:1.18M 2009:1.73M
  SUBWAY                                    1991:0 1992:10.3K 1993:11.5K 1994:6.4K 1995:505.1K 1996:79.5K 1997:116.4K 1998:56.1K 1999:142.7K 2000:94.2K 2001:311.9K 2002:353.7K 2003:1.62M 2004:787.3K 2005:749.5K 2006:296.5K 2007:891.2K 2008:452.3K 2009:18.8K 2010:0 2015:0 2023:0
  SUPER 8 MOTEL                             1991:0 1992:0 1993:0 1994:47.8K 1995:0 1996:278.9K 1997:401.5K 1998:0 1999:3.21M 2000:104.6K 2001:795.7K 2002:2.13M 2003:0 2004:170 2005:641.9K 2006:0 2007:996.1K 2008:0 2009:801.8K 2010:0 2013:0
  THE UPS STORE                             1998:0 1999:0 2002:0 2003:227.5K 2004:1.62M 2005:1.07M 2006:859.9K 2007:138.2K 2008:0 2009:81.9K 2010:0 2017:0 2020:0

FRANCHISENAME by FIRSTDISBURSEMENTDATE, dollars = GROSSCHARGEOFFAMOUNT
  ACE HARDWARE                              1991:0 1992:518.6K 1993:0 1994:0 1995:39.0K 1996:277.5K 1997:153.3K 1998:224.6K 1999:319.7K 2000:162.8K 2001:905.8K 2002:652.5K 2003:288.9K 2004:255.1K 2005:1.45M 2006:2.80M 2007:5.72M 2008:6.47M 2009:2.06M 2010:0 2011:64.4K 2012:267.2K 2013:248.9K 2014:0 2015:0 2016:0
  BEST WESTERN INN                          1991:0 1992:0 1993:0 1994:0 1995:374.3K 1996:454.2K 1997:2.28M 1998:2.19M 1999:4.90M 2000:603.7K 2001:0 2002:5.54M 2003:2.16M 2004:2.45M 2005:8.88M 2006:6.01M 2007:5.03M 2008:8.19M 2009:9.28M 2010:1.71M 2011:0 2012:2.53M 2013:358.6K 2014:2.69M 2015:0 2016:2.96M 2017:949.6K 2018:0 2019:0 2020:0 2021:0
  BLIMPIE                                   1990:0 1991:0 1992:158.9K 1993:185.4K 1994:190.4K 1995:740.0K 1996:749.2K 1997:1.22M 1998:1.02M 1999:2.60M 2000:2.34M 2001:2.66M 2002:1.92M 2003:774.6K 2004:236.0K 2005:137.0K 2006:565.0K 2007:643.2K 2008:111.1K 2009:0 2011:0 2013:0 2015:61.3K 2016:167.5K
  CHOICE HOTELS INTERNATIONAL INC.          1999:948.2K 2000:719.85 2001:0 2002:2.47M 2003:0 2004:3.21M 2005:6.50M 2006:16.82M 2007:30.05M 2008:32.15M 2009:14.63M 2010:7.02M 2011:0 2012:2.77M 2013:1.76M 2014:547.9K 2015:0
  COLD STONE CREAMERY, INC.                 1997:0 1998:84.9K 1999:151.5K 2000:0 2001:0 2002:846.0K 2003:3.65M 2004:8.67M 2005:17.17M 2006:14.13M 2007:5.95M 2008:2.43M 2009:170.9K 2010:60.8K 2011:0 2012:0 2013:0
  COMFORT INN                               1991:0 1992:0 1993:0 1994:0 1995:0 1996:533.0K 1997:987.6K 1998:1.18M 1999:591.0K 2000:400.7K 2001:533.2K 2002:654.5K 2003:4.07M 2004:869.4K 2005:5.57M 2006:11.68M 2007:17.87M 2008:16.56M 2009:11.51M 2010:1.99M 2011:533.7K 2012:0 2013:0 2014:0
  DAIRY QUEEN                               1990:0 1991:744.2K 1992:112.5K 1993:350.8K 1994:0 1995:250.9K 1996:833.1K 1997:1.72M 1998:1.43M 1999:1.55M 2000:1.54M 2001:1.16M 2002:1.34M 2003:1.51M 2004:936.5K 2005:1.58M 2006:3.53M 2007:2.56M 2008:2.43M 2009:393.6K 2010:520.6K 2011:1.31M 2012:467.0K 2013:593.5K 2014:0 2015:0
  DAYS INN                                  1991:0 1992:0 1993:0 1994:665.6K 1995:1.29M 1996:3.49M 1997:4.93M 1998:5.79M 1999:7.64M 2000:8.56M 2001:8.59M 2002:8.58M 2003:1.85M 2004:5.21M 2005:7.23M 2006:12.09M 2007:18.70M 2008:15.44M 2009:10.07M 2010:1.15M 2011:1.87M 2012:0 2013:0 2014:0 2015:0
  DOMINO'S PIZZA                            1991:0 1992:329.9K 1993:79.2K 1994:278.1K 1995:196.6K 1996:108.7K 1997:227.0K 1998:147.8K 1999:144.3K 2000:276.8K 2001:15.5K 2002:225.7K 2003:409.2K 2004:480.0K 2005:4.71M 2006:1.63M 2007:1.70M 2008:1.86M 2009:136.6K 2010:0 2011:0 2012:0 2013:0
  DUNKIN DONUTS                             1991:35.8K 1992:0 1993:77.9K 1994:0 1995:125.9K 1996:548.5K 1997:429.1K 1998:746.7K 1999:551.7K 2000:511.9K 2001:128.5K 2002:568.0K 2003:3.25M 2004:2.59M 2005:6.45M 2006:2.62M 2007:2.54M 2008:126.0K 2009:0 2010:2.41M 2011:0 2012:0 2013:0 2014:0 2015:0
  ECONO LODGE MOTEL                         1991:0 1992:0 1993:411.3K 1994:0 1995:0 1996:746.6K 1997:2.15M 1998:2.24M 1999:3.17M 2000:781.1K 2001:831.1K 2002:808.0K 2003:1.62M 2004:1.19M 2005:4.03M 2006:3.07M 2007:2.95M 2008:5.57M 2009:2.01M 2010:1.49M 2011:0 2012:0 2013:0 2014:0 2015:0
  HOLIDAY INN                               1991:0 1992:0 1993:0 1994:1.73M 1995:0 1996:0 1997:0 1998:0 1999:1.32M 2000:2.23M 2001:2.84M 2002:0 2003:764.6K 2004:688.1K 2005:2.13M 2006:6.00M 2007:2.91M 2008:663.2K 2009:2.20M 2010:795.6K 2011:6.28M 2012:0 2013:0 2015:0
  HOLIDAY INN EXPRESS                       1991:0 1992:0 1993:0 1994:0 1995:0 1996:112.2K 1997:0 1998:0 1999:489.3K 2000:1.98M 2001:0 2002:971.9K 2003:1.30M 2004:1.98M 2005:6.90M 2006:10.98M 2007:19.22M 2008:29.41M 2009:8.03M 2010:1.15M 2011:0 2012:0 2013:0 2014:0 2015:0 2016:0
  HOWARD JOHNSON                            1991:0 1992:0 1993:0 1994:0 1995:45.4K 1996:0 1997:853.5K 1998:761.9K 1999:2.40M 2000:2.73M 2001:2.24M 2002:1.55M 2003:1.03M 2004:3.23M 2005:817.8K 2006:3.20M 2007:6.17M 2008:8.46M 2009:0 2010:369.3K 2011:1.39M 2012:0 2013:1.47M
  LA QUINTA INN                             2002:132.7K 2003:0 2004:0 2005:2.59M 2006:3.81M 2007:6.00M 2008:8.17M 2009:6.04M 2010:1.52M 2011:1.88M 2012:0 2013:0 2014:0 2016:0
  MAIL BOXES ETC. USA                       1991:0 1992:92.1K 1993:0 1994:70.7K 1995:177.1K 1996:400.0K 1997:567.6K 1998:746.4K 1999:1.25M 2000:1.11M 2001:2.03M 2002:1.49M 2003:426.5K 2004:461.0K 2005:325.8K 2006:687.4K 2007:0 2008:120.9K 2009:48.3K 2010:0 2011:0 2012:0 2013:121.8K
  MATCO TOOLS (RENT TOOLS)                  1992:0 1993:20.4K 1994:0 1995:130.3K 1996:146.7K 1997:234.5K 1998:1.13M 1999:1.07M 2000:1.39M 2001:1.17M 2002:2.19M 2003:1.52M 2004:587.7K 2005:130.3K 2006:215.7K 2007:98.8K 2008:0 2009:0 2010:0 2011:32.9K 2012:30.0K 2013:0
  MICROTEL                                  1996:30.1K 1997:368.2K 1998:0 1999:2.64M 2000:2.71M 2001:1.94M 2002:1.25M 2003:1.35M 2004:740.4K 2005:1.43M 2006:2.63M 2007:4.56M 2008:7.34M 2009:3.16M 2010:735.3K 2011:0 2012:0 2013:0 2014:0
  PLANET BEACH                              1999:0 2000:75.4K 2001:456.5K 2002:305.1K 2003:2.00M 2004:1.70M 2005:3.20M 2006:4.03M 2007:6.67M 2008:4.59M 2009:499.4K 2010:204.8K 2011:95.7K 2012:0
  QUALITY INN                               1992:3.5K 1993:0 1994:1.40M 1995:0 1996:0 1997:677.0K 1998:2.38M 1999:0 2000:3.39M 2001:0 2002:140.2K 2003:1.60M 2004:2.29M 2005:2.97M 2006:7.45M 2007:10.81M 2008:9.14M 2009:4.86M 2010:507.7K 2011:4.25M 2012:2.25M 2013:0 2014:1.75M 2020:0
  QUIZNOS                                   1993:0 1994:77.6K 1995:166.5K 1996:428.5K 1997:845.2K 1998:843.2K 1999:1.43M 2000:1.07M 2001:1.41M 2002:2.62M 2003:5.36M 2004:11.31M 2005:15.80M 2006:11.74M 2007:7.31M 2008:3.52M 2009:759.5K 2010:151.7K 2011:535.5K 2012:0 2013:0 2014:0 2016:0
  Quality Inn by Choice Hotels /Quality In  2014:471.9K 2015:0 2017:1.40M 2018:1.92M 2019:1.90M 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  RAMADA INN                                1990:0 1991:0 1992:79.1K 1993:0 1994:0 1995:737.1K 1996:0 1997:1.91M 1998:2.95M 1999:3.95M 2000:5.19M 2001:4.70M 2002:3.38M 2003:1.02M 2004:2.41M 2005:3.30M 2006:10.08M 2007:12.61M 2008:8.47M 2009:4.56M 2010:1.93M 2011:0 2012:0 2013:0 2014:0
  SUBWAY                                    2006:94.8K 2007:24.5K 2008:0 2009:2.0K 2010:375.7K 2012:110.5K 2013:300.7K 2014:2.11M 2015:1.99M 2016:1.67M 2017:1.05M 2018:949.5K 2019:0
  SUBWAY SANDWICH SHOP                      1991:70.0K 1992:79.4K 1993:13.5K 1994:235.1K 1995:957.1K 1996:968.6K 1997:291.4K 1998:929.5K 1999:1.56M 2000:160.3K 2001:907.6K 2002:366.9K 2003:2.95M 2004:2.77M 2005:2.39M 2006:2.50M 2007:2.20M 2008:3.92M 2009:1.32M 2010:1.27M 2011:530.8K 2012:1.03M 2013:594.9K 2014:0 2015:0 2017:0
  SUPER 8 MOTEL                             1991:0 1992:0 1993:0 1994:276.6K 1995:0 1996:1.49M 1997:1.92M 1998:2.03M 1999:3.96M 2000:3.33M 2001:4.24M 2002:8.40M 2003:4.84M 2004:2.94M 2005:4.42M 2006:10.56M 2007:10.55M 2008:6.25M 2009:9.09M 2010:2.22M 2011:0 2012:0 2013:703.0K 2014:0
  Subway                                    2007:0 2008:56.7K 2009:93.6K 2010:107.6K 2011:202.4K 2012:0 2013:0 2014:0 2015:423.8K 2016:867.0K 2017:0 2018:1.37M 2019:434.5K 2020:294.3K 2021:152.8K 2022:275.6K 2023:0 2024:0 2025:0 2026:0
  TEMPORARY FRANCHISES                      1991:0 1993:0 1994:0 1995:0 1996:0 1998:0 1999:65.7K 2000:22.4K 2001:0 2003:204.9K 2004:11.9K 2007:0 2009:2.76M 2010:6.83M 2011:2.09M 2012:1.63M 2013:123.9K 2014:6.00M 2015:0 2017:0
  TRAVELODGE                                1991:322.3K 1992:844.7K 1993:0 1994:975.4K 1995:0 1996:0 1997:760.7K 1998:0 1999:2.29M 2000:2.43M 2001:1.98M 2002:413.7K 2003:696.4K 2004:932.3K 2005:2.11M 2006:2.96M 2007:4.14M 2008:4.04M 2009:0 2010:0 2011:0 2012:2.28M 2013:0
  The UPS Store                             2006:29.1K 2017:0 2018:140.0K 2019:0 2020:0 2021:0 2022:464.6K 2023:0 2024:0 2025:0 2026:0

## where

BORRSTATE: CA 297.6K, TX 164.9K, NY 136.8K, FL 118.5K, OH 94.8K, PA 77.0K, IL 74.1K, MI 65.2K, MA 64.5K, NJ 63.1K, MN 59.7K, GA 57.8K

CDC_STATE: CA 42.6K, FL 18.0K, TX 11.0K, IL 9.9K, NY 9.2K, MN 9.1K, UT 8.5K, DC 8.1K, OH 7.3K, NH 6.8K, WA 6.8K

THIRDPARTYLENDER_STATE: OH 11.4K, CA 11.3K, NC 7.4K, IL 6.6K, UT 6.1K, FL 5.1K, MA 4.8K, SD 4.5K, TX 4.0K, WI 3.8K, NY 3.7K

PROJECTSTATE: CA 297.6K, TX 164.8K, NY 136.9K, FL 118.4K, OH 94.8K, PA 77.0K, IL 74.1K, MI 65.3K, MA 64.5K, NJ 63.1K, MN 59.7K, GA 57.8K

BANKSTATE: OH 353.3K, NC 163.7K, SD 148.0K, CA 135.4K, DE 118.0K, NY 97.8K, UT 62.6K, TX 62.2K, RI 56.7K, NJ 48.1K, VA 47.8K

## what

PROGRAM:  7A 90%, 504 10%

APPROVALFY: 2007 11%, 2006 11%, 2005 11%, 2004 9%, 2025 8%, 2008 8%, 2024 8%, 2003 7%, 2016 7%, 2015 7%, 2017 7%, 2018 7%

PROCESSINGMETHOD: SBA Express Program 37%, Preferred Lenders Program 28%, 7a General 10%, Low Documentation Program 7%, Accredited Lenders Program 5%, 504 Basic 4%, Certified Lenders Program 3%, Community Express 2%, Small Loan Advantage Initiativ 1%, Premier Certified Lenders Prog 1%, Patriot Express Loans 1%, Community Advantage Initiative 0%

SUBPROGRAM: Guaranty 48%, FA$TRK (Small Loan Express) 37%, Sec. 504 - Loan Guarantees - P 10%, Community Express 2%, Lender Advantage Initiative 1%, Sec. 504 - Premier Certified L 1%, Patriot Express 0%, Community Advantage Initiative 0%, Revolving Line of Credit Expor 0%, International Trade - Sec, 7(a 0%, Standard Asset Based 0%

BUSINESSTYPE: CORPORATION 80%, INDIVIDUAL 17%, PARTNERSHIP 3%

BUSINESSAGE: Less than 4 years old but at l 34%, Existing, 5 or more years 15%, New, Less than 1 Year old 15%, Existing or more than 2 years  14%, Startup, Loan Funds will Open  8%, Unanswered 4%, New Business or 2 years or les 3%, Less than 3 years old but at l 2%, Change of Ownership 2%, Less than 5 years old but at l 2%

LOANSTATUS: P I F 55%, CURR 12%, CANCLD 11%, CHGOFF 7%, PREPAID IN FULL 5%, CLSLN 4%, CURRENT 3%, CANCELED 1%, COMMIT 1%, PURCH(NOT C/O) 1%, CHARGED-OFF 1%, LIQUID 0%

COLLATERALIND: FALSE 56%, TRUE 44%

FIXEDORVARIABLEINTERESTIND: V 81%, F 19%

REVOLVERSTATUS: FALSE 76%, TRUE 24%

SOLDSECMRKTIND: Y 98%, N 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ASOFDATE | date | 1 | 0 | 3/31/2026 2.17M |
| PROGRAM | category | 2 | 0 |  7A 1.95M; 504 227.4K |
| LOCATIONID | other | 6.9K | 2.2K | 12096 131.1K; 9551 106.4K; 57328 100.7K; 48270 96.0K |
| BORRNAME | who | 1.82M | 39 | Ladich LLC 3.4K; PLAY IT AGAIN SPORTS 3.3K; FFINCH FRAGRANCE 3.3K; Restaurant Galería Musas  3.3K |
| BORRSTREET | other | 1.92M | 202 | N112 W16298 Mequon Rd 3.4K; 1493 Higuera Street 3.3K; 78 Celis Aguilera  Esq. P 3.3K; 75 WEST RD 3.3K |
| BORRCITY | who | 48.3K | 2 | LOS ANGELES 21.0K; HOUSTON 19.0K; NEW YORK 15.8K; CHICAGO 12.5K |
| BORRSTATE | state | 62 | 5 | CA 297.6K; TX 164.9K; NY 136.8K; FL 118.5K |
| BORRZIP | other | 38.1K | 0 | 90015 6.0K; 93401 4.8K; 94103 4.5K; 3870 4.5K |
| CDC_NAME | who | 251 | 1.95M | CDC Small Business Financ 11.7K; Florida Business Developm 9.4K; Empire State Certified De 8.4K; Mortgage Capital Developm 8.1K |
| CDC_STREET | who | 254 | 1.95M | 2448 Historic Decatur Roa 11.7K; 1715 North Westshore Blvd 9.4K; 19 British American Blvd. 8.4K; 1611 Telegraph Ave 8.1K |
| CDC_CITY | who | 210 | 1.95M | San Diego 11.7K; Tampa 9.4K; Latham 8.4K; Oakland 8.1K |
| CDC_STATE | state | 52 | 1.95M | CA 42.6K; FL 18.0K; TX 11.0K; IL 9.9K |
| CDC_ZIP | other | 234 | 1.95M | 92106 11.7K; 33607 9.4K; 12110 8.4K; 94612 8.1K |
| THIRDPARTYLENDER_NAME | who | 5.6K | 2.05M | JPMorgan Chase Bank, Nati 5.5K; Bank of America, National 3.5K; Zions Bank, A Division of 2.9K; Wells Fargo Bank National 2.8K |
| THIRDPARTYLENDER_CITY | who | 4.1K | 2.05M | Columbus 5.5K; Charlotte 4.8K; SALT LAKE CITY 3.7K; Sioux Falls 3.4K |
| THIRDPARTYLENDER_STATE | state | 62 | 2.05M | OH 11.4K; CA 11.3K; NC 7.4K; IL 6.6K |
| THIRDPARTYDOLLARS | amount | 40.9K | 2.05M | 500000 877; 600000 768; 750000 703; 400000 686 |
| GROSSAPPROVAL | other | 39.8K | 0 | 50000 147.5K; 25000 115.5K; 100000 105.1K; 150000 85.9K |
| APPROVALDATE | date | 10.9K | 0 | 9/28/2001 6.2K; 7/28/2004 6.2K; 7/23/2004 6.2K; 7/29/2004 6.2K |
| APPROVALFY | category | 36 | 0 | 2007 110.3K; 2006 107.2K; 2005 105.1K; 2004 89.5K |
| FIRSTDISBURSEMENTDATE | date | 9.7K | 304.7K | 7/31/1995 14.0K; 4/30/1995 13.9K; 1/31/1995 13.2K; 10/31/1994 12.3K |
| PROCESSINGMETHOD | category | 40 | 0 | SBA Express Program 792.2K; Preferred Lenders Program 603.4K; 7a General 222.5K; Low Documentation Program 144.8K |
| SUBPROGRAM | category | 22 | 7.9K | Guaranty 1.03M; FA$TRK (Small Loan Expres 795.1K; Sec. 504 - Loan Guarantee 205.0K; Community Express 44.9K |
| TERMINMONTHS | other | 420 | 0 | 120 455.3K; 84 445.4K; 240 221.3K; 300 204.9K |
| NAICSCODE | who | 1.5K | 225.8K | 722110 50.2K; 722511 43.3K; 621210 36.9K; 811111 35.8K |
| NAICSDESCRIPTION | who | 2.4K | 225.8K | Full-Service Restaurants 78.1K; Limited-Service Restauran 52.5K; Offices of Dentists 32.3K; General Automotive Repair 31.0K |
| FRANCHISECODE | other | 9.6K | 2.00M | 78760 4.9K; 68020 2.8K; 21780 1.5K; 50564 1.4K |
| FRANCHISENAME | who | 9.0K | 2.00M | SUBWAY SANDWICH SHOP      4.9K; QUIZNOS                   2.8K; DAIRY QUEEN               1.5K; MAIL BOXES ETC. USA       1.4K |
| PROJECTCOUNTY | who | 2.0K | 644 | LOS ANGELES 89.4K; ORANGE 42.7K; COOK 32.7K; MARICOPA 31.5K |
| PROJECTSTATE | state | 61 | 5 | CA 297.6K; TX 164.8K; NY 136.9K; FL 118.4K |
| SBADISTRICTOFFICE | who | 90 | 1 | LOS ANGELES DISTRICT OFFI 98.5K; SOUTH FLORIDA DISTRICT OF 83.2K; ILLINOIS DISTRICT OFFICE  67.0K; MICHIGAN DISTRICT OFFICE  65.2K |
| CONGRESSIONALDISTRICT | other | 55 | 4.1K | 1 282.0K; 2 232.5K; 3 200.1K; 4 163.8K |
| BUSINESSTYPE | category | 4 | 5.3K | CORPORATION 1.73M; INDIVIDUAL 378.6K; PARTNERSHIP 61.7K |
| BUSINESSAGE | category | 11 | 2.6K | Less than 4 years old but 744.6K; Existing, 5 or more years 331.6K; New, Less than 1 Year old 327.8K; Existing or more than 2 y 307.7K |
| LOANSTATUS | category | 35 | 251 | P I F 1.17M; CURR 262.0K; CANCLD 238.3K; CHGOFF 143.1K |
| PAIDINFULLDATE | date | 256 | 891.3K | 7/31/2005 172.8K; 5/31/2005 120.6K; 8/31/2012 8.7K; 3/31/2022 6.5K |
| CHARGEOFFDATE | date | 8.7K | 1.92M | 1/26/2010 728; 5/12/2008 728; 6/4/2008 612; 12/27/2006 611 |
| GROSSCHARGEOFFAMOUNT | amount | 230.0K | 0 | 0 1.92M; 50000 2.3K; 10000 2.2K; 25000 1.8K |
| JOBSSUPPORTED | other | 529 | 2 | 0 595.6K; 2 206.4K; 1 155.4K; 4 145.9K |
| COLLATERALIND | category | 3 | 19.9K | FALSE 1.21M; TRUE 942.6K |
| BANKNAME | who | 5.6K | 229.7K | Wells Fargo Bank National 131.1K; Bank of America, National 107.3K; The Huntington National B 100.6K; JPMorgan Chase Bank, Nati 96.0K |
| BANKFDICNUMBER | other | 3.9K | 419.9K | 3511 131.1K; 3510 106.3K; 6560 100.6K; 628 96.0K |
| BANKNCUANUMBER | other | 599 | 2.14M | 24692 5.4K; 24694 1.5K; 67190 1.0K; 24563 872 |
| BANKSTREET | who | 6.5K | 229.7K | 3201 N 4th Ave 131.1K; 100 North Tryon Street 106.3K; 17 S High St. 100.6K; 1111 Polaris Pkwy 96.0K |
| BANKCITY | who | 3.6K | 229.7K | Sioux Falls 142.8K; WILMINGTON 135.4K; Charlotte 131.3K; COLUMBUS 102.0K |
| BANKSTATE | state | 67 | 229.7K | OH 353.3K; NC 163.7K; SD 148.0K; CA 135.4K |
| BANKZIP | other | 4.8K | 229.7K | 57104 131.6K; 28255 107.3K; 43215 101.4K; 43240 96.0K |
| SBAGUARANTEEDAPPROVAL | other | 65.4K | 227.4K | 25000 110.1K; 12500 95.9K; 5000 63.0K; 50000 60.1K |
| INITIALINTERESTRATE | amount | 2.5K | 1.22M | 6 114.2K; 5.5 48.5K; 5.25 47.9K; 5.75 39.9K |
| FIXEDORVARIABLEINTERESTIND | category | 3 | 1.22M | V 777.7K; F 178.7K |
| REVOLVERSTATUS | category | 3 | 227.4K | FALSE 1.47M; TRUE 472.4K |
| SOLDSECMRKTIND | category | 4 | 1.69M | Y 472.0K; N 11.0K |
| _INGESTED_AT | audit | 1 | 0 | 1783014098883016 2.17M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 091c00fa-38e6-42a0-becb-5 2.17M |
| _SRC_SHA256 | other | 1 | 0 | 96ec1f45a84dea84ad50a681e 2.17M |
