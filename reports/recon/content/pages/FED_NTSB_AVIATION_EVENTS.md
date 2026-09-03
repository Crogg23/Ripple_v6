# FED_NTSB_AVIATION_EVENTS

rows 31.0K  columns 76  scan 5.1s

roles: amount 21, audit 2, category 22, date 2, id 2, other 22, who 5

## when

EV_DATE
  2008      1.9K  ##############################
  2009      1.8K  ############################
  2010      1.8K  ############################
  2011      1.8K  #############################
  2012      1.8K  #############################
  2013      1.6K  #########################
  2014      1.5K  ########################
  2015      1.6K  #########################
  2016      1.7K  ##########################
  2017      1.6K  ##########################
  2018      1.7K  ###########################
  2019      1.6K  ##########################
  2020      1.4K  ######################
  2021      1.6K  ##########################
  2022      1.7K  ###########################
  2023      1.7K  ##########################
  2024      1.7K  ##########################
  2025      1.6K  ##########################
  2026       864  ##############

LCHG_DATE
  2020     18.9K  ##############################
  2021      1.7K  ###
  2022      2.2K  ####
  2023      1.9K  ###
  2024      1.9K  ###
  2025      2.6K  ####
  2026      1.8K  ###

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| APT_DIST | 30.8K | 0 | 0 | 20.21 | 7.7K | 444.2K |
| APT_DIR | 10.0K | 0 | 150 | 360 | 360 | 1.56M |
| APT_ELEV | 17.0K | -210 | 680 | 7.0K | 32.0K | 22.69M |
| WX_OBS_DIR | 31.0K | -2 | 62 | 360 | 360 | 3.41M |
| WX_OBS_ELEV | 21.5K | -115 | 654 | 7.1K | 751.6K | 29.91M |
| WX_OBS_DIST | 31.0K | -19 | 1 | 57.30 | 6.8K | 260.2K |

## who

APT_NAME by rows
     11.9K  None
       207  Private
       103  Private Airstrip
        49  PVT
        30  N/A
        26  Private Strip
        24  NONE
        20  NORTH PERRY
        20  Merrill Field
        18  Centennial Airport
        18  North Las Vegas
        18  NORTH LAS VEGAS
        18  Wittman Regional Airport
        17  FALCON FLD
        17  CENTENNIAL
        17  Phoenix Deer Valley Airport
        17  PHOENIX DEER VALLEY
        17  RENO/STEAD
        16  Falcon Field Airport
        15  LAKE HOOD

APT_NAME by dollars
       1.08M    11.9K rows  None
       29.9K      207 rows  Private
       16.1K      103 rows  Private Airstrip
        7.1K       49 rows  PVT
        4.8K       30 rows  N/A
        4.2K       26 rows  Private Strip
        3.5K       13 rows  AUBURN MUNI
        3.5K       20 rows  NORTH PERRY
        3.3K       24 rows  NONE
        3.2K       17 rows  RENO/STEAD
        3.2K       10 rows  PALM BEACH COUNTY PARK
        2.7K       15 rows  VAN NUYS
        2.6K       11 rows  CABLE
        2.6K       10 rows  BOZEMAN YELLOWSTONE INTL
        2.5K       13 rows  PORTLAND-HILLSBORO
        2.5K       17 rows  FALCON FLD
        2.5K       11 rows  MERRILL FIELD
        2.4K       15 rows  LAKE HOOD
        2.3K        9 rows  VANCE BRAND
        2.3K       18 rows  NORTH LAS VEGAS

