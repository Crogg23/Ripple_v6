# PORTAL_CKA_WPRDC_ALLEGHENY_CE7A2694FC

rows 2.0K  columns 20  scan 3.7s

roles: amount 3, audit 2, category 9, date 2, id 1, other 2, who 2

## when

APPROVED_DATE
  2007         2  
  2008        29  ##
  2009       256  #####################
  2010        42  ####
  2011       106  #########
  2012       116  ##########
  2013        60  #####
  2014       122  ##########
  2015       192  ################
  2016       144  ############
  2017       358  ##############################
  2018       221  ###################
  2019       120  ##########
  2020       100  ########
  2021        31  ###
  2022        25  ##
  2023        14  #
  2024        37  ###

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ABATEMENT_AMOUNT | 2.0K | 2.5K | 250.0K | 250.0K | 250.0K | 320.96M |
| LONGITUDE | 2.0K | -80.08 | -79.98 | -79.90 | -79.89 | -157.9K |
| LATITUDE | 2.0K | 40.36 | 40.45 | 40.48 | 40.49 | 79.9K |

## who

NEIGHBORHOOD by rows
       397  Central Business District
       217  Strip District
       209  Upper Lawrenceville
       206  Lower Lawrenceville
       105  East Allegheny
        76  Central Northside
        71  California-Kirkbride
        70  Central Lawrenceville
        58  Manchester
        55  South Side Flats
        47  Duquesne Heights
        45  Squirrel Hill South
        39  Larimer
        25  Hazelwood
        23  East Liberty
        23  Bluff
        22  Mount Washington
        22  Perry South
        20  Homewood South
        17  West Oakland

NEIGHBORHOOD by dollars
      51.34M      209 rows  Upper Lawrenceville
      50.74M      206 rows  Lower Lawrenceville
      47.29M      397 rows  Central Business District
      24.76M      105 rows  East Allegheny
      17.75M       71 rows  California-Kirkbride
      14.22M       58 rows  Manchester
       9.16M       55 rows  South Side Flats
       8.63M       76 rows  Central Northside
       8.45M      217 rows  Strip District
       7.47M       70 rows  Central Lawrenceville
       6.03M       25 rows  Hazelwood
       5.50M       22 rows  Perry South
       5.43M       39 rows  Larimer
       5.00M       20 rows  Homewood South
       4.64M       23 rows  Bluff
       4.52M       47 rows  Duquesne Heights
       4.45M       45 rows  Squirrel Hill South
       3.92M       16 rows  Upper Hill
       3.40M       16 rows  Allentown
       2.71M       23 rows  East Liberty

SRC_SHA256 by rows
      2.0K  003fbdf0f65fcddbbfba158bd7523672e677cc4df75b20323f343cd8ec60bdbe

SRC_SHA256 by dollars
     320.96M     2.0K rows  003fbdf0f65fcddbbfba158bd7523672e677cc4df75b20323f343cd8ec60

## who x when

