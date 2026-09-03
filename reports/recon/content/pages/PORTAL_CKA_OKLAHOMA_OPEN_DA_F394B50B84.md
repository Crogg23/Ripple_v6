# PORTAL_CKA_OKLAHOMA_OPEN_DA_F394B50B84

rows 10.0K  columns 16  scan 4.1s

roles: amount 1, audit 2, category 3, date 3, id 1, other 2, who 5

## when

TRANSACTION_DATE
  2020     10.0K  ##############################

POST_DATE
  2020     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -61.4K | 106.78 | 4.4K | 61.6K | 3.95M |

## who

LAST_NAME by rows
       248  Duckworth
       190  Brown
       115  Wingfield
        86  Johnson
        80  Robinson
        80  Kindschi
        80  Davis
        80  Edwards
        75  Oliver
        72  Moore
        69  BLACK
        66  Schroeder
        63  Tornakian
        58  Boettcher
        57  Jones
        54  Wilson
        53  WILSON
        52  Turner
        50  Anderson
        49  Brinker

LAST_NAME by dollars
       96.1K      190 rows  Brown
       85.9K       16 rows  Berry
       76.5K      115 rows  Wingfield
       69.6K       39 rows  Forbes
       68.4K       41 rows  Bundy
       55.7K      248 rows  Duckworth
       49.9K       17 rows  Guardado
       49.9K       18 rows  HUBBARD
       49.5K       47 rows  DeLeon
       44.9K       41 rows  PARRIS
       43.7K       42 rows  Price
       42.7K       69 rows  BLACK
       41.0K       80 rows  Robinson
       36.7K       80 rows  Davis
       35.8K       44 rows  Akerman
       35.6K       19 rows  Goad
       35.5K       27 rows  Cuenca
       35.0K       16 rows  McAlister
       33.8K       10 rows  STROUD
       33.7K       41 rows  Newsom

MERCHANT by rows
       344  GRAINGER
       268  LOWES #00241
       129  SOUTH CENTRAL INDUSTRIES
       110  STAPLES       00105288
       103  STILLWATER MILLING COMP
        92  STAPLES
        82  WAL-MART #4241
        82  MCKESSON MEDICAL SUPPLY
        77  VETERANS AFFRS DMC
        64  NAPA AUTO PARTS 0000415
        63  TFS FISHERSCI ECOM HUS
        62  ZOOM.US
        62  WAL-MART #0137
        59  WM SUPERCENTER #137
        59  AIRGAS USA, LLC
        55  WM SUPERCENTER #4241
        54  THE JOURNAL RECORD PUBLIS
        54  VWR INTERNATIONAL INC
        53  B & C Business Products
        53  MCMASTER-CARR

MERCHANT by dollars
      257.5K      129 rows  SOUTH CENTRAL INDUSTRIES
      188.5K      344 rows  GRAINGER
       80.5K       22 rows  DMI  DELL K-12/GOVT
       60.8K       20 rows  KIAMICHI OPPORTUNITIES
       54.8K       82 rows  MCKESSON MEDICAL SUPPLY
       47.7K        2 rows  ESRI
       43.3K        1 rows  DEPARTMENT OF MILITARY
       42.0K       14 rows  DCAM CENTRAL PRINTING
       35.5K       28 rows  GALLS
       35.3K       39 rows  LOWES #02540
       29.4K       34 rows  OKC/EZ-PAY
       28.9K       24 rows  AT&T PREMIER EBIL
       27.6K       47 rows  CENTRAL OKLAHOMAWINLSN
       27.0K       92 rows  STAPLES
       25.0K        5 rows  ORACLE USA INC.
       24.3K      268 rows  LOWES #00241
       23.8K        5 rows  THOMSON WEST TCD
       23.5K        2 rows  GSA-WQMD
       21.7K       53 rows  B & C Business Products
       21.5K       13 rows  H-I-S Paint Reno

