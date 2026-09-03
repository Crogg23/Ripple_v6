# FED_CFTC_COT_FINANCIAL_HIST

rows 4.6K  columns 90  scan 6.6s

roles: amount 53, audit 2, category 11, date 1, id 5, other 11, who 7

## when

REPORT_DATE_AS_MM_DD_YYYY
  2010       836  #############
  2011      1.9K  ##############################
  2012      1.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CHANGE_IN_OPEN_INTEREST_ALL | 4.6K | -1.17M | 816 | 175.4K | 575.0K | 1.12M |
| CHANGE_IN_DEALER_LONG_ALL | 4.6K | -390.9K | 20 | 56.1K | 342.5K | -533.2K |
| CHANGE_IN_DEALER_SHORT_ALL | 4.6K | -565.7K | 89 | 71.9K | 298.2K | -116.1K |
| CHANGE_IN_DEALER_SPREAD_ALL | 4.6K | -395.9K | 1 | 60.9K | 291.0K | -10.7K |
| CHANGE_IN_ASSET_MGR_LONG_ALL | 4.6K | -261.9K | 0 | 57.1K | 232.9K | -764.5K |
| CHANGE_IN_ASSET_MGR_SHORT_ALL | 4.6K | -182.4K | 0 | 58.1K | 235.3K | 261.2K |

## who

OTHER_REPT_POSITIONS_SPREAD_ALL by rows
      2.3K         0
        41         1
        26         2
        19        50
        17      2861
        16        12
        15         5
        14         4
        12      2855
        12       602
        11         3
         9         6
         9        17
         9        38
         8       286
         8        14
         8        45
         8       250
         7      7989
         7       587

OTHER_REPT_POSITIONS_SPREAD_ALL by dollars
      575.0K        1 rows     19332
      557.8K        1 rows     36154
      460.9K        1 rows    178327
      434.1K        1 rows     14613
      416.3K        1 rows    120186
      411.8K        1 rows     14059
      409.0K        1 rows    148840
      393.9K        1 rows    134299
      390.8K        1 rows     32039
      389.0K        1 rows     50769
      356.5K        1 rows    113471
      348.2K        1 rows     19153
      345.8K        1 rows    158340
      342.0K        1 rows    181458
      326.8K        1 rows     17872
      318.3K        1 rows     57163
      305.5K        1 rows    158825
      305.2K        1 rows    174280
      295.2K        1 rows    333015
      288.6K        1 rows     56067

TRADERS_TOT_ALL by rows
        85       21
        79       20
        76       22
        72       23
        64       98
        60       24
        51       29
        51       30
        48      100
        47       95
        47       88
        46       91
        46       99
        44       87
        44       31
        44       97
        43       90
        43       96
        42       92
        41       47

TRADERS_TOT_ALL by dollars
      808.9K       11 rows      262
      727.9K        8 rows      526
      712.0K        3 rows      573
      674.8K        5 rows      534
      619.9K        5 rows      273
      566.8K       17 rows      243
      529.8K        5 rows      537
      495.6K        9 rows      261
      444.5K       10 rows      255
      444.5K        4 rows      303
      443.2K       12 rows      254
      436.2K        5 rows      563
      434.1K        1 rows      497
      426.1K        3 rows      500
      415.4K       11 rows      245
      386.3K       11 rows      242
      384.8K        4 rows      267
      379.5K        5 rows      515
      375.7K       19 rows      251
      358.5K        2 rows      586

TRADERS_TOT_REPT_SHORT_ALL by rows
        84       21
        80       20
        79       23
        73       44
        70       18
        69       19
        68       16
        66       22
        65       47
        64       17
        63       48
        63       12
        61       50
        59       34
        59       42
        58       24
        58       25
        57       49
        56       43
        55       26

