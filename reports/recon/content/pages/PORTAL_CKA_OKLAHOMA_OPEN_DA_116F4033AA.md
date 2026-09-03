# PORTAL_CKA_OKLAHOMA_OPEN_DA_116F4033AA

rows 10.0K  columns 15  scan 5.5s

roles: amount 1, audit 2, category 4, date 4, other 2, who 3

## when

REPORT_DATE
  2024     10.0K  ##############################

CHECK_DATE
  2024     10.0K  ##############################

UPDATE_DATE
  2024     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -6.6K | 1.9K | 26.6K | 802.7K | 40.58M |

## who

LAST_NAME by rows
        88  Johnson
        81  Smith
        77  Williams
        64  Jones
        58  Taylor
        56  Davis
        45  Moore
        44  Wilson
        41  Brown
        40  Anderson
        37  Miller
        37  Baker
        35  Thompson
        31  Robinson
        29  Cook
        29  Allen
        28  Jackson
        28  Evans
        28  Walker
        26  Harris

LAST_NAME by dollars
      802.7K        1 rows  Arens
      512.5K        2 rows  Gundy
      361.5K       81 rows  Smith
      321.5K       88 rows  Johnson
      280.5K       58 rows  Taylor
      256.6K       64 rows  Jones
      200.0K        2 rows  Lutz
      193.2K       37 rows  Miller
      191.0K       45 rows  Moore
      188.5K       37 rows  Baker
      188.1K       56 rows  Davis
      187.5K        1 rows  Boynton
      184.1K       77 rows  Williams
      176.3K       41 rows  Brown
      171.0K       18 rows  Kim
      169.7K       44 rows  Wilson
      154.3K       23 rows  Thomas
      141.8K       13 rows  Dunn
      133.3K       24 rows  Bailey
      130.2K        2 rows  Norwood

AGENCY_NAME by rows
     10.0K  OKLAHOMA STATE UNIVERSITY

AGENCY_NAME by dollars
      40.58M    10.0K rows  OKLAHOMA STATE UNIVERSITY

SRC_SHA256 by rows
     10.0K  a6924520a51ef0ba2dbc73ad98e9215005f1142b51bbc8b866ab129f2df67922

SRC_SHA256 by dollars
      40.58M    10.0K rows  a6924520a51ef0ba2dbc73ad98e9215005f1142b51bbc8b866ab129f2df6

## who x when

LAST_NAME by REPORT_DATE, dollars = AMOUNT
  Allen                                     2024:81.7K
  Anderson                                  2024:129.1K
  Arens                                     2024:802.7K
  Bailey                                    2024:133.3K
  Baker                                     2024:188.5K
  Boynton                                   2024:187.5K
  Brown                                     2024:176.3K
  Cook                                      2024:108.2K
  Davis                                     2024:188.1K
  Dunn                                      2024:141.8K
  Evans                                     2024:44.3K
  Gundy                                     2024:512.5K
  Harris                                    2024:99.1K
  Jackson                                   2024:82.0K
  Johnson                                   2024:321.5K
  Jones                                     2024:256.6K
  Kim                                       2024:171.0K
  Lutz                                      2024:200.0K
  Miller                                    2024:193.2K
  Moore                                     2024:191.0K
  Norwood                                   2024:130.2K
  Robinson                                  2024:106.4K
  Smith                                     2024:361.5K
  Taylor                                    2024:280.5K
  Thomas                                    2024:154.3K
  Thompson                                  2024:102.0K
  Walker                                    2024:99.0K
  Williams                                  2024:184.1K
  Wilson                                    2024:169.7K

AGENCY_NAME by REPORT_DATE, dollars = AMOUNT
  OKLAHOMA STATE UNIVERSITY                 2024:40.58M

## what

FIRST_INITIAL: J 16%, M 11%, A 10%, C 10%, S 10%, K 8%, D 7%, R 7%, B 6%, T 6%, L 5%, E 4%

MIDDLE_INITIAL: L 15%, M 14%, A 13%, D 11%, R 10%, J 10%, E 8%, S 5%, K 5%, C 5%, B 4%

C_ACCOUNT: 511160 48%, 511150 34%, 511140 10%, 511270 5%, 511170 3%, 511310 0%, 511430 0%

ACCOUNT_DESCRIPTION: Sals-H.Ed Non-Prof. Pay 48%, Sals-H.Ed Prof.(Non-Teach) Pay 34%, Sals-H.Ed Teaching Pay 10%, Overtime Wages 5%, Sals-H.Ed Other Teach Pay 3%, Terminal Leave 0%, Employee Exp.Allow-Reportable 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 1 | 0 | 31-Jul-24 10.0K |
| AGENCY_NUMBER | other | 1 | 0 | 01000 10.0K |
| AGENCY_NAME | who | 1 | 0 | OKLAHOMA STATE UNIVERSITY 10.0K |
| LAST_NAME | who | 3.7K | 0 | Johnson 105; Smith 91; Brown 86; Davis 86 |
| FIRST_INITIAL | category | 26 | 0 | J 1.3K; M 903; A 844; C 842 |
| MIDDLE_INITIAL | category | 29 | 890 | L 1.1K; M 1.0K; A 949; D 795 |
| HOURS | other | 177 | 0 | 184 2.6K; 80 2.5K; 0 542; 1 491 |
| AMOUNT | amount | 6.8K | 0 | 1280 63; 5000 61; 800 53; 5700 52 |
| CHECK_DATE | date | 5 | 0 | 31-Jul-24 4.7K; 05-Jul-24 2.6K; 19-Jul-24 2.6K; 12-Jul-24 110 |
| C_ACCOUNT | category | 7 | 0 | 511160 4.8K; 511150 3.4K; 511140 981; 511270 519 |
| ACCOUNT_DESCRIPTION | category | 7 | 0 | Sals-H.Ed Non-Prof. Pay 4.8K; Sals-H.Ed Prof.(Non-Teach 3.4K; Sals-H.Ed Teaching Pay 981; Overtime Wages 519 |
| UPDATE_DATE | date | 1 | 0 | 01-Aug-24 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:58:08.65491 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 85a8da15-548f-494a-b4a9-e 10.0K |
| SRC_SHA256 | who | 1 | 0 | a6924520a51ef0ba2dbc73ad9 10.0K |
