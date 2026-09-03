# PORTAL_CKA_VIRGINIA_OPEN_DA_6973FD2BA7

rows 6  columns 10  scan 1.9s

roles: audit 2, category 7, date 1, who 1

## when

INGESTED_AT
  2026         6  ##############################

## who

SRC_SHA256 by rows
         6  3f14941d5e6f82da094ee68874f67e2a8b0e2f8a7bdc33975f16ce8bd0e323c1

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  3f14941d5e6f82da094ee68874f67e2a8b0e2f8a  2026:6

## what

HOSPITAL_NAME: University of Virginia Transit 17%, Select Specialty Hospital - Ri 17%, Lake Taylor Transitional Care  17%, Hospital For Extended Recovery 17%, Hampton Roads Speciality Hospi 17%, Centra Specialty Hospital 17%

ADDRESS: 2965 Ivy Road 17%, 2230 Edward Holland Drive 17%, 1309 Kempsville Road 17%, 600 Gresham Drive 17%, 500 J Clyde Morris Blvd 17%, 3300 Rivermont Avenue 17%

CITY: Norfolk 33%, Charlottesville 17%, Richmond 17%, Newport News 17%, Lynchburg 17%

ZIP_CODE: 22903 17%, 23230 17%, 23502 17%, 23507 17%, 23601 17%, 24503 17%

HOSPITAL_SYSTEM: UVA Health System 20%, Select Medical 20%, Sentara Healthcare 20%, Riverside 20%, Centra Health 20%

BED_SIZE: 40 17%, 60 17%, 104 17%, 35 17%, 25 17%, 36 17%

VDH_HEALTH_PLANNING_REGION: Eastern Region 50%, Northwest Region 17%, Central Region 17%, Southwest Region 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| HOSPITAL_NAME | category | 6 | 0 | University of Virginia Tr 1; Select Specialty Hospital 1; Lake Taylor Transitional  1; Hospital For Extended Rec 1 |
| ADDRESS | category | 6 | 0 | 2965 Ivy Road 1; 2230 Edward Holland Drive 1; 1309 Kempsville Road 1; 600 Gresham Drive 1 |
| CITY | category | 5 | 0 | Norfolk 2; Charlottesville 1; Richmond 1; Newport News 1 |
| ZIP_CODE | category | 6 | 0 | 22903 1; 23230 1; 23502 1; 23507 1 |
| HOSPITAL_SYSTEM | category | 6 | 1 | UVA Health System 1; Select Medical 1; Sentara Healthcare 1; Riverside 1 |
| BED_SIZE | category | 6 | 0 | 40 1; 60 1; 104 1; 35 1 |
| VDH_HEALTH_PLANNING_REGION | category | 4 | 0 | Eastern Region 3; Northwest Region 1; Central Region 1; Southwest Region 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:10:59.97946 6 |
| SOURCE_RUN_ID | audit | 1 | 0 | fb97fc05-a8dc-4f75-bd0b-f 6 |
| SRC_SHA256 | who | 1 | 0 | 3f14941d5e6f82da094ee6887 6 |
