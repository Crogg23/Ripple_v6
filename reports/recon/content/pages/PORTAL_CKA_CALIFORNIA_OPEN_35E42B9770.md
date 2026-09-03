# PORTAL_CKA_CALIFORNIA_OPEN_35E42B9770

rows 10.0K  columns 37  scan 4.7s

roles: amount 16, audit 2, category 11, date 3, empty 1, other 2, who 3

## when

REPORT_PERIOD_START_DATE
  2014       494  #################
  2015       849  #############################
  2016       852  #############################
  2017       847  #############################
  2018       799  ###########################
  2019       749  ##########################
  2020       809  ############################
  2021       847  #############################
  2022       844  #############################
  2023       875  ##############################
  2024       876  ##############################
  2025       876  ##############################
  2026       283  ##########

REPORT_PERIOD_END_DATE
  2014       494  #################
  2015       849  #############################
  2016       852  #############################
  2017       847  #############################
  2018       799  ###########################
  2019       749  ##########################
  2020       809  ############################
  2021       847  #############################
  2022       844  #############################
  2023       875  ##############################
  2024       876  ##############################
  2025       876  ##############################
  2026       283  ##########

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POTABLE_SUPPLY_GAL | 2.9K | 10.63M | 202.42M | 1.65B | 2.33B | 845.54B |
| POTABLE_VOL_SOLD_GAL | 2.9K | 0 | 0 | 137.98M | 4.74B | 16.54B |
| POTABLE_SUPPLY_MINUS_SOLD_GAL | 10.0K | -4.29B | 208.48M | 1.74B | 2.94B | 3044.14B |
| POTABLE_DEMAND_RES_GAL | 10.0K | 27.7K | 134.87M | 1.12B | 326.70B | 2309.32B |
| R_GPCD | 10.0K | 0.12 | 84.59 | 270.81 | 91.6K | 1.07M |
| POTABLE_DEMAND_AG_GAL | 5.3K | 0 | 0 | 91.32M | 227.77M | 20.48B |

## who

SUPPLIER_NAME by rows
       143  Amador Water Agency
       143  California Water Service Company Mid Peninsula
       143  Alco Water Service
       143  California Water Service Company Livermore
       143  City of Benicia
       143  California Water Service Company Marysville
       143  California Water Service Company Stockton
       143  California American Water Company - San Diego District
       143  California Water Service Company Westlake
       143  Apple Valley Ranchos Water Company
       143  City of Ceres
       143  City of Antioch
       143  Casitas Municipal Water District
       143  California Water Service Company Hermosa/Redondo
       143  City of Cerritos
       143  California Water Service Company Dixon
       143  California Water Service Company Los Altos/Suburban
       143  City of Atwater
       143  California American Water Company - Los Angeles Division
       143  California Water Service Company Dominguez

SUPPLIER_NAME by dollars
     226.21B      142 rows  California Water Service Company Bakersfield
     216.51B      143 rows  City of Anaheim
     159.10B      143 rows  City of Bakersfield
     157.17B      141 rows  Alameda County Water District
     111.23B      143 rows  California Water Service Company Visalia
     108.53B      143 rows  California Water Service Company Dominguez
     108.01B      143 rows  California American Water Company - Sacramento District
      89.84B      143 rows  California Water Service Company Stockton
      81.29B      143 rows  California Water Service Company Chico District
      68.97B      143 rows  California American Water Company - Los Angeles Division
      68.15B      143 rows  Azusa Light and Water
      63.67B      143 rows  California Water Service Company Palos Verdes
      61.20B      143 rows  California Water Service Company Salinas District
      57.63B      143 rows  City of Antioch
      57.08B      143 rows  Carlsbad Municipal Water District
      53.74B      143 rows  California Water Service Company East Los Angeles
      53.19B      143 rows  California American Water Company - Ventura District
      52.69B      136 rows  City of Burbank
      52.21B      143 rows  California Water Service Company Mid Peninsula
      49.02B      134 rows  City of Arcadia

ORG_ID by rows
       143  264
       143  376
       143  178
       143  110
       143  388
       143  392
       143  417
       143  117
       143  262
       143  123
       143  391
       143  286
       143  369
       143  421
       143  443
       143  55
       143  390
       143  524
       143  64
       143  87

