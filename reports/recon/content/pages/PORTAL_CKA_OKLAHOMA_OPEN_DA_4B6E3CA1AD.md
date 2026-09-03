# PORTAL_CKA_OKLAHOMA_OPEN_DA_4B6E3CA1AD

rows 10.0K  columns 16  scan 4.2s

roles: amount 1, audit 2, category 3, date 3, id 1, other 2, who 5

## when

TRANSACTION_DATE
  2014       126  
  2015      9.9K  ##############################

POST_DATE
  2015     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -4.8K | 99 | 3.3K | 31.3K | 3.02M |

## who

LAST_NAME by rows
       208  Hines
       193  Bowers
       174  Tornakian
       162  Forquer
       141  Robinson
        91  Teel
        75  Turner
        70  Hood
        69  Clark
        68  Jones
        67  Brown
        67  Bolser
        58  Bradley
        58  Wood
        54  Ross
        52  Bailey
        52  Dickenson
        49  Young
        48  Williams
        48  Yarbrough-Tessman

LAST_NAME by dollars
       88.0K      162 rows  Forquer
       85.1K      174 rows  Tornakian
       75.8K       35 rows  Edwards
       60.0K      208 rows  Hines
       32.4K       48 rows  Yarbrough-Tessman
       32.1K       29 rows  Berry
       31.7K      141 rows  Robinson
       31.0K       44 rows  Bryant
       30.9K      193 rows  Bowers
       30.3K       45 rows  Biggs
       30.3K       34 rows  Kindred
       29.5K       22 rows  Fitzpatrick
       28.5K       75 rows  Turner
       27.6K       17 rows  Broiles
       25.7K        6 rows  Finley
       25.6K       67 rows  Bolser
       24.1K       52 rows  Bailey
       23.9K       69 rows  Clark
       23.0K        6 rows  Baustert
       22.9K       40 rows  Baker

MERCHANT by rows
       435  AMAZON MKTPLACE PMTS
       282  LOWES #00241
       219  Amazon.com
       193  STAPLES       00105288
       143  WW GRAINGER
       139  AIRGAS CENTRAL
       130  VWR INTERNATIONAL INC
       112  WAL-MART #0137
       106  WM SUPERCENTER #137
        76  SIGMA ALDRICH US
        73  DEARINGER PRINTING & TROP
        72  NAPA AUTO PARTS
        69  WAL-MART #4241
        68  TFS FISHERSCI ECOM HUS
        60  REXEL2442
        59  STILLWATER MILLING COMP
        58  WM SUPERCENTER #4241
        56  STAPLES
        55  AT&T DATA
        54  B&C BUSINESS PRODUCTS

MERCHANT by dollars
       51.7K        7 rows  SIMPLEX GRINNELL WEB P
       51.3K      435 rows  AMAZON MKTPLACE PMTS
       37.8K      143 rows  WW GRAINGER
       31.4K        7 rows  GALT FOUNDATION
       28.8K      130 rows  VWR INTERNATIONAL INC
       28.1K      219 rows  Amazon.com
       25.2K      282 rows  LOWES #00241
       24.6K       68 rows  TFS FISHERSCI ECOM HUS
       24.1K       50 rows  DOD EMALL
       22.5K       13 rows  THOMSON WEST TCD
       22.0K        4 rows  SIMPLEXGRINNELL
       21.5K       25 rows  OK CORRECTIONAL INDUST
       21.3K       60 rows  REXEL2442
       19.8K       30 rows  OKC UTILITY SERVICEWEB S
       19.6K       17 rows  ATT BILL PAYMENT
       18.5K      139 rows  AIRGAS CENTRAL
       18.2K       24 rows  XEROX CORPORATION/RBO
       17.7K        8 rows  SHI CORP
       16.1K      193 rows  STAPLES       00105288
       16.1K       76 rows  SIGMA ALDRICH US

