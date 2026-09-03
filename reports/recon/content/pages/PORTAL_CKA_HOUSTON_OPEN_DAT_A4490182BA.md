# PORTAL_CKA_HOUSTON_OPEN_DAT_A4490182BA

rows 10.0K  columns 48  scan 5.9s

roles: amount 6, audit 2, category 15, date 5, id 3, other 8, who 10

## when

SR_CREATE_DATE
  2012     10.0K  ##############################

DUE_DATE
  2012     10.0K  ##############################

DATE_CLOSED
  2012     10.0K  ##############################
  2013        15  
  2014         3  
  2015         1  
  2016         1  

EXPORTDATE
  2016     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SLA | 10.0K | 0.04 | 2 | 3.00 | 3 | 16.7K |
| OVERDUE | 10.0K | -3 | -1.75 | 12.77 | 1.5K | 4.3K |
| X_COORD | 9.8K | 3.01M | 3.12M | 3.18M | 3.21M | 30.42B |
| Y_COORD | 9.8K | 13.76M | 13.84M | 13.94M | 13.96M | 135.03B |
| LATITUDE | 9.8K | 0 | 29.74 | 30.03 | 30.09 | 290.3K |
| LONGITUDE | 9.8K | -95.70 | -95.36 | -95.16 | 0 | -930.7K |

## who

STREET_NAME by rows
       102  EVELLA
        39  HOLCOMBE
        35  LITTLE YORK
        31  MAIN
        26  SAM HOUSTON
        25  GESSNER
        25  BELLFORT
        23  BISSONNET
        23  WOOLWORTH
        22  KIRKWOOD
        22  BROADWAY
        22  FUQUA
        21  PARKER
        20  POST OAK
        20  FONDREN
        19  ALMEDA GENOA
        19  GALESBURG
        18  WAYSIDE
        18  GULF
        18  BEECHNUT

STREET_NAME by dollars
       91.96      102 rows  EVELLA
       58.48       35 rows  LITTLE YORK
       46.64       31 rows  MAIN
       41.20       23 rows  WOOLWORTH
          39       39 rows  HOLCOMBE
       35.32       21 rows  PARKER
       35.04       19 rows  GALESBURG
       34.56       26 rows  SAM HOUSTON
       34.28       22 rows  FUQUA
       34.16       16 rows  WESTHEIMER
       33.32       22 rows  KIRKWOOD
       32.36       22 rows  BROADWAY
       32.28       23 rows  BISSONNET
          31       15 rows  FLINTRIDGE
       30.16       18 rows  LYNDHURST
       30.16       18 rows  CAROLWOOD
          30       14 rows  CHAPMAN
          30       15 rows  BELMARK
       29.36       20 rows  FONDREN
       29.12       15 rows  JENSEN

TIME_CLOSED by rows
        60  15:30:00
        48  15:31:00
        46  15:33:00
        43  15:32:00
        41  15:43:00
        40  15:29:00
        39  15:34:00
        35  15:28:00
        31  15:51:00
        28  15:42:00
        27  15:58:00
        27  15:52:00
        27  15:35:00
        26  07:08:00
        26  15:41:00
        25  16:00:00
        25  15:49:00
        24  07:11:00
        24  17:04:00
        23  17:03:00

TIME_CLOSED by dollars
      110.32       60 rows  15:30:00
       98.16       48 rows  15:31:00
       93.04       43 rows  15:32:00
       82.48       46 rows  15:33:00
       80.08       41 rows  15:43:00
       75.12       40 rows  15:29:00
       72.20       39 rows  15:34:00
       66.16       35 rows  15:28:00
          59       28 rows  15:42:00
       58.12       31 rows  15:51:00
          57       26 rows  07:08:00
          55       27 rows  15:35:00
       51.20       27 rows  15:52:00
          51       24 rows  17:04:00
       48.24       27 rows  15:58:00
       48.16       26 rows  15:41:00
       48.12       25 rows  16:00:00
       48.08       24 rows  07:11:00
       47.16       25 rows  15:49:00
       47.08       22 rows  17:02:00

DUE_TIME by rows
        50  12:00:00
        35  13:28:00
        32  10:17:00
        31  11:10:00
        31  09:41:00
        30  10:57:00
        29  13:30:00
        28  10:49:00
        27  10:11:00
        27  10:38:00
        27  11:20:00
        27  10:10:00
        27  11:05:00
        27  10:28:00
        27  11:36:00
        27  09:18:00
        27  10:20:00
        26  09:29:00
        26  10:15:00
        26  15:03:00

