# PORTAL_SOC_UTAH_OPEN_DATA_P_F87FB2BFB7

rows 25  columns 14  scan 2.3s

roles: audit 2, category 9, date 2, other 1, who 1

## when

FINAL_CLOSE_DATE
  2004         3  ######################
  2005         1  ########
  2006         2  ###############
  2007         4  ##############################
  2008         1  ########
  2009         2  ###############
  2010         3  ######################
  2011         1  ########
  2012         3  ######################
  2013         4  ##############################
  2014         1  ########

INGESTED_AT
  2026        25  ##############################

## who

SRC_SHA256 by rows
        25  85ceb6ab1391e1754bc3345d79b96a23482fed6c6cbbf963493d9544d1e1d7bc

## who x when

SRC_SHA256 by FINAL_CLOSE_DATE
  85ceb6ab1391e1754bc3345d79b96a23482fed6c  2004:3 2005:1 2006:2 2007:4 2008:1 2009:2 2010:3 2011:1 2012:3 2013:4 2014:1

## what

CASE_TYPE: Deficient Filer 84%, Non Filer 8%, DFVC Underpay 4%, Later Filer 4%

EIN: 87-0393217 8%, 88-0090855 8%, 80-0027170 8%, 84-1470690 8%, 87-0474292 8%, 87-0536150 8%, 22-3863257 8%, 87-0650093 8%, 87-0410426 8%, 71-1009611 8%, 87-0639599 8%, 87-0643818 8%

PN: 1 84%, 2 12%, 333 4%

PLAN_YEAR: 2010 20%, 2004 20%, 2002 16%, 2007 12%, nan 8%, 2009 8%, 2006 8%, 2012 4%, 2011 4%

PLAN_NAME: Salt Lake Air Cargo 401(k) Pla 8%, Leavitt Group Profit Sharing a 8%, ROCKY MOUNTAIN CARE 401(K) PLA 8%, GEMSTONE HOTELS & RESORTS, LLC 8%, VISTA STAFFING SOLUTIONS, INC. 8%, SANSEGAL SPORTSWEAR 401K PENSI 8%, MERIDIAN RESTAURANTS UNLIMITED 8%, ALLIANCE 401(K) PLAN 8%, FFKR ARCHITECTS/PLANNERS II 40 8%, DESERET HEALTH GROUP 401(K) PL 8%, ROCKY MOUNTAIN RECYCLING, L.L. 8%, Innovative Staffing Inc Retire 8%

PLAN_ADMIN: Salt Lake Air Cargo 8%, Leavitt Group Enterprises, Inc 8%, ROCKY MOUNTAIN CARE 8%, GEMSTONE HOTELS & RESORTS, LLC 8%, VISTA STAFFING SOLUTIONS 8%, SANSEGAL SPORTSWEAR 8%, MERIDIAN RESTAURANTS UNLIMITED 8%, EAGLE AIR MED 8%, FFKR ARCHITECTS/PLANNERS II 8%, DESERET HEALTHCARE, INC. 8%, ROCKY MOUNTAIN RECYCLING, L.L. 8%, Innovative Staffing Inc 8%

PLAN_ADMIN_ZIP_CODE:  -  15%, 84010-  8%, 84060-  8%, 84111-  8%, 84070-  8%, 84401-  8%, 84003-  8%, 84104-1021 8%, 84014-  8%, 84126-  8%, 84095-  8%, 84721-8340 8%

FINAL_CLOSE_REASON: Closed after Correspondence 96%, No Enforcement Action Taken 4%

PENALTY_AMOUNT: $0-$10,000 48%, $10,001 - $50,000 40%, $50,001 - $100,000 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CASE_TYPE | category | 4 | 0 | Deficient Filer 21; Non Filer 2; DFVC Underpay 1; Later Filer 1 |
| EIN | category | 25 | 0 | 87-0393217 1; 88-0090855 1; 80-0027170 1; 84-1470690 1 |
| PN | category | 3 | 0 | 1 21; 2 3; 333 1 |
| PLAN_YEAR | category | 9 | 0 | 2010 5; 2004 5; 2002 4; 2007 3 |
| PLAN_NAME | category | 25 | 0 | Salt Lake Air Cargo 401(k 1; Leavitt Group Profit Shar 1; ROCKY MOUNTAIN CARE 401(K 1; GEMSTONE HOTELS & RESORTS 1 |
| PLAN_ADMIN | category | 25 | 0 | Salt Lake Air Cargo 1; Leavitt Group Enterprises 1; ROCKY MOUNTAIN CARE 1; GEMSTONE HOTELS & RESORTS 1 |
| PLAN_ADMIN_STATE | other | 1 | 0 | Utah 25 |
| PLAN_ADMIN_ZIP_CODE | category | 24 | 0 |  -  2; 84010-  1; 84060-  1; 84111-  1 |
| FINAL_CLOSE_REASON | category | 2 | 0 | Closed after Corresponden 24; No Enforcement Action Tak 1 |
| FINAL_CLOSE_DATE | date | 25 | 0 | 2007-05-29T00:00:00.000 1; 2005-01-14T00:00:00.000 1; 2014-08-13T00:00:00.000 1; 2013-08-19T00:00:00.000 1 |
| PENALTY_AMOUNT | category | 3 | 0 | $0-$10,000 12; $10,001 - $50,000 10; $50,001 - $100,000 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:42:19.99964 25 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1d64c1ac-353f-4ce7-871a-e 25 |
| SRC_SHA256 | who | 1 | 0 | 85ceb6ab1391e1754bc3345d7 25 |
