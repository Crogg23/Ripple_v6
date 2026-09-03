# FED_FEC_API

rows 500  columns 23  scan 3.4s

roles: amount 1, audit 2, category 6, date 2, empty 5, other 2, state 1, who 4

## when

CONTRIBUTION_RECEIPT_DATE
  2000         1  
  2005         2  
  2006         1  
  2007         1  
  2012         4  
  2015         4  
  2017         4  
  2018         1  
  2019         2  
  2020        41  ###
  2021        16  #
  2022       423  ##############################

LOAD_DATE
  2025       421  ##############################
  2026        79  ######

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CONTRIBUTION_RECEIPT_AMOUNT | 500 | -35.5K | 4.17 | 10.0K | 50.0K | 192.4K |

## who

CONTRIBUTOR_NAME by rows
        16  UNAVAILABLE, NAME
         6  WHITMAN, TRUDY
         6  BORTH, DONNA E
         6  LEWIS, LINDA B
         5  MUHLESTEIN, RALPH K. MR.
         5  LEWIS, REGINA
         5  SHAW, MADELINE
         5  HASWELL, HOLLEE
         5  PHILLIPS, RICHARD
         5  BLACK, DIANNE
         5  BARGER, DEBORAH
         5  WALICKE, PATRICIA
         4  HESSELINK, RONDA
         4  BOEHLKE, CLAUDIA
         4  COOMBER, ALAN
         4  HOSKINS, PATRICIA
         4  SMITH, DOREEN
         4  ROCHETTE, EDWARD
         4  GEORGE, SUSAN
         4  WILSON, FRED

CONTRIBUTOR_NAME by dollars
       50.0K        1 rows  SIMONS, NATHANIEL
       13.7K        1 rows  DUDA, JENNIFER
       12.0K        4 rows  WILSON, FRED
       12.0K        3 rows  WEISSMAN, ANDY
       12.0K        3 rows  WILSON, JOANNE
       10.0K        1 rows  DERRICK, JIM
       10.0K        1 rows  ABRAMSON, RONALD
       10.0K        1 rows  PATMAN, CARRIN F.
       10.0K        1 rows  PATRICK, KATHY D.
       10.0K        1 rows  SAROFIM, LOUISA STUDE
       10.0K        1 rows  ZAVITSANOS, JONI
        7.3K        1 rows  CONSERVATIVE CONNECTOR LLC
        5.5K        1 rows  DUDA, KENNETH JAMES
        5.0K        1 rows  KOHNERT, PEGGIE
        5.0K        1 rows  REGIONS PAC
        5.0K        1 rows  INTERNATIONAL ASSOC OF MACHINISTS & AEROSPACE WOR
        4.4K        1 rows  SLAUGHTER, DENISE
        4.0K        1 rows  NAVE, ALISA
        3.8K       16 rows  UNAVAILABLE, NAME
        3.5K        1 rows  LINN, RANDY

CONTRIBUTOR_EMPLOYER by rows
       344  RETIRED
        17  SELF-EMPLOYED
         8  SELF- EMPLOYED
         8  UNION SQUARE VENTURES
         5  N/A
         4  NOT EMPLOYED
         4  CDM
         3  ORANGE COUNTY TRANSIT
         3  MISSIPPI LEGISLATURE
         3  INDIVISIBLE DESOTO
         2  UNITEDHEALTH GROUP
         2  WINKLEVOSS CAPITAL MANAGEMENT, LLC
         2  ALARM CENTRAL
         2  BMG
         2  BILL TWINE
         1  STANTEC CONSULTING
         1  COMPASS HEALTH
         1  ST. JOHN'S SCHOOL
         1  WILLIS KNIGHTON HEALTH
         1  MAIN STREET TITLE

CONTRIBUTOR_EMPLOYER by dollars
       50.0K        1 rows  MERITAGE GROUP LP
       29.6K       17 rows  SELF-EMPLOYED
       27.0K        8 rows  UNION SQUARE VENTURES
       24.5K        5 rows  N/A
       15.2K        4 rows  NOT EMPLOYED
       13.5K      344 rows  RETIRED
       10.0K        1 rows  BUCHANAN INGERSOLL & ROONEY
       10.0K        1 rows  GIBBS & BRUNS LLP
        6.2K        2 rows  WINKLEVOSS CAPITAL MANAGEMENT, LLC
        5.5K        1 rows  ARISTA NETWORKS, INC.
        4.0K        1 rows  CORNERSTONE GOVERNMENT AFFAIRS
        3.5K        1 rows  LINN PRODUCTS, INC.
        3.1K        1 rows  BAIN CAPITAL
        2.9K        1 rows  ALLEY CORP
        2.9K        1 rows  KINDER MORGAN INC.
        2.8K        1 rows  GRANT ME THE WISDOM FOUNDATION
        2.0K        1 rows  ST. JOHN'S SCHOOL
        2.0K        1 rows  SELF EMPLOYED
        1.5K        1 rows  PURSUIT TRANSFORMATION COMPANY, INC
        1.5K        1 rows  VARIANT

