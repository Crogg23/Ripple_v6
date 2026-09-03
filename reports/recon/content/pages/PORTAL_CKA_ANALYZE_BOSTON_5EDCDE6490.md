# PORTAL_CKA_ANALYZE_BOSTON_5EDCDE6490

rows 28  columns 20  scan 4.4s

roles: amount 6, audit 2, category 7, date 1, empty 3, who 2

## when

INGESTED_AT
  2026        28  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CENSUS_TRA | 28 | 0 | 0 | 2.3K | 2.3K | 13.0K |
| LATITUDE | 28 | 42.28 | 42.34 | 42.38 | 42.38 | 1.2K |
| LONGITUDE | 28 | -71.17 | -71.10 | -71.05 | -71.05 | -2.0K |
| DAILYAVG | 7 | 65 | 140 | 319.80 | 330 | 1.1K |
| POINT_X | 28 | -71.17 | -71.10 | -71.05 | -71.05 | -2.0K |
| POINT_Y | 28 | 42.28 | 42.34 | 42.38 | 42.38 | 1.2K |

## who

PRIMARY_ALT by rows
        28  Primary

PRIMARY_ALT by dollars
       13.0K       28 rows  Primary

SRC_SHA256 by rows
        28  b1fb27c9b289171f78ae77dbb3db79419b5fe3a209c5c34acf67d4911a8e5e25

SRC_SHA256 by dollars
       13.0K       28 rows  b1fb27c9b289171f78ae77dbb3db79419b5fe3a209c5c34acf67d4911a8e

## who x when

PRIMARY_ALT by INGESTED_AT  LOAD STAMP, not an event date, dollars = CENSUS_TRA
  Primary                                   2026:13.0K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CENSUS_TRA
  b1fb27c9b289171f78ae77dbb3db79419b5fe3a2  2026:13.0K

## what

NAME: Mass General Hospital 8%, MGH at the Navy Yard 8%, Boston Medical Campus 8%, Urgent Care Medical Unit 8%, Erich LIindemann Mental Health 8%, Veterans Affairs Boston Health 8%, BOSTON VETERAN CENTER 8%, New England Baptist Hospital 8%, Boston Medical Center - East N 8%, Beth Israel Deaconess Medical  8%, VA Bos. Healthcare System - W. 8%, VA Bos. Healthcare System - Ja 8%

ADDRESS: 255 265 CHARLES ST 8%,   THIRTEENTH ST 8%, 774 Albany Street 8%, 581 BOYLSTON STREET 8%, 25 STANIFORD STREET 8%, 251 CAUSEWAY STREET 8%, 665 BEACON STREET 8%, 125 Parker Hill Avenue 8%, 88 East Newton Street 8%, 110 Francis Street 8%, 1400 VFW Parkway, Boston, 0213 8%, 150 South Huntington Ave. Bost 8%

ZIPCODE: 02114 23%, 02115 15%, 02118 12%, 02215 12%, 02135 8%, 02130 8%, 02129 4%, 02116 4%, 02120 4%, 02132 4%, 02111 4%, 02124 4%

CONTACT: BOSTON PUBLIC HEALTH COMM 13%, COMMONWEALTH OF MASS 13%, BETH ISRAEL DEACONESS 13%, GENERAL HOSPITAL CORP 7%, CONSTITUTION OFFICE PARK LE 7%, ABBEY BOYLSTON LLC 7%, CAUSEWAY HOLDINGS INC 7%, BOSTON UNIVERSITY TRSTS OF 7%, N E BAPTIST HOSPITAL 7%, UNIVERSITY HOSP INC 7%, UNITED STATES OF AMERICA 7%, UNITED STATES OF AMER 7%

PHONENUMBE: 617-247-1400 9%, 617-626-8500 9%, 617-248-1000 9%, 617-424-0665 9%, (617) 323-7700 9%, (617) 232-9500 9%, (617) 636-5000 9%, 617-789-3000 9%, 617-726-2000 9%, 617-983-7000 9%, 617-632-3000 9%

ALTERNATIVE_NAME: Massachusetts General Hospital 33%, UpdateStat! Massachusetts Gene 33%, Shriner’s Burn Institute  33%

SHAPE_WKT: POINT (-71.068286543999989 42. 8%, POINT (-71.052447000999962 42. 8%, POINT (-71.07221635999997 42.3 8%, POINT (-71.07660537199996 42.3 8%, POINT (-71.063490275999982 42. 8%, POINT (-71.058952078999937 42. 8%, POINT (-71.098543713999959 42. 8%, POINT (-71.107140279999953 42. 8%, POINT (-71.070794885999987 42. 8%, POINT (-71.108921383999984 42. 8%, POINT (-71.171392921999939 42. 8%, POINT (-71.110167408999985 42. 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CENSUS_TRA | amount | 7 | 0 | 0.000000000000000 22; 2084.000000000000000 1; 2092.000000000000000 1; 2139.000000000000000 1 |
| NAME | category | 28 | 0 | Mass General Hospital 1; MGH at the Navy Yard 1; Boston Medical Campus 1; Urgent Care Medical Unit 1 |
| ADDRESS | category | 28 | 0 | 255 265 CHARLES ST 1;   THIRTEENTH ST 1; 774 Albany Street 1; 581 BOYLSTON STREET 1 |
| CITY | empty | 1 | 28 |  |
| ZIPCODE | category | 14 | 0 | 02114 6; 02115 4; 02118 3; 02215 3 |
| STATEA | empty | 1 | 28 |  |
| CONTACT | category | 25 | 0 | BOSTON PUBLIC HEALTH COMM 2; COMMONWEALTH OF MASS 2; BETH ISRAEL DEACONESS 2; GENERAL HOSPITAL CORP 1 |
| PHONENUMBE | category | 23 | 6 | 617-247-1400 1; 617-626-8500 1; 617-248-1000 1; 617-424-0665 1 |
| LATITUDE | amount | 28 | 0 | 42.363155239999998 1; 42.377220770000001 1; 42.333824090000000 1; 42.350554680000002 1 |
| LONGITUDE | amount | 28 | 0 | -71.068527829999994 1; -71.052447000000001 1; -71.072216310000002 1; -71.076605369999996 1 |
| COMMENT | empty | 1 | 28 |  |
| PRIMARY_ALT | who | 1 | 0 | Primary 28 |
| ALTERNATIVE_NAME | category | 4 | 25 | Massachusetts General Hos 1; UpdateStat! Massachusetts 1; Shriner’s Burn Institute  1 |
| DAILYAVG | amount | 7 | 21 | 160.000000000000000 2; 110.000000000000000 1; 90.000000000000000 1; 65.000000000000000 1 |
| SHAPE_WKT | category | 28 | 0 | POINT (-71.06828654399998 1; POINT (-71.05244700099996 1; POINT (-71.07221635999997 1; POINT (-71.07660537199996 1 |
| POINT_X | amount | 28 | 0 | -71.068286543999989 1; -71.052447000999962 1; -71.072216359999970 1; -71.076605371999960 1 |
| POINT_Y | amount | 28 | 0 | 42.362365411000042 1; 42.377220779000027 1; 42.333829494000042 1; 42.350554689000035 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:19:07.21069 28 |
| SOURCE_RUN_ID | audit | 1 | 0 | bc539c4f-9a47-4c9e-b953-a 28 |
| SRC_SHA256 | who | 1 | 0 | b1fb27c9b289171f78ae77dbb 28 |
