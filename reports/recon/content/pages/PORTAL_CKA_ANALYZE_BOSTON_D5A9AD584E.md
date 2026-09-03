# PORTAL_CKA_ANALYZE_BOSTON_D5A9AD584E

rows 10.0K  columns 66  scan 5.0s

roles: amount 4, audit 2, category 47, date 4, id 1, other 8, who 1

## when

PERMIT_APPLICATION_FILING_DATE
  2018       703  #####
  2019      2.0K  ###############
  2020      3.9K  ##############################
  2021       969  ########
  2022       570  ####
  2023       552  ####
  2024       629  #####
  2025       535  ####
  2026       217  ##

PERMIT_ISSUED_DATE
  2018       249  ###
  2019       839  ###########
  2020      2.2K  ##############################
  2021      1.2K  #################
  2022       488  #######
  2023       453  ######
  2024       395  #####
  2025       401  #####
  2026       156  ##

REZONING_EFFECTIVE_DATE
  2024       923  ##############################
  2025       650  #####################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_COMMON_VIOLATIONS | 1.4K | 0 | 1 | 8.20 | 12 | 2.7K |
| X_LONGITUDE | 10.0K | -71.18 | -71.07 | -71.02 | -71 | -710.8K |
| Y_LATITUDE | 10.0K | 42.23 | 42.34 | 42.38 | 42.40 | 423.3K |
| CENSUS_TRACT | 10.0K | 1.01 | 701.04 | 1.4K | 9.8K | 7.35M |

## who

SRC_SHA256 by rows
     10.0K  48752026566407fe15cb7f7ce26e7a7da59f2fba2728dff591b5fd140048c3f0

SRC_SHA256 by dollars
        2.7K    10.0K rows  48752026566407fe15cb7f7ce26e7a7da59f2fba2728dff591b5fd140048

## who x when

SRC_SHA256 by PERMIT_APPLICATION_FILING_DATE, dollars = TOTAL_COMMON_VIOLATIONS
  48752026566407fe15cb7f7ce26e7a7da59f2fba  2018:63 2019:619 2020:1.5K 2021:280 2022:54 2023:67 2024:61 2025:40 2026:13

## what

ZONING_REVIEW_APPROVED: f 52%, t 48%

STARTED_APPEAL: f 90%, t 10%

COMPLETED_APPEAL: f 91%, t 9%

PERMIT_ISSUED: t 64%, f 36%

PERMIT_APPLICATION_ABANDONED: f 78%, t 22%

PERMIT_APPLICATION_INACTIVE: f 98%, t 2%

PERMIT_APPLICATION_HAS_ADU: f 98%, t 2%

PERMIT_APPLICATION_TYPE: Alteration 51%, Amendment 49%

PERMIT_APPLICATION_WORK_TYPE: Interior/Exterior Work 22%, Renovations - Interior NSC 15%, Other 13%, Change Occupancy 9%, Fire Alarm 8%, Renovations - Exterior 7%, Addition 7%, Signs 6%, Fire Protection/Sprinkler 5%, Fast Track Application 5%, Subdivision, Combining Lot 2%, No Record of Occupancy 2%

IN_SQUARES_STREETS_REZONED_AREA: f 99%, t 1%

SQUARES_STREETS_S_DISTRICT_NAME: S4 42%, S2 40%, S0 7%, S1 6%, S3 4%

BEFORE_OR_AFTER_REZONING: before 90%, after 10%

WHICH_REZONING: East Boston rezoning 46%, Downtown rezoning 38%, Mattapan rezoning 9%, Squares and Streets: Roslindal 3%, Squares and Streets: Mattapan 3%

CHILD_CARE_BUSINESS_PERMITTED_WHERE_PREVIOUSLY_NOT_ALLOWED: f 100%, t 0%

RESIDENTIAL_UNITS_BEFORE_PERMITTED_WORK_ON_AND_AFTER_OCT_2024: 0 99%, 5 1%

RESIDENTIAL_UNITS_AFTER_PERMITTED_WORK_ON_AND_AFTER_OCT_2024: 0 99%, 7 1%

IS_ARTICLE_80: f 97%, t 3%

IS_ARTICLE_80_SMALL_PROJECT: f 100%

IS_ARTICLE_80_LARGE_PROJECT: f 100%

CITY_COUNCIL_DISTRICT: District 2 19%, District 1 18%, District 8 13%, District 3 10%, District 6 10%, District 7 10%, District 4 8%, District 5 8%, District 9 6%

