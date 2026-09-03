# FED_EIA861_SALES_ULT_CUST

rows 2.8K  columns 27  scan 7.0s

roles: amount 13, audit 2, category 5, date 1, id 1, other 1, state 1, who 4

## when

_INGESTED_AT
  2026      2.8K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| REVENUES | 2.8K | -159.0K | 8.4K | 1.62M | 9.72M | 244.37M |
| SALES | 2.8K | -1.02M | 65.0K | 10.36M | 70.93M | 1.59B |
| CUSTOMERS | 2.8K | -524.3K | 6.4K | 1.05M | 5.24M | 157.93M |
| REVENUES_1 | 2.8K | -1.97M | 7.1K | 1.14M | 6.59M | 185.04M |
| SALES_1 | 2.8K | -28.19M | 61.7K | 11.99M | 55.94M | 1.74B |
| CUSTOMERS_1 | 2.8K | -2.4K | 948 | 124.3K | 653.3K | 22.11M |

## who

UNNAMED_2 by rows
       177  Adjustment 2024
        79  Sunnova
        45  Tesla Inc.
        34  Sunrun Inc.
        33  Palmetto Solar, LLC
        25  SunPower Capital, LLC
        20  Constellation NewEnergy, Inc
        19  Ahana Renewables, LLC
        19  Calpine Energy Solutions, LLC
        17  Greenbacker Renewable Energy Corporation
        17  Direct Energy Business
        16  BP Energy Retail LLC
        16  TerraForm US Energy Services, LLC
        15  MP2 Energy LLC
        14  ENGIE Resources LLC
        14  Direct Energy Services
        14  EverBright, LLC
        14  SmartEnergy Holdings, LLC
        14  Champion Energy Services
        13  WAPA-- Western Area Power Administration

UNNAMED_2 by dollars
       9.72M        1 rows  Florida Power & Light Co
       8.24M        2 rows  Pacific Gas & Electric Co.
       7.75M        2 rows  Southern California Edison Co
       6.15M      177 rows  Adjustment 2024
       4.67M        2 rows  Consolidated Edison Co-NY Inc
       4.51M        1 rows  Georgia Power Co
       4.27M        3 rows  Virginia Electric & Power Co
       4.14M        2 rows  Duke Energy Carolinas, LLC
       3.67M        1 rows  Duke Energy Florida, LLC
       3.65M        2 rows  Commonwealth Edison Co
       3.49M        1 rows  TXU Energy Retail Co, LLC
       3.33M        1 rows  Reliant Energy Retail Services
       3.05M        2 rows  DTE Electric Company
       3.03M        1 rows  Alabama Power Co
       2.87M        4 rows  FirstEnergy Pennsylvania Electric Co
       2.84M        2 rows  Duke Energy Progress - (NC)
       2.75M        2 rows  Public Service Elec & Gas Co
       2.56M        1 rows  Arizona Public Service Co
       2.49M        2 rows  Connecticut Light & Power Co
       2.39M        2 rows  Consumers Energy Co - (MI)

UNNAMED_1 by rows
       177  99999
        79  59579
        45  57313
        34  59647
        33  66026
        25  59580
        20  13374
        19  59622
        19  16840
        17  60025
        17  18193
        16  64314
        16  60981
        15  59808
        14  58956
        14  54820
        14  54862
        14  66036
        14  19107
        13  50046

UNNAMED_1 by dollars
       9.72M        1 rows  6452
       8.24M        2 rows  14328
       7.75M        2 rows  17609
       6.15M      177 rows  99999
       4.67M        2 rows  4226
       4.51M        1 rows  7140
       4.27M        3 rows  19876
       4.14M        2 rows  5416
       3.67M        1 rows  6455
       3.65M        2 rows  4110
       3.49M        1 rows  19327
       3.33M        1 rows  15847
       3.05M        2 rows  5109
       3.03M        1 rows  195
       2.87M        4 rows  66101
       2.84M        2 rows  3046
       2.75M        2 rows  15477
       2.56M        1 rows  803
       2.49M        2 rows  4176
       2.39M        2 rows  4254

