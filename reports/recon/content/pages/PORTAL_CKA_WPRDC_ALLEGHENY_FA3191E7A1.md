# PORTAL_CKA_WPRDC_ALLEGHENY_FA3191E7A1

rows 10.0K  columns 32  scan 6.0s

roles: amount 3, audit 2, category 8, date 4, id 5, other 5, who 6

## when

EV_DATE
  1988         1  
  1993         1  
  1995         1  
  1996         2  
  1997        10  
  1998         7  
  2000         1  
  2003         3  
  2004         1  
  2005         2  
  2006        10  
  2007       359  ########
  2008       485  ###########
  2009       388  ########
  2010      1.4K  ##############################
  2011      1.2K  ##########################
  2012       681  ###############
  2013      1.0K  ######################
  2014       916  ####################
  2015      1.2K  ##########################
  2016      1.1K  ########################
  2017      1.1K  ########################
  2018       184  ####

SUB_DATE
  2014      5.6K  ##############################
  2015       695  ####
  2016      2.1K  ###########
  2017      1.3K  #######
  2018       240  #

EDIT_DATE
  2018     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 10.0K | -46.77 | 30.64 | 56.32 | 72.63 | 260.0K |
| LONGITUDE | 10.0K | -179.98 | 18.85 | 174.70 | 179.99 | 29.6K |
| GAZ_DIST | 10.0K | 0 | 8.17 | 32.68 | 50.92 | 96.4K |

## who

SRC_NAME by rows
       637  Oregon DOT
        96  maps.google.com
        67  news.xinhuanet
        65  thehimalayantimes
        62  newsinfo.inquirer
        57  thejakartapost
        53  ibnlive.in
        48  Times of India
        40  The Jakarta Post
        40  The Himalayan Times
        37  Seattle Times
        36  The Hindu
        36  articles.timesofindia.indiatimes.com
        36  Hindustan Times
        35  laht
        34  reliefweb
        34  GMA News
        34  google
        33  colombiareports.com
        32  Red Cross - Field reports

SRC_NAME by dollars
       28.4K      637 rows  Oregon DOT
        1.8K       65 rows  thehimalayantimes
        1.7K       37 rows  Seattle Times
        1.6K       67 rows  news.xinhuanet
        1.4K       53 rows  ibnlive.in
        1.2K       48 rows  Times of India
        1.1K       40 rows  The Himalayan Times
        1.0K       22 rows  seattletimes.nwsource
      994.88       36 rows  Hindustan Times
      877.76       62 rows  newsinfo.inquirer
      854.96       36 rows  articles.timesofindia.indiatimes.com
      839.53       18 rows  USGS
      825.56       30 rows  Indian Express
      815.53       20 rows  AKI Press
      757.84       27 rows  eKantipur
      756.47       15 rows  Global News
      752.55       27 rows  Himalayan Times
      738.10       25 rows  chinadaily
      716.76       22 rows  The Tribune
      711.48       29 rows  The Times of India

DIV_NAME by rows
       856  Oregon
       554  California
       435  Washington
       229  Jammu and Kashmir
       191  Uttaranchal
       178  British Columbia
       166  Himachal Pradesh
       156  England
       151  Rio de Janeiro
       146  Colorado
       128  Pennsylvania
       120  Kentucky
       104  West Virginia
       100  Jawa Barat
        90  Ohio
        89  Utah
        87  Benguet
        86  Assam
        85  Manipur
        84  Cebu

DIV_NAME by dollars
       38.2K      856 rows  Oregon
       20.7K      435 rows  Washington
       20.2K      554 rows  California
        9.0K      178 rows  British Columbia
        8.1K      156 rows  England
        7.7K      229 rows  Jammu and Kashmir
        5.8K      191 rows  Uttaranchal
        5.7K      146 rows  Colorado
        5.2K      166 rows  Himachal Pradesh
        5.2K      128 rows  Pennsylvania
        4.5K      120 rows  Kentucky
        4.0K      104 rows  West Virginia
        3.6K       90 rows  Ohio
        3.5K       89 rows  Utah
        3.2K       57 rows  Scotland
        3.2K       70 rows  Idaho
        2.6K       74 rows  North Carolina
        2.4K       69 rows  North-West Frontier
        2.3K       82 rows  Gandaki
        2.3K       75 rows  Sichuan