METAR by rows
     24.8K  None
         2  KPDT 161753Z 32004KT 10SM BKN050 BKN065 OVC080 04/03 A2996 RMK AO2 RAE
         2  METAR KGYR 011647Z VRB04KT 10SM SKC 29/14 A2999=
         2  PATK 161953Z 31003KT 10SM CLR 21/11 A3003 RMK AO2 SLP169 T02110111
         2  K1P1 271715Z AUTO 26003KT 10SM CLR 27/12 A3013 RMK AO2 T02680120
         1  KLFK 021453Z AUTO 10006KT 6SM -RA BR BKN065 OVC080 09/07 A3015 RMK AO2
         1  KGTU 011756Z 20012KT 10SM OVC028 30/23 A2994 RMK AO2 SLP131 T03000228 
         1  METAR K4F2 202135Z AUTO 06003KT 10SM OVC017 20/18 A2987 RMK AO2 LTG DS
         1  SPECI KCNO 051828Z 00000KT 10SM HZ CLR 34/06 A2993 RMK AO2 T03390056=
         1  SPECI KMFR 092222Z 32007KT 10SM -RA FEW060 FEW080 OVC100 18/13 A2992 R
         1  METAR KCDI 271855Z AUTO 09003KT 10SM BKN050 28/17 A3004 RMK AO2 T02800
         1  KSJT 281051Z AUTO 20009G16KT 8SM OVC020 24/19 A2973 RMK AO2 SLP040 T02
         1  METAR KFSD 070856Z AUTO 15013G27KT 10SM CLR 26/22 A2976 RMK AO2 PK WND
         1  KMKL 221953Z 07006KT 10SM CLR 20/13 A3018 RMK AO2 SLP217 T02000128
         1  METAR KFHR 121453Z AUTO 00000KT 2 1/2SM BR OVC004 13/12 A2992
         1  METAR K4S2 061655Z AUTO 00000KT 10SM CLR 23/15 A3004 RMK AO2=
         1  KPGD 222253Z 01006KT 10SM FEW043 24/19 A3001 RMK AO2 SLP162 T02440194
         1  K1F0 071415Z AUTO 14003KT 10SM CLR 13/11 A3013 RMK AO2 T01300111
         1  METAR KSAT 020051Z 32004KT 10SM CLR 12/M01 A3019 RMK AO2 SLP214 T01221
         1  METAR KHUT 111752Z 19017KT 10SM CLR 32/20 A3001 RMK AO2 SLP135 T031702

METAR by dollars
       2.36M    24.8K rows  None
         515        2 rows  K1P1 271715Z AUTO 26003KT 10SM CLR 27/12 A3013 RMK AO2 T0268
         492        2 rows  METAR KGYR 011647Z VRB04KT 10SM SKC 29/14 A2999=
         360        1 rows  KJWN 050150Z 15008KT 10SM CLR 19/15 A2998
         360        1 rows  METAR KF70 280035Z AUTO 22007KT 10SM CLR 18/00 A3000 RMK AO2
         360        1 rows  METAR KLYH 101854Z 28009G22KT 250V320 10SM CLR 07/M07 A2982
         360        1 rows  KLAF 261754Z 01009KT 10SM OVC018 27/21 A2997 RMK AO2 SLP143 
         360        1 rows  PAKN 072354Z 09020G32KT 10SM BKN065 12/01 A2998 RMK AO2 PK W
         360        1 rows  KRNV 261815Z AUTO 00000KT 10SM CLR A3004 RMK AO2 TSNO
         360        1 rows  KI74 201855Z AUTO 00000KT 10SM SCT040 SCT060 28/20 A3001 RMK
         360        1 rows  KCMD 241355Z AUTO 06011KT 10SM FEW120 10/01 A3021 RMK AO2

         360        1 rows  KDWH 291853Z 02011G21KT 10SM CLR 26/03 A3014 RMK AO2 SLP204 
         360        1 rows  METAR KTAZ 112100Z AUTO 30014G19KT 10SM CLR M01/M08 A3010
         360        1 rows  SA	30/11/2021 21:53->	
