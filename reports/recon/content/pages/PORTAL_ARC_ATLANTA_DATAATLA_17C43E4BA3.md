# PORTAL_ARC_ATLANTA_DATAATLA_17C43E4BA3

rows 594  columns 20  scan 3.1s

roles: amount 2, audit 2, date 5, other 7, who 5

## when

APPR_DATE
  2001         4  ####
  2002         3  ###
  2003         3  ###
  2004         1  #
  2005         7  ########
  2006         3  ###
  2007        27  ##############################
  2008        14  ################
  2009         6  #######
  2010         2  ##
  2011         1  #

CREATED_DATE
  2026       594  ##############################

DATE_APP
  1979         1  #
  1985         2  ##
  1987         3  ###
  1991         2  ##
  1992         1  #
  1993         3  ###
  1995         2  ##
  1996         5  ####
  1998         1  #
  2001         4  ###
  2002         3  ###
  2003         3  ###
  2004        14  ############
  2005        27  #######################
  2006        16  ##############
  2007        33  ############################
  2008        23  ####################
  2009        18  ###############
  2010        21  ##################
  2011        24  #####################
  2012        15  #############
  2013        13  ###########
  2014        22  ###################
  2015        17  ###############
  2016        26  ######################
  2017        32  ###########################
  2018        30  ##########################
  2019        35  ##############################
  2020        19  ################
  2021        20  #################
  2022        12  ##########
  2023        20  #################
  2024        17  ###############
  2025        25  #####################
  2026         6  #####

LAST_EDITED_DATE
  2026       594  ##############################

INGESTED_AT
  2026       594  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 594 | 13.49 | 7.6K | 481.0K | 1.38M | 20.42M |
| SHAPE__LENGTH | 594 | 14.69 | 386.75 | 4.8K | 8.7K | 376.8K |

## who

GRANTEE by rows
        31  nan
         5  Pace Academy
         4  Cherokee Town Club
         4  Timothy J O'Toole
         3  Northside Drive Baptist Church
         3  Regency Retail Partnership L P
         3  Buckhead Avenues Development Co. LLC
         3  Jaycee Development LLC
         3  The Lovett School
         3  Ansley Golf Club
         3  Development Authority of Fulton County
         3  Atlanta International School
         3  Atlanta BeltLine Inc
         3  Elizabeth Omilami
         3  Heritage Preparatory Scholl of Georgia
         3  Randy Pisler
         2  Piedmont Driving Club
         2  Atlanta History Center
         2  Wylde Center
         2  Deke D. Cooper

GRANTEE by dollars
       1.98M       31 rows  nan
       1.44M        3 rows  The Lovett School
       1.38M        1 rows  East Lake Holdings Inc.
       1.12M        3 rows  Ansley Golf Club
       1.02M        1 rows  The Westminster School
      590.1K        1 rows  Winifred Watts Hemphill
      563.1K        5 rows  Pace Academy
      514.7K        1 rows  Capital City Club
      446.5K        1 rows  Princeton Lake Preserve LLC
      411.5K        1 rows  AMK Property Holdings  LLC
      390.8K        4 rows  Cherokee Town Club
      385.9K        2 rows  Atlanta History Center
      319.1K        3 rows  Northside Drive Baptist Church
      255.7K        1 rows  Georgia Waste Systems
      227.2K        3 rows  Atlanta International School
      222.3K        1 rows  Passionist Farthers of GA INC
      203.8K        2 rows  The Halle Foundation
      187.1K        1 rows  SRPFA/Moreland LLC
      166.9K        1 rows  VB BTS III LLC
      153.5K        1 rows  Imhotep Foundation

APPSTATUS by rows
       594  Approved

APPSTATUS by dollars
      20.42M      594 rows  Approved

CREATED_USER by rows
       594  gpickren2

CREATED_USER by dollars
      20.42M      594 rows  gpickren2

LAST_EDITED_USER by rows
       594  gpickren2

LAST_EDITED_USER by dollars
      20.42M      594 rows  gpickren2

## who x when

