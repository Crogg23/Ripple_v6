# PORTAL_CKA_OPEN_DATA_SA_58B0401C9A

rows 10.0K  columns 24  scan 4.6s

roles: amount 3, audit 2, category 11, date 2, id 2, other 2, who 3

## when

INSTALLDATE
  1980      4.6K  ###########################
  1984         1  
  1998         1  
  2000      5.0K  ##############################
  2002         2  
  2003         4  
  2004         2  
  2005         8  
  2006         4  
  2007         5  
  2008         5  
  2010         2  
  2011         5  
  2012         8  
  2013         9  
  2014        11  
  2015         8  
  2016        15  
  2017        22  
  2018        22  
  2019        30  
  2020        49  
  2021        48  
  2022        49  
  2023        53  
  2024        14  
  2025        13  
  2026         1  

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LENGTHFEET | 10.0K | 7.10 | 376.65 | 3.1K | 13.5K | 5.72M |
| PAVEMENTWIDTH | 10.0K | 13 | 28.50 | 66 | 66.90 | 307.6K |
| SHAPE__LENGTH | 10.0K | 7.08 | 376.65 | 3.1K | 13.5K | 5.72M |

## who

MSAG_NAME by rows
        72  IH 10 W ACCESS RD
        55  IH 35 S ACCESS RD
        53  IH 35 N ACCESS RD
        39  NE LOOP 410 ACCESS RD
        36  US HWY 281 N ACCESS RD
        35  NW LOOP 410 ACCESS RD
        32  CULEBRA RD
        30  SW LOOP 410 ACCESS RD
        28  IH 10 W
        28  N LOOP 1604 E ACCESS RD
        27  US HWY 281 N
        25  N LOOP 1604 W ACCESS RD
        25  BLANCO RD
        23  HUEBNER RD
        23  IH 37 S ACCESS RD
        23  US HWY 90 W ACCESS RD
        22  W MILITARY DR
        22  IH 10 E
        22  BANDERA RD
        21  IH 10 E ACCESS RD

MSAG_NAME by dollars
       45.8K       17 rows  UNNAMED ST IN CAMP BULLIS
       45.1K       72 rows  IH 10 W ACCESS RD
       44.1K       28 rows  IH 10 W
       38.3K       55 rows  IH 35 S ACCESS RD
       28.7K       20 rows  SE LOOP 410 ACCESS RD
       28.3K       35 rows  NW LOOP 410 ACCESS RD
       27.5K       53 rows  IH 35 N ACCESS RD
       25.8K       32 rows  CULEBRA RD
       24.7K       28 rows  N LOOP 1604 E ACCESS RD
       24.4K       39 rows  NE LOOP 410 ACCESS RD
       23.4K       18 rows  US HWY 90 W
       23.3K       25 rows  N LOOP 1604 W ACCESS RD
       23.0K       36 rows  US HWY 281 N ACCESS RD
       22.8K       22 rows  IH 10 E
       22.3K       25 rows  BLANCO RD
       20.7K       30 rows  SW LOOP 410 ACCESS RD
       20.3K       21 rows  IH 10 E ACCESS RD
       17.5K       23 rows  IH 37 S ACCESS RD
       17.4K       11 rows  WURZBACH PKWY
       17.4K       19 rows  IH 35 S

TOSTREET by rows
       796  CUL-DE-SAC
       648  TBD
       130  Dead End
        60  BRIDGE
        30  US HWY 281 N ACCESS RD
        29  IH 10 W ACCESS RD
        27  IH 35 N ACCESS RD
        23  IH 35 S ACCESS RD
        21  US HWY 90 W ACCESS RD
        21  NW LOOP 410 ACCESS RD
        20  NE LOOP 410 ACCESS RD
        20  US HWY 281 N
        19  BLANCO RD
        19  SW LOOP 410 ACCESS RD
        18  PVT RD
        17  IH 10 W
        16  VANCE JACKSON
        15  RR CROSSING
        14  CITY LIMITS
        14  N LOOP 1604 W ACCESS RD

TOSTREET by dollars
      442.4K      648 rows  TBD
      391.2K      796 rows  CUL-DE-SAC
       61.2K      130 rows  Dead End
       34.4K       12 rows  UNNAMED ST IN CAMP BULLIS
       24.5K       60 rows  BRIDGE
       22.3K       17 rows  IH 10 W
       21.1K       14 rows  CITY LIMITS
       18.9K       23 rows  IH 35 S ACCESS RD
       17.8K       30 rows  US HWY 281 N ACCESS RD
       17.3K       12 rows  SOMERSET RD
       16.7K       12 rows  WURZBACH PKWY ACCESS RD
       15.6K       21 rows  NW LOOP 410 ACCESS RD
       15.3K       14 rows  N LOOP 1604 W ACCESS RD
       14.7K       21 rows  US HWY 90 W ACCESS RD
       14.1K       19 rows  BLANCO RD
       13.6K       12 rows  IH 10 E ACCESS RD
       13.5K        1 rows  STRAUS MEDINA
       13.4K       20 rows  NE LOOP 410 ACCESS RD
       13.2K       27 rows  IH 35 N ACCESS RD
       13.0K       29 rows  IH 10 W ACCESS RD

