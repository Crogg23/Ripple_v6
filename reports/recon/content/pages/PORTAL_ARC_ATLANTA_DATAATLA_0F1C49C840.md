# PORTAL_ARC_ATLANTA_DATAATLA_0F1C49C840

rows 598  columns 20  scan 3.5s

roles: amount 2, audit 2, category 2, date 5, other 7, who 3

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
  2018       440  ##############################
  2019        28  ##
  2020        12  #
  2021        15  #
  2022        31  ##
  2023        19  #
  2024        24  ##
  2025        24  ##
  2026         5  

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
  2026        10  #########

LAST_EDITED_DATE
  2018       427  ##############################
  2019        35  ##
  2020        12  #
  2021         8  #
  2022        36  ###
  2023        20  #
  2024        23  ##
  2025        26  ##
  2026        11  #

INGESTED_AT
  2026       598  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_AREA | 598 | 100 | 56.6K | 3.56M | 10.25M | 152.53M |
| SHAPE_LEN | 598 | 40 | 1.1K | 13.1K | 23.7K | 1.03M |

## who

GRANTEE by rows
        31  nan
         5  Pace Academy
         4  Cherokee Town Club
         4  Timothy J O'Toole
         3  The Lovett School
         3  Heritage Preparatory Scholl of Georgia
         3  Regency Retail Partnership L P
         3  Jaycee Development LLC
         3  Atlanta BeltLine Inc
         3  Atlanta International School
         3  Randy Pisler
         3  Development Authority of Fulton County
         3  Ansley Golf Club
         3  Buckhead Avenues Development Co. LLC
         3  Elizabeth Omilami
         3  Northside Drive Baptist Church
         2  Agape Christian Academy
         2  Regency Retail Group LLC
         2  Dorothy Ward
         2  Mary F. Knight Bagwell

GRANTEE by dollars
      14.65M       31 rows  nan
      10.68M        3 rows  The Lovett School
      10.25M        1 rows  East Lake Holdings Inc.
       8.28M        3 rows  Ansley Golf Club
       7.56M        1 rows  The Westminster School
       4.38M        1 rows  Winifred Watts Hemphill
       4.17M        5 rows  Pace Academy
       3.81M        1 rows  Capital City Club
       3.32M        1 rows  Princeton Lake Preserve LLC
       3.06M        1 rows  AMK Property Holdings  LLC
       2.89M        4 rows  Cherokee Town Club
       2.86M        2 rows  Atlanta History Center
       2.36M        3 rows  Northside Drive Baptist Church
       1.89M        1 rows  Georgia Waste Systems
       1.68M        3 rows  Atlanta International School
       1.65M        1 rows  Passionist Farthers of GA INC
       1.51M        2 rows  The Halle Foundation
       1.39M        1 rows  SRPFA/Moreland LLC
       1.24M        1 rows  VB BTS III LLC
       1.14M        1 rows  Imhotep Foundation

APPSTATUS by rows
       598  Approved

APPSTATUS by dollars
     152.53M      598 rows  Approved

SRC_SHA256 by rows
       598  5cf649aee63edd2a98c27010f6768c5a1c70f1ec536586d3c90c5a14766b9e8d

SRC_SHA256 by dollars
     152.53M      598 rows  5cf649aee63edd2a98c27010f6768c5a1c70f1ec536586d3c90c5a14766b

## who x when

GRANTEE by DATE_APP, dollars = SHAPE_AREA
  AMK Property Holdings  LLC                2021:3.06M
  Agape Christian Academy                   2009:35.3K
  Ansley Golf Club                          2008:2.76M 2016:2.76M
  Atlanta History Center                    2013:1.44M 2015:1.42M
  Atlanta International School              2007:894.9K 2015:788.0K
  Buckhead Avenues Development Co. LLC      2007:326.5K
  Capital City Club                         2007:3.81M
  Cherokee Town Club                        2008:657.9K 2017:789.1K 2025:789.1K
  Development Authority of Fulton County    2016:82.3K 2019:41.1K
  Dorothy Ward                              1987:6.8K
  East Lake Holdings Inc.                   2016:10.25M
  Elizabeth Omilami                         2007:30.5K 2009:31.6K 2017:30.5K
  Georgia Waste Systems                     2013:1.89M
  Heritage Preparatory Scholl of Georgia    2020:137.8K 2021:137.8K 2024:137.8K
  Jaycee Development LLC                    2019:233.9K
  Mary F. Knight Bagwell                    1996:63.2K 2014:63.2K
  Northside Drive Baptist Church            2007:1.58M 2025:787.6K
  Pace Academy                              2006:411.4K 2007:98.3K 2019:1.16M 2026:1.35M
  Passionist Farthers of GA INC             2014:1.65M
  Princeton Lake Preserve LLC               2017:3.32M
  Randy Pisler                              2017:160.1K
  Regency Retail Group LLC                  2015:418.0K 2021:418.0K
  Regency Retail Partnership L P            2005:555.8K 2015:240.1K
  The Halle Foundation                      2020:754.3K 2025:754.3K
  The Lovett School                         2007:3.56M 2020:3.56M 2024:3.56M
  Timothy J O'Toole                         2017:20.1K 2019:20.1K
  Winifred Watts Hemphill                   2005:4.38M
  nan                                       1993:27.5K 2005:182.2K 2008:66.7K 2009:341.2K 2011:4.08M 2012:7.96M 2013:80.2K 2014:15.3K 2017:5.0K 2018:198.3K 2019:34.4K 2022:1.25M 2023:8.0K 2025:5.3K

