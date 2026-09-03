# PORTAL_CKA_OKLAHOMA_OPEN_DA_E1AA111C19

rows 10.0K  columns 16  scan 4.4s

roles: amount 1, audit 2, category 3, date 3, id 1, other 2, who 5

## when

TRANSACTION_DATE
  2025     10.0K  ##############################

POST_DATE
  2025     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -13.5K | 110 | 4.4K | 52.0K | 3.80M |

## who

LAST_NAME by rows
       404  Schmitt
       342  McCoy
       199  Caselman
       119  Brown
        97  Hughes
        88  Moore
        87  Johnson
        83  Risenhoover
        78  Price
        76  Turner
        73  Jones
        55  Shirzad
        53  Mays
        51  Bailey
        51  Paulus
        49  Presley
        47  Blakley
        47  Harris
        46  Anderson
        42  Schmidt

LAST_NAME by dollars
      122.7K       88 rows  Moore
      108.7K      404 rows  Schmitt
      106.9K      199 rows  Caselman
      100.5K      342 rows  McCoy
       97.0K       87 rows  Johnson
       89.9K       78 rows  Price
       56.5K       51 rows  Paulus
       52.8K       31 rows  PARRIS
       39.8K       13 rows  Gunn
       37.8K       49 rows  Presley
       36.2K       73 rows  Jones
       30.3K       34 rows  Rouser
       30.1K       15 rows  Hudspeth
       30.1K       18 rows  Avila
       29.5K       16 rows  Hatfield
       26.8K       13 rows  Broiles
       26.5K      119 rows  Brown
       25.3K       76 rows  Turner
       24.5K       23 rows  Nazario
       23.9K       31 rows  Conaughty

MERCHANT by rows
       226  LOWES #00241
       110  WM SUPERCENTER #4241
        84  WM SUPERCENTER #137
        80  WAL-MART #4241
        76  WorkQuest-Oklahoma
        73  GRAINGER
        62  STILLWATER MILLING COMP
        61  WAL-MART #0137
        61  NAPA AUTO PARTS 0000415
        57  IN  DEARINGER PRINTING &
        53  AMAZON MKTPLACE PMTS
        52  WALMART.COM
        48  WALMART.COM 8009256278
        47  ATWOOD 05 STILLWATER
        45  UBER    TRIP
        42  MCMASTER-CARR
        41  INTEGRATED DNA TECH
        40  O REILLY 5392
        40  STILLWATER WINNELSON C
        37  TFS FISHERSCI ECOM HUS

MERCHANT by dollars
       74.9K       26 rows  SYSCO CORP
       63.5K        3 rows  ESRI
       49.6K       76 rows  WorkQuest-Oklahoma
       40.8K        5 rows  DANA SAFETY SUPPLY
       36.2K        7 rows  WARREN CAT
       33.0K       73 rows  GRAINGER
       28.3K       33 rows  UPS BILLING CENTER
       25.8K       37 rows  TFS FISHERSCI ECOM HUS
       25.2K        7 rows  MSC
       23.5K      226 rows  LOWES #00241
       22.0K       24 rows  THE WEBSTAURANT STORE INC
       21.4K        7 rows  DOC AGRI SERVICES DIVISI
       21.2K       25 rows  ULINE   SHIP SUPPLIES
       19.6K        4 rows  STANDLEY SYSTEMS LLC
       17.9K        3 rows  IMLSS UTAH
       17.9K        7 rows  PROLIFIC_HW
       17.7K       10 rows  OK FILTER
       17.4K        4 rows  TREMENDOUS.COM
       17.3K        1 rows  SOUTHERN TIRE MART #602
       16.8K        1 rows  BIG TEX TRAILERS

