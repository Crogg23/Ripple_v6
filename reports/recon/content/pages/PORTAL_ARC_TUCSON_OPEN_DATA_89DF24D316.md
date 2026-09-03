# PORTAL_ARC_TUCSON_OPEN_DATA_89DF24D316

rows 2.0K  columns 93  scan 4.8s

roles: amount 8, audit 2, category 27, date 3, empty 8, id 15, other 24, who 7

## when

LASTCHANGE
  2005       182  #####################
  2006        29  ###
  2007        48  ######
  2008        30  ####
  2009        28  ###
  2010        33  ####
  2011        45  #####
  2012       158  ###################
  2013        90  ###########
  2014       235  ############################
  2015        92  ###########
  2016       106  ############
  2017       160  ###################
  2018       134  ################
  2019       123  ##############
  2020       154  ##################
  2021       255  ##############################
  2022        98  ############

RECORDDATE
  1963         2  
  1964         1  
  1965         8  ##
  1966         4  #
  1967         6  #
  1968         6  #
  1969        12  ##
  1970         9  ##
  1971         8  ##
  1972         8  ##
  1973        14  ###
  1974         8  ##
  1975         6  #
  1976        12  ##
  1977        20  ####
  1978        17  ###
  1979        15  ###
  1980         7  #
  1981         7  #
  1982         6  #
  1983        12  ##
  1984        13  ###
  1985        11  ##
  1986        20  ####
  1987        13  ###
  1988        24  #####
  1989        26  #####
  1990        31  ######
  1991        21  ####
  1992        38  #######
  1993        32  ######
  1994        37  #######
  1995        26  #####
  1996        37  #######
  1997        24  #####
  1998        24  #####
  1999        40  ########
  2000        41  ########
  2001        40  ########
  2002        42  ########
  2003        50  ##########
  2004        55  ###########
  2005        47  #########
  2006        44  #########
  2007        50  ##########
  2008        32  ######
  2009        32  ######
  2010        37  #######
  2011        50  ##########
  2012        51  ##########
  2013        43  ########
  2014        45  #########
  2015        70  ##############
  2016        82  ################
  2017        80  ################
  2018        88  #################
  2019        89  #################
  2020       116  #######################
  2021       153  ##############################
  2022        36  #######

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 2.0K | 2.2K | 7.3K | 33.7K | 96.5K | 17.54M |
| GISACRES | 2.0K | 0.05 | 0.17 | 0.78 | 2.22 | 402.69 |
| X_HPGN | 2.0K | 983.6K | 992.0K | 995.0K | 995.1K | 1.98B |
| Y_HPGN | 2.0K | 456.2K | 464.2K | 469.0K | 469.2K | 925.60M |
| LANDMEAS | 2.0K | 0.50 | 3.5K | 33.9K | 91.7K | 9.97M |
| SHAPE_LENG | 2.0K | 194.43 | 358.49 | 835.91 | 1.6K | 782.3K |

## who

MAIL3 by rows
      1.7K  TUCSON AZ
        11  ORO VALLEY AZ
         6  AUSTIN TX
         6  CHANDLER AZ
         6  VAIL AZ
         5  MARANA AZ
         5  PHOENIX AZ
         4  SAN JOSE CA
         4  SAN DIEGO CA
         4  PLANO TX
         4  SCOTTSDALE AZ
         3  TEMPE AZ
         3  BROKEN ARROW OK
         3  GREEN VALLEY AZ
         3  2550 W MOORE RD
         2  SAN FRANCISCO CA
         2  AMADO AZ
         2  SEDONA AZ
         2  8372 N MOUNTAIN STONE PINE WAY
         2  LAGUNA BEACH CA

