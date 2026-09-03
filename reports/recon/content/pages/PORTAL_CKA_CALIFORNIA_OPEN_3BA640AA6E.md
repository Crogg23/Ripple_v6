# PORTAL_CKA_CALIFORNIA_OPEN_3BA640AA6E

rows 8  columns 22  scan 5.0s

roles: amount 2, audit 2, category 3, date 4, empty 6, who 6

## when

EDIT_DATE
  2023         8  ##############################

CREATIONDATE
  2026         8  ##############################

EDITDATE
  2026         8  ##############################

INGESTED_AT
  2026         8  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 8 | 54.1K | 130.4K | 245.8K | 247.9K | 1.15M |
| SHAPE__LENGTH | 8 | 2.1K | 3.6K | 5.4K | 5.4K | 28.8K |

## who

STATUS by rows
         8  Evacuation Order

STATUS by dollars
       1.15M        8 rows  Evacuation Order

CREATOR by rows
         8  CalOES_Scripts

CREATOR by dollars
       1.15M        8 rows  CalOES_Scripts

EDITOR by rows
         8  CalOES_Scripts

EDITOR by dollars
       1.15M        8 rows  CalOES_Scripts

COUNTY_JURISDICTION by rows
         8  TULARE

COUNTY_JURISDICTION by dollars
       1.15M        8 rows  TULARE

## who x when

STATUS by EDIT_DATE, dollars = SHAPE__AREA
  Evacuation Order                          2023:1.15M

CREATOR by EDIT_DATE, dollars = SHAPE__AREA
  CalOES_Scripts                            2023:1.15M

## what

OBJECTID: 1096484 12%, 1096483 12%, 1096482 12%, 1096480 12%, 1096477 12%, 1096476 12%, 1096475 12%, 1096474 12%

ZONE_ID: US-CA-XTU-PVL-E042 12%, US-CA-XTU-PVL-E044 12%, US-CA-XTU-PVL-E030 12%, US-CA-XTU-PVL-E039 12%, US-CA-XTU-PVL-E034 12%, US-CA-XTU-PVL-E036 12%, US-CA-XTU-PVL-E038 12%, US-CA-XTU-PVL-E032 12%

GLOBALID: c9f92c79-2df5-4149-9688-08217a 12%, e7a80553-034f-4feb-96e9-bfbf66 12%, a8bb31e3-a2f5-4d39-9997-41c32d 12%, 69151136-a0df-4bf4-9b7b-acdd24 12%, e720c8cd-3670-4dcf-a330-583f93 12%, 475886a4-ca34-4922-a999-7975e2 12%, b6eab73d-9d6a-48a9-bdac-f46143 12%, 38e3d917-af95-4159-8198-38c1b0 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 8 | 0 | 1096484 1; 1096483 1; 1096482 1; 1096480 1 |
| COUNTY_JURISDICTION | who | 1 | 0 | TULARE 8 |
| CITY | empty | 1 | 8 |  |
| ZONE_NAME | empty | 1 | 8 |  |
| ZONE_ID | category | 8 | 0 | US-CA-XTU-PVL-E042 1; US-CA-XTU-PVL-E044 1; US-CA-XTU-PVL-E030 1; US-CA-XTU-PVL-E039 1 |
| STATUS | who | 1 | 0 | Evacuation Order 8 |
| EVENT_TYPE | empty | 1 | 8 |  |
| CRITICAL_INFO | empty | 1 | 8 |  |
| PUBLIC_INFO | empty | 1 | 8 |  |
| EDIT_DATE | date | 1 | 0 | 9/20/2023 10:33:08 PM 8 |
| STATEWIDE_LAST_UPDATED | empty | 1 | 8 |  |
| NOTES | who | 1 | 0 | Flooding 8 |
| SHAPE__AREA | amount | 8 | 0 | 129003.3515625 1; 247872.79296875 1; 160517.921875 1; 117016.98828125 1 |
| SHAPE__LENGTH | amount | 8 | 0 | 3995.56032957061 1; 4705.18995569115 1; 4876.23447713824 1; 2187.59328112443 1 |
| GLOBALID | category | 8 | 0 | c9f92c79-2df5-4149-9688-0 1; e7a80553-034f-4feb-96e9-b 1; a8bb31e3-a2f5-4d39-9997-4 1; 69151136-a0df-4bf4-9b7b-a 1 |
| CREATIONDATE | date | 1 | 0 | 5/18/2026 9:42:07 PM 8 |
| CREATOR | who | 1 | 0 | CalOES_Scripts 8 |
| EDITDATE | date | 1 | 0 | 7/2/2026 9:09:13 AM 8 |
| EDITOR | who | 1 | 0 | CalOES_Scripts 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:11:47.34770 8 |
| SOURCE_RUN_ID | audit | 1 | 0 | b690af90-ada9-497e-a0da-2 8 |
| SRC_SHA256 | who | 1 | 0 | f859f75f0d9b79917c7b339d3 8 |
