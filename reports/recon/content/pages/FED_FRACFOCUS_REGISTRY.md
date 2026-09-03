# FED_FRACFOCUS_REGISTRY

rows 7.20M  columns 34  scan 17.2s

roles: amount 6, audit 2, category 7, date 3, id 1, other 2, who 14

## when

JOBSTARTDATE
  1955         1  
  1982         1  
  1995         1  
  1996         1  
  2001        21  
  2002       116  
  2004        59  
  2005        55  
  2007       151  
  2008       142  
  2009        71  
  2010       658  
  2011     22.2K  #
  2012     87.9K  ##
  2013    842.8K  #######################
  2014     1.11M  ##############################
  2015    647.2K  #################
  2016    391.2K  ###########
  2017    601.9K  ################
  2018    675.1K  ##################
  2019    589.8K  ################
  2020    290.2K  ########
  2021    380.3K  ##########
  2022    426.2K  ###########
  2023    383.2K  ##########
  2024    336.0K  #########
  2025    303.2K  ########
  2026    109.3K  ###

JOBENDDATE
  1955         1  
  1982         1  
  1995         1  
  1996         1  
  2001         1  
  2002        41  
  2008         2  
  2009        50  
  2010       469  
  2011     21.1K  #
  2012     84.2K  ##
  2013    834.5K  #######################
  2014     1.11M  ##############################
  2015    655.3K  ##################
  2016    388.3K  ###########
  2017    592.1K  ################
  2018    679.4K  ##################
  2019    593.6K  ################
  2020    294.3K  ########
  2021    377.4K  ##########
  2022    421.3K  ###########
  2023    388.9K  ###########
  2024    336.2K  #########
  2025    304.5K  ########
  2026    121.2K  ###

_INGESTED_AT
  2026     7.20M  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 7.20M | -81.20 | 32.47 | 48.44 | 70.51 | 254.26M |
| LONGITUDE | 7.20M | -170.91 | -101.91 | -76.25 | 103.26 | -721.14M |
| TOTALBASEWATERVOLUME | 7.17M | 0 | 7.70M | 38.28M | 472.44M | 72511.03B |
| TOTALBASENONWATERVOLUME | 6.96M | -11.53M | 0 | 968.7K | 3.51B | 926.87B |
| PERCENTHIGHADDITIVE | 6.38M | 0 | 10 | 100.00 | 100 | 182.90M |
| MASSINGREDIENT | 6.26M | -23.1K | 170.86 | 105.60M | 18791644.66B | 21391861.37B |

## who

WELLNAME by rows
       779  4H
       488  DEEP CREEK 9-15-4-2E
       414  Alexander #1
       408  NAPU #112R
       336  Wiltcher GU #7
       336  JC RS McKinley
       320  Nell Hudson 14
       312  Embar -B- 0601H
       294  FEDERAL 12 2H
       292  Martinez North D 102H
       279  0075LS
       275  Martinez North D 103H
       272  State 36-1-P
       265  Amy #1-6
       265  N-80R
       258  Oxsheer J19 (SA) 6 6H
       255  Gardendale 5-16
       251  COLBURN #3H
       248  Stokes 21 #1
       247  WEYERHAEUSER CO 15 002

WELLNAME by dollars
      18.73B       86 rows  BROOK B-3F 6H
      16.54B       35 rows  Lowe 26 #2H
      15.83B       54 rows  Fortress of Solitude 16-9-4 H 2LS
      12.89B       64 rows  Kriti C3-6-7 TWF3 2403H
      12.53B       35 rows  BPX GW DG UNIT 5-GW DG UNIT 1 SA 1H
      11.40B      779 rows  4H
      10.35B       55 rows  USA 146-97-29B-32-2H
       9.44B       69 rows  CHUPACABRA 1213-7-1H
       7.73B       35 rows  BLACKWELL A-DLUGOSCH A SA 7  7H
       7.62B      146 rows  JOHNSON24-7H
       7.00B       38 rows  Rosalie E 6-3 252
       7.00B      292 rows  Martinez North D 102H
       6.76B       61 rows  BLIKRE 158-93-6B-7-2H
       6.50B      231 rows  WHITWELL G 119H
       6.48B       35 rows  HSC 320A 512HE
       6.48B       71 rows  Wilson D 5H
       6.46B       45 rows  WR Lacebark Elm Unit #6HB
       6.29B       61 rows  WILSON Federal 31-15-2H
       5.90B       17 rows  Eiswerth 17-8HC 002-ALT
       5.79B       29 rows  PROSPER FARMS 04-65 14-13 03BH

