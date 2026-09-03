# PORTAL_SOC_CONNECTICUT_OPEN_55FF4E7BA7

rows 23  columns 13  scan 4.6s

roles: amount 6, audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        23  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| DIGITAL_ANIMATION | 20 | 0 | 0 | 17.54M | 18.00M | 36.00M |
| FILM_PRODUCTION_INFRASTRUCTURE | 20 | 0 | 0 | 11.53M | 11.79M | 23.58M |
| FIXED_CAPITAL | 20 | 9.8K | 1.15M | 68.10M | 76.10M | 152.20M |
| JOB_EXPANSION | 20 | 0 | 0 | 237.9K | 251.9K | 503.8K |
| RESEARCH_DEVELOPMENT | 20 | 0 | 69.9K | 64.70M | 65.02M | 130.05M |
| RESEARCH_EXPERIMENTAL | 20 | 0 | 84.7K | 21.16M | 22.40M | 44.79M |

## who

SRC_SHA256 by rows
        23  bc9152ef4f4c62702aec568c7589a70e4e65075d945754eea26348aa51302417

SRC_SHA256 by dollars
      36.00M       23 rows  bc9152ef4f4c62702aec568c7589a70e4e65075d945754eea26348aa5130

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = DIGITAL_ANIMATION
  bc9152ef4f4c62702aec568c7589a70e4e65075d  2026:36.00M

## what

NAICS_CODE_AND_INDUSTRY_GROUP: nan 21%, Total  7%, 999999 Not Yet Assigned 7%, 81-92 Other Services 7%, 72 Accomodation and Food Servi 7%, 71 Arts, Entertainment, and Re 7%, 61-62 Education, Health Care a 7%, 56 Administrative and Support  7%, 55 Management of Companies and 7%, 54 Professional, Scientific an 7%, 53 Real Estate and Rental and  7%, 52 Finance and Insurance 7%

ELECTRONIC_DATA_PROCESSING: $24,420,390 9%, 331,174 9%, 158,990 9%, 7,484 9%, 150,133 9%, 561,376 9%, 97,104 9%, 3,628,713 9%, 354,743 9%, 62,954 9%, 12,667,674 9%

FILM_PRODUCTION: 0 42%, nan 11%, $53,809,044 5%, 796,332 5%, 3,185,400 5%, 8,631,230 5%, 1,478,820 5%, 3,273 5%, 31,014,817 5%, 7,143,610 5%, 170,784 5%

URBAN_INDUSTRIAL_SITE_REINVESTMENT: 0 57%, nan 5%, $40,018,416 5%, 33,288,576 5%, 29,442 5%, 4,789,137 5%, 657,254 5%, 36,828 5%, 669,975 5%, 547,204 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAICS_CODE_AND_INDUSTRY_GROUP | category | 21 | 0 | nan 3; Total  1; 999999 Not Yet Assigned 1; 81-92 Other Services 1 |
| DIGITAL_ANIMATION | amount | 9 | 0 | 0.00 13; nan 3; 18001907.00 1; 661876.00 1 |
| ELECTRONIC_DATA_PROCESSING | category | 21 | 3 | $24,420,390 1; 331,174 1; 158,990 1; 7,484 1 |
| FILM_PRODUCTION | category | 15 | 1 | 0 8; nan 2; $53,809,044 1; 796,332 1 |
| FILM_PRODUCTION_INFRASTRUCTURE | amount | 8 | 0 | 0.00 14; nan 3; 11791044.00 1; 55490.00 1 |
| FIXED_CAPITAL | amount | 21 | 0 | nan 3; 76100484.00 1; 3923601.00 1; 157905.00 1 |
| JOB_EXPANSION | amount | 7 | 0 | 0.00 15; nan 3; 251886.00 1; 25740.00 1 |
| RESEARCH_DEVELOPMENT | amount | 17 | 0 | 0.00 5; nan 3; 65024871.00 1; 244751.00 1 |
| RESEARCH_EXPERIMENTAL | amount | 19 | 0 | nan 3; 0.00 3; 22396937.00 1; 946014.00 1 |
| URBAN_INDUSTRIAL_SITE_REINVESTMENT | category | 11 | 2 | 0 12; nan 1; $40,018,416 1; 33,288,576 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:47:05.34889 23 |
| SOURCE_RUN_ID | audit | 1 | 0 | d13b18ac-69b0-4048-8052-d 23 |
| SRC_SHA256 | who | 1 | 0 | bc9152ef4f4c62702aec568c7 23 |
