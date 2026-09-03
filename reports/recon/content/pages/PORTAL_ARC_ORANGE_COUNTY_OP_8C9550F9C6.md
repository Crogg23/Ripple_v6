# PORTAL_ARC_ORANGE_COUNTY_OP_8C9550F9C6

rows 13  columns 29  scan 3.3s

roles: amount 3, audit 2, category 10, date 3, empty 5, other 4, who 3

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
| GIS_LATITUDE | 11 | 33.53 | 33.63 | 33.69 | 33.69 | 369.85 |
| GIS_LONGITUDE | 11 | -117.81 | -117.62 | -117.55 | -117.55 | -1.3K |

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
        13  09c26080ea4f7a6032160c27a4dea9d8cfbf5e6d3fd5eaefe3537800b474be88

SRC_SHA256 by dollars
      369.85       13 rows  09c26080ea4f7a6032160c27a4dea9d8cfbf5e6d3fd5eaefe3537800b474

## who x when

CREATOR by CREATIONDATE, dollars = GIS_LATITUDE
  vickie.bach@ocpw.ocgov.com_OCPW           2025:369.85

EDITOR by CREATIONDATE, dollars = GIS_LATITUDE
  vickie.bach@ocpw.ocgov.com_OCPW           2025:369.85

## what

OBJECTID: 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%

OPERATIONAL_STATUS: OPEN 77%, nan 15%, UNKNOWN 8%

NAME: nan 15%, Live Oak Canyon Stables  8%, TY Nursery 8%, Sakaida Nursery 8%, Rancho Las Lomas Wedding Cente 8%, Tree of Life Nursery 8%, Las Flores Hand Wash 8%, Santiago Ranch Stables (Lease  8%, Lake Forest Golf & Practice Ce 8%, Emerald Canyon Park 8%, Emerald Bay Community Center 8%, Cinnabar Equestrian Operations 8%

ADDRESS: nan 15%, 600 Emerald Bay  Laguna Beach  15%, 31101 Live Oak Canyon Road Tra 8%, 31761 Trabuco Canyon Rd. Trabu 8%, 31971 Trabuco Canyon Rd. Trabu 8%, 19191 Lawrence Canyon Road San 8%, 33201 Ortega Hwy. San Juan Cap 8%, 28622 Oso Pkwy. Las Flores  8%, 18381 Santiago Canyon Rd. Lake 8%, 23308 Cherry Avenue Lake Fores 8%, 23401 Via Pajaro  Coto de Caza 8%

CITY: Trabuco Canyon 23%, nan 15%, Lake Forest 15%, Laguna Beach 15%, Santiago Canyon 8%, San Juan Capistrano 8%, Las Flores 8%, Coto de Caza 8%

ZIP: nan 15%, 92679.0 15%, 92678.0 15%, 92676.0 15%, 92651.0 15%, 92675.0 8%, 92688.0 8%, 92630.0 8%

EXISTING_DEVELOPMENT: Commercial 85%, nan 15%

MOBILE_BUSINESS: NO 85%, nan 15%

GLOBALID: 1ee4670e-8104-4499-9b53-e8ef56 8%, f4fbaefd-35b3-408a-b4e7-a0e16a 8%, 9fc6353f-9e74-4bb0-93d8-cb1108 8%, 96449f8e-4c45-42d0-a00a-cf3d64 8%, c7802550-898c-4415-8f08-9977d7 8%, eabcf5ba-2f81-4ef8-ba6a-11afff 8%, 3ec34c07-1b6c-4051-897e-eb313c 8%, d5d48dbb-6ad5-4db2-b658-ca8ce4 8%, 06018f24-a84a-4653-b09c-21435f 8%, 50c4bada-a7d1-414f-8f01-b5c143 8%, 5b3bd90c-2553-4c26-a0a4-14a2ec 8%, 41fc5090-7620-4793-92a1-07d987 8%

GEOMETRY: nan 15%, {"type": "Point", "coordinates 15%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 13 | 0 | 13 1; 12 1; 11 1; 10 1 |
| FACILITY_ID | empty | 1 | 13 |  |
| OPERATIONAL_STATUS | category | 3 | 0 | OPEN 10; nan 2; UNKNOWN 1 |
| NAME | category | 12 | 0 | nan 2; Live Oak Canyon Stables  1; TY Nursery 1; Sakaida Nursery 1 |
| ADDRESS | category | 11 | 0 | nan 2; 600 Emerald Bay  Laguna B 2; 31101 Live Oak Canyon Roa 1; 31761 Trabuco Canyon Rd.  1 |
| CITY | category | 8 | 0 | Trabuco Canyon 3; nan 2; Lake Forest 2; Laguna Beach 2 |
| ZIP | category | 8 | 0 | nan 2; 92679.0 2; 92678.0 2; 92676.0 2 |
| INSPECTION_DATE | empty | 1 | 13 |  |
| PHONE | amount | 11 | 0 | nan 3; 9097958733.0 1; 9498580202.0 1; 6262859981.0 1 |
| PE | empty | 1 | 13 |  |
| PROGRAM_ELEMENT | empty | 1 | 13 |  |
| GIS_LATITUDE | amount | 11 | 0 | nan 2; 33.554762 2; 33.686825 1; 33.658005 1 |
| GIS_LONGITUDE | amount | 11 | 0 | nan 2; -117.806579 2; -117.614002 1; -117.57288 1 |
| EXISTING_DEVELOPMENT | category | 2 | 0 | Commercial 11; nan 2 |
| MOBILE_BUSINESS | category | 2 | 0 | NO 11; nan 2 |
| NAICS_ICS | empty | 1 | 13 |  |
| NOI_WDID | other | 1 | 0 | N/A 13 |
| POLLUTANTS_IDENTIFICATION | other | 1 | 0 | N/A 13 |
| ADJACENCY_TO_ESA__Y_N | other | 1 | 0 | N/A 13 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | other | 1 | 0 | N/A 13 |
| GLOBALID | category | 12 | 0 | 1ee4670e-8104-4499-9b53-e 1; f4fbaefd-35b3-408a-b4e7-a 1; 9fc6353f-9e74-4bb0-93d8-c 1; 96449f8e-4c45-42d0-a00a-c 1 |
| CREATIONDATE | date | 1 | 0 | 1755810814795 13 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 13 |
| EDITDATE | date | 1 | 0 | 1755810814795 13 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 13 |
| GEOMETRY | category | 11 | 0 | nan 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:13:29.91541 13 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1324208b-9736-41ac-b7d9-f 13 |
| SRC_SHA256 | who | 1 | 0 | 09c26080ea4f7a6032160c27a 13 |
