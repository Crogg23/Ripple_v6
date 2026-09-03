# TX_LOBBY_FOOD_BEVERAGE

rows 14.5K  columns 36  scan 6.2s

roles: amount 3, audit 2, category 11, date 5, empty 1, id 1, other 3, who 10

## when

DUEDT
  2005       670  ###################
  2006       777  ######################
  2007      1.0K  #############################
  2008       598  #################
  2009       923  ##########################
  2010       920  ##########################
  2011       985  ############################
  2012       978  ############################
  2013      1.1K  ##############################
  2014       774  ######################
  2015       839  ########################
  2016       594  #################
  2017       544  ###############
  2018       591  #################
  2019       442  ############
  2020       139  ####
  2021       327  #########
  2022       327  #########
  2023       527  ###############
  2024       425  ############
  2025       627  ##################
  2026       353  ##########

RECEIVEDDT
  2005       677  ##################
  2006       770  #####################
  2007      1.0K  ###########################
  2008       572  ###############
  2009       977  ##########################
  2010       906  ########################
  2011       999  ###########################
  2012       898  ########################
  2013      1.1K  ##############################
  2014       779  #####################
  2015       817  ######################
  2016       542  ###############
  2017       647  #################
  2018       582  ################
  2019       437  ############
  2020       144  ####
  2021       355  ##########
  2022       277  #######
  2023       552  ###############
  2024       417  ###########
  2025       606  ################
  2026       379  ##########

PERIODSTARTDT
  2004         1  
  2005       974  ###########################
  2006       670  ##################
  2007      1.1K  ##############################
  2008       651  ##################
  2009      1.0K  ############################
  2010       727  ####################
  2011      1.0K  ############################
  2012       924  #########################
  2013      1.0K  ############################
  2014       822  ######################
  2015       682  ###################
  2016       584  ################
  2017       594  ################
  2018       509  ##############
  2019       476  #############
  2020        87  ##
  2021       383  ##########
  2022       288  ########
  2023       582  ################
  2024       412  ###########
  2025       632  #################
  2026       269  #######

PERIODENDDT
  2004         1  
  2005       974  ###########################
  2006       670  ##################
  2007      1.1K  ##############################
  2008       651  ##################
  2009      1.0K  ############################
  2010       727  ####################
  2011      1.0K  ############################
  2012       924  #########################
  2013      1.0K  ############################
  2014       822  ######################
  2015       682  ###################
  2016       584  ################
  2017       594  ################
  2018       509  ##############
  2019       476  #############
  2020        87  ##
  2021       383  ##########
  2022       288  ########
  2023       582  ################
  2024       412  ###########
  2025       632  #################
  2026       269  #######

ACTIVITYDATE
  2004         1  
  2005       974  ###########################
  2006       671  ##################
  2007      1.1K  ##############################
  2008       650  ##################
  2009      1.0K  ############################
  2010       725  ####################
  2011      1.0K  ############################
  2012       918  #########################
  2013      1.0K  ############################
  2014       821  ######################
  2015       681  ###################
  2016       585  ################
  2017       593  ################
  2018       509  ##############
  2019       477  #############
  2020        89  ##
  2021       383  ##########
  2022       288  ########
  2023       582  ################
  2024       412  ###########
  2025       633  #################
  2026       268  #######

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACTIVITYEXACTAMOUNT | 4.2K | 0.10 | 28.25 | 644.40 | 78.7K | 442.4K |
| ACTIVITYAMOUNTRANGELOW | 14.5K | 0 | 23.01 | 448.62 | 78.7K | 1.14M |
| ACTIVITYAMOUNTRANGEHIGH | 14.5K | 0 | 99.99 | 486.39 | 78.7K | 1.93M |

## who

RECIPIENTNAMELAST by rows
       161  Smith
       124  King
       121  Taylor
       109  Davis
        85  Gilbert
        81  Turner
        80  Patrick
        80  Johnson
        75  Gonzalez
        72  Williams
        71  Whitmire
        71  Martinez
        69  Thompson
        67  Rodriguez
        66  Miller
        66  Otto
        65  Hegar
        65  Nelson
        63  Guillen
        62  Howard

