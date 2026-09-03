# PORTAL_ARC_ORANGE_COUNTY_OP_572F3C6271

rows 10  columns 29  scan 4.6s

roles: amount 3, audit 2, category 9, date 3, empty 3, other 6, who 4

## when

CREATIONDATE
  2025        10  ##############################

EDITDATE
  2025        10  ##############################

INGESTED_AT
  2026        10  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PHONE | 7 | 949.63M | 7.15B | 9.35B | 9.49B | 46.18B |
| GIS_LATITUDE | 10 | 33.64 | 33.80 | 33.94 | 33.94 | 337.92 |
| GIS_LONGITUDE | 10 | -117.88 | -117.84 | -117.66 | -117.66 | -1.2K |

## who

EXISTING_DEVELOPMENT by rows
        10  Industrial

EXISTING_DEVELOPMENT by dollars
      337.92       10 rows  Industrial

CREATOR by rows
        10  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
      337.92       10 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
        10  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
      337.92       10 rows  vickie.bach@ocpw.ocgov.com_OCPW

SRC_SHA256 by rows
        10  dbab7ecf421814bd0e36e1cf64b7969653db6fb8624f4c0d05c936d0b1210f22

SRC_SHA256 by dollars
      337.92       10 rows  dbab7ecf421814bd0e36e1cf64b7969653db6fb8624f4c0d05c936d0b121

## who x when

EXISTING_DEVELOPMENT by CREATIONDATE, dollars = GIS_LATITUDE
  Industrial                                2025:337.92

CREATOR by CREATIONDATE, dollars = GIS_LATITUDE
  vickie.bach@ocpw.ocgov.com_OCPW           2025:337.92

## what

OBJECTID: 10 10%, 9 10%, 8 10%, 7 10%, 6 10%, 5 10%, 4 10%, 3 10%, 2 10%, 1 10%

FACILITY_ID: 8 30I025442 10%, 8 30I005741 10%, 8 30I026433 10%, 8 30I005261 10%, 8 30I024034 10%, 8 30I005259 10%, 8 30I030132 10%, 8 30I002062 10%, 8 30I024641 10%, nan 10%

NAME: Action Recycling 10%, John Wayne Airport (Air Side) 10%, Bowerman Power LFG LLC 10%, Frank R. Bowerman Landfill 10%, Brea Power II LLC 10%, Olinda Alpha Landfill 10%, K&A Property Management LLC 10%, R.J. Noble Company 10%, Baker Canyon Green Recycling ( 10%, West Newport Oil Co. 10%

ADDRESS: 1942-45 N. Valencia Ave. Brea  20%, 8642  N Olive Ave Orange  10%, 3160 Airway Ave. Costa Mesa  10%, 11006 Bee Canyon Access Road 10%, 11002 Bee Canyon Access Rd. Ir 10%, 15631 & 15635 E Lincoln Ave. O 10%, 15505 East Lincoln Ave. Orange 10%, 26982 Baker Canyon Rd., Silver 10%, 1080 17th St. Costa Mesa Uninc 10%

CITY: Orange 30%, Costa Mesa 20%, Brea 20%, NA 10%, Irvine 10%, Silverado 10%

ZIP: 92865.0 30%, 92823.0 20%, 92626.0 10%, nan 10%, 92602.0 10%, 92676.0 10%, 92627.0 10%

PROGRAM_ELEMENT: Mario Castillo (OCWR) 40%, Jennifer Shook/Jian Peng 20%, Gaby Mendez 714-406-1730 10%, Maria Pope (JWA Staff) 10%, Duc Nguyen 10%, nan 10%

GLOBALID: cb499c5b-e52e-49eb-8c50-5dd076 10%, 3dd9e3e5-e351-4466-8eef-d2dc45 10%, d0dcc8c2-fbca-43df-be7f-07a084 10%, 4ad73e45-a866-42cc-b184-b6e4f1 10%, db7f5571-fc62-498e-a8b6-2dbd37 10%, db669b34-b99a-4ce6-9c17-649cd2 10%, c304d147-df99-455c-ba0e-71c885 10%, 8ab16b8f-49a9-4055-aa42-00a1aa 10%, 891587aa-e987-4e24-a10b-5e3e3a 10%, e0f65838-1b12-48d9-8122-1fe4bd 10%

GEOMETRY: {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 10%, {"type": "Point", "coordinates 10%, {"type": "Point", "coordinates 10%, {"type": "Point", "coordinates 10%, {"type": "Point", "coordinates 10%, {"type": "Point", "coordinates 10%, {"type": "Point", "coordinates 10%, {"type": "Point", "coordinates 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 10 | 0 | 10 1; 9 1; 8 1; 7 1 |
| FACILITY_ID | category | 10 | 0 | 8 30I025442 1; 8 30I005741 1; 8 30I026433 1; 8 30I005261 1 |
| OPERATIONAL_STATUS | other | 1 | 0 | OPEN 10 |
| NAME | category | 10 | 0 | Action Recycling 1; John Wayne Airport (Air S 1; Bowerman Power LFG LLC 1; Frank R. Bowerman Landfil 1 |
| ADDRESS | category | 9 | 0 | 1942-45 N. Valencia Ave.  2; 8642  N Olive Ave Orange  1; 3160 Airway Ave. Costa Me 1; 11006 Bee Canyon Access R 1 |
| CITY | category | 6 | 0 | Orange 3; Costa Mesa 2; Brea 2; NA 1 |
| ZIP | category | 7 | 0 | 92865.0 3; 92823.0 2; 92626.0 1; nan 1 |
| INSPECTION_DATE | empty | 1 | 10 |  |
| PHONE | amount | 8 | 0 | nan 3; 7147329253.0 1; 9492525200.0 1; 7148384000.0 1 |
| PE | empty | 1 | 10 |  |
| PROGRAM_ELEMENT | category | 6 | 0 | Mario Castillo (OCWR) 4; Jennifer Shook/Jian Peng 2; Gaby Mendez 714-406-1730 1; Maria Pope (JWA Staff) 1 |
| GIS_LATITUDE | amount | 9 | 0 | 33.836058 2; 33.837309 1; 33.677228 1; 33.715714 1 |
| GIS_LONGITUDE | amount | 9 | 0 | -117.860388 2; -117.844585 1; -117.870263 1; -117.710535 1 |
| EXISTING_DEVELOPMENT | who | 1 | 0 | Industrial 10 |
| MOBILE_BUSINESS | other | 1 | 0 | NO 10 |
| NAICS_ICS | empty | 1 | 10 |  |
| NOI_WDID | other | 1 | 0 | N/A 10 |
| POLLUTANTS_IDENTIFICATION | other | 1 | 0 | N/A 10 |
| ADJACENCY_TO_ESA__Y_N | other | 1 | 0 | N/A 10 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | other | 1 | 0 | N/A 10 |
| GLOBALID | category | 10 | 0 | cb499c5b-e52e-49eb-8c50-5 1; 3dd9e3e5-e351-4466-8eef-d 1; d0dcc8c2-fbca-43df-be7f-0 1; 4ad73e45-a866-42cc-b184-b 1 |
| CREATIONDATE | date | 1 | 0 | 1755810815374 10 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 10 |
| EDITDATE | date | 1 | 0 | 1755810815374 10 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 10 |
| GEOMETRY | category | 9 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:13:07.17073 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1c8bd5cb-b830-4999-af0d-5 10 |
| SRC_SHA256 | who | 1 | 0 | dbab7ecf421814bd0e36e1cf6 10 |
