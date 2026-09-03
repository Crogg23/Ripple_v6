# PORTAL_CKA_ISRAEL_NATIONAL_2E5C5129DD

rows 54  columns 6  scan 2.1s

roles: audit 2, category 2, date 1, other 1, who 1

## when

INGESTED_AT
  2026        54  ##############################

## who

SRC_SHA256 by rows
        54  2f0e96f8e03cde72562d39b65333c32945e3c98a7f6ccf31ecbd7c202776ff33

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  2f0e96f8e03cde72562d39b65333c32945e3c98a  2026:54

## what

FORMAT: מרקט 62%, היפר 25%, מרקט מהדרין 12%, סיטי 2%

BRANCH: רמלה 11%, ירושלים 11%, בית שמש 11%, אשקלון 11%, תל אביב 7%, רעננה 7%, פתח תקווה 7%, יבנה 7%, חיפה 7%, חדרה 7%, באר שבע 7%, אילת 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FORMAT | category | 5 | 2 | מרקט 32; היפר 13; מרקט מהדרין 6; סיטי 1 |
| BRANCH | category | 38 | 0 | רמלה 3; ירושלים 3; בית שמש 3; אשקלון 3 |
| ADDRESS | other | 53 | 0 | הרוא”ה 2 1; השירה העברית 10 1; מבוא גרופית 2, פינת וייסב 1; דיזינגוף 50, דיזינגוף סנט 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:12:46.56848 54 |
| SOURCE_RUN_ID | audit | 1 | 0 | 24fc09bb-2beb-4176-bd81-7 54 |
| SRC_SHA256 | who | 1 | 0 | 2f0e96f8e03cde72562d39b65 54 |
