# FED_VOTEVIEW_ROLLCALL_META

rows 3.4K  columns 21  scan 4.6s

roles: amount 5, audit 2, category 4, date 1, empty 1, other 5, who 3

## when

DATE
  2023      1.1K  ##############################
  2024       855  ########################
  2025      1.0K  #############################
  2026       418  ############

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NOMINATE_MID_1 | 3.4K | -1 | 0.02 | 0.75 | 1 | 170.17 |
| NOMINATE_MID_2 | 3.4K | -1 | 0 | 1 | 1 | -79.90 |
| NOMINATE_SPREAD_1 | 3.4K | -1.27 | -0.25 | 0.79 | 1.42 | -360.09 |
| NOMINATE_SPREAD_2 | 3.4K | -2.65 | 0 | 1.50 | 2.63 | -69.43 |
| NOMINATE_LOG_LIKELIHOOD | 3.4K | -266.86 | -7.15 | 0 | 0 | -70.3K |

## who

VOTE_DESC by rows
        21  A bill to provide for reconciliation pursuant to title II of H. Con. R
        18  A bill making continuing appropriations and extensions for fiscal year
        15  An executive resolution authorizing the en bloc consideration in Execu
        15  In the nature of a substitute.
        14  A bill to amend title 38, United States Code, to make certain improvem
        12  A joint resolution providing for congressional disapproval under chapt
        11  A bill making appropriations for military construction, the Department
        11  A bill to reauthorize the Morris K. Udall and Stewart L. Udall Trust F
        10  A joint resolution to direct the removal of United States Armed Forces
        10  A bill to rescind certain budget authority proposed to be rescinded in
        10  A bill to repeal the authorizations for use of military force against 
         9  A bill making further consolidated appropriations for the fiscal year 
         9  To improve the bill.
         8  A bill to amend title 49, United States Code, to reauthorize and impro
         7  A bill making continuing appropriations for the fiscal year ending Sep
         7  A bill a bill to increase the supply of housing in America, and for ot
         6  A bill to authorize appropriations for fiscal year 2024 for military a
         6  An original bill to provide for reconciliation pursuant to title II of
         6  A bill to provide for the regulation of payment stablecoins, and for o
         6  National Defense Authorization Act

VOTE_DESC by dollars
        7.97       14 rows  A bill to amend title 38, United States Code, to make certai
        3.06       11 rows  A bill making appropriations for military construction, the 
        2.58        3 rows  A bill to reform the Foreign Intelligence Surveillance Act o
        2.19       10 rows  A bill to rescind certain budget authority proposed to be re
        2.01        5 rows  A bill making further continuing appropriations for fiscal y
        1.72       11 rows  A bill to reauthorize the Morris K. Udall and Stewart L. Uda
        1.53        2 rows  Kurt Campbell, of the District of Columbia, to be Deputy Sec
        1.52        4 rows  A joint resolution providing for congressional disapproval u
        1.52        3 rows  Commerce, Justice, Science; Energy and Water Development; an
        1.49        2 rows  Christopher Koos, of Illinois, to be a Director of the Amtra
        1.48        3 rows  To amend the Permanent Electronic Duck Stamp Act of 2013 to 
        1.37        2 rows  David Rosner, of Massachusetts, to be a Member of the Federa
        1.37        2 rows  Rose E. Jenkins, of the District of Columbia, to be a Judge 
        1.36        2 rows  Christopher T. Hanson, of Michigan, to be a Member of the Nu
        1.34        2 rows  Gen. Charles Q. Brown, Jr., in the Air Force, to be General
        1.34        2 rows  Coast Guard Authorization Act
        1.32        2 rows  Autism CARES Act
        1.29        2 rows  John A. Kazen, of Texas, to be United States District Judge 
        1.29        2 rows  Philip Nathan Jefferson, of North Carolina, to be Vice Chair
        1.28        2 rows  Monica M. Bertagnolli, of Massachusetts, to be Director of t

VOTE_QUESTION by rows
       612  On Agreeing to the Amendment
       461  On the Cloture Motion
       435  On the Nomination
       304  On Passage
       188  On Motion to Suspend the Rules and Pass, as Amended
       173  On the Amendment
       169  On Agreeing to the Resolution
       140  On Motion to Suspend the Rules and Pass
       137  On Motion to Recommit
       121  On Ordering the Previous Question
       112  On the Motion to Proceed
       107  On the Motion
        56  On the Joint Resolution
        48  On Cloture on the Motion to Proceed
        37  On Passage of the Bill
        34  On the Motion to Table
        30  On the Motion to Discharge
        28  On Motion to Suspend the Rules and Agree
        20  Election of the Speaker
        14  On Motion to Table

