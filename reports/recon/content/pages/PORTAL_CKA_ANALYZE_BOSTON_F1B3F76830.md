# PORTAL_CKA_ANALYZE_BOSTON_F1B3F76830

rows 10.0K  columns 27  scan 4.8s

roles: amount 2, audit 2, category 5, date 2, id 1, other 11, state 1, who 4

## when

STATUS_DTTM
  2015      1.5K  ##############################
  2016       960  ###################
  2017       954  ###################
  2018       784  ################
  2019       933  ###################
  2020       731  ###############
  2021       688  ##############
  2022       904  ##################
  2023       657  #############
  2024       848  #################
  2025       675  #############
  2026       358  #######

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 9.9K | 42.23 | 42.33 | 42.38 | 42.39 | 420.8K |
| LONGITUDE | 9.9K | -71.18 | -71.08 | -71.01 | -71 | -706.7K |

## who

VIOLATION_STREET by rows
       224  Washington
       198  Blue Hill
       139  Beacon
       109  Commonwealth
       103  Marlborough
        97  Dorchester
        87  Columbia
        86  Harrison
        84  Tremont
        78  Centre
        76  River
        75  Broadway
        73  Massachusetts
        70  Hyde Park
        65  Bowdoin
        64  Saratoga
        62  Harvard
        60  Adams
        57  Newbury
        55  Bennington

VIOLATION_STREET by dollars
        9.3K      224 rows  Washington
        8.4K      198 rows  Blue Hill
        5.8K      139 rows  Beacon
        4.6K      109 rows  Commonwealth
        4.4K      103 rows  Marlborough
        4.1K       97 rows  Dorchester
        3.7K       87 rows  Columbia
        3.6K       86 rows  Harrison
        3.6K       84 rows  Tremont
        3.3K       78 rows  Centre
        3.2K       76 rows  River
        3.2K       75 rows  Broadway
        3.0K       73 rows  Massachusetts
        3.0K       70 rows  Hyde Park
        2.7K       64 rows  Saratoga
        2.7K       65 rows  Bowdoin
        2.6K       62 rows  Harvard
        2.5K       60 rows  Adams
        2.4K       57 rows  Newbury
        2.3K       55 rows  Bennington

CONTACT_CITY by rows
      1.4K  BOSTON
      1.3K  DORCHESTER
       709  Boston
       453  Dorchester
       349  HYDE PARK
       324  EAST BOSTON
       303  ROXBURY
       265  SOUTH BOSTON
       250  MATTAPAN
       190  BRIGHTON
       177  JAMAICA PLAIN
       170  WEST ROXBURY
       169  ROSLINDALE
       136  CHARLESTOWN
       119  Quincy
       111  East Boston
       104  ALLSTON
       100  Roxbury
       100  BROOKLINE
        95  QUINCY

CONTACT_CITY by dollars
       57.8K     1.4K rows  BOSTON
       53.8K     1.3K rows  DORCHESTER
       29.3K      709 rows  Boston
       19.1K      453 rows  Dorchester
       14.7K      349 rows  HYDE PARK
       13.6K      324 rows  EAST BOSTON
       12.8K      303 rows  ROXBURY
       11.2K      265 rows  SOUTH BOSTON
       10.6K      250 rows  MATTAPAN
        7.9K      190 rows  BRIGHTON
        7.5K      177 rows  JAMAICA PLAIN
        7.1K      170 rows  WEST ROXBURY
        7.1K      169 rows  ROSLINDALE
        5.7K      136 rows  CHARLESTOWN
        5.0K      119 rows  Quincy
        4.7K      111 rows  East Boston
        4.4K      104 rows  ALLSTON
        4.2K      100 rows  Roxbury
        4.2K      100 rows  BROOKLINE
        4.0K       95 rows  QUINCY

