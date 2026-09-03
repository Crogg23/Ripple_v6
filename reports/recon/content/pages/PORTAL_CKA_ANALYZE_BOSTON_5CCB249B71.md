# PORTAL_CKA_ANALYZE_BOSTON_5CCB249B71

rows 10.0K  columns 33  scan 6.5s

roles: amount 8, audit 2, category 9, date 3, empty 2, id 1, other 6, who 3

## when

NEW_INSP_D
  1970      1.7K  #######
  2013       240  #
  2014      7.3K  ##############################
  2015       701  ###

INSP_DATE
  1899      1.0K  #######
  2008       209  #
  2009       313  ##
  2010       725  #####
  2011      3.2K  #####################
  2012      4.5K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SWK_WIDTH | 10.0K | 0 | 7 | 23.18 | 1.8K | 77.6K |
| SWK_SLOPE | 10.0K | 0 | 2.80 | 9.60 | 218 | 31.1K |
| DAM_WIDTH | 9.9K | 0 | 6.50 | 19 | 95 | 65.6K |
| SCI | 9.8K | -23.6K | 89.90 | 100 | 100 | 703.2K |
| CURB_REV | 10.0K | 0 | 5 | 8 | 66 | 47.1K |
| RCR | 10.0K | -2 | 6.30 | 14.80 | 55.60 | 61.2K |

## who

PARENT by rows
       243  CENTR6
       154  DORCH1
        88  ADAMS1
        80  DUDLE1
        64  HYDE 1
        58  BLUE 3
        58  BUNKE1
        54  BAKER3
        53  GALLI1
        53  COLUM15
        48  BOWDO3
        48  BEACO1
        48  BEECH2
        46  E EIG1
        45  BOYLS6
        43  CHELS1
        43  ALBAN3
        42  D ST 1
        40  GENEV1
        39  BERKE1

PARENT by dollars
        1.7K      243 rows  CENTR6
      889.30      154 rows  DORCH1
      565.80       88 rows  ADAMS1
      474.70       80 rows  DUDLE1
      444.30       53 rows  COLUM15
      402.70       48 rows  BEACO1
      385.40       64 rows  HYDE 1
      358.40       48 rows  BOWDO3
      357.50       43 rows  CHELS1
      350.50       54 rows  BAKER3
      349.80       43 rows  ALBAN3
      348.90       36 rows  CLARE5
      330.10       46 rows  E EIG1
      326.30       39 rows  BERKE1
      323.60       48 rows  BEECH2
      303.70       45 rows  BOYLS6
      302.80       58 rows  BLUE 3
      287.50       35 rows  DARTM2
      282.50       42 rows  D ST 1
      275.30       35 rows  BLUE 1

NOTES by rows
       423  NO DAMAGE
        29  CRACKING
        26  CRACKED
        21  private
        17  BC PATCH
        16  LIP
        16  NOT CITY
        15  EMPTY TREE PIT
        13  Private way
        13  DCR
        13  DISTORTION
        12  NOT City
        12  TREE PITS
        11  ASPHALT PATCH
        11  Private
        10  COBBLE STONE CURB
        10  No damage
        10  No Sidewalk
        10  NO CURB
         8  City limits

NOTES by dollars
        1.3K      423 rows  NO DAMAGE
      189.40       26 rows  CRACKED
      161.10       29 rows  CRACKING
      107.60       16 rows  LIP
      105.40       17 rows  BC PATCH
       94.70       13 rows  DISTORTION
       93.80       15 rows  EMPTY TREE PIT
       70.40       12 rows  TREE PITS
       67.20       11 rows  ASPHALT PATCH
       64.80       10 rows  No damage
       60.10       16 rows  NOT CITY
       57.50        3 rows  BECC
       52.80        8 rows  City limits
          52        6 rows  HIP CURB
       48.10        7 rows  TREE PIT
       48.10       10 rows  COBBLE STONE CURB
       41.10        5 rows  DCR roadway
       41.10        8 rows  NO damage
       40.70       10 rows  NO CURB
       40.20        7 rows  BC PATCH AT HYDRANT

SRC_SHA256 by rows
     10.0K  3a3b6c2bb1407a5d3d2ea7c526f5003093301eb67c836b6b427b1baf922e9f24

SRC_SHA256 by dollars
       61.2K    10.0K rows  3a3b6c2bb1407a5d3d2ea7c526f5003093301eb67c836b6b427b1baf922e

## who x when

