# PORTAL_CKA_ANALYZE_BOSTON_B4C5E99B0A

rows 10.0K  columns 70  scan 6.7s

roles: amount 6, audit 2, category 37, date 1, id 1, other 17, state 1, who 6

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RES_FLOOR | 8.2K | 1 | 2 | 4 | 7 | 16.2K |
| LAND_VALUE | 10.0K | 0 | 40.7K | 1.70M | 486.05M | 2.69B |
| BLDG_VALUE | 10.0K | 0 | 528.4K | 2.25M | 103.46M | 6.43B |
| SFYI_VALUE | 10.0K | 0 | 0 | 46.4K | 32.66M | 101.98M |
| TOTAL_VALUE | 10.0K | 0 | 631.0K | 4.73M | 585.00M | 9.22B |
| GROSS_TAX | 8.9K | 4.96 | 8.4K | 45.4K | 1.93M | 102.98M |

## who

ST_NAME by rows
       536  Sumner ST
       482  Saratoga ST
       425  Maverick ST
       421  Bennington ST
       392  Meridian ST
       353  LEWIS ST
       335  Chelsea ST
       333  Lexington ST
       319  Webster ST
       260  Cottage ST
       254  Everett ST
       241  PORTER ST
       227  Border ST
       216  PRINCETON ST
       213  Trenton ST
       209  FALCON ST
       207  Bremen ST
       186  Havre ST
       167  Leyden ST
       162  Paris ST

ST_NAME by dollars
     596.89M      425 rows  Maverick ST
     221.45M      421 rows  Bennington ST
     117.92M      482 rows  Saratoga ST
     101.84M      227 rows  Border ST
      92.01M       38 rows  WM F MCCLELLAN HW
      82.99M      117 rows  Marginal ST
      69.87M       93 rows  WALDEMAR AV
      61.02M      335 rows  Chelsea ST
      60.56M       66 rows  BARNES AV
      60.15M      207 rows  Bremen ST
      52.28M      260 rows  Cottage ST
      51.51M      536 rows  Sumner ST
      42.77M      333 rows  Lexington ST
      42.20M      319 rows  Webster ST
      38.76M      392 rows  Meridian ST
      34.47M      216 rows  PRINCETON ST
      33.29M      254 rows  Everett ST
      32.66M      213 rows  Trenton ST
      31.84M      162 rows  Paris ST
      31.74M      209 rows  FALCON ST

OWNER by rows
       102  CITY OF BOSTON
        77  MASSACHUSETTS PORT AUTHORITY
        34  EBNT HOLDINGS LLC
        26  MASSACHUSETTS  PORT AUTHORITY
        20  28-30 GENEVA STREET CONDOMINIUM TRUST
        20  SONS OF DIVINE PROVIDENCE INC
        16  SOLSKINN PROPERTIES LLC
        13  PACO PROPERTIES LLC
        13  EAST BOSTON AOP LLC
        11  MASS BAY TRANSP AUTH
        11  GLADSTONE STREET LLC
        11  LANDFALL COMMUNITY ASSOCIATES II LLC
        10  MAVERICK SQUARE PROPERTIES LLC
         9  EBCDC INC
         9  EB1 PROPERTY GROUP 1 LLC
         9  EB2 PROPERTY GROUP 1 LLC
         9  INTERIANO ELIAS
         9  SHALOM PROPERTIES INC
         8  MNA REAL ESTATE HOLDING LLC
         8  MASS TURNPIKE AUTHORITY

