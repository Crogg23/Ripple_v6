# PORTAL_CKA_OKLAHOMA_OPEN_DA_5EDE090003

rows 1.4K  columns 18  scan 4.5s

roles: amount 1, audit 2, category 4, date 3, other 4, who 5

## when

PO_DATE
  2024      1.3K  ##############################
  2025       146  ###

REQUISITION_DATE
  2020         2  
  2023         4  
  2024      1.2K  ##############################
  2025       142  ###

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 1.4K | 0 | 30.0K | 2.36M | 61.44M | 286.03M |

## who

BUSINESS_UNIT_NAME by rows
       623  Mental Health & Subst Abuse Sv
       125  Department of Health
        53  Dept of Environmental Quality
        49  Department of Transportation
        47  Department of Human Services
        42  Insurance Department
        42  Service Oklahoma
        41  Oklahoma Tax Commission
        31  Attorney General
        29  State Bureau of Investigation
        28  Department of Veterans Affairs
        26  Department of Public Safety
        21  District Attorneys Council
        20  Wildlife Conservation
        16  Department of Agriculture
        16  Department of Libraries
        15  Narc & Dangerous Drugs Control
        14  Council on Law Enfc Ed & Trng
        14  Dept of Rehabilitation Service
        10  Historical Society

BUSINESS_UNIT_NAME by dollars
     104.17M      623 rows  Mental Health & Subst Abuse Sv
      67.62M       10 rows  Health Care Authority
      36.77M       47 rows  Department of Human Services
      11.64M       16 rows  Department of Agriculture
      10.44M       42 rows  Service Oklahoma
      10.40M      125 rows  Department of Health
       4.86M        7 rows  OESC
       4.30M        7 rows  Department of Commerce
       4.13M       49 rows  Department of Transportation
       3.77M       31 rows  Attorney General
       3.39M       53 rows  Dept of Environmental Quality
       2.63M       29 rows  State Bureau of Investigation
       2.31M       26 rows  Department of Public Safety
       1.59M        9 rows  Okla Education Television Auth
       1.55M       14 rows  Dept of Rehabilitation Service
       1.37M       41 rows  Oklahoma Tax Commission
       1.35M       15 rows  Narc & Dangerous Drugs Control
       1.32M        6 rows  Dept of Career and Tech Educ
       1.25M       42 rows  Insurance Department
       1.19M        3 rows  Department of Education

VENDOR by rows
        42  CREOKS BEHAVIORAL HEALTH SERVICES
        38  GRAND LAKE MENTAL HEALTH CENTER INC
        33  THE OKLAHOMA MENTAL HEALTH COUNCIL
        30  SPACES INC
        29  FAMILY & CHILDRENS SERVICE INC
        24  NORTH OKLAHOMA COUNTY MENTAL HEALTH CENT
        24  HOLOGIC INC
        24  HOPE COMMUNITY SERVICES INC
        23  REVVITY HEALTH SCIENCES INC
        23  THE AMERICAN ASSOCIATION OF MOTOR VEHICL
        21  LIFE TECHNOLOGIES CORPORATION
        19  LIGHTHOUSE BEHAVIORAL WELLNESS CENTERS I
        19  WINDSOR SOLUTIONS INC
        18  GREEN COUNTRY BEHAVIORAL HEALTH SERVICES
        17  INVISALERT SOLUTIONS INC
        16  TOUCHPOINT MEDICAL INC
        16  LABWARE INC
        16  PROJECT HALO HOLDINGS LLC
        14  OCLC INC
        14  FAIRFAX IMAGING INC

VENDOR by dollars
      61.44M        1 rows  GAINWELL ACQUISITION CORP
      24.22M        2 rows  RESPECTFUL PARTNERS INC
      18.06M       29 rows  FAMILY & CHILDRENS SERVICE INC
      15.71M       38 rows  GRAND LAKE MENTAL HEALTH CENTER INC
      10.47M       42 rows  CREOKS BEHAVIORAL HEALTH SERVICES
       9.50M        1 rows  FUTURE FARMERS OF AMERICA
       6.75M        5 rows  FAST LP
       5.90M       33 rows  THE OKLAHOMA MENTAL HEALTH COUNCIL
       5.66M       24 rows  HOPE COMMUNITY SERVICES INC
       5.29M       19 rows  LIGHTHOUSE BEHAVIORAL WELLNESS CENTERS I
       4.39M        1 rows  EMERGENT DEVICES INC
       4.38M       24 rows  NORTH OKLAHOMA COUNTY MENTAL HEALTH CENT
       4.36M        3 rows  EVIDEN USA INC
       3.73M        1 rows  CATHOLIC CHARITIES ARCHDIOCESE OF OKC
       3.17M        4 rows  VITECH SYSTEMS SUB LLC
       3.00M        1 rows  NORSUN OK LLC
       3.00M        4 rows  SAGE PURSUITS INC
       2.93M       18 rows  GREEN COUNTRY BEHAVIORAL HEALTH SERVICES
       2.76M        9 rows  MYCARE INTEGRATED SOFTWARE SOLUTIONS LLC
       2.61M       23 rows  REVVITY HEALTH SCIENCES INC

