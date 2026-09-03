# PORTAL_SOC_NEW_YORK_STATE_O_4A5291BE83

rows 2.0K  columns 15  scan 3.3s

roles: amount 1, audit 2, category 4, date 1, other 6, who 2

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_WAGE | 2.0K | 14.5K | 4.92M | 14.81B | 280.18B | 2849.81B |

## who

AREA by rows
        52  New York City
        23  New York State
        22  Chemung-Schuyler-Steuben
        22  Buffalo-Cheektowaga Metro Area
        22  Dutchess
        22  Niagara
        22  Ontario County
        22  Ontario-Seneca-Wayne-Yates
        22  Onondaga
        22  Mohawk Valley
        22  Tompkins County
        22  Finger Lakes
        22  Syracuse Metro Area
        22  Central New York
        22  Orange-Rockland-Westchester Metro Area
        22  Columbia County
        22  Kiryas Joel-Poughkeepsie-Newburgh NY
        22  Capital Region
        22  Western New York
        22  Southern Tier

AREA by dollars
    1131.95B       52 rows  New York City
     594.97B       23 rows  New York State
     297.51B       13 rows  New York County
      57.07B       18 rows  Long Island
      57.07B       18 rows  Nassau-Suffolk Metropolitan Division
      43.37B       22 rows  Hudson Valley
      34.56B       22 rows  Orange-Rockland-Westchester Metro Area
      31.44B       16 rows  Kings County
      30.00B       18 rows  Suffolk
      30.00B       18 rows  Suffolk County
      29.62B       11 rows  Queens County
      27.07B       10 rows  Nassau County
      23.81B       19 rows  Westchester County
      23.03B       22 rows  Western New York
      22.69B       22 rows  Capital Region
      20.36B       22 rows  Finger Lakes
      20.27B       22 rows  Buffalo-Cheektowaga Metro Area
      19.98B       22 rows  Albany-Schenectady-Troy Metro Area
      18.43B       22 rows  Rochester Metro Area
      18.05B       18 rows  Erie County

SRC_SHA256 by rows
      2.0K  3e3fcfa36bfff9324d256d388eef06abbac38d52afe7f484cc9019d96c94949d

SRC_SHA256 by dollars
    2849.81B     2.0K rows  3e3fcfa36bfff9324d256d388eef06abbac38d52afe7f484cc9019d96c94

## who x when

AREA by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_WAGE
  Buffalo-Cheektowaga Metro Area            2026:20.27B
  Capital Region                            2026:22.69B
  Central New York                          2026:13.48B
  Chemung-Schuyler-Steuben                  2026:3.03B
  Columbia County                           2026:698.24M
  Dutchess                                  2026:4.59B
  Finger Lakes                              2026:20.36B
  Hudson Valley                             2026:43.37B
  Kings County                              2026:31.44B
  Kiryas Joel-Poughkeepsie-Newburgh NY      2026:10.12B
  Long Island                               2026:57.07B
  Mohawk Valley                             2026:6.31B
  Nassau County                             2026:27.07B
  Nassau-Suffolk Metropolitan Division      2026:57.07B
  New York City                             2026:1131.95B
  New York County                           2026:297.51B
  New York State                            2026:594.97B
  Niagara                                   2026:2.22B
  Onondaga                                  2026:10.06B
  Ontario County                            2026:1.94B
  Ontario-Seneca-Wayne-Yates                2026:3.58B
  Orange-Rockland-Westchester Metro Area    2026:34.56B
  Queens County                             2026:29.62B
  Southern Tier                             2026:9.54B
  Suffolk                                   2026:30.00B
  Suffolk County                            2026:30.00B
  Syracuse Metro Area                       2026:11.98B
  Tompkins County                           2026:1.84B
  Westchester County                        2026:23.81B
  Western New York                          2026:23.03B

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_WAGE
  3e3fcfa36bfff9324d256d388eef06abbac38d52  2026:2849.81B

## what

AREA_TYPE: County 46%, Workforce Investment Region 27%, Metropolitan Statistical Area 13%, Labor Market Area 10%, Metropolitan Division 2%, State 1%

OWNERSHIP: Private 39%, Total, All Ownerships 38%, Local Government 6%, Federal Government 6%, Total, All Government 6%, State Government 6%

NAICS: 00 35%, 11 12%, 111 11%, 112 10%, 1112 8%, 1114 7%, 1119 6%, 1113 6%, 1111 5%, 1121 0%

NAICS_TITLE: Total, All Industries 35%, Agriculture, Forestry, Fishing 12%, Crop Production 11%, Animal Production 10%, Vegetable and Melon Farming 8%, Greenhouse and Nursery Product 7%, Other Crop Farming 6%, Fruit and Tree Nut Farming 6%, Oilseed and Grain Farming 5%, Cattle Ranching and Farming 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA_TYPE | category | 6 | 0 | County 918; Workforce Investment Regi 546; Metropolitan Statistical  265; Labor Market Area 209 |
| AREA | who | 117 | 0 | New York City 52; New York State 23; Syracuse Metro Area 22; Rochester Metro Area 22 |
| YEAR | other | 1 | 0 | 2025 2.0K |
| QUARTER | other | 1 | 0 | 1 2.0K |
| OWNERSHIP | category | 6 | 0 | Private 771; Total, All Ownerships 759; Local Government 118; Federal Government 118 |
| NAICS | category | 10 | 0 | 00 706; 11 233; 111 213; 112 209 |
| NAICS_TITLE | category | 10 | 0 | Total, All Industries 706; Agriculture, Forestry, Fi 233; Crop Production 213; Animal Production 209 |
| ESTABLISHMENTS | other | 481 | 0 | 3 79; 10 69; 5 62; 8 55 |
| MONTH_1_EMPLOYMENT | other | 869 | 0 | 30 24; 13 21; 19 21; 3 21 |
| MONTH_2_EMPLOYMENT | other | 847 | 0 | 7 28; 11 26; 29 23; 4 21 |
| MONTH_3_EMPLOYMENT | other | 852 | 0 | 26 32; 10 26; 4 23; 6 23 |
| TOTAL_WAGE | amount | 1.1K | 0 | 1012062 14; 2234406 14; 921338 13; 303996 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:50.12436 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | f678da27-54fb-4833-8d32-7 2.0K |
| SRC_SHA256 | who | 1 | 0 | 3e3fcfa36bfff9324d256d388 2.0K |
