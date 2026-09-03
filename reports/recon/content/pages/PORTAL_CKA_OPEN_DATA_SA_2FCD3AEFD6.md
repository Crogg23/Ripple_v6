# PORTAL_CKA_OPEN_DATA_SA_2FCD3AEFD6

rows 1.2K  columns 10  scan 4.0s

roles: amount 2, audit 2, date 3, id 1, who 3

## when

CREATED_DATE
  2017        18  ##
  2018        40  ####
  2019        48  #####
  2020        57  #####
  2021        70  #######
  2022       116  ###########
  2023       104  ##########
  2024       213  ####################
  2025       319  ##############################
  2026       229  ######################

LAST_EDITED_DATE
  2017        12  #
  2018        24  ##
  2019        40  ###
  2020        47  ####
  2021        52  #####
  2022        94  ########
  2023       101  #########
  2024       203  ##################
  2025       346  ##############################
  2026       295  ##########################

INGESTED_AT
  2026      1.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 1.2K | 1.9K | 281.2K | 5.46M | 27.77M | 813.90M |
| SHAPE__LENGTH | 1.2K | 195.40 | 2.6K | 13.2K | 24.8K | 4.08M |

## who

PLATNAME by rows
         3  Reyes Subdivision
         3  Reserve at San Antonio
         2  Borgfeld Commercial Subdivision
         2  Brown St Development
         2  440 Quarry Improvements
         2  Orsinger Oaks
         2  Hidden Burrow Unit 1
         2  Applewhite
         2  Emory Peak North
         2  Mission Park Stone Oak Unit 4
         2  Dove Trails
         2  TTS Gibbs Sprawl
         2  Cedar Grove Subdivisoin Unit 1
         2  Doggett Freightliner
         2  Cibolo Canyon Unit 9C
         2  Northside Islamic Center
         2  Springvale Subdivision Unit 2
         2  Foster Pointe
         2  Forest Oaks MHC
         2  East Sheaarer Hills

PLATNAME by dollars
      27.77M        1 rows  Sasr Foster Road
      22.94M        1 rows  San Medina
      20.33M        2 rows  Pandora Forest
      17.40M        1 rows  Alamo Junction RailPark-Musket
      15.03M        2 rows  440 North Quarry
      10.08M        2 rows  Forest Oaks MHC
       8.47M        1 rows  Quintana Rail Park
       7.85M        1 rows  Vida Master Planned Community District
       6.01M        1 rows  Homestead Subdivision Unit 1 Phase 1
       5.69M        1 rows  Westpointe East 131
       5.51M        1 rows  Bre Phase 1 Unit 2
       5.47M        1 rows  SAT 1
       5.40M        1 rows  Camino Real Subdivision Unit 1
       5.38M        1 rows  ECIS High School 2
       5.09M        1 rows  Mathis Park Subdivision
       4.64M        1 rows  Luensmann Unit 1A
       4.59M        1 rows  BFS Campus
       4.41M        1 rows  McCombs Lookout At 1604
       4.35M        1 rows  Kinder West Unit 14
       4.24M        1 rows  Alamar Phase Two

PLATNUMBER by rows
       964  0
         1  1911800206
         1  2016000540
         1  1911800194
         1  2110200007
         1  2111800183
         1  2111800427
         1  2018000368
         1  2011800122
         1  2110200012
         1  2011800514
         1  2017000485
         1  1911800145
         1  2016000317
         1  2011800322
         1  2111800433
         1  1911800188
         1  2018000134
         1  1811800137
         1  2017000424

PLATNUMBER by dollars
     662.70M      964 rows  0
      22.94M        1 rows  2111800224
      17.40M        1 rows  1911800211
       3.89M        1 rows  2011800108
       3.83M        1 rows  2111800475
       3.17M        1 rows  2018000102
       2.76M        1 rows  2011800446
       2.49M        1 rows  2111800092
       2.43M        1 rows  1911800145
       1.91M        1 rows  2018000330
       1.82M        1 rows  2011800178
       1.76M        1 rows  2111800627
       1.69M        1 rows  2111800371
       1.62M        1 rows  2111800455
       1.61M        1 rows  2010200095
       1.61M        1 rows  2018000406
       1.58M        1 rows  1911800435
       1.57M        1 rows  2111800273
       1.51M        1 rows  2016000383
       1.46M        1 rows  2110200069

SRC_SHA256 by rows
      1.2K  aad36fcff50d8c36702a162eb0b1f13b66dfd95fb66423604736cf5caaedcd91

SRC_SHA256 by dollars
     813.90M     1.2K rows  aad36fcff50d8c36702a162eb0b1f13b66dfd95fb66423604736cf5caaed

## who x when