RECIPIENTNAMELAST by dollars
       84.5K       69 rows  Thompson
       17.4K        1 rows  Sharbaugh
       16.6K       22 rows  Perry
       16.4K        1 rows  Event to which all legislators and staff are invited
       11.0K       85 rows  Gilbert
       10.5K       53 rows  Llano
        9.3K      124 rows  King
        9.1K      121 rows  Taylor
        7.8K       71 rows  Whitmire
        7.8K      161 rows  Smith
        7.7K       65 rows  Hegar
        7.0K       80 rows  Johnson
        6.9K       63 rows  Guillen
        6.9K      109 rows  Davis
        6.8K       50 rows  Romero
        6.8K       72 rows  Williams
        6.7K       54 rows  Kuempel
        6.1K       39 rows  Ashby
        6.0K       71 rows  Martinez
        5.7K       66 rows  Otto

RESTAURANTNAME by rows
       330  Austin Club
       216  Reliant Stadium
       165  III Forks
       153  The Austin Club
       132  Barton Creek Resort & Country Club
       112  Perry's Steakhouse & Grille
       104  Jason's Deli
        97  Eddie V's
        94  Eat Out In
        90  Tiff's Treats
        89  Ruth's Chris Steakhouse
        87  Whole Foods
        85  The Westin St Francis
        84  The Roaring Fork
        78  NRG Stadium
        76  Tiffs Treats
        75  Hyatt Lost Pines Resort
        69  Roaring Fork
        66  The Breakers
        62  Austin Land and Cattle

RESTAURANTNAME by dollars
       78.9K        8 rows  Levy Restaurant
       20.1K      216 rows  Reliant Stadium
       17.4K        1 rows  Austin Marriott at the Capitol
       16.4K       66 rows  The Breakers
       16.4K        1 rows  TPCA Legislative Barbeque Luncheon on the Capitol Grounds
       14.6K        2 rows  Stephen F. Austin Intercontinental Hotel
       13.9K      165 rows  III Forks
       11.6K      132 rows  Barton Creek Resort & Country Club
       11.5K      112 rows  Perry's Steakhouse & Grille
       10.4K       85 rows  The Westin St Francis
       10.2K       97 rows  Eddie V's
        9.7K       49 rows  The Westin
        9.2K       75 rows  Hyatt Lost Pines Resort
        8.4K       24 rows  The Breakers Palm Beach
        7.4K      330 rows  Austin Club
        7.2K       31 rows  Palace Hotel
        7.2K       52 rows  Fairmont Chateau Whistler
        7.0K       31 rows  The Boulders Resort & Spa
        6.6K       22 rows  Old Edwards Inn
        6.5K      104 rows  Jason's Deli

RECIPIENTNAMEFIRST by rows
       431  John
       169  David
       155  Joe
       151  Jim
       142  Dan
       136  Larry
       132  Michael
       131  Mark
       130  Robert
       124  Brad
       118  Mike
       110  Richard
       108  Ken
       104  Jason
       104  Matt
        98  Ryan
        94  Todd
        94  Chris
        87  Charles
        86  Craig

RECIPIENTNAMEFIRST by dollars
       79.1K        8 rows  Hunter
       54.7K      431 rows  John
       17.7K       51 rows  Rick
       16.0K      124 rows  Brad
       14.6K      169 rows  David
       12.9K      142 rows  Dan
       12.3K      130 rows  Robert
       10.9K      131 rows  Mark
       10.8K      108 rows  Ken
       10.7K      132 rows  Michael
        9.5K       98 rows  Ryan
        9.4K       43 rows  Lulu
        8.4K      155 rows  Joe
        8.3K      136 rows  Larry
        8.1K      151 rows  Jim
        8.0K       52 rows  Daniel
        7.8K      118 rows  Mike
        7.1K       61 rows  Carlos
        6.9K       94 rows  Todd
        6.8K       50 rows  Ramon

