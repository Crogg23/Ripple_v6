# FED_DOJ_FCA_SETTLEMENTS

rows 19  columns 18  scan 2.6s

roles: amount 1, audit 2, category 7, empty 6, other 1, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SETTLEMENT_AMOUNT | 4 | 6.80 | 25 | 197.14 | 202 | 258.80 |

## who

_SRC_SHA256 by rows
        19  d4e82205547609a75506ea636c3ee5080f1a67333227b1c262aa29c862a70fab

_SRC_SHA256 by dollars
      258.80       19 rows  d4e82205547609a75506ea636c3ee5080f1a67333227b1c262aa29c862a7

## what

CASE_TITLE: Error fetching mailto:?body=ht 9%, LinkedIn Login, Sign in | Link 9%, Error fetching http://twitter. 9%, Error fetching http://www.face 9%, Contact the Fraud Section 9%, Report Fraud Against the Feder 9%, Fraud Section Press Releases 9%, The False Claims Act 9%, Fraud Section Practice Areas 9%, Fraud Section 9%, Commercial Litigation Branch 9%

SETTLEMENT_DATE: September 30, 2025 17%, May 23, 2025 8%, March 13, 2025 8%, June 10, 2026 8%, January 15, 2025 8%, January 16, 2026 8%, March 21, 2023 8%, September 26, 2024 8%, June 16, 2026 8%, June 11, 2025 8%, September 29, 2025 8%

FISCAL_YEAR: 2025 58%, 2026 25%, 2023 8%, 2024 8%

QUI_TAM: No 81%, Yes 19%

FRAUD_TYPE: Healthcare 50%, Grant Fraud 21%, Defense Contracting 14%, Financial 14%

AGENCY_DEFRAUDED: VA 47%, Defense 20%, Medicare 13%, HHS 7%, Department of Defense 7%, Medicaid 7%

PRESS_RELEASE_URL: https://www.justice.gov/opa/pr 8%, mailto:?body=https://www.justi 8%, http://www.linkedin.com/shareA 8%, http://twitter.com/intent/twee 8%, http://www.facebook.com/sharer 8%, https://www.justice.gov/civil/ 8%, https://www.justice.gov/civil/ 8%, https://www.justice.gov/civil/ 8%, https://www.justice.gov/civil/ 8%, https://www.justice.gov/civil/ 8%, https://www.justice.gov/civil/ 8%, https://www.justice.gov/civil/ 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CASE_TITLE | category | 19 | 1 | Error fetching mailto:?bo 1; LinkedIn Login, Sign in / 1; Error fetching http://twi 1; Error fetching http://www 1 |
| DEFENDANT_COMPANY | empty | 1 | 19 |  |
| DEFENDANT_PERSON | empty | 1 | 19 |  |
| SETTLEMENT_DATE | category | 12 | 7 | September 30, 2025 2; May 23, 2025 1; March 13, 2025 1; June 10, 2026 1 |
| FISCAL_YEAR | category | 5 | 7 | 2025 7; 2026 3; 2023 1; 2024 1 |
| SETTLEMENT_AMOUNT | amount | 6 | 14 | $40 1; $2.9 billion 1; $202 1; $6.8 1 |
| QUI_TAM | category | 3 | 3 | No 13; Yes 3 |
| RELATOR_NAME | empty | 1 | 19 |  |
| RELATOR_SHARE | empty | 1 | 19 |  |
| FRAUD_TYPE | category | 5 | 5 | Healthcare 7; Grant Fraud 3; Defense Contracting 2; Financial 2 |
| AGENCY_DEFRAUDED | category | 7 | 4 | VA 7; Defense 3; Medicare 2; HHS 1 |
| CASE_NUMBER | empty | 1 | 19 |  |
| DISTRICT | empty | 1 | 19 |  |
| PRESS_RELEASE_URL | category | 19 | 0 | https://www.justice.gov/o 1; mailto:?body=https://www. 1; http://www.linkedin.com/s 1; http://twitter.com/intent 1 |
| SOURCE_URL | other | 1 | 0 | https://www.justice.gov/c 19 |
| _INGESTED_AT | audit | 1 | 0 | 1781716821393581 19 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 32e52764-91c7-417f-a40f-a 19 |
| _SRC_SHA256 | who | 1 | 0 | d4e82205547609a75506ea636 19 |
