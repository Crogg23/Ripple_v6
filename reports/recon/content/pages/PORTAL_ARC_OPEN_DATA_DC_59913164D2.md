# PORTAL_ARC_OPEN_DATA_DC_59913164D2

rows 2.0K  columns 97  scan 4.5s

roles: amount 2, audit 2, category 49, date 4, empty 5, id 9, other 17, who 10

## when

BSTP_INV_SRV_DATE
  2000         1  
  2006      1.4K  ##############################
  2007         2  
  2008        10  
  2009       330  #######
  2012         9  
  2017         7  
  2018        25  #
  2019        24  #

CREATED
  2024      2.0K  ##############################

EDITED
  2024      2.0K  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ONS_CRP_SLP | 2.0K | -9 | 4.40 | 8.90 | 11.20 | 3.6K |
| MEASURE | 2.0K | 3 | 1.4K | 9.0K | 10.2K | 4.28M |

## who

CITY_NAME by rows
      2.0K  Washington

CITY_NAME by dollars
        3.6K     2.0K rows  Washington

AT_STR by rows
        15  7TH ST NW
        14  13TH ST NW
        13  H ST NW
        13  16TH ST NW
        12  4TH ST NW
        12  SAVANNAH ST SE
        11  K ST NW
        11  N ST NW
        11  P ST NW
        11  1ST ST NW
        11  14TH ST NW
        10  SOUTH DAKOTA AVE NE
        10  11TH ST NW
        10  E ST SE
        10  18TH ST NE
        10  14TH ST NE
        10  8TH ST NE
         9  4TH ST SE
         9  MONROE ST NE
         9  6TH ST NE

AT_STR by dollars
       56.10       11 rows  N ST NW
       55.70       10 rows  14TH ST NE
       54.90       11 rows  1ST ST NW
       52.30       10 rows  E ST SE
          51       12 rows  SAVANNAH ST SE
       43.30       15 rows  7TH ST NW
       41.90        8 rows  12TH ST NE
       41.40        8 rows  M ST NW
          41       10 rows  11TH ST NW
       40.70        9 rows  MONROE ST NE
       38.20       12 rows  4TH ST NW
       37.90        7 rows  3RD ST NE
       37.30        8 rows  6TH ST NW
       36.60        9 rows  4TH ST SE
       35.80        9 rows  6TH ST NE
       35.30        7 rows  SHEPHERD ST NW
       35.20       10 rows  SOUTH DAKOTA AVE NE
       33.10        6 rows  NEW JERSEY AVE NW
       31.60        6 rows  INGRAHAM ST NW
       30.50        6 rows  NEW HAMPSHIRE AVE NW

BSTP_LDC by rows
      1.3K  UNKNOWN
        47  nan
        26  LIMITED STOP EXPRESS
        12  OPPO
         8  @ CATCH BASIN
         6  FRT
         5  LIMITED EXPRESS STOP
         5  @ CORNER
         4  BASE PLATED
         4  MT VERNON SQ STATION
         3  75' W OF -
         3  @ XWALK
         3  100' W OF ---
         3  @ HYDRANT
         3  OPPO ENTR TO -
         2  GALLERY PLACE STATION
         2  130' ZONE
         2  IN TREE WELL
         2  90' E OF -
         2  40' N OF -

BSTP_LDC by dollars
        3.5K     1.3K rows  UNKNOWN
      110.50       26 rows  LIMITED STOP EXPRESS
       20.10        4 rows  MT VERNON SQ STATION
       19.70        5 rows  @ CORNER
       17.10        3 rows  @ XWALK
       15.10        8 rows  @ CATCH BASIN
       14.30        2 rows  GALLERY PLACE STATION
       13.10        2 rows  16TH ST
       12.70        2 rows  BUS BAY
       12.30        2 rows  JUDICIARY SQUARE STATION
       12.20        2 rows  130' ZONE
       12.10        2 rows  S OF 1ST DRWY
       11.40        2 rows  IN TREE WELL
       11.20        1 rows  ON LAMPPOST E OF -
       11.10        1 rows  210' E OF ---
       10.50        1 rows  FRT OF #311
       10.40        2 rows  85' ZONE
       10.20        2 rows  100' W OF -
        9.70        1 rows  (OREGON AVE X) BUS BAY & BENCH
        9.70        1 rows  FRT OF 5TH DISTRICT POLICE STA

