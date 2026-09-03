# PORTAL_CKA_WESTERN_PENNSYLV_F810ADDEEC

rows 6.5K  columns 82  scan 6.0s

roles: amount 45, audit 2, category 15, date 1, empty 3, id 3, other 11, who 3

## when

INGESTED_AT
  2026      6.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 6.4K | 39.72 | 40.19 | 40.97 | 41.28 | 258.9K |
| LONGITUDE | 6.4K | -80.52 | -80.13 | -79.24 | -78.91 | -515.4K |
| LANDSLIDEAREA | 4.8K | 1.8K | 40.0K | 454.0K | 1.95M | 333.69M |
| SLOPE | 6.4K | 0 | 11.10 | 26.13 | 36.20 | 74.3K |
| ASPECT | 6.4K | 0 | 159.90 | 355.96 | 360 | 1.08M |
| WETNESSINDEX | 6.4K | 9.24 | 11.47 | 17.77 | 25.98 | 74.7K |

## who

MUNICIPALITY by rows
      1.3K  PITTSBURGH
       351  MORRIS
       272  AMWELL
       221  EAST FINLEY
       201  CENTER
       198  WEST FINLEY
       184  DONEGAL
       158  WHITELEY
       141  WEST BETHLEHEM
       136  WASHINGTON
       135  FRANKLIN
       115  SOUTH STRABANE
       103  WAYNE
        93  ALEPPO
        89  RICHHILL
        88  NORTH BETHLEHEM
        86  SOUTH FRANKLIN
        86  PERRY
        85  INDEPENDENCE
        85  JEFFERSON

MUNICIPALITY by dollars
       53.4K     1.3K rows  PITTSBURGH
       14.0K      351 rows  MORRIS
       10.9K      272 rows  AMWELL
        8.9K      221 rows  EAST FINLEY
        8.0K      201 rows  CENTER
        7.9K      198 rows  WEST FINLEY
        7.4K      184 rows  DONEGAL
        6.3K      158 rows  WHITELEY
        5.6K      141 rows  WEST BETHLEHEM
        5.4K      136 rows  WASHINGTON
        5.4K      135 rows  FRANKLIN
        4.6K      115 rows  SOUTH STRABANE
        4.1K      103 rows  WAYNE
        3.7K       93 rows  ALEPPO
        3.6K       89 rows  RICHHILL
        3.5K       88 rows  NORTH BETHLEHEM
        3.4K       86 rows  SOUTH FRANKLIN
        3.4K       86 rows  PERRY
        3.4K       85 rows  INDEPENDENCE
        3.4K       85 rows  JEFFERSON

SOILUNIT by rows
      1.9K  Bogart loam, 2 to 6 percent slopes
       840  Ernest silt loam, 8 to 25 percent slopes, extremely stony
       679  Ginat silt loam, 0 to 2 percent slopes
       279  Urban land-Conotton complex, 8 to 25 percent slopes
       264  Ernest silt loam, 8 to 15 percent slopes
       231  Riverhead sandy loam, 8 to 15 percent slopes
       226  Varilla very channery sandy loam, 50 to 80 percent slopes, extremely b
       192  Tyler silt loam, 0 to 2 percent slopes
       131  Gilpin-Weikert channery silt loams, 3 to 8 percent slopes
       106  Hazleton channery sandy loam, 3 to 8 percent slopes
        93  Fredon loam, 3 to 8 percent slopes
        88  Rayne silt loam, Conemaugh geology, 3 to 8 percent slopes
        78  Hazleton channery sandy loam, 3 to 8 percent slopes, extremely stony
        64  Udorthents, acid material, very steep
        59  Tyler silt loam, 2 to 6 percent slopes
        55  Clymer channery loam, 3 to 8 percent slopes
        51  Allegheny silt loam, 3 to 8 percent slopes
        50  Gresham silt loam, 3 to 8 percent slopes
        47  Bethesda channery silt loam, 8 to 25 percent slopes
        43  Buchanan loam, 8 to 15 percent slopes

