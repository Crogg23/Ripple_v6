# PORTAL_CKA_SAN_JOSE_OPEN_DA_242D633A81

rows 1.1K  columns 21  scan 3.6s

roles: amount 4, audit 2, category 7, date 1, empty 2, id 2, other 1, who 3

## when

INGESTED_AT
  2026      1.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 1.1K | 6.12M | 6.16M | 6.19M | 6.19M | 6.56B |
| Y | 1.1K | 1.90M | 1.95M | 1.96M | 1.98M | 2.07B |
| LONGITUDE | 1.1K | -122.03 | -121.89 | -121.79 | -121.76 | -129.8K |
| LATITUDE | 1.1K | 37.21 | 37.33 | 37.38 | 37.43 | 39.8K |

## who

FUNDINGSOURCE by rows
       595  Transportation Fund for Clean Air
       129  TDA 3
        96  TFCA
        39  Redevelopment Agency
        10  City of San Jose
         3  Private
         2  Recentv3. ID: SS94
         2  San Carlos Streetscape Project
         1  Recentv3. ID: SS79
         1  Recentv3. ID: SS29
         1  VTA: Branham Station
         1  VTA: Ohlone/Chynoweth Station
         1  San Jose: City Hall (City Employees Only)
         1  VTA: Penitencia Creek Station
         1  Santa Clara County: Service Center
         1  San Jose: Joyce Ellington Library
         1  Recentv3. ID: SS97
         1  RG1
         1  San Jose: Seven Trees Library
         1  Recentv3. ID: SS74

FUNDINGSOURCE by dollars
       3.66B      595 rows  Transportation Fund for Clean Air
     794.52M      129 rows  TDA 3
     591.54M       96 rows  TFCA
     240.16M       39 rows  Redevelopment Agency
      61.56M       10 rows  City of San Jose
      18.46M        3 rows  Private
      12.32M        2 rows  San Carlos Streetscape Project
      12.32M        2 rows  Recentv3. ID: SS94
       6.18M        1 rows  Other
       6.18M        1 rows  VTA: Cottle Station
       6.18M        1 rows  VTA: Eastridge Transit Center
       6.18M        1 rows  San Jose: Dr. Roberto Cruz Library
       6.17M        1 rows  VTA: Alum Rock Transit Center
       6.17M        1 rows  San Jose: Seven Trees Library
       6.17M        1 rows  San Jose: Tully Community Library
       6.17M        1 rows  San Jose: Mayfair Comm. Center Library
       6.17M        1 rows  VTA: Penitencia Creek Station
       6.17M        1 rows  San Jose: Educational Park Library
       6.17M        1 rows  VTA: Branham Station
       6.17M        1 rows  VTA: Ohlone/Chynoweth Station

FACILITYID by rows
         1  2842
         1  2819
         1  2860
         1  2856
         1  2844
         1  2868
         1  2890
         1  2925
         1  2898
         1  2932
         1  2986
         1  2944
         1  2918
         1  2896
         1  2820
         1  2809
         1  2960
         1  2853
         1  2835
         1  2827

FACILITYID by dollars
       6.19M        1 rows  985
       6.19M        1 rows  983
       6.19M        1 rows  3636
       6.19M        1 rows  984
       6.19M        1 rows  3491
       6.19M        1 rows  986
       6.19M        1 rows  987
       6.19M        1 rows  3673
       6.19M        1 rows  929
       6.19M        1 rows  930
       6.19M        1 rows  3637
       6.19M        1 rows  3638
       6.19M        1 rows  3639
       6.19M        1 rows  3640
       6.19M        1 rows  3687
       6.18M        1 rows  1005
       6.18M        1 rows  1004
       6.18M        1 rows  3688
       6.18M        1 rows  3689
       6.18M        1 rows  996

SRC_SHA256 by rows
      1.1K  d7490a52a077d0f93f6930459137ba03abb2ff834fec04fa1bc4edd38824ac78

SRC_SHA256 by dollars
       6.56B     1.1K rows  d7490a52a077d0f93f6930459137ba03abb2ff834fec04fa1bc4edd38824

## who x when

