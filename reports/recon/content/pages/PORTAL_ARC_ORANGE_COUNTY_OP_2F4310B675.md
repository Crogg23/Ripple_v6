# PORTAL_ARC_ORANGE_COUNTY_OP_2F4310B675

rows 31  columns 29  scan 4.7s

roles: amount 2, audit 2, category 11, date 3, empty 2, other 6, who 4

## when

CREATIONDATE
  2025        31  ##############################

EDITDATE
  2025        31  ##############################

INGESTED_AT
  2026        31  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GIS_LATITUDE | 31 | 33.66 | 33.79 | 33.87 | 33.88 | 1.0K |
| GIS_LONGITUDE | 31 | -118.07 | -117.89 | 47.36 | 118.07 | -3.4K |

## who

EXISTING_DEVELOPMENT by rows
        31  Commercial Facilities

EXISTING_DEVELOPMENT by dollars
        1.0K       31 rows  Commercial Facilities

CREATOR by rows
        31  vickie.bach@ocpw.ocgov.com_OCPW

CREATOR by dollars
        1.0K       31 rows  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by rows
        31  vickie.bach@ocpw.ocgov.com_OCPW

EDITOR by dollars
        1.0K       31 rows  vickie.bach@ocpw.ocgov.com_OCPW

SRC_SHA256 by rows
        31  380928c4f885ba30f08eca26c11257f90d8c1e7d02a8b3becb2d39077d7b6791

SRC_SHA256 by dollars
        1.0K       31 rows  380928c4f885ba30f08eca26c11257f90d8c1e7d02a8b3becb2d39077d7b

## who x when

EXISTING_DEVELOPMENT by CREATIONDATE, dollars = GIS_LATITUDE
  Commercial Facilities                     2025:1.0K

CREATOR by CREATIONDATE, dollars = GIS_LATITUDE
  vickie.bach@ocpw.ocgov.com_OCPW           2025:1.0K

## what

OBJECTID: 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%

FACILITY_ID: FA0042587 8%, FA0014379 8%, FA0007503 8%, FA0004228 8%, FA0002929 8%, FA0070323 8%, FA0021189 8%, FA0013952 8%, FA0052604 8%, FA0009978 8%, FA0009432 8%, FA0008221 8%

NAME: FUEL UP! 8%, CANYON INN 8%, YORBA LINDA COUNTRY CLUB 8%, KENNYS DONUT 8%, DEL TACO #711 8%, SMRPD 8%, SILVERADO CANYON MARKET AND KI 8%, SILVER CAFE 8%, TJ MAXX #1048 8%, TACO BELL #3111^ 8%, SANTA ANA COUNTRY CLUB^ 8%, ORANGE COUNTY MINING CO^ 8%

ADDRESS: 19851 ESPERANZA RD  8%, 6821 FAIRLYNN BLVD 8%, 19400 MOUNTAIN VIEW  8%, 6821 FAIRLYNN BLVD  8%, 19701 ESPERANZA RD  8%, 27641 SILVERADO CANYON RD 8%, 28192 SILVERADO CANYON RD STE  8%, 28272 SILVERADO CANYON RD  8%, 3900 S BRISTOL AVE  8%, 16252 S HARBOR BLVD  8%, 20382 NEWPORT BLVD  8%, 10000 CRAWFORD CANYON RD  8%

CITY: LOS ALAMITOS 23%, YORBA LINDA 16%, ORANGE 16%, MIDWAY CITY 16%, SANTA ANA 13%, SILVERADO  10%, COSTA MESA 6%

ZIP: 90720 23%, 92655 16%, 92886 13%, 92869 13%, 92676 10%, 92627 6%, 92686 3%, 92661 3%, 92704 3%, 92707 3%, 92705 3%, 92862 3%

PHONE: 7147773145 8%, 7147790880 8%, 7147792461 8%, 7147775044 8%, 7147798208 8%, 9492801736 8%, 7142222607 8%, 7146492622 8%, 7146411362 8%, 7145316878 8%, 7145563000 8%, 7149977411 8%

PE: 0136 19%, 0112 12%, 0391 12%, 0312 8%, 0133 8%, 0111 8%, 0132 8%, 0131 8%, 0392 8%, 0261 4%, 0315 4%, 0311 4%