SOILUNIT by dollars
       76.1K     1.9K rows  Bogart loam, 2 to 6 percent slopes
       33.6K      840 rows  Ernest silt loam, 8 to 25 percent slopes, extremely stony
       27.5K      679 rows  Ginat silt loam, 0 to 2 percent slopes
       11.2K      279 rows  Urban land-Conotton complex, 8 to 25 percent slopes
       10.7K      264 rows  Ernest silt loam, 8 to 15 percent slopes
        9.3K      231 rows  Riverhead sandy loam, 8 to 15 percent slopes
        9.1K      226 rows  Varilla very channery sandy loam, 50 to 80 percent slopes, e
        7.8K      192 rows  Tyler silt loam, 0 to 2 percent slopes
        5.3K      131 rows  Gilpin-Weikert channery silt loams, 3 to 8 percent slopes
        4.3K      106 rows  Hazleton channery sandy loam, 3 to 8 percent slopes
        3.8K       93 rows  Fredon loam, 3 to 8 percent slopes
        3.5K       88 rows  Rayne silt loam, Conemaugh geology, 3 to 8 percent slopes
        3.2K       78 rows  Hazleton channery sandy loam, 3 to 8 percent slopes, extreme
        2.6K       64 rows  Udorthents, acid material, very steep
        2.4K       59 rows  Tyler silt loam, 2 to 6 percent slopes
        2.2K       55 rows  Clymer channery loam, 3 to 8 percent slopes
        2.0K       51 rows  Allegheny silt loam, 3 to 8 percent slopes
        2.0K       50 rows  Gresham silt loam, 3 to 8 percent slopes
        1.9K       47 rows  Bethesda channery silt loam, 8 to 25 percent slopes
        1.8K       43 rows  Buchanan loam, 8 to 15 percent slopes

SRC_SHA256 by rows
      6.5K  a69cdef0a4cd79ef1c06e3eeae3d6964534122ab8d29f090fd1d68d07a3d8c61

SRC_SHA256 by dollars
      258.9K     6.5K rows  a69cdef0a4cd79ef1c06e3eeae3d6964534122ab8d29f090fd1d68d07a3d

## who x when

MUNICIPALITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  ALEPPO                                    2026:3.7K
  AMWELL                                    2026:10.9K
  CENTER                                    2026:8.0K
  DONEGAL                                   2026:7.4K
  EAST FINLEY                               2026:8.9K
  FRANKLIN                                  2026:5.4K
  INDEPENDENCE                              2026:3.4K
  JEFFERSON                                 2026:3.4K
  MORRIS                                    2026:14.0K
  NORTH BETHLEHEM                           2026:3.5K
  PERRY                                     2026:3.4K
  PITTSBURGH                                2026:53.4K
  RICHHILL                                  2026:3.6K
  SOUTH FRANKLIN                            2026:3.4K
  SOUTH STRABANE                            2026:4.6K
  WASHINGTON                                2026:5.4K
  WAYNE                                     2026:4.1K
  WEST BETHLEHEM                            2026:5.6K
  WEST FINLEY                               2026:7.9K
  WHITELEY                                  2026:6.3K

SOILUNIT by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  Allegheny silt loam, 3 to 8 percent slop  2026:2.0K
  Bethesda channery silt loam, 8 to 25 per  2026:1.9K
  Bogart loam, 2 to 6 percent slopes        2026:76.1K
  Buchanan loam, 8 to 15 percent slopes     2026:1.8K
  Clymer channery loam, 3 to 8 percent slo  2026:2.2K
  Ernest silt loam, 8 to 15 percent slopes  2026:10.7K
  Ernest silt loam, 8 to 25 percent slopes  2026:33.6K
  Fredon loam, 3 to 8 percent slopes        2026:3.8K
  Gilpin-Weikert channery silt loams, 3 to  2026:5.3K
  Ginat silt loam, 0 to 2 percent slopes    2026:27.5K
  Gresham silt loam, 3 to 8 percent slopes  2026:2.0K
  Hazleton channery sandy loam, 3 to 8 per  2026:4.3K
  Hazleton channery sandy loam, 3 to 8 per  2026:3.2K
  Rayne silt loam, Conemaugh geology, 3 to  2026:3.5K
  Riverhead sandy loam, 8 to 15 percent sl  2026:9.3K
  Tyler silt loam, 0 to 2 percent slopes    2026:7.8K
  Tyler silt loam, 2 to 6 percent slopes    2026:2.4K
  Udorthents, acid material, very steep     2026:2.6K
  Urban land-Conotton complex, 8 to 25 per  2026:11.2K
  Varilla very channery sandy loam, 50 to   2026:9.1K

