# PORTAL_SOC_UTAH_OPEN_DATA_P_3967E73A16

rows 2.0K  columns 28  scan 6.0s

roles: amount 4, audit 2, category 5, date 3, id 3, other 6, who 6

## when

CERTIFICATE_DT
  1990        24  ###
  1991         2  
  1993         6  #
  1994         2  
  1995        22  ###
  1996        12  ##
  1997         9  #
  1998        10  #
  1999        14  ##
  2000        24  ###
  2001        42  ######
  2002        71  ##########
  2003        64  #########
  2004        65  #########
  2005       113  ################
  2006       102  ###############
  2007        80  ############
  2008        51  #######
  2009        16  ##
  2010        11  ##
  2011        10  #
  2012        60  #########
  2013        11  ##
  2014        10  #
  2015        61  #########
  2016        66  ##########
  2017        54  ########
  2018        91  #############
  2019       178  ##########################
  2020       208  ##############################
  2021       186  ###########################
  2022       182  ##########################
  2023        25  ####

PATENT_DT
  1990        23  ###
  1991         2  
  1993         1  
  1994         6  #
  1995         7  #
  1996        21  ###
  1997         9  #
  1998        10  #
  1999        11  ##
  2000        28  ####
  2001        40  ######
  2002        72  ###########
  2003        77  ###########
  2004       116  #################
  2005       129  ###################
  2006        85  #############
  2007        75  ###########
  2008        36  #####
  2009         1  
  2010         9  #
  2011        12  ##
  2012         7  #
  2013        18  ###
  2014        30  ####
  2015        68  ##########
  2016        67  ##########
  2017        93  ##############
  2018        90  #############
  2019       183  ###########################
  2020       201  ##############################
  2021       193  #############################
  2022       156  #######################
  2023         9  #

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LOT_PRICE | 1.9K | -2.0K | 16.2K | 146.3K | 443.8K | 42.39M |
| LSEACRES | 2.0K | 0 | 0.18 | 3.96 | 34.70 | 723.69 |
| SHAPE_STAREA | 2.0K | 3.12 | 718.21 | 15.6K | 139.7K | 2.85M |
| SHAPE_STLENGTH | 2.0K | 9.98 | 111.17 | 1.9K | 9.7K | 342.9K |

## who

LOT_DESCR by rows
       705  nan
        19  Townhome
        18  Duplex
         5  Lot 33
         5  Roads
         5  Lot 2
         5  Lot 3
         4  Lot 26
         4  Common Area
         4  Lot 17
         4  Lot 19
         3  Lot 35
         3  Lot 9
         3  Lot 38
         3  Lot 29
         3  Lot 102
         3  Lot 129
         3  Lot 6
         3  Lot 171
         3  Lot 132

LOT_DESCR by dollars
      16.98M      705 rows  nan
      443.8K        1 rows  Book Value: $443,786.16
      419.8K        1 rows  Book Value: $419,787.04
      386.0K        1 rows  CORAL CANYON PHASE 1 - PARCEL G (OFFICE)
      350.0K        1 rows  PARCEL 8A OF CANYON GREENS COMMERCIAL
      277.4K        2 rows  Lot 208
      218.0K        3 rows  Lot 30
      195.5K        3 rows  Lot 28
      194.2K        1 rows  Lot 207
      194.0K        3 rows  Lot 36
      189.6K        3 rows  Lot 35
      182.3K        3 rows  Lot 31
      182.2K       18 rows  Duplex
      177.2K        3 rows  Lot 29
      173.4K       19 rows  Townhome
      171.9K        4 rows  Lot 19
      166.5K        1 rows  Lot 217
      163.1K        2 rows  Lot 18
      156.2K        2 rows  Lot 20
      154.4K        1 rows  PARCEL C OF CORAL CANYON, PHASE 1

