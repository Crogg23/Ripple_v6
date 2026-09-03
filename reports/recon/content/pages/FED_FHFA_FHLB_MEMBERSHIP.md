# FED_FHFA_FHLB_MEMBERSHIP

rows 6.3K  columns 17  scan 3.2s

roles: audit 2, category 3, date 2, id 4, other 2, state 1, who 3

## when

APPR_DATE
  2000       356  ##############################
  2001       174  ###############
  2002       155  #############
  2003       150  #############
  2004       152  #############
  2005       117  ##########
  2006       139  ############
  2007        98  ########
  2008       187  ################
  2009       117  ##########
  2010        88  #######
  2011       136  ###########
  2012        97  ########
  2013        94  ########
  2014       135  ###########
  2015       134  ###########
  2016       122  ##########
  2017       117  ##########
  2018       138  ############
  2019       122  ##########
  2020       132  ###########
  2021        72  ######
  2022        78  #######
  2023       141  ############
  2024       109  #########
  2025        76  ######
  2026        10  #

MEM_DATE
  2000       345  ##############################
  2001       185  ################
  2002       152  #############
  2003       156  ##############
  2004       150  #############
  2005       121  ###########
  2006       132  ###########
  2007       100  #########
  2008       189  ################
  2009       121  ###########
  2010        79  #######
  2011       141  ############
  2012        97  ########
  2013        91  ########
  2014       129  ###########
  2015       133  ############
  2016       126  ###########
  2017       118  ##########
  2018       136  ############
  2019       120  ##########
  2020       138  ############
  2021        71  ######
  2022        83  #######
  2023       140  ############
  2024       105  #########
  2025        84  #######
  2026        13  #
  2033        19  ##
  2034        16  #
  2035        10  #

## who

MEMBER_NAME by rows
        30  First State Bank
        13  Citizens State Bank
        13  Farmers State Bank
        13  Peoples Bank
        11  Community State Bank
        11  Farmers and Merchants Bank
        10  First Community Bank
         9  First Bank
         9  Security State Bank
         8  First FS & LA
         8  Citizens Bank
         8  First National Bank
         8  Community Bank
         7  The Peoples Bank
         7  Pinnacle Bank
         6  First Security Bank
         6  Liberty Bank
         6  Citizens Bank & Trust Company
         6  Peoples State Bank
         5  Citizens Savings Bank

CITY by rows
        51  New York
        47  Chicago
        31  Houston
        28  Columbus
        26  Washington
        26  Dallas
        26  Oklahoma City
        25  Springfield
        23  Madison
        22  Omaha
        21  Cincinnati
        21  West Des Moines
        19  Los Angeles
        18  Wilmington
        18  Philadelphia
        17  Honolulu
        17  Miami
        17  Birmingham
        17  San Antonio
        17  Lincoln

SRC_SHA256 by rows
      6.3K  13bc811157fa20e703204815b7b0fc1181ea22ab0efb2e409d0a3388f720c08e

## who x when

MEMBER_NAME by MEM_DATE
  Citizens Bank                             2000:1 2002:1 2009:1
  Citizens Bank & Trust Company             2000:1 2008:1
  Citizens Savings Bank                     2000:1
  Citizens State Bank                       2000:2 2004:1 2014:1 2024:1
  Community Bank                            2000:1 2006:1
  Community State Bank                      2000:1 2001:1 2004:1 2006:1 2009:1 2026:1
  Farmers State Bank                        2000:3 2001:1 2003:1
  Farmers and Merchants Bank                2003:1 2025:1 2026:1
  First Bank                                2007:1 2015:2
  First National Bank                       2000:1 2002:1
  First Security Bank                       2006:1
  First State Bank                          2000:7 2002:1 2004:2 2005:2 2018:1 2019:1 2021:1 2023:1
  Liberty Bank                              2011:1 2023:1
  Peoples Bank                              2018:1 2020:1
  Peoples State Bank                        2002:1 2003:1
  Pinnacle Bank                             2007:1 2026:1
  Security State Bank                       2000:2 2007:1 2019:1 2023:1
  The Peoples Bank                          2001:1 2005:1 2009:1

