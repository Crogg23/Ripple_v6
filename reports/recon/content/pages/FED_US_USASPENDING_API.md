# FED_US_USASPENDING_API

rows 300  columns 34  scan 2.6s

roles: amount 1, audit 2, category 5, date 3, empty 19, other 1, state 1, who 2

## when

START_DATE
  1978         3  ##
  1984         1  #
  1993         2  #
  1998         1  #
  1999         2  #
  2000         3  ##
  2001         2  #
  2003         5  ###
  2004         3  ##
  2005         4  ##
  2006         7  ####
  2007         6  ###
  2008        11  ######
  2009         5  ###
  2010         4  ##
  2011         8  #####
  2012         9  #####
  2013         6  ###
  2014         8  #####
  2015        10  ######
  2016        13  ########
  2017        21  ############
  2018        11  ######
  2019         8  #####
  2020        22  #############
  2021        12  #######
  2022        52  ##############################
  2023        50  #############################
  2024        11  ######

END_DATE
  2006         1  #
  2007         1  #
  2009         1  #
  2012         2  #
  2014         2  #
  2015         1  #
  2016         1  #
  2017         2  #
  2018         3  ##
  2019         3  ##
  2020         3  ##
  2021         3  ##
  2022         6  ####
  2023        46  ##############################
  2024        43  ############################
  2025        12  ########
  2026        15  ##########
  2027        16  ##########
  2028        10  #######
  2029         6  ####
  2030         8  #####
  2031         4  ###
  2032         2  #
  2033         3  ##
  2034         1  #
  2035         2  #

LAST_MODIFIED_DATE
  2023         1  
  2024        69  ###############
  2025        94  #####################
  2026       136  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AWARD_AMOUNT | 300 | 151.33M | 7.02B | 71.77B | 91.98B | 3334.20B |

## who

RECIPIENT_NAME by rows
        17  LOCKHEED MARTIN CORPORATION
        12  THE BOEING COMPANY
         9  HEALTH CARE SERVICES, CALIFORNIA DEPARTMENT OF
         8  LOCKHEED MARTIN CORP
         7  MERCK SHARP & DOHME LLC
         6  GLAXOSMITHKLINE, LLC
         6  PFIZER INC
         6  SANOFI VACCINES US INC.
         5  ELECTRIC BOAT CORPORATION
         5  LEIDOS, INC.
         4  NORTHROP GRUMMAN SYSTEMS CORPORATION
         4  VA DEPARTMENT OF MEDICAL ASSISTANCE SERVICE
         4  KBR WYLE SERVICES, LLC
         4  SCIENCE APPLICATIONS INTERNATIONAL CORPORATION
         4  NYS DEPARTMENT OF HEALTH
         4  AMENTUM TECHNOLOGY, INC.
         3  DEPARTMENT OF SOCIAL SERVICES CALIFORNIA
         3  HUMANA GOVERNMENT BUSINESS INC
         3  SPACE EXPLORATION TECHNOLOGIES CORP.
         3  BELL BOEING JOINT PROJECT OFFICE

