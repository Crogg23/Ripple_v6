# FED_FRA_CROSSING_INCIDENTS

rows 251.1K  columns 157  scan 8.1s

roles: amount 5, audit 2, category 101, date 1, empty 8, id 2, other 24, who 14

## when

DATE
  1975     12.1K  ###########################
  1976     13.2K  #############################
  1977     13.4K  ##############################
  1978     13.6K  ##############################
  1979     12.8K  ############################
  1980     10.8K  ########################
  1981      9.5K  #####################
  1982      7.9K  ##################
  1983      7.3K  ################
  1984      7.5K  ################
  1985      7.1K  ################
  1986      6.5K  ##############
  1987      6.4K  ##############
  1988      6.6K  ###############
  1989      6.5K  ##############
  1990      5.7K  #############
  1991      5.4K  ############
  1992      4.9K  ###########
  1993      4.9K  ###########
  1994      5.0K  ###########
  1995      4.6K  ##########
  1996      4.3K  #########
  1997      3.9K  #########
  1998      3.5K  ########
  1999      3.5K  ########
  2000      3.6K  ########
  2001      3.2K  #######
  2002      3.1K  #######
  2003      3.0K  #######
  2004      3.1K  #######
  2005      3.1K  #######
  2006      2.9K  #######
  2007      2.8K  ######
  2008      2.4K  #####
  2009      1.9K  ####
  2010      2.1K  #####
  2011      2.1K  #####
  2012      2.0K  ####
  2013      2.1K  #####
  2014      2.3K  #####
  2015      2.1K  #####
  2016      2.0K  #####
  2017      2.1K  #####
  2018      2.2K  #####
  2019      2.2K  #####
  2020      1.9K  ####
  2021      2.2K  #####
  2022      2.2K  #####
  2023      2.2K  #####
  2024      2.3K  #####
  2025      2.3K  #####
  2026       845  ##

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VEHICLE_DAMAGE_COST | 249.3K | 0 | 1.0K | 40.7K | 1.00M | 920.78M |
| TOTAL_KILLED_FORM_57 | 251.1K | 0 | 0 | 2 | 60 | 25.5K |
| TOTAL_INJURED_FORM_57 | 251.1K | 0 | 0 | 3 | 124 | 89.3K |
| TOTAL_KILLED_FORM_55A | 251.1K | 0 | 0 | 2 | 12 | 24.8K |
| TOTAL_INJURED_FORM_55A | 251.1K | 0 | 0 | 3 | 124 | 93.2K |

## who

HIGHWAY_NAME by rows
      7.7K  PRIVATE
      4.6K  PRIVATE CROSSING
      2.3K  COUNTY ROAD
      1.8K  MAIN STREET
      1.7K  MAIN ST
      1.4K  PRIVATE XING
      1.3K  COUNTY RD
       804  PRIVATE ROAD
       443  PUBLIC
       373  BROADWAY
       311  WASHINGTON ST
       297  4TH STREET
       254  WASHINGTON STREET
       252  WALNUT ST
       249  CENTRAL AVE
       240  3RD STREET
       239  7TH STREET
       218  4TH ST
       214  MARKET ST
       206  MAIN

HIGHWAY_NAME by dollars
         662     7.7K rows  PRIVATE
         372     4.6K rows  PRIVATE CROSSING
         359     2.3K rows  COUNTY ROAD
         233     1.8K rows  MAIN STREET
         188     1.7K rows  MAIN ST
         173     1.3K rows  COUNTY RD
          82     1.4K rows  PRIVATE XING
          72      804 rows  PRIVATE ROAD
          67        4 rows  STATE ROAD 54
          66      443 rows  PUBLIC
          41      373 rows  BROADWAY
          34      240 rows  3RD STREET
          33      249 rows  CENTRAL AVE
          31      111 rows  MILL STREET
          30      311 rows  WASHINGTON ST
          29      110 rows  COUNTY ROAD CROSSING
          29      206 rows  MAIN
          28      178 rows  COUNTY LINE ROAD
          28      134 rows  COUNTY
          27      297 rows  4TH STREET

TRACK_NAME by rows
     43.1K  MAIN
     42.7K  SINGLE MAIN TRACK
     36.1K  SINGLE MAIN
     12.0K  MAIN LINE
      7.0K  MAINLINE
      5.6K  MAIN TRACK
      2.1K  #1 MAIN
      2.0K  SINGLE MAIN LINE
      2.0K  YARD
      1.8K  #2 MAIN
      1.3K  INDUSTRY
      1.1K  WESTBOUND MAIN
      1.1K  EASTBOUND MAIN
       969  NO 1 MAIN
       876  NORTH MAIN
       874  1
       868  EAST MAIN
       866  WEST MAIN
       832  MAIN 1
       829  DOUBLE MAIN

TRACK_NAME by dollars
        4.8K    42.7K rows  SINGLE MAIN TRACK
        4.7K    43.1K rows  MAIN
        4.1K    36.1K rows  SINGLE MAIN
        1.2K    12.0K rows  MAIN LINE
         762     7.0K rows  MAINLINE
         674     5.6K rows  MAIN TRACK
         288     2.1K rows  #1 MAIN
         242     1.8K rows  #2 MAIN
         213     2.0K rows  SINGLE MAIN LINE
         166      866 rows  WEST MAIN
         165      868 rows  EAST MAIN
         163      874 rows  1
         148      829 rows  DOUBLE MAIN
         145      832 rows  MAIN 1
         135      378 rows  MAIN TRACK 1
         135     1.1K rows  EASTBOUND MAIN
         134      636 rows  MAIN 1 TRACK
         130     1.1K rows  WESTBOUND MAIN
         128      348 rows  MAIN TRACK 2
         126      805 rows  SOUTH MAIN

MAINTENANCE_RAILROAD_NAME by rows
     25.9K  Union Pacific Railroad Company
     21.0K  CSX Transportation
     15.0K  Norfolk Southern Railway Company
     14.9K  Conrail
     13.9K  Burlington Northern Railroad Company
     11.2K  BNSF Railway Company
      9.8K  Southern Pacific Transportation Company
      8.3K  Atchison, Topeka & Santa Fe Railway Company
      8.0K  Norfolk & Western Railway Company
      6.6K  Missouri Pacific Railroad Company
      6.5K  SOUTHERN RAILWAY COMPANY
      5.5K  Chicago And North Western Railway Company
      4.8K  Seaboard Coast Line Railroad
      4.7K  Illinois Central Gulf Railroad Company
      4.1K  Kansas City Southern Railway Company
      3.1K  Illinois Central Railroad Company
      3.1K  SOO Line Railroad Company
      3.0K  Louisville And Nashville Railroad Company
      2.8K  Baltimore And Ohio Railroad Company
      2.7K  CHESAPEAKE & OHIO RAILWAY CO.

MAINTENANCE_RAILROAD_NAME by dollars
        3.6K    25.9K rows  Union Pacific Railroad Company
        2.4K    21.0K rows  CSX Transportation
        1.8K    11.2K rows  BNSF Railway Company
        1.6K    13.9K rows  Burlington Northern Railroad Company
        1.5K    15.0K rows  Norfolk Southern Railway Company
        1.5K    14.9K rows  Conrail
         978     8.3K rows  Atchison, Topeka & Santa Fe Railway Company
         962     9.8K rows  Southern Pacific Transportation Company
         761     8.0K rows  Norfolk & Western Railway Company
         639     6.6K rows  Missouri Pacific Railroad Company
         468     6.5K rows  SOUTHERN RAILWAY COMPANY
         465     4.8K rows  Seaboard Coast Line Railroad
         417     5.5K rows  Chicago And North Western Railway Company
         387     3.1K rows  Illinois Central Railroad Company
         357     4.1K rows  Kansas City Southern Railway Company
         329     1.7K rows  Florida East Coast Railway Company
         306     4.7K rows  Illinois Central Gulf Railroad Company
         295     2.3K rows  GRAND TRUNK WESTERN RAILROAD INC.
         282     3.1K rows  SOO Line Railroad Company
         264     1.9K rows  ST. LOUIS SOUTHWESTERN RAILWAY CO.

RAILROAD_NAME by rows
     25.0K  Union Pacific Railroad Company
     19.6K  CSX Transportation
     15.5K  Conrail
     14.6K  Norfolk Southern Railway Company
     14.6K  Burlington Northern Railroad Company
     10.9K  Southern Pacific Transportation Company
     10.7K  BNSF Railway Company
      9.3K  Norfolk & Western Railway Company
      8.5K  Atchison, Topeka & Santa Fe Railway Company
      8.3K  Amtrak (National Railroad Passenger Corporation)
      7.5K  Missouri Pacific Railroad Company
      7.1K  SOUTHERN RAILWAY COMPANY
      6.5K  Chicago And North Western Railway Company
      5.8K  Seaboard Coast Line Railroad
      5.6K  Illinois Central Gulf Railroad Company
      4.3K  Kansas City Southern Railway Company
      4.1K  Louisville And Nashville Railroad Company
      3.5K  SOO Line Railroad Company
      3.2K  Baltimore And Ohio Railroad Company
      3.1K  Chicago, Milwaukee, St. Paul & Pacific Railroad

RAILROAD_NAME by dollars
        3.2K    25.0K rows  Union Pacific Railroad Company
        2.2K     8.3K rows  Amtrak (National Railroad Passenger Corporation)
        2.0K    19.6K rows  CSX Transportation
        1.7K    14.6K rows  Burlington Northern Railroad Company
        1.5K    10.7K rows  BNSF Railway Company
        1.5K    15.5K rows  Conrail
        1.4K    14.6K rows  Norfolk Southern Railway Company
         992    10.9K rows  Southern Pacific Transportation Company
         966     8.5K rows  Atchison, Topeka & Santa Fe Railway Company
         897     9.3K rows  Norfolk & Western Railway Company
         727     7.5K rows  Missouri Pacific Railroad Company
         637     5.8K rows  Seaboard Coast Line Railroad
         517     7.1K rows  SOUTHERN RAILWAY COMPANY
         481     6.5K rows  Chicago And North Western Railway Company
         388     5.6K rows  Illinois Central Gulf Railroad Company
         365     4.3K rows  Kansas City Southern Railway Company
         314     2.3K rows  ST. LOUIS SOUTHWESTERN RAILWAY CO.
         300     2.5K rows  GRAND TRUNK WESTERN RAILROAD INC.
         291     4.1K rows  Louisville And Nashville Railroad Company
         285     3.5K rows  SOO Line Railroad Company