ORG_ID by dollars
     226.21B      142 rows  386
     216.51B      143 rows  64
     159.10B      143 rows  123
     157.17B      141 rows  23
     111.23B      143 rows  427
     108.53B      143 rows  391
     108.01B      143 rows  372
      89.84B      143 rows  424
      81.29B      143 rows  388
      68.97B      143 rows  368
      68.15B      143 rows  117
      63.67B      143 rows  413
      61.20B      143 rows  417
      57.63B      143 rows  82
      57.08B      143 rows  478
      53.74B      143 rows  392
      53.19B      143 rows  376
      52.69B      136 rows  285
      52.21B      143 rows  420
      49.02B      134 rows  93

SRC_SHA256 by rows
     10.0K  672e89a2d01bc8ee5f1f51937f331496b78d4554d77e696e808cb107a5072521

SRC_SHA256 by dollars
    3044.14B    10.0K rows  672e89a2d01bc8ee5f1f51937f331496b78d4554d77e696e808cb107a507

## who x when

SUPPLIER_NAME by REPORT_PERIOD_START_DATE, dollars = POTABLE_SUPPLY_MINUS_SOLD_GAL
  Alameda County Water District             2014:6.80B 2015:11.86B 2016:12.44B 2017:13.32B 2018:13.67B 2019:13.54B 2020:14.44B 2021:13.77B 2022:11.91B 2023:13.40B 2024:13.93B 2025:13.97B 2026:4.11B
  Alco Water Service                        2014:848.94M 2015:1.22B 2016:1.15B 2017:1.21B 2018:1.25B 2019:1.23B 2020:1.32B 2021:1.29B 2022:1.30B 2023:1.26B 2024:1.23B 2025:1.23B 2026:359.64M
  Amador Water Agency                       2014:699.20M 2015:877.06M 2016:948.83M 2017:1.09B 2018:1.18B 2019:1.15B 2020:1.24B 2021:1.16B 2022:1.22B 2023:1.11B 2024:1.19B 2025:1.14B 2026:298.79M
  Apple Valley Ranchos Water Company        2014:2.62B 2015:3.12B 2016:3.00B 2017:3.09B 2018:3.11B 2019:3.05B 2020:3.28B 2021:3.26B 2022:3.11B 2023:3.06B 2024:3.16B 2025:3.14B 2026:846.51M
  Azusa Light and Water                     2014:3.85B 2015:5.55B 2016:5.56B 2017:6.13B 2018:6.09B 2019:5.65B 2020:5.91B 2021:5.90B 2022:5.53B 2023:5.07B 2024:5.54B 2025:5.69B 2026:1.67B
  California American Water Company - Los   2014:4.37B 2015:5.60B 2016:5.61B 2017:6.05B 2018:6.30B 2019:5.84B 2020:6.32B 2021:6.19B 2022:5.53B 2023:4.93B 2024:5.31B 2025:5.40B 2026:1.51B
  California American Water Company - Sacr  2014:6.33B 2015:7.92B 2016:8.21B 2017:8.96B 2018:9.04B 2019:9.00B 2020:9.73B 2021:9.41B 2022:9.01B 2023:8.54B 2024:9.88B 2025:9.69B 2026:2.30B
  California American Water Company - San   2014:2.13B 2015:2.93B 2016:3.20B 2017:3.35B 2018:3.42B 2019:3.07B 2020:3.29B 2021:3.31B 2022:3.32B 2023:3.00B 2024:3.06B 2025:3.16B 2026:958.63M
  California Water Service Company Bakersf  2014:15.02B 2015:17.93B 2016:18.78B 2017:20.26B 2018:20.62B 2019:19.64B 2020:19.36B 2021:19.25B 2022:16.91B 2023:16.87B 2024:18.32B 2025:18.65B 2026:4.60B
  California Water Service Company Chico D  2014:5.02B 2015:5.93B 2016:5.98B 2017:6.56B 2018:6.65B 2019:6.64B 2020:7.39B 2021:7.18B 2022:7.07B 2023:6.82B 2024:7.23B 2025:7.11B 2026:1.72B
  California Water Service Company Dixon    2014:298.15M 2015:375.12M 2016:362.54M 2017:383.49M 2018:404.87M 2019:412.89M 2020:453.32M 2021:427.32M 2022:403.31M 2023:417.13M 2024:441.61M 2025:439.19M 2026:120.73M
  California Water Service Company Domingu  2014:6.56B 2015:10.20B 2016:9.67B 2017:9.43B 2018:10.41B 2019:9.41B 2020:9.25B 2021:8.85B 2022:8.09B 2023:8.37B 2024:8.21B 2025:7.78B 2026:2.31B
  California Water Service Company Hermosa  2014:2.42B 2015:3.51B 2016:3.38B 2017:3.45B 2018:3.53B 2019:3.40B 2020:3.57B 2021:3.58B 2022:3.32B 2023:3.09B 2024:2.85B 2025:3.09B 2026:956.72M
  California Water Service Company Livermo  2014:1.66B 2015:2.22B 2016:2.48B 2017:2.65B 2018:2.60B 2019:3.01B 2020:3.12B 2021:2.94B 2022:2.75B 2023:2.63B 2024:2.74B 2025:2.72B 2026:677.90M
  California Water Service Company Los Alt  2014:2.72B 2015:3.32B 2016:3.34B 2017:3.80B 2018:4.05B 2019:3.87B 2020:4.24B 2021:3.73B 2022:3.51B 2023:3.33B 2024:3.45B 2025:3.36B 2026:868.24M
  California Water Service Company Marysvi  2014:432.08M 2015:567.50M 2016:616.05M 2017:642.02M 2018:596.96M 2019:596.70M 2020:655.68M 2021:658.90M 2022:564.83M 2023:577.58M 2024:594.43M 2025:560.95M 2026:136.92M
  California Water Service Company Mid Pen  2014:2.96B 2015:4.13B 2016:4.08B 2017:4.43B 2018:4.54B 2019:4.58B 2020:4.73B 2021:4.52B 2022:4.32B 2023:4.23B 2024:4.29B 2025:4.20B 2026:1.19B
  California Water Service Company Palos V  2014:4.20B 2015:5.43B 2016:5.27B 2017:5.73B 2018:5.72B 2019:5.28B 2020:5.89B 2021:5.78B 2022:5.22B 2023:4.38B 2024:4.63B 2025:4.76B 2026:1.37B
  California Water Service Company Salinas  2014:3.42B 2015:4.78B 2016:4.64B 2017:5.12B 2018:5.27B 2019:5.21B 2020:5.37B 2021:5.31B 2022:5.16B 2023:5.19B 2024:5.12B 2025:5.13B 2026:1.49B
  California Water Service Company Stockto  2014:5.36B 2015:7.20B 2016:7.23B 2017:7.59B 2018:7.63B 2019:7.63B 2020:7.88B 2021:7.75B 2022:7.50B 2023:7.33B 2024:7.55B 2025:7.16B 2026:2.04B
  California Water Service Company Visalia  2014:6.33B 2015:8.10B 2016:8.42B 2017:9.09B 2018:9.53B 2019:9.42B 2020:9.90B 2021:9.90B 2022:9.65B 2023:9.18B 2024:9.69B 2025:9.60B 2026:2.43B
  California Water Service Company Westlak  2014:1.64B 2015:2.13B 2016:1.95B 2017:2.23B 2018:2.34B 2019:2.14B 2020:2.30B 2021:2.26B 2022:1.79B 2023:1.64B 2024:1.84B 2025:1.95B 2026:521.16M
  Casitas Municipal Water District          2014:2.60B 2015:3.75B 2016:3.33B 2017:3.11B 2018:2.67B 2019:2.11B 2020:3.04B 2021:3.02B 2022:2.93B 2023:2.09B 2024:2.42B 2025:2.46B 2026:575.72M
  City of Anaheim                           2014:13.19B 2015:18.06B 2016:17.89B 2017:19.32B 2018:19.37B 2019:18.16B 2020:18.27B 2021:18.46B 2022:18.46B 2023:16.22B 2024:17.24B 2025:17.28B 2026:4.58B
  City of Antioch                           2014:3.48B 2015:4.49B 2016:4.54B 2017:4.80B 2018:4.84B 2019:4.70B 2020:5.09B 2021:5.00B 2022:4.37B 2023:4.54B 2024:5.14B 2025:5.30B 2026:1.33B
  City of Atwater                           2014:1.82B 2015:2.05B 2016:2.21B 2017:2.33B 2018:2.70B 2019:2.66B 2020:2.79B 2021:2.63B 2022:2.48B 2023:2.32B 2024:2.22B 2025:2.18B 2026:547.07M
  City of Bakersfield                       2014:9.66B 2015:11.01B 2016:11.91B 2017:12.67B 2018:13.38B 2019:13.04B 2020:13.85B 2021:14.26B 2022:13.21B 2023:12.45B 2024:14.92B 2025:15.19B 2026:3.54B
  City of Benicia                           2014:1.03B 2015:1.37B 2016:1.20B 2017:1.51B 2018:1.20B 2019:1.26B 2020:1.37B 2021:1.31B 2022:1.31B 2023:1.33B 2024:1.24B 2025:1.25B 2026:337.09M
  City of Ceres                             2014:1.61B 2015:2.10B 2016:1.98B 2017:2.11B 2018:2.14B 2019:1.96B 2020:2.13B 2021:2.15B 2022:2.11B 2023:1.98B 2024:2.09B 2025:2.17B 2026:554.92M
  City of Cerritos                          2014:1.66B 2015:2.26B 2016:2.30B 2017:2.40B 2018:2.48B 2019:2.25B 2020:2.43B 2021:2.50B 2022:2.37B 2023:2.15B 2024:2.23B 2025:2.28B 2026:687.62M

