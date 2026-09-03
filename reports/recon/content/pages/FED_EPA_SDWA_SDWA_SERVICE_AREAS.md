# FED_EPA_SDWA_SDWA_SERVICE_AREAS

rows 422.5K  columns 9  scan 2.4s

roles: audit 2, category 2, date 2, other 3

## when

FIRST_REPORTED_DATE
  2005      3.1K  #####
  2006      8.1K  #############
  2007      4.4K  #######
  2008     18.9K  ##############################
  2009      4.4K  #######
  2010      5.8K  #########
  2011      3.6K  ######
  2012      2.8K  ####
  2013      3.9K  ######
  2014      5.1K  ########
  2015      2.5K  ####
  2016      2.7K  ####
  2017      2.6K  ####
  2018      2.8K  ####
  2019      3.5K  ######
  2020      2.8K  ####
  2021      1.9K  ###
  2022      1.8K  ###
  2023      2.4K  ####
  2024      2.2K  ####
  2025      2.0K  ###
  2026      2.2K  ####

LAST_REPORTED_DATE
  1995    117.3K  #######################
  1996     21.8K  ####
  1997      8.4K  ##
  1998      3.3K  #
  1999      4.1K  #
  2000      3.4K  #
  2001     12.1K  ##
  2002      6.1K  #
  2003      4.1K  #
  2004      3.4K  #
  2005     11.0K  ##
  2006      5.0K  #
  2007      4.0K  #
  2008      4.0K  #
  2009      3.7K  #
  2010      3.5K  #
  2011      3.6K  #
  2012      3.3K  #
  2013      3.2K  #
  2014      3.0K  #
  2015      3.1K  #
  2016      3.3K  #
  2017      3.0K  #
  2018      3.1K  #
  2019      2.8K  #
  2020      2.5K  
  2021      2.5K  
  2022      2.6K  #
  2023      2.4K  
  2024      2.8K  #
  2025     12.2K  ##
  2026    152.6K  ##############################

## what

SERVICE_AREA_TYPE_CODE: RS 17%, OT 16%, RA 15%, PA 13%, OA 12%, SC 5%, MH 5%, IA 4%, HM 4%, SS 3%, ON 3%, MU 2%

IS_PRIMARY_SERVICE_AREA_CODE: Y 98%, N 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SUBMISSIONYEARQUARTER | other | 1 | 0 | 2026Q2 422.5K |
| PWSID | other | 379.9K | 0 | WY5680249 2.1K; WY5680243 2.1K; WY5680237 2.1K; WY5680236 2.1K |
| SERVICE_AREA_TYPE_CODE | category | 28 | 0 | RS 64.8K; OT 58.4K; RA 56.6K; PA 48.8K |
| IS_PRIMARY_SERVICE_AREA_CODE | category | 2 | 99.5K | Y 316.8K; N 6.2K |
| FIRST_REPORTED_DATE | date | 2.2K | 332.9K | 02/27/2008 14.1K; 08/19/2014 2.8K; 06/24/2013 1.7K; 02/16/2010 1.7K |
| LAST_REPORTED_DATE | date | 3.2K | 1.3K | 07/22/1995 53.1K; 07/24/1995 41.0K; 06/26/2026 22.0K; 05/29/2026 17.9K |
| _INGESTED_AT | audit | 1 | 0 | 1786044262222211 422.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | df7923a4-b2b9-47fa-93e2-7 422.5K |
| _SRC_SHA256 | other | 1 | 0 | 12e674ac32484a544421b6052 422.5K |
