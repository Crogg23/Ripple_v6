# PORTAL_CKA_CALIFORNIA_OPEN_F8F7B5716B

rows 808  columns 12  scan 3.3s

roles: audit 2, category 3, date 5, who 3

## when

FY_START_DATE
  2023       404  ##############################
  2024       404  ##############################

FY_END_DATE
  2024       404  ##############################
  2025       404  ##############################

DATE_SUBMITTED_INITIAL
  2024       306  ########################
  2025       381  ##############################
  2026        51  ####

DATE_RESUBMITTED
  2024         1  
  2025        98  ##############################
  2026        25  ########

INGESTED_AT
  2026       808  ##############################

## who

SUPPLIER_NAME by rows
         2  California Water Service Company Bakersfield
         2  Apple Valley Ranchos Water Company
         2  Brentwood  City Of
         2  California Water Service Company Marysville
         2  California Water Service Company Los Altos/Suburban
         2  California Water Service Company Salinas District
         2  Chowchilla  City of
         2  Compton  City Of
         2  Coachella  City Of
         2  East Valley Water District
         2  California Water Service Company Livermore
         2  El Monte  City Of
         2  Coachella Valley Water District
         2  Calaveras County Water District
         2  Arcadia  City Of
         2  American Canyon  City Of
         2  Fortuna  City Of
         2  California American Water Company - Sacramento District
         2  Benicia  City Of
         2  Bakman Water Company

ORG_ID by rows
         2  748
         2  467
         2  607
         2  424
         2  759
         2  739
         2  1004
         2  1054
         2  1030
         2  1059
         2  1388
         2  1109
         2  1052
         2  711
         2  124
         2  82
         2  1167
         2  851
         2  2979
         2  351

SRC_SHA256 by rows
       808  08ab22f11562b2764e37c04e608ca7b4966f48c7ac38786df03c8590d47f6e10

## who x when

SUPPLIER_NAME by FY_START_DATE
  American Canyon  City Of                  2023:1 2024:1
  Apple Valley Ranchos Water Company        2023:1 2024:1
  Arcadia  City Of                          2023:1 2024:1
  Bakman Water Company                      2023:1 2024:1
  Benicia  City Of                          2023:1 2024:1
  Brentwood  City Of                        2023:1 2024:1
  Calaveras County Water District           2023:1 2024:1
  California American Water Company - Sacr  2023:1 2024:1
  California Water Service Company Bakersf  2023:1 2024:1
  California Water Service Company Livermo  2023:1 2024:1
  California Water Service Company Los Alt  2023:1 2024:1
  California Water Service Company Marysvi  2023:1 2024:1
  California Water Service Company Salinas  2023:1 2024:1
  Chowchilla  City of                       2023:1 2024:1
  Coachella  City Of                        2023:1 2024:1
  Coachella Valley Water District           2023:1 2024:1
  Compton  City Of                          2023:1 2024:1
  East Valley Water District                2023:1 2024:1
  El Monte  City Of                         2023:1 2024:1
  Fortuna  City Of                          2023:1 2024:1

ORG_ID by FY_START_DATE
  1004                                      2023:1 2024:1
  1030                                      2023:1 2024:1
  1052                                      2023:1 2024:1
  1054                                      2023:1 2024:1
  1059                                      2023:1 2024:1
  1109                                      2023:1 2024:1
  1167                                      2023:1 2024:1
  124                                       2023:1 2024:1
  1388                                      2023:1 2024:1
  2979                                      2023:1 2024:1
  351                                       2023:1 2024:1
  424                                       2023:1 2024:1
  467                                       2023:1 2024:1
  607                                       2023:1 2024:1
  711                                       2023:1 2024:1
  739                                       2023:1 2024:1
  748                                       2023:1 2024:1
  759                                       2023:1 2024:1
  82                                        2023:1 2024:1
  851                                       2023:1 2024:1

## what

LATE_SUBMISSION: Yes 99%, No (extension granted) 1%

SUBMITTED_INVALID_FILE: Yes 100%

NO_SUBMISSION: Yes 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ORG_ID | who | 405 | 0 | 2793 6; 2790 6; 2789 6; 2782 6 |
| SUPPLIER_NAME | who | 400 | 0 | Yucaipa Valley Water Dist 6; Yuba City 6; Yreka  City Of 6; Yorba Linda Water Distric 6 |
| FY_START_DATE | date | 2 | 0 | 2024-07-01 404; 2023-07-01 404 |
| FY_END_DATE | date | 2 | 0 | 2025-06-30 404; 2024-06-30 404 |
| DATE_SUBMITTED_INITIAL | date | 122 | 70 | 12/20/2024 49; 12/23/2025 47; 12/23/2024 45; 12/22/2025 42 |
| DATE_RESUBMITTED | date | 42 | 684 | 05/07/2025 43; 05/05/2025 12; 05/06/2025 7; 04/23/2025 5 |
| LATE_SUBMISSION | category | 3 | 704 | Yes 103; No (extension granted) 1 |
| SUBMITTED_INVALID_FILE | category | 2 | 803 | Yes 5 |
| NO_SUBMISSION | category | 2 | 738 | Yes 70 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:22:52.39121 808 |
| SOURCE_RUN_ID | audit | 1 | 0 | 02a3907f-d693-42b6-8f75-0 808 |
| SRC_SHA256 | who | 1 | 0 | 08ab22f11562b2764e37c04e6 808 |