TRADERS_TOT_REPT_SHORT_ALL by dollars
      866.4K        4 rows      222
      811.7K        2 rows      384
      624.8K        5 rows      220
      623.3K        3 rows      246
      599.7K        2 rows      388
      565.4K        2 rows      245
      536.8K        4 rows      234
      489.2K        2 rows      377
      468.9K        4 rows      331
      467.9K        2 rows      243
      465.2K        3 rows      236
      458.5K        3 rows      364
      458.4K        3 rows      351
      451.0K        8 rows      205
      448.5K        5 rows      215
      425.1K        7 rows      201
      424.9K        3 rows      238
      395.4K        4 rows      242
      372.1K        3 rows      435
      362.2K        2 rows      373

TRADERS_TOT_REPT_LONG_ALL by rows
        96       17
        94       15
        92       14
        89       13
        80       16
        70       12
        68       18
        58       58
        55       11
        53       67
        52       59
        52       65
        50       44
        49       19
        48       38
        48       46
        48       56
        47       62
        47       50
        46       43

TRADERS_TOT_REPT_LONG_ALL by dollars
       1.21M        5 rows      227
      862.2K        3 rows      241
      636.2K        6 rows      362
      632.9K        5 rows      229
      511.6K        2 rows      244
      507.3K        3 rows      361
      503.3K        5 rows      224
      503.1K        5 rows      214
      501.4K        6 rows      220
      452.7K        4 rows      346
      434.1K        1 rows      327
      414.2K        4 rows      237
      408.1K        3 rows      344
      393.9K        1 rows      240
      390.8K        1 rows      378
      380.3K        2 rows      254
      371.0K       23 rows      108
      351.9K        2 rows      358
      347.4K        4 rows      230
      330.6K        3 rows      219

## who x when

OTHER_REPT_POSITIONS_SPREAD_ALL by REPORT_DATE_AS_MM_DD_YYYY, dollars = CHANGE_IN_OPEN_INTEREST_ALL
         0                                  2010:190.5K 2011:-748.6K 2012:-519.2K
         1                                  2010:64.1K 2011:-33.8K 2012:-72.6K
         2                                  2010:2.8K 2011:118.7K 2012:-164.5K
         3                                  2010:7.5K 2011:644 2012:21.0K
         4                                  2010:12.1K 2011:-65.6K 2012:7.4K
         5                                  2010:-4.5K 2011:42.7K 2012:-24.9K
         6                                  2011:3.6K 2012:-6.1K
        12                                  2010:-4.9K 2011:-28.9K 2012:-89.6K
        14                                  2010:0 2011:29.5K 2012:-5.2K
        17                                  2010:-17.9K 2011:-3.0K
        38                                  2010:-42.0K 2011:927 2012:61.5K
        45                                  2010:22.4K 2012:-39.4K
        50                                  2010:-55.4K 2011:-42.4K 2012:-30.3K
       250                                  2011:6.5K 2012:44.8K
       286                                  2011:-6.2K 2012:67
       587                                  2011:-49.1K 2012:45.1K
       602                                  2010:7.0K 2011:-8.2K
      2855                                  2012:-6.1K
      2861                                  2012:-23.3K
      7989                                  2012:-21.8K
     14059                                  2010:411.8K
     14613                                  2010:434.1K
     19332                                  2011:575.0K
     32039                                  2012:390.8K
     36154                                  2011:557.8K
     50769                                  2011:389.0K
    120186                                  2011:416.3K
    134299                                  2011:393.9K
    148840                                  2011:409.0K
    178327                                  2011:460.9K

