# PORTAL_CKA_ANALYZE_BOSTON_94AE63A33F

rows 10.0K  columns 24  scan 4.7s

roles: amount 2, audit 2, category 8, date 3, who 10

## when

ADD_DATE
  2022      3.0K  #######################
  2023      3.9K  ##############################
  2024      3.0K  #######################
  2025        12  

CONTRIBUTION_DATE
  2022       256  #######################
  2023       335  ##############################
  2024       142  #############
  2025         1  

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CONTRIBUTION_AMOUNT | 3.5K | 0 | 0 | 1.0K | 20.0K | 274.8K |
| AMOUNT | 3.0K | 0 | 500 | 36.8K | 2.00M | 16.04M |

## who

LOBBYIST_CLIENT_NAME by rows
       118  A Better City
       118  Michael Vaughan & Christine McMahon
       110  NAIOP Massachusetts The Commercial Real Estate Development Association
        92  The Greater Boston Chamber of Commerce
        57  Rasky Partners
        54  Nauset Strategies
        49  Michael Vaughan
        40  Benchmark Strategies
        39  John Harrington
        39  Amazon.com
        37  Issues Management Group Public Affairs, LLC
        37  Luz Arregoces
        37  New England Aquarium
        35  Christine McMahon
        33  ACLU of MA
        33  Tishman Speyer Properties, L.P.
        32  DoorDash
        32  Harvard University
        30  Procter & Gamble
        29  Boch Center

LOBBYIST_CLIENT_NAME by dollars
           0       10 rows  Jeff Terrey
           0        6 rows  gopuff
           0        3 rows  Jennifer Jackson
           0       29 rows  Boch Center
           0        8 rows  NAIOP Massachusetts, The Commercial Real Estate Development 
           0        4 rows  Angela Holm
           0       10 rows  RMR Group LLC
           0        6 rows  Serlin Haley LLP
           0       49 rows  Michael Vaughan
           0       21 rows  Paul Scapicchio 
           0       26 rows  Conference of Boston Teaching Hospitals
           0        6 rows  Joe Rull
           0        1 rows  ACLU MA
           0        1 rows  Molly Sullivan 
           0      110 rows  NAIOP Massachusetts The Commercial Real Estate Development A
           0       10 rows  Ariella Hellman
           0        3 rows  Bird Rides, Inc.
           0       10 rows  Tamara Small
           0       12 rows  GBREB
           0        9 rows  Verizon

SUBJECT_NAME by rows
       124  General
        97  RE Development
        92  Real Estate
        30  Cargo Ventures LLC
        29  Permitting
        29  Cultural Institutions
        28  Allston I-90 Multimodal Project
        26  Other
        25  Real Estate 
        25  Boston Cannabis Board
        22  Climate Ready Boston
        21  Harbor Garage
        19  Dell
        19  Lobbying Issue
        19  BERDO
        19  South Boston Seaport Transit Plan
        19  Street Furniture contract
        19  Executive decisions/approval of decisions concerning real property
        18  Boch Center
        17  Article 80 Review

SUBJECT_NAME by dollars
           0        2 rows  Leslie Credle
           0        3 rows  City Contracting
           0        7 rows  Sonder
           0        5 rows  Street Furniture Contract
           0        1 rows  Regulations implementing Boston local wetlands ordinance
           0        1 rows  Art 80 Large Project
           0        8 rows  Housing
           0        1 rows  fines and fees legislation
           0        1 rows  Tufts Medical Center
           0        1 rows  CoB/MBTA/MASCO re: Discuss LMA Study
           0        1 rows  one kenmore square redevelopment
           0        1 rows  Municipal fiber network
           0        1 rows  Marijuana Facility 
           0        1 rows  DEP Settlement
           0        8 rows  MA Site Assessment
           0        2 rows  BPDA net zero 
           0        9 rows  Berklee College of Music Institutional Master Plan
           0        1 rows  Marijuana Dispensary Permitting & Licensing
           0        1 rows  Miriama White-Hammond
           0        3 rows  Landmarks 