PLATNAME by CREATED_DATE, dollars = SHAPE__AREA
  440 North Quarry                          2024:7.52M 2025:7.52M
  440 Quarry Improvements                   2024:214.7K 2025:377.4K
  Alamo Junction RailPark-Musket            2019:17.40M
  Applewhite                                2023:177.1K 2025:177.1K
  Borgfeld Commercial Subdivision           2021:175.3K 2026:318.2K
  Bre Phase 1 Unit 2                        2026:5.51M
  Brown St Development                      2020:12.8K 2023:12.8K
  Cedar Grove Subdivisoin Unit 1            2024:699.5K 2025:699.5K
  Cibolo Canyon Unit 9C                     2022:1.60M 2026:328.5K
  Doggett Freightliner                      2019:699.6K 2025:1.53M
  Dove Trails                               2025:526.8K
  East Sheaarer Hills                       2025:39.0K
  Emory Peak North                          2023:397.1K 2025:397.1K
  Forest Oaks MHC                           2022:5.04M 2025:5.04M
  Foster Pointe                             2024:391.1K 2026:391.1K
  Hidden Burrow Unit 1                      2023:1.15M 2024:1.27M
  Homestead Subdivision Unit 1 Phase 1      2024:6.01M
  Mission Park Stone Oak Unit 4             2022:145.4K 2025:145.4K
  Northside Islamic Center                  2022:320.8K 2025:308.9K
  Orsinger Oaks                             2024:54.0K 2026:54.0K
  Pandora Forest                            2022:10.17M 2025:10.17M
  Quintana Rail Park                        2025:8.47M
  Reserve at San Antonio                    2023:693.7K 2024:696.6K 2025:696.6K
  Reyes Subdivision                         2022:167.9K 2026:84.0K
  San Medina                                2021:22.94M
  Sasr Foster Road                          2026:27.77M
  Springvale Subdivision Unit 2             2023:98.6K 2026:98.6K
  TTS Gibbs Sprawl                          2024:461.3K 2025:461.3K
  Vida Master Planned Community District    2026:7.85M
  Westpointe East 131                       2026:5.69M

PLATNUMBER by CREATED_DATE, dollars = SHAPE__AREA
  0                                         2022:79.24M 2023:61.89M 2024:149.95M 2025:211.86M 2026:159.75M
  1811800137                                2019:42.9K
  1911800145                                2019:2.43M
  1911800188                                2019:178.0K
  1911800194                                2019:216.9K
  1911800206                                2019:699.6K
  1911800211                                2019:17.40M
  2011800108                                2021:3.89M
  2011800122                                2020:252.5K
  2011800178                                2020:1.82M
  2011800322                                2020:176.5K
  2011800446                                2020:2.76M
  2011800514                                2020:895.3K
  2016000317                                2017:669.8K
  2016000540                                2017:25.4K
  2017000424                                2017:360.3K
  2017000485                                2018:850.3K
  2018000102                                2018:3.17M
  2018000134                                2018:143.8K
  2018000330                                2019:1.91M
  2018000368                                2018:123.7K
  2110200007                                2021:12.8K
  2110200012                                2021:4.6K
  2111800092                                2021:2.49M
  2111800183                                2021:88.9K
  2111800224                                2021:22.94M
  2111800427                                2021:107.4K
  2111800433                                2021:43.6K
  2111800475                                2022:3.83M
  2111800627                                2022:1.76M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.2K | 0 | 1214 7; 1213 7; 1212 7; 1211 7 |
| PLATNUMBER | who | 252 | 0 | 0 964; 2011800294 2; 2011800197 2; 2111800313 2 |
| PLATNAME | who | 1.2K | 2 | Wurzbach Duplex 7; Gabriels Place Lot 18 7; Green Mountain 11 and 12 7; Mesquite Ridge Unit 2 7 |
| CREATED_DATE | date | 1.2K | 0 | 1/10/2025 5:49:43 PM 7; 11/6/2020 3:28:09 PM 7; 10/18/2024 3:43:22 PM 7; 11/22/2024 2:20:58 PM 7 |
| LAST_EDITED_DATE | date | 1.2K | 0 | 1/10/2025 5:49:43 PM 7; 11/6/2020 3:28:52 PM 7; 10/18/2024 3:43:22 PM 7; 2/28/2025 4:15:50 PM 7 |
| SHAPE__AREA | amount | 1.2K | 0 | 136162.21875 7; 172943.862148214 7; 1535549.07617188 7; 1217143.40429688 7 |
| SHAPE__LENGTH | amount | 1.2K | 0 | 2386.56687250465 7; 1704.07141963005 7; 6460.33707301494 7; 4451.54661686934 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:51:30.14087 1.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 6744fa12-9084-4fb4-aede-4 1.2K |
| SRC_SHA256 | who | 1 | 0 | aad36fcff50d8c36702a162eb 1.2K |
