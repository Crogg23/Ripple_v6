# FED_SENATE_STOCK_WATCHER

rows 8.3K  columns 13  scan 2.9s

roles: audit 2, category 4, date 1, other 2, who 4

## when

TRANSACTION_DATE
  2012        60  #
  2013       184  ####
  2014       727  ###############
  2015      1.2K  ########################
  2016       977  ####################
  2017      1.4K  ############################
  2018      1.4K  #############################
  2019      1.0K  ######################
  2020      1.4K  ##############################

## who

SENATOR by rows
      2.6K  David A Perdue , Jr
       877  Thomas R Carper
       687  Sheldon Whitehouse
       460  Pat Roberts
       441  Susan M Collins
       347  Shelley M Capito
       279  Kelly Loeffler
       250  John F Reed
       227  James M Inhofe
       225  John Hoeven
       211  Ron L Wyden
       192  Patrick J Toomey
       161  Patty Murray
       148  William Cassidy
       142  Rick Scott
       136  Jerry Moran,
       133  Gary C Peters
        99  Thomas R Tillis
        96  Richard M Burr
        88  Mark R Warner

ASSET_DESCRIPTION by rows
       463  This filing was disclosed via scanned PDF. Use link in ptr_link column
       127  Apple Inc.
        76  Bank of America Corporation
        67  First Data Corporation
        66  Pfizer Inc.
        65  Urban Outfitters, Inc.
        64  The Walt Disney Company
        63  Microsoft Corporation
        62  FireEye, Inc.
        61  Caesars Entertainment Corporation
        60  Netflix, Inc.
        57  AT&amp;T Inc.
        48  Amazon.com, Inc.
        48  NVIDIA Corporation
        42  General Electric Company
        42  Facebook, Inc.
        41  FedEx Corporation
        40  Hanesbrands Inc.
        39  BWX Technologies, Inc.
        38  Entegris, Inc.

COMMENT by rows
      7.1K  --
       179  R
       117  sep
        51  555
        23  Sep
        18  r
        15  Full sale from Wells Fargo Acct
        12  Dividend Reinvestment
        11  SEP
         9  Gorfam Inc. sold stock to benefit another shareholder. Child received 
         9  THIS IS A SUB-ASSET HOLDING OF ANANIA &amp; ASSOCIATES INVESTMENT CO L
         8  Underlying asset of West Virginia Growth Investment LLC
         6  Child #2
         5  Acquired as a result of a 9/21/16 inheritance.
         5  roth
         5  Jt
         4  IRA (bond matured)
         4  Less than $1000
         4  fran45
         4  "Called" Redemption

_SRC_SHA256 by rows
      8.3K  d99afca9e7e56352c8d3dcfc28b00143b98d49b6a729e22c27bc0c1bcd6aca8d

## who x when

SENATOR by TRANSACTION_DATE
  David A Perdue , Jr                       2015:496 2016:347 2017:418 2018:489 2019:435 2020:412
  Gary C Peters                             2015:28 2016:27 2017:19 2018:29 2019:25 2020:5
  James M Inhofe                            2015:47 2016:34 2017:50 2018:61 2019:20 2020:15
  Jerry Moran,                              2018:58 2019:40 2020:38
  John F Reed                               2012:3 2013:7 2014:39 2015:33 2016:53 2017:41 2018:33 2019:41
  John Hoeven                               2012:5 2013:10 2014:25 2015:24 2016:42 2017:45 2018:30 2019:42 2020:2
  Kelly Loeffler                            2020:279
  Mark R Warner                             2012:4 2013:12 2014:11 2015:9 2016:12 2017:11 2018:15 2019:7 2020:7
  Pat Roberts                               2012:5 2013:11 2014:50 2015:59 2016:22 2017:93 2018:74 2019:22 2020:124
  Patrick J Toomey                          2012:2 2013:6 2014:26 2015:45 2016:19 2017:21 2018:41 2019:20 2020:12
  Patty Murray                              2017:161
  Richard M Burr                            2012:2 2013:14 2014:11 2015:10 2016:11 2017:15 2018:15 2019:16 2020:2
  Rick Scott                                2019:99 2020:43
  Ron L Wyden                               2016:7 2018:1 2019:6 2020:197
  Sheldon Whitehouse                        2012:5 2013:11 2014:150 2015:106 2016:166 2017:119 2018:86 2019:32 2020:12
  Shelley M Capito                          2015:4 2016:25 2017:92 2018:156 2019:64 2020:6
  Susan M Collins                           2012:8 2013:43 2014:251 2015:45 2016:38 2017:12 2018:34 2019:8 2020:2
  Thomas R Carper                           2012:8 2013:17 2014:105 2015:96 2016:78 2017:135 2018:141 2019:70 2020:227
  Thomas R Tillis                           2015:94 2017:3 2018:2
  William Cassidy                           2015:5 2016:54 2017:18 2018:33 2019:12 2020:26

