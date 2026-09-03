# FED_ICE_DETENTION_STINTS

rows 2.62M  columns 71  scan 9.9s

roles: amount 4, audit 2, category 28, date 14, id 1, other 8, state 1, who 13

## when

STAY_BOOK_IN_DATE_TIME
  2004         2  
  2011         6  
  2012         3  
  2014         9  
  2015         3  
  2016         3  
  2017        12  
  2018        31  
  2019       105  
  2020       284  
  2021      1.2K  
  2022    141.9K  ####
  2023    549.0K  ###############
  2024    587.9K  ################
  2025     1.12M  ##############################
  2026    213.6K  ######

BOOK_IN_DATE_TIME
  2004         1  
  2011         2  
  2012         1  
  2014         5  
  2015         1  
  2016         2  
  2017         3  
  2018         7  
  2019        28  
  2020        61  
  2021       381  
  2022    128.6K  ###
  2023    531.8K  ##############
  2024    575.7K  ###############
  2025     1.12M  ##############################
  2026    262.2K  #######

BOOK_OUT_DATE_TIME
  2022    108.7K  ###
  2023    515.0K  ##############
  2024    573.2K  ################
  2025     1.09M  ##############################
  2026    268.3K  #######

STAY_BOOK_OUT_DATE_TIME
  2022     94.5K  ###
  2023    494.5K  ###############
  2024    567.4K  #################
  2025     1.01M  ##############################
  2026    273.2K  ########

STAY_BOOK_OUT_DATE
  2022     94.5K  ###
  2023    494.5K  ###############
  2024    567.4K  #################
  2025     1.01M  ##############################
  2026    273.2K  ########

BOND_POSTED_DATE
  1979         4  
  1981         7  
  1982         2  
  1983         8  
  1984         1  
  1985         1  
  1986        22  
  1987         7  
  1988        17  
  1989        54  
  1990        59  
  1991        63  
  1992        71  
  1993        95  
  1994       160  
  1995       170  
  1996       208  
  1997       198  
  1998       366  
  1999       261  
  2000       633  
  2001       460  
  2002       498  
  2003       534  
  2004       299  
  2005       400  
  2006       338  
  2007       482  
  2008       666  
  2009      1.0K  #
  2010      1.8K  #
  2011      3.2K  ##
  2012      4.1K  ##
  2013      4.2K  ##
  2014      5.2K  ###
  2015      3.2K  ##
  2016      4.4K  ###
  2017      5.7K  ###
  2018      7.5K  ####
  2019      7.3K  ####
  2020      3.9K  ##
  2021      2.4K  #
  2022     13.5K  ########
  2023     27.5K  ################
  2024     24.4K  ##############
  2025     50.7K  ##############################
  2026     14.3K  ########

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| BOND_POSTED_AMOUNT | 190.3K | 50 | 5.0K | 25.0K | 750.0K | 1.32B |
| INITIAL_BOND_SET_AMOUNT | 200.6K | 1 | 5.0K | 30.0K | 246.92M | 2.76B |
| INITIAL_BOND_SET_AMOUNT_LOWEST_SEEN | 200.7K | 1 | 5.0K | 25.0K | 246.92M | 1.65B |
| BOND_POSTED_AMOUNT_LOWEST_SEEN | 192.6K | 50 | 5.0K | 25.0K | 750.0K | 1.28B |

## who

DETENTION_FACILITY by rows
    125.9K  ALEXANDRIA STAGING FACILITY
    118.1K  PORT ISABEL SPC
    103.2K  FLORENCE STAGING FACILITY
     52.9K  MONTGOMERY PROCESSING CTR
     46.6K  WINN CORRECTIONAL CENTER
     45.8K  PINE PRAIRIE ICE PROCESSING CENTER
     44.6K  ELOY FED CTR FACILITY (CORE CIVIC)
     44.1K  FLORENCE SPC
     42.7K  SOUTH TEXAS ICE PROCESSING CENTER
     41.6K  ERO EL PASO CAMP EAST MONTANA
     40.8K  PRAIRIELAND DETENTION CENTER
     40.8K  STEWART DETENTION CENTER
     36.8K  MONTGOMERY HOLD RM
     36.3K  OTAY MESA DETENTION CENTER
     35.8K  CENTRAL LOUISIANA ICE PROC CTR
     35.5K  JACKSON PARISH CORRECTIONAL CENTER
     34.5K  DALLAS F.O. HOLD
     34.0K  PHOENIX DIST OFFICE
     33.3K  KARNES CO IMMIGRATION PROCESS CTR
     33.1K  KROME NORTH SPC

