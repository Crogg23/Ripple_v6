# FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS

rows 21.9K  columns 13  scan 2.0s

roles: audit 2, category 4, date 1, other 5, who 1

## when

ACHIEVED_DATE
  1970         1  
  1998         1  
  1999         4  
  2000        11  
  2001        71  #
  2002       407  ########
  2003      1.5K  #############################
  2004      1.1K  #####################
  2005      1.3K  ##########################
  2006      1.2K  #######################
  2007      1.0K  ####################
  2008      1.1K  ######################
  2009      1.3K  ##########################
  2010      1.4K  ###########################
  2011      1.5K  ##############################
  2012      1.4K  ############################
  2013       860  #################
  2014      1.0K  ####################
  2015       572  ###########
  2016       486  #########
  2017       341  #######
  2018       322  ######
  2019       357  #######
  2020       442  #########
  2021       448  #########
  2022       490  ##########
  2023       249  #####
  2024       294  ######
  2025       315  ######
  2026       483  #########

## who

_SRC_SHA256 by rows
     21.9K  4264581de159dd9128df2157fae2f3a9e047ddf9286bb6a7ae383461e9879390

## who x when

_SRC_SHA256 by ACHIEVED_DATE
  4264581de159dd9128df2157fae2f3a9e047ddf9  1970:1 1998:1 1999:4 2000:11 2001:71 2002:407 2003:1.5K 2004:1.1K 2005:1.3K 2006:1.2K 2007:1.0K 2008:1.1K 2009:1.3K 2010:1.4K 2011:1.5K 2012:1.4K 2013:860 2014:1.0K 2015:572 2016:486 2017:341 2018:322 2019:357 2020:442 2021:448 2022:490 2023:249 2024:294 2025:315 2026:483

## what

PGM_SYS_ACRNM: ICIS 79%, RCRAINFO 14%, SFDW 5%, SSTS 1%, TRIS 1%, NCDB 0%, RMP 0%, STATE 0%, OH-CORE 0%, ND-FP 0%, BR 0%, TSCA 0%

ENF_TYPE_CODE: NOV 57%, NONC 29%, LOVWL 14%

ENF_TYPE_DESC: Notice of Violation 57%, Notice of Noncompliance Issued 29%, Letter of Violation/ Warning L 14%

STATUTE: SDWA 44%, TSCA 19%, RCRA 15%, FIFRA 14%, EPCRA 3%, CAA 3%, CWA 2%, CERCLA 0%, AIM 0%, MPRSA 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PGM_SYS_ACRNM | category | 20 | 0 | ICIS 17.2K; RCRAINFO 3.0K; SFDW 1.2K; SSTS 250 |
| PGM_SYS_ID | other | 15.2K | 0 | MID980991566 112; OHD048415665 111; IND000646950 111; 3602060263 111 |
| REGISTRY_ID | other | 14.8K | 0 | 110013687929 143; 110017718594 114; 110072238033 112; 110072219301 112 |
| AGENCY | other | 1 | 0 | EPA 21.9K |
| ACTIVITY_TYPE_CODE | other | 1 | 0 | AIF 21.9K |
| ENF_TYPE_CODE | category | 3 | 0 | NOV 12.6K; NONC 6.3K; LOVWL 3.0K |
| ENF_TYPE_DESC | category | 3 | 0 | Notice of Violation 12.6K; Notice of Noncompliance I 6.3K; Letter of Violation/ Warn 3.0K |
| ACHIEVED_DATE | date | 4.2K | 1.9K | 03/27/2006 202; 12/04/2012 193; 05/09/2003 193; 04/25/2011 164 |
| ENF_IDENTIFIER | other | 18.8K | 0 | 06-200057591 122; 06-200206814 112; 06-200286212 111; 03-200029354 110 |
| STATUTE | category | 10 | 0 | SDWA 9.5K; TSCA 4.2K; RCRA 3.3K; FIFRA 3.0K |
| _INGESTED_AT | audit | 1 | 0 | 1785096200489384 21.9K |
| _SOURCE_RUN_ID | audit | 1 | 0 | dcaf75a6-f232-4aa7-be50-0 21.9K |
| _SRC_SHA256 | who | 1 | 0 | 4264581de159dd9128df2157f 21.9K |
