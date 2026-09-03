# XC_CENSUS_CB_STATE

rows 56  columns 14  scan 1.7s

roles: audit 2, date 1, empty 1, other 9, state 1, who 1

## errors
  _INGESTED_AT: 100039 (22003): Numeric value '56643299' is out of range

## who

NAME by rows
         1  West Virginia
         1  Alabama
         1  New Hampshire
         1  Ohio
         1  Louisiana
         1  California
         1  Alaska
         1  Rhode Island
         1  Delaware
         1  Pennsylvania
         1  Tennessee
         1  Colorado
         1  Oregon
         1  District of Columbia
         1  Kansas
         1  New Mexico
         1  Utah
         1  South Carolina
         1  Virginia
         1  Iowa

## where

STUSPS: LA 1, WV 1, VA 1, NC 1, MS 1, OR 1, WI 1, OH 1, TX 1, PR 1, WA 1, NE 1

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATEFP | other | 56 | 0 | 22 1; 54 1; 51 1; 37 1 |
| STATENS | other | 56 | 0 | 01629543 1; 01779805 1; 01779803 1; 01027616 1 |
| GEOIDFQ | other | 56 | 0 | 0400000US22 1; 0400000US54 1; 0400000US51 1; 0400000US37 1 |
| GEOID | other | 56 | 0 | 22 1; 54 1; 51 1; 37 1 |
| STUSPS | state | 56 | 0 | LA 1; WV 1; VA 1; NC 1 |
| NAME | who | 55 | 0 | Louisiana 1; West Virginia 1; Virginia 1; North Carolina 1 |
| LSAD | other | 1 | 0 | 00 56 |
| ALAND | other | 55 | 0 | 111930452904 1; 62266499712 1; 102258163252 1; 125935880061 1 |
| AWATER | other | 56 | 0 | 23721187320 1; 489003081 1; 8528087616 1; 13453540851 1 |
| GEOMETRY_WKT | other | 56 | 0 | MULTIPOLYGON (((-88.8677  1; MULTIPOLYGON (((-82.64319 1; MULTIPOLYGON (((-75.74240 1; MULTIPOLYGON (((-75.72680 1 |
| VINTAGE | other | 1 | 0 | 2023 56 |
| _INGESTED_AT | audit date | 1 | 0 | 56643299-10-15 08:13:35.0 56 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 05fecf80-b2e0-4931-ab76-f 56 |
| _SRC_SHA256 | empty | 0 | 56 |  |
