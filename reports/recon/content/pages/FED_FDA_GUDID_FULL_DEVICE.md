# FED_FDA_GUDID_FULL_DEVICE

rows 5.18M  columns 37  scan 6.8s

roles: audit 2, category 3, date 4, id 2, other 24, who 3

## errors
  _INGESTED_AT: 100039 (22003): Numeric value '56656526' is out of range

## when

PUBLICVERSIONDATE
  2018    353.7K  #########
  2019    215.0K  #####
  2020    350.3K  #########
  2021    354.5K  #########
  2022    841.1K  #####################
  2023    626.8K  ################
  2024    793.4K  ####################
  2025     1.20M  ##############################
  2026    451.5K  ###########

DEVICEPUBLISHDATE
  2013         3  
  2014     35.3K  #
  2015    450.2K  ##################
  2016    762.5K  ##############################
  2017    311.5K  ############
  2018    416.7K  ################
  2019    422.1K  #################
  2020    392.4K  ###############
  2021    406.9K  ################
  2022    613.9K  ########################
  2023    430.9K  #################
  2024    398.0K  ################
  2025    360.8K  ##############
  2026    181.5K  #######

DEVICECOMMDISTRIBUTIONENDDATE
  2014       185  
  2015      5.2K  ##
  2016     11.4K  #####
  2017     17.5K  ########
  2018     32.4K  ###############
  2019     26.3K  ############
  2020     41.6K  ###################
  2021     43.7K  ####################
  2022     61.4K  ############################
  2023     52.3K  ########################
  2024     66.2K  ##############################
  2025     61.9K  ############################
  2026     29.3K  #############
  2027      3.6K  ##
  2028      1.3K  #
  2029      1.1K  
  2030      1.9K  #
  2031       707  
  2032       129  
  2033        96  
  2034        34  
  2035        33  

## who

BRANDNAME by rows
    371.9K  CARDINAL HEALTH
    217.6K  Medline Industries, Inc.
     53.7K  Bivona
     31.1K  MDT Diamond Coated Dental Burs
     26.3K  Halyard
     25.9K  AVID TruCustom
     25.5K  VenoTrain micro
     24.8K  The JASPER Spinal Fixation System
     22.0K  ACS
     21.5K  Surgical Direct
     18.4K  ReLine
     18.1K  Millennium
     18.1K  FOSTER GRANT
     17.7K  Arthrex®
     17.5K  Ambler Surgical
     17.1K  MEDI
     16.2K  VenoTrain soft
     14.9K  N.A.
     14.1K  DeRoyal
     13.9K  Invictus

COMPANYNAME by rows
    377.2K  Cardinal Health 200, LLC
    251.7K  MEDLINE INDUSTRIES, INC.
     74.5K  FGX INTERNATIONAL INC.
     64.3K  ICU MEDICAL, INC.
     55.9K  Bauerfeind AG
     53.7K  Smith & Nephew, Inc.
     50.2K  GBS Commonwealth Co.,Ltd.
     47.5K  ALPHATEC SPINE, INC.
     46.5K  AVID MEDICAL, INC.
     45.2K  MEDTRONIC SOFAMOR DANEK, INC.
     44.7K  Nuvasive, Inc.
     43.3K  GLOBUS MEDICAL, INC.
     42.0K  Biomet Orthopedics, LLC
     37.5K  M.D.T. - MICRO DIAMOND TECHNOLOGIES LTD.
     32.7K  Zimmer, Inc.
     32.6K  BIOMET SPINE LLC
     31.4K  Synthes GmbH
     30.5K  MEDTRONIC, INC.
     29.6K  TELEFLEX INCORPORATED
     29.1K  Avalign Technologies, Inc.

DUNSNUMBER by rows
    377.2K  961027315
    251.7K  025460908
     74.5K  062312087
     64.3K  118380146
     55.9K  315914853
     53.7K  045483575
     50.2K  694609156
     47.5K  602465783
     46.5K  015623119
     45.2K  830350380
     44.7K  053950783
     43.3K  139105691
     42.0K  129278169
     37.5K  600226468
     32.7K  056038268
     32.6K  018577570
     31.3K  486711679
     29.8K  006261481
     29.6K  002348191
     29.1K  792528510

## who x when

