# PORTAL_SOC_DELAWARE_OPEN_DA_EB5F15ED0E

rows 67  columns 20  scan 4.3s

roles: amount 4, audit 2, category 3, date 3, other 7, who 2

## when

UPDATED
  2025        57  ##############################
  2026        10  #####

ISSUE_DATE
  2023         1  #
  2024        19  ################
  2025        35  ##############################
  2026         3  ###

INGESTED_AT
  2026        67  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 67 | 1.21 | 44.32 | 244.78 | 263.40 | 3.6K |
| SHAPE_AREA | 67 | 8.1K | 296.8K | 1.67M | 1.79M | 24.43M |
| SHAPE_LEN | 67 | 522.25 | 2.7K | 7.6K | 8.1K | 187.0K |
| CALC_ACRES | 67 | 1.21 | 44.32 | 244.79 | 263.41 | 3.6K |

## who

COMPANY1 by rows
         4  Harbeson DEA, LLC
         2  Chesapeake SU165 Solar, LLC
         2  SSI Shaws Road Solar, LLC
         2  Delaware Ave Solar, LLC
         2  Frankford DEB, LLC
         2  E Evens Community Energy Initiative LLC
         1  Grears Corner Solar, LLC
         1  Syncarpha Newark, LLC
         1  nan
         1  TPE Development, LLC (TPE DE KE19, LLC)
         1  West Evens Road Community Energy Initiative LLC
         1  DEL022-30423B Thorogoods Rd, LLC
         1  Chaberton Solar Crestone LLC
         1  TPE Development, LLC (SU75)
         1  Maryland Line Road Solar, LLC
         1  Glenville hollow Community Energy Initiative LLC
         1  Frankford Community Energy Initiative II LLC
         1  Hastings Community Energy Initiative LLC
         1  Econox Renewables Inc
         1  Syncarpha New Castle, LLC

COMPANY1 by dollars
      263.40        1 rows  Econox Renewables Inc
      235.19        1 rows  Kearsarge New Castle East LLC
      134.27        1 rows  Glenville hollow Community Energy Initiative LLC
      119.26        1 rows  Hartly DE Solar CSS LLC
      110.37        1 rows  TPE DE SU07, LLC
      105.24        1 rows  TPE Development, LLC (TPE DE KE19, LLC)
      103.36        1 rows  Chesapeake KE73 Solar, LLC
       96.85        1 rows  Syncarpha Newark, LLC
       95.78        1 rows  Rifle Range Road Solar, LLC
       90.80        2 rows  Chesapeake SU165 Solar, LLC
       80.93        1 rows  Dupont Highway Solar 1 LLC
       78.76        1 rows  Hartly Community Energy Initiative LLC
       78.08        1 rows  Taylor Mill Road Solar 1, LLC
       77.21        1 rows  SSI Blackiston Solar, LLC
       76.16        1 rows  Bridgeville DEA, LLC
       76.10        1 rows  Syncarpha New Castle, LLC
       74.31        1 rows  West Evens Road Community Energy Initiative LLC
       73.84        1 rows  TPE Development, LLC (SU75)
       69.83        1 rows  Frankford DEA, LLC
       65.21        1 rows  Pearsons Corner Community Energy Initiative LLC

SRC_SHA256 by rows
        67  71b4627da207f077317e34de73cce47d8e4b5100a6ab640566f1c4cb99475702

SRC_SHA256 by dollars
        3.6K       67 rows  71b4627da207f077317e34de73cce47d8e4b5100a6ab640566f1c4cb9947

## who x when

