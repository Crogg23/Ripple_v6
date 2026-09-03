# FED_USGS_3DEP

rows 5.0K  columns 34  scan 4.1s

roles: amount 5, audit 2, category 3, date 2, empty 3, id 5, other 7, who 7

## when

ACQUISITIONDATE
  2010        10  
  2012        79  #
  2013      2.7K  ##############################
  2014        61  #
  2015        40  
  2016       146  ##
  2017       183  ##
  2018       226  ###
  2019       334  ####
  2020       170  ##
  2021       188  ##
  2022       161  ##
  2023       304  ###
  2024       295  ###
  2025       115  #

PUBDATE
  2013      2.6K  ##############################
  2015        51  #
  2016        62  #
  2017        90  #
  2018       170  ##
  2019       346  ####
  2020        78  #
  2021       181  ##
  2022       178  ##
  2023       213  ##
  2024       429  #####
  2026       566  ######

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LOWPS | 5.0K | 10.31 | 30.92 | 61.84 | 61.84 | 156.9K |
| CENTERX | 5.0K | -19.96M | -11.74M | 14.97M | 19.98M | -59.69B |
| CENTERY | 5.0K | -1.63M | 7.66M | 16.59M | 18.31M | 38.78B |
| SHAPE_LENGTH | 5.0K | 446.8K | 628.1K | 1.74M | 2.20M | 3.46B |
| SHAPE_AREA | 5.0K | 12.48B | 22.60B | 84.50B | 110.42B | 130698.32B |

## who

NAME by rows
         3  n60w144
         3  n61w159
         3  n70w157
         3  n59w153
         3  n70w158
         3  n65w165
         3  n69w146
         3  n65w158
         3  n65w142
         3  n66w153
         3  n65w151
         3  n54w168
         3  n56w134
         3  n66w167
         3  n54e172
         3  n63w148
         3  n63w161
         3  n68w141
         3  n53w171
         3  n66w145

NAME by dollars
      103.07        3 rows  n53w170
      103.07        3 rows  n68w145
      103.07        3 rows  n69w162
      103.07        3 rows  n66w147
      103.07        3 rows  n62w166
      103.07        3 rows  n57w162
      103.07        3 rows  n71w164
      103.07        3 rows  n52e178
      103.07        3 rows  n63w165
      103.07        3 rows  n63w152
      103.07        3 rows  n67w159
      103.07        3 rows  n65w142
      103.07        3 rows  n62w146
      103.07        3 rows  n53w171
      103.07        3 rows  n69w155
      103.07        3 rows  n67w142
      103.07        3 rows  n61w161
      103.07        3 rows  n54w168
      103.07        3 rows  n69w159
      103.07        3 rows  n61w159

PRODUCTNAME by rows
      5.0K  USGS_3DEP

PRODUCTNAME by dollars
      156.9K     5.0K rows  USGS_3DEP

TAG by rows
      5.0K  Dataset

TAG by dollars
      156.9K     5.0K rows  Dataset

VERTICALDATUM by rows
      5.0K  North American Vertical Datum of 1988 (NAVD 88)

VERTICALDATUM by dollars
      156.9K     5.0K rows  North American Vertical Datum of 1988 (NAVD 88)

## who x when

NAME by ACQUISITIONDATE, dollars = LOWPS
  n52e178                                   2019:103.07
  n53w170                                   2018:103.07
  n53w171                                   2019:103.07
  n54e172                                   2019:103.07
  n54w168                                   2018:103.07
  n56w134                                   2018:103.07
  n57w162                                   2018:103.07
  n59w153                                   2019:103.07
  n60w144                                   2012:61.84 2013:41.23
  n61w159                                   2017:103.07
  n62w166                                   2016:103.07
  n63w148                                   2012:103.07
  n63w152                                   2010:103.07
  n63w161                                   2017:103.07
  n63w165                                   2025:103.07
  n65w142                                   2016:103.07
  n65w151                                   2010:41.23 2013:61.84
  n65w158                                   2017:103.07
  n65w165                                   2013:103.07
  n66w145                                   2016:103.07
  n66w147                                   2016:61.84 2017:41.23
  n66w153                                   2017:103.07
  n66w167                                   2013:103.07
  n68w141                                   2016:103.07
  n68w145                                   2016:103.07
  n69w146                                   2016:103.07
  n69w162                                   2013:103.07
  n70w157                                   2018:103.07
  n70w158                                   2018:103.07
  n71w164                                   2013:103.07

PRODUCTNAME by ACQUISITIONDATE, dollars = LOWPS
  USGS_3DEP                                 2010:371.05 2012:3.2K 2013:86.9K 2014:2.5K 2015:1.5K 2016:5.7K 2017:6.7K 2018:7.6K 2019:10.4K 2020:4.4K 2021:4.8K 2022:4.1K 2023:7.6K 2024:7.4K 2025:3.8K

## what

MAXPS: 150 87%, 27 13%