ORG_ID by REPORT_PERIOD_START_DATE, dollars = POTABLE_SUPPLY_MINUS_SOLD_GAL
  110                                       2014:1.82B 2015:2.05B 2016:2.21B 2017:2.33B 2018:2.70B 2019:2.66B 2020:2.79B 2021:2.63B 2022:2.48B 2023:2.32B 2024:2.22B 2025:2.18B 2026:547.07M
  117                                       2014:3.85B 2015:5.55B 2016:5.56B 2017:6.13B 2018:6.09B 2019:5.65B 2020:5.91B 2021:5.90B 2022:5.53B 2023:5.07B 2024:5.54B 2025:5.69B 2026:1.67B
  123                                       2014:9.66B 2015:11.01B 2016:11.91B 2017:12.67B 2018:13.38B 2019:13.04B 2020:13.85B 2021:14.26B 2022:13.21B 2023:12.45B 2024:14.92B 2025:15.19B 2026:3.54B
  178                                       2014:1.03B 2015:1.37B 2016:1.20B 2017:1.51B 2018:1.20B 2019:1.26B 2020:1.37B 2021:1.31B 2022:1.31B 2023:1.33B 2024:1.24B 2025:1.25B 2026:337.09M
  23                                        2014:6.80B 2015:11.86B 2016:12.44B 2017:13.32B 2018:13.67B 2019:13.54B 2020:14.44B 2021:13.77B 2022:11.91B 2023:13.40B 2024:13.93B 2025:13.97B 2026:4.11B
  262                                       2014:1.07B 2015:1.54B 2016:1.70B 2017:1.77B 2018:1.80B 2019:2.08B 2020:2.17B 2021:2.19B 2022:2.13B 2023:1.94B 2024:1.98B 2025:2.27B 2026:618.60M
  264                                       2014:2.37B 2015:2.64B 2016:2.74B 2017:3.22B 2018:3.33B 2019:3.37B 2020:3.83B 2021:3.74B 2022:3.60B 2023:3.36B 2024:3.56B 2025:3.50B 2026:855.39M
  285                                       2014:3.61B 2015:4.90B 2016:4.76B 2017:5.09B 2018:5.37B 2019:1.80B 2020:5.27B 2021:5.27B 2022:4.85B 2023:4.41B 2024:208.29M 2025:5.70B 2026:1.43B
  286                                       2014:809.67M 2015:1.17B 2016:1.17B 2017:1.26B 2018:1.27B 2019:1.26B 2020:1.23B 2021:1.15B 2022:1.14B 2023:1.12B 2024:1.20B 2025:1.21B 2026:361.43M
  368                                       2014:4.37B 2015:5.60B 2016:5.61B 2017:6.05B 2018:6.30B 2019:5.84B 2020:6.32B 2021:6.19B 2022:5.53B 2023:4.93B 2024:5.31B 2025:5.40B 2026:1.51B
  369                                       2014:2.12B 2015:3.27B 2016:3.06B 2017:3.07B 2018:3.06B 2019:3.01B 2020:2.98B 2021:2.92B 2022:2.98B 2023:3.67B 2024:3.58B 2025:3.32B 2026:1.23B
  372                                       2014:6.33B 2015:7.92B 2016:8.21B 2017:8.96B 2018:9.04B 2019:9.00B 2020:9.73B 2021:9.41B 2022:9.01B 2023:8.54B 2024:9.88B 2025:9.69B 2026:2.30B
  376                                       2014:3.36B 2015:4.57B 2016:4.36B 2017:4.75B 2018:4.80B 2019:4.40B 2020:4.93B 2021:4.96B 2022:4.09B 2023:3.65B 2024:3.96B 2025:4.14B 2026:1.21B
  386                                       2014:15.02B 2015:17.93B 2016:18.78B 2017:20.26B 2018:20.62B 2019:19.64B 2020:19.36B 2021:19.25B 2022:16.91B 2023:16.87B 2024:18.32B 2025:18.65B 2026:4.60B
  388                                       2014:5.02B 2015:5.93B 2016:5.98B 2017:6.56B 2018:6.65B 2019:6.64B 2020:7.39B 2021:7.18B 2022:7.07B 2023:6.82B 2024:7.23B 2025:7.11B 2026:1.72B
  390                                       2014:298.15M 2015:375.12M 2016:362.54M 2017:383.49M 2018:404.87M 2019:412.89M 2020:453.32M 2021:427.32M 2022:403.31M 2023:417.13M 2024:441.61M 2025:439.19M 2026:120.73M
  391                                       2014:6.56B 2015:10.20B 2016:9.67B 2017:9.43B 2018:10.41B 2019:9.41B 2020:9.25B 2021:8.85B 2022:8.09B 2023:8.37B 2024:8.21B 2025:7.78B 2026:2.31B
  392                                       2014:3.09B 2015:4.65B 2016:4.53B 2017:4.61B 2018:4.64B 2019:4.46B 2020:4.64B 2021:4.58B 2022:4.44B 2023:4.14B 2024:4.28B 2025:4.33B 2026:1.36B
  413                                       2014:4.20B 2015:5.43B 2016:5.27B 2017:5.73B 2018:5.72B 2019:5.28B 2020:5.89B 2021:5.78B 2022:5.22B 2023:4.38B 2024:4.63B 2025:4.76B 2026:1.37B
  417                                       2014:3.42B 2015:4.78B 2016:4.64B 2017:5.12B 2018:5.27B 2019:5.21B 2020:5.37B 2021:5.31B 2022:5.16B 2023:5.19B 2024:5.12B 2025:5.13B 2026:1.49B
  421                                       2014:1.09B 2015:1.29B 2016:1.25B 2017:1.31B 2018:1.32B 2019:1.31B 2020:1.50B 2021:1.32B 2022:1.26B 2023:1.21B 2024:1.22B 2025:1.23B 2026:315.11M
  424                                       2014:5.36B 2015:7.20B 2016:7.23B 2017:7.59B 2018:7.63B 2019:7.63B 2020:7.88B 2021:7.75B 2022:7.50B 2023:7.33B 2024:7.55B 2025:7.16B 2026:2.04B
  427                                       2014:6.33B 2015:8.10B 2016:8.42B 2017:9.09B 2018:9.53B 2019:9.42B 2020:9.90B 2021:9.90B 2022:9.65B 2023:9.18B 2024:9.69B 2025:9.60B 2026:2.43B
  443                                       2014:1.70B 2015:2.55B 2016:2.39B 2017:2.48B 2018:2.48B 2019:2.28B 2020:2.55B 2021:2.61B 2022:2.46B 2023:2.26B 2024:2.53B 2025:2.57B 2026:773.80M
  478                                       2014:3.57B 2015:4.68B 2016:4.73B 2017:5.09B 2018:5.22B 2019:4.57B 2020:4.60B 2021:4.80B 2022:4.82B 2023:4.30B 2024:4.66B 2025:4.65B 2026:1.39B
  524                                       2014:1.66B 2015:2.26B 2016:2.30B 2017:2.40B 2018:2.48B 2019:2.25B 2020:2.43B 2021:2.50B 2022:2.37B 2023:2.15B 2024:2.23B 2025:2.28B 2026:687.62M
  55                                        2014:699.20M 2015:877.06M 2016:948.83M 2017:1.09B 2018:1.18B 2019:1.15B 2020:1.24B 2021:1.16B 2022:1.22B 2023:1.11B 2024:1.19B 2025:1.14B 2026:298.79M
  64                                        2014:13.19B 2015:18.06B 2016:17.89B 2017:19.32B 2018:19.37B 2019:18.16B 2020:18.27B 2021:18.46B 2022:18.46B 2023:16.22B 2024:17.24B 2025:17.28B 2026:4.58B
  82                                        2014:3.48B 2015:4.49B 2016:4.54B 2017:4.80B 2018:4.84B 2019:4.70B 2020:5.09B 2021:5.00B 2022:4.37B 2023:4.54B 2024:5.14B 2025:5.30B 2026:1.33B
  87                                        2014:2.62B 2015:3.12B 2016:3.00B 2017:3.09B 2018:3.11B 2019:3.05B 2020:3.28B 2021:3.26B 2022:3.11B 2023:3.06B 2024:3.16B 2025:3.14B 2026:846.51M