DETENTION_FACILITY by dollars
     253.83M    15.4K rows  IMPERIAL REGIONAL ADULT DET FAC
      55.81M    52.9K rows  MONTGOMERY PROCESSING CTR
      46.42M   103.2K rows  FLORENCE STAGING FACILITY
      41.84M   125.9K rows  ALEXANDRIA STAGING FACILITY
      41.32M    36.8K rows  MONTGOMERY HOLD RM
      32.64M    33.1K rows  KROME NORTH SPC
      29.80M    44.6K rows  ELOY FED CTR FACILITY (CORE CIVIC)
      28.46M   118.1K rows  PORT ISABEL SPC
      26.26M    44.1K rows  FLORENCE SPC
      25.52M    24.9K rows  MOSHANNON VALLEY PROCESSING CENTER
      23.90M    14.8K rows  BUFFALO SPC
      23.03M    40.8K rows  STEWART DETENTION CENTER
      21.74M    23.2K rows  BROWARD TRANSITIONAL CENTER
      20.00M    24.3K rows  DENVER CONTRACT DETENTION FACILITY
      19.35M    46.6K rows  WINN CORRECTIONAL CENTER
      19.33M    12.2K rows  DESERT VIEW ANNEX
      18.63M    36.3K rows  OTAY MESA DETENTION CENTER
      17.86M    22.4K rows  LOS CUST CASE
      16.80M    18.2K rows  ELIZABETH CONTRACT D.F.
      16.80M    40.8K rows  PRAIRIELAND DETENTION CENTER

UNIQUE_IDENTIFIER by rows
        38  c65403e032fc0fce7256b84d5233eba7757c0dbf
        38  7672975edb261b8fdcd3b9b02059ece07a63145b
        35  6b2bb255419a9b7c41edc0f957ee1df892eb287f
        34  587f01f9d440e56b4b449668bc3b4a93012572cc
        34  1683afd417a2ac2395fca447d3fa09330058d929
        32  1dcf72d0e7f734f59ada6a2c6ad9e728fd692d4a
        31  07a5575246dce36f70712749eabe904934f9e879
        30  4b00b08c9a6eadcc35862394d62f818c80f78659
        30  7bbe134306da6eb743570fdae103d8af30bca6c5
        30  768cf01d0d1afb971ecd1df04e2fcecfd0624c44
        28  ffcc541c51e1a3d052fed071309229e9dda81544
        28  61a0a5df6d2eb10525f6151d1af0003ac400995a
        28  1fcef472847a5c344e120a14c278aa79414933c4
        28  d2bb07e58883cd1738ce94cb5a0d9474006f43db
        28  08a599d9c190bdf5b05dc0f4eebebeec7739e69c
        28  d1bdcc330e7b66d20e34bb7a3f13ef9cdc37f9b1
        28  4db3042e0ba491199ca8f9f91047091f07208d5c
        27  a0752d9fb76666fa99e73879d0da83b8f3c4a885
        27  023b9ba47782d774971e34ed338a9d41e2f4ee1d
        27  eef4c692ec0c6d4db9b338569261906126139774

UNIQUE_IDENTIFIER by dollars
     246.92M        1 rows  69a4236efc5a0525d4dedc4fa9d0c672e50d450d
       7.50M       10 rows  b365ac74c242b7dd1b0d5b271cb9cea2aa1a5668
       7.00M        7 rows  6dafa327296592cd4ce9bc4f2bc72e302a263237
       5.00M        5 rows  4d6af2c7ef37908a69d7f395348771f4d6b8403c
       3.72M        5 rows  de319e20e91f115e0d8b5543229309bfacb8f937
       2.50M        5 rows  35eb23b3b443cc75efbc4c8d05352a14ca4a77cb
       2.00M        2 rows  23eabf9e58359af53fd482322e10b7d5ac628518
       1.60M        4 rows  ec9f10f05a16dd73288cdbf9865be9277f9d89c1
       1.52M        5 rows  120d9a1661dd4bc1fb057d98b88c43c6e8ac7293
       1.20M       16 rows  b762a528ed2ce6e9fa6bb6274c013b8865536ec2
      955.5K       13 rows  58267e456830769dd255eff54c467c2711be500b
      900.0K        6 rows  bc2c2b75ecaa73ba5fa2cf37abefc6b1a13a77b4
      750.0K        3 rows  41a012cc43af03cb033f666c4d6c851045e871c1
      750.0K        3 rows  810a913c0d223a9fb5cf73ac49efcd7027c16357
      702.0K       12 rows  330845156987c090cc61f6f13e8450761904849c
      645.0K        3 rows  98597040327d098336accdec30d7a314967af669
      600.0K        8 rows  81fec6dd4a9cb2a9814636fb307cc8e3db87458c
      588.0K        8 rows  fe4684721fbb5d8318486801e0cac03ccf3ab638
      570.0K       38 rows  7672975edb261b8fdcd3b9b02059ece07a63145b
      514.5K        7 rows  75e8d35234745833fc28c25ed43a4e046d923675

