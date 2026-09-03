# FED_FBI_NICS_CHECKS

rows 16.4K  columns 30  scan 3.1s

roles: amount 1, audit 2, category 4, other 20, who 3

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTALS | 16.4K | 0 | 14.0K | 248.5K | 1.43M | 460.38M |

## who

MONTH by rows
        55  2018-09
        55  2023-02
        55  2020-08
        55  2017-03
        55  2018-01
        55  2016-04
        55  2016-01
        55  2011-10
        55  2015-08
        55  2011-09
        55  2010-02
        55  2011-01
        55  2013-07
        55  2019-03
        55  2022-06
        55  2023-07
        55  2010-12
        55  2017-04
        55  2021-02
        55  2021-04

MONTH by dollars
       4.65M       55 rows  2021-03
       4.29M       55 rows  2021-01
       3.91M       55 rows  2020-06
       3.90M       55 rows  2020-12
       3.71M       55 rows  2020-03
       3.61M       55 rows  2020-07
       3.60M       55 rows  2020-11
       3.49M       55 rows  2021-04
       3.39M       55 rows  2021-02
       3.31M       55 rows  2015-12
       3.27M       55 rows  2020-10
       3.21M       55 rows  2021-05
       3.09M       55 rows  2020-08
       3.08M       55 rows  2021-12
       3.07M       55 rows  2020-05
       3.04M       55 rows  2021-06
       3.01M       55 rows  2022-03
       3.00M       55 rows  2022-12
       2.95M       55 rows  2023-03
       2.90M       55 rows  2019-12

STATE by rows
       299  Indiana
       299  Florida
       299  Colorado
       299  New Jersey
       299  Mariana Islands
       299  Oklahoma
       299  Delaware
       299  Minnesota
       299  Guam
       299  New Mexico
       299  Wisconsin
       299  Virginia
       299  Kansas
       299  Hawaii
       299  North Carolina
       299  California
       299  Washington
       299  Massachusetts
       299  Alabama
       299  Iowa

STATE by dollars
      54.07M      299 rows  Kentucky
      47.31M      299 rows  Illinois
      30.16M      299 rows  Texas
      27.53M      299 rows  California
      20.55M      299 rows  Florida
      20.37M      299 rows  Pennsylvania
      15.73M      299 rows  Indiana
      12.97M      299 rows  Ohio
      12.17M      299 rows  Tennessee
      11.81M      299 rows  North Carolina
      11.77M      299 rows  Michigan
      11.21M      299 rows  Alabama
      11.17M      299 rows  Georgia
      11.15M      299 rows  Minnesota
      10.50M      299 rows  Washington
       9.92M      299 rows  Missouri
       9.68M      299 rows  Utah
       9.45M      299 rows  Virginia
       9.43M      299 rows  Colorado
       8.72M      299 rows  Wisconsin

SRC_SHA256 by rows
     16.4K  ae0476f1bfe0df28582c8a3a6aecedda4ce0e9ad779cb875971611344533cfd6

SRC_SHA256 by dollars
     460.38M    16.4K rows  ae0476f1bfe0df28582c8a3a6aecedda4ce0e9ad779cb875971611344533

## what

PREPAWN_OTHER: 0 81%, 1 11%, 2 4%, 3 2%, 4 1%, 5 0%, 8 0%, 7 0%, 9 0%, 6 0%, 10 0%

RENTALS_HANDGUN: 0 97%, 1 1%, 2 1%, 3 0%, 4 0%, 7 0%, 5 0%, 9 0%, 6 0%, 10 0%, 12 0%

RENTALS_LONG_GUN: 0 97%, 2 1%, 3 0%, 5 0%, 1 0%, 4 0%, 6 0%, 8 0%, 7 0%, 12 0%, 10 0%

RETURN_TO_SELLER_OTHER: 0 91%, 1 7%, 2 2%, 3 0%, 4 0%, 5 0%, 18 0%, 6 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MONTH | who | 302 | 0 | 1998-11 110; 1998-12 110; 1999-01 110; 1999-02 110 |
| STATE | who | 54 | 0 | Wyoming 299; Wisconsin 299; West Virginia 299; Washington 299 |
| PERMIT | other | 7.4K | 24 | 0 5.2K; 1 83; 2 63; 4 59 |
| PERMIT_RECHECK | other | 1.2K | 11.4K | 0 2.6K; 1 117; 2 80; 3 65 |
| HANDGUN | other | 9.4K | 20 | 0 756; 1 112; 2 87; 149 80 |
| LONG_GUN | other | 10.3K | 19 | 0 686; 1 129; 2 94; 35 80 |
| OTHER | other | 2.2K | 7.0K | 0 1.3K; 1 79; 16 64; 10 58 |
| MULTIPLE | other | 1.7K | 0 | 0 2.3K; 1 321; 2 232; 3 189 |
| ADMIN | other | 555 | 23 | 0 12.5K; 1 773; 2 454; 3 280 |
| PREPAWN_HANDGUN | other | 106 | 1.9K | 0 7.7K; 1 1.1K; 2 711; 3 568 |
| PREPAWN_LONG_GUN | other | 138 | 1.9K | 0 6.6K; 1 1.2K; 2 848; 3 662 |
| PREPAWN_OTHER | category | 22 | 7.4K | 0 7.4K; 1 964; 2 363; 3 157 |
| REDEMPTION_HANDGUN | other | 2.3K | 1.9K | 0 4.9K; 1 347; 2 270; 3 192 |
| REDEMPTION_LONG_GUN | other | 2.5K | 1.9K | 0 4.3K; 1 175; 2 145; 4 99 |
| REDEMPTION_OTHER | other | 79 | 7.4K | 0 4.7K; 1 1.1K; 2 709; 3 489 |
| RETURNED_HANDGUN | other | 634 | 10.3K | 0 2.4K; 1 183; 2 104; 4 68 |
| RETURNED_LONG_GUN | other | 195 | 10.3K | 0 2.9K; 1 273; 2 196; 3 188 |
| RETURNED_OTHER | other | 114 | 10.7K | 0 4.0K; 1 565; 2 298; 3 188 |
| RENTALS_HANDGUN | category | 15 | 11.5K | 0 4.8K; 1 40; 2 32; 3 23 |
| RENTALS_LONG_GUN | category | 15 | 11.7K | 0 4.6K; 2 26; 3 23; 5 22 |
| PRIVATE_SALE_HANDGUN | other | 443 | 9.7K | 0 3.3K; 7 142; 1 139; 3 138 |
| PRIVATE_SALE_LONG_GUN | other | 360 | 9.7K | 0 3.0K; 5 180; 2 174; 4 172 |
| PRIVATE_SALE_OTHER | other | 168 | 9.7K | 0 4.1K; 1 700; 2 456; 3 260 |
| RETURN_TO_SELLER_HANDGUN | other | 67 | 10.0K | 0 4.9K; 1 750; 2 323; 3 147 |
| RETURN_TO_SELLER_LONG_GUN | other | 52 | 9.7K | 0 5.0K; 1 846; 2 346; 3 164 |
| RETURN_TO_SELLER_OTHER | category | 9 | 10.2K | 0 5.7K; 1 406; 2 102; 3 29 |
| TOTALS | amount | 13.5K | 0 | 0 290; 1 92; 2 87; 107 83 |
| INGESTED_AT | audit | 1 | 0 | 1782615724041597 16.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 71862c93-4059-442c-a7d1-5 16.4K |
| SRC_SHA256 | who | 1 | 0 | ae0476f1bfe0df28582c8a3a6 16.4K |