GRANTEE by DATE_APP, dollars = SHAPE__AREA
  AMK Property Holdings  LLC                2021:411.5K
  Ansley Golf Club                          2008:372.4K 2016:372.4K
  Atlanta History Center                    2013:194.0K 2015:191.9K
  Atlanta International School              2007:120.8K 2015:106.4K
  Buckhead Avenues Development Co. LLC      2007:44.1K
  Capital City Club                         2007:514.7K
  Cherokee Town Club                        2008:88.8K 2017:106.6K 2025:106.6K
  Deke D. Cooper                            2007:15.8K 2011:15.8K
  Development Authority of Fulton County    2016:11.1K 2019:5.5K
  East Lake Holdings Inc.                   2016:1.38M
  Elizabeth Omilami                         2007:4.1K 2009:4.3K 2017:4.1K
  Georgia Waste Systems                     2013:255.7K
  Heritage Preparatory Scholl of Georgia    2020:18.6K 2021:18.6K 2024:18.6K
  Jaycee Development LLC                    2019:31.5K
  Northside Drive Baptist Church            2007:212.7K 2025:106.4K
  Pace Academy                              2006:55.5K 2007:13.3K 2019:156.2K 2026:182.0K
  Passionist Farthers of GA INC             2014:222.3K
  Piedmont Driving Club                     2008:42.3K 2018:42.3K
  Princeton Lake Preserve LLC               2017:446.5K
  Randy Pisler                              2017:21.6K
  Regency Retail Partnership L P            2005:75.1K 2015:32.4K
  SRPFA/Moreland LLC                        2020:187.1K
  The Halle Foundation                      2020:101.9K 2025:101.9K
  The Lovett School                         2007:481.0K 2020:481.0K 2024:481.0K
  Timothy J O'Toole                         2017:2.7K 2019:2.7K
  Winifred Watts Hemphill                   2005:590.1K
  Wylde Center                              2014:1.6K 2023:1.6K
  nan                                       1993:3.7K 2005:24.6K 2008:9.0K 2009:46.0K 2011:549.8K 2012:1.07M 2013:10.8K 2014:2.1K 2017:673.79 2018:26.7K 2019:4.6K 2022:168.6K 2023:1.1K 2025:718.54

APPSTATUS by DATE_APP, dollars = SHAPE__AREA
  Approved                                  1979:1.4K 1985:2.5K 1987:7.6K 1991:15.8K 1992:5.2K 1993:6.7K 1995:2.8K 1996:34.2K 1998:1.1K 2001:40.4K 2002:51.8K 2003:40.8K 2004:225.6K 2005:1.32M 2006:343.7K 2007:1.64M 2008:1.03M 2009:356.6K 2010:559.9K 2011:861.2K 2012:1.17M 2013:501.3K 2014:510.4K 2015:640.9K 2016:1.92M 2017:1.10M 2018:694.8K 2019:674.8K 2020:910.4K 2021:725.6K 2022:319.6K 2023:175.8K 2024:824.5K 2025:597.9K 2026:375.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 587 | 0 | 46721 3; 44801 3; 44177 3; 44162 3 |
| ADDRESS | other | 523 | 0 | 979 Crescent Ave 6; 966 West Paces Ferry Road 5; 1800 Piedmont Rd NE 5; 1000 Marietta St NW 5 |
| APPR_DATE | date | 61 | 18 | nan 487; 07/05/07 7; 08/26/08 5; 02/12/08 5 |
| APPSTATUS | who | 1 | 0 | Approved 594 |
| CREATED_DATE | date | 1 | 0 | 1774542156814 594 |
| CREATED_USER | who | 1 | 0 | gpickren2 594 |
| DATE_APP | date | 278 | 0 | nan 79; 1566950400000.0 7; 1573603200000.0 7; 1481673600000.0 7 |
| GRANTEE | who | 499 | 0 | nan 31; Pace Academy 5; Heritage Preparatory Scho 5; Jaycee Development LLC 5 |
| LAST_EDITED_DATE | date | 1 | 0 | 1774542156814 594 |
| LAST_EDITED_USER | who | 1 | 0 | gpickren2 594 |
| ORDINANCE | other | 507 | 0 | nan 77; 21-O-0392 5; 24-O-1026 4; 19-O-1031 4 |
| SUP_DOCKET | other | 550 | 2 | nan 34; observed 6; U-18-037 4; U-21-010 4 |
| SUP_TYPE | other | 53 | 0 | PCH 80; DCC 75; CHU 54; PVS 46 |
| GLOBALID | other | 579 | 0 | c89d7aef-7155-4c9f-8b6f-b 3; 48cd611b-fdd9-42c0-a63a-b 3; 4a58dd93-ad98-488f-b3a5-6 3; a93c8770-2b80-45a6-b52e-4 3 |
| SHAPE__AREA | amount | 538 | 0 | 5006.47265625 7; 106358.6796875 5; 18592.65625 5; 27964.69921875 5 |
| SHAPE__LENGTH | amount | 526 | 0 | 301.90347743725164 7; 1980.1980778571512 5; 658.7150207505449 5; 689.6621107877439 5 |
| GEOMETRY | other | 533 | 0 | {"type": "Polygon", "coor 7; {"type": "Polygon", "coor 5; {"type": "Polygon", "coor 5; {"type": "Polygon", "coor 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:51:26.45104 594 |
| SOURCE_RUN_ID | audit | 1 | 0 | 371a6ca9-5a89-4df6-8fe4-f 594 |
| SRC_SHA256 | who | 1 | 0 | 87326dbe8be276df41df29f33 594 |
