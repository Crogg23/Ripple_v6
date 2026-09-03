# PORTAL_CKA_HOUSTON_OPEN_DAT_CFDCDF13FD

rows 15  columns 7  scan 2.4s

roles: audit 2, category 2, date 1, other 1, who 2

## when

INGESTED_AT
  2026        15  ##############################

## who

NAME by rows
        15  Houston city, Texas

SRC_SHA256 by rows
        15  6ffdb816a50d0d4ebe7a27e373302141be143b58f946ca9ccc4059c52e8d91f4

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Houston city, Texas                       2026:15

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  6ffdb816a50d0d4ebe7a27e373302141be143b58  2026:15

## what

YEAR: 2010 8%, 2011 8%, 2012 8%, 2013 8%, 2014 8%, 2015 8%, 2016 8%, 2017 8%, 2018 8%, 2019 8%, 2020 8%, 2021 8%

B25064_001E: 793 8%, 820 8%, 837 8%, 848 8%, 862 8%, 873 8%, 898 8%, 940 8%, 990 8%, 1041 8%, 1086 8%, 1136 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 15 | 0 | 2010 1; 2011 1; 2012 1; 2013 1 |
| GEO_ID | other | 1 | 0 | 4835000 15 |
| NAME | who | 1 | 0 | Houston city, Texas 15 |
| B25064_001E | category | 15 | 0 | 793 1; 820 1; 837 1; 848 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:39.68191 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | 91cfb6c5-a29a-4391-8dcc-0 15 |
| SRC_SHA256 | who | 1 | 0 | 6ffdb816a50d0d4ebe7a27e37 15 |
