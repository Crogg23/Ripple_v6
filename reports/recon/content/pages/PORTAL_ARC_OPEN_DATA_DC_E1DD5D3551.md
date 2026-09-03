# PORTAL_ARC_OPEN_DATA_DC_E1DD5D3551

rows 11  columns 31  scan 4.0s

roles: amount 2, audit 2, category 13, date 1, empty 2, other 7, who 5

## when

INGESTED_AT
  2026        11  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 11 | 38.82 | 38.90 | 38.96 | 38.96 | 427.90 |
| LONGITUDE | 11 | -77.11 | -77.01 | -76.95 | -76.95 | -847.25 |

## who

PROPOSED by rows
        11  In Service

PROPOSED by dollars
      427.90       11 rows  In Service

DESC by rows
        11  In Service Substation

DESC by dollars
      427.90       11 rows  In Service Substation

NAICS_DESC by rows
        11  Electric Bulk Power Transmission and Control

NAICS_DESC by dollars
      427.90       11 rows  Electric Bulk Power Transmission and Control

COUNTRY by rows
        11  United States

COUNTRY by dollars
      427.90       11 rows  United States

## who x when

PROPOSED by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  In Service                                2026:427.90

DESC by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  In Service Substation                     2026:427.90

## what

FID: 11 9%, 10 9%, 9 9%, 8 9%, 7 9%, 6 9%, 5 9%, 4 9%, 3 9%, 2 9%, 1 9%

OBJECTID: 11 9%, 10 9%, 9 9%, 8 9%, 7 9%, 6 9%, 5 9%, 4 9%, 3 9%, 2 9%, 1 9%

NAME: Van Ness 9%, St Elizabeths Campus CHP 9%, Southwest 9%, Ft Slocum 9%, Dalecarlia 9%, Buzzard Point 9%, Blue Plains (Sub 83) 9%, Benning 9%, 12TH & Irving 9%, 10TH Street 9%, "O" Street 9%

CITY: Washington D.C., DC 36%, Somerset, MD 9%, Glassmanor, MD 9%, Chillum, MD 9%, Brookmont, MD 9%, Alexandria, VA 9%, Fairmount Heights, MD 9%, Mount Rainier, MD 9%

ZIP_CODE: 20016 18%, 20032 18%, 20003 9%, 20011 9%, 20024 9%, 20019 9%, 20017 9%, 20001 9%, 20005 9%

NUM_LINES: 4 36%, 0 18%, 2 18%, 12 9%, 10 9%, 8 9%

MIN_VOLT: 138 36%, 69 27%, 0 18%, 4 18%

MAX_VOLT: 138 36%, 230 27%, 0 18%, 69 18%

POSIT_REL: 1 82%, 3 9%, 2 9%

SOURCE: Aerial Imagery 82%, Previously Mapped Plant; Venty 18%

SOURCEDATE: 05/2005 36%, na 27%, 11/2009 18%, 01/2010 9%, 2006 9%

UNIQUE_ID: 39687 9%, 1012767 9%, 39684 9%, 54784 9%, 1011805 9%, 35146 9%, 43980 9%, 35145 9%, 54785 9%, 39683 9%, 39685 9%

GEOMETRY: {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 11 | 0 | 11 1; 10 1; 9 1; 8 1 |
| OBJECTID | category | 11 | 0 | 11 1; 10 1; 9 1; 8 1 |
| NAME | category | 11 | 0 | Van Ness 1; St Elizabeths Campus CHP 1; Southwest 1; Ft Slocum 1 |
| PROPOSED | who | 1 | 0 | In Service 11 |
| CITY | category | 8 | 0 | Washington D.C., DC 4; Somerset, MD 1; Glassmanor, MD 1; Chillum, MD 1 |
| STATE | other | 1 | 0 | DC 11 |
| ZIP_CODE | category | 9 | 0 | 20016 2; 20032 2; 20003 1; 20011 1 |
| COUNTRY | who | 1 | 0 | United States 11 |
| LATITUDE | amount | 11 | 0 | 38.942611 1; 38.8539 1; 38.880613 1; 38.961508 1 |
| LONGITUDE | amount | 11 | 0 | -77.078932 1; -76.998939 1; -77.008567 1; -77.010762 1 |
| DESC | who | 1 | 0 | In Service Substation 11 |
| NUM_LINES | category | 6 | 0 | 4 4; 0 2; 2 2; 12 1 |
| FLOWGATE | other | 1 | 0 | F 11 |
| MIN_VOLT | category | 4 | 0 | 138 4; 69 3; 0 2; 4 2 |
| MAX_VOLT | category | 4 | 0 | 138 4; 230 3; 0 2; 69 2 |
| AVG_LOAD | empty | 1 | 11 |  |
| AVG_OUTPUT | empty | 1 | 11 |  |
| NAICS_CODE | other | 1 | 0 | 221121 11 |
| NAICS_DESC | who | 1 | 0 | Electric Bulk Power Trans 11 |
| SIC_CODE | other | 1 | 0 | 491 11 |
| POSIT_REL | category | 3 | 0 | 1 9; 3 1; 2 1 |
| SOURCE | category | 2 | 0 | Aerial Imagery 9; Previously Mapped Plant;  2 |
| SOURCEDATE | category | 5 | 0 | 05/2005 4; na 3; 11/2009 2; 01/2010 1 |
| UNIQUE_ID | category | 11 | 0 | 39687 1; 1012767 1; 39684 1; 54784 1 |
| FEAT_TYPE | other | 1 | 0 | Point 11 |
| IN_DOEE_MG | other | 1 | 0 | 0 11 |
| CONSEQUENC | other | 1 | 0 | 18 11 |
| GEOMETRY | category | 11 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:13:12.52099 11 |
| SOURCE_RUN_ID | audit | 1 | 0 | 93056e24-08f4-401c-9db4-2 11 |
| SRC_SHA256 | who | 1 | 0 | d43a65cb24e5cc05d1d57c79f 11 |
