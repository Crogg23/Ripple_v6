# FED_ITIS_EXPERTS

rows 197  columns 8  scan 2.1s

roles: audit 2, date 1, other 4, who 1

## when

UPDATE_DATE
  1998         1  #
  2000         6  #######
  2001        15  #################
  2002         8  #########
  2003        22  ########################
  2004        27  ##############################
  2005         8  #########
  2006         2  ##
  2007         4  ####
  2008         1  #
  2010        27  ##############################
  2011        21  #######################
  2012        12  #############
  2013         7  ########
  2014         5  ######
  2015         7  ########
  2016         2  ##
  2017         5  ######
  2018         8  #########
  2019         4  ####
  2020         2  ##
  2021         1  #
  2023         1  #
  2024         1  #

## who

SRC_SHA256 by rows
       197  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f5cf0f50cadf6c22e71debe21

## who x when

SRC_SHA256 by UPDATE_DATE
  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f  1998:1 2000:6 2001:15 2002:8 2003:22 2004:27 2005:8 2006:2 2007:4 2008:1 2010:27 2011:21 2012:12 2013:7 2014:5 2015:7 2016:2 2017:5 2018:8 2019:4 2020:2 2021:1 2023:1 2024:1

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| EXPERT_ID_PREFIX | other | 1 | 0 | EXP 197 |
| EXPERT_ID | other | 197 | 0 | 252 1; 251 1; 250 1; 249 1 |
| EXPERT | other | 196 | 0 | Chris A. Taylor 2; Daniela Arenas-Viveros 1; Matthew E. Neilson 1; Howard L. Jelks 1 |
| EXP_COMMENT | other | 185 | 0 | None 6; Research Botanist and Ass 2; Senior Curator, Missouri  2; National Museum of Natura 2 |
| UPDATE_DATE | date | 117 | 0 | 2010-10-05 22; 2003-09-26 7; 2011-07-25 6; 2004-04-09 6 |
| INGESTED_AT | audit | 1 | 0 | 1786164250570840 197 |
| SOURCE_RUN_ID | audit | 1 | 0 | 21ca1ab0-8d12-4dc1-a750-3 197 |
| SRC_SHA256 | who | 1 | 0 | d98c5f0cb5207f84bb56ef033 197 |
