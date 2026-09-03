# PORTAL_CKA_OKLAHOMA_OPEN_DA_6DFA4FF30D

rows 10.0K  columns 15  scan 4.2s

roles: amount 1, audit 2, category 4, date 4, other 2, who 3

## when

REPORT_DATE
  2022     10.0K  ##############################

CHECK_DATE
  2022     10.0K  ##############################

UPDATE_DATE
  2023     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -1.7K | 1.4K | 21.0K | 450.0K | 28.48M |

## who

LAST_NAME by rows
        94  Johnson
        82  Jones
        71  Brown
        67  Davis
        59  Moore
        56  Miller
        49  Wilson
        47  Martin
        45  Anderson
        40  Harris
        35  Cook
        33  Campbell
        33  Baker
        33  Cooper
        30  Phillips
        30  Lewis
        29  Lee
        28  Cox
        27  Edwards
        26  Allen

LAST_NAME by dollars
      491.7K        2 rows  Gundy
      292.1K       94 rows  Johnson
      223.9K       82 rows  Jones
      220.5K       71 rows  Brown
      212.7K        8 rows  Boynton
      186.4K       59 rows  Moore
      164.3K       49 rows  Wilson
      162.4K       56 rows  Miller
      152.4K       67 rows  Davis
      144.7K       19 rows  Kim
      135.3K       47 rows  Martin
      128.2K        8 rows  Mason
      116.8K       16 rows  Dunn
      116.3K       45 rows  Anderson
      115.0K       26 rows  Bailey
      104.9K       30 rows  Lewis
      103.7K       35 rows  Cook
      102.8K        4 rows  Beaman
       97.6K       40 rows  Harris
       92.2K        4 rows  Glass

AGENCY_NAME by rows
     10.0K  OKLAHOMA STATE UNIVERSITY

AGENCY_NAME by dollars
      28.48M    10.0K rows  OKLAHOMA STATE UNIVERSITY

SRC_SHA256 by rows
     10.0K  479b8fbfa2c0fe2ef1ea2672584f018702e41c881b199f7c5108007a8559fba9

SRC_SHA256 by dollars
      28.48M    10.0K rows  479b8fbfa2c0fe2ef1ea2672584f018702e41c881b199f7c5108007a8559

## who x when

LAST_NAME by REPORT_DATE, dollars = AMOUNT
  Allen                                     2022:90.6K
  Anderson                                  2022:116.3K
  Bailey                                    2022:115.0K
  Baker                                     2022:81.9K
  Beaman                                    2022:102.8K
  Boynton                                   2022:212.7K
  Brown                                     2022:220.5K
  Campbell                                  2022:61.4K
  Cook                                      2022:103.7K
  Cooper                                    2022:67.6K
  Cox                                       2022:52.1K
  Davis                                     2022:152.4K
  Dunn                                      2022:116.8K
  Edwards                                   2022:87.9K
  Glass                                     2022:92.2K
  Gundy                                     2022:491.7K
  Harris                                    2022:97.6K
  Johnson                                   2022:292.1K
  Jones                                     2022:223.9K
  Kim                                       2022:144.7K
  Lee                                       2022:63.5K
  Lewis                                     2022:104.9K
  Martin                                    2022:135.3K
  Mason                                     2022:128.2K
  Miller                                    2022:162.4K
  Moore                                     2022:186.4K
  Phillips                                  2022:87.3K
  Wilson                                    2022:164.3K

AGENCY_NAME by REPORT_DATE, dollars = AMOUNT
  OKLAHOMA STATE UNIVERSITY                 2022:28.48M

## what

FIRST_INITIAL: J 14%, M 11%, A 11%, C 11%, S 9%, K 8%, R 7%, D 7%, B 6%, T 6%, L 6%, E 4%

MIDDLE_INITIAL: L 15%, A 14%, M 13%, R 10%, D 10%, J 10%, E 8%, S 6%, C 5%, K 5%, G 4%

C_ACCOUNT: 511160 60%, 511150 23%, 511140 7%, 511270 6%, 511170 3%, 511310 0%, 511430 0%

ACCOUNT_DESCRIPTION: Sals-H.Ed Non-Prof. Pay 60%, Sals-H.Ed Prof.(Non-Teach) Pay 23%, Sals-H.Ed Teaching Pay 7%, Overtime Wages 6%, Sals-H.Ed Other Teach Pay 3%, Terminal Leave 0%, Employee Exp.Allow-Reportable 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 1 | 0 | 31-Jul-22 10.0K |
| AGENCY_NUMBER | other | 1 | 0 | 01000 10.0K |
| AGENCY_NAME | who | 1 | 0 | OKLAHOMA STATE UNIVERSITY 10.0K |
| LAST_NAME | who | 3.6K | 0 | Johnson 116; Brown 106; Jones 101; Wilson 92 |
| FIRST_INITIAL | category | 26 | 0 | J 1.2K; M 970; A 947; C 909 |
| MIDDLE_INITIAL | category | 29 | 959 | L 1.1K; A 1.0K; M 969; R 757 |
| HOURS | other | 183 | 0 | 80 1.9K; 168 1.8K; 84 636; 0 410 |
| AMOUNT | amount | 7.0K | 0 | 1200 71; 2100 54; 240 52; 1804 51 |
| CHECK_DATE | date | 10 | 0 | 29-Jul-22 3.9K; 08-Jul-22 3.1K; 22-Jul-22 2.9K; 12-Jul-22 74 |
| C_ACCOUNT | category | 7 | 0 | 511160 6.0K; 511150 2.3K; 511140 678; 511270 640 |
| ACCOUNT_DESCRIPTION | category | 7 | 0 | Sals-H.Ed Non-Prof. Pay 6.0K; Sals-H.Ed Prof.(Non-Teach 2.3K; Sals-H.Ed Teaching Pay 678; Overtime Wages 640 |
| UPDATE_DATE | date | 1 | 0 | 06-Feb-23 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:58:00.80295 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | ed01fb71-14f0-4c63-bdd6-d 10.0K |
| SRC_SHA256 | who | 1 | 0 | 479b8fbfa2c0fe2ef1ea26725 10.0K |