DESCRIPTION by rows
      2.9K  Failure to Obtain Permit
      1.9K  Unsafe and Dangerous
      1.4K  Maintenance
       731  Testing & Certification
       636  Unsafe Structures
       367  Failed to comply w permit term
       253  Right of Entry
       181  Protection of Adj. Property
       143  Certificate of Occupancy
        96  Building or Use of Premise req
        92  Periodic Inspections
        90  No use of premises permit:
        60  Fire Protection Systems
        56  Inspections
        44  Maintenance of Means of Egress
        42  Suspension or Revocation
        41  Permits
        40  Means of Egress
        39  Locks and Latches
        37  Failure to secure permit

DESCRIPTION by dollars
      121.1K     2.9K rows  Failure to Obtain Permit
       80.1K     1.9K rows  Unsafe and Dangerous
       59.9K     1.4K rows  Maintenance
       30.7K      731 rows  Testing & Certification
       26.8K      636 rows  Unsafe Structures
       15.5K      367 rows  Failed to comply w permit term
       10.7K      253 rows  Right of Entry
        7.6K      181 rows  Protection of Adj. Property
        6.0K      143 rows  Certificate of Occupancy
        4.1K       96 rows  Building or Use of Premise req
        3.9K       92 rows  Periodic Inspections
        3.8K       90 rows  No use of premises permit:
        2.5K       60 rows  Fire Protection Systems
        2.4K       56 rows  Inspections
        1.9K       44 rows  Maintenance of Means of Egress
        1.8K       42 rows  Suspension or Revocation
        1.7K       40 rows  Means of Egress
        1.7K       41 rows  Permits
        1.6K       39 rows  Locks and Latches
        1.6K       37 rows  Failure to secure permit

SRC_SHA256 by rows
     10.0K  ea50b0fee050e578a7b7059849db3494d9989a0809563bd336c2f20bcdc473dd

SRC_SHA256 by dollars
      420.8K    10.0K rows  ea50b0fee050e578a7b7059849db3494d9989a0809563bd336c2f20bcdc4

## who x when

