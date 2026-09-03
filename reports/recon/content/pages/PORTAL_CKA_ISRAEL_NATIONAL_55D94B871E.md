# PORTAL_CKA_ISRAEL_NATIONAL_55D94B871E

rows 7.5K  columns 6  scan 3.2s

roles: audit 2, category 2, date 1, who 2

## when

INGESTED_AT
  2026      7.5K  ##############################

## who

DIAMOND_DEALER_NAME by rows
         3  כהן יוסף
         2  צדוק יצחק
         2  לוי יצחק
         2  לוי אברהם
         2  אסף כהן
         2  ארז מיכאל
         2  אליהו יעקב
         2  נעים שמעון
         2  גרינברג יוסף
         2  בורשטיין אברהם
         2  ארבוב גבריאל
         2  יעקב כהן
         2  אברהם לוי
         2  יצחק ניסנוב
         2  כהן משה
         2  דוד לוי
         2  גרוסמן יוסף
         2  לוי אליהו
         2  לוי מרדכי
         2  מזרחי שלום

SRC_SHA256 by rows
      7.5K  0434c2c52f943d53b12e6664d8c43c01c4fdc0f4823ede41a172c9b1875677a5

## who x when

DIAMOND_DEALER_NAME by INGESTED_AT  LOAD STAMP, not an event date
  אברהם לוי                                 2026:2
  אליהו יעקב                                2026:2
  אסף כהן                                   2026:2
  ארבוב גבריאל                              2026:2
  ארז מיכאל                                 2026:2
  בורשטיין אברהם                            2026:2
  גרוסמן יוסף                               2026:2
  גרינברג יוסף                              2026:2
  דוד לוי                                   2026:2
  יעקב כהן                                  2026:2
  יצחק ניסנוב                               2026:2
  כהן יוסף                                  2026:3
  כהן משה                                   2026:2
  לוי אברהם                                 2026:2
  לוי אליהו                                 2026:2
  לוי יצחק                                  2026:2
  לוי מרדכי                                 2026:2
  מזרחי שלום                                2026:2
  נעים שמעון                                2026:2
  צדוק יצחק                                 2026:2

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  0434c2c52f943d53b12e6664d8c43c01c4fdc0f4  2026:7.5K

## what

STATUS: לא פעיל 74%, פעיל 25%, בהליך רישום 0%

LICENSE_TYPE: סחר 58%, יצרן 27%, צורף 15%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DIAMOND_DEALER_NAME | who | 7.5K | 0 | תשובה עמי 38; תשובה הרצל 38; תרשיש-סולימני בע"מ 38; תרשיש רחמים 38 |
| STATUS | category | 3 | 0 | לא פעיל 5.6K; פעיל 1.9K; בהליך רישום 21 |
| LICENSE_TYPE | category | 3 | 0 | סחר 4.3K; יצרן 2.0K; צורף 1.1K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:36:24.39489 7.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 60b78218-14e0-4fe2-84c3-c 7.5K |
| SRC_SHA256 | who | 1 | 0 | 0434c2c52f943d53b12e6664d 7.5K |