BUSINESS_UNIT by rows
       623  45200
       125  34000
        53  29200
        49  34500
        47  83000
        42  64000
        42  38500
        41  69500
        31  04900
        29  30800
        28  65000
        26  58500
        21  22000
        20  32000
        16  43000
        16  04000
        15  47700
        14  80500
        14  41500
        10  35000

BUSINESS_UNIT by dollars
     104.17M      623 rows  45200
      67.62M       10 rows  80700
      36.77M       47 rows  83000
      11.64M       16 rows  04000
      10.44M       42 rows  64000
      10.40M      125 rows  34000
       4.86M        7 rows  29000
       4.30M        7 rows  16000
       4.13M       49 rows  34500
       3.77M       31 rows  04900
       3.39M       53 rows  29200
       2.63M       29 rows  30800
       2.31M       26 rows  58500
       1.59M        9 rows  26600
       1.55M       14 rows  80500
       1.37M       41 rows  69500
       1.35M       15 rows  47700
       1.32M        6 rows  80000
       1.25M       42 rows  38500
       1.19M        3 rows  26500

FEDERAL_IDENTIFICATION_2 by rows
        42  731108774
        38  731039733
        33  736111618
        30  731569748
        29  730580270
        24  731134098
        24  731098634
        24  042902449
        23  530172317
        23  043361624
        21  330373077
        19  730618672
        19  931245518
        18  731084521
        17  833174567
        16  208696880
        16  820631018
        16  812602060
        14  310734115
        14  541701382

FEDERAL_IDENTIFICATION_2 by dollars
      61.44M        1 rows  851850812
      18.06M       29 rows  730580270
      15.71M       38 rows  731039733
      10.47M       42 rows  731108774
       6.75M        5 rows  300951152
       5.90M       33 rows  736111618
       5.66M       24 rows  731098634
       5.29M       19 rows  730618672
       4.39M        1 rows  364778238
       4.38M       24 rows  731134098
       4.36M        3 rows  884399707
       3.73M        1 rows  730636561
       3.17M        4 rows  133785492
       3.00M        4 rows  900766239
       2.93M       18 rows  731084521
       2.76M        9 rows  823743778
       2.61M       23 rows  043361624
       2.59M        9 rows  731064338
       2.56M        2 rows  842133828
       2.52M        4 rows  811745068

## who x when

BUSINESS_UNIT_NAME by PO_DATE, dollars = AMOUNT
  Attorney General                          2024:1.56M 2025:2.21M
  Council on Law Enfc Ed & Trng             2024:82.0K 2025:16.5K
  Department of Agriculture                 2024:1.93M 2025:9.71M
  Department of Commerce                    2024:4.30M
  Department of Education                   2024:1.19M
  Department of Health                      2024:7.37M 2025:3.03M
  Department of Human Services              2024:11.29M 2025:25.47M
  Department of Libraries                   2024:554.1K
  Department of Public Safety               2024:1.49M 2025:817.4K
  Department of Transportation              2024:3.40M 2025:724.0K
  Department of Veterans Affairs            2024:878.8K 2025:62.9K
  Dept of Career and Tech Educ              2024:1.32M
  Dept of Environmental Quality             2024:3.24M 2025:150.0K
  Dept of Rehabilitation Service            2024:1.29M 2025:258.8K
  District Attorneys Council                2024:902.1K 2025:2.2K
  Health Care Authority                     2024:64.45M 2025:3.17M
  Historical Society                        2024:353.4K
  Insurance Department                      2024:1.19M 2025:62.2K
  Mental Health & Subst Abuse Sv            2024:103.70M 2025:479.1K
  Narc & Dangerous Drugs Control            2024:734.5K 2025:615.9K
  OESC                                      2024:4.81M 2025:52.6K
  Okla Education Television Auth            2024:1.20M 2025:397.0K
  Oklahoma Tax Commission                   2024:917.4K 2025:455.1K
  Service Oklahoma                          2024:10.32M 2025:119.2K
  State Bureau of Investigation             2024:1.61M 2025:1.02M
  Wildlife Conservation                     2024:485.6K 2025:42.6K