UNNAMED_8 by rows
       746  PJM
       362  MISO
       262  ISNE
       172  TVA
       166  SWPP
       154  ERCO
       119  NYIS
        85  SOCO
        82  CISO
        70  BPAT
        58  WACM
        40  DUK
        39  AECI
        30  CPLE
        29  NEVP
        28  WALC
        26  PSCO
        25  PACE
        20  PACW
        19  PNM

UNNAMED_8 by dollars
      45.48M      746 rows  PJM
      31.76M      362 rows  MISO
      23.33M       82 rows  CISO
      22.17M      154 rows  ERCO
      13.24M      262 rows  ISNE
      13.18M       85 rows  SOCO
      12.41M      119 rows  NYIS
      10.34M       10 rows  FPL
      10.03M      166 rows  SWPP
       7.75M      172 rows  TVA
       5.82M       40 rows  DUK
       4.40M       30 rows  CPLE
       3.82M       11 rows  FPC
       2.76M       16 rows  AZPS
       2.45M       70 rows  BPAT
       2.23M       26 rows  PSCO
       2.20M       29 rows  NEVP
       2.17M        9 rows  LDWP
       2.07M        7 rows  SRP
       1.73M       25 rows  PACE

_SRC_FILE by rows
      2.8K  Sales_Ult_Cust_2024.xlsx

_SRC_FILE by dollars
     244.37M     2.8K rows  Sales_Ult_Cust_2024.xlsx

## who x when

UNNAMED_2 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = REVENUES
  Adjustment 2024                           2026:6.15M
  Ahana Renewables, LLC                     2026:0
  BP Energy Retail LLC                      2026:0
  Calpine Energy Solutions, LLC             2026:0
  Champion Energy Services                  2026:257.3K
  Commonwealth Edison Co                    2026:3.65M
  Consolidated Edison Co-NY Inc             2026:4.67M
  Constellation NewEnergy, Inc              2026:1.31M
  Direct Energy Business                    2026:0
  Direct Energy Services                    2026:1.64M
  Duke Energy Carolinas, LLC                2026:4.14M
  Duke Energy Florida, LLC                  2026:3.67M
  ENGIE Resources LLC                       2026:0
  EverBright, LLC                           2026:33.6K
  Florida Power & Light Co                  2026:9.72M
  Georgia Power Co                          2026:4.51M
  Greenbacker Renewable Energy Corporation  2026:6.20
  MP2 Energy LLC                            2026:84.7K
  Pacific Gas & Electric Co.                2026:8.24M
  Palmetto Solar, LLC                       2026:12.7K
  SmartEnergy Holdings, LLC                 2026:191.4K
  Southern California Edison Co             2026:7.75M
  SunPower Capital, LLC                     2026:179.2K
  Sunnova                                   2026:325.3K
  Sunrun Inc.                               2026:1.25M
  TXU Energy Retail Co, LLC                 2026:3.49M
  TerraForm US Energy Services, LLC         2026:0
  Tesla Inc.                                2026:369.8K
  Virginia Electric & Power Co              2026:4.27M
  WAPA-- Western Area Power Administration  2026:0

UNNAMED_1 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = REVENUES
  13374                                     2026:1.31M
  14328                                     2026:8.24M
  16840                                     2026:0
  17609                                     2026:7.75M
  18193                                     2026:0
  19107                                     2026:0
  19327                                     2026:3.49M
  19876                                     2026:4.27M
  4110                                      2026:3.65M
  4226                                      2026:4.67M
  50046                                     2026:0
  5416                                      2026:4.14M
  54820                                     2026:1.64M
  54862                                     2026:257.3K
  57313                                     2026:369.8K
  58956                                     2026:191.4K
  59579                                     2026:325.3K
  59580                                     2026:179.2K
  59622                                     2026:0
  59647                                     2026:1.25M
  59808                                     2026:84.7K
  60025                                     2026:6.20
  60981                                     2026:0
  64314                                     2026:0
  6452                                      2026:9.72M
  6455                                      2026:3.67M
  66026                                     2026:12.7K
  66036                                     2026:33.6K
  7140                                      2026:4.51M
  99999                                     2026:6.15M

