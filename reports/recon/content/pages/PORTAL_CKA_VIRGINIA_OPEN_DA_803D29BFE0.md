# PORTAL_CKA_VIRGINIA_OPEN_DA_803D29BFE0

rows 41  columns 11  scan 2.9s

roles: amount 1, audit 2, category 6, date 1, who 2

## when

INGESTED_AT
  2026        41  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SIR | 41 | 0 | 0.36 | 1.32 | 1.44 | 15.34 |

## who

HAI by rows
        41  C. difficile

HAI by dollars
       15.34       41 rows  C. difficile

SRC_SHA256 by rows
        41  016645c2801be626f9d2db8c15f6eb88bffb7d33f0f5e51dbdb7ae6f49fdc1ab

SRC_SHA256 by dollars
       15.34       41 rows  016645c2801be626f9d2db8c15f6eb88bffb7d33f0f5e51dbdb7ae6f49fd

## who x when

HAI by INGESTED_AT  LOAD STAMP, not an event date, dollars = SIR
  C. difficile                              2026:15.34

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SIR
  016645c2801be626f9d2db8c15f6eb88bffb7d33  2026:15.34

## what

YEAR: 2024 17%, 2022 17%, 2021 17%, 2020 17%, 2019 17%, 2023 15%

HOSPITAL_NAME: Select Specialty Hospital - Ri 15%, Lake Taylor Transitional Care  15%, Hospital for Extended Recovery 15%, Hampton Roads Speciality Hospi 15%, Centra Speciality Care Hospita 15%, All Virginia LTACHs 15%, Univerisity of Virginia Transi 10%, Inova Specialty Hospital 2%

PATIENT_DAYS: 14539 8%, 21703 8%, 1687 8%, 5208 8%, 7977 8%, 6835 8%, 64226 8%, 10283 8%, 22289 8%, 5761 8%, 7497 8%, 7642 8%

NUMBER_OF_OBSERVED_EVENTS: 0 23%, 1 17%, 2 14%, 4 11%, 3 9%, 18 6%, 15 6%, 10 3%, 24 3%, 19 3%, 25 3%, 14 3%

NUMBER_OF_PREDICTED_EVENTS: 16.110 8%, 21.300 8%, 1.770 8%, 3.930 8%, 7.510 8%, 6.090 8%, 63.280 8%, 11.850 8%, 24.480 8%, 5.380 8%, 7.850 8%, 4.990 8%

SIR_INTERPRETATION: Better 68%, Same 29%, Worse 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 6 | 0 | 2024 7; 2022 7; 2021 7; 2020 7 |
| HAI | who | 1 | 0 | C. difficile 41 |
| HOSPITAL_NAME | category | 8 | 0 | Select Specialty Hospital 6; Lake Taylor Transitional  6; Hospital for Extended Rec 6; Hampton Roads Speciality  6 |
| PATIENT_DAYS | category | 41 | 0 | 14539 1; 21703 1; 1687 1; 5208 1 |
| NUMBER_OF_OBSERVED_EVENTS | category | 18 | 0 | 0 8; 1 6; 2 5; 4 4 |
| NUMBER_OF_PREDICTED_EVENTS | category | 41 | 0 | 16.110 1; 21.300 1; 1.770 1; 3.930 1 |
| SIR | amount | 32 | 0 | 0.000 8; 0.470 2; 0.360 2; 0.250 1 |
| SIR_INTERPRETATION | category | 3 | 0 | Better 28; Same 12; Worse 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:11:34.98121 41 |
| SOURCE_RUN_ID | audit | 1 | 0 | a91b8638-f1ce-4ee3-9d4e-2 41 |
| SRC_SHA256 | who | 1 | 0 | 016645c2801be626f9d2db8c1 41 |