BRANDNAME by DEVICEPUBLISHDATE
  ACS                                       2018:4.3K 2019:3.9K 2020:3.3K 2021:3.4K 2022:2.0K 2023:2.7K 2024:1.8K 2025:480 2026:69
  AVID TruCustom                            2016:9.6K 2017:5.2K 2018:4.4K 2019:4.5K 2020:2.1K
  Ambler Surgical                           2016:2.6K 2021:14.9K 2022:1
  Arthrex®                                  2017:5.4K 2018:5.6K 2019:958 2020:774 2021:673 2022:542 2023:1.1K 2024:640 2025:1.2K 2026:886
  Bivona                                    2015:17.9K 2016:4.2K 2017:3.8K 2018:3.5K 2019:3.8K 2020:3.3K 2021:3.3K 2022:3.0K 2023:653 2024:5.7K 2025:3.0K 2026:1.5K
  CARDINAL HEALTH                           2015:5.7K 2016:34.7K 2017:20.2K 2018:39.4K 2019:30.7K 2020:25.9K 2021:50.9K 2022:41.8K 2023:36.9K 2024:30.8K 2025:36.8K 2026:18.0K
  DeRoyal                                   2016:3.6K 2017:90 2018:284 2019:58 2020:87 2021:8.1K 2023:1.3K 2024:140 2025:118 2026:158
  FOSTER GRANT                              2021:6 2022:18.1K
  Halyard                                   2015:242 2016:2.2K 2017:803 2018:366 2019:643 2020:4.9K 2021:2.0K 2022:2.5K 2023:2.1K 2024:3.3K 2025:5.2K 2026:2.2K
  Invictus                                  2020:3.3K 2021:2.1K 2022:2.3K 2023:3.2K 2024:1.2K 2025:1.6K 2026:184
  MDT Diamond Coated Dental Burs            2024:31.1K
  MEDI                                      2016:4.5K 2017:2.3K 2018:1.9K 2019:867 2020:1.5K 2021:790 2022:595 2023:121 2024:2.9K 2025:790 2026:758
  Medline Industries, Inc.                  2015:122 2016:30.6K 2018:32.5K 2019:25.0K 2020:2.6K 2021:40.6K 2022:24.8K 2023:25.9K 2024:27.2K 2025:8.1K 2026:159
  Millennium                                2016:1 2017:3.9K 2018:248 2019:280 2020:423 2021:5.0K 2022:518 2023:4.3K 2024:914 2025:1.7K 2026:816
  N.A.                                      2016:1.7K 2017:135 2018:64 2019:12.2K 2020:144 2021:590 2022:6 2023:8 2024:15 2025:2 2026:5
  ReLine                                    2015:8.9K 2016:1.2K 2017:2.0K 2018:882 2019:1.2K 2020:325 2021:2.1K 2022:1.4K 2023:129 2024:4 2025:90 2026:18
  Surgical Direct                           2020:1.1K 2022:9.5K 2023:4.7K 2024:3.6K 2025:1.9K 2026:709
  The JASPER Spinal Fixation System         2019:24.8K 2020:8
  VenoTrain micro                           2016:13.1K 2018:2.0K 2019:2.5K 2020:1 2021:4.5K 2022:2.3K 2023:1.1K
  VenoTrain soft                            2016:4.3K 2018:1.4K 2019:4.1K 2020:1 2021:3.7K 2022:1.8K 2023:896

