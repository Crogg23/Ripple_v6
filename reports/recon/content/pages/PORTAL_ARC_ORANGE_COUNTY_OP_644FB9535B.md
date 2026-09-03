# PORTAL_ARC_ORANGE_COUNTY_OP_644FB9535B

rows 9  columns 28  scan 3.1s

roles: amount 2, audit 2, category 6, date 3, empty 6, other 6, who 4

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
| PROGRAM_ELEMENT | 9 | 33.46 | 33.51 | 33.54 | 33.54 | 301.57 |
| GIS_LATITUDE | 9 | -117.74 | -117.61 | -117.57 | -117.57 | -1.1K |

## who

PE by rows
         9  Annual

PE by dollars
      301.57        9 rows  Annual

CREATOR by rows
         9  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
      301.57        9 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
         9  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
      301.57        9 rows  vickie.bach@ocpw.ocgov.com_OCPW

SRC_SHA256 by rows
         9  b48ad2f52409303c17f1351da67ef33fe3522d2b573d68edcea7537743af494c

SRC_SHA256 by dollars
      301.57        9 rows  b48ad2f52409303c17f1351da67ef33fe3522d2b573d68edcea7537743af

## who x when

PE by CREATIONDATE, dollars = PROGRAM_ELEMENT
  Annual                                    2025:301.57

CREATOR by CREATIONDATE, dollars = PROGRAM_ELEMENT
  vickie.bach@ocpw.ocgov.com_OCPW           2025:301.57

## what

OBJECTID: 9 11%, 8 11%, 7 11%, 6 11%, 5 11%, 4 11%, 3 11%, 2 11%, 1 11%

NAME: SOCWA - Coastal Treatment Plan 11%, Greenstone Materials 11%, Fortistar Methane Group (MM De 11%, Dana Point Shipyard (Industria 11%, Santa Margarita Water District 11%, Tierra Verde Industries (La Pa 11%, Ewles Materials- San Juan Capi 11%, CRR Inc. San Juan Cap 11%, Lapeyre Industrial Sands Inc./ 11%

ADDRESS: 28303 Alicia Pkwy Laguna Nigue 11%, 31507 Ortega Hwy. San Juan Cap 11%, 32250 La Pata Ave. San Juan Ca 11%, 34671 Puerto  Pl. Dana Point H 11%, 28793 Ortega Hwy. San Juan Cap 11%, 31748 La Pata Ave. San Juan Ca 11%, 32501 Ortega Hwy. San Juan Cap 11%, 31641 Ortega Hwy. San Juan Cap 11%, 31302 Ortega Hwy. San Juan Cap 11%

CITY: San Juan Capistrano 67%, Laguna Niguel 11%, nan 11%, Dana Point 11%

PHONE: nan 78%,  949-551-0363 11%, 949-728-0436 11%

GLOBALID: 234e1104-6ef0-406e-b7a8-cedcef 11%, 83507b18-f816-432e-8d40-9850d2 11%, 0814d180-2a88-4517-a980-b0915d 11%, fbd5ea1c-f099-4248-91e4-7704ce 11%, 679ef4f7-9b99-4b28-94d6-422e50 11%, a5631d7b-2339-49fb-9375-14a241 11%, 10fbcb86-73e2-4ba9-ad19-aefe07 11%, fd55137c-62bc-41c3-a537-21a2eb 11%, 4ce0639d-67a1-451d-906c-d3925f 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 9 | 0 | 9 1; 8 1; 7 1; 6 1 |
| FACILITY_ID | other | 1 | 0 | OPEN 9 |
| OPERATIONAL_STATUS | empty | 1 | 9 |  |
| NAME | category | 9 | 0 | SOCWA - Coastal Treatment 1; Greenstone Materials 1; Fortistar Methane Group ( 1; Dana Point Shipyard (Indu 1 |
| ADDRESS | category | 9 | 0 | 28303 Alicia Pkwy Laguna  1; 31507 Ortega Hwy. San Jua 1; 32250 La Pata Ave. San Ju 1; 34671 Puerto  Pl. Dana Po 1 |
| CITY | category | 4 | 0 | San Juan Capistrano 6; Laguna Niguel 1; nan 1; Dana Point 1 |
| ZIP | empty | 1 | 9 |  |
| INSPECTION_DATE | empty | 1 | 9 |  |
| PHONE | category | 3 | 0 | nan 7;  949-551-0363 1; 949-728-0436 1 |
| PE | who | 1 | 0 | Annual 9 |
| PROGRAM_ELEMENT | amount | 9 | 0 | 33.51874 1; 33.513705 1; 33.499253 1; 33.460474 1 |
| GIS_LATITUDE | amount | 9 | 0 | -117.737012 1; -117.580683 1; -117.618305 1; -117.69049 1 |
| GIS_LONGITUDE | empty | 1 | 9 |  |
| EXISTING_DEVELOPMENT | other | 1 | 0 | NO 9 |
| MOBILE_BUSINESS | empty | 1 | 9 |  |
| NAICS_ICS | other | 1 | 0 | N/A 9 |
| NOI_WDID | other | 1 | 0 | N/A 9 |
| POLLUTANTS_IDENTIFICATION | other | 1 | 0 | N/A 9 |
| ADJACENCY_TO_ESA__Y_N | other | 1 | 0 | N/A 9 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | empty | 1 | 9 |  |
| GLOBALID | category | 9 | 0 | 234e1104-6ef0-406e-b7a8-c 1; 83507b18-f816-432e-8d40-9 1; 0814d180-2a88-4517-a980-b 1; fbd5ea1c-f099-4248-91e4-7 1 |
| CREATIONDATE | date | 1 | 0 | 1755810816765 9 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 9 |
| EDITDATE | date | 1 | 0 | 1755810816765 9 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:12:51.21459 9 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2e31eb8e-8e5e-4162-b2a0-a 9 |
| SRC_SHA256 | who | 1 | 0 | b48ad2f52409303c17f1351da 9 |
