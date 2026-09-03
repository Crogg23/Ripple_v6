# PORTAL_ARC_LA_COUNTY_OPEN_D_1632A8E413

rows 12  columns 28  scan 3.9s

roles: amount 1, audit 2, category 19, date 1, other 2, who 4

## when

INGESTED_AT
  2026        12  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 12 | 98.59 | 100 | 100 | 100 | 1.2K |

## who

STATE_NAME by rows
        12  California

STATE_NAME by dollars
        1.2K       12 rows  California

SOURCE by rows
        12  INFOGROUP

SOURCE by dollars
        1.2K       12 rows  INFOGROUP

CITY by rows
        12  LOS ANGELES

CITY by dollars
        1.2K       12 rows  LOS ANGELES

SRC_SHA256 by rows
        12  8f0e7b8cfd54626e7f9fe23c3e8a5fd6f4302d506bc9eee38c375340edf483b0

SRC_SHA256 by dollars
        1.2K       12 rows  8f0e7b8cfd54626e7f9fe23c3e8a5fd6f4302d506bc9eee38c375340edf4

## who x when

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:1.2K

SOURCE by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  INFOGROUP                                 2026:1.2K

## what

OBJECTID: 19 8%, 18 8%, 17 8%, 16 8%, 10 8%, 9 8%, 7 8%, 5 8%, 4 8%, 3 8%, 2 8%, 1 8%

LOCNUM: 730297130 8%, 719500563 8%, 706479041 8%, 698231784 8%, 688183805 8%, 688159748 8%, 477696249 8%, 414637690 8%, 412889274 8%, 381990225 8%, 372126920 8%, 170412415 8%

CONAME: MC DONALD'S 83%, MCDONALD WRIGHT 8%, MC DONALD'S SWIM STADIUM 8%

STREET: S FIGUEROA ST 18%, W SLAUSON AVE 18%, W MARTIN LUTHER KING JR BLVD 18%, W FLORENCE AVE 9%, S CENTRAL AVE 9%, W WASHINGTON BLVD 9%, E SLAUSON AVE 9%, W 34TH ST 9%

ZIP: 90044 17%, 90011 17%, 90037 17%, 90001 8%, 90007 8%, 90047 8%, 90015 8%, 90089 8%, 90008 8%

ZIP4: 6101 9%, 2707 9%, 3257 9%, 1129 9%, 3514 9%, 4800 9%, 2002 9%, 0086 9%, 1816 9%, 2722 9%, 5599 9%

NAICS: 72251301 83%, 99999004 8%, 71394019 8%

SIC: 581208 83%, 999977 8%, 799704 8%

SALESVOL: 2663 42%, 0 8%, 4188 8%, 3551 8%, 182 8%, 2367 8%, 2012 8%, 3255 8%

HDBRCH: 2 100%

ULTNUM: 001682400 83%, 000000000 17%

PUBPRV: 2 100%

EMPNUM: 45 42%, 0 8%, 90 8%, 60 8%, 2 8%, 40 8%, 34 8%, 55 8%

FRNCOD: K 100%

ISCODE: e 100%

SQFTCODE: 3 75%, 1 17%, 2 8%

LOC_NAME: PointAddress 83%, Postal 8%, StreetAddress 8%

REC_TYPE: 0 92%, 1 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 12 | 0 | 19 1; 18 1; 17 1; 16 1 |
| LOCNUM | category | 12 | 0 | 730297130 1; 719500563 1; 706479041 1; 698231784 1 |
| CONAME | category | 3 | 0 | MC DONALD'S 10; MCDONALD WRIGHT 1; MC DONALD'S SWIM STADIUM 1 |
| STREET | category | 9 | 1 | S FIGUEROA ST 2; W SLAUSON AVE 2; W MARTIN LUTHER KING JR B 2; W FLORENCE AVE 1 |
| CITY | who | 1 | 0 | LOS ANGELES 12 |
| STATE | other | 1 | 0 | CA 12 |
| STATE_NAME | who | 1 | 0 | California 12 |
| ZIP | category | 9 | 0 | 90044 2; 90011 2; 90037 2; 90001 1 |
| ZIP4 | category | 12 | 1 | 6101 1; 2707 1; 3257 1; 1129 1 |
| NAICS | category | 3 | 0 | 72251301 10; 99999004 1; 71394019 1 |
| SIC | category | 3 | 0 | 581208 10; 999977 1; 799704 1 |
| SALESVOL | category | 8 | 0 | 2663 5; 0 1; 4188 1; 3551 1 |
| HDBRCH | category | 2 | 2 | 2 10 |
| ULTNUM | category | 2 | 0 | 001682400 10; 000000000 2 |
| PUBPRV | category | 2 | 2 | 2 10 |
| EMPNUM | category | 8 | 0 | 45 5; 0 1; 90 1; 60 1 |
| FRNCOD | category | 2 | 2 | K 10 |
| ISCODE | category | 2 | 2 | e 10 |
| SQFTCODE | category | 3 | 0 | 3 9; 1 2; 2 1 |
| LOC_NAME | category | 3 | 0 | PointAddress 10; Postal 1; StreetAddress 1 |
| STATUS | other | 1 | 0 | M 12 |
| SCORE | amount | 2 | 0 | 100.0 10; 98.59375 2 |
| SOURCE | who | 1 | 0 | INFOGROUP 12 |
| REC_TYPE | category | 2 | 0 | 0 11; 1 1 |
| GEOMETRY | category | 12 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:13:24.21518 12 |
| SOURCE_RUN_ID | audit | 1 | 0 | a99e7764-f364-4278-9fdb-3 12 |
| SRC_SHA256 | who | 1 | 0 | 8f0e7b8cfd54626e7f9fe23c3 12 |