TRADERS_TOT_ALL by REPORT_DATE_AS_MM_DD_YYYY, dollars = CHANGE_IN_OPEN_INTEREST_ALL
       20                                   2010:6.2K 2011:1.8K 2012:279
       21                                   2010:10.5K 2011:25.0K 2012:939
       22                                   2010:-12.8K 2011:16.4K 2012:6.9K
       23                                   2010:15.7K 2011:-322 2012:26.5K
       24                                   2010:6.1K 2011:19.8K 2012:-9.8K
       29                                   2010:-21.4K 2011:-13.7K 2012:-1.4K
       30                                   2010:2.4K 2011:-621 2012:-8.2K
       31                                   2010:6.4K 2011:-30.4K 2012:-9.5K
       47                                   2010:1.9K 2011:7.9K 2012:21.4K
       87                                   2010:55.8K 2011:-120.7K 2012:-2.1K
       88                                   2010:-22.1K 2011:18.3K 2012:-62.3K
       90                                   2010:-3.8K 2011:68.9K 2012:48.3K
       91                                   2010:22.1K 2011:1.9K 2012:-37.1K
       92                                   2010:-5.4K 2011:24.8K 2012:-50.5K
       95                                   2010:-2.5K 2011:60.5K 2012:39.9K
       96                                   2010:-10.3K 2011:-13.1K 2012:69.0K
       97                                   2010:36.7K 2011:71.3K 2012:-34.9K
       98                                   2010:-59.9K 2011:-19.2K 2012:-115.7K
       99                                   2010:1.1K 2011:32.3K 2012:-193.2K
      100                                   2010:13.9K 2011:63.8K 2012:-40.1K
      243                                   2010:294.1K 2011:174.6K 2012:98.1K
      255                                   2010:23.0K 2011:-36.2K 2012:457.7K
      261                                   2011:511.6K 2012:-15.9K
      262                                   2010:94.1K 2011:491.9K 2012:222.9K
      273                                   2011:527.6K 2012:92.4K
      303                                   2011:305.2K 2012:139.3K
      526                                   2010:5.3K 2011:833.7K 2012:-111.2K
      534                                   2011:574.9K 2012:99.8K
      537                                   2010:27.9K 2012:501.9K
      573                                   2011:706.4K 2012:5.5K

## what

MARKET_AND_EXCHANGE_NAMES: VIX FUTURES - CBOE FUTURES EXC 8%, U.S. DOLLAR INDEX - ICE FUTURE 8%, INTEREST RATE SWAPS 5YR - CHIC 8%, INTEREST RATE SWAPS 10YR - CHI 8%, 3-MONTH EURODOLLARS - CHICAGO  8%, 30-DAY FEDERAL FUNDS - CHICAGO 8%, 5-YEAR U.S. TREASURY NOTES - C 8%, 10-YEAR U.S. TREASURY NOTES -  8%, 2-YEAR U.S. TREASURY NOTES - C 8%, LONG-TERM U.S. TREASURY BONDS  8%, U.S. TREASURY BONDS - CHICAGO  8%, NIKKEI STOCK AVERAGE YEN DENOM 8%

CFTC_CONTRACT_MARKET_CODE: 1170E1  8%, 098662  8%, 247602  8%, 246602  8%, 132741  8%, 045601  8%, 044601  8%, 043602  8%, 042601  8%, 020604  8%, 020601  8%, 240743  8%

CFTC_MARKET_CODE: CME  57%, CBT  31%, ICUS  6%, NYL  4%, E  3%, NYL2  0%

CFTC_REGION_CODE: 00  91%, 01  9%

CFTC_COMMODITY_CODE: 138  18%, 209  12%, 124  10%, 246  9%, 020  9%, 240  9%, 244  9%, 045  5%, 042  5%, 117  5%, 098  5%, 132  5%

