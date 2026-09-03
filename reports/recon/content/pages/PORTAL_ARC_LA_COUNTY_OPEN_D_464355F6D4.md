# PORTAL_ARC_LA_COUNTY_OPEN_D_464355F6D4

rows 6  columns 28  scan 3.9s

roles: amount 1, audit 2, category 11, date 1, empty 1, other 6, who 7

## when

INGESTED_AT
  2026         6  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 6 | 98.83 | 100 | 100 | 100 | 597.69 |

## who

CONAME by rows
         6  T-MOBILE

CONAME by dollars
      597.69        6 rows  T-MOBILE

STATE_NAME by rows
         6  California

STATE_NAME by dollars
      597.69        6 rows  California

NAICS by rows
         6  51731214

NAICS by dollars
      597.69        6 rows  51731214

SIC by rows
         6  481207

SIC by dollars
      597.69        6 rows  481207

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  T-MOBILE                                  2026:597.69

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:597.69

## what

OBJECTID: 16 17%, 14 17%, 9 17%, 7 17%, 6 17%, 4 17%

LOCNUM: 727710888 17%, 726058391 17%, 718613371 17%, 700275496 17%, 686878489 17%, 425911570 17%

STREET: S ALAMEDA ST 17%, E WASHINGTON BLVD 17%, W MARTIN LUTHER KING JR BLVD 17%, E GAGE AVE 17%, S FIGUEROA ST 17%, S VERMONT AVE 17%

CITY: LOS ANGELES 83%, HUNTINGTON PARK 17%

ZIP: 90255 17%, 90021 17%, 90037 17%, 90001 17%, 90007 17%, 90044 17%

ZIP4: 3620 17%, 3070 17%, 1816 17%, 1786 17%, 2549 17%, 3712 17%

SALESVOL: 5781 50%, 4817 17%, 1927 17%, 11561 17%

EMPNUM: 6 50%, 5 17%, 2 17%, 12 17%

FRNCOD: d 67%, T 33%

LOC_NAME: PointAddress 50%, StreetAddress 33%, Subaddress 17%

GEOMETRY: {"type": "Point", "coordinates 17%, {"type": "Point", "coordinates 17%, {"type": "Point", "coordinates 17%, {"type": "Point", "coordinates 17%, {"type": "Point", "coordinates 17%, {"type": "Point", "coordinates 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 6 | 0 | 16 1; 14 1; 9 1; 7 1 |
| LOCNUM | category | 6 | 0 | 727710888 1; 726058391 1; 718613371 1; 700275496 1 |
| CONAME | who | 1 | 0 | T-MOBILE 6 |
| STREET | category | 6 | 0 | S ALAMEDA ST 1; E WASHINGTON BLVD 1; W MARTIN LUTHER KING JR B 1; E GAGE AVE 1 |
| CITY | category | 2 | 0 | LOS ANGELES 5; HUNTINGTON PARK 1 |
| STATE | other | 1 | 0 | CA 6 |
| STATE_NAME | who | 1 | 0 | California 6 |
| ZIP | category | 6 | 0 | 90255 1; 90021 1; 90037 1; 90001 1 |
| ZIP4 | category | 6 | 0 | 3620 1; 3070 1; 1816 1; 1786 1 |
| NAICS | who | 1 | 0 | 51731214 6 |
| SIC | who | 1 | 0 | 481207 6 |
| SALESVOL | category | 4 | 0 | 5781 3; 4817 1; 1927 1; 11561 1 |
| HDBRCH | other | 1 | 0 | 2 6 |
| ULTNUM | who | 1 | 0 | 507958353 6 |
| PUBPRV | other | 1 | 0 | 2 6 |
| EMPNUM | category | 4 | 0 | 6 3; 5 1; 2 1; 12 1 |
| FRNCOD | category | 2 | 0 | d 4; T 2 |
| ISCODE | empty | 1 | 6 |  |
| SQFTCODE | other | 1 | 0 | 2 6 |
| LOC_NAME | category | 3 | 0 | PointAddress 3; StreetAddress 2; Subaddress 1 |
| STATUS | other | 1 | 0 | M 6 |
| SCORE | amount | 3 | 0 | 100.0 4; 98.859375 1; 98.828125 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 6 |
| REC_TYPE | other | 1 | 0 | 0 6 |
| GEOMETRY | category | 6 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:32.14818 6 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6b5e2e93-0912-44cd-bd1c-c 6 |
| SRC_SHA256 | who | 1 | 0 | 660f09d6c3b209509e062edf5 6 |
