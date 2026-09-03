# PORTAL_CKA_VIRGINIA_OPEN_DA_6207BDEB36

rows 10.0K  columns 8  scan 3.2s

roles: audit 2, category 3, date 3, who 1

## when

REPORT_DATE
  2024     10.0K  ##############################

DATE_VDH_NOTIFIED
  2020      1.9K  ##################
  2021      2.9K  ############################
  2022      3.2K  ##############################
  2023      1.6K  ###############
  2024       443  ####

INGESTED_AT
  2026     10.0K  ##############################

## who

SRC_SHA256 by rows
     10.0K  3688581adf17014707f8faf3ecd393ccfd051d84f46193738a3ec30e639e106d

## who x when

SRC_SHA256 by REPORT_DATE
  3688581adf17014707f8faf3ecd393ccfd051d84  2024:10.0K

## what

HEALTH_REGION_NAME: Central 27%, Northern 23%, Eastern 18%, Northwest 16%, Southwest 15%

FACILITY_TYPE_GROUP: Long Term Care Facilities 33%, Congregate Setting 22%, K-12 18%, Child Care 11%, Healthcare Setting 6%, Correctional Facility 6%, College/University 3%, Gym 0%

NUMBER_OF_OUTBREAKS: 1 68%, 2 20%, 3 7%, 4 3%, 5 1%, 6 1%, 7 0%, 9 0%, 10 0%, 8 0%, 14 0%, 12 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 6 | 0 | 2024-09-03 3.0K; 2024-08-06 2.7K; 2024-07-16 1.6K; 2024-08-27 1.2K |
| DATE_VDH_NOTIFIED | date | 1.2K | 0 | 2021-12-28 66; 2022-01-14 61; 2021-08-30 61; 2022-01-13 60 |
| HEALTH_REGION_NAME | category | 5 | 0 | Central 2.7K; Northern 2.3K; Eastern 1.8K; Northwest 1.6K |
| FACILITY_TYPE_GROUP | category | 8 | 0 | Long Term Care Facilities 3.3K; Congregate Setting 2.2K; K-12 1.8K; Child Care 1.1K |
| NUMBER_OF_OUTBREAKS | category | 16 | 0 | 1 6.8K; 2 2.0K; 3 650; 4 311 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:59:08.45173 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | d41ea241-0326-499a-949b-7 10.0K |
| SRC_SHA256 | who | 1 | 0 | 3688581adf17014707f8faf3e 10.0K |