VIOLATION_STREET by STATUS_DTTM, dollars = LATITUDE
  Adams                                     2015:1.1K 2017:84.58 2018:465.29 2019:253.93 2020:84.70 2021:169.16 2022:42.30 2023:253.76 2025:126.88
  Beacon                                    2015:804.72 2016:635.29 2017:508.22 2018:677.65 2019:550.49 2020:381.15 2021:254.01 2022:169.31 2023:931.73 2024:719.80 2025:169.31 2026:42.35
  Bennington                                2015:254.30 2016:211.90 2017:169.53 2018:84.76 2019:466.19 2020:169.53 2021:211.90 2022:254.28 2023:508.59
  Blue Hill                                 2015:930.68 2016:803.65 2017:380.59 2018:465.30 2019:719.20 2020:930.65 2021:972.81 2022:465.23 2023:507.42 2024:845.91 2025:1.1K 2026:296.14
  Bowdoin                                   2015:296.23 2016:380.76 2017:169.22 2018:211.51 2019:465.59 2020:169.29 2021:42.31 2022:338.61 2023:42.30 2024:253.90 2025:296.26 2026:42.31
  Broadway                                  2015:127.02 2016:211.70 2017:508.08 2018:169.36 2019:465.74 2020:169.36 2021:211.70 2022:127.02 2023:381.06 2024:550.42 2025:254.04
  Centre                                    2015:634.49 2016:211.49 2017:465.27 2018:549.70 2019:126.95 2020:253.86 2021:296.17 2022:338.41 2023:126.93 2024:126.92 2025:84.61 2026:84.60
  Columbia                                  2015:296.22 2016:211.59 2017:888.60 2018:169.26 2019:126.95 2020:465.52 2021:169.25 2022:338.52 2023:465.49 2024:211.59 2025:296.24 2026:42.32
  Commonwealth                              2015:846.96 2016:423.47 2017:338.78 2018:84.70 2019:465.85 2020:381.14 2021:211.75 2022:254.10 2023:719.88 2024:381.11 2025:381.13 2026:127.05
  Dorchester                                2015:761.39 2016:423.09 2017:296.18 2018:126.96 2019:169.17 2020:169.23 2021:423.17 2022:465.38 2023:338.49 2024:338.50 2025:296.26 2026:253.91
  Harrison                                  2015:1.6K 2016:423.31 2017:169.39 2018:169.36 2019:381.05 2022:169.38 2023:127.03 2024:169.40 2025:338.80 2026:84.70
  Harvard                                   2015:592.65 2016:211.60 2017:126.89 2018:42.35 2019:338.50 2020:253.85 2021:338.45 2022:211.45 2023:84.67 2024:126.95 2025:42.35 2026:253.83
  Hyde Park                                 2015:169.03 2016:295.93 2017:338.09 2018:253.65 2019:169.09 2020:253.67 2021:211.31 2022:126.87 2023:126.80 2024:464.93 2025:338.12 2026:211.36
  Marlborough                               2015:423.50 2016:550.55 2017:465.85 2018:169.40 2019:465.85 2020:84.70 2021:127.05 2022:1.0K 2023:211.75 2024:592.90 2025:169.40 2026:84.70
  Massachusetts                             2015:254.03 2016:296.36 2017:338.72 2018:592.66 2019:42.34 2020:508.05 2021:42.33 2023:338.68 2024:254 2025:254.02 2026:127.01
  Newbury                                   2015:762.30 2016:338.80 2017:84.70 2018:211.75 2019:254.10 2020:296.45 2021:169.40 2022:84.70 2023:169.40 2024:42.35
  River                                     2015:634.05 2016:126.77 2017:422.62 2018:84.62 2019:169.08 2020:169.06 2021:42.27 2022:169.01 2023:295.83 2024:591.81 2025:380.54 2026:126.75
  Saratoga                                  2015:466.23 2016:296.67 2017:211.91 2018:84.76 2019:211.90 2020:211.91 2022:296.67 2023:254.30 2024:254.29 2025:339.05 2026:84.76
  Tremont                                   2015:635.04 2016:169.43 2017:423.47 2018:211.72 2019:127.04 2020:169.40 2021:42.35 2022:465.79 2023:169.37 2024:465.82 2025:550.42 2026:127.02
  Washington                                2015:1.6K 2016:677.15 2017:549.89 2018:677.06 2019:1.1K 2020:930.65 2021:804 2022:888.28 2023:550.23 2024:804.20 2025:380.84 2026:296.24

