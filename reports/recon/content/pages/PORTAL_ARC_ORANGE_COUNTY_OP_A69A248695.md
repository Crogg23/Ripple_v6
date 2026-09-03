# PORTAL_ARC_ORANGE_COUNTY_OP_A69A248695

rows 10  columns 28  scan 4.5s

roles: amount 3, audit 2, category 6, date 3, empty 6, other 6, who 3

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
| PROGRAM_ELEMENT | 10 | 33.64 | 33.80 | 33.94 | 33.94 | 337.92 |
| GIS_LATITUDE | 10 | -117.88 | -117.84 | -117.66 | -117.66 | -1.2K |

## who

CREATOR by rows
        10  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
      337.92       10 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
        10  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
      337.92       10 rows  vickie.bach@ocpw.ocgov.com_OCPW

SRC_SHA256 by rows
        10  542df8bbde12f250c07e08d3e058b81af0c47afe468d00bbca925fd4ac90d603

SRC_SHA256 by dollars
      337.92       10 rows  542df8bbde12f250c07e08d3e058b81af0c47afe468d00bbca925fd4ac90

## who x when

CREATOR by CREATIONDATE, dollars = PROGRAM_ELEMENT
  vickie.bach@ocpw.ocgov.com_OCPW           2025:337.92

EDITOR by CREATIONDATE, dollars = PROGRAM_ELEMENT
  vickie.bach@ocpw.ocgov.com_OCPW           2025:337.92

## what

OBJECTID: 10 10%, 9 10%, 8 10%, 7 10%, 6 10%, 5 10%, 4 10%, 3 10%, 2 10%, 1 10%

NAME: Action Recycling 10%, John Wayne Airport (Air Side) 10%, Bowerman Power LFG LLC 10%, Frank R. Bowerman Landfill 10%, Brea Power II LLC 10%, Olinda Alpha Landfill 10%, K&A Property Management LLC 10%, R.J. Noble Company 10%, Baker Canyon Green Recycling ( 10%, West Newport Oil Co. 10%

ADDRESS: 1942-45 N. Valencia Ave. Brea  20%, 8642  N Olive Ave Orange  10%, 3160 Airway Ave. Costa Mesa  10%, 11006 Bee Canyon Access Road 10%, 11002 Bee Canyon Access Rd. Ir 10%, 15631 & 15635 E Lincoln Ave. O 10%, 15505 East Lincoln Ave. Orange 10%, 26982 Baker Canyon Rd., Silver 10%, 1080 17th St. Costa Mesa Uninc 10%

CITY: Orange 30%, Costa Mesa 20%, Brea 20%, NA 10%, Irvine 10%, Silverado 10%

PE: Mario Castillo (OCWR) 40%, Jennifer Shook/Jian Peng 20%, Gaby Mendez 714-406-1730 10%, Maria Pope (JWA Staff) 10%, Duc Nguyen 10%, nan 10%

GLOBALID: 79c72152-1c6d-42e2-a8a5-265014 10%, ae619c0a-a9f6-42f9-aacd-cf4e0a 10%, b0a4723e-9376-4a28-be0e-114465 10%, ae23dc08-93ac-46c4-b4b9-d2f886 10%, 228f211b-850a-468f-9ea3-76fce2 10%, 16f9ba16-d81b-4389-9847-0db466 10%, dc1daa31-e0c5-44ef-8d6b-efc6ec 10%, 5f58064a-c632-437f-bdd4-7a43fc 10%, 77cc07ec-a3a3-4e4f-ba00-b89f0f 10%, 173f974d-347a-4200-92b8-37fe18 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 10 | 0 | 10 1; 9 1; 8 1; 7 1 |
| FACILITY_ID | other | 1 | 0 | OPEN 10 |
| OPERATIONAL_STATUS | empty | 1 | 10 |  |
| NAME | category | 10 | 0 | Action Recycling 1; John Wayne Airport (Air S 1; Bowerman Power LFG LLC 1; Frank R. Bowerman Landfil 1 |
| ADDRESS | category | 9 | 0 | 1942-45 N. Valencia Ave.  2; 8642  N Olive Ave Orange  1; 3160 Airway Ave. Costa Me 1; 11006 Bee Canyon Access R 1 |
| CITY | category | 6 | 0 | Orange 3; Costa Mesa 2; Brea 2; NA 1 |
| ZIP | empty | 1 | 10 |  |
| INSPECTION_DATE | empty | 1 | 10 |  |
| PHONE | amount | 8 | 0 | nan 3; 7147329253.0 1; 9492525200.0 1; 7148384000.0 1 |
| PE | category | 6 | 0 | Mario Castillo (OCWR) 4; Jennifer Shook/Jian Peng 2; Gaby Mendez 714-406-1730 1; Maria Pope (JWA Staff) 1 |
| PROGRAM_ELEMENT | amount | 9 | 0 | 33.836058 2; 33.837309 1; 33.677228 1; 33.715714 1 |
| GIS_LATITUDE | amount | 9 | 0 | -117.860388 2; -117.844585 1; -117.870263 1; -117.710535 1 |
| GIS_LONGITUDE | empty | 1 | 10 |  |
| EXISTING_DEVELOPMENT | other | 1 | 0 | NO 10 |
| MOBILE_BUSINESS | empty | 1 | 10 |  |
| NAICS_ICS | other | 1 | 0 | N/A 10 |
| NOI_WDID | other | 1 | 0 | N/A 10 |
| POLLUTANTS_IDENTIFICATION | other | 1 | 0 | N/A 10 |
| ADJACENCY_TO_ESA__Y_N | other | 1 | 0 | N/A 10 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | empty | 1 | 10 |  |
| GLOBALID | category | 10 | 0 | 79c72152-1c6d-42e2-a8a5-2 1; ae619c0a-a9f6-42f9-aacd-c 1; b0a4723e-9376-4a28-be0e-1 1; ae23dc08-93ac-46c4-b4b9-d 1 |
| CREATIONDATE | date | 1 | 0 | 1755810816937 10 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 10 |
| EDITDATE | date | 1 | 0 | 1755810816937 10 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:13:01.45787 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | df3f181d-ddd6-4e93-acb4-c 10 |
| SRC_SHA256 | who | 1 | 0 | 542df8bbde12f250c07e08d3e 10 |
