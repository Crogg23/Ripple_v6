# FED_CDC_DATA_PORTAL

rows 15.0K  columns 16  scan 2.1s

roles: audit 3, category 5, date 1, empty 7, who 1

## when

UPDATED_AT
  2022      5.0K  ###############
  2023     10.0K  ##############################

## who

_SRC_SHA256 by rows
     15.0K  c4be45fd5439c301627cededed719ef0f03d8527987027f6c9eed1357b5aa526

## who x when

_SRC_SHA256 by UPDATED_AT  LOAD STAMP, not an event date
  c4be45fd5439c301627cededed719ef0f03d8527  2022:5.0K 2023:10.0K

## what

DATASET_ID: muzy-jte6 33%, 3h58-x6cd 33%, unsk-b7fc 33%

INDICATOR: Weekly Provisional Counts of D 33%, NCHS - Teen Birth Rates for Ag 33%, COVID-19 Vaccinations in the U 33%

YEAR: 2016 9%, 2015 9%, 2014 9%, 2013 9%, 2012 9%, 2011 9%, 2010 9%, 2009 9%, 2008 9%, 2007 9%, 2006 9%

STATE: Arkansas 27%, Alabama 24%, California 21%, Colorado 14%, Alaska 9%, Arizona 5%

TOPIC: National Center for Health Sta 67%, Vaccinations 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATASET_ID | category | 3 | 0 | muzy-jte6 5.0K; 3h58-x6cd 5.0K; unsk-b7fc 5.0K |
| INDICATOR | category | 3 | 0 | Weekly Provisional Counts 5.0K; NCHS - Teen Birth Rates f 5.0K; COVID-19 Vaccinations in  5.0K |
| YEAR | category | 19 | 10.0K | 2016 278; 2015 278; 2014 278; 2013 278 |
| STATE | category | 7 | 10.0K | Arkansas 1.4K; Alabama 1.2K; California 1.0K; Colorado 680 |
| FIPS | empty | 1 | 15.0K |  |
| ZIP_CODE | empty | 1 | 15.0K |  |
| VALUE | empty | 1 | 15.0K |  |
| UNIT | empty | 1 | 15.0K |  |
| DATA_VALUE_TYPE | empty | 1 | 15.0K |  |
| TOPIC | category | 2 | 0 | National Center for Healt 10.0K; Vaccinations 5.0K |
| CATEGORY | empty | 1 | 15.0K |  |
| SOURCE | empty | 1 | 15.0K |  |
| UPDATED_AT | audit date | 3 | 0 | 1695825836 5.0K; 1649445233 5.0K; 1683869443 5.0K |
| _INGESTED_AT | audit | 1 | 0 | 1782941234974124 15.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | e1c0b3d0-ef07-4c6e-bf28-1 15.0K |
| _SRC_SHA256 | who | 1 | 0 | c4be45fd5439c301627cedede 15.0K |