FULL_NAME by rows
       262  Nauset Strategies
       141  Tishman Speyer Properties, L.P.
       123  Christine McMahon
       114  Kearney Donovan & McGee,LLC
        93  Rasky Partners
        88  Patrick Bench Benchmark Strategies
        84  Lawrence DiCara
        77  Greater Boston Chamber of Commerce
        69  Joyce Strategies, LLC
        66  Tamara Small
        59  Anastasia Daou
        59  New England Aquarium
        58  Jeff Terrey
        51  Kade Crockford
        50  Michael OBrien
        50  ACLU of Massachusetts
        47  Abundant Housing MA, Inc. Jesse Kanson-Benanav
        47  William F. Coyne, Jr., Esq. PC
        46  Preti Strategies
        45  Patricia McMullin

FULL_NAME by dollars
       37.5K       11 rows  Nicole Green
       21.2K       33 rows  Charlene Rideout
       20.8K       34 rows  Daniel R. Cullinane
       13.2K       50 rows  Michael OBrien
       11.7K      262 rows  Nauset Strategies
       11.5K       29 rows  Jaimie Unite here Local 26
       10.2K       21 rows  Rockpoint Group, L.L.C.
        8.0K       16 rows  McDermott Ventures, LLC
        7.5K       20 rows  Thomas O'Brien
        6.2K       84 rows  Lawrence DiCara
        6.0K       22 rows  William Dillon
        5.5K       28 rows  John Nucci
        5.2K      123 rows  Christine McMahon
        4.9K       22 rows  Mark McGowan
        4.8K       22 rows  Douglas Manz
        3.6K       69 rows  Joyce Strategies, LLC
        3.4K       33 rows  Eugene O'Flaherty
        3.4K       47 rows  William F. Coyne, Jr., Esq. PC
        3.0K       16 rows  Christopher Jeffries
        3.0K       17 rows  Boston Firefighters Local 718

RECIPIENT_NAME by rows
       165  Michelle Wu
        55  Ed Flynn
        31  Erin Murphy
        26  Sharon Durkan
        23  John Fitzgerald
        22  Gabriela Coletta
        17  Ruthzee Louijeune
        16  Michael Flaherty
        13  Brian Worrell
        13  Henry Santana
        11  n/a
        11  Liz Breadon
        10  Edward Flynn
        10  Frank Baker
         9  Mayor Michelle Wu
         8  Matt Patton
         8  John FitzGerald
         7  N/A
         6  Edward Michael Flynn
         6  Erin Murphy Committee

RECIPIENT_NAME by dollars
       49.3K      165 rows  Michelle Wu
       25.9K       23 rows  John Fitzgerald
       25.4K       26 rows  Sharon Durkan
       22.5K        3 rows  The Novus Group
       15.0K        1 rows  The Novus Group 
       13.5K       55 rows  Ed Flynn
        7.7K        6 rows  Andrea Campbell
        6.8K       31 rows  Erin Murphy
        5.8K       22 rows  Gabriela Coletta
        4.7K       16 rows  Michael Flaherty
        3.9K       17 rows  Ruthzee Louijeune
        3.6K        6 rows  Maura Healey
        3.4K       10 rows  Edward Flynn
        3.3K       13 rows  Brian Worrell
        2.9K        1 rows  Jake Auchincloss
        2.5K        3 rows  William King
        2.4K       10 rows  Frank Baker
        2.4K        9 rows  Mayor Michelle Wu
        2.0K        2 rows  Mayor Michelle Wu 
        2.0K        3 rows  Mayor Wu

## who x when