MSC_CHARGE by rows
    106.8K  Driving Under Influence Liquor
     67.4K  Illegal Entry (INA SEC.101(a)(43)(O), 8USC1325 only)
     55.6K  Assault
     50.7K  Traffic Offense
     42.8K  Illegal Re-Entry (INA SEC.101(a)(43)(O), 8USC1326 only)
     25.8K  Drug Trafficking
     23.6K  Larceny
     18.5K  Burglary
     17.8K  Dangerous Drugs
     17.8K  Domestic Violence
     17.0K  Sex Assault
     13.5K  Resisting Officer
     12.9K  Smuggling Aliens
     12.9K  Aggravated Assault - Weapon
     12.2K  Trespassing
     10.3K  Cocaine - Sell
     10.3K  Robbery
     10.0K  Possession Of Weapon
      9.9K  Drug Possession
      9.8K  Battery

MSC_CHARGE by dollars
     112.61M   106.8K rows  Driving Under Influence Liquor
      50.56M    50.7K rows  Traffic Offense
      42.01M    55.6K rows  Assault
      17.46M    23.6K rows  Larceny
      16.95M    17.8K rows  Domestic Violence
      16.81M    18.5K rows  Burglary
      16.41M    67.4K rows  Illegal Entry (INA SEC.101(a)(43)(O), 8USC1325 only)
      14.75M     7.1K rows  Fraud
      10.87M    13.5K rows  Resisting Officer
      10.72M     9.5K rows  Public Order Crimes
      10.67M    17.8K rows  Dangerous Drugs
       9.75M     7.7K rows  Disorderly Conduct
       8.09M     9.8K rows  Battery
       7.73M     8.8K rows  Hit and Run
       6.52M     5.6K rows  Licensing Violation
       6.21M    10.3K rows  Robbery
       6.16M    17.0K rows  Sex Assault
       5.88M     9.9K rows  Drug Possession
       5.87M    10.0K rows  Possession Of Weapon
       5.76M    25.8K rows  Drug Trafficking

RELIGION by rows
     27.6K  CATHOLIC
      6.6K  Unknown
      5.2K  CATH
      3.9K  Catholic
      3.4K  Christian
      2.4K  Islam
      2.2K  CHRISTIAN
      2.1K  UNKNOWN
      1.9K  NTA
       995  unknown
       806  Christian Orthodox
       725  Hindu
       608  UNK
       529  MUSLIM
       298  catholic
       206  EVANGELICO
       189  HINDU
       177  A01
       165  NA
       136  LTRB

RELIGION by dollars
      23.04M    27.6K rows  CATHOLIC
       7.32M     6.6K rows  Unknown
       2.72M     5.2K rows  CATH
       2.50M     2.2K rows  CHRISTIAN
       2.28M     3.9K rows  Catholic
       1.77M     2.1K rows  UNKNOWN
      970.0K      995 rows  unknown
      765.5K     3.4K rows  Christian
      730.0K     1.9K rows  NTA
      702.0K      529 rows  MUSLIM
      696.0K      608 rows  UNK
      484.5K      136 rows  LTRB
      278.5K     2.4K rows  Islam
      213.5K      131 rows  Muslim
      176.2K      206 rows  EVANGELICO
      175.0K       54 rows  ISLAM
      120.0K       10 rows  MORM
       96.5K      298 rows  catholic
       96.0K       15 rows  Evangelic
       80.0K        7 rows  ADVENTISTA

## who x when