NEIGHBORHOOD by APPROVED_DATE, dollars = ABATEMENT_AMOUNT
  Allentown                                 2008:250.0K 2013:750.0K 2014:100.0K 2015:1.00M 2017:50.0K 2018:500.0K 2019:250.0K 2021:500.0K
  Bluff                                     2012:300.0K 2013:300.0K 2015:750.0K 2016:400.0K 2018:836.8K 2020:500.0K 2021:175.0K 2022:500.0K 2024:875.0K
  California-Kirkbride                      2017:6.50M 2018:8.25M 2020:1.00M 2021:1.50M 2022:500.0K
  Central Business District                 2007:150.0K 2008:152.7K 2009:37.62M 2011:450.0K 2012:712.1K 2013:1.00M 2014:350.0K 2015:500.0K 2016:1.15M 2017:1.96M 2018:1.20M 2019:250.0K 2020:750.0K 2021:175.0K 2022:500.0K 2024:375.0K
  Central Lawrenceville                     2010:100.0K 2011:173.5K 2012:250.0K 2013:86.8K 2014:954.2K 2015:1.46M 2016:510.2K 2017:1.38M 2018:1.11M 2019:520.5K 2020:173.5K 2022:750.0K
  Central Northside                         2012:336.8K 2015:607.2K 2016:250.0K 2017:1.69M 2018:3.86M 2019:260.2K 2021:1.45M 2022:175.0K
  Duquesne Heights                          2011:347.0K 2012:173.5K 2013:173.5K 2014:173.5K 2015:433.8K 2016:520.5K 2017:433.8K 2018:1.21M 2019:173.5K 2021:700.0K 2022:175.0K
  East Allegheny                            2008:250.0K 2009:1.84M 2010:2.25M 2011:750.0K 2012:3.34M 2014:3.09M 2015:3.25M 2016:750.0K 2017:5.25M 2018:3.00M 2019:750.0K 2024:250.0K
  East Liberty                              2009:50.0K 2011:86.8K 2012:423.5K 2014:250.0K 2015:460.2K 2016:857.2K 2017:250.0K 2018:86.8K 2022:125.0K 2024:125.0K
  Hazelwood                                 2008:1.25M 2009:250.0K 2014:250.0K 2016:500.0K 2017:1.25M 2019:1.25M 2021:250.0K 2022:250.0K 2024:775.0K
  Homewood South                            2008:1.50M 2009:1.00M 2011:1.00M 2014:1.50M
  Larimer                                   2010:86.8K 2014:4.75M 2016:340.0K 2022:250.0K
  Lower Lawrenceville                       2010:250.0K 2011:3.50M 2012:7.80M 2013:3.25M 2014:3.15M 2015:6.39M 2016:2.25M 2017:5.75M 2018:2.75M 2019:7.50M 2020:7.40M 2021:250.0K 2022:500.0K
  Manchester                                2010:500.0K 2011:1.50M 2012:1.75M 2013:1.25M 2014:1.75M 2015:750.0K 2016:2.25M 2017:1.75M 2018:500.0K 2019:300.0K 2020:1.50M 2021:425.0K
  Mount Washington                          2009:250.0K 2012:86.8K 2013:423.5K 2014:173.5K 2015:433.8K 2016:347.0K 2017:86.8K 2018:86.8K 2019:86.8K 2022:350.0K 2023:175.0K
  Perry South                               2017:500.0K 2018:1.00M 2020:4.00M
  South Side Flats                          2008:86.8K 2009:136.8K 2010:520.5K 2011:173.5K 2014:750.0K 2015:2.63M 2017:597.0K 2018:173.5K 2019:86.8K 2020:250.0K 2024:3.75M
  Squirrel Hill South                       2008:86.8K 2010:260.2K 2011:173.5K 2012:173.5K 2013:607.2K 2014:954.2K 2015:867.5K 2017:810.2K 2018:86.8K 2021:175.0K 2023:250.0K
  Strip District                            2007:150.0K 2010:58.1K 2011:303.9K 2012:50.0K 2014:550.0K 2015:1.63M 2016:947.2K 2017:602.7K 2018:789.1K 2019:1.27M 2020:823.5K 2021:925.0K 2022:350.0K
  Upper Hill                                2008:1.50M 2009:250.0K 2010:250.0K 2012:250.0K 2015:1.25M 2019:250.0K 2023:175.0K
  Upper Lawrenceville                       2008:250.0K 2009:500.0K 2010:1.25M 2012:750.0K 2013:1.50M 2014:2.59M 2015:7.55M 2016:3.25M 2017:23.05M 2018:5.25M 2019:4.30M 2020:500.0K 2022:175.0K 2023:425.0K
  West Oakland                              2013:150.0K 2017:500.0K 2020:1.21M

SRC_SHA256 by APPROVED_DATE, dollars = ABATEMENT_AMOUNT
  003fbdf0f65fcddbbfba158bd7523672e677cc4d  2007:300.0K 2008:6.41M 2009:42.57M 2010:6.55M 2011:9.68M 2012:19.15M 2013:11.39M 2014:22.86M 2015:33.30M 2016:16.37M 2017:57.49M 2018:33.31M 2019:18.04M 2020:19.86M 2021:6.70M 2022:5.53M 2023:3.05M 2024:8.40M

## what

START_YEAR: 2021 13%, 2017 13%, 2018 11%, 2019 10%, 2016 10%, 2022 8%, 2014 8%, 2013 7%, 2010 7%, 2020 7%, 2012 6%

