# PORTAL_CKA_OPEN_DATA_SA_581DE3800B

rows 12  columns 9  scan 3.0s

roles: amount 2, audit 2, category 3, date 2, who 1

## when

CREATED_DATE
  2024        12  ##############################

INGESTED_AT
  2026        12  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SQUAREMILES | 12 | 0.18 | 0.23 | 0.35 | 0.35 | 3.05 |
| SHAPE__LENGTH | 12 | 0.03 | 0.04 | 0.04 | 0.04 | 0.43 |

## who

SRC_SHA256 by rows
        12  a9bd4d5eb79b754a93d6f7ebb06061eb254a01a3ffa59b12115373504d4fdaad

SRC_SHA256 by dollars
        3.05       12 rows  a9bd4d5eb79b754a93d6f7ebb06061eb254a01a3ffa59b12115373504d4f

## who x when

SRC_SHA256 by CREATED_DATE, dollars = SQUAREMILES
  a9bd4d5eb79b754a93d6f7ebb06061eb254a01a3  2024:3.05

## what

OBJECTID: 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%, 1 8%

DISTRICT: 10 8%, 12 8%, 11 8%, 8 8%, 4 8%, 2 8%, 3 8%, 5 8%, 9 8%, 6 8%, 7 8%, 1 8%

SHAPE__AREA: 7.87949277309963E-05 8%, 7.13468079993618E-05 8%, 8.29544585485564E-05 8%, 6.40750781712995E-05 8%, 4.67284444312099E-05 8%, 8.04333183168637E-05 8%, 4.40009177964384E-05 8%, 4.8926672889138E-05 8%, 4.26823564794176E-05 8%, 4.60333124010504E-05 8%, 4.63121323264204E-05 8%, 8.4780702536591E-05 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 12 | 0 | 12 1; 11 1; 10 1; 9 1 |
| DISTRICT | category | 12 | 0 | 10 1; 12 1; 11 1; 8 1 |
| SQUAREMILES | amount | 12 | 0 | 0.32712434 1; 0.29619981 1; 0.34441884 1; 0.26604896 1 |
| CREATED_DATE | date | 1 | 0 | 1/23/2024 11:57:22 PM 12 |
| SHAPE__AREA | category | 12 | 0 | 7.87949277309963E-05 1; 7.13468079993618E-05 1; 8.29544585485564E-05 1; 6.40750781712995E-05 1 |
| SHAPE__LENGTH | amount | 12 | 0 | 0.0411017764752606 1; 0.0331641995344996 1; 0.0380066621755859 1; 0.0356521581626248 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:13:56.43438 12 |
| SOURCE_RUN_ID | audit | 1 | 0 | 63343fba-f28a-469a-9ff0-d 12 |
| SRC_SHA256 | who | 1 | 0 | a9bd4d5eb79b754a93d6f7ebb 12 |