OWNER by dollars
     580.19M       77 rows  MASSACHUSETTS PORT AUTHORITY
     160.78M      102 rows  CITY OF BOSTON
     128.62M        2 rows  METROPOLITAN DIST COMMISSION
      75.02M        2 rows  COMMONWLTH OF MASS
      58.48M        5 rows  COMMONWEALTH OF MASS
      53.61M        1 rows  MCCLELLAN HIGHWAY DEVELOPMENT COMPANY LLC
      23.53M        4 rows  EDDY OWNER LLC
      23.25M        2 rows  COMMONWEALTH OF MASS DEPARTMENT OF HIGHWAYS
      21.46M        2 rows  CLIPPERSHIP WHARF MULTIFAMILY LLC
      19.85M        1 rows  BOSTON EAST OWNER LLC
      19.17M        1 rows  BRANDYWYNE VILLAGE CO
      18.49M        3 rows  SLUMBER TIME LLC
      18.31M        1 rows  EBSP ASSOCIATES LLC MASS LLC
      16.69M        1 rows  YEBBA BROTHERS LLC
      16.16M        2 rows  305-365 MCC HIGHWAY LLC
      15.81M        8 rows  SUNOCO PARTNERS MARKETING & TERMINALS LP
      12.90M        1 rows  144 ADDISON STREET LLC
      12.56M        3 rows  HERITAGE HOUSING CORP
      10.18M        1 rows  MASSACHUSETTS BAY TRANSIT AUTHORITY
       9.69M       26 rows  MASSACHUSETTS  PORT AUTHORITY

BLDG_TYPE by rows
      1.5K  DK - Decker
      1.2K  LR - Low Rise
       914  FS - Free Standing
       752  SD - Semi-Det
       732  MR - Mid Rise
       673  CV - Conventional
       663  RM - Row Middle
       535  RE - Row End
       462  TF - Two Fam Stack
       407  99 - Vacant
       359  CL - Colonial
       290  NoBld
       269  111 - APT 4-6 UNITS
       146  TH - Town House
       105  026 - RC: TWO RES UNITS
        92  CP - Cape
        80  HR - High Rise
        69  112 - APT 7-30 UNITS
        69  DX - Duplex
        45  RN - Ranch

BLDG_TYPE by dollars
     492.65M       40 rows  027 - RC: THREE RES UNITS
     428.35M      290 rows  NoBld
     230.22M     1.5K rows  DK - Decker
     182.16M      673 rows  CV - Conventional
     123.75M      462 rows  TF - Two Fam Stack
     121.71M      752 rows  SD - Semi-Det
      96.18M       13 rows  976 - SCHOOL
      84.10M        8 rows  114 - APT 100+ UNITS
      82.72M      359 rows  CL - Colonial
      70.28M      663 rows  RM - Row Middle
      65.72M      269 rows  111 - APT 4-6 UNITS
      58.73M       25 rows  125 - SUBSD HOUSING S- 8
      53.61M        1 rows  366 - FIELDHOUSE/TRACK
      50.07M        4 rows  120 - LUXURY APARTMENT
      50.02M      407 rows  99 - Vacant
      45.37M      535 rows  RE - Row End
      45.08M        4 rows  300 - HOTEL
      33.01M       69 rows  112 - APT 7-30 UNITS
      30.88M       12 rows  316 - WAREHOUSE /Distrib
      20.94M       92 rows  CP - Cape

LU_DESC by rows
      3.7K  RESIDENTIAL CONDO
      1.6K  THREE-FAM DWELLING
      1.0K  TWO-FAM DWELLING
       839  SINGLE FAM DWELLING
       650  CONDO MAIN
       349  CONDO PARKING (RES)
       225  APT 4-6 UNITS
       219  OTHER EXEMPT BLDG
       207  RES /COMMERCIAL USE
       172  RES LAND (Unusable)
       101  RESIDENTIAL LAND
        77  SUBSD HOUSING S- 8
        64  COMM MULTI-USE
        61  RES ANCILL IMPROVEMT
        60  APT 7-30 UNITS
        47  OTHER PUBLIC LAND
        40  RET/WHSL/SERVICE
        38  REPAIR GARAGE
        37  PARKING LOT
        33  CITY OF BOSTON

