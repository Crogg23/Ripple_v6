# FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS

rows 1.6K  columns 11  scan 3.0s

roles: audit 2, date 2, id 3, other 3, state 1, who 2

## when

MEDICARE_ID_EFFECTIVE_DATE
  2014         5  
  2019         1  
  2020      1.1K  ##############################
  2021       109  ###
  2022        63  ##
  2023        72  ##
  2024        67  ##
  2025        82  ##
  2026        40  #

_INGESTED_AT
  2026      1.6K  ##############################

## who

PROVIDER_NAME by rows
        47  BRIGHTVIEW LLC
        35  AEGIS TREATMENT CENTERS LLC
        19  COMMUNITY MEDICAL SERVICES MONTANA
        18  HABIT OPCO, LLC
        17  METRO TREATMENT OF FLORIDA, LP
        15  ADDICTION RESEARCH AND TREATMENT IN
        14  COMMUNITY MEDICAL SERVICES ARIZONA-
        13  METRO TREATMENT OF FLORIDA LP
        12  SPECTRUM HEALTH SYSTEMS, INC
        11  WESTERN PACIFIC MED-CORP
        11  FAMILY GUIDANCE CENTERS INC
        11  ATS OF NORTH CAROLINA, LLC
        11  BAART BEHAVIORAL HEALTH SERVICES IN
        10  DENVER RECOVERY GROUP LLC
        10  COMMUNITY HEALTH CARE INC
        10  COMMUNITY MEDICAL SERVICES ARIZONA
        10  HARTFORD DISPENSARY
         9  METRO TREATMENT OF NORTH CAROLINA L
         8  QUALITY ADDICTION MANAGEMENT INC
         8  CFSATC INC

CITY by rows
        30  BALTIMORE
        21  CHICAGO
        21  NEW YORK
        15  BROOKLYN
        13  BRONX
        12  PHOENIX
        11  TUCSON
        11  COLUMBUS
        10  CINCINNATI
         9  SPRINGFIELD
         8  RICHMOND
         8  PHILADELPHIA
         8  DETROIT
         8  WILMINGTON
         7  ALBUQUERQUE
         7  DENVER
         7  SAN ANTONIO
         6  PITTSBURGH
         6  NEW HAVEN
         6  HOUSTON

## who x when

PROVIDER_NAME by MEDICARE_ID_EFFECTIVE_DATE
  ADDICTION RESEARCH AND TREATMENT IN       2020:15
  AEGIS TREATMENT CENTERS LLC               2020:35
  ATS OF NORTH CAROLINA, LLC                2020:11
  BAART BEHAVIORAL HEALTH SERVICES IN       2014:4 2020:5 2021:2
  BRIGHTVIEW LLC                            2020:31 2021:2 2023:14
  CFSATC INC                                2020:8
  COMMUNITY HEALTH CARE INC                 2020:10
  COMMUNITY MEDICAL SERVICES ARIZONA        2020:10
  COMMUNITY MEDICAL SERVICES ARIZONA-       2020:14
  COMMUNITY MEDICAL SERVICES MONTANA        2020:9 2024:10
  DENVER RECOVERY GROUP LLC                 2020:10
  FAMILY GUIDANCE CENTERS INC               2020:11
  HABIT OPCO, LLC                           2020:18
  HARTFORD DISPENSARY                       2020:10
  METRO TREATMENT OF FLORIDA LP             2020:13
  METRO TREATMENT OF FLORIDA, LP            2020:17
  METRO TREATMENT OF NORTH CAROLINA L       2020:9
  QUALITY ADDICTION MANAGEMENT INC          2020:8
  SPECTRUM HEALTH SYSTEMS, INC              2020:11 2021:1
  WESTERN PACIFIC MED-CORP                  2020:11

CITY by MEDICARE_ID_EFFECTIVE_DATE
  ALBUQUERQUE                               2020:5 2021:1 2026:1
  BALTIMORE                                 2020:10 2021:3 2022:7 2024:3 2025:3 2026:4
  BRONX                                     2020:7 2021:5 2024:1
  BROOKLYN                                  2019:1 2020:8 2021:5 2024:1
  CHICAGO                                   2020:9 2021:2 2023:1 2024:1 2025:5 2026:3
  CINCINNATI                                2020:9 2024:1
  COLUMBUS                                  2020:9 2021:2
  DENVER                                    2020:4 2024:1 2025:1 2026:1
  DETROIT                                   2020:6 2025:1 2026:1
  HOUSTON                                   2020:3 2022:1 2023:1 2024:1
  NEW HAVEN                                 2020:5 2021:1
  NEW YORK                                  2020:14 2021:3 2023:1 2024:1 2026:2
  PHILADELPHIA                              2020:5 2021:1 2022:1 2023:1
  PHOENIX                                   2020:10 2023:1 2024:1
  PITTSBURGH                                2020:5 2021:1
  RICHMOND                                  2020:6 2023:1 2025:1
  SAN ANTONIO                               2020:4 2025:2 2026:1
  SPRINGFIELD                               2020:6 2022:1 2024:1 2025:1
  TUCSON                                    2020:11
  WILMINGTON                                2020:7 2025:1

## where

STATE: CA 140, OH 104, NY 95, NC 88, MD 78, FL 69, TX 68, PA 66, IL 63, GA 55, MA 52, VA 47

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | other | 1.3K | 0 | 1659769446 53; 1487608485 17; 1912980251 16; 1023175072 14 |
| PROVIDER_NAME | who | 890 | 0 | BRIGHTVIEW LLC 49; AEGIS TREATMENT CENTERS L 35; COMMUNITY MEDICAL SERVICE 19; HABIT OPCO, LLC 18 |
| ADDRESS_LINE_1 | id | 1.5K | 0 | 15 GREEN HILLS DR 9; 475 UNION ST 9; 5121 CRESTWAY RD 8; 1301 PIERCE ST 8 |
| ADDRESS_LINE_2 | other | 341 | 1.0K | STE A 23; STE C 20; STE 101 17; STE 100 14 |
| CITY | who | 930 | 0 | BALTIMORE 30; NEW YORK 21; CHICAGO 21; BROOKLYN 15 |
| STATE | state | 50 | 0 | CA 140; OH 104; NY 95; NC 88 |
| ZIP | id | 1.5K | 0 | 24482-2674 9; 05855-5499 9; 78239-1975 8; 94115-4005 8 |
| MEDICARE_ID_EFFECTIVE_DATE | date | 361 | 0 | 01/01/2020 858; 04/01/2020 48; 03/17/2023 15; 03/01/2020 13 |
| PHONE | other | 1.4K | 0 | 8335104357 61; 8008056989 20; 8662912393 14; 6148824343 10 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-26 12:06:27.208 1.6K |
| _SOURCE_RUN_ID | audit id | 1.6K | 0 | 4e2315f7-77d5-4a01-9c86-4 8; a97b5f0c-b6ec-4441-b1f4-c 8; 724a7ac5-a878-4366-b14d-c 8; 456b06ef-9b62-439b-bfd6-9 8 |
