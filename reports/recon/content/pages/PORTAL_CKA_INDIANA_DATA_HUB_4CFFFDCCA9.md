# PORTAL_CKA_INDIANA_DATA_HUB_4CFFFDCCA9

rows 77  columns 6  scan 3.1s

roles: audit 2, category 1, date 1, other 1, who 2

## when

INGESTED_AT
  2026        77  ##############################

## who

COLUMN_NAME by rows
         6  Id
         3  FishSurveyId
         2  WaterbodyName
         2  SpeciesName
         2  Latitude
         2  County
         2  WaterbodyId
         2  StartDate
         2  ScientificName
         2  WaterbodyType
         2  Longitude
         2  GearId
         1  TotalWeightLb
         1  EndDate
         1  PhBottom
         1  MinLengthIn
         1  owner_type
         1  district
         1  EffortUnit
         1  DepthFt

SRC_SHA256 by rows
        77  d1a064c003dc0431edb42fa53d534a1f691c5cfcfc5f1d11d97e9376d3325129

## who x when

COLUMN_NAME by INGESTED_AT  LOAD STAMP, not an event date
  County                                    2026:2
  DepthFt                                   2026:1
  EffortUnit                                2026:1
  EndDate                                   2026:1
  FishSurveyId                              2026:3
  GearId                                    2026:2
  Id                                        2026:6
  Latitude                                  2026:2
  Longitude                                 2026:2
  MinLengthIn                               2026:1
  PhBottom                                  2026:1
  ScientificName                            2026:2
  SpeciesName                               2026:2
  StartDate                                 2026:2
  TotalWeightLb                             2026:1
  WaterbodyId                               2026:2
  WaterbodyName                             2026:2
  WaterbodyType                             2026:2
  district                                  2026:1
  owner_type                                2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  d1a064c003dc0431edb42fa53d534a1f691c5cfc  2026:77

## what

FILE: Waterbodies 21%, Water_Quality_Surveys 17%, Fish_Gear 14%, Fish_Records 14%, Fish_Surveys 13%, Batch_Fish_Records 12%, Water_Quality_Records 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FILE | category | 7 | 0 | Waterbodies 16; Water_Quality_Surveys 13; Fish_Gear 11; Fish_Records 11 |
| COLUMN_NAME | who | 60 | 0 | Id 6; FishSurveyId 3; Longitude 2; Latitude 2 |
| DESCRIPTION | other | 63 | 0 | Unique Id for associated  4; Waterbody name 3; Record location. Longitud 2; Record location. Latitude 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:13:51.99384 77 |
| SOURCE_RUN_ID | audit | 1 | 0 | 63b6e98a-7386-4cf9-b841-b 77 |
| SRC_SHA256 | who | 1 | 0 | d1a064c003dc0431edb42fa53 77 |