RECIPIENT_NAME by dollars
     497.06B        9 rows  HEALTH CARE SERVICES, CALIFORNIA DEPARTMENT OF
     235.34B       17 rows  LOCKHEED MARTIN CORPORATION
     182.74B        4 rows  NYS DEPARTMENT OF HEALTH
     154.87B       12 rows  THE BOEING COMPANY
     111.46B        5 rows  ELECTRIC BOAT CORPORATION
     102.60B        8 rows  LOCKHEED MARTIN CORP
      80.02B        3 rows  HUMANA GOVERNMENT BUSINESS INC
      75.91B        3 rows  PA DEPARTMENT OF HUMAN SERVICES
      65.34B        2 rows  HEALTH & HUMAN SVC COMMN TX
      47.31B        2 rows  OHIO DEPARTMENT OF MEDICAID
      43.15B        4 rows  VA DEPARTMENT OF MEDICAL ASSISTANCE SERVICE
      42.91B        2 rows  HEALTH NET FEDERAL SERVICES, LLC
      42.62B        2 rows  FLORIDA AGENCY FOR HEALTH CARE ADMINISTRATION
      42.37B        1 rows  NATIONAL TECHNOLOGY & ENGINEERING SOLUTIONS OF SANDIA, LLC
      42.10B        1 rows  UT-BATTELLE LLC
      41.09B        1 rows  LAWRENCE LIVERMORE NATIONAL SECURITY, LLC
      39.29B        2 rows  ILLINOIS DEPARTMENT OF HEALTHCARE & FAMILY SERVICES
      37.75B        2 rows  THE REGENTS OF THE UNIVERSITY OF CALIFORNIA
      35.31B        2 rows  NORTH CAROLINA DEPARTMENT OF HEALTH & HUMAN SERVICES
      35.30B        1 rows  REGENTS OF THE UNIVERSITY OF CALIFORNIA, THE

_SRC_SHA256 by rows
       300  1c52aa22f33682ecaab9afa6d267336ea5bce00a904b3e957ad1ac13b97cdf35

_SRC_SHA256 by dollars
    3334.20B      300 rows  1c52aa22f33682ecaab9afa6d267336ea5bce00a904b3e957ad1ac13b97c

## who x when

RECIPIENT_NAME by START_DATE, dollars = AWARD_AMOUNT
  AMENTUM TECHNOLOGY, INC.                  2011:262.50M 2016:319.40M 2022:1.22B 2023:1.19B
  BELL BOEING JOINT PROJECT OFFICE          2007:11.04B 2011:7.34B 2016:6.60B
  DEPARTMENT OF SOCIAL SERVICES CALIFORNIA  2021:3.63B 2022:3.63B 2023:3.63B
  ELECTRIC BOAT CORPORATION                 2003:9.40B 2008:16.24B 2012:20.18B 2017:65.64B
  FLORIDA AGENCY FOR HEALTH CARE ADMINISTR  2022:22.29B 2023:20.33B
  GLAXOSMITHKLINE, LLC                      2013:218.53M 2020:517.04M 2021:879.07M 2022:864.28M 2023:856.89M 2024:835.59M
  HEALTH & HUMAN SVC COMMN TX               2022:36.91B 2023:28.43B
  HEALTH CARE SERVICES, CALIFORNIA DEPARTM  2017:48.77B 2018:52.69B 2020:61.42B 2021:80.53B 2022:156.65B 2023:96.99B
  HEALTH NET FEDERAL SERVICES, LLC          2010:19.41B 2016:23.49B
  HUMANA GOVERNMENT BUSINESS INC            2011:20.45B 2016:51.27B 2023:8.30B
  ILLINOIS DEPARTMENT OF HEALTHCARE & FAMI  2022:20.22B 2023:19.06B
  KBR WYLE SERVICES, LLC                    2014:1.01B 2015:1.56B 2020:190.29M 2023:415.79M
  LAWRENCE LIVERMORE NATIONAL SECURITY, LL  2007:41.09B
  LEIDOS, INC.                              2003:805.55M 2005:2.37B 2010:455.18M 2020:1.70B 2022:925.22M
  LOCKHEED MARTIN CORP                      1993:48.06B 2001:9.03B 2006:28.64B 2013:5.93B 2018:7.44B 2019:3.50B
  LOCKHEED MARTIN CORPORATION               2001:34.17B 2005:7.58B 2008:8.82B 2011:7.19B 2013:6.04B 2014:7.00B 2015:22.82B 2017:44.22B 2019:30.14B 2020:18.43B 2022:24.50B 2024:24.44B
  MERCK SHARP & DOHME LLC                   2018:1.52B 2019:1.67B 2020:1.20B 2021:1.89B 2022:2.17B 2023:2.44B 2024:2.61B
  NATIONAL TECHNOLOGY & ENGINEERING SOLUTI  2017:42.37B
  NORTHROP GRUMMAN SYSTEMS CORPORATION      1998:10.01B 2016:3.65B 2018:8.48B 2020:1.36B
  NYS DEPARTMENT OF HEALTH                  2017:39.44B 2022:58.90B 2023:54.31B 2024:30.10B
  OHIO DEPARTMENT OF MEDICAID               2022:23.44B 2023:23.87B
  PA DEPARTMENT OF HUMAN SERVICES           2020:21.99B 2022:27.82B 2023:26.10B
  PFIZER INC                                2020:11.91B 2021:1.21B 2022:1.14B 2023:811.33M 2024:1.13B
  SANOFI VACCINES US INC.                   2019:612.23M 2020:386.76M 2021:560.45M 2022:485.29M 2023:841.14M 2024:1.00B
  SCIENCE APPLICATIONS INTERNATIONAL CORPO  2012:213.94M 2016:520.19M 2019:242.18M 2020:918.41M
  SPACE EXPLORATION TECHNOLOGIES CORP.      2010:1.72B 2014:1.24B 2016:3.70B
  THE BOEING COMPANY                        1993:22.44B 2000:18.76B 2003:11.09B 2004:7.63B 2007:10.51B 2011:38.43B 2012:11.20B 2014:20.35B 2016:7.47B 2017:6.98B
  THE REGENTS OF THE UNIVERSITY OF CALIFOR  1999:18.01B 2005:19.74B
  UT-BATTELLE LLC                           1999:42.10B
  VA DEPARTMENT OF MEDICAL ASSISTANCE SERV  2019:6.34B 2020:8.80B 2022:14.07B 2023:13.94B

