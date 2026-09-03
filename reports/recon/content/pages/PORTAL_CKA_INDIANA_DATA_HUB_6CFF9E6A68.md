# PORTAL_CKA_INDIANA_DATA_HUB_6CFF9E6A68

rows 12  columns 5  scan 2.0s

roles: audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026        12  ##############################

## who

SRC_SHA256 by rows
        12  5c894071a72d589dad2fb7c09bef8f2e96bd97dc86405832dc66edb741e80f16

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  5c894071a72d589dad2fb7c09bef8f2e96bd97dc  2026:12

## what

FIELD_NAME: IN_ZIP_TOTAL_COUNT 8%, ETHNICITY 8%, RACE 8%, GENDER 8%, ZIP 8%, COUNTY_CLEAN 8%, STATE_CLEAN 8%, ANSWER 8%, QUESTION_TEXT 8%, LICENSE_STATUS_NAME 8%, LICENSE_TYPE_NAME 8%, PROFESSION_NAME 8%

DESCRIPTION: total number of zip codes in I 8%, Veterinarian ethnicity 8%, Veterinarian Race 8%, Veterinarian Gender 8%, Primary practice zip 8%, Primary practice county 8%, Primary practice state 8%, Survey Answer 8%, Survey Question  8%, Veterinary License status 8%, Veterinary License type 8%, Profession Name 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_NAME | category | 12 | 0 | IN_ZIP_TOTAL_COUNT 1; ETHNICITY 1; RACE 1; GENDER 1 |
| DESCRIPTION | category | 12 | 0 | total number of zip codes 1; Veterinarian ethnicity 1; Veterinarian Race 1; Veterinarian Gender 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:21.69827 12 |
| SOURCE_RUN_ID | audit | 1 | 0 | 495ab6fa-58f7-45fd-8e37-a 12 |
| SRC_SHA256 | who | 1 | 0 | 5c894071a72d589dad2fb7c09 12 |