ZONING_RELIEF_TYPE: Variance 67%, Variance and Conditional Use P 18%, Conditional Use Permit 14%

VIOLATION_FOR_EXISTING_BUILDING_ALIGNMENT: f 99%, t 1%

VIOLATION_FOR_ROOF_RESTRICTION: f 79%, t 21%

VIOLATION_FOR_ACCESSORY_PARKING_USE: f 98%, t 2%

VIOLATION_FOR_PARKING_DESIGN_AND_MANEUVERABILITY: f 98%, t 2%

VIOLATION_FOR_INSUFFICIENT_PARKING_OR_LOADING: f 81%, t 19%

VIOLATION_FOR_INSUFFICIENT_LOT_WIDTH: f 99%, t 1%

VIOLATION_FOR_INSUFFICIENT_ADDITIONAL_LOT_AREA: f 92%, t 8%

VIOLATION_FOR_INSUFFICIENT_LOT_AREA: f 97%, t 3%

VIOLATION_FOR_INSUFFICIENT_LOT_FRONTAGE: f 99%, t 1%

VIOLATION_FOR_INSUFFICIENT_USABLE_OPEN_SPACE: f 87%, t 13%

VIOLATION_FOR_INSUFFICIENT_FRONT_YARD: f 91%, t 9%

VIOLATION_FOR_INSUFFICIENT_SIDE_YARD: f 72%, t 28%

VIOLATION_FOR_INSUFFICIENT_REAR_YARD: f 73%, t 27%

VIOLATION_FOR_EXCESSIVE_HEIGHT_IN_STORIES: f 89%, t 11%

VIOLATION_FOR_EXCESSIVE_HEIGHT_IN_FEET: f 94%, t 6%

VIOLATION_FOR_EXCESSIVE_HEIGHT_ALONE: f 94%, t 6%

VIOLATION_FOR_EXCESSIVE_FLOOR_AREA_RATIO: f 62%, t 38%

BY_RIGHT: f 57%, t 43%

ZONING_DISTRICT: Dorchester Neighborhood 14%, Boston Proper 12%, Roxbury Neighborhood 10%, East Boston Neighborhood 9%, South Boston Neighborhood 9%, Boston Zoning Code 9%, Allston/Brighton Neighborhood 8%, Jamaica Plain Neighborhood 7%, South End Neighborhood 6%, West Roxbury Neighborhood 5%, Hyde Park Neighborhood 5%, Greater Mattapan Neighborhood 5%

NEIGHBORHOOD: Dorchester 18%, South Boston 11%, Downtown 10%, East Boston 10%, Roxbury 9%, Back Bay 9%, Jamaica Plain 7%, South End 6%, West Roxbury 5%, Charlestown 5%, Hyde Park 5%, Brighton 5%

ZONING_BOARD_OF_APPEAL_DECISION_LINK: https://drive.google.com/file/ 33%, https://drive.google.com/file/ 33%, https://drive.google.com/file/ 33%

PLANNING_DEPARTMENT_RECOMMENDATION_LINK: https://www.bostonplans.org/do 12%, https://www.bostonplans.org/do 12%, https://www.bostonplans.org/do 8%, https://www.bostonplans.org/do 8%, https://www.bostonplans.org/do 8%, https://www.bostonplans.org/do 8%, https://www.bostonplans.org/do 8%, https://www.bostonplans.org/do 8%, https://www.bostonplans.org/do 8%, https://www.bostonplans.org/do 8%, https://www.bostonplans.org/do 8%

RESUBMITTED_PLANS_UNLIKELY: f 87%, t 13%

RESUBMITTED_PLANS_LIKELY: f 99%, t 1%

ZIP_CODE: 02127 13%, 02128 12%, 02116 12%, 02124 8%, 02130 8%, 02125 8%, 02118 8%, 02119 7%, 02121 7%, 02132 6%, 02129 6%, 02136 6%

