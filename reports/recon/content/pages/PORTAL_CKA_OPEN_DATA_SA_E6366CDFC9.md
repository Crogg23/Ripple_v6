# PORTAL_CKA_OPEN_DATA_SA_E6366CDFC9

rows 88  columns 12  scan 3.2s

roles: amount 3, audit 2, category 2, date 2, other 3, who 1

## when

CREATED_DATE
  2025        88  ##############################

INGESTED_AT
  2026        88  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SQMILES | 88 | 0.53 | 4.13 | 27.58 | 40.41 | 512.66 |
| SHAPE__AREA | 88 | 0 | 0 | 0.01 | 0.01 | 0.03 |
| SHAPE__LENGTH | 88 | 0.05 | 0.16 | 0.99 | 1 | 19.35 |

## who

SRC_SHA256 by rows
        88  ac0365d676048b2db4faaa31a782df766189b1a0c10e985751ecced00cde6219

SRC_SHA256 by dollars
      512.66       88 rows  ac0365d676048b2db4faaa31a782df766189b1a0c10e985751ecced00cde

## who x when

SRC_SHA256 by CREATED_DATE, dollars = SQMILES
  ac0365d676048b2db4faaa31a782df766189b1a0  2025:512.66

## what

SERVICE_AREA: South 20%, East 18%, Prue 17%, West 17%, North 14%, Downtown 8%, Central 6%

WEBSITE: http://www.sanantonio.gov/SAPD 99%, https://www.sanantonio.gov/SAP 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 88 | 0 | 88 1; 87 1; 86 1; 85 1 |
| SERVICE_AREA | category | 7 | 0 | South 18; East 16; Prue 15; West 15 |
| SAFFEZONE | other | 89 | 0 | P-11 1; P-13 1; W-09 1; E-15 1 |
| DISTRICTS | other | 86 | 0 | 7230 7240 2; 7150 7160 2; 7320 7360 1; 7330 1 |
| SQMILES | amount | 86 | 0 | 8.42276955 2; 4.36478551 2; 5.12769825 2; 10.74685518 1 |
| CREATED_DATE | date | 1 | 0 | 11/17/2025 8:24:32 PM 88 |
| WEBSITE | category | 3 | 1 | http://www.sanantonio.gov 86; https://www.sanantonio.go 1 |
| SHAPE__AREA | amount | 89 | 0 | 0.00259101201254452 1; 0.00104834577541624 1; 0.000577324497953668 1; 0.000770064700191142 1 |
| SHAPE__LENGTH | amount | 87 | 0 | 0.379154634040419 1; 0.161519672776177 1; 0.112162333712852 1; 0.171547626125657 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:30:24.75567 88 |
| SOURCE_RUN_ID | audit | 1 | 0 | ab7747b3-d40b-4775-b297-b 88 |
| SRC_SHA256 | who | 1 | 0 | ac0365d676048b2db4faaa31a 88 |
