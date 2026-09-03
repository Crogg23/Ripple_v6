# PORTAL_CKA_WESTERN_PENNSYLV_34DD959083

rows 10.0K  columns 11  scan 3.7s

roles: audit 2, category 4, date 1, other 2, who 3

## when

INGESTED_AT
  2026     10.0K  ##############################

## who

GEO_AREA_NAME by rows
        96  X-Unassigned
        60  District 7
        54  Crafton
        54  South Versailles
        54  Sewickley
        54  Baldwin Borough
        54  Ben Avon Heights
        54  State House 019
        54  State House 023
        54  State House 040
        54  District 4
        54  Frazer
        54  State House 027
        54  Carnegie
        54  Bridgeville
        54  State House 028
        54  Kilbuck
        54  Blawnox
        54  Council District 2
        54  Baldwin Township

REPORT_GROUP by rows
     10.0K  Community Trends

SRC_SHA256 by rows
     10.0K  35a74bd96cff825243e415c2d81079eb0471110157056e7d84df9d432566c8e6

## who x when

GEO_AREA_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Baldwin Borough                           2026:54
  Baldwin Township                          2026:54
  Ben Avon Heights                          2026:54
  Blawnox                                   2026:54
  Bridgeville                               2026:54
  Carnegie                                  2026:54
  Council District 2                        2026:54
  Crafton                                   2026:54
  District 4                                2026:54
  District 7                                2026:60
  Frazer                                    2026:54
  Kilbuck                                   2026:54
  Sewickley                                 2026:54
  South Versailles                          2026:54
  State House 019                           2026:54
  State House 023                           2026:54
  State House 027                           2026:54
  State House 028                           2026:54
  State House 040                           2026:54
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
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:44:30.98827 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 6546a230-1b42-487c-beb1-a 10.0K |
| SRC_SHA256 | who | 1 | 0 | 35a74bd96cff825243e415c2d 10.0K |
