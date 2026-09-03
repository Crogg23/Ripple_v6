# PORTAL_CKA_OPEN_DATA_SA_75596F44E9

rows 105  columns 14  scan 4.2s

roles: amount 3, audit 2, category 6, date 2, other 1, who 1

## when

TERMSEFFEC
  2006         2  ##
  2007         1  #
  2008         1  #
  2011         1  #
  2013         2  ##
  2014         8  #######
  2017        35  ##############################
  2018         4  ###
  2021         1  #

INGESTED_AT
  2026       105  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 105 | 0 | 56.64 | 3.6K | 4.3K | 40.0K |
| SHAPE__AREA | 105 | 9.37 | 303.0K | 19.04M | 23.38M | 214.44M |
| SHAPE__LENGTH | 105 | 10.91 | 3.2K | 38.6K | 39.7K | 635.4K |

## who

SRC_SHA256 by rows
       105  f6034780ae19bac9f59171e457266343bdb354391af6b826ee446c4e4318417e

SRC_SHA256 by dollars
       40.0K      105 rows  f6034780ae19bac9f59171e457266343bdb354391af6b826ee446c4e4318

## who x when

SRC_SHA256 by TERMSEFFEC, dollars = ACRES
  f6034780ae19bac9f59171e457266343bdb35439  2006:2.9K 2007:4.3K 2008:806.53 2011:130.33 2013:3.6K 2014:539.73 2017:1.9K 2018:1.8K 2021:131.25

## what

TYPE: Agricultural 50%, Public Improvement District (P 26%, Other 12%, Special Improvement District ( 7%, Water Control Improvement Dist 4%, Industrial 2%

NAME: Neal Rd 42%, IH10East/Loop 1604 Interchange 19%, US 281 Residential Areas 12%, Preserve at the Medina 10%, Gallagher Medina 4%, Talley Road 4%, Westside 211 PID 2%, Espada Area 2%, Lumberman Investment Corporati 2%, Fischer Gardens 1%, Espada PID No 1 1%, Lucero PID 1%

ORDYR: 2017 65%, 2013 11%, 2024 4%, 2022 4%, 2020 4%, 2018 4%, 0 2%, 2006 2%, 2023 1%, 2021 1%, 2019 1%

ORDINANCE: 201706220510 44%, 2017-08-31-0622 20%, 201703020131 13%, 12050876 10%, 201811290954 4%, 2013-12-05-0877 3%, 10121180 3%, 2024-06-20-0503 1%, 2024-06-20-0502 1%, 2022-10-20-0798 1%

ADDRESS: Talley Road 21%, S STATE HWY 16 
TX 14%, 15895 S STATE HWY 16 
TX 14%, Potranco and Hwy 211 7%, Hwy 90 and Grosenbacker Road 7%, Dietz Road and Old Fredricksbu 7%, Hwy 90 and Hwy211 7%, US HWY 87 7%, FM 2538 7%, FM1937 and US HIGHWAY 281 
TX 7%

TERMEXT: 30 Years 67%, 20 Years 17%, 30 years 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 104 | 0 | 105 1; 104 1; 103 1; 102 1 |
| TYPE | category | 6 | 0 | Agricultural 52; Public Improvement Distri 27; Other 13; Special Improvement Distr 7 |
| ACRES | amount | 98 | 0 | 2219.94353889 3; 639.50894349 3; 951.49897649 3; 166.20496125 1 |
| NAME | category | 32 | 0 | Neal Rd 35; IH10East/Loop 1604 Interc 16; US 281 Residential Areas 10; Preserve at the Medina 8 |
| ORDYR | category | 16 | 6 | 2017 62; 2013 10; 2024 4; 2022 4 |
| ORDINANCE | category | 28 | 10 | 201706220510 35; 2017-08-31-0622 16; 201703020131 10; 12050876 8 |
| TERMSEFFEC | date | 14 | 39 | 07/13/2017 - 07/13/2027 35; 2017-2033 10; 01/01/2014 - 01/01/2044 8; 11/29/2018 - 11/29/2048 3 |
| ADDRESS | category | 17 | 86 | Talley Road 3; S STATE HWY 16 
TX 2; 15895 S STATE HWY 16 
TX 2; Potranco and Hwy 211 1 |
| TERMEXT | category | 5 | 99 | 30 Years 4; 20 Years 1; 30 years 1 |
| SHAPE__AREA | amount | 99 | 0 | 11945316.5585938 3; 3443703.19921875 3; 5117138.37890625 3; 890308.06640625 1 |
| SHAPE__LENGTH | amount | 99 | 0 | 21777.5957688957 3; 10630.5186496637 3; 9268.60451670735 3; 5069.87461549757 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:32:13.92174 105 |
| SOURCE_RUN_ID | audit | 1 | 0 | e84c5196-12e3-4ddd-9ad6-c 105 |
| SRC_SHA256 | who | 1 | 0 | f6034780ae19bac9f59171e45 105 |
