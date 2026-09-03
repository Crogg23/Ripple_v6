# FED_ITIS_GEOGRAPHIC_DIV

rows 480.4K  columns 6  scan 2.1s

roles: audit 2, category 1, date 1, other 2

## when

UPDATE_DATE
  1900         1  
  1996     26.2K  ####################
  1997      2.0K  ##
  1998      4.6K  ####
  1999       476  
  2000     16.7K  #############
  2001     19.5K  ###############
  2002      2.3K  ##
  2003      7.0K  #####
  2004     10.9K  ########
  2005     13.6K  ###########
  2006     10.7K  ########
  2007     23.0K  ##################
  2008      6.1K  #####
  2009      1.1K  #
  2010     13.0K  ##########
  2011     20.5K  ################
  2012     11.2K  #########
  2013     14.2K  ###########
  2014     14.6K  ###########
  2015     19.4K  ###############
  2016     14.2K  ###########
  2017     14.7K  ###########
  2018     20.9K  ################
  2019     38.7K  ##############################
  2020     35.8K  ############################
  2021     33.7K  ##########################
  2022     20.0K  ###############
  2023     15.8K  ############
  2024     17.9K  ##############
  2025     25.4K  ####################
  2026      5.9K  #####

## what

GEOGRAPHIC_VALUE: North America 23%, Southern Asia 16%, South America 13%, Africa 12%, Europe & Northern Asia (exclud 10%, Middle America 8%, Australia 7%, Caribbean 4%, Indo-West Pacific 3%, Oceania 2%, Western Atlantic Ocean 2%, East Pacific 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TSN | other | 409.0K | 0 | 1283184 2.4K; 1283116 2.4K; 1283115 2.4K; 1283114 2.4K |
| GEOGRAPHIC_VALUE | category | 13 | 0 | North America 109.5K; Southern Asia 74.6K; South America 60.9K; Africa 59.1K |
| UPDATE_DATE | date | 451 | 0 | 1996-11-05 26.2K; 2021-12-19 13.4K; 2019-09-28 13.3K; 2001-12-20 12.5K |
| INGESTED_AT | audit | 1 | 0 | 1786164250570840 480.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 21ca1ab0-8d12-4dc1-a750-3 480.4K |
| SRC_SHA256 | other | 1 | 0 | d98c5f0cb5207f84bb56ef033 480.4K |