METAR KRAL 302153Z VRB06G21KT 10SM CL
         360        1 rows  METAR KTYS 121853Z 24019G28KT 10SM FEW055 SCT100 BKN250 14/0
         360        1 rows  KEDN 012115Z AUTO 25004KT 10SM SCT046 SCT055 32/23 A2980 RMK
         360        1 rows  METAR K2G4 282000Z AUTO 15009KT 10SM CLR 08/01 A3039 RMK AO1
         360        1 rows  METAR KLOU 011453Z 17008KT 10SM CLR 03/00 A3012 RMK AO2 SLP2
         360        1 rows  KDGW 162153Z AUTO VRB04KT 10SM CLR 28/01 A2987 RMK AO2 SLP06
         360        1 rows  KDAB 211753Z 25005KT 10SM SCT044TCU SCT055 BKN180 BKN250 34/

ALTIMETER by rows
      7.7K  0.0
       976  30.040000915527344
       874  29.950000762939453
       731  30.1200008392334
       693  30.0
       615  30.020000457763672
       582  30.010000228881836
       576  30.049999237060547
       556  29.959999084472656
       556  29.969999313354492
       556  29.979999542236328
       549  30.09000015258789
       548  30.030000686645508
       542  30.059999465942383
       520  29.8700008392334
       501  30.200000762939453
       501  30.100000381469727
       498  29.940000534057617
       494  30.06999969482422
       487  29.920000076293945

ALTIMETER by dollars
      141.1K      976 rows  30.040000915527344
      122.0K      874 rows  29.950000762939453
      100.3K      731 rows  30.1200008392334
       96.0K      693 rows  30.0
       96.0K      615 rows  30.020000457763672
       86.4K     7.7K rows  0.0
       84.8K      548 rows  30.030000686645508
       84.5K      556 rows  29.969999313354492
       80.8K      582 rows  30.010000228881836
       79.9K      576 rows  30.049999237060547
       79.7K      556 rows  29.979999542236328
       78.3K      556 rows  29.959999084472656
       78.1K      542 rows  30.059999465942383
       76.0K      549 rows  30.09000015258789
       73.7K      494 rows  30.06999969482422
       73.3K      501 rows  30.100000381469727
       72.8K      520 rows  29.8700008392334
       71.8K      501 rows  30.200000762939453
       70.4K      498 rows  29.940000534057617
       68.3K      465 rows  29.93000030517578

EV_CITY by rows
       125  Anchorage
        91  Phoenix
        91  Atlanta
        88  Houston
        88  Palmer
        82  Fairbanks
        79  Miami
        77  Talkeetna
        74  Las Vegas
        67  Denver
        66  Mesa
        65  San Diego
        65  Reno
        63  Albuquerque
        60  Oshkosh
        58  London
        56  San Antonio
        56  Chicago
        56  Lancaster
        53  Wasilla

EV_CITY by dollars
       16.5K       88 rows  Palmer
       15.3K      125 rows  Anchorage
       12.0K       88 rows  Houston
        9.2K       79 rows  Miami
        9.2K       77 rows  Talkeetna
        8.8K       91 rows  Phoenix
        8.7K       65 rows  Reno
        8.1K       48 rows  Springfield
        7.7K       38 rows  Hillsboro
        7.7K       56 rows  San Antonio
        7.3K       63 rows  Albuquerque
        7.3K       30 rows  Spanish Fork
        7.2K       66 rows  Mesa
        7.0K       82 rows  Fairbanks
        7.0K       36 rows  Auburn
        6.9K       91 rows  Atlanta
        6.9K       56 rows  Lancaster
        6.7K       65 rows  San Diego
        6.5K       36 rows  Knoxville
        6.5K       40 rows  Midland

## who x when