VOTE_QUESTION by dollars
       70.92      612 rows  On Agreeing to the Amendment
       35.35      435 rows  On the Nomination
       33.44      461 rows  On the Cloture Motion
       23.85      140 rows  On Motion to Suspend the Rules and Pass
       23.62      188 rows  On Motion to Suspend the Rules and Pass, as Amended
        9.38      107 rows  On the Motion
        4.06      137 rows  On Motion to Recommit
        3.21      121 rows  On Ordering the Previous Question
        1.80        4 rows  On Motion to Suspend the Rules and Concur in the Senate Amen
        1.72       34 rows  On the Motion to Table
        1.58        7 rows  On the Motion to Recommit
        1.22       37 rows  On Passage of the Bill
        0.95        5 rows  On Motion to Discharge
        0.85        1 rows  On Retaining Division A
        0.69       28 rows  On Motion to Suspend the Rules and Agree
        0.66        2 rows  On the Motion to Refer
        0.55        1 rows  On Motion to Suspend the Rules and Concur in Senate Adt to H
        0.54       10 rows  On Motion to Adjourn
        0.53        2 rows  On the Motion for Attendance
        0.39        1 rows  On Motion to Concur in the Senate Amendment with an Amendmen

_SRC_SHA256 by rows
      3.4K  cd540c94667f2c4e33fdaf0c2b2e1938018044c777477276fbd177ef4f71f233

_SRC_SHA256 by dollars
      170.17     3.4K rows  cd540c94667f2c4e33fdaf0c2b2e1938018044c777477276fbd177ef4f71

## who x when

VOTE_DESC by DATE, dollars = NOMINATE_MID_1
  A bill a bill to increase the supply of   2026:-0.19
  A bill making appropriations for militar  2023:0.14 2024:2.92
  A bill making continuing appropriations   2025:-6.58
  A bill making continuing appropriations   2025:0
  A bill making further consolidated appro  2026:-1.56
  A bill making further continuing appropr  2023:0.83 2024:1.18
  A bill to amend title 38, United States   2023:0.32 2024:7.65
  A bill to amend title 49, United States   2023:1.27 2024:-0.41
  A bill to authorize appropriations for f  2023:0.32
  A bill to provide for reconciliation pur  2025:0.88
  A bill to provide for the regulation of   2025:-0.08
  A bill to reauthorize the Morris K. Udal  2024:1.72
  A bill to reform the Foreign Intelligenc  2024:2.58
  A bill to repeal the authorizations for   2023:-1.83
  A bill to rescind certain budget authori  2025:2.19
  A joint resolution providing for congres  2025:1.52
  A joint resolution providing for congres  2025:-0.13
  A joint resolution to direct the removal  2026:-2.59
  An executive resolution authorizing the   2025:-0.16 2026:0
  An original bill to provide for reconcil  2026:0.65
  Christopher Koos, of Illinois, to be a D  2024:1.49
  Christopher T. Hanson, of Michigan, to b  2024:1.36
  Commerce, Justice, Science; Energy and W  2026:1.52
  David Rosner, of Massachusetts, to be a   2024:1.37
  In the nature of a substitute.            2023:0.60 2024:0.68 2025:-1.84 2026:0.89
  Kurt Campbell, of the District of Columb  2024:1.53
  National Defense Authorization Act        2023:-0.70
  Rose E. Jenkins, of the District of Colu  2024:1.37
  To amend the Permanent Electronic Duck S  2024:1.48
  To improve the bill.                      2023:0.07 2025:-1.22

