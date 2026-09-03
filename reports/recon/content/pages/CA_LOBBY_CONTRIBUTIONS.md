# CA_LOBBY_CONTRIBUTIONS

rows 6.5K  columns 10  scan 4.5s

roles: amount 1, audit 2, date 2, empty 1, who 4

## when

FILING_PERIOD_START_DT
  2000      5.6K  ##############################
  2001       861  #####

FILING_PERIOD_END_DT
  2000      5.6K  ##############################
  2001       861  #####
  2031         5  

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 6.5K | -750 | 1.0K | 25.0K | 125.0K | 12.90M |

## who

RECIPIENT_NAME by rows
        74  ASSEMBLY DEMOCRATIC LEADERSHIP 2000
        69  FRIENDS OF DENNIS CARDOZA
        65  GOVERNOR GRAY DAVIS COMMITTEE
        60  STRICKLAND FOR ASSEMBLY
        59  FRIENDS OF JIM BRULTE
        56  SHELLEY FOR ASSEMBLY
        55  FRIENDS OF JACK O'CONNELL
        55  WESSON FOR ASSEMBLY
        50  SENATE DEMOCRATIC LEADERSHIP FUND
        50  MACHADO FOR SENATE 2000
        47  FRIENDS OF BILL CAMPBELL
        46  DEDE ALPERT FOR SENATE
        45  PAT BATES FOR ASSEMBLY
        44  POOCHIGIAN SENATE COMMITTEE
        42  ANTHONY PESCETTI FOR ASSEMBLY
        41  CITIZENS FOR BOB MARGETT
        40  TONY CARDENAS 2000
        39  FRIENDS OF DEAN FLOREZ
        38  RAINEY FOR SENATE
        37  ROD WRIGHT FOR ASSEMBLY

RECIPIENT_NAME by dollars
      768.5K       65 rows  GOVERNOR GRAY DAVIS COMMITTEE
      565.8K       35 rows  DAVIS COMMITTEE THE GOVERNOR GRAY
      351.5K       74 rows  ASSEMBLY DEMOCRATIC LEADERSHIP 2000
      246.0K       25 rows  BURTON FOR STATE SENATE 2000
      213.5K       15 rows  THE GOVERNOR GRAY DAVIS COMMITTEE
      175.5K       50 rows  SENATE DEMOCRATIC LEADERSHIP FUND
      160.4K       59 rows  FRIENDS OF JIM BRULTE
      154.0K       55 rows  WESSON FOR ASSEMBLY
      125.6K       69 rows  FRIENDS OF DENNIS CARDOZA
      125.0K        1 rows  TOBACCO SETTLEMENT FUND COMMITTEE
      125.0K        2 rows  TAXPAYERS FOR ACCOUNTABILITY & BETTER SCHOOLS
      116.2K        7 rows  SENATE MAJORITY FUND
      113.4K       18 rows  FRIENDS OF BOB HERTZBERG
      109.5K       16 rows  FRIENDS OF BILL LOCKYER
      106.0K       23 rows  BRULTE FRIENDS OF JIM
      105.5K        7 rows  DEMOCRATIC STATE CENTRAL COMMITTEE OF CALIFORNIA
      100.0K        1 rows  CALIFORNIANS FOR SAFE PARKS/YES ON 12/VILLARAIGOSA
       98.8K        9 rows  CALIFORNIANS FOR GRAY DAVIS
       95.0K        3 rows  BOB HERTZBERG (ASSEMBLY DEMOCRATIC LEADERSHIP 2000)
       93.0K       56 rows  SHELLEY FOR ASSEMBLY

FILER_ID by rows
       261  1147080
       199  1146774
       177  1146864
       168  1146888
       156  1146836
       133  1146844
       110  1143662
       107  1147006
       103  1146815
       102  1142845
        97  1149615
        86  1143015
        84  1147066
        82  1146936
        82  1223813
        80  1146894
        77  1143505
        70  1144055
        68  1147122
        66  1146713

