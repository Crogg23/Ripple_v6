# PORTAL_SOC_NEW_YORK_STATE_O_49CD8C5B65

rows 161  columns 9  scan 3.7s

roles: audit 2, category 2, date 2, other 2, who 2

## when

ISSUE_DATE
  1984         1  ###
  1993         1  ###
  1994         2  #####
  1995         2  #####
  1996         5  ##############
  1997         7  ###################
  1998         4  ###########
  1999         5  ##############
  2000         1  ###
  2001         6  ################
  2002         2  #####
  2003         5  ##############
  2005         5  ##############
  2006         9  #########################
  2007         3  ########
  2008         6  ################
  2009         9  #########################
  2010         7  ###################
  2011        10  ###########################
  2012         7  ###################
  2013         5  ##############
  2014         3  ########
  2015         5  ##############
  2016         6  ################
  2017         7  ###################
  2018         7  ###################
  2019         7  ###################
  2020         3  ########
  2021        11  ##############################
  2022         4  ###########
  2023         3  ########
  2024         1  ###
  2025         2  #####

INGESTED_AT
  2026       161  ##############################

## who

STATUS by rows
       161  Issued

SRC_SHA256 by rows
       161  d3adf788fda1c11030d5ffad72d0947a39e508266f128ddac58bf7892d62b57f

## who x when

STATUS by ISSUE_DATE
  Issued                                    1984:1 1993:1 1994:2 1995:2 1996:5 1997:7 1998:4 1999:5 2000:1 2001:6 2002:2 2003:5 2005:5 2006:9 2007:3 2008:6 2009:9 2010:7 2011:10 2012:7 2013:5 2014:3 2015:5 2016:6 2017:7 2018:7 2019:7 2020:3 2021:11 2022:4 2023:3 2024:1 2025:2

SRC_SHA256 by ISSUE_DATE
  d3adf788fda1c11030d5ffad72d0947a39e50826  1984:1 1993:1 1994:2 1995:2 1996:5 1997:7 1998:4 1999:5 2000:1 2001:6 2002:2 2003:5 2005:5 2006:9 2007:3 2008:6 2009:9 2010:7 2011:10 2012:7 2013:5 2014:3 2015:5 2016:6 2017:7 2018:7 2019:7 2020:3 2021:11 2022:4 2023:3 2024:1 2025:2

## what

COUNTRY: United States 99%, Unitd States 1%

PATENT_ASSIGNEE_OWNER: Health Research, Inc, for Rosw 72%, Health Research, Inc. for Rosw 14%, Health Research, Inc. 4%, The Research Foundation for th 3%, Health Research, Inc, for Rosw 3%, Health Research, Inc, for Rosw 1%, Health Research, Inc. for Rosw 1%, Health Research, Inc., for Ros 1%, Health Research, Inc, for Rosw 1%, Bayer Pharma AG, Ardrea Biosci 1%, Health Research, Inc, for Rosw 1%, Health Research, Inc, for Rosw 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PATENT_NUMBER | other | 159 | 0 | 7,820,664 2; 16,318,787 1; 12,125,206 1; 11,773,181 B2 1 |
| STATUS | who | 1 | 0 | Issued 161 |
| ISSUE_DATE | date | 151 | 0 | 2010-10-26T00:00:00.000 3; 2019-11-26T00:00:00.000 2; 2016-03-29T00:00:00.000 2; 2013-12-17T00:00:00.000 2 |
| COUNTRY | category | 2 | 0 | United States 160; Unitd States 1 |
| PATENT_TITLE | other | 135 | 0 | Stress Protein Compositio 4; Compositions and Methods  3; Compositions and Methods  3; Method of Enhancing the E 3 |
| PATENT_ASSIGNEE_OWNER | category | 16 | 0 | Health Research, Inc, for 113; Health Research, Inc. for 22; Health Research, Inc. 6; The Research Foundation f 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:10:27.89514 161 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8f6864da-f710-4a24-9d65-8 161 |
| SRC_SHA256 | who | 1 | 0 | d3adf788fda1c11030d5ffad7 161 |