## who x when

HIGHWAY_NAME by DATE, dollars = TOTAL_KILLED_FORM_57
  3RD STREET                                1975:0 1976:1 1977:2 1978:0 1979:0 1980:1 1981:0 1982:1 1983:0 1984:0 1985:0 1986:0 1987:0 1988:0 1989:1 1990:0 1991:2 1992:2 1993:1 1994:1 1995:2 1996:3 1997:1 1998:1 1999:0 2000:0 2001:4 2003:0 2004:1 2005:0 2006:0 2007:1 2008:0 2009:0 2010:1 2013:0 2014:0 2015:0 2017:2 2019:0 2020:1 2021:1 2022:1 2023:2 2024:0 2025:1
  4TH ST                                    1975:0 1976:0 1977:1 1978:0 1979:0 1980:1 1981:1 1982:2 1983:0 1984:3 1985:0 1986:2 1987:1 1988:1 1989:0 1990:0 1992:0 1993:0 1994:0 1995:0 1996:0 1999:0 2000:0 2003:1 2006:0 2007:1 2010:1 2011:0 2012:1 2013:2 2014:0 2016:0 2017:1 2020:0 2021:0 2024:0 2025:0
  4TH STREET                                1975:0 1976:0 1977:0 1978:0 1979:0 1980:0 1981:0 1982:1 1983:0 1984:2 1985:0 1986:0 1987:1 1988:0 1989:0 1990:2 1991:2 1992:1 1993:0 1994:0 1995:0 1996:3 1997:3 1998:0 1999:0 2000:0 2001:2 2002:1 2003:4 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:1 2012:0 2013:1 2014:1 2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:1 2022:1 2024:0 2025:0
  7TH STREET                                1975:0 1976:1 1977:1 1978:0 1979:0 1980:1 1981:0 1982:2 1983:0 1984:0 1985:1 1986:0 1987:0 1988:0 1989:2 1990:0 1991:0 1992:0 1993:1 1994:0 1995:1 1996:0 1997:1 1998:0 1999:0 2000:1 2001:0 2002:0 2003:1 2004:1 2005:0 2006:0 2007:0 2009:0 2011:0 2013:1 2014:1 2017:1 2018:0 2020:1 2021:0 2022:0 2023:0 2025:1 2026:0
  BROADWAY                                  1975:2 1976:5 1977:1 1978:3 1979:2 1980:0 1981:0 1982:6 1983:0 1984:0 1985:2 1986:2 1987:0 1988:0 1989:0 1990:0 1991:0 1992:1 1993:0 1994:1 1995:0 1996:3 1997:1 1998:0 1999:0 2000:0 2001:1 2002:0 2003:1 2005:0 2006:1 2007:1 2008:3 2010:1 2011:1 2012:1 2013:0 2015:0 2016:0 2017:0 2018:0 2019:1 2020:0 2021:1 2022:0 2023:0 2024:0 2025:0
  CENTRAL AVE                               1975:1 1976:1 1977:1 1978:1 1979:2 1980:0 1981:0 1982:0 1983:0 1984:1 1985:1 1986:2 1987:0 1988:3 1989:0 1990:0 1991:0 1992:0 1993:1 1994:0 1995:0 1996:1 1997:1 1998:0 1999:0 2000:0 2001:1 2004:1 2005:0 2006:0 2010:0 2011:4 2012:1 2014:0 2016:1 2018:1 2019:0 2020:0 2021:2 2022:4 2023:0 2024:0 2025:2
  COUNTY                                    1975:2 1976:1 1977:0 1978:0 1979:0 1980:0 1981:2 1982:0 1983:0 1984:2 1985:0 1986:0 1987:4 1988:1 1989:0 1990:7 1991:2 1992:1 1993:0 1994:0 1995:0 1996:2 1997:1 1998:0 1999:0 2000:2 2002:0 2003:0 2004:0 2008:0 2009:0 2010:0 2011:0 2014:0 2017:1
  COUNTY LINE ROAD                          1975:3 1976:2 1977:2 1978:2 1979:0 1980:1 1981:0 1982:3 1983:1 1984:0 1985:0 1986:0 1987:0 1989:3 1990:2 1992:0 1993:0 1994:4 1995:0 1996:0 1997:0 1998:0 1999:0 2000:3 2001:0 2002:0 2004:0 2005:0 2007:1 2008:0 2010:0 2011:0 2012:0 2015:0 2021:1 2023:0 2025:0
  COUNTY RD                                 1975:0 1976:0 1977:1 1978:2 1979:9 1980:18 1981:12 1982:17 1983:21 1984:10 1985:10 1986:18 1987:9 1988:10 1989:6 1990:2 1991:10 1992:1 1993:2 1994:3 1995:2 1996:6 1997:0 1998:0 1999:0 2000:0 2001:0 2003:0 2004:0 2005:2 2006:0 2007:0 2008:0 2009:0 2010:1 2011:1 2012:0 2013:0 2014:0 2024:0 2025:0
  COUNTY ROAD                               1975:27 1976:40 1977:36 1978:23 1979:5 1980:2 1981:8 1982:4 1983:1 1984:15 1985:4 1986:1 1987:0 1988:7 1989:16 1990:15 1991:2 1992:15 1993:14 1994:28 1995:15 1996:5 1997:11 1998:3 1999:5 2000:2 2001:4 2002:5 2003:6 2004:2 2005:5 2006:3 2007:2 2008:2 2009:1 2010:6 2011:2 2012:1 2013:1 2014:4 2015:3 2016:0 2017:0 2018:1 2019:2 2020:0 2021:0 2022:3 2023:0 2024:1 2025:0 2026:1
  COUNTY ROAD CROSSING                      1975:6 1976:6 1977:9 1978:6 1980:0 1981:1 1982:1 1983:0 1984:0
  MAIN                                      1975:0 1976:0 1977:0 1978:3 1979:1 1980:1 1981:2 1982:0 1983:0 1984:1 1985:0 1986:0 1987:0 1988:2 1989:0 1990:0 1991:4 1992:3 1993:0 1994:0 1995:0 1996:2 1997:0 1998:1 1999:0 2000:0 2001:2 2002:1 2003:0 2004:3 2005:0 2006:0 2007:0 2008:2 2009:1 2010:0 2011:0 2012:0 2014:0 2015:0 2016:0 2017:0 2018:0 2022:0 2024:0 2025:0 2026:0
  MAIN ST                                   1975:4 1976:4 1977:2 1978:4 1979:14 1980:12 1981:7 1982:5 1983:6 1984:10 1985:4 1986:9 1987:21 1988:4 1989:1 1990:4 1991:13 1992:2 1993:0 1994:2 1995:1 1996:0 1997:3 1998:0 1999:1 2000:0 2001:0 2002:2 2003:2 2004:4 2005:2 2006:5 2007:3 2008:3 2009:1 2010:0 2011:3 2012:1 2013:0 2014:3 2015:0 2016:3 2017:4 2018:0 2019:4 2020:2 2021:2 2022:1 2023:4 2024:1 2025:5 2026:0
  MAIN STREET                               1975:12 1976:29 1977:24 1978:11 1979:4 1980:1 1981:7 1982:1 1983:3 1984:7 1985:2 1986:1 1987:1 1988:1 1989:11 1990:3 1991:1 1992:5 1993:10 1994:5 1995:5 1996:3 1997:1 1998:5 1999:9 2000:2 2001:2 2002:2 2003:3 2004:4 2005:5 2006:4 2007:0 2008:0 2009:3 2010:4 2011:4 2012:2 2013:2 2014:6 2015:4 2016:0 2017:7 2018:2 2019:3 2020:4 2021:3 2022:2 2023:1 2024:1 2025:1 2026:0
  MARKET ST                                 1975:2 1976:0 1977:1 1978:0 1979:1 1980:2 1981:0 1982:3 1983:1 1984:0 1985:1 1986:1 1987:0 1988:0 1989:0 1990:0 1991:1 1992:1 1993:1 1994:1 1995:0 1996:0 1997:0 1998:0 1999:0 2000:0 2001:0 2003:0 2004:0 2005:1 2006:0 2007:0 2008:1 2009:0 2011:2 2012:0 2013:0 2015:1 2019:0 2023:0 2024:0 2025:1
  MILL STREET                               1975:22 1976:0 1977:1 1978:0 1979:0 1980:1 1981:1 1982:0 1983:1 1984:2 1985:0 1989:0 1990:0 1991:0 1992:0 1993:0 1995:0 1996:0 1997:0 1998:0 1999:0 2001:0 2002:0 2004:1 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2013:0 2015:1 2016:0 2018:0 2019:0 2021:1 2023:0
  PRIVATE                                   1975:29 1976:14 1977:9 1978:12 1979:14 1980:18 1981:7 1982:1 1983:1 1984:8 1985:12 1986:6 1987:2 1988:1 1989:8 1990:17 1991:3 1992:16 1993:17 1994:22 1995:13 1996:13 1997:12 1998:19 1999:15 2000:14 2001:9 2002:22 2003:12 2004:20 2005:14 2006:14 2007:17 2008:8 2009:11 2010:15 2011:11 2012:11 2013:7 2014:14 2015:13 2016:9 2017:11 2018:14 2019:17 2020:14 2021:11 2022:16 2023:25 2024:21 2025:19 2026:4
  PRIVATE CROSSING                          1975:24 1976:11 1977:22 1978:17 1979:3 1980:4 1981:4 1982:7 1983:11 1984:15 1985:14 1986:9 1987:8 1988:31 1989:26 1990:24 1991:24 1992:10 1993:11 1994:7 1995:12 1996:5 1997:12 1998:2 1999:3 2000:4 2001:0 2002:1 2003:1 2004:2 2005:3 2006:2 2007:3 2008:2 2009:1 2010:4 2011:1 2012:3 2013:8 2014:2 2015:3 2016:9 2017:3 2018:1 2019:1 2020:2 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  PRIVATE ROAD                              1975:0 1976:2 1977:0 1978:0 1980:0 1981:0 1982:0 1984:1 1985:0 1986:0 1988:0 1989:1 1990:0 1991:0 1992:3 1993:1 1994:0 1995:0 1996:0 1997:0 1998:1 1999:1 2000:2 2001:2 2002:1 2003:1 2004:2 2005:3 2006:3 2007:3 2008:3 2009:0 2010:4 2011:3 2012:6 2013:4 2014:2 2015:3 2016:3 2017:1 2018:1 2019:3 2020:1 2021:2 2022:1 2023:1 2024:3 2025:2 2026:2
  PRIVATE XING                              1975:0 1976:0 1977:0 1978:1 1979:14 1980:9 1981:12 1982:11 1983:16 1984:1 1985:0 1986:4 1987:4 1988:0 1989:0 1990:0 1991:0 1992:0 1993:3 1994:2 1995:1 1996:4 1997:0 1998:0 2000:0 2001:0 2002:0 2003:0 2004:0 2005:0 2006:0 2008:0 2012:0 2013:0 2016:0 2017:0 2018:0 2019:0 2020:0
  PUBLIC                                    1975:0 1977:0 1978:4 1979:3 1980:0 1981:0 1982:1 1983:0 1984:0 1985:0 1986:0 1987:5 1988:3 1989:2 1990:2 1991:1 1992:1 1993:0 1994:2 1995:0 1996:0 1997:0 1998:2 1999:1 2000:1 2001:3 2002:1 2003:2 2004:3 2005:10 2006:3 2007:3 2008:3 2009:5 2010:3 2011:1 2012:0 2013:0 2014:0 2016:0 2017:1 2020:0 2021:0 2022:0
  STATE ROAD 54                             1976:67
  WALNUT ST                                 1975:1 1976:0 1977:0 1978:0 1979:3 1980:4 1981:1 1982:0 1983:0 1984:1 1985:0 1986:2 1987:1 1988:5 1989:1 1990:0 1991:0 1992:0 1993:0 1994:0 1995:1 1996:0 1998:0 1999:0 2000:1 2001:0 2002:0 2003:0 2005:1 2006:1 2008:0 2010:0 2012:0 2015:0 2017:0 2018:0 2019:0 2020:1 2022:0 2023:0 2024:1 2025:0 2026:0
  WASHINGTON ST                             1975:0 1976:0 1977:4 1978:0 1979:0 1980:0 1981:0 1982:1 1983:0 1984:1 1985:0 1986:0 1987:0 1988:3 1989:1 1990:3 1991:0 1992:0 1993:1 1994:0 1995:0 1996:0 1997:0 1998:1 1999:0 2000:1 2001:0 2002:0 2003:1 2004:1 2005:1 2006:0 2007:1 2008:0 2009:0 2011:1 2012:1 2013:1 2014:0 2015:0 2016:0 2017:0 2018:2 2019:1 2020:2 2021:1 2022:0 2023:0 2025:1 2026:0
  WASHINGTON STREET                         1975:0 1976:1 1977:1 1978:0 1979:0 1980:0 1981:2 1982:0 1983:0 1984:1 1985:0 1989:0 1990:1 1991:0 1992:0 1993:1 1994:3 1995:0 1996:0 1997:0 1998:0 1999:0 2000:0 2001:1 2002:0 2003:0 2004:1 2005:1 2006:0 2007:2 2008:1 2009:0 2010:0 2011:1 2012:0 2013:0 2014:0 2015:2 2016:0 2017:0 2018:1 2019:0 2020:1 2021:0 2022:0 2023:2 2025:0 2026:0