CONTRACT_UNITS: (CONTRACTS OF $100,000 FACE VA 21%, (CONTRACTS OF $100,000)  11%, (S&P 500 INDEX X $250.00)  11%, (NASDAQ 100 INDEX X $100)  9%, (MSCI EAFE INDEX X $50)  9%, ($10 X DJIA INDEX)  7%, (CONTRACTS OF $5,000,000)  6%, ($1000 X INDEX)  5%, (U.S. DOLLAR INDEX X $1000)  5%, (CONTRACTS OF $1,000,000)  5%, (CONTRACTS OF $200,000 FACE VA 5%, (NIKKEI INDEX X JPY 500)  5%

CFTC_CONTRACT_MARKET_CODE_QUOTES: 1170E1  8%, 098662  8%, 247602  8%, 246602  8%, 132741  8%, 045601  8%, 044601  8%, 043602  8%, 042601  8%, 020604  8%, 020601  8%, 240743  8%

CFTC_MARKET_CODE_QUOTES: CME  57%, CBT  31%, ICUS  6%, NYL  4%, E  3%, NYL2  0%

CFTC_COMMODITY_CODE_QUOTES: 138  18%, 209  12%, 124  10%, 246  9%, 020  9%, 240  9%, 244  9%, 045  5%, 042  5%, 117  5%, 098  5%, 132  5%

CFTC_SUBGROUP_CODE: F20  39%, F10  17%, F30  14%, F33  12%, F15  10%, F90  9%

SRC_SHA256: c5b65a8c3e0f597fae6b41eaba9246 41%, 583a93474847f1070b213e2b12cfa7 41%, 5392a28735d28dcb8feb5e60282c7c 18%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MARKET_AND_EXCHANGE_NAMES | category | 41 | 0 | VIX FUTURES - CBOE FUTURE 129; U.S. DOLLAR INDEX - ICE F 129; INTEREST RATE SWAPS 5YR - 129; INTEREST RATE SWAPS 10YR  129 |
| AS_OF_DATE_IN_FORM_YYMMDD | who | 130 | 0 | 110614  39; 120911  38; 120918  38; 110524  38 |
| REPORT_DATE_AS_MM_DD_YYYY | date | 128 | 0 | 2011-06-14 39; 2012-09-11 38; 2012-09-18 38; 2011-05-24 38 |
| CFTC_CONTRACT_MARKET_CODE | category | 40 | 0 | 1170E1  129; 098662  129; 247602  129; 246602  129 |
| CFTC_MARKET_CODE | category | 6 | 0 | CME  2.6K; CBT  1.4K; ICUS  258; NYL  164 |
| CFTC_REGION_CODE | category | 2 | 0 | 00  4.2K; 01  422 |
| CFTC_COMMODITY_CODE | category | 26 | 0 | 138  516; 209  354; 124  296; 246  258 |
| OPEN_INTEREST_ALL | id | 4.6K | 0 |    10903 24;     9711 24;     9528 24;    10350 24 |
| DEALER_POSITIONS_LONG_ALL | other | 4.3K | 0 |        0 61;      844 27;      222 26;    11727 25 |
| DEALER_POSITIONS_SHORT_ALL | id | 4.5K | 0 |     6965 25;     8245 24;     8397 24;     8242 24 |
| DEALER_POSITIONS_SPREAD_ALL | other | 3.1K | 0 |        0 560;        1 32;       20 25;     1262 24 |
| ASSET_MGR_POSITIONS_LONG_ALL | other | 4.2K | 0 |        0 162;        9 31;     1036 27;     1058 25 |
| ASSET_MGR_POSITIONS_SHORT_ALL | other | 3.7K | 0 |        0 388;     2015 31;      973 29;      300 29 |
| ASSET_MGR_POSITIONS_SPREAD_ALL | other | 3.0K | 0 |        0 622;        6 49;       42 29;       45 28 |
| LEV_MONEY_POSITIONS_LONG_ALL | other | 4.3K | 0 |        0 33;     1817 26;     1658 25;     1708 25 |
| LEV_MONEY_POSITIONS_SHORT_ALL | id | 4.5K | 0 |     1131 24;     1159 24;     1145 24;     1799 24 |
| LEV_MONEY_POSITIONS_SPREAD_ALL | other | 2.9K | 0 |        0 459;        4 36;        3 35;      594 31 |
| OTHER_REPT_POSITIONS_LONG_ALL | other | 3.2K | 0 |        0 426;       40 43;     4800 37;      290 34 |
| OTHER_REPT_POSITIONS_SHORT_ALL | other | 3.2K | 0 |        0 594;       30 39;      215 33;      305 26 |
| OTHER_REPT_POSITIONS_SPREAD_ALL | who | 1.6K | 0 |        0 2.3K;        1 41;        2 26;     2861 23 |
| TOT_REPT_POSITIONS_LONG_ALL | id | 4.6K | 0 |     9545 24;     8470 24;     8107 24;     8935 24 |
| TOT_REPT_POSITIONS_SHORT_ALL | id | 4.7K | 0 |    10580 24;     9556 24;     9387 24;    10083 24 |
| NONREPT_POSITIONS_LONG_ALL | other | 4.3K | 0 |      125 26;       53 24;      147 24;      110 24 |
| NONREPT_POSITIONS_SHORT_ALL | other | 4.2K | 0 |        5 29;       40 26;       25 26;        9 26 |
| CHANGE_IN_OPEN_INTEREST_ALL | amount | 4.2K | 0 |        . 69;      206 24;    -1192 23;     -183 23 |
| CHANGE_IN_DEALER_LONG_ALL | amount | 3.6K | 0 |        0 136;        . 69;       -4 24;       -1 24 |
| CHANGE_IN_DEALER_SHORT_ALL | amount | 3.9K | 0 |        . 69;        0 53;       -6 25;       -3 24 |
| CHANGE_IN_DEALER_SPREAD_ALL | amount | 2.8K | 0 |        0 668;        . 69;        1 29;        3 27 |
| CHANGE_IN_ASSET_MGR_LONG_ALL | amount | 3.1K | 0 |        0 354;        . 69;       -3 26;       -2 24 |
| CHANGE_IN_ASSET_MGR_SHORT_ALL | amount | 2.7K | 0 |        0 583;        . 69;        1 23;       50 23 |
| CHANGE_IN_ASSET_MGR_SPREAD_ALL | amount | 2.0K | 0 |        0 989;        . 69;       -2 23;        2 22 |
| CHANGE_IN_LEV_MONEY_LONG_ALL | amount | 3.8K | 0 |        0 79;        . 69;      121 23;      779 23 |
| CHANGE_IN_LEV_MONEY_SHORT_ALL | amount | 3.9K | 0 |        . 69;        0 29;      645 24;       11 24 |
| CHANGE_IN_LEV_MONEY_SPREAD_ALL | amount | 2.7K | 0 |        0 629;        . 69;        1 36;        2 26 |
| CHANGE_IN_OTHER_REPT_LONG_ALL | amount | 2.4K | 0 |        0 899;        . 69;       30 23;      -20 22 |
| CHANGE_IN_OTHER_REPT_SHORT_ALL | amount | 2.5K | 0 |        0 938;        . 69;      -40 23;       25 21 |
| CHANGE_IN_OTHER_REPT_SPREAD_ALL | amount | 1.5K | 0 |        0 2.3K;        . 69;       -1 27;        1 23 |
| CHANGE_IN_TOT_REPT_LONG_ALL | amount | 4.1K | 0 |        . 69;    -1075 23;     -363 23;      828 23 |
| CHANGE_IN_TOT_REPT_SHORT_ALL | amount | 4.1K | 0 |        . 69;      208 24;       26 24;    -1024 23 |
| CHANGE_IN_NONREPT_LONG_ALL | amount | 3.4K | 0 |        . 69;        2 27;        0 26;        3 25 |
| CHANGE_IN_NONREPT_SHORT_ALL | amount | 3.3K | 0 |        . 69;        0 39;       -1 29;       -4 28 |
| PCT_OF_OPEN_INTEREST_ALL | who | 1 | 0 |   100.0 4.6K |
| PCT_OF_OI_DEALER_LONG_ALL | amount | 771 | 0 |     0.0 62;     5.2 34;     0.7 34;     1.3 31 |
| PCT_OF_OI_DEALER_SHORT_ALL | amount | 864 | 0 |     8.7 26;     5.3 26;    11.6 26;    10.3 26 |
| PCT_OF_OI_DEALER_SPREAD_ALL | amount | 394 | 0 |     0.0 728;     0.1 222;     0.2 166;     0.3 165 |
| PCT_OF_OI_ASSET_MGR_LONG_ALL | amount | 722 | 0 |     0.0 175;     0.6 39;     1.9 31;     0.2 30 |
| PCT_OF_OI_ASSET_MGR_SHORT_ALL | amount | 584 | 0 |     0.0 401;     0.5 56;     0.3 53;     0.4 52 |
| PCT_OF_OI_ASSET_MGR_SPREAD_ALL | amount | 164 | 0 |     0.0 659;     0.1 188;     0.2 167;     0.3 155 |
| PCT_OF_OI_LEV_MONEY_LONG_ALL | amount | 694 | 0 |     0.5 38;     0.0 35;    10.0 31;    11.5 31 |
| PCT_OF_OI_LEV_MONEY_SHORT_ALL | amount | 639 | 0 |    16.0 29;    21.7 27;    19.7 27;     7.8 26 |
| PCT_OF_OI_LEV_MONEY_SPREAD_ALL | amount | 202 | 0 |     0.0 742;     0.1 254;     0.2 207;     0.4 182 |
| PCT_OF_OI_OTHER_REPT_LONG_ALL | amount | 256 | 0 |     0.0 445;     0.6 125;     0.7 122;     0.8 117 |
| PCT_OF_OI_OTHER_REPT_SHORT_ALL | amount | 295 | 0 |     0.0 620;     0.9 81;     1.7 77;     0.7 75 |
| PCT_OF_OI_OTHER_REPT_SPREAD_ALL | amount | 116 | 0 |     0.0 2.7K;     0.1 345;     0.2 208;     0.3 152 |
| PCT_OF_OI_TOT_REPT_LONG_ALL | amount | 439 | 0 |    84.5 38;    90.6 35;    91.2 33;    84.9 33 |
| PCT_OF_OI_TOT_REPT_SHORT_ALL | amount | 507 | 0 |    99.6 63;    99.9 59;    99.7 47;    99.5 44 |
| PCT_OF_OI_NONREPT_LONG_ALL | amount | 438 | 0 |    15.5 38;     9.4 35;     8.8 33;    15.1 33 |
| PCT_OF_OI_NONREPT_SHORT_ALL | amount | 496 | 0 |     0.4 63;     0.1 59;     0.3 47;     0.5 44 |
| TRADERS_TOT_ALL | who | 386 | 0 |      21 85;      20 79;      22 76;      23 72 |
| TRADERS_DEALER_LONG_ALL | amount | 45 | 0 |       . 655;       4 331;       5 301;       6 285 |
| TRADERS_DEALER_SHORT_ALL | amount | 71 | 0 |       . 392;      11 265;      10 260;       4 246 |
| TRADERS_DEALER_SPREAD_ALL | amount | 78 | 0 |       . 1.7K;       0 560;       4 355;       5 284 |
| TRADERS_ASSET_MGR_LONG_ALL | amount | 102 | 0 |       . 958;       4 259;       5 220;       6 197 |
| TRADERS_ASSET_MGR_SHORT_ALL | amount | 77 | 0 |       . 1.0K;       4 432;       0 388;       5 294 |
| TRADERS_ASSET_MGR_SPREAD_ALL | amount | 71 | 0 |       . 1.6K;       0 622;      10 181;       4 155 |
| TRADERS_LEV_MONEY_LONG_ALL | amount | 113 | 0 |       . 371;       5 194;       4 186;       6 180 |
| TRADERS_LEV_MONEY_SHORT_ALL | amount | 135 | 0 |       . 364;       7 192;       9 176;      10 174 |
| TRADERS_LEV_MONEY_SPREAD_ALL | amount | 98 | 0 |       . 1.4K;       0 459;       5 215;       4 214 |
| TRADERS_OTHER_REPT_LONG_ALL | amount | 48 | 0 |       . 1.8K;       0 426;       4 342;       5 268 |
| TRADERS_OTHER_REPT_SHORT_ALL | amount | 60 | 0 |       . 1.5K;       0 594;       4 373;       5 270 |
| TRADERS_OTHER_REPT_SPREAD_ALL | amount | 28 | 0 |       0 2.3K;       . 1.5K;       4 178;       5 105 |
| TRADERS_TOT_REPT_LONG_ALL | who | 343 | 0 |      17 96;      15 94;      14 92;      13 89 |
| TRADERS_TOT_REPT_SHORT_ALL | who | 355 | 0 |      21 84;      20 80;      23 79;      44 73 |
| CONC_GROSS_LE_4_TDR_LONG_ALL | amount | 804 | 0 |     50.6 29;     22.3 29;     34.1 28;     22.9 27 |
| CONC_GROSS_LE_4_TDR_SHORT_ALL | amount | 841 | 0 |     25.1 28;     28.1 28;     24.9 26;     69.6 25 |
| CONC_GROSS_LE_8_TDR_LONG_ALL | amount | 765 | 0 |     47.3 29;     46.7 27;     96.4 26;     50.6 26 |
| CONC_GROSS_LE_8_TDR_SHORT_ALL | amount | 828 | 0 |     94.7 26;     36.8 26;     86.4 25;     86.0 25 |
| CONC_NET_LE_4_TDR_LONG_ALL | amount | 800 | 0 |     31.4 28;     33.0 27;     32.8 26;     19.1 25 |
| CONC_NET_LE_4_TDR_SHORT_ALL | amount | 841 | 0 |     18.1 27;     18.4 26;     28.7 26;     19.0 26 |
| CONC_NET_LE_8_TDR_LONG_ALL | amount | 800 | 0 |     39.6 28;     37.9 26;     27.6 26;     28.0 26 |
| CONC_NET_LE_8_TDR_SHORT_ALL | amount | 848 | 0 |     86.0 28;     91.3 26;     27.1 26;     25.4 26 |
| CONTRACT_UNITS | category | 31 | 0 | (CONTRACTS OF $100,000 FA 516; (CONTRACTS OF $100,000)  258; (S&P 500 INDEX X $250.00) 258; (NASDAQ 100 INDEX X $100) 225 |
| CFTC_CONTRACT_MARKET_CODE_QUOTES | category | 40 | 0 | 1170E1  129; 098662  129; 247602  129; 246602  129 |
| CFTC_MARKET_CODE_QUOTES | category | 6 | 0 | CME  2.6K; CBT  1.4K; ICUS  258; NYL  164 |
| CFTC_COMMODITY_CODE_QUOTES | category | 26 | 0 | 138  516; 209  354; 124  296; 246  258 |
| CFTC_SUBGROUP_CODE | category | 6 | 0 | F20  1.8K; F10  774; F30  652; F33  531 |
| FUTONLY_OR_COMBINED | who | 1 | 0 | FutOnly 4.6K |
| INGESTED_AT | audit | 3 | 0 | 1786464191573044 1.9K; 1786464188879469 1.9K; 1786464186031143 836 |
| SOURCE_RUN_ID | audit | 3 | 0 | 9b1e495b-83ec-47db-a989-0 1.9K; f620e9aa-a82c-462e-bd51-5 1.9K; 29796ace-0a7e-4eff-a7e3-b 836 |
| SRC_SHA256 | category | 3 | 0 | c5b65a8c3e0f597fae6b41eab 1.9K; 583a93474847f1070b213e2b1 1.9K; 5392a28735d28dcb8feb5e602 836 |