FILERNAME by rows
       590  J.P. Morgan Securities LLC
       333  Morgan Stanley & Co. LLC
       319  English Jr., C. M. (Mr.)
       256  Barclays Capital, Inc.
       249  Stuart, Charles (Mr.)
       209  Neighbors, Phil (Mr.)
       209  Greytok, John (Mr.)
       200  Stagner, Robert
       195  Weist, Jon (Mr.)
       193  Boyer, Victor (Mr.)
       179  Fitzpatrick, John (Mr.)
       178  Mills, D. Alex (Mr.)
       166  Gibson, Stephanie (Ms.)
       161  McKnight, Peyton (Mr.)
       157  Ballew, Joel D. (Mr.)
       139  Gilmore, Scott (Mr.)
       138  Morgan Stanley Investment Management Inc.
       133  Guenthner, David (Mr.)
       130  Fox, Jeffrey A. (Mr.)
       129  Volkening, Ronnie (Mr.)

FILERNAME by dollars
       79.1K       11 rows  Hutchins-Robertson, Tedrah (Mrs.)
       72.7K      590 rows  J.P. Morgan Securities LLC
       67.5K      333 rows  Morgan Stanley & Co. LLC
       43.6K      256 rows  Barclays Capital, Inc.
       36.4K      161 rows  McKnight, Peyton (Mr.)
       24.1K      138 rows  Morgan Stanley Investment Management Inc.
       23.7K      249 rows  Stuart, Charles (Mr.)
       23.4K      200 rows  Stagner, Robert
       19.5K      209 rows  Greytok, John (Mr.)
       19.1K      179 rows  Fitzpatrick, John (Mr.)
       18.8K      103 rows  Woodard, Jennifer W. (Ms.)
       18.4K       12 rows  Sharbaugh, John M (Mr.)
       17.5K      319 rows  English Jr., C. M. (Mr.)
       16.4K        2 rows  Allred, Lynton (Mr.)
       15.8K      105 rows  Stagner, Robert (Mr.)
       15.3K       46 rows  Esparza, John (Mr.)
       14.6K      130 rows  Fox, Jeffrey A. (Mr.)
       13.6K      133 rows  Guenthner, David (Mr.)
       12.6K       94 rows  Stagner, Robert S. (Mr.)
       10.3K       55 rows  Keller, Andrew Barclay (Mr.)

## who x when

