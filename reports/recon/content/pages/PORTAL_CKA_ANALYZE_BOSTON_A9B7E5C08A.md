# PORTAL_CKA_ANALYZE_BOSTON_A9B7E5C08A

rows 10.0K  columns 22  scan 3.7s

roles: audit 2, category 9, date 6, other 4, who 2

## when

SUBMITTED_DATE
  2018      1.5K  ###########################
  2019      1.6K  ##############################
  2020      1.2K  ######################
  2021      1.2K  ######################
  2022      1.4K  ###########################
  2023      1.1K  ####################
  2024       865  ################
  2025       807  ###############
  2026       300  ######

RECEIVED_DATE
  1801         1  
  2018      1.5K  ###########################
  2019      1.6K  ##############################
  2020      1.1K  #####################
  2021      1.2K  ######################
  2022      1.2K  ######################
  2023      1.0K  ###################
  2024       798  ###############
  2025       806  ###############
  2026       289  #####

HEARING_DATE
  2018       879  #################
  2019      1.6K  ##############################
  2020      1.0K  ###################
  2021      1.3K  ########################
  2022       955  ##################
  2023      1.1K  ####################
  2024       876  #################
  2025       712  ##############
  2026       361  #######

FINAL_DECISION_DATE
  2016         1  
  2018       737  ##############
  2019      1.6K  ##############################
  2020       966  ##################
  2021      1.5K  ###########################
  2022       938  #################
  2023      1.1K  ####################
  2024       998  ###################
  2025       731  ##############
  2026       296  ######

CLOSED_DATE
  2016         1  
  2018       741  ##############
  2019      1.6K  ##############################
  2020       873  ################
  2021      1.6K  ##############################
  2022      1.2K  ######################
  2023      1.1K  #####################
  2024      1.1K  ####################
  2025       818  ###############
  2026       381  #######

INGESTED_AT
  2026     10.0K  ##############################

## who

CONTACT by rows
       545  Jeffrey Drago
       500  Richard Lynds
       201  John Pulgini
       170  Marc LaCasse
       164  Ryan Spitz
       153  Nicholas Zozula
       102  Charles McCarthy
       101  Xhaklina Desmond
        98  John Gorman
        96  Timothy Burke
        94  derric small
        86  TIMOTHY JOHNSON
        76  John Moran
        73  James  Christopher
        71  Ryan Gazda
        68  George Morancy
        63  Timothy Sheehan
        59  Patrick Mahoney Esq.
        57  George Morancy, ESQ
        57  Hezekiah Pratt

SRC_SHA256 by rows
     10.0K  48608bd95bbade7fdf2f2478a700d16208f3e0c02e3f5eda55ebc23240de3243

## who x when

CONTACT by FINAL_DECISION_DATE
  Charles McCarthy                          2019:3 2020:7 2021:29 2022:20 2023:27 2024:6
  George Morancy                            2018:16 2019:34 2020:11 2021:1 2023:1
  George Morancy, ESQ                       2024:22 2025:16 2026:8
  Hezekiah Pratt                            2018:1 2019:34 2020:4 2021:3 2022:1 2023:1 2024:2 2025:2
  James  Christopher                        2020:2 2021:9 2022:11 2023:4 2024:13 2025:16 2026:6
  Jeffrey Drago                             2018:27 2019:114 2020:72 2021:84 2022:71 2023:68 2024:40 2025:27 2026:11
  John Gorman                               2018:70 2019:16 2020:2 2021:2 2022:5
  John Moran                                2018:3 2019:13 2020:11 2021:12 2022:6 2023:18 2024:7 2025:3 2026:3
  John Pulgini                              2018:21 2019:17 2020:25 2021:17 2022:21 2023:17 2024:33 2025:20 2026:6
  Marc LaCasse                              2018:3 2019:40 2020:10 2021:28 2022:19 2023:32 2024:13 2025:8 2026:4
  Nicholas Zozula                           2020:1 2021:36 2022:15 2023:23 2024:33 2025:28 2026:4
  Patrick Mahoney Esq.                      2018:10 2019:39 2020:3 2021:7
  Richard Lynds                             2018:19 2019:72 2020:57 2021:91 2022:53 2023:64 2024:68 2025:20 2026:15
  Ryan Gazda                                2021:20 2022:5 2023:6 2024:7 2025:14 2026:3
  Ryan Spitz                                2021:4 2022:16 2023:38 2024:35 2025:29 2026:23
  TIMOTHY JOHNSON                           2018:5 2019:16 2020:12 2021:16 2022:17 2023:2 2024:5 2025:4 2026:1
  Timothy Burke                             2018:4 2019:21 2020:11 2021:18 2022:4 2023:6 2024:8 2025:7 2026:6
  Timothy Sheehan                           2018:6 2019:24 2020:4 2021:14 2022:7
  Xhaklina Desmond                          2018:2 2021:28 2022:18 2023:19 2024:8 2025:5 2026:1
  derric small                              2021:27 2022:13 2023:18 2024:16 2025:10 2026:2

