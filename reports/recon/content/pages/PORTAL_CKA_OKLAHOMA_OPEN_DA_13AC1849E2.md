# PORTAL_CKA_OKLAHOMA_OPEN_DA_13AC1849E2

rows 10.0K  columns 16  scan 4.6s

roles: amount 1, audit 2, category 3, date 3, id 1, other 2, who 5

## when

TRANSACTION_DATE
  2017     10.0K  ##############################

POST_DATE
  2017     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -2.8K | 102.80 | 3.5K | 39.6K | 3.29M |

## who

LAST_NAME by rows
       825  Brown
       289  Dugan
        87  Robinson
        79  Hines
        78  Jones
        77  Jacob
        76  Turner
        74  Bowers
        74  Connelly
        66  Clark
        62  Wang
        59  Bolser
        57  HUBBARD
        53  Paulk
        52  Anderson
        51  Wood
        50  Keener
        49  Smith
        46  Dickenson
        45  Edwards

LAST_NAME by dollars
      200.7K      825 rows  Brown
       82.8K      289 rows  Dugan
       60.6K       53 rows  Paulk
       50.1K       41 rows  PARRIS
       48.0K       10 rows  Baustert
       44.0K       59 rows  Bolser
       41.9K       87 rows  Robinson
       41.5K       46 rows  Dickenson
       39.2K       74 rows  Connelly
       39.0K       35 rows  Newsom
       37.1K        9 rows  Stover
       34.8K       21 rows  Berry
       30.3K       15 rows  Broiles
       30.2K       24 rows  Filonow
       26.8K        9 rows  Finley
       26.4K       66 rows  Clark
       25.4K       76 rows  Turner
       23.5K       78 rows  Jones
       23.3K       12 rows  Holston
       22.7K       40 rows  Martin

MERCHANT by rows
       464  AMAZON MKTPLACE PMTS
       330  LOWES #00241
       188  WW GRAINGER
       125  Amazon.com
       114  WAL-MART #4241
        95  STAPLES       00105288
        90  WM SUPERCENTER #4241
        81  WM SUPERCENTER #137
        75  QUALITY WATER SERVICES
        72  STILLWATER MILLING COMP
        71  WAL-MART #0137
        70  NAPA AUTO PARTS 0000415
        69  STAPLES
        67  SIGMA ALDRICH US
        67  HOLIDAY INN EXPRESS & SU
        60  FOOD PYRAMID #69
        55  VWR INTERNATIONAL INC
        52  IN  DEARINGER PRINTING &
        52  DAYS INN ALTUS
        51  TFS FISHERSCI ECOM HUS

MERCHANT by dollars
       83.5K      188 rows  WW GRAINGER
       60.0K      464 rows  AMAZON MKTPLACE PMTS
       42.5K        6 rows  GALT FOUNDATION
       40.0K       34 rows  OKC UTILITY SERVICEWEB S
       39.6K        1 rows  ESRI
       35.0K       17 rows  SOUTH CENTRAL INDUSTRIES
       32.9K       26 rows  STANDLEY SYSTEMS LLC
       32.4K      330 rows  LOWES #00241
       31.1K       33 rows  ATT BILL PAYMENT
       27.6K        8 rows  THOMSON WEST TCD
       25.6K      125 rows  Amazon.com
       23.5K        8 rows  RESIDENCE INN STILLWAT
       20.3K       13 rows  OK CORRECTIONAL INDUST
       19.9K       69 rows  STAPLES
       17.5K       28 rows  XEROX CORPORATION/RBO
       16.6K       72 rows  STILLWATER MILLING COMP
       16.4K        4 rows  SHI INTERNATIONAL CORP
       16.4K       67 rows  SIGMA ALDRICH US
       14.5K       51 rows  TFS FISHERSCI ECOM HUS
       14.3K        4 rows  MULTIVIEW INC

ITEM_DESCR by rows
      5.4K  GENERAL PURCHASE
      1.0K  AIR TRAVEL
       490  ROOM CHARGES
        46  DESCRIPTION EACH
        34  SQUARE PURCHASE NMB
        32  AT&T SERVICE PAYMENT
        23  25 nmole DNA Oligo 1|25 nmole DNA Oligo 1|25 nmole
        22  PRODUCTS AND SERVICES EA
        21  237817 Service Unit
        18  PRODUCT EACH
        16  GOOGLE * Clicks
        15  FACEBOOK ADS EAC
        15  UNISOURCE ITEM EA
        15  CAR RENTAL
        12  UTILITY SERVICES EA
        10  Ralph Ellison: A Biography PCE
        10  PARTS SET
        10  STAPLES-VT INVOICE CHARGES EA
         9  SHIPPING CHARGES
         8  MFG COMP EA