CITY by MEM_DATE
  Birmingham                                2000:2 2004:1 2015:2 2016:1 2017:2 2018:1 2020:1 2021:1 2024:1
  Chicago                                   2001:2 2002:1 2003:1 2004:1 2005:1 2008:1 2009:1 2010:1 2011:1 2013:4 2015:1 2016:2 2017:2 2018:4 2020:3 2021:3 2022:2 2024:1
  Cincinnati                                2001:1 2006:1 2009:1 2011:2 2016:2 2017:1 2021:1
  Columbus                                  2000:1 2001:2 2002:1 2003:1 2004:1 2008:2 2010:1 2011:1 2012:2 2015:2 2017:1 2018:1 2019:2 2020:2 2024:1
  Dallas                                    2001:1 2003:3 2006:1 2008:3 2009:1 2015:1 2017:2 2018:3 2019:1 2020:1 2022:1 2024:2
  Honolulu                                  2000:1 2014:1 2016:1 2018:1 2020:1 2023:1 2024:1 2025:1
  Houston                                   2000:1 2003:1 2004:1 2005:1 2007:1 2008:1 2009:1 2010:2 2011:2 2014:1 2017:1 2019:1 2020:5 2022:1 2023:2 2024:1
  Lincoln                                   2002:1 2008:1 2016:3 2017:2 2021:1 2023:1 2025:1 2033:1
  Los Angeles                               2000:2 2003:1 2006:1 2014:1 2015:2 2016:2 2017:1 2019:1
  Madison                                   2000:1 2002:1 2003:1 2009:2 2011:1 2013:1 2016:1 2020:1 2021:1 2022:1 2023:1 2024:1 2025:2 2026:1
  Miami                                     2000:1 2002:1 2007:1 2014:1 2023:1 2024:1 2025:1
  New York                                  2000:1 2002:1 2003:1 2005:2 2007:1 2008:1 2013:1 2014:3 2015:2 2016:3 2017:3 2018:3 2019:2 2020:5 2021:3 2022:2 2024:3 2025:4
  Oklahoma City                             2000:2 2002:2 2003:1 2005:2 2013:1 2017:1 2019:1 2020:1 2022:1
  Omaha                                     2002:3 2005:1 2008:2 2014:1 2019:1 2021:3 2024:1
  Philadelphia                              2000:1 2014:1 2015:3 2017:3 2021:1
  San Antonio                               2002:2 2015:1 2017:1 2018:5 2020:1 2023:2
  Springfield                               2000:1 2005:1 2007:1 2012:1 2013:2 2014:2 2015:1 2017:2 2018:1 2020:1 2021:1 2023:1 2034:1
  Washington                                2000:2 2002:1 2013:1 2014:1 2015:1 2020:2 2021:1 2022:1 2023:1 2024:1 2025:2
  West Des Moines                           2002:1 2009:1 2013:1 2015:1 2017:1 2018:1 2019:1 2022:1 2025:2
  Wilmington                                2008:1 2015:1 2016:1 2017:1 2018:4 2023:2 2024:2

## where

STATE: TX 448, IL 396, IA 296, OH 290, CA 266, MN 260, MO 230, WI 229, NY 227, MI 206, PA 198, KS 194

## what

DISTRICT: Des Moines 19%, Atlanta 12%, Dallas 12%, Topeka 10%, Chicago 10%, Cincinnati 9%, Boston 7%, Indianapolis 6%, New York 5%, San Francisco 5%, Pittsburgh 4%

MEM_TYPE: Commercial Bank 55%, Credit Union 26%, Insurance Company 10%, Savings Bank 4%, Saving Associate 4%, Community Development Financia 1%

CHAR_TYPE: State 70%, Federal 19%, National 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FHFA_ID | id | 6.2K | 0 | 56994 32; 56993 32; 56992 32; 56988 32 |
| DISTRICT | category | 11 | 0 | Des Moines 1.2K; Atlanta 770; Dallas 769; Topeka 648 |
| MEMBER_NAME | who | 5.8K | 0 | Farmers and Merchants Ban 33; First State Bank 33; MapleMark Bank 32; Ozark National Life Insur 32 |
| CITY | who | 3.4K | 0 | New York 58; Chicago 47; Houston 39; Madison 36 |
| STATE | state | 54 | 0 | TX 448; IL 396; IA 296; OH 290 |
| ZIP | other | 4.7K | 0 | 60606 35; 07960 33; 50266 33; 43615 33 |
| MEM_TYPE | category | 6 | 0 | Commercial Bank 3.5K; Credit Union 1.6K; Insurance Company 622; Savings Bank 269 |
| CHAR_TYPE | category | 3 | 705 | State 3.9K; Federal 1.1K; National 614 |
| CERT | id | 4.0K | 2.3K | 03182 20; 05619 20; 35583 20; 04144 20 |
| FED_ID | id | 4.0K | 2.3K | 0594451 20; 0378044 20; 2925666 20; 0836656 20 |
| NCUA_ID | id | 1.7K | 4.7K | 23521 9; 08367 9; 95786 9; 64036 9 |
| NAIC_ID | other | 621 | 5.7K | 67393 4; 69922 4; 16924 4; 30180 4 |
| APPR_DATE | date | 3.5K | 518 | 12/18/25 33; 07/10/23 33; 12/24/24 32; 04/02/24 32 |
| MEM_DATE | date | 4.1K | 0 | 12/31/89 337; 12/29/25 32; 12/26/25 32; 10/24/25 32 |
| INGESTED_AT | audit | 1 | 0 | 1786129697399693 6.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | cb1bbb7f-9747-42ef-8913-e 6.3K |
| SRC_SHA256 | who | 1 | 0 | 13bc811157fa20e703204815b 6.3K |
