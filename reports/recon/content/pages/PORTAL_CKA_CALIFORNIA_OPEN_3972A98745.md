# PORTAL_CKA_CALIFORNIA_OPEN_3972A98745

rows 25  columns 7  scan 2.6s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        25  ##############################

## who

SRC_SHA256 by rows
        25  9cb684126f749d98c30d4db6834f5da27e8660d22aecb4a9890caaf7e2abb355

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  9cb684126f749d98c30d4db6834f5da27e8660d2  2026:25

## what

FIELD_TITLE: General Comments 8%, Supporting Documents 8%, WAC at Introduction 8%, Year Drug Introduced to Market 8%, WAC Amount - Year Prior 8%, WAC at Acquisition 8%, Acquisition Price Comment 8%, Acquisition Price Non-Public I 8%, Acquisition Price 8%, Company Acquired From 8%, Acquisition Date 8%, Change/Improvement Description 8%

FIELD_NAME: General Comments 8%, Supporting Documents 8%, WAC at Intro to Market 8%, Year Drug Introduced to Market 8%, WAC Amount - Year Prior 8%, WAC at Acquisition 8%, Acquisition Price Comment 8%, Acquisition Price Non-Pub Ind 8%, Acquisition Price 8%, Company Acquired From 8%, Acquisition Date 8%, Chg/Imp Desc Non-Pub Ind 8%

DATA_TYPE: Plain Text 44%, Number 40%, Date 12%, Attachment 4%

DESCRIPTION: A manufacturer may limit the i 27%, Manufacturer appended comments 7%, A document submitted by the ma 7%, If the drug product was acquir 7%, If the drug product was acquir 7%, If the drug product was acquir 7%, If the drug product was acquir 7%, Manufacturer appended comments 7%, If the drug product was acquir 7%, If the drug product was acquir 7%, If the drug product was acquir 7%, A narrative description of the 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_TITLE | category | 25 | 0 | General Comments 1; Supporting Documents 1; WAC at Introduction 1; Year Drug Introduced to M 1 |
| FIELD_NAME | category | 25 | 0 | General Comments 1; Supporting Documents 1; WAC at Intro to Market 1; Year Drug Introduced to M 1 |
| DATA_TYPE | category | 4 | 0 | Plain Text 11; Number 10; Date 3; Attachment 1 |
| DESCRIPTION | category | 22 | 0 | A manufacturer may limit  4; Manufacturer appended com 1; A document submitted by t 1; If the drug product was a 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:10:04.86575 25 |
| SOURCE_RUN_ID | audit | 1 | 0 | 72585a8a-0106-4889-88ed-b 25 |
| SRC_SHA256 | who | 1 | 0 | 9cb684126f749d98c30d4db68 25 |