ITEM_DESCR by rows
      4.3K  GENERAL PURCHASE
       680  AIR TRAVEL
       538  ROOM CHARGES
       325  Order Summary item
        64  CAR RENTAL
        61  Facebook Ads EAC
        50  Product EA
        41  Miscellaneous EA
        40  SPECIALIZED VEHICLES EA
        35  UBER RIDE EA
        31  ChatGPT Plus Subscription item
        28  25 nmole DNA Oligo 1|25 nmole DNA Oligo 1|25 nmole
        26  Groceries NMB
        20  ENERGY SERVICES EA
        19  Benefit Overpayment NMB
        19  wholesale janitorial & p EA
        18  INVOICE EACH
        16  GENERIC PRODUCT CCT
        16  Eureka Water Company EACH
        15  RUBBER TIRES OR TUBES PROD EA

ITEM_DESCR by dollars
       1.46M     4.3K rows  GENERAL PURCHASE
      232.5K      680 rows  AIR TRAVEL
      211.2K      538 rows  ROOM CHARGES
       80.2K       50 rows  Product EA
       74.9K       26 rows  Groceries NMB
       64.0K      325 rows  Order Summary item
       52.0K        1 rows  SUBSCRPUBLIC SFTYAGOLMB EA|SUBSCRPUBLIC SFTYAGOLCR
       23.0K       64 rows  CAR RENTAL
       17.4K        4 rows  Funds added EACH
       17.1K       16 rows  GENERIC PRODUCT CCT
       16.6K        1 rows  Misc L3 Item EA|Inv INV1801405:Contract 15 1|Inv I
       15.5K        1 rows  Legal services item
       14.8K        1 rows  115V 50D ICE&WATER DISPENS EA
       13.5K        1 rows  10-FT SS ICE CONNECTOR EA|Counter-Depth 32.2-cu ft
       11.7K       41 rows  Miscellaneous EA
       11.2K        1 rows  FY2025 - LEASE OPTION$1995 NMB
       10.4K       40 rows  SPECIALIZED VEHICLES EA
       10.1K        2 rows  COMPLETE KIT WITH ALL HARD NMB|EDUCATION DISCOUNT
       10.0K        1 rows  Oklahoma National Guard Fo item
        9.8K        1 rows  SAR8888F32D EA|SAR7138ETL26D RHR LA1B EA|BEA10TD90

MCC_DESCRIPTION by rows
      1.3K  BOOK STORES
       672  GROCERY STORES  SUPERMARKETS
       405  MISCELLANEOUS AND RETAIL STORES
       320  HOME SUPPLY WAREHOUSE STORES
       297  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
       282  AMERICAN AIRLINES
       241  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
       230  COMPUTER SOFTWARE STORES
       208  TRAVEL AGENCIES
       202  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
       187  VARIETY STORES
       182  EATING PLACES  RESTAURANTS
       174  HARDWARE STORES
       163  PLUMBING & HEATING EQUIPMENT AND SUPPLIE
       156  AUTOMOTIVE PARTS  ACCESSORIES STORES
       152  AIRLINES  AIR CARRIERS
       150  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       149  CHARITABLE AND SOCIAL SERVICE ORGANIZATI
       128  MISCELLANEOUS AUTOMOTIVE DEALERS
       127  MISCELLANEOUS PUBLISHING & PRINTING

