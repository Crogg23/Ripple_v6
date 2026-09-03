# PORTAL_CKA_VIRGINIA_OPEN_DA_154B43ED61

rows 18  columns 12  scan 3.3s

roles: amount 1, audit 2, category 7, date 1, who 2

## when

INGESTED_AT
  2026        18  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SIR | 18 | 0.21 | 0.67 | 1.48 | 1.50 | 12.46 |

## who

HOPSITAL_NAME by rows
        18  All Virginia LTACHs

HOPSITAL_NAME by dollars
       12.46       18 rows  All Virginia LTACHs

SRC_SHA256 by rows
        18  d96463eadc63fdf8865f9b26ac479ac1d283f1382bcce538c39afb156df39b03

SRC_SHA256 by dollars
       12.46       18 rows  d96463eadc63fdf8865f9b26ac479ac1d283f1382bcce538c39afb156df3

## who x when

HOPSITAL_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SIR
  All Virginia LTACHs                       2026:12.46

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SIR
  d96463eadc63fdf8865f9b26ac479ac1d283f138  2026:12.46

## what

YEAR: 2019 17%, 2020 17%, 2021 17%, 2022 17%, 2023 17%, 2024 17%

HAI: CLABSI 33%, CAUTI 33%, C. difficile 33%

DEVICE_OR_PATIENT_DAYS: Patient Days 67%, Device Days 33%

DEVICE_OR_PATIENT_DAYS_COUNTS: 27123 8%, 27636 8%, 20701 8%, 16614 8%, 13173 8%, 14867 8%, 19794 8%, 21502 8%, 20028 8%, 18661 8%, 13895 8%, 16096 8%

NUMBER_OF_OBSERVED_EVENTS: 25 19%, 21 12%, 32 12%, 27 6%, 14 6%, 29 6%, 30 6%, 13 6%, 11 6%, 42 6%, 31 6%, 18 6%

NUMBER_OF_PREDICTED_EVENTS: 33.730 8%, 32.570 8%, 24.560 8%, 18.330 8%, 16.970 8%, 19.340 8%, 37.960 8%, 43.560 8%, 39.940 8%, 32.730 8%, 27.380 8%, 30.490 8%

SIR_INTERPREATION: Better 53%, Same 35%, Worse 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 6 | 0 | 2019 3; 2020 3; 2021 3; 2022 3 |
| HAI | category | 3 | 0 | CLABSI 6; CAUTI 6; C. difficile 6 |
| HOPSITAL_NAME | who | 1 | 0 | All Virginia LTACHs 18 |
| DEVICE_OR_PATIENT_DAYS | category | 2 | 0 | Patient Days 12; Device Days 6 |
| DEVICE_OR_PATIENT_DAYS_COUNTS | category | 18 | 0 | 27123 1; 27636 1; 20701 1; 16614 1 |
| NUMBER_OF_OBSERVED_EVENTS | category | 14 | 0 | 25 3; 21 2; 32 2; 27 1 |
| NUMBER_OF_PREDICTED_EVENTS | category | 18 | 0 | 33.730 1; 32.570 1; 24.560 1; 18.330 1 |
| SIR | amount | 16 | 0 | 0.830 2; 0.400 2; 0.620 1; 1.020 1 |
| SIR_INTERPREATION | category | 4 | 1 | Better 9; Same 6; Worse 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:09:25.54082 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | b6b4a6ee-07e4-4ac8-91b9-1 18 |
| SRC_SHA256 | who | 1 | 0 | d96463eadc63fdf8865f9b26a 18 |