RECIPIENTNAMELAST by PERIODSTARTDT, dollars = ACTIVITYAMOUNTRANGELOW
  Ashby                                     2013:262 2014:450 2015:350 2016:0 2017:300 2018:450 2019:400 2021:1.2K 2022:850 2023:500 2024:400 2025:500 2026:400
  Davis                                     2005:118.24 2006:324.18 2007:38.84 2008:22.56 2009:620.50 2010:261.23 2011:477.05 2012:388.25 2013:628.81 2014:150 2015:276.37 2017:31.05 2018:0 2019:178.19 2021:0 2022:750 2023:300 2024:850 2025:0 2026:1.4K
  Event to which all legislators and staff  2005:16.4K
  Gilbert                                   2005:18.16 2010:35.33 2011:253.40 2012:1.3K 2013:900 2014:2.0K 2015:1.6K 2016:100 2017:250 2018:1.5K 2019:1.1K 2021:250 2022:450 2023:600 2024:200 2025:300 2026:300
  Gonzalez                                  2005:20.92 2006:55.09 2007:21.24 2008:0 2009:48.55 2010:12 2011:679.36 2012:14.54 2013:116.73 2014:105.55 2016:59.19 2017:100 2018:509.88 2019:250 2021:450 2023:0 2024:25.71 2025:550 2026:200
  Guillen                                   2005:100 2006:100 2007:138.02 2009:301.69 2010:167.06 2011:28.25 2012:0 2013:156.84 2014:105 2015:371.88 2019:100 2021:0 2023:1.5K 2024:700 2025:3.2K
  Hegar                                     2006:54.60 2007:200 2008:100 2009:368 2011:185.50 2012:300 2013:300 2014:350 2015:606.79 2016:32 2017:250 2018:400 2019:500 2021:600 2022:200 2023:1.7K 2024:1.2K 2025:400
  Howard                                    2005:0 2006:300 2007:205.89 2008:736 2009:183.29 2010:98.34 2011:323 2012:22.45 2013:0 2016:0 2017:300 2018:0 2019:150 2021:100 2023:200
  Johnson                                   2005:300 2006:190.56 2007:450 2008:100 2009:0 2010:0 2011:69.17 2012:9.15 2013:143.41 2014:49.97 2015:403.85 2016:652.86 2017:886.82 2018:352.65 2019:279.49 2020:200 2021:200 2022:7.10 2023:900.46 2024:809.32 2025:577.23 2026:400
  King                                      2005:253.55 2006:122.91 2007:378.58 2008:140 2009:140.30 2010:183.51 2011:75.05 2012:32 2013:178.14 2014:156.94 2015:800 2016:200 2017:677.81 2018:550 2019:400 2021:300 2022:1.4K 2023:1.2K 2024:800 2025:450 2026:900
  Kuempel                                   2005:150 2006:100 2008:0 2009:397.24 2011:100 2012:300 2013:0 2014:505 2015:283.25 2017:200 2018:650 2019:400 2021:300 2022:1.4K 2023:1.1K 2024:750
  Llano                                     2011:0 2012:45.15 2013:100 2014:100 2015:100 2016:274.86 2017:300 2018:1.6K 2019:1.9K 2020:900 2023:450 2024:2.1K 2025:1.4K 2026:1.2K
  Martinez                                  2005:105.56 2006:100 2007:0 2008:0 2009:30.50 2010:16.17 2011:240.56 2012:29.08 2013:560.73 2015:172.33 2016:450 2017:450 2018:100 2019:100 2020:150 2021:800 2022:650 2023:600 2024:875.71 2025:250 2026:350
  Miller                                    2005:100 2006:0 2007:0 2008:0 2009:100 2010:0 2011:496.71 2012:133.63 2013:317.18 2014:322.10 2015:326.96 2016:266 2017:114.38 2018:0 2023:500 2025:150
  Nelson                                    2005:196.24 2007:190 2008:13.53 2009:480.50 2010:91.40 2011:121 2012:250 2013:292 2014:634.75 2015:100 2016:100 2017:0 2018:0 2019:0 2020:0 2021:0 2022:450 2023:800 2024:950 2025:100
  Otto                                      2005:651.18 2006:541.70 2007:500 2008:695 2009:744.71 2010:452.56 2011:300 2012:378.20 2013:445.40 2014:350 2015:600
  Patrick                                   2006:0 2007:285 2008:90.24 2009:550.39 2010:214.42 2011:113.84 2012:247.40 2013:619.45 2014:318.86 2015:211.93 2017:506 2023:1.2K 2025:1.2K
  Perry                                     2005:0 2008:14.7K 2011:100 2012:0 2014:205 2015:0 2016:0 2017:366.59 2021:150 2023:504.49 2025:548.14
  Rodriguez                                 2005:200 2007:44.29 2009:445 2010:53.25 2011:751.74 2012:128.50 2013:694.97 2014:190.23 2015:578.38 2016:48.93 2017:375 2018:0 2021:0 2023:250 2025:0 2026:583.90
  Romero                                    2006:0 2007:0 2014:115.76 2015:0 2016:500 2018:0 2019:600 2020:300 2021:900 2022:850.39 2023:600 2024:1.3K 2025:1.5K 2026:200
  Sharbaugh                                 2005:17.4K
  Smith                                     2005:0 2006:490.56 2007:841.32 2008:981.76 2009:1.1K 2010:693.20 2011:206.09 2012:317.49 2013:117 2014:686.76 2015:700 2016:200 2017:57.14 2019:0 2021:0 2022:200 2023:481.30 2024:271.81 2025:121.25 2026:317.79
  Taylor                                    2005:353.12 2006:100 2007:349.34 2008:0 2009:100 2010:345.62 2011:219.70 2012:514.25 2013:726.21 2014:1.3K 2015:234.66 2016:707 2017:500 2018:387 2019:550 2020:300 2021:800 2022:569.44 2023:0 2024:150 2025:854
  Thompson                                  2005:419.55 2006:50.56 2007:642.08 2008:218.93 2009:646.45 2010:0 2011:250 2012:9.15 2013:453.09 2014:79.3K 2015:504.11 2016:100 2017:150 2018:0 2019:0 2020:0 2021:0 2023:100 2024:1.5K 2025:200
  Turner                                    2005:162.77 2006:0 2007:240.95 2008:100 2009:333.80 2010:195.79 2011:300 2012:0 2013:1.4K 2014:276.46 2015:133.13 2016:38.04 2017:150 2018:0 2019:261.75 2021:154.44 2022:16.63 2023:321.14 2025:495.55
  Whitmire                                  2005:596.59 2006:676.80 2007:600 2008:350 2009:541.37 2010:645.62 2011:400 2012:102.43 2013:450 2014:650 2015:450 2017:550 2018:0 2019:800 2020:150 2021:850
  Williams                                  2005:150 2006:400 2007:492 2008:30 2009:700 2010:40.10 2011:505.25 2012:650 2013:400 2014:200 2015:100 2016:234 2017:574.52 2018:870.20 2019:650 2021:0 2023:100 2024:400 2025:181 2026:100