DETENTION_FACILITY by STAY_BOOK_OUT_DATE, dollars = INITIAL_BOND_SET_AMOUNT_LOWEST_SEEN
  ALEXANDRIA STAGING FACILITY               2022:1.19M 2023:7.07M 2024:8.43M 2025:20.69M 2026:2.64M
  BROWARD TRANSITIONAL CENTER               2022:1.52M 2023:3.39M 2024:2.73M 2025:12.03M 2026:1.54M
  BUFFALO SPC                               2022:290.0K 2023:9.26M 2024:4.72M 2025:6.31M 2026:2.39M
  CENTRAL LOUISIANA ICE PROC CTR            2022:896.0K 2023:3.38M 2024:4.77M 2025:4.86M 2026:1.24M
  DALLAS F.O. HOLD                          2022:139.0K 2023:2.98M 2024:3.65M 2025:7.56M 2026:1.30M
  DENVER CONTRACT DETENTION FACILITY        2022:1.47M 2023:3.70M 2024:6.48M 2025:5.34M 2026:2.00M
  DESERT VIEW ANNEX                         2022:228.0K 2023:5.73M 2024:3.64M 2025:7.42M 2026:1.92M
  ELIZABETH CONTRACT D.F.                   2022:417.0K 2023:3.90M 2024:4.96M 2025:5.87M 2026:815.0K
  ELOY FED CTR FACILITY (CORE CIVIC)        2022:8.65M 2023:7.87M 2024:5.03M 2025:5.61M 2026:1.88M
  ERO EL PASO CAMP EAST MONTANA             2025:7.25M 2026:5.81M
  FLORENCE SPC                              2022:2.53M 2023:5.89M 2024:6.59M 2025:8.77M 2026:2.03M
  FLORENCE STAGING FACILITY                 2022:2.29M 2023:9.39M 2024:9.34M 2025:18.73M 2026:4.41M
  IMPERIAL REGIONAL ADULT DET FAC           2022:417.0K 2023:249.30M 2024:1.12M 2025:1.70M 2026:869.6K
  JACKSON PARISH CORRECTIONAL CENTER        2022:3.03M 2023:2.10M 2024:988.0K 2025:2.84M 2026:1.50M
  KARNES CO IMMIGRATION PROCESS CTR         2022:71.5K 2023:1.57M 2024:784.5K 2025:4.07M 2026:641.5K
  KROME NORTH SPC                           2022:715.0K 2023:4.94M 2024:5.01M 2025:19.27M 2026:1.67M
  LOS CUST CASE                             2022:104.5K 2023:960.5K 2024:1.46M 2025:9.60M 2026:4.38M
  MONTGOMERY HOLD RM                        2022:1.38M 2023:15.94M 2024:10.21M 2025:10.92M 2026:1.96M
  MONTGOMERY PROCESSING CTR                 2022:2.69M 2023:17.58M 2024:12.35M 2025:18.61M 2026:3.10M
  MOSHANNON VALLEY PROCESSING CENTER        2022:1.18M 2023:5.91M 2024:6.13M 2025:9.25M 2026:1.69M
  OTAY MESA DETENTION CENTER                2022:1.96M 2023:2.52M 2024:3.35M 2025:7.59M 2026:2.74M
  PHOENIX DIST OFFICE                       2022:457.2K 2023:2.79M 2024:2.31M 2025:5.56M 2026:1.47M
  PINE PRAIRIE ICE PROCESSING CENTER        2022:940.5K 2023:1.14M 2024:3.81M 2025:9.25M 2026:1.15M
  PORT ISABEL SPC                           2022:1.54M 2023:2.52M 2024:1.61M 2025:15.57M 2026:5.92M
  PRAIRIELAND DETENTION CENTER              2022:1.18M 2023:3.20M 2024:4.28M 2025:6.45M 2026:1.07M
  SOUTH TEXAS ICE PROCESSING CENTER         2022:1.37M 2023:5.03M 2024:2.63M 2025:6.10M 2026:840.0K
  STEWART DETENTION CENTER                  2022:1.28M 2023:6.36M 2024:3.67M 2025:8.24M 2026:1.86M
  WINN CORRECTIONAL CENTER                  2022:3.71M 2023:5.46M 2024:2.80M 2025:5.40M 2026:1.38M

UNIQUE_IDENTIFIER by STAY_BOOK_OUT_DATE, dollars = INITIAL_BOND_SET_AMOUNT_LOWEST_SEEN
  023b9ba47782d774971e34ed338a9d41e2f4ee1d  2024:30.0K 2025:240.0K
  07a5575246dce36f70712749eabe904934f9e879  2025:31
  08a599d9c190bdf5b05dc0f4eebebeec7739e69c  2023:12.0K 2026:4
  120d9a1661dd4bc1fb057d98b88c43c6e8ac7293  2025:1.52M
  1683afd417a2ac2395fca447d3fa09330058d929  2026:17.0K
  1dcf72d0e7f734f59ada6a2c6ad9e728fd692d4a  2023:16.0K
  1fcef472847a5c344e120a14c278aa79414933c4  2023:3.0K 2025:39.0K
  23eabf9e58359af53fd482322e10b7d5ac628518  2025:2.00M
  35eb23b3b443cc75efbc4c8d05352a14ca4a77cb  2025:2.50M
  4b00b08c9a6eadcc35862394d62f818c80f78659  2025:225.0K
  4d6af2c7ef37908a69d7f395348771f4d6b8403c  2025:5.00M
  4db3042e0ba491199ca8f9f91047091f07208d5c  2026:28
  587f01f9d440e56b4b449668bc3b4a93012572cc  2025:18.0K 2026:84.0K
  61a0a5df6d2eb10525f6151d1af0003ac400995a  2025:70.0K 2026:70.0K
  69a4236efc5a0525d4dedc4fa9d0c672e50d450d  2023:246.92M
  6b2bb255419a9b7c41edc0f957ee1df892eb287f  2025:35
  6dafa327296592cd4ce9bc4f2bc72e302a263237  2025:2.00M 2026:5.00M
  7672975edb261b8fdcd3b9b02059ece07a63145b  2025:570.0K
  768cf01d0d1afb971ecd1df04e2fcecfd0624c44  2024:27.0K 2025:18.0K
  7bbe134306da6eb743570fdae103d8af30bca6c5  2024:30.0K 2025:45.0K
  a0752d9fb76666fa99e73879d0da83b8f3c4a885  2024:36.0K 2026:3
  b365ac74c242b7dd1b0d5b271cb9cea2aa1a5668  2022:1.50M
  b762a528ed2ce6e9fa6bb6274c013b8865536ec2  2025:1.20M
  c65403e032fc0fce7256b84d5233eba7757c0dbf  2024:38
  d1bdcc330e7b66d20e34bb7a3f13ef9cdc37f9b1  2025:56.0K
  d2bb07e58883cd1738ce94cb5a0d9474006f43db  2023:24.0K 2024:16.0K 2025:72.0K
  de319e20e91f115e0d8b5543229309bfacb8f937  2025:3.72M
  eef4c692ec0c6d4db9b338569261906126139774  2024:270.0K
  ffcc541c51e1a3d052fed071309229e9dda81544  2025:224.0K

