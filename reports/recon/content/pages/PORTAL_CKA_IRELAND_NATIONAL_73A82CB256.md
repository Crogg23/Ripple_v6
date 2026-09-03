# PORTAL_CKA_IRELAND_NATIONAL_73A82CB256

rows 6  columns 10  scan 3.2s

roles: amount 2, audit 2, category 5, date 1, who 1

## when

INGESTED_AT
  2026         6  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 6 | 481.9K | 1.18M | 18.74M | 19.61M | 25.25M |
| SHAPE__LENGTH | 6 | 3.3K | 11.3K | 26.1K | 26.7K | 74.3K |

## who

SRC_SHA256 by rows
         6  24bae79a6a406604f7e3fd6ff9ae77d7a2d2ee295d2550c62831112094530535

SRC_SHA256 by dollars
      25.25M        6 rows  24bae79a6a406604f7e3fd6ff9ae77d7a2d2ee295d2550c6283111209453

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  24bae79a6a406604f7e3fd6ff9ae77d7a2d2ee29  2026:25.25M

## what

FID: 6 17%, 5 17%, 4 17%, 3 17%, 2 17%, 1 17%

MAP_REF: 4 17%, 5 17%, 3 17%, 6 17%, 2 17%, 1 17%

ID: Glendalough 17%, Glenealo Valley 17%, Vale of Clara 17%, Knocksink Wood 17%, Deputy's Pass, Glenealy 17%, Glen of the Downs 17%

HABIITAT: Woodland 83%, Blanket bog, heath 17%

PLAN_DESCR: County Development Plan 2022-2 50%, County Development Plan 2022-2 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 6 | 0 | 6 1; 5 1; 4 1; 3 1 |
| MAP_REF | category | 6 | 0 | 4 1; 5 1; 3 1; 6 1 |
| ID | category | 6 | 0 | Glendalough 1; Glenealo Valley 1; Vale of Clara 1; Knocksink Wood 1 |
| HABIITAT | category | 2 | 0 | Woodland 5; Blanket bog, heath 1 |
| PLAN_DESCR | category | 2 | 0 | County Development Plan 2 3; County Development Plan 2 3 |
| SHAPE__AREA | amount | 6 | 0 | 1688278.05917358 1; 19612684.7077942 1; 2252177.78405762 1; 552854.450500488 1 |
| SHAPE__LENGTH | amount | 6 | 0 | 13981.6416574339 1; 26688.0572387076 1; 15840.8937260924 1; 8629.19453963647 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:10:46.74080 6 |
| SOURCE_RUN_ID | audit | 1 | 0 | fb13b5e1-5919-4c9a-84b2-0 6 |
| SRC_SHA256 | who | 1 | 0 | 24bae79a6a406604f7e3fd6ff 6 |