ITEM_DESCR by dollars
       1.91M     5.4K rows  GENERAL PURCHASE
      239.2K     1.0K rows  AIR TRAVEL
      175.5K      490 rows  ROOM CHARGES
       39.6K        1 rows  MAINTPRMAVSU EA|MAINTSCNDRYAVSU EA|MAINTPRMAEW/EXT
       31.0K       22 rows  PRODUCTS AND SERVICES EA
       18.2K       34 rows  SQUARE PURCHASE NMB
       16.5K        4 rows  00070509 ITM
       11.9K       46 rows  DESCRIPTION EACH
       11.9K        2 rows   EAC
       10.2K        1 rows  Dell 16 GB Certified Memo EA
        8.7K       21 rows  237817 Service Unit
        6.9K        1 rows  LED Lamp BR40 13W 3000 EA|LED High Bay Light Engin
        6.1K        1 rows  Water Heater65 gal.3600 EA
        5.8K        1 rows  089703429 PCS
        5.6K       15 rows  UNISOURCE ITEM EA
        5.4K        6 rows  PRODUCT EAC
        5.4K        1 rows  ZENworksSuitePriorityMaint EA
        5.1K       18 rows  PRODUCT EACH
        5.0K        1 rows  DJI Matrice 600 Pro Hexaco PCE
        4.8K        1 rows  300444474 PCS

MCC_DESCRIPTION by rows
       677  GROCERY STORES  SUPERMARKETS
       644  BOOK STORES
       513  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
       497  AIRLINES  AIR CARRIERS
       473  HOME SUPPLY WAREHOUSE STORES
       351  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
       333  MISCELLANEOUS AND RETAIL STORES
       289  AMERICAN AIRLINES
       255  HARDWARE STORES
       207  STATIONERY OFFICE SUPPLIES PRINTING AND
       182  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
       181  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLAS
       167  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       159  EATING PLACES  RESTAURANTS
       158  STATIONARY  OFFICE AND SCHOOL SUPPLY STO
       158  AUTOMOTIVE PARTS  ACCESSORIES STORES
       141  ALL OTHER DIRECT MARKETERS
       141  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
       138  PLUMBING & HEATING EQUIPMENT AND SUPPLIE
       134  HOLIDAY INNS

MCC_DESCRIPTION by dollars
      188.6K      513 rows  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
      158.5K      351 rows  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
      124.9K      289 rows  AMERICAN AIRLINES
      106.6K       64 rows  COMPUTERS COMPUTER PERIPHERAL EQUIPMENT 
      101.8K      644 rows  BOOK STORES
      101.6K      181 rows  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLAS
       97.3K      106 rows  PROFESSIONAL SERVICES NOT ELSEWHERE CLAS
       94.3K      333 rows  MISCELLANEOUS AND RETAIL STORES
       75.7K      141 rows  ALL OTHER DIRECT MARKETERS
       74.2K      207 rows  STATIONERY OFFICE SUPPLIES PRINTING AND
       69.4K      119 rows  UTILITIES-ELEC/GAS/HEAT OIL/SANITARY/WTR
       64.4K      473 rows  HOME SUPPLY WAREHOUSE STORES
       64.3K       85 rows  SCHOOLS AND EDUCATIONAL SERVICES NOT ELS
       60.2K      182 rows  TELECOMMUNICATION SERV.INCLUD. LOCAL/L.D
       59.5K      167 rows  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       57.3K      141 rows  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
       56.2K       65 rows  OFFICE  PHOTOGRAPHIC  PHOTOCOPY  AND MIC
       50.7K      159 rows  EATING PLACES  RESTAURANTS
       49.9K      115 rows  CHARITABLE AND SOCIAL SERVICE ORGANIZATI
       48.5K       93 rows  DURABLE GOODS NOT ELSEWHERE CLASSIFIED

## who x when

LAST_NAME by TRANSACTION_DATE, dollars = AMOUNT
  Anderson                                  2017:11.9K
  Baustert                                  2017:48.0K
  Berry                                     2017:34.8K
  Bolser                                    2017:44.0K
  Bowers                                    2017:17.7K
  Broiles                                   2017:30.3K
  Brown                                     2017:200.7K
  Clark                                     2017:26.4K
  Connelly                                  2017:39.2K
  Dickenson                                 2017:41.5K
  Dugan                                     2017:82.8K
  Edwards                                   2017:10.0K
  Filonow                                   2017:30.2K
  Finley                                    2017:26.8K
  HUBBARD                                   2017:18.2K
  Hines                                     2017:11.3K
  Holston                                   2017:23.3K
  Jacob                                     2017:22.5K
  Jones                                     2017:23.5K
  Keener                                    2017:9.4K
  Martin                                    2017:22.7K
  Newsom                                    2017:39.0K
  PARRIS                                    2017:50.1K
  Paulk                                     2017:60.6K
  Robinson                                  2017:41.9K
  Smith                                     2017:11.2K
  Stover                                    2017:37.1K
  Turner                                    2017:25.4K
  Wang                                      2017:21.1K
  Wood                                      2017:14.3K