RESOLUTION_X: 0.00001 54%, 2.77777777786999E-04 14%, 0.00027777778 7%, 9.25925926922017E-05 7%, 0.00055555556 6%, 2.7777777803598E-04 4%, 0.000092592593 3%, 9.25925927753796E-05 2%, 2.77777777787015E-04 1%, 5.55555554709991E-04 1%, 5.55555554709975E-04 1%, 9.25925926921964E-05 0%

RESOLUTION_Y: 1e-05 54%, -0.000277777777786999 13%, 0.00027777778 7%, -9.259259269220167e-05 6%, 0.00055555556 6%, -0.00027777777803598015 3%, 9.2592593e-05 3%, -9.25925927753796e-05 2%, -0.0002777777777870148 2%, -0.00027777777803599587 1%, -0.0005555555547099906 1%, -9.259259269219641e-05 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 5.0K | 0 | 5000 25; 4999 25; 4998 25; 4997 25 |
| NAME | who | 3.8K | 0 | n63w146 25; n40w086 25; n39w109 25; n49w102 25 |
| MINPS | other | 1 | 0 | 0 5.0K |
| MAXPS | category | 2 | 0 | 150 4.3K; 27 668 |
| LOWPS | amount | 22 | 0 | 30.92208098137158 2.2K; 30.92208098137202 850; 30.92208098137114 607; 10.307360350155633 504 |
| HIGHPS | other | 1 | 0 | 16 5.0K |
| CATEGORY | other | 1 | 0 | 1 5.0K |
| TAG | who | 1 | 0 | Dataset 5.0K |
| GROUPNAME | empty | 1 | 5.0K |  |
| PRODUCTNAME | who | 1 | 0 | USGS_3DEP 5.0K |
| CENTERX | amount | 5.0K | 0 | -16196988.579473468 25; -9517817.009178007 25; -12078165.947791614 25; -11298929.497391257 25 |
| CENTERY | amount | 5.0K | 0 | 8979699.652812887 25; 4793808.590740921 25; 4650550.096673631 25; 6190860.344912688 25 |
| ZORDER | empty | 1 | 5.0K |  |
| SHAPE_LENGTH | amount | 5.0K | 0 | 705638.5036000399 25; 511748.54840000195 25; 507694.1111000025 25; 559273.0112000118 25 |
| SHAPE_AREA | amount | 5.0K | 0 | 26899717362.75014 25; 16095861513.29569 25; 15869941479.368982 25; 18744000744.506966 25 |
| DATASET_ID | other | 1 | 0 | usgs 5.0K |
| BEST | other | 441 | 0 | 130288 2.5K; 141574 133; 112574 55; 101288 55 |
| DEM_TYPE | other | 1 | 0 | 1 5.0K |
| SOURCE | other | 1 | 0 | USGS 5.0K |
| VERTICALDATUM | who | 1 | 0 | North American Vertical D 5.0K |
| ACQUISITIONDATE | date | 240 | 0 | 1357862400000 2.6K; 1451606400000 134; 1563753600000 80; 1325376000000 79 |
| URL | id | 5.0K | 0 | https://prd-tnm.s3.amazon 25; https://prd-tnm.s3.amazon 25; https://prd-tnm.s3.amazon 25; https://prd-tnm.s3.amazon 25 |
| METADATA | id | 5.0K | 0 | D:\USGS_3DEP\data\13\n63w 25; D:\USGS_3DEP\data\13\n40w 25; D:\USGS_3DEP\data\13\n39w 25; D:\USGS_3DEP\data\13\n49w 25 |
| PUBDATE | date | 301 | 0 | 2013 2.6K; 20191113 54; 20260515 53; 20260326 51 |
| TITLE | id | 4.9K | 0 | USGS 1/3 arc-second n63w1 25; USGS 1/3 Arc Second n40w0 25; USGS 1/3 Arc Second n39w1 25; USGS 1/3 Arc Second n49w1 25 |
| RESOLUTION_X | category | 40 | 0 | 0.00001 2.6K; 2.77777777786999E-04 671; 0.00027777778 340; 9.25925926922017E-05 321 |
| RESOLUTION_Y | category | 46 | 0 | 1e-05 2.6K; -0.000277777777786999 650; 0.00027777778 340; -9.259259269220167e-05 283 |
| CDATE | empty | 1 | 5.0K |  |
| STARTDATE | who | 277 | 0 | 19990201 2.6K; 0 89; 2016 82; 20190601 80 |
| ENDDATE | who | 234 | 0 | 20131101 2.6K; 2016 134; 20190722 80; 2012 79 |
| SHAPE | id | 5.1K | 0 | {"rings": [[[-16252710.12 25; {"rings": [[[-9573538.611 25; {"rings": [[[-12133887.54 25; {"rings": [[[-11354651.09 25 |
| _INGESTED_AT | audit | 1 | 0 | 1783016046692652 5.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 7957c0b7-adb1-4839-a30a-6 5.0K |
| _SRC_SHA256 | who | 1 | 0 | 0368d6541ca069701b4a1754e 5.0K |
