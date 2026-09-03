# PORTAL_CKA_OKLAHOMA_OPEN_DA_46271D5059

rows 1.4K  columns 18  scan 4.5s

roles: amount 1, audit 2, category 4, date 3, other 4, who 5

## when

PO_DATE
  2024      1.2K  ##############################
  2025       224  ######

REQUISITION_DATE
  2023         4  
  2024      1.1K  ##############################
  2025       263  #######

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 1.4K | 0 | 28.3K | 2.16M | 61.44M | 282.41M |

## who

BUSINESS_UNIT_NAME by rows
       640  Mental Health & Subst Abuse Sv
       130  Department of Health
        55  Dept of Environmental Quality
        50  Department of Transportation
        40  Insurance Department
        40  Service Oklahoma
        39  Department of Human Services
        32  State Bureau of Investigation
        31  Department of Public Safety
        27  Attorney General
        27  Department of Veterans Affairs
        26  Wildlife Conservation
        17  Department of Agriculture
        17  District Attorneys Council
        16  Department of Libraries
        14  Dept of Rehabilitation Service
        14  Narc & Dangerous Drugs Control
        13  Council on Law Enfc Ed & Trng
        12  Oklahoma Tax Commission
        10  Health Care Authority

BUSINESS_UNIT_NAME by dollars
     104.58M      640 rows  Mental Health & Subst Abuse Sv
      67.62M       10 rows  Health Care Authority
      35.93M       39 rows  Department of Human Services
      11.66M       17 rows  Department of Agriculture
      10.52M      130 rows  Department of Health
       7.91M       40 rows  Service Oklahoma
       4.56M        6 rows  OESC
       4.28M        6 rows  Department of Commerce
       4.24M       50 rows  Department of Transportation
       3.24M       31 rows  Department of Public Safety
       2.74M       32 rows  State Bureau of Investigation
       2.63M       55 rows  Dept of Environmental Quality
       2.30M       27 rows  Attorney General
       2.26M       14 rows  Dept of Rehabilitation Service
       1.60M        9 rows  Dept of Career and Tech Educ
       1.59M        9 rows  Okla Education Television Auth
       1.28M       14 rows  Narc & Dangerous Drugs Control
       1.19M        3 rows  Department of Education
      975.5K        4 rows  State Treasurer
      933.3K       40 rows  Insurance Department

VENDOR by rows
        42  CREOKS BEHAVIORAL HEALTH SERVICES
        39  GRAND LAKE MENTAL HEALTH CENTER INC
        34  THE OKLAHOMA MENTAL HEALTH COUNCIL
        30  FAMILY & CHILDRENS SERVICE INC
        26  REVVITY HEALTH SCIENCES INC
        25  NORTH OKLAHOMA COUNTY MENTAL HEALTH CENT
        24  HOLOGIC INC
        24  HOPE COMMUNITY SERVICES INC
        23  THE AMERICAN ASSOCIATION OF MOTOR VEHICL
        21  LIFE TECHNOLOGIES CORPORATION
        21  TOUCHPOINT MEDICAL INC
        20  LIGHTHOUSE BEHAVIORAL WELLNESS CENTERS I
        19  WINDSOR SOLUTIONS INC
        18  GREEN COUNTRY BEHAVIORAL HEALTH SERVICES
        17  INVISALERT SOLUTIONS INC
        16  LABWARE INC
        16  PROJECT HALO HOLDINGS LLC
        14  FAIRFAX IMAGING INC
        14  OCLC INC
        13  COMMUNITY TREATMENT INTEGRATIONS OK INC

VENDOR by dollars
      61.44M        1 rows  GAINWELL ACQUISITION CORP
      24.22M        2 rows  RESPECTFUL PARTNERS INC
      18.06M       30 rows  FAMILY & CHILDRENS SERVICE INC
      15.96M       39 rows  GRAND LAKE MENTAL HEALTH CENTER INC
      10.47M       42 rows  CREOKS BEHAVIORAL HEALTH SERVICES
       9.50M        1 rows  FUTURE FARMERS OF AMERICA
       6.75M        5 rows  FAST LP
       5.90M       34 rows  THE OKLAHOMA MENTAL HEALTH COUNCIL
       5.67M       24 rows  HOPE COMMUNITY SERVICES INC
       4.39M       25 rows  NORTH OKLAHOMA COUNTY MENTAL HEALTH CENT
       4.39M        1 rows  EMERGENT DEVICES INC
       4.36M        3 rows  EVIDEN USA INC
       3.89M       20 rows  LIGHTHOUSE BEHAVIORAL WELLNESS CENTERS I
       3.73M        1 rows  CATHOLIC CHARITIES ARCHDIOCESE OF OKC
       3.17M        4 rows  VITECH SYSTEMS SUB LLC
       3.00M        1 rows  NORSUN OK LLC
       3.00M        4 rows  SAGE PURSUITS INC
       2.93M       18 rows  GREEN COUNTRY BEHAVIORAL HEALTH SERVICES
       2.76M        9 rows  MYCARE INTEGRATED SOFTWARE SOLUTIONS LLC
       2.65M       26 rows  REVVITY HEALTH SCIENCES INC

