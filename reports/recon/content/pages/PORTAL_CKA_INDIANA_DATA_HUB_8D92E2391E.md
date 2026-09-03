# PORTAL_CKA_INDIANA_DATA_HUB_8D92E2391E

rows 18  columns 5  scan 1.9s

roles: audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026        18  ##############################

## who

SRC_SHA256 by rows
        18  04daaedbce3c131b64d17ab9edf42e764f619d9c1c86f9d241fc8061eda24a84

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  04daaedbce3c131b64d17ab9edf42e764f619d9c  2026:18

## what

COLUMN_NAME: Vendor Id 8%, Expenditure Category 8%, Legal Fund Name 8%, Legal Fund ID 8%, Journal Id 8%, Journal Date 8%, Funding Source 8%, Fund Name 8%, Fund ID 8%, Division of Government 8%, Fiscal Year 8%, Expenditure SubCategory 8%

DESCRIPTION: Vendor's identification number 8%, Classification of expenditure 8%, Legal Fund Description 8%, Legal Fund Code; 4 digits 8%, Agency code, 5 digit number 8%, Date the transaction posted to 8%, Funding source description 8%, Fund description 8%, Fund code, 5 digit number 8%, Description of government sect 8%, Fiscal year of transaction 8%, Description of the subcategory 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COLUMN_NAME | category | 18 | 0 | Vendor Id 1; Expenditure Category 1; Legal Fund Name 1; Legal Fund ID 1 |
| DESCRIPTION | category | 18 | 0 | Vendor's identification n 1; Classification of expendi 1; Legal Fund Description 1; Legal Fund Code; 4 digits 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:09:32.46045 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | 36d7466f-fc69-44e1-9ddd-3 18 |
| SRC_SHA256 | who | 1 | 0 | 04daaedbce3c131b64d17ab9e 18 |