SRC_SHA256 by rows
     10.0K  6fd9a851dcd70ab4a0425477861be0f7f36426feccb468ebe58f80b631af85cc

SRC_SHA256 by dollars
       5.72M    10.0K rows  6fd9a851dcd70ab4a0425477861be0f7f36426feccb468ebe58f80b631af

## who x when

MSAG_NAME by INSTALLDATE, dollars = LENGTHFEET
  BANDERA RD                                2000:12.8K
  BLANCO RD                                 1980:2.8K 2000:19.6K
  CULEBRA RD                                1980:3.8K 2000:22.0K
  HUEBNER RD                                1980:11.9K 2000:1.3K
  IH 10 E                                   2000:22.8K
  IH 10 E ACCESS RD                         2000:20.3K
  IH 10 W                                   2000:44.1K
  IH 10 W ACCESS RD                         2000:45.1K
  IH 35 N ACCESS RD                         2000:27.5K
  IH 35 S                                   2000:17.4K
  IH 35 S ACCESS RD                         2000:38.3K
  IH 37 S ACCESS RD                         2000:17.5K
  N LOOP 1604 E ACCESS RD                   2000:24.7K
  N LOOP 1604 W ACCESS RD                   2000:23.3K
  NE LOOP 410 ACCESS RD                     2000:24.4K
  NW LOOP 410 ACCESS RD                     2000:28.3K
  SE LOOP 410 ACCESS RD                     2000:28.7K
  SW LOOP 410 ACCESS RD                     2000:20.7K
  UNNAMED ST IN CAMP BULLIS                 2000:45.8K
  US HWY 281 N                              2000:15.8K
  US HWY 281 N ACCESS RD                    2000:23.0K
  US HWY 90 W                               2000:23.4K
  US HWY 90 W ACCESS RD                     2000:15.4K
  W MILITARY DR                             1980:6.6K 2000:8.7K 2020:109.20
  WURZBACH PKWY                             2000:17.4K

TOSTREET by INSTALLDATE, dollars = LENGTHFEET
  BLANCO RD                                 1980:10.9K 2000:3.1K
  BRIDGE                                    1980:20.2K 2000:3.6K 2002:583 2013:119.50
  CITY LIMITS                               1980:6.9K 2000:12.2K 2015:2.0K
  CUL-DE-SAC                                1980:61.1K 2000:308.1K 2004:234.20 2005:433.10 2006:184.20 2007:703.10 2010:271.40 2012:283.20 2014:836 2016:499.70 2017:1.3K 2019:149.70 2020:900.80 2021:1.2K 2022:3.5K 2023:9.8K 2024:1.2K 2025:368.80
  Dead End                                  1980:26.2K 1984:269.70 1998:299.90 2000:26.9K 2016:140.30 2018:471.80 2019:1.7K 2020:1.7K 2021:1.4K 2025:2.2K
  IH 10 E ACCESS RD                         1980:4.8K 2000:8.6K 2004:193
  IH 10 W                                   1980:514.80 2000:21.8K
  IH 10 W ACCESS RD                         1980:3.3K 2000:9.7K
  IH 35 N ACCESS RD                         1980:1.8K 2000:11.4K
  IH 35 S ACCESS RD                         1980:3.8K 2000:15.1K
  N LOOP 1604 W ACCESS RD                   2000:14.8K 2016:470.60
  NE LOOP 410 ACCESS RD                     1980:2.2K 2000:11.2K
  NW LOOP 410 ACCESS RD                     1980:2.5K 2000:13.1K
  PVT RD                                    1980:2.5K 2000:6.7K 2022:1.9K
  RR CROSSING                               1980:5.4K 2000:110
  SOMERSET RD                               1980:3.9K 2000:13.4K
  STRAUS MEDINA                             2000:13.5K
  SW LOOP 410 ACCESS RD                     1980:5.8K 2000:6.0K
  TBD                                       2000:441.4K 2021:1.0K
  UNNAMED ST IN CAMP BULLIS                 2000:34.4K
  US HWY 281 N                              1980:1.3K 2000:11.5K
  US HWY 281 N ACCESS RD                    1980:5.3K 2000:12.5K
  US HWY 90 W ACCESS RD                     1980:1.1K 2000:13.6K
  VANCE JACKSON                             1980:6.2K 2000:5.8K
  WURZBACH PKWY ACCESS RD                   1980:3.0K 2000:13.7K

## what

JURISDICTION: San Antonio 72%, ETJ San Antonio 19%, Converse 2%, Bexar County 1%, Universal City 1%, Live Oak 1%, Ft Sam Houston 1%, Lackland AFB 1%, Alamo Heights 1%, Randolph AFB 1%, Helotes 1%, Leon Valley 1%