## what

DATA_SOURCE: USGS 75%, 311 16%, Adams 3%, Nasa 2%, Ackenheil 1%, City 1%, County 1%, Pitt 0%, ForestHill 0%

COUNTY: ALLEGHENY 34%, WASHINGTON 33%, GREENE 21%, BEAVER 4%, ARMSTRONG 4%, WESTMORELAND 2%, BUTLER 1%, INDIANA 1%, FAYETTE 0%, CLARION 0%, JEFFERSON 0%

STATEROUTE: 51 25%, 65 12%, 18 12%, 130 12%, 837 12%, 2020 12%, 88 12%

STARTSEGMENT: 770 25%, 192 25%, 60 25%, 70 25%

ABOVEORBELOWROAD: A 79%, B 21%

SLIDETYPEDCNR: Rockfall 35%, Mudflow 19%, Debris slide 12%, Debris flow 11%, Earthflow 11%, Debris avalanche 5%, Slump 3%, Soil creep 2%, soil creep 1%, Debris Slide 1%, Rock slump 1%

MONTH: 4 14%, 2 13%, 5 13%, 3 12%, 7 10%, 6 10%, 1 7%, 8 6%, 9 6%, 12 5%, 10 4%

DAY: 26 11%, 13 10%, 21 9%, 23 9%, 16 9%, 28 9%, 7 9%, 17 9%, 1 9%, 25 9%, 15 8%

YEAR: 2018 27%, 2019 24%, 2020 10%, 2022 9%, 2017 8%, 2021 8%, 2016 5%, 2015 4%, 2011 2%, 1951 1%, 2013 1%

TOPOGRAPHICROUGHNESS: 5 20%, 4 19%, 6 15%, 7 11%, 3 9%, 8 8%, 9 6%, 10 4%, 11 3%, 12 2%, 2 2%, 13 1%

EROSIONHAZARDPOTENTIAL: Severe 62%, Slight 20%, Not rated 16%, Moderate 2%, xx 0%

PLANNINGLIMITATIONLOCALROADSANDSTREETS: Very limited 84%, Somewhat limited 11%, Not rated 6%, xx 0%, Not limited 0%

GEOLOGICFORMATIONORGROUP: Greene Formation 28%, Casselman Formation 24%, Washington Formation 18%, Glenshaw Formation 10%, Monongahela Group 9%, Allegheny Formation 6%, Waynesburg Formation 4%, Pottsville Formation 1%, Shenango Formation through Osw 0%, Burgoon Sandstone 0%, Mauch Chunk Formation 0%

NUMBEROFFREEZETHAWALTERATIONSOVER7DAYSBEFORELANDSLIDE: 0 68%, 3 7%, 4 6%, 2 6%, 5 5%, 1 4%, 6 3%