COMPANYNAME by DEVICEPUBLISHDATE
  ALPHATEC SPINE, INC.                      2014:1.5K 2015:3.4K 2016:2.9K 2017:81 2018:90 2019:1.2K 2020:9.7K 2021:9.4K 2022:4.3K 2023:5.5K 2024:3.5K 2025:4.9K 2026:1.1K
  AVID MEDICAL, INC.                        2016:9.6K 2017:5.2K 2018:4.4K 2019:4.5K 2020:6.2K 2021:1.9K 2022:2.3K 2023:2.0K 2024:3.2K 2025:5.0K 2026:2.0K
  Avalign Technologies, Inc.                2017:7.6K 2018:601 2019:457 2020:1.0K 2021:6.6K 2022:557 2023:8.6K 2024:978 2025:1.8K 2026:864
  BIOMET SPINE LLC                          2015:14.0K 2016:986 2017:1.0K 2018:704 2019:2.2K 2020:11.2K 2021:2.5K 2022:23
  Bauerfeind AG                             2016:23.1K 2018:3.9K 2019:6.8K 2020:44 2021:11.2K 2022:7.0K 2023:3.9K
  Biomet Orthopedics, LLC                   2014:16 2015:17.5K 2016:3.9K 2017:6.5K 2018:1.4K 2019:1.3K 2020:4.3K 2021:2.7K 2022:3.4K 2023:874 2024:15 2025:87 2026:61
  Cardinal Health 200, LLC                  2015:5.6K 2016:36.4K 2017:20.5K 2018:39.8K 2019:31.0K 2020:25.9K 2021:51.2K 2022:42.1K 2023:37.4K 2024:31.8K 2025:37.3K 2026:18.3K
  FGX INTERNATIONAL INC.                    2021:12 2022:74.5K
  GBS Commonwealth Co.,Ltd.                 2019:33.4K 2020:9.6K 2021:3.0K 2023:1.5K 2024:2.7K
  GLOBUS MEDICAL, INC.                      2014:337 2015:19.9K 2016:6.6K 2018:2.3K 2019:7.6K 2020:1.5K 2021:1.1K 2022:1.1K 2023:749 2024:338 2025:235 2026:1.5K
  ICU MEDICAL, INC.                         2014:2 2015:18.6K 2016:6.5K 2017:8.2K 2018:3.6K 2019:4.1K 2020:3.6K 2021:5.6K 2022:3.0K 2023:713 2024:5.8K 2025:3.0K 2026:1.6K
  M.D.T. - MICRO DIAMOND TECHNOLOGIES LTD.  2024:37.5K
  MEDLINE INDUSTRIES, INC.                  2015:481 2016:33.5K 2017:118 2018:32.9K 2019:24.7K 2020:4.8K 2021:45.7K 2022:29.8K 2023:28.6K 2024:29.8K 2025:20.2K 2026:1.2K
  MEDTRONIC SOFAMOR DANEK, INC.             2014:214 2015:20.4K 2016:3.9K 2017:5.3K 2018:1.4K 2019:695 2020:916 2021:1.1K 2022:7.6K 2023:248 2024:803 2025:1.9K 2026:683
  MEDTRONIC, INC.                           2014:2.9K 2015:1.7K 2016:11.8K 2017:2.2K 2018:1.8K 2019:1.4K 2020:1.3K 2021:1.6K 2022:1.0K 2023:648 2024:2.5K 2025:1.2K 2026:333
  Nuvasive, Inc.                            2014:26 2015:17.2K 2016:2.7K 2017:3.2K 2018:9.2K 2019:3.9K 2020:1.6K 2021:3.7K 2022:1.5K 2023:806 2024:434 2025:185 2026:171
  Smith & Nephew, Inc.                      2015:28.9K 2016:3.0K 2017:4.6K 2018:2.1K 2019:2.3K 2020:1.6K 2021:2.9K 2022:3.7K 2023:2.7K 2024:504 2025:1.4K 2026:69
  Synthes GmbH                              2015:16.3K 2016:8.3K 2017:602 2018:1.1K 2019:541 2020:508 2021:1.2K 2022:450 2023:30 2024:2.2K 2025:169 2026:46
  TELEFLEX INCORPORATED                     2015:3.0K 2016:5.7K 2017:1.4K 2018:6.9K 2019:2.6K 2020:1.6K 2021:1.5K 2022:3.9K 2023:798 2024:1.1K 2025:591 2026:496
  Zimmer, Inc.                              2015:10.9K 2016:9.6K 2017:2.9K 2018:1.9K 2019:1.7K 2020:910 2021:283 2022:1.9K 2023:275 2024:1.6K 2025:611 2026:287

## what

PUBLICVERSIONSTATUS: Update 62%, New 38%

DEVICECOMMDISTRIBUTIONSTATUS: In Commercial Distribution 91%, Not in Commercial Distribution 9%