ITEM_DESCR by rows
      4.8K  GENERAL PURCHASE
       203  ROOM CHARGES
       129  Janitorial Supplies CS
        81  CREDIT_CARD_CHARGE EA
        77  Benefit Overpayment NMB
        63  Miscellaneous EA
        47  Electrical Equipment EA
        46  SPECIALIZED VEHICLES EA
        45  PRODUCT EA
        42  Facebook Ads EAC
        38  PAYMENT ON ACCOUNT EA
        36  Utility Bill EA
        25  Grimsleys Inc EACH
        25  INVOICE EA
        24  25 nmole DNA Oligo 1|25 nmole DNA Oligo 1|25 nmole
        24  AIR TRAVEL
        23  AUTOMOBILES OR CARS EA
        19  STAPLES-VT INVOICE CHARGES EA
        17  Ozarka Water Company EACH
        14  PARTS EACH

ITEM_DESCR by dollars
       1.73M     4.8K rows  GENERAL PURCHASE
      257.5K      129 rows  Janitorial Supplies CS
       61.6K        1 rows  INTEL VPRO TECHNOLOGY ADVA EA|2ND 3 CELL 51WHR EXP
       56.1K       38 rows  PAYMENT ON ACCOUNT EA
       55.1K       81 rows  CREDIT_CARD_CHARGE EA
       45.3K       45 rows  PRODUCT EA
       43.6K        1 rows  MAINTPRMAVW/EXTSU EA|MAINTSCNDRYAVSU EA|MAINTSCNDR
       40.1K      203 rows  ROOM CHARGES
       31.4K       63 rows  Miscellaneous EA
       29.7K       36 rows  Utility Bill EA
       23.8K        5 rows  PRODUCTS AND SERVICES EA
       21.2K        1 rows  SOS SO IN LOVE SQF|TEC SS 4-GAL GEN USE MULTI EA|B
       18.1K        1 rows  Pasta EACH
       17.5K       47 rows  Electrical Equipment EA
       17.4K        3 rows  Detergent EACH
       15.1K       46 rows  SPECIALIZED VEHICLES EA
       12.5K       25 rows  Grimsleys Inc EACH
       11.9K        1 rows  4052065971OK DEPT. OF COR ECH
       10.9K       42 rows  Facebook Ads EAC
       10.3K       12 rows  BUSINESS SERVICES EA

MCC_DESCRIPTION by rows
      1.2K  BOOK STORES
       719  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
       533  HOME SUPPLY WAREHOUSE STORES
       427  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
       423  GROCERY STORES, SUPERMARKETS
       316  MISCELLANEOUS AND RETAIL STORES
       295  STATIONERY,OFFICE SUPPLIES,PRINTING AND
       245  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
       236  UTILITIES-ELEC/GAS/HEAT OIL/SANITARY/WTR
       223  HARDWARE STORES
       216  CONTINUITY/SUBSCRIPTION MERCHANTS
       209  COMMERCIAL EQUIPMENT, NOT ELSEWHERE CLAS
       207  ALL OTHER DIRECT MARKETERS
       203  AUTOMOTIVE PARTS, ACCESSORIES STORES
       189  COMPUTER SOFTWARE STORES
       178  PLUMBING & HEATING EQUIPMENT AND SUPPLIE
       178  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       164  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
       147  ELECTRICAL PARTS AND EQUIPMENT
       143  MISCELLANEOUS AUTOMOTIVE DEALERS