DUE_TIME by dollars
       60.24       31 rows  11:10:00
       60.08       31 rows  09:41:00
       57.44       35 rows  13:28:00
       57.28       32 rows  10:17:00
       56.36       50 rows  12:00:00
       56.08       29 rows  13:30:00
       55.08       30 rows  10:57:00
       53.04       24 rows  08:45:00
       51.24       26 rows  10:45:00
       51.20       27 rows  09:18:00
       51.20       27 rows  11:36:00
       50.24       27 rows  10:28:00
       50.20       27 rows  10:20:00
       50.08       23 rows  09:46:00
       49.32       25 rows  11:06:00
          49       23 rows  09:10:00
       48.40       28 rows  10:49:00
       48.20       24 rows  09:39:00
       48.16       26 rows  09:29:00
       48.12       26 rows  10:15:00

SR_CREATE_TIME by rows
        49  12:00:00
        37  09:41:00
        33  10:17:00
        32  10:57:00
        31  13:30:00
        31  10:25:00
        31  13:28:00
        30  09:33:00
        29  11:10:00
        29  09:20:00
        29  08:45:00
        29  11:13:00
        28  10:28:00
        28  09:29:00
        28  11:01:00
        28  10:20:00
        27  11:25:00
        27  10:49:00
        27  10:45:00
        27  15:07:00

SR_CREATE_TIME by dollars
       60.44       37 rows  09:41:00
       60.12       29 rows  11:10:00
       57.36       33 rows  10:17:00
       57.16       31 rows  13:28:00
       56.32       49 rows  12:00:00
       56.20       31 rows  13:30:00
       55.24       32 rows  10:57:00
       53.36       29 rows  08:45:00
       51.28       27 rows  10:45:00
       51.16       25 rows  09:18:00
       51.16       26 rows  11:36:00
       50.40       28 rows  10:28:00
       50.28       28 rows  10:20:00
       50.20       26 rows  09:46:00
       49.20       24 rows  11:06:00
       49.20       26 rows  09:10:00
       48.36       27 rows  10:49:00
       48.32       28 rows  09:29:00
       48.16       26 rows  10:15:00
       48.16       23 rows  09:39:00

## who x when

STREET_NAME by DATE_CLOSED, dollars = SLA
  ALMEDA GENOA                              2012:26.24
  BEECHNUT                                  2012:25.44
  BELLFORT                                  2012:21.80
  BELMARK                                   2012:30
  BISSONNET                                 2012:31.28 2013:1
  BROADWAY                                  2012:32.36
  CAROLWOOD                                 2012:30.16
  CHAPMAN                                   2012:30
  EVELLA                                    2012:91.96
  FLINTRIDGE                                2012:31
  FONDREN                                   2012:29.36
  FUQUA                                     2012:34.28
  GALESBURG                                 2012:35.04
  GESSNER                                   2012:28.64
  GULF                                      2012:23.32
  HOLCOMBE                                  2012:39
  JENSEN                                    2012:29.12
  KIRKWOOD                                  2012:33.32
  LITTLE YORK                               2012:58.48
  LYNDHURST                                 2012:30.16
  MAIN                                      2012:46.64
  PARKER                                    2012:35.32
  POST OAK                                  2012:23.48
  SAM HOUSTON                               2012:34.56
  WAYSIDE                                   2012:26.20
  WESTHEIMER                                2012:34.16
  WOOLWORTH                                 2012:41.20

TIME_CLOSED by DATE_CLOSED, dollars = SLA
  07:08:00                                  2012:57
  07:11:00                                  2012:48.08
  15:28:00                                  2012:66.16
  15:29:00                                  2012:75.12
  15:30:00                                  2012:110.32
  15:31:00                                  2012:98.16
  15:32:00                                  2012:93.04
  15:33:00                                  2012:82.48
  15:34:00                                  2012:72.20
  15:35:00                                  2012:55
  15:41:00                                  2012:48.16
  15:42:00                                  2012:59
  15:43:00                                  2012:80.08
  15:49:00                                  2012:47.16
  15:51:00                                  2012:58.12
  15:52:00                                  2012:51.20
  15:58:00                                  2012:48.24
  16:00:00                                  2012:48.12
  17:02:00                                  2012:47.08
  17:03:00                                  2012:42.24
  17:04:00                                  2012:51

## what

MIN_ACTIVITY_SEQ: 1 100%, 2 0%, 3 0%, 4 0%, 10 0%, 15 0%

MAX_ACTIVITY_SEQ: 1 89%, 2 7%, 3 2%, 4 1%, 5 0%, 6 0%, 10 0%, 7 0%, 11 0%, 9 0%, 8 0%, 13 0%

