# PORTAL_ARC_ORANGE_COUNTY_OP_1A50E60D53

rows 13  columns 28  scan 3.5s

roles: amount 3, audit 2, category 7, date 3, empty 7, other 4, who 3

## when

CREATIONDATE
  2025        13  ##############################

EDITDATE
  2025        13  ##############################

INGESTED_AT
  2026        13  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PHONE | 10 | 3.23B | 9.50B | 9.50B | 9.50B | 85.08B |
| PROGRAM_ELEMENT | 11 | 33.53 | 33.63 | 33.69 | 33.69 | 369.85 |
| GIS_LATITUDE | 11 | -117.81 | -117.62 | -117.55 | -117.55 | -1.3K |

## who

CREATOR by rows
        13  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
      369.85       13 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
        13  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
      369.85       13 rows  vickie.bach@ocpw.ocgov.com_OCPW

SRC_SHA256 by rows
        13  e5bd285ad8e2ba144da607b105b2551d27e7d3fc34ee7394a2386d4ec1f46c6b

SRC_SHA256 by dollars
      369.85       13 rows  e5bd285ad8e2ba144da607b105b2551d27e7d3fc34ee7394a2386d4ec1f4

## who x when

CREATOR by CREATIONDATE, dollars = PROGRAM_ELEMENT
  vickie.bach@ocpw.ocgov.com_OCPW           2025:369.85

EDITOR by CREATIONDATE, dollars = PROGRAM_ELEMENT
  vickie.bach@ocpw.ocgov.com_OCPW           2025:369.85

## what

OBJECTID: 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%

FACILITY_ID: OPEN 77%, nan 15%, UNKNOWN 8%

NAME: nan 15%, Live Oak Canyon Stables  8%, TY Nursery 8%, Sakaida Nursery 8%, Rancho Las Lomas Wedding Cente 8%, Tree of Life Nursery 8%, Las Flores Hand Wash 8%, Santiago Ranch Stables (Lease  8%, Lake Forest Golf & Practice Ce 8%, Emerald Canyon Park 8%, Emerald Bay Community Center 8%, Cinnabar Equestrian Operations 8%

ADDRESS: nan 15%, 600 Emerald Bay  Laguna Beach  15%, 31101 Live Oak Canyon Road Tra 8%, 31761 Trabuco Canyon Rd. Trabu 8%, 31971 Trabuco Canyon Rd. Trabu 8%, 19191 Lawrence Canyon Road San 8%, 33201 Ortega Hwy. San Juan Cap 8%, 28622 Oso Pkwy. Las Flores  8%, 18381 Santiago Canyon Rd. Lake 8%, 23308 Cherry Avenue Lake Fores 8%, 23401 Via Pajaro  Coto de Caza 8%

CITY: Trabuco Canyon 23%, nan 15%, Lake Forest 15%, Laguna Beach 15%, Santiago Canyon 8%, San Juan Capistrano 8%, Las Flores 8%, Coto de Caza 8%

EXISTING_DEVELOPMENT: NO 85%, nan 15%

GLOBALID: 71311754-fe8f-4336-9f6f-2e7a95 8%, 0a0cf836-6c90-46ce-a142-10732b 8%, 7640ae58-3b06-4c84-bc96-6a1c57 8%, f5ddb8a1-a1bb-4998-a8ed-582bc0 8%, 1517ae99-5744-4b18-a8e9-19de22 8%, 2a3602e0-a8cf-4516-9d48-52fb7e 8%, ef9fbfa5-416f-4bec-b555-cb98b8 8%, 314f7aed-68f4-4324-9723-71c8e4 8%, 4ccd30a2-e2d8-447c-be8f-41a69e 8%, 821313a9-dfc1-4e7f-bac6-75b203 8%, 6cd5d28d-69a3-4496-a840-f3f20e 8%, ce49f6f1-647b-4784-858d-2822a7 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 13 | 0 | 13 1; 12 1; 11 1; 10 1 |
| FACILITY_ID | category | 3 | 0 | OPEN 10; nan 2; UNKNOWN 1 |
| OPERATIONAL_STATUS | empty | 1 | 13 |  |
| NAME | category | 12 | 0 | nan 2; Live Oak Canyon Stables  1; TY Nursery 1; Sakaida Nursery 1 |
| ADDRESS | category | 11 | 0 | nan 2; 600 Emerald Bay  Laguna B 2; 31101 Live Oak Canyon Roa 1; 31761 Trabuco Canyon Rd.  1 |
| CITY | category | 8 | 0 | Trabuco Canyon 3; nan 2; Lake Forest 2; Laguna Beach 2 |
| ZIP | empty | 1 | 13 |  |
| INSPECTION_DATE | empty | 1 | 13 |  |
| PHONE | amount | 11 | 0 | nan 3; 9097958733.0 1; 9498580202.0 1; 6262859981.0 1 |
| PE | empty | 1 | 13 |  |
| PROGRAM_ELEMENT | amount | 11 | 0 | nan 2; 33.554762 2; 33.686825 1; 33.658005 1 |
| GIS_LATITUDE | amount | 11 | 0 | nan 2; -117.806579 2; -117.614002 1; -117.57288 1 |
| GIS_LONGITUDE | empty | 1 | 13 |  |
| EXISTING_DEVELOPMENT | category | 2 | 0 | NO 11; nan 2 |
| MOBILE_BUSINESS | empty | 1 | 13 |  |
| NAICS_ICS | other | 1 | 0 | N/A 13 |
| NOI_WDID | other | 1 | 0 | N/A 13 |
| POLLUTANTS_IDENTIFICATION | other | 1 | 0 | N/A 13 |
| ADJACENCY_TO_ESA__Y_N | other | 1 | 0 | N/A 13 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | empty | 1 | 13 |  |
| GLOBALID | category | 13 | 0 | 71311754-fe8f-4336-9f6f-2 1; 0a0cf836-6c90-46ce-a142-1 1; 7640ae58-3b06-4c84-bc96-6 1; f5ddb8a1-a1bb-4998-a8ed-5 1 |
| CREATIONDATE | date | 1 | 0 | 1755810816312 13 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 13 |
| EDITDATE | date | 1 | 0 | 1755810816312 13 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:13:53.86906 13 |
| SOURCE_RUN_ID | audit | 1 | 0 | cf9739e9-6ea1-42d4-8a33-5 13 |
| SRC_SHA256 | who | 1 | 0 | e5bd285ad8e2ba144da607b10 13 |
