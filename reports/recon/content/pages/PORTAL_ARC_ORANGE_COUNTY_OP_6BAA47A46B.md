# PORTAL_ARC_ORANGE_COUNTY_OP_6BAA47A46B

rows 33  columns 28  scan 3.9s

roles: amount 2, audit 2, category 11, date 3, empty 8, who 3

## when

CREATIONDATE
  2025        33  ##############################

EDITDATE
  2025        33  ##############################

INGESTED_AT
  2026        33  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PROGRAM_ELEMENT | 31 | 33.54 | 33.56 | 33.63 | 33.63 | 1.0K |
| GIS_LATITUDE | 31 | -117.65 | -117.64 | -117.58 | -117.58 | -3.6K |

## who

CREATOR by rows
        33  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
        1.0K       33 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
        33  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
        1.0K       33 rows  vickie.bach@ocpw.ocgov.com_OCPW

SRC_SHA256 by rows
        33  3220fa53f9380546cf44cbd7e34ccb061bef919fed7a4d588e5bd388a1a9ddfe

SRC_SHA256 by dollars
        1.0K       33 rows  3220fa53f9380546cf44cbd7e34ccb061bef919fed7a4d588e5bd388a1a9

## who x when

CREATOR by CREATIONDATE, dollars = PROGRAM_ELEMENT
  vickie.bach@ocpw.ocgov.com_OCPW           2025:1.0K

EDITOR by CREATIONDATE, dollars = PROGRAM_ELEMENT
  vickie.bach@ocpw.ocgov.com_OCPW           2025:1.0K

## what

OBJECTID: 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%

FACILITY_ID: OPEN 94%, nan 6%

NAME: nan 15%, Oak Tree Park and Pool 8%, Starlight Ridge Park 8%, Flintridge Village Club 8%, Chapparal Park 8%, Township Plunge 8%, Town Green 8%, Oak Knoll Village Club 8%, Hilltop Park 8%, Celestial Plunge 8%, Poets Park 8%, Boreal Plunge 8%

ADDRESS: nan 15%, 25571 Meandering Trail  Las Fl 8%, 25702 Crestview  Las Flores  8%, 28112 Roanoke Drive Ladera Ran 8%, 29075 Sienna Pkwy. Ladera Ranc 8%, 28532 Second Street Ladera Ran 8%, 28801 Sienna Pkwy. Ladera Ranc 8%, 28192 O'neill Pkwy. Ladera Ran 8%, 1 Wickford Lane Ladera Ranch  8%, 29145 Ethereal Street Ladera R 8%, 28741 Tuberose Street Ladera R 8%, 27642 Gaia Lane Ladera Ranch  8%

CITY: Ladera Ranch 70%, Coto de Caza 18%, nan 6%, Las Flores 6%

EXISTING_DEVELOPMENT: NO 94%, nan 6%

NAICS_ICS: N/A 94%, nan 6%

NOI_WDID: N/A 94%, nan 6%

POLLUTANTS_IDENTIFICATION: N/A 94%, nan 6%

ADJACENCY_TO_ESA__Y_N: N/A 94%, nan 6%

GLOBALID: e105a5f5-e327-407f-b770-29516c 8%, ed9244d0-83e9-4a0b-93f4-a7c246 8%, f30f4424-790e-4eb2-83ad-6693b7 8%, 92d7a7ec-2c42-482f-9f7b-6a9a7a 8%, 7f160356-f53a-47b8-87f9-b8a4d9 8%, 52450c5c-514d-47e9-8339-bb8366 8%, 0fab03c9-e46d-4bf7-8670-8a08af 8%, 1bb4f70a-debd-443c-b4e7-43e078 8%, bc5aa62a-95bd-4bd6-ae17-495317 8%, 3c354511-44fc-49ad-9134-30a807 8%, 6a284f56-61ae-4e08-87e9-3175cc 8%, d6ea0b00-a767-4260-9eda-580580 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 33 | 0 | 33 1; 32 1; 31 1; 30 1 |
| FACILITY_ID | category | 2 | 0 | OPEN 31; nan 2 |
| OPERATIONAL_STATUS | empty | 1 | 33 |  |
| NAME | category | 32 | 0 | nan 2; Oak Tree Park and Pool 1; Starlight Ridge Park 1; Flintridge Village Club 1 |
| ADDRESS | category | 32 | 0 | nan 2; 25571 Meandering Trail  L 1; 25702 Crestview  Las Flor 1; 28112 Roanoke Drive Lader 1 |
| CITY | category | 4 | 0 | Ladera Ranch 23; Coto de Caza 6; nan 2; Las Flores 2 |
| ZIP | empty | 1 | 33 |  |
| INSPECTION_DATE | empty | 1 | 33 |  |
| PHONE | empty | 1 | 33 |  |
| PE | empty | 1 | 33 |  |
| PROGRAM_ELEMENT | amount | 32 | 0 | nan 2; 33.591428 1; 33.589117 1; 33.559742 1 |
| GIS_LATITUDE | amount | 32 | 0 | nan 2; -117.62446 1; -117.620458 1; -117.639842 1 |
| GIS_LONGITUDE | empty | 1 | 33 |  |
| EXISTING_DEVELOPMENT | category | 2 | 0 | NO 31; nan 2 |
| MOBILE_BUSINESS | empty | 1 | 33 |  |
| NAICS_ICS | category | 2 | 0 | N/A 31; nan 2 |
| NOI_WDID | category | 2 | 0 | N/A 31; nan 2 |
| POLLUTANTS_IDENTIFICATION | category | 2 | 0 | N/A 31; nan 2 |
| ADJACENCY_TO_ESA__Y_N | category | 2 | 0 | N/A 31; nan 2 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | empty | 1 | 33 |  |
| GLOBALID | category | 33 | 0 | e105a5f5-e327-407f-b770-2 1; ed9244d0-83e9-4a0b-93f4-a 1; f30f4424-790e-4eb2-83ad-6 1; 92d7a7ec-2c42-482f-9f7b-6 1 |
| CREATIONDATE | date | 1 | 0 | 1755810816608 33 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 33 |
| EDITDATE | date | 1 | 0 | 1755810816608 33 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 33 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:15:55.15501 33 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1577fd23-9276-4452-acec-1 33 |
| SRC_SHA256 | who | 1 | 0 | 3220fa53f9380546cf44cbd7e 33 |
