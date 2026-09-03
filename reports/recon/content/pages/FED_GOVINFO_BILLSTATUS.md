# FED_GOVINFO_BILLSTATUS

rows 36.5K  columns 17  scan 3.7s

roles: audit 2, category 4, date 2, other 4, who 5

## when

INTRODUCED_DATE
  2023     12.2K  ##############################
  2024      7.1K  #################
  2025     12.4K  ##############################
  2026      4.8K  ############

LATEST_ACTION_DATE
  2023     10.7K  ############################
  2024      8.6K  ######################
  2025     11.5K  ##############################
  2026      5.7K  ###############

## who

SPONSOR_NAME by rows
       720  Rep. Biggs, Andy [R-AZ-5]
       299  Sen. Scott, Rick [R-FL]
       288  Sen. Markey, Edward J. [D-MA]
       270  Sen. Rubio, Marco [R-FL]
       266  Sen. Cruz, Ted [R-TX]
       260  Sen. Booker, Cory A. [D-NJ]
       258  Sen. Durbin, Richard J. [D-IL]
       255  Sen. Lee, Mike [R-UT]
       247  Sen. Cornyn, John [R-TX]
       244  Sen. Peters, Gary C. [D-MI]
       243  Sen. Klobuchar, Amy [D-MN]
       234  Sen. Blackburn, Marsha [R-TN]
       221  Del. Norton, Eleanor Holmes [D-DC-At Large]
       213  Sen. Blumenthal, Richard [D-CT]
       209  Sen. Merkley, Jeff [D-OR]
       205  Sen. Cortez Masto, Catherine [D-NV]
       201  Sen. Cassidy, Bill [R-LA]
       200  Sen. Padilla, Alex [D-CA]
       189  Sen. Shaheen, Jeanne [D-NH]
       185  Rep. Neguse, Joe [D-CO-2]

SPONSOR_BIOGUIDE by rows
       720  B001302
       299  S001217
       288  M000133
       270  R000595
       266  C001098
       260  B001288
       258  D000563
       255  L000577
       247  C001056
       244  P000595
       243  K000367
       234  B001243
       225  N000147
       213  B001277
       209  M001176
       205  C001113
       201  C001075
       200  P000145
       189  S001181
       185  N000191

N_COSPONSORS by rows
      7.3K  0
      6.8K  1
      3.1K  2
      2.7K  3
      2.0K  5
      1.7K  4
      1.2K  6
      1.1K  7
       865  8
       750  9
       676  10
       582  11
       538  12
       479  13
       384  14
       373  15
       336  16
       333  17
       294  18
       291  19

LATEST_ACTION_TEXT by rows
      2.2K  Referred to the House Committee on the Judiciary.
      1.5K  Referred to the Subcommittee on Health.
      1.5K  Read twice and referred to the Committee on Finance.
      1.4K  Referred to the House Committee on Ways and Means.
      1.4K  Referred to the House Committee on Energy and Commerce.
      1.3K  Read twice and referred to the Committee on Health, Education, Labor, 
      1.1K  Read twice and referred to the Committee on the Judiciary.
      1.0K  Referred to the House Committee on Foreign Affairs.
       973  Referred to the House Committee on Financial Services.
       868  Referred to the House Committee on Education and the Workforce.
       708  Read twice and referred to the Committee on Commerce, Science, and Tra
       686  Read twice and referred to the Committee on Banking, Housing, and Urba
       645  Referred to the House Committee on Education and Workforce.
       642  Read twice and referred to the Committee on Homeland Security and Gove
       636  Referred to the House Committee on Armed Services.
       633  Read twice and referred to the Committee on Agriculture, Nutrition, an
       619  Referred to the House Committee on Oversight and Accountability.
       606  Referred to the House Committee on Natural Resources.
       560  Referred to the House Committee on Oversight and Government Reform.
       489  Read twice and referred to the Committee on Foreign Relations.

## who x when

