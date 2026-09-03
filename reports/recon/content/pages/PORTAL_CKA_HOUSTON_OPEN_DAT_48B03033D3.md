# PORTAL_CKA_HOUSTON_OPEN_DAT_48B03033D3

rows 31  columns 7  scan 2.1s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        31  ##############################

## who

SRC_SHA256 by rows
        31  cbf21916504a20789a94b50ca31f062b96baf4a663b333e99818f6541a695412

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  cbf21916504a20789a94b50ca31f062b96baf4a6  2026:31

## what

BUSINESS_AREA_ID: 9999 8%, 9900 8%, 9800 8%, 9700 8%, 9000 8%, 8000 8%, 7500 8%, 7000 8%, 6800 8%, 6700 8%, 6500 8%, 6400 8%

BUSINESS_AREA_TYPE: Administrative Services 32%, Public Safety 19%, Human & Cultural Services 19%, Development & Maintenance Serv 13%, Debt Service 6%, General Government 3%, Revolving Funds 3%, Enterprise Funds 3%

BUSINESS_AREA_NAME: Forensic Services 8%, General Government 8%, Investment Management 8%, General Debt Service 8%, Legal 8%, Human Resources 8%, City Secretary 8%, Planning & Development 8%, Houston Information Technology 8%, Fleet Management Department 8%, Administration and Regulatory  8%, Finance Department 8%

BUSINESS_AREA_SHORT_NAME: CL 8%, GG 8%, IM 8%, GDS 8%, LGL 8%, HR 8%, CSC 8%, PD 8%, IT 8%, FMD 8%, ARA 8%, FIN 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_AREA_ID | category | 30 | 0 | 9999 1; 9900 1; 9800 1; 9700 1 |
| BUSINESS_AREA_TYPE | category | 8 | 0 | Administrative Services 10; Public Safety 6; Human & Cultural Services 6; Development & Maintenance 4 |
| BUSINESS_AREA_NAME | category | 31 | 0 | Forensic Services 1; General Government 1; Investment Management 1; General Debt Service 1 |
| BUSINESS_AREA_SHORT_NAME | category | 31 | 0 | CL 1; GG 1; IM 1; GDS 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:10:49.65561 31 |
| SOURCE_RUN_ID | audit | 1 | 0 | fd880807-5f65-4325-aff0-1 31 |
| SRC_SHA256 | who | 1 | 0 | cbf21916504a20789a94b50ca 31 |
