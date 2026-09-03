# PORTAL_CKA_WESTERN_PENNSYLV_7AC49E7444

rows 37  columns 13  scan 4.9s

roles: amount 2, audit 2, category 2, date 1, other 2, who 5

## when

INGESTED_AT
  2026        37  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 37 | 1.65 | 93.20 | 1.0K | 1.1K | 7.4K |
| SQMILES | 37 | 0 | 0.15 | 1.57 | 1.65 | 11.56 |

## who

LAST_EDITED_USER by rows
        37  pgh.admin

LAST_EDITED_USER by dollars
        7.4K       37 rows  pgh.admin

CREATED_USER by rows
        37  pgh.admin

CREATED_USER by dollars
        7.4K       37 rows  pgh.admin

LAST_EDITED_DATE by rows
        37  Mon, 19 Mar 2018 19:03:26 GMT

LAST_EDITED_DATE by dollars
        7.4K       37 rows  Mon, 19 Mar 2018 19:03:26 GMT

CREATED_DATE by rows
        37  Mon, 19 Mar 2018 19:03:26 GMT

CREATED_DATE by dollars
        7.4K       37 rows  Mon, 19 Mar 2018 19:03:26 GMT

## who x when

LAST_EDITED_USER by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  pgh.admin                                 2026:7.4K

CREATED_USER by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  pgh.admin                                 2026:7.4K

## what

OBJECTID: 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%

DATASPATIAL_WKB: \x000000000300000001000001c6c0 8%, \x00000000030000000100000171c0 8%, \x00000000030000000100000048c0 8%, \x00000000030000000100000036c0 8%, \x000000000300000001000000c6c0 8%, \x000000000300000001000000b3c0 8%, \x000000000300000001000000f9c0 8%, \x000000000300000001000000a8c0 8%, \x00000000030000000100000374c0 8%, \x0000000003000000010000023fc0 8%, \x000000000300000001000001d5c0 8%, \x0000000003000000010000028bc0 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LANDSLIDEPRONE | other | 1 | 0 | Yes 37 |
| LAST_EDITED_USER | who | 1 | 0 | pgh.admin 37 |
| CREATED_USER | who | 1 | 0 | pgh.admin 37 |
| LAST_EDITED_DATE | who | 1 | 0 | Mon, 19 Mar 2018 19:03:26 37 |
| OBJECTID | category | 37 | 0 | 37 1; 36 1; 35 1; 34 1 |
| CODE | other | 1 | 0 | p 37 |
| CREATED_DATE | who | 1 | 0 | Mon, 19 Mar 2018 19:03:26 37 |
| ACRES | amount | 37 | 0 | 280.649 1; 216.452 1; 19.897 1; 12.22 1 |
| SQMILES | amount | 36 | 0 | 0.021 2; 0.439 1; 0.338 1; 0.031 1 |
| DATASPATIAL_WKB | category | 37 | 0 | \x00000000030000000100000 1; \x00000000030000000100000 1; \x00000000030000000100000 1; \x00000000030000000100000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:20:37.88134 37 |
| SOURCE_RUN_ID | audit | 1 | 0 | 488ad605-0cb6-44f5-86d6-d 37 |
| SRC_SHA256 | who | 1 | 0 | 96fc39a3874d806717c79c4ef 37 |