MCC_DESCRIPTION by dollars
      331.9K      719 rows  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
      306.4K      207 rows  ALL OTHER DIRECT MARKETERS
      191.8K     1.2K rows  BOOK STORES
      183.0K      245 rows  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
      174.9K      427 rows  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
      172.5K       74 rows  COMPUTERS,COMPUTER PERIPHERAL EQUIPMENT,
      154.4K      209 rows  COMMERCIAL EQUIPMENT, NOT ELSEWHERE CLAS
      107.7K      295 rows  STATIONERY,OFFICE SUPPLIES,PRINTING AND
      104.5K      533 rows  HOME SUPPLY WAREHOUSE STORES
       96.2K      316 rows  MISCELLANEOUS AND RETAIL STORES
       93.1K      189 rows  COMPUTER SOFTWARE STORES
       77.2K      236 rows  UTILITIES-ELEC/GAS/HEAT OIL/SANITARY/WTR
       71.1K       41 rows  MISC FOOD STORES-SPECIALITY,CONVENIENCE,
       71.1K      178 rows  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       70.0K      164 rows  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
       67.3K      178 rows  PLUMBING & HEATING EQUIPMENT AND SUPPLIE
       64.8K       60 rows  PROFESSIONAL SERVICES NOT ELSEWHERE CLAS
       59.4K      114 rows  CHARITABLE AND SOCIAL SERVICE ORGANIZATI
       56.8K      147 rows  ELECTRICAL PARTS AND EQUIPMENT
       53.4K      143 rows  MISCELLANEOUS AUTOMOTIVE DEALERS

## who x when

LAST_NAME by TRANSACTION_DATE, dollars = AMOUNT
  Akerman                                   2020:35.8K
  Anderson                                  2020:12.4K
  BLACK                                     2020:42.7K
  Berry                                     2020:85.9K
  Boettcher                                 2020:21.5K
  Brinker                                   2020:12.6K
  Brown                                     2020:96.1K
  Bundy                                     2020:68.4K
  Davis                                     2020:36.7K
  DeLeon                                    2020:49.5K
  Duckworth                                 2020:55.7K
  Edwards                                   2020:32.2K
  Forbes                                    2020:69.6K
  Goad                                      2020:35.6K
  Guardado                                  2020:49.9K
  HUBBARD                                   2020:49.9K
  Johnson                                   2020:24.2K
  Jones                                     2020:7.2K
  Kindschi                                  2020:12.3K
  Moore                                     2020:10.1K
  Oliver                                    2020:1.5K
  PARRIS                                    2020:44.9K
  Price                                     2020:43.7K
  Robinson                                  2020:41.0K
  Schroeder                                 2020:32.1K
  Tornakian                                 2020:16.3K
  Turner                                    2020:12.1K
  WILSON                                    2020:12.3K
  Wilson                                    2020:19.0K
  Wingfield                                 2020:76.5K

MERCHANT by TRANSACTION_DATE, dollars = AMOUNT
  AIRGAS USA, LLC                           2020:7.2K
  AT&T PREMIER EBIL                         2020:28.9K
  B & C Business Products                   2020:21.7K
  CENTRAL OKLAHOMAWINLSN                    2020:27.6K
  DCAM CENTRAL PRINTING                     2020:42.0K
  DEPARTMENT OF MILITARY                    2020:43.3K
  DMI  DELL K-12/GOVT                       2020:80.5K
  ESRI                                      2020:47.7K
  GALLS                                     2020:35.5K
  GRAINGER                                  2020:188.5K
  KIAMICHI OPPORTUNITIES                    2020:60.8K
  LOWES #00241                              2020:24.3K
  LOWES #02540                              2020:35.3K
  MCKESSON MEDICAL SUPPLY                   2020:54.8K
  MCMASTER-CARR                             2020:8.5K
  NAPA AUTO PARTS 0000415                   2020:6.0K
  OKC/EZ-PAY                                2020:29.4K
  SOUTH CENTRAL INDUSTRIES                  2020:257.5K
  STAPLES                                   2020:27.0K
  STAPLES       00105288                    2020:7.7K
  STILLWATER MILLING COMP                   2020:19.1K
  TFS FISHERSCI ECOM HUS                    2020:18.6K
  THE JOURNAL RECORD PUBLIS                 2020:6.5K
  VETERANS AFFRS DMC                        2020:10.1K
  VWR INTERNATIONAL INC                     2020:13.6K
  WAL-MART #0137                            2020:2.1K
  WAL-MART #4241                            2020:5.1K
  WM SUPERCENTER #137                       2020:5.1K
  WM SUPERCENTER #4241                      2020:3.0K
  ZOOM.US                                   2020:4.7K

