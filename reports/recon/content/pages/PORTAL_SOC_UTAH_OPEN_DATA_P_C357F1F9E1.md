# PORTAL_SOC_UTAH_OPEN_DATA_P_C357F1F9E1

rows 28  columns 14  scan 2.1s

roles: audit 2, category 10, date 2, who 1

## when

CLOSING_DATE
  2000         1  ########
  2001         3  ######################
  2004         4  ##############################
  2006         2  ###############
  2007         3  ######################
  2008         1  ########
  2009         2  ###############
  2010         3  ######################
  2011         1  ########
  2012         3  ######################
  2013         4  ##############################
  2014         1  ########

INGESTED_AT
  2026        28  ##############################

## who

SRC_SHA256 by rows
        28  6fbf622bf14abe616c318c999aa4257d1e84edf001d09f20918153c19b534243

## who x when

SRC_SHA256 by CLOSING_DATE
  6fbf622bf14abe616c318c999aa4257d1e84edf0  2000:1 2001:3 2004:4 2006:2 2007:3 2008:1 2009:2 2010:3 2011:1 2012:3 2013:4 2014:1

## what

PLAN_NAME: WILSON FINANCIAL ADVISORS, INC 8%, VISTA STAFFING SOLUTIONS, INC. 8%, VALLEY SERVICES, INC. PROFIT S 8%, TURN COMMUNITY SERVICES 401K P 8%, STATE BANK OF SOUTHERN UTAH PR 8%, SME 401K EMPLOYEE SAVINGS PLAN 8%, SKAGGS COMPANIES INC EMPLOYEES 8%, SANSEGAL SPORTSWEAR 401K PENSI 8%, ROCKY MOUNTAIN RECYCLING, L.L. 8%, ROCKY MOUNTAIN CARE 401(K) PLA 8%, RAZORFISH, INC. 401K PLAN 8%, NICHOLAS & COMPANY 401K PROFIT 8%

PLAN_ADMINISTRATOR: WILSON FINANCIAL ADVISORS, INC 8%, VISTA STAFFING SOLUTIONS 8%, VALLEY SERVICES, INC. 8%, TURN COMMUNITY SERVICES 401K P 8%, STATE BANK OF SOUTHERN UTAH 8%, SME 8%, SKAGGS COMPANIES INC EMPLOYEES 8%, SANSEGAL SPORTSWEAR 8%, ROCKY MOUNTAIN RECYCLING, L.L. 8%, ROCKY MOUNTAIN CARE 8%, RAZORFISH, INC. 8%, NICHOLAS & COMPANY, INC. 8%

ADMIN_STATE: Utah 100%

ADMIN_ZIP_CODE: 84003-  15%, 84102-1021 8%, 84111-  8%, 84118-3731 8%, 84102-  8%, 84720-2639 8%, 84088-5667 8%, 84107-  8%, 84070-  8%, 84126-  8%, 84010-  8%, 84121-7080 8%

PLAN_EIN: 87-0441589 8%, 87-0474292 8%, 87-0503440 8%, 87-0303448 8%, 87-0234702 8%, 87-0495960 8%, 84-1410470 8%, 87-0536150 8%, 87-0639599 8%, 80-0027170 8%, 13-3804503 8%, 87-0235565 8%

PLAN_NO: 1 86%, 2 7%, 3 4%, 333 4%

PLAN_YEAR: 2010 18%, 2004 18%, 2002 11%, 2007 11%, 1998 11%, 2009 7%, 2006 7%, 1997 4%, 2012 4%, nan 4%, 2000 4%, 2011 4%

CASE_TYPE: Deficient Filer 89%, Later Filer 4%, DFVC Underpay 4%, Non Filer 4%

CLOSING_REASON: Closed after Correspondence 89%, Closed after ALJ 4%, Referred for Further Action 4%, No Enforcement Action Taken 4%

PENALTY_AMOUNT: $0-$10,000 57%, $10,001 - $50,000 36%, $50,001 - $100,000 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PLAN_NAME | category | 28 | 0 | WILSON FINANCIAL ADVISORS 1; VISTA STAFFING SOLUTIONS, 1; VALLEY SERVICES, INC. PRO 1; TURN COMMUNITY SERVICES 4 1 |
| PLAN_ADMINISTRATOR | category | 28 | 0 | WILSON FINANCIAL ADVISORS 1; VISTA STAFFING SOLUTIONS 1; VALLEY SERVICES, INC. 1; TURN COMMUNITY SERVICES 4 1 |
| ADMIN_STATE | category | 2 | 5 | Utah 23 |
| ADMIN_ZIP_CODE | category | 27 | 0 | 84003-  2; 84102-1021 1; 84111-  1; 84118-3731 1 |
| PLAN_EIN | category | 28 | 0 | 87-0441589 1; 87-0474292 1; 87-0503440 1; 87-0303448 1 |
| PLAN_NO | category | 4 | 0 | 1 24; 2 2; 3 1; 333 1 |
| PLAN_YEAR | category | 12 | 0 | 2010 5; 2004 5; 2002 3; 2007 3 |
| CASE_TYPE | category | 4 | 0 | Deficient Filer 25; Later Filer 1; DFVC Underpay 1; Non Filer 1 |
| CLOSING_REASON | category | 4 | 0 | Closed after Corresponden 25; Closed after ALJ 1; Referred for Further Acti 1; No Enforcement Action Tak 1 |
| CLOSING_DATE | date | 28 | 0 | 2004-10-12T00:00:00.000 1; 2013-12-23T00:00:00.000 1; 2010-03-25T00:00:00.000 1; 2000-11-27T00:00:00.000 1 |
| PENALTY_AMOUNT | category | 3 | 0 | $0-$10,000 16; $10,001 - $50,000 10; $50,001 - $100,000 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:43:12.66791 28 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5cba7d7e-6b72-4a2e-a461-0 28 |
| SRC_SHA256 | who | 1 | 0 | 6fbf622bf14abe616c318c999 28 |
