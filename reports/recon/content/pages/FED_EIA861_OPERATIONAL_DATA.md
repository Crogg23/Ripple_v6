# FED_EIA861_OPERATIONAL_DATA

rows 1.7K  columns 35  scan 5.5s

roles: amount 25, audit 2, category 4, date 1, state 1, who 3

## when

_INGESTED_AT
  2026      1.7K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MEGAWATTS | 1.7K | 0 | 92.10 | 10.5K | 31.1K | 1.10M |
| UNNAMED_7 | 1.7K | 0 | 87.90 | 9.1K | 34.6K | 971.0K |
| UNNAMED_8 | 1.7K | -3.3K | 0 | 32.46M | 207.92M | 2.56B |
| UNNAMED_9 | 1.7K | 0 | 480.2K | 37.81M | 254.95M | 4.42B |
| POWER_EXCHANGED | 1.7K | 0 | 0 | 1.89M | 29.04M | 168.39M |
| UNNAMED_11 | 1.7K | 0 | 0 | 1.24M | 28.07M | 128.10M |

## who

UNNAMED_2 by rows
         3  Withheld
         1  City of College Park - (GA)
         1  Appalachian Power Co
         1  City of Alexandria - (MN)
         1  Blue Ridge Electric Coop Inc - (SC)
         1  Basin Electric Power Coop
         1  Athens Utility Board
         1  Town of Apex- (NC)
         1  C & L Electric Coop Corp
         1  Boone Electric Coop
         1  Altamaha Electric Member Corp
         1  City of Carthage - (MO)
         1  Clark Energy Coop Inc - (KY)
         1  City of Boscobel - (WI)
         1  PUD No 1 of Benton County
         1  Algoma Utility Comm
         1  Central Missouri Elec Coop Inc
         1  City of Ames - (IA)
         1  BP Energy Company
         1  Amicalola Electric Member Corp

UNNAMED_2 by dollars
       31.1K        1 rows  Tennessee Valley Authority
       30.5K        1 rows  Oncor Electric Delivery Company LLC
       28.3K        1 rows  Florida Power & Light Co
       23.8K        1 rows  Southern California Edison Co
       21.6K        1 rows  Commonwealth Edison Co
       19.0K        1 rows  Pacific Gas & Electric Co.
       18.4K        1 rows  Virginia Electric & Power Co
       18.3K        1 rows  Duke Energy Carolinas, LLC
       16.6K        1 rows  Georgia Power Co
       13.3K        1 rows  Alabama Power Co
       12.9K        1 rows  American Transmission Co
       12.8K        1 rows  Duke Energy Progress - (NC)
       11.9K        1 rows  Consolidated Edison Co-NY Inc
       11.6K        1 rows  American Transmission Systems Inc
       11.0K        1 rows  PacifiCorp
       10.8K        1 rows  International Transmission Company
       10.7K        1 rows  DTE Electric Company
       10.4K        1 rows  FirstEnergy Pennsylvania Electric Co
       10.3K        1 rows  Entergy Louisiana LLC
       10.3K        1 rows  Oglethorpe Power Corporation

UNNAMED_1 by rows
         3  88888
         1  2442
         1  1591
         1  213
         1  2008
         1  1764
         1  1613
         1  689
         1  2985
         1  2678
         1  994
         1  3208
         1  4294
         1  2248
         1  1889
         1  298
         1  3758
         1  1015
         1  307
         1  471

UNNAMED_1 by dollars
       31.1K        1 rows  18642
       30.5K        1 rows  44372
       28.3K        1 rows  6452
       23.8K        1 rows  17609
       21.6K        1 rows  4110
       19.0K        1 rows  14328
       18.4K        1 rows  19876
       18.3K        1 rows  5416
       16.6K        1 rows  7140
       13.3K        1 rows  195
       12.9K        1 rows  659
       12.8K        1 rows  3046
       11.9K        1 rows  4226
       11.6K        1 rows  56162
       11.0K        1 rows  14354
       10.8K        1 rows  56068
       10.7K        1 rows  5109
       10.4K        1 rows  66101
       10.3K        1 rows  11241
       10.3K        1 rows  13994

