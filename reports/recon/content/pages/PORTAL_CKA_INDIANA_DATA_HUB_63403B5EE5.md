# PORTAL_CKA_INDIANA_DATA_HUB_63403B5EE5

rows 77  columns 6  scan 2.9s

roles: audit 2, category 1, date 1, other 1, who 2

## when

INGESTED_AT
  2026        77  ##############################

## who

COLUMN_NAME by rows
         6  Id
         3  FishSurveyId
         2  StartDate
         2  SpeciesName
         2  Longitude
         2  Latitude
         2  ScientificName
         2  WaterbodyId
         2  WaterbodyName
         2  GearId
         2  WaterbodyType
         2  County
         1  AlkalinityBottomPPM
         1  MaxLengthIn
         1  AgeYrs
         1  TotalWeightLb
         1  LengthIn
         1  district
         1  ConductivitymSv
         1  aread_m2

SRC_SHA256 by rows
        77  d1a064c003dc0431edb42fa53d534a1f691c5cfcfc5f1d11d97e9376d3325129

## who x when

COLUMN_NAME by INGESTED_AT  LOAD STAMP, not an event date
  AgeYrs                                    2026:1
  AlkalinityBottomPPM                       2026:1
  ConductivitymSv                           2026:1
  County                                    2026:2
  FishSurveyId                              2026:3
  GearId                                    2026:2
  Id                                        2026:6
  Latitude                                  2026:2
  LengthIn                                  2026:1
  Longitude                                 2026:2
  MaxLengthIn                               2026:1
  ScientificName                            2026:2
  SpeciesName                               2026:2
  StartDate                                 2026:2
  TotalWeightLb                             2026:1
  WaterbodyId                               2026:2
  WaterbodyName                             2026:2
  WaterbodyType                             2026:2
  aread_m2                                  2026:1
  district                                  2026:1

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
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:14:02.09836 77 |
| SOURCE_RUN_ID | audit | 1 | 0 | 06d910e9-f1b6-43eb-9272-4 77 |
| SRC_SHA256 | who | 1 | 0 | d1a064c003dc0431edb42fa53 77 |
