# PORTAL_CKA_OKLAHOMA_OPEN_DA_B65187987B

rows 10.0K  columns 16  scan 6.3s

roles: amount 1, audit 2, category 3, date 3, id 1, other 2, who 5

## when

TRANSACTION_DATE
  2015     10.0K  ##############################

POST_DATE
  2015     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -7.1K | 104 | 3.2K | 128.7K | 3.29M |

## who

LAST_NAME by rows
       396  Tornakian
       141  Connelly
       100  Jones
        96  Melone
        95  Turner
        86  Clark
        82  Bowers
        70  Brown
        65  Broderius
        58  Williams
        56  Dickenson
        51  Bailey
        51  Sundstrom
        50  Ferri
        50  Liang
        50  Thompson
        49  Yarbrough-Tessman
        49  Custar
        48  Wood
        45  HUBBARD

LAST_NAME by dollars
      135.0K        3 rows  Ropers
      116.7K      396 rows  Tornakian
       85.4K       17 rows  Edwards
       47.6K       86 rows  Clark
       43.9K       33 rows  PARRIS
       38.8K      141 rows  Connelly
       38.0K       15 rows  Baustert
       37.5K       10 rows  Finley
       33.8K       95 rows  Turner
       32.1K       51 rows  Bailey
       31.6K       32 rows  Kindred
       29.7K       49 rows  Yarbrough-Tessman
       27.6K       96 rows  Melone
       27.6K       24 rows  Marshall
       26.5K       26 rows  Berry
       23.0K       32 rows  Fitzpatrick
       21.4K       42 rows  Ries
       20.3K       27 rows  Newsom
       19.4K       21 rows  Bender
       18.3K       50 rows  Liang

MERCHANT by rows
       353  AMAZON MKTPLACE PMTS
       302  LOWES #00241
       181  Amazon.com
       166  STAPLES       00105288
       141  VWR INTERNATIONAL INC
       136  WW GRAINGER
       110  AIRGAS CENTRAL
       106  WAL-MART #0137
        90  STILLWATER MILLING COMP
        84  WAL-MART #4241
        83  WM SUPERCENTER #137
        83  TFS FISHERSCI ECOM HUS
        80  SIGMA ALDRICH US
        79  WM SUPERCENTER #4241
        75  NAPA AUTO PARTS
        60  DEARINGER PRINTING & TROP
        57  QUALITY WATER SERVICES
        55  STAPLES DIRECT
        54  B&C BUSINESS PRODUCTS
        53  OFFICE DEPOT #1079

MERCHANT by dollars
      128.7K        1 rows  STILLWATER UTILITIES
       84.1K        9 rows  SIMPLEXGRINNELL
       73.2K      136 rows  WW GRAINGER
       48.8K       12 rows  GALT FOUNDATION
       40.9K      353 rows  AMAZON MKTPLACE PMTS
       29.2K      141 rows  VWR INTERNATIONAL INC
       28.9K       83 rows  TFS FISHERSCI ECOM HUS
       26.3K      181 rows  Amazon.com
       25.0K      302 rows  LOWES #00241
       22.3K       39 rows  ALLEGRA PRINT AND IMAGING
       22.0K       80 rows  SIGMA ALDRICH US
       21.7K      166 rows  STAPLES       00105288
       21.3K       90 rows  STILLWATER MILLING COMP
       20.3K       26 rows  OKC UTILITY SERVICEWEB S
       19.1K       41 rows  P & K EQUIPMENT
       19.1K        7 rows  THOMSON WEST TCD
       18.2K       35 rows  WWW.NEWEGG.COM
       17.8K       31 rows  STILLWATER WINLECTRIC
       14.1K       32 rows  XEROX CORPORATION/RBO
       12.9K       54 rows  B&C BUSINESS PRODUCTS

ITEM_DESCR by rows
      6.5K  GENERAL PURCHASE
       371  ROOM CHARGES
       214  AIR TRAVEL
        52  AT&T SERVICE PAYMENT ITM
        32  PRODUCT EACH
        30  PRODUCTS AND SERVICES EA
        28  PARTS SET
        23  25 nmole DNA Oligo 1|25 nmole DNA Oligo 1|25 nmole
        21  SHIPPING CHARGES
        17  001 Priority          1LB PCE
        14  Merchandise General EA
        13  DESCRIPTION EACH
        10  CAR RENTAL
        10  INVOICE CHARGES ST
         9  DESCRIPTION SET
         8  Electrical Parts EA
         8  NEWS ADV./SUBSC. EACH
         8  237817 Service Unit
         8  Subscriptions PCE
         8  PARTS EACH

