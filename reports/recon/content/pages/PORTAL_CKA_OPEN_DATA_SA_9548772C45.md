# PORTAL_CKA_OPEN_DATA_SA_9548772C45

rows 21  columns 11  scan 3.7s

roles: amount 3, audit 2, category 3, date 2, who 2

## when

YEARDESIGNATED
  1999         2  ####################
  2000         2  ####################
  2001         1  ##########
  2002         1  ##########
  2004         2  ####################
  2006         1  ##########
  2007         1  ##########
  2008         3  ##############################
  2014         1  ##########
  2017         1  ##########
  2019         1  ##########
  2021         3  ##############################
  2023         1  ##########
  2025         1  ##########

INGESTED_AT
  2026        21  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 21 | 39.35 | 259.62 | 3.5K | 3.6K | 20.5K |
| SHAPE__AREA | 21 | 1.71M | 12.07M | 150.91M | 154.91M | 892.48M |
| SHAPE__LENGTH | 21 | 8.0K | 23.4K | 297.2K | 337.4K | 1.25M |

## who

TIRZSTATUS by rows
        21  Designated

TIRZSTATUS by dollars
       20.5K       21 rows  Designated

SRC_SHA256 by rows
        21  6671615f11718a4cc61ffc8a81d68a9db86513925824a96367f5d480f93195a4

SRC_SHA256 by dollars
       20.5K       21 rows  6671615f11718a4cc61ffc8a81d68a9db86513925824a96367f5d480f931

## who x when

TIRZSTATUS by YEARDESIGNATED, dollars = ACRES
  Designated                                1999:1.3K 2000:3.7K 2001:39.35 2002:461.07 2004:2.6K 2006:90.30 2007:3.1K 2008:4.4K 2014:2.0K 2017:148.98 2019:88.31 2021:455.41 2023:241.63 2025:1.9K

SRC_SHA256 by YEARDESIGNATED, dollars = ACRES
  6671615f11718a4cc61ffc8a81d68a9db8651392  1999:1.3K 2000:3.7K 2001:39.35 2002:461.07 2004:2.6K 2006:90.30 2007:3.1K 2008:4.4K 2014:2.0K 2017:148.98 2019:88.31 2021:455.41 2023:241.63 2025:1.9K

## what

OBJECTID: 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%

TIRZNUM: 41 8%, 9 8%, 30 8%, 25 8%, 38 8%, 17 8%, 36 8%, 34 8%, 6 8%, 33 8%, 13 8%, 37 8%

TIRZNAME: Rosillio 8%, Houston Street 8%, Westside 8%, Hunter's Pond 8%, Somerset Grove 8%, Mission Creek 8%, Thea Meadows 8%, Hemisfair 8%, Mission del Lago 8%, Northeast Corridor 8%, Lackland Hills 8%, Nabors 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 21 | 0 | 21 1; 20 1; 19 1; 18 1 |
| TIRZNUM | category | 21 | 0 | 41 1; 9 1; 30 1; 25 1 |
| TIRZNAME | category | 21 | 0 | Rosillio 1; Houston Street 1; Westside 1; Hunter's Pond 1 |
| TIRZSTATUS | who | 1 | 0 | Designated 21 |
| ACRES | amount | 21 | 0 | 1854.6 1; 259.61690134 1; 1506.82912792 1; 90.29817331 1 |
| YEARDESIGNATED | date | 16 | 0 | 12/11/2008 12:00:00 AM 3; 6/17/2021 12:00:00 AM 2; 12/9/2004 12:00:00 AM 2; 12/14/2000 12:00:00 AM 2 |
| SHAPE__AREA | amount | 21 | 0 | 80812718.8847656 1; 12070840.2949219 1; 64994201.9589844 1; 3933372.69726563 1 |
| SHAPE__LENGTH | amount | 21 | 0 | 58326.160333917 1; 22719.153587467 1; 117140.755952334 1; 11909.2196744562 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:16:47.16273 21 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9c6533ce-b716-436d-bb36-7 21 |
| SRC_SHA256 | who | 1 | 0 | 6671615f11718a4cc61ffc8a8 21 |
