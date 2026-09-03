# PORTAL_CKA_INDIANA_DATA_HUB_71C6F53126

rows 18  columns 7  scan 2.3s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        18  ##############################

## who

SRC_SHA256 by rows
        18  a9116c3cb474e1a51423767d74e20d44633c8ff5e0ab184b05dbff0245fbcc5f

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  a9116c3cb474e1a51423767d74e20d44633c8ff5  2026:18

## what

FIELD_NAME: Fiscal Year 8%, CF_ATTRIB_VALUE_DESCR 8%, CF_ATTRIB_VALUE 8%, CF_ATTRIBUTE 8%, Vendor Name 8%, Legal Fund Name 8%, Legal Fund ID 8%, Fund Name 8%, Fund ID 8%, Account Name 8%, Account ID 8%, Amount 8%

FIELD_TYPE: VARCHAR(20) 12%, VARCHAR(5) 12%, VARCHAR(40) 12%, DATE 12%, DECIMAL(28,0) 6%, VARCHAR(60) 6%, VARCHAR(15) 6%, Varchar(40) 6%, VARCHAR(70) 6%, VARCHAR(30) 6%, VARCHAR(10) 6%, Decimal(26,3) 6%

DESCRIPTION: Fiscal Year of Transaction 8%, Chartfield attribute descripti 8%, Chartfield attribute value 8%, Chartfield attribute number 8%, Supplier name 8%, Legal Fund description 8%, Legal Fund code; 4 digits 8%, Fund description 8%, Fund code, 5 digit number 8%, Account description 8%, Account code; 6 digits 8%, Distribution amount 8%

NOTES: References classification of e 17%, The state operates on a fiscal 8%, Ex: Motor Vehicle Highway; Ref 8%, Ex: MOTOR_VEHICLE_HWY; Referen 8%, Ex. LOCAL_GOV_DISTR; Reference 8%, Name of local unit 8%, Ex. General Fund, State Highwa 8%, Ex. 1000; References money set 8%, Ex. Access Indiana; References 8%, Ex. 46710; References operatin 8%, Local unit's identification nu 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_NAME | category | 18 | 0 | Fiscal Year 1; CF_ATTRIB_VALUE_DESCR 1; CF_ATTRIB_VALUE 1; CF_ATTRIBUTE 1 |
| FIELD_TYPE | category | 14 | 0 | VARCHAR(20) 2; VARCHAR(5) 2; VARCHAR(40) 2; DATE 2 |
| DESCRIPTION | category | 18 | 0 | Fiscal Year of Transactio 1; Chartfield attribute desc 1; Chartfield attribute valu 1; Chartfield attribute numb 1 |
| NOTES | category | 14 | 4 | References classification 2; The state operates on a f 1; Ex: Motor Vehicle Highway 1; Ex: MOTOR_VEHICLE_HWY; Re 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:09:38.44061 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | bdd3cf4f-234d-45e6-82ba-c 18 |
| SRC_SHA256 | who | 1 | 0 | a9116c3cb474e1a51423767d7 18 |