PROGRAM_ELEMENT: RESTAURANT 201+ PERSONS - COMP 19%, RESTAURANT 31-60 PERSONS - NON 12%, FOOD MARKET - PACKAGED FOOD 1- 12%, FOOD MARKET NON-COMPLEX 2000-5 8%, RESTAURANT 61-100 PERSONS - CO 8%, RESTAURANT UNDER 31 PERSONS -  8%, RESTAURANT 31-60 PERSONS - COM 8%, RESTAURANT UNDER 31 PERSONS -  8%, FOOD MARKET - PACKAGED FOOD 20 8%, SENIOR FEEDING NUTRITION SITE 4%, FOOD MARKET W/ 1 PREP AREA 200 4%, FOOD MARKET NON-COMPLEX UNDER  4%

GLOBALID: 82c6a745-099f-4476-a22c-458d7b 8%, b2e45a22-bab9-4afd-b071-2aa431 8%, b8908bac-49af-43ab-ad23-50584d 8%, 45b8f5a3-ecc7-4aeb-a14d-7fe408 8%, e13ea27f-15cd-4216-a426-05bcb1 8%, edebd53c-e2e0-49dd-9f1a-e1cb35 8%, 10143c03-bcfc-4d1e-92b4-c2ce28 8%, 98e4ab95-a670-457b-bcfc-feb0cc 8%, 1142cff8-f1ed-4c01-bb14-3f4d4d 8%, b2cc0dda-69fa-4141-8e10-f0dc77 8%, 6d2833ae-8e57-4cea-a4ea-b575f4 8%, cc302917-c3c4-42e7-bf5f-d558b0 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 31 | 0 | 31 1; 30 1; 29 1; 28 1 |
| FACILITY_ID | category | 31 | 1 | FA0042587 1; FA0014379 1; FA0007503 1; FA0004228 1 |
| OPERATIONAL_STATUS | other | 1 | 0 | OPEN 31 |
| NAME | category | 31 | 0 | FUEL UP! 1; CANYON INN 1; YORBA LINDA COUNTRY CLUB 1; KENNYS DONUT 1 |
| ADDRESS | category | 31 | 0 | 19851 ESPERANZA RD  1; 6821 FAIRLYNN BLVD 1; 19400 MOUNTAIN VIEW  1; 6821 FAIRLYNN BLVD  1 |
| CITY | category | 7 | 0 | LOS ALAMITOS 7; YORBA LINDA 5; ORANGE 5; MIDWAY CITY 5 |
| ZIP | category | 12 | 0 | 90720 7; 92655 5; 92886 4; 92869 4 |
| INSPECTION_DATE | other | 1 | 0 | N/A 31 |
| PHONE | category | 31 | 0 | 7147773145 1; 7147790880 1; 7147792461 1; 7147775044 1 |
| PE | category | 17 | 1 | 0136 5; 0112 3; 0391 3; 0312 2 |
| PROGRAM_ELEMENT | category | 17 | 1 | RESTAURANT 201+ PERSONS - 5; RESTAURANT 31-60 PERSONS  3; FOOD MARKET - PACKAGED FO 3; FOOD MARKET NON-COMPLEX 2 2 |
| GIS_LATITUDE | amount | 31 | 0 | 33.86306 1; 33.86345 1; 33.877163 1; 33.863648 1 |
| GIS_LONGITUDE | amount | 30 | 0 | -117.885461 2; -117.786508285133 1; -117.78678570584 1; -117.795628 1 |
| EXISTING_DEVELOPMENT | who | 1 | 0 | Commercial Facilities 31 |
| MOBILE_BUSINESS | other | 1 | 0 | NO 31 |
| NAICS_ICS | empty | 1 | 31 |  |
| NOI_WDID | other | 1 | 0 | N/A 31 |
| POLLUTANTS_IDENTIFICATION | empty | 1 | 31 |  |
| ADJACENCY_TO_ESA__Y_N | other | 1 | 0 | N/A 31 |
| WATER_BODY_SEGMENT_IMPAIRED__Y | other | 1 | 0 | N/A 31 |
| GLOBALID | category | 30 | 0 | 82c6a745-099f-4476-a22c-4 1; b2e45a22-bab9-4afd-b071-2 1; b8908bac-49af-43ab-ad23-5 1; 45b8f5a3-ecc7-4aeb-a14d-7 1 |
| CREATIONDATE | date | 1 | 0 | 1755810815796 31 |
| CREATOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 31 |
| EDITDATE | date | 1 | 0 | 1755810815796 31 |
| EDITOR | who | 1 | 0 | vickie.bach@ocpw.ocgov.co 31 |
| GEOMETRY | category | 30 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:15:32.20280 31 |
| SOURCE_RUN_ID | audit | 1 | 0 | 88d76345-c2c5-4e22-94b1-a 31 |
| SRC_SHA256 | who | 1 | 0 | 380928c4f885ba30f08eca26c 31 |
