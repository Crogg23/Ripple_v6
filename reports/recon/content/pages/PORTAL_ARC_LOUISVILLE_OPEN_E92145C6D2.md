# PORTAL_ARC_LOUISVILLE_OPEN_E92145C6D2

rows 18  columns 17  scan 3.9s

roles: amount 2, audit 2, category 9, date 1, other 1, who 3

## when

INGESTED_AT
  2026        18  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 18 | 38.05 | 38.22 | 38.29 | 38.30 | 687.59 |
| LONGITUDE | 18 | -85.91 | -85.82 | -85.51 | -85.51 | -1.5K |

## who

CITY by rows
        18  louisville

CITY by dollars
      687.59       18 rows  louisville

COUNTY by rows
        18  jefferson county

COUNTY by dollars
      687.59       18 rows  jefferson county

SRC_SHA256 by rows
        18  94f50b5795b1d415031d57391744e3d64ad3bca5e93c01eae9ee8aa212ae25dc

SRC_SHA256 by dollars
      687.59       18 rows  94f50b5795b1d415031d57391744e3d64ad3bca5e93c01eae9ee8aa212ae

## who x when

CITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  louisville                                2026:687.59

COUNTY by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  jefferson county                          2026:687.59

## what

FACILITY_NAME: zeon chemicals l.p. 8%, sysco louisville inc. 8%, sealed air, louisville 8%, mill creek station 8%, lubrizol advanced materials, i 8%, louisville packaging 8%, lineage logistics - louisville 8%, kentucky distribution center 8%, jbs louisville pork processing 8%, hexion inc.. louisville, ky 8%, e.i. du pont de nemours 8%, conagra foods, inc. 8%

STREET_ADDRESS_LINE_1: 4100 bells lane 8%, 7705 national turnpike 8%, 7665 national turnpike 8%, 14660 dixie highway 8%, 4200 bells lane 8%, 7745 national turnpike 8%, 7201 winstead drive 8%, 2000 nelson miller parkway 8%, 1200 story avenue 8%, 6200 campground rd. 8%, 4250 camp ground road 8%, 12650 westport road 8%

ZIP_CODE: 40216 33%, 40214 17%, 40211 11%, 40272 6%, 40258 6%, 40223 6%, 40206 6%, 40245 6%, 40210 6%, 40208 6%

NAICS: 325 44%, 424 17%, 493 17%, 311 11%, 326 6%, 221 6%

PROGRAM_LEVEL: 3 83%, 2 17%

INDUSTRY: Chemical Manufacturing 44%, Merchant Wholesalers, Nondurab 17%, Warehousing and Storage 17%, Food Manufacturing 11%, Plastics and Rubber Products M 6%, Utilities 6%

RESPONDING: y 61%, n 33%, NA 6%

OBJECTID: 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FACILITY_NAME | category | 18 | 0 | zeon chemicals l.p. 1; sysco louisville inc. 1; sealed air, louisville 1; mill creek station 1 |
| STREET_ADDRESS_LINE_1 | category | 17 | 0 | 4100 bells lane 1; 7705 national turnpike 1; 7665 national turnpike 1; 14660 dixie highway 1 |
| CITY | who | 1 | 0 | louisville 18 |
| STATE | other | 1 | 0 | ky 18 |
| ZIP_CODE | category | 10 | 0 | 40216 6; 40214 3; 40211 2; 40272 1 |
| COUNTY | who | 1 | 0 | jefferson county 18 |
| LATITUDE | amount | 18 | 0 | 38.222222 1; 38.141944 1; 38.143694 1; 38.050556 1 |
| LONGITUDE | amount | 17 | 0 | -85.840056 2; -85.82681 1; -85.753611 1; -85.748111 1 |
| NAICS | category | 6 | 0 | 325 8; 424 3; 493 3; 311 2 |
| PROGRAM_LEVEL | category | 2 | 0 | 3 15; 2 3 |
| INDUSTRY | category | 6 | 0 | Chemical Manufacturing 8; Merchant Wholesalers, Non 3; Warehousing and Storage 3; Food Manufacturing 2 |
| RESPONDING | category | 3 | 0 | y 11; n 6; NA 1 |
| OBJECTID | category | 18 | 0 | 18 1; 17 1; 16 1; 15 1 |
| GEOMETRY | category | 18 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:35.46780 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9a2bf4a6-42a7-492f-969b-7 18 |
| SRC_SHA256 | who | 1 | 0 | 94f50b5795b1d415031d57391 18 |