CONTRIBUTOR_OCCUPATION by rows
       346  RETIRED
         9  PHYSICIAN
         8  NOT EMPLOYED
         6  PARTNER
         5  HAIRDRESSER
         4  HCA
         4  DRIVER
         4  INVESTOR
         3  AUTHOR
         3  REALTOR
         3  MS STATE HOUSE REPRESENTATIVE
         3  ATTORNEY
         3  CHAIR
         2  LCSW
         2  DIRECTOR
         2  MANAGER
         2  VENTURE CAPITAL INVESTOR
         2  LANDSCAPE CONTRACTOR
         2  SECURTY
         1  REAL ESTATE

CONTRIBUTOR_OCCUPATION by dollars
       59.2K        4 rows  INVESTOR
       26.1K        8 rows  NOT EMPLOYED
       20.5K        3 rows  ATTORNEY
       17.1K        6 rows  PARTNER
       13.7K      346 rows  RETIRED
       13.6K        9 rows  PHYSICIAN
       12.0K        3 rows  AUTHOR
       10.0K        1 rows  ARTIST
       10.0K        2 rows  VENTURE CAPITAL INVESTOR
        7.0K        3 rows  REALTOR
        5.5K        1 rows  EXECUTIVE
        4.0K        1 rows  GOVERNMENT AFFAIRS
        3.5K        1 rows  OWNER PRESIDENT
        2.9K        1 rows  FOUNDER & CEO
        2.9K        1 rows  EXECUTIVE CHAIRMAN
        2.8K        1 rows  EXECUTIVE DIRECTOR
        2.5K        1 rows  CONSULTING MINISTER
        2.0K        1 rows  MIDDLE SCHOOL TEACHER
        1.5K        1 rows  ENTREPRENEUR
        1.5K        1 rows  CO-FOUNDER & GENERAL PARTNER

_SRC_SHA256 by rows
       500  685e60920b48aca9f96b129bfb4ad1ab3bc4105ee4d528598707c8a39c05bd84

_SRC_SHA256 by dollars
      192.4K      500 rows  685e60920b48aca9f96b129bfb4ad1ab3bc4105ee4d528598707c8a39c05

## who x when

CONTRIBUTOR_NAME by CONTRIBUTION_RECEIPT_DATE, dollars = CONTRIBUTION_RECEIPT_AMOUNT
  ABRAMSON, RONALD                          2006:10.0K
  BARGER, DEBORAH                           2022:3.01
  BLACK, DIANNE                             2020:134.03 2021:48.90
  BOEHLKE, CLAUDIA                          2022:2
  BORTH, DONNA E                            2022:13.68
  COOMBER, ALAN                             2022:4.68
  DERRICK, JIM                              2020:10.0K
  DUDA, JENNIFER                            2022:13.7K
  GEORGE, SUSAN                             2022:66.68
  HASWELL, HOLLEE                           2022:10.50
  HESSELINK, RONDA                          2022:1
  HOSKINS, PATRICIA                         2022:0.68
  LEWIS, LINDA B                            2022:1.02
  LEWIS, REGINA                             2022:1.84
  MUHLESTEIN, RALPH K. MR.                  2022:13.35
  PATMAN, CARRIN F.                         2021:10.0K
  PATRICK, KATHY D.                         2020:10.0K
  PHILLIPS, RICHARD                         2022:-126
  ROCHETTE, EDWARD                          2022:9.18
  SAROFIM, LOUISA STUDE                     2020:10.0K
  SHAW, MADELINE                            2022:9.51
  SIMONS, NATHANIEL                         2022:50.0K
  SMITH, DOREEN                             2022:1.34
  UNAVAILABLE, NAME                         2017:470 2018:40 2019:400 2020:2.4K 2021:520
  WALICKE, PATRICIA                         2022:21.67
  WEISSMAN, ANDY                            2022:12.0K
  WHITMAN, TRUDY                            2022:36.67
  WILSON, FRED                              2022:12.0K
  WILSON, JOANNE                            2022:12.0K
  ZAVITSANOS, JONI                          2020:10.0K