ON_STR by rows
        84  16TH ST NW
        71  14TH ST NW
        51  CONNECTICUT AVE NW
        40  GEORGIA AVE NW
        36  MASSACHUSETTS AVE NW
        34  MACARTHUR BLVD NW
        33  ALABAMA AVE SE
        32  11TH ST NW
        32  MARTIN LUTHER KING JR AVE SE
        31  RHODE ISLAND AVE NE
        29  SOUTHERN AVE SE
        26  EASTERN AVE NE
        25  BLADENSBURG RD NE
        25  MINNESOTA AVE SE
        23  P ST NW
        21  7TH ST NW
        20  NEBRASKA AVE NW
        20  5TH ST NW
        18  N CAPITOL ST NW
        18  SOUTHERN AVE

ON_STR by dollars
      358.60       84 rows  16TH ST NW
      245.30       71 rows  14TH ST NW
      167.90       51 rows  CONNECTICUT AVE NW
      132.40       40 rows  GEORGIA AVE NW
       97.70       21 rows  7TH ST NW
       89.20       25 rows  MINNESOTA AVE SE
       85.90       36 rows  MASSACHUSETTS AVE NW
       82.60       18 rows  N CAPITOL ST NW
       82.20       32 rows  11TH ST NW
       80.50       33 rows  ALABAMA AVE SE
       78.80       14 rows  12TH ST NE
       78.70       34 rows  MACARTHUR BLVD NW
       78.70       23 rows  P ST NW
       78.50       25 rows  BLADENSBURG RD NE
          76       13 rows  BENNING RD NE
          72       17 rows  NEW HAMPSHIRE AVE NW
       67.20       12 rows  E ST NW
       66.30       11 rows  U ST NW
       64.40       14 rows  8TH ST NE
       61.70       13 rows  RHODE ISLAND AVE NW

## who x when

CITY_NAME by BSTP_INV_SRV_DATE, dollars = ONS_CRP_SLP
  Washington                                2000:-9 2006:3.6K 2007:19.20 2008:3.20 2009:1.1K 2012:29.10 2017:17.20 2018:79.80 2019:82.30

AT_STR by BSTP_INV_SRV_DATE, dollars = ONS_CRP_SLP
  11TH ST NW                                2006:17.30 2009:20.80 2017:1.70 2018:1.20
  12TH ST NE                                2006:37.20 2009:4.70
  13TH ST NW                                2006:24.90 2009:9.60
  14TH ST NE                                2006:48.70 2009:7
  14TH ST NW                                2006:7.70 2009:25.10
  16TH ST NW                                2006:25.40 2009:6.50
  18TH ST NE                                2006:16
  1ST ST NW                                 2006:37.50 2009:12.20 2017:5.20
  3RD ST NE                                 2006:27.20 2009:6.10
  4TH ST NW                                 2000:-9 2006:47.40 2017:3.40 2018:5.40
  4TH ST SE                                 2006:39.20 2009:-2.60
  6TH ST NE                                 2006:28 2018:7.80
  6TH ST NW                                 2006:21.20 2017:2.80 2019:13.30
  7TH ST NW                                 2006:42.60 2007:8.90 2009:18.80
  8TH ST NE                                 2006:14 2009:5.30
  E ST SE                                   2006:37.70 2009:14.60
  H ST NW                                   2006:35.10 2009:15.80
  INGRAHAM ST NW                            2006:27 2009:4.60
  K ST NW                                   2006:30 2009:13.70
  M ST NW                                   2006:31 2009:10.40
  MONROE ST NE                              2006:30.20 2009:6.60 2019:3.90
  N ST NW                                   2006:40.10 2009:16
  NEW HAMPSHIRE AVE NW                      2006:13.70 2009:16.80
  NEW JERSEY AVE NW                         2006:16.10 2009:17
  P ST NW                                   2006:3.80 2009:14.80
  SAVANNAH ST SE                            2006:51
  SHEPHERD ST NW                            2006:35.30
  SOUTH DAKOTA AVE NE                       2006:19.60 2009:9.90 2019:5.70