TRACK_NAME by DATE, dollars = TOTAL_KILLED_FORM_57
  #1 MAIN                                   1975:5 1976:14 1977:11 1978:14 1979:12 1980:9 1981:4 1982:8 1983:13 1984:11 1985:17 1986:12 1987:6 1988:6 1989:17 1990:5 1991:2 1992:2 1993:7 1994:1 1995:2 1996:0 1997:5 1998:3 1999:2 2000:3 2001:1 2002:0 2003:1 2004:6 2005:2 2006:2 2007:13 2008:6 2009:1 2010:1 2011:5 2012:6 2013:7 2014:5 2015:8 2016:2 2017:8 2018:4 2019:7 2020:2 2021:4 2022:1 2023:3 2024:2 2025:0 2026:0
  #2 MAIN                                   1975:9 1976:23 1977:3 1978:8 1979:7 1980:11 1981:3 1982:16 1983:13 1984:6 1985:11 1986:5 1987:7 1988:2 1989:10 1990:5 1991:4 1992:4 1993:4 1994:2 1995:7 1996:0 1997:8 1998:2 1999:0 2000:1 2001:0 2002:2 2003:2 2004:0 2005:5 2006:5 2007:4 2008:2 2009:1 2010:1 2011:7 2012:2 2013:4 2014:6 2015:6 2016:4 2017:3 2018:5 2019:2 2020:2 2021:2 2022:1 2023:2 2024:2 2025:1 2026:0
  1                                         1975:27 1976:2 1977:3 1978:7 1979:5 1980:4 1981:0 1982:1 1983:1 1984:3 1985:5 1986:0 1987:4 1988:5 1989:4 1990:1 1991:1 1992:0 1993:3 1994:1 1995:0 1996:1 1997:1 1998:0 1999:2 2000:2 2001:3 2002:4 2003:3 2004:1 2005:1 2006:4 2007:3 2008:0 2009:1 2010:6 2011:6 2012:2 2013:5 2014:0 2015:1 2016:6 2017:6 2018:3 2019:4 2020:7 2021:1 2022:3 2023:2 2024:1 2025:5 2026:2
  DOUBLE MAIN                               1975:0 1976:8 1977:10 1978:18 1979:25 1980:15 1981:23 1982:10 1983:7 1984:6 1985:0 1986:1 1987:0 1988:3 1989:2 1990:4 1991:1 1994:0 1995:1 1996:1 1997:0 1998:0 2000:0 2002:0 2003:1 2004:0 2005:1 2007:1 2008:2 2009:6 2012:0 2015:1 2018:0 2019:1 2025:0
  EAST MAIN                                 1975:6 1976:2 1977:2 1978:1 1979:1 1980:0 1981:0 1982:0 1983:2 1984:0 1985:0 1986:2 1987:4 1988:1 1989:8 1990:4 1991:6 1992:10 1993:15 1994:14 1995:7 1996:5 1997:8 1998:2 1999:6 2000:5 2001:3 2002:2 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:1 2011:0 2012:0 2013:1 2015:0 2016:0 2017:0 2018:2 2019:3 2020:1 2021:3 2022:10 2023:6 2024:13 2025:5 2026:4
  EASTBOUND MAIN                            1975:33 1976:10 1977:6 1978:9 1979:1 1980:2 1981:11 1982:5 1983:2 1984:1 1985:4 1986:3 1987:4 1988:6 1989:10 1990:3 1991:4 1992:1 1993:3 1994:6 1995:3 1996:0 1997:3 1998:2 1999:0 2000:0 2001:0 2002:0 2003:1 2004:1 2006:0 2007:0 2009:1 2010:0 2012:0
  INDUSTRY                                  1975:0 1976:0 1977:0 1978:0 1979:0 1980:0 1981:0 1982:0 1983:2 1984:0 1985:0 1986:1 1987:0 1988:0 1989:0 1990:0 1991:0 1992:0 1993:0 1994:0 1995:0 1996:1 1997:4 1998:0 1999:6 2000:1 2001:2 2002:0 2003:2 2004:0 2005:3 2006:1 2007:3 2008:0 2009:0 2010:0 2011:0 2012:0 2013:0 2014:0 2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  MAIN                                      1975:152 1976:141 1977:147 1978:158 1979:140 1980:134 1981:152 1982:110 1983:111 1984:165 1985:156 1986:171 1987:172 1988:197 1989:193 1990:210 1991:139 1992:113 1993:128 1994:91 1995:135 1996:143 1997:181 1998:203 1999:166 2000:117 2001:121 2002:108 2003:82 2004:74 2005:106 2006:87 2007:41 2008:29 2009:20 2010:7 2011:4 2012:7 2013:8 2014:5 2015:9 2016:8 2017:5 2018:8 2019:5 2020:7 2021:7 2022:4 2023:4 2024:2 2025:12 2026:1
  MAIN 1                                    1975:0 1976:1 1977:1 1978:0 1979:1 1980:0 1981:2 1982:0 1984:0 1985:0 1986:0 1987:0 1988:0 1989:0 1990:0 1991:2 1992:2 1993:0 1994:3 1995:2 1996:1 1997:0 1998:2 1999:1 2000:3 2001:0 2002:4 2003:0 2004:0 2005:2 2006:3 2007:6 2008:11 2009:0 2010:4 2011:6 2012:2 2013:9 2014:5 2015:9 2016:13 2017:6 2018:16 2019:14 2020:8 2021:1 2022:1 2023:0 2024:1 2025:3 2026:0
  MAIN 1 TRACK                              2004:0 2008:0 2009:2 2010:3 2011:8 2012:3 2013:10 2014:6 2015:8 2016:14 2017:6 2018:10 2019:5 2020:8 2021:16 2022:7 2023:8 2024:10 2025:6 2026:4
  MAIN LINE                                 1975:40 1976:139 1977:67 1978:62 1979:49 1980:52 1981:61 1982:46 1983:54 1984:40 1985:18 1986:20 1987:39 1988:51 1989:42 1990:28 1991:32 1992:28 1993:81 1994:46 1995:24 1996:16 1997:9 1998:11 1999:9 2000:31 2001:30 2002:8 2003:6 2004:14 2005:2 2006:13 2007:5 2008:2 2009:4 2010:0 2011:2 2012:0 2013:1 2014:0 2015:10 2016:11 2017:1 2018:1 2019:2 2020:0 2021:1 2022:0 2023:0 2024:0 2025:0 2026:1
  MAIN TRACK                                1975:54 1976:68 1977:51 1978:29 1979:48 1980:23 1981:8 1982:4 1983:7 1984:26 1985:10 1986:15 1987:9 1988:20 1989:25 1990:21 1991:21 1992:16 1993:11 1994:7 1995:10 1996:9 1997:2 1998:3 1999:2 2000:7 2001:10 2002:9 2003:9 2004:8 2005:7 2006:6 2007:6 2008:6 2009:6 2010:2 2011:0 2012:0 2013:5 2014:2 2015:9 2016:13 2017:1 2018:1 2019:2 2020:2 2021:7 2022:7 2023:10 2024:17 2025:18 2026:5
  MAIN TRACK 1                              1975:0 1976:0 1977:1 1978:0 1980:0 1989:0 1990:0 1991:0 1992:4 1993:1 1994:3 1996:1 2000:0 2003:1 2004:3 2005:0 2006:0 2007:2 2008:1 2009:8 2010:6 2011:2 2012:5 2013:5 2014:1 2015:6 2016:4 2017:1 2018:4 2019:5 2020:2 2021:12 2022:10 2023:13 2024:17 2025:12 2026:5
  MAIN TRACK 2                              1975:1 1976:0 1977:1 1978:0 1981:0 1982:0 1988:1 1990:1 1992:0 1993:0 1994:0 1999:0 2002:0 2003:0 2004:3 2005:0 2006:1 2007:0 2008:3 2009:9 2010:4 2011:4 2012:11 2013:8 2014:1 2015:6 2016:5 2017:6 2018:3 2019:4 2020:2 2021:5 2022:12 2023:9 2024:11 2025:9 2026:8
  MAINLINE                                  1975:5 1976:7 1977:7 1978:16 1979:11 1980:21 1981:16 1982:13 1983:6 1984:26 1985:35 1986:69 1987:57 1988:17 1989:35 1990:34 1991:35 1992:29 1993:22 1994:29 1995:33 1996:26 1997:21 1998:11 1999:22 2000:22 2001:9 2002:13 2003:16 2004:23 2005:25 2006:20 2007:11 2008:1 2009:1 2010:0 2011:1 2012:1 2013:0 2014:1 2015:2 2016:0 2017:0 2018:0 2019:5 2020:2 2021:1 2022:1 2023:0 2024:1 2025:2 2026:1
  NO 1 MAIN                                 1975:9 1976:10 1977:4 1978:5 1979:6 1980:10 1981:2 1982:4 1983:0 1984:0 1985:0 1986:0 1987:2 1988:0 1989:1 1990:1 1991:0 1993:1 1994:0 1995:0 1996:1 1997:0 1998:6 1999:3 2000:5 2001:1 2002:2 2003:5 2004:6 2005:9 2006:7 2007:4 2008:3 2009:0 2010:0 2011:2 2013:0 2014:1 2015:2 2016:0
  NORTH MAIN                                1975:1 1976:8 1977:3 1978:3 1979:1 1980:5 1981:5 1982:0 1983:6 1984:1 1985:0 1986:3 1987:0 1988:2 1989:0 1990:4 1991:3 1992:2 1993:5 1994:19 1995:11 1996:11 1997:4 1998:9 1999:3 2000:5 2001:4 2002:1 2003:3 2004:0 2005:0 2008:0 2009:0 2017:0
  SINGLE MAIN                               1975:93 1976:160 1977:163 1978:108 1979:94 1980:102 1981:117 1982:155 1983:163 1984:54 1985:47 1986:51 1987:28 1988:51 1989:51 1990:26 1991:91 1992:113 1993:98 1994:109 1995:72 1996:97 1997:127 1998:105 1999:99 2000:114 2001:94 2002:82 2003:103 2004:104 2005:75 2006:112 2007:115 2008:85 2009:61 2010:101 2011:60 2012:108 2013:83 2014:106 2015:77 2016:78 2017:84 2018:36 2019:29 2020:11 2021:6 2022:6 2023:5 2024:1 2025:4 2026:0
  SINGLE MAIN LINE                          1975:14 1976:39 1977:35 1978:18 1979:22 1980:11 1981:8 1982:16 1983:9 1984:0 1985:2 1986:2 1987:3 1988:9 1989:1 1990:0 1991:2 1992:0 1993:1 1994:6 1995:5 1996:1 1997:0 1998:0 1999:0 2000:0 2001:0 2003:0 2004:0 2005:0 2006:3 2007:0 2008:0 2009:1 2010:0 2011:0 2012:2 2013:0 2014:0 2015:0 2016:0 2017:0 2018:1 2019:0 2020:0 2021:0 2022:0 2023:0 2024:1 2025:1
  SINGLE MAIN TRACK                         1975:227 1976:252 1977:215 1978:254 1979:181 1980:175 1981:100 1982:47 1983:38 1984:148 1985:130 1986:74 1987:117 1988:115 1989:135 1990:130 1991:74 1992:83 1993:73 1994:110 1995:132 1996:86 1997:8 1998:8 1999:8 2000:9 2001:12 2002:8 2003:7 2004:2 2005:30 2006:30 2007:36 2008:65 2009:48 2010:58 2011:53 2012:49 2013:50 2014:86 2015:54 2016:47 2017:87 2018:119 2019:130 2020:102 2021:114 2022:142 2023:135 2024:146 2025:150 2026:64
  SOUTH MAIN                                1975:2 1976:1 1977:8 1978:3 1979:1 1980:1 1981:1 1982:2 1983:0 1984:0 1985:0 1986:0 1987:0 1988:2 1989:0 1990:1 1991:3 1992:9 1993:9 1994:16 1995:9 1996:13 1997:8 1998:10 1999:9 2000:5 2001:7 2002:2 2003:3 2004:1 2006:0 2007:0
  WEST MAIN                                 1975:3 1976:1 1977:1 1978:0 1979:1 1980:0 1981:1 1982:2 1983:1 1984:1 1985:0 1986:0 1987:2 1988:3 1989:0 1990:1 1991:6 1992:11 1993:14 1994:13 1995:5 1996:5 1997:5 1998:14 1999:9 2000:3 2001:2 2002:5 2003:3 2004:0 2005:0 2006:0 2007:1 2008:0 2009:1 2010:0 2011:0 2012:0 2014:0 2018:3 2019:11 2020:3 2021:5 2022:7 2023:4 2024:8 2025:9 2026:2
  WESTBOUND MAIN                            1975:13 1976:9 1977:8 1978:15 1979:8 1980:8 1981:12 1982:5 1983:5 1984:6 1985:8 1986:3 1987:1 1988:4 1989:2 1990:4 1991:0 1992:2 1993:1 1994:7 1995:3 1996:3 1997:1 1998:0 1999:0 2000:0 2001:0 2003:0 2004:0 2007:2
  YARD                                      1975:3 1976:0 1977:0 1978:1 1979:2 1980:1 1981:0 1982:0 1983:0 1984:0 1985:1 1986:7 1987:0 1988:1 1989:0 1990:0 1991:0 1992:1 1993:0 1994:0 1995:0 1996:1 1997:1 1998:1 1999:0 2000:1 2001:1 2002:1 2003:0 2004:0 2005:2 2006:1 2007:1 2008:0 2009:0 2010:0 2011:0 2012:0 2013:2 2014:0 2015:0 2017:0 2021:0

