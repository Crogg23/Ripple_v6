# PORTAL_CKA_OKLAHOMA_OPEN_DA_682EDC2856

rows 10.0K  columns 15  scan 4.1s

roles: amount 1, audit 2, category 4, date 4, other 2, who 3

## when

REPORT_DATE
  2023     10.0K  ##############################

CHECK_DATE
  2023     10.0K  ##############################

UPDATE_DATE
  2023     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -2.3K | 1.5K | 22.9K | 460.4K | 31.01M |

## who

LAST_NAME by rows
       146  Smith
        81  Davis
        66  Brown
        55  Miller
        52  Taylor
        49  Baker
        48  Moore
        46  Anderson
        42  Thomas
        38  Harris
        36  Martin
        33  Robinson
        33  Wilson
        32  Allen
        32  Zhang
        30  Thompson
        30  Edwards
        29  Evans
        28  Hall
        24  Cook

LAST_NAME by dollars
      502.1K        2 rows  Gundy
      405.9K      146 rows  Smith
      259.7K       66 rows  Brown
      209.3K        4 rows  Boynton
      197.3K       81 rows  Davis
      183.6K       52 rows  Taylor
      169.8K       55 rows  Miller
      169.6K       49 rows  Baker
      149.7K       48 rows  Moore
      137.1K       46 rows  Anderson
      136.5K       42 rows  Thomas
      127.6K       36 rows  Martin
      120.3K       11 rows  Dunn
      115.4K       32 rows  Zhang
      113.3K       24 rows  Bailey
      105.8K        2 rows  Shrum
       96.0K       38 rows  Harris
       95.7K       24 rows  Wang
       92.4K       23 rows  Young
       89.7K       30 rows  Thompson

AGENCY_NAME by rows
     10.0K  OKLAHOMA STATE UNIVERSITY

AGENCY_NAME by dollars
      31.01M    10.0K rows  OKLAHOMA STATE UNIVERSITY

SRC_SHA256 by rows
     10.0K  8ba3e72b5761a13f5866e39fa17c109602e78048ffd1e72ad1f47a8bd71a2112

SRC_SHA256 by dollars
      31.01M    10.0K rows  8ba3e72b5761a13f5866e39fa17c109602e78048ffd1e72ad1f47a8bd71a

## who x when

LAST_NAME by REPORT_DATE, dollars = AMOUNT
  Allen                                     2023:79.5K
  Anderson                                  2023:137.1K
  Bailey                                    2023:113.3K
  Baker                                     2023:169.6K
  Boynton                                   2023:209.3K
  Brown                                     2023:259.7K
  Cook                                      2023:85.3K
  Davis                                     2023:197.3K
  Dunn                                      2023:120.3K
  Edwards                                   2023:77.1K
  Evans                                     2023:43.7K
  Gundy                                     2023:502.1K
  Hall                                      2023:66.1K
  Harris                                    2023:96.0K
  Martin                                    2023:127.6K
  Miller                                    2023:169.8K
  Moore                                     2023:149.7K
  Robinson                                  2023:85.8K
  Shrum                                     2023:105.8K
  Smith                                     2023:405.9K
  Taylor                                    2023:183.6K
  Thomas                                    2023:136.5K
  Thompson                                  2023:89.7K
  Wang                                      2023:95.7K
  Wilson                                    2023:89.6K
  Young                                     2023:92.4K
  Zhang                                     2023:115.4K

AGENCY_NAME by REPORT_DATE, dollars = AMOUNT
  OKLAHOMA STATE UNIVERSITY                 2023:31.01M

## what

FIRST_INITIAL: J 14%, M 12%, A 11%, C 10%, S 9%, K 8%, R 7%, D 7%, T 6%, L 6%, B 6%, E 4%

MIDDLE_INITIAL: M 14%, L 14%, A 13%, J 11%, R 10%, D 10%, E 8%, S 6%, C 5%, K 5%, N 4%

C_ACCOUNT: 511160 61%, 511150 24%, 511140 7%, 511270 5%, 511170 3%, 511310 0%, 511430 0%

ACCOUNT_DESCRIPTION: Sals-H.Ed Non-Prof. Pay 61%, Sals-H.Ed Prof.(Non-Teach) Pay 24%, Sals-H.Ed Teaching Pay 7%, Overtime Wages 5%, Sals-H.Ed Other Teach Pay 3%, Terminal Leave 0%, Employee Exp.Allow-Reportable 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 1 | 0 | 31-Jul-23 10.0K |
| AGENCY_NUMBER | other | 1 | 0 | 01000 10.0K |
| AGENCY_NAME | who | 1 | 0 | OKLAHOMA STATE UNIVERSITY 10.0K |
| LAST_NAME | who | 3.6K | 0 | Smith 151; Davis 91; Wilson 78; Harris 71 |
| FIRST_INITIAL | category | 26 | 0 | J 1.2K; M 984; A 910; C 850 |
| MIDDLE_INITIAL | category | 29 | 1.1K | M 1.0K; L 991; A 935; J 773 |
| HOURS | other | 162 | 0 | 80 2.0K; 168 1.9K; 84 726; 0 386 |
| AMOUNT | amount | 6.9K | 0 | 2200 66; 1200 55; 600 52; 5000 51 |
| CHECK_DATE | date | 4 | 0 | 31-Jul-23 4.1K; 07-Jul-23 3.0K; 21-Jul-23 2.8K; 12-Jul-23 100 |
| C_ACCOUNT | category | 7 | 0 | 511160 6.1K; 511150 2.4K; 511140 681; 511270 499 |
| ACCOUNT_DESCRIPTION | category | 7 | 0 | Sals-H.Ed Non-Prof. Pay 6.1K; Sals-H.Ed Prof.(Non-Teach 2.4K; Sals-H.Ed Teaching Pay 681; Overtime Wages 499 |
| UPDATE_DATE | date | 1 | 0 | 01-Aug-23 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:58:16.74345 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 66ba9c42-caa2-49f5-b1e9-9 10.0K |
| SRC_SHA256 | who | 1 | 0 | 8ba3e72b5761a13f5866e39fa 10.0K |