LU_DESC by dollars
     887.42M      219 rows  OTHER EXEMPT BLDG
     436.00M     1.6K rows  THREE-FAM DWELLING
     275.68M     1.0K rows  TWO-FAM DWELLING
     186.72M      839 rows  SINGLE FAM DWELLING
      93.77M       15 rows  SCHOOL
      72.62M       47 rows  OTHER PUBLIC LAND
      72.20M      207 rows  RES /COMMERCIAL USE
      59.02M       16 rows  LUXURY APARTMENT
      57.34M       13 rows  COM BILLBOARD
      54.81M      225 rows  APT 4-6 UNITS
      53.33M       77 rows  SUBSD HOUSING S- 8
      48.67M       17 rows  Commonwealth of Mass
      45.08M        4 rows  HOTEL
      41.98M       18 rows  WAREHOUSE /DISTRIB
      25.49M       60 rows  APT 7-30 UNITS
      24.33M       29 rows  COMMERCIAL LAND
      19.00M       20 rows  EXEMPT 121A PROP
      14.59M        6 rows  PAY PARKING LOT
      14.03M      101 rows  RESIDENTIAL LAND
      12.85M       64 rows  COMM MULTI-USE

## who x when

ST_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LAND_VALUE
  BARNES AV                                 2026:60.56M
  Bennington ST                             2026:221.45M
  Border ST                                 2026:101.84M
  Bremen ST                                 2026:60.15M
  Chelsea ST                                2026:61.02M
  Cottage ST                                2026:52.28M
  Everett ST                                2026:33.29M
  FALCON ST                                 2026:31.74M
  Havre ST                                  2026:26.60M
  LEWIS ST                                  2026:22.10M
  Lexington ST                              2026:42.77M
  Leyden ST                                 2026:23.97M
  Marginal ST                               2026:82.99M
  Maverick ST                               2026:596.89M
  Meridian ST                               2026:38.76M
  PORTER ST                                 2026:13.08M
  PRINCETON ST                              2026:34.47M
  Paris ST                                  2026:31.84M
  Saratoga ST                               2026:117.92M
  Sumner ST                                 2026:51.51M
  Trenton ST                                2026:32.66M
  WALDEMAR AV                               2026:69.87M
  WM F MCCLELLAN HW                         2026:92.01M
  Webster ST                                2026:42.20M

OWNER by INGESTED_AT  LOAD STAMP, not an event date, dollars = LAND_VALUE
  28-30 GENEVA STREET CONDOMINIUM TRUST     2026:0
  BOSTON EAST OWNER LLC                     2026:19.85M
  BRANDYWYNE VILLAGE CO                     2026:19.17M
  CITY OF BOSTON                            2026:160.78M
  CLIPPERSHIP WHARF MULTIFAMILY LLC         2026:21.46M
  COMMONWEALTH OF MASS                      2026:58.48M
  COMMONWEALTH OF MASS DEPARTMENT OF HIGHW  2026:23.25M
  COMMONWLTH OF MASS                        2026:75.02M
  EAST BOSTON AOP LLC                       2026:2.37M
  EB1 PROPERTY GROUP 1 LLC                  2026:2.05M
  EB2 PROPERTY GROUP 1 LLC                  2026:1.93M
  EBCDC INC                                 2026:2.41M
  EBNT HOLDINGS LLC                         2026:4.33M
  EDDY OWNER LLC                            2026:23.53M
  GLADSTONE STREET LLC                      2026:1.60M
  INTERIANO ELIAS                           2026:1.61M
  LANDFALL COMMUNITY ASSOCIATES II LLC      2026:4.52M
  MASS BAY TRANSP AUTH                      2026:6.97M
  MASS TURNPIKE AUTHORITY                   2026:4.85M
  MASSACHUSETTS  PORT AUTHORITY             2026:9.69M
  MASSACHUSETTS PORT AUTHORITY              2026:580.19M
  MAVERICK SQUARE PROPERTIES LLC            2026:1.83M
  MCCLELLAN HIGHWAY DEVELOPMENT COMPANY LL  2026:53.61M
  METROPOLITAN DIST COMMISSION              2026:128.62M
  MNA REAL ESTATE HOLDING LLC               2026:662.5K
  PACO PROPERTIES LLC                       2026:1.10M
  SHALOM PROPERTIES INC                     2026:1.03M
  SLUMBER TIME LLC                          2026:18.49M
  SOLSKINN PROPERTIES LLC                   2026:4.33M
  SONS OF DIVINE PROVIDENCE INC             2026:7.25M