APT_NAME by EV_DATE, dollars = WX_OBS_DIR
  AUBURN MUNI                               2014:50 2016:333 2017:848 2021:307 2022:993 2024:333 2025:307 2026:310
  BOZEMAN YELLOWSTONE INTL                  2015:40 2017:472 2018:665 2019:358 2021:325 2023:325 2024:428
  CABLE                                     2013:146 2015:150 2016:173 2019:258 2020:375 2022:307 2023:595 2025:307 2026:307
  CENTENNIAL                                2014:475 2015:5 2017:0 2018:16 2019:496 2020:0 2021:7 2022:204 2023:211 2025:381 2026:154
  Centennial Airport                        2008:0 2009:0 2010:0 2013:360 2018:360 2020:0 2021:0 2022:370 2024:174 2025:0 2026:174
  FALCON FLD                                2014:618 2015:162 2016:328 2017:263 2018:328 2021:328 2022:97 2023:50 2024:158 2025:158
  Falcon Field Airport                      2008:240 2010:150 2011:0 2012:232 2013:56 2014:0 2021:338 2023:0
  LAKE HOOD                                 2014:170 2015:180 2016:181 2018:784 2019:254 2021:450 2022:409
  MERRILL FIELD                             2008:0 2013:317 2015:95 2016:613 2017:311 2018:562 2019:279 2020:281
  Merrill Field                             2008:0 2009:0 2010:90 2011:0 2012:0 2015:0 2024:539 2025:771 2026:558
  N/A                                       2018:349 2020:115 2021:839 2022:662 2023:526 2024:200 2025:1.6K 2026:480
  NONE                                      2008:410 2009:295 2010:330 2011:157 2013:40 2014:140 2017:45 2018:0 2020:477 2022:555 2023:427 2024:272 2025:157
  NORTH LAS VEGAS                           2013:90 2015:0 2016:307 2017:767 2018:0 2019:184 2021:570 2022:45 2023:314 2025:15
  NORTH PERRY                               2016:212 2017:196 2018:196 2019:915 2020:0 2021:473 2023:384 2025:651 2026:438
  None                                      2008:44.9K 2009:52.4K 2010:47.3K 2011:54.9K 2012:67.1K 2013:54.0K 2014:57.0K 2015:68.6K 2016:62.6K 2017:61.3K 2018:65.4K 2019:66.5K 2020:48.0K 2021:65.8K 2022:55.7K 2023:66.8K 2024:58.5K 2025:50.3K 2026:31.0K
  North Las Vegas                           2008:448 2009:177 2010:0 2011:0 2013:220 2014:200 2018:0 2019:66 2020:362 2021:330 2023:81
  PALM BEACH COUNTY PARK                    2014:353 2015:1.1K 2018:352 2021:339 2022:0 2023:703 2025:345
  PHOENIX DEER VALLEY                       2013:0 2014:185 2015:0 2016:90 2017:212 2018:546 2019:301 2022:123 2024:83 2025:438
  PORTLAND-HILLSBORO                        2008:0 2013:134 2014:0 2016:344 2018:709 2020:134 2021:135 2022:459 2024:295 2026:331
  PVT                                       2010:340 2012:41 2013:0 2014:556 2015:25 2017:22 2018:711 2019:362 2020:892 2021:1.5K 2022:376 2023:542 2024:904 2025:648 2026:201
  Phoenix Deer Valley Airport               2008:0 2009:360 2010:180 2011:215 2013:330 2015:0 2022:83 2025:171 2026:255
  Private                                   2008:1.0K 2009:931 2010:1.0K 2011:1.5K 2012:2.3K 2013:2.2K 2014:2.2K 2015:1.5K 2016:186 2017:1.5K 2018:3.2K 2019:1.3K 2020:1.8K 2021:3.4K 2022:1.9K 2023:464 2024:2.2K 2025:1.3K 2026:135
  Private Airstrip                          2008:635 2009:1.5K 2010:703 2011:1.9K 2012:3.4K 2013:1.0K 2014:1.1K 2015:1.7K 2016:132 2017:289 2018:1.0K 2019:367 2020:229 2021:215 2022:332 2023:762 2024:612 2026:106
  Private Strip                             2008:50 2009:315 2010:327 2011:543 2012:821 2013:575 2014:283 2015:250 2016:160 2017:235 2018:222 2021:75 2025:323
  RENO/STEAD                                2013:157 2014:316 2015:211 2016:805 2017:422 2018:817 2022:489
  VAN NUYS                                  2015:0 2016:336 2017:642 2018:278 2020:166 2023:339 2024:335 2025:339 2026:310
  VANCE BRAND                               2015:0 2016:643 2017:330 2018:428 2019:318 2020:313 2025:315
  Wittman Regional Airport                  2008:0 2009:0 2010:0 2011:180 2012:0 2013:75 2014:0 2015:0 2019:180 2021:185 2023:175 2024:0 2025:5