LEASEGIS by rows
       135  SUBD0.015
        56  SUBD2.0
        48  SUBD10.0
        45  SUBD10.0A
        43  SUBD84.0
        40  SUBD0.030
        34  SUBD0.01
        33  SUBD0.012
        32  SUBD14.0
        32  SUBD0.020
        29  SUBD55.0
        27  SUBD62.0
        26  SUBD124.0
        25  SUBD117.0
        25  SUBD40.0
        24  SUBD98.0
        22  SUBD75.0
        22  SUBD139.0
        21  SUBD59.0
        21  SUBD46.0

LEASEGIS by dollars
       3.13M       45 rows  SUBD10.0A
       1.93M       25 rows  SUBD117.0
       1.38M      135 rows  SUBD0.015
       1.21M       43 rows  SUBD84.0
       1.19M        8 rows  SUBD7.0
       1.01M       15 rows  SUBD36.0
      961.6K        8 rows  SUBD6.0
      863.6K        2 rows  SUBD0.0901
      815.6K       12 rows  SUBD11.0A
      791.4K       19 rows  SUBD12.0
      738.1K       56 rows  SUBD2.0
      668.2K       48 rows  SUBD10.0
      666.2K       27 rows  SUBD62.0
      636.0K       22 rows  SUBD75.0
      613.6K       20 rows  SUBD102.0
      518.3K       15 rows  SUBD43.0
      518.3K        6 rows  SUBD150.0
      509.6K       32 rows  SUBD14.0
      507.4K       16 rows  SUBD0.017
      483.6K        6 rows  SUBD0.026

LABEL by rows
       135  SUBD 0-15
        56  SUBD 2
        48  SUBD 10
        45  SUBD 10-A
        43  SUBD 84
        40  SUBD 0-30
        34  SUBD 0-1
        33  SUBD 0-12
        32  SUBD 14
        32  SUBD 0-20
        29  SUBD 55
        27  SUBD 62
        26  SUBD 124
        25  SUBD 40
        25  SUBD 117
        24  SUBD 98
        22  SUBD 75
        22  SUBD 139
        21  SUBD 59
        21  SUBD 46

LABEL by dollars
       3.13M       45 rows  SUBD 10-A
       1.93M       25 rows  SUBD 117
       1.38M      135 rows  SUBD 0-15
       1.21M       43 rows  SUBD 84
       1.19M        8 rows  SUBD 7
       1.01M       15 rows  SUBD 36
      961.6K        8 rows  SUBD 6
      863.6K        2 rows  SUBD 0-901
      815.6K       12 rows  SUBD 11-A
      791.4K       19 rows  SUBD 12
      738.1K       56 rows  SUBD 2
      668.2K       48 rows  SUBD 10
      666.2K       27 rows  SUBD 62
      636.0K       22 rows  SUBD 75
      613.6K       20 rows  SUBD 102
      518.3K       15 rows  SUBD 43
      518.3K        6 rows  SUBD 150
      509.6K       32 rows  SUBD 14
      507.4K       16 rows  SUBD 0-17
      483.6K        6 rows  SUBD 0-26

DESCR by rows
       135  Coral Canyon Development Phase 1
        93  Highland Park Phase 1 Subdivision
        56  Area 2 - Phase 3 Subdivision of the Coral Canyon Community
        43  Overland Phase "D" Plat 1
        40  Fourteen Fairway Subdivision Phase 1
        34  Ticaboo Subdivision Plat II
        33  Ticaboo Subdivision Plat III 4th amended, Recorded under number 256337
        32  Coral Canyon Area 6 - Phase 1 Subdivision
        32  Casitas At Hidden Valley Amended and Extended
        29  Overland Phase "B", Plat 1
        27  Auburn Hills Phase 1
        26  Sendera at Sienna Hills Phase 2
        25  Casitas at Sienna Hills Phase 3
        25  Desert Color Resort Phase 5
        24  Paseos at Sienna Hills Phase 3
        22  Sage Haven Phase 9
        22  The Cliffs at Sunrise (AMENDED)
        21  Arroyo At Sienna Hills Phase 6
        21  Arroyo At Sienna Hills Phase 3
        20  Escondido at Sienna Hills Phase 3

