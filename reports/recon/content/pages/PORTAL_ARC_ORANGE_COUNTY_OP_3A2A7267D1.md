# PORTAL_ARC_ORANGE_COUNTY_OP_3A2A7267D1

rows 33  columns 29  scan 3.2s

roles: amount 2, audit 2, category 14, date 3, empty 6, who 3

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
| GIS_LATITUDE | 31 | 33.54 | 33.56 | 33.63 | 33.63 | 1.0K |
| GIS_LONGITUDE | 31 | -117.65 | -117.64 | -117.58 | -117.58 | -3.6K |

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
        33  babb3ea644dd273081ac8d93aa8a4f4bd45edfc5db7c6bb862b9045ab2d3283a

SRC_SHA256 by dollars
        1.0K       33 rows  babb3ea644dd273081ac8d93aa8a4f4bd45edfc5db7c6bb862b9045ab2d3

## who x when

CREATOR by CREATIONDATE, dollars = GIS_LATITUDE
  vickie.bach@ocpw.ocgov.com_OCPW           2025:1.0K

EDITOR by CREATIONDATE, dollars = GIS_LATITUDE
  vickie.bach@ocpw.ocgov.com_OCPW           2025:1.0K

## what

OBJECTID: 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%

OPERATIONAL_STATUS: OPEN 94%, nan 6%

NAME: nan 15%, Oak Tree Park and Pool 8%, Starlight Ridge Park 8%, Flintridge Village Club 8%, Chapparal Park 8%, Township Plunge 8%, Town Green 8%, Oak Knoll Village Club 8%, Hilltop Park 8%, Celestial Plunge 8%, Poets Park 8%, Boreal Plunge 8%

ADDRESS: nan 15%, 25571 Meandering Trail  Las Fl 8%, 25702 Crestview  Las Flores  8%, 28112 Roanoke Drive Ladera Ran 8%, 29075 Sienna Pkwy. Ladera Ranc 8%, 28532 Second Street Ladera Ran 8%, 28801 Sienna Pkwy. Ladera Ranc 8%, 28192 O'neill Pkwy. Ladera Ran 8%, 1 Wickford Lane Ladera Ranch  8%, 29145 Ethereal Street Ladera R 8%, 28741 Tuberose Street Ladera R 8%, 27642 Gaia Lane Ladera Ranch  8%

CITY: Ladera Ranch 70%, Coto de Caza 18%, nan 6%, Las Flores 6%

ZIP: 92694.0 70%, 92679.0 18%, nan 6%, 92688.0 6%

EXISTING_DEVELOPMENT: Commercial 94%, nan 6%

MOBILE_BUSINESS: NO 94%, nan 6%

NOI_WDID: N/A 94%, nan 6%

POLLUTANTS_IDENTIFICATION: N/A 94%, nan 6%

ADJACENCY_TO_ESA__Y_N: N/A 94%, nan 6%

WATER_BODY_SEGMENT_IMPAIRED__Y: N/A 94%, nan 6%

GLOBALID: 54c457a9-0af3-443e-8723-be28c6 8%, 6dd2cf4c-6e53-40ed-a03d-c42776 8%, 9637ce3c-0856-463e-9f24-776f38 8%, 99e42c48-f176-450f-9d08-9e4c8c 8%, f7d4a0a2-65ff-460e-b4e3-e965d5 8%, fab7927f-c9fe-4d17-ab6e-a667b4 8%, 9094c5cb-8177-4653-9bd6-8b881e 8%, fb5f5dcd-4758-4913-810c-6ec067 8%, ea2b19c0-94b4-4f44-9825-667ceb 8%, 0513e909-5758-4ee8-aa08-19584c 8%, 47f02ec2-b1c3-4b59-8da9-588ff5 8%, 15834acc-7b1b-4680-9c2f-0e0124 8%

GEOMETRY: nan 15%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 33 | 0 | 33 1; 32 1; 31 1; 30 1 |
| FACILITY_ID | empty | 1 | 33 |  |
| OPERATIONAL_STATUS | category | 2 | 0 | OPEN 31; nan 2 |
| NAME | category | 32 | 0 | nan 2; Oak Tree Park and Pool 1; Starlight Ridge Park 1; Flintridge Village Club 1 |
| ADDRESS | category | 32 | 0 | nan 2; 25571 Meandering Trail  L 1; 25702 Crestview  Las Flor 1; 28112 Roanoke Drive Lader 1 |
| CITY | category | 4 | 0 | Ladera Ranch 23; Coto de Caza 6; nan 2; Las Flores 2 |
| ZIP | category | 4 | 0 | 92694.0 23; 92679.0 6; nan 2; 92688.0 2 |
| INSPECTION_DATE | empty | 1 | 33 |  |
| PHONE | empty | 1 | 33 |  |
| PE | empty | 1 | 33 |  |
| PROGRAM_ELEMENT | empty | 1 | 33 |  |
| GIS_LATITUDE | amount | 32 | 0 | nan 2; 33.591428 1; 33.589117 1; 33.559742 1 |
| GIS_LONGITUDE | amount | 32 | 0 | nan 2; -117.62446 1; -117.620458 1; -117.639842 1 |
| EXISTING_DEVELOPMENT | category | 2 | 0 | Commercial 31; nan 2 |
| MOBILE_BUSINESS | category | 2 | 0 | NO 31; nan 2 |
| NAICS_ICS | empty | 1 | 33 |  |
| NOI_WDID | category | 2 | 0 | N/A 31; nan 2 |
| POLLUTANTS_IDENTIFICATION | category | 2 | 0 | N/A 31; nan 2 |
| ADJACENCY_TO_ESA__Y_N | category | 2 | 0 | N/A 31; nan 2 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | category | 2 | 0 | N/A 31; nan 2 |
| GLOBALID | category | 31 | 0 | 54c457a9-0af3-443e-8723-b 1; 6dd2cf4c-6e53-40ed-a03d-c 1; 9637ce3c-0856-463e-9f24-7 1; 99e42c48-f176-450f-9d08-9 1 |
| CREATIONDATE | date | 1 | 0 | 1755810814576 33 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 33 |
| EDITDATE | date | 1 | 0 | 1755810814576 33 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 33 |
| GEOMETRY | category | 32 | 0 | nan 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:15:50.18115 33 |
| SOURCE_RUN_ID | audit | 1 | 0 | adf1e83c-ffe1-4635-95bf-e 33 |
| SRC_SHA256 | who | 1 | 0 | babb3ea644dd273081ac8d93a 33 |