SRC_SHA256 by FINAL_DECISION_DATE
  48608bd95bbade7fdf2f2478a700d16208f3e0c0  2016:1 2018:737 2019:1.6K 2020:966 2021:1.5K 2022:938 2023:1.1K 2024:998 2025:731 2026:296

## what

STATUS: Appeal Closed 94%, Community Process 3%, Hearing Scheduled 1%, ZBA Decision Finalized 1%, Hearing Concluded 1%, Appeal Submitted 0%, Hearing Rescheduled 0%

APPEAL_TYPE: Zoning 96%, Building 4%

EVER_DEFERRED: N 88%, Y 12%

NUM_DEFERRALS: 0 88%, 1 8%, 2 2%, 3 1%, 4 0%, 5 0%, 6 0%, 9 0%, 7 0%, 10 0%, 11 0%

DECISION: AppProv 52%, Approved 35%, DeniedPrej 5%, Withdrawn 3%, Denied 3%, Withdraw 0%, Void 0%

CITY: Dorchester 22%, Boston 13%, East Boston 11%, South Boston 11%, Roxbury 10%, Jamaica Plain 6%, Roslindale 5%, Brighton 5%, West Roxbury 4%, Charlestown 4%, Hyde Park 4%, Mattapan 3%

ZIP: 02128 15%, 02127 15%, 02124 10%, 02130 8%, 02125 8%, 02131 7%, 02118 7%, 02136 6%, 02119 6%, 02132 6%, 02135 6%, 02121 6%

WARD: 01 15%, 18 10%, 06 10%, 20 9%, 03 8%, 05 8%, 07 8%, 14 7%, 16 7%, 22 6%, 19 6%, 02 6%

ZONING_DISTRICT: Dorchester Neighborhood 18%, East Boston Neighborhood 13%, South Boston Neighborhood 11%, Roxbury Neighborhood 9%, Allston/Brighton Neighborhood 8%, Jamaica Plain Neighborhood 7%, South End Neighborhood 6%, Boston Proper 6%, Roslindale Neighborhood 6%, Hyde Park Neighborhood 5%, Greater Mattapan Neighborhood 5%, West Roxbury Neighborhood 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ADDRESS | other | 6.4K | 0 | 537A to 537 Columbus AV R 53; 9 Glencoe ST Brighton 021 53; 97 Woodrow AV Dorchester  52; 441 to 445 Hanover ST Bos 52 |
| STATUS | category | 7 | 0 | Appeal Closed 9.4K; Community Process 346; Hearing Scheduled 67; ZBA Decision Finalized 63 |
| PARENT_APNO | other | 9.1K | 213 | ERT602665 50; COO1689778 50; ALT793801 50; ALT778805 50 |
| BOA_APNO | other | 7.4K | 0 | BOA814667 53; BOA812645 52; BOA812908 52; BOA813877 52 |
| APPEAL_TYPE | category | 2 | 0 | Zoning 9.6K; Building 424 |
| CONTACT | who | 2.8K | 0 | Jeffrey Drago 545; Richard Lynds 500; John Pulgini 201; Marc LaCasse 170 |
| SUBMITTED_DATE | date | 2.0K | 81 | 2018-09-18 107; 2022-01-06 98; 2019-04-17 79; 2018-05-22 69 |
| RECEIVED_DATE | date | 1.8K | 532 | 2018-09-18 105; 2019-04-17 78; 2018-05-22 67; 2018-07-26 64 |
| HEARING_DATE | date | 303 | 1.3K | 2018-10-16 131; 2019-06-11 102; 2019-08-13 94; 2019-03-12 89 |
| EVER_DEFERRED | category | 3 | 1.3K | N 7.7K; Y 1.0K |
| NUM_DEFERRALS | category | 12 | 1.3K | 0 7.7K; 1 667; 2 211; 3 74 |
| FINAL_DECISION_DATE | date | 526 | 1.2K | 2019-06-14 164; 2019-01-18 113; 2019-11-01 110; 2019-10-11 109 |
| DECISION | category | 9 | 1.2K | AppProv 4.6K; Approved 3.1K; DeniedPrej 457; Withdrawn 294 |
| CLOSED_DATE | date | 770 | 573 | 2019-06-14 167; 2022-02-11 160; 2019-01-18 116; 2019-11-01 113 |
| CITY | category | 18 | 0 | Dorchester 2.1K; Boston 1.2K; East Boston 1.1K; South Boston 1.1K |
| ZIP | category | 29 | 0 | 02128 1.1K; 02127 1.1K; 02124 713; 02130 564 |
| WARD | category | 22 | 0 | 01 1.1K; 18 739; 06 726; 20 670 |
| ZONING_DISTRICT | category | 35 | 17 | Dorchester Neighborhood 1.6K; East Boston Neighborhood 1.1K; South Boston Neighborhood 971; Roxbury Neighborhood 794 |
| PROJECT_DESCRIPTION | other | 8.7K | 216 | ERECT SINGLE FAMILY DWELL 51; ERECT 2 FAMILY DWELLING 51; erect new three family wi 50; Three Family DwellingCert 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:33:07.71950 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0a7f35f4-c182-452c-b531-4 10.0K |
| SRC_SHA256 | who | 1 | 0 | 48608bd95bbade7fdf2f2478a 10.0K |
