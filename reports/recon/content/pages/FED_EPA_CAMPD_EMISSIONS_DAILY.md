# FED_EPA_CAMPD_EMISSIONS_DAILY

rows 16.51M  columns 29  scan 14.3s

roles: amount 9, audit 2, category 2, date 2, other 4, state 1, who 10

## errors
  _INGESTED_AT: 100039 (22003): Numeric value '56662974' is out of range

## when

DATE
  2015     1.62M  ##############################
  2016     1.58M  #############################
  2017     1.54M  ############################
  2018     1.53M  ############################
  2019     1.51M  ############################
  2020     1.49M  ############################
  2021     1.47M  ###########################
  2022     1.47M  ###########################
  2023     1.45M  ###########################
  2024     1.42M  ##########################
  2025     1.42M  ##########################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GROSS_LOAD_MWH | 6.74M | 0 | 3.2K | 18.3K | 35.4K | 27.64B |
| STEAM_LOAD_1000_LB | 641.5K | 0 | 4.8K | 44.6K | 80.0K | 4.65B |
| SO2_MASS_SHORT_TONS | 6.86M | 0 | 0.01 | 32.21 | 766.36 | 11.83M |
| SO2_RATE_LBS_MMBTU | 6.85M | 0 | 0 | 0.76 | 35.2K | 560.3K |
| CO2_MASS_SHORT_TONS | 6.77M | 0 | 1.9K | 18.3K | 67.6K | 19.48B |
| CO2_RATE_SHORT_TONS_MMBTU | 6.76M | 0 | 0.06 | 0.11 | 172.79 | 485.0K |

## who

FACILITY_NAME by rows
     98.4K  Johnsonville
     96.4K  Clark
     87.7K  Gowanus Generating Station
     85.9K  Astoria Gas Turbine Power
     80.4K  Holtsville Facility
     72.3K  Midland Cogeneration Venture
     70.5K  E F Barrett
     66.2K  Lincoln Combustion Turbine
     60.3K  Bayside Power Station
     56.3K  T H Wharton
     56.3K  Lagoon Creek
     49.8K  Ravenswood Generating Station
     48.2K  NCEMC Hamlet Plant
     48.2K  LSP University Park, LLC
     48.2K  Coolidge Generating Station
     48.2K  University Park Energy
     48.2K  Big Sandy Peaker Plant
     48.2K  Gallatin
     48.2K  NCEMC Anson Plant
     47.5K  Midulla Generating Station

FACILITY_NAME by dollars
      402.6K    16.1K rows  Labadie
      361.9K    32.9K rows  W A Parish
      330.8K    12.1K rows  Martin Lake
      259.4K    12.1K rows  Gen J M Gavin
      242.7K     8.0K rows  Gerald Gentleman Station
      217.1K    20.1K rows  Belle River
      178.0K    36.2K rows  Shawnee
      177.5K     8.0K rows  Keystone
      171.9K    24.1K rows  Independence
      171.8K     8.0K rows  White Bluff
      157.7K    12.1K rows  Thomas Hill Energy Center
      152.2K     9.6K rows  Homer City
      146.6K     2.4K rows  Big Brown
      141.8K     7.3K rows  Rush Island
      138.0K     8.0K rows  Nebraska City Station
      135.2K    12.1K rows  Miami Fort Power Station
      135.1K    12.1K rows  Rockport
      134.7K     8.0K rows  New Madrid Power Plant
      133.1K     4.0K rows  Coyote
      131.4K    12.1K rows  Harrison Power Station

_SRC_FILE by rows
    155.9K  emissions-daily-2025-tx.csv
    154.9K  emissions-daily-2024-tx.csv
    151.7K  emissions-daily-2023-tx.csv
    145.9K  emissions-daily-2022-tx.csv
    141.1K  emissions-daily-2021-tx.csv
    140.8K  emissions-daily-2017-tx.csv
    140.0K  emissions-daily-2015-tx.csv
    139.7K  emissions-daily-2016-tx.csv
    139.2K  emissions-daily-2018-tx.csv
    138.4K  emissions-daily-2020-tx.csv
    138.4K  emissions-daily-2019-tx.csv
    108.8K  emissions-daily-2015-fl.csv
    107.2K  emissions-daily-2016-fl.csv
    105.7K  emissions-daily-2021-ny.csv
    103.0K  emissions-daily-2022-ny.csv
    101.4K  emissions-daily-2023-ny.csv
    101.3K  emissions-daily-2015-ny.csv
    101.3K  emissions-daily-2016-ny.csv
    100.8K  emissions-daily-2017-ny.csv
     99.9K  emissions-daily-2018-ny.csv