MAIL3 by dollars
      14.54M     1.7K rows  TUCSON AZ
       89.4K       11 rows  ORO VALLEY AZ
       85.5K        1 rows  201 E PASTIME RD
       66.1K        4 rows  SAN JOSE CA
       61.6K        6 rows  VAIL AZ
       59.1K        6 rows  CHANDLER AZ
       51.5K        2 rows  SAHUARITA AZ
       48.3K        3 rows  2550 W MOORE RD
       46.4K        3 rows  BROKEN ARROW OK
       43.9K        6 rows  AUSTIN TX
       37.9K        2 rows  LOS ANGELES CA
       37.9K        5 rows  PHOENIX AZ
       36.7K        1 rows  4338 N 4TH AVE
       36.3K        1 rows  541 W PLACITA DE LA POZA
       36.3K        1 rows  561 E CALLE ARIZONA
       36.1K        2 rows  PO BOX 35337
       34.5K        2 rows  AMADO AZ
       34.0K        5 rows  MARANA AZ
       31.1K        4 rows  PLANO TX
       30.8K        4 rows  SCOTTSDALE AZ

JURIS_OL by rows
      2.0K  TUCSON

JURIS_OL by dollars
      17.54M     2.0K rows  TUCSON

PPT_DESC by rows
      2.0K  Residential              

PPT_DESC by dollars
      17.54M     2.0K rows  Residential              

DATASOURCE by rows
      2.0K  PAREGION

DATASOURCE by dollars
      17.54M     2.0K rows  PAREGION

## who x when

MAIL3 by LASTCHANGE, dollars = GISAREA
  201 E PASTIME RD                          2012:85.5K
  2550 W MOORE RD                           2010:18.5K 2012:29.8K
  4338 N 4TH AVE                            2021:36.7K
  541 W PLACITA DE LA POZA                  2014:36.3K
  561 E CALLE ARIZONA                       2010:36.3K
  8372 N MOUNTAIN STONE PINE WAY            2019:6.4K 2022:6.2K
  AMADO AZ                                  2020:12.0K 2021:22.5K
  AUSTIN TX                                 2017:5.5K 2019:7.4K 2020:6.8K 2021:15.5K 2022:8.8K
  BROKEN ARROW OK                           2021:46.4K
  CHANDLER AZ                               2011:15.8K 2017:25.0K 2019:7.0K 2020:11.2K
  GREEN VALLEY AZ                           2014:8.8K 2020:12.4K
  LAGUNA BEACH CA                           2022:24.1K
  LOS ANGELES CA                            2020:9.6K 2021:28.3K
  MARANA AZ                                 2014:7.5K 2016:6.2K 2019:3.4K 2021:9.4K 2022:7.6K
  ORO VALLEY AZ                             2012:6.7K 2013:5.7K 2014:28.3K 2016:7.1K 2017:8.5K 2019:6.7K 2020:11.2K 2021:15.2K
  PHOENIX AZ                                2014:9.8K 2021:28.0K
  PLANO TX                                  2018:31.1K
  PO BOX 35337                              2013:36.1K
  SAHUARITA AZ                              2019:51.5K
  SAN DIEGO CA                              2017:3.5K 2019:8.7K 2021:5.8K 2022:7.0K
  SAN FRANCISCO CA                          2019:11.3K 2022:6.4K
  SAN JOSE CA                               2015:42.4K 2022:23.7K
  SCOTTSDALE AZ                             2011:7.6K 2013:7.0K 2021:9.3K 2022:6.9K
  SEDONA AZ                                 2017:22.2K
  TEMPE AZ                                  2018:16.7K
  TUCSON AZ                                 2005:1.45M 2006:256.7K 2007:372.1K 2008:264.1K 2009:206.9K 2010:215.9K 2011:359.4K 2012:1.09M 2013:607.6K 2014:1.68M 2015:708.2K 2016:854.4K 2017:1.16M 2018:1.06M 2019:939.9K 2020:1.08M 2021:1.63M 2022:587.2K
  VAIL AZ                                   2006:6.5K 2016:6.0K 2020:6.7K 2021:42.4K

JURIS_OL by LASTCHANGE, dollars = GISAREA
  TUCSON                                    2005:1.55M 2006:281.8K 2007:420.2K 2008:280.4K 2009:241.9K 2010:306.2K 2011:438.6K 2012:1.34M 2013:758.9K 2014:1.97M 2015:825.9K 2016:924.0K 2017:1.39M 2018:1.24M 2019:1.18M 2020:1.29M 2021:2.28M 2022:822.4K

## what

TRS_OL: 131336E 33%, 131326E 28%, 131325E 22%, 131324E 10%, 131322E 5%, 131335E 1%, 131327E 0%