CONTACT_CITY by STATUS_DTTM, dollars = LATITUDE
  ALLSTON                                   2015:804.71 2016:381.21 2017:465.91 2018:211.76 2019:169.38 2020:338.67 2021:296.49 2022:254.08 2023:423.60 2024:677.52 2025:254.05 2026:126.95
  BOSTON                                    2015:6.0K 2016:5.3K 2017:6.6K 2018:3.8K 2019:5.8K 2020:5.2K 2021:3.6K 2022:7.7K 2023:4.1K 2024:5.5K 2025:2.8K 2026:1.4K
  BRIGHTON                                  2015:762.27 2016:635.18 2017:1.7K 2018:635.11 2019:550.52 2020:296.44 2021:592.96 2022:592.83 2023:762.27 2024:677.56 2025:465.79 2026:254.06
  BROOKLINE                                 2015:931.62 2016:381.15 2017:211.70 2018:380.98 2019:338.70 2020:423.47 2021:254.12 2022:508.05 2023:338.70 2024:169.43 2025:169.40 2026:84.61
  Boston                                    2015:6.6K 2016:3.5K 2017:1.9K 2018:1.8K 2019:3.6K 2020:1.4K 2021:1.2K 2022:1.4K 2023:1.3K 2024:2.3K 2025:3.2K 2026:1.2K
  CHARLESTOWN                               2015:889.88 2016:762.80 2017:932.21 2018:254.24 2019:550.92 2020:593.16 2021:423.75 2022:466 2023:84.74 2024:296.62 2025:254.23 2026:211.84
  DORCHESTER                                2015:6.3K 2016:3.8K 2017:4.3K 2018:4.7K 2019:5.3K 2020:5.2K 2021:6.7K 2022:5.2K 2023:3.5K 2024:5.3K 2025:1.7K 2026:1.9K
  Dorchester                                2015:4.9K 2016:2.0K 2017:888.56 2018:507.90 2019:1.7K 2020:1.5K 2021:845.99 2022:634.49 2023:930.64 2024:930.75 2025:2.7K 2026:1.5K
  EAST BOSTON                               2015:762.76 2016:1.5K 2017:1.3K 2018:1.2K 2019:1.4K 2020:720.33 2021:423.72 2022:2.9K 2023:1.7K 2024:1.2K 2025:423.75 2026:42.37
  East Boston                               2015:1.4K 2016:889.96 2017:169.50 2018:127.03 2019:254.16 2020:211.89 2021:42.38 2022:381.37 2023:169.49 2024:254.23 2025:550.89 2026:169.53
  HYDE PARK                                 2015:1.1K 2016:1.2K 2017:1.6K 2018:1.1K 2019:972.14 2020:1.6K 2021:1.0K 2022:1.6K 2023:1.2K 2024:1.3K 2025:1.4K 2026:676.14
  JAMAICA PLAIN                             2015:550.12 2016:549.92 2017:1.3K 2018:1.0K 2019:1.1K 2020:380.79 2021:338.40 2022:465.37 2023:634.70 2024:761.63 2025:169.24 2026:211.57
  MATTAPAN                                  2015:1.1K 2016:634.19 2017:1.1K 2018:1.1K 2019:930.07 2020:803.34 2021:930.14 2022:1.1K 2023:465.02 2024:1.1K 2025:972.35 2026:380.46
  QUINCY                                    2015:423.08 2016:211.70 2017:296.08 2018:634.79 2019:549.98 2020:84.57 2021:507.89 2022:550.12 2023:169.32 2024:592.08
  Quincy                                    2015:2.3K 2016:507.69 2017:253.88 2018:634.98 2019:253.79 2020:42.37 2021:296.09 2022:84.68 2023:169.31 2024:42.34 2025:338.66 2026:126.92
  ROSLINDALE                                2015:634.29 2016:507.44 2017:1.1K 2018:887.93 2019:338.36 2020:676.62 2021:422.87 2022:718.87 2023:549.65 2024:591.97 2025:380.54 2026:338.23
  ROXBURY                                   2015:2.3K 2016:761.75 2017:761.79 2018:1.2K 2019:1.5K 2020:1.1K 2021:1.1K 2022:931.01 2023:592.50 2024:1.9K 2025:507.91 2026:126.98
  Roxbury                                   2015:1.1K 2016:296.29 2017:126.96 2018:423.24 2019:592.45 2020:253.87 2021:296.22 2022:126.93 2023:169.30 2024:296.27 2025:211.64 2026:296.27
  SOUTH BOSTON                              2015:761.92 2016:1.2K 2017:1.4K 2018:1.2K 2019:1.0K 2020:550.36 2021:804.39 2022:1.1K 2023:1.5K 2024:889.05 2025:465.69 2026:423.28
  WEST ROXBURY                              2015:592.22 2016:634.18 2017:1.7K 2018:845.60 2019:634.29 2020:507.36 2021:549.84 2022:592.19 2023:296 2024:296.12 2025:253.73 2026:253.74

## where

CONTACT_STATE: MA 9.6K, NY 51, FL 43, TX 32, Ma 29, NH 27, NC 18, MD 17, RI 16, CA 16, ME 15, PA 15

## what

STATUS: Closed 92%, Open 8%

VIOLATION_SUFFIX: ST 74%, AV 15%, RD 6%, PL 1%, PK 1%, SQ 1%, TE 1%, CT 1%, HW 0%, BL 0%, PW 0%

VIOLATION_CITY: Dorchester 29%, Boston 19%, Roxbury 11%, East Boston 9%, Mattapan 6%, South Boston 6%, Hyde Park 5%, Brighton 4%, Allston 3%, Roslindale 3%, Charlestown 3%, Jamaica Plain 3%