LOBBYIST_CLIENT_NAME by ADD_DATE, dollars = CONTRIBUTION_AMOUNT
  A Better City                             2022:31 2023:50 2024:37
  ACLU of MA                                2023:13 2024:20
  Amazon.com                                2022:10 2023:17 2024:12
  Angela Holm                               2022:3 2024:1
  Benchmark Strategies                      2022:12 2023:19 2024:9
  Boch Center                               2022:8 2023:12 2024:9
  Christine McMahon                         2022:15 2023:12 2024:8
  Conference of Boston Teaching Hospitals   2022:6 2023:10 2024:10
  DoorDash                                  2022:9 2023:14 2024:9
  Harvard University                        2022:9 2024:23
  Issues Management Group Public Affairs,   2022:8 2023:22 2024:7
  Jeff Terrey                               2022:3 2023:4 2024:3
  Jennifer Jackson                          2022:1 2023:1 2024:1
  Joe Rull                                  2022:3 2023:3
  John Harrington                           2022:18 2023:14 2024:7
  Luz Arregoces                             2023:21 2024:16
  Michael Vaughan                           2022:17 2023:20 2024:12
  Michael Vaughan & Christine McMahon       2022:36 2023:47 2024:35
  NAIOP Massachusetts The Commercial Real   2022:14 2023:59 2024:37
  NAIOP Massachusetts, The Commercial Real  2022:8
  Nauset Strategies                         2022:17 2023:21 2024:16
  New England Aquarium                      2023:21 2024:16
  Paul Scapicchio                           2022:10 2023:11
  Procter & Gamble                          2022:7 2023:14 2024:9
  RMR Group LLC                             2022:3 2023:4 2024:3
  Rasky Partners                            2022:18 2023:21 2024:18
  Serlin Haley LLP                          2022:4 2023:2
  The Greater Boston Chamber of Commerce    2022:27 2023:39 2024:26
  Tishman Speyer Properties, L.P.           2022:21 2023:12
  gopuff                                    2022:2 2023:3 2024:1

SUBJECT_NAME by ADD_DATE, dollars = CONTRIBUTION_AMOUNT
  Allston I-90 Multimodal Project           2022:7 2023:12 2024:9
  Art 80 Large Project                      2022:1
  Article 80 Review                         2022:4 2023:8 2024:5
  BERDO                                     2022:11 2023:7 2024:1
  Boch Center                               2022:5 2023:7 2024:6
  Boston Cannabis Board                     2022:6 2023:13 2024:6
  Cargo Ventures LLC                        2022:9 2023:12 2024:9
  City Contracting                          2022:3
  Climate Ready Boston                      2022:6 2023:8 2024:8
  CoB/MBTA/MASCO re: Discuss LMA Study      2022:1
  Cultural Institutions                     2023:14 2024:15
  Dell                                      2022:4 2023:9 2024:6
  Executive decisions/approval of decision  2022:8 2023:8 2024:3
  General                                   2022:36 2023:48 2024:40
  Harbor Garage                             2022:7 2023:8 2024:6
  Housing                                   2022:5 2023:2 2024:1
  Leslie Credle                             2022:2
  Lobbying Issue                            2022:8 2023:4 2024:7
  Other                                     2022:9 2023:17
  Permitting                                2022:16 2023:10 2024:3
  RE Development                            2022:22 2023:39 2024:36
  Real Estate                               2022:18 2023:38 2024:36
  Real Estate                               2022:20 2023:3 2024:2
  Regulations implementing Boston local we  2022:1
  Sonder                                    2022:5 2023:2
  South Boston Seaport Transit Plan         2022:6 2023:8 2024:5
  Street Furniture Contract                 2022:4 2023:1
  Street Furniture contract                 2022:5 2023:8 2024:6
  Tufts Medical Center                      2022:1
  fines and fees legislation                2022:1

## what

CATEGORY: CCLOBBY 55%, CCCLIENT 25%, CCENTITY 20%

YEAR: 2022 41%, 2023 39%, 2024 19%

QUARTER: 2nd 30%, 1st 29%, 3rd 21%, 4th 20%

