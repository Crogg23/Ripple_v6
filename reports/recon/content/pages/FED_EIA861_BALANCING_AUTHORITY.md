# FED_EIA861_BALANCING_AUTHORITY

rows 188  columns 8  scan 2.1s

roles: audit 2, date 1, other 3, state 1, who 2

## when

_INGESTED_AT
  2026       188  ##############################

## who

ALCOA_POWER_GENERATING_INC_YADKIN_DIVISION by rows
        17  Midcontinent Independent Transmission System Operator, Inc..
        15  PJM Interconnection, LLC
        14  Southwest Power Pool
         9  Western Area Power Administration - Rocky Mountain Region
         7  Tennessee Valley Authority
         7  ISO New England Inc.
         7  Bonneville Power Administration
         7  PacifiCorp - East
         5  Public Service Company of New Mexico
         5  Western Area Power Administration - Desert Southwest Region
         4  PacifiCorp - West
         4  Associated Electric Cooperative, Inc.
         4  Public Service Company of Colorado
         4  Southern Company Services, Inc. - Trans
         3  Avista Corporation
         3  Nevada Power Company
         3  Western Area Power Administration UGP West
         3  Southeastern Power Administration
         3  California Independent System Operator
         3  Duke Energy Carolinas

_SRC_FILE by rows
       188  Balancing_Authority_2024.xlsx

## who x when

ALCOA_POWER_GENERATING_INC_YADKIN_DIVISION by _INGESTED_AT  LOAD STAMP, not an event date
  Associated Electric Cooperative, Inc.     2026:4
  Avista Corporation                        2026:3
  Bonneville Power Administration           2026:7
  California Independent System Operator    2026:3
  Duke Energy Carolinas                     2026:3
  ISO New England Inc.                      2026:7
  Midcontinent Independent Transmission Sy  2026:17
  Nevada Power Company                      2026:3
  PJM Interconnection, LLC                  2026:15
  PacifiCorp - East                         2026:7
  PacifiCorp - West                         2026:4
  Public Service Company of Colorado        2026:4
  Public Service Company of New Mexico      2026:5
  Southeastern Power Administration         2026:3
  Southern Company Services, Inc. - Trans   2026:4
  Southwest Power Pool                      2026:14
  Tennessee Valley Authority                2026:7
  Western Area Power Administration - Dese  2026:5
  Western Area Power Administration - Rock  2026:9
  Western Area Power Administration UGP We  2026:3

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date
  Balancing_Authority_2024.xlsx             2026:188

## where

NC: NM 11, AZ 11, FL 10, MT 9, WA 9, CA 8, UT 7, WY 6, NC 6, CO 5, NV 5, GA 5

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| C_2024 | other | 1 | 0 | 2024 188 |
| C_317 | other | 66 | 0 | 56669 17; 14725 15; 59504 14; 28503 9 |
| YAD | other | 66 | 0 | MISO 17; PJM 15; SWPP 14; WACM 9 |
| NC | state | 51 | 0 | NM 11; AZ 11; FL 10; MT 9 |
| ALCOA_POWER_GENERATING_INC_YADKIN_DIVISION | who | 66 | 0 | Midcontinent Independent  17; PJM Interconnection, LLC 15; Southwest Power Pool 14; Western Area Power Admini 9 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:50.98423 188 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 2bf96b14-5972-42a9-b620-1 188 |
| _SRC_FILE | who | 1 | 0 | Balancing_Authority_2024. 188 |