PARENT by INSP_DATE, dollars = RCR
  ADAMS1                                    1899:0 2011:98 2012:467.80
  ALBAN3                                    1899:0 2009:6.40 2011:263.70 2012:79.70
  BAKER3                                    1899:0 2011:135.20 2012:215.30
  BEACO1                                    1899:0 2009:22.70 2010:182.30 2011:190.40 2012:7.30
  BEECH2                                    1899:0 2012:323.60
  BERKE1                                    1899:0 2010:185.50 2011:140.80
  BLUE 1                                    1899:0 2012:275.30
  BLUE 3                                    1899:0 2012:302.80
  BOWDO3                                    1899:0 2012:358.40
  BOYLS6                                    1899:0 2010:112.50 2011:191.20
  BUNKE1                                    1899:0 2008:260.40
  CENTR6                                    1899:0 2010:17.40 2011:898.80 2012:806.20
  CHELS1                                    1899:0 2009:62.10 2012:295.40
  CLARE5                                    1899:0 2010:144.30 2011:204.60
  COLUM15                                   1899:0 2009:32.40 2010:81.80 2011:190.90 2012:139.20
  D ST 1                                    1899:0 2011:282.50
  DARTM2                                    1899:0 2010:112.20 2011:175.30
  DORCH1                                    1899:0 2010:36.20 2011:259.80 2012:593.30
  DUDLE1                                    1899:0 2009:16.30 2010:84.30 2012:374.10
  E EIG1                                    1899:0 2011:330.10
  GALLI1                                    1899:0 2011:75.90 2012:71.70
  GENEV1                                    1899:0 2012:268.80
  HYDE 1                                    1899:0 2009:5.20 2010:47.60 2012:332.60

NOTES by INSP_DATE, dollars = RCR
  ASPHALT PATCH                             2009:5.20 2010:62
  BC PATCH                                  2008:7.80 2009:17.60 2010:66.50 2011:8.40 2012:5.10
  BC PATCH AT HYDRANT                       2009:15.60 2010:24.60
  BECC                                      2011:57.50
  COBBLE STONE CURB                         2012:48.10
  CRACKED                                   2010:160.70 2011:28.70
  CRACKING                                  2010:133.20 2011:22.90 2012:5
  City limits                               2011:9 2012:43.80
  DCR                                       1899:0 2011:18.30 2012:12.30
  DCR roadway                               2011:41.10
  DISTORTION                                2010:75.40 2011:19.30
  EMPTY TREE PIT                            2008:5.70 2009:22.50 2010:65.60
  HIP CURB                                  2012:52
  LIP                                       2010:97.80 2011:9.80
  NO CURB                                   2011:15.10 2012:25.60
  NO DAMAGE                                 1899:0 2009:28.60 2010:337.40 2011:573.20 2012:313.80
  NO damage                                 2011:20.20 2012:20.90
  NOT CITY                                  1899:0 2011:35.40 2012:24.70
  NOT City                                  1899:0 2011:20.40 2012:14
  No Sidewalk                               1899:0 2012:16.80
  No damage                                 2008:5 2011:20.20 2012:39.60
  Private                                   1899:0 2010:15 2012:4
  Private way                               1899:0 2008:9.90 2011:28.30
  TREE PIT                                  2010:44.40 2011:3.70
  TREE PITS                                 2009:2.50 2010:15.40 2011:52.50
  private                                   1899:0 2012:5.20

## what

INSP: Mike Haggerty 31%, Serge Lindor 17%, Derek Chan 16%, Kevin Linskey 13%, Danny Moy 7%, John Vozzella 6%, Tan Pham 2%, Brian Forde 2%, Mike Somers 2%, BWT 2%, Marty Lee 1%

MATERIAL: CC 84%, BR 6%, BC 5%, CB 4%, OT 1%, GB 0%, BL 0%, OTHER 0%

CURB_TYPE: Vertical Granite 98%, Asphalt 1%, Sloped Granite 1%, Concrete 0%

AREAWAY: no 99%, yes 1%

UTIL: CITY REPAIR 95%, UNKNOWN 2%, BOSTON WATER & SEWER COMMISSIO 1%, KEYSPAN GAS 1%, COMCAST CABLE 0%, NSTAR GAS 0%, NSTAR ELECTRIC 0%, VERIZON 0%, TRIGEN-BOSTON ENERGY 0%

SURVEY: SURVEYED 89%, MISSING SURVEY 6%, RE-SURVEY 5%

DISTRICT: NORTH DORCHESTER 14%, SOUTH DORCHESTER 12%, WEST ROXBURY 11%, DOWNTOWN 10%, SOUTH BOSTON 8%, HYDE PARK 8%, JAMAICA PLAIN 8%, ROXBURY 10B 6%, EAST BOSTON 6%, ROXBURY 10A 6%, ALLSTON/BRIGHTON 6%, NORTH END 3%

