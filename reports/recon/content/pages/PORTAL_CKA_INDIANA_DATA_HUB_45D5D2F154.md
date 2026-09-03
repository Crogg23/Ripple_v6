# PORTAL_CKA_INDIANA_DATA_HUB_45D5D2F154

rows 20  columns 7  scan 2.1s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        20  ##############################

## who

SRC_SHA256 by rows
        20  46393268e5e6991baf483e746fb69c0f19140671cacd131a80c881b7d35a9125

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  46393268e5e6991baf483e746fb69c0f19140671  2026:20

## what

FIELD_NAME: Vendor Name 8%, Vendor ID 8%, Source 8%, Legal Fund Name 8%, Legal Fund ID 8%, Last Updated 8%, Journal ID 8%, Journal Date 8%, Journal Agency ID 8%, Funding Source 8%, Fund Name 8%, Fund ID 8%

FIELD_TYPE: Varchar(10) 15%, Varchar(70) 15%, Varchar(5) 15%, Varchar(50) 10%, Varchar(40) 10%, Varchar(25) 5%, Varchar(20) 5%, TIMESTAMP 5%, Date 5%, Varchar(4) 5%, Varchar(41) 5%, Decimal(28,3) 5%

DESCRIPTION: Agency code, 5 digit number 15%, Name of vendor 8%, Vendor's identification number 8%, Data location 8%, Legal Fund Description 8%, Legal Fund Code; 4 digits 8%, Date of latest data extraction 8%, Reference number to ledger tra 8%, Date the transaction posted to 8%, Funding source description 8%, Fund description 8%, Fund code, 5 digit number 8%

NOTES: Reference to classification of 17%, Expenditures to state vendors  8%, Ex. PeopleSoft Financials, the 8%, Ex. General Fund, State Highwa 8%, Ex. 1000; References money set 8%, Refers to the agency reporting 8%, Ex. General Fund (G), Federal  8%, Ex. IND OFC OF TECHNOLOGY; Ref 8%, Ex. 71660; References operatin 8%, The State of Indiana functions 8%, The state operates on a fiscal 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_NAME | category | 20 | 0 | Vendor Name 1; Vendor ID 1; Source 1; Legal Fund Name 1 |
| FIELD_TYPE | category | 12 | 0 | Varchar(10) 3; Varchar(70) 3; Varchar(5) 3; Varchar(50) 2 |
| DESCRIPTION | category | 19 | 0 | Agency code, 5 digit numb 2; Name of vendor 1; Vendor's identification n 1; Data location 1 |
| NOTES | category | 15 | 5 | Reference to classificati 2; Expenditures to state ven 1; Ex. PeopleSoft Financials 1; Ex. General Fund, State H 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:09:44.20628 20 |
| SOURCE_RUN_ID | audit | 1 | 0 | e28747f5-d434-4527-9d08-3 20 |
| SRC_SHA256 | who | 1 | 0 | 46393268e5e6991baf483e746 20 |