RESTAURANTNAME by PERIODSTARTDT, dollars = ACTIVITYAMOUNTRANGELOW
  Austin Club                               2005:1.5K 2006:382.51 2007:94.43 2008:229.28 2009:323.51 2010:1.6K 2011:707.47 2012:167.70 2013:0 2014:1.4K 2015:767.48 2026:150
  Austin Land and Cattle                    2005:70 2008:43.85 2009:275.38 2010:70 2011:208 2012:0 2013:637.44 2014:10.34 2015:0 2016:100 2017:100 2018:0
  Austin Marriott at the Capitol            2005:17.4K
  Barton Creek Resort & Country Club        2005:4.6K 2006:7.0K
  Eat Out In                                2005:1.4K 2007:1.0K 2009:582.64 2011:245.46 2013:400.62 2015:1.0K
  Eddie V's                                 2005:1.6K 2006:150 2007:4.2K 2008:47.50 2009:1.0K 2010:400 2011:400 2013:942.35 2014:100 2015:200 2016:100 2017:45.36 2019:153.82 2023:400.92 2024:0 2026:400
  Fairmont Chateau Whistler                 2007:3.1K 2012:2.0K 2023:2.0K
  Hyatt Lost Pines Resort                   2007:9.2K
  III Forks                                 2007:1.2K 2009:2.6K 2010:300 2011:2.4K 2012:0 2013:2.3K 2014:2.6K 2015:0 2016:253.16 2018:400 2019:400 2021:400 2022:400 2023:200 2024:300 2025:152
  Jason's Deli                              2005:2.6K 2006:188.70 2007:1.2K 2008:222.82 2009:811.10 2011:375.20 2012:200 2013:550.89 2014:68.42 2015:393.02
  Levy Restaurant                           2013:0 2014:78.9K
  NRG Stadium                               2015:2.5K 2016:2.6K 2021:0 2022:0
  Old Edwards Inn                           2026:6.6K
  Palace Hotel                              2015:800 2017:300 2019:1.0K 2020:3.0K 2022:1.0K 2024:950 2026:200
  Perry's Steakhouse & Grille               2009:0 2010:400 2011:596.16 2012:2.1K 2014:500 2015:1.3K 2016:1.0K 2017:500 2020:1.1K 2023:2.0K 2025:800 2026:1.2K
  Reliant Stadium                           2006:0 2007:3.2K 2008:600 2009:2.2K 2010:3.4K 2011:3.3K 2012:2.2K 2013:2.5K 2014:2.7K
  Roaring Fork                              2005:217.20 2006:16.74 2007:300 2008:51.88 2009:395 2010:49.55 2011:0 2012:47.88 2013:20.72 2017:250 2021:300 2022:150 2023:500 2024:100 2025:1.2K 2026:0
  Ruth's Chris Steakhouse                   2005:1.4K 2007:1.5K 2008:0 2009:297.24 2010:425.78 2011:300 2012:178.20 2013:724.75 2014:0 2015:300 2017:200 2023:150 2025:150
  Stephen F. Austin Intercontinental Hotel  2008:14.5K 2011:48
  TPCA Legislative Barbeque Luncheon on th  2005:16.4K
  The Austin Club                           2005:242.40 2006:171.86 2007:64.50 2008:423.57 2009:213.06 2010:130.30 2011:345.38 2012:475.85 2013:545.62 2014:914.47 2015:102.06 2018:0 2023:0
  The Boulders Resort & Spa                 2019:2.8K 2021:4.2K
  The Breakers                              2015:650 2017:300 2018:3.6K 2019:5.8K 2020:3.2K 2023:300 2024:2.5K
  The Breakers Palm Beach                   2025:4.4K 2026:4.1K
  The Roaring Fork                          2005:94.54 2006:0 2007:400 2009:231.64 2010:152.87 2011:164.73 2013:445.89 2014:47.35 2015:14.25 2017:0 2018:42.85 2019:0 2021:100 2025:0
  The Westin                                2026:9.7K
  The Westin St Francis                     2017:5.0K 2018:5.2K 2019:150 2020:100
  Tiff's Treats                             2005:0 2006:0 2007:280.10 2009:753.68 2011:121.50 2013:0 2017:0 2019:32
  Tiffs Treats                              2005:0 2007:0 2009:0 2011:213.34 2013:89.28 2014:21.60 2017:0 2021:0 2023:0
  Whole Foods                               2005:0 2007:0 2009:19.95 2011:71.33 2012:0 2015:0 2017:0

