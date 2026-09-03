# PORTAL_CKA_VIRGINIA_OPEN_DA_E3C86F8B93

rows 123  columns 12  scan 2.4s

roles: amount 1, audit 2, category 6, date 1, other 2, who 1

## when

INGESTED_AT
  2026       123  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SIR | 117 | 0 | 0.54 | 3.45 | 6.30 | 81.17 |

## who

SRC_SHA256 by rows
       123  83a4fa70208090fc4d84533f6d4f274e296e12426224a1b4279b1010a18d43e7

SRC_SHA256 by dollars
       81.17      123 rows  83a4fa70208090fc4d84533f6d4f274e296e12426224a1b4279b1010a18d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SIR
  83a4fa70208090fc4d84533f6d4f274e296e1242  2026:81.17

## what

YEAR: 2024 17%, 2022 17%, 2021 17%, 2020 17%, 2019 17%, 2023 15%

HAI: C. difficile 33%, CLABSI 33%, CAUTI 33%

HOSPITAL_NAME: All Virginia LTACHs 15%, Select Specialty Hospital - Ri 15%, Lake Taylor Transitional Care  15%, Hospital for Extended Recovery 15%, Hampton Roads Speciality Hospi 15%, Centra Speciality Care Hospita 15%, Univerisity of Virginia Transi 10%, Inova Specialty Hospital 2%

DAY_TYPE: Patient Days 67%, Device Days 33%

NUMBER_OF_OBSERVED_EVENTS: 0 27%, 4 13%, 2 13%, 3 11%, 1 9%, 7 6%, 15 4%, 6 4%, 8 3%, 5 3%, 9 3%, 25 3%

SIR_INTERPRETATION: Same 44%, Better 41%, Worse 10%, No Conclusion 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 6 | 0 | 2024 21; 2022 21; 2021 21; 2020 21 |
| HAI | category | 3 | 0 | C. difficile 41; CLABSI 41; CAUTI 41 |
| HOSPITAL_NAME | category | 8 | 0 | All Virginia LTACHs 18; Select Specialty Hospital 18; Lake Taylor Transitional  18; Hospital for Extended Rec 18 |
| DAY_TYPE | category | 2 | 0 | Patient Days 82; Device Days 41 |
| DAY_COUNT | other | 121 | 0 | 64226 1; 14539 1; 21703 1; 1687 1 |
| NUMBER_OF_OBSERVED_EVENTS | category | 29 | 0 | 0 27; 4 13; 2 13; 3 11 |
| NUMBER_OF_PREDICTED_EVENTS | other | 113 | 0 | 1.110 3; 2.090 2; 0.900 2; 15.390 2 |
| SIR | amount | 78 | 0 | 0 25; N/A 6; 0.4 3; 0.83 3 |
| SIR_INTERPRETATION | category | 4 | 0 | Same 54; Better 51; Worse 12; No Conclusion 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:15:49.18228 123 |
| SOURCE_RUN_ID | audit | 1 | 0 | d1aadbe3-df02-46f9-84b6-7 123 |
| SRC_SHA256 | who | 1 | 0 | 83a4fa70208090fc4d84533f6 123 |