_SRC_FILE by dollars
      276.2K   140.8K rows  emissions-daily-2017-tx.csv
      260.3K   140.0K rows  emissions-daily-2015-tx.csv
      246.0K   139.7K rows  emissions-daily-2016-tx.csv
      211.2K   139.2K rows  emissions-daily-2018-tx.csv
      200.1K    62.3K rows  emissions-daily-2015-pa.csv
      177.3K    50.7K rows  emissions-daily-2015-oh.csv
      166.4K    53.6K rows  emissions-daily-2015-in.csv
      154.9K   141.1K rows  emissions-daily-2021-tx.csv
      149.3K   138.4K rows  emissions-daily-2019-tx.csv
      132.6K    52.8K rows  emissions-daily-2015-mi.csv
      131.7K    36.8K rows  emissions-daily-2015-ky.csv
      130.3K   138.4K rows  emissions-daily-2020-tx.csv
      128.3K   145.9K rows  emissions-daily-2022-tx.csv
      113.7K    44.7K rows  emissions-daily-2015-mo.csv
      109.4K   155.9K rows  emissions-daily-2025-tx.csv
      106.0K    43.8K rows  emissions-daily-2017-mo.csv
      104.3K   151.7K rows  emissions-daily-2023-tx.csv
      102.6K    43.7K rows  emissions-daily-2018-mo.csv
      101.0K    39.8K rows  emissions-daily-2021-mo.csv
       99.5K    44.3K rows  emissions-daily-2016-mo.csv

NOX_CONTROLS by rows
     2.24M  Water Injection
     1.81M  Dry Low NOx Burners
     1.15M  Dry Low NOx Burners,Selective Catalytic Reduction
     1.12M  Selective Catalytic Reduction
    742.4K  Dry Low NOx Burners,Water Injection
    654.6K  Dry Low NOx Burners|Selective Catalytic Reduction
    565.2K  Water Injection,Selective Catalytic Reduction
    428.2K  Water Injection|Selective Catalytic Reduction
    426.0K  Low NOx Burner Technology (Dry Bottom only)
    323.7K  Dry Low NOx Burners,Water Injection,Selective Catalytic Reduction
    291.8K  Steam Injection
    267.6K  Dry Low NOx Burners|Water Injection
    246.3K  Overfire Air
    203.9K  Low NOx Burner Technology w/ Overfire Air
    194.6K  Low NOx Burner Technology w/ Closed-coupled/Separated OFA
    180.2K  Other
    151.6K  Low NOx Burner Technology w/ Separated OFA
    151.2K  Dry Low NOx Burners|Water Injection|Selective Catalytic Reduction
    146.5K  Selective Non-catalytic Reduction
    139.5K  Combustion Modification/Fuel Reburning

