# PORTAL_CKA_ISRAEL_NATIONAL_F6DE3CB3A1

rows 26  columns 9  scan 2.2s

roles: audit 2, category 6, date 1, who 1

## when

INGESTED_AT
  2026        26  ##############################

## who

SRC_SHA256 by rows
        26  04efd0262f81b8bd39e5eed5a85469f354ebe57b8634be300dd627256b05549a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  04efd0262f81b8bd39e5eed5a85469f354ebe57b  2026:26

## what

COL: 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%

FIELD_NAME: DATEUPDATED 8%, RECID 8%, ORDERER 8%, FINISH_DATE 8%, UPDATE_DATE 8%, SURVEY_DATE 8%, REG_MUN_ID 8%, LOCALITY_ID 8%, GUSH_SUFFIX 8%, GUSH_NUM 8%, TALAR_COMMENT 8%, MAX_NS 8%

DATA_TYPE: Long 42%, Text 38%, Double 8%, Date 4%, Geometry 4%, Object ID 4%

ALLOW_NULL: 1 92%, 0 8%

LENGTH: 20 50%, 200 10%, 2000 10%, 35 10%, 30 10%, 9 10%

COL_2: תאריך עדכון השכבה 8%, RECID 8%, שם המזמין 8%, תאריך סיום מדידה 8%, תאריך עדכון מדידה 8%, תאריך מדידה 8%, קוד רשות מוניציפלית לפי הלמ"ס 8%, קוד מקום לפי הלמ"ס 8%, מספר תת גוש 8%, מספר גוש 8%, הערות מתוך גיליון התצ"ר 8%, אורדינטה מקסימלית של המלבן החו 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COL | category | 26 | 0 | 26 1; 25 1; 24 1; 23 1 |
| FIELD_NAME | category | 26 | 0 | DATEUPDATED 1; RECID 1; ORDERER 1; FINISH_DATE 1 |
| DATA_TYPE | category | 6 | 0 | Long 11; Text 10; Double 2; Date 1 |
| ALLOW_NULL | category | 2 | 0 | 1 24; 0 2 |
| LENGTH | category | 7 | 16 | 20 5; 200 1; 2000 1; 35 1 |
| COL_2 | category | 26 | 0 | תאריך עדכון השכבה 1; RECID 1; שם המזמין 1; תאריך סיום מדידה 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:10:10.78639 26 |
| SOURCE_RUN_ID | audit | 1 | 0 | 44ff4915-6b14-4cc1-a27c-0 26 |
| SRC_SHA256 | who | 1 | 0 | 04efd0262f81b8bd39e5eed5a 26 |