TRADENAME by rows
     1.86M  Ingredient Container
    560.0K  Other Chemical(s)
    129.2K  Water
     46.4K  Other Ingredients
     43.7K  Fresh Water
     36.1K  Sand
     34.1K  Ingredients in Additive(s) (MSDS and non-MSDS)
     32.1K  FRW-200
     29.4K  ACI-97
     24.6K  NE-227
     24.2K  CI-150
     23.3K  Proppant Transport
     23.2K  LoSurf-300D
     21.5K  NE116-Plexbreak 116
     19.9K  Sand (Proppant)
     17.0K  IC5-Iron Control
     16.6K  PLEXGEL 907 L-EB
     16.1K  Hydrochloric Acid
     15.8K  VICON NF BREAKER
     15.0K  SG-15G

TRADENAME by dollars
   24111.33B    1.86M rows  Ingredient Container
    9443.97B   560.0K rows  Other Chemical(s)
    1467.28B   129.2K rows  Water
     441.08B    36.1K rows  Sand
     427.29B    43.7K rows  Fresh Water
     394.43B    29.4K rows  ACI-97
     387.26B    21.5K rows  NE116-Plexbreak 116
     248.63B    32.1K rows  FRW-200
     232.18B    17.0K rows  IC5-Iron Control
     218.83B    12.4K rows  Crystalline Silica Quartz / US Silica
     200.02B    24.2K rows  CI-150
     198.51B    46.4K rows  Other Ingredients
     197.37B    24.6K rows  NE-227
     179.88B    19.9K rows  Sand (Proppant)
     179.14B    16.1K rows  Hydrochloric Acid
     173.91B    12.3K rows  HA04-10-15% HCL
     173.36B    12.2K rows  OptiKleen-WF(TM)
     173.22B    34.1K rows  Ingredients in Additive(s) (MSDS and non-MSDS)
     161.14B    14.3K rows  15% HCL
     153.34B     6.1K rows  Clearal 268

INGREDIENTNAME by rows
    559.7K  Water
    173.5K  Methanol
     67.8K  Ethanol
     66.2K  Ethylene Glycol
     64.7K  Glutaraldehyde
     62.7K  Crystalline silica, quartz
     60.9K  Hydrochloric Acid
     57.4K  Proprietary
     54.1K  Isopropanol
     53.3K  Sodium chloride
     49.2K  Hydrochloric acid
     45.6K  WATER
     45.1K  Sodium Chloride
     44.1K  Sodium Hydroxide
     41.0K  Ammonium Persulfate
     37.9K  Sodium hydroxide
     37.0K  Ammonium chloride
     34.6K  Guar gum
     34.3K  Acetic acid
     33.5K  Hydrogen Chloride

INGREDIENTNAME by dollars
    5974.40B   559.7K rows  Water
    1668.20B   173.5K rows  Methanol
     802.46B    67.8K rows  Ethanol
     769.32B    64.7K rows  Glutaraldehyde
     662.79B    60.9K rows  Hydrochloric Acid
     588.26B    62.7K rows  Crystalline silica, quartz
     565.76B    49.2K rows  Hydrochloric acid
     543.33B    66.2K rows  Ethylene Glycol
     532.37B    57.4K rows  Proprietary
     485.67B    54.1K rows  Isopropanol
     476.32B    53.3K rows  Sodium chloride
     446.18B    28.9K rows  Distillates (petroleum), hydrotreated light
     433.64B    44.1K rows  Sodium Hydroxide
     426.00B    37.9K rows  Sodium hydroxide
     413.14B    37.0K rows  Ammonium chloride
     412.91B    33.5K rows  Hydrogen Chloride
     405.93B    45.1K rows  Sodium Chloride
     404.29B    32.2K rows  Acetic Acid
     384.20B    32.3K rows  Citric Acid
     374.98B    22.8K rows  Ethoxylated alcohols