MERCHANT by TRANSACTION_DATE, dollars = AMOUNT
  AMAZON MKTPLACE PMTS                      2017:60.0K
  ATT BILL PAYMENT                          2017:31.1K
  Amazon.com                                2017:25.6K
  DAYS INN ALTUS                            2017:3.0K
  ESRI                                      2017:39.6K
  FOOD PYRAMID #69                          2017:1.8K
  GALT FOUNDATION                           2017:42.5K
  HOLIDAY INN EXPRESS & SU                  2017:9.3K
  IN  DEARINGER PRINTING &                  2017:14.1K
  LOWES #00241                              2017:32.4K
  NAPA AUTO PARTS 0000415                   2017:5.6K
  OK CORRECTIONAL INDUST                    2017:20.3K
  OKC UTILITY SERVICEWEB S                  2017:40.0K
  QUALITY WATER SERVICES                    2017:3.8K
  RESIDENCE INN STILLWAT                    2017:23.5K
  SIGMA ALDRICH US                          2017:16.4K
  SOUTH CENTRAL INDUSTRIES                  2017:35.0K
  STANDLEY SYSTEMS LLC                      2017:32.9K
  STAPLES                                   2017:19.9K
  STAPLES       00105288                    2017:8.7K
  STILLWATER MILLING COMP                   2017:16.6K
  TFS FISHERSCI ECOM HUS                    2017:14.5K
  THOMSON WEST TCD                          2017:27.6K
  VWR INTERNATIONAL INC                     2017:10.2K
  WAL-MART #0137                            2017:3.5K
  WAL-MART #4241                            2017:7.6K
  WM SUPERCENTER #137                       2017:4.2K
  WM SUPERCENTER #4241                      2017:7.4K
  WW GRAINGER                               2017:83.5K
  XEROX CORPORATION/RBO                     2017:17.5K

## what

AGENCYNBR:  01000 82%,  04000 5%,  09000 4%,  02500 4%,  13100 3%,  04900 1%,  04700 1%,  06500 0%,  09200 0%,  06000 0%,  03000 0%,  03900 0%

AGENCYNAME: OKLAHOMA STATE UNIVERSITY 82%, DEPT OF AGRICULTURE FOOD & FOR 5%, OFFICE OF MANAGEMENT AND ENTER 4%, OKLAHOMA MILITARY DEPARTMENT 4%, DEPARTMENT OF CORRECTIONS 3%, ATTORNEY GENERAL 1%, INDIGENT DEFENSE SYSTEM 1%, STATE BANKING DEPARTMENT 0%, TOBACCO SETTLEMENT ENDMT TRUST 0%, OK DEP AEROSPACE & AERONAUTICS 0%, ALCOHOLIC BEV. LAWS ENFORCE. 0%, BOLL WEEVIL ERADICATION ORG. 0%

FIRST_INITIAL: A 15%, J 14%, D 10%, M 10%, L 9%, K 9%, S 8%, C 7%, R 6%, T 4%, P 4%, B 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CALENDAR_YEAR | other | 1 | 0 | 2017 10.0K |
| CALENDAR_MONTH | other | 1 | 0 | 07 10.0K |
| AGENCYNBR | category | 19 | 0 |  01000 8.1K;  04000 451;  09000 406;  02500 396 |
| AGENCYNAME | category | 19 | 0 | OKLAHOMA STATE UNIVERSITY 8.1K; DEPT OF AGRICULTURE FOOD  451; OFFICE OF MANAGEMENT AND  406; OKLAHOMA MILITARY DEPARTM 396 |
| LAST_NAME | who | 1.2K | 0 | Brown 825; Dugan 289; Robinson 97; Bolser 91 |
| FIRST_INITIAL | category | 26 | 0 | A 1.4K; J 1.3K; D 895; M 842 |
| ITEM_DESCR | who | 2.5K | 1 | GENERAL PURCHASE 5.4K; AIR TRAVEL 1.0K; ROOM CHARGES 490; DESCRIPTION EACH 49 |
| AMOUNT | amount | 6.7K | 0 | 9.00000000000000000000000 310; 25.0000000000000000000000 159; 59.0000000000000000000000 92; 91.0000000000000000000000 79 |
| MERCHANT | who | 4.0K | 0 | AMAZON MKTPLACE PMTS 464; LOWES #00241 330; WW GRAINGER 196; Amazon.com 125 |
| TRANSACTION_DATE | date | 40 | 0 | 07-Jul-17 524; 25-Jul-17 518; 11-Jul-17 513; 21-Jul-17 509 |
| POST_DATE | date | 21 | 0 | 10-Jul-17 863; 24-Jul-17 826; 03-Jul-17 785; 31-Jul-17 778 |
| MCC_DESCRIPTION | who | 241 | 0 | GROCERY STORES  SUPERMARK 677; BOOK STORES 644; INDUSTRIAL SUPPLIES NOT E 513; AIRLINES  AIR CARRIERS 497 |
| ROWID | id | 9.9K | 0 | AAAJGhAAEAAEN9XAAR 50; AAAJGhAAEAAEN9XAAQ 50; AAAJGhAAEAAEN9XAAP 50; AAAJGhAAEAAEN9XAAO 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:46:40.33226 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | cafb83d6-6211-4dc9-a3bf-d 10.0K |
| SRC_SHA256 | who | 1 | 0 | f090a837ba73a13ad9f2eadc4 10.0K |
