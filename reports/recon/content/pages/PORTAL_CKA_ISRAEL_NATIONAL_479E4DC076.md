# PORTAL_CKA_ISRAEL_NATIONAL_479E4DC076

rows 13  columns 8  scan 1.9s

roles: audit 2, category 5, date 1, who 1

## when

INGESTED_AT
  2026        13  ##############################

## who

SRC_SHA256 by rows
        13  62b50b8d3e59e3054834c0bd7e98142e6148428816c09d227674d75550aa03e4

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  62b50b8d3e59e3054834c0bd7e98142e61484288  2026:13

## what

COL: 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%

FIELD_NAME: DATEUPDATED 8%, RECID 8%, TATAG_STATUS_DATE 8%, TATAG_STATUS 8%, TATAG_YEAR 8%, TATAG_NUM 8%, LOCALITY_ID 8%, GUSH_SUFFIX 8%, GUSH_NUM 8%, Shape_Area 8%, Shape_Length 8%, Shape 8%

DATA_TYPE: Long 38%, Date 15%, Short 15%, Double 15%, Geometry 8%, Object ID 8%

ALLOW_NULL: 1 85%, 0 15%

COL_2: תאריך עדכון השכבה 8%, RECID 8%, תאריך עדכון סטטוס 8%, קוד סטטוס. 1 - תת"ג בביקורת, 2 8%, שנת תת"ג 8%, מספר תת"ג 8%, קוד מקום לפי הלמ"ס 8%, מספר תת גוש 8%, מספר גוש 8%, שטח הגיאומטריה 8%, אורך הגיאומטריה 8%, הגאומטריה 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COL | category | 13 | 0 | 13 1; 12 1; 11 1; 10 1 |
| FIELD_NAME | category | 13 | 0 | DATEUPDATED 1; RECID 1; TATAG_STATUS_DATE 1; TATAG_STATUS 1 |
| DATA_TYPE | category | 6 | 0 | Long 5; Date 2; Short 2; Double 2 |
| ALLOW_NULL | category | 2 | 0 | 1 11; 0 2 |
| COL_2 | category | 13 | 0 | תאריך עדכון השכבה 1; RECID 1; תאריך עדכון סטטוס 1; קוד סטטוס. 1 - תת"ג בביקו 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:32.28415 13 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9ba28ba8-e861-4f64-84c6-b 13 |
| SRC_SHA256 | who | 1 | 0 | 62b50b8d3e59e3054834c0bd7 13 |