MP_OL: 03115 36%, 12064 9%, 06019 8%, 08061 7%, 13040 7%, 15031 7%, 10059 6%, 13090 5%, 05028 5%, 13085 5%, 12032 4%

SEQ_NUM_S: 20200800562 29%, 20173560657 24%, 20090940486 18%, 20072080368 12%, 20192250579 12%, 20201080814 6%

CURZONE_OL: R-2 52%, R-1 33%, R-3 8%, O-3 5%, C-2 2%, C-1 0%, MH-1 0%, O-1 0%

PARCEL_USE: 0131 68%, 0121 17%, 0325 7%, 0132 2%, 0111 2%, 0335 1%, 0345 1%, 0346 0%, 0122 0%, 0326 0%, 0321 0%, 0141 0%

LANDUNIT: F 50%, S 50%

LEGAL3: SEC 25-13-13 39%, (DISS: 8760/200) 11%, MESA VERDE ADDN .12 AC SEC 35- 6%, E202.27' LOT 9-S 6%, (11085/369 & 398 & 399) 6%, (QC:9343/625) 6%, (11007/1424 & 1426) 6%, (TERM: 9637/2263) 6%, (11211/529 11626/671) 6%, & EXC E148.33' THEREOF EXC S25 6%, (11480/312) 6%

MAIL4: TUCSON AZ 92%, 210 E DOROTHY LN 1%, 13519 EMELITA ST 1%, COLORADO SPRINGS CO 1%, MARANA AZ 1%, MESA AZ 1%, 55 E NARANJA DR 1%, JACKSONVILLE FL 1%, PEARL CITY HI 1%, PO BOX 41041 1%, 3334 N EL BURRITO AVE 1%

MAIL5: TUCSON AZ 68%, VAN NUYS CA 11%, IDYLLWILD CA 5%, CLEVELAND OH 5%, SAN JOSE CA 5%, EL CAJON CA 5%

MP: 03115 34%, 12064 9%, 06019 8%, 08061 7%, 13040 7%, 15031 7%, 10059 6%, 06065 5%, 13090 5%, 05028 4%, 13085 4%, 12032 4%

TAXAREA: 1050 67%, 0851 24%, 1051 9%

TAXYR: 2022 100%

STATE_PROVINCE: AZ 96%, CA 2%, TX 1%, NM 0%, CO 0%, OR 0%, OK 0%, NY 0%, NV 0%, WA 0%, nan 0%, AK 0%

SITE_ZIP: 85705 100%

SITE_ZIPCITY: TUCSON 100%

USE_DESC: SFR GRADE 010-3 URBAN SUBDIVID 68%, SFR GRADE 010-2 URBAN SUBDIVID 17%, DUPLEX - 1 STORY               7%, SFR GRADE 010-3 URBAN NON-SUBD 2%, SFR GRADE 010-1 URBAN SUBDIVID 2%, TRIPLEX - 1 STORY              1%, FOURPLEX - 1 STORY             1%, FOURPLEX - 2 STORY             0%, SFR GRADE 010-2 URBAN NON-SUBD 0%, DUPLEX - 2 STORY               0%, DUPLEX - 2 TO 4 DUPLEX BUILDIN 0%, SFR GRADE 010-4 URBAN SUBDIVID 0%

SPT_DESC: RES SINGLE FAM       90%, RES TWOPLEX          7%, RES TRI/FOURPLEX     3%

ADR_STATUS: ONE 92%, MULTIPLE 7%, NONE 0%

VAN: not_van 100%, van_building_house 0%, van_vacant_lot 0%

FID_L02018_VULNERABILITY_INDEX: 95 31%, 873 28%, 792 18%, 923 8%, 876 5%, 1370 4%, 924 4%, 92 1%

TRACTCE: 001304 31%, 004505 28%, 004511 18%, 002604 8%, 004513 5%, 004510 4%, 002602 4%, 001303 1%

GEOID: 04019001304 31%, 04019004505 28%, 04019004511 18%, 04019002604 8%, 04019004513 5%, 04019004510 4%, 04019002602 4%, 04019001303 1%

