# PORTAL_SOC_CONNECTICUT_OPEN_28F32B559B

rows 21  columns 14  scan 2.0s

roles: audit 2, category 11, date 1, who 1

## when

INGESTED_AT
  2026        21  ##############################

## who

SRC_SHA256 by rows
        21  b7d5fb56952eee19a3cf11be21b8cea79425bea34cfa47cb771bf7227ef230d6

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  b7d5fb56952eee19a3cf11be21b8cea79425bea3  2026:21

## what

NAICS_CODE: nan 15%, 999999 8%, 81-92 8%, 72 8%, 71 8%, 61-62 8%, 56 8%, 55 8%, 54 8%, 53 8%, 52 8%, 51 8%

NAICS_INDUSTRY_GROUP: nan 9%, Not Yet Assigned 9%, Other Services 9%, Accommodation and Food Service 9%, Arts, Entertainment, and Recre 9%, Education, Health Care and Soc 9%, Administrative and Support Ser 9%, Management of Companies and En 9%, Professional, Scientific and T 9%, Real Estate and Rental and Lea 9%, Finance and Insurance 9%

DIGITAL_ANIMATION: 0 81%, nan 10%, 15445835 5%, 685167 5%

ELECTRONIC_DATA_PROCESSING: nan 15%, 581810 8%, 114625 8%, 15877 8%, 11298 8%, 428916 8%, 400068 8%, 2015587 8%, 354467 8%, 71043 8%, 9047969 8%, 10047521 8%

FILM_PRODUCTION: 0 52%, nan 10%, 1182652 5%, 152279 5%, 24074932 5%, 10006049 5%, 255213 5%, 4570869 5%, 570718 5%, 9222352 5%

FILM_INFRASTRUCTURE: 0 81%, nan 10%, 8057516 5%, 1478407 5%

FIXED_CAP_INVESTMENT: nan 15%, 5079275 8%, 223138 8%, 146044 8%, 914543 8%, 379819 8%, 275472 8%, 15425753 8%, 1442260 8%, 114239 8%, 1428665 8%, 6303836 8%

JOB_EXPANSION: 0 29%, nan 12%, 14782 6%, 4563 6%, 19500 6%, 1469 6%, 7000 6%, 40500 6%, 487899 6%, 2461 6%, 240845 6%, 61900 6%

RESEARCH_DEVELOPMENT: 0 29%, nan 12%, 270841 6%, 687 6%, 11316 6%, 190873 6%, 569923 6%, 378272 6%, 8916 6%, 61030 6%, 13913 6%, 311469 6%

RESEARCH_EXPERIMENTATION: 0 20%, nan 13%, 1303949 7%, 118240 7%, 16535 7%, 323146 7%, 951247 7%, 1856891 7%, 4658387 7%, 74280 7%, 3226 7%, 369805 7%

URBAN_INDUSTRIAL_SITE_REINVESTMENT: 0 43%, nan 10%, 4115601 5%, 33600000 5%, 358485 5%, 4423325 5%, 1622704 5%, 1200000 5%, 2806113 5%, 728895 5%, 1771435 5%, 7500000 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAICS_CODE | category | 20 | 0 | nan 2; 999999 1; 81-92 1; 72 1 |
| NAICS_INDUSTRY_GROUP | category | 21 | 1 | nan 1; Not Yet Assigned 1; Other Services 1; Accommodation and Food Se 1 |
| DIGITAL_ANIMATION | category | 4 | 0 | 0 17; nan 2; 15445835 1; 685167 1 |
| ELECTRONIC_DATA_PROCESSING | category | 20 | 0 | nan 2; 581810 1; 114625 1; 15877 1 |
| FILM_PRODUCTION | category | 10 | 0 | 0 11; nan 2; 1182652 1; 152279 1 |
| FILM_INFRASTRUCTURE | category | 4 | 0 | 0 17; nan 2; 8057516 1; 1478407 1 |
| FIXED_CAP_INVESTMENT | category | 20 | 0 | nan 2; 5079275 1; 223138 1; 146044 1 |
| JOB_EXPANSION | category | 16 | 0 | 0 5; nan 2; 14782 1; 4563 1 |
| RESEARCH_DEVELOPMENT | category | 16 | 0 | 0 5; nan 2; 270841 1; 687 1 |
| RESEARCH_EXPERIMENTATION | category | 18 | 0 | 0 3; nan 2; 1303949 1; 118240 1 |
| URBAN_INDUSTRIAL_SITE_REINVESTMENT | category | 12 | 0 | 0 9; nan 2; 4115601 1; 33600000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:46:08.88620 21 |
| SOURCE_RUN_ID | audit | 1 | 0 | e17b06f9-8ee0-42bb-8c35-8 21 |
| SRC_SHA256 | who | 1 | 0 | b7d5fb56952eee19a3cf11be2 21 |