COUNT_SEQ: 1 89%, 2 7%, 3 2%, 4 1%, 5 0%, 6 0%, 7 0%, 10 0%, 11 0%, 9 0%, 8 0%, 13 0%

COUNTY: HARRIS 95%, NULL 5%, FORT BEND 0%

DISTRICT: B 19%, D 15%, H 14%, I 12%, K 10%, A 6%, F 6%, E 5%, C 5%, J 4%, NULL 2%, G 2%

TRASH_QUAD: NE 26%, SE 26%, NULL 20%, SW 14%, NW 14%

RECYCLE_QUAD: SW 41%, NULL 31%, NW 28%

TRASH_DAY: FRIDAY 27%, NULL 20%, TUESDAY 20%, MONDAY 19%, THURSDAY 15%

HEAVY_TRASH_DAY: NULL 29%, 4th Thursday 7%, 2nd Monday 7%, 1st Tuesday 7%, 4th Tuesday 6%, 1st Friday 6%, 4th Wednesday 6%, 1st Thursday 6%, 2nd Tuesday 6%, 4th Monday 6%, 3rd Friday 6%, 2nd Friday 6%

RECYCLE_DAY: NULL 31%, Friday-b 13%, Monday-a 11%, Tuesday-a 11%, Friday-a 9%, Thursday-a 8%, Monday-b 6%, Thursday-b 5%, Tuesday-b 4%, non active 3%, Tuesday-A 0%

MANAGEMENT_DISTRICT: Greater Northside MD 26%, HCID #10-A 11%, East End MD 11%, Five Corners HCID #10B 11%, HCID #9 7%, Spring Branch MD 7%, International MD 7%, Sharpstown MD 6%, NULL 5%, Greater Southeast MD 5%, Near Northwest MD 4%

SR_TYPE: Stray Animal 60%, Animal Control Violation 30%, Animal Control Assist Officer 6%, Transport Animal 3%, Wild Animal 1%, Other BARC Case 0%

STATUS: CANCELLED 65%, COMPLETED 35%

CITY: HOUSTON 99%, KINGWOOD 0%, HUMBLE 0%, NULL 0%, MISSOURI CITY 0%, WEBSTER 0%, HUFFMAN 0%, MISSOURI 0%, PASADENA 0%, HOUSTN 0%, HOOUSTON 0%, HOUTON 0%

