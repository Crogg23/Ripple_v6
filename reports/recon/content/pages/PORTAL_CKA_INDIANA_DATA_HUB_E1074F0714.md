# PORTAL_CKA_INDIANA_DATA_HUB_E1074F0714

rows 4.8K  columns 5  scan 2.9s

roles: audit 2, date 1, other 1, who 2

## when

INGESTED_AT
  2026      4.8K  ##############################

## who

SITE_NAME by rows
         1  Vigo County Clerk
         1  Marion County Superior Court - Probation Northeast
         1  Women's Care Center - Elkhart
         1  Coburn Place
         1  Riverbend Cancer Services
         1  Octapharma Plasma Donation Center - Indianapolis - Lafayette Road
         1  Humane Society of Elkhart County
         1  Beyond Homeless
         1  New Hope Christian Center
         1  Geminus
         1  Northeast Indiana Small Business Development Center
         1  Wellspring Shoppe
         1  Scottsburg Mobile Food Pantry
         1  Salvation Army Adult Rehabilitation Center - Indianapolis
         1  Ebenezer Baptist Church - Rainbow House Food Pantry
         1  Quarantine Shelter Point of Contact - Aspire Indiana
         1  Churches In Mission - Martinsville
         1  The Milk Bank at IU Health North
         1  Bowen Center - DeKalb County
         1  Duke Energy

SRC_SHA256 by rows
      4.8K  6b50ddca5a44ce3345027aed9ca5a4343ca94d1333b3d0792a2c56449d9876ff

## who x when

SITE_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Beyond Homeless                           2026:1
  Bowen Center - DeKalb County              2026:1
  Churches In Mission - Martinsville        2026:1
  Coburn Place                              2026:1
  Duke Energy                               2026:1
  Ebenezer Baptist Church - Rainbow House   2026:1
  Geminus                                   2026:1
  Humane Society of Elkhart County          2026:1
  Marion County Superior Court - Probation  2026:1
  New Hope Christian Center                 2026:1
  Northeast Indiana Small Business Develop  2026:1
  Octapharma Plasma Donation Center - Indi  2026:1
  Quarantine Shelter Point of Contact - As  2026:1
  Riverbend Cancer Services                 2026:1
  Salvation Army Adult Rehabilitation Cent  2026:1
  Scottsburg Mobile Food Pantry             2026:1
  The Milk Bank at IU Health North          2026:1
  Vigo County Clerk                         2026:1
  Wellspring Shoppe                         2026:1
  Women's Care Center - Elkhart             2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  6b50ddca5a44ce3345027aed9ca5a4343ca94d13  2026:4.8K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SITE_NAME | who | 4.8K | 0 | Wayne Township Assessor 24; SCAN 24; Miller Township Trustee - 24; Catholic Charities Crisis 24 |
| REFERRALS | other | 771 | 0 | 10 180; 12 151; 11 146; 13 145 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:33:18.03326 4.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | 087e42bb-7be7-4ea8-82d9-2 4.8K |
| SRC_SHA256 | who | 1 | 0 | 6b50ddca5a44ce3345027aed9 4.8K |
