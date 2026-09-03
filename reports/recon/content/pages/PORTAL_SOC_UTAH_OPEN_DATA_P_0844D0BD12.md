# PORTAL_SOC_UTAH_OPEN_DATA_P_0844D0BD12

rows 2.0K  columns 20  scan 3.6s

roles: audit 2, category 7, date 2, id 1, other 3, who 6

## when

DATEAPPROVED
  2020      2.0K  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## who

BUSINESSNAME by rows
         1  GRANGER MEDICAL CLINIC, PC
         1  BARNEY TRUCKING INCORPORATED
         1  HB BOYS, L.C.
         1  RULON HARPER CONSTRUCTION INC.
         1  CENTRAL UTAH CLINIC PC
         1  FIRE ENGINEERING COMPANY, INC.
         1  A&K RAILROAD MATERIALS, INC.
         1  ECOBRITE SERVICES, LLC.
         1  JOHN H. FIRMAGE, INC.
         1  POLATECHNO CO., LTD
         1  MIDWEST COMMERCIAL INTERIORS
         1  WAVETRNOIX LLC
         1  LOW VA RATES, LLC
         1  SIERRA FOREST PRODUCTS, INC
         1  UTAH NAVAJO HEALTH SYSTEM, INC.
         1  SHIPEX INC.
         1  TRES ENTERPRISES, INC.
         1  MORGAN ASPHALT INC
         1  SIZZLING PLATTER, LLC
         1  KNDRS LLC

LENDER by rows
       515  Zions Bank, A Division of
       199  KeyBank National Association
       190  Cache Valley Bank
       131  JPMorgan Chase Bank, National Association
        75  Bank of Utah
        65  Mountain America FCU
        50  Altabank
        49  Continental Bank
        39  First Utah Bank
        38  Readycap Lending, LLC
        38  Central Bank
        37  Goldenwest FCU
        28  State Bank of Southern Utah
        28  America First FCU
        28  Wells Fargo Bank, National Association
        27  Cross River Bank
        27  Bank of America, National Association
        26  Glacier Bank
        24  U.S. Bank, National Association
        24  Celtic Bank Corporation

NAICSCODE by rows
        81  441110
        70  238220
        51  236220
        50  238210
        46  511210
        37  238990
        37  484110
        35  453998
        31  238910
        29  541110
        29  236115
        24  722513
        24  621111
        22  238110
        21  237310
        21  238160
        20  541330
        20  524210
        19  531311
        18  323111

NAICS_DESCRIPTION by rows
       125  Building Equipment Contractors
       118  Vehicle Dealers
       107  Merchant Wholesalers
        73  Structural Contractors
        68  Specialty Trade Contractors
        67  NonResidential Building Construction
        60  Residential Building Construction
        58  Fabricated Metal Manufacturing
        46  Software Publishers
        42  Building Finishing Contractors
        40  Misc Manufacturing
        37  Truck Transportation
        35  Retail Stores Misc
        32  Merchant Wholesalers Nondurable goods
        29  Law Offices
        28  Computer Product Manufacturing
        27  Machinery Manufacturing
        24  Physicians
        24  Limited Service Restaurants
        23  Furniture Manufacturing

## who x when

BUSINESSNAME by DATEAPPROVED
  A&K RAILROAD MATERIALS, INC.              2020:1
  BARNEY TRUCKING INCORPORATED              2020:1
  CENTRAL UTAH CLINIC PC                    2020:1
  ECOBRITE SERVICES, LLC.                   2020:1
  FIRE ENGINEERING COMPANY, INC.            2020:1
  GRANGER MEDICAL CLINIC, PC                2020:1
  HB BOYS, L.C.                             2020:1
  JOHN H. FIRMAGE, INC.                     2020:1
  KNDRS LLC                                 2020:1
  LOW VA RATES, LLC                         2020:1
  MIDWEST COMMERCIAL INTERIORS              2020:1
  MORGAN ASPHALT INC                        2020:1
  POLATECHNO CO., LTD                       2020:1
  RULON HARPER CONSTRUCTION INC.            2020:1
  SHIPEX INC.                               2020:1
  SIERRA FOREST PRODUCTS, INC               2020:1
  SIZZLING PLATTER, LLC                     2020:1
  TRES ENTERPRISES, INC.                    2020:1
  UTAH NAVAJO HEALTH SYSTEM, INC.           2020:1
  WAVETRNOIX LLC                            2020:1