## where

MAIL_STATE: MA 9.7K, NY 58, FL 34, NH 31, CA 29, TX 23, RI 17, CT 10, ME 9, VA 8, IL 8

## what

CITY: EAST BOSTON 100%, BOSTON 0%

ZIP_CODE: 02128 100%, 02115 0%

LU: CD 37%, R3 17%, R2 11%, R1 9%, CM 7%, E 4%, CP 4%, RL - RL 3%, C 3%, RC 3%, R4 2%, A 2%

OWN_OCC: N 59%, Y 41%

CD_FLOOR: 2 29%, 3 25%, 1 21%, 4 10%, 0 8%, 5 3%, 6 2%, 7 0%, 03 0%, 01 0%

RES_UNITS: 3 46%, 2 18%, 4 15%, 6 6%, 9 5%, 8 3%, 5 3%, 7 2%, 0 1%, 14 1%, 12 1%

COM_UNITS: 0 96%, 1 2%, 2 1%, 3 0%

RC_UNITS: 0 100%

STRUCTURE_CLASS: C - Brick/Concr 53%, D - Wood/Frame 38%, B - Reinf Concr 8%, A - Struct Steel 0%, E - Metal 0%

ROOF_STRUCTURE: F - Flat 71%, G - Gable 18%, M - Mansard 5%, H - Hip 4%, L - Gambrel 0%, S - Shed 0%, O - Other 0%

ROOF_COVER: R - Rubber Roof 56%, A - Asphalt Shingl 26%, C - Composition 16%, S - Slate 1%, O - Other 0%, W - Wood Shingle 0%

INT_WALL: N - Normal 100%, E - Elaborate 0%, S - Substandard 0%

EXT_FNISHED: M - Vinyl 35%, B - Brick/Stone 19%, C - Cement Board 17%, V - Brck/Stn Venr 6%, F - Frame/Clapbrd 6%, 01 - Brick 4%, W - Wood Shake 4%, A - Asbestos 3%, 09 - Wood Siding 2%, 10 - Alum/Vinyl 2%, P - Asphalt 2%

INT_COND: A - Average 42%, G - Good 34%, E - Excellent 23%, F - Fair 1%, P - Poor 0%

EXT_COND: A - Average 50%, G - Good 28%, E - Excellent 19%, F - Fair 2%, P - Poor 0%

OVERALL_COND: A - Average 69%, G - Good 27%, VG - Very Good 1%, E - Excellent 1%, F - Fair 1%, EX - Excellent 0%, P - Poor 0%, US - Unsound 0%

BED_RMS: 2 32%, 3 17%, 1 13%, 6 10%, 4 10%, 5 8%, 8 4%, 9 3%, 7 2%, 0 1%, 11 1%

FULL_BTH: 2 29%, 1 28%, 0 21%, 3 20%, 4 2%, 6 0%, 5 0%, 7 0%, 9 0%, 8 0%, 15 0%

HLF_BTH: 0 88%, 1 11%, 2 0%, 3 0%, 4 0%

KITCHENS: 1 49%, 0 21%, 3 19%, 2 12%, 4 0%

TT_RMS: 4 26%, 5 16%, 3 10%, 6 10%, 14 7%, 11 6%, 12 6%, 9 5%, 15 5%, 7 5%, 10 5%

BDRM_COND: A - Average 95%, G - Good 4%, F - Fair 0%, P - Poor 0%

BTHRM_STYLE1: M - Modern 61%, S - Semi-Modern 34%, N - No Remodeling 4%, L - Luxury 1%

BTHRM_STYLE2: M - Modern 55%, S - Semi-Modern 39%, N - No Remodeling 5%, L - Luxury 0%