ITEM_DESCR by dollars
       2.34M     6.5K rows  GENERAL PURCHASE
      117.2K      371 rows  ROOM CHARGES
       66.9K      214 rows  AIR TRAVEL
       26.7K        4 rows  Bottle Filling StationSi EA
       11.6K       30 rows  PRODUCTS AND SERVICES EA
       11.3K       14 rows  Merchandise General EA
       10.9K       32 rows  PRODUCT EACH
        9.9K       13 rows  DESCRIPTION EACH
        9.2K        1 rows  SurfacePro312In8Gb256GbI7 EA
        8.9K       28 rows  PARTS SET
        6.4K        1 rows  701874497 PCS
        5.5K        4 rows  UNISOURCE ITEM EA|UNISOURCE ITEM EA|UNISOURCE ITEM
        5.0K        1 rows  DT ASUS D510MT-I74790080F PCS|SSD 120G   CORSAIR C
        4.9K        1 rows  ACCESSORIES U
        4.9K        2 rows  MS SURFACE PRO 3 I5 256G PCB|MS SURFACE PRO 3 COVE
        4.8K        1 rows  181148 EA
        4.7K        1 rows  HVAC Services EA
        4.3K        1 rows  Newspaper Advertising eac
        4.3K        1 rows  JET 414483 VBS-1408 14-Inc PCE
        4.3K        1 rows  FLUKE 1310/1150 SF PRO K PCB

MCC_DESCRIPTION by rows
       630  GROCERY STORES  SUPERMARKETS
       573  BOOK STORES
       563  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
       455  MISCELLANEOUS AND RETAIL STORES
       411  HOME SUPPLY WAREHOUSE STORES
       391  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
       278  STATIONERY OFFICE SUPPLIES PRINTING AND
       277  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       237  STATIONARY  OFFICE AND SCHOOL SUPPLY STO
       225  HARDWARE STORES
       220  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLAS
       208  AUTOMOTIVE PARTS  ACCESSORIES STORES
       195  CHEMICALS AND ALLIED PRODUCTS NOT ESLEWH
       180  PLUMBING & HEATING EQUIPMENT AND SUPPLIE
       170  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
       167  ALL OTHER DIRECT MARKETERS
       162  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
       159  ELECTRICAL PARTS AND EQUIPMENT
       149  ELECTRONIC SALES
       126  CATALOG MERCHANTS

MCC_DESCRIPTION by dollars
      209.0K      563 rows  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
      162.8K       94 rows  UTILITIES-ELEC/GAS/HEAT OIL/SANITARY/WTR
      153.1K      391 rows  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
      110.2K      277 rows  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
      106.2K      455 rows  MISCELLANEOUS AND RETAIL STORES
      102.3K      220 rows  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLAS
       86.9K      573 rows  BOOK STORES
       84.4K       18 rows  DETECTIVE AGENCIES & PROTECTIVE AGENCY A
       79.1K      167 rows  ALL OTHER DIRECT MARKETERS
       75.7K      102 rows  PROFESSIONAL SERVICES NOT ELSEWHERE CLAS
       66.2K      278 rows  STATIONERY OFFICE SUPPLIES PRINTING AND
       64.1K      103 rows  CHARITABLE AND SOCIAL SERVICE ORGANIZATI
       63.7K      149 rows  ELECTRONIC SALES
       57.4K      126 rows  CATALOG MERCHANTS
       55.0K       99 rows  SCHOOLS AND EDUCATIONAL SERVICES NOT ELS
       53.0K      159 rows  ELECTRICAL PARTS AND EQUIPMENT
       52.3K      195 rows  CHEMICALS AND ALLIED PRODUCTS NOT ESLEWH
       51.6K      180 rows  PLUMBING & HEATING EQUIPMENT AND SUPPLIE
       49.2K       14 rows  EMPLOYMENT AGENCIES  TEMPORARY HELP SUPP
       48.4K       64 rows  MISCELLANEOUS PUBLISHING & PRINTING

## who x when

LAST_NAME by TRANSACTION_DATE, dollars = AMOUNT
  Bailey                                    2015:32.1K
  Baustert                                  2015:38.0K
  Berry                                     2015:26.5K
  Bowers                                    2015:16.2K
  Broderius                                 2015:12.3K
  Brown                                     2015:12.2K
  Clark                                     2015:47.6K
  Connelly                                  2015:38.8K
  Custar                                    2015:15.8K
  Dickenson                                 2015:16.8K
  Edwards                                   2015:85.4K
  Ferri                                     2015:8.2K
  Finley                                    2015:37.5K
  Fitzpatrick                               2015:23.0K
  HUBBARD                                   2015:13.3K
  Jones                                     2015:15.7K
  Kindred                                   2015:31.6K
  Liang                                     2015:18.3K
  Marshall                                  2015:27.6K
  Melone                                    2015:27.6K
  PARRIS                                    2015:43.9K
  Ries                                      2015:21.4K
  Ropers                                    2015:135.0K
  Sundstrom                                 2015:9.2K
  Thompson                                  2015:13.2K
  Tornakian                                 2015:116.7K
  Turner                                    2015:33.8K
  Williams                                  2015:14.6K
  Wood                                      2015:12.0K
  Yarbrough-Tessman                         2015:29.7K