## what

FORMTYPECD: LOBBYACT 91%, CORLOBBYACT 9%

REPORTTYPECD: LOBBYACTANNUAL 21%, LOBBYACTJUN 10%, LOBBYACTAPR 8%, LOBBYACTMAY 8%, LOBBYACTFEB 8%, LOBBYACTMAR 7%, LOBBYACTSEP 7%, LOBBYACTNOV 7%, LOBBYACTDEC 6%, LOBBYACTJUL 6%, LOBBYACTOCT 6%, LOBBYACTAUG 6%

APPLICABLEYEAR: 2007 10%, 2011 10%, 2009 10%, 2013 10%, 2005 9%, 2012 9%, 2014 8%, 2010 7%, 2008 7%, 2015 7%, 2006 6%, 2025 6%

CREDITCARDFLAG: N 94%, Y 6%

ACTIVITYAMOUNTCD: LT100 38%, OTHER 29%, LT150 17%, LT200 8%, LT250 4%, LT300 2%, LT350 1%, LT400 1%, LT450 0%, UNKNOWN 0%, LT500 0%

RECIPIENTPERSENTTYPECD: INDIVIDUAL 100%

RECIPIENTNAMESUFFIXCD: MD 39%, JR 30%, DVM 9%, III 8%, PHD 6%, ESQ 3%, DO 2%, MR 2%, IV 1%, MA 1%, CPA 1%

RECIPIENTNAMEPREFIXCD: MR 48%, REPRESENTATIVE 18%, MS 18%, MRS 7%, SENATOR 3%, HONORABLE 2%, MISS 1%, COMMISSNR 1%, DR 1%, AGENT 0%, JUDGE 0%

RESTAURANTSTREETSTATECD: TX 84%, NY 4%, CA 4%, FL 2%, MA 1%, ZZ 1%, CO 1%, AZ 1%, IL 1%, DC 1%, GA 1%

RESTAURANTSTREETCOUNTRYCD: USA 98%, ISR 1%, SGP 0%, CAN 0%, GBR 0%, ESP 0%, JPN 0%, FRA 0%, MEX 0%, BRA 0%, DEU 0%