STORM_NAME by rows
        25  Supertyphoon Juan (Megi)
        20  Tropical Depression Parma
        19  Agaton
        12  Tropical Cyclone Agatha
        11  Tropical Storm Tomas
        11  Tropical Depression Urduja
        10  Utor
        10  Lawin
         9  Trami
         9  Karen
         9  Hurricane Tomas
         7  Earl
         6  Soudelor
         6  Seniang
         6  Typhoon Morakot
         6  Typhoon Aure(Aere), Bebeng
         5  Tropical Storm Olga
         5  Tropical Storm Noel
         5  Typhoon Chedeng (Songda)
         5  Hurricane Dora

STORM_NAME by dollars
      401.32       25 rows  Supertyphoon Juan (Megi)
      334.34       20 rows  Tropical Depression Parma
      267.53       10 rows  Utor
      187.65        9 rows  Trami
      176.51       12 rows  Tropical Cyclone Agatha
      173.73       19 rows  Agaton
      166.63       10 rows  Lawin
      163.44        6 rows  Soudelor
      139.16        7 rows  Earl
      138.80        6 rows  Typhoon Morakot
      136.44        9 rows  Karen
      124.91        3 rows  Hurricane Sandy
      122.12        9 rows  Hurricane Tomas
      121.57        3 rows  Frank
      107.39        4 rows  Toraji
      104.16       11 rows  Tropical Storm Tomas
       96.84        4 rows  Tropical Storm Nicole
       96.36       11 rows  Tropical Depression Urduja
       94.89        5 rows  Ingrid
       94.23        5 rows  Hurricane Dora

CTRY_NAME by rows
      3.2K  United States
      1.4K  India
       649  Philippines
       487  China
       485  Nepal
       363  Indonesia
       242  Canada
       236  United Kingdom
       205  Brazil
       194  Malaysia
       155  Pakistan
       120  New Zealand
       120  Vietnam
       100  Colombia
        98  Australia
        85  Sri Lanka
        82  Mexico
        80  Bangladesh
        75  Japan
        73  Guatemala

CTRY_NAME by dollars
      132.0K     3.2K rows  United States
       36.2K     1.4K rows  India
       13.9K      487 rows  China
       13.6K      485 rows  Nepal
       12.6K      236 rows  United Kingdom
       12.1K      242 rows  Canada
        7.8K      649 rows  Philippines
        5.3K      155 rows  Pakistan
        2.6K       75 rows  Japan
        2.6K       60 rows  Italy
        2.4K       59 rows  Kyrgyzstan
        2.1K      120 rows  Vietnam
        1.8K       80 rows  Bangladesh
        1.6K       82 rows  Mexico
        1.6K       37 rows  Georgia
        1.4K       31 rows  Switzerland
        1.4K       33 rows  Bulgaria
        1.3K       22 rows  Norway
        1.3K       24 rows  Ireland
        1.1K       73 rows  Guatemala

## who x when

SRC_NAME by EV_DATE, dollars = LATITUDE
  AKI Press                                 2017:815.53
  GMA News                                  2007:48.84 2008:13.48 2009:31 2011:21.42 2012:17.67 2014:158.48 2015:27.17 2016:64.41
  Global News                               2014:198.29 2015:102.29 2016:256.65 2017:50.25 2018:148.99
  Himalayan Times                           2010:55.62 2011:285.53 2014:106.90 2015:56.07 2016:193.75 2017:54.68
  Hindustan Times                           2009:39.08 2010:34.12 2012:117.01 2014:66.10 2015:276.44 2016:124.58 2017:337.55
  Indian Express                            2010:31.11 2014:58.75 2015:215.68 2016:487.39 2017:32.63
  Oregon DOT                                2011:4.1K 2012:7.4K 2013:2.9K 2014:5.1K 2015:6.8K 2016:2.1K
  Red Cross - Field reports                 2007:668.86
  Seattle Times                             2005:94.83 2006:380.33 2007:94.34 2008:47.55 2009:92.09 2010:191.62 2011:142.84 2013:95.90 2014:170.94 2015:373.04 2016:47.86
  The Himalayan Times                       2010:27.87 2014:28.29 2015:106.67 2016:751.31 2017:195.40
  The Hindu                                 2013:51.48 2014:21.28 2015:144.49 2016:181.47 2017:186.40 2018:34.30
  The Jakarta Post                          2009:-7.57 2010:-1.87 2014:-111.56 2015:-1.73 2016:-27.31 2017:-44.31
  The Times of India                        2011:30.77 2014:74.45 2015:382.75 2016:44.77 2017:62.72 2018:116.02
  The Tribune                               2015:317.47 2016:35.77 2017:363.52
  Times of India                            2010:36.20 2011:320.41 2013:32.36 2014:333.39 2015:121.39 2016:189.81 2017:102.89 2018:30.72
  USGS                                      1996:91.13 1997:428.84 1998:319.56
  articles.timesofindia.indiatimes.com      2013:854.96
  chinadaily                                2008:51.89 2010:147.38 2011:312.47 2012:226.36
  colombiareports.com                       2008:21.64 2010:50.60 2011:112.33 2012:6.98 2013:1.74
  eKantipur                                 2013:28.27 2014:393.49 2015:336.08
  google                                    2009:92.91 2010:304.97 2011:55.34 2012:92.41
  ibnlive.in                                2011:1.2K 2012:213.31
  laht                                      2008:3.25 2009:16.20 2010:52.62 2011:-96.82 2012:-33.94
  maps.google.com                           2010:-2.2K
  news.xinhuanet                            2008:488.75 2009:105.07 2010:714.96 2011:269.62 2012:32.06
  newsinfo.inquirer                         2008:238.61 2009:129.54 2010:106.48 2011:317.64 2012:85.49
  reliefweb                                 2008:116.43 2009:-18.53 2010:282.40 2011:22.05 2012:10.41 2014:74.09
  seattletimes.nwsource                     2010:239.22 2011:762 2012:47.95
  thehimalayantimes                         2008:139.88 2009:113.59 2010:588.13 2011:731.05 2012:253.64
  thejakartapost                            2008:-15.68 2009:-53.23 2010:-108.31 2011:-51.57 2012:-9.96 2015:0.91

