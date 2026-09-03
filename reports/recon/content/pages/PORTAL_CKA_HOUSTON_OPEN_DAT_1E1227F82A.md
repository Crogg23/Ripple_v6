# PORTAL_CKA_HOUSTON_OPEN_DAT_1E1227F82A

rows 2.0K  columns 9  scan 2.6s

roles: amount 1, audit 2, category 1, date 1, id 1, other 2, who 2

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_AWARDED | 904 | 0 | 690.5K | 55.08M | 275.11M | 3.55B |

## who

SUPPLIER_NAME by rows
         4  XEROX CORPORATION
         2  INTERNATIONAL ROADWAY RESEARCH
         2  ALL PLAY INC
         2  IBM CORPORATION
         2  MAXIMUS INC
         2  LION APPAREL INC
         2  BROOKSIDE EQUIPMENT SALES INC
         2  SIEMENS WATER TECHNOLOGIES
         2  TIBH INDUSTRIES INC
         2  JBT AEROTECH SERVICES
         2  ICS - INTERGRATED
         2  GLOBE ELECTRIC COMPANY INC
         2  HOUMA ARMATURE WORKS HOUSTON
         2  HERTZ EQUIPMENT RENTAL CORP
         2  MOORE MEDICAL LLC
         2  HARRIS COUNTY
         2  GRAYBAR ELECTRIC COMPANY INC
         2  NORTHWEST PIPE COMPANY
         2  AIRGAS-SOUTHWEST INC
         2  FERNANDEZ AND SONS

SUPPLIER_NAME by dollars
     275.11M        1 rows  DEPARTMENT OF INFO RESOURCES
     172.43M        1 rows  MOTIVA ENTERPRISES LLC
     126.32M        1 rows  GENUINE PARTS COMPANY
      98.00M        1 rows  DRC EMERGENCY SERVICES,LLC
      97.27M        1 rows  TD INDUSTRIES
      88.86M        1 rows  ALTIVIA CORPORATION
      88.08M        1 rows  CONOCOPHILLIPS COMPANY
      66.93M        1 rows  G4S SECURE SOLUTIONS(USA)INC
      66.07M        1 rows  BOMBARDIER TRANSPORTATION
      55.24M        1 rows  SOUTHWESTERN BELL TELEPHONE CO
      50.00M        1 rows  PETROLEUM TRADERS CORPORATION
      49.94M        1 rows  MID-AMERICAN / E.R.S JOINT VENTURE
      46.99M        1 rows  Itron
      43.07M        1 rows  CENTURY ASPHALT MATERIALS
      39.00M        1 rows  US BANK NATIONAL ASSOCIATION ND
      35.00M        1 rows  BECK DISASTER RECOVERY INC
      33.64M        1 rows  VERIZON SELECT SERVICES,INC
      32.27M        1 rows  SYNAGRO OF TEXAS-CDR INC
      30.81M        1 rows  JOHNSON CONTROLS, INC
      30.36M        1 rows  COMFORT SYSTEMS USA SOUTH CENTRAL

SRC_SHA256 by rows
      2.0K  043763635d7eda10dfa389ca227db155daddd9741a9bbfee50afdc544a07362d

SRC_SHA256 by dollars
       3.55B     2.0K rows  043763635d7eda10dfa389ca227db155daddd9741a9bbfee50afdc544a07

## who x when

SUPPLIER_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_AWARDED
  AIRGAS-SOUTHWEST INC                      2026:3.66M
  ALL PLAY INC                              2026:265.5K
  ALTIVIA CORPORATION                       2026:88.86M
  BOMBARDIER TRANSPORTATION                 2026:66.07M
  BROOKSIDE EQUIPMENT SALES INC             2026:793.3K
  CONOCOPHILLIPS COMPANY                    2026:88.08M
  DEPARTMENT OF INFO RESOURCES              2026:275.11M
  DRC EMERGENCY SERVICES,LLC                2026:98.00M
  FERNANDEZ AND SONS                        2026:1.60M
  G4S SECURE SOLUTIONS(USA)INC              2026:66.93M
  GENUINE PARTS COMPANY                     2026:126.32M
  GLOBE ELECTRIC COMPANY INC                2026:1.56M
  GRAYBAR ELECTRIC COMPANY INC              2026:5.71M
  HARRIS COUNTY                             2026:698.9K
  HERTZ EQUIPMENT RENTAL CORP               2026:339.4K
  HOUMA ARMATURE WORKS HOUSTON              2026:17.31M
  IBM CORPORATION                           2026:760.1K
  ICS - INTERGRATED                         2026:1.20M
  INTERNATIONAL ROADWAY RESEARCH            2026:156.0K
  JBT AEROTECH SERVICES                     2026:30.21M
  LION APPAREL INC                          2026:22.11M
  MAXIMUS INC                               2026:540.4K
  MOORE MEDICAL LLC                         2026:734.3K
  MOTIVA ENTERPRISES LLC                    2026:172.43M
  NORTHWEST PIPE COMPANY                    2026:1.02M
  SIEMENS WATER TECHNOLOGIES                2026:2.33M
  SOUTHWESTERN BELL TELEPHONE CO            2026:55.24M
  TD INDUSTRIES                             2026:97.27M
  TIBH INDUSTRIES INC                       2026:30.20M
  XEROX CORPORATION                         2026:23.17M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_AWARDED
  043763635d7eda10dfa389ca227db155daddd974  2026:3.55B

## what

WEB: - 100%, http://www.hon.com 0%, http://www.allsteeloffice.com/ 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SUPPLIER_NAME | who | 873 | 1.1K | XEROX CORPORATION 8; TIBH INDUSTRIES INC 6; ZIPCAR, INC. 5; ZEP MANUFACTURING COMPANY 5 |
| ADDRESS | id | 2.0K | 0 | N/A 17; PO Box 650361 13; CAMBRIDGE MA 02141 11; 25 11 |
| PHONE | other | 826 | 1.1K | - 25; N/A 16; 936-321-3845 6; 713-849-2045 6 |
| FAX | other | 735 | 1.1K | - 153; 713-402-6457 5; 281-348-2578 4; 214-614-4904 4 |
| WEB | category | 4 | 1.1K | - 902; http://www.hon.com 1; http://www.allsteeloffice 1 |
| TOTAL_AWARDED | amount | 771 | 1.1K | 0 110; 1000000 8; 1 7; 300000 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:28:17.49561 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c0fbc1fa-73f7-4a37-b54a-d 2.0K |
| SRC_SHA256 | who | 1 | 0 | 043763635d7eda10dfa389ca2 2.0K |