VENDOR by PO_DATE, dollars = AMOUNT
  CATHOLIC CHARITIES ARCHDIOCESE OF OKC     2024:3.73M
  CREOKS BEHAVIORAL HEALTH SERVICES         2024:10.47M
  EMERGENT DEVICES INC                      2024:4.39M
  EVIDEN USA INC                            2024:4.36M
  FAIRFAX IMAGING INC                       2025:574.3K
  FAMILY & CHILDRENS SERVICE INC            2024:18.06M
  FAST LP                                   2024:6.75M
  FUTURE FARMERS OF AMERICA                 2025:9.50M
  GAINWELL ACQUISITION CORP                 2024:61.44M
  GRAND LAKE MENTAL HEALTH CENTER INC       2024:15.71M
  GREEN COUNTRY BEHAVIORAL HEALTH SERVICES  2024:2.93M
  HOLOGIC INC                               2024:663.4K
  HOPE COMMUNITY SERVICES INC               2024:5.66M
  INVISALERT SOLUTIONS INC                  2024:525.1K
  LABWARE INC                               2024:582.7K
  LIFE TECHNOLOGIES CORPORATION             2024:245.0K 2025:211.0K
  LIGHTHOUSE BEHAVIORAL WELLNESS CENTERS I  2024:5.29M
  NORSUN OK LLC                             2024:3.00M
  NORTH OKLAHOMA COUNTY MENTAL HEALTH CENT  2024:4.38M
  OCLC INC                                  2024:527.3K
  PROJECT HALO HOLDINGS LLC                 2024:268.6K 2025:5.2K
  RESPECTFUL PARTNERS INC                   2025:24.22M
  REVVITY HEALTH SCIENCES INC               2024:2.61M
  SAGE PURSUITS INC                         2025:3.00M
  SPACES INC                                2024:919.5K
  THE AMERICAN ASSOCIATION OF MOTOR VEHICL  2024:378.2K
  THE OKLAHOMA MENTAL HEALTH COUNCIL        2024:5.90M
  TOUCHPOINT MEDICAL INC                    2024:150.6K 2025:16.3K
  VITECH SYSTEMS SUB LLC                    2025:3.17M
  WINDSOR SOLUTIONS INC                     2024:1.26M

## what

LINE_NBR: 1 45%, 2 15%, 3 9%, 4 7%, 5 5%, 6 4%, 7 4%, 8 3%, 9 2%, 10 2%, 11 2%, 12 2%

SS_TYPE: TYP1 - Sole Make/Model/Brand 74%, TYP3 - Additional / Replacemen 16%, TYP2 - Sole Vendor 7%, TYP4 - Original Vendor 2%, TYP8 - Statute Authorization 0%, TYP5 - Brand Name for Resale 0%

ORIGIN: CHG 44%, CP 19%, AGY 18%, OSF 17%, EXC 2%

FEDERAL_IDENTIFICATION: TIN 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_UNIT | who | 54 | 0 | 45200 623; 34000 125; 29200 53; 34500 49 |
| BUSINESS_UNIT_NAME | who | 54 | 0 | Mental Health & Subst Abu 623; Department of Health 125; Dept of Environmental Qua 53; Department of Transportat 49 |
| PO_ID | other | 556 | 0 | 4529067895 42; 4529067843 38; 4529067866 33; 4529067762 27 |
| LINE_NBR | category | 44 | 0 | 1 540; 2 180; 3 113; 4 87 |
| VENDOR | who | 413 | 0 | CREOKS BEHAVIORAL HEALTH  42; GRAND LAKE MENTAL HEALTH  38; THE OKLAHOMA MENTAL HEALT 33; SPACES INC 30 |
| DESC | other | 1.0K | 0 | SUD - Outpatient - VBP -  38; GRANT:Federal Funding to  37; Flex Funds - Housing - St 29; Office Furniture 26 |
| AMOUNT | amount | 862 | 0 | 0 96; 50000 29; 20000 25; 40000 24 |
| PO_DATE | date | 193 | 0 | 2024-06-19 00:00:00 94; 2024-06-12 00:00:00 60; 2024-06-25 00:00:00 51; 2024-06-24 00:00:00 50 |
| SS_TYPE | category | 7 | 1 | TYP1 - Sole Make/Model/Br 1.0K; TYP3 - Additional / Repla 218; TYP2 - Sole Vendor 102; TYP4 - Original Vendor 34 |
| ORIGIN | category | 5 | 0 | CHG 616; CP 265; AGY 254; OSF 237 |
| REQUISITION_ID | other | 675 | 69 | 4520012151 28; 3400026644 27; 3400026762 26; 6400000382 26 |
| REQUISITION_DATE | date | 234 | 30 | 2024-06-11 00:00:00 87; 2024-06-10 00:00:00 49; 2024-06-12 00:00:00 38; 2024-09-18 00:00:00 34 |
| CATEGORY_CODE | other | 225 | 0 | 85111617 259; 85101500 243; 81111805 62; 81112200 58 |
| FEDERAL_IDENTIFICATION | category | 2 | 56 | TIN 1.3K |
| FEDERAL_IDENTIFICATION_2 | who | 379 | 56 | 731108774 42; 731039733 38; 736111618 33; 731569748 30 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:26:09.75307 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 94dcdfc1-48f3-4340-a2d2-7 1.4K |
| SRC_SHA256 | who | 1 | 0 | 0623f5682404f63a37a4bbc39 1.4K |
