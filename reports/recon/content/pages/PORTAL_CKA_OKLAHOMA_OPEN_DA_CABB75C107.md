# PORTAL_CKA_OKLAHOMA_OPEN_DA_CABB75C107

rows 10.0K  columns 16  scan 5.0s

roles: amount 1, audit 2, category 3, date 3, id 1, other 2, who 5

## when

TRANSACTION_DATE
  2018     10.0K  ##############################

POST_DATE
  2018     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -2.0K | 103.49 | 3.4K | 41.0K | 3.17M |

## who

LAST_NAME by rows
       842  Dang
       343  Dugan
       161  Brown
        87  Clark
        84  Mitchell
        78  Bowers
        68  Johnson
        67  Jacob
        67  Troester
        67  Turner
        65  Jones
        62  Duff
        61  Smith
        61  Davis
        61  Anderson
        60  Price
        56  Phillips
        51  Wang
        50  Martin
        49  Edwards

LAST_NAME by dollars
      199.6K      842 rows  Dang
       96.4K      343 rows  Dugan
       51.8K       87 rows  Clark
       46.9K       23 rows  Marshall
       46.2K        4 rows  Killman
       44.9K       60 rows  Price
       43.0K       19 rows  Broiles
       34.2K      161 rows  Brown
       30.0K       50 rows  Martin
       27.3K        6 rows  Stover
       26.3K       31 rows  Newsom
       26.2K       65 rows  Jones
       25.0K       67 rows  Turner
       24.3K       45 rows  Robinson
       24.3K       62 rows  Duff
       22.6K       78 rows  Bowers
       21.8K       67 rows  Troester
       20.3K       38 rows  Kindred
       20.1K       61 rows  Davis
       19.5K       68 rows  Johnson

MERCHANT by rows
       339  AMAZON MKTPLACE PMTS
       305  LOWES #00241
       277  AMAZON MKTPLACE PMTS WWW.
       131  GRAINGER
       126  Amazon.com
       126  STAPLES       00105288
       114  IN  DEARINGER PRINTING &
        95  STILLWATER MILLING COMP
        80  WAL-MART #0137
        80  WM SUPERCENTER #137
        79  WAL-MART #4241
        78  WM SUPERCENTER #4241
        74  LOCKE SUPPLY
        74  MCMASTER-CARR
        69  VWR INTERNATIONAL INC
        63  AMAZON.COM AMZN.COM/BILL
        60  TFS FISHERSCI ECOM HUS
        58  OK DEPT OF CAREER TECH
        55  NAPA AUTO PARTS 0000415
        55  ATWOOD 05 STILLWATER

MERCHANT by dollars
       50.7K        3 rows  ESRI
       45.2K      339 rows  AMAZON MKTPLACE PMTS
       43.9K      131 rows  GRAINGER
       41.4K      277 rows  AMAZON MKTPLACE PMTS WWW.
       33.8K      114 rows  IN  DEARINGER PRINTING &
       28.7K       19 rows  ATT BILL PAYMENT
       28.4K      305 rows  LOWES #00241
       26.7K       60 rows  TFS FISHERSCI ECOM HUS
       25.9K      126 rows  Amazon.com
       24.5K        9 rows  RESIDENCE INN STILLWAT
       23.1K        7 rows  THOMSON WEST TCD
       22.0K       58 rows  OK DEPT OF CAREER TECH
       21.3K       22 rows  OKC/EZ-PAY
       19.5K       50 rows  STILLWATER WINNELSON C
       19.3K       35 rows  XEROX CORPORATION/RBO
       17.9K       69 rows  VWR INTERNATIONAL INC
       15.6K       10 rows  HOMETOWN BRAND CENTER
       15.5K       17 rows  ALLEGRA PRINT AND IMAGING
       15.3K       19 rows  4IMPRINT
       15.1K       95 rows  STILLWATER MILLING COMP

ITEM_DESCR by rows
      5.1K  GENERAL PURCHASE
      1.1K  AIR TRAVEL
       489  ROOM CHARGES
        64  DESCRIPTION EACH
        54  SQUARE PURCHASE NMB
        38  Square Purchase NMB
        35  Facebook Ads EAC
        25  CAR RENTAL
        22  INVOICE EA
        20  25 nmole DNA Oligo 1|25 nmole DNA Oligo 1|25 nmole
        19  Electrical Equipment/Suppl INV
        16  PRODUCTS AND SERVICES EA
        13  PAYMENT ON ACCOUNT EA
        13  SHIPPING CHARGES
        12  Default Product Unit
        12  GOOGLE * Clicks
        11  Spider Woman s Granddaught PCE
        11  UTILITY SERVICES EA
        10  PARTS EAC
         9  PARTS EACH

