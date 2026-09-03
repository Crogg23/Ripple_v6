# PORTAL_ARC_ORANGE_COUNTY_OP_62E4574F5E

rows 9  columns 29  scan 3.6s

roles: amount 2, audit 2, category 9, date 3, empty 3, other 6, who 5

## when

CREATIONDATE
  2025         9  ##############################

EDITDATE
  2025         9  ##############################

INGESTED_AT
  2026         9  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GIS_LATITUDE | 9 | 33.46 | 33.51 | 33.54 | 33.54 | 301.57 |
| GIS_LONGITUDE | 9 | -117.74 | -117.61 | -117.57 | -117.57 | -1.1K |

## who

PROGRAM_ELEMENT by rows
         9  Annual

PROGRAM_ELEMENT by dollars
      301.57        9 rows  Annual

EXISTING_DEVELOPMENT by rows
         9  Industrial

EXISTING_DEVELOPMENT by dollars
      301.57        9 rows  Industrial

CREATOR by rows
         9  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
      301.57        9 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
         9  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
      301.57        9 rows  vickie.bach@ocpw.ocgov.com_OCPW

## who x when

PROGRAM_ELEMENT by CREATIONDATE, dollars = GIS_LATITUDE
  Annual                                    2025:301.57

EXISTING_DEVELOPMENT by CREATIONDATE, dollars = GIS_LATITUDE
  Industrial                                2025:301.57

## what

OBJECTID: 9 11%, 8 11%, 7 11%, 6 11%, 5 11%, 4 11%, 3 11%, 2 11%, 1 11%

FACILITY_ID: 9 30I005780 11%, 9 30I024451 11%, 930I015350 11%, 9 000000219 11%, 9 30I005771 11%, 9 30I014449 11%, 9 30I011101 11%, 9 30I014441 11%, 9 30I024079 11%

NAME: SOCWA - Coastal Treatment Plan 11%, Greenstone Materials 11%, Fortistar Methane Group (MM De 11%, Dana Point Shipyard (Industria 11%, Santa Margarita Water District 11%, Tierra Verde Industries (La Pa 11%, Ewles Materials- San Juan Capi 11%, CRR Inc. San Juan Cap 11%, Lapeyre Industrial Sands Inc./ 11%

ADDRESS: 28303 Alicia Pkwy Laguna Nigue 11%, 31507 Ortega Hwy. San Juan Cap 11%, 32250 La Pata Ave. San Juan Ca 11%, 34671 Puerto  Pl. Dana Point H 11%, 28793 Ortega Hwy. San Juan Cap 11%, 31748 La Pata Ave. San Juan Ca 11%, 32501 Ortega Hwy. San Juan Cap 11%, 31641 Ortega Hwy. San Juan Cap 11%, 31302 Ortega Hwy. San Juan Cap 11%

CITY: San Juan Capistrano 67%, Laguna Niguel 11%, nan 11%, Dana Point 11%

ZIP: 92675 67%, 92677 11%, 92650 11%, 92629 11%

PHONE: nan 78%,  949-551-0363 11%, 949-728-0436 11%

GLOBALID: 28cec57e-6630-4a22-9fac-ce447d 11%, 39b9ebd4-23e7-4ef6-9ea0-d2465c 11%, 6314d719-30e9-4119-b5c2-42c2ca 11%, 6f10fc24-5643-4d9d-8ce2-74c0a3 11%, 3667371c-6283-49bb-8cd0-200d9e 11%, f7600444-b807-430c-b760-6c217b 11%, fad0798d-3cde-4c3d-8d25-e963aa 11%, edb8344b-9838-471e-b067-4ee66c 11%, 45c1a53d-2b54-4b76-80ea-7a763e 11%

GEOMETRY: {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 9 | 0 | 9 1; 8 1; 7 1; 6 1 |
| FACILITY_ID | category | 9 | 0 | 9 30I005780 1; 9 30I024451 1; 930I015350 1; 9 000000219 1 |
| OPERATIONAL_STATUS | other | 1 | 0 | OPEN 9 |
| NAME | category | 9 | 0 | SOCWA - Coastal Treatment 1; Greenstone Materials 1; Fortistar Methane Group ( 1; Dana Point Shipyard (Indu 1 |
| ADDRESS | category | 9 | 0 | 28303 Alicia Pkwy Laguna  1; 31507 Ortega Hwy. San Jua 1; 32250 La Pata Ave. San Ju 1; 34671 Puerto  Pl. Dana Po 1 |
| CITY | category | 4 | 0 | San Juan Capistrano 6; Laguna Niguel 1; nan 1; Dana Point 1 |
| ZIP | category | 4 | 0 | 92675 6; 92677 1; 92650 1; 92629 1 |
| INSPECTION_DATE | empty | 1 | 9 |  |
| PHONE | category | 3 | 0 | nan 7;  949-551-0363 1; 949-728-0436 1 |
| PE | empty | 1 | 9 |  |
| PROGRAM_ELEMENT | who | 1 | 0 | Annual 9 |
| GIS_LATITUDE | amount | 9 | 0 | 33.51874 1; 33.513705 1; 33.499253 1; 33.460474 1 |
| GIS_LONGITUDE | amount | 9 | 0 | -117.737012 1; -117.580683 1; -117.618305 1; -117.69049 1 |
| EXISTING_DEVELOPMENT | who | 1 | 0 | Industrial 9 |
| MOBILE_BUSINESS | other | 1 | 0 | NO 9 |
| NAICS_ICS | empty | 1 | 9 |  |
| NOI_WDID | other | 1 | 0 | N/A 9 |
| POLLUTANTS_IDENTIFICATION | other | 1 | 0 | N/A 9 |
| ADJACENCY_TO_ESA__Y_N | other | 1 | 0 | N/A 9 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | other | 1 | 0 | N/A 9 |
| GLOBALID | category | 9 | 0 | 28cec57e-6630-4a22-9fac-c 1; 39b9ebd4-23e7-4ef6-9ea0-d 1; 6314d719-30e9-4119-b5c2-4 1; 6f10fc24-5643-4d9d-8ce2-7 1 |
| CREATIONDATE | date | 1 | 0 | 1755810815186 9 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 9 |
| EDITDATE | date | 1 | 0 | 1755810815186 9 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 9 |
| GEOMETRY | category | 9 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:56.50040 9 |
| SOURCE_RUN_ID | audit | 1 | 0 | 52896331-bfce-44ac-9648-9 9 |
| SRC_SHA256 | who | 1 | 0 | f8a4d182827d44b7a6614ab59 9 |
