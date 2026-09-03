# PORTAL_CKA_INDIANA_DATA_HUB_34B4DEE108

rows 13  columns 7  scan 2.2s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        13  ##############################

## who

SRC_SHA256 by rows
        13  adc36101075177d882d21e26e9e3c64b8e435606983cd2a6c6019186e16935a8

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  adc36101075177d882d21e26e9e3c64b8e435606  2026:13

## what

FIELD_NAME: Source 8%, Profile Description 8%, Last Updated 8%, Fund Name 8%, Fund ID 8%, Category Description 8%, Asset Type Description 8%, Asset ID 8%, Asset Description 8%, Agency Name 8%, Agency ID 8%, Acquisition Date 8%

FIELD_TYPE: Varchar(40) 46%, Varchar(5) 15%, Varchar(25) 8%, TIMESTAMP 8%, Varchar(12) 8%, Date 8%, Decimal(28,7) 8%

DESCRIPTION: Data location 8%, Classification of Asset 8%, Date of latest data extraction 8%, Fund description 8%, Fund code, 5 digit number 8%, Asset category description 8%, Type of the asset 8%, Asset identification number 8%, Description of asset 8%, Name of agency 8%, Agency code, 5 digit number 8%, Date the asset was acquired 8%

NOTES: Ex. PeopleSoft Financials, the 9%, Ex. Office Building, Education 9%, Ex. IND OFC OF TECHNOLOGY; Ref 9%, Ex. 71660; References operatin 9%, Ex. Computers & Accessories; C 9%, Broad category of the asset; T 9%, Asset ID is not unique overall 9%, Specific description of an ass 9%, References a state agency unde 9%, Ex. 00060; Business Unit repre 9%, Refers to the cost of an asset 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_NAME | category | 13 | 0 | Source 1; Profile Description 1; Last Updated 1; Fund Name 1 |
| FIELD_TYPE | category | 7 | 0 | Varchar(40) 6; Varchar(5) 2; Varchar(25) 1; TIMESTAMP 1 |
| DESCRIPTION | category | 13 | 0 | Data location 1; Classification of Asset 1; Date of latest data extra 1; Fund description 1 |
| NOTES | category | 12 | 2 | Ex. PeopleSoft Financials 1; Ex. Office Building, Educ 1; Ex. IND OFC OF TECHNOLOGY 1; Ex. 71660; References ope 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:26.70937 13 |
| SOURCE_RUN_ID | audit | 1 | 0 | 07efe2e2-c63a-4f8c-81b2-a 13 |
| SRC_SHA256 | who | 1 | 0 | adc36101075177d882d21e26e 13 |