DESCR by dollars
       3.80M       93 rows  Highland Park Phase 1 Subdivision
       1.93M       25 rows  Desert Color Resort Phase 5
       1.38M      135 rows  Coral Canyon Development Phase 1
       1.21M       43 rows  Overland Phase "D" Plat 1
       1.19M        8 rows  The Cliffs of Snow Canyon - Plat 'H'
       1.01M       15 rows  The Estates at Green Spring
      961.6K        8 rows  Kachina Cliffs Phase 2 - Entrada at Snow Canyon
      954.2K       17 rows  Highland Park Area 4-Phase I Subdivision at the Coral Canyon
      863.6K        2 rows  Grapevine Crossing at Sienna Hills SITLA owns 33,34% (lots 1
      791.4K       19 rows  Estates at Hidden Valley Phase 1
      738.1K       56 rows  Area 2 - Phase 3 Subdivision of the Coral Canyon Community
      666.2K       27 rows  Auburn Hills Phase 1
      636.0K       22 rows  The Cliffs at Sunrise (AMENDED)
      613.6K       20 rows  Overland Phase C Plat 4
      518.3K       15 rows  The Terraces at Green Spring Phase 2
      518.3K        6 rows  Waters Edge at Desert Color Shores
      509.6K       32 rows  Casitas At Hidden Valley Amended and Extended
      507.4K       16 rows  Kwavasa
      483.6K        6 rows  Kachina Cliffs Phase I
      462.4K       13 rows  Reserve At Green Springs Phase 3

## who x when

LOT_DESCR by CERTIFICATE_DT, dollars = LOT_PRICE
  CORAL CANYON PHASE 1 - PARCEL G (OFFICE)  2016:386.0K
  Duplex                                    2016:182.2K
  Lot 102                                   2006:24.9K 2013:32.5K
  Lot 129                                   2006:6.8K 2007:19.1K 2018:42.2K
  Lot 132                                   2006:10.6K 2009:7.8K 2014:38.3K
  Lot 17                                    2005:13.1K 2007:44.5K 2012:13.1K 2015:17.8K
  Lot 171                                   2012:62.7K 2015:33.3K 2016:37.4K
  Lot 19                                    2005:13.1K 2007:33.9K 2012:124.9K
  Lot 2                                     2006:13.1K 2007:29.8K 2008:47.4K 2016:19.6K
  Lot 207                                   2006:194.2K
  Lot 208                                   2007:264.1K 2010:13.3K
  Lot 26                                    2005:13.1K 2007:35.3K 2012:73.1K
  Lot 28                                    2007:130.9K 2010:47.1K 2015:17.5K
  Lot 29                                    2006:13.1K 2007:146.6K 2015:17.5K
  Lot 3                                     2005:13.1K 2007:13.1K 2009:43.4K 2011:20.9K 2021:3.1K
  Lot 30                                    2008:145.8K 2012:54.7K 2015:17.5K
  Lot 31                                    2007:151.7K 2015:30.6K
  Lot 33                                    2005:13.1K 2006:13.1K 2007:73.3K 2015:17.5K
  Lot 35                                    2005:13.1K 2006:176.5K
  Lot 36                                    2006:176.5K 2015:17.5K
  Lot 38                                    2005:19.7K 2012:78.0K
  Lot 6                                     2005:26.2K 2021:3.1K
  Lot 9                                     2005:13.1K 2007:10.7K 2015:13.1K
  PARCEL 8A OF CANYON GREENS COMMERCIAL     2016:350.0K
  Roads                                     2013:1
  Townhome                                  2016:173.4K
  nan                                       2000:40.9K 2001:19.3K 2006:105.0K 2014:45.5K 2015:317.4K 2016:896.6K 2017:1.49M 2018:1.06M 2019:335.5K 2020:1.91M 2021:4.67M 2022:5.50M 2023:592.7K

LEASEGIS by CERTIFICATE_DT, dollars = LOT_PRICE
  SUBD0.01                                  1999:5.4K 2000:1.1K 2001:2.2K 2003:1.5K 2004:0 2006:375 2007:27.4K 2020:2.5K 2021:6.0K
  SUBD0.012                                 1997:2.5K 1999:2.5K 2000:1.2K 2002:3.8K 2003:2.5K 2005:1.2K 2007:4.0K 2015:3.6K 2018:4.8K 2021:55.8K
  SUBD0.015                                 2000:94.1K 2001:280.9K 2002:203.1K 2003:270.9K 2004:5.6K 2005:134.4K 2008:0 2016:386.0K
  SUBD0.017                                 2001:74.4K 2002:244.8K 2003:188.2K
  SUBD0.020                                 2005:212.4K 2006:28.0K
  SUBD0.030                                 2004:125.6K 2005:48.1K 2008:0
  SUBD10.0                                  2006:73.7K 2007:271.2K 2008:131.9K 2009:117.2K 2010:74.3K
  SUBD10.0A                                 2010:47.1K 2011:187.2K 2012:2.65M 2017:121.5K 2018:117.4K
  SUBD102.0                                 2021:405.0K 2022:208.5K
  SUBD11.0A                                 2012:612.4K 2017:203.2K
  SUBD117.0                                 2021:1.70M 2022:228.0K
  SUBD12.0                                  2007:586.2K 2008:158.1K 2009:26.3K 2011:20.9K
  SUBD124.0                                 2021:297.8K
  SUBD139.0                                 2022:260.8K 2023:93.6K
  SUBD14.0                                  2007:151.8K 2008:123.1K 2010:39.2K 2011:48.1K 2012:89.6K 2013:57.8K
  SUBD150.0                                 2022:518.3K
  SUBD2.0                                   2006:725.2K 2007:12.8K 2008:0
  SUBD36.0                                  2016:615.9K 2017:156.0K 2018:240.6K
  SUBD40.0                                  2016:228.0K
  SUBD43.0                                  2017:518.3K
  SUBD46.0                                  2017:343.9K
  SUBD55.0                                  2019:89.9K 2020:82.1K 2022:22.6K
  SUBD59.0                                  2019:367.5K
  SUBD6.0                                   2006:326.7K 2007:429.1K 2008:145.8K 2012:60.0K
  SUBD62.0                                  2019:632.2K 2020:34.0K
  SUBD7.0                                   2006:588.3K 2007:529.3K 2012:72.2K
  SUBD75.0                                  2020:171.0K 2021:222.6K 2022:210.2K 2023:32.2K
  SUBD84.0                                  2022:980.7K 2023:230.5K
  SUBD98.0                                  2020:450.0K

## what

LOT_TYPE_CD: 1 94%, 5 3%, 2 2%, 3 1%, 4 0%

CUSTOMER_NAME: nan 31%, BRENNAN HOLDINGS NO. 200, LLC 17%, DESERT COLOR ST. GEORGE, LLC 14%, IVORY HOMES LTD. 10%, BRENNAN HOLDINGS NO. 100, LLC 7%, IVORY SOUTHERN, LLC 5%, DEVELOPMENT TEAM, LLC 4%, GOLDEN HERITAGE HOMES, INC. 4%, CW CORAL CANYON, LLC 3%, NS CANYON RIDGE 2%, TICABOO RESORT, LLC 2%, THE HOLLOWS LLC 1%

SOLD_STATUS_DESCR: SOLD 98%, NOT SOLD 2%

SUFFIX: nan 77%, 15 8%, A 3%, 30 2%, 1 2%, 12 2%, 20 2%, 28 1%, 2 1%, 18 1%, 31 1%, 34 1%

SUFIX: nan 77%, 15 8%, A 3%, 30 2%, 1 2%, 12 2%, 20 2%, 28 1%, 2 1%, 18 1%, 31 1%, 34 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| THE_GEOM | id | 2.0K | 0 | {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10; {"type": "MultiPolygon",  10 |
| LEASEGIS | who | 162 | 0 | SUBD0.015 135; SUBD2.0 56; SUBD10.0 48; SUBD10.0A 45 |
| LABEL | who | 160 | 0 | SUBD 0-15 135; SUBD 2 56; SUBD 10 48; SUBD 10-A 45 |
| CLASS | other | 1 | 0 | SUBD 2.0K |
| NBR | other | 124 | 0 | 0 565; 10 93; 2 56; 84 43 |
| LOT_REF | other | 735 | 0 | A 52; 2 25; 3 24; 1 21 |
| DESCR | who | 157 | 0 | Coral Canyon Development  135; Highland Park Phase 1 Sub 93; Area 2 - Phase 3 Subdivis 56; Overland Phase "D" Plat 1 43 |
| LOT_PRICE | amount | 992 | 0 | nan 115; 18750 72; 13125 56; 11750 49 |
| LOT_TYPE_CD | category | 5 | 0 | 1 1.9K; 5 51; 2 37; 3 26 |
| APP_DESCR | who | 1 | 0 | DEVELOPMENT SUBDIVISION 2.0K |
| LSEACRES | amount | 175 | 0 | 0.09 106; 0.03 101; 0.04 97; 0.05 85 |
| CUSTOMER_NAME | category | 21 | 0 | nan 602; BRENNAN HOLDINGS NO. 200, 325; DESERT COLOR ST. GEORGE,  265; IVORY HOMES LTD. 202 |
| CERTIFICATE_NBR | other | 1.2K | 0 | nan 89; C-26634-63-00 28; C-26973 26; C-26548 26 |
| CERTIFICATE_DT | date | 896 | 0 | nan 118; 2021-10-25T00:00:00.000Z 39; 2021-05-05T12:00:00.000Z 28; 2019-10-22T00:00:00.000Z 27 |
| PATENT_NBR | other | 1.3K | 0 | nan 92; P-20361-63-00 28; P-20741 27; P-20361-124-00 25 |
| PATENT_DT | date | 467 | 0 | nan 111; 2005-09-16T00:00:00.000Z 53; 2007-01-31T00:00:00.000Z 43; 2003-11-01T00:00:00.000Z 41 |
| SOLD_STATUS_DESCR | category | 2 | 0 | SOLD 2.0K; NOT SOLD 37 |
| CLASSVALUE | other | 1 | 0 | SUBD 2.0K |
| GLOBALID | id | 2.0K | 0 | {1D3518EE-57B0-468C-AE7E- 10; {29C1B52D-AE11-44D8-8CE7- 10; {9C1EAC45-155B-494F-80C7- 10; {1BEAB03D-7392-4F83-A4E9- 10 |
| OBJECTID | id | 2.0K | 0 | 1475255 10; 1475610 10; 1472897 10; 1476798 10 |
| SHAPE_STAREA | amount | 1.9K | 0 | 136.91875315999999 11; 154.2621 10; 196.30889999999999 10; 1681.1556499999999 10 |
| SHAPE_STLENGTH | amount | 2.0K | 0 | 53.845983775955297 11; 55.552076577081692 10; 56.583837708596526 10; 165.29680462122249 10 |
| LOT_DESCR | who | 1.2K | 0 | nan 705; Townhome 19; Duplex 18; Lot 51 8 |
| SUFFIX | category | 38 | 0 | nan 1.4K; 15 135; A 57; 30 40 |
| SUFIX | category | 38 | 0 | nan 1.4K; 15 135; A 57; 30 40 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:10:20.94410 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 6de8a8af-bded-4ef2-af46-6 2.0K |
| SRC_SHA256 | who | 1 | 0 | 3804d5e2517c333c9253a62b2 2.0K |
