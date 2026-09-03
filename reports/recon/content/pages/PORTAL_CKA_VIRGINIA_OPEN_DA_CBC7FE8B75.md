# PORTAL_CKA_VIRGINIA_OPEN_DA_CBC7FE8B75

rows 10.0K  columns 9  scan 3.1s

roles: amount 1, audit 2, category 2, date 1, other 2, who 2

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| HRI_INCIDENT_COUNT_MEAN | 10.0K | 0 | 1.83 | 34 | 154 | 29.2K |

## who

INCIDENT_LOCALITY by rows
        75  Gloucester
        75  Lynchburg
        75  Highland
        75  Rockbridge
        75  King and Queen
        75  Powhatan
        75  Patrick
        75  Montgomery
        75  Bland
        75  Virginia Beach
        75  Mathews
        75  Alexandria
        75  Dickenson
        75  Madison
        75  Goochland
        75  Pittsylvania
        75  Norton
        75  Pulaski
        75  Emporia
        75  Washington

INCIDENT_LOCALITY by dollars
        2.0K       75 rows  Virginia Beach
        1.8K       75 rows  Fairfax
        1.3K       75 rows  Richmond City
        1.2K       75 rows  Henrico
        1.1K       74 rows  Chesapeake
      943.41       74 rows  Norfolk
      846.41       75 rows  Chesterfield
      836.07       75 rows  Prince William
      810.24       74 rows  Newport News
      729.26       74 rows  Roanoke City
      719.73       74 rows  Loudoun
      562.24       75 rows  Portsmouth
      514.73       74 rows  Hampton
      475.54       74 rows  Suffolk
      404.90       75 rows  Hanover
      389.39       75 rows  James City
      386.86       75 rows  Danville
      384.58       74 rows  Spotsylvania
      381.41       75 rows  Lynchburg
      380.22       74 rows  Albemarle

SRC_SHA256 by rows
     10.0K  21883b430e9836e957f8136f847aec0de3d93b46a7c69a45e9ae5f5aefd042ed

SRC_SHA256 by dollars
       29.2K    10.0K rows  21883b430e9836e957f8136f847aec0de3d93b46a7c69a45e9ae5f5aefd0

## who x when

INCIDENT_LOCALITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = HRI_INCIDENT_COUNT_MEAN
  Alexandria                                2026:332.05
  Bland                                     2026:5.49
  Chesapeake                                2026:1.1K
  Chesterfield                              2026:846.41
  Dickenson                                 2026:23.79
  Emporia                                   2026:59.09
  Fairfax                                   2026:1.8K
  Gloucester                                2026:145.39
  Goochland                                 2026:134.05
  Henrico                                   2026:1.2K
  Highland                                  2026:7.32
  King and Queen                            2026:27.45
  Loudoun                                   2026:719.73
  Lynchburg                                 2026:381.41
  Madison                                   2026:59.90
  Mathews                                   2026:32.94
  Montgomery                                2026:183.54
  Newport News                              2026:810.24
  Norfolk                                   2026:943.41
  Norton                                    2026:9.15
  Patrick                                   2026:54.90
  Pittsylvania                              2026:171.86
  Powhatan                                  2026:70.07
  Prince William                            2026:836.07
  Pulaski                                   2026:177.71
  Richmond City                             2026:1.3K
  Roanoke City                              2026:729.26
  Rockbridge                                2026:66.90
  Virginia Beach                            2026:2.0K
  Washington                                2026:107.37

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = HRI_INCIDENT_COUNT_MEAN
  21883b430e9836e957f8136f847aec0de3d93b46  2026:29.2K

## what

INCIDENT_YEAR: 2025 15%, 2022 14%, 2024 13%, 2021 13%, 2023 13%, 2019 13%, 2020 13%, 2026 5%

INCIDENT_MONTH: 5 11%, 4 11%, 3 11%, 1 10%, 7 9%, 12 9%, 10 9%, 8 9%, 6 9%, 9 9%, 2 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INCIDENT_YEAR | category | 8 | 0 | 2025 1.5K; 2022 1.4K; 2024 1.3K; 2021 1.3K |
| INCIDENT_MONTH | category | 11 | 0 | 5 1.1K; 4 1.1K; 3 1.1K; 1 994 |
| INCIDENT_FIPS | other | 135 | 0 | 51077 75; 51595 75; 51125 75; 51053 75 |
| INCIDENT_LOCALITY | who | 133 | 0 | Grayson 75; Emporia 75; Nelson 75; Dinwiddie 75 |
| HRI_INCIDENT_COUNT | other | 78 | 0 | 0 4.5K; * 3.8K; 5 298; 6 238 |
| HRI_INCIDENT_COUNT_MEAN | amount | 79 | 0 | 0 4.5K; 1.83175 3.8K; 5 298; 6 238 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:26:08.31656 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 399063b1-78f7-4fad-8cdb-d 10.0K |
| SRC_SHA256 | who | 1 | 0 | 21883b430e9836e957f8136f8 10.0K |