BUSINESS_UNIT by rows
       640  45200
       130  34000
        55  29200
        50  34500
        40  38500
        40  64000
        39  83000
        32  30800
        31  58500
        27  4900
        27  65000
        26  32000
        17  4000
        17  22000
        16  43000
        14  80500
        14  47700
        13  41500
        12  69500
        10  56600

BUSINESS_UNIT by dollars
     104.58M      640 rows  45200
      67.62M       10 rows  80700
      35.93M       39 rows  83000
      11.66M       17 rows  4000
      10.52M      130 rows  34000
       7.91M       40 rows  64000
       4.56M        6 rows  29000
       4.28M        6 rows  16000
       4.24M       50 rows  34500
       3.24M       31 rows  58500
       2.74M       32 rows  30800
       2.63M       55 rows  29200
       2.30M       27 rows  4900
       2.26M       14 rows  80500
       1.60M        9 rows  80000
       1.59M        9 rows  26600
       1.28M       14 rows  47700
       1.19M        3 rows  26500
      975.5K        4 rows  74000
      933.3K       40 rows  38500

FEDERAL_IDENTIFICATION_2 by rows
        42  731108774
        39  731039733
        34  736111618
        30  730580270
        26  43361624
        25  731134098
        24  731098634
        24  42902449
        23  530172317
        21  330373077
        21  812602060
        20  730618672
        19  931245518
        18  731084521
        17  833174567
        16  820631018
        15  208696880
        14  310734115
        14  541701382
        13  862303924

FEDERAL_IDENTIFICATION_2 by dollars
      61.44M        1 rows  851850812
      18.06M       30 rows  730580270
      15.96M       39 rows  731039733
      10.47M       42 rows  731108774
       6.75M        5 rows  300951152
       5.90M       34 rows  736111618
       5.67M       24 rows  731098634
       4.39M       25 rows  731134098
       4.39M        1 rows  364778238
       4.36M        3 rows  884399707
       3.89M       20 rows  730618672
       3.73M        1 rows  730636561
       3.17M        4 rows  133785492
       3.00M        4 rows  900766239
       2.93M       18 rows  731084521
       2.76M        9 rows  823743778
       2.65M       26 rows  43361624
       2.56M        2 rows  842133828
       2.39M        9 rows  731064338
       2.13M       13 rows  862303924

## who x when

BUSINESS_UNIT_NAME by PO_DATE, dollars = AMOUNT
  Attorney General                          2024:90.0K 2025:2.21M
  Council on Law Enfc Ed & Trng             2024:42.0K 2025:16.5K
  Department of Agriculture                 2024:1.93M 2025:9.73M
  Department of Commerce                    2024:4.28M
  Department of Education                   2024:1.19M
  Department of Health                      2024:7.00M 2025:3.52M
  Department of Human Services              2024:10.42M 2025:25.51M
  Department of Libraries                   2024:554.1K
  Department of Public Safety               2024:1.39M 2025:1.85M
  Department of Transportation              2024:3.39M 2025:848.6K
  Department of Veterans Affairs            2024:845.6K 2025:62.9K
  Dept of Career and Tech Educ              2024:1.55M 2025:47.2K
  Dept of Environmental Quality             2024:2.41M 2025:225.0K
  Dept of Rehabilitation Service            2024:1.23M 2025:1.03M
  District Attorneys Council                2024:692.9K 2025:2.2K
  Health Care Authority                     2024:64.41M 2025:3.21M
  Insurance Department                      2024:778.6K 2025:154.8K
  Mental Health & Subst Abuse Sv            2024:103.38M 2025:1.20M
  Narc & Dangerous Drugs Control            2024:663.4K 2025:615.9K
  OESC                                      2024:4.50M 2025:52.6K
  Okla Education Television Auth            2024:1.20M 2025:397.0K
  Oklahoma Tax Commission                   2025:455.1K
  Service Oklahoma                          2024:7.75M 2025:152.3K
  State Bureau of Investigation             2024:1.21M 2025:1.53M
  State Treasurer                           2024:965.0K 2025:10.5K
  Wildlife Conservation                     2024:491.4K 2025:183.3K

