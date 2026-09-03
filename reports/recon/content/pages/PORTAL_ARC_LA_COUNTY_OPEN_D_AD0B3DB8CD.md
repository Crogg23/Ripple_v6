# PORTAL_ARC_LA_COUNTY_OPEN_D_AD0B3DB8CD

rows 22  columns 28  scan 3.5s

roles: amount 1, audit 2, category 16, date 1, empty 1, other 3, who 5

## when

INGESTED_AT
  2026        22  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 22 | 98.83 | 100 | 100 | 100 | 2.2K |

## who

STATE_NAME by rows
        22  California

STATE_NAME by dollars
        2.2K       22 rows  California

NAICS by rows
        22  51731214

NAICS by dollars
        2.2K       22 rows  51731214

SIC by rows
        22  481207

SIC by dollars
        2.2K       22 rows  481207

SOURCE by rows
        22  INFOGROUP

SOURCE by dollars
        2.2K       22 rows  INFOGROUP

## who x when

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:2.2K

NAICS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  51731214                                  2026:2.2K

## what

OBJECTID: 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%

LOCNUM: 744782238 8%, 735191338 8%, 727710888 8%, 726058481 8%, 726058391 8%, 724910044 8%, 722384350 8%, 718615231 8%, 718613686 8%, 718613371 8%, 718613325 8%, 708796417 8%

CONAME: T-MOBILE 73%, SPRINT 23%, AT&T STORE 5%

STREET: S VERMONT AVE 19%, W SLAUSON AVE 10%, E WASHINGTON BLVD 10%, W PICO BLVD 10%, S WESTERN AVE 10%, S FIGUEROA ST 10%, S BROADWAY 10%, S ALAMEDA ST 5%, E 2ND ST 5%, W MARTIN LUTHER KING JR BLVD 5%, E GAGE AVE 5%, WILSHIRE BLVD 5%

CITY: LOS ANGELES 95%, HUNTINGTON PARK 5%

ZIP: 90006 20%, 90047 10%, 90044 10%, 90015 10%, 90012 10%, 90017 10%, 90255 5%, 90005 5%, 90021 5%, 90037 5%, 90001 5%, 90007 5%

ZIP4: 3712 14%, 5804 14%, 1129 7%, 3620 7%, 1521 7%, 3070 7%, 2409 7%, 4651 7%, 3819 7%, 1816 7%, 2561 7%, 3721 7%

SALESVOL: 5781 32%, 1927 27%, 6744 14%, 4817 9%, 11561 9%, 9634 9%

HDBRCH: 2 100%

ULTNUM: 507958353 68%, 800138737 23%, 460637358 5%, 000000000 5%

PUBPRV: 2 100%

EMPNUM: 6 32%, 2 27%, 7 14%, 5 9%, 12 9%, 10 9%

FRNCOD: d 45%, T 27%, S 23%, D 5%

SQFTCODE: 2 73%, 3 23%, 5 5%

LOC_NAME: PointAddress 50%, Subaddress 32%, StreetAddress 18%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 22 | 0 | 22 1; 21 1; 20 1; 19 1 |
| LOCNUM | category | 22 | 0 | 744782238 1; 735191338 1; 727710888 1; 726058481 1 |
| CONAME | category | 3 | 0 | T-MOBILE 16; SPRINT 5; AT&T STORE 1 |
| STREET | category | 13 | 0 | S VERMONT AVE 4; W SLAUSON AVE 2; E WASHINGTON BLVD 2; W PICO BLVD 2 |
| CITY | category | 2 | 0 | LOS ANGELES 21; HUNTINGTON PARK 1 |
| STATE | other | 1 | 0 | CA 22 |
| STATE_NAME | who | 1 | 0 | California 22 |
| ZIP | category | 14 | 0 | 90006 4; 90047 2; 90044 2; 90015 2 |
| ZIP4 | category | 19 | 1 | 3712 2; 5804 2; 1129 1; 3620 1 |
| NAICS | who | 1 | 0 | 51731214 22 |
| SIC | who | 1 | 0 | 481207 22 |
| SALESVOL | category | 6 | 0 | 5781 7; 1927 6; 6744 3; 4817 2 |
| HDBRCH | category | 2 | 1 | 2 21 |
| ULTNUM | category | 4 | 0 | 507958353 15; 800138737 5; 460637358 1; 000000000 1 |
| PUBPRV | category | 2 | 1 | 2 21 |
| EMPNUM | category | 6 | 0 | 6 7; 2 6; 7 3; 5 2 |
| FRNCOD | category | 4 | 0 | d 10; T 6; S 5; D 1 |
| ISCODE | empty | 1 | 22 |  |
| SQFTCODE | category | 3 | 0 | 2 16; 3 5; 5 1 |
| LOC_NAME | category | 3 | 0 | PointAddress 11; Subaddress 7; StreetAddress 4 |
| STATUS | other | 1 | 0 | M 22 |
| SCORE | amount | 3 | 0 | 100.0 20; 98.859375 1; 98.828125 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 22 |
| REC_TYPE | other | 1 | 0 | 0 22 |
| GEOMETRY | category | 22 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:56.74437 22 |
| SOURCE_RUN_ID | audit | 1 | 0 | af8e792d-b97c-4c22-97f8-5 22 |
| SRC_SHA256 | who | 1 | 0 | 557609ec13a7f67b494d1f056 22 |