OPERATORNAME by rows
    375.2K  Pioneer Natural Resources
    206.6K  XTO Energy/ExxonMobil
    200.7K  Chesapeake Operating, Inc.
    194.6K  EOG Resources, Inc.
    185.7K  Occidental Oil and Gas
    171.9K  Anadarko Petroleum Corporation
    166.8K  Devon Energy Production Company L. P.
    160.6K  ConocoPhillips Company/Burlington Resources
    149.2K  Marathon Oil
    146.8K  Continental Resources, Inc
    122.5K  COG Operating LLC
    115.2K  Apache Corporation
    108.7K  Chevron USA Inc.
    100.1K  Whiting Petroleum
     90.4K  Noble Energy, Inc.
     90.1K  Diamondback E&P LLC
     87.4K  Newfield Exploration
     84.4K  PDC Energy
     78.0K  EP Energy
     71.5K  Aera Energy LLC

OPERATORNAME by dollars
    6528.21B   375.2K rows  Pioneer Natural Resources
    2280.30B   194.6K rows  EOG Resources, Inc.
    2099.40B   206.6K rows  XTO Energy/ExxonMobil
    1785.17B    90.1K rows  Diamondback E&P LLC
    1776.76B   122.5K rows  COG Operating LLC
    1772.26B   146.8K rows  Continental Resources, Inc
    1538.02B   200.7K rows  Chesapeake Operating, Inc.
    1528.22B   185.7K rows  Occidental Oil and Gas
    1300.85B   166.8K rows  Devon Energy Production Company L. P.
    1263.73B   108.7K rows  Chevron USA Inc.
    1184.74B   160.6K rows  ConocoPhillips Company/Burlington Resources
    1171.88B   171.9K rows  Anadarko Petroleum Corporation
    1160.73B    90.4K rows  Noble Energy, Inc.
    1142.21B    71.5K rows  MEWBOURNE OIL COMPANY
    1105.97B    62.0K rows  SM Energy
    1007.55B   149.2K rows  Marathon Oil
     916.94B    52.4K rows  EQT Production
     901.15B    54.1K rows  Antero Resources Corporation
     849.23B    53.5K rows  Cimarex Energy Co.
     836.49B   115.2K rows  Apache Corporation

## who x when

WELLNAME by JOBSTARTDATE, dollars = TOTALBASEWATERVOLUME
  0075LS                                    2019:3.44B
  4H                                        2019:11.40B
  Alexander #1                              2013:78.21M 2014:19.34M 2015:184.4K
  Amy #1-6                                  2013:13.66M
  BLACKWELL A-DLUGOSCH A SA 7  7H           2025:7.73B
  BPX GW DG UNIT 5-GW DG UNIT 1 SA 1H       2025:12.53B
  BROOK B-3F 6H                             2025:18.73B
  CHUPACABRA 1213-7-1H                      2017:9.44B
  COLBURN #3H                               2014:1.74B
  DEEP CREEK 9-15-4-2E                      2014:27.20M
  Embar -B- 0601H                           2018:1.79B
  FEDERAL 12 2H                             2014:184.61M
  Fortress of Solitude 16-9-4 H 2LS         2022:15.83B
  Gardendale 5-16                           2013:350.97M
  JC RS McKinley                            2014:14.13M
  JOHNSON24-7H                              2018:7.62B
  Kriti C3-6-7 TWF3 2403H                   2019:12.89B
  Lowe 26 #2H                               2016:16.54B
  Martinez North D 102H                     2019:7.00B
  Martinez North D 103H                     2019:5.28B
  N-80R                                     2014:5.00M 2017:826.7K
  NAPU #112R                                2015:10.65M
  Nell Hudson 14                            2013:13.58M
  Oxsheer J19 (SA) 6 6H                     2017:2.78B
  Rosalie E 6-3 252                         2019:7.00B
  State 36-1-P                              2014:9.47M
  Stokes 21 #1                              2014:379.81M
  USA 146-97-29B-32-2H                      2024:10.35B
  WEYERHAEUSER CO 15 002                    2017:74.09M
  Wiltcher GU #7                            2013:74.23M 2014:296.08M

