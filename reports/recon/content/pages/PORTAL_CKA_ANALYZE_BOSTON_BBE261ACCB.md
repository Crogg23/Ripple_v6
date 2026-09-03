# PORTAL_CKA_ANALYZE_BOSTON_BBE261ACCB

rows 10.0K  columns 31  scan 7.3s

roles: amount 5, audit 2, category 10, date 4, empty 1, id 2, other 6, who 2

## when

PLACEMENT1
  2007      9.2K  ##############################
  2008       102  
  2009       299  #
  2010        61  
  2011        82  
  2012        25  
  2013        42  
  2014        41  
  2015        81  
  2016        17  

UPDATE_DAT
  2008      1.3K  ######
  2009      6.8K  ##############################
  2010       849  ####
  2011       135  #
  2012        85  
  2013       102  
  2014       215  #
  2015       254  #
  2016       281  #

INSTALL_DA
  1891         1  
  1899         3  
  1900         1  
  1901         1  
  1903         1  
  1911         1  
  1920         1  
  1922         1  
  1927         2  
  1929         1  
  1930         1  
  1932         1  
  1937         1  
  1938         1  
  1941         1  
  1950         3  
  1958         2  
  1959         3  
  1960         2  
  1961         1  
  1963         2  
  1964         3  
  1966         1  
  1967         2  
  1968         1  
  1969         1  
  1970         4  
  1971         1  
  1972         6  #
  1973         6  #
  1974         9  #
  1975         6  #
  1976         9  #
  1977         4  
  1978         5  #
  1979         3  
  1980        25  ###
  1981        14  ##
  1982        24  ###
  1983        15  ##
  1984        21  ##
  1985        22  ###
  1986        14  ##
  1987        36  ####
  1988        32  ####
  1989        49  ######
  1990        68  ########
  1991        84  ##########
  1992       128  ###############
  1993       127  ###############
  1994       125  ##############
  1995        86  ##########
  1996        30  ###
  1997       146  #################
  1998       161  ###################
  1999        89  ##########
  2000       164  ###################
  2001       151  #################
  2002       149  #################
  2003       259  ##############################
  2004       222  ##########################
  2005       162  ###################
  2006       189  ######################
  2007       179  #####################
  2008       135  ################
  2009       159  ##################
  2010        80  #########
  2011        61  #######
  2012        52  ######
  2013        65  ########
  2014        53  ######
  2015        17  ##

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SYMBOL_ROT | 10.0K | 0 | 73 | 358 | 360 | 1.19M |
| LONGITUDE | 10.0K | 742.9K | 768.2K | 789.0K | 792.6K | 7.67B |
| LATITUDE | 10.0K | 2.91M | 2.94M | 2.97M | 2.97M | 29.41B |
| POINT_X | 10.0K | -71.18 | -71.09 | -71.01 | -70.99 | -710.9K |
| POINT_Y | 10.0K | 42.23 | 42.32 | 42.39 | 42.39 | 423.2K |

## who

FACILITY_I by rows
         1  28MH84
         1  23CH102
         1  20KH135
         1  20LH72
         1  30PH4
         1  24KH259
         1  13LH74
         1  25KH3
         1  23LH693
         1  15IH148
         1  9JH128
         1  21JH52
         1  20IH158
         1  27KH252
         1  18KH72
         1  22MH128
         1  14KH20
         1  29OH92
         1  21IH153
         1  14JH178

FACILITY_I by dollars
         360        1 rows  10GH16
         360        1 rows  4FH38
         360        1 rows  8HH165
         360        1 rows  7CH50
         360        1 rows  8HH136
         360        1 rows  16KH156
         360        1 rows  9DH56
         360        1 rows  8FH84
         360        1 rows  21CH20
         360        1 rows  29JH121
         360        1 rows  20NH32
         360        1 rows  9HH72
         360        1 rows  9HH60
      359.91        1 rows  13GH104
      359.90        1 rows  17KH46
      359.90        1 rows  17KH164
      359.90        1 rows  17KH76
      359.90        1 rows  17KH4
      359.90        1 rows  17KH70
      359.90        1 rows  17KH216