VIOLATION_ZIP: 02128 12%, 02124 12%, 02121 11%, 02125 9%, 02119 9%, 02136 8%, 02127 8%, 02122 7%, 02126 7%, 02116 6%, 02135 6%, 02118 6%

WARD: 18 14%, 03 12%, 01 12%, 14 12%, 05 10%, 12 7%, 17 6%, 15 6%, 22 6%, 16 5%, 13 5%, 07 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CASE_NO | id | 10.0K | 0 | V227935 54; V227263 52; V227312 51; V225147 50 |
| AP_CASE_DEFN_KEY | other | 1 | 0 | 1013 10.0K |
| STATUS_DTTM | date | 9.9K | 1 | 2015-02-23 14:45:21 54; 2015-02-19 10:04:30 52; 2015-02-19 10:36:49 51; 2015-02-06 09:29:22 50 |
| STATUS | category | 2 | 0 | Closed 9.2K; Open 779 |
| CODE | other | 307 | 0 | 105.1 2.9K; 102.8 1.3K; 116.2 1.1K; 116.1 760 |
| VALUE | other | 1 | 0 | N/A 10.0K |
| DESCRIPTION | who | 261 | 97 | Failure to Obtain Permit 2.9K; Unsafe and Dangerous 1.9K; Maintenance 1.4K; Testing & Certification 731 |
| VIOLATION_STNO | other | 1.2K | 7 | 6 142; 15 142; 7 130; 11 127 |
| VIOLATION_STHIGH | other | 692 | 7.7K | 8 26; 20 25; 25 25; 44 25 |
| VIOLATION_STREET | who | 1.6K | 7 | Washington 224; Blue Hill 198; Beacon 139; Commonwealth 109 |
| VIOLATION_SUFFIX | category | 22 | 93 | ST 7.3K; AV 1.5K; RD 600; PL 86 |
| VIOLATION_CITY | category | 25 | 8 | Dorchester 2.7K; Boston 1.8K; Roxbury 1.0K; East Boston 868 |
| VIOLATION_STATE | other | 1 | 0 | MA 10.0K |
| VIOLATION_ZIP | category | 32 | 9 | 02128 870; 02124 835; 02121 775; 02125 645 |
| WARD | category | 23 | 10 | 18 1.0K; 03 906; 01 869; 14 864 |
| CONTACT_ADDR1 | other | 7.7K | 3 | 71 Rogers St 68; 619 CENTRE ST 63; 15 Woodbriar Road 56; 201 E COTTAGE ST 54 |
| CONTACT_ADDR2 | other | 1.1K | 8.3K | Unit 1 105; Unit 2 98; Unit 3 47; UNIT 1 17 |
| CONTACT_CITY | who | 630 | 1 | BOSTON 1.4K; DORCHESTER 1.3K; Boston 709; Dorchester 453 |
| CONTACT_STATE | state | 57 | 1 | MA 9.6K; NY 51; FL 43; TX 32 |
| CONTACT_ZIP | other | 888 | 1 | 02124 625; 02128 516; 02136 420; 02125 407 |
| SAM_ID | other | 6.8K | 38 | 30891 58; 129629 55; 43572 54; 340723 54 |
| LATITUDE | amount | 6.6K | 57 | 42.3532559998717 58; 42.317479999598255 55; 42.31945000024701 54; 42.35159985699556 54 |
| LONGITUDE | amount | 6.8K | 57 | -71.12839600126908 58; -71.05351000119647 55; -71.06058000093033 54; -71.06099622702814 54 |
| LOCATION | other | 6.7K | 57 | (42.3532559998717, -71.12 58; (42.317479999598255, -71. 55; (42.31945000024701, -71.0 54; (42.35159985699556, -71.0 54 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:34:41.99589 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | f19dc65e-7495-473d-95d3-d 10.0K |
| SRC_SHA256 | who | 1 | 0 | ea50b0fee050e578a7b705984 10.0K |
