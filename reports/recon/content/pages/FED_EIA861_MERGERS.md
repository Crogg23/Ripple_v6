# FED_EIA861_MERGERS

rows 4  columns 13  scan 2.2s

roles: audit 2, category 8, date 2, other 1, who 1

## when

C_03_01_2024
  2024         4  ##############################

_INGESTED_AT
  2026         4  ##############################

## who

_SRC_FILE by rows
         4  Mergers_2024.xlsx

## who x when

_SRC_FILE by C_03_01_2024
  Mergers_2024.xlsx                         2024:4

## what

C_6389: 66101 25%, 64929 25%, 59062 25%, 6458 25%

ENERGY_HARBOR_GENERATION_LLC: FirstEnergy Pennsylvania Elect 25%, Good Charlie & Co., LLC 25%, Horizon Power and Light, LLC 25%, Energy Harbor Corp. 25%

VISTRA_CORP: see footnotes 33%, Federal Power & Gas LLC 33%, Vistra Corp 33%

VISTRA_CORP_1: see footnotes 25%, Champion Energy Marketing, LLC 25%, Federal Power & Gas LLC 25%, Vistra Corp 25%

C_6555_SIERRA_DR: 341 White Pond Dr. 25%, 1500 Rankin Road Suite 200 25%, 539 W. Commerce St #779 25%, 6555 Sierra Drive 25%

IRVING: Akron 25%, Houston 25%, Dallas 25%, Irving 25%

TX: TX 75%, OH 25%

C_75039: 44320 25%, 77073 25%, 75208 25%, 75039 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| C_2024 | other | 1 | 0 | 2024 4 |
| C_6389 | category | 4 | 0 | 66101 1; 64929 1; 59062 1; 6458 1 |
| ENERGY_HARBOR_GENERATION_LLC | category | 4 | 0 | FirstEnergy Pennsylvania  1; Good Charlie & Co., LLC 1; Horizon Power and Light,  1; Energy Harbor Corp. 1 |
| C_03_01_2024 | date | 4 | 0 | 01/01/2024 1; 11/20/2024 1; 06/01/2024 1; 03/01/2024 1 |
| VISTRA_CORP | category | 3 | 1 | see footnotes 1; Federal Power & Gas LLC 1; Vistra Corp 1 |
| VISTRA_CORP_1 | category | 4 | 0 | see footnotes 1; Champion Energy Marketing 1; Federal Power & Gas LLC 1; Vistra Corp 1 |
| C_6555_SIERRA_DR | category | 4 | 0 | 341 White Pond Dr. 1; 1500 Rankin Road Suite 20 1; 539 W. Commerce St #779 1; 6555 Sierra Drive 1 |
| IRVING | category | 4 | 0 | Akron 1; Houston 1; Dallas 1; Irving 1 |
| TX | category | 2 | 0 | TX 3; OH 1 |
| C_75039 | category | 4 | 0 | 44320 1; 77073 1; 75208 1; 75039 1 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:39:20.07759 4 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 61ffd0ce-3f01-4721-9f6f-b 4 |
| _SRC_FILE | who | 1 | 0 | Mergers_2024.xlsx 4 |