SPONSOR_NAME by LATEST_ACTION_DATE
  Del. Norton, Eleanor Holmes [D-DC-At Lar  2023:77 2024:51 2025:69 2026:24
  Rep. Biggs, Andy [R-AZ-5]                 2023:589 2024:23 2025:97 2026:11
  Rep. Neguse, Joe [D-CO-2]                 2023:67 2024:40 2025:63 2026:15
  Sen. Blackburn, Marsha [R-TN]             2023:47 2024:54 2025:108 2026:25
  Sen. Blumenthal, Richard [D-CT]           2023:51 2024:48 2025:80 2026:34
  Sen. Booker, Cory A. [D-NJ]               2023:105 2024:51 2025:66 2026:38
  Sen. Cassidy, Bill [R-LA]                 2023:50 2024:45 2025:87 2026:19
  Sen. Cornyn, John [R-TX]                  2023:52 2024:66 2025:87 2026:42
  Sen. Cortez Masto, Catherine [D-NV]       2023:54 2024:44 2025:62 2026:45
  Sen. Cruz, Ted [R-TX]                     2023:83 2024:59 2025:96 2026:28
  Sen. Durbin, Richard J. [D-IL]            2023:71 2024:58 2025:78 2026:51
  Sen. Klobuchar, Amy [D-MN]                2023:94 2024:59 2025:75 2026:15
  Sen. Lee, Mike [R-UT]                     2023:53 2024:76 2025:93 2026:33
  Sen. Markey, Edward J. [D-MA]             2023:88 2024:55 2025:94 2026:51
  Sen. Merkley, Jeff [D-OR]                 2023:59 2024:42 2025:70 2026:38
  Sen. Padilla, Alex [D-CA]                 2023:56 2024:49 2025:64 2026:31
  Sen. Peters, Gary C. [D-MI]               2023:73 2024:89 2025:58 2026:24
  Sen. Rubio, Marco [R-FL]                  2023:185 2024:85
  Sen. Scott, Rick [R-FL]                   2023:84 2024:44 2025:117 2026:54
  Sen. Shaheen, Jeanne [D-NH]               2023:57 2024:39 2025:55 2026:38

SPONSOR_BIOGUIDE by LATEST_ACTION_DATE
  B001243                                   2023:47 2024:54 2025:108 2026:25
  B001277                                   2023:51 2024:48 2025:80 2026:34
  B001288                                   2023:105 2024:51 2025:66 2026:38
  B001302                                   2023:589 2024:23 2025:97 2026:11
  C001056                                   2023:52 2024:66 2025:87 2026:42
  C001075                                   2023:50 2024:45 2025:87 2026:19
  C001098                                   2023:83 2024:59 2025:96 2026:28
  C001113                                   2023:54 2024:44 2025:62 2026:45
  D000563                                   2023:71 2024:58 2025:78 2026:51
  K000367                                   2023:94 2024:59 2025:75 2026:15
  L000577                                   2023:53 2024:76 2025:93 2026:33
  M000133                                   2023:88 2024:55 2025:94 2026:51
  M001176                                   2023:59 2024:42 2025:70 2026:38
  N000147                                   2023:77 2024:51 2025:73 2026:24
  N000191                                   2023:67 2024:40 2025:63 2026:15
  P000145                                   2023:56 2024:49 2025:64 2026:31
  P000595                                   2023:73 2024:89 2025:58 2026:24
  R000595                                   2023:185 2024:85
  S001181                                   2023:57 2024:39 2025:55 2026:38
  S001217                                   2023:84 2024:44 2025:117 2026:54

## what

CONGRESS: 118 53%, 119 47%

BILL_TYPE: HR 55%, S 29%, HRES 8%, SRES 5%, HJRES 1%, SJRES 1%, HCONRES 1%, SCONRES 0%

LAW_TYPE: Public Law 99%, Private Law 1%

ACTION_TYPES: IntroReferral 70%, Committee|IntroReferral 18%, Floor|IntroReferral 3%, Calendars|Committee|IntroRefer 3%, Calendars|Committee|Floor|Intr 3%, Committee|Discharge|Floor|Intr 1%, Committee|Floor|IntroReferral 1%, BecameLaw|Calendars|Committee| 0%, Calendars|Committee|Discharge| 0%, BecameLaw|Committee|Discharge| 0%, Floor 0%, Calendars|Committee|Discharge| 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CONGRESS | category | 2 | 0 | 118 19.3K; 119 17.1K |
| BILL_TYPE | category | 8 | 0 | HR 20.1K; S 10.6K; HRES 3.0K; SRES 1.7K |
| BILL_NUMBER | other | 10.5K | 0 | 795 183; 756 183; 760 183; 788 183 |
| INTRODUCED_DATE | date | 697 | 0 | 2023-03-29 612; 2025-01-03 315; 2023-07-27 305; 2025-04-10 303 |
| TITLE | other | 27.0K | 0 | Electing Members to certa 193; Directing the President,  188; A joint resolution to dir 186; An executive resolution a 184 |
| SPONSOR_BIOGUIDE | who | 634 | 0 | B001302 720; S001217 346; M000133 335; R000595 317 |
| SPONSOR_NAME | who | 677 | 0 | Rep. Biggs, Andy [R-AZ-5] 720; Sen. Scott, Rick [R-FL] 346; Sen. Markey, Edward J. [D 335; Sen. Rubio, Marco [R-FL] 317 |
| LAW_TYPE | category | 3 | 36.1K | Public Law 373; Private Law 2 |
| LAW_NUMBER | other | 377 | 36.1K | 119-2 3; 119-1 3; 119-47 2; 119-20 2 |
| ACTION_TYPES | category | 42 | 5 | IntroReferral 25.2K; Committee/IntroReferral 6.6K; Floor/IntroReferral 1.1K; Calendars/Committee/Intro 1.1K |
| N_ACTIONS | other | 81 | 0 | 3 12.9K; 2 10.4K; 4 5.7K; 5 2.0K |
| LATEST_ACTION_DATE | date | 855 | 5 | 2024-12-17 918; 2023-03-29 424; 2026-06-24 286; 2025-04-10 278 |
| LATEST_ACTION_TEXT | who | 5.3K | 5 | Referred to the House Com 2.2K; Referred to the Subcommit 1.5K; Read twice and referred t 1.5K; Referred to the House Com 1.4K |
| N_COSPONSORS | who | 256 | 0 | 0 7.3K; 1 6.8K; 2 3.1K; 3 2.7K |
| _INGESTED_AT | audit | 1 | 0 | 1782777303465989 36.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | eb8d043a-6281-4669-adba-c 36.5K |
| _SRC_SHA256 | who | 1 | 0 | 74d92c6f5ab59976d6d965fc6 36.5K |