NOX_CONTROLS by dollars
       1.19M   194.6K rows  Low NOx Burner Technology w/ Closed-coupled/Separated OFA
      956.4K   426.0K rows  Low NOx Burner Technology (Dry Bottom only)
      913.7K   151.6K rows  Low NOx Burner Technology w/ Separated OFA
      845.0K   203.9K rows  Low NOx Burner Technology w/ Overfire Air
      682.8K    1.12M rows  Selective Catalytic Reduction
      550.4K   246.3K rows  Overfire Air
      524.1K   110.1K rows  Low NOx Burner Technology w/ Overfire Air,Selective Catalyti
      523.1K    52.3K rows  Low NOx Cell Burner,Selective Catalytic Reduction
      495.9K   130.2K rows  Low NOx Burner Technology (Dry Bottom only),Selective Cataly
      317.1K    59.0K rows  Low NOx Burner Technology w/ Closed-coupled/Separated OFA,Se
      264.2K    30.8K rows  Low NOx Burner Technology w/ Overfire Air,Selective Non-cata
      258.6K    21.7K rows  Low NOx Burner Technology w/ Separated OFA,Selective Non-cat
      257.9K    79.3K rows  Overfire Air,Selective Catalytic Reduction
      241.4K   146.5K rows  Selective Non-catalytic Reduction
      238.5K    97.7K rows  Low NOx Burner Technology w/ Closed-coupled OFA
      209.9K    58.8K rows  Low NOx Burner Technology w/ Separated OFA,Selective Catalyt
      178.5K    22.3K rows  Low NOx Burner Technology w/ Closed-coupled/Separated OFA,Ov
      157.4K    26.1K rows  Selective Catalytic Reduction,Low NOx Burner Technology (Dry
      141.4K    17.5K rows  Selective Catalytic Reduction,Overfire Air
      116.4K    42.2K rows  Low NOx Burner Technology (Dry Bottom only)|Selective Cataly

UNIT_TYPE by rows
     7.55M  Combustion turbine
     4.40M  Combined cycle
     1.96M  Dry bottom wall-fired boiler
     1.41M  Tangentially-fired
    277.8K  Circulating fluidized bed boiler
    221.6K  Other boiler
    190.7K  Stoker
    174.7K  Cyclone boiler
    100.1K  Cell burner boiler
     56.8K  Dry bottom turbo-fired boiler
     53.4K  Wet bottom wall-fired boiler
     18.1K  Dry bottom vertically-fired boiler
     15.0K  Integrated gasification combined cycle
     14.7K  Bubbling fluidized bed boiler
      7.7K  Wet bottom turbo-fired boiler
      4.0K  Other turbine
      1.3K  Cement Kiln
       734  Combustion turbine (Started May 20, 2024)
       730  Combined cycle (Started Jul 08, 2022), Combustion turbine (Ended Jul 0
       640  Combustion turbine (Started Apr 08, 2018)

UNIT_TYPE by dollars
       4.81M    1.41M rows  Tangentially-fired
       4.80M    1.96M rows  Dry bottom wall-fired boiler
      819.8K   100.1K rows  Cell burner boiler
      701.7K   174.7K rows  Cyclone boiler
      384.4K   277.8K rows  Circulating fluidized bed boiler
       88.7K    53.4K rows  Wet bottom wall-fired boiler
       71.7K    56.8K rows  Dry bottom turbo-fired boiler
       55.7K   190.7K rows  Stoker
       33.7K    4.40M rows  Combined cycle
       13.3K    18.1K rows  Dry bottom vertically-fired boiler
       13.0K     7.7K rows  Wet bottom turbo-fired boiler
       11.1K    14.7K rows  Bubbling fluidized bed boiler
        9.0K    7.55M rows  Combustion turbine
        8.2K   221.6K rows  Other boiler
        4.4K    15.0K rows  Integrated gasification combined cycle
      241.08      366 rows  Integrated gasification combined cycle (Ended Dec 31, 2016),
       13.16      275 rows  Combined cycle (Started Jan 24, 2018)
       12.28      275 rows  Combined cycle (Started Jan 18, 2018)
        8.89      275 rows  Circulating fluidized bed boiler (Started May 20, 2017)
        4.55       92 rows  Combustion turbine (Started May 08, 2020)

## who x when

FACILITY_NAME by DATE, dollars = SO2_MASS_SHORT_TONS
  Astoria Gas Turbine Power                 2015:5.58 2016:7.35 2017:2.82 2018:8.96 2019:1.26 2020:1.42 2021:5.20 2022:28.88 2023:0.78
  Bayside Power Station                     2015:20.84 2016:19.42 2017:15.41 2018:16.93 2019:18.27 2020:17.65 2021:18.65 2022:17.78 2023:14.12 2024:11.29 2025:12.41
  Belle River                               2015:23.7K 2016:20.8K 2017:22.6K 2018:24.0K 2019:17.5K 2020:14.6K 2021:22.4K 2022:20.6K 2023:16.8K 2024:15.9K 2025:18.2K
  Big Sandy Peaker Plant                    2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0
  Clark                                     2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0
  Coolidge Generating Station               2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0
  E F Barrett                               2015:64.20 2016:20.55 2017:41.38 2018:65.77 2019:39.90 2020:23.53 2021:109.26 2022:47.01 2023:23.22 2024:4.38 2025:46.97
  Gallatin                                  2015:12.3K 2016:1.4K 2017:1.1K 2018:1.8K 2019:1.7K 2020:1.0K 2021:1.8K 2022:1.8K 2023:1.4K 2024:1.4K 2025:1.7K
  Gen J M Gavin                             2015:26.5K 2016:20.0K 2017:25.4K 2018:27.6K 2019:26.5K 2020:28.2K 2021:25.8K 2022:20.3K 2023:18.4K 2024:19.2K 2025:21.6K
  Gerald Gentleman Station                  2015:25.0K 2016:22.8K 2017:21.3K 2018:27.7K 2019:23.4K 2020:18.2K 2021:19.4K 2022:21.2K 2023:20.9K 2024:20.5K 2025:22.3K
  Gowanus Generating Station                2015:5.9K 2016:5.9K 2017:5.9K 2018:5.9K 2019:5.9K 2020:5.9K 2021:11.7K 2022:11.7K 2023:11.7K 2024:11.7K 2025:5.8K
  Holtsville Facility                       2015:97.36 2016:135.76 2017:0 2018:0.06 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0
  Independence                              2015:15.0K 2016:22.6K 2017:19.5K 2018:24.3K 2019:15.9K 2020:8.0K 2021:11.1K 2022:12.4K 2023:12.9K 2024:13.7K 2025:16.7K
  Johnsonville                              2015:29.7K 2016:9.2K 2017:6.3K 2018:22.59 2019:14.40 2020:18.12 2021:28.98 2022:88.93 2023:16.26 2024:9.63 2025:7.78
  Keystone                                  2015:24.4K 2016:22.4K 2017:23.3K 2018:24.0K 2019:19.8K 2020:13.0K 2021:17.0K 2022:11.0K 2023:6.4K 2024:7.3K 2025:8.9K
  LSP University Park, LLC                  2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0
  Labadie                                   2015:34.4K 2016:31.1K 2017:33.1K 2018:33.7K 2019:34.5K 2020:39.4K 2021:41.9K 2022:44.3K 2023:39.2K 2024:32.7K 2025:38.2K
  Lagoon Creek                              2015:7.59 2016:7.30 2017:6.36 2018:7.65 2019:6.62 2020:6.30 2021:5.17 2022:11.84 2023:6.03 2024:6.79 2025:5.73
  Lincoln Combustion Turbine                2015:2.57 2016:0.70 2017:0.07 2018:5.35 2019:0.04 2020:4.55 2021:84.18 2022:1.96 2023:0.20 2024:0.11 2025:0.06
  Martin Lake                               2015:22.9K 2016:25.5K 2017:36.4K 2018:56.2K 2019:46.5K 2020:43.6K 2021:48.8K 2022:17.7K 2023:13.3K 2024:9.9K 2025:10.0K
  Midland Cogeneration Venture              2015:18.55 2016:27.85 2017:21.64 2018:27.51 2019:32.79 2020:33.99 2021:22.43 2022:24.16 2023:35.87 2024:38.34 2025:34.39
  Midulla Generating Station                2015:4.86 2016:7.03 2017:6.72 2018:6.53 2019:6.14 2020:7 2021:6.74 2022:6.72 2023:4.84 2024:5.28 2025:6.40
  NCEMC Anson Plant                         2015:0.04 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0.07 2025:0
  NCEMC Hamlet Plant                        2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0
  Ravenswood Generating Station             2015:89.07 2016:68.69 2017:60.31 2018:184.65 2019:30.01 2020:4.95 2021:13.19 2022:24.26 2023:18 2024:8.44 2025:6.86
  Shawnee                                   2015:24.3K 2016:23.8K 2017:20.5K 2018:15.2K 2019:16.3K 2020:9.0K 2021:14.7K 2022:14.3K 2023:11.7K 2024:12.6K 2025:15.6K
  T H Wharton                               2015:0.22 2016:0.01 2017:0.01 2018:5.1K 2019:5.1K 2020:5.1K 2021:5.1K 2022:5.1K 2023:5.1K 2024:5.1K 2025:5.1K
  University Park Energy                    2015:0 2016:0 2017:0.18 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0
  W A Parish                                2015:42.7K 2016:34.1K 2017:37.6K 2018:38.2K 2019:28.8K 2020:23.9K 2021:33.9K 2022:34.1K 2023:28.5K 2024:24.1K 2025:36.0K
  White Bluff                               2015:20.5K 2016:18.3K 2017:23.2K 2018:22.3K 2019:19.3K 2020:10.7K 2021:18.5K 2022:14.0K 2023:9.5K 2024:5.5K 2025:10.0K

_SRC_FILE by DATE, dollars = SO2_MASS_SHORT_TONS
  emissions-daily-2015-fl.csv               2015:61.4K
  emissions-daily-2015-in.csv               2015:166.4K
  emissions-daily-2015-ky.csv               2015:131.7K
  emissions-daily-2015-mi.csv               2015:132.6K
  emissions-daily-2015-mo.csv               2015:113.7K
  emissions-daily-2015-ny.csv               2015:8.8K
  emissions-daily-2015-oh.csv               2015:177.3K
  emissions-daily-2015-pa.csv               2015:200.1K
  emissions-daily-2015-tx.csv               2015:260.3K
  emissions-daily-2016-fl.csv               2016:39.2K
  emissions-daily-2016-mo.csv               2016:99.5K
  emissions-daily-2016-ny.csv               2016:4.5K
  emissions-daily-2016-tx.csv               2016:246.0K
  emissions-daily-2017-mo.csv               2017:106.0K
  emissions-daily-2017-ny.csv               2017:2.6K
  emissions-daily-2017-tx.csv               2017:276.2K
  emissions-daily-2018-mo.csv               2018:102.6K
  emissions-daily-2018-ny.csv               2018:4.9K
  emissions-daily-2018-tx.csv               2018:211.2K
  emissions-daily-2019-tx.csv               2019:149.3K
  emissions-daily-2020-tx.csv               2020:130.3K
  emissions-daily-2021-mo.csv               2021:101.0K
  emissions-daily-2021-ny.csv               2021:1.6K
  emissions-daily-2021-tx.csv               2021:154.9K
  emissions-daily-2022-ny.csv               2022:2.7K
  emissions-daily-2022-tx.csv               2022:128.3K
  emissions-daily-2023-ny.csv               2023:635.98
  emissions-daily-2023-tx.csv               2023:104.3K
  emissions-daily-2024-tx.csv               2024:88.1K
  emissions-daily-2025-tx.csv               2025:109.4K

## where

STATE: TX 1.59M, NY 1.09M, CA 980.7K, IL 903.7K, FL 896.1K, PA 686.3K, GA 559.7K, NC 542.8K, IN 529.1K, MI 497.0K, OH 495.0K, VA 471.1K

## what

OPERATING_TIME_COUNT: 0 60%, 24 30%, 3 1%, 4 1%, 5 1%, 6 1%, 2 1%, 8 1%, 10 1%, 9 1%, 7 1%, 11 1%

PRIMARY_FUEL_TYPE: Pipeline Natural Gas 72%, Coal 14%, Diesel Oil 8%, Natural Gas 3%, Residual Oil 1%, Process Gas 1%, Wood 1%, Other Gas 0%, Other Oil 0%, Coal Refuse 0%, Petroleum Coke 0%, Coal, Pipeline Natural Gas 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATE | state | 51 | 0 | TX 1.59M; NY 1.09M; CA 980.7K; IL 903.7K |
| FACILITY_NAME | who | 1.6K | 0 | Johnsonville 118.5K; Clark 104.5K; Astoria Gas Turbine Power 102.7K; Gowanus Generating Statio 97.7K |
| FACILITY_ID | who | 1.6K | 0 | 3406 118.5K; 2322 104.5K; 55243 102.7K; 2494 97.7K |
| UNIT_ID | other | 1.7K | 0 | 1 1.61M; 2 1.34M; 3 834.1K; 4 647.4K |
| ASSOCIATED_STACKS | other | 162 | 14.37M | CP001 199.1K; CP1 175.5K; CP100 160.7K; CP0001 139.8K |
| DATE | date | 4.0K | 0 | 2024-08-07 21.2K; 2024-08-08 21.2K; 2024-08-09 21.2K; 2024-08-10 21.2K |
| OPERATING_TIME_COUNT | category | 25 | 0 | 0 9.11M; 24 4.52M; 3 167.9K; 4 165.8K |
| SUM_OF_THE_OPERATING_TIME | other | 2.4K | 73.6K | 0 9.03M; 24 4.40M; 2 14.9K; 11 11.4K |
| GROSS_LOAD_MWH | amount | 537.3K | 9.78M | 0 121.2K; 16.2 8.7K; 0.05 8.3K; 0.07 8.3K |
| STEAM_LOAD_1000_LB | amount | 89.8K | 15.87M | 0 6.5K; 3976 898; 4873 710; 2670 709 |
| SO2_MASS_SHORT_TONS | amount | 61.9K | 9.66M | 0 663.9K; 0.001 652.1K; 0.002 396.1K; 0.012 391.1K |
| SO2_RATE_LBS_MMBTU | amount | 24.2K | 9.66M | 0.001 4.69M; 0 120.4K; 0.0009 104.7K; 0.0008 71.6K |
| CO2_MASS_SHORT_TONS | amount | 1.65M | 9.74M | 0 9.9K; 237 9.0K; 193.1 9.0K; 0.6 8.8K |
| CO2_RATE_SHORT_TONS_MMBTU | amount | 4.2K | 9.75M | 0.059 3.56M; 0.105 666.6K; 0.103 499.7K; 0.0591 365.7K |
| NOX_MASS_SHORT_TONS | amount | 35.6K | 9.12M | 0 50.4K; 0.007 43.4K; 0.009 42.6K; 0.01 41.7K |
| NOX_RATE_LBS_MMBTU | amount | 11.4K | 9.16M | 0.007 131.1K; 0.008 124.9K; 0.006 124.5K; 0.011 78.5K |
| HEAT_INPUT_MMBTU | amount | 3.54M | 9.16M | 0.8 9.2K; 7975.2 4.9K; 6964.9 4.9K; 7177.9 4.9K |
| PRIMARY_FUEL_TYPE | category | 24 | 181 | Pipeline Natural Gas 11.80M; Coal 2.36M; Diesel Oil 1.25M; Natural Gas 441.1K |
| SECONDARY_FUEL_TYPE | who | 68 | 9.95M | Diesel Oil 4.48M; Pipeline Natural Gas 684.9K; Residual Oil 483.9K; Natural Gas 111.0K |
| UNIT_TYPE | who | 287 | 0 | Combustion turbine 7.55M; Combined cycle 4.40M; Dry bottom wall-fired boi 1.96M; Tangentially-fired 1.41M |
| SO2_CONTROLS | who | 78 | 14.58M | Wet Limestone 656.5K; Dry Lime FGD 462.3K; Wet Lime FGD 400.7K; Fluidized Bed Limestone I 161.9K |
| NOX_CONTROLS | who | 407 | 2.57M | Water Injection 2.24M; Dry Low NOx Burners 1.81M; Dry Low NOx Burners,Selec 1.15M; Selective Catalytic Reduc 1.12M |
| PM_CONTROLS | who | 137 | 13.67M | Electrostatic Precipitato 1.29M; Baghouse 897.2K; Electrostatic Precipitato 129.2K; Baghouse,Electrostatic Pr 96.7K |
| HG_CONTROLS | who | 120 | 15.68M | Halogenated PAC Sorbent I 370.8K; Additives to Enhance PAC  125.6K; Untreated PAC Sorbent Inj 76.2K; Additives to Enhance PAC  49.0K |
| PROGRAM_CODE | other | 105 | 36.4K | ARP 2.83M; ARP, CSOSG2 1.63M; ARP, CSNOX, CSOSG2, CSSO2 1.42M; SIPNOX 881.4K |
| _INGESTED_AT | audit date | 1 | 0 | 56662974-12-02 07:16:07.0 16.51M |
| _SOURCE_RUN_ID | audit | 1 | 0 | da335ca4-ebd8-4b9a-b822-9 16.51M |
| _SRC_SHA256 | who | 558 | 0 | ccc1c9a921129f382aaeceb1e 155.9K; a0a664f22883a58c8517e4544 154.9K; d695d006b51e160234b9ca2ba 151.7K; c307d84b92adf8288a619cd77 145.9K |
| _SRC_FILE | who | 555 | 0 | emissions-daily-2025-tx.c 155.9K; emissions-daily-2024-tx.c 154.9K; emissions-daily-2023-tx.c 151.7K; emissions-daily-2022-tx.c 145.9K |
