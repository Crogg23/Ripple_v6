# PORTAL_CKA_HOUSTON_OPEN_DAT_5B1522DD22

rows 10.0K  columns 16  scan 3.3s

roles: amount 3, audit 2, category 4, date 2, id 1, other 2, who 3

## when

RECEIPT_DT
  2012       310  ##############################
  2013        85  ########

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_COLLECTED | 10.0K | -55.6K | 154.03 | 637.92 | 55.6K | 1.79M |
| PERMIT_FEE | 10.0K | -37.8K | 129.03 | 206.46 | 37.8K | 1.36M |
| CANCEL_FEE | 10.0K | 0 | 0 | 157.15 | 55.6K | 111.3K |

## who

APPLICANT_NAME by rows
        44  *A T & T
        33  *HISD/CFS CONTRACT ADMINISTRATION
        30  *HISD-CONTRACT ADMINISTRATION
        20  *HISD/CONTRACT ADMINISTRATION
        19  *PUBLIC STORAGE
        19  *TEXAS PETROLEUM GROUP
        19  *WHATABURGER RESTAURANTS LLC
        17  *BANK OF AMERICA
        15  *CASH AMERICA
        14  *HOUSTON COMMUNITY COLLEGE SYSTEM
        14  *BOXER PROPERTY
        14  *AUTOZONE TEXAS, L.P.
        13  *CITY OF HOUSTON/BUILDING SVCS DEPT
        12  *CONTINENTAL AIRLINES
        12  *TEXAS TACO CABANA, LP
        12  *LUBY'S FUDDRUCKERS RESTAURANT LLC
        12  *HISD CONTRACT ADMIN
        11  *WEINGARTEN REALTY INVESTORS
        10  *EMERALD FOOD'S INC.
        10  *EZ PAWN CORP / JULIE GAITAN

APPLICANT_NAME by dollars
        7.6K       33 rows  *HISD/CFS CONTRACT ADMINISTRATION
        7.3K       44 rows  *A T & T
        7.0K       19 rows  *WHATABURGER RESTAURANTS LLC
        6.9K       30 rows  *HISD-CONTRACT ADMINISTRATION
        6.7K       14 rows  *HOUSTON COMMUNITY COLLEGE SYSTEM
        4.6K       20 rows  *HISD/CONTRACT ADMINISTRATION
        4.0K       14 rows  *AUTOZONE TEXAS, L.P.
        3.9K        6 rows  *GREAT VALUE STORAGE
        3.2K       19 rows  *TEXAS PETROLEUM GROUP
        2.9K       17 rows  *BANK OF AMERICA
        2.9K       19 rows  *PUBLIC STORAGE
        2.8K       12 rows  *HISD CONTRACT ADMIN
        2.5K        6 rows  *JACK IN THE BOX
        2.5K       14 rows  *BOXER PROPERTY
        2.3K       15 rows  *CASH AMERICA
        2.1K        9 rows  *HISD-CONTRACT ADMINISTRATION/BLDG 17
        2.1K       12 rows  *CONTINENTAL AIRLINES
        2.0K       10 rows  *MCDONALD'S
        1.8K       12 rows  *TEXAS TACO CABANA, LP
        1.6K        7 rows  *FAMILY DOLLAR STORES OF TX, LP

PAYEE_ZIP by rows
       302  77055
       274  77007
       261  77092
       251  77087
       237  77041
       218  77036
       192  77054
       174  77057
       173  77043
       173  77008
       167  77081
       159  77018
       158  77029
       148  77080
       144  77042
       141  77022
       140  77040
       139  77063
       136  77093
       135  77020

PAYEE_ZIP by dollars
       52.1K      274 rows  77007
       50.9K      302 rows  77055
       45.6K      261 rows  77092
       44.2K      251 rows  77087
       40.4K      218 rows  77036
       39.5K      237 rows  77041
       35.2K      192 rows  77054
       31.7K      173 rows  77008
       30.9K      158 rows  77029
       30.8K      174 rows  77057
       29.0K      173 rows  77043
       28.9K      167 rows  77081
       26.8K      148 rows  77080
       26.5K      159 rows  77018
       26.0K      144 rows  77042
       25.7K      140 rows  77040
       24.2K      133 rows  77024
       23.9K      141 rows  77022
       23.6K      124 rows  77017
       23.0K      135 rows  77020

SRC_SHA256 by rows
     10.0K  e964d5a1798d870a5bda294f4d4b5b08936d662061c20f141d51719253b1a7bd