## what

AGENCYNBR: 01000 69%, 13100 15%, 09000 4%, 02500 4%, 04000 4%, 15000 1%, 04900 1%, 18500 0%, 04700 0%, 10500 0%, 12500 0%, 03900 0%

AGENCYNAME: OKLAHOMA STATE UNIVERSITY 69%, DEPARTMENT OF CORRECTIONS 15%, OFFICE OF MANAGEMENT AND ENTER 4%, OKLAHOMA MILITARY DEPARTMENT 4%, DEPT OF AGRICULTURE FOOD & FOR 4%, UNIV.OF SCIENCE & ARTS OF OK 1%, ATTORNEY GENERAL 1%, CORPORATION COMMISSION 0%, INDIGENT DEFENSE SYSTEM 0%, CAPITOL IMPROVEMENT AUTHORITY 0%, DEPARTMENT OF MINES 0%, BOLL WEEVIL ERADICATION ORG. 0%

FIRST_INITIAL: J 15%, K 11%, A 11%, C 10%, M 9%, S 9%, D 7%, T 7%, L 6%, R 6%, B 5%, P 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CALENDAR_YEAR | other | 1 | 0 | 2020 10.0K |
| CALENDAR_MONTH | other | 1 | 0 | 07 10.0K |
| AGENCYNBR | category | 22 | 0 | 01000 6.8K; 13100 1.5K; 09000 441; 02500 427 |
| AGENCYNAME | category | 22 | 0 | OKLAHOMA STATE UNIVERSITY 6.8K; DEPARTMENT OF CORRECTIONS 1.5K; OFFICE OF MANAGEMENT AND  441; OKLAHOMA MILITARY DEPARTM 427 |
| LAST_NAME | who | 1.1K | 0 | Duckworth 248; Brown 194; Wingfield 147; Moore 100 |
| FIRST_INITIAL | category | 26 | 0 | J 1.3K; K 936; A 931; C 872 |
| ITEM_DESCR | who | 3.9K | 0 | GENERAL PURCHASE 4.8K; ROOM CHARGES 203; Janitorial Supplies CS 144; CREDIT_CARD_CHARGE EA 98 |
| AMOUNT | amount | 7.0K | 0 | 51.48 58; 125 58; 192 56; 6.9 55 |
| MERCHANT | who | 4.1K | 0 | GRAINGER 346; LOWES #00241 268; SOUTH CENTRAL INDUSTRIES 158; STAPLES 121 |
| TRANSACTION_DATE | date | 43 | 0 | 28-Jul-20 503; 08-Jul-20 489; 16-Jul-20 483; 30-Jun-20 471 |
| POST_DATE | date | 23 | 0 | 13-Jul-20 652; 27-Jul-20 635; 20-Jul-20 557; 29-Jul-20 500 |
| MCC_DESCRIPTION | who | 197 | 0 | BOOK STORES 1.2K; INDUSTRIAL SUPPLIES NOT E 719; HOME SUPPLY WAREHOUSE STO 533; LAB/MEDICAL/DENTAL/OPHTHA 427 |
| ROWID | id | 10.0K | 0 | AAAJGhAAEAAH8O7AAP 50; AAAJGhAAEAAH8OvAAV 50; AAAJGhAAEAAH8OvAAU 50; AAAJGhAAEAAH8OvAAT 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:45:10.77200 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9bb05e83-44ae-47ab-a723-f 10.0K |
| SRC_SHA256 | who | 1 | 0 | a767e1433e1d2fbf1b883ab8f 10.0K |
