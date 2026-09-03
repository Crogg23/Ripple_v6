# FED_FRA_CASUALTIES

rows 1.15M  columns 73  scan 6.9s

roles: amount 2, audit 2, category 34, date 1, id 3, other 18, who 13

## when

DATE
  1997     12.8K  ##############################
  1998     12.5K  #############################
  1999     12.6K  #############################
  2000     12.9K  ##############################
  2001     12.0K  ############################
  2002     12.1K  ############################
  2003     10.2K  ########################
  2004     10.2K  ########################
  2005     10.6K  #########################
  2006      9.8K  #######################
  2007     10.6K  #########################
  2008     10.0K  #######################
  2009      8.8K  ####################
  2010      9.2K  #####################
  2011      9.2K  #####################
  2012      9.2K  #####################
  2013      9.5K  ######################
  2014      9.6K  ######################
  2015      9.9K  #######################
  2016      9.5K  ######################
  2017      9.8K  #######################
  2018      9.2K  #####################
  2019      9.0K  #####################
  2020      6.4K  ###############
  2021      6.9K  ################
  2022      7.5K  #################
  2023      7.8K  ##################
  2024      7.6K  ##################
  2025      7.3K  #################
  2026      3.0K  #######

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 218.6K | 0 | 0 | 47.21 | 180 | 2.56M |
| LONGITUDE | 218.6K | -965.01 | 0 | 0 | 0 | -6.31M |

## who

RAILROAD_NAME by rows
    100.3K  Union Pacific Railroad Company
     98.6K  Conrail
     92.8K  Amtrak (National Railroad Passenger Corporation)
     81.7K  Burlington Northern Railroad Company
     52.2K  Southern Pacific Transportation Company
     45.3K  CSX Transportation
     40.2K  Long Island Rail Road
     37.3K  Norfolk & Western Railway Company
     33.4K  Atchison, Topeka & Santa Fe Railway Company
     32.2K  BNSF Railway Company
     29.4K  Illinois Central Gulf Railroad Company
     25.6K  Missouri Pacific Railroad Company
     24.0K  Chicago And North Western Railway Company
     23.7K  Norfolk Southern Railway Company
     22.1K  SOUTHERN RAILWAY COMPANY
     19.7K  Metro North Commuter Railroad Company
     17.5K  CHESAPEAKE & OHIO RAILWAY CO.
     16.8K  SOO Line Railroad Company
     16.8K  Seaboard Coast Line Railroad
     16.6K  Baltimore And Ohio Railroad Company

RAILROAD_NAME by dollars
      511.4K   100.3K rows  Union Pacific Railroad Company
      439.8K    32.2K rows  BNSF Railway Company
      348.9K    23.7K rows  Norfolk Southern Railway Company
      329.3K    45.3K rows  CSX Transportation
      314.1K    92.8K rows  Amtrak (National Railroad Passenger Corporation)
       37.8K     1.5K rows  Consolidated Rail Corporation
       28.6K    13.8K rows  New Jersey Transit Rail Operations
       23.2K     7.3K rows  NORTHEAST ILLINOIS REGIONAL COMMUTER RAIL CORP. -- METRA
       23.0K     5.7K rows  Illinois Central Railroad Company
       21.7K     1.6K rows  Southern California Regional Rail Authority
       21.5K     1.3K rows  Union Pacific Metra
       20.9K    40.2K rows  Long Island Rail Road
       20.0K     3.7K rows  WISCONSIN CENTRAL LTD.
       16.1K    19.7K rows  Metro North Commuter Railroad Company
       11.7K     1.4K rows  Canadian Pacific Railway Company
       11.4K      948 rows  Caltrain Commuter Railroad Company
       10.2K     2.9K rows  Alaska Railroad Corporation
        9.6K     2.9K rows  Florida East Coast Railway Company
        8.7K     8.8K rows  Kansas City Southern Railway Company
        8.6K      518 rows  CANADIAN PACIFIC KANSAS CITY

REPORTING_PARENT_RAILROAD_NAME by rows
    225.2K  Union Pacific Railroad Company
    156.0K  BNSF Railway Company
    133.3K  CSX Transportation
    100.1K  Consolidated Rail Corporation
     96.4K  Amtrak (National Railroad Passenger Corporation)
     91.0K  Norfolk Southern Railway Company
     64.9K  Canadian National - North America
     48.6K  CANADIAN PACIFIC KANSAS CITY
     40.2K  Long Island Rail Road
     19.7K  Metro North Commuter Railroad Company
     13.8K  New Jersey Transit Rail Operations
     12.6K  Southeastern Pennsylvania Transportation Authority
     10.4K  Port Authority Trans Hudson
      9.2K  Penn Central Transportation Company
      9.2K  NORTHEAST ILLINOIS REGIONAL COMMUTER RAIL CORP. -- METRA
      6.7K  Pan Am Railways/Guilford System
      5.5K  Chicago, Rock Island And Pacific Railroad
      3.6K  Massachusetts Bay Transportation Authority
      3.1K  Indiana Harbor Belt Railroad Company
      3.0K  THREE RIVERS RAILWAY COMPANY

REPORTING_PARENT_RAILROAD_NAME by dollars
      515.3K   225.2K rows  Union Pacific Railroad Company
      440.2K   156.0K rows  BNSF Railway Company
      349.2K    91.0K rows  Norfolk Southern Railway Company
      329.4K   133.3K rows  CSX Transportation
      314.1K    96.4K rows  Amtrak (National Railroad Passenger Corporation)
       64.5K    64.9K rows  Canadian National - North America
       52.4K     9.2K rows  NORTHEAST ILLINOIS REGIONAL COMMUTER RAIL CORP. -- METRA
       37.8K   100.1K rows  Consolidated Rail Corporation
       34.3K    48.6K rows  CANADIAN PACIFIC KANSAS CITY
       28.6K    13.8K rows  New Jersey Transit Rail Operations
       21.7K     1.6K rows  Southern California Regional Rail Authority
       20.9K    40.2K rows  Long Island Rail Road
       16.1K    19.7K rows  Metro North Commuter Railroad Company
       11.4K      948 rows  Caltrain Commuter Railroad Company
       10.2K     2.9K rows  Alaska Railroad Corporation
        9.6K     2.9K rows  Florida East Coast Railway Company
        8.5K     1.0K rows  Northern Indiana Commuter Transportation District
        8.1K      403 rows  Brightline Train
        7.9K      360 rows  READING BLUE MOUNTAIN & NORTHERN RAILROAD COMMISSION
        7.7K     1.6K rows  Montana Rail Link