MCC_DESCRIPTION by dollars
      203.4K     1.3K rows  BOOK STORES
      156.8K      241 rows  LAB/MEDICAL/DENTAL/OPHTHALMIC HOSPITAL E
      155.4K      297 rows  INDUSTRIAL SUPPLIES NOT ESLEWHERE CLASSI
      143.0K      405 rows  MISCELLANEOUS AND RETAIL STORES
      117.0K      282 rows  AMERICAN AIRLINES
      101.0K       97 rows  NON-DURABLE GOODS NOT ELSEWHERE CLASSIFI
       97.5K       41 rows  COMPUTERS COMPUTER PERIPHERAL EQUIPMENT 
       92.1K      150 rows  BUSINESS SERVICES NOT ELSEWHERE CLASSIFI
       87.8K      149 rows  CHARITABLE AND SOCIAL SERVICE ORGANIZATI
       81.4K      202 rows  GOVERNMENT SERVICES NOT ELSEWHERE CLASSI
       77.8K      127 rows  MEMBERSHIP ORGANIZATIONS NOT ELSEWHERE C
       76.5K       68 rows  DURABLE GOODS NOT ELSEWHERE CLASSIFIED
       75.2K      230 rows  COMPUTER SOFTWARE STORES
       74.7K       71 rows  COMMERCIAL EQUIPMENT  NOT ELSEWHERE CLAS
       72.5K      163 rows  PLUMBING & HEATING EQUIPMENT AND SUPPLIE
       71.7K       72 rows  SCHOOLS AND EDUCATIONAL SERVICES NOT ELS
       71.6K      103 rows  CATALOG MERCHANTS
       64.1K      127 rows  MISCELLANEOUS PUBLISHING & PRINTING
       61.2K       88 rows  PROFESSIONAL SERVICES NOT ELSEWHERE CLAS
       60.4K      156 rows  AUTOMOTIVE PARTS  ACCESSORIES STORES

## who x when

LAST_NAME by TRANSACTION_DATE, dollars = AMOUNT
  Anderson                                  2025:6.3K
  Avila                                     2025:30.1K
  Bailey                                    2025:18.0K
  Blakley                                   2025:18.0K
  Broiles                                   2025:26.8K
  Brown                                     2025:26.5K
  Caselman                                  2025:106.9K
  Conaughty                                 2025:23.9K
  Gunn                                      2025:39.8K
  Harris                                    2025:16.0K
  Hatfield                                  2025:29.5K
  Hudspeth                                  2025:30.1K
  Hughes                                    2025:10.6K
  Johnson                                   2025:97.0K
  Jones                                     2025:36.2K
  Mays                                      2025:22.1K
  McCoy                                     2025:100.5K
  Moore                                     2025:122.7K
  Nazario                                   2025:24.5K
  PARRIS                                    2025:52.8K
  Paulus                                    2025:56.5K
  Presley                                   2025:37.8K
  Price                                     2025:89.9K
  Risenhoover                               2025:12.2K
  Rouser                                    2025:30.3K
  Schmidt                                   2025:17.4K
  Schmitt                                   2025:108.7K
  Shirzad                                   2025:19.1K
  Turner                                    2025:25.3K

MERCHANT by TRANSACTION_DATE, dollars = AMOUNT
  AMAZON MKTPLACE PMTS                      2025:-3.3K
  ATWOOD 05 STILLWATER                      2025:6.5K
  DANA SAFETY SUPPLY                        2025:40.8K
  DOC AGRI SERVICES DIVISI                  2025:21.4K
  ESRI                                      2025:63.5K
  GRAINGER                                  2025:33.0K
  IN  DEARINGER PRINTING &                  2025:15.7K
  INTEGRATED DNA TECH                       2025:6.3K
  LOWES #00241                              2025:23.5K
  MCMASTER-CARR                             2025:15.3K
  MSC                                       2025:25.2K
  NAPA AUTO PARTS 0000415                   2025:7.6K
  O REILLY 5392                             2025:4.3K
  STANDLEY SYSTEMS LLC                      2025:19.6K
  STILLWATER MILLING COMP                   2025:10.5K
  STILLWATER WINNELSON C                    2025:9.7K
  SYSCO CORP                                2025:74.9K
  TFS FISHERSCI ECOM HUS                    2025:25.8K
  THE WEBSTAURANT STORE INC                 2025:22.0K
  UBER    TRIP                              2025:1.5K
  ULINE   SHIP SUPPLIES                     2025:21.2K
  UPS BILLING CENTER                        2025:28.3K
  WAL-MART #0137                            2025:6.8K
  WAL-MART #4241                            2025:6.0K
  WALMART.COM                               2025:7.6K
  WALMART.COM 8009256278                    2025:8.9K
  WARREN CAT                                2025:36.2K
  WM SUPERCENTER #137                       2025:8.3K
  WM SUPERCENTER #4241                      2025:7.6K
  WorkQuest-Oklahoma                        2025:49.6K

