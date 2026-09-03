# PORTAL_CKA_TAMPA_OPEN_DATA_3DAE51799D

rows 266  columns 13  scan 4.3s

roles: amount 1, audit 2, category 5, date 2, who 4

## when

DATE
  2026       266  ##############################

INGESTED_AT
  2026       266  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 266 | 0 | 41 | 81.72 | 86 | 11.7K |

## who

C_ORGANIZATION by rows
       266  Neighborhood Enhancement

C_ORGANIZATION by dollars
       11.7K      266 rows  Neighborhood Enhancement

PERIOD by rows
         5  2024/Q2
         5  2026/Q2
         5  2024/Q3
         5  2025/Q4
         5  2025/Q3
         5  2024/Q4
         5  2026/Q1
         5  2025/Q1
         5  2025/Q2
         5  2024/Q1
         4  2024/10-Oct
         4  2024/09-Sep
         4  2024/04-Apr
         4  2025/10-Oct
         4  2023/Q1
         4  2023/Q3
         4  2025/11-Nov
         4  2025/05-May
         4  2025/09-Sep
         4  2025/01-Jan

PERIOD by dollars
      248.52        5 rows  2024/Q1
      238.02        5 rows  2024/Q2
      233.12        5 rows  2024/Q3
      231.07        5 rows  2025/Q1
      228.28        5 rows  2025/Q2
      225.99        5 rows  2024/Q4
      221.17        5 rows  2025/Q3
      220.55        5 rows  2025/Q4
      214.58        4 rows  2024/10-Oct
      208.20        5 rows  2026/Q1
      187.74        5 rows  2026/Q2
      185.54        4 rows  2024/12-Dec
      178.53        4 rows  2024/09-Sep
      177.17        4 rows  2024/01-Jan
      172.76        4 rows  2024/11-Nov
      171.85        4 rows  2023/Q3
      169.17        4 rows  2024/04-Apr
      167.57        4 rows  2023/Q4
      166.38        4 rows  2023/Q1
      164.89        4 rows  2024/02-Feb

TYPEDATA by rows
       266  Period

TYPEDATA by dollars
       11.7K      266 rows  Period

SRC_SHA256 by rows
       266  9d9e248f8474697210501e32aabf22ba727660714fbe1eb7afabc82410edd717

SRC_SHA256 by dollars
       11.7K      266 rows  9d9e248f8474697210501e32aabf22ba727660714fbe1eb7afabc82410ed

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Neighborhood Enhancement                  2026:11.7K

PERIOD by DATE, dollars = VALUE
  2023/Q1                                   2026:166.38
  2023/Q3                                   2026:171.85
  2023/Q4                                   2026:167.57
  2024/01-Jan                               2026:177.17
  2024/02-Feb                               2026:164.89
  2024/04-Apr                               2026:169.17
  2024/09-Sep                               2026:178.53
  2024/10-Oct                               2026:214.58
  2024/11-Nov                               2026:172.76
  2024/12-Dec                               2026:185.54
  2024/Q1                                   2026:248.52
  2024/Q2                                   2026:238.02
  2024/Q3                                   2026:233.12
  2024/Q4                                   2026:225.99
  2025/01-Jan                               2026:154.09
  2025/05-May                               2026:152.50
  2025/09-Sep                               2026:145.08
  2025/10-Oct                               2026:142.62
  2025/11-Nov                               2026:151.83
  2025/Q1                                   2026:231.07
  2025/Q2                                   2026:228.28
  2025/Q3                                   2026:221.17
  2025/Q4                                   2026:220.55
  2026/Q1                                   2026:208.20
  2026/Q2                                   2026:187.74

## what

ID: 9 9%, 6 9%, 3 9%, 10 8%, 8 8%, 7 8%, 5 8%, 4 8%, 2 8%, 1 8%, 12 8%, 14 7%

CHARTNAME: Percent of Proactive Cases 16%, Complaint Response 16%, Average Days of Final Course o 16%, Avg Number of Days Cases are O 16%, Percentage of Voluntary Compli 11%, Percent of Proactive Cases by  5%, Average Days of Final Course o 5%, Avg Number of Days Cases are O 5%, Complaint Response by Quarter 5%, Percentage of Voluntary Compli 4%

DESCRIPTION: Percent of Proactive Cases 16%, Complaint Response 16%, Average Days of Final Course o 16%, Avg Number of Days Cases are O 16%, Percentage of Voluntary Compli 11%, Percent of Proactive Cases by  5%, Average Days of Final Course o 5%, Avg Number of Days Cases are O 5%, Complaint Response by Quarter 5%, Percentage of Voluntary Compli 4%

CATEGORY: Days 42%, Cases 36%, Complaints 21%

SUMMARY: Average 64%, Percent 36%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | category | 43 | 0 | 9 10; 6 10; 3 10; 10 9 |
| C_ORGANIZATION | who | 1 | 0 | Neighborhood Enhancement 266 |
| CHARTNAME | category | 10 | 0 | Percent of Proactive Case 43; Complaint Response 43; Average Days of Final Cou 42; Avg Number of Days Cases  42 |
| DESCRIPTION | category | 10 | 0 | Percent of Proactive Case 43; Complaint Response 43; Average Days of Final Cou 42; Avg Number of Days Cases  42 |
| CATEGORY | category | 3 | 0 | Days 112; Cases 97; Complaints 57 |
| SUMMARY | category | 2 | 0 | Average 169; Percent 97 |
| TYPEDATA | who | 1 | 0 | Period 266 |
| DATE | date | 1 | 0 | 07/02/2026 12:30:40 266 |
| PERIOD | who | 102 | 0 | 2026/Q2 5; 2026/Q1 5; 2025/Q4 5; 2025/Q3 5 |
| VALUE | amount | 151 | 0 | 3.00 17; 2.00 16; 29.00 9; 31.00 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:17:58.61549 266 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1d664dcd-fb55-4f98-82c7-c 266 |
| SRC_SHA256 | who | 1 | 0 | 9d9e248f8474697210501e32a 266 |