COUNTY_NAME by rows
     14.6K  COOK
      9.4K  NEW YORK
      7.9K  PHILADELPHIA
      6.9K  HUDSON
      6.7K  QUEENS
      5.6K  SUFFOLK
      5.0K  LOS ANGELES
      4.2K  NASSAU
      4.0K  WESTCHESTER
      3.7K  JEFFERSON
      3.1K  WASHINGTON, DC
      3.0K  ESSEX
      2.6K  HARRIS
      2.4K  MONTGOMERY
      2.3K  SAN BERNARDINO
      2.2K  MIDDLESEX
      2.1K  LAKE
      2.0K  MARION
      2.0K  FAIRFIELD
      1.8K  WARD

COUNTY_NAME by dollars
      109.6K    14.6K rows  COOK
       46.4K     5.0K rows  LOS ANGELES
       41.7K     3.7K rows  JEFFERSON
       27.5K     2.3K rows  SAN BERNARDINO
       24.8K     2.6K rows  HARRIS
       24.5K     7.9K rows  PHILADELPHIA
       22.5K     2.1K rows  LAKE
       19.4K     1.7K rows  WAYNE
       19.3K     2.0K rows  MARION
       18.6K     1.5K rows  KING
       18.5K     1.7K rows  TARRANT
       18.2K     1.5K rows  SHELBY
       17.4K     1.6K rows  LINCOLN
       17.2K      830 rows  PIERCE
       16.8K      487 rows  GLOUCESTER
       16.6K     1.6K rows  JACKSON
       16.5K     1.3K rows  FULTON
       16.1K     1.1K rows  HAMILTON
       15.0K     2.4K rows  MONTGOMERY
       14.9K      948 rows  WILL

STATE_NAME by rows
     96.6K  ILLINOIS
     96.0K  NEW YORK
     76.1K  TEXAS
     71.9K  PENNSYLVANIA
     68.5K  CALIFORNIA
     51.7K  OHIO
     37.7K  NEW JERSEY
     35.6K  MICHIGAN
     34.3K  INDIANA
     28.8K  MISSOURI
     28.3K  NEBRASKA
     26.9K  GEORGIA
     26.2K  VIRGINIA
     26.0K  FLORIDA
     25.2K  KENTUCKY
     24.9K  MINNESOTA
     23.8K  LOUISIANA
     22.7K  WISCONSIN
     22.4K  IOWA
     21.1K  WASHINGTON

STATE_NAME by dollars
      266.8K    68.5K rows  CALIFORNIA
      213.9K    96.6K rows  ILLINOIS
      188.4K    76.1K rows  TEXAS
      116.5K    71.9K rows  PENNSYLVANIA
       94.3K    96.0K rows  NEW YORK
       90.2K    51.7K rows  OHIO
       86.1K    34.3K rows  INDIANA
       80.9K    26.9K rows  GEORGIA
       79.1K    21.1K rows  WASHINGTON
       77.3K    37.7K rows  NEW JERSEY
       62.7K    26.0K rows  FLORIDA
       59.2K    28.3K rows  NEBRASKA
       59.1K    28.8K rows  MISSOURI
       57.3K    19.3K rows  TENNESSEE
       54.7K    20.1K rows  KANSAS
       53.1K    17.6K rows  ALABAMA
       51.8K    24.9K rows  MINNESOTA
       49.9K    26.2K rows  VIRGINIA
       49.5K    15.4K rows  NORTH CAROLINA
       47.2K    23.8K rows  LOUISIANA

## who x when