COMPANY1 by ISSUE_DATE, dollars = ACRES
  Bridgeville DEA, LLC                      2025:76.16
  Chaberton Solar Crestone LLC              2024:36.97
  Chesapeake KE73 Solar, LLC                2024:103.36
  Chesapeake SU165 Solar, LLC               2025:90.80
  DEL022-30423B Thorogoods Rd, LLC          2025:21.49
  Delaware Ave Solar, LLC                   2025:17.82
  E Evens Community Energy Initiative LLC   2025:21.76
  Econox Renewables Inc                     2024:263.40
  Frankford Community Energy Initiative II  2026:41.94
  Frankford DEB, LLC                        2025:57.13
  Glenville hollow Community Energy Initia  2025:134.27
  Grears Corner Solar, LLC                  2025:39.81
  Harbeson DEA, LLC                         2025:42.33
  Hartly Community Energy Initiative LLC    2024:78.76
  Hartly DE Solar CSS LLC                   2025:119.26
  Hastings Community Energy Initiative LLC  2024:57.81
  Maryland Line Road Solar, LLC             2025:21.43
  Rifle Range Road Solar, LLC               2025:95.78
  SSI Shaws Road Solar, LLC                 2025:24.50
  Syncarpha New Castle, LLC                 2025:76.10
  Syncarpha Newark, LLC                     2025:96.85
  TPE DE SU07, LLC                          2024:110.37
  TPE Development, LLC (SU75)               2023:73.84
  TPE Development, LLC (TPE DE KE19, LLC)   2024:105.24
  Taylor Mill Road Solar 1, LLC             2024:78.08
  West Evens Road Community Energy Initiat  2025:74.31

SRC_SHA256 by ISSUE_DATE, dollars = ACRES
  71b4627da207f077317e34de73cce47d8e4b5100  2023:73.84 2024:1.2K 2025:1.6K 2026:159.15

## what

COUNTY: Sussex 54%, Kent 33%, New Castle 13%

APPROVED: Yes 87%, No 12%, nan 1%

STATUS: Final 43%, Preliminary 28%, Prelim 27%, nan 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| THE_GEOM | other | 66 | 0 | {"type": "MultiPolygon",  2; {"type": "MultiPolygon",  1; {"type": "MultiPolygon",  1; {"type": "MultiPolygon",  1 |
| OBJECTID | other | 67 | 0 | 15240 1; 15217 1; 15256 1; 15212 1 |
| PIN | other | 67 | 0 | 7-00-10400-01-2700-00001 2; 233-5.00-187.01 1; 533-4.00-23.00 1; 1502600217 1 |
| ACRES | amount | 66 | 0 | 39.39783098 2; 21.49112788 1; 41.94339009 1; 45.49210327 1 |
| COUNTY | category | 3 | 0 | Sussex 36; Kent 22; New Castle 9 |
| UPDATED | date | 11 | 0 | 2025-05-15T00:00:00.000Z 34; 2025-12-29T00:00:00.000Z 7; 2025-10-13T00:00:00.000Z 5; 2025-08-14T00:00:00.000Z 4 |
| DOCKET_NO | other | 59 | 0 | 25-0032 4; 25-1261 2; 25-0996 2; 25-0813 2 |
| COMPANY1 | who | 59 | 0 | Harbeson DEA, LLC 4; E Evens Community Energy  2; Delaware Ave Solar, LLC 2; SSI Shaws Road Solar, LLC 2 |
| APPROVED | category | 3 | 0 | Yes 58; No 8; nan 1 |
| TAX_PARCEL | other | 68 | 0 | 233-5.00-187.01 1; 533-4.00-23.00 1; 1502600217 1; 532-6.00-32.00 1 |
| STATUS | category | 4 | 0 | Final 29; Preliminary 19; Prelim 18; nan 1 |
| SHAPE_AREA | amount | 66 | 0 | 265069.24913632998 2; 142491.33636722001 1; 277546.22963789001 1; 307938.780344125 1 |
| SHAPE_LEN | amount | 66 | 0 | 3167.5249331585105 2; 1537.08057374391 1; 2354.29177617304 1; 2395.3263720067503 1 |
| GLOBALID | other | 68 | 0 | {A7EDE98B-FD90-4276-8730- 1; {41F3135F-1229-4089-945D- 1; {57B43CE1-27F1-4D00-A5E5- 1; {718228EB-FCA7-45D6-83E5- 1 |
| CALC_ACRES | amount | 67 | 0 | 39.39783098 2; 21.49110262 1; 41.94341598 1; 45.49229877 1 |
| ISSUE_DATE | date | 25 | 0 | nan 9; 2025-02-19T00:00:00.000Z 8; 2025-10-15T00:00:00.000Z 5; 2024-06-12T00:00:00.000Z 4 |
| ORDERNUMB | other | 53 | 0 | nan 9; 10915 2; 10883 2; 10846 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:08:09.43811 67 |
| SOURCE_RUN_ID | audit | 1 | 0 | ccec133f-25b4-4e11-a8cb-9 67 |
| SRC_SHA256 | who | 1 | 0 | 71b4627da207f077317e34de7 67 |
