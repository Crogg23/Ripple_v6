# PORTAL_SOC_CONNECTICUT_OPEN_886AEF6AC6

rows 20  columns 14  scan 1.9s

roles: audit 2, category 11, date 1, who 1

## when

INGESTED_AT
  2026        20  ##############################

## who

SRC_SHA256 by rows
        20  3f5a9db2c30ebb1e3dd6886a1d76457aab864c2f2f4ecf4ef7d0a6e48f5324a4

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  3f5a9db2c30ebb1e3dd6886a1d76457aab864c2f  2026:20

## what

NAICS_CODE: nan 8%, 999999 8%, 81-92 8%, 72 8%, 71 8%, 61-62 8%, 56 8%, 55 8%, 54 8%, 53 8%, 52 8%, 51 8%

NAICS_INDUSTRY_GROUP: nan 8%, Not Yet Assigned 8%, Other Services 8%, Accommodation and Food Service 8%, Arts, Entertainment, and Recre 8%, Education, Health Care and Soc 8%, Administrative and Support Ser 8%, Management of Companies and En 8%, Professional, Scientific and T 8%, Real Estate and Rental and Lea 8%, Finance and Insurance 8%, Information 8%

DIGITAL_ANIMATION: 0 80%, nan 5%, 13332559 5%, 3074419 5%, 528394 5%

ELECTRONIC_DATA_PROCESSING: nan 8%, 372162 8%, 102520 8%, 2485 8%, 10028 8%, 1936971 8%, 426090 8%, 1293309 8%, 328746 8%, 79468 8%, 8603619 8%, 6646185 8%

FILM_PRODUCTION: 0 45%, nan 5%, 700000 5%, 12250303 5%, 1906912 5%, 124521 5%, 22832991 5%, 9495135 5%, 217271 5%, 489461 5%, 100000 5%, 4674045 5%

FILM_INFRASTRUCTURE: 0 85%, nan 5%, 793426 5%, 525581 5%

FIXED_CAP_INVESTMENT: nan 8%, 4094336 8%, 196368 8%, 110314 8%, 145555 8%, 736159 8%, 146013 8%, 9932247 8%, 1728040 8%, 225766 8%, 870454 8%, 16077767 8%

JOB_EXPANSION: 0 65%, nan 5%, 438 5%, 21203 5%, 196593 5%, 980 5%, 46723 5%, 7500 5%

RESEARCH_DEVELOPMENT: 0 39%, nan 6%, 209665 6%, 335 6%, 14994 6%, 25449 6%, 251643 6%, 726208 6%, 6647 6%, 23692 6%, 31028 6%, 8351 6%

RESEARCH_EXPERIMENTATION: 0 27%, nan 7%, 203940 7%, 91280 7%, 9870 7%, 453557 7%, 1173252 7%, 133172 7%, 4444705 7%, 87404 7%, 356940 7%, 1063223 7%

URBAN_INDUSTRIAL_SITE_REINVESTMENT: 0 55%, nan 5%, 279362 5%, 241515 5%, 2234772 5%, 627281 5%, 294627 5%, 2680336 5%, 635919 5%, 3093205 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAICS_CODE | category | 20 | 0 | nan 1; 999999 1; 81-92 1; 72 1 |
| NAICS_INDUSTRY_GROUP | category | 20 | 0 | nan 1; Not Yet Assigned 1; Other Services 1; Accommodation and Food Se 1 |
| DIGITAL_ANIMATION | category | 5 | 0 | 0 16; nan 1; 13332559 1; 3074419 1 |
| ELECTRONIC_DATA_PROCESSING | category | 18 | 0 | nan 1; 372162 1; 102520 1; 2485 1 |
| FILM_PRODUCTION | category | 12 | 0 | 0 9; nan 1; 700000 1; 12250303 1 |
| FILM_INFRASTRUCTURE | category | 4 | 0 | 0 17; nan 1; 793426 1; 525581 1 |
| FIXED_CAP_INVESTMENT | category | 20 | 0 | nan 1; 4094336 1; 196368 1; 110314 1 |
| JOB_EXPANSION | category | 8 | 0 | 0 13; nan 1; 438 1; 21203 1 |
| RESEARCH_DEVELOPMENT | category | 14 | 0 | 0 7; nan 1; 209665 1; 335 1 |
| RESEARCH_EXPERIMENTATION | category | 17 | 0 | 0 4; nan 1; 203940 1; 91280 1 |
| URBAN_INDUSTRIAL_SITE_REINVESTMENT | category | 10 | 0 | 0 11; nan 1; 279362 1; 241515 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:46:20.45751 20 |
| SOURCE_RUN_ID | audit | 1 | 0 | eb854f4d-cded-4de7-8ed7-7 20 |
| SRC_SHA256 | who | 1 | 0 | 3f5a9db2c30ebb1e3dd6886a1 20 |
