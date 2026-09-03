# PORTAL_CKA_HOUSTON_OPEN_DAT_FB1F968C19

rows 1.0K  columns 5  scan 2.5s

roles: audit 2, date 1, id 1, who 2

## when

INGESTED_AT
  2026      1.0K  ##############################

## who

FUND_CENTER_NAME by rows
         3  DO NOT USE
         2  HFD - Procurement
         2  SWM-Yard Waste
         2  PRD-Family Programs
         2  FIN.-Accounts Receivable & Collections
         2  F&A-Special Events
         2  PWE-EB Cape Center
         2  SWM-Administration
         1  HPD-Technology Svcs
         1  HPD-Homicide
         1  PWE-Brdge Replacemnt
         1  HPD-Staff Services Command
         1  HPD-Investigati Ops
         1  HEC-Police Call Take
         1  PWE-JointCrackSealng
         1  HPD-Kingwood Patrol
         1  HPD-Phase Down A
         1  PWE-Houston TranStar
         1  MDJ
         1  HPD-Red Light Funded Programs

SRC_SHA256 by rows
      1.0K  8ed8fd94a3b4a4b38dd078629a0ecb048a014a699557e6e0ed44c28600631d2e

## who x when

FUND_CENTER_NAME by INGESTED_AT  LOAD STAMP, not an event date
  DO NOT USE                                2026:3
  F&A-Special Events                        2026:2
  FIN.-Accounts Receivable & Collections    2026:2
  HEC-Police Call Take                      2026:1
  HFD - Procurement                         2026:2
  HPD-Homicide                              2026:1
  HPD-Investigati Ops                       2026:1
  HPD-Kingwood Patrol                       2026:1
  HPD-Phase Down A                          2026:1
  HPD-Red Light Funded Programs             2026:1
  HPD-Staff Services Command                2026:1
  HPD-Technology Svcs                       2026:1
  MDJ                                       2026:1
  PRD-Family Programs                       2026:2
  PWE-Brdge Replacemnt                      2026:1
  PWE-EB Cape Center                        2026:2
  PWE-Houston TranStar                      2026:1
  PWE-JointCrackSealng                      2026:1
  SWM-Administration                        2026:2
  SWM-Yard Waste                            2026:2

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  8ed8fd94a3b4a4b38dd078629a0ecb048a014a69  2026:1.0K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FUND_CENTER_ID | id | 1.0K | 0 | 9900010005 6; 9900010004 6; 9900010003 6; 9900010002 6 |
| FUND_CENTER_NAME | who | 1.0K | 0 | GGOV-Other-Hurricane Ike  6; GGOV-ERP Equipment Acquis 6; GGOV-Mayor Com Child 6; GGOV-H&CDNonGrantExp 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:24:01.46516 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1e6042d9-3904-47a9-9859-c 1.0K |
| SRC_SHA256 | who | 1 | 0 | 8ed8fd94a3b4a4b38dd078629 1.0K |
