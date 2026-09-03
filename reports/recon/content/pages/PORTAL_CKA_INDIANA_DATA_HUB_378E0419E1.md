# PORTAL_CKA_INDIANA_DATA_HUB_378E0419E1

rows 10  columns 6  scan 1.9s

roles: audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026        10  ##############################

## who

SRC_SHA256 by rows
        10  0ba70b917ffcef6283c72fb24f66f37d0b23ced486060b5d0504908de3a96d46

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  0ba70b917ffcef6283c72fb24f66f37d0b23ced4  2026:10

## what

COLUMN_NAME: MAX_SNAPSHOT_DT  10%, SOURCE  10%, RACE_ETHNICITY  10%, COUNTY  10%, FELONY_TYPE  10%, CONVICTION_MSO_CATEGORY  10%, SENTENCED_DAYS  10%, INTAKE_AGE_GROUP  10%, INTAKE_YR  10%, SNAPSHOT_DT  10%

DATA_TYPE: String 60%, Date 20%, Integer 20%

DEFINITION:  The maximum snapshot date for 10%,  DOC data source 10%,  The offender's race as report 10%,  The Indiana county in which t 10%,  The conviction type for the m 10%,  The crime category of the Mos 10%,  The number of days sentenced  10%,  The age group of the offender 10%,  The year of the original inta 10%,  The date on which the data wa 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COLUMN_NAME | category | 10 | 0 | MAX_SNAPSHOT_DT  1; SOURCE  1; RACE_ETHNICITY  1; COUNTY  1 |
| DATA_TYPE | category | 3 | 0 | String 6; Date 2; Integer 2 |
| DEFINITION | category | 10 | 0 |  The maximum snapshot dat 1;  DOC data source 1;  The offender's race as r 1;  The Indiana county in wh 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:06:43.18754 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | fff10a01-4d69-4e94-9810-6 10 |
| SRC_SHA256 | who | 1 | 0 | 0ba70b917ffcef6283c72fb24 10 |
