# PORTAL_CKA_HOUSTON_OPEN_DAT_C3F216770E

rows 10.0K  columns 16  scan 3.2s

roles: audit 2, category 5, date 3, other 2, who 5

## when

INSPECTION_DATE
  2011     10.0K  ##############################

CORRECT_BY_DATE
  1900         1  
  2011      9.2K  ##############################
  2012        13  
  2016         1  

INGESTED_AT
  2026     10.0K  ##############################

## who

FACILITY_NAME by rows
        87  SUNCO MARKET PLACE
        77  LA ESPERANZA # 1
        76  EL PAISANO MEAT MARKET #2
        63  EL AHORRO SUPERMARKET #15
        54  MCDONALD'S
        50  HUNGRY FARMER BAR-B-Q
        48  EL PENJAMO
        47  BURNS OLD FASHIONED PIT BAR B.Q.
        46  LA MICHOACANA  MEAT MARKET
        46  RELIANT STADIUM
        45  CHINA STAR CHINESE BUFFET
        44  PHILLIPS 66 LOCKWOOD
        41  RELIANT CENTER CONCESSIONS
        41  FRENCHY'S
        40  GUAYABA LATIN GRILL
        39  TODAI
        37  GOLDEN CORRAL
        36  LA MICHOACANA
        36  TOKYO ONE
        36  LA MIA CAFE

SITE_NAME by rows
      2.3K  KITCHEN
      1.7K  Kitchen
       957  0
       240  GROCERY
       224  7411 PARK PLACE
       148  Restaurant
       134  Store
       127  Taqueria
       124  STORE
       121  Grocery
       110  Bar
       108  TAQUERIA
        77  Main Kitchen
        68  BAR
        67  Bakery
        65  Meat
        59  Meat Market
        47  MEAT
        42  BAKERY
        41  kitchen

C_ACCOUNT by rows
        87  207638
        77  409606
        76  408445
        63  414924
        50  981991
        48  215774
        47  417507
        46  416238
        46  212500
        45  412055
        44  415267
        41  212467
        40  410683
        39  205567
        36  416269
        36  409272
        35  410367
        34  412422
        33  415676
        32  410952

ADDRESS by rows
        87  9632 W MONTGOMERY, HOUSTON, TX 77088
        77  9822 N HOUSTON ROSSLYN RD, HOUSTON, TX 77088-2132
        76  426 CROSSTIMBERS, HOUSTON, TX 77022
        63  6910 CAPITOL, HOUSTON, TX 77011
        50  40 E CROSSTIMBERS, HOUSTON, TX 77022
        48  6110 LYONS, HOUSTON, TX 77020
        47  6314 ANTOINE DR, HOUSTON, TX 77091
        46  2 RELIANT PKWY, HOUSTON, TX 77054
        46  5902 N SHEPHERD DR, HOUSTON, TX 77091
        45  4414 NORTH FWY, HOUSTON, TX 77022
        44  5320 EAST FWY, HOUSTON, TX 77020
        41  8334 FANNIN, HOUSTON, TX 77054
        40  17505 HIGHWAY 249, HOUSTON, TX 77064
        39  7620 KATY FWY STE 300, HOUSTON, TX 77024
        36  5801 MEMORIAL DR, HOUSTON, TX 77007-2541
        36  7465 W GREENS  RD, HOUSTON, TX 77064
        35  5350 NORTH FWY, HOUSTON, TX 77022
        34  4711 W 34TH ST, HOUSTON, TX 77092
        33  8201 BROADWAY ST, HOUSTON, TX 77061
        32  5328 ANTOINE DR, HOUSTON, TX 77091-4900

## who x when

FACILITY_NAME by INSPECTION_DATE
  BURNS OLD FASHIONED PIT BAR B.Q.          2011:47
  CHINA STAR CHINESE BUFFET                 2011:45
  EL AHORRO SUPERMARKET #15                 2011:63
  EL PAISANO MEAT MARKET #2                 2011:76
  EL PENJAMO                                2011:48
  FRENCHY'S                                 2011:41
  GOLDEN CORRAL                             2011:37
  GUAYABA LATIN GRILL                       2011:40
  HUNGRY FARMER BAR-B-Q                     2011:50
  LA ESPERANZA # 1                          2011:77
  LA MIA CAFE                               2011:36
  LA MICHOACANA                             2011:36
  LA MICHOACANA  MEAT MARKET                2011:46
  MCDONALD'S                                2011:54
  PHILLIPS 66 LOCKWOOD                      2011:44
  RELIANT CENTER CONCESSIONS                2011:41
  RELIANT STADIUM                           2011:46
  SUNCO MARKET PLACE                        2011:87
  TODAI                                     2011:39
  TOKYO ONE                                 2011:36