_SRC_FILE by rows
      1.7K  Operational_Data_2024.xlsx

_SRC_FILE by dollars
       1.10M     1.7K rows  Operational_Data_2024.xlsx

## who x when

UNNAMED_2 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = MEGAWATTS
  Alabama Power Co                          2026:13.3K
  Algoma Utility Comm                       2026:7.20
  Altamaha Electric Member Corp             2026:128.10
  Amicalola Electric Member Corp            2026:212.90
  Appalachian Power Co                      2026:5.5K
  Athens Utility Board                      2026:115.30
  BP Energy Company                         2026:0
  Basin Electric Power Coop                 2026:4.8K
  Blue Ridge Electric Coop Inc - (SC)       2026:310
  Boone Electric Coop                       2026:148.70
  C & L Electric Coop Corp                  2026:104.20
  Central Missouri Elec Coop Inc            2026:68.50
  City of Alexandria - (MN)                 2026:56.80
  City of Ames - (IA)                       2026:112.80
  City of Boscobel - (WI)                   2026:10
  City of Carthage - (MO)                   2026:65
  City of College Park - (GA)               2026:84.90
  Clark Energy Coop Inc - (KY)              2026:96
  Commonwealth Edison Co                    2026:21.6K
  Duke Energy Carolinas, LLC                2026:18.3K
  Florida Power & Light Co                  2026:28.3K
  Georgia Power Co                          2026:16.6K
  Oncor Electric Delivery Company LLC       2026:30.5K
  PUD No 1 of Benton County                 2026:437.60
  Pacific Gas & Electric Co.                2026:19.0K
  Southern California Edison Co             2026:23.8K
  Tennessee Valley Authority                2026:31.1K
  Town of Apex- (NC)                        2026:125.30
  Virginia Electric & Power Co              2026:18.4K
  Withheld                                  2026:0

UNNAMED_1 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = MEGAWATTS
  1015                                      2026:3.1K
  14328                                     2026:19.0K
  1591                                      2026:71.80
  1613                                      2026:893.50
  17609                                     2026:23.8K
  1764                                      2026:9.70
  18642                                     2026:31.1K
  1889                                      2026:196
  195                                       2026:13.3K
  19876                                     2026:18.4K
  2008                                      2026:52
  213                                       2026:68
  2248                                      2026:87.20
  2442                                      2026:386.60
  2678                                      2026:104.20
  298                                       2026:159
  2985                                      2026:89.10
  307                                       2026:7.20
  3208                                      2026:26.20
  3758                                      2026:207.60
  4110                                      2026:21.6K
  4294                                      2026:122.90
  44372                                     2026:30.5K
  471                                       2026:12.80
  5416                                      2026:18.3K
  6452                                      2026:28.3K
  689                                       2026:534.20
  7140                                      2026:16.6K
  88888                                     2026:0
  994                                       2026:57

## where

UNNAMED_3: TX 208, CA 85, TN 82, NY 76, WI 70, NC 65, GA 62, OH 57, MN 52, MO 51, AL 47, IN 46

## what

UNNAMED_0: 2024 100%, Data Year 0%

UNNAMED_4: Cooperative 35%, Municipal 27%, Retail Power Marketer 15%, Investor Owned 10%, Political Subdivision 5%, Wholesale Power Marketer 2%, Transmission 2%, Community Choice Aggregator 2%, State 1%, Municipal Mktg Authority 1%, Behind the Meter 1%, Federal 0%

UNNAMED_5: SERC 32%, WECC 16%, RFC 15%, MRO 11%, SPP 7%, TRE 6%, NPCC 6%, MISO 4%, FRCC 2%, AK 1%, ERCOT 0%, HI 0%

