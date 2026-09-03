# FED_MAPPING_INEQUALITY

rows 10.2K  columns 15  scan 1.6s

roles: audit 2, category 1, empty 5, id 3, other 1, state 1, who 2

## who

CITY by rows
       703  Chicago
       417  Los Angeles
       239  Detroit
       192  Cleveland
       169  Queens
       163  Bergen Co.
       144  Essex Co.
       136  New Orleans
       133  Union Co.
       127  St. Louis
       122  Greater Kansas City
       120  Oakland
       119  Columbus
       116  Pittsburgh
       114  Milwaukee Co.
       113  Atlanta
       106  Springfield
       100  Norfolk
        98  Portland
        98  San Francisco

_SRC_SHA256 by rows
     10.2K  17f3b75e7485b27e48cfe17c93bd234e1ad4b025a24fc0cd0eab00cf812d6ff0

## where

STATE: IL 925, NY 891, CA 879, OH 714, NJ 684, MI 572, PA 552, MA 490, VA 320, MO 320, IN 305, TX 279

## what

HOLC_GRADE: C 38%, B 27%, D 23%, A 12%, E 0%, F 0%, C  0%, A  0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| HOLC_ID | empty | 1 | 10.2K |  |
| CITY | who | 304 | 0 | Chicago 703; Los Angeles 417; Detroit 239; Cleveland 192 |
| STATE | state | 42 | 0 | IL 925; NY 891; CA 879; OH 714 |
| FIPS | empty | 1 | 10.2K |  |
| HOLC_GRADE | category | 10 | 817 | C 3.6K; B 2.5K; D 2.2K; A 1.1K |
| HOLC_COLOR | empty | 1 | 10.2K |  |
| AREA_DESCRIPTION_DATA | other | 1 | 0 | {} 10.2K |
| RESIDENTIAL_DESCRIPTION | empty | 1 | 10.2K |  |
| YEAR_MAPPED | empty | 1 | 10.2K |  |
| GEOMETRY | id | 10.0K | 0 | {"type": "MultiPolygon",  51; {"type": "MultiPolygon",  51; {"type": "MultiPolygon",  51; {"type": "MultiPolygon",  51 |
| LAT | id | 10.0K | 0 | 40.04434666666667 51; 40.04881894736842 51; 40.047884761904776 51; 40.07143142857142 51 |
| LON | id | 10.1K | 0 | -80.66354952380952 51; -80.65256526315788 51; -80.72301035714293 51; -80.733746 51 |
| _INGESTED_AT | audit | 1 | 0 | 1781719772237327 10.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | fa7f4863-8b81-497e-9b62-4 10.2K |
| _SRC_SHA256 | who | 1 | 0 | 17f3b75e7485b27e48cfe17c9 10.2K |
