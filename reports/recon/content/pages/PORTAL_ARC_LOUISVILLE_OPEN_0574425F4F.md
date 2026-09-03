# PORTAL_ARC_LOUISVILLE_OPEN_0574425F4F

rows 17  columns 21  scan 3.5s

roles: amount 2, audit 2, category 11, date 3, who 4

## when

CREATIONDATE
  2025        17  ##############################

EDITDATE
  2025        17  ##############################

INGESTED_AT
  2026        17  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 17 | 38.05 | 38.22 | 38.30 | 38.30 | 649.38 |
| LONGITUDE | 17 | -85.91 | -85.81 | -85.51 | -85.51 | -1.5K |

## who

CREATOR by rows
        17  andy.purdon_Metro

CREATOR by dollars
      649.38       17 rows  andy.purdon_Metro

EDITOR by rows
        17  andy.purdon_Metro

EDITOR by dollars
      649.38       17 rows  andy.purdon_Metro

COUNTY by rows
        17  jefferson county

COUNTY by dollars
      649.38       17 rows  jefferson county

SRC_SHA256 by rows
        17  5facce2fcbdcdef2ed7db4b55d37cbc44bdb2823a1cb06cc1b9ee761c8cb04ab

SRC_SHA256 by dollars
      649.38       17 rows  5facce2fcbdcdef2ed7db4b55d37cbc44bdb2823a1cb06cc1b9ee761c8cb

## who x when

CREATOR by CREATIONDATE, dollars = LATITUDE
  andy.purdon_Metro                         2025:649.38

EDITOR by CREATIONDATE, dollars = LATITUDE
  andy.purdon_Metro                         2025:649.38

## what

FACILITY_NAME: ZEON CHEMICALS L.P. 8%, Sysco Louisville Inc. 8%, Sealed Air, Louisville 8%, Mill Creek Station 8%, Lubrizol Advanced Materials, I 8%, Louisville Packaging 8%, Lineage Logistics Louisville - 8%, Lineage Logistics - Louisville 8%, Kentucky Distribution Center 8%, JBS Louisville Pork Processing 8%, Hexion Inc.. Louisville, KY 8%, DuPont Specialty Products USA, 8%

STREET_ADDRESS_LINE_1: 4100 bells lane 8%, 7705 national turnpike 8%, 7665 national turnpike 8%, 14660 dixie highway 8%, 4200 bells lane 8%, 7745 national turnpike 8%, 607 Industry Road 8%, 7201 winstead drive 8%, 2000 nelson miller parkway 8%, 1200 story avenue 8%, 6200 campground rd. 8%, 4250 camp ground road 8%

CITY: louisville 94%, Louisville 6%

STATE: ky 94%, KY 6%

ZIP_CODE: 40216 29%, 40214 18%, 40211 12%, 40272 6%, 40208 6%, 40258 6%, 40223 6%, 40206 6%, 40245 6%, 40210 6%

NAICS: 325 47%, 493 18%, 424 12%, 311 12%, 326 6%, 221 6%

PROGRAM_LEVEL: 3 94%, 2 6%

INDUSTRY: Chemical Manufacturing 47%, Warehousing and Storage 18%, Merchant Wholesalers, Nondurab 12%, Food Manufacturing 12%, Plastics and Rubber Products M 6%, Utilities 6%

RESPONDING: y 65%, n 35%

OBJECTID: 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FACILITY_NAME | category | 17 | 0 | ZEON CHEMICALS L.P. 1; Sysco Louisville Inc. 1; Sealed Air, Louisville 1; Mill Creek Station 1 |
| STREET_ADDRESS_LINE_1 | category | 16 | 0 | 4100 bells lane 1; 7705 national turnpike 1; 7665 national turnpike 1; 14660 dixie highway 1 |
| CITY | category | 2 | 0 | louisville 16; Louisville 1 |
| STATE | category | 2 | 0 | ky 16; KY 1 |
| ZIP_CODE | category | 10 | 0 | 40216 5; 40214 3; 40211 2; 40272 1 |
| COUNTY | who | 1 | 0 | jefferson county 17 |
| LATITUDE | amount | 17 | 0 | 38.222222 1; 38.141944 1; 38.143694 1; 38.050556 1 |
| LONGITUDE | amount | 16 | 0 | -85.840056 2; -85.82681 1; -85.753611 1; -85.748111 1 |
| NAICS | category | 6 | 0 | 325 8; 493 3; 424 2; 311 2 |
| PROGRAM_LEVEL | category | 2 | 0 | 3 16; 2 1 |
| INDUSTRY | category | 6 | 0 | Chemical Manufacturing 8; Warehousing and Storage 3; Merchant Wholesalers, Non 2; Food Manufacturing 2 |
| RESPONDING | category | 2 | 0 | y 11; n 6 |
| OBJECTID | category | 17 | 0 | 17 1; 16 1; 15 1; 14 1 |
| CREATIONDATE | date | 1 | 0 | 1763469185818 17 |
| CREATOR | who | 1 | 0 | andy.purdon_Metro 17 |
| EDITDATE | date | 1 | 0 | 1763469185818 17 |
| EDITOR | who | 1 | 0 | andy.purdon_Metro 17 |
| GEOMETRY | category | 17 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:22.86010 17 |
| SOURCE_RUN_ID | audit | 1 | 0 | 971025ec-ae3e-4106-a0e5-8 17 |
| SRC_SHA256 | who | 1 | 0 | 5facce2fcbdcdef2ed7db4b55 17 |
