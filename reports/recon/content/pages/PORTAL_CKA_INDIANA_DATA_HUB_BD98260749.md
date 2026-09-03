# PORTAL_CKA_INDIANA_DATA_HUB_BD98260749

rows 10  columns 6  scan 2.1s

roles: audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026        10  ##############################

## who

SRC_SHA256 by rows
        10  bf205985f8439cf9950239f056e20e96b8d27f07f0f882132f2624e3cb7c6d3c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  bf205985f8439cf9950239f056e20e96b8d27f07  2026:10

## what

COLUMN_NAME: RACE_ETHNICITY  10%, COUNTY  10%, FELONY_TYPE  10%, CONVICTION_MSO_CATEGORY  10%, SERVED_DAYS  10%, SENTENCED_DAYS  10%, RELEASE_AGE_GROUP  10%, RELEASE_YR  10%, INTAKE_AGE_GROUP  10%, INTAKE_YR  10%

DATA_TYPE: String 60%, Integer 40%

DEFINITION:  The offender's race as report 10%,  The Indiana county in which t 10%,  The conviction type for the m 10%,  The crime category of the Mos 10%,  The number of sentenced days  10%,  The number of days sentenced  10%,  The age group of the offender 10%,  The year of the date when the 10%,  The age group of the offender 10%,  The year of the original inta 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COLUMN_NAME | category | 10 | 0 | RACE_ETHNICITY  1; COUNTY  1; FELONY_TYPE  1; CONVICTION_MSO_CATEGORY  1 |
| DATA_TYPE | category | 2 | 0 | String 6; Integer 4 |
| DEFINITION | category | 10 | 0 |  The offender's race as r 1;  The Indiana county in wh 1;  The conviction type for  1;  The crime category of th 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:06:49.05934 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | bf1a95a1-543f-43f3-a4ac-1 10 |
| SRC_SHA256 | who | 1 | 0 | bf205985f8439cf9950239f05 10 |