STATE: TX 100%, NULL 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ANIMAL_PUBLIC_BARC_DATA_KEY | id | 10.2K | 0 | 24897 50; 24896 50; 24895 50; 24894 50 |
| UNIQUE_ACTIVITY_NO | id | 10.0K | 0 | A12-578736 50; A12-578735 50; A12-578734 50; A12-578733 50 |
| MIN_ACTIVITY_SEQ | category | 6 | 0 | 1 10.0K; 2 8; 3 3; 4 2 |
| MAX_ACTIVITY_SEQ | category | 16 | 0 | 1 8.9K; 2 735; 3 179; 4 83 |
| COUNT_SEQ | category | 15 | 0 | 1 8.9K; 2 728; 3 176; 4 82 |
| CASE_NUMBER | id | 10.0K | 0 | A12-578736 50; A12-578735 50; A12-578734 50; A12-578733 50 |
| SR_LOCATION | other | 8.4K | 0 | 2700 EVELLA ST, HOUSTON T 53; 14400 POLO ST, HOUSTON TX 53; 8200 FLINTRIDGE DR, HOUST 51; 10106 BRETTON DR, HOUSTON 51 |
| COUNTY | category | 4 | 1 | HARRIS 9.5K; NULL 521; FORT BEND 2 |
| DISTRICT | category | 13 | 66 | B 1.9K; D 1.5K; H 1.4K; I 1.1K |
| NEIGHBORHOOD | who | 91 | 74 | CENTRAL SOUTHWEST 502; ALIEF 437; NORTHSIDE/NORTHLINE 400; GOLFCREST / BELLFORT / RE 319 |
| TAX_ID | other | 7.3K | 1 | NULL 521; 422010000210 98; 920930000017 50; 760870100170 49 |
| TRASH_QUAD | category | 6 | 62 | NE 2.6K; SE 2.5K; NULL 2.0K; SW 1.4K |
| RECYCLE_QUAD | category | 4 | 3.5K | SW 2.7K; NULL 2.0K; NW 1.8K |
| TRASH_DAY | category | 6 | 62 | FRIDAY 2.6K; NULL 2.0K; TUESDAY 2.0K; MONDAY 1.9K |
| HEAVY_TRASH_DAY | category | 22 | 62 | NULL 2.0K; 4th Thursday 499; 2nd Monday 472; 1st Tuesday 454 |
| RECYCLE_DAY | category | 14 | 3.5K | NULL 2.0K; Friday-b 871; Monday-a 722; Tuesday-a 696 |
| KEY_MAP | other | 1.1K | 1 | 494A       124; 415W       62; 534W       62; 414Z       55 |
| MANAGEMENT_DISTRICT | category | 31 | 5.2K | Greater Northside MD 1.2K; HCID #10-A 495; East End MD 470; Five Corners HCID #10B 465 |
| DEPARTMENT | who | 1 | 0 | BARC Animal Rescue & Cont 10.0K |
| DIVISION | who | 1 | 0 | BARC Animal Rescue & Cont 10.0K |
| SR_TYPE | category | 6 | 0 | Stray Animal 6.0K; Animal Control Violation 3.0K; Animal Control Assist Off 573; Transport Animal 344 |
| QUEUE | other | 1 | 0 | NULL 10.0K |
| SLA | amount | 5 | 0 | 2 5.7K; 3 1.3K; 1 1.2K; 0.0833 1.1K |
| STATUS | category | 2 | 0 | CANCELLED 6.5K; COMPLETED 3.5K |
| SR_CREATE_DATE | date | 173 | 0 | 2012-04-17 00:00:00 154; 2012-03-28 00:00:00 142; 2012-02-22 00:00:00 137; 2012-03-12 00:00:00 134 |
| SR_CREATE_TIME | who | 757 | 0 | 10:17:00 52; 09:10:00 52; 13:30:00 52; 12:00:00 52 |
| DUE_DATE | date | 246 | 0 | 2012-03-30 00:00:00 122; 2012-04-26 00:00:00 117; 2012-03-15 00:00:00 115; 2012-03-14 00:00:00 111 |
| DUE_TIME | who | 802 | 0 | 12:00:00 53; 11:10:00 52; 14:17:00 52; 13:30:00 52 |
| DATE_CLOSED | date | 264 | 0 | 2012-04-17 00:00:00 161; 2012-04-24 00:00:00 135; 2012-04-04 00:00:00 131; 2012-02-29 00:00:00 126 |
| TIME_CLOSED | who | 4.8K | 0 | 15:30:00 61; 15:33:00 54; 14:16:00 53; 15:48:00 53 |
| OVERDUE | amount | 367 | 0 | -1.958333 849; -1.916666 652; -2 614; -1.833333 484 |
| TITLE | who | 110 | 0 | STRAY DOMESTIC ANIMAL / A 1.9K; INVESTIGATION / CITY ORDI 1.5K; STRAY DOMESTIC ANIMAL / U 791; STRAY DOMESTIC ANIMAL / U 706 |
| X_COORD | amount | 7.6K | 0 | NULL 242; 3128057.98290956 98; 3089533.19808266 51; 3148734.41695032 50 |
| Y_COORD | amount | 7.6K | 0 | NULL 242; 13853206.2579961 98; 13789416.4259304 51; 13869995.1118855 50 |
| LATITUDE | amount | 7.4K | 0 | NULL 241; 29.79079299 98; 29.61870469 51; 29.83514516 50 |
| LONGITUDE | amount | 7.7K | 0 | NULL 241; -95.34361352 98; -95.47108461 51; -95.27677421 50 |
| CHANNEL_TYPE | who | 1 | 0 | Unknown 10.0K |
| STREET_NUM | other | 4.2K | 0 | 2700 111; 2250 57; 14400 52; 8200 51 |
| STREET_NAME | who | 3.8K | 0 | EVELLA 103; PARKER 54; CORPORATE 53; POLO 52 |
| CITY | category | 29 | 0 | HOUSTON 9.8K; KINGWOOD 41; HUMBLE 30; NULL 24 |
| STATE | category | 2 | 0 | TX 10.0K; NULL 11 |
| ZIPCODE | other | 118 | 0 | 77016 388; 77033 360; 77026 348; 77009 313 |
| ADDRESS | other | 7.9K | 0 | 2700 EVELLA 101; 14400 POLO 52; 8200 FLINTRIDGE 51; 9004 LANEWOOD 51 |
| IS_GEOCODED | other | 1 | 0 | Y 10.0K |
| EXPORTDATE | date | 1 | 0 | 2016-10-17 00:00:00 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:51:38.58187 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 26c655e3-c190-466f-a444-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | a99dc61d865f0b68f99dbe1ef 10.0K |