QUARTER_ACTIVITY: N 52%, Y 47%, NC 0%

TYPE: Contribution 35%, Lobbyist Activity 34%, Client/Entity Activity 30%

SUBJECT_TYPE: AdminAct 36%, Other 33%, Decision 22%, LegAct 7%, PoL 3%

SUPPORT_OPPOSE: S 90%, O 10%

INCURRED_OR_PAID: PAID 87%, INC 13%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CCL | who | 611 | 0 | CCL392779 152; CCL392258 126; CCL392781 116; CCL392905 116 |
| CATEGORY | category | 3 | 0 | CCLOBBY 5.5K; CCCLIENT 2.5K; CCENTITY 2.0K |
| FULL_NAME | who | 560 | 0 | Nauset Strategies 265; Tishman Speyer Properties 143; Christine McMahon 126; Kearney Donovan & McGee,L 116 |
| ADD_DATE | date | 9.6K | 0 | 2024-10-08 14:52:48.757+0 50; 2024-10-08 14:52:48.74+00 50; 2024-10-08 14:47:19.3+00 50; 2024-10-08 14:47:19.27+00 50 |
| YEAR | category | 3 | 0 | 2022 4.1K; 2023 3.9K; 2024 1.9K |
| QUARTER | category | 4 | 0 | 2nd 3.0K; 1st 2.9K; 3rd 2.1K; 4th 2.0K |
| QUARTER_ACTIVITY | category | 3 | 0 | N 5.2K; Y 4.7K; NC 36 |
| TYPE | category | 3 | 0 | Contribution 3.5K; Lobbyist Activity 3.4K; Client/Entity Activity 3.0K |
| CONTRIBUTION_DATE | date | 363 | 9.3K | 2024-04-24 13; 2023-10-17 9; 2023-07-11 9; 2023-09-18 9 |
| CONTRIBUTION_AMOUNT | amount | 32 | 6.5K | 0.00 2.8K; 200.00 357; 100.00 106; 500.00 56 |
| RECIPIENT_NAME | who | 208 | 9.2K | Michelle Wu 165; Ed Flynn 55; Erin Murphy 31; Sharon Durkan 26 |
| INCUMBENT_CANDIDATE | who | 116 | 9.3K | City Councilor 274; Mayor 184; City Council 36; City Council Candidate 18 |
| LOBBYIST_CLIENT_NAME | who | 713 | 5.5K | A Better City 119; Michael Vaughan & Christi 119; NAIOP Massachusetts The C 110; The Greater Boston Chambe 92 |
| LOBBYIST_CLIENT_CCL | who | 593 | 5.5K | n/a 239; CCL 393519 118; CCL392781 + CCL392258 92; CCL392779 61 |
| SUBJECT_NAME | who | 613 | 8.0K | General 124; RE Development 98; Real Estate 92; Cultural Institutions 31 |
| SUBJECT_TYPE | category | 7 | 8.0K | AdminAct 697; Other 640; Decision 436; LegAct 132 |
| SUPPORT_OPPOSE | category | 3 | 8.1K | S 1.8K; O 194 |
| SUPPORT_OPPOSE_STATEMENT | who | 1.3K | 7.6K | No activity to report. 82; No activity 44; N/A 36; Address real estate issue 27 |
| ISSUE_DESCRIPTION | who | 1.2K | 7.8K | Address real estate issue 66; Support Article 80 proces 29; Issues related to real es 29; Address real estate issue 28 |
| INCURRED_OR_PAID | category | 4 | 7.8K | PAID 1.9K; INC 285 |
| AMOUNT | amount | 372 | 7.0K | 0.0 1.3K; 3000.0 186; 15000.0 98; 7500.0 74 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:40:49.24433 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | d853705a-905b-48e7-aa14-d 10.0K |
| SRC_SHA256 | who | 1 | 0 | 5f2ae5b1785228e3cba28672d 10.0K |
