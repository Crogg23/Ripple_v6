# PORTAL_CKA_OKLAHOMA_OPEN_DA_41B624C494

rows 10.0K  columns 15  scan 4.4s

roles: amount 1, audit 2, category 6, date 4, other 1, who 2

## when

REPORT_DATE
  2025     10.0K  ##############################

CHECK_DATE
  2025     10.0K  ##############################

UPDATE_DATE
  2013        14  
  2014        26  
  2015        40  
  2016         3  
  2017        21  
  2018        41  
  2019        27  
  2020        58  
  2021         9  
  2022        21  
  2023        12  
  2024        11  
  2025      9.7K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | 0.38 | 2.4K | 26.8K | 165.7K | 34.70M |

## who

LAST_NAME by rows
        77  Williams
        72  Smith
        62  Johnson
        57  Jones
        48  Nguyen
        44  Martin
        42  Brown
        39  Wilson
        36  Lee
        34  Moore
        30  Miller
        29  Patel
        27  Thompson
        26  Davis
        26  White
        24  Tran
        24  Wood
        24  Vu
        23  Khan
        23  Carter

LAST_NAME by dollars
      411.8K       77 rows  Williams
      215.8K        7 rows  Pierce
      201.8K       72 rows  Smith
      191.4K       57 rows  Jones
      188.0K       24 rows  Wood
      173.0K       23 rows  Khan
      154.5K       20 rows  Walker
      151.2K       62 rows  Johnson
      139.8K        2 rows  Brannon
      133.2K       16 rows  Richardson
      133.1K       18 rows  Nelson
      131.6K        2 rows  Al-Juhaishi
      126.2K        2 rows  Alhyari
      121.0K        4 rows  Stratton
      120.2K        8 rows  Kumar
      115.2K       39 rows  Wilson
      111.6K       23 rows  Taylor
      111.5K       48 rows  Nguyen
      103.5K       34 rows  Moore
      102.9K        2 rows  North

SRC_SHA256 by rows
     10.0K  bf7341e1b417a445877b44494558cad6389eb222dc58b347f3300d4c28783656

SRC_SHA256 by dollars
      34.70M    10.0K rows  bf7341e1b417a445877b44494558cad6389eb222dc58b347f3300d4c2878

## who x when

LAST_NAME by REPORT_DATE, dollars = AMOUNT
  Al-Juhaishi                               2025:131.6K
  Alhyari                                   2025:126.2K
  Brannon                                   2025:139.8K
  Brown                                     2025:101.4K
  Carter                                    2025:46.2K
  Davis                                     2025:63.8K
  Johnson                                   2025:151.2K
  Jones                                     2025:191.4K
  Khan                                      2025:173.0K
  Kumar                                     2025:120.2K
  Lee                                       2025:65.8K
  Martin                                    2025:87.4K
  Miller                                    2025:89.4K
  Moore                                     2025:103.5K
  Nelson                                    2025:133.1K
  Nguyen                                    2025:111.5K
  Patel                                     2025:77.8K
  Pierce                                    2025:215.8K
  Richardson                                2025:133.2K
  Smith                                     2025:201.8K
  Stratton                                  2025:121.0K
  Taylor                                    2025:111.6K
  Thompson                                  2025:77.4K
  Tran                                      2025:47.7K
  Vu                                        2025:52.3K
  Walker                                    2025:154.5K
  White                                     2025:65.4K
  Williams                                  2025:411.8K
  Wilson                                    2025:115.2K
  Wood                                      2025:188.0K

SRC_SHA256 by REPORT_DATE, dollars = AMOUNT
  bf7341e1b417a445877b44494558cad6389eb222  2025:34.70M

## what

AGENCY_NUMBER: 77000 89%, 48500 6%, 46100 2%, 83000 1%, 13100 0%, 58500 0%, 34500 0%, 65000 0%, 45200 0%, 34000 0%, 18500 0%, 22000 0%