SRC_SHA256 by rows
     10.0K  f7451b5522d22ec18e0a2e5506a5e1e3b1a38cc7def201a04f13e5f67915c0c3

SRC_SHA256 by dollars
       1.19M    10.0K rows  f7451b5522d22ec18e0a2e5506a5e1e3b1a38cc7def201a04f13e5f67915

## who x when

FACILITY_I by INSTALL_DA, dollars = SYMBOL_ROT
  14JH178                                   1994:296
  14KH20                                    2004:183.21
  15IH148                                   2007:0
  27KH252                                   2014:215
  28MH84                                    1992:0
  4FH38                                     2006:360
  8HH136                                    1996:360
  9JH128                                    2006:0

SRC_SHA256 by INSTALL_DA, dollars = SYMBOL_ROT
  f7451b5522d22ec18e0a2e5506a5e1e3b1a38cc7  1891:249 1899:311 1900:283 1901:0 1903:249 1911:258.22 1920:321.17 1922:236 1927:442 1929:0 1930:220 1932:0 1937:10 1938:0 1941:53 1950:487 1958:0 1959:476 1960:569.40 1961:0 1963:716 1964:0 1966:184 1967:36 1968:32.91 1969:0 1970:252 1971:182.10 1972:468 1973:850.90 1974:1.7K 1975:1.1K 1976:662 1977:221 1978:472 1979:213 1980:2.6K 1981:1.5K 1982:3.6K 1983:1.7K 1984:3.7K 1985:1.4K 1986:1.4K 1987:3.5K 1988:3.9K 1989:3.5K 1990:8.8K 1991:9.8K 1992:14.9K 1993:16.0K 1994:16.2K 1995:10.2K 1996:4.0K 1997:16.8K 1998:18.7K 1999:8.2K 2000:18.2K 2001:16.0K 2002:16.6K 2003:26.6K 2004:32.2K 2005:24.6K 2006:28.4K 2007:24.8K 2008:17.0K 2009:24.3K 2010:13.9K 2011:8.2K 2012:7.9K 2013:9.8K 2014:8.8K 2015:3.0K

## what

PLACEMENT: MIGRATED 92%, mulline 2%, blundonr 2%, denapolipd 1%, chalmersh 1%, BlundoNR 1%, connorsm 0%, digiornom 0%, dorleansr 0%, palaciolv 0%, samayoa-galvisr 0%, obrienm 0%

UPDATE_ID: blundonr 48%, chalmersh 14%, connorsm 9%, denapolipd 9%, palaciolv 7%, mulline 6%, dorleansr 2%, BlundoNR 1%, chings 1%, pullenn 1%, hoffmanr 1%, digiornom 1%

SYNCH_FLAG: U 100%

SUBTYPE_CO: 1 99%, 2 0%, 3 0%

SERVICE_AR: SH 54%, SL 26%, NL 10%, SEH 8%, HPFS 1%, U 1%, NH 0%

HYDRANT_MA: MU 42%, KE 33%, US 7%, DA 6%, U 5%, MH 3%, WA 2%, SM 1%, LO 0%, AM 0%, PO 0%, BF 0%

OWNER_CODE: BWSC 91%, PRIV 8%, U 0%

METERED_FL: U 100%, N 0%

LOC_SOURCE: MANUAL 68%, GIS 16%, U 8%, GPS 6%, AS BUILT 1%

