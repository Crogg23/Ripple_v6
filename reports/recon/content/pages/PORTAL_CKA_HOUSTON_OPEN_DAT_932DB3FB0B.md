# PORTAL_CKA_HOUSTON_OPEN_DAT_932DB3FB0B

rows 174  columns 11  scan 2.5s

roles: audit 2, category 2, date 1, other 5, state 1, who 1

## when

INGESTED_AT
  2026       174  ##############################

## who

SRC_SHA256 by rows
       174  d6eaca8b0a0c1b71d21d3f1a4ca1c2c1cf3c9aff485fb57907d039a08646348a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  d6eaca8b0a0c1b71d21d3f1a4ca1c2c1cf3c9aff  2026:174

## where

STATE: TX 168, TN 3, AL 1, OK 1, LA 1

## what

CITY: Houston 72%, Pearland 5%, Baytown 4%, Spring 3%, Humble 3%, Pasadena 3%, Channelview 2%, La Porte 2%, Porter 2%, Cypress 1%, Sugar Land 1%, Cleveland 1%

STATUS: AR 98%, O 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FRANCHISE_NO | other | 175 | 0 | 174 1; 173 1; 172 1; 171 1 |
| ORDINANCE_NO | other | 175 | 0 | 2015-0244 1; 2015-0243 1; 2015-0242 1; 2015-0241 1 |
| FRANCHISEE | other | 169 | 0 | The Grease Police 1; Storm-Tex Services, LLC  1; Stream Environmental, LLC 1; Velez Trucking, Inc. 1 |
| PHYSICAL_ADDRESS | other | 173 | 0 | 9000 Liberty Rd. 2; 5200 Egbert St. 2; 6418 Chippewa Blvd. 2; 10234 Lucore St 2 |
| CITY | category | 40 | 0 | Houston 102; Pearland 7; Baytown 6; Spring 4 |
| STATE | state | 5 | 0 | TX 168; TN 3; AL 1; OK 1 |
| ZIP | other | 106 | 0 | 77041 6; 77581 6; 77013 6; 77039 5 |
| STATUS | category | 2 | 0 | AR 170; O 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:36:18.24779 174 |
| SOURCE_RUN_ID | audit | 1 | 0 | ab0679f9-372f-46d8-92ae-5 174 |
| SRC_SHA256 | who | 1 | 0 | d6eaca8b0a0c1b71d21d3f1a4 174 |
