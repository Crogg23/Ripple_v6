# PORTAL_ARC_ATLANTA_DATAATLA_3E1237B0E9

rows 128  columns 20  scan 3.4s

roles: amount 2, audit 2, category 4, date 5, other 5, who 3

## when

APPR_DATE
  2001         4  ####################
  2002         3  ###############
  2003         3  ###############
  2005         6  ##############################
  2006         2  ##########
  2007         4  ####################
  2008         1  #####
  2009         4  ####################

CREATED_DATE
  2018       115  ##############################
  2020         1  
  2021         2  #
  2022         2  #
  2023         3  #
  2024         3  #
  2026         2  #

DATE_APP
  1985         2  ##########
  1987         3  ###############
  1991         1  #####
  1992         1  #####
  1993         3  ###############
  1995         2  ##########
  1996         5  #########################
  1998         1  #####
  2001         4  ####################
  2002         3  ###############
  2003         3  ###############
  2004         1  #####
  2005         6  ##############################
  2006         3  ###############
  2007         4  ####################
  2008         4  ####################
  2009         3  ###############
  2010         3  ###############
  2011         3  ###############
  2012         2  ##########
  2013         1  #####
  2014         2  ##########
  2015         2  ##########
  2016         1  #####
  2017         1  #####
  2018         5  #########################
  2019         1  #####
  2021         1  #####
  2022         1  #####
  2023         4  ####################
  2024         1  #####
  2025         1  #####

LAST_EDITED_DATE
  2018       114  ##############################
  2019         1  
  2021         2  #
  2022         1  
  2023         4  #
  2024         3  #
  2025         1  
  2026         2  #

INGESTED_AT
  2026       128  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_AREA | 128 | 4.8K | 27.0K | 722.3K | 1.09M | 12.06M |
| SHAPE_LEN | 128 | 283.66 | 738.81 | 3.7K | 6.2K | 142.8K |

## who

GRANTEE by rows
         7  nan
         2  Mary F. Knight Bagwell
         2  Salvation Army
         2  Valerie D. Cater
         2  Canterbury Court
         1  Paula & Willie Moss
         1  West End Group Home: from DHR list (Jan 2011)
         1  Brighton Gardens: from DHR list (January 2011)
         1  Betty's PCH: from DHR list (January 2011)
         1  Charles Serge (exp. 7/20/2012)
         1  Elvin Mitchell, Sr.
         1  Angel Youth Foundation
         1  Kathryn Bell
         1  OV'S PCH: from DHR list (January 2011)
         1  Keeping It Realty LLC
         1  Rosa Wesley
         1  Lucile P. Fears
         1  Ike Pascal
         1  Ruby Newsome
         1  Villas of Hope

GRANTEE by dollars
       1.10M        2 rows  Canterbury Court
       1.09M        1 rows  Quality Care PCH: from DHR list (January 2011)
      740.1K        1 rows  Isakonson/Barnhart Development
      674.5K        1 rows  Ivory Young
      555.0K        7 rows  nan
      476.7K        1 rows  Canterbury Court: from DHR list (January 2011)
      452.4K        1 rows  Wm Bremman: from DHR list (January 2011)
      383.8K        1 rows  Village Park Paces LLC
      365.6K        1 rows  City of Refuge
      341.6K        1 rows  Trinity Presby. Church
      341.2K        1 rows  Hillside INC
      252.4K        1 rows  Sunrise: from DHR list (January 2011)
      244.8K        1 rows  Dr. Julius M. Willis
      240.2K        1 rows  Reliable Health & Rehab: from DHR (Jan 2011)
      217.0K        1 rows  Brighton Gardens: from DHR list (January 2011)
      188.0K        1 rows  Westminster Presbyterian Homes
      179.8K        1 rows  Victory Outreach Church
      176.0K        1 rows  Campbell-Stone
      170.4K        1 rows  Heritage Healthcare: from DHR list (January 2011)
      157.6K        1 rows  Our Lady of Perpetual Help: DHR list (Jan 2011)

ORDINANCE by rows
        60  nan
         1  18-O-1007
         1  05-O-1115
         1  11-O-1590
         1  85-O-1244
         1  18-O-1022
         1  09-O-0845
         1  18-O-1343
         1  18-O-1440
         1  04-O-1842
         1  87-O-1157
         1  07-O-1541
         1  05-O-1311
         1  01-O-1519
         1  20-O-1724
         1  00-O-1448
         1  18-O-1705
         1  25-O-1327
         1  05-O-1942
         1  96-O-0068

ORDINANCE by dollars
       6.60M       60 rows  nan
      740.1K        1 rows  04-O-1842
      551.2K        1 rows  18-O-1705
      383.8K        1 rows  18-O-1007
      341.2K        1 rows  09-O-0845
      341.2K        1 rows  24-O-1026
      244.8K        1 rows  04-O-2082
      188.0K        1 rows  02-O-1993
      148.3K        1 rows  08-O-1143
      144.9K        1 rows  01-O-0903
      125.3K        1 rows  96-O-0068
      108.9K        1 rows  07-O-0633
      108.7K        1 rows  08-O-1146
      106.7K        1 rows  01-O-1519
       96.3K        1 rows  09-O-0508
       93.8K        1 rows  23-O-1055
       93.4K        1 rows  18-O-1440
       87.6K        1 rows  18-O-1011
       86.7K        1 rows  04-O-0361
       84.6K        1 rows  06-O-2257

SRC_SHA256 by rows
       128  74d94511064bb6fc469a87595fc76e169f4d3f48582fa745ed97505098fd99a6

SRC_SHA256 by dollars
      12.06M      128 rows  74d94511064bb6fc469a87595fc76e169f4d3f48582fa745ed97505098fd

