# PORTAL_CKA_WPRDC_ALLEGHENY_4A2424EA96

rows 588  columns 11  scan 4.1s

roles: amount 3, audit 2, category 3, date 1, other 2, who 1

## when

INGESTED_AT
  2026       588  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_AREA | 588 | 2.9K | 91.0K | 6.56M | 12.76M | 260.78M |
| SHAPE_LENGTH | 588 | 218.13 | 1.8K | 31.9K | 130.6K | 2.30M |
| SQ_FT | 588 | 18.4K | 566.8K | 40.90M | 79.53M | 1.62B |

## who

SRC_SHA256 by rows
       588  8f647cc53703b270064e0936dab6e7654335605a8083188cfd1d7c3ae646a761

SRC_SHA256 by dollars
     260.78M      588 rows  8f647cc53703b270064e0936dab6e7654335605a8083188cfd1d7c3ae646

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  8f647cc53703b270064e0936dab6e7654335605a  2026:260.78M

## what

DATA_YEAR: 1958 map 100%, 1976 map 0%

ZONING_DISTRICT1958: S 18%, C3 14%, C1 12%, R2 11%, R3 9%, R1 8%, R4 7%, M2 6%, M1 6%, M3 5%, R5 2%, C4 2%

ZONING_DISTRICT1967: S 18%, C3 14%, C1 12%, R2 12%, R3 9%, R1 9%, R4 8%, M2 6%, M1 5%, M3 5%, R5 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATA_YEAR | category | 2 | 0 | 1958 map 587; 1976 map 1 |
| OBJECTID | other | 574 | 0 | 588 3; 587 3; 586 3; 585 3 |
| SHAPE_AREA | amount | 587 | 0 | 53130.743806013095 3; 50511.7402668389 3; 116676.37213128922 3; 109398.82874261968 3 |
| SHAPE_LENGTH | amount | 591 | 0 | 1154.6693108483414 3; 1144.033218793884 3; 1961.4198980898443 3; 1918.3728198583258 3 |
| SQ_FT | amount | 573 | 0 | 330829.79642201954 3; 314446.9404247843 3; 726385.8023777358 3; 681053.4076839043 3 |
| ZONING_DISTRICT1958 | category | 19 | 0 | S 104; C3 81; C1 66; R2 63 |
| ZONING_DISTRICT1967 | category | 21 | 14 | S 99; C3 76; C1 65; R2 64 |
| GEOMETRY | other | 588 | 0 | POLYGON ((584346.84790254 3; POLYGON ((582972.42402269 3; POLYGON ((583058.19966071 3; POLYGON ((582411.83025220 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:44:02.80418 588 |
| SOURCE_RUN_ID | audit | 1 | 0 | dfbd73fd-4c13-4315-a9e6-a 588 |
| SRC_SHA256 | who | 1 | 0 | 8f647cc53703b270064e0936d 588 |