RESTAURANTSTREETREGION: Ontario 45%, B.C. 16%, QC 15%, Mayfair 5%, Maharashtra 4%, Panamá 4%, Hesse 3%, Ciudad de México 3%, Mexico 3%, Chuo‐ku 1%, Minato-ku 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RECORDTYPE | other | 1 | 0 | FOOD 14.5K |
| FORMTYPECD | category | 2 | 0 | LOBBYACT 13.1K; CORLOBBYACT 1.4K |
| REPORTTYPECD | category | 15 | 0 | LOBBYACTANNUAL 2.7K; LOBBYACTJUN 1.3K; LOBBYACTAPR 1.0K; LOBBYACTMAY 1.0K |
| REPORTINFOIDENT | who | 2.9K | 0 | 100640051 119; 576220 118; 100821006 116; 100822486 112 |
| APPLICABLEYEAR | category | 23 | 0 | 2007 1.1K; 2011 1.0K; 2009 1.0K; 2013 1.0K |
| FILERIDENT | who | 739 | 0 | 00080771 607; 00012985 399; 00068424 346; 00034785 319 |
| FILERTYPECD | other | 1 | 0 | LOBB 14.5K |
| FILERNAME | who | 855 | 0 | J.P. Morgan Securities LL 610; Morgan Stanley & Co. LLC 348; English Jr., C. M. (Mr.) 320; Barclays Capital, Inc. 270 |
| FILERSORT | who | 858 | 0 | J.P. MORGAN SECURITIES LL 609; MORGAN STANLEY & CO. LLC 348; ENGLISH JR., C. M. (MR.) 320; BARCLAYS CAPITAL, INC. 270 |
| DUEDT | date | 263 | 0 | 20100111 423; 20090112 320; 20060110 305; 20120110 293 |
| RECEIVEDDT | date | 1.3K | 0 | 20130107 146; 20090112 144; 20100111 117; 20160810 113 |
| PERIODSTARTDT | date | 261 | 0 | 20090101 496; 20120101 399; 20110101 394; 20050101 372 |
| PERIODENDDT | date | 272 | 0 | 20091231 434; 20081231 320; 20051231 305; 20111231 293 |
| LOBBYACTIVITYID | id | 15.1K | 0 | 100041157 73; 100041156 73; 100041155 73; 100041154 73 |
| CREDITCARDFLAG | category | 2 | 0 | N 13.5K; Y 906 |
| ACTIVITYDATE | date | 3.1K | 0 | 20210517 116; 20230711 99; 20251023 91; 20240930 91 |
| ACTIVITYAMOUNTCD | category | 11 | 0 | LT100 5.5K; OTHER 4.2K; LT150 2.4K; LT200 1.2K |
| ACTIVITYEXACTAMOUNT | amount | 1.6K | 10.2K | 30.00 66; 117.55 58; 128.52 53; 25.00 48 |
| ACTIVITYAMOUNTRANGELOW | amount | 1.6K | 0 | 0.00 5.5K; 100.00 2.4K; 150.00 1.2K; 200.00 524 |
| ACTIVITYAMOUNTRANGEHIGH | amount | 1.6K | 0 | 99.99 5.5K; 149.99 2.4K; 199.99 1.2K; 249.99 509 |
| RECIPIENTPERSENTTYPECD | category | 2 | 117 | INDIVIDUAL 14.3K |
| RECIPIENTNAMEORGANIZATION | empty | 1 | 14.5K |  |
| RECIPIENTNAMELAST | who | 3.2K | 127 | Smith 161; King 125; Taylor 121; Gilbert 118 |
| RECIPIENTNAMESUFFIXCD | category | 15 | 14.3K | MD 69; JR 53; DVM 17; III 15 |
| RECIPIENTNAMEFIRST | who | 2.2K | 304 | John 431; David 169; Joe 155; Jim 151 |
| RECIPIENTNAMEPREFIXCD | category | 13 | 8.2K | MR 3.0K; REPRESENTATIVE 1.2K; MS 1.1K; MRS 443 |
| RECIPIENTNAMESHORT | who | 79 | 14.2K | Doc 23; Bill 18; Chuy 17; Bob 16 |
| RESTAURANTNAME | who | 3.2K | 11 | Austin Club 330; Reliant Stadium 225; III Forks 165; The Austin Club 153 |
| RESTAURANTSTREETCITY | who | 446 | 112 | Austin 7.6K; Houston 917; New York 552; San Antonio 404 |
| RESTAURANTSTREETSTATECD | category | 37 | 430 | TX 11.5K; NY 592; CA 582; FL 212 |
| RESTAURANTSTREETCOUNTRYCD | category | 23 | 69 | USA 14.1K; ISR 82; SGP 71; CAN 57 |
| RESTAURANTSTREETPOSTALCODE | other | 629 | 2.1K | 78701 4.3K; 78703 499; 78704 367; 77054 313 |
| RESTAURANTSTREETREGION | category | 14 | 14.4K | Ontario 34; B.C. 12; QC 11; Mayfair 4 |
| INGESTED_AT | audit | 1 | 0 | 1785965501497811 14.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 190ade3d-5ab5-42a1-b3d1-6 14.5K |
| SRC_SHA256 | who | 1 | 0 | 97339e04a26aa6305472d9579 14.5K |