LENDER by DATEAPPROVED
  Altabank                                  2020:50
  America First FCU                         2020:28
  Bank of America, National Association     2020:27
  Bank of Utah                              2020:75
  Cache Valley Bank                         2020:190
  Celtic Bank Corporation                   2020:24
  Central Bank                              2020:38
  Continental Bank                          2020:49
  Cross River Bank                          2020:27
  First Utah Bank                           2020:39
  Glacier Bank                              2020:26
  Goldenwest FCU                            2020:37
  JPMorgan Chase Bank, National Associatio  2020:131
  KeyBank National Association              2020:199
  Mountain America FCU                      2020:65
  Readycap Lending, LLC                     2020:38
  State Bank of Southern Utah               2020:28
  U.S. Bank, National Association           2020:24
  Wells Fargo Bank, National Association    2020:28
  Zions Bank, A Division of                 2020:515

## what

LOANRANGE: d $350,000-1 million 59%, c $1-2 million 27%, b $2-5 million 12%, a $5-10 million 2%

BUSINESSTYPE: Corporation 42%, Limited  Liability Company(LLC 33%, Subchapter S Corporation 20%, Non-Profit Organization 3%, Sole Proprietorship 2%, Partnership 1%, nan 0%, Limited Liability Partnership 0%, Professional Association 0%, Independent Contractors 0%

RACEETHNICITY: Unanswered 81%, White 18%, Hispanic 1%, Asian 0%, Black or African American 0%, American Indian or Alaska Nati 0%

GENDER: Unanswered 64%, Male Owned 33%, Female Owned 3%

VETERAN: Unanswered 71%, Non-Veteran 28%, Veteran 1%

CD: UT - 02 40%, UT - 03 30%, UT - 01 19%, UT - 04 11%

NONPROFIT: True 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOANRANGE | category | 4 | 0 | d $350,000-1 million 1.2K; c $1-2 million 547; b $2-5 million 240; a $5-10 million 41 |
| BUSINESSNAME | who | 2.0K | 0 | RICHARDS BRANDT MILLER NE 10; BTJD 10; PEARSON & BUTLER, PLLC 10; KIPP AND CHRISTIAN, P.C. 10 |
| NAICS_DESCRIPTION | who | 234 | 0 | Building Equipment Contra 125; Vehicle Dealers 118; Merchant Wholesalers 107; Structural Contractors 73 |
| ADDRESS | id | 1.9K | 0 | LEGEND HILLS DR 13; 10355 South Jordan Gatewa 11; 1411 W 1250 S #300 11; 5745 W 300 S 11 |
| CITY | who | 138 | 0 | SALT LAKE CITY 577; OGDEN 103; SANDY 69; DRAPER 68 |
| STATE | other | 1 | 0 | UT 2.0K |
| ZIP | other | 155 | 0 | 84104 121; 84115 93; 84107 90; 84119 77 |
| NAICSCODE | who | 490 | 0 | 441110 81; 238220 70; 236220 51; 238210 50 |
| BUSINESSTYPE | category | 10 | 0 | Corporation 834; Limited  Liability Compan 655; Subchapter S Corporation 397; Non-Profit Organization 54 |
| RACEETHNICITY | category | 6 | 0 | Unanswered 1.6K; White 357; Hispanic 17; Asian 7 |
| GENDER | category | 3 | 0 | Unanswered 1.3K; Male Owned 654; Female Owned 59 |
| VETERAN | category | 3 | 0 | Unanswered 1.4K; Non-Veteran 555; Veteran 28 |
| JOBSRETAINED | other | 330 | 0 | 500 57; nan 44; 32 34; 40 34 |
| DATEAPPROVED | date | 49 | 0 | 2020-04-13T00:00:00.000 236; 2020-04-15T00:00:00.000 225; 2020-04-14T00:00:00.000 153; 2020-04-27T00:00:00.000 145 |
| LENDER | who | 136 | 0 | Zions Bank, A Division of 515; KeyBank National Associat 199; Cache Valley Bank 190; JPMorgan Chase Bank, Nati 131 |
| CD | category | 4 | 0 | UT - 02 790; UT - 03 601; UT - 01 382; UT - 04 227 |
| NONPROFIT | category | 2 | 1.9K | True 54 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:47:34.36206 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | f53c0703-7aaf-4f12-969f-a 2.0K |
| SRC_SHA256 | who | 1 | 0 | 0eccdfdf65dbd20b2e236dffe 2.0K |