## what

BSTP_TCD: REV 81%, UNK 19%, SCH 1%

BSTP_POS_TCD: NEA 56%, FAR 27%, NEX 6%, MID 6%, FAX 3%, ATP 1%, MIX 0%, UNK 0%, ACR 0%

BSTP_LAT_LON_TCD: nan 96%, PER 4%, TMP 1%

BSTP_INV_SYR_TCD: KFH 92%, UNK 6%, WSV 3%

BSTP_BNH_CNT: 0 63%, -9 21%, 1 15%, 2 1%, 3 0%, 4 0%

BSTP_BST_TCD: UNK 81%, INS 15%, EXM 2%, FRE 1%

BSTP_IFC_OWN: WMAT 67%, UNKW 31%, NAPP 1%, CIRC 1%

BSTP_HAS_BKRS: N 91%, U 8%, Y 1%

BSTP_HAS_PRS: Y 77%, N 14%, U 9%

BSTP_HAS_PVM: N 85%, U 9%, Y 5%, E 1%

BSTP_HAS_PRM: N 46%, Y 45%, U 9%

BSTP_PDP_SIZE_TCD: 58U 59%, SWK 17%, UNK 11%, 58O 8%, <58 6%, NON 0%

BSTP_PDP_MTR_TCD: CON 77%, UNK 11%, BRK 11%, EXM 1%, ASP 0%

BSTP_PDP_OBS_TCD: NON 80%, UNK 11%, SHL 5%, TRC 2%, EXM 1%, NWB 0%, BSP 0%, FEN 0%, DIR 0%, MLB 0%

BSTP_PDP_HAS_CCN: Y 78%, U 11%, N 10%, E 1%

BSTP_HAS_BDR_PDP: N 80%, Y 11%, U 9%

BSTP_BDR_PDP_OBS: E 80%, U 19%, N 1%, Y 0%

BSTP_SWK_WDT: 6 39%, 5 12%, 4 11%, 0 10%, 11 7%, 3 6%, 8 5%, 9 3%, 7 3%, -9 3%, 2 1%, 10 1%

BSTP_SWK_HAS_CCN: N 54%, Y 33%, U 12%, E 0%

BSTP_SWK_HAS_PPC: Y 77%, N 10%, U 9%, E 4%

BSTP_SWK_SLP_WVL: N 78%, U 12%, Y 9%, E 0%

BSTP_SWK_OBS_TCD: NON 80%, UNK 14%, SHL 2%, LSC 2%, TRC 1%, UTP 1%, BSP 0%, NWB 0%, EXM 0%, FEN 0%, BNH 0%, STO 0%

BSTP_SWK_IPD_TCD: UNK 85%, UPV 6%, SLP 5%, NON 3%, CRK 1%, GRS 0%, EXM 0%, LSC 0%, ROC 0%

ONS_CRP: Y 62%, N 30%, U 9%, E 0%

OFS_CRP: Y 60%, N 31%, U 9%, E 0%

AT_STR_ABS_CRP: Y 69%, U 23%, N 7%, E 0%

AT_STR_OSS_CRP: Y 64%, N 27%, U 9%, E 0%

ONS_CWK: Y 64%, N 24%, U 12%, E 0%

OFS_CWK: Y 62%, N 26%, U 13%, E 0%

AT_STR_ABS_CWK: Y 66%, U 24%, N 9%, E 0%

AT_STR_OSS_CWK: Y 61%, U 29%, N 10%, E 1%

ON_STR_STS_OR_TFL: Y 60%, N 31%, U 9%, E 0%

ON_STR_PDC_SGL: N 52%, Y 39%, U 9%, E 0%

AT_STR_PDC_SGL: N 54%, Y 37%, U 9%, E 0%

BSTP_PRK_RST_TCD: NSG 59%, YUN 14%, NPL 12%, UNK 9%, YMR 5%

BSTP_NPK_ZNE_LTH: -9 97%, 150 1%, 100 1%, 80 1%, 65 0%, 0 0%, 130 0%, 50 0%, 115 0%, 72 0%, 60 0%, 56 0%

