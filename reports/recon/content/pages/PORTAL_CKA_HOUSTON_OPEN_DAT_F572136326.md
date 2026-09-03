# PORTAL_CKA_HOUSTON_OPEN_DAT_F572136326

rows 15  columns 8  scan 2.9s

roles: audit 2, category 3, date 1, other 1, who 2

## when

INGESTED_AT
  2026        15  ##############################

## who

NAME by rows
        15  Houston city, Texas

SRC_SHA256 by rows
        15  3a2c976c203738ce5884393ad922d8d886ec985451b2d1e3b4a0e1949cd454bc

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  Houston city, Texas                       2026:15

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  3a2c976c203738ce5884393ad922d8d886ec9854  2026:15

## what

YEAR: 2010 8%, 2011 8%, 2012 8%, 2013 8%, 2014 8%, 2015 8%, 2016 8%, 2017 8%, 2018 8%, 2019 8%, 2020 8%, 2021 8%

B19013_001E: 42962 8%, 44124 8%, 44648 8%, 45010 8%, 45728 8%, 46187 8%, 47010 8%, 49399 8%, 51140 8%, 52338 8%, 53600 8%, 56019 8%

B25077_001E: 123800 8%, 124400 8%, 124700 8%, 123900 8%, 125400 8%, 131700 8%, 140300 8%, 149000 8%, 161300 8%, 171800 8%, 186800 8%, 200700 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 15 | 0 | 2010 1; 2011 1; 2012 1; 2013 1 |
| GEO_ID | other | 1 | 0 | 4835000 15 |
| NAME | who | 1 | 0 | Houston city, Texas 15 |
| B19013_001E | category | 15 | 0 | 42962 1; 44124 1; 44648 1; 45010 1 |
| B25077_001E | category | 15 | 0 | 123800 1; 124400 1; 124700 1; 123900 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:46.35576 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | ac9562a5-248e-4b37-9600-2 15 |
| SRC_SHA256 | who | 1 | 0 | 3a2c976c203738ce5884393ad 15 |