RAILROAD_NAME by DATE, dollars = LATITUDE
  Alaska Railroad Corporation               1997:74 1998:60 1999:62 2000:51 2001:57 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:126.07 2012:0 2013:0 2014:0 2015:126.04 2016:244.74 2017:1.0K 2018:816.32 2019:122.35 2020:566.13 2021:183.51 2022:872.70 2023:990.04 2024:1.8K 2025:2.6K 2026:802.74
  Amtrak (National Railroad Passenger Corp  1997:1.4K 1998:1.3K 1999:1.3K 2000:1.5K 2001:1.7K 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:126.81 2010:201.05 2011:14.6K 2012:13.8K 2013:10.8K 2014:10.9K 2015:25.7K 2016:21.1K 2017:18.3K 2018:15.7K 2019:11.9K 2020:8.5K 2021:12.3K 2022:14.6K 2023:12.5K 2024:43.8K 2025:56.3K 2026:23.0K
  BNSF Railway Company                      1997:1.4K 1998:1.6K 1999:1.6K 2000:1.6K 2001:1.6K 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:38.05 2009:0 2010:46.55 2011:4.4K 2012:33.4K 2013:33.8K 2014:35.0K 2015:33.1K 2016:32.4K 2017:33.1K 2018:31.0K 2019:30.0K 2020:28.2K 2021:28.0K 2022:30.3K 2023:27.0K 2024:28.6K 2025:23.6K 2026:7.6K
  CSX Transportation                        1997:1.0K 1998:1.1K 1999:1.3K 2000:1.4K 2001:1.3K 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:27.95 2010:122.74 2011:15.1K 2012:20.4K 2013:24.7K 2014:25.5K 2015:33.0K 2016:23.3K 2017:24.9K 2018:22.2K 2019:18.5K 2020:16.1K 2021:18.1K 2022:18.9K 2023:19.6K 2024:21.4K 2025:20.6K 2026:6.9K
  Caltrain Commuter Railroad Company        1997:22 1998:29 1999:14 2000:39 2001:35 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:224.88 2012:1.3K 2013:1.2K 2014:1.3K 2015:975.18 2016:600.18 2017:636.42 2018:1.4K 2019:1.2K 2020:936.93 2021:975.92 2022:638.16
  Canadian Pacific Railway Company          2004:0 2007:0 2012:42.31 2013:1.7K 2014:1.9K 2015:1.2K 2016:988.92 2017:974.79 2018:1.1K 2019:741.88 2020:751.28 2021:783.58 2022:1.3K 2023:216.18
  Conrail                                   1997:686 1998:544 1999:245
  Consolidated Rail Corporation             1999:31 2000:57 2001:60 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:525.83 2012:16.5K 2013:2.2K 2014:2.4K 2015:2.1K 2016:1.5K 2017:1.7K 2018:2.2K 2019:1.7K 2020:1.4K 2021:1.0K 2022:771.64 2023:1.3K 2024:896.53 2025:1.2K 2026:363.38
  Illinois Central Railroad Company         1997:153 1998:145 1999:168 2000:203 2001:176 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:1.2K 2012:1.2K 2013:618.88 2014:730.17 2015:1.3K 2016:662.63 2017:1.5K 2018:874.69 2019:2.0K 2020:2.8K 2021:2.4K 2022:2.3K 2023:2.1K 2024:2.2K 2025:1.1K
  Long Island Rail Road                     1997:724 1998:579 1999:540 2000:0 2001:392 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:489.10 2012:1.0K 2013:774.71 2014:570.78 2015:1.4K 2016:1.1K 2017:814.83 2018:1.1K 2019:1.2K 2020:1.1K 2021:1.3K 2022:1.7K 2023:3.1K 2024:2.1K 2025:1.9K 2026:1.2K
  Metro North Commuter Railroad Company     1997:488 1998:393 1999:455 2000:0 2001:469 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:205.40 2012:247.44 2013:3.7K 2014:287.96 2015:2.2K 2016:491.53 2017:986.19 2018:535.07 2019:864.68 2020:697.54 2021:697.18 2022:1.4K 2023:1.2K 2024:1.0K 2025:1.2K 2026:287.52
  NORTHEAST ILLINOIS REGIONAL COMMUTER RAI  1997:196 1998:212 1999:240 2000:288 2001:319 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:708.18 2012:1.0K 2013:1.4K 2014:710.73 2015:751.85 2016:711.37 2017:837.73 2018:501.09 2019:333.79 2020:501.37 2021:2.0K 2022:2.6K 2023:2.4K 2024:3.2K 2025:3.5K 2026:2.1K
  New Jersey Transit Rail Operations        1997:141 1998:118 1999:158 2000:195 2001:251 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:527.53 2012:489 2013:1.3K 2014:1.3K 2015:1.3K 2016:1.1K 2017:731.65 2018:1.1K 2019:653.28 2020:1.1K 2021:896.76 2022:815.23 2023:1.0K 2024:974.89 2025:9.7K 2026:5.6K
  Norfolk Southern Railway Company          1997:642 1998:675 1999:860 2000:896 2001:779 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:120.61 2010:902.92 2011:13.5K 2012:22.2K 2013:28.4K 2014:28.2K 2015:25.7K 2016:26.4K 2017:27.0K 2018:26.0K 2019:27.7K 2020:21.0K 2021:18.9K 2022:17.5K 2023:19.5K 2024:20.2K 2025:17.5K 2026:8.2K
  SOO Line Railroad Company                 1997:265 1998:206 1999:210 2000:171 2001:172 2002:0 2003:259.80 2004:410.98 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:1.7K 2012:995.99
  Southern California Regional Rail Author  1997:37 1998:22 1999:17 2000:32 2001:25 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:989.16 2012:2.1K 2013:2.7K 2014:1.3K 2015:853.20 2016:1.1K 2017:920.57 2018:955.54 2019:1.0K 2020:1.0K 2021:1.4K 2022:1.6K 2023:1.7K 2024:1.5K 2025:2.1K 2026:476.47
  Union Pacific Metra                       2001:54 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:967 2012:1.7K 2013:1.6K 2014:1.9K 2015:2.2K 2016:1.6K 2017:2.4K 2018:2.6K 2019:1.4K 2020:671.96 2021:882.51 2022:1.1K 2023:1.1K 2024:840.39 2025:503.79
  Union Pacific Railroad Company            1997:2.3K 1998:2.4K 1999:2.6K 2000:2.2K 2001:2.1K 2002:0 2003:0 2004:0 2005:0 2006:0 2007:34.90 2008:0 2009:0 2010:41.14 2011:19.8K 2012:33.8K 2013:34.5K 2014:35.6K 2015:32.7K 2016:30.5K 2017:35.0K 2018:35.9K 2019:36.2K 2020:32.3K 2021:34.2K 2022:35.3K 2023:40.4K 2024:34.0K 2025:29.0K 2026:12.0K
  WISCONSIN CENTRAL LTD.                    1997:189 1998:135 1999:138 2000:172 2001:132 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:443.46 2012:450.81 2013:1.5K 2014:804.01 2015:789.11 2016:528.93 2017:1.4K 2018:979.59 2019:2.4K 2020:2.3K 2021:1.9K 2022:2.3K 2023:2.3K 2024:1.3K 2025:529.18

REPORTING_PARENT_RAILROAD_NAME by DATE, dollars = LATITUDE
  Alaska Railroad Corporation               1997:74 1998:60 1999:62 2000:51 2001:57 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:126.07 2012:0 2013:0 2014:0 2015:126.04 2016:244.74 2017:1.0K 2018:816.32 2019:122.35 2020:566.13 2021:183.51 2022:872.70 2023:990.04 2024:1.8K 2025:2.6K 2026:802.74
  Amtrak (National Railroad Passenger Corp  1997:1.4K 1998:1.3K 1999:1.3K 2000:1.5K 2001:1.7K 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:126.81 2010:201.05 2011:14.6K 2012:13.8K 2013:10.8K 2014:10.9K 2015:25.7K 2016:21.1K 2017:18.3K 2018:15.7K 2019:11.9K 2020:8.5K 2021:12.3K 2022:14.6K 2023:12.5K 2024:43.8K 2025:56.3K 2026:23.0K
  BNSF Railway Company                      1997:1.4K 1998:1.6K 1999:1.6K 2000:1.7K 2001:1.6K 2002:0 2003:0 2004:180 2005:0 2006:0 2007:0 2008:38.05 2009:0 2010:46.55 2011:4.4K 2012:33.4K 2013:33.8K 2014:35.0K 2015:33.1K 2016:32.4K 2017:33.1K 2018:31.0K 2019:30.1K 2020:28.2K 2021:28.0K 2022:30.3K 2023:27.0K 2024:28.6K 2025:23.6K 2026:7.6K
  Brightline Train                          2017:106.11 2018:687.29 2019:1.1K 2020:210.15 2021:261.48 2022:1.0K 2023:790.01 2024:1.9K 2025:1.5K 2026:555.79
  CANADIAN PACIFIC KANSAS CITY              1997:558 1998:519 1999:499 2000:454 2001:420 2002:0 2003:259.80 2004:410.98 2005:0 2006:0 2007:81.69 2008:0 2009:0 2010:0 2011:3.4K 2012:2.1K 2013:2.2K 2014:2.6K 2015:1.9K 2016:1.5K 2017:1.6K 2018:1.8K 2019:1.3K 2020:1.8K 2021:1.7K 2022:2.4K 2023:2.9K 2024:3.1K 2025:2.3K 2026:937.99
  CSX Transportation                        1997:1.0K 1998:1.1K 1999:1.3K 2000:1.4K 2001:1.3K 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:27.95 2010:122.74 2011:15.1K 2012:20.4K 2013:24.7K 2014:25.6K 2015:33.0K 2016:23.3K 2017:24.9K 2018:22.3K 2019:18.5K 2020:16.1K 2021:18.1K 2022:18.9K 2023:19.6K 2024:21.4K 2025:20.6K 2026:6.9K
  Caltrain Commuter Railroad Company        1997:22 1998:29 1999:14 2000:39 2001:35 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:224.88 2012:1.3K 2013:1.2K 2014:1.3K 2015:975.18 2016:600.18 2017:636.42 2018:1.4K 2019:1.2K 2020:936.93 2021:975.92 2022:638.16
  Canadian National - North America         1997:695 1998:604 1999:554 2000:618 2001:525 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:2.2K 2012:2.4K 2013:2.6K 2014:2.8K 2015:2.6K 2016:2.0K 2017:4.2K 2018:2.5K 2019:5.3K 2020:7.1K 2021:5.7K 2022:6.7K 2023:5.5K 2024:4.5K 2025:5.9K 2026:2.6K
  Consolidated Rail Corporation             1997:686 1998:544 1999:276 2000:57 2001:60 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:525.83 2012:16.5K 2013:2.2K 2014:2.4K 2015:2.1K 2016:1.5K 2017:1.7K 2018:2.2K 2019:1.7K 2020:1.4K 2021:1.0K 2022:771.64 2023:1.3K 2024:896.53 2025:1.2K 2026:363.38
  Florida East Coast Railway Company        1997:87 1998:72 1999:68 2000:68 2001:40 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:546.24 2012:652.64 2013:692.36 2014:702.85 2015:706.16 2016:904.56 2017:600.32 2018:463.61 2019:547.34 2020:517.56 2021:591.73 2022:412.88 2023:636.46 2024:549.10 2025:597.91 2026:432.40
  Indiana Harbor Belt Railroad Company      1997:66 1998:57 1999:38 2000:45 2001:42 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:83.26 2012:41.83 2013:41.80 2014:83.26 2015:41.70 2016:41.71 2017:83.75 2018:249.75 2019:583.41 2020:333.44 2021:249.80 2022:291.82 2023:333.17 2024:500.01 2025:208.13 2026:166.56
  Long Island Rail Road                     1997:724 1998:579 1999:540 2000:0 2001:392 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:489.10 2012:1.0K 2013:774.71 2014:570.78 2015:1.4K 2016:1.1K 2017:814.83 2018:1.1K 2019:1.2K 2020:1.1K 2021:1.3K 2022:1.7K 2023:3.1K 2024:2.1K 2025:1.9K 2026:1.2K
  Massachusetts Bay Transportation Authori  1997:85 1998:96 1999:98 2000:114 2001:124 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:169.71 2012:169.39 2013:296.97 2014:423.23 2015:338.11 2016:339.21 2017:888.54 2018:510.06 2019:337.21 2020:381.92 2021:211.85 2022:380.63 2023:466.43 2024:507.55 2025:549.79 2026:889.71
  Metro North Commuter Railroad Company     1997:488 1998:393 1999:455 2000:0 2001:469 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:205.40 2012:247.44 2013:3.7K 2014:287.96 2015:2.2K 2016:491.53 2017:986.19 2018:535.07 2019:864.68 2020:697.54 2021:697.18 2022:1.4K 2023:1.2K 2024:1.0K 2025:1.2K 2026:287.52
  Montana Rail Link                         1997:54 1998:18 1999:27 2000:25 2001:40 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:93.92 2012:233.01 2013:187.27 2014:832.09 2015:830.79 2016:831.15 2017:1.0K 2018:1.3K 2019:278.72 2020:279.19 2021:508.39 2022:650.51 2023:600.67
  NORTHEAST ILLINOIS REGIONAL COMMUTER RAI  1997:196 1998:212 1999:240 2000:288 2001:405 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:2.1K 2012:3.6K 2013:3.2K 2014:3.1K 2015:3.3K 2016:2.8K 2017:3.7K 2018:3.8K 2019:2.6K 2020:1.4K 2021:3.3K 2022:4.2K 2023:3.8K 2024:4.5K 2025:4.7K 2026:2.3K
  New Jersey Transit Rail Operations        1997:141 1998:118 1999:158 2000:195 2001:251 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:527.53 2012:489 2013:1.3K 2014:1.3K 2015:1.3K 2016:1.1K 2017:731.65 2018:1.1K 2019:653.28 2020:1.1K 2021:896.76 2022:815.23 2023:1.0K 2024:974.89 2025:9.7K 2026:5.6K
  Norfolk Southern Railway Company          1997:642 1998:676 1999:865 2000:899 2001:783 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:120.61 2010:902.92 2011:13.5K 2012:22.2K 2013:28.4K 2014:28.2K 2015:25.8K 2016:26.4K 2017:27.1K 2018:26.0K 2019:27.7K 2020:21.0K 2021:18.9K 2022:17.5K 2023:19.6K 2024:20.2K 2025:17.5K 2026:8.2K
  Northern Indiana Commuter Transportation  1997:32 1998:33 1999:38 2000:21 2001:8 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:333.36 2012:499.93 2013:458.68 2014:500.30 2015:291.65 2016:208.16 2017:582.65 2018:708.68 2019:497.51 2020:500.29 2021:1.1K 2022:1.0K 2023:416.69 2024:208.11 2025:458.52 2026:708.26
  Pan Am Railways/Guilford System           1997:23 1998:28 1999:26 2000:32 2001:17 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:0 2012:303.18 2013:648.63 2014:776.04 2015:602.33 2016:431.51 2017:257.48 2018:565.18 2019:426.64 2020:426.97 2021:606.83 2022:651.62 2023:736.67
  Port Authority Trans Hudson               1997:188 1998:165 1999:159 2000:200 2001:160 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:0 2012:0 2013:0 2014:40.73 2015:81.47 2016:0 2017:0 2018:40.73 2019:0 2020:122.22 2021:40.73 2022:122.23 2023:122.16 2024:122.20 2025:1.0K 2026:40.73
  READING BLUE MOUNTAIN & NORTHERN RAILROA  1997:10 1998:8 1999:10 2000:2 2001:3 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:82.69 2012:367.56 2013:489.95 2014:449.61 2015:326.82 2016:571.01 2017:326.05 2018:368.54 2019:487.57 2020:530.23 2021:447.75 2022:732.60 2023:776.51 2024:612.76 2025:938.72 2026:408.35
  Southeastern Pennsylvania Transportation  1997:383 1998:377 1999:358 2000:282 2001:265 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:80.27 2012:640.79 2013:441.02 2014:601.12 2015:361 2016:400.30 2017:681.07 2018:640.13 2019:319.83 2020:320.47 2021:240.03 2022:280.20 2023:240.05 2024:119.94 2025:359.75 2026:80.19
  Southern California Regional Rail Author  1997:37 1998:22 1999:17 2000:32 2001:25 2002:0 2003:0 2004:0 2005:0 2006:0 2007:0 2008:0 2009:0 2010:0 2011:989.16 2012:2.1K 2013:2.7K 2014:1.3K 2015:853.20 2016:1.1K 2017:920.57 2018:955.54 2019:1.0K 2020:1.0K 2021:1.4K 2022:1.6K 2023:1.7K 2024:1.5K 2025:2.1K 2026:476.47
  Union Pacific Railroad Company            1997:2.4K 1998:2.5K 1999:2.7K 2000:2.2K 2001:2.1K 2002:0 2003:0 2004:0 2005:0 2006:0 2007:34.90 2008:0 2009:0 2010:41.14 2011:19.9K 2012:34.0K 2013:35.0K 2014:35.7K 2015:32.8K 2016:30.6K 2017:35.2K 2018:36.2K 2019:36.5K 2020:32.6K 2021:34.6K 2022:35.5K 2023:40.8K 2024:34.5K 2025:29.3K 2026:12.0K

## what

INCIDENT_MONTH: 08 9%, 07 9%, 06 9%, 10 9%, 01 9%, 09 9%, 05 8%, 03 8%, 04 8%, 11 8%, 02 7%, 12 7%

INCIDENT_DAY: 00 89%, 18 1%, 06 1%, 12 1%, 15 1%, 17 1%, 09 1%, 07 1%, 10 1%, 03 1%, 05 1%, 08 1%

TYPE_OF_PERSON_CODE: A 77%, D 11%, E 6%, C 4%, B 1%, F 1%, G 1%, J 0%, H 0%, I 0%

TYPE_OF_PERSON: Worker on Duty–Railroad Employ 77%, Nontrespassers–On Railroad Pro 11%, Trespassers 6%, Passengers on Trains 4%, Railroad Employee Not On Duty 1%, Worker On Duty–Contractor 1%, Contractor–Other 1%, Nontrespassers–Off Railroad Pr 0%, Workeron Duty–Volunteer 0%, Volunteer–Other 0%

POSITIVE_ALCOHOL_TESTS: 00 77%, 01 22%, N 0%, D0 0%, 02 0%, 0 0%, A0 0%, AD 0%, 05 0%, Y 0%, N/ 0%

POSITIVE_DRUG_TESTS: 00 50%, 01 50%, 03 0%, 02 0%, A0 0%, 0 0%, D1 0%, 09 0%, A 0%

LOCATION_OF_INJURY_ON_BODY: 6 28%, 3 23%, 1 20%, 5 18%, 9 6%, 8 3%, 0 1%, 2 0%, 4 0%, 7 0%, J 0%

SPECIFIC_LOCATION: F 25%, C 22%, D 15%, B 14%, A 9%, E 9%, G 3%, I 1%, H 1%, J 1%, 1 1%

GENERAL_LOCATION_OF_PERSON_CODE: A 49%, B 19%, P 12%, Q 6%, J 4%, D 3%, C 2%, N 2%, E 2%, M 1%, Z 1%

GENERAL_LOCATION_OF_PERSON: Main/branch 49%, Yard 19%, Passenger terminal 12%, Repair shop 6%, Highway/roadway 4%, Industry 3%, Siding 2%, Parking lot 2%, Repair 2%, Office environment 1%, Other location 1%

ON_TRACK_EQUIPMENT_CODE: 99 36%, 03 18%, 14 12%, 13 6%, 09 6%, 05 5%, 16 5%, 04 4%, 60 3%, 51 3%, 10 2%

ON_TRACK_EQUIPMENT: The A/I was not associated wit 36%, Freight train - moving 18%, Passenger train - moving 12%, Passenger train - standing 6%, Locomotive(s), not remote cont 6%, Freight car(s) - standing 5%, Passenger car(s) - standing 5%, Freight train - standing 4%, Truck 3%, Automobile 3%, Locomotive(s), not remote cont 2%

SPECIFIC_LOCATION_OF_PERSON_CODE: A3 15%, B4 14%, A7 13%, A2 11%, B7 11%, A1 8%, X9 7%, A6 6%, C2 6%, A9 5%, C4 5%

HAZMAT_EXPOSURE: No 98%, Yes 2%

COVERED_DATA_CODE: P 47%, R 33%, A 20%

COVERED_DATA_REASON: PLHCP prescribed OTC medicatio 47%, PLHCP prescribed restriction o 33%, PLHCP prescribed time off, but 20%

EMPLOYEE_SUSPENSION: No 100%, Yes 0%

DISTRICT: 4 18%, 2 17%, 1 15%, 3 13%, 5 12%, 6 10%, 7 8%, 8 7%, 9 0%

FATALITY: No 95%, Yes 5%

FORM_57_FILED: No 90%, Yes 10%

FORM_54_FILED: No 97%, Yes 3%

CLASS_CODE: 1L 72%, 3L 9%, 3 4%, 1 4%, 6 4%, 2 2%, 3S 2%, CL 1%, 2L 1%, 1S 1%, Cl 0%, 2S 0%

CLASS: Class I 63%, Class III 24%, Not Assigned 12%, Class II 1%, Unassigned 0%

EQUIPMENT_MOVEMENT_CODE: T 92%, X 3%, D 3%, C 3%

REPORTING_RAILROAD_SMT_GROUPING: SMT-6 - UP/KCS 20%, SMT-1 - Amtrak, Commuter East 17%, SMT-5 - BNSF 14%, Not Assigned 13%, SMT-9 - CSX 12%, SMT-3 - Norfolk Southern 8%, SMT-4 - CPKC/CP/CN/CCD 8%, SMT-8 - Short Line West 4%, SMT-2 - Short Line East 3%, SMT-7 - Commuter West 1%, Unassigned 0%

REPORTING_RAILROAD_HOLDING_COMPANY: Not Assigned 29%, Union Pacific Railroad Company 20%, BNSF Railway Company 14%, CSX Transportation 12%, Amtrak 8%, Norfolk Southern Railway Compa 8%, Canadian National - North Amer 6%, Canadian Pacific Railway Compa 1%, Kansas City Southern Railway C 1%, Genesee & Wyoming 1%, Transtar 0%, Railroad Acquisition Holdings 0%

REPORTING_RAILROAD_INDIVIDUAL_CLASS: Not Assigned 56%, Class III 23%, Class I 18%, Unassigned 2%, Class II 1%

REPORTING_RAILROAD_PASSENGER: Not Assigned 43%, Unassigned 38%, Yes 19%

REPORTING_RAILROAD_COMMUTER: Unassigned 46%, Not Assigned 44%, Yes 10%

REPORTING_RAILROAD_SWITCHING_TERMINAL: Unassigned 54%, Not Assigned 44%, Yes 3%

REPORTING_RAILROAD_TOURIST: Unassigned 48%, Not Assigned 43%, Yes 9%

REPORTING_RAILROAD_FREIGHT: Not Assigned 43%, Unassigned 32%, Yes 25%

REPORTING_RAILROAD_SHORT_LINE: Unassigned 51%, Not Assigned 44%, Yes 5%

_SRC_SHA256: f92aa246bd1781fbcc48369f78b0f0 9%, 91981a146bd40f4fd4c0cfab6c2293 9%, 03a110ddeed378c40f5046bfe47c07 9%, f62238a7055b7c67c47d4907cc2436 9%, 00866f63ee9805b9fda51937f9055d 9%, cab918b7448afd1c46d78578a32569 9%, 945bf333605a4386eeaca1e5d6f488 9%, 9d493226010f0a04ac4e5c0e805ffc 9%, 35a783c50d54c020cf84f568764cde 9%, 32d5cc565de9928f553680ae87c37a 9%, 81982576adc0e6317fa5c525ca5832 9%, 066f906a7f10ce89f04ff8bb5231f0 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAILROAD_CODE | other | 1.3K | 0 | UP 100.3K; CR 98.6K; ATK 92.8K; BN 81.7K |
| RAILROAD_NAME | who | 1.3K | 0 | Union Pacific Railroad Co 100.3K; Conrail 98.6K; Amtrak (National Railroad 92.8K; Burlington Northern Railr 81.7K |
| PDF_REPORT | id | 1.09M | 7 | https://safetydata.fra.do 1.8K; https://safetydata.fra.do 902; https://safetydata.fra.do 902; https://safetydata.fra.do 902 |
| INCIDENT_NUMBER | other | 811.4K | 0 | 170488 1.8K; 1 1.6K; ST0113 905; ST0108 904 |
| INCIDENT_YEAR | other | 53 | 0 | 1979 75.6K; 1978 74.2K; 1977 69.4K; 1976 67.0K |
| INCIDENT_MONTH | category | 12 | 0 | 08 109.2K; 07 105.4K; 06 102.1K; 10 101.5K |
| INCIDENT_DAY | category | 32 | 0 | 00 865.1K; 18 10.9K; 06 9.9K; 12 9.8K |
| DATE | date | 10.6K | 865.1K | 01/18/2002 1.5K; 01/08/2003 810; 04/20/2009 712; 06/01/2006 620 |
| TIME | who | 1.4K | 0 | 00:00 865.1K; 10:00 AM 6.2K; 12:00 PM 5.3K; 11:00 AM 4.8K |
| COUNTY_CODE | other | 278 | 865.2K | 031 19.3K; 061 12.0K; 017 11.0K; 101 11.0K |
| COUNTY_NAME | who | 1.6K | 865.1K | COOK 14.6K; NEW YORK 9.6K; PHILADELPHIA 8.0K; HUDSON 7.1K |
| STATE_CODE | other | 53 | 4 | 17 96.6K; 36 96.0K; 48 76.1K; 42 71.9K |
| STATE_NAME | who | 52 | 13 | ILLINOIS 96.6K; NEW YORK 96.0K; TEXAS 76.1K; PENNSYLVANIA 71.9K |
| TYPE_OF_PERSON_CODE | category | 11 | 10 | A 882.2K; D 121.7K; E 68.6K; C 45.4K |
| TYPE_OF_PERSON | category | 11 | 10 | Worker on Duty–Railroad E 882.2K; Nontrespassers–On Railroa 121.7K; Trespassers 68.6K; Passengers on Trains 45.4K |
| EMPLOYEE_JOB_CODE | other | 133 | 249.1K | 313 97.0K; 615 82.6K; 409 46.9K; 312 42.8K |
| EMPLOYEE_JOB_DESCRIPTION | who | 122 | 249.2K | Section Laborers 97.0K; Yard Brakemen and Yard He 82.6K; Carmen (Freight) 46.9K; Extra Gang Laborers 42.8K |
| AGE_OF_PERSON | other | 101 | 39.6K | 30 36.7K; 29 34.9K; 28 34.3K; 27 33.8K |
| POSITIVE_ALCOHOL_TESTS | category | 12 | 980.4K | 00 132.0K; 01 38.3K; N 70; D0 10 |
| POSITIVE_DRUG_TESTS | category | 10 | 979.6K | 00 86.0K; 01 85.0K; 03 125; 02 14 |
| INJURY_ILLNESS_CODE | other | 914 | 4 | 206 90.6K; 206C 79.0K; 203 46.5K; 301F 39.0K |
| NATURE_OF_INJURY | other | 58 | 4 | 20 392.0K; 10 220.5K; 30 164.5K; 70 98.1K |
| LOCATION_OF_INJURY_ON_BODY | category | 15 | 25.2K | 6 314.4K; 3 255.7K; 1 230.7K; 5 208.2K |
| SPECIFIC_LOCATION | category | 22 | 562.2K | F 144.6K; C 126.5K; D 87.8K; B 79.3K |
| INJURY_ILLNESS | who | 795 | 10.4K | Sprain/Strain, torso. 90.6K; Sprain/Strain, lower back 79.0K; Sprain/Strain, leg/foot. 46.5K; Cut/laceration/abrasion,  39.0K |
| PHYSICAL_ACT_CIRCUMSTANCES_CODE | other | 98 | 865.1K | 72 53.2K; 21 25.0K; 58 20.4K; 60 17.9K |
| PHYSICAL_ACT_CIRCUMSTANCES | who | 96 | 865.1K | Walking 53.2K; Driving (motor vehicle, f 25.0K; Riding 20.4K; Sitting 17.9K |
| GENERAL_LOCATION_OF_PERSON_CODE | category | 24 | 865.1K | A 135.3K; B 52.6K; P 32.0K; Q 15.5K |
| GENERAL_LOCATION_OF_PERSON | category | 23 | 865.1K | Main/branch 135.3K; Yard 52.6K; Passenger terminal 32.0K; Repair shop 15.5K |
| ON_TRACK_EQUIPMENT_CODE | category | 40 | 865.1K | 99 92.4K; 03 45.3K; 14 31.0K; 13 16.3K |
| ON_TRACK_EQUIPMENT | category | 41 | 865.1K | The A/I was not associate 92.4K; Freight train - moving 45.3K; Passenger train - moving 31.0K; Passenger train - standin 16.3K |
| SPECIFIC_LOCATION_OF_PERSON_CODE | category | 50 | 865.1K | A3 33.3K; B4 32.6K; A7 28.8K; A2 25.5K |
| SPECIFIC_LOCATION_OF_PERSON | who | 51 | 865.1K | Track, beside 33.3K; On highway-rail crossing 32.6K; Car, in (rail car) 28.8K; At work station 25.5K |
| EVENT_CODE | other | 83 | 865.1K | 32 37.7K; 70 32.4K; 38 24.2K; 59 22.9K |
| EVENT | who | 84 | 865.1K | Highway-rail collision/im 37.7K; Slipped, fell, stumbled,  32.4K; Overexertion 24.2K; Struck by on-track equipm 22.9K |
| TOOLS_CODE | other | 96 | 865.1K | 99 46.1K; 14 37.5K; 18 31.0K; 82 14.6K |
| TOOLS | who | 91 | 867.7K | Other (describe in narrat 46.1K; Ground 37.5K; Highway, street, road 31.0K; Locomotive, other 14.6K |
| INJURY_CAUSE_CODE | other | 62 | 865.1K | 09 127.4K; 99 43.5K; 10 37.0K; 01 24.2K |
| INJURY_CAUSE | who | 57 | 889.4K | Human factor 127.4K; Undetermined 43.5K; Trespassing 37.0K; Equipment 18.3K |
| DAYS_AWAY_FROM_WORK | other | 375 | 38 | 0 635.8K; 1 46.3K; 2 44.3K; 3 35.0K |
| DAYS_RESTRICTED_ACTIVITY | other | 347 | 38 | 0 1.01M; 5 15.5K; 2 13.5K; 1 11.8K |
| HAZMAT_EXPOSURE | category | 3 | 950.9K | No 196.6K; Yes 3.3K |
| COVERED_DATA_CODE | category | 4 | 1.15M | P 840; R 583; A 366 |
| COVERED_DATA_REASON | category | 4 | 1.15M | PLHCP prescribed OTC medi 840; PLHCP prescribed restrict 583; PLHCP prescribed time off 366 |
| LATITUDE | amount | 50.1K | 932.2K | 0.0 151.1K; 39.834580000000003 448; 39.957106000000003 326; 35.870749000000004 267 |
| LONGITUDE | amount | 49.4K | 932.2K | 0.0 151.0K; -75.23669800000000 448; -75.18491500000000 326; -83.96094100000001 267 |
| NARRATIVE | other | 110.3K | 1.02M | Per #0001 3.4K; 5J- SLEEPING;  5K- HOME;  1.4K; THE TRESPASSER WAS STRUCK 1.4K; STS IDENTIFIED. 1.1K |
| EMPLOYEE_SUSPENSION | category | 3 | 1.03M | No 125.0K; Yes 487 |
| DISTRICT | category | 10 | 10 | 4 212.8K; 2 193.9K; 1 167.5K; 3 153.2K |
| FATALITY | category | 2 | 0 | No 1.10M; Yes 53.1K |
| FORM_57_FILED | category | 2 | 0 | No 1.03M; Yes 118.0K |
| FORM_54_FILED | category | 2 | 0 | No 1.12M; Yes 34.1K |
| CLASS_CODE | category | 15 | 16 | 1L 826.2K; 3L 103.4K; 3 47.1K; 1 44.0K |
| CLASS | category | 5 | 0 | Class I 719.5K; Class III 280.0K; Not Assigned 134.3K; Class II 16.0K |
| CASUALTY_OCCURRENCE_CODE | other | 230 | 285.7K | 609 76.8K; 864 25.8K; 825 25.2K; 940 25.0K |
| EQUIPMENT_MOVEMENT_CODE | category | 5 | 928.0K | T 204.3K; X 6.4K; D 6.0K; C 6.0K |
| REPORT_KEY | id | 1.17M | 0 | ATK1873212025061143845 902; ICGST0118197701127993 902; ICGST0118197801197821 902; ICGST0117198101409796 902 |
| REPORTING_RAILROAD_SMT_GROUPING | category | 11 | 0 | SMT-6 - UP/KCS 231.6K; SMT-1 - Amtrak, Commuter  198.2K; SMT-5 - BNSF 156.2K; Not Assigned 147.9K |
| REPORTING_PARENT_RAILROAD_CODE | other | 1.1K | 0 | UP 225.2K; BNSF 156.0K; CSX 133.3K; CRSH 100.1K |
| REPORTING_PARENT_RAILROAD_NAME | who | 1.1K | 0 | Union Pacific Railroad Co 225.2K; BNSF Railway Company 156.0K; CSX Transportation 133.3K; Consolidated Rail Corpora 100.1K |
| REPORTING_RAILROAD_HOLDING_COMPANY | category | 50 | 0 | Not Assigned 328.4K; Union Pacific Railroad Co 225.1K; BNSF Railway Company 156.0K; CSX Transportation 133.3K |
| GEOCODE | who | 51.2K | 932.2K | POINT (0 0) 151.1K; POINT (-75.236698 39.8345 448; POINT (-75.184915 39.9571 326; POINT (-83.960941 35.8707 267 |
| INCIDENT_KEY | id | 1.10M | 0 | SOO170488200201 1.8K; ATK187321202506 902; ICGST0118197701 902; ICGST0118197801 902 |
| REPORTING_RAILROAD_INDIVIDUAL_CLASS | category | 5 | 0 | Not Assigned 646.1K; Class III 266.3K; Class I 211.2K; Unassigned 17.7K |
| REPORTING_RAILROAD_PASSENGER | category | 3 | 0 | Not Assigned 500.0K; Unassigned 437.0K; Yes 213.8K |
| REPORTING_RAILROAD_COMMUTER | category | 3 | 0 | Unassigned 533.8K; Not Assigned 501.8K; Yes 115.2K |
| REPORTING_RAILROAD_SWITCHING_TERMINAL | category | 3 | 0 | Unassigned 618.8K; Not Assigned 501.6K; Yes 30.4K |
| REPORTING_RAILROAD_TOURIST | category | 3 | 0 | Unassigned 547.1K; Not Assigned 498.8K; Yes 104.9K |
| REPORTING_RAILROAD_FREIGHT | category | 3 | 0 | Not Assigned 495.6K; Unassigned 364.1K; Yes 291.1K |
| REPORTING_RAILROAD_SHORT_LINE | category | 3 | 0 | Unassigned 590.3K; Not Assigned 500.7K; Yes 59.8K |
| _INGESTED_AT | audit | 1 | 0 | 1786299726422939 1.15M |
| _SOURCE_RUN_ID | audit | 1 | 0 | e9d61b78-932d-468d-bf9e-f 1.15M |
| _SRC_SHA256 | category | 12 | 0 | f92aa246bd1781fbcc48369f7 100.0K; 91981a146bd40f4fd4c0cfab6 100.0K; 03a110ddeed378c40f5046bfe 100.0K; f62238a7055b7c67c47d4907c 100.0K |