SITE_NAME by INSPECTION_DATE
  0                                         2011:957
  7411 PARK PLACE                           2011:224
  BAKERY                                    2011:42
  BAR                                       2011:68
  Bakery                                    2011:67
  Bar                                       2011:110
  GROCERY                                   2011:240
  Grocery                                   2011:121
  KITCHEN                                   2011:2.3K
  Kitchen                                   2011:1.7K
  MEAT                                      2011:47
  Main Kitchen                              2011:77
  Meat                                      2011:65
  Meat Market                               2011:59
  Restaurant                                2011:148
  STORE                                     2011:124
  Store                                     2011:134
  TAQUERIA                                  2011:108
  Taqueria                                  2011:127
  kitchen                                   2011:41

## what

RISK: 3 64%, 2 27%, 1 9%

FACILITY_TYPE: (001) Restaurant - Full Servic 38%, (002) Restaurant - Single Serv 26%, (091) Retail Food Market - Mul 8%, (101) Convenience Grocery - Op 6%, (070) Mobile - Conventional, U 5%, (090) Retail Food Market with  4%, (040) Hospitals 3%, (071) Mobile - Conventional, U 3%, (031) School Cafeteria - Inter 2%, (050) Day Care Center - Open F 2%, (100) Convenience Grocery - Pa 2%, (120) Bakery - Retail  1%

INSPECTOR: Rosalind LaFleur 13%, Zenobia Walker 12%, Remonda Robinson 11%, I-Yuan Chen 10%, Yolanda Wilkins 9%, Mastaneh Sarraf 8%, Marcia Washington 8%, Gene Bowden 7%, Jerry Bradshaw 7%, Paul Chen 5%, Joseph Raia 5%, Ching-Ping Yang 5%

VIOLATION_WEIGHT: 1 65%, 2 13%, 3 13%, 4 7%, 25 2%, 5 0%, 0 0%

SCORE: 1 29%, 3 27%, 2 23%, 5 13%, 4 8%, 0 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| C_ACCOUNT | who | 1.7K | 0 | 408445 97; 215774 89; 207638 87; 409606 87 |
| FACILITY_NAME | who | 1.6K | 0 | EL PAISANO MEAT MARKET #2 97; EL PENJAMO 88; SUNCO MARKET PLACE 87; LA ESPERANZA # 1 86 |
| RISK | category | 3 | 0 | 3 6.4K; 2 2.7K; 1 906 |
| FACILITY_TYPE | category | 48 | 0 | (001) Restaurant - Full S 3.5K; (002) Restaurant - Single 2.4K; (091) Retail Food Market  756; (101) Convenience Grocery 537 |
| INSPECTION_DATE | date | 79 | 0 | 2011-07-21 00:00:00 281; 2011-09-01 00:00:00 280; 2011-08-15 00:00:00 277; 2011-09-13 00:00:00 273 |
| INSPECTOR | category | 31 | 0 | Rosalind LaFleur 977; Zenobia Walker 891; Remonda Robinson 807; I-Yuan Chen 750 |
| SITE_NAME | who | 1.1K | 0 | KITCHEN 2.3K; Kitchen 1.7K; 0 957; GROCERY 240 |
| ADDRESS | who | 1.7K | 0 | 426 CROSSTIMBERS, HOUSTON 97; 6110 LYONS, HOUSTON, TX 7 89; 9632 W MONTGOMERY, HOUSTO 87; 9822 N HOUSTON ROSSLYN RD 87 |
| VIOLATION_CODE | other | 269 | 0 | 47-522 651; 20-21.23(a) 523; 20-21.10(a) 514; 20-21.22(a) 398 |
| VIOLATION_WEIGHT | category | 8 | 2 | 1 6.5K; 2 1.3K; 3 1.3K; 4 739 |
| VIOLATION_COMMENTS | other | 8.5K | 0 | Generator return copy of  147; Generator copy of the was 124; Interceptor has not been  85; Store wiping cloths in a  58 |
| CORRECT_BY_DATE | date | 122 | 784 | 2011-07-21 00:00:00 269; 2011-09-13 00:00:00 228; 2011-09-01 00:00:00 216; 2011-08-31 00:00:00 213 |
| SCORE | category | 6 | 0 | 1 2.9K; 3 2.7K; 2 2.3K; 5 1.3K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:51:47.40266 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | cf0156ab-c330-4d72-9b17-a 10.0K |
| SRC_SHA256 | who | 1 | 0 | e39bfdb7f6491acd92eaeaa1d 10.0K |
