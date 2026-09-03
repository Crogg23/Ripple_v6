# PORTAL_SOC_CONNECTICUT_OPEN_421E7F6A7E

rows 2.0K  columns 11  scan 4.4s

roles: amount 4, audit 2, category 1, date 1, other 1, who 3

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TAXPAYER_COUNT | 2.0K | 10 | 27 | 415 | 5.9K | 125.5K |
| RETAIL_SALES | 2.0K | 0 | 1.37M | 209.93M | 2.93B | 31.50B |
| TOTAL_AMOUNT_DUE_6_35 | 2.0K | 0 | 69.0K | 6.61M | 41.89M | 850.46M |
| LUXURY_TAX_DUE_AT_7_75 | 2.0K | 0 | 0 | 189.8K | 2.86M | 16.93M |

## who

MUNICIPALITY by rows
        28  OUT OF STATE (170)
        27  NORWALK (103)
        26  WATERBURY (151)
        26  DANBURY (034)
        25  BRIDGEPORT (015)
        25  GREENWICH (057)
        25  STAMFORD (135)
        25  HARTFORD (064)
        24  MANCHESTER (077)
        24  WALLINGFORD (148)
        24  MILFORD (084)
        23  FAIRFIELD (051)
        23  HAMDEN (062)
        23  WEST HARTFORD (155)
        22  STRATFORD (138)
        22  BRANFORD (014)
        22  NEW HAVEN (093)
        21  SOUTHINGTON (131)
        21  MERIDEN (080)
        20  MIDDLETOWN (083)

MUNICIPALITY by dollars
       33.1K       28 rows  OUT OF STATE (170)
        3.9K       25 rows  STAMFORD (135)
        3.1K       27 rows  NORWALK (103)
        2.6K       26 rows  DANBURY (034)
        2.6K       25 rows  BRIDGEPORT (015)
        2.3K       22 rows  NEW HAVEN (093)
        2.3K       25 rows  HARTFORD (064)
        2.2K       25 rows  GREENWICH (057)
        2.0K       26 rows  WATERBURY (151)
        2.0K       23 rows  FAIRFIELD (051)
        1.9K       24 rows  MILFORD (084)
        1.8K       23 rows  WEST HARTFORD (155)
        1.6K       24 rows  WALLINGFORD (148)
        1.4K       24 rows  MANCHESTER (077)
        1.4K       21 rows  SOUTHINGTON (131)
        1.4K       19 rows  BRISTOL (017)
        1.4K       23 rows  HAMDEN (062)
        1.4K       22 rows  STRATFORD (138)
        1.2K       21 rows  MERIDEN (080)
        1.2K       19 rows  WESTPORT (158)

PERIODS_ENDING by rows
      2.0K  Quarter 1 - JAN to MAR

PERIODS_ENDING by dollars
      125.5K     2.0K rows  Quarter 1 - JAN to MAR

SRC_SHA256 by rows
      2.0K  f3aae4fb0bf63dea67a84ee36f5a964cbf4739fb09533860df1b684b3fc82772

SRC_SHA256 by dollars
      125.5K     2.0K rows  f3aae4fb0bf63dea67a84ee36f5a964cbf4739fb09533860df1b684b3fc8

## who x when

MUNICIPALITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = TAXPAYER_COUNT
  BRANFORD (014)                            2026:1.1K
  BRIDGEPORT (015)                          2026:2.6K
  BRISTOL (017)                             2026:1.4K
  DANBURY (034)                             2026:2.6K
  FAIRFIELD (051)                           2026:2.0K
  GREENWICH (057)                           2026:2.2K
  HAMDEN (062)                              2026:1.4K
  HARTFORD (064)                            2026:2.3K
  MANCHESTER (077)                          2026:1.4K
  MERIDEN (080)                             2026:1.2K
  MIDDLETOWN (083)                          2026:1.1K
  MILFORD (084)                             2026:1.9K
  NEW HAVEN (093)                           2026:2.3K
  NORWALK (103)                             2026:3.1K
  OUT OF STATE (170)                        2026:33.1K
  SOUTHINGTON (131)                         2026:1.4K
  STAMFORD (135)                            2026:3.9K
  STRATFORD (138)                           2026:1.4K
  WALLINGFORD (148)                         2026:1.6K
  WATERBURY (151)                           2026:2.0K
  WEST HARTFORD (155)                       2026:1.8K
  WESTPORT (158)                            2026:1.2K

PERIODS_ENDING by INGESTED_AT  LOAD STAMP, not an event date, dollars = TAXPAYER_COUNT
  Quarter 1 - JAN to MAR                    2026:125.5K

## what

NAICS_INDUSTRY_CODE: 230 Construction 11%, 560 Administrative and Support 10%, 453 Miscellaneous store retail 10%, 810 Other Services 10%, 540 Professional, Scientific a 10%, 310 Manufacturing 9%, 454 Nonstore retailers 9%, 720 Accomodation and Food Serv 8%, 420 Wholesale Trade 7%, 445 Food and beverage stores 6%, 710 Arts, Entertainment, Recre 6%, 110 Agriculture, Forestry, Fis 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CALENDAR_YEAR | other | 1 | 0 | 2019 2.0K |
| PERIODS_ENDING | who | 1 | 0 | Quarter 1 - JAN to MAR 2.0K |
| MUNICIPALITY | who | 159 | 0 | OUT OF STATE (170) 28; NORWALK (103) 27; WATERBURY (151) 26; DANBURY (034) 26 |
| NAICS_INDUSTRY_CODE | category | 28 | 0 | 230 Construction 157; 560 Administrative and Su 147; 453 Miscellaneous store r 144; 810 Other Services 142 |
| TAXPAYER_COUNT | amount | 225 | 0 | 10 106; 11 92; 12 79; 14 78 |
| RETAIL_SALES | amount | 2.0K | 0 | 0.00 11; 128378.00 10; 1313.00 10; 661552.00 10 |
| TOTAL_AMOUNT_DUE_6_35 | amount | 2.0K | 0 | 14311.06 10; 83.38 10; 23712.68 10; 31052.96 10 |
| LUXURY_TAX_DUE_AT_7_75 | amount | 161 | 0 | 0.00 1.8K; 4389.83 1; 2093.04 1; 81.07 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:48:02.25358 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 579dfa83-3fc0-46b3-bc68-d 2.0K |
| SRC_SHA256 | who | 1 | 0 | f3aae4fb0bf63dea67a84ee36 2.0K |