FILER_ID by dollars
      518.5K       70 rows  1144055
      486.3K      110 rows  1143662
      426.4K       97 rows  1149615
      424.7K       46 rows  1147194
      405.6K      168 rows  1146888
      352.7K      156 rows  1146836
      324.6K      261 rows  1147080
      322.4K      133 rows  1146844
      314.0K       46 rows  1143248
      276.1K      177 rows  1146864
      270.2K       17 rows  1146797
      262.4K       17 rows  1143663
      253.7K      199 rows  1146774
      240.2K      103 rows  1146815
      209.8K       49 rows  1143258
      200.0K        2 rows  1223221
      198.8K       22 rows  1143689
      183.5K       82 rows  1146936
      180.5K       41 rows  1145306
      150.9K       68 rows  1147122

RECIPIENT_ID by rows
       132  1069390
       116  1077687
        96  1069427
        95  1065754
        93  1075516
        90  1064947
        86  1069846
        83  1076036
        81  1059023
        80  1069406
        73  1071970
        68  1071976
        67  1069416
        65  1069579
        65  1069524
        62  1064987
        62  1065492
        62  1069359
        60  1069401
        60  1075712

RECIPIENT_ID by dollars
       1.60M      132 rows  1069390
      603.0K      116 rows  1077687
      446.5K       90 rows  1064947
      344.0K       60 rows  1069401
      308.3K       96 rows  1069427
      241.7K       83 rows  1076036
      229.9K       80 rows  1069406
      165.1K       41 rows  1069827
      158.3K       25 rows  1072280
      152.5K       86 rows  1069846
      149.7K       16 rows  1018392
      145.5K       26 rows  1070549
      135.0K        3 rows  1222562
      129.6K       67 rows  1069416
      129.3K       23 rows  1072954
      128.9K       93 rows  1075516
      125.0K        1 rows  1220053
      122.8K       52 rows  1075828
      117.1K       73 rows  1071970
      110.3K       65 rows  1069524

SRC_SHA256 by rows
      6.5K  94fe7d9f7d91b235fd64d6bac73c005339e70206df69079fc53b473b8a797a4b

SRC_SHA256 by dollars
      12.90M     6.5K rows  94fe7d9f7d91b235fd64d6bac73c005339e70206df69079fc53b473b8a79

## who x when

RECIPIENT_NAME by FILING_PERIOD_START_DT, dollars = AMOUNT
  ANTHONY PESCETTI FOR ASSEMBLY             2000:41.6K 2001:2.0K
  ASSEMBLY DEMOCRATIC LEADERSHIP 2000       2000:349.5K 2001:2.0K
  BRULTE FRIENDS OF JIM                     2000:106.0K
  BURTON FOR STATE SENATE 2000              2000:245.0K 2001:1.0K
  CITIZENS FOR BOB MARGETT                  2000:43.0K 2001:2.8K
  DAVIS COMMITTEE THE GOVERNOR GRAY         2000:540.8K 2001:25.0K
  DEDE ALPERT FOR SENATE                    2000:45.1K
  DEMOCRATIC STATE CENTRAL COMMITTEE OF CA  2000:67.5K 2001:38.0K
  FRIENDS OF BILL CAMPBELL                  2000:45.3K 2001:1.0K
  FRIENDS OF BILL LOCKYER                   2000:109.5K
  FRIENDS OF BOB HERTZBERG                  2000:109.4K 2001:4.0K
  FRIENDS OF DEAN FLOREZ                    2000:39.7K
  FRIENDS OF DENNIS CARDOZA                 2000:124.8K 2001:750
  FRIENDS OF JACK O'CONNELL                 2000:54.0K 2001:8.0K
  FRIENDS OF JIM BRULTE                     2000:160.4K
  GOVERNOR GRAY DAVIS COMMITTEE             2000:672.0K 2001:96.5K
  MACHADO FOR SENATE 2000                   2000:61.2K 2001:2.5K
  PAT BATES FOR ASSEMBLY                    2000:35.0K 2001:3.6K
  POOCHIGIAN SENATE COMMITTEE               2000:38.8K 2001:4.8K
  RAINEY FOR SENATE                         2000:41.6K
  ROD WRIGHT FOR ASSEMBLY                   2000:64.7K 2001:1.0K
  SENATE DEMOCRATIC LEADERSHIP FUND         2000:175.5K
  SENATE MAJORITY FUND                      2000:116.2K
  SHELLEY FOR ASSEMBLY                      2000:89.0K 2001:4.0K
  STRICKLAND FOR ASSEMBLY                   2000:62.7K 2001:5.0K
  TAXPAYERS FOR ACCOUNTABILITY & BETTER SC  2000:125.0K
  THE GOVERNOR GRAY DAVIS COMMITTEE         2000:207.5K 2001:6.0K
  TOBACCO SETTLEMENT FUND COMMITTEE         2000:125.0K
  TONY CARDENAS 2000                        2000:51.5K
  WESSON FOR ASSEMBLY                       2000:149.0K 2001:5.0K

