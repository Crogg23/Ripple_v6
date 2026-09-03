# PORTAL_SOC_WASHINGTON_STATE_1A95FB1665

rows 112  columns 10  scan 4.2s

roles: audit 2, category 3, date 3, other 1, who 2

## when

AUDIT_RECEIVED_OR_CONDUCTED
  2022        32  ###########################
  2023        36  ##############################
  2024        23  ###################
  2025        21  ##################

AUDIT_CLOSED_DATE
  2022        17  ###########
  2023        45  ##############################
  2024        26  #################
  2025        24  ################

INGESTED_AT
  2026       112  ##############################

## who

RECIPIENT_NAME by rows
         3  Washington State University, Transportation Services
         3  Western Washington University
         3  Seattle Municipal Court
         3  Seattle DOT/IT
         3  LexisNexis Risk Solutions, Inc.
         3  RL Polk
         3  Embark Safety LLC
         3  Novoaglobal, Inc.
         3  Data Ticket, Inc.
         3  Department of Social and Health Services
         3  City of Vancouver
         3  Office of Superintendent of Public Instruction
         3  Department of Veterans Affairs
         3  Employment Security Department
         2  Insurance Information Exchange, LLC
         2  Bellingham Municipal Court
         2  Administrative Office of the Courts
         2  Office of Financial Management
         2  Parks & Recreation
         2  Selective Service

SRC_SHA256 by rows
       112  e4cf4b22bd70d71573b8175ec91508a9ca254f4d9d4649b141a1943056808304

## who x when

RECIPIENT_NAME by AUDIT_CLOSED_DATE
  Administrative Office of the Courts       2023:1 2024:1
  Bellingham Municipal Court                2023:1 2025:1
  City of Vancouver                         2023:2 2025:1
  Data Ticket, Inc.                         2022:1 2024:1 2025:1
  Department of Social and Health Services  2023:2 2024:1
  Department of Veterans Affairs            2022:1 2023:1 2025:1
  Embark Safety LLC                         2022:1 2025:2
  Employment Security Department            2023:2 2025:1
  Insurance Information Exchange, LLC       2024:2
  LexisNexis Risk Solutions, Inc.           2022:1 2024:1 2025:1
  Novoaglobal, Inc.                         2022:1 2024:1 2025:1
  Office of Financial Management            2022:1 2024:1
  Office of Superintendent of Public Instr  2022:1 2023:1 2025:1
  Parks & Recreation                        2023:1 2025:1
  RL Polk                                   2023:2 2025:1
  Seattle DOT/IT                            2023:2 2025:1
  Seattle Municipal Court                   2022:1 2025:2
  Selective Service                         2023:1 2025:1
  Washington State University, Transportat  2022:2 2025:1
  Western Washington University             2022:1 2024:1 2025:1

SRC_SHA256 by AUDIT_CLOSED_DATE
  e4cf4b22bd70d71573b8175ec91508a9ca254f4d  2022:17 2023:45 2024:26 2025:24

## what

RECIPIENT_TYPE: Public 55%, Private 45%

AUDIT_TYPE: Data Security 54%, Permissible Use 41%, Security Review 4%

UBI_EIN: nan 47%, 3650 7%, 604292732 6%, 3600 6%, 3800 4%, 603084803 4%, 409001390 4%, 4650 4%, 3500 4%, 604184086 4%, 600231290 4%, 5400 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AUDIT_CONTROL_NUMBER | other | 112 | 0 | 25-006_PUA 1; 24-001_DSA 1; 25-017_DSA 1; 24-012_DSA 1 |
| RECIPIENT_NAME | who | 69 | 0 | Western Washington Univer 3; Washington State Universi 3; Seattle Municipal Court 3; Seattle DOT/IT 3 |
| RECIPIENT_TYPE | category | 2 | 0 | Public 62; Private 50 |
| AUDIT_TYPE | category | 3 | 0 | Data Security 61; Permissible Use 46; Security Review 5 |
| AUDIT_RECEIVED_OR_CONDUCTED | date | 106 | 0 | 2025-01-21T00:00:00.000 2; 2023-02-17T00:00:00.000 2; 2023-06-20T00:00:00.000 2; 2022-09-19T00:00:00.000 2 |
| AUDIT_CLOSED_DATE | date | 94 | 0 | 2023-02-03T00:00:00.000 3; 2023-02-24T00:00:00.000 3; 2025-03-11T00:00:00.000 2; 2025-09-25T00:00:00.000 2 |
| UBI_EIN | category | 37 | 0 | nan 33; 3650 5; 604292732 4; 3600 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:41:34.59106 112 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0fd6f91d-bd15-49c2-9969-e 112 |
| SRC_SHA256 | who | 1 | 0 | e4cf4b22bd70d71573b8175ec 112 |