HYDRANT_MO: MUCENT 41%, KEK81-A 30%, U 8%, ADB-84-B 5%, USMET250 4%, WAWB67P 2%, USSEN 2%, MH929 2%, KEK81 2%, ADB-62-B 1%, MH129 1%, KEK11 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | empty | 1 | 10.0K |  |
| ANCILLARYR | other | 1 | 0 | 0 10.0K |
| ENABLED | other | 1 | 0 | 1 10.0K |
| FEATURE_ID | id | 10.0K | 0 | 1203740092 50; 2207740012 50; 2211740243 50; 2612740105 50 |
| PLACEMENT | category | 18 | 0 | MIGRATED 9.2K; mulline 200; blundonr 181; denapolipd 106 |
| PLACEMENT1 | date | 381 | 0 | 2007-04-27T00:00:00 9.2K; 2009-07-15T00:00:00 85; 2009-04-21T00:00:00 50; 2009-07-16T00:00:00 43 |
| UPDATE_ID | category | 25 | 3 | blundonr 4.7K; chalmersh 1.4K; connorsm 905; denapolipd 839 |
| UPDATE_DAT | date | 699 | 3 | 2009-10-14T00:00:00 2.8K; 2009-06-09T00:00:00 483; 2009-01-14T00:00:00 314; 2010-08-25T00:00:00 258 |
| SYNCH_FLAG | category | 2 | 1.6K | U 8.4K |
| SYMBOL_ROT | amount | 1.2K | 0 | 0.0 3.7K; 180.0 41; 230.0 39; 318.0 38 |
| FACILITY_I | who | 10.1K | 0 | 12CH16 50; 22GH16 50; 22KH771 50; 26LH69 50 |
| SUBTYPE_CO | category | 3 | 0 | 1 9.9K; 2 41; 3 31 |
| SERVICE_AR | category | 7 | 0 | SH 5.4K; SL 2.6K; NL 1.0K; SEH 834 |
| INSTALL_DA | date | 998 | 0 | 9999-01-01T00:00:00 6.5K; 2004-06-01T00:00:00 81; 1993-01-01T00:00:00 76; 1994-01-01T00:00:00 74 |
| HYDRANT_MA | category | 17 | 0 | MU 4.2K; KE 3.3K; US 683; DA 608 |
| OWNER_CODE | category | 3 | 0 | BWSC 9.1K; PRIV 850; U 7 |
| METERED_FL | category | 2 | 0 | U 10.0K; N 9 |
| ADDRESS_NU | other | 2.3K | 1.4K | 15 124; 11 102; 19 89; 12 81 |
| STREET_FEA | other | 3.1K | 0 | 0 92; 1090 78; 567 58; 882 58 |
| CROSS_STRE | other | 3.3K | 0 | 0 587; 2032 51; 801 51; 84 49 |
| LOC_SOURCE | category | 6 | 3 | MANUAL 6.8K; GIS 1.6K; U 835; GPS 635 |
| MANUFACTUR | other | 65 | 0 | 1994 906; 1992 791; -999 769; 1995 645 |
| HYDRANT_MO | category | 23 | 3 | MUCENT 4.1K; KEK81-A 3.0K; U 792; ADB-84-B 517 |
| LONGITUDE | amount | 10.0K | 0 | 746110.096948 50; 762602.631877 50; 775696.196569 50; 779798.435083 50 |
| LATITUDE | amount | 10.1K | 0 | 2931357.00795 50; 2951862.71628 50; 2950772.68894 50; 2959797.4678 50 |
| SHAPE_WKT | id | 10.1K | 0 | POINT (-71.16757342699997 50; POINT (-71.10626877299995 50; POINT (-71.05785437399998 50; POINT (-71.04250122299998 50 |
| POINT_X | amount | 9.8K | 0 | -71.16757342699998 50; -71.10626877299995 50; -71.05785437399999 50; -71.04250122299999 50 |
| POINT_Y | amount | 9.9K | 0 | 42.291311918000076 50; 42.34738802500004 50; 42.34422090900006 50; 42.368925697000066 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:28:30.48054 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3a83cb5c-feef-4fd0-a7ae-2 10.0K |
| SRC_SHA256 | who | 1 | 0 | f7451b5522d22ec18e0a2e550 10.0K |
