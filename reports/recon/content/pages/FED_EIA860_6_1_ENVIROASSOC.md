# FED_EIA860_6_1_ENVIROASSOC

rows 7.0K  columns 10  scan 3.4s

roles: audit 2, category 1, date 1, other 4, who 3

## when

_INGESTED_AT
  2026      7.0K  ##############################

## who

PLANT_NAME by rows
       123  Tennessee Eastman Operations
        75  University of Illinois Abbott Power Plt
        66  RED-Rochester, LLC
        63  Archer Daniels Midland Decatur
        56  Celanese Acetate LLC
        56  Archer Daniels Midland Clinton
        50  Whiting Refinery
        50  Archer Daniels Midland Peoria
        48  Longview Fibre
        47  Clewiston Sugar House
        45  MU Combined Heat and Power Plant
        44  Radford Army Ammunition Plant
        43  Motiva Enterprises Port Arthur Refinery
        42  Genesis Alkali
        41  Havana
        41  Consumer Operations LLC
        40  University of Notre Dame
        39  Covington Facility
        38  International Paper Franklin Mill
        38  ExxonMobil Beaumont Refinery

UTILITY_NAME by rows
       151  Archer Daniels Midland Co
       123  Eastman Chemical Co-TN Ops
        88  Tennessee Valley Authority
        84  Florida Power & Light Co
        75  University of Illinois
        71  United States Sugar Corp
        66  RED-Rochester, LLC
        63  Virginia Electric & Power Co
        61  Cleveland Cliffs
        60  Interstate Power and Light Co
        59  Entergy Louisiana LLC
        59  Dynegy Midwest Generation Inc
        56  Celanese Acetate LLC
        51  Georgia Power Co
        50  BP PLC
        50  BioUrja Renewables LLC
        48  Longview Fibre Co
        47  Wheelabrator Environmental Systems
        46  ExxonMobil Oil Corp
        45  Curators of the University of Missouri

_SRC_FILE by rows
      7.0K  6_1_EnviroAssoc_Y2024.xlsx

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  Archer Daniels Midland Clinton            2026:56
  Archer Daniels Midland Decatur            2026:63
  Archer Daniels Midland Peoria             2026:50
  Celanese Acetate LLC                      2026:56
  Clewiston Sugar House                     2026:47
  Consumer Operations LLC                   2026:41
  Covington Facility                        2026:39
  ExxonMobil Beaumont Refinery              2026:38
  Genesis Alkali                            2026:42
  Havana                                    2026:41
  International Paper Franklin Mill         2026:38
  Longview Fibre                            2026:48
  MU Combined Heat and Power Plant          2026:45
  Motiva Enterprises Port Arthur Refinery   2026:43
  RED-Rochester, LLC                        2026:66
  Radford Army Ammunition Plant             2026:44
  Tennessee Eastman Operations              2026:123
  University of Illinois Abbott Power Plt   2026:75
  University of Notre Dame                  2026:40
  Whiting Refinery                          2026:50

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  Archer Daniels Midland Co                 2026:151
  BP PLC                                    2026:50
  BioUrja Renewables LLC                    2026:50
  Celanese Acetate LLC                      2026:56
  Cleveland Cliffs                          2026:61
  Curators of the University of Missouri    2026:45
  Dynegy Midwest Generation Inc             2026:59
  Eastman Chemical Co-TN Ops                2026:123
  Entergy Louisiana LLC                     2026:59
  ExxonMobil Oil Corp                       2026:46
  Florida Power & Light Co                  2026:84
  Georgia Power Co                          2026:51
  Interstate Power and Light Co             2026:60
  Longview Fibre Co                         2026:48
  RED-Rochester, LLC                        2026:66
  Tennessee Valley Authority                2026:88
  United States Sugar Corp                  2026:71
  University of Illinois                    2026:75
  Virginia Electric & Power Co              2026:63
  Wheelabrator Environmental Systems        2026:47

## what

STEAM_PLANT_TYPE: 2 39%, 1 37%, 4 18%, 3 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 934 | 0 | 772 158; 5610 133; 19528 92; 18642 88 |
| UTILITY_NAME | who | 905 | 1 | Archer Daniels Midland Co 158; Eastman Chemical Co-TN Op 133; University of Illinois 91; Tennessee Valley Authorit 88 |
| PLANT_CODE | other | 1.6K | 1 | 50481 136; 54780 93; 10025 76; 10865 75 |
| PLANT_NAME | who | 1.6K | 1 | Tennessee Eastman Operati 136; University of Illinois Ab 93; RED-Rochester, LLC 76; Archer Daniels Midland De 75 |
| BOILER_ID | other | 1.1K | 1 | 1 544; 2 481; 3 374; 4 277 |
| GENERATOR_ID | other | 474 | 1 | GEN1 590; 1 578; 2 503; GEN2 444 |
| STEAM_PLANT_TYPE | category | 4 | 1 | 2 2.8K; 1 2.6K; 4 1.3K; 3 385 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:27.42857 7.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 1856fd25-3de4-4bc4-a93c-c 7.0K |
| _SRC_FILE | who | 1 | 0 | 6_1_EnviroAssoc_Y2024.xls 7.0K |