## what

INCIDENT_MONTH: 01 10%, 12 10%, 10 9%, 11 9%, 02 9%, 03 8%, 08 8%, 09 8%, 07 7%, 05 7%, 06 7%, 04 7%

OTHER_INCIDENT_YEAR: 77 15%, 78 12%, 79 12%, 80 9%, 82 9%, 84 8%, 76 8%, 81 8%, 83 7%, 85 7%, 86 5%

OTHER_INCIDENT_MONTH: 01 12%, 12 11%, 10 10%, 02 10%, 03 9%, 05 8%, 09 8%, 11 8%, 06 8%, 04 8%, 08 8%

MAINTENANCE_INCIDENT_MONTH: 01 11%, 12 11%, 02 10%, 10 10%, 11 9%, 03 9%, 08 9%, 09 8%, 07 8%, 06 8%, 05 8%

MONTH: 01 10%, 12 10%, 10 9%, 11 9%, 02 9%, 03 8%, 08 8%, 09 8%, 07 7%, 05 7%, 06 7%, 04 7%

DAY: 09 8%, 20 8%, 07 8%, 18 8%, 08 8%, 03 8%, 12 8%, 06 8%, 17 8%, 10 8%, 05 8%, 13 8%

HOUR: 11 9%, 10 9%, 9 9%, 1 8%, 7 8%, 8 8%, 12 8%, 2 8%, 6 8%, 3 8%, 5 7%, 4 7%

AM_PM: PM 58%, AM 42%

PUBLIC_PRIVATE_CODE: Y 90%, N 10%

PUBLIC_PRIVATE: Public 90%, Private 10%

HIGHWAY_USER_CODE: A 59%, B 18%, C 10%, D 4%, M 3%, K 2%, J 1%, E 1%, H 1%, F 0%, G 0%