APPSTATUS by DATE_APP, dollars = SHAPE_AREA
  Approved                                  1979:10.6K 1985:18.9K 1987:56.3K 1991:116.9K 1992:38.9K 1993:49.9K 1995:20.5K 1996:253.7K 1998:8.1K 2001:299.0K 2002:383.8K 2003:302.8K 2004:1.67M 2005:9.78M 2006:2.55M 2007:12.15M 2008:7.64M 2009:2.65M 2010:4.15M 2011:6.39M 2012:8.67M 2013:3.71M 2014:3.78M 2015:4.75M 2016:14.24M 2017:8.15M 2018:5.15M 2019:5.00M 2020:6.75M 2021:5.39M 2022:2.38M 2023:1.31M 2024:6.11M 2025:4.43M 2026:3.94M

## what

CREATED_USER: GIS 89%, SHENDERSON 11%

LAST_EDITED_USER: GIS 90%, SHENDERSON 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 591 | 0 | 47361 3; 46721 3; 46402 3; 46083 3 |
| ADDRESS | other | 528 | 0 | 979 Crescent Ave 6; 966 West Paces Ferry Road 5; 1800 Piedmont Rd NE 5; 1000 Marietta St NW 5 |
| APPR_DATE | date | 61 | 18 | nan 491; 07/05/07 7; 08/26/08 5; 02/12/08 5 |
| APPSTATUS | who | 1 | 0 | Approved 598 |
| CREATED_DATE | date | 178 | 0 | 1524578745000 417; 1654787132000 3; 1777994550000 1; 1773085442000 1 |
| CREATED_USER | category | 2 | 0 | GIS 533; SHENDERSON 65 |
| DATE_APP | date | 281 | 0 | nan 79; 1566950400000.0 7; 1573603200000.0 7; 1481673600000.0 7 |
| GRANTEE | who | 503 | 0 | nan 31; Pace Academy 5; Heritage Preparatory Scho 5; Jaycee Development LLC 5 |
| LAST_EDITED_DATE | date | 195 | 0 | 1524579175000 260; 1524579174000 144; 1654787132000 2; 1777994701000 1 |
| LAST_EDITED_USER | category | 2 | 0 | GIS 537; SHENDERSON 61 |
| ORDINANCE | other | 509 | 0 | nan 77; 21-O-0392 5; 24-O-1026 4; 19-O-1031 4 |
| SUP_DOCKET | other | 554 | 2 | nan 34; observed 6; U-18-037 4; U-21-010 4 |
| SUP_TYPE | other | 53 | 0 | PCH 80; DCC 76; CHU 54; PVS 46 |
| GLOBALID | other | 599 | 0 | {F2A9AFC4-5A31-4C7D-A34F- 3; {C89D7AEF-7155-4C9F-8B6F- 3; {4712E3EE-03D4-4DBE-92D2- 3; {5A142420-91C3-4C89-8113- 3 |
| SHAPE_AREA | amount | 533 | 0 | 37125.7658595733 7; 787623.107444146 5; 137800.686807133 5; 207387.062039194 5 |
| SHAPE_LEN | amount | 532 | 0 | 821.955825729266 7; 5389.2646866807 5; 1794.1229974372002 5; 1878.1360322445 5 |
| GEOMETRY | other | 541 | 0 | {"type": "Polygon", "coor 7; {"type": "Polygon", "coor 5; {"type": "Polygon", "coor 5; {"type": "Polygon", "coor 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:51:19.19300 598 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9e04c4c4-4b89-45e2-9950-b 598 |
| SRC_SHA256 | who | 1 | 0 | 5cf649aee63edd2a98c27010f 598 |
