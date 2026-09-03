# FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS

rows 106.0K  columns 13  scan 2.3s

roles: amount 1, audit 2, category 5, date 1, id 2, other 2

## when

SETTLEMENT_ENTERED_DATE
  1972         1  
  1973        10  
  1974        32  
  1975        96  #
  1976       101  #
  1977       142  #
  1978       130  #
  1979       113  #
  1980        86  #
  1981       133  #
  1982       136  #
  1983       159  #
  1984       263  ##
  1985       400  ###
  1986       590  ####
  1987       520  ####
  1988       742  #####
  1989       785  ######
  1990      1.0K  #######
  1991      1.0K  #######
  1992      1.0K  #######
  1993      1.4K  ##########
  1994      1.9K  #############
  1995      1.5K  ###########
  1996      1.5K  ###########
  1997      1.8K  #############
  1998      2.2K  ################
  1999      2.3K  ################
  2000      2.5K  ##################
  2001      3.5K  #########################
  2002      3.8K  ###########################
  2003      4.1K  #############################
  2004      3.8K  ###########################
  2005      4.1K  #############################
  2006      3.9K  ############################
  2007      3.5K  #########################
  2008      3.9K  ###########################
  2009      4.2K  ##############################
  2010      3.7K  ##########################
  2011      3.7K  ##########################
  2012      3.1K  ######################
  2013      3.3K  ########################
  2014      3.4K  ########################
  2015      3.0K  #####################
  2016      3.1K  ######################
  2017      2.5K  ##################
  2018      2.8K  ####################
  2019      3.0K  #####################
  2020      2.5K  #################
  2021      2.7K  ###################
  2022      3.1K  ######################
  2023      2.8K  ####################
  2024      2.6K  ##################
  2025      2.1K  ###############
  2026      1.1K  ########

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PENALTY_AMOUNT | 106.0K | 0 | 2.2K | 787.8K | 100.73M | 5.81B |

## what

ACTIVITY_TYPE_CODE: AFR 95%, JDC 5%

ACTIVITY_TYPE_DESC: Administrative - Formal 95%, Judicial 5%

STATE_EPA_FLAG: S 65%, L 20%, E 15%

ENF_TYPE_CODE: SCAAAO 83%, 113D1 6%, CIV 5%, 113A 5%, 113DWD 1%, 113D1E1 0%, 120 0%, 325 0%, 3008A 0%, 113 0%, 113D1E 0%, 311B6B2 0%

ENF_TYPE_DESC: Administrative Order 83%, CAA 113D1 Action For Penalty 6%, Civil Judicial Action 5%, CAA 113A Admin Compliance Orde 5%, CAA 113D Withdrawn 1%, CAA 113D1 Action For Penalty - 0%, CAA 120 AO For Noncompliance P 0%, EPCRA 325 Action For Penalty 0%, RCRA 3008A AO For Comp And/Or  0%, CAA 113 Notice Of Violation 0%, CAA 113D1 Action For Penalty - 0%, CWA 311B6B2 AO For Class II Pe 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PGM_SYS_ID | other | 38.2K | 0 | CASJV00006029S0037 770; CABAA00006013A0010 545; CASJV00006029S1738 538; CASJV00006029S1547 538 |
| ACTIVITY_ID | id | 101.1K | 0 | 3600354879 550; 3603724602 535; 3605017356 531; 3604013808 531 |
| ENF_IDENTIFIER | id | 101.0K | 0 | TX000A300485682003235 550; 03-2023-7005 535; 06-2026-3307 531; PA000A0000E00000000430023 531 |
| ACTIVITY_TYPE_CODE | category | 2 | 0 | AFR 100.7K; JDC 5.3K |
| ACTIVITY_TYPE_DESC | category | 2 | 0 | Administrative - Formal 100.7K; Judicial 5.3K |
| STATE_EPA_FLAG | category | 3 | 0 | S 69.3K; L 20.9K; E 15.8K |
| ENF_TYPE_CODE | category | 47 | 0 | SCAAAO 87.8K; 113D1 6.7K; CIV 5.3K; 113A 4.8K |
| ENF_TYPE_DESC | category | 45 | 0 | Administrative Order 87.8K; CAA 113D1 Action For Pena 6.7K; Civil Judicial Action 5.3K; CAA 113A Admin Compliance 4.8K |
| SETTLEMENT_ENTERED_DATE | date | 11.8K | 41 | 10/20/2001 550; 03/16/2026 545; 06/08/2022 544; 02/10/2025 534 |
| PENALTY_AMOUNT | amount | 10.5K | 0 | 0 33.4K; 1000 2.7K; 2000 2.4K; 500 2.4K |
| _INGESTED_AT | audit | 1 | 0 | 1785966236108491 106.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 113e8522-bb16-43d2-8799-3 106.0K |
| _SRC_SHA256 | other | 1 | 0 | 2c7e0626060f567954658e7e2 106.0K |