CENSUS_BLOCK_GROUP: 1 38%, 2 32%, 3 17%, 4 8%, 5 3%, 6 1%, 7 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ADDRESS | other | 6.1K | 0 | 200 Clarendon ST 56; 1006 to 1022 Massachusett 54; 451 D ST 53; 1605 to 1607 VFW PW 51 |
| PERMIT_APPLICATION_NUMBER | id | 10.0K | 0 | ALT1165270 50; ALT1165259 50; ALT1165253 50; ALT1165187 50 |
| PERMIT_APPLICATION_FILING_DATE | date | 2.1K | 0 | 2021-01-28 61; 2020-09-24 61; 2020-07-23 60; 2021-02-19 59 |
| ZONING_REVIEW_APPROVED | category | 2 | 0 | f 5.2K; t 4.8K |
| STARTED_APPEAL | category | 2 | 0 | f 9.0K; t 1.0K |
| COMPLETED_APPEAL | category | 2 | 0 | f 9.1K; t 910 |
| PERMIT_ISSUED | category | 2 | 0 | t 6.4K; f 3.6K |
| PERMIT_APPLICATION_ABANDONED | category | 2 | 0 | f 7.8K; t 2.2K |
| PERMIT_APPLICATION_INACTIVE | category | 2 | 0 | f 9.8K; t 199 |
| PERMIT_ISSUED_DATE | date | 1.7K | 3.6K | 2021-02-03 44; 2021-02-04 43; 2021-01-27 38; 2020-11-12 38 |
| DAYS_TO_PERMIT_ISSUANCE | other | 705 | 3.6K | 14 121; 28 113; 7 108; 15 105 |
| DAYS_AT_ZBA | other | 355 | 9.1K | 127 14; 175 13; 121 12; 135 12 |
| PERMIT_APPLICATION_HAS_ADU | category | 2 | 0 | f 9.8K; t 156 |
| PERMIT_APPLICATION_TYPE | category | 2 | 0 | Alteration 5.1K; Amendment 4.9K |
| PERMIT_APPLICATION_WORK_TYPE | category | 22 | 16 | Interior/Exterior Work 2.1K; Renovations - Interior NS 1.4K; Other 1.2K; Change Occupancy 836 |
| IN_SQUARES_STREETS_REZONED_AREA | category | 2 | 0 | f 9.9K; t 113 |
| SQUARES_STREETS_S_DISTRICT_NAME | category | 6 | 9.9K | S4 48; S2 45; S0 8; S1 7 |
| BEFORE_OR_AFTER_REZONING | category | 3 | 8.4K | before 1.4K; after 150 |
| WHICH_REZONING | category | 6 | 8.4K | East Boston rezoning 729; Downtown rezoning 597; Mattapan rezoning 145; Squares and Streets: Rosl 53 |
| REZONING_EFFECTIVE_DATE | date | 6 | 8.4K | 2024-05-01 729; 2025-10-28 597; 2024-02-07 145; 2025-06-02 53 |
| CHILD_CARE_BUSINESS_PERMITTED_WHERE_PREVIOUSLY_NOT_ALLOWED | category | 2 | 0 | f 10.0K; t 3 |
| NUMBER_OF_CHILDREN_CHILD_CARE_IS_ELIGIBLE_TO_SERVE | other | 57 | 9.7K | 40 34; 287 22; 60 21; 25 18 |
| RESIDENTIAL_UNITS_BEFORE_PERMITTED_WORK_ON_AND_AFTER_OCT_2024 | category | 3 | 9.9K | 0 139; 5 1 |
| RESIDENTIAL_UNITS_AFTER_PERMITTED_WORK_ON_AND_AFTER_OCT_2024 | category | 3 | 9.9K | 0 139; 7 1 |
| IS_ARTICLE_80 | category | 2 | 0 | f 9.7K; t 309 |
| IS_ARTICLE_80_SMALL_PROJECT | category | 2 | 9.7K | f 309 |
| IS_ARTICLE_80_LARGE_PROJECT | category | 2 | 9.7K | f 309 |
| CITY_COUNCIL_DISTRICT | category | 9 | 0 | District 2 1.9K; District 1 1.8K; District 8 1.3K; District 3 975 |
| ZONING_RELIEF_TYPE | category | 4 | 9.0K | Variance 662; Variance and Conditional  180; Conditional Use Permit 141 |
| TOTAL_COMMON_VIOLATIONS | amount | 13 | 8.6K | 1 429; 0 291; 2 267; 3 162 |
| VIOLATION_FOR_EXISTING_BUILDING_ALIGNMENT | category | 3 | 8.6K | f 1.4K; t 18 |
| VIOLATION_FOR_ROOF_RESTRICTION | category | 3 | 8.6K | f 1.1K; t 286 |
| VIOLATION_FOR_ACCESSORY_PARKING_USE | category | 3 | 8.6K | f 1.3K; t 33 |
| VIOLATION_FOR_PARKING_DESIGN_AND_MANEUVERABILITY | category | 3 | 8.6K | f 1.3K; t 32 |
| VIOLATION_FOR_INSUFFICIENT_PARKING_OR_LOADING | category | 3 | 8.6K | f 1.1K; t 262 |
| VIOLATION_FOR_INSUFFICIENT_LOT_WIDTH | category | 3 | 8.6K | f 1.4K; t 14 |
| VIOLATION_FOR_INSUFFICIENT_ADDITIONAL_LOT_AREA | category | 3 | 8.6K | f 1.3K; t 106 |
| VIOLATION_FOR_INSUFFICIENT_LOT_AREA | category | 3 | 8.6K | f 1.3K; t 35 |
| VIOLATION_FOR_INSUFFICIENT_LOT_FRONTAGE | category | 3 | 8.6K | f 1.4K; t 16 |
| VIOLATION_FOR_INSUFFICIENT_USABLE_OPEN_SPACE | category | 3 | 8.6K | f 1.2K; t 180 |
| VIOLATION_FOR_INSUFFICIENT_FRONT_YARD | category | 3 | 8.6K | f 1.3K; t 124 |
| VIOLATION_FOR_INSUFFICIENT_SIDE_YARD | category | 3 | 8.6K | f 988; t 393 |
| VIOLATION_FOR_INSUFFICIENT_REAR_YARD | category | 3 | 8.6K | f 1.0K; t 377 |
| VIOLATION_FOR_EXCESSIVE_HEIGHT_IN_STORIES | category | 3 | 8.6K | f 1.2K; t 151 |
| VIOLATION_FOR_EXCESSIVE_HEIGHT_IN_FEET | category | 3 | 8.6K | f 1.3K; t 88 |
| VIOLATION_FOR_EXCESSIVE_HEIGHT_ALONE | category | 3 | 8.6K | f 1.3K; t 84 |
| VIOLATION_FOR_EXCESSIVE_FLOOR_AREA_RATIO | category | 3 | 8.6K | f 862; t 519 |
| BY_RIGHT | category | 2 | 0 | f 5.7K; t 4.3K |
| ZONING_DISTRICT | category | 37 | 0 | Dorchester Neighborhood 1.1K; Boston Proper 904; Roxbury Neighborhood 774; East Boston Neighborhood 734 |
| NEIGHBORHOOD | category | 25 | 0 | Dorchester 1.4K; South Boston 825; Downtown 742; East Boston 734 |
| BOARD_OF_APPEAL_APPLICATION_NUMBER | other | 979 | 9.0K | BOA1223671 5; BOA1177169 5; BOA1183021 5; BOA1183223 5 |
| ZONING_BOARD_OF_APPEAL_DECISION_LINK | category | 4 | 10.0K | https://drive.google.com/ 1; https://drive.google.com/ 1; https://drive.google.com/ 1 |
| PLANNING_DEPARTMENT_RECOMMENDATION_LINK | category | 39 | 9.9K | https://www.bostonplans.o 3; https://www.bostonplans.o 3; https://www.bostonplans.o 2; https://www.bostonplans.o 2 |
| RESUBMITTED_PLANS_UNLIKELY | category | 2 | 0 | f 8.7K; t 1.3K |
| RESUBMITTED_PLANS_LIKELY | category | 2 | 0 | f 9.9K; t 77 |
| X_LONGITUDE | amount | 6.2K | 0 | -71.07513000164919 56; -71.06721126818432 54; -71.04255000074501 53; -71.16922269257971 51 |
| Y_LATITUDE | amount | 6.2K | 0 | 42.34921000046016 56; 42.327950038070824 54; 42.34556999997615 53; 42.26578377822917 51 |
| PARCEL_ID | other | 5.9K | 0 | 0401134000 56; 0801023000 54; 0602825000 53; 0102280000, 0102280100 53 |
| SAM_ID | other | 6.3K | 13 | 33209 56; 167483 54; 45546 53; 140325 51 |
| ZIP_CODE | category | 31 | 0 | 02127 794; 02128 734; 02116 711; 02124 494 |
| CENSUS_TRACT | amount | 196 | 0 | 701.04 376; 303.02 242; 107.02 186; 106 173 |
| CENSUS_BLOCK_GROUP | category | 7 | 0 | 1 3.8K; 2 3.2K; 3 1.7K; 4 810 |
| GEOM_POINT_4326 | other | 6.3K | 0 | 0101000020E6100000070211E 56; 0101000020E61000008FB17D3 54; 0101000020E61000004169A32 53; 0101000020E6100000BD976A8 51 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:52:49.60490 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3558ff79-42ec-4101-9561-8 10.0K |
| SRC_SHA256 | who | 1 | 0 | 48752026566407fe15cb7f7ce 10.0K |
