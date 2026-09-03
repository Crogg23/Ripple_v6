# PORTAL_SOC_NEW_YORK_STATE_O_1C387B0AE6

rows 2.0K  columns 8  scan 2.3s

roles: audit 2, category 4, date 1, id 1, who 1

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

SRC_SHA256 by rows
      2.0K  24a6eadbf248fb503d5255cca6c4061f5d3173c5bbe7a12895953670dc6dccea

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  24a6eadbf248fb503d5255cca6c4061f5d3173c5  2026:2.0K

## what

YEAR: 2023 13%, 2024 13%, 2017 12%, 2018 12%, 2019 12%, 2020 12%, 2021 12%, 2022 12%, 2016 6%

REGION: Mid-Hudson 9%, Long Island 9%, Finger Lakes 9%, Central New York 9%, Capital Region 9%, Mohawk Valley 9%, Western New York 8%, Southern Tier 8%, North Country 8%, New York City 8%, New York, area not reported 7%, New York 3%

NAICS_CODE: 31-33 8%, 23 8%, 22 8%, 21 8%, 11 8%, 99 8%, 90 8%, 81 8%, 72 8%, 71 8%, 62 8%, 61 8%

INDUSTRY: Manufacturing 8%, Construction 8%, Utilities 8%, Mining, Quarrying, and Oil and 8%, Agriculture, Forestry, Fishing 8%, Unclassified Industry 8%, Government 8%, Other Services (except Public  8%, Accommodation and Food Service 8%, Arts, Entertainment, and Recre 8%, Health Care and Social Assista 8%, Educational Services 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 9 | 0 | 2023 252; 2024 252; 2017 231; 2018 231 |
| REGION | category | 12 | 0 | Mid-Hudson 189; Long Island 189; Finger Lakes 189; Central New York 189 |
| NAICS_CODE | category | 21 | 0 | 31-33 96; 23 96; 22 96; 21 96 |
| INDUSTRY | category | 21 | 0 | Manufacturing 96; Construction 96; Utilities 96; Mining, Quarrying, and Oi 96 |
| JOBS | id | 2.0K | 0 | 17762 10; 4774 10; 612 10; 278 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:42:34.87114 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9ad9607d-25bf-4c8d-b5f1-9 2.0K |
| SRC_SHA256 | who | 1 | 0 | 24a6eadbf248fb503d5255cca 2.0K |
