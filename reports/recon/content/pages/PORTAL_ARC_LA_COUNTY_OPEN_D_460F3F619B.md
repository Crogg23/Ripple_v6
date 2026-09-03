# PORTAL_ARC_LA_COUNTY_OPEN_D_460F3F619B

rows 366  columns 20  scan 3.6s

roles: amount 2, audit 2, category 7, date 1, other 6, who 3

## when

INGESTED_AT
  2026       366  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 366 | 33.74 | 34.10 | 34.32 | 34.32 | 12.5K |
| LONGITUDE | 366 | -118.64 | -118.39 | -118.20 | -118.19 | -43.3K |

## who

COMPANY_NM by rows
         6  Cedars-Sinai Medical Center
         6  University of California, Los
         5  Kaiser Foundation Hospitals
         5  County of Los Angeles
         4  Motion Picture and Television
         3  Childrens Hospital Los Angeles
         3  Good Samaritan Hospital
         2  Dignity Health
         2  Banfield Pet Hospital
         2  University of Southern Califor
         2  Amisub of California, Inc.
         2  White Memorial Medical Center
         2  Cfhs Holdings, Inc.
         2  Tenet Healthsystem Medical, In
         2  Gateway's Hospital and Mental
         2  Kaiser Permanente Internationa
         1  Burn Center Recovery
         1  Reality House
         1  Champion Medical Group Corp
         1  Lavender Hospice, Inc.

COMPANY_NM by dollars
      204.67        6 rows  University of California, Los
      204.41        6 rows  Cedars-Sinai Medical Center
      170.72        5 rows  Kaiser Foundation Hospitals
      170.69        5 rows  County of Los Angeles
      136.52        4 rows  Motion Picture and Television
      102.30        3 rows  Childrens Hospital Los Angeles
      102.16        3 rows  Good Samaritan Hospital
       68.35        2 rows  Tenet Healthsystem Medical, In
       68.33        2 rows  Amisub of California, Inc.
       68.16        2 rows  Gateway's Hospital and Mental
       68.10        2 rows  White Memorial Medical Center
       68.10        2 rows  Dignity Health
       68.08        2 rows  University of Southern Califor
       68.02        2 rows  Banfield Pet Hospital
       67.96        2 rows  Cfhs Holdings, Inc.
       67.78        2 rows  Kaiser Permanente Internationa
       34.32        1 rows  Olive View Medical Center
       34.32        1 rows  Oasis Women's Recovering Commu
       34.32        1 rows  Narconon Drug Prevention & Edu
       34.31        1 rows  Total Family Support Clinic

TRACT by rows
        13  214900
        12  191300
        11  203300
        10  265301
         9  128702
         9  125400
         9  139400
         5  267200
         5  267100
         5  224010
         5  139701
         4  275302
         4  134422
         4  216300
         4  106606
         4  128100
         4  139600
         3  267700
         3  103400
         3  127220

TRACT by dollars
      442.92       13 rows  214900
      409.20       12 rows  191300
      374.66       11 rows  203300
      340.68       10 rows  265301
      307.53        9 rows  139400
      307.44        9 rows  128702
      307.35        9 rows  125400
      170.80        5 rows  139701
      170.29        5 rows  267100
      170.24        5 rows  267200
      170.19        5 rows  224010
      137.12        4 rows  106606
      136.80        4 rows  134422
      136.76        4 rows  128100
      136.66        4 rows  139600
      136.24        4 rows  216300
      135.92        4 rows  275302
      102.96        3 rows  106010
      102.78        3 rows  103400
      102.66        3 rows  115402

SRC_SHA256 by rows
       366  831686fd55c6e6fb06c5b5365cb232e6fed9f45363df894f4d9dfaa18657c7be

SRC_SHA256 by dollars
       12.5K      366 rows  831686fd55c6e6fb06c5b5365cb232e6fed9f45363df894f4d9dfaa18657

## who x when

COMPANY_NM by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  Amisub of California, Inc.                2026:68.33
  Banfield Pet Hospital                     2026:68.02
  Burn Center Recovery                      2026:34.16
  Cedars-Sinai Medical Center               2026:204.41
  Cfhs Holdings, Inc.                       2026:67.96
  Champion Medical Group Corp               2026:34.06
  Childrens Hospital Los Angeles            2026:102.30
  County of Los Angeles                     2026:170.69
  Dignity Health                            2026:68.10
  Gateway's Hospital and Mental             2026:68.16
  Good Samaritan Hospital                   2026:102.16
  Kaiser Foundation Hospitals               2026:170.72
  Kaiser Permanente Internationa            2026:67.78
  Lavender Hospice, Inc.                    2026:34.26
  Motion Picture and Television             2026:136.52
  Narconon Drug Prevention & Edu            2026:34.32
  Oasis Women's Recovering Commu            2026:34.32
  Olive View Medical Center                 2026:34.32
  Reality House                             2026:33.99
  Tenet Healthsystem Medical, In            2026:68.35
  Total Family Support Clinic               2026:34.31
  University of California, Los             2026:204.67
  University of Southern Califor            2026:68.08
  White Memorial Medical Center             2026:68.10

