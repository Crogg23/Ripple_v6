# PORTAL_CKA_CALIFORNIA_OPEN_DCAEBA5312

rows 18  columns 7  scan 2.1s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        18  ##############################

## who

SRC_SHA256 by rows
        18  4f3282c21f1d8f004d7f5736d8d07509a9ce6bd338d77640181300b1e79bb8ca

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  4f3282c21f1d8f004d7f5736d8d07509a9ce6bd3  2026:18

## what

FIELD_TITLE: Supporting Documents 9%, General Comments  9%, Acquisition Price Comment  9%, Acquisition Price Non-Public I 9%, Acquisition Price   9%, Acquisition Date   9%, Priority Review Indicator   9%, Breakthrough Therapy Indicator 9%, Estimated Number of Patients 9%, Marketing/Pricing Plan Non-Pub 9%, Marketing/Pricing Plan Descrip 9%

FIELD_NAME: Supporting Documents 9%, General Comments  9%, Acquisition Price Comment  9%, Acquisition Price Nonpublic In 9%, Acquisition Price   9%, Acquisition Date   9%, Priority Review Indicator   9%, Breakthrough Therapy Indicator 9%, Estimated Number of Patients 9%, Marketing/Pricing Plan Nonpubl 9%, Marketing/Pricing Plan Descrip 9%

DATA_TYPE: Plain Text 47%, Number 41%, Date 12%

DESCRIPTION: A manufacturer may limit the i 17%, Links to supporting documents  8%, Any other comments by the manu 8%, Manufacturer comments, if repo 8%, If the drug was not developed  8%, If the drug was not developed  8%, Indicates whether the drug was 8%, Indicate whether the drug was  8%, The estimated number of patien 8%, A narrative description of the 8%, “Wholesale Acquisition Cost” ( 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_TITLE | category | 18 | 1 | Supporting Documents 1; General Comments  1; Acquisition Price Comment 1; Acquisition Price Non-Pub 1 |
| FIELD_NAME | category | 18 | 1 | Supporting Documents 1; General Comments  1; Acquisition Price Comment 1; Acquisition Price Nonpubl 1 |
| DATA_TYPE | category | 4 | 1 | Plain Text 8; Number 7; Date 2 |
| DESCRIPTION | category | 17 | 1 | A manufacturer may limit  2; Links to supporting docum 1; Any other comments by the 1; Manufacturer comments, if 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:09:19.56772 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | 49e4e559-4f63-41e5-a01d-2 18 |
| SRC_SHA256 | who | 1 | 0 | 4f3282c21f1d8f004d7f5736d 18 |
