# PORTAL_CKA_INDIANA_DATA_HUB_90819D705E

rows 770  columns 7  scan 3.4s

roles: amount 1, audit 2, date 1, other 3, who 1

## when

INGESTED_AT
  2026       770  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERCENTAGE | 520 | 2.37 | 23.55 | 35.57 | 57.36 | 12.3K |

## who

SRC_SHA256 by rows
       770  cc3fae407e45dcdd30dfdac8e6f2c3252afc49b473f4ba3041aa6cbf571ef031

SRC_SHA256 by dollars
       12.3K      770 rows  cc3fae407e45dcdd30dfdac8e6f2c3252afc49b473f4ba3041aa6cbf571e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PERCENTAGE
  cc3fae407e45dcdd30dfdac8e6f2c3252afc49b4  2026:12.3K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ZIP_CD | other | 757 | 0 | Unknown 4; 47805 4; 47670 4; 46582 4 |
| PATIENT_COUNT | other | 495 | 0 | Suppressed 249; 2998 4; 980 4; 1241 4 |
| POPULATION | other | 512 | 0 | Suppressed 249; Unknown 3; 12852 3; 12352 3 |
| PERCENTAGE | amount | 520 | 0 | Suppressed 249; Unknown 3; 26.260500 3; 34.828300 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:46:47.12074 770 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5582f7d6-fd7e-493c-a137-9 770 |
| SRC_SHA256 | who | 1 | 0 | cc3fae407e45dcdd30dfdac8e 770 |
