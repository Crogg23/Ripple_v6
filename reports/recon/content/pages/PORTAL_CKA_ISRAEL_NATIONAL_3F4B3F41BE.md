# PORTAL_CKA_ISRAEL_NATIONAL_3F4B3F41BE

rows 150  columns 10  scan 2.2s

roles: audit 2, category 1, date 1, other 6, who 1

## when

INGESTED_AT
  2026       150  ##############################

## who

SRC_SHA256 by rows
       150  d9b07ab9a3f40e92b0325207783cb601bbd8229baa7f9aa83aa81bbcc760299d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  d9b07ab9a3f40e92b0325207783cb601bbd8229b  2026:150

## what

MAAMAD: שגרירות 68%, שגרירות לא תושבת 21%, קונסוליה כללית 9%, קונסוליה 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| K_NTZ | other | 147 | 0 | 27 4; 74 2; 242 1; 130 1 |
| SHEM_MDN | other | 132 | 0 | קונגו 4; צרפת 4; רומניה 2; בלגיה 2 |
| SHEM_NTZ | other | 148 | 0 | הרפובליקה של קונגו 4; הרפובליקה של פרגוואי 2; של רומניה בחיפה 1; של ממלכת בלגיה בירושלים 1 |
| MAAMAD | category | 4 | 0 | שגרירות 102; שגרירות לא תושבת 32; קונסוליה כללית 13; קונסוליה 3 |
| ADDRESS | other | 101 | 46 | Herzliya Pituach Maskit 9 4; Herzliya Pituah Arieh She 2; Tel Aviv Rehov Pinkas 54/ 1; Tel Aviv Israelis St. 9   1 |
| TEL | other | 95 | 53 | 09-957 7130 2; 03-5535772 2; 09-7732555 2; 03-5465866 1 |
| FAX | other | 90 | 59 | 09-957 7216 2; 03-5535769 2; 03-5444545 1; 03-524 7379 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:16:30.01366 150 |
| SOURCE_RUN_ID | audit | 1 | 0 | a0b63cf9-30d1-409b-afad-b 150 |
| SRC_SHA256 | who | 1 | 0 | d9b07ab9a3f40e92b03252077 150 |