BTHRM_STYLE3: S - Semi-Modern 49%, M - Modern 43%, N - No Remodeling 7%, L - Luxury 0%

KITCHEN_TYPE: O - One Person 36%, 3F - 3 Full Eat In Kitchens 22%, 2F - 2 Full Eat In Kitchens 15%, F - Full Eat In 13%, 1F - 1 Full Eat In Kitchens 11%, 0F - 0 Full Eat In Kitchens 1%, P - Pullman 1%, 4F - 4 Full Eat In Kitchens 0%, N - None 0%

KITCHEN_STYLE1: M - Modern 62%, S - Semi-Modern 33%, N - No Remodeling 5%, L - Luxury 1%

KITCHEN_STYLE2: S - Semi-Modern 58%, M - Modern 33%, N - No Remodeling 9%, L - Luxury 0%

KITCHEN_STYLE3: S - Semi-Modern 57%, M - Modern 34%, N - No Remodeling 9%, L - Luxury 0%

HEAT_TYPE: F - Forced Hot Air 49%, W - Ht Water/Steam 42%, E - Electric 6%, S - Space Heat 3%, P - Heat Pump 1%, N - None 0%, O - Other 0%

HEAT_SYSTEM: I - Indiv. Cntrl 65%, Y - Self Contained 33%, N - None 1%, C - Common 1%

AC_TYPE: N - None 51%, C - Central AC 47%, D - Ductless AC 2%

FIREPLACES: 0 94%, 1 5%, 2 1%, 3 0%, 4 0%, 5 0%

ORIENTATION: T - Through 56%, F - Front/Street 24%, A - Rear Above 11%, B - Rear Below 5%, M - Middle 2%, C - Courtyard 1%, E - End 1%

NUM_PARKING: 0 65%, 1 20%, 2 8%, 3 3%, 4 2%, 6 1%, 5 1%, 125 0%, 7 0%, 8 0%, 9 0%

PROP_VIEW: A - Average 81%, G - Good 9%, F - Fair 5%, E - Excellent 3%, P - Poor 1%, S - Special 0%

