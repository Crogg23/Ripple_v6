# FED_ITIS_JURISDICTION

rows 161.9K  columns 7  scan 2.2s

roles: audit 2, category 2, date 1, other 2

## when

UPDATE_DATE
  1997         3  
  1998         4  
  1999       907  #
  2000     31.9K  ##############################
  2001       165  
  2002       891  #
  2003       190  
  2004      2.1K  ##
  2005     11.9K  ###########
  2006      5.2K  #####
  2007     19.2K  ##################
  2008      2.9K  ###
  2009      2.1K  ##
  2010      5.0K  #####
  2011     11.6K  ###########
  2012      4.6K  ####
  2013      8.9K  ########
  2014      7.0K  #######
  2015      2.4K  ##
  2016      2.6K  ##
  2017      2.5K  ##
  2018      3.6K  ###
  2019      7.1K  #######
  2020     10.6K  ##########
  2021      5.2K  #####
  2022      3.2K  ###
  2023      2.3K  ##
  2024      2.4K  ##
  2025      4.3K  ####
  2026      1.1K  #

## what

JURISDICTION_VALUE: Continental US 55%, Canada 15%, Mexico 15%, Hawaii 6%, Alaska 4%, Caribbean Territories 4%, Central Pacific Territories 0%, Caribbean territories 0%

ORIGIN: Native 91%, Introduced 7%, Incidental 1%, Native & Introduced 0%, Native & Extinct 0%, Native & Extirpated 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TSN | other | 116.4K | 0 | 1283061 811; 1281719 811; 1280667 811; 1279645 811 |
| JURISDICTION_VALUE | category | 8 | 0 | Continental US 88.7K; Canada 24.9K; Mexico 24.4K; Hawaii 9.5K |
| ORIGIN | category | 6 | 0 | Native 148.1K; Introduced 11.7K; Incidental 1.2K; Native & Introduced 641 |
| UPDATE_DATE | date | 343 | 0 | 2000-03-15 31.8K; 2007-02-09 6.1K; 2013-12-23 4.8K; 2007-04-10 4.8K |
| INGESTED_AT | audit | 1 | 0 | 1786164250570840 161.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | 21ca1ab0-8d12-4dc1-a750-3 161.9K |
| SRC_SHA256 | other | 1 | 0 | d98c5f0cb5207f84bb56ef033 161.9K |