VENDOR by PO_DATE, dollars = AMOUNT
  CATHOLIC CHARITIES ARCHDIOCESE OF OKC     2024:3.73M
  COMMUNITY TREATMENT INTEGRATIONS OK INC   2024:2.13M
  CREOKS BEHAVIORAL HEALTH SERVICES         2024:10.47M
  EMERGENT DEVICES INC                      2024:4.39M
  EVIDEN USA INC                            2024:4.36M
  FAIRFAX IMAGING INC                       2025:574.3K
  FAMILY & CHILDRENS SERVICE INC            2024:18.06M
  FAST LP                                   2024:6.75M
  FUTURE FARMERS OF AMERICA                 2025:9.50M
  GAINWELL ACQUISITION CORP                 2024:61.44M
  GRAND LAKE MENTAL HEALTH CENTER INC       2024:15.96M
  GREEN COUNTRY BEHAVIORAL HEALTH SERVICES  2024:2.93M
  HOLOGIC INC                               2024:663.4K
  HOPE COMMUNITY SERVICES INC               2024:5.67M
  INVISALERT SOLUTIONS INC                  2024:525.1K
  LABWARE INC                               2024:450.7K 2025:182.4K
  LIFE TECHNOLOGIES CORPORATION             2024:245.0K 2025:211.0K
  LIGHTHOUSE BEHAVIORAL WELLNESS CENTERS I  2024:3.89M
  NORSUN OK LLC                             2024:3.00M
  NORTH OKLAHOMA COUNTY MENTAL HEALTH CENT  2024:4.39M
  OCLC INC                                  2024:527.3K
  PROJECT HALO HOLDINGS LLC                 2024:268.6K 2025:5.2K
  RESPECTFUL PARTNERS INC                   2025:24.22M
  REVVITY HEALTH SCIENCES INC               2024:2.65M
  SAGE PURSUITS INC                         2025:3.00M
  THE AMERICAN ASSOCIATION OF MOTOR VEHICL  2024:378.2K
  THE OKLAHOMA MENTAL HEALTH COUNCIL        2024:5.90M
  TOUCHPOINT MEDICAL INC                    2024:157.0K 2025:207.7K
  VITECH SYSTEMS SUB LLC                    2025:3.17M
  WINDSOR SOLUTIONS INC                     2024:1.26M

## what

LINE_NBR: 1 43%, 2 16%, 3 10%, 4 8%, 5 6%, 6 4%, 7 3%, 8 3%, 9 2%, 10 2%, 11 2%, 12 1%

SS_TYPE: TYP1 - Sole Make/Model/Brand 77%, TYP3 - Additional / Replacemen 15%, TYP2 - Sole Vendor 6%, TYP4 - Original Vendor 2%, TYP8 - Statute Authorization 0%, TYP5 - Brand Name for Resale 0%

ORIGIN: CHG 48%, AGY 17%, CP 17%, OSF 17%, EXC 1%

FEDERAL_IDENTIFICATION: TIN 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_UNIT | who | 55 | 0 | 45200 640; 34000 130; 29200 55; 34500 50 |
| BUSINESS_UNIT_NAME | who | 55 | 0 | Mental Health & Subst Abu 640; Department of Health 130; Dept of Environmental Qua 55; Department of Transportat 50 |
| PO_ID | other | 546 | 0 | 4529067895 42; 4529067843 39; 4529067866 34; 4529067762 28 |
| LINE_NBR | category | 46 | 0 | 1 523; 2 188; 3 118; 4 92 |
| VENDOR | who | 408 | 0 | CREOKS BEHAVIORAL HEALTH  42; GRAND LAKE MENTAL HEALTH  39; THE OKLAHOMA MENTAL HEALT 34; FAMILY & CHILDRENS SERVIC 30 |
| DESC | other | 1.0K | 0 | SUD - Outpatient - VBP -  58; Flex Funds - Housing - St 31; GRANT:Federal Funding to  31; Criminal Justice - SQE -  20 |
| AMOUNT | amount | 847 | 0 | 0 125; 50000 29; 20000 26; 30000 23 |
| PO_DATE | date | 186 | 0 | 2024-06-19T00:00:00 95; 2024-06-12T00:00:00 64; 2024-06-25T00:00:00 53; 2024-06-24T00:00:00 53 |
| SS_TYPE | category | 7 | 2 | TYP1 - Sole Make/Model/Br 1.1K; TYP3 - Additional / Repla 204; TYP2 - Sole Vendor 80; TYP4 - Original Vendor 32 |
| ORIGIN | category | 5 | 0 | CHG 674; AGY 240; CP 236; OSF 233 |
| REQUISITION_ID | other | 689 | 67 | 3400026644 25; 6400000382 25; 4520012147 25; 4520012126 25 |
| REQUISITION_DATE | date | 241 | 11 | 2024-06-11T00:00:00 87; 2024-06-10T00:00:00 49; 2024-06-12T00:00:00 38; 2024-09-18T00:00:00 34 |
| CATEGORY_CODE | other | 228 | 0 | 85111617 279; 85101500 246; 81111805 61; 81112200 59 |
| FEDERAL_IDENTIFICATION | category | 2 | 69 | TIN 1.3K |
| FEDERAL_IDENTIFICATION_2 | who | 372 | 69 | 731108774 42; 731039733 39; 736111618 34; 730580270 30 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:26:15.72203 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 60064aa9-941c-4371-b57f-6 1.4K |
| SRC_SHA256 | who | 1 | 0 | 7ad7198601d48428ab7b2cacc 1.4K |
