# PORTAL_CKA_ANALYZE_BOSTON_ECC632A66F

rows 13  columns 10  scan 3.2s

roles: amount 4, audit 2, category 2, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        13  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FIREDIST_I | 13 | 1 | 7 | 11.88 | 12 | 83 |
| DISTRICT | 13 | 1 | 7 | 11.88 | 12 | 83 |
| SHAPE_LENGTH | 13 | 0.05 | 0.19 | 0.51 | 0.54 | 2.92 |
| SHAPE_AREA | 13 | 0 | 0 | 0.01 | 0.01 | 0.01 |

## who

SRC_SHA256 by rows
        13  5b75c7b42ed1f627b9f156aa2dbe8fe85e7dfe7a2589f849b7f3f078e78e3e99

SRC_SHA256 by dollars
          83       13 rows  5b75c7b42ed1f627b9f156aa2dbe8fe85e7dfe7a2589f849b7f3f078e78e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = FIREDIST_I
  5b75c7b42ed1f627b9f156aa2dbe8fe85e7dfe7a  2026:83

## what

CAD_DIST: F8 15%, F3 15%, F1 15%, F9 8%, F7 8%, F6 8%, F4 8%, F12 8%, F11 8%, F10 8%

DESCR: District 9 8%, District 8 8%, District 7 8%, District 6 8%, District 4 8%, District 3 8%, District 12 8%, District 11 8%, District 10 8%, District 1 8%, District 1 - Deer Island 8%, District 3 - Boston Harbor 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIREDIST_I | amount | 10 | 0 | 8.000000000000000 2; 3.000000000000000 2; 1.000000000000000 2; 9.000000000000000 1 |
| DISTRICT | amount | 10 | 0 | 8.000000000000000 2; 3.000000000000000 2; 1.000000000000000 2; 9.000000000000000 1 |
| CAD_DIST | category | 10 | 0 | F8 2; F3 2; F1 2; F9 1 |
| DESCR | category | 13 | 0 | District 9 1; District 8 1; District 7 1; District 6 1 |
| SHAPE_LENGTH | amount | 13 | 0 | 0.195016225059558 1; 0.224878592872903 1; 0.190827528925671 1; 0.187118287202126 1 |
| SHAPE_AREA | amount | 13 | 0 | 0.001646784528006 1; 0.001398249862012 1; 0.001319111830306 1; 0.001897219812155 1 |
| SHAPE_WKT | empty | 1 | 13 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:14:16.62773 13 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6b5610f4-a031-4bb1-9c6e-9 13 |
| SRC_SHA256 | who | 1 | 0 | 5b75c7b42ed1f627b9f156aa2 13 |