## where

STATE: TX 779.9K, LA 354.1K, AZ 288.4K, FL 215.5K, CA 158.9K, GA 102.3K, MS 61.6K, NY 53.7K, VA 52.4K, PA 47.8K, NM 45.9K, NJ 34.4K

## what

DETENTION_RELEASE_REASON: Transferred 62%, Removed 26%, Paroled 4%, Order of recognizance 3%, Bonded Out - IJ 2%, U.S. Marshals or other agency  1%, Paroled - Humanitarian 1%, Order of supervision 0%, Processing Disposition Changed 0%, Order of Recognizance - Humani 0%, Bonded Out - Field Office 0%

STAY_RELEASE_REASON: Removed 77%, Paroled 7%, Order of recognizance 5%, Bonded Out - IJ 4%, U.S. Marshals or other agency  2%, Paroled - Humanitarian 1%, Voluntary departure 1%, Order of supervision 1%, Bonded Out - Field Office 1%, Transferred 1%, Relief Granted by IJ 1%

GENDER: Male 89%, Female 11%, Unknown 0%

MARITAL_STATUS: Unknown 45%, Single 45%, Married 9%, Divorced 1%, Separated 0%, Widowed 0%

ETHNICITY: Hispanic Origin 90%, Not of Hispanic Origin 8%, Unknown 2%

KNOWN_TERRORIST_YES_NO: NO 99%, YES 1%

SUSPECTED_GANG_YES_NO: NO 98%, YES 2%

