# FED_EPA_RCRA_EVALUATIONS

rows 1.17M  columns 11  scan 2.9s

roles: audit 2, category 4, date 1, other 3, state 1

## when

EVALUATION_START_DATE
  1901         3  
  1911         1  
  1919         3  
  1920         1  
  1930         1  
  1954         1  
  1955         1  
  1961         1  
  1977         2  
  1979         1  
  1980        26  
  1981       293  
  1982       585  
  1983      3.0K  ##
  1984     14.7K  ############
  1985     18.4K  ###############
  1986     20.9K  #################
  1987     21.4K  #################
  1988     23.5K  ###################
  1989     23.9K  ###################
  1990     25.7K  #####################
  1991     29.2K  ########################
  1992     29.7K  ########################
  1993     30.4K  #########################
  1994     37.1K  ##############################
  1995     30.6K  #########################
  1996     30.4K  #########################
  1997     30.5K  #########################
  1998     30.8K  #########################
  1999     27.4K  ######################
  2000     27.0K  ######################
  2001     28.1K  #######################
  2002     27.7K  ######################
  2003     29.2K  ########################
  2004     30.3K  ########################
  2005     29.9K  ########################
  2006     31.1K  #########################
  2007     31.9K  ##########################
  2008     32.5K  ##########################
  2009     34.6K  ############################
  2010     34.4K  ############################
  2011     31.6K  ##########################
  2012     31.5K  #########################
  2013     29.7K  ########################
  2014     31.7K  ##########################
  2015     28.3K  #######################
  2016     28.4K  #######################
  2017     26.7K  ######################
  2018     26.7K  ######################
  2019     23.3K  ###################
  2020     18.8K  ###############
  2021     21.9K  ##################
  2022     25.0K  ####################
  2023     22.8K  ##################
  2024     23.2K  ###################
  2025     21.9K  ##################
  2026      9.8K  ########

## where

ACTIVITY_LOCATION: NJ 85.6K, CO 74.6K, FL 71.0K, NC 64.7K, PA 57.9K, KY 55.3K, OH 45.9K, CA 44.1K, NY 43.6K, MI 41.9K, TN 39.6K, GA 34.3K

## what

EVALUATION_TYPE: CEI 53%, FCI 12%, NRR 11%, CSE 5%, FSD 5%, FRR 4%, CAV 3%, SNY 2%, SNN 2%, FUI 2%, CDI 1%, GME 1%

EVALUATION_DESC: COMPLIANCE EVALUATION INSPECTI 54%, FOCUSED COMPLIANCE INSPECTION 12%, NON-FINANCIAL RECORD REVIEW 11%, COMPLIANCE SCHEDULE EVALUATION 5%, FINANCIAL RECORD REVIEW 4%, FACILITY SELF DISCLOSURE 4%, COMPLIANCE ASSISTANCE VISIT 3%, SIGNIFICANT NON-COMPLIER 2%, NO LONGER A SIGNIFICANT NON-CO 2%, FOLLOW-UP INSPECTION 2%, Facility Self Disclosure 1%, CASE DEVELOPMENT INSPECTION 1%

EVALUATION_AGENCY: S   92%, E   5%, C   1%, B   1%, X   0%, L   0%, T   0%, N   0%

FOUND_VIOLATION: N   66%, Y   33%, U   1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID_NUMBER | other | 309.6K | 0 | COR000218263 4.4K; COR000210997 4.3K; COR000212175 4.3K; COR000212803 4.3K |
| ACTIVITY_LOCATION | state | 63 | 0 | NJ 85.6K; CO 74.6K; FL 71.0K; NC 64.7K |
| EVALUATION_IDENTIFIER | other | 1.6K | 0 | 001 543.5K; 000 137.1K; 002 57.5K; 003 27.4K |
| EVALUATION_TYPE | category | 15 | 0 | CEI 617.0K; FCI 135.8K; NRR 129.1K; CSE 59.3K |
| EVALUATION_DESC | category | 16 | 0 | COMPLIANCE EVALUATION INS 617.0K; FOCUSED COMPLIANCE INSPEC 135.8K; NON-FINANCIAL RECORD REVI 129.1K; COMPLIANCE SCHEDULE EVALU 59.3K |
| EVALUATION_AGENCY | category | 8 | 0 | S   1.07M; E   64.0K; C   15.6K; B   12.1K |
| EVALUATION_START_DATE | date | 14.6K | 0 | 07/16/2012 3.0K; 08/27/2009 3.0K; 08/31/2009 3.0K; 08/28/2009 3.0K |
| FOUND_VIOLATION | category | 3 | 0 | N   775.2K; Y   381.0K; U   10.1K |
| INGESTED_AT | audit | 1 | 0 | 1786163847152640 1.17M |
| SOURCE_RUN_ID | audit | 1 | 0 | ee35a6a3-0939-44ee-a263-f 1.17M |
| SRC_SHA256 | other | 1 | 0 | 8457e99a525f9546773bc2e3f 1.17M |