METAR by EV_DATE, dollars = WX_OBS_DIR
  K1F0 071415Z AUTO 14003KT 10SM CLR 13/11  2020:291
  K1P1 271715Z AUTO 26003KT 10SM CLR 27/12  2024:515
  KCMD 241355Z AUTO 06011KT 10SM FEW120 10  2023:360
  KDWH 291853Z 02011G21KT 10SM CLR 26/03 A  2020:360
  KGTU 011756Z 20012KT 10SM OVC028 30/23 A  2020:10
  KI74 201855Z AUTO 00000KT 10SM SCT040 SC  2021:360
  KJWN 050150Z 15008KT 10SM CLR 19/15 A299  2024:360
  KLAF 261754Z 01009KT 10SM OVC018 27/21 A  2023:360
  KLFK 021453Z AUTO 10006KT 6SM -RA BR BKN  2020:300
  KMKL 221953Z 07006KT 10SM CLR 20/13 A301  2020:242
  KPDT 161753Z 32004KT 10SM BKN050 BKN065   2024:132
  KPGD 222253Z 01006KT 10SM FEW043 24/19 A  2020:76
  KRNV 261815Z AUTO 00000KT 10SM CLR A3004  2022:360
  KSJT 281051Z AUTO 20009G16KT 8SM OVC020   2019:72
  METAR K4F2 202135Z AUTO 06003KT 10SM OVC  2020:341
  METAR K4S2 061655Z AUTO 00000KT 10SM CLR  2019:137
  METAR KCDI 271855Z AUTO 09003KT 10SM BKN  2020:215
  METAR KF70 280035Z AUTO 22007KT 10SM CLR  2023:360
  METAR KFHR 121453Z AUTO 00000KT 2 1/2SM   2018:141
  METAR KFSD 070856Z AUTO 15013G27KT 10SM   2020:246
  METAR KGYR 011647Z VRB04KT 10SM SKC 29/1  2025:492
  METAR KHUT 111752Z 19017KT 10SM CLR 32/2  2019:28
  METAR KLYH 101854Z 28009G22KT 250V320 10  2025:360
  METAR KSAT 020051Z 32004KT 10SM CLR 12/M  2019:117
  METAR KTAZ 112100Z AUTO 30014G19KT 10SM   2022:360
  None                                      2008:151.8K 2009:166.0K 2010:156.0K 2011:171.9K 2012:185.6K 2013:161.4K 2014:167.1K 2015:195.7K 2016:202.7K 2017:199.6K 2018:218.5K 2019:189.6K 2020:117.6K 2021:33.1K 2022:11.2K 2023:13.3K 2024:6.9K 2025:10.9K 2026:5.9K
  PAKN 072354Z 09020G32KT 10SM BKN065 12/0  2024:360
  PATK 161953Z 31003KT 10SM CLR 21/11 A300  2021:153
  SPECI KCNO 051828Z 00000KT 10SM HZ CLR 3  2020:218
  SPECI KMFR 092222Z 32007KT 10SM -RA FEW0  2019:236

## what

EV_TYPE: ACC 93%, INC 7%

EV_DOW: Sa 18%, Su 15%, Fr 15%, Th 14%, We 13%, Mo 13%, Tu 12%

EV_TMZN: UTC 96%, None 4%

EV_YEAR: 2008 9%, 2011 9%, 2012 9%, 2010 9%, 2009 9%, 2022 8%, 2018 8%, 2024 8%, 2016 8%, 2023 8%, 2021 8%, 2017 8%