CONTRIBUTOR_EMPLOYER by CONTRIBUTION_RECEIPT_DATE, dollars = CONTRIBUTION_RECEIPT_AMOUNT
  ALARM CENTRAL                             2022:8.34
  ALLEY CORP                                2022:2.9K
  ARISTA NETWORKS, INC.                     2022:5.5K
  BAIN CAPITAL                              2022:3.1K
  BILL TWINE                                2022:16.66
  BMG                                       2022:33.34
  BUCHANAN INGERSOLL & ROONEY               2006:10.0K
  CDM                                       2022:1
  COMPASS HEALTH                            2005:1.0K
  CORNERSTONE GOVERNMENT AFFAIRS            2020:4.0K
  GIBBS & BRUNS LLP                         2020:10.0K
  GRANT ME THE WISDOM FOUNDATION            2020:2.8K
  INDIVISIBLE DESOTO                        2020:1.0K 2021:40
  KINDER MORGAN INC.                        2021:2.9K
  LINN PRODUCTS, INC.                       2005:3.5K
  MAIN STREET TITLE                         2022:8.33
  MERITAGE GROUP LP                         2022:50.0K
  MISSIPPI LEGISLATURE                      2020:120 2021:20 2022:100
  N/A                                       2020:14.5K 2021:10.0K
  NOT EMPLOYED                              2020:1.5K 2022:13.7K
  ORANGE COUNTY TRANSIT                     2022:21.66
  RETIRED                                   2012:625 2020:10.0K 2022:2.9K
  SELF- EMPLOYED                            2022:27.02
  SELF-EMPLOYED                             2020:17.6K 2021:48.90 2022:11.9K
  ST. JOHN'S SCHOOL                         2020:2.0K
  STANTEC CONSULTING                        2022:8.33
  UNION SQUARE VENTURES                     2022:27.0K
  UNITEDHEALTH GROUP                        2022:1.66
  WILLIS KNIGHTON HEALTH                    2022:16.67
  WINKLEVOSS CAPITAL MANAGEMENT, LLC        2022:6.2K

## where

CONTRIBUTOR_STATE: TX 56, FL 51, CA 42, NY 41, MS 25, NC 19, AZ 15, MI 15, WA 15, GA 14, OK 13

## what

COMMITTEE_ID: C00808311 80%, C00931220 8%, C00099267 3%, C00699744 3%, C00010603 1%, C00394957 1%, C00662767 1%, C00550970 1%, C00193433 1%, C00905471 0%, C00785899 0%, C00167346 0%

CANDIDATE_ID: H4GA07275 100%

REPORT_TYPE: MY 78%, YE 13%, M7 3%, Q1 2%, Q3 1%, M3 1%, Q2 1%, M2 0%, M4 0%, 12R 0%, M12 0%

FILING_FORM: F3X 93%, F3 7%

ENTITY_TYPE: IND 96%, CAN 2%, PAC 1%, CCM 1%, ORG 0%, COM 0%

IS_INDIVIDUAL: True 95%, False 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TRANSACTION_ID | other | 504 | 1 | SA.1126708.1.SV01 3; SA.1131258.1.SV01 3; SA.1126687.1.SV01 3; SA.1126952.1.SV01 3 |
| COMMITTEE_ID | category | 25 | 0 | C00808311 388; C00931220 41; C00099267 15; C00699744 13 |
| CANDIDATE_ID | category | 2 | 499 | H4GA07275 1 |
| CONTRIBUTOR_NAME | who | 333 | 0 | UNAVAILABLE, NAME 16; WHITMAN, TRUDY 7; LEWIS, LINDA B 7; WALICKE, PATRICIA 6 |
| CONTRIBUTOR_EMPLOYER | who | 61 | 46 | RETIRED 344; SELF-EMPLOYED 17; SELF- EMPLOYED 8; UNION SQUARE VENTURES 8 |
| CONTRIBUTOR_OCCUPATION | who | 62 | 45 | RETIRED 346; PHYSICIAN 9; NOT EMPLOYED 8; PARTNER 6 |
| CONTRIBUTOR_ZIP | other | 312 | 29 | 719538024 7; 100108219 7; 863367114 6; 075061433 6 |
| CONTRIBUTOR_STATE | state | 46 | 17 | TX 56; FL 51; CA 42; NY 41 |
| CONTRIBUTION_RECEIPT_AMOUNT | amount | 79 | 0 | 4.17 108; 1.67 81; 0.17 38; 0.83 36 |
| CONTRIBUTION_RECEIPT_DATE | date | 81 | 0 | 2022-05-26 388; 2022-04-13 7; 2022-04-16 6; 2020-06-30 4 |
| REPORT_TYPE | category | 11 | 0 | MY 390; YE 64; M7 15; Q1 9 |
| FILING_FORM | category | 2 | 0 | F3X 465; F3 35 |
| ENTITY_TYPE | category | 7 | 1 | IND 477; CAN 10; PAC 6; CCM 3 |
| PARTY | empty | 1 | 500 |  |
| OFFICE | empty | 1 | 500 |  |
| ELECTION_YEAR | empty | 1 | 500 |  |
| STATE | empty | 1 | 500 |  |
| DISTRICT | empty | 1 | 500 |  |
| IS_INDIVIDUAL | category | 2 | 0 | True 476; False 24 |
| LOAD_DATE | date | 26 | 0 | 2025-07-31T04:06:24 390; 2026-03-15T03:05:48 41; 2025-07-30T04:06:20 15; 2026-03-11T03:06:01 13 |
| _INGESTED_AT | audit | 1 | 0 | 1783007621650445 500 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 0789b9e1-fa01-45b3-9c1b-d 500 |
| _SRC_SHA256 | who | 1 | 0 | 685e60920b48aca9f96b129bf 500 |
