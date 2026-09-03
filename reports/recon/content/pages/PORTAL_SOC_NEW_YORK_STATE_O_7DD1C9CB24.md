# PORTAL_SOC_NEW_YORK_STATE_O_7DD1C9CB24

rows 743  columns 11  scan 7.2s

roles: amount 2, audit 2, date 3, other 2, who 3

## when

CONTRACT_EXECUTION_DATE
  2009         1  
  2010        13  ###
  2011        15  ###
  2012         6  #
  2013        64  #############
  2014       100  ####################
  2015       149  ##############################
  2016       136  ###########################
  2017        81  ################
  2018       126  #########################
  2019        48  ##########

CONTRACT_END_DATE
  2013         5  #
  2014        11  ##
  2015        70  ################
  2016        39  #########
  2017        61  ##############
  2018        36  ########
  2019       133  ##############################
  2020        70  ################
  2021        17  ####
  2022        38  #########
  2029         1  

INGESTED_AT
  2026       743  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_CONTRACT_AMOUNT | 737 | 0 | 420.0K | 97.99M | 211.50M | 3.53B |
| AMOUNT_OF_CDBG_DR_FUNDS | 737 | 0 | 500.0K | 92.61M | 200.00M | 3.19B |

## who

CONTRACTOR_NAME by rows
        13  Brinnier and Larios, P.C.
         9  D&B Engineers and Architects, P.C.
         9  H2M Architects, Engineers, Land Surveying and Landscape Architecture, 
         7  Cameron Engineering & Associates, LLP
         6  Cashin Associates, P.C.
         6  Milone & Macbroom, Inc.
         6  Tetra Tech Inc
         6  Dewberry Engineers, Inc.
         6  Tectonic Engineering & Surveying Consultants PC
         5  Barton & Loguidice, D.P.C.
         5  N&P Engineers & Land Surveyor, PLLC
         5  Lamont Engineers, PC
         5  LiRo Engineers, Inc.
         4  City of Long Beach
         4  Louis K. McLean Associates Engineers & Surveyors, PC
         4  Keystone Associates Architects, Engineers & Surveyors, LLC
         4  TRC Engineers Inc
         4  Town of Hempstead
         4  LiRo Program and Construction Management, PE, P.C.
         4  Solar Liberty Energy Systems, Inc.

