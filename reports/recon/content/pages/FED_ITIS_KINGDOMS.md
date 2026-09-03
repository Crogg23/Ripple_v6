# FED_ITIS_KINGDOMS

rows 7  columns 6  scan 2.0s

roles: audit 2, category 2, date 1, who 1

## when

UPDATE_DATE
  1996         3  ##############################
  2004         2  ####################
  2014         2  ####################

## who

SRC_SHA256 by rows
         7  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f5cf0f50cadf6c22e71debe21

## who x when

SRC_SHA256 by UPDATE_DATE
  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f  1996:3 2004:2 2014:2

## what

KINGDOM_ID: 7 14%, 6 14%, 5 14%, 4 14%, 3 14%, 2 14%, 1 14%

KINGDOM_NAME: Archaea 14%, Chromista 14%, Animalia 14%, Fungi 14%, Plantae 14%, Protozoa 14%, Bacteria 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| KINGDOM_ID | category | 7 | 0 | 7 1; 6 1; 5 1; 4 1 |
| KINGDOM_NAME | category | 7 | 0 | Archaea 1; Chromista 1; Animalia 1; Fungi 1 |
| UPDATE_DATE | date | 3 | 0 | 1996-03-26 3; 2014-08-20 2; 2004-06-04 2 |
| INGESTED_AT | audit | 1 | 0 | 1786164250570840 7 |
| SOURCE_RUN_ID | audit | 1 | 0 | 21ca1ab0-8d12-4dc1-a750-3 7 |
| SRC_SHA256 | who | 1 | 0 | d98c5f0cb5207f84bb56ef033 7 |
