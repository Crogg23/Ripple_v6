# PORTAL_SOC_CONNECTICUT_OPEN_7909C84EE4

rows 22  columns 14  scan 2.0s

roles: audit 2, category 11, date 1, who 1

## when

INGESTED_AT
  2026        22  ##############################

## who

SRC_SHA256 by rows
        22  a4b49fec22c353f923e83bb0cb8b3d744341d8153ca8d27a82a2b552a39f8a6a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  a4b49fec22c353f923e83bb0cb8b3d744341d815  2026:22

## what

NAICS_CODE: nan 15%, 999999 8%, 81-92 8%, 72 8%, 71 8%, 61-62 8%, 56 8%, 55 8%, 54 8%, 53 8%, 52 8%, 51 8%

NAICS_INDUSTRY_GROUP: nan 9%, Not Yet Assigned 9%, Other Services 9%, Accomodation and Food Services 9%, Arts, Entertainment, and Recre 9%, Education, Health Care and Soc 9%, Administrative and Support Ser 9%, Management of Companies and En 9%, Professional, Scientific and T 9%, Real Estate and Rental and Lea 9%, Finance and Insurance 9%

DIGITAL_ANIMATION: 0 73%, nan 14%, 6875794 5%, 700000 5%, 634131 5%

ELECTRONIC_DATA_PROCESSING: nan 21%, 1450456 7%, 787157 7%, 12117 7%, 229079 7%, 511738 7%, 42358 7%, 2597617 7%, 294456 7%, 64696 7%, 11780908 7%, 1738237 7%

FILM_PRODUCTION: 0 45%, nan 14%, 140000 5%, 6577195 5%, 554872 5%, 78389 5%, 22051553 5%, 1038528 5%, 381366 5%, 1206305 5%, 8196977 5%

FILM_PRODUCTION_INFRASTRUCTURE: 0 59%, nan 14%, 1340154 5%, 514682 5%, 2062 5%, 15598778 5%, 13515014 5%, 21593 5%

FIXED_CAPITAL: nan 21%, 4821526 7%, 180418 7%, 177019 7%, 475519 7%, 734344 7%, 520912 7%, 13478978 7%, 1191866 7%, 166016 7%, 626097 7%, 14113622 7%

JOB_EXPANSION: 0 45%, nan 14%, 2764 5%, 30000 5%, 536943 5%, 52784 5%, 263830 5%, 15000 5%, 911500 5%, 3638996 5%, 11429 5%

RESEARCH_DEVELOPMENT: 0 24%, nan 18%, 219396 6%, 126334 6%, 142110 6%, 60723 6%, 543360 6%, 2029082 6%, 1646 6%, 13865 6%, 168158 6%, 9217 6%

RESEARCH_EXPERIMENTAL: nan 19%, 0 19%, 1300576 6%, 121222 6%, 30379 6%, 72311 6%, 733341 6%, 1443877 6%, 3718192 6%, 47088 6%, 62892 6%, 2211151 6%

URBAN_INDUSTRIAL_SITE_REINVESTMENT: 0 45%, nan 14%, 3125446 5%, 51080000 5%, 105243 5%, 9521495 5%, 2139569 5%, 1069253 5%, 1324862 5%, 835664 5%, 6600000 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAICS_CODE | category | 21 | 0 | nan 2; 999999 1; 81-92 1; 72 1 |
| NAICS_INDUSTRY_GROUP | category | 22 | 1 | nan 1; Not Yet Assigned 1; Other Services 1; Accomodation and Food Ser 1 |
| DIGITAL_ANIMATION | category | 5 | 0 | 0 16; nan 3; 6875794 1; 700000 1 |
| ELECTRONIC_DATA_PROCESSING | category | 20 | 0 | nan 3; 1450456 1; 787157 1; 12117 1 |
| FILM_PRODUCTION | category | 11 | 0 | 0 10; nan 3; 140000 1; 6577195 1 |
| FILM_PRODUCTION_INFRASTRUCTURE | category | 8 | 0 | 0 13; nan 3; 1340154 1; 514682 1 |
| FIXED_CAPITAL | category | 20 | 0 | nan 3; 4821526 1; 180418 1; 177019 1 |
| JOB_EXPANSION | category | 11 | 0 | 0 10; nan 3; 2764 1; 30000 1 |
| RESEARCH_DEVELOPMENT | category | 17 | 0 | 0 4; nan 3; 219396 1; 126334 1 |
| RESEARCH_EXPERIMENTAL | category | 18 | 0 | nan 3; 0 3; 1300576 1; 121222 1 |
| URBAN_INDUSTRIAL_SITE_REINVESTMENT | category | 11 | 0 | 0 10; nan 3; 3125446 1; 51080000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:47:16.90047 22 |
| SOURCE_RUN_ID | audit | 1 | 0 | dfc94555-de44-46d4-a660-5 22 |
| SRC_SHA256 | who | 1 | 0 | a4b49fec22c353f923e83bb0c 22 |
