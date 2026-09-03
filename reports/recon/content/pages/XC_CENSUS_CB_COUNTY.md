# XC_CENSUS_CB_COUNTY

rows 3.2K  columns 17  scan 2.0s

roles: audit 2, category 1, date 1, empty 1, id 6, other 3, state 1, who 3

## errors
  _INGESTED_AT: 100039 (22003): Numeric value '56643299' is out of range

## who

NAMELSAD by rows
        30  Washington County
        25  Jefferson County
        24  Franklin County
        23  Jackson County
        23  Lincoln County
        19  Madison County
        18  Clay County
        18  Montgomery County
        17  Union County
        17  Monroe County
        17  Marion County
        16  Wayne County
        14  Grant County
        14  Greene County
        14  Warren County
        13  Carroll County
        12  Douglas County
        12  Clark County
        12  Lee County
        12  Lake County

NAME by rows
        31  Washington
        26  Franklin
        26  Jefferson
        24  Jackson
        24  Lincoln
        20  Madison
        18  Montgomery
        18  Union
        18  Clay
        17  Marion
        17  Monroe
        16  Wayne
        15  Grant
        14  Greene
        14  Warren
        13  Carroll
        12  Polk
        12  Douglas
        12  Adams
        12  Lake

STATE_NAME by rows
       254  Texas
       159  Georgia
       133  Virginia
       120  Kentucky
       115  Missouri
       105  Kansas
       102  Illinois
       100  North Carolina
        99  Iowa
        95  Tennessee
        93  Nebraska
        92  Indiana
        88  Ohio
        87  Minnesota
        83  Michigan
        82  Mississippi
        78  Puerto Rico
        77  Oklahoma
        75  Arkansas
        72  Wisconsin

## where

STUSPS: TX 254, GA 159, VA 133, KY 120, MO 115, KS 105, IL 102, NC 100, IA 99, TN 95, NE 93, IN 92

## what

LSAD: 06 93%, 13 2%, 15 2%, 25 1%, 04 0%, 05 0%, PL 0%, 12 0%, 00 0%, 03 0%, 07 0%, 10 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATEFP | other | 56 | 0 | 48 254; 13 159; 51 133; 21 120 |
| COUNTYFP | other | 335 | 0 | 005 49; 001 49; 003 49; 009 48 |
| COUNTYNS | id | 3.2K | 0 | 01804484 17; 01804549 17; 01804482 17; 00424296 17 |
| GEOIDFQ | id | 3.3K | 0 | 0500000US72009 17; 0500000US72137 17; 0500000US72005 17; 0500000US17191 17 |
| GEOID | id | 3.3K | 0 | 72009 17; 72137 17; 72005 17; 17191 17 |
| NAME | who | 1.9K | 0 | Washington 31; Franklin 26; Jefferson 26; Lincoln 25 |
| NAMELSAD | who | 2.0K | 0 | Washington County 30; Jefferson County 25; Franklin County 24; Lincoln County 24 |
| STUSPS | state | 56 | 0 | TX 254; GA 159; VA 133; KY 120 |
| STATE_NAME | who | 55 | 0 | Texas 254; Georgia 159; Virginia 133; Kentucky 120 |
| LSAD | category | 12 | 0 | 06 3.0K; 13 78; 15 64; 25 40 |
| ALAND | id | 3.3K | 0 | 81098530 17; 60201713 17; 94642779 17; 1848810381 17 |
| AWATER | id | 3.3K | 0 | 67829 17; 48075983 17; 101102905 17; 4224962 17 |
| GEOMETRY_WKT | id | 3.3K | 0 | MULTIPOLYGON (((-66.31803 17; MULTIPOLYGON (((-66.13741 17; MULTIPOLYGON (((-67.16951 17; MULTIPOLYGON (((-88.70219 17 |
| VINTAGE | other | 1 | 0 | 2023 3.2K |
| _INGESTED_AT | audit date | 1 | 0 | 56643299-10-15 08:13:35.0 3.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 05fecf80-b2e0-4931-ab76-f 3.2K |
| _SRC_SHA256 | empty | 0 | 3.2K |  |