ITEM_DESCR by dollars
       1.73M     5.1K rows  GENERAL PURCHASE
      250.2K     1.1K rows  AIR TRAVEL
      204.0K      489 rows  ROOM CHARGES
       41.0K        1 rows  MAINTPRMAVSU EA|MAINTSCNDRYAVSU EA|MAINTPRMAEW/EXT
       34.1K       54 rows  SQUARE PURCHASE NMB
       26.8K        6 rows  00070509 ITM
       26.0K       16 rows  PRODUCTS AND SERVICES EA
       25.8K       64 rows  DESCRIPTION EACH
       14.7K       13 rows  PAYMENT ON ACCOUNT EA
       11.6K       38 rows  Square Purchase NMB
        9.2K       10 rows  PARTS EAC
        9.1K        7 rows  UNISOURCE ITEM EA
        8.6K        9 rows  PRODUCT EA
        7.6K        1 rows  MAINTPRMAVCU EA|MAINTPRMAG SACU EA|MAINTPRMAG 3DCU
        7.0K        8 rows  PARTS SET
        6.5K        1 rows  FBOPYMT29109800 PCE
        6.4K        4 rows  Automotive General Merch EA
        5.9K        1 rows  093716773 PCS
        5.9K        2 rows  NSQ 500/550 HI OUTPUT KT V EA
        5.7K        4 rows  FREIGHT NMB

MCC_DESCRIPTION by rows
       823  BOOK STORES
       581  GROCERY STORES  SUPERMARKETS
       525  AIRLINES  AIR CARRIERS
       451  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
       433  HOME SUPPLY WAREHOUSE STORES
       332  MISCELLANEOUS AND RETAIL STORES
       322  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
       302  AMERICAN AIRLINES
       252  HARDWARE STORES
       197  STATIONARY  OFFICE AND SCHOOL SUPPLY STO
       176  EATING PLACES  RESTAURANTS
       168  STATIONERY OFFICE SUPPLIES PRINTING AND
       166  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       163  MISCELLANEOUS PUBLISHING & PRINTING
       149  AUTOMOTIVE PARTS  ACCESSORIES STORES
       147  PLUMBING & HEATING EQUIPMENT AND SUPPLIE
       135  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
       135  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLAS
       128  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
       124  ELECTRONIC SALES

MCC_DESCRIPTION by dollars
      145.8K      322 rows  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
      138.1K      823 rows  BOOK STORES
      137.4K      302 rows  AMERICAN AIRLINES
      127.9K      451 rows  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
       93.7K       59 rows  COMPUTERS COMPUTER PERIPHERAL EQUIPMENT 
       82.6K      166 rows  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       79.6K      332 rows  MISCELLANEOUS AND RETAIL STORES
       79.6K      124 rows  CHARITABLE AND SOCIAL SERVICE ORGANIZATI
       76.7K      135 rows  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLAS
       72.8K      163 rows  MISCELLANEOUS PUBLISHING & PRINTING
       62.8K       86 rows  SCHOOLS AND EDUCATIONAL SERVICES NOT ELS
       61.9K      128 rows  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
       60.9K       69 rows  PROFESSIONAL SERVICES NOT ELSEWHERE CLAS
       57.3K      124 rows  ELECTRONIC SALES
       56.1K      176 rows  EATING PLACES  RESTAURANTS
       52.7K       63 rows  DURABLE GOODS NOT ELSEWHERE CLASSIFIED
       50.6K      135 rows  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
       48.1K      433 rows  HOME SUPPLY WAREHOUSE STORES
       47.9K       94 rows  ALL OTHER DIRECT MARKETERS
       43.7K       67 rows  DELTA

## who x when

LAST_NAME by TRANSACTION_DATE, dollars = AMOUNT
  Anderson                                  2018:14.8K
  Bowers                                    2018:22.6K
  Broiles                                   2018:43.0K
  Brown                                     2018:34.2K
  Clark                                     2018:51.8K
  Dang                                      2018:199.6K
  Davis                                     2018:20.1K
  Duff                                      2018:24.3K
  Dugan                                     2018:96.4K
  Edwards                                   2018:9.6K
  Jacob                                     2018:18.5K
  Johnson                                   2018:19.5K
  Jones                                     2018:26.2K
  Killman                                   2018:46.2K
  Kindred                                   2018:20.3K
  Marshall                                  2018:46.9K
  Martin                                    2018:30.0K
  Mitchell                                  2018:12.5K
  Newsom                                    2018:26.3K
  Phillips                                  2018:12.1K
  Price                                     2018:44.9K
  Robinson                                  2018:24.3K
  Smith                                     2018:15.2K
  Stover                                    2018:27.3K
  Troester                                  2018:21.8K
  Turner                                    2018:25.0K
  Wang                                      2018:14.0K