FILER_ID by FILING_PERIOD_START_DT, dollars = AMOUNT
  1142845                                   2000:16.1K 2001:39.0K
  1143015                                   2000:23.5K 2001:26.9K
  1143248                                   2000:314.0K
  1143258                                   2000:209.8K
  1143505                                   2000:74.7K
  1143662                                   2000:477.8K 2001:8.5K
  1143663                                   2000:262.4K
  1143689                                   2000:198.8K
  1144055                                   2000:431.0K 2001:87.5K
  1145306                                   2000:180.0K 2001:500
  1146713                                   2000:88.0K 2001:12.0K
  1146774                                   2000:253.7K
  1146797                                   2000:270.2K
  1146815                                   2000:240.2K
  1146836                                   2000:352.7K
  1146844                                   2000:322.4K
  1146864                                   2000:276.1K
  1146888                                   2000:405.6K 2001:0
  1146894                                   2000:82.8K 2001:21.0K
  1146936                                   2000:182.5K 2001:1.0K
  1147006                                   2000:124.8K
  1147066                                   2000:88.4K 2001:30.2K
  1147080                                   2000:324.6K
  1147122                                   2000:150.9K 2001:0
  1147194                                   2000:380.7K 2001:44.0K
  1149615                                   2000:426.4K
  1223221                                   2000:200.0K
  1223813                                   2000:110.2K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FILER_ID | who | 596 | 0 | 1147080 261; 1146774 199; 1146864 177; 1146888 168 |
| FILING_PERIOD_START_DT | date | 11 | 0 | 7/1/2000 12:00:00 AM 2.6K; 1/1/2000 12:00:00 AM 1.7K; 10/1/2000 12:00:00 AM 1.2K; 1/1/2001 12:00:00 AM 812 |
| FILING_PERIOD_END_DT | date | 14 | 0 | 9/30/2000 12:00:00 AM 2.6K; 3/31/2000 12:00:00 AM 1.7K; 12/31/2000 12:00:00 AM 1.2K; 3/31/2001 12:00:00 AM 790 |
| CONTRIBUTION_DT | empty | 1 | 6.5K |  |
| RECIPIENT_NAME | who | 1.8K | 38 | ASSEMBLY DEMOCRATIC LEADE 75; FRIENDS OF DENNIS CARDOZA 69; GOVERNOR GRAY DAVIS COMMI 65; STRICKLAND FOR ASSEMBLY 60 |
| RECIPIENT_ID | who | 562 | 177 | 1069390 132; 1077687 116; 1069427 96; 1065754 95 |
| AMOUNT | amount | 209 | 2 | 1000 2.2K; 500 1.4K; 750 473; 5000 339 |
| INGESTED_AT | audit | 1 | 0 | 1785965845800949 6.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | d8e2006d-709a-42b4-889f-4 6.5K |
| SRC_SHA256 | who | 1 | 0 | 94fe7d9f7d91b235fd64d6bac 6.5K |