MRISAFETYSTATUS: Labeling does not contain MRI  90%, MR Conditional 5%, MR Unsafe 3%, MR Safe 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PRIMARYDI | id | 5.26M | 0 | 00749756362726 3.8K; 00749756362733 3.8K; 00749756362740 3.8K; 00749756362764 3.8K |
| PUBLICDEVICERECORDKEY | id | 5.29M | 0 | 99517ca8-4758-4e1a-89a8-3 3.8K; 80518d15-7558-40d2-8383-b 3.8K; 5fc186db-5e94-49e6-933c-4 3.8K; f3485aa1-d0d4-4f0e-afe8-2 3.8K |
| PUBLICVERSIONSTATUS | category | 2 | 0 | Update 3.20M; New 1.99M |
| DEVICERECORDSTATUS | other | 1 | 0 | Published 5.18M |
| PUBLICVERSIONNUMBER | other | 56 | 0 | 1 1.98M; 2 832.9K; 3 760.5K; 4 564.8K |
| PUBLICVERSIONDATE | date | 2.2K | 0 | 2022-06-17 234.5K; 2025-07-02 131.0K; 2018-03-29 107.0K; 2024-09-11 101.8K |
| DEVICEPUBLISHDATE | date | 4.3K | 0 | 2016-09-24 91.0K; 2015-10-24 70.6K; 2015-09-24 63.5K; 2022-06-22 41.8K |
| DEVICECOMMDISTRIBUTIONENDDATE | date | 4.4K | 4.72M | 2024-09-01 8.4K; 2025-11-30 6.4K; 2022-05-05 6.1K; 2025-09-22 5.7K |
| DEVICECOMMDISTRIBUTIONSTATUS | category | 2 | 0 | In Commercial Distributio 4.74M; Not in Commercial Distrib 444.6K |
| BRANDNAME | who | 338.8K | 156.9K | CARDINAL HEALTH 376.5K; Medline Industries, Inc. 216.9K; Bivona 53.7K; MDT Diamond Coated Dental 32.0K |
| VERSIONMODELNUMBER | other | 4.61M | 4.8K | 1 38.7K; A 10.1K; Perfusion Pack 8.2K; rev 01 5.5K |
| CATALOGNUMBER | other | 2.66M | 2.21M | 16636 2.9K; 16936 2.8K; 16716 2.8K; 16116 2.7K |
| DUNSNUMBER | who | 12.5K | 0 | 961027315 378.7K; 025460908 252.5K; 062312087 76.2K; 118380146 56.7K |
| COMPANYNAME | who | 12.2K | 8 | Cardinal Health 200, LLC 378.7K; MEDLINE INDUSTRIES, INC. 252.5K; FGX INTERNATIONAL INC. 76.2K; ICU MEDICAL, INC. 56.7K |
| DEVICECOUNT | other | 422 | 0 | 1 4.87M; 10 60.3K; 5 59.5K; 100 28.3K |
| DEVICEDESCRIPTION | other | 2.69M | 1.05M | Rotary diamond instrument 17.5K; FG Rotary diamond instrum 15.9K; HAND PACK 10.6K; TOTAL KNEE PACK 10.5K |
| DMEXEMPT | other | 1 | 4.48M | true 702.5K |
| PREMARKETEXEMPT | other | 1 | 2.63M | true 2.55M |
| DEVICEHCTP | other | 1 | 5.18M | true 3.4K |
| DEVICEKIT | other | 1 | 4.27M | true 908.2K |
| DEVICECOMBINATIONPRODUCT | other | 1 | 5.11M | true 74.9K |
| SINGLEUSE | other | 1 | 1.95M | true 3.23M |
| LOTBATCH | other | 1 | 676.8K | true 4.51M |
| SERIALNUMBER | other | 1 | 4.57M | true 614.2K |
| MANUFACTURINGDATE | other | 1 | 3.13M | true 2.06M |
| EXPIRATIONDATE | other | 1 | 3.10M | true 2.08M |
| DONATIONIDNUMBER | other | 1 | 5.13M | true 49.4K |
| LABELEDCONTAINSNRL | other | 1 | 5.10M | true 81.2K |
| LABELEDNONRL | other | 1 | 4.31M | true 877.1K |
| MRISAFETYSTATUS | category | 4 | 0 | Labeling does not contain 4.67M; MR Conditional 266.8K; MR Unsafe 165.7K; MR Safe 81.8K |
| RX | other | 1 | 1.56M | true 3.62M |
| OTC | other | 1 | 4.95M | true 234.1K |
| DEVICESTERILE | other | 1 | 3.53M | true 1.65M |
| STERILIZATIONPRIORTOUSE | other | 1 | 3.20M | true 1.98M |
| _INGESTED_AT | audit date | 1 | 0 | 56656526-09-15 12:46:16.0 5.18M |
| _SOURCE_RUN_ID | audit | 1 | 0 | c208d4a8-979e-4e09-8ff2-d 5.18M |
| _SRC_SHA256 | other | 1 | 0 | b069d3950b2c75da08b2adbf4 5.18M |