VOTE_QUESTION by DATE, dollars = NOMINATE_MID_1
  Election of the Speaker                   2023:-0.39 2025:-0.14
  On Agreeing to the Amendment              2023:50.31 2024:13.82 2025:5.50 2026:1.29
  On Agreeing to the Resolution             2023:-1.48 2024:-1.93 2025:-2.01 2026:-0.26
  On Cloture on the Motion to Proceed       2023:-0.16 2024:0.70 2025:-5.36 2026:-1.62
  On Motion to Adjourn                      2023:0.55 2025:-0.03 2026:0.02
  On Motion to Concur in the Senate Amendm  2024:0.39
  On Motion to Discharge                    2025:0.27 2026:0.68
  On Motion to Recommit                     2023:0.52 2024:1.12 2025:0.50 2026:1.92
  On Motion to Suspend the Rules and Agree  2023:0.19 2024:0.37 2025:-0.19 2026:0.32
  On Motion to Suspend the Rules and Concu  2026:0.55
  On Motion to Suspend the Rules and Concu  2024:1.80
  On Motion to Suspend the Rules and Pass   2023:0.64 2024:11.07 2025:9.72 2026:2.42
  On Motion to Suspend the Rules and Pass,  2023:1.29 2024:16.30 2025:1.98 2026:4.05
  On Motion to Table                        2023:-0.24 2024:0.38 2025:-0.28
  On Ordering the Previous Question         2023:1.03 2024:0.62 2025:1.07 2026:0.49
  On Passage                                2023:-3.20 2024:-6.52 2025:-6.66 2026:0.03
  On Passage of the Bill                    2023:1.24 2024:3.51 2025:-3.06 2026:-0.47
  On Retaining Division A                   2026:0.85
  On the Amendment                          2023:-2.67 2024:-0.98 2025:-0.61 2026:1.66
  On the Cloture Motion                     2023:22.91 2024:25.12 2025:-12.20 2026:-2.39
  On the Joint Resolution                   2023:-1.48 2024:-0.11 2025:-0.23 2026:-0.08
  On the Motion                             2023:0.32 2024:3.41 2025:1.75 2026:3.90
  On the Motion for Attendance              2023:0.04 2024:0.49
  On the Motion to Discharge                2023:-1.25 2024:-1.64 2025:-1.59 2026:-3.41
  On the Motion to Proceed                  2023:0.05 2024:2.56 2025:-2.40 2026:-0.13
  On the Motion to Recommit                 2025:1.58
  On the Motion to Refer                    2024:0.66
  On the Motion to Table                    2023:0.98 2024:0.58 2025:-1.04 2026:1.20
  On the Nomination                         2023:25.55 2024:21.23 2025:-8.83 2026:-2.60

## what

CONGRESS: 118 57%, 119 43%

CHAMBER: House 54%, Senate 46%

SESSION: 1 62%, 2 38%

VOTE_RESULT: Passed 31%, Failed 21%, Cloture Motion Agreed to 14%, Nomination Confirmed 14%, Agreed to 6%, Amendment Rejected 5%, Motion to Proceed Agreed to 3%, Motion Rejected 3%, Joint Resolution Passed 2%, Cloture on the Motion to Proce 1%, Bill Passed 1%, Amendment Agreed to 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CONGRESS | category | 2 | 0 | 118 1.9K; 119 1.4K |
| CHAMBER | category | 2 | 0 | House 1.8K; Senate 1.5K |
| ROLLNUMBER | other | 1.2K | 0 | 851 17; 850 17; 849 17; 848 17 |
| DATE | date | 536 | 0 | 2023-09-28 55; 2023-09-27 48; 2023-11-02 34; 2025-06-30 33 |
| SESSION | category | 2 | 0 | 1 2.1K; 2 1.3K |
| CLERK_ROLLNUMBER | other | 709 | 0 | 192 17; 191 17; 190 17; 189 17 |
| YEA_COUNT | other | 387 | 0 | 51 183; 50 161; 52 157; 53 125 |
| NAY_COUNT | other | 341 | 0 | 45 150; 46 141; 47 137; 0 96 |
| NOMINATE_MID_1 | amount | 987 | 0 | 0.0 245; -0.003 135; -0.002 80; -0.004 58 |
| NOMINATE_MID_2 | amount | 1.2K | 0 | 0.0 242; -0.248 93; -1.0 34; -0.247 34 |
| NOMINATE_SPREAD_1 | amount | 1.1K | 0 | 0.0 240; -0.693 129; -0.715 93; -0.692 61 |
| NOMINATE_SPREAD_2 | amount | 1.7K | 0 | 0.0 242; 0.438 37; 0.446 32; 0.444 30 |
| NOMINATE_LOG_LIKELIHOOD | amount | 2.3K | 0 | -0.06 241; 0.0 240; -0.059 48; -0.257 42 |
| BILL_NUMBER | other | 1.4K | 42 | HR1 63; HR21 59; HR2670 43; S2 41 |
| VOTE_RESULT | category | 40 | 0 | Passed 975; Failed 648; Cloture Motion Agreed to 441; Nomination Confirmed 435 |
| VOTE_DESC | who | 1.6K | 657 | A bill to provide for rec 31; A bill making continuing  29; An executive resolution a 26; A joint resolution provid 22 |
| VOTE_QUESTION | who | 58 | 0 | On Agreeing to the Amendm 612; On the Cloture Motion 461; On the Nomination 435; On Passage 304 |
| DTL_DESC | empty | 1 | 3.4K |  |
| _INGESTED_AT | audit | 1 | 0 | 1782772025533315 3.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 86afa55b-d6b2-4dbf-ad65-6 3.4K |
| _SRC_SHA256 | who | 1 | 0 | cd540c94667f2c4e33fdaf0c2 3.4K |