ASSET_DESCRIPTION by TRANSACTION_DATE
  AT&amp;T Inc.                             2017:12 2018:11 2019:17 2020:17
  Amazon.com, Inc.                          2016:2 2017:6 2018:13 2019:6 2020:21
  Apple Inc.                                2016:21 2017:17 2018:26 2019:16 2020:47
  BWX Technologies, Inc.                    2018:12 2019:27
  Bank of America Corporation               2016:29 2017:16 2018:17 2019:1 2020:13
  Caesars Entertainment Corporation         2017:18 2018:10 2019:20 2020:13
  Entegris, Inc.                            2016:4 2017:11 2018:3 2019:15 2020:5
  Facebook, Inc.                            2016:15 2017:6 2018:12 2019:2 2020:7
  FedEx Corporation                         2016:2 2017:2 2018:3 2019:28 2020:6
  FireEye, Inc.                             2016:32 2017:5 2018:14 2019:7 2020:4
  First Data Corporation                    2017:19 2018:29 2019:19
  General Electric Company                  2016:13 2017:16 2018:9 2019:3 2020:1
  Hanesbrands Inc.                          2017:22 2018:11 2019:2 2020:5
  Microsoft Corporation                     2016:15 2017:5 2018:9 2019:11 2020:23
  NVIDIA Corporation                        2016:5 2017:6 2018:8 2019:2 2020:27
  Netflix, Inc.                             2016:6 2017:7 2018:14 2019:6 2020:27
  Pfizer Inc.                               2016:16 2017:19 2018:19 2020:12
  The Walt Disney Company                   2016:19 2017:8 2018:4 2019:10 2020:23
  This filing was disclosed via scanned PD  2012:55 2013:163 2014:36 2015:26 2016:34 2017:36 2018:49 2019:46 2020:18
  Urban Outfitters, Inc.                    2017:21 2018:20 2019:14 2020:10

## what

OWNER: Joint 40%, Spouse 38%, Self 15%, N/A 6%, Child 2%

ASSET_TYPE: Stock 81%, PDF Disclosed Filing 6%, Municipal Security 5%, Other Securities 4%, Corporate Bond 3%, Non-Public Stock 1%, Stock Option 1%

TYPE: Purchase 49%, Sale (Full) 24%, Sale (Partial) 21%, N/A 6%, Exchange 1%

AMOUNT: $1,001 - $15,000 65%, $15,001 - $50,000 18%, $50,001 - $100,000 6%, Unknown 6%, $100,001 - $250,000 3%, $250,001 - $500,000 1%, $500,001 - $1,000,000 1%, $1,000,001 - $5,000,000 0%, $5,000,001 - $25,000,000 0%, $25,000,001 - $50,000,000 0%, Over $50,000,000 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TRANSACTION_DATE | date | 1.7K | 0 | 04/14/2020 148; 02/13/2015 128; 06/15/2017 122; 04/07/2020 116 |
| OWNER | category | 5 | 0 | Joint 3.3K; Spouse 3.1K; Self 1.3K; N/A 463 |
| TICKER | other | 1.0K | 0 | -- 1.6K; N/A 463; AAPL 153; BAC 84 |
| ASSET_DESCRIPTION | who | 2.6K | 0 | This filing was disclosed 463; Apple Inc. 127; Bank of America Corporati 76; First Data Corporation 74 |
| ASSET_TYPE | category | 8 | 666 | Stock 6.2K; PDF Disclosed Filing 463; Municipal Security 354; Other Securities 305 |
| TYPE | category | 5 | 0 | Purchase 4.1K; Sale (Full) 2.0K; Sale (Partial) 1.7K; N/A 463 |
| AMOUNT | category | 11 | 0 | $1,001 - $15,000 5.4K; $15,001 - $50,000 1.5K; $50,001 - $100,000 493; Unknown 463 |
| COMMENT | who | 234 | 463 | -- 7.1K; R 179; sep 117; 555 51 |
| SENATOR | who | 67 | 0 | David A Perdue , Jr 2.6K; Thomas R Carper 877; Sheldon Whitehouse 687; Pat Roberts 460 |
| PTR_LINK | other | 1.4K | 0 | https://efdsearch.senate. 189; https://efdsearch.senate. 181; https://efdsearch.senate. 145; https://efdsearch.senate. 113 |
| _INGESTED_AT | audit | 1 | 0 | 1785614421741010 8.3K |
| _SOURCE_RUN_ID | audit | 1 | 0 | f43f6d15-7c99-4cf9-b43a-c 8.3K |
| _SRC_SHA256 | who | 1 | 0 | d99afca9e7e56352c8d3dcfc2 8.3K |