EV_MONTH: 7 12%, 6 11%, 8 11%, 5 10%, 9 9%, 10 8%, 4 8%, 3 8%, 2 6%, 11 6%, 1 6%, 12 6%

MID_AIR: None 98%, N 1%, Y 1%

ON_GROUND_COLLISION: None 98%, Y 1%, N 1%

LATLONG_ACQ: MEAS 61%, None 29%, EST 10%

EV_NR_APT_LOC: ONAP 43%, OFAP 42%, None 15%

WX_SRC_IIC: WFAC 70%, None 22%, PILO 7%, WIT 0%

WX_OBS_TMZN: UTC 52%, None 48%

LIGHT_COND: DAYL 73%, None 18%, NITE 5%, DUSK 2%, NDRK 2%, DAWN 1%, NR 0%, NBRT 0%

SKY_COND_NONCEIL: CLER 45%, None 32%, FEW 11%, SCAT 11%, UNK 1%, OVCT 1%

SKY_COND_CEIL: NONE 50%, None 29%, BKN 13%, OVC 8%, UNK 1%, VV 0%

WIND_DIR_IND: U 93%, Y 7%, None 0%

WIND_VEL_IND: F 93%, T 7%, None 0%

GUST_IND: T 52%, F 48%, None 0%

EV_HIGHEST_INJURY: NONE 51%, FATL 20%, MINR 13%, SERS 11%, None 5%

INJ_TOT_M: 0 83%, 1 11%, 2 4%, 3 1%, 4 0%, 5 0%, 6 0%, 7 0%, 9 0%, 8 0%, 11 0%, 10 0%

INJ_TOT_S: 0 87%, 1 10%, 2 2%, 3 0%, 4 0%, 5 0%, 6 0%, 7 0%, 12 0%, 14 0%, 8 0%, 32 0%

INVEST_AGY: N 81%, O 18%, None 1%