DIV_NAME by EV_DATE, dollars = LATITUDE
  Assam                                     2007:77.64 2008:132.93 2009:50.69 2010:279.55 2011:128.14 2012:128.67 2013:78.44 2014:364.33 2015:180.52 2016:332.01 2017:466.59
  Benguet                                   2007:49.15 2008:98.82 2009:330.11 2010:180.80 2011:131.24 2012:49.37 2013:148.79 2015:181.39 2016:231.21 2017:32.61
  British Columbia                          2000:52.08 2007:252.37 2008:561.91 2009:148.36 2010:695.87 2011:612.64 2012:548.62 2013:509.62 2014:805.28 2015:1.3K 2016:866.60 2017:2.2K 2018:511.07
  California                                2007:250.56 2008:661.43 2009:399.92 2010:2.5K 2011:2.3K 2012:877.71 2013:494.43 2014:1.8K 2015:1.4K 2016:3.1K 2017:6.2K 2018:187.65
  Cebu                                      2007:30.90 2008:71.58 2009:20.25 2010:196.30 2011:124.13 2012:72.36 2013:134.32 2014:72.56 2015:10.36 2016:61.86 2017:71.86
  Colorado                                  2007:160.04 2008:310.38 2009:40.12 2010:505.36 2011:587.33 2012:200.24 2013:1.1K 2014:388.03 2015:699.64 2016:1.1K 2017:547.08
  England                                   1993:54.27 2007:413.48 2008:321.64 2009:51.04 2010:575.19 2011:105.63 2012:998.28 2013:565.34 2014:1.6K 2015:572.92 2016:1.7K 2017:930.39 2018:208.83
  Gandaki                                   2007:56.25 2008:112.41 2009:168.11 2010:224.64 2011:392.82 2012:84.49 2013:111.74 2014:225.45 2015:367.26 2016:338.24 2017:225.62
  Himachal Pradesh                          2007:64.83 2008:313.25 2009:159.28 2010:1.4K 2011:508.48 2012:253.66 2013:949.35 2014:189.92 2015:668.28 2016:314.55 2017:443.29
  Idaho                                     2007:43.68 2008:133.61 2009:43.69 2011:365.30 2012:284.30 2013:742.13 2014:87.66 2015:179.03 2016:315.28 2017:990.10
  Jammu and Kashmir                         2007:201.60 2008:433.43 2010:745.90 2011:900.69 2012:503.44 2013:535.41 2014:769.20 2015:1.5K 2016:531.30 2017:1.3K 2018:204.81
  Jawa Barat                                2007:-6.79 2008:-27.81 2009:-7.47 2010:-139.78 2011:-69.53 2012:-130.68 2013:-68.09 2014:-75.03 2015:-13.89 2016:-70.61 2017:-80.54
  Kentucky                                  2007:114.01 2008:39.04 2009:186.37 2010:749.73 2011:682.84 2012:74.68 2013:410.13 2014:341.28 2015:1.0K 2016:413.64 2017:487.79
  Manipur                                   2007:124.69 2008:49.59 2009:49.85 2010:451.90 2011:199.62 2012:24.81 2013:200.86 2015:595.08 2016:50.49 2017:321.66 2018:49.85
  North Carolina                            2008:70.86 2009:107.17 2010:249.82 2011:71.57 2012:35.44 2013:926.90 2014:35.40 2015:321.55 2016:214.18 2017:287.78 2018:320.96
  North-West Frontier                       2007:70.62 2008:69.56 2010:312.72 2011:209.54 2012:70.74 2013:140.24 2014:34.50 2015:459.14 2016:625.47 2017:422.18
  Ohio                                      2007:80.48 2008:159.23 2009:39.12 2010:272.38 2011:1.5K 2012:236.72 2013:117.74 2014:195.39 2015:400.56 2016:118.40 2017:320.07 2018:118.07
  Oregon                                    1996:91.13 1998:224.94 2006:44.10 2007:318.37 2008:313.73 2009:227.97 2010:494.67 2011:5.9K 2012:8.6K 2013:3.0K 2014:6.0K 2015:8.1K 2016:2.8K 2017:2.0K 2018:89.66
  Pennsylvania                              2007:40.39 2008:242.44 2009:40.44 2010:405.26 2011:1.1K 2012:242.74 2013:565.86 2014:403.94 2015:567 2016:363.60 2017:810.54 2018:366.71
  Rio de Janeiro                            2007:-44.33 2008:-22.38 2009:-91.35 2010:-2.5K 2011:-491.70 2012:-44.27 2013:-136.13 2016:-45.44 2018:-23
  Scotland                                  2007:117.81 2008:112.82 2009:340.16 2010:282.10 2011:340.70 2012:396.36 2013:169.90 2014:566.29 2015:286.28 2016:457.37 2017:55.89 2018:113.63
  Sichuan                                   2007:209.15 2008:246.87 2009:120.56 2010:301.60 2011:338.85 2012:207.34 2013:306.61 2014:62.61 2015:121.29 2016:238.99 2017:64.16 2018:58.34
  Utah                                      2008:79.05 2009:286.35 2010:159.79 2011:320.13 2012:198.59 2013:1.2K 2014:158.82 2015:432.29 2016:81.44 2017:592.35 2018:78.46
  Uttaranchal                               2007:121.27 2008:29.33 2009:88.70 2010:1.3K 2011:910.61 2012:242.35 2013:1.6K 2014:151.03 2015:548.14 2016:516.04 2017:272.75 2018:30.72
  Washington                                1997:381.18 1998:94.62 2005:94.83 2006:380.33 2007:421.76 2008:239.28 2009:1.1K 2010:2.6K 2011:2.4K 2012:993.36 2013:1.1K 2014:2.5K 2015:3.6K 2016:1.0K 2017:3.5K 2018:189.13
  West Virginia                             2008:114.14 2009:38.18 2010:153.73 2011:626.72 2012:76.04 2013:420.18 2014:38.16 2015:881.91 2016:806.02 2017:576.63 2018:270.71