## what

AGENCYNBR: 1000 86%, 4000 5%, 2500 5%, 4900 2%, 4700 1%, 9000 0%, 6000 0%, 3000 0%, 6500 0%, 8500 0%, 3900 0%, 2000 0%

AGENCYNAME: OKLAHOMA STATE UNIVERSITY 86%, DEPT OF AGRICULTURE FOOD & FOR 5%, OKLAHOMA MILITARY DEPARTMENT 5%, ATTORNEY GENERAL 2%, INDIGENT DEFENSE SYSTEM 1%, OFFICE OF MANAGEMENT AND ENTER 0%, OK DEP AEROSPACE & AERONAUTICS 0%, ALCOHOLIC BEV. LAWS ENFORCE. 0%, STATE BANKING DEPARTMENT 0%, OKLAHOMA BROADBAND OFFICE 0%, BOLL WEEVIL ERADICATION ORG. 0%, OKLAHOMA ACCOUNTANCY BOARD 0%

FIRST_INITIAL: C 13%, A 12%, K 12%, J 12%, M 10%, S 7%, D 7%, T 6%, R 6%, L 5%, B 5%, E 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CALENDAR_YEAR | other | 1 | 0 | 2025 10.0K |
| CALENDAR_MONTH | other | 1 | 0 | 7 10.0K |
| AGENCYNBR | category | 15 | 0 | 1000 8.6K; 4000 499; 2500 468; 4900 197 |
| AGENCYNAME | category | 15 | 0 | OKLAHOMA STATE UNIVERSITY 8.6K; DEPT OF AGRICULTURE FOOD  499; OKLAHOMA MILITARY DEPARTM 468; ATTORNEY GENERAL 197 |
| LAST_NAME | who | 1.1K | 0 | Schmitt 404; McCoy 342; Caselman 199; Brown 119 |
| FIRST_INITIAL | category | 26 | 0 | C 1.2K; A 1.1K; K 1.1K; J 1.1K |
| ITEM_DESCR | who | 3.2K | 1 | GENERAL PURCHASE 4.3K; AIR TRAVEL 680; ROOM CHARGES 538; Order Summary item 325 |
| AMOUNT | amount | 6.6K | 0 | 25.0 153; 5.0 137; 110.0 124; 20.0 80 |
| MERCHANT | who | 5.2K | 0 | LOWES #00241 226; WorkQuest-Oklahoma 116; WM SUPERCENTER #4241 110; GRAINGER 105 |
| TRANSACTION_DATE | date | 43 | 0 | 2025-07-10T00:00:00 519; 2025-07-16T00:00:00 501; 2025-07-22T00:00:00 491; 2025-07-01T00:00:00 488 |
| POST_DATE | date | 23 | 0 | 2025-07-14T00:00:00 714; 2025-07-28T00:00:00 676; 2025-07-21T00:00:00 668; 2025-07-24T00:00:00 535 |
| MCC_DESCRIPTION | who | 243 | 0 | BOOK STORES 1.3K; GROCERY STORES  SUPERMARK 672; MISCELLANEOUS AND RETAIL  405; HOME SUPPLY WAREHOUSE STO 320 |
| ROWID | id | 10.0K | 0 | AAAJGhAANAANWsvAAG 50; AAAJGhAANAANWsvAAF 50; AAAJGhAANAANWsvAAE 50; AAAJGhAANAANWsvAAD 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:46:48.38748 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9ff0bc5e-dcc9-442b-bb0d-e 10.0K |
| SRC_SHA256 | who | 1 | 0 | 985d5ccece7e90a457b959c5c 10.0K |
