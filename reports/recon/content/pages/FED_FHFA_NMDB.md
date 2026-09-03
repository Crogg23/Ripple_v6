# FED_FHFA_NMDB

rows 11.6K  columns 13  scan 2.7s

roles: audit 2, category 1, date 1, empty 5, other 2, who 2

## when

RELEASE_DATE
  2026     11.6K  ##############################

## who

GEO_NAME by rows
       473  West
       473  Middle Atlantic
       473  South Atlantic
       473  United States
       473  United States Non-Rural
       473  Mountain
       473  Northeast
       473  East South Central
       473  East North Central
       473  Pacific
       473  West South Central
       473  Midwest
       473  South
       473  West North Central
       473  United States Rural
       473  New England
        80  North Dakota
        80  Delaware
        80  Maine
        80  Florida

_SRC_SHA256 by rows
     11.6K  aec4d96bc9c8dbefbdd1729561c14875433f52463d4409e0998988b512dda1d6

## who x when

GEO_NAME by RELEASE_DATE
  Delaware                                  2026:80
  East North Central                        2026:473
  East South Central                        2026:473
  Florida                                   2026:80
  Maine                                     2026:80
  Middle Atlantic                           2026:473
  Midwest                                   2026:473
  Mountain                                  2026:473
  New England                               2026:473
  North Dakota                              2026:80
  Northeast                                 2026:473
  Pacific                                   2026:473
  South                                     2026:473
  South Atlantic                            2026:473
  United States                             2026:473
  United States Non-Rural                   2026:473
  United States Rural                       2026:473
  West                                      2026:473
  West North Central                        2026:473
  West South Central                        2026:473

_SRC_SHA256 by RELEASE_DATE
  aec4d96bc9c8dbefbdd1729561c14875433f5246  2026:11.6K

## what

PERIOD_TYPE: Monthly 46%, Quarterly 39%, Annual 16%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEO_TYPE | empty | 1 | 11.6K |  |
| GEO_CODE | other | 67 | 0 | DESC 473; DENC 473; RS 473; RW 473 |
| GEO_NAME | who | 67 | 0 | East South Central 473; East North Central 473; South 473; West 473 |
| PERIOD_TYPE | category | 3 | 0 | Monthly 5.3K; Quarterly 4.5K; Annual 1.8K |
| PERIOD_VALUE | other | 476 | 0 | 2013Q2 71; 2024Q1 71; 1999 71; 2013 70 |
| DATASET_FAMILY | empty | 1 | 11.6K |  |
| STATISTIC_NAME | empty | 1 | 11.6K |  |
| STATISTIC_VALUE | empty | 1 | 11.6K |  |
| STATISTIC_UNIT | empty | 1 | 11.6K |  |
| RELEASE_DATE | date | 1 | 0 | 2026-07-01 11.6K |
| _INGESTED_AT | audit | 1 | 0 | 1782953590214590 11.6K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 263b1d47-4ce0-4e65-9006-5 11.6K |
| _SRC_SHA256 | who | 1 | 0 | aec4d96bc9c8dbefbdd172956 11.6K |