## what

EV_TIME: 09:00 18%, 23:00 17%, unknown 14%, 15:00 10%, 08:00 10%, 18:00 9%, 22:00 5%, 14:00 5%, 10:00 5%, 12:00 4%, 16:00 4%

LOC_ACCU: 5km 29%, 1km 20%, 25km 13%, 10km 13%, exact 12%, 50km 7%, unknown 5%, 100km 0%, 250km 0%

LS_CAT: landslide 69%, mudslide 19%, rock_fall 6%, complex 2%, debris_flow 2%, other 1%, riverbank_collapse 0%, unknown 0%, translational_slide 0%, snow_avalanche 0%, creep 0%, earth_flow 0%

LS_TRIG: downpour 43%, rain 24%, unknown 15%, continuous_rain 7%, tropical_cyclone 5%, snowfall_snowmelt 1%, monsoon 1%, mining 1%, earthquake 1%, construction 1%, flooding 1%, no_apparent_trigger 1%

LS_SIZE: medium 59%, small 25%, unknown 7%, large 7%, very_large 1%, catastrophic 0%

LS_SETTING: unknown 57%, above_road 28%, natural_slope 5%, urban 2%, below_road 2%, mine 2%, above_river 1%, deforested_slope 1%, retaining_wall 1%, other 0%, bluff 0%

INJURIES: 0 95%, 1 2%, 2 1%, 3 1%, 5 0%, 4 0%, 7 0%, 6 0%, 10 0%, 8 0%, 12 0%, 20 0%