CONTRACTOR_NAME by dollars
     211.50M        1 rows  BBDO
     206.00M        2 rows  Dormitory Authority of the State of New York (DASNY)
     195.75M        2 rows  BSRJ A T/V
     146.16M        2 rows  Nassau County
     143.42M        1 rows  Long Island Power Authority
     127.20M        1 rows  Dormitory Authority of the State of New York  (DASNY)
     119.40M        1 rows  Prosource Technologies LLC
     111.20M        1 rows  New York State Offices of Parks, Recreations and Historic Pr
      99.80M        4 rows  Hunt Gulliot & Associates LLC (HGA)
      84.00M        1 rows  Innovative Emergency Management Inc (IEM)
      66.10M        1 rows  Freeport Housing Authority - Moxey Rigby LLC
      65.99M        1 rows  Armand Corporation
      63.60M        1 rows  TELACU Construction Management, Inc.
      58.13M        3 rows  LiRo Engineers Inc.
      56.65M        1 rows  Riverhead Apartments LLC
      51.95M        2 rows  Almas Construction LLC
      50.21M        4 rows  Town of Hempstead
      47.11M        1 rows  City of New York (Mayor's Office of Recovery & Resiliency/OR
      46.91M        6 rows  Tectonic Engineering & Surveying Consultants PC
      40.00M        1 rows  Empire State Development Corporation (ESD)

PROCURED_BY by rows
       327  HTFC/GOSR
        75  DASNY
        27  Town of Hempstead
        23  OPRHP
        15  Town of Babylon
        13  Nassau County
        13  HCR/GOSR
        10  The St. Bernard Project, Inc.
        10  Town of Union
        10  Town of Saugerties
         8  Village of Johnson City
         8  SSWCD
         8  Town of Oyster Bay
         7  Town of Esperance
         7  Town of Rosendale
         7  Essex County
         7  Village of Saugerties
         6  Town of Blooming Grove
         6  City of Long Beach
         5  Town of Windham

PROCURED_BY by dollars
       2.36B      327 rows  HTFC/GOSR
     358.66M       13 rows  HCR/GOSR
     255.82M       13 rows  Nassau County
     212.99M        5 rows  ESD
     103.28M       23 rows  OPRHP
      33.00M        2 rows  DOB/HTFC
      22.21M        2 rows  DEC/EFC (Nassau)
      20.53M        5 rows  City of New York (Mayor's Office of Recovery & Resiliency/OR
      19.73M        2 rows  Suffolk County
      14.49M       27 rows  Town of Hempstead
      11.48M        1 rows  DEC/EFC (Suffolk)
       7.95M       15 rows  Town of Babylon
       5.50M        6 rows  City of Long Beach
       5.46M       10 rows  The St. Bernard Project, Inc.
       4.69M        1 rows  City of Binghamton
       4.44M        2 rows  Town of Clarkstown
       4.41M       10 rows  Town of Union
       4.14M        4 rows  Town of Prattsville
       3.60M        8 rows  Town of Oyster Bay
       3.52M        1 rows  NYS DOT

SRC_SHA256 by rows
       743  52424b9f7279e61e204af7d6aace090d89528244e08e4e5f25bf3ad916d31210

SRC_SHA256 by dollars
       3.53B      743 rows  52424b9f7279e61e204af7d6aace090d89528244e08e4e5f25bf3ad916d3

## who x when

CONTRACTOR_NAME by CONTRACT_EXECUTION_DATE, dollars = TOTAL_CONTRACT_AMOUNT
  BBDO                                      2011:211.50M
  BSRJ A T/V                                2015:195.75M
  Barton & Loguidice, D.P.C.                2015:512.5K 2017:161.5K 2018:38.0K
  Brinnier and Larios, P.C.                 2015:1.05M 2016:203.8K 2017:143.7K 2018:369.7K
  Cameron Engineering & Associates, LLP     2010:0 2015:103.7K 2016:0 2018:1.01M
  Cashin Associates, P.C.                   2015:273.8K 2018:2.54M
  City of Long Beach                        2013:1.63M 2014:21.95M 2017:494.0K
  D&B Engineers and Architects, P.C.        2010:0 2014:3.00M 2015:1.05M 2016:352.0K
  Dewberry Engineers, Inc.                  2014:3.72M 2015:14.09M 2016:0 2018:1.12M 2019:1.00M
  Dormitory Authority of the State of New   2013:127.20M
  Dormitory Authority of the State of New   2013:6.00M 2014:200.00M
  H2M Architects, Engineers, Land Surveyin  2010:0 2011:0 2015:199.0K 2016:1.63M 2017:234.8K 2018:298.0K
  Hunt Gulliot & Associates LLC (HGA)       2014:46.94M 2015:26.86M 2018:26.00M
  Innovative Emergency Management Inc (IEM  2014:84.00M
  Keystone Associates Architects, Engineer  2015:397.7K 2016:229.7K
  Lamont Engineers, PC                      2015:507.5K 2016:33.3K 2018:124.5K
  LiRo Engineers, Inc.                      2009:0 2011:0 2017:0 2019:1.00M
  LiRo Program and Construction Management  2013:0 2018:1.21M
  Long Island Power Authority               2014:143.42M
  Louis K. McLean Associates Engineers & S  2015:443.1K 2017:59.7K 2018:1.19M
  Milone & Macbroom, Inc.                   2015:784.7K 2016:215.2K
  N&P Engineers & Land Surveyor, PLLC       2015:518.5K 2018:934.3K
  Nassau County                             2014:145.91M 2016:257.2K
  New York State Offices of Parks, Recreat  2014:111.20M
  Prosource Technologies LLC                2013:119.40M
  Solar Liberty Energy Systems, Inc.        2019:880.1K
  TRC Engineers Inc                         2014:6.85M 2015:450.0K
  Tectonic Engineering & Surveying Consult  2014:1.11M 2015:45.80M
  Tetra Tech Inc                            2013:3.47M 2014:3.46M 2015:2.06M 2016:170.6K
  Town of Hempstead                         2013:1.38M 2014:46.93M 2017:1.69M 2018:217.7K

PROCURED_BY by CONTRACT_EXECUTION_DATE, dollars = TOTAL_CONTRACT_AMOUNT
  City of Binghamton                        2017:4.69M
  City of Long Beach                        2013:742.0K 2015:4.36M 2018:405.9K
  City of New York (Mayor's Office of Reco  2014:12.44M 2016:8.09M
  DASNY                                     2009:0 2010:0 2011:0 2012:0 2013:0 2014:0 2016:51.9K 2017:130.8K 2018:0 2019:0
  DEC/EFC (Nassau)                          2015:22.21M
  DEC/EFC (Suffolk)                         2014:11.48M
  DOB/HTFC                                  2012:33.00M
  ESD                                       2011:211.50M 2013:1.44M 2015:42.0K
  Essex County                              2015:358.5K 2016:96.5K 2018:2.87M
  HCR/GOSR                                  2015:144.30M 2016:73.28M 2017:141.08M
  HTFC/GOSR                                 2011:998.2K 2013:362.26M 2014:1.15B 2015:530.81M 2016:149.63M 2017:84.90M 2018:53.88M 2019:23.27M
  NYS DOT                                   2013:3.52M
  Nassau County                             2015:197.68M 2016:57.51M 2018:64.9K 2019:565.0K
  OPRHP                                     2012:11.00M 2013:10.74M 2014:25.26M 2015:30.34M 2016:11.59M 2017:12.71M 2018:856.0K
  SSWCD                                     2015:357.1K 2017:161.5K 2018:1.07M 2019:1.24M
  Suffolk County                            2014:11.55M 2017:8.18M
  The St. Bernard Project, Inc.             2016:1.65M 2017:563.6K 2018:3.24M
  Town of Babylon                           2015:1.57M 2017:1.01M 2018:4.39M 2019:980.8K
  Town of Blooming Grove                    2015:448.5K 2016:352.0K 2018:319.1K 2019:599.0K
  Town of Clarkstown                        2018:4.44M
  Town of Esperance                         2015:253.0K 2016:96.1K 2017:452.0K 2018:32.9K 2019:727.0K
  Town of Hempstead                         2015:1.35M 2016:600.8K 2017:402.5K 2018:11.50M 2019:632.1K
  Town of Oyster Bay                        2015:219.3K 2018:3.38M
  Town of Prattsville                       2014:3.90M 2015:237.2K 2016:0
  Town of Rosendale                         2015:255.0K 2017:822.6K 2018:1.33M 2019:73.0K
  Town of Saugerties                        2015:179.6K 2016:493.3K 2017:143.7K 2018:758.3K
  Town of Union                             2016:1.04M 2017:294.5K 2018:3.07M
  Town of Windham                           2016:181.1K 2017:204.2K 2018:895.5K
  Village of Johnson City                   2015:90.5K 2016:1.01M 2018:514.9K
  Village of Saugerties                     2015:399.2K 2016:336.4K 2018:566.6K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CONTRACTOR_NAME | who | 528 | 0 | Brinnier and Larios, P.C. 13; H2M Architects, Engineers 9; D&B Engineers and Archite 9; Tetra Tech Inc 8 |
| DUNS_NUMBER | other | 476 | 0 | 05-499-2334 15; 18-460-3124 14; 05-773-2869 14; 02-067-1103 13 |
| PROCURED_BY | who | 87 | 0 | HTFC/GOSR 327; DASNY 75; Town of Hempstead 27; OPRHP 23 |
| CONTRACT_EXECUTION_DATE | date | 474 | 0 | 2013-10-01T00:00:00.000 16; 2014-11-25T00:00:00.000 11; 2014-11-24T00:00:00.000 11; 2014-12-05T00:00:00.000 8 |
| CONTRACT_END_DATE | date | 215 | 0 | nan 262; 2019-09-30T00:00:00.000 77; 2022-09-30T00:00:00.000 33; 2015-09-30T00:00:00.000 19 |
| TOTAL_CONTRACT_AMOUNT | amount | 560 | 0 | 0 80; 1000000 29; 3000000 19; 150000 10 |
| AMOUNT_OF_CDBG_DR_FUNDS | amount | 631 | 0 | 1000000 28; 3000000 19; 0 11; 150000 10 |
| BRIEF_DESCRIPTION_OF_CONTRACT | other | 449 | 0 | A/E Services 97; Code Enforcement Activiti 18; Advisory & Project Manage 13; Temporary Staffing Servic 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:11:02.88726 743 |
| SOURCE_RUN_ID | audit | 1 | 0 | 484d6461-c186-41a6-8786-4 743 |
| SRC_SHA256 | who | 1 | 0 | 52424b9f7279e61e204af7d6a 743 |