FUNDINGSOURCE by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  City of San Jose                          2026:61.56M
  Other                                     2026:6.18M
  Private                                   2026:18.46M
  RG1                                       2026:6.15M
  Recentv3. ID: SS29                        2026:6.16M
  Recentv3. ID: SS74                        2026:6.16M
  Recentv3. ID: SS79                        2026:6.16M
  Recentv3. ID: SS94                        2026:12.32M
  Recentv3. ID: SS97                        2026:6.16M
  Redevelopment Agency                      2026:240.16M
  San Carlos Streetscape Project            2026:12.32M
  San Jose: City Hall (City Employees Only  2026:6.16M
  San Jose: Dr. Roberto Cruz Library        2026:6.18M
  San Jose: Educational Park Library        2026:6.17M
  San Jose: Joyce Ellington Library         2026:6.16M
  San Jose: Mayfair Comm. Center Library    2026:6.17M
  San Jose: Seven Trees Library             2026:6.17M
  San Jose: Tully Community Library         2026:6.17M
  Santa Clara County: Service Center        2026:6.16M
  TDA 3                                     2026:794.52M
  TFCA                                      2026:591.54M
  Transportation Fund for Clean Air         2026:3.66B
  VTA: Alum Rock Transit Center             2026:6.17M
  VTA: Branham Station                      2026:6.17M
  VTA: Cottle Station                       2026:6.18M
  VTA: Eastridge Transit Center             2026:6.18M
  VTA: Ohlone/Chynoweth Station             2026:6.17M
  VTA: Penitencia Creek Station             2026:6.17M

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  2809                                      2026:6.16M
  2819                                      2026:6.16M
  2820                                      2026:6.16M
  2827                                      2026:6.16M
  2835                                      2026:6.16M
  2842                                      2026:6.16M
  2844                                      2026:6.16M
  2853                                      2026:6.16M
  2856                                      2026:6.16M
  2860                                      2026:6.16M
  2868                                      2026:6.16M
  2890                                      2026:6.16M
  2896                                      2026:6.16M
  2898                                      2026:6.16M
  2918                                      2026:6.16M
  2925                                      2026:6.16M
  2932                                      2026:6.16M
  2944                                      2026:6.17M
  2960                                      2026:6.16M
  2986                                      2026:6.15M
  3491                                      2026:6.19M
  3636                                      2026:6.19M
  3673                                      2026:6.19M
  929                                       2026:6.19M
  930                                       2026:6.19M
  983                                       2026:6.19M
  984                                       2026:6.19M
  985                                       2026:6.19M
  986                                       2026:6.19M
  987                                       2026:6.19M

## what

RACKTYPE: Staple, Galvanized Steel, Surf 63%, Inverted-U, Galvanized Steel,  21%, Inverted-U, Powder-coated Stee 7%, Electronic Bike Locker (for mo 3%, Ribbon, Stainless Steel, In Gr 2%, Ribbon, Stainless Steel, Surfa 2%, Ribbon, Galvanized Steel, In G 1%, Ribbon, Galvanized Steel, Surf 0%, Lightning Bolt, Stainless Stee 0%, Bike ribbon, Stainless Steel,  0%, ribbon, stainless, core mount 0%

NUMBEROFRACKS: 1 83%, 2 7%, 4 3%, 6 1%, 3 1%, 10 1%, 8 1%, 5 1%, 20 0%, 15 0%, 7 0%, 16 0%

BIKECAPACITY: 2 76%, 4 8%, 5 3%, 8 2%, 11 2%, 7 2%, 12 2%, 6 2%, 10 1%, 20 1%, 9 1%, 16 1%

YEARINSTALLED: 2008 27%, 2012 22%, 2016 13%, 2020 9%, 2013 8%, 2010 7%, 2018 6%, 2017 4%, 2011 2%, 2021 1%, 2009 0%

COUNCILDISTRICT: 3 61%, 6 22%, 5 6%, 8 3%, 10 2%, 1 2%, 7 2%, 9 1%, 4 1%, 2 0%

LOCATION: Downtown 72%, Park 11%, School 6%, Transit 3%, Library 3%, Community Center 2%, City Hall 1%, Municipal 1%, Stadium 1%, In-street Corral 0%

LASTUPDATE: 2019/12/19 23:57:34+00 33%, 2019/12/19 23:57:33+00 29%, 2019/12/19 23:57:35+00 27%, 2022/02/10 00:45:41+00 2%, 2021/02/12 01:00:43+00 2%, 2021/02/12 01:00:46+00 1%, 2021/02/12 01:00:45+00 1%, 2021/02/12 01:00:44+00 1%, 2021/05/14 00:04:20+00 1%, 2021/02/12 01:00:42+00 1%, 2022/02/10 00:45:40+00 1%, 2021/02/12 01:02:30+00 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 943 | 0 | 6159010.85661575 7; 6163969.44709225 7; 6156617.96048291 7; 6172773.36517991 6 |
| Y | amount | 934 | 0 | 1943297.51726565 7; 1947737.84073406 7; 1951620.18205073 7; 1952909.8021749 7 |
| OBJECTID | id | 1.1K | 0 | 4289 6; 4288 6; 4287 6; 4286 6 |
| RACKID | other | 934 | 20 | 0 106; 958 5; 957 5; 956 5 |
| RACKTYPE | category | 18 | 21 | Staple, Galvanized Steel, 649; Inverted-U, Galvanized St 218; Inverted-U, Powder-coated 76; Electronic Bike Locker (f 33 |
| NUMBEROFRACKS | category | 19 | 3 | 1 873; 2 71; 4 29; 6 15 |
| BIKECAPACITY | category | 24 | 1 | 2 793; 4 83; 5 28; 8 24 |
| YEARINSTALLED | category | 12 | 177 | 2008 243; 2012 192; 2016 112; 2020 84 |
| FUNDINGSOURCE | who | 56 | 143 | Transportation Fund for C 595; TDA 3 129; TFCA 96; Redevelopment Agency 39 |
| COUNCILDISTRICT | category | 11 | 1 | 3 645; 6 237; 5 59; 8 28 |
| LOCATION | category | 18 | 593 | Downtown 336; Park 52; School 28; Transit 15 |
| FACILITYID | who | 1.1K | 0 | 1010 6; 1009 6; 1008 6; 1007 6 |
| INTID | id | 1.1K | 0 | 1010 6; 1009 6; 1008 6; 1007 6 |
| LONGITUDE | amount | 973 | 1 | -121.88503248 7; -121.86817387 7; -121.8935271 7; -121.83597906 6 |
| LATITUDE | amount | 973 | 1 | 37.33585118 7; 37.34671308 7; 37.34995669 7; 37.2401751 6 |
| CREATIONDATE | empty | 1 | 1.1K |  |
| LASTUPDATE | category | 21 | 0 | 2019/12/19 23:57:34+00 346; 2019/12/19 23:57:33+00 306; 2019/12/19 23:57:35+00 278; 2022/02/10 00:45:41+00 24 |
| NOTES | empty | 2 | 1.1K |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:49:47.75624 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3f62b0cf-2d4b-446f-890e-0 1.1K |
| SRC_SHA256 | who | 1 | 0 | d7490a52a077d0f93f6930459 1.1K |