CNF_NPK_SNS: N 63%, U 33%, Y 4%

STR_LGT_WTN_30_FT: Y 57%, N 34%, U 9%

BSTP_HAS_LED_DSP: U 91%, Y 6%, N 3%, E 0%

BSTP_ACC_RATING: N 46%, Y 39%, U 15%

BSTP_BRDG_STP: U 99%, Y 1%

BSTP_HAS_LUM_SIGN: U 94%, Y 3%, N 3%, E 0%

BSTP_HAS_PWR_SRC: U 97%, N 2%, Y 0%, E 0%

METRO_ACCS_STP: U 100%, Y 0%

WARD_ID: 5 17%, 8 16%, 4 15%, 7 13%, 2 12%, 3 10%, 6 9%, 1 7%

ANC_ID: ANC 2C 12%, ANC 8C 11%, ANC 5B 10%, ANC 8E 9%, ANC 5C 8%, ANC 4B 8%, ANC 4A 8%, ANC 7C 7%, ANC 7B 7%, ANC 3/4G 7%, ANC 5A 7%, ANC 8A 6%

OFFSET: 3.0 50%, -3.0 49%, nan 1%

SNOWPRIORITY: nan 83%, YES 17%

MSTN_ID: nan 98%, MSTN_001 1%, MSTN_017 0%, MSTN_025 0%, MSTN_033 0%, MSTN_004 0%, MSTN_008 0%, MSTN_009 0%, MSTN_023 0%, MSTN_030 0%, MSTN_018 0%, MSTN_034 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| JOIN_COUNT | other | 1 | 0 | 1 2.0K |
| TARGET_FID | id | 2.0K | 0 | 61425 10; 61422 10; 61418 10; 61416 10 |
| EGIS_ID | id | 2.0K | 0 | 1304090 10; 1305542 10; 1308445 10; 1308754 10 |
| REG_ID | id | 2.0K | 0 | 1000661 10; 1002188 10; 1002819 10; 1002693 10 |
| BSTP_GEO_ID | id | 2.0K | 0 | 99999 19; 4701 10; 7818 10; 9456 10 |
| BSTP_OPS_TCD | other | 1 | 0 | PRS 2.0K |
| BSTP_EFF_DATE | who | 671 | 0 | -2177434800000 337; -248554800000 77; -254948400000 49; 256712400000 38 |
| BSTP_TCD | category | 3 | 0 | REV 1.6K; UNK 371; SCH 12 |
| AT_STR | who | 878 | 0 | 7TH ST NW 15; 13TH ST NW 14; 16TH ST NW 13; H ST NW 13 |
| ON_STR | who | 351 | 0 | 16TH ST NW 84; 14TH ST NW 71; CONNECTICUT AVE NW 51; GEORGIA AVE NW 40 |
| BSTP_HDG | other | 343 | 0 | 180 90; 360 77; 270 67; 90 58 |
| BSTP_POS_TCD | category | 9 | 0 | NEA 1.1K; FAR 546; NEX 128; MID 117 |
| BSTP_LDC | who | 572 | 0 | UNKNOWN 1.3K; nan 47; LIMITED STOP EXPRESS 26; OPPO 12 |
| BSTP_MSG_TEXT | other | 1.6K | 0 | KENNEDY ST NW + 13TH ST N 11; AINGER PL SE + BRUCE PL S 11; EASTERN AVE NE + MICHIGAN 11; WESTERN AVE + UPLAND TER  11 |
| BSTP_LON | id | 1.9K | 0 | -77.065913 11; -76.941029 10; -76.962953 10; -77.019832 10 |
| BSTP_LAT | id | 2.0K | 0 | 38.964962 11; 38.884589 10; 38.934907 10; 38.973468 10 |
| BSTP_LAT_LON_TCD | category | 3 | 0 | nan 1.9K; PER 76; TMP 11 |
| BSTP_INV_SYR_TCD | category | 3 | 0 | KFH 1.8K; UNK 110; WSV 56 |
| BSTP_INV_SRV_DATE | date | 213 | 0 | -2208970800000 98; -2177434800000 52; 1148616000000 41; 1150430400000 34 |
| BSTP_BNH_CNT | category | 6 | 0 | 0 1.3K; -9 419; 1 296; 2 29 |
| BSTP_BST_TCD | category | 4 | 0 | UNK 1.6K; INS 298; EXM 48; FRE 27 |
| BSTP_IFC_OWN | category | 4 | 0 | WMAT 1.3K; UNKW 617; NAPP 29; CIRC 15 |
| BSTP_HAS_BKRS | category | 3 | 0 | N 1.8K; U 157; Y 15 |
| BSTP_HAS_PRS | category | 3 | 0 | Y 1.5K; N 285; U 176 |
| BSTP_HAS_PVM | category | 4 | 0 | N 1.7K; U 176; Y 104; E 13 |
| BSTP_HAS_PRM | category | 3 | 0 | N 927; Y 897; U 176 |
| BSTP_PDP_SIZE_TCD | category | 6 | 0 | 58U 1.2K; SWK 343; UNK 214; 58O 153 |
| BSTP_PDP_MTR_TCD | category | 5 | 0 | CON 1.5K; UNK 216; BRK 215; EXM 19 |
| BSTP_PDP_OBS_TCD | category | 10 | 0 | NON 1.6K; UNK 221; SHL 95; TRC 45 |
| BSTP_PDP_HAS_CCN | category | 4 | 0 | Y 1.6K; U 214; N 199; E 17 |
| BSTP_HAS_BDR_PDP | category | 3 | 0 | N 1.6K; Y 214; U 176 |
| BSTP_BDR_PDP_OBS | category | 4 | 0 | E 1.6K; U 381; N 25; Y 1 |
| BSTP_SWK_WDT | category | 16 | 0 | 6 772; 5 233; 4 225; 0 193 |
| BSTP_SWK_HAS_CCN | category | 4 | 0 | N 1.1K; Y 669; U 242; E 3 |
| BSTP_SWK_HAS_PPC | category | 4 | 0 | Y 1.5K; N 203; U 176; E 89 |
| BSTP_SWK_SLP_WVL | category | 4 | 0 | N 1.6K; U 244; Y 184; E 3 |
| BSTP_SWK_OBS_TCD | category | 12 | 0 | NON 1.6K; UNK 271; SHL 47; LSC 36 |
| BSTP_SWK_IPD_TCD | category | 9 | 0 | UNK 1.7K; UPV 125; SLP 95; NON 55 |
| ONS_CRP_SLP | amount | 95 | 0 | -9.0 451; 5.0 56; 4.80000019 54; 4.69999981 53 |
| ONS_CRP | category | 4 | 0 | Y 1.2K; N 590; U 175; E 3 |
| OFS_CRP | category | 4 | 0 | Y 1.2K; N 624; U 178; E 6 |
| AT_STR_ABS_CRP | category | 4 | 0 | Y 1.4K; U 466; N 142; E 5 |
| AT_STR_OSS_CRP | category | 4 | 0 | Y 1.3K; N 541; U 177; E 6 |
| ONS_CWK | category | 4 | 0 | Y 1.3K; N 487; U 233; E 2 |
| OFS_CWK | category | 4 | 0 | Y 1.2K; N 510; U 253; E 6 |
| AT_STR_ABS_CWK | category | 4 | 0 | Y 1.3K; U 487; N 178; E 9 |
| AT_STR_OSS_CWK | category | 4 | 0 | Y 1.2K; U 571; N 206; E 12 |
| ON_STR_STS_OR_TFL | category | 4 | 0 | Y 1.2K; N 617; U 177; E 1 |
| ON_STR_PDC_SGL | category | 4 | 0 | N 1.0K; Y 784; U 176; E 1 |
| AT_STR_PDC_SGL | category | 4 | 0 | N 1.1K; Y 746; U 179; E 2 |
| BSTP_PRK_RST_TCD | category | 5 | 0 | NSG 1.2K; YUN 287; NPL 245; UNK 176 |
| BSTP_NPK_ZNE_LTH | category | 18 | 0 | -9 1.9K; 150 18; 100 17; 80 11 |
| CNF_NPK_SNS | category | 3 | 0 | N 1.3K; U 667; Y 74 |
| STR_LGT_WTN_30_FT | category | 3 | 0 | Y 1.1K; N 687; U 176 |
| BSTP_HAS_LED_DSP | category | 4 | 0 | U 1.8K; Y 115; N 60; E 1 |
| BSTP_ACC_RATING | category | 3 | 0 | N 912; Y 782; U 306 |
| BSTP_BRDG_STP | category | 2 | 0 | U 2.0K; Y 23 |
| BSTP_HAS_LUM_SIGN | category | 4 | 0 | U 1.9K; Y 67; N 52; E 1 |
| BSTP_HAS_PWR_SRC | category | 4 | 0 | U 1.9K; N 48; Y 7; E 1 |
| METRO_ACCS_STP | category | 2 | 0 | U 2.0K; Y 5 |
| WARD_ID | category | 8 | 0 | 5 342; 8 327; 4 302; 7 262 |
| ANC_ID | category | 44 | 0 | ANC 2C 103; ANC 8C 96; ANC 5B 93; ANC 8E 78 |
| SMD_ID | other | 328 | 0 | SMD 2C03 44; SMD 2C01 39; SMD 8A06 24; SMD 3/4G01 23 |
| ROUTEID | who | 391 | 0 | 11001602 84; 11001402 70; 13081512 47; 11025152 45 |
| MEASURE | amount | 1.9K | 0 | nan 20; 1587.19995117 10; 3925.39990234 10; 6797.5 10 |
| OFFSET | category | 3 | 0 | 3.0 996; -3.0 984; nan 20 |
| BLOCKKEY | other | 1.5K | 0 | nan 110; 744dfa53dd64da50039d8a216 11; 40a03b6be23f898664f478dcd 11; f8ed6f841b6d50fb0c4c37ab9 11 |
| BLOCKFACEKEY | other | 1.9K | 0 | nan 20; 224c488dccc566748927700d3 11; 3421ae8c4ee7b9e5c4936ea00 11; 51ebfc1993cc04b2ab255b400 11 |
| GIS_ID | id | 2.0K | 0 | BusStopPt_39741 10; BusStopPt_39737 10; BusStopPt_39732 10; BusStopPt_39729 10 |
| SE_ANNO_CAD_DATA | empty | 1 | 2.0K |  |
| CREATOR | other | 1 | 0 | JLAY 2.0K |
| CREATED | date | 1 | 0 | 1705632948000 2.0K |
| EDITOR | other | 1 | 0 | JLAY 2.0K |
| EDITED | date | 1 | 0 | 1705632948000 2.0K |
| SNOWPRIORITY | category | 2 | 0 | nan 1.7K; YES 347 |
| BSTP_OPS_FTU_TCD | other | 1 | 0 | NON 2.0K |
| MSTN_ID | category | 13 | 0 | nan 1.9K; MSTN_001 10; MSTN_017 7; MSTN_025 6 |
| OBJECTID_1 | other | 1 | 0 | 1 2.0K |
| CITY_NAME | who | 1 | 0 | Washington 2.0K |
| STATE_CITY | who | 1 | 0 | 1150000 2.0K |
| CAPITAL | other | 1 | 0 | Y 2.0K |
| WEB_URL | other | 1 | 0 | http://www.dc.gov 2.0K |
| AREAKM | who | 1 | 0 | 177.47 2.0K |
| AREAMILES | other | 1 | 0 | 68.52 2.0K |
| GIS_ID_1 | other | 1 | 0 | DCBndyPly_1 2.0K |
| GLOBALID_1 | who | 1 | 0 | {ED39E1E0-B1E5-4B42-BE73- 2.0K |
| CREATOR_1 | empty | 1 | 2.0K |  |
| CREATED_1 | empty | 1 | 2.0K |  |
| EDITOR_1 | empty | 1 | 2.0K |  |
| EDITED_1 | empty | 1 | 2.0K |  |
| SHAPEAREA | other | 1 | 0 | 0 2.0K |
| SHAPELEN | other | 1 | 0 | 0 2.0K |
| GEOMETRY | id | 2.0K | 0 | {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:34:24.88740 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | d9acde22-0276-48ca-82f4-8 2.0K |
| SRC_SHA256 | who | 1 | 0 | 37706e9eba788d03557ede09d 2.0K |