DISTRICT: 0 31%, 02 9%, 01 9%, 03 8%, 10 8%, 05 7%, 09 7%, 04 6%, 07 6%, 08 6%, 06 5%, 02_10 0%

ROW_TYPE: Street 95%, Alley Non-Service 3%, Alley Service 1%, Alley Easement 1%, TBD 0%

SURFACE_TYPE: AC Asphalt Concrete 53%, TBD 43%, Earth 3%, PCC Jointed Concrete 0%, Gravel 0%, Brick and Block 0%

SPEEDLIMIT: 0 88%, 30 10%, 35 1%, 40 1%, 45 0%, 20 0%, 25 0%

ONEWAY: No 98%, Yes 2%

OWNER: San Antonio 55%, Bexar County 15%, TxDOT 13%, Private 12%, Converse 1%, Ft Sam Houston 1%, Universal City 1%, Lackland AFB 1%, Alamo Heights 1%, Randolph AFB 1%, Live Oak 1%, Leon Valley 0%

ROADFUNCTION: Local 69%, Minor 9%, Access Road 5%, Collector 5%, Alley 4%, Principal 3%, TBD 3%, Interstate 2%, Easement 1%, Paper Street 0%, Pedestrian 0%

MAINTENANCERESPONSIBILITY: COSA - Public Works Dept 52%, Bexar County 15%, TxDOT 13%, Private 12%, Property Owner 3%, Converse 1%, Ft Sam Houston 1%, Universal City 1%, Lackland AFB 1%, Alamo Heights 1%, Randolph AFB 1%, Live Oak 1%

STATUS: TBD 88%, Inactive 7%, Active 5%

STAGE: Existing 93%, New 7%, TBD 0%, Future 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| CARTID | id | 9.8K | 0 | 405776 50; 420315 50; 201220 50; 417392 50 |
| MSAG_NAME | who | 6.6K | 0 | IH 10 W ACCESS RD 72; IH 35 S ACCESS RD 58; IH 35 N ACCESS RD 56; N LOOP 1604 E ACCESS RD 53 |
| FROMSTREET | other | 6.2K | 0 | CUL-DE-SAC 201; TBD 146; Dead End 89; IH 10 W ACCESS RD 58 |
| TOSTREET | who | 5.7K | 1 | CUL-DE-SAC 796; TBD 648; Dead End 130; BRIDGE 60 |
| JURISDICTION | category | 35 | 0 | San Antonio 6.9K; ETJ San Antonio 1.8K; Converse 152; Bexar County 137 |
| DISTRICT | category | 29 | 0 | 0 3.0K; 02 891; 01 839; 03 741 |
| LENGTHFEET | amount | 6.2K | 0 | 301.3 51; 288.3 51; 366.9 51; 185.1 50 |
| INSTALLDATE | date | 219 | 0 | 1/1/2000 12:00:00 AM 5.0K; 1/1/1980 12:00:00 AM 4.6K; 11/30/2022 12:00:00 AM 20; 12/11/2023 12:00:00 AM 15 |
| PCI | other | 96 | 0 | 87 4.8K; 49 292; 88 201; 96 199 |
| ROW_TYPE | category | 5 | 0 | Street 9.5K; Alley Non-Service 307; Alley Service 102; Alley Easement 65 |
| SURFACE_TYPE | category | 6 | 0 | AC Asphalt Concrete 5.3K; TBD 4.3K; Earth 327; PCC Jointed Concrete 50 |
| PAVEMENTWIDTH | amount | 41 | 0 | 28.5 3.9K; 28.6 1.3K; 30 1.1K; 28 1.0K |
| SPEEDLIMIT | category | 7 | 0 | 0 8.8K; 30 988; 35 130; 40 77 |
| ONEWAY | category | 2 | 0 | No 9.8K; Yes 212 |
| OWNER | category | 39 | 0 | San Antonio 5.2K; Bexar County 1.4K; TxDOT 1.2K; Private 1.1K |
| ROADFUNCTION | category | 11 | 0 | Local 6.9K; Minor 908; Access Road 490; Collector 467 |
| MAINTENANCERESPONSIBILITY | category | 41 | 0 | COSA - Public Works Dept 4.9K; Bexar County 1.4K; TxDOT 1.2K; Private 1.1K |
| STATUS | category | 3 | 0 | TBD 8.8K; Inactive 712; Active 505 |
| STAGE | category | 4 | 0 | Existing 9.3K; New 695; TBD 30; Future 4 |
| SHAPE__LENGTH | amount | 9.9K | 0 | 185.062435328636 50; 56.6788068856569 50; 548.303375039885 50; 327.290661554342 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:03:59.70407 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | ecabe77f-dd86-4267-8652-3 10.0K |
| SRC_SHA256 | who | 1 | 0 | 6fd9a851dcd70ab4a04254778 10.0K |
