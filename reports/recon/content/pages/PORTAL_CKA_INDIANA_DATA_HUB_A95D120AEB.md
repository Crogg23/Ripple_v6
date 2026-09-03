# PORTAL_CKA_INDIANA_DATA_HUB_A95D120AEB

rows 9  columns 6  scan 2.0s

roles: audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026         9  ##############################

## who

SRC_SHA256 by rows
         9  ee07933005c1fbadac543b965e21805c60cca628feee7b4f468f3f37e0e8b1eb

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  ee07933005c1fbadac543b965e21805c60cca628  2026:9

## what

COLUMN_NAME: RACE_ETHNICITY  11%, COUNTY  11%, LIFE_WITHOUT_PAROLE_FLG  11%, FELONY_TYPE  11%, CONVICTION_MSO_CATEGORY  11%, SERVED_DAYS  11%, SENTENCED_DAYS  11%, INTAKE_AGE_GROUP  11%, INTAKE_YR  11%

DATA_TYPE: String 56%, Integer 44%

DEFINITION:  The offender's race as report 11%,  The Indiana county in which t 11%,  A flag indicating a "life sen 11%,  The conviction type for the m 11%,  The crime category of the Mos 11%,  The number of sentenced days  11%,  The number of days sentenced  11%,  The age group of the offender 11%,  The year of the original inta 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COLUMN_NAME | category | 9 | 0 | RACE_ETHNICITY  1; COUNTY  1; LIFE_WITHOUT_PAROLE_FLG  1; FELONY_TYPE  1 |
| DATA_TYPE | category | 2 | 0 | String 5; Integer 4 |
| DEFINITION | category | 9 | 0 |  The offender's race as r 1;  The Indiana county in wh 1;  A flag indicating a "lif 1;  The conviction type for  1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:06:30.81407 9 |
| SOURCE_RUN_ID | audit | 1 | 0 | 59708361-f22c-4cc6-ba57-b 9 |
| SRC_SHA256 | who | 1 | 0 | ee07933005c1fbadac543b965 9 |
