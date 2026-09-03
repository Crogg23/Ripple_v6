# PORTAL_CKA_OPEN_DATA_SA_AD9A53047C

rows 8  columns 9  scan 3.2s

roles: amount 3, audit 2, category 2, date 2, who 1

## when

CREATED_DATE
  2025         8  ##############################

INGESTED_AT
  2026         8  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SQMILES | 8 | 26.33 | 71.14 | 86.56 | 86.92 | 520.22 |
| SHAPE__AREA | 8 | 0.01 | 0.02 | 0.02 | 0.02 | 0.13 |
| SHAPE__LENGTH | 8 | 0.68 | 1.58 | 2.84 | 2.91 | 12.63 |

## who

SRC_SHA256 by rows
         8  496980259f9e44f79f4f6e0ea607d690c36898692548d8bed1ed4dbff733f49b

SRC_SHA256 by dollars
      520.22        8 rows  496980259f9e44f79f4f6e0ea607d690c36898692548d8bed1ed4dbff733

## who x when

SRC_SHA256 by CREATED_DATE, dollars = SQMILES
  496980259f9e44f79f4f6e0ea607d690c3689869  2025:520.22

## what

OBJECTID: 8 12%, 7 12%, 6 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

BATTALION: 8 12%, 7 12%, 6 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 8 | 0 | 8 1; 7 1; 6 1; 5 1 |
| BATTALION | category | 8 | 0 | 8 1; 7 1; 6 1; 5 1 |
| SQMILES | amount | 8 | 0 | 79.91342489 1; 67.70522882 1; 55.1141778 1; 74.57400924 1 |
| CREATED_DATE | date | 1 | 0 | 11/13/2025 4:35:04 PM 8 |
| SHAPE__AREA | amount | 8 | 0 | 0.0192504880765227 1; 0.0163197440554086 1; 0.0132672257645936 1; 0.0179906426556045 1 |
| SHAPE__LENGTH | amount | 8 | 0 | 2.90894899032906 1; 1.96307129046336 1; 0.974094999526326 1; 1.70091124124655 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:11:36.58466 8 |
| SOURCE_RUN_ID | audit | 1 | 0 | b80628bb-5e24-4dfc-aced-7 8 |
| SRC_SHA256 | who | 1 | 0 | 496980259f9e44f79f4f6e0ea 8 |
