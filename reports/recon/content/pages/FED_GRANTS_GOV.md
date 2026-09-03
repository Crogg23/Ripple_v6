# FED_GRANTS_GOV

rows 100  columns 26  scan 3.0s

roles: audit 2, category 1, date 2, empty 16, other 3, who 2

## when

POSTED_DATE
  2026       100  ##############################

CLOSE_DATE
  2026        88  ##############################
  2027         2  #

## who

CFDA_NUMBERS by rows
        10  ['93.310']
         9  ['97.045']
         7  ['93.532']
         6  ['93.490']
         5  ['93.048']
         4  ['93.113']
         4  ['45.201']
         4  ['93.847']
         2  ['17.502']
         2  ['93.761']
         2  ['19.022']
         2  ['19.705']
         2  ['16.601']
         2  ['20.909']
         2  ['19.703']
         1  ['10.574']
         1  ['93.647']
         1  ['93.00J']
         1  ['97.043']
         1  ['93.325']

_SRC_SHA256 by rows
       100  39a5be2b0a735ce1941041a79228a0afd4e3e4acc410efe5e440511fd34aebf4

## who x when

CFDA_NUMBERS by POSTED_DATE
  ['10.574']                                2026:1
  ['16.601']                                2026:2
  ['17.502']                                2026:2
  ['19.022']                                2026:2
  ['19.703']                                2026:2
  ['19.705']                                2026:2
  ['20.909']                                2026:2
  ['45.201']                                2026:4
  ['93.00J']                                2026:1
  ['93.048']                                2026:5
  ['93.113']                                2026:4
  ['93.310']                                2026:10
  ['93.325']                                2026:1
  ['93.490']                                2026:6
  ['93.532']                                2026:7
  ['93.647']                                2026:1
  ['93.761']                                2026:2
  ['93.847']                                2026:4
  ['97.043']                                2026:1
  ['97.045']                                2026:9

_SRC_SHA256 by POSTED_DATE
  39a5be2b0a735ce1941041a79228a0afd4e3e4ac  2026:100

## what

AGENCY_CODE: HHS-NIH11 28%, DHS-DHS 19%, HHS-SAMHS-SAMHSA 15%, HHS-ACL 12%, NEA 5%, DOS-INL 5%, DOS-ACN 3%, DOI-BIA 3%, HHS-HRSA 3%, DOT-FHWA 3%, USDOJ-BOP-NIC 3%, DOT-RITA 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OPPORTUNITY_ID | other | 98 | 0 | 362963 1; 362965 1; 362968 1; 362834 1 |
| OPPORTUNITY_NUMBER | other | 100 | 0 | DFOP0018149 1; RFA-OD-27-009 1; BIA-TTGP-2026-OIED 1; HRSA-26-038 1 |
| OPPORTUNITY_TITLE | other | 98 | 0 | Export Controls and Inves 1; NIH Research Evaluation a 1; Tribal Tourism Grant Prog 1; Rural Communities Opioid  1 |
| AGENCY_CODE | category | 31 | 0 | HHS-NIH11 22; DHS-DHS 15; HHS-SAMHS-SAMHSA 12; HHS-ACL 9 |
| AGENCY_NAME | empty | 1 | 100 |  |
| OPPORTUNITY_STATUS | empty | 1 | 100 |  |
| OPPORTUNITY_CATEGORY | empty | 1 | 100 |  |
| FUNDING_INSTRUMENT_TYPE | empty | 1 | 100 |  |
| CATEGORY_OF_FUNDING_ACTIVITY | empty | 1 | 100 |  |
| CFDA_NUMBERS | who | 51 | 0 | ['93.310'] 10; ['97.045'] 9; ['93.532'] 7; ['93.490'] 6 |
| ELIGIBLE_APPLICANTS | empty | 1 | 100 |  |
| AWARD_CEILING | empty | 1 | 100 |  |
| AWARD_FLOOR | empty | 1 | 100 |  |
| ESTIMATED_TOTAL_PROGRAM_FUNDING | empty | 1 | 100 |  |
| EXPECTED_NUMBER_OF_AWARDS | empty | 1 | 100 |  |
| POSTED_DATE | date | 5 | 0 | 07/01/2026 36; 06/30/2026 29; 06/26/2026 19; 06/29/2026 10 |
| CLOSE_DATE | date | 39 | 10 | 07/27/2026 23; 08/17/2026 11; 07/31/2026 10; 07/29/2026 3 |
| LAST_UPDATED_DATE | empty | 1 | 100 |  |
| ARCHIVE_DATE | empty | 1 | 100 |  |
| SYNOPSIS_DESC | empty | 1 | 100 |  |
| GRANTOR_CONTACT_EMAIL | empty | 1 | 100 |  |
| GRANTOR_CONTACT_NAME | empty | 1 | 100 |  |
| VERSION | empty | 1 | 100 |  |
| _INGESTED_AT | audit | 1 | 0 | 1782954706092155 100 |
| _SOURCE_RUN_ID | audit | 1 | 0 | e1931d9d-71ef-4d01-821b-2 100 |
| _SRC_SHA256 | who | 1 | 0 | 39a5be2b0a735ce1941041a79 100 |