_SRC_SHA256 by START_DATE, dollars = AWARD_AMOUNT
  1c52aa22f33682ecaab9afa6d267336ea5bce00a  1978:80.70B 1984:20.65B 1993:70.50B 1998:10.01B 1999:60.11B 2000:46.99B 2001:43.21B 2003:34.41B 2004:34.31B 2005:57.12B 2006:60.08B 2007:71.32B 2008:100.25B 2009:26.92B 2010:24.07B 2011:74.83B 2012:59.99B 2013:55.92B 2014:36.00B 2015:64.91B 2016:117.67B 2017:322.38B 2018:158.63B 2019:46.17B 2020:201.74B 2021:94.60B 2022:696.01B 2023:584.35B 2024:80.38B

## where

PLACE_OF_PERFORMANCE_STATE: CA 25, TX 23, CT 12, NY 10, WA 9, NM 7, VA 7, TN 6, FL 5, AL 5, CO 5

## what

AWARDING_AGENCY_NAME: Department of Health and Human 39%, Department of Defense 23%, National Aeronautics and Space 15%, Department of Energy 12%, Department of Transportation 5%, Department of Homeland Securit 3%, Department of Education 1%, Environmental Protection Agenc 1%, Social Security Administration 0%, General Services Administratio 0%, Department of Agriculture 0%, Department of Justice 0%

AWARDING_AGENCY_CODE: 075 39%, 097 23%, 080 15%, 089 12%, 069 5%, 070 3%, 091 1%, 068 1%, 028 0%, 047 0%, 012 0%, 015 0%

FUNDING_AGENCY_NAME: Department of Health and Human 39%, Department of Defense 25%, National Aeronautics and Space 15%, Department of Energy 9%, Department of Transportation 5%, Department of Homeland Securit 3%, Department of Education 1%, Environmental Protection Agenc 1%, Social Security Administration 0%, General Services Administratio 0%, Department of Agriculture 0%, Department of Justice 0%

AWARD_TYPE: BLOCK GRANT (A) 86%, PROJECT GRANT (B) 10%, FORMULA GRANT (A) 2%, COOPERATIVE AGREEMENT (B) 2%

