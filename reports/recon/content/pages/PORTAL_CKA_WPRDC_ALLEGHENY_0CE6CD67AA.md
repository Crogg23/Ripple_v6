# PORTAL_CKA_WPRDC_ALLEGHENY_0CE6CD67AA

rows 10.0K  columns 11  scan 2.8s

roles: audit 2, category 4, date 1, other 2, who 3

## when

INGESTED_AT
  2026     10.0K  ##############################

## who

GEO_AREA_NAME by rows
        96  X-Unassigned
        60  District 7
        54  District 3
        54  Braddock
        54  District 12
        54  Etna
        54  Elizabeth Township
        54  East Deer
        54  Congress District 17
        54  McDonald
        54  Harrison
        54  Mount Oliver
        54  Pleasant Hills
        54  Harmar
        54  Council District 4
        54  Cheswick
        54  Pine
        54  District 2
        54  District 10
        54  Council District 1

REPORT_GROUP by rows
     10.0K  Community Trends

SRC_SHA256 by rows
     10.0K  35a74bd96cff825243e415c2d81079eb0471110157056e7d84df9d432566c8e6

## who x when

GEO_AREA_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Braddock                                  2026:54
  Cheswick                                  2026:54
  Congress District 17                      2026:54
  Council District 1                        2026:54
  Council District 4                        2026:54
  District 10                               2026:54
  District 12                               2026:54
  District 2                                2026:54
  District 3                                2026:54
  District 7                                2026:60
  East Deer                                 2026:54
  Elizabeth Township                        2026:54
  Etna                                      2026:54
  Harmar                                    2026:54
  Harrison                                  2026:54
  McDonald                                  2026:54
  Mount Oliver                              2026:54
  Pine                                      2026:54
  Pleasant Hills                            2026:54
  X-Unassigned                              2026:96

REPORT_GROUP by INGESTED_AT  LOAD STAMP, not an event date
  Community Trends                          2026:10.0K

## what

METRIC_NAME: Jail Population 11%, Individuals Receiving Income S 11%, Suicides 11%, Homeless Population 11%, Involuntary Commitments 11%, Mental Health Crises 11%, Homicides 11%, Children in Care 11%, Overdoses 11%

CALENDAR_YEAR: 2021 17%, 2026 17%, 2025 17%, 2024 17%, 2023 17%, 2022 17%

POPULATION_NAME: Total Population 46%, NA 31%, Adults 18 and Over 8%, Individuals 15 and Over 8%, Children Under 18 8%

ACS_5_YR_EST: 2023 67%, 2021 17%, 2022 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| METRIC_NAME | category | 9 | 0 | Jail Population 1.1K; Individuals Receiving Inc 1.1K; Suicides 1.1K; Homeless Population 1.1K |
| REPORT_GROUP | who | 1 | 0 | Community Trends 10.0K |
| CALENDAR_YEAR | category | 6 | 0 | 2021 1.7K; 2026 1.7K; 2025 1.7K; 2024 1.7K |
| KPI_COUNT | other | 1.4K | 4.4K | 6 240; 7 184; 8 157; 10 147 |
| GEO_AREA_NAME | who | 213 | 0 | X-Unassigned 96; District 7 60; State Senate 45 54; State Senate 43 54 |
| POPULATION_NAME | category | 5 | 0 | Total Population 4.6K; NA 3.0K; Adults 18 and Over 786; Individuals 15 and Over 786 |
| ACS_5_YR_EST | category | 3 | 0 | 2023 6.7K; 2021 1.7K; 2022 1.7K |
| KPI_POPULATION | other | 1.4K | 3.1K | 1515 37; 3355 37; 396 37; 13686 37 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:44:00.04447 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4a11d3b1-36ef-4a64-9290-0 10.0K |
| SRC_SHA256 | who | 1 | 0 | 35a74bd96cff825243e415c2d 10.0K |