CORNER_UNIT: N - No 84%, Y - Yes 16%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PID | id | 10.1K | 0 | 0106505000 50; 0106503000 50; 0106502000 50; 0106501000 50 |
| CM_ID | other | 653 | 5.3K | 0105400040 243; 0104164010 222; 0105403000 201; 0105400400 127 |
| GIS_ID | other | 5.8K | 0 | 0105400020 386; 0104164010 242; 0105403000 224; 0103662000 138 |
| ST_NUM | other | 896 | 547 | 65 293; 156 263; 99 227; 45 150 |
| ST_ALPHA | other | 165 | 9.8K | A 30; R 26; B 7; HF 3 |
| ST_NUM2 | other | 343 | 8.8K | 207 88; 19 41; 30 24; 105 23 |
| ST_NAME | who | 173 | 0 | Sumner ST 536; Saratoga ST 482; Maverick ST 425; Bennington ST 421 |
| UNIT_NUM | other | 930 | 5.9K | 2 544; 1 543; 3 443; 4 161 |
| CITY | category | 2 | 0 | EAST BOSTON 10.0K; BOSTON 3 |
| ZIP_CODE | category | 3 | 1 | 02128 10.0K; 02115 5 |
| BLDG_SEQ | other | 1 | 0 | 1 10.0K |
| NUM_BLDGS | other | 1 | 0 | 1 10.0K |
| LUC | other | 106 | 0 | 102 3.7K; 105 1.6K; 104 1.0K; 101 839 |
| LU | category | 16 | 0 | CD 3.7K; R3 1.6K; R2 1.0K; R1 839 |
| LU_DESC | who | 104 | 0 | RESIDENTIAL CONDO 3.7K; THREE-FAM DWELLING 1.6K; TWO-FAM DWELLING 1.0K; SINGLE FAM DWELLING 839 |
| BLDG_TYPE | who | 109 | 121 | DK - Decker 1.5K; LR - Low Rise 1.2K; FS - Free Standing 914; SD - Semi-Det 752 |
| OWN_OCC | category | 2 | 0 | N 5.9K; Y 4.1K |
| OWNER | who | 8.3K | 0 | CITY OF BOSTON 104; MASSACHUSETTS PORT AUTHOR 79; LONDON STREET REALTY LLC 53; CARDONAS INC 52 |
| MAIL_ADDRESSEE | other | 1.2K | 8.4K | C/O EBCDC INC 37; C/O RICHARD CRESPO, MANAG 24; C/O SHARON TATRO, KINGSLE 22; C/O N O A H 16 |
| MAIL_STREET_ADDRESS | other | 8.1K | 0 | 1 HARBORSIDE DR #200S 83; 625 MAIN ST 61; 80 BORDER ST 3RD FL 57; 297 HAVRE ST 53 |
| MAIL_CITY | who | 356 | 0 | EAST BOSTON 6.8K; BOSTON 659; E BOSTON 531; REVERE 155 |
| MAIL_STATE | state | 33 | 19 | MA 9.7K; NY 58; FL 34; NH 31 |
| MAIL_ZIP_CODE | other | 405 | 4 | 02128 7.6K; 02151 155; 02110 79; 02152 78 |
| RES_FLOOR | amount | 18 | 1.8K | 1 3.1K; 3.0 1.7K; 2.0 1.3K; 3 684 |
| CD_FLOOR | category | 11 | 6.3K | 2 1.1K; 3 929; 1 785; 4 364 |
| RES_UNITS | category | 37 | 9.3K | 3 285; 2 110; 4 90; 6 36 |
| COM_UNITS | category | 5 | 9.3K | 0 626; 1 14; 2 7; 3 3 |
| RC_UNITS | category | 2 | 9.3K | 0 650 |
| LAND_SF | other | 3.0K | 365 | 2,500 584; 5,000 140; 2,000 108; 4,500 92 |
| GROSS_AREA | other | 3.7K | 1.8K | 747 53; 733 46; 2250 43; 1002 43 |
| LIVING_AREA | other | 3.6K | 1.8K | 747 52; 733 45; 1040 44; 1080 44 |
| LAND_VALUE | amount | 2.9K | 0 | 0 4.7K; 40,700 30; 267,100 29; 176,000 28 |
| BLDG_VALUE | amount | 5.1K | 0 | 0 1.1K; 70,000 244; 200 220; 25,300 60 |
| SFYI_VALUE | amount | 334 | 0 | 0 9.5K; 3,900 7; 2,400 7; 1,800 6 |
| TOTAL_VALUE | amount | 6.0K | 0 | 0 650; 70,000 247; 25,300 63; 67,800 58 |
| GROSS_TAX | amount | 6.3K | 0 |  $-    1.1K;  $868.00  245;  $313.72  61;  $840.72  57 |
| YR_BUILT | other | 166 | 865 | 1900 2.1K; 1910 1.4K; 2020 563; 2017 469 |
| YR_REMODEL | other | 67 | 5.9K | 2019 324; 2017 308; 2004 281; 2022 192 |
| STRUCTURE_CLASS | category | 6 | 8.5K | C - Brick/Concr 790; D - Wood/Frame 563; B - Reinf Concr 121; A - Struct Steel 7 |
| ROOF_STRUCTURE | category | 8 | 1.8K | F - Flat 5.9K; G - Gable 1.5K; M - Mansard 401; H - Hip 353 |
| ROOF_COVER | category | 7 | 1.8K | R - Rubber Roof 4.6K; A - Asphalt Shingl 2.2K; C - Composition 1.3K; S - Slate 113 |
| INT_WALL | category | 3 | 2.7K | N - Normal 7.3K; E - Elaborate 7; S - Substandard 5 |
| EXT_FNISHED | category | 26 | 852 | M - Vinyl 3.1K; B - Brick/Stone 1.7K; C - Cement Board 1.5K; V - Brck/Stn Venr 542 |
| INT_COND | category | 6 | 2.7K | A - Average 3.0K; G - Good 2.5K; E - Excellent 1.7K; F - Fair 71 |
| EXT_COND | category | 6 | 1.8K | A - Average 4.1K; G - Good 2.3K; E - Excellent 1.6K; F - Fair 201 |
| OVERALL_COND | category | 9 | 838 | A - Average 6.3K; G - Good 2.5K; VG - Very Good 137; E - Excellent 130 |
| BED_RMS | category | 17 | 2.7K | 2 2.3K; 3 1.2K; 1 960; 6 734 |
| FULL_BTH | category | 12 | 815 | 2 2.7K; 1 2.5K; 0 1.9K; 3 1.9K |
| HLF_BTH | category | 6 | 816 | 0 8.1K; 1 996; 2 44; 3 16 |
| KITCHENS | category | 6 | 815 | 1 4.5K; 0 1.9K; 3 1.7K; 2 1.1K |
| TT_RMS | category | 21 | 2.7K | 4 1.6K; 5 991; 3 612; 6 586 |
| BDRM_COND | category | 5 | 6.3K | A - Average 3.5K; G - Good 159; F - Fair 9; P - Poor 1 |
| BTHRM_STYLE1 | category | 5 | 2.7K | M - Modern 4.5K; S - Semi-Modern 2.5K; N - No Remodeling 311; L - Luxury 37 |
| BTHRM_STYLE2 | category | 5 | 4.8K | M - Modern 2.9K; S - Semi-Modern 2.1K; N - No Remodeling 269; L - Luxury 10 |
| BTHRM_STYLE3 | category | 5 | 7.5K | S - Semi-Modern 1.2K; M - Modern 1.1K; N - No Remodeling 184; L - Luxury 7 |
| KITCHEN_TYPE | category | 10 | 2.7K | O - One Person 2.6K; 3F - 3 Full Eat In Kitche 1.6K; 2F - 2 Full Eat In Kitche 1.1K; F - Full Eat In 970 |
| KITCHEN_STYLE1 | category | 5 | 2.7K | M - Modern 4.5K; S - Semi-Modern 2.4K; N - No Remodeling 336; L - Luxury 54 |
| KITCHEN_STYLE2 | category | 5 | 7.2K | S - Semi-Modern 1.6K; M - Modern 922; N - No Remodeling 251; L - Luxury 4 |
| KITCHEN_STYLE3 | category | 5 | 8.2K | S - Semi-Modern 1.0K; M - Modern 588; N - No Remodeling 158; L - Luxury 4 |
| HEAT_TYPE | category | 8 | 2.6K | F - Forced Hot Air 3.6K; W - Ht Water/Steam 3.1K; E - Electric 407; S - Space Heat 204 |
| HEAT_SYSTEM | category | 5 | 6.3K | I - Indiv. Cntrl 2.4K; Y - Self Contained 1.2K; N - None 43; C - Common 33 |
| AC_TYPE | category | 4 | 2.6K | N - None 3.7K; C - Central AC 3.5K; D - Ductless AC 146 |
| FIREPLACES | category | 7 | 815 | 0 8.6K; 1 443; 2 96; 3 10 |
| ORIENTATION | category | 8 | 6.3K | T - Through 2.1K; F - Front/Street 869; A - Rear Above 419; B - Rear Below 175 |
| NUM_PARKING | category | 14 | 2.7K | 0 4.8K; 1 1.4K; 2 567; 3 255 |
| PROP_VIEW | category | 7 | 2.4K | A - Average 6.1K; G - Good 691; F - Fair 408; E - Excellent 264 |
| CORNER_UNIT | category | 3 | 6.3K | N - No 3.1K; Y - Yes 595 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:05:07.16785 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | f5a3fe02-decf-48af-bf4e-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | c4f551614b80661d47262f7bf 10.0K |
