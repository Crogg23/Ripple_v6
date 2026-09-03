# PORTAL_CKA_SAN_JOSE_OPEN_DA_876760587A

rows 8  columns 15  scan 3.1s

roles: amount 2, audit 2, category 7, date 1, empty 2, who 2

## when

INGESTED_AT
  2026         8  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 8 | 7.5K | 236.8K | 732.6K | 755.8K | 2.12M |
| SHAPE_AREA | 8 | 1.28M | 595.30M | 1.55B | 1.58B | 5.04B |

## who

DISTRICTCLASS by rows
         8  Operations

DISTRICTCLASS by dollars
       2.12M        8 rows  Operations

SRC_SHA256 by rows
         8  f027c596587588a98dbc49a5cc527fd750b17a8e3d2518e8543b08f98ee51d0c

SRC_SHA256 by dollars
       2.12M        8 rows  f027c596587588a98dbc49a5cc527fd750b17a8e3d2518e8543b08f98ee5

## who x when

DISTRICTCLASS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Operations                                2026:2.12M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  f027c596587588a98dbc49a5cc527fd750b17a8e  2026:2.12M

## what

OBJECTID: 16 12%, 13 12%, 8 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

FACILITYID: 7 12%, 6 12%, 8 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

PARKDISTRICT: 7 12%, 6 12%, 8 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

SERVICEYARD: Central Service Yard 50%, PAL Stadium Yard 12%, Kelley/Prusch Park Yards 12%, Guadalupe River Park Yard 12%, Lake Cunningham Park Yard 12%

LASTUPDATE: 2022/12/02 02:10:35+00 12%, 2025/09/30 23:02:22+00 12%, 2025/09/30 22:46:59+00 12%, 2025/03/11 18:16:42+00 12%, 2025/09/30 22:46:36+00 12%, 2025/09/30 22:46:28+00 12%, 2025/09/30 22:46:23+00 12%, 2025/09/30 22:44:08+00 12%

ENTERPRISEID: PRN-PARD-0000000007 12%, PRN-PARD-0000000006 12%, PRN-PARD-0000000008 12%, PRN-PARD-0000000005 12%, PRN-PARD-0000000004 12%, PRN-PARD-0000000003 12%, PRN-PARD-0000000002 12%, PRN-PARD-0000000001 12%

INTID: 7 12%, 6 12%, 8 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 8 | 0 | 16 1; 13 1; 8 1; 5 1 |
| FACILITYID | category | 8 | 0 | 7 1; 6 1; 8 1; 5 1 |
| GISOBJID | empty | 1 | 8 |  |
| PARKDISTRICT | category | 8 | 0 | 7 1; 6 1; 8 1; 5 1 |
| DISTRICTCLASS | who | 1 | 0 | Operations 8 |
| SERVICEYARD | category | 5 | 0 | Central Service Yard 4; PAL Stadium Yard 1; Kelley/Prusch Park Yards 1; Guadalupe River Park Yard 1 |
| UPDATE_COUNT | empty | 1 | 8 |  |
| LASTUPDATE | category | 8 | 0 | 2022/12/02 02:10:35+00 1; 2025/09/30 23:02:22+00 1; 2025/09/30 22:46:59+00 1; 2025/03/11 18:16:42+00 1 |
| ENTERPRISEID | category | 8 | 0 | PRN-PARD-0000000007 1; PRN-PARD-0000000006 1; PRN-PARD-0000000008 1; PRN-PARD-0000000005 1 |
| INTID | category | 8 | 0 | 7 1; 6 1; 8 1; 5 1 |
| SHAPE_LENGTH | amount | 8 | 0 | 7511.38950669391 1; 10345.9717800417 1; 424650.417129273 1; 135616.160617518 1 |
| SHAPE_AREA | amount | 8 | 0 | 1278690.90028326 1; 2782117.66749419 1; 1270974797.42543 1; 338071456.98739 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:11:42.14264 8 |
| SOURCE_RUN_ID | audit | 1 | 0 | 52e3c465-3b51-4ea2-bf89-6 8 |
| SRC_SHA256 | who | 1 | 0 | f027c596587588a98dbc49a5c 8 |
