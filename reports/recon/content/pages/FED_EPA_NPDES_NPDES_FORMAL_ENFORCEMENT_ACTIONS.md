# FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS

rows 112.4K  columns 13  scan 2.8s

roles: amount 2, audit 2, category 4, date 1, other 4

## when

SETTLEMENT_ENTERED_DATE
  1970         1  
  1973         1  
  1974         1  
  1976        15  
  1977        12  
  1978        23  
  1979        19  
  1980        42  
  1981        68  
  1982       100  #
  1983       298  ##
  1984       517  ####
  1985       863  ######
  1986       814  ######
  1987      1.1K  ########
  1988      1.8K  #############
  1989      2.0K  ##############
  1990      2.0K  ##############
  1991      2.2K  ################
  1992      2.2K  ################
  1993      2.0K  ##############
  1994      1.9K  #############
  1995      1.7K  ############
  1996      1.4K  ##########
  1997      1.7K  ############
  1998      2.4K  #################
  1999      2.1K  ###############
  2000      2.5K  #################
  2001      2.1K  ###############
  2002      2.5K  #################
  2003      3.3K  #######################
  2004      3.0K  #####################
  2005      2.9K  #####################
  2006      2.5K  #################
  2007      2.7K  ###################
  2008      2.8K  ####################
  2009      2.9K  #####################
  2010      3.2K  ######################
  2011      3.1K  ######################
  2012      2.9K  ####################
  2013      2.7K  ###################
  2014      3.1K  ######################
  2015      3.1K  ######################
  2016      3.2K  #######################
  2017      3.1K  ######################
  2018      3.4K  ########################
  2019      4.2K  ##############################
  2020      3.8K  ###########################
  2021      3.4K  ########################
  2022      3.7K  ##########################
  2023      3.8K  ###########################
  2024      3.7K  ##########################
  2025      3.3K  #######################
  2026      1.6K  ###########

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FED_PENALTY_ASSESSED_AMT | 4.5K | 0 | 23.0K | 6.70M | 3.35B | 8.13B |
| STATE_LOCAL_PENALTY_AMT | 48.1K | 0 | 3.0K | 507.0K | 57.01M | 1.50B |

## what

ACTIVITY_TYPE_CODE: AFR 95%, JDC 5%

ENF_TYPE_CODE: SCWAAPO 28%, STAOCO 23%, SCWAAO 22%, 309A 16%, CIV 5%, 309G2B 3%, 309G2A 1%, COL 1%, 309G2E 1%, 309G2E1 0%, OSUSREV 0%, 311B6B2 0%

ENF_TYPE_DESC: State CWA Penalty AO 28%, State Administrative Order of  23%, State CWA Non Penalty AO 22%, CWA 309A AO For Compliance 16%, Civil Judicial Action 5%, CWA 309G2B AO For Class II Pen 3%, CWA 309G2A AO For Class I Pena 1%, Collection Action 1%, CWA 309G2E AO For Class I Pena 1%, CWA 309G2E AO For Class I Pena 0%, Order of Suspension or Revocat 0%, CWA 311B6B2 AO For Class II Pe 0%

AGENCY: State 77%, EPA 23%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPDES_ID | other | 51.7K | 0 | PA0265420 563; KY0001821 563; ILL027723 562; WA0021164 562 |
| ENF_IDENTIFIER | other | 104.2K | 0 | LA-WECN090306 564; LA-WEC1400788 563; 07-2021-0003 562; 10-2024-0138 562 |
| ACTIVITY_ID | other | 105.1K | 0 | 1800074149 564; 3600024000 563; 3602845430 562; 3603994995 562 |
| ACTIVITY_TYPE_CODE | category | 2 | 0 | AFR 106.2K; JDC 6.2K |
| ENF_TYPE_CODE | category | 47 | 0 | SCWAAPO 30.9K; STAOCO 26.2K; SCWAAO 24.9K; 309A 18.2K |
| ENF_TYPE_DESC | category | 45 | 0 | State CWA Penalty AO 30.9K; State Administrative Orde 26.2K; State CWA Non Penalty AO 24.9K; CWA 309A AO For Complianc 18.2K |
| AGENCY | category | 2 | 0 | State 86.0K; EPA 26.4K |
| SETTLEMENT_ENTERED_DATE | date | 11.9K | 2.9K | 03/16/2020 710; 06/19/2019 553; 07/06/2017 549; 01/06/2010 549 |
| FED_PENALTY_ASSESSED_AMT | amount | 1.1K | 107.8K | 1024427 135; 483064 126; 1000 112; 300000 110 |
| STATE_LOCAL_PENALTY_AMT | amount | 11.1K | 64.2K | 1000 2.1K; 500 1.5K; 5000 1.3K; 2000 1.0K |
| _INGESTED_AT | audit | 1 | 0 | 1786044021142830 112.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | e32b1554-f62d-4e70-9716-f 112.4K |
| _SRC_SHA256 | other | 1 | 0 | 7ca17810ade4a917bd57e8d86 112.4K |