## what

COUNTY: LOS ANGELES 24%, KERN 11%, VENTURA 10%, SAN BERNARDINO 9%, SAN MATEO 8%, MONTEREY 6%, ORANGE 6%, SAN LUIS OBISPO 6%, RIVERSIDE 6%, SAN DIEGO 4%, FRESNO 4%, SOLANO 4%

HYDRO_REGION: South Coast 35%, San Francisco Bay 13%, Sacramento River 11%, Tulare Lake 10%, Central Coast 10%, San Joaquin River 10%, Colorado River 5%, South Lahontan 4%, North Coast 1%

CLIMATE_ZONE: 12 17%, 9 12%, 13 11%, 3 11%, 8 9%, 6 9%, 11 7%, 16 6%, 15 6%, 14 5%, 10 4%, 7 3%

DWR_STANDARD_LEVEL: 2 (10-19% Shortage) 40%, 1 (Less than 10% Shortage) 35%, 0 (No Shortage Level Invoked) 17%, 3 (20-29% Shortage) 5%, Not Applicable 3%, 4 (30-39% Shortage) 0%, 5 (40-49% Shortage) 0%, WSCP Does Not Include Stages 0%, 1 (Less than 10% Shortage), 2  0%

DWR_STANDARD_LEVEL_FLAG: Reported as no Water Shortage  100%

