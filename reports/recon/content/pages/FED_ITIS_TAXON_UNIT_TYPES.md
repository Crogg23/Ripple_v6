# FED_ITIS_TAXON_UNIT_TYPES

rows 182  columns 9  scan 2.0s

roles: audit 2, category 5, date 1, who 1

## when

UPDATE_DATE
  1996        62  ##############################
  1999        22  ###########
  2004        43  #####################
  2005         2  #
  2012        10  #####
  2013         3  #
  2014        38  ##################
  2024         2  #

## who

SRC_SHA256 by rows
       182  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f5cf0f50cadf6c22e71debe21

## who x when

SRC_SHA256 by UPDATE_DATE
  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f  1996:62 1999:22 2004:43 2005:2 2012:10 2013:3 2014:38 2024:2

## what

KINGDOM_ID: 5 18%, 6 16%, 3 15%, 2 14%, 4 13%, 1 13%, 7 12%

RANK_ID: 230 8%, 220 8%, 190 8%, 180 8%, 170 8%, 160 8%, 150 8%, 140 8%, 110 8%, 100 8%, 90 8%, 70 8%

RANK_NAME: Subspecies 8%, Species 8%, Subgenus 8%, Genus 8%, Subtribe 8%, Tribe 8%, Subfamily 8%, Family 8%, Suborder 8%, Order 8%, Superorder 8%, Subclass 8%

DIR_PARENT_RANK_ID: 220 19%, 10 13%, 190 7%, 180 7%, 170 7%, 160 7%, 150 7%, 140 7%, 110 7%, 100 7%, 90 7%, 70 7%

REQ_PARENT_RANK_ID: 180 23%, 140 15%, 10 15%, 60 15%, 30 14%, 100 13%, 220 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| KINGDOM_ID | category | 7 | 0 | 5 33; 6 29; 3 28; 2 25 |
| RANK_ID | category | 37 | 0 | 230 7; 220 7; 190 7; 180 7 |
| RANK_NAME | category | 41 | 0 | Subspecies 7; Species 7; Subgenus 7; Genus 7 |
| DIR_PARENT_RANK_ID | category | 32 | 0 | 220 20; 10 14; 190 7; 180 7 |
| REQ_PARENT_RANK_ID | category | 7 | 0 | 180 41; 140 28; 10 28; 60 27 |
| UPDATE_DATE | date | 13 | 0 | 2004-06-04 43; 1996-06-13 41; 2014-08-20 38; 1999-03-04 21 |
| INGESTED_AT | audit | 1 | 0 | 1786164250570840 182 |
| SOURCE_RUN_ID | audit | 1 | 0 | 21ca1ab0-8d12-4dc1-a750-3 182 |
| SRC_SHA256 | who | 1 | 0 | d98c5f0cb5207f84bb56ef033 182 |