FELON: Not an Aggravated Felon 97%, Other 2%, Drugs 1%, Both (drug and other agg felon 0%

OFFENSE_INA_236C_YES_NO: N 95%, Y 5%

CASE_INA_236C_YES_NO: N 94%, Y 6%

CASE_STATUS: 8-Excluded/Removed - Inadmissi 46%, ACTIVE 26%, 6-Deported/Removed - Deportabi 11%, 3-Voluntary Departure Confirme 11%, 8-Excluded/Deported/Removed 2%, 9-VR Witnessed 1%, E-Charging Document Canceled b 1%, A-Proceedings Terminated 1%, B-Relief Granted 1%, 0-Withdrawal Permitted - I-275 0%, L-Legalization - Permanent Res 0%

CASE_CATEGORY: [8C] Excludable / Inadmissible 40%, [16] Reinstated Final Order 21%, [8B] Excludable / Inadmissible 13%, [8F] Expedited Removal 7%, [3] Deportable - Administrativ 6%, [1A] Voluntary Departure - Un- 5%, [2A] Deportable - Under Adjudi 2%, [8A] Excludable / Inadmissible 2%, [9] VR Under Safeguards 2%, [11] Administrative Deportatio 2%, [8D] Excludable / Inadmissible 1%

FINAL_ORDER_YES_NO: YES 65%, NO 35%

CASE_THREAT_LEVEL: NA 68%, 1 14%, 3 10%, 2 8%

DETAINEE_CLASSIFICATION: Low 59%, Medium / Low 16%, Medium / High 15%, High 10%

BOOK_IN_CRIMINALITY: 3 Other Immigration Violator 47%, 1 Convicted Criminal 32%, 2 Pending Criminal Charges 21%

RACE: White 82%, Unknown 9%, Black 5%, Asian or Pacific Islander 3%, American Indian or Alaskan Nat 0%, black 0%

FINAL_PROGRAM: ERO Criminal Alien Program 41%, Border Patrol 33%, Fugitive Operations 11%, Non-Detained Docket Control 5%, Inspections - Land 3%, Alternatives to Detention 2%, Homeland Security Investigatio 2%, Detained Docket Control 2%, 287G Program 1%, Detention and Deportation 1%, Inspections - Air 1%

MSC_CRIMINAL_CHARGE_STATUS: Convicted 100%, Pending 0%, Overturned 0%

MSC_CRIMINAL_CHARGE_STATUS_CODE: C 100%, P 0%, O 0%

MSC_CRIME_CLASS: Misdemeanor 51%, Felony 32%, Aggravated Felony 12%, Other 4%, Not Applicable 0%

BOOK_IN_AOR: New Orleans Area of Responsibi 21%, Phoenix Area of Responsibility 13%, Harlingen Area of Responsibili 11%, Miami Area of Responsibility 10%, Houston Area of Responsibility 8%, San Antonio Area of Responsibi 7%, Dallas Area of Responsibility 7%, El Paso Area of Responsibility 6%, Atlanta Area of Responsibility 6%, Chicago Area of Responsibility 4%, San Diego Area of Responsibili 4%, Los Angeles Area of Responsibi 3%

FILE_ORIGINAL: 2026-ICLI-00005_Detentions_FY2 34%, 2026-ICLI-00005_Detentions_FY2 24%, 2026-ICLI-00005_Detentions_FY2 22%, 2026-ICLI-00005_Detentions_FY2 19%, 2026-ICLI-00005_Detentions_Pri 1%

SHEET_ORIGINAL: FY2025 34%, FY2026 24%, FY2024 22%, FY2023 19%, Prior FY2023 1%

DUPLICATE_LIKELY_BOND: False 100%, True 0%

DUPLICATE_LIKELY_SAMEDAY: False 99%, True 1%

DUPLICATE_DROP_ROW: False 98%, True 2%

DUPLICATE_LIKELY: False 98%, True 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STAY_BOOK_IN_DATE_TIME | date | 469.2K | 0 | 2024-08-28 14:00:00+00:00 6.6K; 2024-08-20 14:50:00+00:00 6.6K; 2024-08-24 08:30:00+00:00 6.6K; 2024-08-23 00:51:00+00:00 6.6K |
| BOOK_IN_DATE_TIME | date | 748.7K | 0 | 2024-08-27 18:15:00+00:00 6.6K; 2024-08-31 15:00:00+00:00 6.6K; 2024-08-24 20:34:00+00:00 6.6K; 2024-08-27 22:00:00+00:00 6.6K |
| DETENTION_FACILITY | who | 732 | 0 | ALEXANDRIA STAGING FACILI 125.9K; PORT ISABEL SPC 118.1K; FLORENCE STAGING FACILITY 103.2K; MONTGOMERY PROCESSING CTR 52.9K |
| BOOK_OUT_DATE_TIME | date | 579.3K | 61.9K | 2024-08-27 03:55:00+00:00 6.5K; 2024-08-31 11:50:00+00:00 6.5K; 2024-09-04 15:44:00+00:00 6.5K; 2024-09-03 19:00:00+00:00 6.5K |
| STAY_BOOK_OUT_DATE_TIME | date | 320.7K | 177.3K | 2024-08-31 11:50:00+00:00 6.3K; 2024-08-30 08:30:00+00:00 6.3K; 2024-08-31 15:06:00+00:00 6.3K; 2024-08-29 07:25:00+00:00 6.3K |
| DETENTION_RELEASE_REASON | category | 28 | 102.8K | Transferred 1.54M; Removed 636.4K; Paroled 105.8K; Order of recognizance 66.6K |
| STAY_BOOK_OUT_DATE | date | 1.3K | 177.3K | 2024-11-22 8.9K; 2024-06-07 8.2K; 2025-04-29 8.1K; 2024-05-30 8.0K |
| STAY_RELEASE_REASON | category | 28 | 240.3K | Removed 1.79M; Paroled 156.5K; Order of recognizance 113.0K; Bonded Out - IJ 102.3K |
| RELIGION | who | 330 | 2.55M | CATHOLIC 27.6K; Unknown 6.6K; CATH 5.2K; Catholic 3.9K |
| GENDER | category | 3 | 0 | Male 2.32M; Female 294.7K; Unknown 688 |
| MARITAL_STATUS | category | 7 | 11.6K | Unknown 1.18M; Single 1.16M; Married 226.1K; Divorced 29.3K |
| ETHNICITY | category | 4 | 1.29M | Hispanic Origin 1.19M; Not of Hispanic Origin 106.5K; Unknown 22.9K |
| BIRTH_COUNTRY | who | 221 | 0 | MEXICO 697.4K; GUATEMALA 336.3K; HONDURAS 271.0K; VENEZUELA 180.8K |
| CITIZENSHIP_COUNTRY | who | 208 | 9 | MEXICO 698.3K; GUATEMALA 336.6K; HONDURAS 270.9K; VENEZUELA 179.1K |
| ENTRY_STATUS | who | 58 | 218.9K | Not  Applicable 1.47M; PWA Mexico 780.3K; No Documents 31.4K; Other Applicant for Admis 30.6K |
| KNOWN_TERRORIST_YES_NO | category | 2 | 0 | NO 2.60M; YES 13.7K |
| SUSPECTED_GANG_YES_NO | category | 2 | 0 | NO 2.56M; YES 54.6K |
| MSC_CHARGE | who | 420 | 1.78M | Driving Under Influence L 106.8K; Illegal Entry (INA SEC.10 67.4K; Assault 55.6K; Traffic Offense 50.7K |
| MSC_SENTENCE_DAYS | other | 652 | 2.34M | 30 31.9K; 180 16.9K; 90 15.9K; 60 14.8K |
| MSC_SENTENCE_MONTHS | other | 325 | 2.44M | 12 22.4K; 6 22.0K; 11 11.0K; 18 7.9K |
| MSC_SENTENCE_YEARS | other | 92 | 2.46M | 2 31.9K; 1 24.6K; 5 22.1K; 3 21.5K |
| MOST_SERIOUS_CONVICTION_CODE | other | 421 | 1.78M | 5404 106.8K; 0301 67.4K; 1399 55.6K; 5499 50.7K |
| FELON | category | 5 | 1.31M | Not an Aggravated Felon 1.26M; Other 28.3K; Drugs 13.4K; Both (drug and other agg  3.9K |
| OFFENSE_INA_236C_YES_NO | category | 3 | 78.3K | N 2.41M; Y 127.4K |
| CASE_INA_236C_YES_NO | category | 3 | 14.6K | N 2.45M; Y 148.8K |
| BOND_POSTED_DATE | date | 57.4K | 2.43M | 2022-07-21 00:00:00+00:00 462; 2016-07-19 00:00:00+00:00 460; 2010-10-15 00:00:00+00:00 460; 2019-09-23 00:00:00+00:00 364 |
| BOND_POSTED_AMOUNT | amount | 131 | 2.43M | 5000 35.8K; 10000 23.7K; 7500 16.5K; 1500 16.2K |
| CASE_STATUS | category | 15 | 14.6K | 8-Excluded/Removed - Inad 1.20M; ACTIVE 677.1K; 6-Deported/Removed - Depo 288.5K; 3-Voluntary Departure Con 282.4K |
| CASE_CATEGORY | category | 28 | 508.4K | [8C] Excludable / Inadmis 829.9K; [16] Reinstated Final Ord 439.4K; [8B] Excludable / Inadmis 260.2K; [8F] Expedited Removal 147.5K |
| FINAL_ORDER_YES_NO | category | 3 | 14.6K | YES 1.70M; NO 901.7K |
| FINAL_ORDER_DATE | date | 11.6K | 916.2K | 2024-08-09 6.6K; 2025-04-16 6.3K; 2024-05-21 5.6K; 2024-05-09 5.5K |
| CASE_THREAT_LEVEL | category | 5 | 14.6K | NA 1.76M; 1 370.3K; 3 267.7K; 2 202.3K |
| DETAINEE_CLASSIFICATION | category | 4 | 0 | Low 1.55M; Medium / Low 414.8K; Medium / High 382.5K; High 266.5K |
| FINAL_CHARGE | who | 165 | 757.8K | ALIEN PRESENT WITHOUT ADM 730.1K; IMMIGRANT WITHOUT AN IMMI 562.6K; ALIEN PREVIOUSLY REMOVED  112.6K; PREVIOUSLY ORDERED REMOVE 89.7K |
| DEPARTED_DATE | date | 1.3K | 756.4K | 2025-04-30 7.9K; 2025-05-14 7.6K; 2025-05-30 7.2K; 2024-11-18 6.7K |
| DEPARTURE_COUNTRY | who | 218 | 757.0K | MEXICO 625.9K; GUATEMALA 278.4K; HONDURAS 228.7K; COLOMBIA 95.4K |
| INITIAL_BOND_SET_AMOUNT | amount | 164 | 2.42M | 5000 36.8K; 10000 25.6K; 7500 17.4K; 1500 16.7K |
| INITIAL_BOND_SET_DATE | date | 3.4K | 2.60M | 2019-11-13 69; 2025-01-17 66; 2025-07-31 65; 2017-06-12 57 |
| DETENTION_FACILITY_CODE | who | 704 | 0 | JENATLA 125.9K; PIC 118.1K; FSF 103.2K; MTGPCTX 52.9K |
| BIRTH_YEAR | other | 93 | 1 | 1997 100.9K; 1995 99.5K; 1999 99.5K; 1996 99.4K |
| BOOK_IN_CRIMINALITY | category | 3 | 0 | 3 Other Immigration Viola 1.23M; 1 Convicted Criminal 834.6K; 2 Pending Criminal Charge 555.6K |
| RACE | category | 7 | 41.4K | White 2.10M; Unknown 243.9K; Black 140.6K; Asian or Pacific Islander 85.2K |
| ENTRY_DATE | date | 15.3K | 1.04M | 2024-05-05 6.2K; 2024-04-04 6.0K; 2024-08-23 5.8K; 2024-07-10 5.8K |
| FINAL_PROGRAM | category | 29 | 82.9K | ERO Criminal Alien Progra 1.01M; Border Patrol 821.8K; Fugitive Operations 282.1K; Non-Detained Docket Contr 113.9K |
| MSC_CHARGE_DATE | date | 13.8K | 1.80M | 2024-08-23 2.6K; 2024-08-29 2.6K; 2024-07-22 2.6K; 2024-08-06 2.5K |
| MSC_CONVICTION_DATE | date | 12.6K | 1.78M | 2024-07-11 3.7K; 2024-07-16 3.2K; 2024-05-30 3.1K; 2024-08-23 2.7K |
| MSC_CRIMINAL_CHARGE_STATUS | category | 4 | 1.78M | Convicted 840.3K; Pending 23; Overturned 3 |
| MSC_CRIMINAL_CHARGE_STATUS_CODE | category | 4 | 1.78M | C 840.3K; P 23; O 3 |
| MSC_CRIME_CLASS | category | 6 | 1.80M | Misdemeanor 420.0K; Felony 262.9K; Aggravated Felony 96.5K; Other 36.4K |
| BOOK_IN_SITE | who | 224 | 0 | ERO - Oakdale, LA Sub-Off 189.3K; FLORENCE, AZ, SERVICE PRO 186.3K; PORT ISABEL, TX, DOCKET C 143.8K; KROME, MIAMI, FL, DOCKET  134.4K |
| BOOK_IN_AOR | category | 25 | 0 | New Orleans Area of Respo 466.8K; Phoenix Area of Responsib 275.8K; Harlingen Area of Respons 229.8K; Miami Area of Responsibil 223.3K |
| UNIQUE_IDENTIFIER | who | 989.7K | 7.3K | 332c329184b35b152a47050ba 3.5K; d7f4d3c159bc33ca8376a147f 3.5K; db75322045d0b64475bef8e4d 3.5K; ee90c6650b0bde4d449c1734e 3.5K |
| STAY_ID | other | 1.10M | 7.3K | 332c329184b35b152a47050ba 3.5K; d7f4d3c159bc33ca8376a147f 3.5K; db75322045d0b64475bef8e4d 3.5K; ee90c6650b0bde4d449c1734e 3.5K |
| FILE_ORIGINAL | category | 5 | 0 | 2026-ICLI-00005_Detention 891.0K; 2026-ICLI-00005_Detention 628.1K; 2026-ICLI-00005_Detention 572.1K; 2026-ICLI-00005_Detention 501.2K |
| SHEET_ORIGINAL | category | 5 | 0 | FY2025 891.0K; FY2026 628.1K; FY2024 572.1K; FY2023 501.2K |
| ROW_ORIGINAL | other | 891.0K | 0 | 498608 1.9K; 61252 1.9K; 127119 1.9K; 148567 1.9K |
| STINT_ID | id | 2.59M | 7.3K | df7f31a256818bc5a575d9a72 1.9K; 1b6f79635987a3dd63ae310e6 1.9K; 3954a4aabb32367a878d98522 1.9K; 4304e2ba2487c83e46db4b4c1 1.9K |
| INITIAL_BOND_SET_AMOUNT_LOWEST_SEEN | amount | 157 | 2.42M | 5000 37.0K; 10000 24.4K; 1500 17.3K; 7500 16.9K |
| INITIAL_BOND_SET_DATE_EARLIEST_SEEN | date | 3.4K | 2.59M | 2019-09-25 82; 2019-12-03 79; 2019-11-13 76; 2019-05-01 74 |
| BOND_POSTED_AMOUNT_LOWEST_SEEN | amount | 129 | 2.43M | 5000 36.4K; 10000 22.9K; 1500 17.0K; 7500 16.2K |
| BOND_POSTED_DATE_EARLIEST_SEEN | date | 55.6K | 2.43M | 2022-07-21 00:00:00+00:00 468; 2016-07-19 00:00:00+00:00 466; 2010-10-15 00:00:00+00:00 465; 2011-12-23 00:00:00+00:00 391 |
| DUPLICATE_LIKELY_BOND | category | 2 | 0 | False 2.61M; True 11.6K |
| DUPLICATE_LIKELY_SAMEDAY | category | 2 | 0 | False 2.58M; True 34.2K |
| DUPLICATE_DROP_ROW | category | 2 | 0 | False 2.57M; True 45.9K |
| DUPLICATE_LIKELY | category | 3 | 7.3K | False 2.56M; True 45.9K |
| CITY | who | 414 | 396.9K | Florence 161.8K; Alexandria 125.9K; Los Fresnos 118.5K; El Paso 86.4K |
| STATE | state | 56 | 3.7K | TX 779.9K; LA 354.1K; AZ 288.4K; FL 215.5K |
| COUNTY | who | 342 | 397.8K | Pinal 207.3K; Rapides 125.9K; Cameron 118.5K; El Paso 86.4K |
| INGESTED_AT | audit | 1 | 0 | 1785991945282269 2.62M |
| SOURCE_RUN_ID | audit | 1 | 0 | fa50cba6-210d-49cb-be0e-0 2.62M |
| SRC_SHA256 | other | 1 | 0 | f46ab153e30aa8da5687e9550 2.62M |
