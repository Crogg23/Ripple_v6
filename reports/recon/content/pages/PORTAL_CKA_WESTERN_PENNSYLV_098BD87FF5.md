# PORTAL_CKA_WESTERN_PENNSYLV_098BD87FF5

rows 11  columns 12  scan 2.9s

roles: amount 3, audit 2, category 6, date 1, who 1

## when

INGESTED_AT
  2026        11  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 11 | 2.12M | 98.37M | 398.06M | 406.37M | 1.54B |
| SHAPE__LENGTH | 11 | 9.0K | 76.3K | 168.9K | 177.1K | 724.0K |
| PERIMETER | 11 | 9.0K | 31.0K | 94.8K | 95.3K | 516.5K |

## who

SRC_SHA256 by rows
        11  ecacfabedf25e671bb404e1600667e25f3e638a580fcd124ff64a63492f8422e

SRC_SHA256 by dollars
       1.54B       11 rows  ecacfabedf25e671bb404e1600667e25f3e638a580fcd124ff64a63492f8

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  ecacfabedf25e671bb404e1600667e25f3e638a5  2026:1.54B

## what

DIVISION: 3 27%, 6 27%, 1 18%, 2 18%, 5 9%

DPWDIVS: 13 11%, 10 11%, 9 11%, 8 11%, 6 11%, 5 11%, 4 11%, 3 11%, 2 11%

DPWDIVS_ID: 1 22%, 8 11%, 4 11%, 99 11%, 112 11%, 10 11%, 3 11%, 9 11%

OBJECTID: 11 9%, 10 9%, 9 9%, 8 9%, 7 9%, 6 9%, 5 9%, 4 9%, 3 9%, 2 9%, 1 9%

UNIQUE_ID: 7 27%, 25 18%, 6 9%, 57 9%, 14 9%, 85 9%, 18 9%, 24 9%

GEOMETRY: POLYGON ((586747.8378788958070 9%, POLYGON ((585853.4664604710415 9%, POLYGON ((588571.4416921818628 9%, POLYGON ((588387.4596749007469 9%, POLYGON ((585520.4998539087828 9%, POLYGON ((587486.2128001677338 9%, POLYGON ((586384.7794955329736 9%, POLYGON ((580750.3294781286967 9%, POLYGON ((587486.2128001677338 9%, POLYGON ((593096.9582832485903 9%, POLYGON ((584456.0905770534882 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SHAPE__AREA | amount | 11 | 0 | 120984601.566101 1; 406371700.692078 1; 98370565.2354431 1; 323218488.811523 1 |
| SHAPE__LENGTH | amount | 11 | 0 | 76328.6919628821 1; 177056.646841776 1; 87455.8320051722 1; 95261.1098293809 1 |
| DIVISION | category | 5 | 0 | 3 3; 6 3; 1 2; 2 2 |
| DPWDIVS | category | 10 | 2 | 13 1; 10 1; 9 1; 8 1 |
| DPWDIVS_ID | category | 9 | 2 | 1 2; 8 1; 4 1; 99 1 |
| OBJECTID | category | 11 | 0 | 11 1; 10 1; 9 1; 8 1 |
| PERIMETER | amount | 11 | 0 | 26532.701 1; 19320.406 1; 87455.83170243 1; 95261.11145374 1 |
| UNIQUE_ID | category | 8 | 0 | 7 3; 25 2; 6 1; 57 1 |
| GEOMETRY | category | 11 | 0 | POLYGON ((586747.83787889 1; POLYGON ((585853.46646047 1; POLYGON ((588571.44169218 1; POLYGON ((588387.45967490 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:13:25.13045 11 |
| SOURCE_RUN_ID | audit | 1 | 0 | 03fac5b3-851f-4d5e-9a09-1 11 |
| SRC_SHA256 | who | 1 | 0 | ecacfabedf25e671bb404e160 11 |