POTABLE_SUPPLY_PRELIM_EST: Yes 100%

POTABLE_SUPPLY_MINUS_SOLD_FLAG: Flagged 100%

RES_FLAG: Flagged 100%

POTABLE_DEMAND_RES_PRELIM_EST: Yes 100%

POTABLE_DEMAND_PRELIM_EST: Yes 100%

POTABLE_SUPPLY_MINUS_SOLD_MINUS_AG_GAL_FLAG: Flagged 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ORG_ID | who | 72 | 0 | 524 143; 522 143; 495 143; 478 143 |
| SUPPLIER_NAME | who | 74 | 0 | City of Cerritos 143; City of Ceres 143; Casitas Municipal Water D 143; Carlsbad Municipal Water  143 |
| WATER_SYSTEM_ID | other | 74 | 0 | CA1910019 143; CA5010028 143; CA5610014,CA5610024 143; CA3710005 143 |
| COUNTY | category | 31 | 0 | LOS ANGELES 1.7K; KERN 751; VENTURA 699; SAN BERNARDINO 606 |
| HYDRO_REGION | category | 9 | 0 | South Coast 3.5K; San Francisco Bay 1.3K; Sacramento River 1.1K; Tulare Lake 1.0K |
| CLIMATE_ZONE | category | 16 | 0 | 12 1.5K; 9 1.1K; 13 999; 3 999 |
| REPORT_PERIOD_START_DATE | date | 143 | 0 | 2023-02-01T00:00:00 73; 2023-03-01T00:00:00 73; 2023-04-01T00:00:00 73; 2023-05-01T00:00:00 73 |
| REPORT_PERIOD_END_DATE | date | 143 | 0 | 2023-02-28T00:00:00 73; 2023-03-31T00:00:00 73; 2023-04-30T00:00:00 73; 2023-05-31T00:00:00 73 |
| POP_REPORT_PERIOD | other | 2.5K | 0 | 46300 145; 6032 127; 11147 118; 49041 117 |
| DWR_STANDARD_LEVEL | category | 10 | 6.4K | 2 (10-19% Shortage) 1.4K; 1 (Less than 10% Shortage 1.3K; 0 (No Shortage Level Invo 611; 3 (20-29% Shortage) 164 |
| DWR_STANDARD_LEVEL_FLAG | category | 2 | 9.9K | Reported as no Water Shor 101 |
| POTABLE_SUPPLY_GAL | amount | 3.0K | 7.1K | 300170682.69 15; 285706156.8 15; 365448413.52 15; 410249667.51 15 |
| POTABLE_SUPPLY_PRELIM_EST | category | 2 | 9.9K | Yes 135 |
| POTABLE_VOL_SOLD_GAL | amount | 505 | 7.1K | 0.0 2.4K; 7176216.573 4; 16155692.58 4; 1000.0 4 |
| POTABLE_SUPPLY_MINUS_SOLD_GAL | amount | 9.5K | 0 | 180886407.12 51; 300170682.69 50; 285706156.8 50; 365448413.52 50 |
| POTABLE_SUPPLY_MINUS_SOLD_FLAG | category | 2 | 10.0K | Flagged 3 |
| POTABLE_DEMAND_RES_GAL | amount | 10.0K | 0 | 157371174.1944 51; 148148157.15 50; 152807826.45000002 50; 183978733.11 50 |
| R_GPCD | amount | 10.1K | 0 | 64.08679278706396 50; 59.70548357792574 50; 74.28081924660853 50; 74.23366937828209 50 |
| RES_FLAG | category | 2 | 10.0K | Flagged 10 |
| POTABLE_DEMAND_RES_PRELIM_EST | category | 2 | 9.8K | Yes 151 |
| POTABLE_DEMAND_AG_GAL | amount | 766 | 4.7K | 0.0 4.4K; 260680.8 7; 377987.16 5; 260680.80000000002 5 |
| POTABLE_DEMAND_CII_IRR_GAL | amount | 4.3K | 4.6K | 0.0 127; 5000000.0 41; 37798716.0 31; 26068080.0 29 |
| POTABLE_DEMAND_CII_GAL | amount | 2.8K | 7.1K | 0.0 37; 58210022.63999999 15; 56561216.58 15; 68396124.89999999 15 |
| POTABLE_DEMAND_IRR_GAL | amount | 1.7K | 7.1K | 0.0 1.2K; 19880169.509999998 9; 28104648.75 9; 23471047.53 9 |
| POTABLE_DEMAND_O_GAL | amount | 1.7K | 7.1K | 0.0 711; 48877.65 36; 48623.380000000005 14; 81462.75 12 |
| POTABLE_DEMAND_PRELIM_EST | category | 2 | 9.9K | Yes 136 |
| RECYCLED_DEMAND_GAL | amount | 1.1K | 4.9K | 0.0 3.9K; 91140524.7 8; 977553.0 8; 20782776.78 7 |
| NON_POTABLE_DEMAND_PRELIM_EST | empty | 1 | 10.0K |  |
| POTABLE_SUPPLY_MINUS_SOLD_MINUS_AG_GAL | amount | 9.5K | 0 | 180886407.12 51; 299792695.53 50; 285445476.0 50; 365217059.31 50 |
| POTABLE_SUPPLY_MINUS_SOLD_MINUS_AG_GAL_FLAG | category | 2 | 10.0K | Flagged 13 |
| POTABLE_SUPPLY_MINUS_SOLD_ZSCORE | amount | 10.0K | 0 | 0.0 133; -0.6745 51; 0.6745 51; -0.030730103267798018 50 |
| POTABLE_DEMAND_RES_ZSCORE | amount | 9.5K | 0 | 0.0 104; -0.6745 51; -0.9062032077881762 50; -1.0285605941137819 50 |
| R_GPCD_ZSCORE | amount | 9.6K | 0 | 0.0 117; 0.6745 56; -0.47707255994856657 50; -1.0039177272238813 50 |
| POTABLE_SUPPLY_MINUS_SOLD_MINUS_AG_ZSCORE | amount | 9.8K | 0 | 0.0 129; -0.03996334607178545 50; -0.6640036417846804 50; -0.39796776167038683 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:51:22.53075 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8a2ce776-1251-48a6-98a7-5 10.0K |
| SRC_SHA256 | who | 1 | 0 | 672e89a2d01bc8ee5f1f51937 10.0K |