## where

UNNAMED_6: TX 183, PA 140, OH 138, CA 125, IL 122, NY 119, NJ 108, MD 98, MA 91, TN 91, FL 69, WI 68

## what

UNNAMED_0: 2024 100%, To calculate a state or the US 0%, Data Year 0%

UNNAMED_3: A 65%, B 30%, D 3%, C 3%, Part 0%

UNNAMED_4: Bundled 68%, Energy 30%, Delivery 3%, Service Type 0%

UNNAMED_5: O 94%, I 6%, Data Type
O = Observed
I = Imp 0%

UNNAMED_7: Retail Power Marketer 32%, Cooperative 24%, Municipal 18%, Behind the Meter 12%, Investor Owned 10%, Political Subdivision 2%, Community Choice Aggregator 1%, Federal 1%, State 1%, Ownership 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | category | 3 | 0 | 2024 2.8K; To calculate a state or t 1; Data Year 1 |
| UNNAMED_1 | who | 1.5K | 1 | 99999 186; 59579 87; 57313 52; 66026 42 |
| UNNAMED_2 | who | 1.5K | 1 | Adjustment 2024 186; Sunnova 87; Tesla Inc. 52; Palmetto Solar, LLC 42 |
| UNNAMED_3 | category | 5 | 1 | A 1.8K; B 834; D 85; C 73 |
| UNNAMED_4 | category | 4 | 1 | Bundled 1.9K; Energy 834; Delivery 73; Service Type 1 |
| UNNAMED_5 | category | 3 | 1 | O 2.6K; I 177; Data Type
O = Observed
I  1 |
| UNNAMED_6 | state | 52 | 1 | TX 183; PA 140; OH 138; CA 125 |
| UNNAMED_7 | category | 10 | 178 | Retail Power Marketer 854; Cooperative 633; Municipal 462; Behind the Meter 315 |
| UNNAMED_8 | who | 58 | 28 | PJM 746; MISO 362; ISNE 262; TVA 172 |
| REVENUES | amount | 2.3K | 1 | 0 408; . 60; 50201.8 12; 35401.9 12 |
| SALES | amount | 2.3K | 1 | 0 408; . 60; 310 13; 6 13 |
| CUSTOMERS | amount | 2.3K | 1 | 0 383; . 60; 2 19; 1 15 |
| REVENUES_1 | amount | 2.3K | 1 | . 234; 0 158; 17599 13; 14498.1 13 |
| SALES_1 | amount | 2.4K | 1 | . 234; 0 157; 277998 13; 251829 13 |
| CUSTOMERS_1 | amount | 1.8K | 1 | . 234; 0 149; 1 65; 2 34 |
| REVENUES_2 | amount | 1.6K | 1 | 0 783; . 412; 39472.5 9; 10488.9 9 |
| SALES_2 | amount | 1.6K | 1 | 0 782; . 414; 587453 9; 139953 9 |
| CUSTOMERS_2 | amount | 550 | 1 | 0 781; . 414; 1 112; 2 81 |
| REVENUES_3 | amount | 91 | 1 | 0 1.6K; . 1.1K; -307.7 1; 27861.1 1 |
| SALES_3 | amount | 88 | 1 | 0 1.6K; . 1.1K; -3079 1; 335590 1 |
| CUSTOMERS_3 | amount | 9 | 1 | 0 1.6K; . 1.1K; 1 61; 2 12 |
| REVENUES_4 | amount | 2.8K | 1 | 0 43; 57071.5 14; 24987 14; 58182.8 14 |
| SALES_4 | id | 2.8K | 1 | 0 43; 865451 14; 391782 14; 367085 14 |
| CUSTOMERS_4 | other | 2.4K | 1 | 1 76; 2 30; 0 28; 3 24 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:39:39.77435 2.8K |
| _SOURCE_RUN_ID | audit | 1 | 0 | d386b6ac-c08a-4733-98c6-5 2.8K |
| _SRC_FILE | who | 1 | 0 | Sales_Ult_Cust_2024.xlsx 2.8K |