PROGRAM_NAME: ACT42 ENHANCED RESIDENTIAL 46%, ACT42 RESIDENTIAL 19%, RESIDENTIAL ENHANCED LERTA 18%, LOCAL ECONOMIC STIMULUS 5%, RESIDENTIAL LERTA 3%, CHAPTER 265 ENHANCED 3%, COMMERCIAL LERTA 3%, CHAPTER 265 BASE 2%, VISITABILITY RESIDENTIAL 1%, CHAPTER 267 ENHANCED 1%, CHAPTER 267 BASE 0%, LERTA PRIOR TO 07/2007 0%

NUM_YEARS: 10 76%, 3 20%, 5 4%

COUNCIL_DISTRICT: 7 37%, 6 36%, 1 8%, 9 5%, 3 5%, 2 4%, 5 4%, 8 1%, 4 0%

WARD: 2 27%, 10 14%, 6 13%, 1 10%, 25 8%, 23 6%, 21 6%, 9 4%, 19 4%, 15 3%, 12 3%, 14 3%

DPW_STREETS: 2 31%, 6 31%, 1 20%, 3 10%, 5 4%, 4 4%

DPW_ENVIRO: Central 64%, Northern 20%, Eastern 8%, Southern 8%

DPW_PARKS: Highland 40%, Riverview 38%, Schenley 8%, Frick 6%, Emerald 5%, Northern 1%, McKinley 1%, Northeast 1%, Western 0%, Eastern 0%

POLICE_ZONE: 2 59%, 1 19%, 3 8%, 4 7%, 5 6%, 6 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PIN | id | 1.9K | 0 | 0008S00155000000 11; 0002A00025000000 11; 0025K00050000000 11; 0024S00072000000 11 |
| ADDRESS | other | 1.8K | 0 | 11 5TH AVE 22; 725 PENN AVE 11; 820 LIBERTY AVE 11; 211 26TH ST 11 |
| START_YEAR | category | 18 | 549 | 2021 159; 2017 148; 2018 135; 2019 121 |
| APPROVED_DATE | date | 655 | 0 | 2009-06-10 126; 2017-12-29 88; 2017-11-21 70; 2009-11-20 45 |
| PROGRAM_NAME | category | 12 | 0 | ACT42 ENHANCED RESIDENTIA 916; ACT42 RESIDENTIAL 367; RESIDENTIAL ENHANCED LERT 354; LOCAL ECONOMIC STIMULUS 89 |
| NUM_YEARS | category | 3 | 0 | 10 1.5K; 3 404; 5 73 |
| ABATEMENT_AMOUNT | amount | 8 | 0 | 250000 1.1K; 86750 367; 2700 354; 150000 69 |
| NEIGHBORHOOD | who | 62 | 1 | Central Business District 397; Strip District 217; Upper Lawrenceville 209; Lower Lawrenceville 206 |
| COUNCIL_DISTRICT | category | 10 | 1 | 7 735; 6 701; 1 157; 9 102 |
| WARD | category | 32 | 1 | 2 450; 10 226; 6 221; 1 173 |
| DPW_STREETS | category | 7 | 1 | 2 621; 6 608; 1 390; 3 192 |
| DPW_ENVIRO | category | 5 | 1 | Central 1.3K; Northern 389; Eastern 165; Southern 155 |
| DPW_PARKS | category | 11 | 1 | Highland 793; Riverview 749; Schenley 156; Frick 117 |
| POLICE_ZONE | category | 7 | 1 | 2 1.2K; 1 375; 3 150; 4 141 |
| FIRE_ZONE | other | 73 | 1 | 1-4 278; 3-5 226; 2-25 194; 3-3 172 |
| LONGITUDE | amount | 1.9K | 1 | -79.99974210704873 11; -79.99818730272801 11; -79.97832861102809 11; -79.98385599725997 11 |
| LATITUDE | amount | 1.9K | 1 | 40.44379019089672 11; 40.44271322221956 11; 40.45590383093392 11; 40.45443939822557 11 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:02:40.34783 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 75d21209-8350-4e65-89ea-0 2.0K |
| SRC_SHA256 | who | 1 | 0 | 003fbdf0f65fcddbbfba158bd 2.0K |