HIGHWAY_USER: Auto 59%, Truck 18%, Truck-trailer 10%, Pick-up truck 4%, Other 3%, Pedestrian 2%, Other motor vehicle 1%, Van 1%, Motorcycle 1%, Bus 0%, School bus 0%

VEHICLE_DIRECTION_CODE: 1 26%, 3 25%, 2 25%, 4 24%, 0 0%, A 0%

VEHICLE_DIRECTION: North 26%, East 25%, South 25%, West 24%

HIGHWAY_USER_POSITION_CODE: 3 72%, 2 17%, 1 10%, 4 1%, 5 0%

HIGHWAY_USER_POSITION: Moving over crossing 72%, Stopped on crossing 17%, Stalled or stuck on crossing 10%, Trapped on crossing by traffic 1%, Blocked on crossing by gates 0%

EQUIPMENT_INVOLVED_CODE: 1 80%, 2 8%, 6 7%, 4 2%, 3 2%, 8 1%, 5 0%, 7 0%, D 0%, B 0%, A 0%, E 0%

EQUIPMENT_INVOLVED: Train (units pulling) 80%, Train (units pushing) 8%, Light loco(s) (moving) 7%, Car(s) (moving) 2%, Train (standing) 2%, Other 1%, Car(s) (standing) 0%, Light loco(s) (standing) 0%, EMU Locomotive(s) 0%, Train pushing - RCL 0%, Train pulling - RCL 0%, DMU Locomotive(s) 0%

EQUIPMENT_STRUCK_CODE: 1 76%, 2 24%, 4 0%

EQUIPMENT_STRUCK: Rail equipment struck highway  76%, Rail equipment struck by highw 24%

HAZMAT_INVOLVEMENT_CODE: 4 88%, 2 11%, 1 1%, 3 0%, 0 0%

HAZMAT_INVOLVEMENT: Neither 88%, Rail equipment 11%, Highway user 1%, Both 0%

HAZMAT_RELEASED_BY_CODE: 4 97%, 0 3%, 1 0%, 2 0%, 3 0%, 9 0%

HAZMAT_RELEASED_BY: Neither 100%, Highway user 0%, Rail equipment 0%, Both 0%

HAZMAT_RELEASED_MEASURE: 0 90%, GALS 4%, GALL 2%, TONS 1%, GAL 1%, 000 1%, LBS 0%, . 0%, DRUM 0%, UART 0%, OUNC 0%

VISIBILITY_CODE: 2 57%, 4 35%, 3 4%, 1 3%

VISIBILITY: Day 57%, Dark 35%, Dusk 4%, Dawn 3%

WEATHER_CONDITION_CODE: 1 66%, 2 21%, 3 8%, 6 3%, 4 2%, 5 0%, 0 0%

WEATHER_CONDITION: Clear 66%, Cloudy 21%, Rain 8%, Snow 3%, Fog 2%, Sleet 0%

EQUIPMENT_TYPE_CODE: 1 72%, 7 11%, 8 7%, 2 6%, 4 2%, 3 1%, 9 0%, A 0%, C 0%, B 0%, D 0%

EQUIPMENT_TYPE: Freight Train 72%, Yard/switching 11%, Light loco(s) 7%, Passenger Train - Pulling 6%, Work train 2%, Commuter Train - Pulling 1%, Maint./inspect Car 0%, Spec. MoW Equip. 0%, Commuter Train - Pushing 0%, Passenger Train - Pushing 0%, EMU 0%

TRACK_TYPE_CODE: 1 86%, 2 7%, 4 5%, 3 1%, 0 0%, 8 0%

TRACK_TYPE: Main 86%, Yard 7%, Industry 5%, Siding 1%

TRACK_CLASS: 4 32%, 3 26%, 2 19%, 1 19%, 5 4%, X 1%, 6 0%, 0 0%, 8 0%, 9 0%, 7 0%

NUMBER_OF_LOCOMOTIVE_UNITS: 1 33%, 2 32%, 3 19%, 4 9%, 5 3%, 0 3%, 6 1%, 7 0%, 8 0%, 10 0%, 9 0%, 12 0%

ESTIMATED_RECORDED_SPEED: E 83%, R 17%

TRAIN_DIRECTION_CODE: 4 29%, 3 28%, 1 22%, 2 21%, A 0%

TRAIN_DIRECTION: West 29%, East 28%, North 22%, South 21%

CROSSING_WARNING_EXPANDED_CODE_1: 7 40%, 1 21%, 3 19%, 8 6%, 2 5%, 12 4%, 5 1%, 4 1%, 10 1%, 6 1%, 11 1%, 9 0%

CROSSING_WARNING_EXPANDED_CODE_2: 3 29%, 7 21%, 6 16%, 2 10%, 8 8%, 11 8%, 10 4%, 5 3%, 4 1%, 9 0%, 12 0%

CROSSING_WARNING_EXPANDED_CODE_3: 6 44%, 7 25%, 3 12%, 11 7%, 5 4%, 8 4%, 10 3%, 4 1%, 9 0%, 12 0%, 1 0%

CROSSING_WARNING_EXPANDED_CODE_4: 7 53%, 6 27%, 11 9%, 8 5%, 5 3%, 10 2%, 4 1%, 9 0%, 3 0%, 1 0%, 12 0%

CROSSING_WARNING_EXPANDED_CODE_5: 7 58%, 11 23%, 6 10%, 8 5%, 10 3%, 9 1%, 5 1%, 3 0%, 12 0%, 1 0%

CROSSING_WARNING_EXPANDED_CODE_6: 11 49%, 7 39%, 8 5%, 10 4%, 6 2%, 9 0%, 12 0%, 3 0%

CROSSING_WARNING_EXPANDED_CODE_7: 11 64%, 7 30%, 10 4%, 8 1%, 9 1%, 12 1%

CROSSING_WARNING_EXPANDED_CODE_8: 10 100%

CROSSING_WARNING_EXPANDED_1: Crossbucks 42%, Gates 22%, Standard FLS 20%, Stop signs 6%, Cantilever FLS 6%, Hwy. traffic signals 1%, Wig wags 1%, Flagged by crew 1%, Audible 1%, Other 1%, Watchman 0%

CROSSING_WARNING_EXPANDED_2: Standard FLS 29%, Crossbucks 21%, Audible 16%, Cantilever FLS 10%, Stop signs 8%, Other 8%, Flagged by crew 4%, Hwy. traffic signals 3%, Wig wags 1%, Watchman 0%, Gates 0%

CROSSING_WARNING_EXPANDED_3: Audible 44%, Crossbucks 25%, Standard FLS 12%, Other 7%, Hwy. traffic signals 4%, Stop signs 4%, Flagged by crew 3%, Wig wags 1%, Watchman 0%, Gates 0%, Cantilever FLS 0%

CROSSING_WARNING_EXPANDED_4: Crossbucks 53%, Audible 27%, Other 9%, Stop signs 5%, Hwy. traffic signals 3%, Flagged by crew 2%, Wig wags 1%, Watchman 0%, Standard FLS 0%, Gates 0%

CROSSING_WARNING_EXPANDED_5: Crossbucks 58%, Other 23%, Audible 10%, Stop signs 5%, Flagged by crew 3%, Watchman 1%, Hwy. traffic signals 1%, Standard FLS 0%, Gates 0%

CROSSING_WARNING_EXPANDED_6: Other 49%, Crossbucks 39%, Stop signs 5%, Flagged by crew 4%, Audible 2%, Watchman 0%, Standard FLS 0%

CROSSING_WARNING_EXPANDED_7: Other 64%, Crossbucks 30%, Flagged by crew 4%, Stop signs 1%, Watchman 1%

CROSSING_WARNING_EXPANDED_8: Flagged by crew 100%

SIGNALED_CROSSING_WARNING_CODE: 1 96%, 4 2%, 2 1%, 7 1%, 3 0%, 5 0%, 6 0%, 8 0%, E 0%, S 0%, 0 0%

SIGNALED_CROSSING_WARNING: Provided minimum 20-second war 96%, Alleged no warning 2%, Alleged warning time greater t 1%, Confirmed no warning 1%, Alleged warning time less than 0%, Confirmed warning time greater 0%, Confirmed warning time less th 0%

CROSSING_WARNING_EXPLANATION_CODE: A 55%, S 17%, F 9%, J 6%, E 5%, R 3%, G 2%, P 1%, B 1%, L 1%, H 1%

CROSSING_WARNING_EXPLANATION: Insulated rail traffic 55%, Other cause(s) - explain in Na 17%, Devices out of service 9%, Warning > 60 secs - other trai 6%, Devices down for repair 5%, No warning attributed to signa 3%, Warning > 60 secs - train stop 2%, Warning < 20 secs - violation  1%, Storm/Lightning damage 1%, Warning < 20 secs - train oper 1%, Warning > 60 secs - track circ 1%

ROADWAY_CONDITION_CODE: A 84%, B 10%, C 4%, E 1%, D 1%, F 0%

ROADWAY_CONDITION: Dry 84%, Wet 10%, Snow/slush 4%, Sand, Mud, Dirt, Oil, Grease 1%, Ice 1%, Water (Standing, Moving) 0%

CROSSING_WARNING_LOCATION_CODE: 1 91%, 2 5%, 0 2%, 3 1%, 4 0%, N 0%

CROSSING_WARNING_LOCATION: Both sides 93%, Side of vehicle approach 5%, Opposite side of vehicle appro 1%

WARNING_CONNECTED_TO_SIGNAL: No 77%, Unknown 16%, Yes 7%

CROSSING_ILLUMINATED: No 57%, Yes 25%, Unknown 19%

USER_SEX: Male 76%, Female 24%

USER_STRUCK_BY_SECOND_TRAIN: No 96%, Yes 2%, Unknown 1%

HIGHWAY_USER_ACTION_CODE: 3 53%, 4 26%, 1 9%, 2 6%, 5 5%, 7 1%, 8 0%, 6 0%, 0 0%