## who x when

GRANTEE by DATE_APP, dollars = SHAPE_AREA
  Angel Youth Foundation                    2023:12.8K
  Canterbury Court                          2019:551.2K
  Charles Serge (exp. 7/20/2012)            2009:5.2K
  Elvin Mitchell, Sr.                       1996:12.1K
  Hillside INC                              2024:341.2K
  Ike Pascal                                2015:16.1K
  Isakonson/Barnhart Development            2005:740.1K
  Ivory Young                               2010:674.5K
  Kathryn Bell                              1996:42.0K
  Keeping It Realty LLC                     2018:6.1K
  Lucile P. Fears                           2001:11.8K
  Mary F. Knight Bagwell                    1996:63.2K 2014:63.2K
  Paula & Willie Moss                       2007:8.3K
  Rosa Wesley                               1995:12.2K
  Ruby Newsome                              1985:11.2K
  Salvation Army                            2003:57.8K 2023:57.8K
  Trinity Presby. Church                    2002:341.6K
  Valerie D. Cater                          2006:23.8K 2023:23.8K
  Village Park Paces LLC                    2018:383.8K
  nan                                       1993:27.5K 2009:341.2K 2011:58.7K 2012:103.4K

ORDINANCE by DATE_APP, dollars = SHAPE_AREA
  00-O-1448                                 2001:11.8K
  01-O-0903                                 2001:144.9K
  01-O-1519                                 2001:106.7K
  02-O-1993                                 2003:188.0K
  04-O-1842                                 2005:740.1K
  04-O-2082                                 2005:244.8K
  05-O-1115                                 2005:17.8K
  05-O-1311                                 2005:12.3K
  05-O-1942                                 2005:22.2K
  07-O-0633                                 2007:108.9K
  07-O-1541                                 2007:26.4K
  08-O-1143                                 2008:148.3K
  08-O-1146                                 2008:108.7K
  09-O-0508                                 2009:96.3K
  09-O-0845                                 2009:341.2K
  11-O-1590                                 2012:78.9K
  18-O-1007                                 2018:383.8K
  18-O-1011                                 2018:87.6K
  18-O-1022                                 2018:6.1K
  18-O-1343                                 2018:64.0K
  18-O-1440                                 2018:93.4K
  18-O-1705                                 2019:551.2K
  20-O-1724                                 2021:21.0K
  23-O-1055                                 2023:93.8K
  24-O-1026                                 2024:341.2K
  25-O-1327                                 2025:7.6K
  85-O-1244                                 1985:7.7K
  87-O-1157                                 1987:40.9K
  96-O-0068                                 1996:125.3K
  nan                                       1987:8.5K 1991:5.0K 1992:38.9K 1995:20.5K 1996:116.3K 1998:8.1K 2002:351.3K 2010:674.5K 2011:48.0K

## what

APPSTATUS: Approved 95%, New Application 5%

CREATED_USER: GIS 97%, SHENDERSON 3%

LAST_EDITED_USER: GIS 96%, SHENDERSON 4%

SUP_TYPE: PCH 66%, ALF 17%, NHM 10%, RHC 4%, SHF 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 126 | 0 | 48001 1; 45761 1; 35841 1; 35521 1 |
| ADDRESS | other | 120 | 0 | 3750 Peachtree RD NE 2; 540 Mobile Avenue 2; 690 Courtenay Drive 2; 2045 Graham Cir. 2 |
| APPR_DATE | date | 43 | 3 | nan 81; 7/13/09 2; 10/10/05 2; 06/03/85 2 |
| APPSTATUS | category | 2 | 0 | Approved 122; New Application 6 |
| CREATED_DATE | date | 17 | 0 | 1524578745000 112; 1781708970000 1; 1769026870000 1; 1720018549000 1 |
| CREATED_USER | category | 2 | 0 | GIS 124; SHENDERSON 4 |
| DATE_APP | date | 75 | 0 | nan 50; 1128902400000.0 2; 1156809600000.0 2; 486604800000.0 2 |
| GRANTEE | who | 119 | 0 | nan 7; Canterbury Court 2; Valerie D. Cater 2; Salvation Army 2 |
| LAST_EDITED_DATE | date | 19 | 0 | 1524579175000 63; 1524579174000 48; 1781709066000 1; 1769026959000 1 |
| LAST_EDITED_USER | category | 2 | 0 | GIS 123; SHENDERSON 5 |
| ORDINANCE | who | 69 | 0 | nan 60; 25-O-1327 1; 23-O-1492 1; 24-O-1026 1 |
| SUP_DOCKET | other | 91 | 2 | nan 33; observed 4; U-26-011 1; U-25-041 1 |
| SUP_TYPE | category | 5 | 0 | PCH 85; ALF 22; NHM 13; RHC 5 |
| GLOBALID | other | 128 | 0 | {ACA35968-FB38-4638-BC68- 1; {ECDAC5F0-1502-4E45-B9E1- 1; {CC98327B-17AA-4386-BBC2- 1; {18BBAB93-0E99-4DD3-973B- 1 |
| SHAPE_AREA | amount | 122 | 0 | 551156.40348022 2; 23795.0465358812 2; 341230.74316336797 2; 12193.5219972388 2 |
| SHAPE_LEN | amount | 121 | 0 | 3743.82357059106 2; 736.53081653836 2; 2338.6073337419602 2; 442.25742959947803 2 |
| GEOMETRY | other | 125 | 0 | {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:49:18.51630 128 |
| SOURCE_RUN_ID | audit | 1 | 0 | a14bc957-0ea5-4b30-aa5b-3 128 |
| SRC_SHA256 | who | 1 | 0 | 74d94511064bb6fc469a87595 128 |