NAMELSAD: Census Tract 13.04 31%, Census Tract 45.05 28%, Census Tract 45.11 18%, Census Tract 26.04 8%, Census Tract 45.13 5%, Census Tract 45.10 4%, Census Tract 26.02 4%, Census Tract 13.03 1%

ALAND: 1624379 31%, 1913456 28%, 1613445 18%, 2467686 8%, 1145775 5%, 1842776 4%, 2095779 4%, 967935 1%

INTPTLAT: +32.2558835 31%, +32.2711693 28%, +32.2796583 18%, +32.2691453 8%, +32.2836988 5%, +32.2866046 4%, +32.2692028 4%, +32.2556507 1%

INTPTLON: -110.9708547 31%, -110.9918647 28%, -110.9669487 18%, -110.9766651 8%, -111.0027616 5%, -110.9671622 4%, -110.9582158 4%, -110.9822535 1%

RENTER: Yes 95%, No 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| FID_RESPARCELS_PRE1978_TARGETZI | id | 2.0K | 0 | 2026 10; 2025 10; 2024 10; 2023 10 |
| PARCEL | id | 2.0K | 0 | 107080130 10; 107080120 10; 107080110 10; 107080100 10 |
| GISAREA | amount | 2.0K | 0 | 8797.50029503 11; 6691.05477981 10; 7054.13114055 10; 7413.5933673 10 |
| GISACRES | amount | 2.0K | 0 | 0.20195542 14; 0.15359985 10; 0.16193463 10; 0.17018645 10 |
| X_HPGN | amount | 2.0K | 0 | 988041.815935 10; 988091.110083 10; 988142.940516 10; 988203.918938 10 |
| Y_HPGN | amount | 2.0K | 0 | 458567.175777 10; 458568.084083 10; 458568.218327 10; 458569.310426 10 |
| LON | id | 2.0K | 0 | -110.98486391 10; -110.98470444 10; -110.98453679 10; -110.98433952 10 |
| LAT | id | 2.0K | 0 | 32.2572486 10; 32.25724992 10; 32.25724905 10; 32.2572506 10 |
| LOT_R | other | 138 | 60 | 2 147; 10 130; 1 116; 9 111 |
| LINK | id | 2.0K | 0 | HTTPS://GIS.PIMA.GOV/D.HT 10; HTTPS://GIS.PIMA.GOV/D.HT 10; HTTPS://GIS.PIMA.GOV/D.HT 10; HTTPS://GIS.PIMA.GOV/D.HT 10 |
| TRS_OL | category | 7 | 0 | 131336E 666; 131326E 561; 131325E 438; 131324E 201 |
| MP_OL | category | 40 | 68 | 03115 513; 12064 131; 06019 114; 08061 106 |
| SEQ_NUM_S | category | 7 | 2.0K | 20200800562 5; 20173560657 4; 20090940486 3; 20072080368 2 |
| JURIS_OL | who | 1 | 0 | TUCSON 2.0K |
| CURZONE_OL | category | 8 | 0 | R-2 1.0K; R-1 661; R-3 168; O-3 93 |
| ADDRESS_OL | id | 1.8K | 155 | 809 W GLENN ST 10; 805 W GLENN ST 10; 801 W GLENN ST 10; 757 W GLENN ST 10 |
| SEQ_NUM_D | other | 1.6K | 0 | 0 353; 20210040496 9; 20141150145 9; 20213640508 9 |
| PARCEL_USE | category | 15 | 0 | 0131 1.4K; 0121 341; 0325 134; 0132 38 |
| LANDMEAS | amount | 388 | 0 | 1.0 969; 6000.0 144; 7200.0 77; 9000.0 53 |
| LANDUNIT | category | 2 | 0 | F 1.0K; S 994 |
| LASTCHANGE | date | 1.1K | 0 | 1121151600000 174; 1393916400000 84; 1418022000000 36; 1486969200000 28 |
| LEGAL1 | other | 1.8K | 0 | CORONADO HEIGHTS RESUB OF 55; CORONADO HEIGHTS RESUB BL 14; CORONADO HEIGHTS RESUB OF 12; MIRACLE MILE MANOR W 50'  10 |
| LEGAL2 | other | 504 | 1.3K | F W .24 AC 14; SEC 24-13-13 11; FW .24 AC 10; F W .29 AC 9 |
| LEGAL3 | category | 39 | 2.0K | SEC 25-13-13 7; (DISS: 8760/200) 2; MESA VERDE ADDN .12 AC SE 1; E202.27' LOT 9-S 1 |
| LEGAL4 | empty | 1 | 2.0K |  |
| LEGAL5 | empty | 1 | 2.0K |  |
| LOT | other | 146 | 60 | 00002 147; 00010 128; 00001 116; 00009 111 |
| MAIL1 | id | 1.9K | 0 | HARO ARMANDO 14; VU TUAN QUOC & NHAN THI D 12; KTW PROPERTIES LLC 65% &  11; MILLER-GRAY FAMILY LIVING 11 |
| MAIL2 | other | 1.9K | 2 | 284 E PASTIME RD 14; 5651 N PLACITA ARTURO 12; 5225 E PIMA ST 12; 210 E NAVAJO RD 11 |
| MAIL3 | who | 251 | 0 | TUCSON AZ 1.7K; ORO VALLEY AZ 11; VAIL AZ 6; AUSTIN TX 6 |
| MAIL4 | category | 43 | 1.8K | TUCSON AZ 142; 210 E DOROTHY LN 2; 13519 EMELITA ST 2; COLORADO SPRINGS CO 1 |
| MAIL5 | category | 7 | 2.0K | TUCSON AZ 13; VAN NUYS CA 2; IDYLLWILD CA 1; CLEVELAND OH 1 |
| MP | category | 39 | 39 | 03115 516; 12064 131; 06019 114; 08061 106 |
| PAGE | other | 964 | 0 | 0 901; 2262 7; 330 7; 116 7 |
| RECORDDATE | date | 1.7K | 22 | 20000501 12; 20180330 11; 20180215 11; 20210330 11 |
| DOCKET | other | 1.0K | 1 | 0 900; 11288 8; 11016 7; 12631 7 |
| RECTRACT | empty | 1 | 2.0K |  |
| SECTMODIF | empty | 1 | 2.0K |  |
| TAXAREA | category | 3 | 0 | 1050 1.3K; 0851 481; 1051 179 |
| ZIP | other | 152 | 0 | 85705 1.5K; 85704 46; 85718 43; 85719 35 |
| ZIP4 | other | 825 | 2 | 0000 217; 4117 16; 3132 14; 2563 14 |
| TAXYR | category | 2 | 1 | 2022 2.0K |
| LIMNET | other | 1.6K | 0 | 8555 28; 9700 21; 9995 20; 9135 20 |
| FCV | other | 1.7K | 0 | 116180 24; 125508 23; 117856 21; 131554 19 |
| SHAPE_LENG | amount | 2.0K | 0 | 392.99998652 12; 392.99998651 11; 374.71639164 10; 380.13285263 10 |
| ADDRESSEE | id | 1.9K | 0 | HARO ARMANDO 14; VU TUAN QUOC & NHAN THI D 12; KTW PROPERTIES LLC 65% &  11; HARDING PROPERTIES LLC 11 |
| ADDRESS | other | 1.8K | 0 | 284 E PASTIME RD 14; 5225 E PIMA ST 13; 5651 N PLACITA ARTURO 12; 210 E NAVAJO RD 11 |
| CITY | who | 89 | 0 | TUCSON 1.8K; ORO VALLEY 12; VAIL 7; AUSTIN 7 |
| STATE_PROVINCE | category | 20 | 0 | AZ 1.9K; CA 38; TX 18; NM 5 |
| COUNTRY | empty | 1 | 2.0K |  |
| POSTAL_CODE | other | 881 | 0 | 85705-0000 192; 85705-4117 16; 85705-3132 14; 85705-2563 14 |
| SITE_ADDRESS | id | 2.0K | 0 | nan 12; 809 W GLENN ST 10; 805 W GLENN ST 10; 801 W GLENN ST 10 |
| SITE_ZIP | category | 2 | 7 | 85705 2.0K |
| SITE_ZIPCITY | category | 2 | 7 | TUCSON 2.0K |
| USE_DESC | category | 15 | 0 | SFR GRADE 010-3 URBAN SUB 1.4K; SFR GRADE 010-2 URBAN SUB 341; DUPLEX - 1 STORY          134; SFR GRADE 010-3 URBAN NON 38 |
| SPT_DESC | category | 3 | 0 | RES SINGLE FAM       1.8K; RES TWOPLEX          146; RES TRI/FOURPLEX     63 |
| PPT_DESC | who | 1 | 0 | Residential               2.0K |
| DATASOURCE | who | 1 | 0 | PAREGION 2.0K |
| URL | id | 2.0K | 0 | www.tucsonaz.gov/pro/pdsd 10; www.tucsonaz.gov/pro/pdsd 10; www.tucsonaz.gov/pro/pdsd 10; www.tucsonaz.gov/pro/pdsd 10 |
| URL2 | id | 2.0K | 0 | http://gis.pima.gov/maps/ 10; http://gis.pima.gov/maps/ 10; http://gis.pima.gov/maps/ 10; http://gis.pima.gov/maps/ 10 |
| ADR_STATUS | category | 3 | 0 | ONE 1.8K; MULTIPLE 148; NONE 7 |
| LEGAL_DESC | id | 2.0K | 0 | MIRACLE MILE MANOR W 50'  10; MIRACLE MILE MANOR E25' O 10; MIRACLE MILE MANOR E 50'  10; MIRACLE MILE MANOR W50' L 10 |
| OWN | who | 1 | 0 | Private 2.0K |
| VAN | category | 3 | 0 | not_van 2.0K; van_building_house 1; van_vacant_lot 1 |
| YEARBUILT | empty | 1 | 2.0K |  |
| LAST_EDITED_USER | empty | 1 | 2.0K |  |
| LAST_EDITED_DATE | empty | 1 | 2.0K |  |
| FID_L02018_VULNERABILITY_INDEX | category | 8 | 0 | 95 625; 873 553; 792 364; 923 161 |
| AVG_Z | amount | 8 | 0 | 19.87005747 625; 11.31375831 553; 11.78029093 364; 20.81624637 161 |
| STATEFP | other | 1 | 0 | 04 2.0K |
| COUNTYFP | other | 1 | 0 | 019 2.0K |
| TRACTCE | category | 8 | 0 | 001304 625; 004505 553; 004511 364; 002604 161 |
| GEOID | category | 8 | 0 | 04019001304 625; 04019004505 553; 04019004511 364; 04019002604 161 |
| NAME | amount | 8 | 0 | 13.04 625; 45.05 553; 45.11 364; 26.04 161 |
| NAMELSAD | category | 8 | 0 | Census Tract 13.04 625; Census Tract 45.05 553; Census Tract 45.11 364; Census Tract 26.04 161 |
| MTFCC | other | 1 | 0 | G5020 2.0K |
| FUNCSTAT | other | 1 | 0 | S 2.0K |
| ALAND | category | 8 | 0 | 1624379 625; 1913456 553; 1613445 364; 2467686 161 |
| AWATER | other | 1 | 0 | 0 2.0K |
| INTPTLAT | category | 8 | 0 | +32.2558835 625; +32.2711693 553; +32.2796583 364; +32.2691453 161 |
| INTPTLON | category | 8 | 0 | -110.9708547 625; -110.9918647 553; -110.9669487 364; -110.9766651 161 |
| VULNERABLE | other | 1 | 0 | Yes 2.0K |
| RENTER | category | 2 | 0 | Yes 1.9K; No 107 |
| POC | other | 1 | 0 | Yes 2.0K |
| LOW_INCOME | other | 1 | 0 | Yes 2.0K |
| CHILDREN_IN_POVERTY | other | 1 | 0 | Yes 2.0K |
| COLLEGE_EDUCATED | other | 1 | 0 | Yes 2.0K |
| ORIG_FID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| GEOMETRY | id | 2.0K | 0 | {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:02:28.07791 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 56c447d3-b2f7-4db5-a780-9 2.0K |
| SRC_SHA256 | who | 1 | 0 | 5b25eb84d4834e38c6b1e4a6f 2.0K |