WX_COND_BASIC: VMC 78%, None 17%, IMC 4%, Unk 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| EV_ID | id | 31.4K | 0 | 20260731203497 155; 20260731203496 155; 20260730203490 155; 20260728203478 155 |
| NTSB_NO | id | 30.2K | 0 | DCA26WA297 155; GAA26WA267 155; CEN26LA274 155; WPR26LA280 155 |
| EV_TYPE | category | 2 | 0 | ACC 28.7K; INC 2.3K |
| EV_DATE | date | 6.8K | 0 | 2026-07-07 00:00:00 164; 2026-07-05 00:00:00 161; 2026-02-06 00:00:00 161; 2026-07-18 00:00:00 160 |
| EV_DOW | category | 7 | 0 | Sa 5.5K; Su 4.8K; Fr 4.7K; Th 4.2K |
| EV_TIME | other | 1.4K | 0 | 1800.0 529; 1900.0 466; 2000.0 465; 2100.0 456 |
| EV_TMZN | category | 2 | 0 | UTC 29.8K; None 1.2K |
| EV_CITY | who | 10.5K | 0 | Skwentna 156; New York 156; Peyton 156; Lafayette 156 |
| EV_STATE | other | 58 | 0 | None 4.7K; CA 2.3K; TX 2.1K; FL 1.9K |
| EV_COUNTRY | other | 185 | 0 | USA 25.2K; BR 497; AU 373; GB 358 |
| EV_SITE_ZIPCODE | other | 9.2K | 0 | None 6.6K; 0 133; 99667 124; 37083 124 |
| EV_YEAR | category | 19 | 0 | 2008 1.9K; 2011 1.8K; 2012 1.8K; 2010 1.8K |
| EV_MONTH | category | 12 | 0 | 7 3.8K; 6 3.4K; 8 3.4K; 5 3.0K |
| MID_AIR | category | 3 | 0 | None 30.5K; N 287; Y 194 |
| ON_GROUND_COLLISION | category | 3 | 0 | None 30.5K; Y 287; N 194 |
| LATITUDE | other | 20.2K | 0 | None 3.4K; 481243N 139; 032415N 139; 034393N 139 |
| LONGITUDE | other | 22.4K | 0 | None 3.4K; 0106356W 139; 0955859W 139; 0963641W 139 |
| LATLONG_ACQ | category | 3 | 0 | MEAS 18.9K; None 8.9K; EST 3.2K |
| APT_NAME | who | 11.5K | 0 | None 11.9K; Private 207; Private Airstrip 104; N/A 99 |
| EV_NR_APT_ID | other | 6.5K | 0 | None 11.7K; PVT 351; NONE 213; N/A 185 |
| EV_NR_APT_LOC | category | 3 | 0 | ONAP 13.3K; OFAP 13.1K; None 4.6K |
| APT_DIST | amount | 318 | 0 | 0.0 24.7K; 1.0 2.8K; 2.0 586; 0.5 364 |
| APT_DIR | amount | 363 | 0 | nan 20.9K; 0.0 1.4K; 90.0 306; 180.0 289 |
| APT_ELEV | amount | 2.7K | 0 | nan 14.0K; 10.0 132; 13.0 132; 9.0 112 |
| WX_BRIEF_COMP | other | 1 | 0 | None 31.0K |
| WX_SRC_IIC | category | 4 | 0 | WFAC 21.8K; None 6.7K; PILO 2.3K; WIT 144 |
| WX_OBS_TIME | other | 1.1K | 0 | nan 7.9K; 1753.0 613; 1653.0 586; 1853.0 552 |
| WX_OBS_DIR | amount | 365 | 0 | 0.0 12.7K; 270.0 592; 180.0 586; 360.0 580 |
| WX_OBS_FAC_ID | other | 4.6K | 0 | None 7.7K; PAAQ 121; KFLY 119; KDVT 119 |
| WX_OBS_ELEV | amount | 2.5K | 0 | nan 9.5K; 10.0 195; 8.0 125; 9.0 125 |
| WX_OBS_DIST | amount | 157 | 0 | 0.0 15.0K; 1.0 1.9K; 10.0 866; 5.0 786 |
| WX_OBS_TMZN | category | 2 | 0 | UTC 16.0K; None 15.0K |
| LIGHT_COND | category | 8 | 0 | DAYL 22.6K; None 5.6K; NITE 1.4K; DUSK 596 |
| SKY_COND_NONCEIL | category | 6 | 0 | CLER 13.9K; None 9.8K; FEW 3.5K; SCAT 3.3K |
| SKY_NONCEIL_HT | amount | 119 | 0 | 0.0 23.7K; 5000.0 372; 6000.0 368; 3000.0 254 |
| SKY_CEIL_HT | amount | 117 | 0 | 0.0 24.6K; 10000.0 283; 25000.0 266; 6000.0 255 |
| SKY_COND_CEIL | category | 6 | 0 | NONE 15.6K; None 8.9K; BKN 3.9K; OVC 2.4K |
| VIS_RVR | amount | 29 | 0 | nan 30.9K; 6000.0 7; 5000.0 5; 5500.0 3 |
| VIS_RVV | other | 1 | 0 | None 31.0K |
| VIS_SM | amount | 67 | 0 | 10.0 20.9K; nan 6.9K; 7.0 494; 9.0 392 |
| WX_TEMP | amount | 149 | 0 | 0.0 6.7K; 81.0 1.2K; 79.0 1.2K; 75.0 1.1K |
| WX_DEW_PT | amount | 130 | 0 | 0.0 7.8K; 52.0 908; 55.0 883; 54.0 879 |
| WIND_DIR_DEG | amount | 134 | 0 | 0.0 12.2K; 180.0 763; 200.0 712; 170.0 700 |
| WIND_DIR_IND | category | 3 | 0 | U 28.8K; Y 2.1K; None 8 |
| WIND_VEL_KTS | amount | 56 | 0 | nan 11.0K; 5.0 2.4K; 4.0 2.2K; 6.0 2.2K |
| WIND_VEL_IND | category | 3 | 0 | F 28.8K; T 2.1K; None 8 |
| GUST_IND | category | 3 | 0 | T 16.1K; F 14.8K; None 8 |
| GUST_KTS | amount | 56 | 0 | 0.0 27.0K; 15.0 361; 20.0 338; 18.0 332 |
| ALTIMETER | who | 289 | 0 | 0.0 7.7K; 30.040000915527344 976; 29.950000762939453 874; 30.1200008392334 731 |
| WX_DENS_ALT | other | 1 | 0 | None 31.0K |
| WX_INT_PRECIP | other | 1 | 0 | None 31.0K |
| METAR | who | 6.1K | 0 | None 24.8K; KGGW 241453Z AUTO 00000KT 31; METAR KTRL 231753Z AUTO 0 31; METAR KADH 211935Z AUTO 0 31 |
| EV_HIGHEST_INJURY | category | 5 | 0 | NONE 15.7K; FATL 6.3K; MINR 4.1K; SERS 3.4K |
| INJ_F_GRND | amount | 13 | 0 | nan 27.9K; 0.0 3.0K; 1.0 63; 2.0 14 |
| INJ_M_GRND | amount | 11 | 0 | nan 27.3K; 0.0 3.6K; 1.0 63; 2.0 22 |
| INJ_S_GRND | amount | 10 | 0 | nan 28.0K; 0.0 2.9K; 1.0 86; 2.0 19 |
| INJ_TOT_F | other | 62 | 0 | 0 24.7K; 1 3.3K; 2 1.7K; 3 515 |
| INJ_TOT_M | category | 36 | 0 | 0 25.8K; 1 3.4K; 2 1.2K; 3 250 |
| INJ_TOT_N | other | 338 | 0 | 0 13.4K; 1 8.1K; 2 5.5K; 3 1.2K |
| INJ_TOT_S | category | 22 | 0 | 0 26.8K; 1 3.1K; 2 750; 3 150 |
| INJ_TOT_T | amount | 338 | 0 | 1.0 13.1K; 2.0 9.8K; 3.0 2.4K; 4.0 1.4K |
| INVEST_AGY | category | 3 | 0 | N 25.1K; O 5.7K; None 225 |
| NTSB_DOCKET | other | 1 | 0 | None 31.0K |
| NTSB_NOTF_FROM | other | 1 | 0 | None 31.0K |
| NTSB_NOTF_DATE | other | 1 | 0 | None 31.0K |
| NTSB_NOTF_TM | other | 1 | 0 | None 31.0K |
| FICHE_NUMBER | other | 1 | 0 | None 31.0K |
| LCHG_DATE | date | 10.0K | 0 | 2020-09-25 18:01:38 370; 2020-09-25 18:00:53 366; 2020-09-25 18:06:16 347; 2020-09-25 17:59:24 342 |
| LCHG_USERID | other | 191 | 0 | None 18.7K; coln 5.0K; broda 930; dobn 675 |
| WX_COND_BASIC | category | 4 | 0 | VMC 24.2K; None 5.3K; IMC 1.2K; Unk 318 |
| FAA_DIST_OFFICE | other | 1 | 0 | None 31.0K |
| DEC_LATITUDE | amount | 23.1K | 0 | nan 3.4K; 48.212 139; 32.68472 139; 34.65082 139 |
| DEC_LONGITUDE | amount | 23.7K | 0 | nan 3.4K; -106.585 139; -95.98316 139; -96.61133 139 |
| INGESTED_AT | audit | 1 | 0 | 1786154107240125 31.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 767e3583-447f-4101-bd46-a 31.0K |
| SRC_SHA256 | who | 1 | 0 | 0cf30a610d18eb109035b8310 31.0K |