TRADENAME by JOBSTARTDATE, dollars = TOTALBASEWATERVOLUME
  15% HCL                                   2011:37.08M 2012:228.99M 2013:2.42B 2014:6.65B 2015:8.48B 2016:7.07B 2017:12.84B 2018:16.58B 2019:20.72B 2020:13.00B 2021:13.24B 2022:16.22B 2023:18.07B 2024:9.11B 2025:7.27B 2026:9.22B
  ACI-97                                    2016:6.93B 2017:48.96B 2018:64.40B 2019:73.69B 2020:53.06B 2021:70.28B 2022:43.43B 2023:33.28B 2024:86.30M 2025:165.94M
  CI-150                                    2011:144.75M 2012:4.06B 2013:35.43B 2014:51.70B 2015:46.39B 2016:27.48B 2017:10.76B 2018:11.21B 2019:11.58B 2020:947.88M 2023:80.25M 2024:224.56M 2025:1.77M
  Clearal 268                               2015:20.72M 2018:380.06M 2019:9.95B 2020:20.87B 2021:20.91B 2022:31.78B 2023:25.74B 2024:17.77B 2025:17.00B 2026:8.91B
  Crystalline Silica Quartz / US Silica     2017:9.44B 2018:22.97B 2019:30.65B 2020:17.37B 2021:41.47B 2022:55.81B 2023:41.05B
  FRW-200                                   2011:80.53M 2012:954.15M 2013:48.13B 2014:81.15B 2015:75.32B 2016:29.53B 2017:5.21B 2018:4.54B 2019:3.18B 2020:64.49M 2023:454.73M
  Fresh Water                               2010:5.15M 2011:150.18M 2012:755.17M 2013:15.73B 2014:26.20B 2015:26.28B 2016:26.34B 2017:44.29B 2018:57.10B 2019:52.10B 2020:23.63B 2021:26.35B 2022:31.66B 2023:31.05B 2024:26.15B 2025:27.85B 2026:11.60B
  HA04-10-15% HCL                           2011:25.22M 2012:76.80M 2013:31.64M 2014:2.97B 2015:5.61B 2016:6.09B 2017:13.97B 2018:22.37B 2019:38.38B 2020:16.28B 2021:25.96B 2022:22.71B 2023:13.05B 2024:5.44B 2025:968.86M
  Hydrochloric Acid                         2008:93.5K 2011:60.96M 2012:401.92M 2013:9.09B 2014:14.01B 2015:7.52B 2016:7.83B 2017:9.46B 2018:13.91B 2019:12.99B 2020:9.48B 2021:11.80B 2022:15.07B 2023:16.27B 2024:25.19B 2025:23.24B 2026:2.83B
  IC5-Iron Control                          2011:37.83M 2012:115.20M 2013:80.04M 2014:4.83B 2015:7.48B 2016:9.12B 2017:20.95B 2018:33.55B 2019:59.03B 2020:29.40B 2021:44.89B 2022:10.74B 2023:7.40B 2024:4.56B
  Ingredient Container                      1955:1 1982:1 1995:1 1996:1 2001:19.26M 2002:790.19M 2004:6.06M 2005:66.2K 2007:2.12B 2008:222.80M 2009:160.95M 2010:169.73M 2011:2.35B 2012:23.43B 2013:82.27B 2014:115.92B 2015:115.36B 2016:993.92B 2017:3011.57B 2018:3673.12B 2019:3393.11B 2020:1716.03B 2021:1878.75B 2022:2204.16B 2023:2136.58B 2024:1954.58B 2025:1943.72B 2026:858.76B
  Ingredients in Additive(s) (MSDS and non  2011:338.5K 2012:28.77M 2013:2.05B 2014:77.90B 2015:91.26B 2016:1.97B 2020:46.4K 2022:27.7K
  LoSurf-300D                               2010:13.27M 2011:795.89M 2012:2.51B 2013:24.58B 2014:26.58B 2015:4.86B 2016:116.90M 2018:27.97M 2019:5.19B 2020:3.38B 2021:4.40B 2022:6.40B 2023:7.99B 2024:2.66B 2025:1.09B 2026:715.55M
  NE-227                                    2012:19.30M 2013:2.19B 2014:3.16B 2015:3.01B 2016:4.40B 2017:12.20B 2018:16.61B 2019:23.65B 2020:31.46B 2021:38.14B 2022:36.33B 2023:11.57B 2024:4.30B 2025:6.30B 2026:4.04B
  NE116-Plexbreak 116                       2016:5.27B 2017:27.37B 2018:44.74B 2019:78.71B 2020:39.20B 2021:57.52B 2022:53.45B 2023:43.59B 2024:34.50B 2025:2.66B 2026:265.80M
  OptiKleen-WF(TM)                          2011:32.51M 2012:25.79M 2013:47.28M 2014:1.14B 2015:3.15B 2016:7.72B 2017:20.72B 2018:26.92B 2019:25.12B 2020:11.42B 2021:16.62B 2022:18.65B 2023:14.83B 2024:10.14B 2025:11.80B 2026:5.01B
  Other Chemical(s)                         2012:101.55M 2013:14.05M 2014:410.88M 2015:1.45B 2016:102.82B 2017:329.90B 2018:375.72B 2019:849.22B 2020:709.15B 2021:1017.77B 2022:1178.77B 2023:1149.00B 2024:1612.37B 2025:1715.70B 2026:401.58B
  Other Ingredients                         2011:170.63M 2012:1.96B 2013:26.80B 2014:58.54B 2015:44.54B 2016:26.36B 2017:21.11M 2018:9.50M 2019:1.70M 2020:1.20B 2021:1.33M 2022:1.31B 2024:35.79B 2025:1.80B
  PLEXGEL 907 L-EB                          2008:209.7K 2013:272.68M 2014:266.70M 2015:64.24M 2016:95.93M 2017:278.70M 2018:238.45M 2019:277.45M 2020:180.35M 2021:228.71M 2022:160.67M 2023:153.26M 2024:148.10M 2025:447.52M 2026:21.95M
  Proppant Transport                        2013:54.09M 2014:34.71B 2015:60.22B 2016:8.22B
  SG-15G                                    2012:8.53M 2013:211.40M 2014:3.13B 2015:3.58B 2016:4.10B 2017:7.59B 2018:6.16B 2019:3.83B 2020:903.72M 2021:617.09M 2022:2.52B 2023:2.16B 2024:753.31M 2025:482.96M 2026:208.77M
  Sand                                      2005:66.2K 2008:206.8K 2009:8.17M 2011:157.71M 2012:643.50M 2013:12.47B 2014:19.14B 2015:14.07B 2016:16.02B 2017:25.93B 2018:40.36B 2019:45.35B 2020:29.76B 2021:35.23B 2022:42.97B 2023:48.05B 2024:52.13B 2025:45.10B 2026:13.67B
  Sand (Proppant)                           2010:10.36M 2011:468.3K 2012:578.19M 2013:8.33B 2014:14.15B 2015:10.92B 2016:7.56B 2017:16.70B 2018:19.60B 2019:16.29B 2020:11.48B 2021:11.10B 2022:16.36B 2023:15.45B 2024:13.09B 2025:13.53B 2026:4.74B
  VICON NF BREAKER                          2010:8.48M 2011:237.74M 2012:724.10M 2013:11.07B 2014:20.03B 2015:10.45B 2016:5.39B 2017:10.53B 2018:11.18B 2019:7.87B 2020:4.04B 2021:5.00B 2022:4.66B 2023:3.13B 2024:2.06B 2025:2.21B 2026:649.13M
  Water                                     2001:19.26M 2002:86.49M 2004:1.43M 2005:66.2K 2007:54.46M 2008:10.53M 2009:8.22M 2010:10.36M 2011:428.89M 2012:2.63B 2013:34.38B 2014:62.75B 2015:47.34B 2016:49.08B 2017:94.83B 2018:126.74B 2019:132.35B 2020:81.99B 2021:126.65B 2022:156.70B 2023:158.59B 2024:166.96B 2025:167.49B 2026:58.06B

## what

STATENAME: Texas 51%, Oklahoma 9%, North Dakota 9%, Colorado 8%, New Mexico 6%, Pennsylvania 4%, Utah 3%, Wyoming 3%, Louisiana 2%, Ohio 2%, West Virginia 2%, California 1%

PROJECTION: NAD27 58%, NAD83 40%, WGS84 2%, Nad27 0%, Nad83 0%

FFVERSION: 3 48%, 2 39%, 4 13%, 1 1%

FEDERALWELL: False 92%, True 8%

INDIANWELL: False 99%, True 1%

INGREDIENTMSDS: True 79%, False 21%

_SRC_FILE: FracFocusRegistry_8.csv 8%, FracFocusRegistry_5.csv 8%, FracFocusRegistry_7.csv 8%, FracFocusRegistry_6.csv 8%, FracFocusRegistry_12.csv 8%, FracFocusRegistry_3.csv 8%, FracFocusRegistry_4.csv 8%, FracFocusRegistry_11.csv 8%, FracFocusRegistry_2.csv 8%, FracFocusRegistry_13.csv 8%, FracFocusRegistry_9.csv 8%, FracFocusRegistry_10.csv 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DISCLOSUREID | who | 247.6K | 0 | 89a9b69f-f86e-442e-a544-d 5.1K; e3bd8ea6-eba4-4404-94a7-6 5.1K; f3cb47d4-4f70-4731-a7f0-a 5.1K; 87cd0473-8bda-470d-8df9-5 5.1K |
| JOBSTARTDATE | date | 69.4K | 713 | 11/4/2019 6:00:00 AM 9.1K; 11/5/2019 6:00:00 AM 8.8K; 11/3/2019 5:00:00 AM 8.8K; 11/6/2019 12:00:00 AM 8.7K |
| JOBENDDATE | date | 71.2K | 0 | 7/16/2013 12:00:00 AM 7.1K; 7/30/2013 12:00:00 AM 7.0K; 7/24/2013 12:00:00 AM 6.9K; 7/26/2013 12:00:00 AM 6.9K |
| APINUMBER | who | 237.6K | 0 | 42127379380000 5.1K; 42285340600000 5.1K; 49009432360000 5.1K; 42329419640000 5.1K |
| STATENAME | category | 26 | 0 | Texas 3.63M; Oklahoma 647.3K; North Dakota 610.5K; Colorado 563.2K |
| COUNTYNAME | who | 533 | 89 | Weld 431.3K; Midland 325.3K; Martin 272.0K; McKenzie 227.3K |
| OPERATORNAME | who | 2.0K | 0 | Pioneer Natural Resources 375.2K; XTO Energy/ExxonMobil 206.6K; Chesapeake Operating, Inc 200.7K; EOG Resources, Inc. 194.6K |
| WELLNAME | who | 237.7K | 0 | Carol-Robin (SA) Unit 2 2 5.1K; SPILLMAN DRAW UNIT 35-73  5.1K; BLACKFOOT WEST UNIT 703WA 5.1K; Gooseneck 13-13A-4-2 5.1K |
| LATITUDE | amount | 207.7K | 1.5K | 47.846600 9.5K; 32.571428 5.1K; 28.416580 5.1K; 28.529275 5.1K |
| LONGITUDE | amount | 221.0K | 1.5K | -103.555278 10.0K; -104.793160 5.2K; -99.880780 5.1K; -104.032500 5.1K |
| PROJECTION | category | 5 | 0 | NAD27 4.20M; NAD83 2.86M; WGS84 139.3K; Nad27 7 |
| TVD | other | 40.1K | 30.1K | 0 97.6K; 6500 14.4K; 9981 10.7K; 11000 10.7K |
| TOTALBASEWATERVOLUME | amount | 203.2K | 30.3K | 0 29.2K; 7249746 5.1K; 22049074 5.1K; 22448706 5.1K |
| TOTALBASENONWATERVOLUME | amount | 21.0K | 236.6K | 0 6.03M; 2000 4.7K; 1000 3.3K; 3000 2.3K |
| FFVERSION | category | 4 | 0 | 3 3.43M; 2 2.81M; 4 918.0K; 1 43.8K |
| FEDERALWELL | category | 2 | 0 | False 6.62M; True 579.4K |
| INDIANWELL | category | 2 | 0 | False 7.14M; True 63.2K |
| PURPOSEID | who | 2.75M | 0 | 14205d45-f214-45bf-a5a7-9 5.1K; 14c3a697-c72e-486a-bd13-8 5.0K; ff5fca57-71b8-4682-bc25-0 5.0K; 7e746240-b1b9-4ddd-b144-c 5.0K |
| TRADENAME | who | 30.5K | 610.6K | Ingredient Container 1.86M; Other Chemical(s) 561.6K; Water 129.2K; Other Ingredients 49.0K |
| SUPPLIER | who | 6.4K | 610.2K | Ingredient Container 1.86M; Listed Above 558.8K; Halliburton 508.1K; Schlumberger 278.6K |
| PURPOSE | who | 9.2K | 20.3K | Ingredient Container Purp 1.86M; See Trade Name(s) List 588.1K; Friction Reducer 253.1K; Other Chemicals 234.0K |
| INGREDIENTSID | id | 6.47M | 813.1K | 2ec437b2-8081-4fbe-81e6-e 4.6K; 66ba9aeb-86c0-471f-b3d1-d 4.6K; 2eaa6910-6da6-486c-9b4f-d 4.6K; a0fbbc2e-69b0-48c5-bf7d-b 4.6K |
| CASNUMBER | who | 2.7K | 899.4K | Proprietary 750.0K; 7732-18-5 653.4K; 14808-60-7 309.5K; 67-56-1 232.4K |
| INGREDIENTNAME | who | 21.5K | 823.7K | Water 559.7K; Methanol 173.5K; Ethanol 67.8K; Ethylene Glycol 66.2K |
| INGREDIENTCOMMONNAME | who | 473 | 2.20M | Water 653.4K; Crystalline silica, quart 309.5K; Methyl Alchol 232.4K; Hydrotreated light petrol 206.8K |
| PERCENTHIGHADDITIVE | amount | 76.1K | 816.0K | 100 733.4K; 0 730.6K; 5 682.1K; 30 560.0K |
| PERCENTHFJOB | other | 3.34M | 818.6K | 0 417.5K; 1E-05 48.9K; 2E-05 23.3K; 4E-05 18.8K |
| INGREDIENTCOMMENT | who | 16.7K | 6.95M | SmartCare Product 66.7K; Denise Tuck, Halliburton, 14.6K; Proprietary CAS & Additiv 14.2K; Density = 8.330 13.1K |
| INGREDIENTMSDS | category | 2 | 813.1K | True 5.08M; False 1.31M |
| MASSINGREDIENT | amount | 1.60M | 944.5K | 0 1.74M; 1 46.6K; 2 5.9K; 3 5.8K |
| CLAIMANTCOMPANY | who | 1.8K | 6.40M | Halliburton 189.4K; ProFrac 87.5K; Null 27.5K; - 26.8K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:36:36.25513 7.20M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 1c995965-ebbf-4837-a0f5-0 7.20M |
| _SRC_FILE | category | 15 | 0 | FracFocusRegistry_8.csv 500.0K; FracFocusRegistry_5.csv 500.0K; FracFocusRegistry_7.csv 500.0K; FracFocusRegistry_6.csv 500.0K |