UNNAMED_31: O 100%, Data Type
O = Observed
I = Imp 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | category | 2 | 0 | 2024 1.7K; Data Year 1 |
| UNNAMED_1 | who | 1.7K | 0 | 88888 11; 67251 9; 67122 9; 67113 9 |
| UNNAMED_2 | who | 1.7K | 0 | Withheld 11; GridLiance Heartland LLC 9; Selfserve Energy Corp. 9; Morongo Transmission LLC 9 |
| UNNAMED_3 | state | 53 | 1 | TX 208; CA 85; TN 82; NY 76 |
| UNNAMED_4 | category | 13 | 0 | Cooperative 602; Municipal 458; Retail Power Marketer 257; Investor Owned 163 |
| UNNAMED_5 | category | 19 | 325 | SERC 441; WECC 217; RFC 206; MRO 154 |
| MEGAWATTS | amount | 1.2K | 0 | . 262; 28.9 8; 25.5 8; 86.7 8 |
| UNNAMED_7 | amount | 1.2K | 0 | . 262; 36.6 9; 8.1 9; 41 9 |
| UNNAMED_8 | amount | 455 | 0 | . 984; 0 275; 96423 3; 20706 3 |
| UNNAMED_9 | amount | 1.6K | 0 | . 82; 0 13; 3167844 9; 2385999 9 |
| POWER_EXCHANGED | amount | 91 | 0 | . 1.3K; 0 310; 157395 1; 242 1 |
| UNNAMED_11 | amount | 79 | 0 | . 1.5K; 0 157; 223 1; 2476 1 |
| UNNAMED_12 | amount | 89 | 0 | 0 1.5K; . 81; 157395 1; 19 1 |
| WHEELED_POWER | amount | 114 | 0 | . 1.3K; 0 294; 15929 1; 25719705 1 |
| UNNAMED_14 | amount | 113 | 0 | . 1.3K; 0 294; 15929 1; 25719705 1 |
| UNNAMED_15 | amount | 43 | 0 | 0 1.6K; . 81; 23992 1; 177 1 |
| UNNAMED_16 | amount | 70 | 0 | . 1.4K; 0 293; -567619 2; -19 1 |
| UNNAMED_17 | amount | 1.7K | 0 | . 31; 0 10; 3167844 9; 2385999 9 |
| MEGAWATTHOURS | amount | 1.5K | 0 | . 181; 0 13; 78014 9; 3167844 8 |
| UNNAMED_19 | amount | 464 | 0 | . 984; 0 268; 426371 3; 5766674 3 |
| UNNAMED_20 | amount | 197 | 0 | . 1.2K; 0 314; 8713 1; 14238 1 |
| UNNAMED_21 | amount | 596 | 0 | . 907; 0 147; 595 5; 207 5 |
| UNNAMED_22 | amount | 1.3K | 0 | . 362; 0 39; 8294 7; 7611 7 |
| UNNAMED_23 | amount | 1.7K | 0 | . 33; 3167844 9; 2385999 9; 221996 9 |
| THOUSANDS_DOLLARS | amount | 1.5K | 0 | . 185; 0 10; 135342 8; 100686 8 |
| UNNAMED_25 | amount | 77 | 0 | . 1.5K; 0 117; 652749.5 1; 2362.4 1 |
| UNNAMED_26 | amount | 459 | 0 | . 976; 0 277; 16884.3 3; 225632 3 |
| UNNAMED_27 | amount | 146 | 0 | . 1.3K; 0 313; -8243 1; -30571 1 |
| UNNAMED_28 | amount | 300 | 0 | . 1.1K; 0 305; 5521.9 2; 49057.7 2 |
| UNNAMED_29 | amount | 1.1K | 0 | . 563; 0 69; 1282.3 6; 75388.3 6 |
| UNNAMED_30 | amount | 1.7K | 0 | 135342 9; 92443 9; 9260 9; 5521.9 9 |
| UNNAMED_31 | category | 2 | 0 | O 1.7K; Data Type
O = Observed
I  1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:39:33.07911 1.7K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 119a36bb-f5cc-4045-a9b2-e 1.7K |
| _SRC_FILE | who | 1 | 0 | Operational_Data_2024.xls 1.7K |