MERCHANT by TRANSACTION_DATE, dollars = AMOUNT
  AIRGAS CENTRAL                            2015:8.9K
  ALLEGRA PRINT AND IMAGING                 2015:22.3K
  AMAZON MKTPLACE PMTS                      2015:40.9K
  Amazon.com                                2015:26.3K
  B&C BUSINESS PRODUCTS                     2015:12.9K
  DEARINGER PRINTING & TROP                 2015:7.5K
  GALT FOUNDATION                           2015:48.8K
  LOWES #00241                              2015:25.0K
  NAPA AUTO PARTS                           2015:7.0K
  OFFICE DEPOT #1079                        2015:6.1K
  OKC UTILITY SERVICEWEB S                  2015:20.3K
  P & K EQUIPMENT                           2015:19.1K
  QUALITY WATER SERVICES                    2015:3.1K
  SIGMA ALDRICH US                          2015:22.0K
  SIMPLEXGRINNELL                           2015:84.1K
  STAPLES       00105288                    2015:21.7K
  STAPLES DIRECT                            2015:7.5K
  STILLWATER MILLING COMP                   2015:21.3K
  STILLWATER UTILITIES                      2015:128.7K
  STILLWATER WINLECTRIC                     2015:17.8K
  TFS FISHERSCI ECOM HUS                    2015:28.9K
  THOMSON WEST TCD                          2015:19.1K
  VWR INTERNATIONAL INC                     2015:29.2K
  WAL-MART #0137                            2015:5.8K
  WAL-MART #4241                            2015:4.7K
  WM SUPERCENTER #137                       2015:6.4K
  WM SUPERCENTER #4241                      2015:5.7K
  WW GRAINGER                               2015:73.2K
  WWW.NEWEGG.COM                            2015:18.2K
  XEROX CORPORATION/RBO                     2015:14.1K

## what

AGENCYNBR:  01000 88%,  04000 4%,  02500 4%,  04900 1%,  09000 1%,  04700 1%,  06500 0%,  03000 0%,  05500 0%,  06000 0%,  03900 0%,  02000 0%

AGENCYNAME: OKLAHOMA STATE UNIVERSITY 88%, DEPT OF AGRICULTURE FOOD & FOR 4%, OKLAHOMA MILITARY DEPARTMENT 4%, ATTORNEY GENERAL 1%, OFFICE OF MANAGEMENT AND ENTER 1%, INDIGENT DEFENSE SYSTEM 1%, STATE BANKING DEPARTMENT 0%, ALCOHOLIC BEV. LAWS ENFORCE. 0%, STATE ARTS COUNCIL 0%, OK DEP AEROSPACE & AERONAUTICS 0%, BOLL WEEVIL ERADICATION ORG. 0%, OKLAHOMA ACCOUNTANCY BOARD 0%

FIRST_INITIAL: J 14%, M 14%, D 11%, K 10%, S 9%, R 9%, C 7%, A 7%, L 6%, T 5%, B 5%, P 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CALENDAR_YEAR | other | 1 | 0 | 2015 10.0K |
| CALENDAR_MONTH | other | 1 | 0 | 07 10.0K |
| AGENCYNBR | category | 13 | 0 |  01000 8.8K;  04000 369;  02500 355;  04900 128 |
| AGENCYNAME | category | 13 | 0 | OKLAHOMA STATE UNIVERSITY 8.8K; DEPT OF AGRICULTURE FOOD  369; OKLAHOMA MILITARY DEPARTM 355; ATTORNEY GENERAL 128 |
| LAST_NAME | who | 1.2K | 0 | Tornakian 396; Connelly 141; Jones 101; Melone 96 |
| FIRST_INITIAL | category | 26 | 0 | J 1.3K; M 1.3K; D 976; K 854 |
| ITEM_DESCR | who | 2.4K | 8 | GENERAL PURCHASE 6.5K; ROOM CHARGES 371; AIR TRAVEL 214; AT&T SERVICE PAYMENT ITM 52 |
| AMOUNT | amount | 7.0K | 0 | 50.0000000000000000000000 81; 83.0000000000000000000000 63; 12.0000000000000000000000 62; 25.0000000000000000000000 60 |
| MERCHANT | who | 3.4K | 0 | AMAZON MKTPLACE PMTS 353; LOWES #00241 302; Amazon.com 181; STAPLES       00105288 166 |
| TRANSACTION_DATE | date | 44 | 0 | 15-Jul-15 519; 01-Jul-15 517; 21-Jul-15 485; 22-Jul-15 482 |
| POST_DATE | date | 23 | 0 | 13-Jul-15 681; 27-Jul-15 620; 20-Jul-15 553; 16-Jul-15 542 |
| MCC_DESCRIPTION | who | 236 | 0 | GROCERY STORES  SUPERMARK 630; BOOK STORES 573; LAB/MEDICAL/DENTAL/OPHTHA 563; MISCELLANEOUS AND RETAIL  455 |
| ROWID | id | 9.8K | 0 | AAAJGhAANAAONeMAAA 50; AAAJGhAANAAONeZAAB 50; AAAJGhAANAAONeZAAA 50; AAAJGhAANAAONfxAAV 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:47:32.78923 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 28791c6d-6683-4cf7-9709-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | 932bf4edf9546c260fd415be0 10.0K |