HIGHWAY_USER_ACTION: Did not stop 53%, Stopped on crossing 26%, Went around the gate 9%, Stopped and then proceeded 6%, Other 5%, Went thru the gate 1%, Suicide/attempted suicide 0%, Went around/thru temporary bar 0%

DRIVER_PASSED_VEHICLE: No 89%, Unknown 8%, Yes 3%

VIEW_OBSTRUCTION_CODE: 8 93%, 1 2%, 5 2%, 7 1%, 4 1%, 2 1%, 3 0%, 6 0%, 0 0%, 9 0%

VIEW_OBSTRUCTION: Not obstructed 93%, Permanent structure 2%, Vegetation 2%, Other 1%, Topography 1%, Standing railroad equipment 1%, Passing train 0%, Highway vehicles 0%

DRIVER_CONDITION_CODE: 3 69%, 2 24%, 1 7%, 0 0%, 8 0%

DRIVER_CONDITION: Uninjured 69%, Injured 24%, Killed 7%

DRIVER_IN_VEHICLE: Yes 85%, No 15%, Unknown 0%

CROSSING_USERS_KILLED: 0 91%, 1 7%, 2 1%, 3 0%, 4 0%, 5 0%, 6 0%, 7 0%, 8 0%, 9 0%, 10 0%

CROSSING_USERS_INJURED: 0 74%, 1 21%, 2 4%, 3 1%, 4 0%, 5 0%, 6 0%, 7 0%, 8 0%, 9 0%, 10 0%

EMPLOYEES_KILLED: 0 100%, 1 0%, 2 0%, 3 0%

EMPLOYEES_INJURED: 0 98%, 1 1%, 2 0%, 3 0%, 4 0%, 5 0%, 6 0%, 8 0%, 7 0%, 9 0%, 12 0%

FORM_54_FILED: No 96%, Yes 4%

PASSENGERS_KILLED: 0 100%, 1 0%, 11 0%, 5 0%, 4 0%, 3 0%

PASSENGERS_INJURED: 0 100%, 1 0%, 2 0%, 3 0%, 4 0%, 6 0%, 5 0%, 7 0%, 9 0%, 8 0%, 13 0%

VIDEO_TAKEN: Yes 55%, No 45%

VIDEO_USED: No 78%, Yes 22%

SPECIAL_STUDY_1: N/A 53%, NO NO 22%, 0 7%, NO 5%, 1 4%, . 3%, AGE OF DRIVER UNKNOW 2%, YESYES 2%, N 1%, #8 1%, NA 1%

SPECIAL_STUDY_2: 0 74%, N/A 15%, VIDEO USED - NO 3%, NO 3%, 1 2%, YES 1%, VIDEO USED - YES 1%, CWR 1%, . 1%, N/ 0%, N 0%

RAILROAD_TYPE: 1L 75%, 1 8%, 3L 6%, 3 3%, CL 3%, 2 1%, 6 1%, 3S 1%, 2L 1%, Cl 1%, 1S 0%, No 0%

JOINT_CODE: 1 99%, 2 1%

DISTRICT: 3 22%, 5 20%, 4 20%, 2 11%, 6 11%, 7 7%, 8 6%, 1 3%, 0 0%

WHISTLE_BAN_CODE: 2 88%, 3 6%, 1 4%, N 2%

WHISTLE_BAN: No 90%, Not Provided 6%, Yes 4%

REPORTING_RAILROAD_CLASS: Class I 78%, Class III 14%, Not Assigned 6%, Class II 2%, Unassigned 0%

REPORTING_RAILROAD_SMT_GROUPING: SMT-6 - UP/KCS 24%, SMT-9 - CSX 16%, SMT-5 - BNSF 15%, SMT-3 - Norfolk Southern 14%, Not Assigned 9%, SMT-4 - CPKC/CP/CN/CCD 8%, SMT-8 - Short Line West 4%, SMT-2 - Short Line East 4%, SMT-1 - Amtrak, Commuter East 4%, SMT-7 - Commuter West 1%, Unassigned 0%

REPORTING_RAILROAD_HOLDING_COMPANY: Union Pacific Railroad Company 23%, Not Assigned 16%, CSX Transportation 16%, BNSF Railway Company 15%, Norfolk Southern Railway Compa 14%, Canadian National - North Amer 6%, Amtrak 3%, Kansas City Southern Railway C 3%, Canadian Pacific Railway Compa 2%, Genesee & Wyoming 1%, Railroad Acquisition Holdings 1%, Watco 0%

REPORTING_RAILROAD_INDIVIDUAL_CLASS: Not Assigned 51%, Class I 30%, Class III 16%, Unassigned 1%, Class II 1%

REPORTING_RAILROAD_PASSENGER: Unassigned 51%, Not Assigned 44%, Yes 5%

REPORTING_RAILROAD_COMMUTER: Unassigned 55%, Not Assigned 44%, Yes 2%

REPORTING_RAILROAD_SWITCHING_TERMINAL: Unassigned 53%, Not Assigned 44%, Yes 3%

REPORTING_RAILROAD_TOURIST: Unassigned 54%, Not Assigned 43%, Yes 2%

REPORTING_RAILROAD_FREIGHT: Not Assigned 43%, Yes 38%, Unassigned 18%

REPORTING_RAILROAD_SHORT_LINE: Unassigned 50%, Not Assigned 44%, Yes 7%

