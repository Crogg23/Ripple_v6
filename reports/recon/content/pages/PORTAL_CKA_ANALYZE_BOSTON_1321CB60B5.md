# PORTAL_CKA_ANALYZE_BOSTON_1321CB60B5

rows 156  columns 13  scan 3.1s

roles: amount 2, audit 2, category 3, date 2, other 4, who 1

## when

DATE_TIME
  2015        20  #############################
  2016        21  ##############################
  2017        14  ####################
  2018        10  ##############
  2019        11  ################
  2020        14  ####################
  2021        15  #####################
  2022        10  ##############
  2023        11  ################
  2024        16  #######################
  2025        14  ####################

INGESTED_AT
  2026       156  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X_CORD | 156 | 747.0K | 770.7K | 788.9K | 789.9K | 119.92M |
| Y_CORD | 156 | 2.91M | 2.95M | 2.97M | 2.97M | 459.13M |

## who

SRC_SHA256 by rows
       156  1e9d0324b3a32f645fe0e25c867a51e7b8fbf59d57454c8d783665735b5cc95f

SRC_SHA256 by dollars
     119.92M      156 rows  1e9d0324b3a32f645fe0e25c867a51e7b8fbf59d57454c8d783665735b5c

## who x when

SRC_SHA256 by DATE_TIME, dollars = X_CORD
  1e9d0324b3a32f645fe0e25c867a51e7b8fbf59d  2015:15.37M 2016:16.17M 2017:10.76M 2018:7.69M 2019:8.48M 2020:10.79M 2021:11.48M 2022:7.68M 2023:8.43M 2024:12.31M 2025:10.76M

## what

MODE_TYPE: ped 59%, mv 34%, bike 7%

LOCATION_TYPE: Intersection 59%, Street 41%

STREET: WASHINGTON ST 34%, CAMBRIDGE ST 10%, WOOD AVE 10%, COLUMBIA RD 7%, HUMBOLDT AVE 7%, CHELSEA ST 7%, BENNINGTON ST 7%, WALK HILL ST 7%, GENEVA AVE 3%, PARK ST 3%, NEWMARKET SQ 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATE_TIME | date | 157 | 0 | 2018-11-07 12:06:09+00 1; 2020-07-04 17:08:48+00 1; 2016-01-12 21:41:34+00 1; 2019-08-26 00:34:53+00 1 |
| MODE_TYPE | category | 3 | 0 | ped 92; mv 53; bike 11 |
| LOCATION_TYPE | category | 2 | 0 | Intersection 92; Street 64 |
| STREET | category | 46 | 92 | WASHINGTON ST 10; CAMBRIDGE ST 3; WOOD AVE 3; COLUMBIA RD 2 |
| XSTREET1 | other | 117 | 0 | MASSACHUSETTS AVE 11; MELNEA CASS BLVD 5; AMERICAN LEGION HWY 5; WASHINGTON ST 3 |
| XSTREET2 | other | 112 | 0 | WASHINGTON ST 7; MASSACHUSETTS AVE 7; DORCHESTER AVE 5; SEAVER ST 3 |
| X_CORD | amount | 147 | 0 | 771859.870000000000 3; 769445.790000000000 2; 776337.870000000000 2; 767885.270000000000 2 |
| Y_CORD | amount | 148 | 0 | 2946498.890000000000 3; 2946609.710000000000 2; 2949908.400000000000 2; 2933934.350000000000 2 |
| LONG | other | 148 | 0 | -71.07212419686832 3; -71.08105018996379 2; -71.05549749653231 2; -71.08704845767167 2 |
| LAT | other | 147 | 0 | 42.33254716094328 3; 42.33288413870876 2; 42.341840125671645 2; 42.29812323243154 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:35:25.42401 156 |
| SOURCE_RUN_ID | audit | 1 | 0 | f1c1fb1f-5675-416d-baac-0 156 |
| SRC_SHA256 | who | 1 | 0 | 1e9d0324b3a32f645fe0e25c8 156 |