SRC_SHA256 by dollars
       1.79M    10.0K rows  e964d5a1798d870a5bda294f4d4b5b08936d662061c20f141d51719253b1

## who x when

APPLICANT_NAME by RECEIPT_DT, dollars = TOTAL_COLLECTED
  *A T & T                                  2012:154.03
  *BANK OF AMERICA                          2012:308.06
  *BOXER PROPERTY                           2012:154.03
  *EZ PAWN CORP / JULIE GAITAN              2012:154.03 2013:0
  *HISD-CONTRACT ADMINISTRATION             2012:231.46
  *LUBY'S FUDDRUCKERS RESTAURANT LLC        2012:154.03
  *PUBLIC STORAGE                           2012:308.06
  *TEXAS TACO CABANA, LP                    2012:154.03
  *WEINGARTEN REALTY INVESTORS              2012:225

PAYEE_ZIP by RECEIPT_DT, dollars = TOTAL_COLLECTED
  77007                                     2012:925.01 2013:0
  77008                                     2012:951.61 2013:289.31
  77017                                     2012:-258.06 2013:-132.15
  77018                                     2012:154.03
  77020                                     2012:231.46 2013:0
  77022                                     2012:308.06
  77024                                     2012:616.12
  77029                                     2012:458.06 2013:0
  77036                                     2012:918.55 2013:289.31
  77040                                     2012:270.97 2013:0
  77041                                     2012:308.89 2013:-157.15
  77042                                     2012:-91.11
  77043                                     2012:304.03 2013:-421.48
  77054                                     2012:154.03
  77055                                     2012:-258.06 2013:157.15
  77057                                     2012:308.06
  77063                                     2012:323.01 2013:154.03
  77080                                     2012:791.12
  77081                                     2012:462.92 2013:-283.06
  77087                                     2012:1.2K
  77092                                     2012:1.1K 2013:154.03
  77093                                     2012:-154.03

## what

NO_CHRG: Y 100%

PERMIT_COUNT: 1 97%, -1 3%, 261 0%, -261 0%

UNITS: 1 79%, 2 11%, 3 3%, -1 2%, 4 2%, 6 1%, 5 1%, 8 0%, 7 0%, -2 0%, 9 0%, 10 0%

OF_YEARS_PAID: 1 88%, 2 6%, 3 5%, 0 1%, 4 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RECEIPT_DT | date | 197 | 9.6K | 2013-01-02 00:00:00 3; 2012-12-28 00:00:00 3; 2012-12-20 00:00:00 3; 2012-12-18 00:00:00 3 |
| RECEIPT_NO | id | 10.1K | 2 | 5266310 50; 5266307 50; 5266306 50; 5266305 50 |
| PROJECT_NO | other | 9.3K | 2 | 07108807 52; 05008528 50; 04096751 50; 04120598 50 |
| APPLICANT_NAME | who | 8.7K | 2 | *A T & T 74; *HOUSTON COMMUNITY COLLEG 62; *HISD/CONTRACT ADMINISTRA 60; *WHATABURGER RESTAURANTS  60 |
| ADDRESS | other | 9.0K | 2 | 4409 NEW ORLEANS ST 77020 52; 150 NORTH SAM HOUSTON EAS 50; 2422 BAY AREA BLVD 77058 50; 823 ANTOINE DR 77024 50 |
| PAYEE_ZIP | who | 557 | 2 | 77055 302; 77007 274; 77092 261; 77087 251 |
| NO_CHRG | category | 2 | 9.9K | Y 71 |
| TOTAL_COLLECTED | amount | 72 | 0 | 154.03 6.6K; 231.46 1.6K; 283.06 428; 412.09 368 |
| PERMIT_COUNT | category | 4 | 0 | 1 9.7K; -1 261; 261 1; -261 1 |
| UNITS | category | 35 | 0 | 1 7.8K; 2 1.1K; 3 289; -1 206 |
| PERMIT_FEE | amount | 17 | 0 | 129.03 7.5K; 206.46 1.9K; 125 260; -129.03 147 |
| OF_YEARS_PAID | category | 6 | 2 | 1 8.8K; 2 577; 3 514; 0 68 |
| CANCEL_FEE | amount | 24 | 0 | 0 9.7K; 154.03 131; 231.46 26; 157.15 21 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:56:31.75295 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c6fece23-9bb1-43e8-bf28-3 10.0K |
| SRC_SHA256 | who | 1 | 0 | e964d5a1798d870a5bda294f4 10.0K |