EV_IMP_SRC: GLC 100%, LRC 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SRC_NAME | who | 3.7K | 1 | Oregon DOT 637; maps.google.com 96; news.xinhuanet 67; thehimalayantimes 67 |
| SRC_LINK | other | 7.9K | 673 | http://maps.google.com.br 96; http://www.laprensa.hn/su 47; http://english.people.com 47; http://www.nwcn.com/news/ 47 |
| EV_ID | id | 9.9K | 0 | 7,449 50; 2,039 50; 3,161 50; 9,208 50 |
| EV_DATE | date | 3.0K | 0 | 2010-04-06 108; 2015-12-08 53; 2016-12-16 52; 2017-03-26 52 |
| EV_TIME | category | 25 | 5.5K | 09:00 550; 23:00 512; unknown 414; 15:00 296 |
| EV_TITLE | id | 9.7K | 1 | OR 62, milepost 34 51; San Juan Arriba de El Cor 50; Chongqing municipality 50; Germantown road, Portland 50 |
| EV_DESC | other | 8.6K | 725 | O mapa da devastao no Rio 48; The victim was identified 47; A highway is blocked afte 47; Melting snow and the rece 47 |
| LOC_DESC | id | 9.5K | 98 | Ozgon, Osh 51; OR 62, milepost 34 51; San Juan Arriba de El Cor 50; Chongqing municipality 50 |
| LOC_ACCU | category | 10 | 2 | 5km 2.9K; 1km 2.0K; 25km 1.3K; 10km 1.3K |
| LS_CAT | category | 16 | 2 | landslide 6.9K; mudslide 1.9K; rock_fall 620; complex 207 |
| LS_TRIG | category | 19 | 27 | downpour 4.2K; rain 2.4K; unknown 1.5K; continuous_rain 688 |
| LS_SIZE | category | 7 | 9 | medium 5.9K; small 2.5K; unknown 722; large 711 |
| LS_SETTING | category | 15 | 73 | unknown 5.6K; above_road 2.8K; natural_slope 493; urban 243 |
| FATALITIES | other | 99 | 0 | 0 7.8K; 1 583; 2 367; 3 272 |
| INJURIES | category | 41 | 0 | 0 9.4K; 1 193; 2 103; 3 70 |
| STORM_NAME | who | 207 | 9.5K | Supertyphoon Juan (Megi) 25; Tropical Depression Parma 20; Agaton 19; Tropical Cyclone Agatha 12 |
| PHOTO_LINK | id | 1.4K | 8.5K | http://www.9news.com/img/ 11; http://www.laprensa.hn/cs 8; http://images2.sina.com/e 8; https://thehimalayantimes 8 |
| COMMENTS | other | 268 | 9.7K | Video in link 11; Date approximate 9; Date approximated from da 5; Event occurred in the mor 5 |
| EV_IMP_SRC | category | 2 | 0 | GLC 9.9K; LRC 50 |
| EV_IMP_ID | id | 8.4K | 1.6K | 7449 43; 2039 43; 3161 43; 9208 43 |
| LATITUDE | amount | 9.7K | 0 | 13.2861 50; 29.66239066 50; 45.5872 50; 28.1855 50 |
| LONGITUDE | amount | 9.7K | 0 | -122.6169 51; -87.0329 50; 107.1969335 50; -122.7739 50 |
| CTRY_NAME | who | 151 | 33 | United States 3.2K; India 1.4K; Philippines 649; China 487 |
| CTRY_CODE | other | 143 | 33 | US 3.2K; IN 1.4K; PH 649; CN 487 |
| DIV_NAME | who | 960 | 36 | Oregon 856; California 554; Washington 435; Jammu and Kashmir 229 |
| GAZ_POINT | who | 4.4K | 0 | Santos Dumont 83; Steamboat 54; Tidewater 54; Pearson Airpark 52 |
| GAZ_DIST | amount | 2.5K | 0 | 10.87 51; 7.89 51; 1.58 51; 4.55 51 |
| SUB_DATE | date | 400 | 7 | 2014-04-01 4.7K; 2014-08-24 331; 2016-06-30 162; 2016-07-08 151 |
| EDIT_DATE | date | 1 | 0 | 2018-06-23 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:25:29.02505 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4d1fa03d-7f91-4a51-b898-a 10.0K |
| SRC_SHA256 | who | 1 | 0 | 706ec2e60ed5d5308816970b9 10.0K |