ITEM_DESCR by rows
      6.3K  GENERAL PURCHASE
       307  ROOM CHARGES
       159  AIR TRAVEL
        55  AT&T SERVICE PAYMENT ITM
        33  PARTS SET
        32  JANITORIAL SUPPLIES NMB
        31  25 nmole DNA Oligo 1|25 nmole DNA Oligo 1|25 nmole
        25  PRODUCTS AND SERVICES EA
        20  237817 Service Unit
        15  NEWS ADV./SUBSC. EACH
        12  CAR RENTAL
        10  UNISOURCE ITEM EA
         9  SHIPPING CHARGES
         9   PCE
         9  001 Priority          1LB PCE
         9  GOOGLE* Clicks
         8  001 Economy           1LB PCE
         8  CYLCARBONDIOXIDEIND200CGA3 MO
         8  CYLACETYLENEINDUSTRIAL3 MO|CYLACETYLENEIND4CGA510
         7  Merchandise General EA

ITEM_DESCR by dollars
       2.17M     6.3K rows  GENERAL PURCHASE
       86.1K      307 rows  ROOM CHARGES
       46.2K      159 rows  AIR TRAVEL
       17.4K        4 rows  00070509 ITM
       11.9K       25 rows  PRODUCTS AND SERVICES EA
        9.7K       20 rows  237817 Service Unit
        8.5K       32 rows  JANITORIAL SUPPLIES NMB
        6.6K       10 rows  UNISOURCE ITEM EA
        6.4K       33 rows  PARTS SET
        5.9K        4 rows  UNISOURCE ITEM EA|UNISOURCE ITEM EA|UNISOURCE ITEM
        5.7K        1 rows  701830498 PCS
        5.7K        1 rows  701822188 PCS
        5.6K        2 rows  PAYMENT ON ACCOUNT EA
        5.3K        3 rows  Firehouse World (Booth # 1 EAC
        4.8K        1 rows  115097 EA
        4.6K        2 rows  PRINTING NMB
        4.6K        1 rows  NONE TON
        4.5K       15 rows  NEWS ADV./SUBSC. EACH
        4.4K        7 rows  Merchandise General EA
        4.1K        1 rows  AcrobatPro11NEWCLPL2 EA

MCC_DESCRIPTION by rows
       707  BOOK STORES
       604  GROCERY STORES AND SUPERMARKETS
       521  DENTAL/LABORATORY/MEDICAL/OPHTHALMIC HOSP EQIP AND SUP.
       459  MISCELLANEOUS AND SPECIALTY RETAIL STORES
       423  HOME SUPPLY WAREHOUSE STORES
       395  INDUSTRIAL SUPPLIES NOT ELSEWHERE CLASSIFIED
       326  STATIONERY  OFFICE SUPPLIES  PRINTING AND WRITING PAPER
       317  BUSINESS SERVICES NOT ELSEWHERE CLASSIFIED
       267  STATIONERY OFFICE AND SCHOOL SUPPLY STORES
       222  PLUMBING AND HEATING EQUIPMENT AND SUPPLIES
       218  GOVERNMENT SERVICES--NOT ELSEWHERE CLASSIFIED
       196  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLASSIFIED
       195  CHEMICALS AND ALLIED PRODUCTS NOT ELSEWHERE CLASSIFIED
       190  HARDWARE STORES
       188  DIRCT MARKETING/DIRCT MARKETERS--NOT ELSEWHERE CLASSIFIED
       187  AUTOMOTIVE PARTS AND ACCESSORIES STORES
       180  ELECTRICAL PARTS AND EQUIPMENT
       177  TELECOMMUNICATION SERVICES
       156  ELECTRONICS STORES
       137  MEMBERSHIP ORGANIZATIONS--NOT ELSEWHERE CLASSIFIED

MCC_DESCRIPTION by dollars
      189.9K      521 rows  DENTAL/LABORATORY/MEDICAL/OPHTHALMIC HOSP EQIP AND SUP.
      145.6K      317 rows  BUSINESS SERVICES NOT ELSEWHERE CLASSIFIED
      128.5K      459 rows  MISCELLANEOUS AND SPECIALTY RETAIL STORES
      117.3K      395 rows  INDUSTRIAL SUPPLIES NOT ELSEWHERE CLASSIFIED
      101.0K      218 rows  GOVERNMENT SERVICES--NOT ELSEWHERE CLASSIFIED
       95.1K      196 rows  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLASSIFIED
       90.1K      707 rows  BOOK STORES
       83.0K      326 rows  STATIONERY  OFFICE SUPPLIES  PRINTING AND WRITING PAPER
       77.4K      180 rows  ELECTRICAL PARTS AND EQUIPMENT
       72.2K      188 rows  DIRCT MARKETING/DIRCT MARKETERS--NOT ELSEWHERE CLASSIFIED
       68.8K      137 rows  MEMBERSHIP ORGANIZATIONS--NOT ELSEWHERE CLASSIFIED
       64.6K      222 rows  PLUMBING AND HEATING EQUIPMENT AND SUPPLIES
       56.8K       85 rows  PROFESSIONAL SERVICES NOT ELSEWHERE CLASSIFIED
       52.2K      116 rows  CHARITABLE AND SOCIAL SERVICE ORGANIZATIONS
       50.7K      127 rows  CATALOG MERCHANTS
       48.7K      195 rows  CHEMICALS AND ALLIED PRODUCTS NOT ELSEWHERE CLASSIFIED
       45.7K       69 rows  SCHOOLS AND EDUCATIONAL SERVICES NOT ELSEWHERE CLASSIFIED
       45.6K      156 rows  ELECTRONICS STORES
       45.1K       73 rows  OFFICE  PHOTOGRAPHIC  PHOTOCOPY  AND MICROFILM EQUIPMENT
       44.9K       61 rows  COMPUTERS  COMPUTER PERIPHERAL EQUIPMENT  SOFTWARE

## who x when

LAST_NAME by TRANSACTION_DATE, dollars = AMOUNT
  Bailey                                    2015:24.1K
  Baker                                     2014:2.7K 2015:20.2K
  Baustert                                  2015:23.0K
  Berry                                     2015:32.1K
  Biggs                                     2014:652.24 2015:29.6K
  Bolser                                    2015:25.6K
  Bowers                                    2015:30.9K
  Bradley                                   2014:50 2015:6.6K
  Broiles                                   2014:43.56 2015:27.5K
  Brown                                     2014:4.48 2015:12.0K
  Bryant                                    2015:31.0K
  Clark                                     2014:9.99 2015:23.9K
  Dickenson                                 2015:13.9K
  Edwards                                   2014:109.99 2015:75.7K
  Finley                                    2015:25.7K
  Fitzpatrick                               2015:29.5K
  Forquer                                   2015:88.0K
  Hines                                     2014:1.8K 2015:58.2K
  Hood                                      2014:93.56 2015:17.0K
  Jones                                     2014:142.03 2015:20.8K
  Kindred                                   2015:30.3K
  Robinson                                  2015:31.7K
  Ross                                      2015:9.0K
  Teel                                      2015:22.8K
  Tornakian                                 2014:343.30 2015:84.8K
  Turner                                    2014:14.76 2015:28.4K
  Williams                                  2014:-0.75 2015:7.9K
  Wood                                      2015:22.6K
  Yarbrough-Tessman                         2014:499.53 2015:31.9K
  Young                                     2015:7.3K

MERCHANT by TRANSACTION_DATE, dollars = AMOUNT
  AIRGAS CENTRAL                            2015:18.5K
  AMAZON MKTPLACE PMTS                      2014:55 2015:51.3K
  AT&T DATA                                 2014:44.99 2015:1.7K
  ATT BILL PAYMENT                          2015:19.6K
  Amazon.com                                2015:28.1K
  B&C BUSINESS PRODUCTS                     2015:14.1K
  DEARINGER PRINTING & TROP                 2015:8.2K
  DOD EMALL                                 2015:24.1K
  GALT FOUNDATION                           2015:31.4K
  LOWES #00241                              2014:129.62 2015:25.0K
  NAPA AUTO PARTS                           2014:468.92 2015:4.6K
  OK CORRECTIONAL INDUST                    2015:21.5K
  OKC UTILITY SERVICEWEB S                  2015:19.8K
  REXEL2442                                 2015:21.3K
  SHI CORP                                  2015:17.7K
  SIGMA ALDRICH US                          2015:16.1K
  SIMPLEX GRINNELL WEB P                    2015:51.7K
  SIMPLEXGRINNELL                           2015:22.0K
  STAPLES                                   2015:11.4K
  STAPLES       00105288                    2014:637.71 2015:15.5K
  STILLWATER MILLING COMP                   2014:272.55 2015:11.2K
  TFS FISHERSCI ECOM HUS                    2014:374.30 2015:24.3K
  THOMSON WEST TCD                          2015:22.5K
  VWR INTERNATIONAL INC                     2015:28.8K
  WAL-MART #0137                            2014:11.04 2015:5.4K
  WAL-MART #4241                            2014:8.91 2015:4.5K
  WM SUPERCENTER #137                       2014:4.48 2015:4.3K
  WM SUPERCENTER #4241                      2015:3.0K
  WW GRAINGER                               2015:37.8K
  XEROX CORPORATION/RBO                     2015:18.2K

## what

AGENCYNBR:  01000 86%,  04000 4%,  02500 4%,  09000 3%,  04900 1%,  04700 1%,  03000 0%,  06000 0%,  06500 0%,  03900 0%,  05500 0%,  02000 0%

AGENCYNAME: OKLAHOMA STATE UNIVERSITY 86%, DEPT OF AGRICULTURE FOOD & FOR 4%, OKLAHOMA MILITARY DEPARTMENT 4%, OFFICE OF MANAGEMENT AND ENTER 3%, ATTORNEY GENERAL 1%, INDIGENT DEFENSE SYSTEM 1%, ALCOHOLIC BEV. LAWS ENFORCE. 0%, OK DEP AEROSPACE & AERONAUTICS 0%, STATE BANKING DEPARTMENT 0%, BOLL WEEVIL ERADICATION ORG. 0%, STATE ARTS COUNCIL 0%, OKLAHOMA ACCOUNTANCY BOARD 0%

FIRST_INITIAL: J 15%, M 12%, R 10%, S 10%, D 10%, C 9%, K 8%, L 6%, T 6%, B 6%, A 6%, G 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CALENDAR_YEAR | other | 1 | 0 | 2015 10.0K |
| CALENDAR_MONTH | other | 1 | 0 | 01 10.0K |
| AGENCYNBR | category | 13 | 0 |  01000 8.6K;  04000 432;  02500 356;  09000 263 |
| AGENCYNAME | category | 13 | 0 | OKLAHOMA STATE UNIVERSITY 8.6K; DEPT OF AGRICULTURE FOOD  432; OKLAHOMA MILITARY DEPARTM 356; OFFICE OF MANAGEMENT AND  263 |
| LAST_NAME | who | 1.2K | 0 | Hines 208; Bowers 194; Tornakian 174; Forquer 162 |
| FIRST_INITIAL | category | 26 | 0 | J 1.3K; M 1.0K; R 891; S 884 |
| ITEM_DESCR | who | 2.8K | 5 | GENERAL PURCHASE 6.3K; ROOM CHARGES 307; AIR TRAVEL 159; AT&T SERVICE PAYMENT ITM 55 |
| AMOUNT | amount | 7.0K | 0 | 25.0000000000000000000000 92; 83.0000000000000000000000 61; 170.000000000000000000000 55; 89.0000000000000000000000 55 |
| MERCHANT | who | 3.2K | 0 | AMAZON MKTPLACE PMTS 435; LOWES #00241 282; Amazon.com 219; STAPLES       00105288 193 |
| TRANSACTION_DATE | date | 39 | 0 | 21-Jan-15 605; 27-Jan-15 601; 08-Jan-15 570; 07-Jan-15 568 |
| POST_DATE | date | 21 | 0 | 26-Jan-15 787; 12-Jan-15 773; 19-Jan-15 685; 23-Jan-15 593 |
| MCC_DESCRIPTION | who | 241 | 0 | BOOK STORES 707; GROCERY STORES AND SUPERM 604; DENTAL/LABORATORY/MEDICAL 521; MISCELLANEOUS AND SPECIAL 459 |
| ROWID | id | 10.1K | 0 | AAAJGhAANAANqWEAAR 50; AAAJGhAANAANqWEAAQ 50; AAAJGhAANAANqWEAAP 50; AAAJGhAANAANqWEAAO 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:47:26.13747 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0aaf68a9-b999-4c5e-b525-e 10.0K |
| SRC_SHA256 | who | 1 | 0 | b765669164ebbb4d558eb6e3b 10.0K |