NUMBEROFFREEZETHAWALTERATIONSOVER30DAYSBEFORELANDSLIDE: 0 63%, 13 5%, 12 5%, 17 4%, 20 4%, 15 3%, 14 3%, 18 3%, 3 3%, 16 3%, 19 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 6.4K | 0 | USGS-4844 33; USGS-4843 33; USGS-4842 33; USGS-4841 33 |
| DATA_SOURCE | category | 9 | 0 | USGS 4.8K; 311 1.0K; Adams 223; Nasa 127 |
| ORIGINALLABEL | id | 1.6K | 4.9K | 14011939 9; 14012979 9; 14006188 9; 14016488 9 |
| LATITUDE | amount | 6.2K | 27 | 41.27635963 33; 41.05523997 33; 41.05398809 33; 41.03684898 33 |
| LONGITUDE | amount | 6.2K | 27 | -79.09187694 33; -79.85382862 33; -79.85398669 33; -79.63775417 33 |
| COUNTY | category | 14 | 27 | ALLEGHENY 2.2K; WASHINGTON 2.1K; GREENE 1.4K; BEAVER 248 |
| MUNICIPALITY | who | 259 | 27 | PITTSBURGH 1.3K; MORRIS 351; AMWELL 272; EAST FINLEY 221 |
| STATEROUTE | category | 8 | 6.5K | 51 2; 65 1; 18 1; 130 1 |
| STARTSEGMENT | category | 5 | 6.5K | 770 1; 192 1; 60 1; 70 1 |
| OFFSETFROMSTARTSEGMENT | empty | 1 | 6.5K |  |
| ABOVEORBELOWROAD | category | 3 | 6.4K | A 50; B 13 |
| SLIDETYPEDCNR | category | 13 | 6.3K | Rockfall 45; Mudflow 24; Debris slide 15; Debris flow 14 |
| LANDSLIDEAREA | amount | 4.9K | 1.6K | 22824.58 25; 89310.62 25; 74240.63 25; 443094.92 25 |
| LANDSLIDEDOWNSLOPEDISPLACEMENT | empty | 1 | 6.5K |  |
| DEPTHTOFAILUREPLANE | empty | 1 | 6.5K |  |
| MONTH | category | 13 | 5.2K | 4 168; 2 162; 5 158; 3 139 |
| DAY | category | 32 | 5.2K | 26 56; 13 50; 21 49; 23 47 |
| YEAR | category | 41 | 5.2K | 2018 308; 2019 274; 2020 112; 2022 107 |
| ELEVATION | other | 739 | 39 | 1113 35; 1013 34; 1107 34; 990 34 |
| LOCALRELIEF | other | 425 | 39 | 181 64; 192 61; 205 51; 204 51 |
| SLOPE | amount | 303 | 40 | 11.1 85; 10.0 83; 10.4 82; 10.6 79 |
| TOPOGRAPHICROUGHNESS | category | 29 | 27 | 5 1.3K; 4 1.2K; 6 955; 7 703 |
| ASPECT | amount | 3.0K | 73 | 355.9 33; 111.7 33; 88.2 33; 21.7 33 |
| DRAINAGEAREA | other | 5.7K | 27 | 1490 36; 27129 34; 18317 33; 35386 33 |
| WETNESSINDEX | amount | 616 | 73 | 11.53 48; 11.38 48; 11.34 46; 11.33 46 |
| HILLSLOPEPOSITION | amount | 102 | 40 | 0.36 160; 0.4 156; 0.39 151; 0.44 140 |
| DISTANCETONEARESTSTREAM | other | 1.6K | 27 | 0 57; 60 54; 120 53; 21 48 |
| DISTANCETONEARESTROAD | amount | 2.5K | 27 | 0.0 400; 30.1 248; 21.3 231; 42.5 216 |
| MEANCURVATURE | other | 5.8K | 39 | 2.12e-05 33; -1.59e-05 33; -0.000232848 33; 0.000147082 33 |
| PLANARCURVATURE | id | 6.1K | 39 | -5.35e-05 33; 0.000123346 33; 0.001369171 33; -0.000401441 33 |
| PROFILECURVATURE | other | 5.8K | 39 | -4.07e-05 33; 1.6e-05 33; 9.97e-05 33; -0.000198178 33 |
| SOILUNIT | who | 200 | 27 | Bogart loam, 2 to 6 perce 1.9K; Ernest silt loam, 8 to 25 840; Ginat silt loam, 0 to 2 p 679; Urban land-Conotton compl 279 |
| SANDCONTENT | amount | 346 | 983 | 13.6 826; 12.4 233; 17.5 232; 12.3 231 |
| SILTCONTENT | amount | 451 | 983 | 57.5 1.1K; 57.8 414; 57.7 356; 57.6 332 |
| CLAYCONTENT | amount | 315 | 983 | 28.9 793; 29.9 284; 30.7 214; 29.0 159 |
| ERODIBILITYFACTOR | amount | 48 | 983 | 0.29 1.4K; 0.28 903; 0.26 364; 0.3 329 |
| AVERAGESOILTHICKNESS | amount | 2.2K | 983 | 57.91 603; 56.69 191; 44.46 190; 31.54 86 |
| AASHTOSOIL | amount | 1.2K | 983 | 12.9 592; 14.11 207; 16.72 190; 3.46 89 |
| EROSIONHAZARDPOTENTIAL | category | 6 | 27 | Severe 4.0K; Slight 1.3K; Not rated 1.0K; Moderate 123 |
| EROSIONCLASS | amount | 203 | 1.3K | 1.0 2.4K; 3.0 239; 1.01 94; 1.02 69 |
| PLANNINGLIMITATIONLOCALROADSANDSTREETS | category | 6 | 27 | Very limited 5.4K; Somewhat limited 681; Not rated 359; xx 4 |
| DRAINAGECLASS | amount | 226 | 626 | 3.55 994; 3.56 551; 4.0 297; 3.92 280 |
| RUNOFFCLASS | amount | 158 | 5.7K | 6.0 141; 5.2 49; 5.84 33; 5.67 31 |
| SOILSLIPPOTENTIAL | amount | 202 | 960 | 3.0 668; 2.9 633; 1.65 188; 1.0 154 |
| SOILPOROSITY | amount | 48 | 627 | 0.46 2.9K; 0.47 466; 0.48 428; 0.49 361 |
| SATURATEDHYDRAULICCONDUCTIVITY | amount | 1.5K | 627 | 10.43 634; 10.23 214; 11.65 196; 9.32 88 |
| GEOLOGICFORMATIONORGROUP | category | 13 | 27 | Greene Formation 1.8K; Casselman Formation 1.5K; Washington Formation 1.2K; Glenshaw Formation 612 |
| ELEVATIONABOVEPITTSBURGHCOAL | other | 1.1K | 2.6K | 43 22; 115 22; 286 22; 603 22 |
| ELEVATIONABOVEUPPERFREEPORTCOAL | other | 1.5K | 448 | 268 35; 175 34; 287 33; 304 33 |
| DIPOFPITTSBURGHCOAL | amount | 30 | 2.6K | 0.2 720; 0.3 636; 0.1 611; 0.4 477 |
| DIPOFUPPERFREEPORTCOAL | amount | 28 | 454 | 0.2 1.2K; 0.1 1.0K; 0.3 925; 0.0 814 |
| ASPECTOFPITTSBURGHCOAL | amount | 2.1K | 2.6K | 237.0 21; 251.9 21; 137.5 20; 180.7 20 |
| ASPECTOFUPPERFREEPORTCOAL | amount | 2.2K | 454 | 184.5 32; 180.1 32; 288.1 31; 85.2 31 |
| DISTANCETOUNDERGROUNDMINE | other | 3.4K | 27 | 0 1.8K; 30 55; 60 35; 451 26 |
| DEPTHTOUNDERGROUNDMINE | other | 763 | 4.7K | 163 11; 272 11; 352 10; 277 10 |
| MEANPRECIPITATIONATDAYOFLANDSLIDE | amount | 156 | 5.2K | 0.0 544; 0.02 35; 0.05 32; 0.1 28 |
| MEANPRECIPITATIONOVER2DAYSBEFORELANDSLIDE | amount | 132 | 5.3K | 0.0 313; 0.02 53; 0.03 47; 0.01 46 |
| MEANPRECIPITATIONOVER7DAYSBEFORELANDSLIDE | amount | 77 | 5.2K | 0.07 49; 0.1 47; 0.03 46; 0.02 45 |
| MEANPRECIPITATIONOVER30DAYSBEFORELANDSLIDE | amount | 40 | 5.2K | 0.14 97; 0.15 91; 0.12 82; 0.16 80 |
| MEANPRECIPITATIONOVER90DAYSBEFORELANDSLIDE | amount | 21 | 5.3K | 0.15 144; 0.13 136; 0.14 135; 0.12 114 |
| MEANPRECIPITATIONOVER180DAYSBEFORELANDSLIDE | amount | 17 | 5.3K | 0.13 229; 0.14 176; 0.12 132; 0.15 115 |
| NUMBEROFFREEZETHAWALTERATIONSOVER7DAYSBEFORELANDSLIDE | category | 8 | 5.3K | 0 790; 3 85; 4 71; 2 71 |
| MEANLENGTHOFFREEZETHAWCYCLESOVER7DAYSBEFORELANDSLIDE | amount | 7 | 6.1K | 1.75 85; 1.4 71; 2.33 71; 1.17 56 |
| MEANTEMPERATUREOFFREEZECYCLESOVER7DAYSBEFORELANDSLIDE | amount | 122 | 6.1K | 27.5 18; 27.9 10; 26.3 10; 27.1 9 |
| MINIMUMTEMPERATUREOFFREEZECYCLESOVER7DAYSBEFORELANDSLIDE | amount | 161 | 6.1K | 26.4 12; 24.6 11; 25.2 9; 27.1 9 |
| MEANTEMPERATUREOFTHAWCYCLESOVER7DAYSBEFORELANDSLIDE | amount | 152 | 6.1K | 40.0 9; 45.6 8; 40.2 7; 42.2 7 |
| MEANGENERALTEMPERATUREOVER7DAYSBEFORELANDSLIDE | amount | 452 | 5.3K | 76.1 11; 52.0 10; 75.4 10; 66.9 9 |
| NUMBEROFFREEZETHAWALTERATIONSOVER30DAYSBEFORELANDSLIDE | category | 27 | 5.3K | 0 597; 13 49; 12 45; 17 42 |
| MEANLENGTHOFFREEZETHAWCYCLESOVER30DAYSBEFORELANDSLIDE | amount | 26 | 5.9K | 2.14 49; 2.31 45; 1.67 42; 1.43 37 |
| MEANTEMPERATUREOFFREEZECYCLESOVER30DAYSBEFORELANDSLIDE | amount | 108 | 5.9K | 23.9 22; 21.6 18; 24.7 14; 24.4 13 |
| MINIMUMTEMPERATUREOFFREEZECYCLESOVER30DAYSBEFORELANDSLIDE | amount | 210 | 5.9K | 8.5 18; 11.1 12; 10.9 12; 20.0 12 |
| MEANTEMPERATUREOFTHAWCYCLESOVER30DAYSBEFORELANDSLIDE | amount | 154 | 5.9K | 46.4 16; 42.2 14; 43.2 12; 42.6 12 |
| MEANGENERALTEMPERATUREOVER30DAYSBEFORELANDSLIDE | amount | 415 | 5.3K | 35.1 16; 36.3 14; 34.2 14; 35.5 13 |
| NUMBEROFFREEZETHAWALTERATIONSOVER365DAYSBEFORELANDSLIDE | other | 60 | 5.3K | 80 73; 65 70; 85 66; 81 64 |
| MEANLENGTHOFFREEZETHAWCYCLESOVER365DAYSBEFORELANDSLIDE | amount | 62 | 5.3K | 4.51 73; 5.53 70; 4.24 66; 4.45 64 |
| MEANTEMPERATUREOFFREEZECYCLESOVER365DAYSBEFORELANDSLIDE | amount | 69 | 5.3K | 22.9 102; 22.7 73; 23.0 73; 19.4 59 |
| MINIMUMTEMPERATUREOFFREEZECYCLESOVER365DAYSBEFORELANDSLIDE | amount | 143 | 5.3K | -4.7 143; -5.0 55; -4.1 48; 5.3 40 |
| MEANTEMPERATUREOFTHAWCYCLESOVER365DAYSBEFORELANDSLIDE | amount | 38 | 5.3K | 58.5 91; 58.4 87; 58.6 81; 58.8 81 |
| MEANGENERALTEMPERATUREOVER365DAYSBEFORELANDSLIDE | amount | 67 | 5.3K | 52.8 66; 52.7 48; 52.3 48; 52.4 48 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:09:45.79690 6.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 50f0f3c1-2146-4a07-8928-e 6.5K |
| SRC_SHA256 | who | 1 | 0 | a69cdef0a4cd79ef1c06e3eea 6.5K |
