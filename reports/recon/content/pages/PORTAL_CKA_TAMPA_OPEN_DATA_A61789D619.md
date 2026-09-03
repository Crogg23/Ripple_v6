# PORTAL_CKA_TAMPA_OPEN_DATA_A61789D619

rows 106  columns 13  scan 3.3s

roles: amount 1, audit 2, category 4, date 2, other 2, who 3

## when

DATE
  2023        24  #########################
  2024        24  #########################
  2025        29  ##############################
  2026        29  ##############################

INGESTED_AT
  2026       106  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 106 | 5 | 42 | 274.2K | 276.3K | 2.02M |

## who

C_ORGANIZATION by rows
       106  Police Department

C_ORGANIZATION by dollars
       2.02M      106 rows  Police Department

TYPEDATA by rows
       106  Period

TYPEDATA by dollars
       2.02M      106 rows  Period

SRC_SHA256 by rows
       106  819291c93c891e91e11b340d26ff08aee33aaf848b11d0bed3abe9f1e1e3a68d

SRC_SHA256 by dollars
       2.02M      106 rows  819291c93c891e91e11b340d26ff08aee33aaf848b11d0bed3abe9f1e1e3

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Police Department                         2023:477.7K 2024:511.4K 2025:523.6K 2026:508.5K

TYPEDATA by DATE, dollars = VALUE
  Period                                    2023:477.7K 2024:511.4K 2025:523.6K 2026:508.5K

## what

CHARTNAME: High Crash Intersections 66%, Big Five Crimes 19%, Calls for Service 8%, Juvenile Arrests 4%, Index Crime 4%

DESCRIPTION: High Crash Intersections 66%, Big Five Crimes 19%, Calls for Service 8%, Juvenile Arrests 4%, Tampa's Crime Rate 4%

CATEGORY: HILLSBOROUGH AV E / NEBRASKA A 8%, HILLSBOROUGH AV E / FLORIDA AV 8%, HILLSBOROUGH AV E / 40TH ST N 8%, HILLSBOROUGH AV E / 30TH ST N 8%, GANDY BL W / DALEMABRY HW S 8%, DALEMABRY HW N / KENNEDY BL W 8%, DALEMABRY / COLUMBUS DR W 8%, 7701 W COURTNEY CAMPBELL CSWY 8%, BUSCH BL E / NEBRASKA AV N 8%, ARMENIA AV N / HILLSBOROUGH AV 8%, 50TH ST N / COLUMBUS DR E 8%, 50TH ST N / BUSCH BL E 8%

PERIOD: 2025 27%, 2024 27%, 2023 23%, 2022 23%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 107 | 0 | 20625 1; 20624 1; 20623 1; 20622 1 |
| C_ORGANIZATION | who | 1 | 0 | Police Department 106 |
| CHARTNAME | category | 5 | 0 | High Crash Intersections 70; Big Five Crimes 20; Calls for Service 8; Juvenile Arrests 4 |
| DESCRIPTION | category | 5 | 0 | High Crash Intersections 70; Big Five Crimes 20; Calls for Service 8; Juvenile Arrests 4 |
| CATEGORY | category | 29 | 0 | HILLSBOROUGH AV E / NEBRA 4; HILLSBOROUGH AV E / FLORI 4; HILLSBOROUGH AV E / 40TH  4; HILLSBOROUGH AV E / 30TH  4 |
| SUMMARY | other | 1 | 0 | Total 106 |
| TYPEDATA | who | 1 | 0 | Period 106 |
| DATE | date | 87 | 0 | 02/03/2023 00:00:00 5; 05/07/2026 11:25:00 2; 05/07/2026 11:17:00 2; 05/07/2026 11:15:00 2 |
| PERIOD | category | 4 | 0 | 2025 29; 2024 29; 2023 24; 2022 24 |
| VALUE | amount | 79 | 0 | 34.000 5; 27.000 4; 29.000 4; 32.000 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:15:23.46054 106 |
| SOURCE_RUN_ID | audit | 1 | 0 | d200dc42-7494-45ec-8ccc-5 106 |
| SRC_SHA256 | who | 1 | 0 | 819291c93c891e91e11b340d2 106 |
