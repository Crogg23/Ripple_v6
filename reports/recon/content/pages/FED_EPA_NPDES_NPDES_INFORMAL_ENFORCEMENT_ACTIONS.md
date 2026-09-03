# FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS

rows 478.9K  columns 14  scan 2.8s

roles: audit 2, category 4, date 1, id 2, other 5

## when

ACHIEVED_DATE
  1969         1  
  1975         9  
  1976         6  
  1977        10  
  1978        20  
  1979        47  
  1980      1.3K  ##
  1981      1.7K  ##
  1982      1.3K  ##
  1983      1.1K  #
  1984       645  #
  1985       948  #
  1986      1.4K  ##
  1987      2.2K  ###
  1988      3.2K  ####
  1989      3.9K  #####
  1990      4.7K  ######
  1991      5.0K  #######
  1992      4.9K  #######
  1993      3.9K  #####
  1994      4.3K  ######
  1995      5.1K  #######
  1996      4.5K  ######
  1997      5.4K  #######
  1998      6.2K  ########
  1999      7.3K  ##########
  2000      7.9K  ##########
  2001      7.7K  ##########
  2002      6.2K  ########
  2003      7.5K  ##########
  2004      7.5K  ##########
  2005     14.3K  ###################
  2006      8.1K  ###########
  2007      9.7K  #############
  2008      9.4K  #############
  2009     10.2K  ##############
  2010     12.1K  ################
  2011     18.7K  #########################
  2012     17.1K  #######################
  2013     17.7K  ########################
  2014     18.0K  ########################
  2015     20.8K  ############################
  2016     15.4K  ####################
  2017     19.0K  #########################
  2018     22.5K  ##############################
  2019     20.0K  ###########################
  2020     20.0K  ###########################
  2021     20.8K  ############################
  2022     21.1K  ############################
  2023     21.1K  ############################
  2024     20.3K  ###########################
  2025     21.0K  ############################
  2026      9.4K  #############
  2029         1  

## what

AGENCY: State 92%, EPA 8%

ENF_TYPE_CODE: LOVWL 43%, NOV 24%, AER 10%, NONC 7%, PHEMAIL 5%, UNDREV 4%, PHEMLS 4%, UNDREVS 1%, AERS 1%, ENFMTG 1%, NFAS 0%, LRE 0%

ENF_TYPE_DESC: Letter of Violation/ Warning L 43%, Notice of Violation 23%, Agency Enforcement Review 11%, Phone Call/ EMAIL 9%, Notice of Noncompliance Issued 6%, Under Review 5%, Enforcement Meeting 1%, No Further Action 0%, Letter to Regulated Entity 0%, Information Request Letter 0%, Oral Notification of Violation 0%, Compliance Agreement 0%

OFFICIAL_FLG: Y 73%, N 27%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPDES_ID | other | 119.4K | 0 | SC0000990 1.3K; GAIS14324 1.3K; SD0022624 1.3K; ALR10C131 1.3K |
| REGISTRY_ID | other | 115.1K | 0 | 110000353536 1.3K; 110072111727 1.3K; 110009791555 1.3K; 110070831074 1.3K |
| AGENCY | category | 2 | 0 | State 440.8K; EPA 38.1K |
| ACTIVITY_ID | id | 478.5K | 0 | 3200285087 1.3K; 3603534379 1.3K; 2200046224 1.3K; 3603388493 1.3K |
| ACTIVITY_TYPE_CODE | other | 1 | 0 | AIF 478.9K |
| ACTIVITY_TYPE_DESC | other | 1 | 0 | Administrative - Informal 478.9K |
| ENF_TYPE_CODE | category | 35 | 0 | LOVWL 205.0K; NOV 112.0K; AER 49.7K; NONC 31.0K |
| ENF_TYPE_DESC | category | 25 | 0 | Letter of Violation/ Warn 205.0K; Notice of Violation 112.0K; Agency Enforcement Review 53.5K; Phone Call/ EMAIL 42.5K |
| ACHIEVED_DATE | date | 12.9K | 6.3K | 08/29/2005 4.3K; 09/23/2005 3.0K; 10/16/2019 2.4K; 12/18/2013 2.4K |
| ENF_IDENTIFIER | id | 474.3K | 0 | SC-N00015676 1.3K; GA-NPDENF014319 1.3K; SD-200044430 1.3K; AL-39470010921285717 1.3K |
| OFFICIAL_FLG | category | 2 | 0 | Y 348.0K; N 130.8K |
| _INGESTED_AT | audit | 1 | 0 | 1786044028753063 478.9K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 2e0286a6-b615-4614-b1e4-d 478.9K |
| _SRC_SHA256 | other | 1 | 0 | 4efc9ba7de539755aa5d6cc8e 478.9K |