SIDE: RIGHT 51%, LEFT 49%

INSPECTED: yes 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SWK_ID | id | 9.8K | 0 | 9558 50; 9557 50; 9556 50; 9555 50 |
| NEW_INSP_D | date | 252 | 0 | 1/1/1970 0:00:00 1.7K; 12/13/2014 0:00:00 167; 12/8/2014 0:00:00 135; 12/6/2014 0:00:00 128 |
| INSP | category | 30 | 111 | Mike Haggerty 2.9K; Serge Lindor 1.6K; Derek Chan 1.5K; Kevin Linskey 1.2K |
| MATERIAL | category | 9 | 1.4K | CC 7.2K; BR 547; BC 449; CB 305 |
| SWK_WIDTH | amount | 186 | 11 | 6 1.4K; 6.5 1.2K; 7 1.2K; 8 911 |
| SWK_SLOPE | amount | 248 | 9 | 0 429; 2.3 351; 2.2 324; 2.4 319 |
| DAM_LENGTH | other | 558 | 156 | 0 1.2K; 20 847; 10 817; 30 580 |
| DAM_WIDTH | amount | 146 | 27 | 6 1.6K; 6.5 1.3K; 7 908; 0 899 |
| SCI | amount | 1.1K | 211 | 100.0 1.5K; 100 142; 95.5 54; 94.8 52 |
| CURB_TYPE | category | 5 | 815 | Vertical Granite 9.0K; Asphalt 127; Sloped Granite 58; Concrete 43 |
| CURB_REV | amount | 81 | 7 | 6 2.3K; 4 2.1K; 5 1.9K; 0 598 |
| AREAWAY | category | 3 | 7.3K | no 2.7K; yes 14 |
| NOTES | who | 511 | 8.7K | NO DAMAGE 423; CRACKING 29; CRACKED 26; private 21 |
| ADD_NOTE | empty | 1 | 10.0K |  |
| INSP_DATE | date | 242 | 0 | 12/30/1899 0:00:00 1.0K; 2/13/2012 0:00:00 241; 1/9/2012 0:00:00 237; 1/3/2012 0:00:00 227 |
| DAM_AREA | other | 1.4K | 211 | 0 1.6K; 120 230; 60 189; 150 167 |
| RCR | amount | 197 | 0 | 0 1.0K; 6.6 350; 6.5 295; 6.4 215 |
| UTIL | category | 10 | 1.2K | CITY REPAIR 8.4K; UNKNOWN 156; BOSTON WATER & SEWER COMM 118; KEYSPAN GAS 71 |
| SURVEY | category | 3 | 0 | SURVEYED 8.9K; MISSING SURVEY 636; RE-SURVEY 471 |
| DISTRICT | category | 15 | 0 | NORTH DORCHESTER 1.3K; SOUTH DORCHESTER 1.2K; WEST ROXBURY 1.1K; DOWNTOWN 995 |
| SWK_AREA | other | 4.3K | 0 | 1848 51; 1304 51; 1408 51; 1146 50 |
| PARENT | who | 1.9K | 0 | CENTR6 244; DORCH1 176; DUDLE1 104; ADAMS1 89 |
| SNOW_ROUTE | other | 207 | 0 | 7-4-3 160; 6-4-2 148; 3-4-3 138; 1C-7-2 136 |
| SEG_ID | other | 5.8K | 0 | MARIO2_518 51; MARIO1_0 51; MONMO1_0 51; LEXIN2_2119 51 |
| SIDE | category | 2 | 0 | RIGHT 5.1K; LEFT 4.9K |
| ROUTE | empty | 1 | 10.0K |  |
| INSPECTED | category | 2 | 303 | yes 9.7K |
| SHAPE_LENGTH | amount | 10.2K | 0 | 0.000805639661722 50; 0.003412853000063 50; 0.000700070346073 50; 0.001195019499170 50 |
| SHAPE_AREA | amount | 10.1K | 0 | 0.000000011634728 50; 0.000000049185620 50; 0.000000008056017 50; 0.000000005066674 50 |
| SHAPE_WKT | other | 210 | 9.8K | MULTIPOLYGON (((-71.03060 2; MULTIPOLYGON (((-70.99634 2; MULTIPOLYGON (((-71.08697 2; MULTIPOLYGON (((-71.06042 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:44:37.98281 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 581ea693-dbe7-49bf-8f6e-f 10.0K |
| SRC_SHA256 | who | 1 | 0 | 3a3b6c2bb1407a5d3d2ea7c52 10.0K |
