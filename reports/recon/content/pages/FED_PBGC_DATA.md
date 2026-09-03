# FED_PBGC_DATA

rows 140.5K  columns 13  scan 2.7s

roles: audit 2, category 2, empty 4, other 1, who 4

## who

METRIC_NAME by rows
      3.2K  2010
      3.0K  2011
      2.9K  2008
      2.8K  2009
      2.8K  2012
      2.7K  2013
      2.5K  2006
      2.5K  2007
      2.5K  2005
      2.5K  2003
      2.5K  2004
      2.5K  2014
      2.5K  2001
      2.4K  2002
      2.3K  2015
      2.1K  2000
      2.0K  2016
      2.0K  1999
      2.0K  1998
      2.0K  1996

TABLE_NAME by rows
      6.7K  S-51
      6.5K  S-52
      3.6K  S-20
      3.1K  S-21
      3.0K  M-5
      2.9K  S-30
      2.8K  M-6
      2.8K  S-31
      2.7K  M-14
      2.6K  S-34
      2.6K  S-35
      2.5K  M-12
      2.5K  S-50
      2.5K  S-3
      2.4K  S-47
      2.4K  M-9
      2.4K  S-38
      2.3K  S-44
      2.3K  S-29
      2.2K  S-40

METRIC_VALUE by rows
      2.0K  ---
      1.6K  1
       453  *
       383  0
       327  2
       266  4
       243  9
       229  5
       212  6
       207  0.053
       204  3
       199  0.054
       194  0.064
       193  23
       182  19
       178  21
       177  24
       176  0.05
       172  14
       169  0.0725

STATE by rows
       128  SOUTHWEST
       128  GREAT LAKES
       128  California
       128  Pennsylvania
       128  Ohio
       128  Arkansas
       128  New York
       128  Kentucky
       128  Illinois
       128  Michigan
       128  Florida
       128  SOUTHEAST
       128  MID-ATLANTIC
       128  West Virginia
       128  Texas
       128  TOTAL
       128  New Jersey
       128  PACIFIC
       127  Louisiana
       127  Massachusetts

## what

DATA_YEAR: 2021 11%, 2023 10%, 2022 10%, 2020 9%, 2019 9%, 2018 8%, 2017 8%, 2015 8%, 2016 8%, 2014 7%, 2013 7%, 2010 7%

SOURCE_FILE: https://www.pbgc.gov/sites/def 11%, https://www.pbgc.gov/sites/def 10%, https://www.pbgc.gov/sites/def 10%, https://www.pbgc.gov/sites/def 9%, https://www.pbgc.gov/sites/def 9%, https://www.pbgc.gov/sites/def 8%, https://www.pbgc.gov/sites/def 8%, https://www.pbgc.gov/sites/def 8%, https://www.pbgc.gov/sites/def 8%, https://www.pbgc.gov/sites/def 7%, https://www.pbgc.gov/sites/def 7%, https://www.pbgc.gov/sites/def 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATA_YEAR | category | 14 | 0 | 2021 13.3K; 2023 12.3K; 2022 11.9K; 2020 11.0K |
| PUBLICATION_DATE | empty | 1 | 140.5K |  |
| PROGRAM_TYPE | empty | 1 | 140.5K |  |
| TABLE_NAME | who | 89 | 0 | S-51 6.7K; S-52 6.5K; S-20 3.6K; S-21 3.1K |
| METRIC_NAME | who | 711 | 26.0K | 2010 3.2K; 2011 3.0K; 2008 2.9K; 2009 2.8K |
| METRIC_VALUE | who | 46.3K | 0 | --- 2.0K; 1 1.6K; 293 692; 10,000 or More 692 |
| UNIT | empty | 1 | 140.5K |  |
| STATE | who | 80 | 132.5K | GREAT LAKES 128; Arkansas 128; Texas 128; SOUTHWEST 128 |
| SOURCE_FILE | category | 14 | 0 | https://www.pbgc.gov/site 13.3K; https://www.pbgc.gov/site 12.3K; https://www.pbgc.gov/site 11.9K; https://www.pbgc.gov/site 11.0K |
| NOTES_FLAG | empty | 1 | 140.5K |  |
| _INGESTED_AT | audit | 1 | 0 | 1783013702678139 140.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 55085d88-f796-45fe-a87e-f 140.5K |
| _SRC_SHA256 | other | 1 | 0 | 81ce80e01804cb7fabbf378ab 140.5K |
