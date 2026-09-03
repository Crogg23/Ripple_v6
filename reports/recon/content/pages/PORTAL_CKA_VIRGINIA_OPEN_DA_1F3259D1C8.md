# PORTAL_CKA_VIRGINIA_OPEN_DA_1F3259D1C8

rows 82  columns 12  scan 3.1s

roles: amount 1, audit 2, category 6, date 1, other 2, who 1

## when

INGESTED_AT
  2026        82  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SIR | 76 | 0 | 0.69 | 4.28 | 6.30 | 65.83 |

## who

SRC_SHA256 by rows
        82  43ac0b33014add4ba0c7150786cba034a835619f8c3e8919e1efc6e9df1c9e61

SRC_SHA256 by dollars
       65.83       82 rows  43ac0b33014add4ba0c7150786cba034a835619f8c3e8919e1efc6e9df1c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SIR
  43ac0b33014add4ba0c7150786cba034a835619f  2026:65.83

## what

YEAR: 2024 17%, 2022 17%, 2021 17%, 2020 17%, 2019 17%, 2023 15%

HAI: CLABSI 50%, CAUTI 50%

HOSPITAL_NAME: All Virginia LTACHs 15%, Select Specialty Hospital - Ri 15%, Lake Taylor Transitional Care  15%, Hospital for Extended Recovery 15%, Hampton Roads Speciality Hospi 15%, Centra Speciality Care Hospita 15%, Univerisity of Virginia Transi 10%, Inova Specialty Hospital 2%

DAY_TYPE: Device Days 50%, Patient Days 50%

NUMBER_OF_OBSERVED_EVENTS: 0 28%, 4 13%, 2 12%, 3 12%, 7 7%, 9 4%, 1 4%, 6 4%, 8 4%, 5 4%, 25 3%, 13 3%

SIR_INTERPREATION: Same 51%, Better 28%, Worse 13%, No Conclusion 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 6 | 0 | 2024 14; 2022 14; 2021 14; 2020 14 |
| HAI | category | 2 | 0 | CLABSI 41; CAUTI 41 |
| HOSPITAL_NAME | category | 8 | 0 | All Virginia LTACHs 12; Select Specialty Hospital 12; Lake Taylor Transitional  12; Hospital for Extended Rec 12 |
| DAY_TYPE | category | 2 | 0 | Device Days 41; Patient Days 41 |
| DAY_COUNT | other | 81 | 0 | 14867 1; 3812 1; 3974 1; 1723 1 |
| NUMBER_OF_OBSERVED_EVENTS | category | 23 | 0 | 0 19; 4 9; 2 8; 3 8 |
| NUMBER_OF_PREDICTED_EVENTS | other | 75 | 0 | 1.110 3; 2.090 2; 0.900 2; 2.660 2 |
| SIR | amount | 54 | 0 | 0 17; N/A 6; 0.83 3; 0.69 2 |
| SIR_INTERPREATION | category | 4 | 0 | Same 42; Better 23; Worse 11; No Conclusion 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:14:25.58640 82 |
| SOURCE_RUN_ID | audit | 1 | 0 | e8093268-42e8-491d-988e-b 82 |
| SRC_SHA256 | who | 1 | 0 | 43ac0b33014add4ba0c715078 82 |
