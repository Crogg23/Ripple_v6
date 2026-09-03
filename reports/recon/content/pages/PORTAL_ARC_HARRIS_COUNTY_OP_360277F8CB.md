# PORTAL_ARC_HARRIS_COUNTY_OP_360277F8CB

rows 2  columns 35  scan 2.5s

roles: audit 2, category 32, date 1, who 1

## when

INGESTED_AT
  2026         2  ##############################

## who

SRC_SHA256 by rows
         2  4e4b69e7dd78f5a88a4b2989513b97a0bfbd32af79d1a9bf5f740f9d58b75e69

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  4e4b69e7dd78f5a88a4b2989513b97a0bfbd32af  2026:2

## what

OBJECTID: 2 50%, 1 50%

NCESID: nan 50%, 482025001981 50%

NAME: Sam Houston Elementary 50%, CLOVERLEAF EL 50%

ADDRESS: nan 50%, 1035 FRANKIE 50%

CITY: nan 50%, HOUSTON 50%

STATE: nan 50%, TX 50%

ZIP: nan 50%, 77015 50%

ZIP4: nan 50%, 5180 50%

TELEPHONE: nan 50%, (832) 386-3200 50%

TYPE: nan 50%, 1 50%

STATUS: nan 50%, 1 50%

POPULATION: nan 50%, 851.0 50%

COUNTY: nan 50%, HARRIS 50%

COUNTYFIPS: nan 50%, 48201 50%

COUNTRY: nan 50%, USA 50%

LATITUDE: nan 50%, 29.7760548 50%

LONGITUDE: nan 50%, -95.1747467 50%

NAICS_CODE: nan 50%, 611110 50%

NAICS_DESC: nan 50%, ELEMENTARY AND SECONDARY SCHOO 50%

SOURCE: nan 50%, https://nces.ed.gov/ccd/school 50%

SOURCE_DAT: nan 50%, 1706659200000.0 50%

VAL_METHOD: nan 50%, IMAGERY/OTHER 50%

VAL_DATE: nan 50%, 1267315200000.0 50%

WEBSITE: nan 50%, http://www.galenaparkisd.com 50%

LEVEL: nan 50%, ELEMENTARY 50%

ENROLLMENT: nan 50%, 803.0 50%

ST_GRADE: nan 50%, PK 50%

END_GRADE: nan 50%, 05 50%

DISTRICTID: nan 50%, 4820250 50%

FT_TEACHER: nan 50%, 48.0 50%

SHELTER_ID: nan 50%, NOT AVAILABLE 50%

GEOMETRY: {"type": "Point", "coordinates 50%, {"type": "Point", "coordinates 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 2 1; 1 1 |
| NCESID | category | 2 | 0 | nan 1; 482025001981 1 |
| NAME | category | 2 | 0 | Sam Houston Elementary 1; CLOVERLEAF EL 1 |
| ADDRESS | category | 2 | 0 | nan 1; 1035 FRANKIE 1 |
| CITY | category | 2 | 0 | nan 1; HOUSTON 1 |
| STATE | category | 2 | 0 | nan 1; TX 1 |
| ZIP | category | 2 | 0 | nan 1; 77015 1 |
| ZIP4 | category | 2 | 0 | nan 1; 5180 1 |
| TELEPHONE | category | 2 | 0 | nan 1; (832) 386-3200 1 |
| TYPE | category | 2 | 0 | nan 1; 1 1 |
| STATUS | category | 2 | 0 | nan 1; 1 1 |
| POPULATION | category | 2 | 0 | nan 1; 851.0 1 |
| COUNTY | category | 2 | 0 | nan 1; HARRIS 1 |
| COUNTYFIPS | category | 2 | 0 | nan 1; 48201 1 |
| COUNTRY | category | 2 | 0 | nan 1; USA 1 |
| LATITUDE | category | 2 | 0 | nan 1; 29.7760548 1 |
| LONGITUDE | category | 2 | 0 | nan 1; -95.1747467 1 |
| NAICS_CODE | category | 2 | 0 | nan 1; 611110 1 |
| NAICS_DESC | category | 2 | 0 | nan 1; ELEMENTARY AND SECONDARY  1 |
| SOURCE | category | 2 | 0 | nan 1; https://nces.ed.gov/ccd/s 1 |
| SOURCE_DAT | category | 2 | 0 | nan 1; 1706659200000.0 1 |
| VAL_METHOD | category | 2 | 0 | nan 1; IMAGERY/OTHER 1 |
| VAL_DATE | category | 2 | 0 | nan 1; 1267315200000.0 1 |
| WEBSITE | category | 2 | 0 | nan 1; http://www.galenaparkisd. 1 |
| LEVEL | category | 2 | 0 | nan 1; ELEMENTARY 1 |
| ENROLLMENT | category | 2 | 0 | nan 1; 803.0 1 |
| ST_GRADE | category | 2 | 0 | nan 1; PK 1 |
| END_GRADE | category | 2 | 0 | nan 1; 05 1 |
| DISTRICTID | category | 2 | 0 | nan 1; 4820250 1 |
| FT_TEACHER | category | 2 | 0 | nan 1; 48.0 1 |
| SHELTER_ID | category | 2 | 0 | nan 1; NOT AVAILABLE 1 |
| GEOMETRY | category | 2 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:11:49.89615 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | e982619e-5c03-4bae-a9c7-3 2 |
| SRC_SHA256 | who | 1 | 0 | 4e4b69e7dd78f5a88a4b29895 2 |