MERCHANT by TRANSACTION_DATE, dollars = AMOUNT
  4IMPRINT                                  2018:15.3K
  ALLEGRA PRINT AND IMAGING                 2018:15.5K
  AMAZON MKTPLACE PMTS                      2018:45.2K
  AMAZON MKTPLACE PMTS WWW.                 2018:41.4K
  AMAZON.COM AMZN.COM/BILL                  2018:10.8K
  ATT BILL PAYMENT                          2018:28.7K
  ATWOOD 05 STILLWATER                      2018:3.8K
  Amazon.com                                2018:25.9K
  ESRI                                      2018:50.7K
  GRAINGER                                  2018:43.9K
  HOMETOWN BRAND CENTER                     2018:15.6K
  IN  DEARINGER PRINTING &                  2018:33.8K
  LOCKE SUPPLY                              2018:6.0K
  LOWES #00241                              2018:28.4K
  MCMASTER-CARR                             2018:10.7K
  NAPA AUTO PARTS 0000415                   2018:3.5K
  OK DEPT OF CAREER TECH                    2018:22.0K
  OKC/EZ-PAY                                2018:21.3K
  RESIDENCE INN STILLWAT                    2018:24.5K
  STAPLES       00105288                    2018:11.8K
  STILLWATER MILLING COMP                   2018:15.1K
  STILLWATER WINNELSON C                    2018:19.5K
  TFS FISHERSCI ECOM HUS                    2018:26.7K
  THOMSON WEST TCD                          2018:23.1K
  VWR INTERNATIONAL INC                     2018:17.9K
  WAL-MART #0137                            2018:6.0K
  WAL-MART #4241                            2018:9.5K
  WM SUPERCENTER #137                       2018:6.5K
  WM SUPERCENTER #4241                      2018:6.0K
  XEROX CORPORATION/RBO                     2018:19.3K

## what

AGENCYNBR:  01000 88%,  04000 4%,  02500 3%,  09000 2%,  04900 1%,  04700 1%,  06500 0%,  03000 0%,  04500 0%,  03900 0%,  05500 0%,  06000 0%

AGENCYNAME: OKLAHOMA STATE UNIVERSITY 88%, DEPT OF AGRICULTURE FOOD & FOR 4%, OKLAHOMA MILITARY DEPARTMENT 3%, OFFICE OF MANAGEMENT AND ENTER 2%, ATTORNEY GENERAL 1%, INDIGENT DEFENSE SYSTEM 1%, STATE BANKING DEPARTMENT 0%, ALCOHOLIC BEV. LAWS ENFORCE. 0%, OKLA. BD. OF ARCHITECTS 0%, BOLL WEEVIL ERADICATION ORG. 0%, STATE ARTS COUNCIL 0%, OK DEP AEROSPACE & AERONAUTICS 0%

FIRST_INITIAL: T 14%, J 13%, M 10%, L 9%, S 8%, K 8%, A 8%, D 8%, C 8%, R 6%, B 4%, P 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CALENDAR_YEAR | other | 1 | 0 | 2018 10.0K |
| CALENDAR_MONTH | other | 1 | 0 | 07 10.0K |
| AGENCYNBR | category | 14 | 0 |  01000 8.8K;  04000 401;  02500 342;  09000 188 |
| AGENCYNAME | category | 14 | 0 | OKLAHOMA STATE UNIVERSITY 8.8K; DEPT OF AGRICULTURE FOOD  401; OKLAHOMA MILITARY DEPARTM 342; OFFICE OF MANAGEMENT AND  188 |
| LAST_NAME | who | 1.1K | 0 | Dang 843; Dugan 344; Brown 162; Price 94 |
| FIRST_INITIAL | category | 26 | 0 | T 1.3K; J 1.1K; M 896; L 838 |
| ITEM_DESCR | who | 2.7K | 0 | GENERAL PURCHASE 5.1K; AIR TRAVEL 1.1K; ROOM CHARGES 489; DESCRIPTION EACH 64 |
| AMOUNT | amount | 6.8K | 0 | 9.00000000000000000000000 329; 25.0000000000000000000000 162; 186.000000000000000000000 63; 5.75000000000000000000000 62 |
| MERCHANT | who | 4.1K | 0 | AMAZON MKTPLACE PMTS 339; LOWES #00241 305; AMAZON MKTPLACE PMTS WWW. 277; GRAINGER 138 |
| TRANSACTION_DATE | date | 45 | 0 | 03-Jul-18 505; 12-Jul-18 494; 24-Jul-18 479; 11-Jul-18 467 |
| POST_DATE | date | 22 | 0 | 23-Jul-18 791; 30-Jul-18 708; 16-Jul-18 692; 09-Jul-18 660 |
| MCC_DESCRIPTION | who | 248 | 0 | BOOK STORES 823; GROCERY STORES  SUPERMARK 581; AIRLINES  AIR CARRIERS 525; INDUSTRIAL SUPPLIES NOT E 451 |
| ROWID | id | 10.0K | 0 | AAAJGhAAEAADP3eAAL 50; AAAJGhAAEAADP3eAAK 50; AAAJGhAAEAADP3eAAJ 50; AAAJGhAAEAADP3eAAI 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:46:20.14474 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3dd8bad7-bce3-4edc-809c-9 10.0K |
| SRC_SHA256 | who | 1 | 0 | c7ea72a2151208b2f97a011a8 10.0K |