CFDA_NUMBER: 93.778 83%, 97.036 7%, 93.558 3%, 20.507 2%, 66.957 2%, 20.315 2%, 93.423 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AWARD_ID | other | 304 | 0 | 89303321DEM000065 2; HHSO100201200002I 2; HSCG8906D6WKAAA 2; EDFSA09D0013 2 |
| GENERATED_UNIQUE_AWARD_ID | empty | 1 | 300 |  |
| RECIPIENT_NAME | who | 152 | 0 | LOCKHEED MARTIN CORPORATI 17; THE BOEING COMPANY 12; HEALTH CARE SERVICES, CAL 9; LOCKHEED MARTIN CORP 8 |
| RECIPIENT_UEI | empty | 1 | 300 |  |
| RECIPIENT_DUNS | empty | 1 | 300 |  |
| RECIPIENT_EIN | empty | 1 | 300 |  |
| AWARDING_AGENCY_NAME | category | 13 | 0 | Department of Health and  116; Department of Defense 69; National Aeronautics and  45; Department of Energy 35 |
| AWARDING_AGENCY_CODE | category | 13 | 0 | 075 116; 097 69; 080 45; 089 35 |
| FUNDING_AGENCY_NAME | category | 13 | 0 | Department of Health and  117; Department of Defense 75; National Aeronautics and  45; Department of Energy 28 |
| AWARD_TYPE | category | 5 | 200 | BLOCK GRANT (A) 86; PROJECT GRANT (B) 10; FORMULA GRANT (A) 2; COOPERATIVE AGREEMENT (B) 2 |
| TOTAL_OBLIGATION | empty | 1 | 300 |  |
| TOTAL_OUTLAY | empty | 1 | 300 |  |
| AWARD_AMOUNT | amount | 300 | 0 | 151333151.76 2; 153365693.41 2; 153395819.42 2; 153396171.81 2 |
| START_DATE | date | 191 | 0 | 2023-10-01 39; 2022-10-01 37; 2024-04-01 7; 2020-04-01 5 |
| END_DATE | date | 91 | 100 | 2023-09-30 41; 2024-09-30 39; 2026-09-30 10; 2027-09-30 4 |
| LAST_MODIFIED_DATE | date | 232 | 0 | 2024-03-20 19:55:49 14; 2025-03-20 19:08:02 12; 2025-03-05 20:06:40 8; 2025-04-04 21:04:34 7 |
| FISCAL_YEAR | empty | 1 | 300 |  |
| NAICS_CODE | empty | 1 | 300 |  |
| NAICS_DESCRIPTION | empty | 1 | 300 |  |
| CFDA_NUMBER | category | 8 | 200 | 93.778 83; 97.036 7; 93.558 3; 20.507 2 |
| CFDA_TITLE | empty | 1 | 300 |  |
| PLACE_OF_PERFORMANCE_STATE | state | 41 | 105 | CA 25; TX 23; CT 12; NY 10 |
| PLACE_OF_PERFORMANCE_FIPS | empty | 1 | 300 |  |
| PLACE_OF_PERFORMANCE_CITY | empty | 1 | 300 |  |
| RECIPIENT_LOCATION_STATE | empty | 1 | 300 |  |
| RECIPIENT_LOCATION_FIPS | empty | 1 | 300 |  |
| FEDERAL_ACCOUNT_CODE | empty | 1 | 300 |  |
| TREASURY_ACCOUNT_SYMBOL | empty | 1 | 300 |  |
| DEF_CODE | empty | 1 | 300 |  |
| TRANSACTION_COUNT | empty | 1 | 300 |  |
| SUBAWARD_COUNT | empty | 1 | 300 |  |
| _INGESTED_AT | audit | 1 | 0 | 1782938244267895 300 |
| _SOURCE_RUN_ID | audit | 1 | 0 | fe6dd2fe-1781-4e47-83bc-1 300 |
| _SRC_SHA256 | who | 1 | 0 | 1c52aa22f33682ecaab9afa6d 300 |