AGENCY_NAME: UNIV. OF OKLA. HEALTH SCIENCES 89%, NORTHEASTERN STATE UNIVERSITY 6%, ROGERS STATE UNIVERSITY 2%, DEPARTMENT OF HUMAN SERVICES 1%, DEPARTMENT OF CORRECTIONS 0%, DEPARTMENT OF PUBLIC SAFETY 0%, DEPARTMENT OF TRANSPORTATION 0%, DEPARTMENT OF VETERANS AFFAIRS 0%, MENTAL HEALTH AND SUBSTANCE AB 0%, OKLAHOMA STATE DEPARTMENT OF H 0%, CORPORATION COMMISSION 0%, DISTRICT ATTORNEYS COUNCIL 0%

FIRST_INITIAL: J 14%, A 12%, M 12%, S 10%, C 9%, K 9%, D 6%, L 6%, B 6%, T 6%, R 6%, E 4%

MIDDLE_INITIAL: M 15%, A 14%, L 14%, D 10%, J 10%, R 9%, E 7%, C 7%, S 6%, K 5%, N 4%

C_ACCOUNT: 511150 66%, 511160 28%, 511130 2%, 511110 2%, 511140 1%, 511290 0%, 511270 0%, 511170 0%, 511210 0%, 511430 0%, 511280 0%, 511310 0%

ACCOUNT_DESCRIPTION: Sals-H.Ed Prof.(Non-Teach) Pay 66%, Sals-H.Ed Non-Prof. Pay 28%, Sals-Non-Reg Pay 2%, Sals-Regular Pay 2%, Sals-H.Ed Teaching Pay 1%, Pay Differential 0%, Overtime Wages 0%, Sals-H.Ed Other Teach Pay 0%, Longevity Pay-State Employees 0%, Employee Exp.Allow-Reportable 0%, Holiday Pay - Payroll Only 0%, Terminal Leave 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 1 | 0 | 31-Aug-25 10.0K |
| AGENCY_NUMBER | category | 42 | 0 | 77000 8.8K; 48500 642; 46100 215; 83000 66 |
| AGENCY_NAME | category | 42 | 0 | UNIV. OF OKLA. HEALTH SCI 8.8K; NORTHEASTERN STATE UNIVER 642; ROGERS STATE UNIVERSITY 215; DEPARTMENT OF HUMAN SERVI 66 |
| LAST_NAME | who | 4.0K | 0 | Williams 78; Smith 74; Johnson 65; Jones 63 |
| FIRST_INITIAL | category | 26 | 0 | J 1.1K; A 1.0K; M 953; S 861 |
| MIDDLE_INITIAL | category | 27 | 2.0K | M 936; A 895; L 871; D 659 |
| HOURS | other | 121 | 0 | 80 7.8K; 168 280; 40 176; 8 147 |
| AMOUNT | amount | 5.0K | 0 | 2412.73 279; 2507.88 272; 2606.65 230; 2734.65 143 |
| CHECK_DATE | date | 10 | 0 | 08-Aug-25 4.6K; 22-Aug-25 4.5K; 29-Aug-25 348; 15-Aug-25 173 |
| C_ACCOUNT | category | 13 | 0 | 511150 6.6K; 511160 2.8K; 511130 211; 511110 185 |
| ACCOUNT_DESCRIPTION | category | 13 | 0 | Sals-H.Ed Prof.(Non-Teach 6.6K; Sals-H.Ed Non-Prof. Pay 2.8K; Sals-Non-Reg Pay 211; Sals-Regular Pay 185 |
| UPDATE_DATE | date | 191 | 0 | 15-Aug-25 8.8K; 27-Aug-25 642; 25-Aug-25 215; 28-Feb-20 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:58:23.50100 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | cd208cb5-d7e8-4cee-9fcc-3 10.0K |
| SRC_SHA256 | who | 1 | 0 | bf7341e1b417a445877b44494 10.0K |