TRACT by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  103400                                    2026:102.78
  106010                                    2026:102.96
  106606                                    2026:137.12
  115402                                    2026:102.66
  125400                                    2026:307.35
  127220                                    2026:102.61
  128100                                    2026:136.76
  128702                                    2026:307.44
  134422                                    2026:136.80
  139400                                    2026:307.53
  139600                                    2026:136.66
  139701                                    2026:170.80
  191300                                    2026:409.20
  203300                                    2026:374.66
  214900                                    2026:442.92
  216300                                    2026:136.24
  224010                                    2026:170.19
  265301                                    2026:340.68
  267100                                    2026:170.29
  267200                                    2026:170.24
  267700                                    2026:102.12
  275302                                    2026:135.92

## what

STREETCITY: Los Angeles 57%, North Hollywood 10%, Van Nuys 9%, Sherman Oaks 4%, Tarzana 3%, Encino 3%, Woodland Hills 3%, Sylmar 3%, Canoga Park 2%, Marina Del Rey 2%, Reseda 2%, Northridge 2%

NAICS_CD: 622110 51%, 622310 28%, 622210 20%

NAICS_DESC: General Medical and Surgical H 51%, Specialty (except Psychiatric  28%, Psychiatric and Substance Abus 20%

LWIA: Los Angeles City 96%, Los Angeles County 4%

LWDA: LA City 99%, LA County 1%

SUP: 3 62%, 2 16%, 1 15%, 5 5%, 4 1%

WFR: San Fernando Valley 52%, Central LA 25%, Westside Cities 20%, South Bay 2%, Gateway Cities 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | other | 365 | 0 | 366 2; 365 2; 364 2; 363 2 |
| OBJECTID_1 | other | 1 | 0 | 0 366 |
| COMPANY_NM | who | 321 | 0 | Cedars-Sinai Medical Cent 6; University of California, 6; County of Los Angeles 5; Kaiser Foundation Hospita 5 |
| TRADESTYLE | other | 83 | 277 | Hollywood Presbyterian Me 2; Sylmar Hlth Rehabilitatio 2; Cardiology Department 2; Ucla Medical Center 2 |
| STREETCITY | category | 34 | 0 | Los Angeles 180; North Hollywood 32; Van Nuys 28; Sherman Oaks 14 |
| STREETZIP | other | 93 | 0 | 90048 18; 90027 16; 90033 15; 90025 12 |
| NAICS_CD | category | 3 | 0 | 622110 187; 622310 104; 622210 75 |
| NAICS_DESC | category | 3 | 0 | General Medical and Surgi 187; Specialty (except Psychia 104; Psychiatric and Substance 75 |
| LATITUDE | amount | 308 | 0 | 34.15355 7; 34.09801 6; 34.07374 5; 33.98169 4 |
| LONGITUDE | amount | 312 | 0 | -118.36794 7; -118.29064 7; -118.43997 4; -118.44888 4 |
| TRACT | who | 209 | 0 | 214900 13; 191300 12; 203300 11; 265301 10 |
| FIPSSTCO | other | 1 | 0 | 06037 366 |
| LWIA | category | 2 | 0 | Los Angeles City 350; Los Angeles County 16 |
| LWDA | category | 2 | 0 | LA City 363; LA County 3 |
| SUP | category | 5 | 0 | 3 228; 2 60; 1 55; 5 18 |
| WFR | category | 5 | 0 | San Fernando Valley 191; Central LA 92; Westside Cities 73; South Bay 8 |
| GEOMETRY | other | 316 | 0 | {"type": "Point", "coordi 7; {"type": "Point", "coordi 6; {"type": "Point", "coordi 4; {"type": "Point", "coordi 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:23:07.51754 366 |
| SOURCE_RUN_ID | audit | 1 | 0 | 19a7f418-7c76-471d-802a-4 366 |
| SRC_SHA256 | who | 1 | 0 | 831686fd55c6e6fb06c5b5365 366 |