_SRC_SHA256: 03027049ff66bf57e4b49bba6d186e 40%, fba6564de28c044430abca048d1570 40%, 475feae587bcd0b526c1bfbcebd5c7 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAILROAD_CODE | other | 1.1K | 0 | UP 25.0K; CSX 19.6K; CR 15.5K; NS 14.6K |
| RAILROAD_NAME | who | 1.1K | 0 | Union Pacific Railroad Co 25.0K; CSX Transportation 19.6K; Conrail 15.5K; Norfolk Southern Railway  14.6K |
| REPORT_YEAR | other | 52 | 0 | 1978 13.6K; 1977 13.4K; 1976 13.2K; 1979 12.8K |
| INCIDENT_NUMBER | other | 221.1K | 1 | 1 440; E3420 256; E3360 256; A3350 256 |
| INCIDENT_YEAR | other | 51 | 0 | 78 13.6K; 77 13.4K; 76 13.2K; 79 12.8K |
| INCIDENT_MONTH | category | 13 | 0 | 01 26.1K; 12 24.9K; 10 22.4K; 11 22.2K |
| OTHER_RAILROAD_CODE | other | 106 | 246.6K | ATK 2.1K; CR 339; SCL 241; ICG 236 |
| OTHER_RAILROAD_NAME | who | 105 | 246.6K | Amtrak (National Railroad 2.1K; Conrail 339; Seaboard Coast Line Railr 241; Illinois Central Gulf Rai 236 |
| OTHER_INCIDENT_NUMBER | other | 4.1K | 246.6K | XXX 185; ZZZ 23; 0970302 12; 0940304 11 |
| OTHER_INCIDENT_YEAR | category | 34 | 246.6K | 77 630; 78 525; 79 517; 80 362 |
| OTHER_INCIDENT_MONTH | category | 13 | 246.6K | 01 497; 12 456; 10 416; 02 410 |
| MAINTENANCE_RAILROAD_CODE | other | 2.0K | 19.3K | UP 25.9K; CSX 21.0K; NS 15.0K; CR 14.9K |
| MAINTENANCE_RAILROAD_NAME | who | 1.9K | 19.3K | Union Pacific Railroad Co 25.9K; CSX Transportation 21.0K; Norfolk Southern Railway  15.0K; Conrail 14.9K |
| MAINTAINANCE_INCIDENT_NUMBER | other | 189.8K | 19.4K | XXX 15.2K; 1 414; E3420 240; E3360 240 |
| MAINTENANCE_INCIDENT_YEAR | other | 52 | 19.4K | 78 13.6K; 77 13.4K; 79 12.8K; 80 10.8K |
| MAINTENANCE_INCIDENT_MONTH | category | 13 | 19.4K | 01 24.2K; 12 22.8K; 02 20.5K; 10 20.5K |
| GRADE_CROSSING_ID | other | 101.3K | 5.5K | NOTASGN 2.0K; 300235N 434; 233071R 434; 751558D 434 |
| DATE | date | 18.4K | 10 | 07/15/1990 268; 06/22/1990 268; 06/29/1990 267; 07/17/1990 266 |
| MONTH | category | 12 | 0 | 01 26.1K; 12 24.9K; 10 22.4K; 11 22.2K |
| DAY | category | 32 | 0 | 09 8.6K; 20 8.5K; 07 8.5K; 18 8.5K |
| HOUR | category | 13 | 0 | 11 23.0K; 10 22.8K; 9 22.4K; 1 21.3K |
| MINUTE | other | 60 | 0 | 30 24.2K; 0 21.7K; 45 19.1K; 15 18.6K |
| AM_PM | category | 3 | 31 | PM 146.3K; AM 104.8K |
| TIME | who | 1.5K | 0 | 03:30 PM 1.4K; 02:30 PM 1.4K; 04:00 PM 1.4K; 04:30 PM 1.4K |
| NEAREST_STATION | who | 28.4K | 970 | HOUSTON 1.7K; BATON ROUGE 956; JACKSON 930; MOBILE 889 |
| DIVISION | who | 972 | 208.3K | SYSTEM 5.3K; CHICAGO 1.2K; GULF 1.2K; ATLANTA 1.2K |
| SUBDIVISION | who | 2.5K | 218.9K | SYSTEM 1.9K; ALABAMA 494; PIEDMONT 484; GEORGIA 451 |
| COUNTY_CODE | other | 286 | 1.9K | 031 8.1K; 037 5.3K; 201 5.1K; 089 4.7K |
| COUNTY_NAME | who | 2.3K | 278 | JEFFERSON 5.6K; COOK 4.9K; HARRIS 4.7K; LAKE 3.2K |
| STATE_CODE | other | 53 | 3 | 48 26.4K; 17 15.9K; 18 14.2K; 39 14.2K |
| STATE_NAME | who | 52 | 5 | TEXAS 26.4K; ILLINOIS 15.9K; INDIANA 14.2K; OHIO 14.2K |
| CITY_NAME | who | 17.8K | 41.5K | HOUSTON 3.1K; CHICAGO 1.8K; N/A 1.6K; PHOENIX 927 |
| HIGHWAY_NAME | who | 113.1K | 2.5K | PRIVATE 7.7K; PRIVATE CROSSING 4.6K; COUNTY ROAD 2.4K; MAIN STREET 1.8K |
| PUBLIC_PRIVATE_CODE | category | 2 | 0 | Y 226.9K; N 24.2K |
| PUBLIC_PRIVATE | category | 2 | 0 | Public 226.9K; Private 24.2K |
| HIGHWAY_USER_CODE | category | 12 | 9 | A 148.3K; B 45.3K; C 26.2K; D 10.3K |
| HIGHWAY_USER | category | 12 | 9 | Auto 148.3K; Truck 45.3K; Truck-trailer 26.2K; Pick-up truck 10.3K |
| ESTIMATED_VEHICLE_SPEED | other | 97 | 28.1K | 0 66.3K; 5 30.2K; 10 29.3K; 20 14.7K |
| VEHICLE_DIRECTION_CODE | category | 7 | 1.7K | 1 64.1K; 3 63.2K; 2 62.1K; 4 60.0K |
| VEHICLE_DIRECTION | category | 5 | 1.7K | North 64.1K; East 63.2K; South 62.1K; West 60.0K |
| HIGHWAY_USER_POSITION_CODE | category | 6 | 403 | 3 179.6K; 2 43.4K; 1 26.3K; 4 1.3K |
| HIGHWAY_USER_POSITION | category | 6 | 403 | Moving over crossing 179.6K; Stopped on crossing 43.4K; Stalled or stuck on cross 26.3K; Trapped on crossing by tr 1.3K |
| EQUIPMENT_INVOLVED_CODE | category | 14 | 5 | 1 201.9K; 2 19.0K; 6 17.6K; 4 5.2K |
| EQUIPMENT_INVOLVED | category | 14 | 5 | Train (units pulling) 201.9K; Train (units pushing) 19.0K; Light loco(s) (moving) 17.6K; Car(s) (moving) 5.2K |
| RAILROAD_CAR_UNIT_POSITION | other | 179 | 1.3K | 1 226.2K; 2 4.9K; 3 2.1K; 4 1.3K |
| EQUIPMENT_STRUCK_CODE | category | 4 | 7 | 1 190.6K; 2 60.5K; 4 3 |
| EQUIPMENT_STRUCK | category | 3 | 10 | Rail equipment struck hig 190.6K; Rail equipment struck by  60.5K |
| HAZMAT_INVOLVEMENT_CODE | category | 6 | 375 | 4 220.3K; 2 28.7K; 1 1.3K; 3 409 |
| HAZMAT_INVOLVEMENT | category | 5 | 388 | Neither 220.3K; Rail equipment 28.7K; Highway user 1.3K; Both 409 |
| HAZMAT_RELEASED_BY_CODE | category | 7 | 179.6K | 4 69.4K; 0 1.9K; 1 201; 2 51 |
| HAZMAT_RELEASED_BY | category | 5 | 181.5K | Neither 69.4K; Highway user 201; Rail equipment 51; Both 4 |
| HAZMAT_RELEASED_NAME | who | 124 | 250.9K | DIESEL FUEL 46; DIESEL 14; FUEL 5; BATTERY ACID 5 |
| HAZMAT_RELEASED_QUANTITY | other | 81 | 250.9K | 000 20; 0 16; TON 13; 10 12 |
| HAZMAT_RELEASED_MEASURE | category | 39 | 249.0K | 0 1.9K; GALS 89; GALL 36; TONS 29 |
| TEMPERATURE | other | 189 | 1 | 70 14.4K; 60 14.3K; 50 13.2K; 80 12.0K |
| VISIBILITY_CODE | category | 5 | 18 | 2 143.3K; 4 88.9K; 3 10.6K; 1 8.3K |
| VISIBILITY | category | 5 | 18 | Day 143.3K; Dark 88.9K; Dusk 10.6K; Dawn 8.3K |
| WEATHER_CONDITION_CODE | category | 8 | 137 | 1 166.4K; 2 53.0K; 3 19.5K; 6 7.2K |
| WEATHER_CONDITION | category | 7 | 145 | Clear 166.4K; Cloudy 53.0K; Rain 19.5K; Snow 7.2K |
| EQUIPMENT_TYPE_CODE | category | 15 | 505 | 1 179.0K; 7 28.3K; 8 17.1K; 2 15.8K |
| EQUIPMENT_TYPE | category | 15 | 505 | Freight Train 179.0K; Yard/switching 28.3K; Light loco(s) 17.1K; Passenger Train - Pulling 15.8K |
| TRACK_TYPE_CODE | category | 7 | 234 | 1 216.3K; 2 17.5K; 4 13.6K; 3 3.5K |
| TRACK_TYPE | category | 5 | 236 | Main 216.3K; Yard 17.5K; Industry 13.6K; Siding 3.5K |
| TRACK_NAME | who | 30.2K | 579 | MAIN 43.1K; SINGLE MAIN TRACK 42.7K; SINGLE MAIN 36.1K; MAIN LINE 12.0K |
| TRACK_CLASS | category | 15 | 4.0K | 4 78.7K; 3 63.9K; 2 46.7K; 1 46.5K |
| NUMBER_OF_LOCOMOTIVE_UNITS | category | 44 | 13 | 1 82.4K; 2 79.2K; 3 48.9K; 4 22.5K |
| NUMBER_OF_CARS | other | 279 | 59 | 0 20.8K; 1 12.7K; 4 7.8K; 5 7.3K |
| TRAIN_SPEED | other | 114 | 2.6K | 10 20.8K; 5 19.2K; 25 15.5K; 40 14.6K |
| ESTIMATED_RECORDED_SPEED | category | 3 | 2.0K | E 205.8K; R 43.4K |
| TRAIN_DIRECTION_CODE | category | 6 | 1.0K | 4 72.0K; 3 70.5K; 1 54.6K; 2 53.0K |
| TRAIN_DIRECTION | category | 5 | 1.0K | West 72.0K; East 70.5K; North 54.6K; South 53.0K |
| CROSSING_WARNING_EXPANDED_CODE_1 | category | 13 | 4 | 7 100.8K; 1 53.1K; 3 48.0K; 8 14.5K |
| CROSSING_WARNING_EXPANDED_CODE_2 | category | 13 | 136.6K | 3 33.5K; 7 23.9K; 6 18.9K; 2 11.5K |
| CROSSING_WARNING_EXPANDED_CODE_3 | category | 13 | 198.0K | 6 23.2K; 7 13.3K; 3 6.5K; 11 3.8K |
| CROSSING_WARNING_EXPANDED_CODE_4 | category | 12 | 225.1K | 7 13.8K; 6 7.0K; 11 2.4K; 8 1.2K |
| CROSSING_WARNING_EXPANDED_CODE_5 | category | 11 | 242.3K | 7 5.1K; 11 2.0K; 6 912; 8 438 |
| CROSSING_WARNING_EXPANDED_CODE_6 | category | 9 | 249.3K | 11 922; 7 745; 8 99; 10 74 |
| CROSSING_WARNING_EXPANDED_CODE_7 | category | 7 | 251.0K | 11 108; 7 51; 10 7; 8 2 |
| CROSSING_WARNING_EXPANDED_CODE_8 | category | 2 | 251.1K | 10 1 |
| CROSSING_WARNING_EXPANDED_CODE_9 | empty | 1 | 251.1K |  |
| CROSSING_WARNING_EXPANDED_CODE_10 | empty | 1 | 251.1K |  |
| CROSSING_WARNING_EXPANDED_CODE_11 | empty | 1 | 251.1K |  |
| CROSSING_WARNING_EXPANDED_CODE_12 | empty | 1 | 251.1K |  |
| CROSSING_WARNING_EXPANDED_1 | category | 12 | 10.7K | Crossbucks 100.8K; Gates 53.1K; Standard FLS 48.0K; Stop signs 14.5K |
| CROSSING_WARNING_EXPANDED_2 | category | 12 | 136.7K | Standard FLS 33.5K; Crossbucks 23.9K; Audible 18.9K; Cantilever FLS 11.5K |
| CROSSING_WARNING_EXPANDED_3 | category | 12 | 198.0K | Audible 23.2K; Crossbucks 13.3K; Standard FLS 6.5K; Other 3.8K |
| CROSSING_WARNING_EXPANDED_4 | category | 11 | 225.1K | Crossbucks 13.8K; Audible 7.0K; Other 2.4K; Stop signs 1.2K |
| CROSSING_WARNING_EXPANDED_5 | category | 10 | 242.3K | Crossbucks 5.1K; Other 2.0K; Audible 912; Stop signs 438 |
| CROSSING_WARNING_EXPANDED_6 | category | 8 | 249.3K | Other 922; Crossbucks 745; Stop signs 99; Flagged by crew 74 |
| CROSSING_WARNING_EXPANDED_7 | category | 6 | 251.0K | Other 108; Crossbucks 51; Flagged by crew 7; Stop signs 2 |
| CROSSING_WARNING_EXPANDED_8 | category | 2 | 251.1K | Flagged by crew 1 |
| CROSSING_WARNING_EXPANDED_9 | empty | 1 | 251.1K |  |
| CROSSING_WARNING_EXPANDED_10 | empty | 1 | 251.1K |  |
| CROSSING_WARNING_EXPANDED_11 | empty | 1 | 251.1K |  |
| CROSSING_WARNING_EXPANDED_12 | empty | 1 | 251.1K |  |
| SIGNALED_CROSSING_WARNING_CODE | category | 12 | 127.4K | 1 118.7K; 4 2.6K; 2 1.3K; 7 755 |
| SIGNALED_CROSSING_WARNING | category | 8 | 127.4K | Provided minimum 20-secon 118.7K; Alleged no warning 2.6K; Alleged warning time grea 1.3K; Confirmed no warning 755 |
| CROSSING_WARNING_EXPLANATION_CODE | category | 17 | 250.2K | A 519; S 163; F 81; J 55 |
| CROSSING_WARNING_EXPLANATION | category | 17 | 250.2K | Insulated rail traffic 519; Other cause(s) - explain  163; Devices out of service 81; Warning > 60 secs - other 55 |
| ROADWAY_CONDITION_CODE | category | 7 | 218.9K | A 27.1K; B 3.1K; C 1.2K; E 477 |
| ROADWAY_CONDITION | category | 7 | 218.9K | Dry 27.1K; Wet 3.1K; Snow/slush 1.2K; Sand, Mud, Dirt, Oil, Gre 477 |
| CROSSING_WARNING_LOCATION_CODE | category | 7 | 5.6K | 1 223.4K; 2 13.2K; 0 5.6K; 3 3.4K |
| CROSSING_WARNING_LOCATION | category | 4 | 11.2K | Both sides 223.4K; Side of vehicle approach 13.2K; Opposite side of vehicle  3.4K |
| WARNING_CONNECTED_TO_SIGNAL | category | 4 | 26.6K | No 172.3K; Unknown 35.8K; Yes 16.4K |
| CROSSING_ILLUMINATED | category | 4 | 9.0K | No 137.4K; Yes 59.3K; Unknown 45.3K |
| USER_AGE | other | 98 | 180.7K | 0 7.9K; 40 2.6K; 21 2.4K; 30 2.2K |
| USER_SEX | category | 3 | 180.2K | Male 53.7K; Female 17.3K |
| USER_STRUCK_BY_SECOND_TRAIN | category | 4 | 3.5K | No 238.2K; Yes 5.8K; Unknown 3.7K |
| HIGHWAY_USER_ACTION_CODE | category | 10 | 3.1K | 3 131.4K; 4 64.8K; 1 21.6K; 2 14.6K |
| HIGHWAY_USER_ACTION | category | 9 | 3.1K | Did not stop 131.4K; Stopped on crossing 64.8K; Went around the gate 21.6K; Stopped and then proceede 14.6K |
| DRIVER_PASSED_VEHICLE | category | 4 | 5.8K | No 218.5K; Unknown 19.7K; Yes 7.2K |
| VIEW_OBSTRUCTION_CODE | category | 11 | 269 | 8 232.3K; 1 6.2K; 5 4.4K; 7 2.3K |
| VIEW_OBSTRUCTION | category | 9 | 272 | Not obstructed 232.3K; Permanent structure 6.2K; Vegetation 4.4K; Other 2.3K |
| DRIVER_CONDITION_CODE | category | 6 | 6.8K | 3 169.1K; 2 59.2K; 1 16.1K; 0 27 |
| DRIVER_CONDITION | category | 4 | 6.8K | Uninjured 169.1K; Injured 59.2K; Killed 16.1K |
| DRIVER_IN_VEHICLE | category | 4 | 6.1K | Yes 209.0K; No 36.0K; Unknown 2 |
| CROSSING_USERS_KILLED | category | 13 | 2.2K | 0 227.6K; 1 18.3K; 2 2.2K; 3 507 |
| CROSSING_USERS_INJURED | category | 29 | 1.8K | 0 183.8K; 1 52.9K; 2 8.9K; 3 2.3K |
| VEHICLE_DAMAGE_COST | amount | 2.0K | 1.9K | 0 41.9K; 1000 23.1K; 500 20.5K; 2000 17.8K |
| NUMBER_VEHICLE_OCCUPANTS | other | 54 | 224 | 1 166.8K; 0 34.4K; 2 33.2K; 3 9.9K |
| EMPLOYEES_KILLED | category | 5 | 2.5K | 0 248.5K; 1 76; 2 15; 3 3 |
| EMPLOYEES_INJURED | category | 18 | 2.4K | 0 244.7K; 1 2.9K; 2 799; 3 188 |
| NUMBER_PEOPLE_ON_TRAIN | other | 550 | 176.0K | 2 47.8K; 3 14.4K; 1 3.0K; 4 1.5K |
| FORM_54_FILED | category | 3 | 308 | No 240.5K; Yes 10.3K |
| PASSENGERS_KILLED | category | 7 | 6.1K | 0 245.1K; 1 3; 11 1; 5 1 |
| PASSENGERS_INJURED | category | 43 | 6.1K | 0 244.3K; 1 388; 2 119; 3 72 |
| VIDEO_TAKEN | category | 3 | 218.9K | Yes 17.9K; No 14.4K |
| VIDEO_USED | category | 3 | 218.9K | No 25.2K; Yes 7.0K |
| SPECIAL_STUDY_1 | category | 15 | 251.0K | N/A 60; NO NO 25; 0 8; NO 6 |
| SPECIAL_STUDY_2 | category | 17 | 250.8K | 0 285; N/A 58; VIDEO USED - NO 12; NO 11 |
| NARRATIVE | other | 51.7K | 194.2K | AGE OF DRIVER UNKNOWN 836; HIGHWAY USER'S ACTIONS: D 728; AGE OF DRIVER UNKNOWN. 569; HIGHWAY USER'S ACTIONS: S 511 |
| TOTAL_KILLED_FORM_57 | amount | 15 | 0 | 0 229.8K; 1 18.4K; 2 2.2K; 3 513 |
| TOTAL_INJURED_FORM_57 | amount | 44 | 0 | 0 183.8K; 1 53.8K; 2 9.5K; 3 2.5K |
| RAILROAD_TYPE | category | 16 | 12 | 1L 188.5K; 1 19.9K; 3L 14.2K; 3 7.3K |
| JOINT_CODE | category | 2 | 0 | 1 248.9K; 2 2.3K |
| TOTAL_KILLED_FORM_55A | amount | 13 | 0 | 0 230.4K; 1 17.8K; 2 2.2K; 3 518 |
| TOTAL_INJURED_FORM_55A | amount | 45 | 0 | 0 182.4K; 1 54.1K; 2 10.1K; 3 2.8K |
| DISTRICT | category | 10 | 25.3K | 3 50.2K; 5 45.3K; 4 44.9K; 2 25.8K |
| WHISTLE_BAN_CODE | category | 5 | 207.2K | 2 38.6K; 3 2.5K; 1 1.8K; N 1.1K |
| WHISTLE_BAN | category | 4 | 208.3K | No 38.6K; Not Provided 2.5K; Yes 1.8K |
| REPORT_KEY | id | 247.6K | 0 | NWX920890200199008 369; NWX820890159199008 369; NWX820890149199008 369; NWX550890159199008 369 |
| REPORTING_RAILROAD_CLASS | category | 5 | 0 | Class I 196.9K; Class III 35.2K; Not Assigned 14.2K; Class II 4.6K |
| REPORTING_RAILROAD_SMT_GROUPING | category | 11 | 0 | SMT-6 - UP/KCS 60.7K; SMT-9 - CSX 39.9K; SMT-5 - BNSF 36.5K; SMT-3 - Norfolk Southern 34.2K |
| REPORTING_PARENT_RAILROAD_CODE | other | 862 | 0 | UP 56.4K; CSX 39.9K; BNSF 36.5K; NS 34.3K |
| REPORTING_PARENT_RAILROAD_NAME | who | 879 | 0 | Union Pacific Railroad Co 56.4K; CSX Transportation 39.9K; BNSF Railway Company 36.5K; Norfolk Southern Railway  34.3K |
| REPORTING_RAILROAD_HOLDING_COMPANY | category | 45 | 0 | Union Pacific Railroad Co 56.4K; Not Assigned 40.1K; CSX Transportation 39.9K; BNSF Railway Company 36.5K |
| URL | id | 251.1K | 72 | https://safetydata.fra.do 369; https://safetydata.fra.do 369; https://safetydata.fra.do 369; https://safetydata.fra.do 369 |
| REPORTING_RAILROAD_INDIVIDUAL_CLASS | category | 5 | 0 | Not Assigned 128.7K; Class I 74.6K; Class III 40.6K; Unassigned 3.7K |
| REPORTING_RAILROAD_PASSENGER | category | 3 | 0 | Unassigned 128.0K; Not Assigned 109.6K; Yes 13.6K |
| REPORTING_RAILROAD_COMMUTER | category | 3 | 0 | Unassigned 137.0K; Not Assigned 109.9K; Yes 4.3K |
| REPORTING_RAILROAD_SWITCHING_TERMINAL | category | 3 | 0 | Unassigned 133.7K; Not Assigned 109.8K; Yes 7.7K |
| REPORTING_RAILROAD_TOURIST | category | 3 | 0 | Unassigned 136.5K; Not Assigned 109.2K; Yes 5.5K |
| REPORTING_RAILROAD_FREIGHT | category | 3 | 0 | Not Assigned 108.4K; Yes 96.4K; Unassigned 46.3K |
| REPORTING_RAILROAD_SHORT_LINE | category | 3 | 0 | Unassigned 124.9K; Not Assigned 109.6K; Yes 16.6K |
| _INGESTED_AT | audit | 1 | 0 | 1786299998946552 251.1K |
| _SOURCE_RUN_ID | audit | 1 | 0 | c514637e-4260-4e80-948b-4 251.1K |
| _SRC_SHA256 | category | 3 | 0 | 03027049ff66bf57e4b49bba6 100.0K; fba6564de28c044430abca048 100.0K; 475feae587bcd0b526c1bfbce 51.1K |
