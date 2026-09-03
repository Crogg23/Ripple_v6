# FED_EPA_CAMPD_FACILITY

rows 128.5K  columns 34  scan 4.9s

roles: amount 2, audit 2, category 9, date 2, other 7, state 1, who 12

## errors
  _INGESTED_AT: 100039 (22003): Numeric value '56662972' is out of range

## when

COMMERCIAL_OPERATION_DATE
  1917        20  
  1919         3  
  1921        11  
  1924        17  
  1926         3  
  1928        59  
  1929        20  
  1930       179  #
  1931        27  
  1932        52  
  1935        34  
  1937         6  
  1938       140  
  1939        35  
  1940       236  #
  1941       229  #
  1942       188  #
  1943       329  #
  1944       172  #
  1945       131  
  1946        23  
  1947       374  #
  1948       984  ###
  1949      1.1K  ###
  1950      1.1K  ###
  1951      1.3K  ####
  1952      1.3K  ####
  1953      1.5K  ####
  1954      2.2K  #######
  1955      1.8K  #####
  1956      1.0K  ###
  1957      1.2K  ####
  1958      2.4K  #######
  1959      1.6K  #####
  1960      1.5K  ####
  1961       964  ###
  1962      1.1K  ###
  1963      1.2K  ###
  1964      1.2K  ####
  1965      1.4K  ####
  1966      1.1K  ###
  1967      1.5K  ####
  1968      2.1K  ######
  1969      2.1K  ######
  1970      4.0K  ############
  1971      3.7K  ###########
  1972      3.8K  ###########
  1973      2.3K  #######
  1974      3.5K  ##########
  1975      1.5K  #####
  1976      1.3K  ####
  1977      1.4K  ####
  1978      1.5K  ####
  1979       942  ###
  1980      1.3K  ####
  1981       891  ###
  1982      1.0K  ###
  1983       413  #
  1984       753  ##
  1985       741  ##
  1986       398  #
  1987       744  ##
  1988       774  ##
  1989       754  ##
  1990      1.6K  #####
  1991      1.6K  #####
  1992      2.0K  ######
  1993      1.4K  ####
  1994      1.8K  #####
  1995      2.3K  #######
  1996      1.3K  ####
  1997       658  ##
  1998       528  ##
  1999      2.1K  ######
  2000      5.8K  #################
  2001     10.2K  ##############################
  2002      9.3K  ###########################
  2003      5.6K  ################
  2004      1.7K  #####
  2005      2.1K  ######
  2006       812  ##
  2007      1.2K  ####
  2008      1.6K  #####
  2009      1.4K  ####
  2010       989  ###
  2011       851  ###
  2012       934  ###
  2013       674  ##
  2014       302  #
  2015       418  #
  2016       441  #
  2017       433  #
  2018       397  #
  2019       228  #
  2020       101  
  2021       219  #
  2022       120  
  2023        82  
  2024        38  
  2025        26  

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 128.4K | 17.95 | 38.54 | 46.75 | 63.85 | 4.80M |
| LONGITUDE | 128.4K | -158.13 | -86.24 | -71.03 | -66.10 | -11.36M |

## who

FACILITY_NAME by rows
       848  Gowanus Generating Station
       764  Astoria Gas Turbine Power
       730  Johnsonville
       552  Ravenswood Generating Station
       540  Holtsville Facility
       498  Lincoln Combustion Turbine
       489  E F Barrett
       474  Clark
       432  Narrows Generating Station
       384  Midland Cogeneration Venture
       371  Lauderdale
       348  Fort Myers
       337  Intercession City
       337  Greene County
       336  Delaware City Refinery
       331  Lagoon Creek
       320  Gallatin
       311  Colbert
       309  Burlington Generating Station
       305  Chalk Point

FACILITY_NAME by dollars
       34.5K      848 rows  Gowanus Generating Station
       31.2K      764 rows  Astoria Gas Turbine Power
       26.3K      730 rows  Johnsonville
       22.5K      552 rows  Ravenswood Generating Station
       22.0K      540 rows  Holtsville Facility
       19.9K      489 rows  E F Barrett
       17.6K      498 rows  Lincoln Combustion Turbine
       17.6K      432 rows  Narrows Generating Station
       17.1K      474 rows  Clark
       16.7K      384 rows  Midland Cogeneration Venture
       13.3K      336 rows  Delaware City Refinery
       12.5K      303 rows  Devon
       12.4K      300 rows  University Park Energy
       12.4K      309 rows  Burlington Generating Station
       11.9K      288 rows  LSP University Park, LLC
       11.8K      331 rows  Lagoon Creek
       11.8K      305 rows  Chalk Point
       11.6K      320 rows  Gallatin
       11.5K      300 rows  Big Sandy Peaker Plant
       11.3K      278 rows  Astoria Generating Station

ASSOCIATED_GENERATORS_NAMEPLATE_CAPACITY_MWE by rows
       390  1 (75)
       309  1 (50)
       270  3 (75)
       242  2 (75)
       223  1 (69)
       216  GEN1 (54.2)
       210  5 (100)
       198  2 (100)
       191  3 (50)
       174  1 (44)
       160  1 (100)
       159  GEN2 (54.2)
       153  2 (125)
       152  2 (163.2)
       152  1 (136)
       150  6 (50)
       148  1 (26.6)
       145  2 (69)
       143  5 (50)
       142  1 (163.2)

ASSOCIATED_GENERATORS_NAMEPLATE_CAPACITY_MWE by dollars
       13.8K      390 rows  1 (75)
       11.6K      309 rows  1 (50)
        9.9K      270 rows  3 (75)
        9.2K      242 rows  2 (75)
        8.5K      223 rows  1 (69)
        7.8K      216 rows  GEN1 (54.2)
        7.7K      198 rows  2 (100)
        7.6K      210 rows  5 (100)
        7.3K      191 rows  3 (50)
        6.4K      174 rows  1 (44)
        6.2K      160 rows  1 (100)
        5.9K      152 rows  1 (136)
        5.9K      150 rows  6 (50)
        5.9K      143 rows  5 (50)
        5.7K      152 rows  2 (163.2)
        5.7K      159 rows  GEN2 (54.2)
        5.7K      141 rows  1 (47)
        5.6K      148 rows  1 (26.6)
        5.5K      141 rows  3 (80)
        5.4K      153 rows  2 (125)

OWNER_OPERATOR by rows
      2.9K  Tennessee Valley Authority (Owner)|Tennessee Valley Authority (Operato
      1.9K  Florida Power & Light Company (Owner)|Florida Power & Light Company (O
      1.3K  Entergy Corporation (Owner)|Entergy Corporation (Operator)
      1.3K  Virginia Electric & Power Company (Owner)|Dominion Generation (Operato
      1.3K  Union Electric Company (Owner)|Union Electric Company (Operator)
      1.2K  Astoria Generating Company, LP (Owner)|Astoria Operating Services, Inc
      1.1K  Georgia Power Company (Owner)|Georgia Power Company (Operator)
      1.0K  Duke Energy Corporation (Owner/Operator)|Duke Energy Corporation (Owne
       841  National Grid Generation LLC (Owner)|National Grid Generation LLC (Ope
       702  Duke Energy Corporation (Owner)|Duke Energy Corporation (Operator)
       697  NV Energy (Owner)|NV Energy (Operator)
       688  Wisconsin Electric Power Company (Owner)|Wisconsin Electric Power Comp
       676  Detroit Edison Company (Owner)|Detroit Edison Company (Operator)
       674  NRG Energy, Inc (Owner)|NRG Energy, Inc (Operator)
       674  Alabama Power Company (Owner)|Alabama Power Company (Operator)
       627  Northern States Power (Xcel Energy) (Owner)|Northern States Power (Xce
       577  Tampa Electric Company (Owner)|Tampa Electric Company (Operator)
       553  Exelon Generation Company LLC (Owner)|Exelon Generation Company LLC (O
       546  Los Angeles Department of Water and Power (Owner)|Los Angeles Departme
       540  KeySpan Corporation (Owner/Operator)|KeySpan Corporation (Owner/Operat

OWNER_OPERATOR by dollars
      102.3K     2.9K rows  Tennessee Valley Authority (Owner)|Tennessee Valley Authorit
       50.4K     1.9K rows  Florida Power & Light Company (Owner)|Florida Power & Light 
       50.4K     1.2K rows  Astoria Generating Company, LP (Owner)|Astoria Operating Ser
       49.7K     1.3K rows  Union Electric Company (Owner)|Union Electric Company (Opera
       48.5K     1.3K rows  Virginia Electric & Power Company (Owner)|Dominion Generatio
       41.2K     1.3K rows  Entergy Corporation (Owner)|Entergy Corporation (Operator)
       38.0K     1.0K rows  Duke Energy Corporation (Owner/Operator)|Duke Energy Corpora
       37.3K     1.1K rows  Georgia Power Company (Owner)|Georgia Power Company (Operato
       34.3K      841 rows  National Grid Generation LLC (Owner)|National Grid Generatio
       29.9K      688 rows  Wisconsin Electric Power Company (Owner)|Wisconsin Electric 
       28.8K      676 rows  Detroit Edison Company (Owner)|Detroit Edison Company (Opera
       28.1K      627 rows  Northern States Power (Xcel Energy) (Owner)|Northern States 
       25.5K      702 rows  Duke Energy Corporation (Owner)|Duke Energy Corporation (Ope
       25.2K      697 rows  NV Energy (Owner)|NV Energy (Operator)
       22.5K      553 rows  Exelon Generation Company LLC (Owner)|Exelon Generation Comp
       22.0K      540 rows  KeySpan Corporation (Owner/Operator)|KeySpan Corporation (Ow
       21.8K      674 rows  Alabama Power Company (Owner)|Alabama Power Company (Operato
       21.7K      533 rows  Astoria Energy, LLC (Owner)|Astoria Energy, LLC (Operator)
       20.7K      509 rows  PSEG (Owner/Operator)|PSEG (Owner/Operator)
       20.5K      674 rows  NRG Energy, Inc (Owner)|NRG Energy, Inc (Operator)

OPERATING_STATUS by rows
    121.3K  Operating
      2.9K  Retired
       337  Long-term Cold Storage
       130  Future
        45  Cancelled
        41  Operating (Retired 06/30/2015)
        27  Operating (Retired 05/01/2023)
        23  Operating (Retired 09/30/2012)
        20  Operating (Started 07/01/2002)
        20  Retired (Retired 01/01/2003)
        18  Operating (Started 06/01/2001)
        17  Operating (Retired 04/15/2016)
        17  Operating (Retired 05/31/2015)
        15  Operating (Retired 06/01/2018)
        15  Operating (Retired 03/31/2013)
        15  Operating (Retired 06/01/2023)
        15  Operating (Retired 06/01/2020)
        14  Operating (Retired 06/01/2017)
        14  Operating (Started 06/01/2002)
        12  Operating (Retired 04/16/2015)

OPERATING_STATUS by dollars
       4.53M   121.3K rows  Operating
      107.2K     2.9K rows  Retired
       12.7K      337 rows  Long-term Cold Storage
        3.2K      130 rows  Future
        1.7K       41 rows  Operating (Retired 06/30/2015)
        1.3K       45 rows  Cancelled
        1.1K       27 rows  Operating (Retired 05/01/2023)
      833.25       23 rows  Operating (Retired 09/30/2012)
      787.91       20 rows  Operating (Started 07/01/2002)
      713.14       18 rows  Operating (Started 06/01/2001)
      712.20       20 rows  Retired (Retired 01/01/2003)
      687.02       17 rows  Operating (Retired 04/15/2016)
      662.16       17 rows  Operating (Retired 05/31/2015)
      630.11       15 rows  Operating (Retired 06/01/2023)
      603.66       15 rows  Operating (Retired 06/01/2020)
      578.67       14 rows  Operating (Retired 06/01/2017)
      572.76       15 rows  Operating (Retired 03/31/2013)
      566.54       15 rows  Operating (Retired 06/01/2018)
      519.68       14 rows  Operating (Started 06/01/2002)
      480.95       12 rows  Operating (Retired 04/16/2015)

## who x when

FACILITY_NAME by COMMERCIAL_OPERATION_DATE, dollars = LATITUDE
  Astoria Gas Turbine Power                 1970:27.6K 1971:3.6K
  Astoria Generating Station                1953:1.3K 1958:5.8K 1962:3.1K 1967:1.1K
  Big Sandy Peaker Plant                    2001:11.5K
  Burlington Generating Station             1955:480.96 1967:681.36 1972:5.3K 1993:1.8K 2000:4.2K
  Chalk Point                               1964:1.0K 1965:1.0K 1967:192.70 1974:1.1K 1975:1.2K 1981:1.2K 1990:1.1K 1991:4.8K
  Clark                                     1955:433.08 1957:433.08 1961:433.08 2008:15.6K
  Colbert                                   1954:764.28 1955:2.3K 1965:764.28 1972:6.7K 2023:312.66
  Delaware City Refinery                    1956:4.5K 1960:1.9K 1961:1.1K 1972:1.1K 1983:1.5K 1996:1.1K 2000:2.1K
  Devon                                     1942:906.62 1947:906.62 1949:453.31 1951:453.31 1955:535.73 1957:535.73 1985:1.1K 1996:4.9K 2010:2.6K
  E F Barrett                               1956:1.3K 1963:1.3K 1970:17.3K
  Fort Myers                                1958:320.40 1969:320.40 1974:2.9K 2000:1.4K 2001:2.7K 2003:1.2K 2016:480.60
  Gallatin                                  1956:1.1K 1957:1.1K 1959:2.3K 1975:3.3K 2000:3.8K
  Gowanus Generating Station                1971:34.5K
  Greene County                             1965:1.0K 1966:1.0K 1995:5.1K 1996:3.9K
  Holtsville Facility                       1974:22.0K
  Intercession City                         1974:3.1K 1993:3.5K 1996:847.80 2000:2.1K
  Johnsonville                              1951:1.7K 1952:2.5K 1953:828.69 1958:828.69 1959:2.5K 1974:13.3K 2000:3.7K 2017:648.54 2024:144.12 2025:216.18
  LSP University Park, LLC                  2002:11.9K
  Lagoon Creek                              2001:7.1K 2002:3.5K 2010:1.1K
  Lauderdale                                1957:78.21 1958:78.21 1970:2.8K 1972:2.8K 1993:2.5K 2016:1.2K 2022:208.56
  Lincoln Combustion Turbine                1995:13.2K 1996:4.3K 2020:212.58
  Midland Cogeneration Venture              1990:12.0K 2008:3.1K 2009:1.6K
  Narrows Generating Station                1972:17.6K
  Ravenswood Generating Station             1963:2.5K 1965:1.3K 1967:1.1K 1970:15.0K 2004:896.72
  University Park Energy                    2001:12.4K

ASSOCIATED_GENERATORS_NAMEPLATE_CAPACITY_MWE by COMMERCIAL_OPERATION_DATE, dollars = LATITUDE
  1 (100)                                   1952:2.5K 1954:411 1959:897.12 1960:363 1965:2.1K
  1 (136)                                   1960:852.60 1962:1.4K 1968:2.7K 1970:1.0K
  1 (163.2)                                 1956:844.25 1958:1.9K 1960:1.4K 1964:982.80
  1 (26.6)                                  1943:567.12 1963:460.32 1971:2.2K 1973:2.5K
  1 (44)                                    1948:850.98 1949:472.56 1950:476.04 1964:1.1K 1965:737.44 2002:1.7K 2003:1.1K
  1 (47)                                    1993:715.87 1999:1.1K 2000:1.0K 2001:2.0K 2005:814.80
  1 (50)                                    1940:1.3K 1941:1.3K 1949:1.2K 1952:655.41 1954:698.04 1955:433.08 1957:1.1K 1958:1.3K 1984:1.4K 1991:1 1995:876.68 2006:679.20 2011:507.90 2017:283.95
  1 (69)                                    1943:486.84 1948:1.1K 1949:952.28 1951:2.5K 1952:908.27 1954:457.05 1977:2.1K
  1 (75)                                    1951:806.20 1952:1.3K 1953:1.5K 1954:1.7K 1957:1.7K 1958:1.8K 1962:1.6K 1967:1.0K 1971:730.80 1972:922.56 2003:735.54
  2 (100)                                   1952:919.38 1953:1.5K 1954:376.75 1961:897.12 1963:363 1966:1.2K 1972:1.0K 1995:1.4K
  2 (125)                                   1951:828.69 1954:2.1K 1955:1.0K 1958:334.92 1968:1.1K
  2 (163.2)                                 1957:844.25 1959:1.9K 1960:1.2K 1963:780.33 1964:982.25
  2 (69)                                    1948:266.16 1949:2.3K 1951:720.96 1952:2.2K
  2 (75)                                    1950:458.22 1951:1.4K 1953:975.75 1954:468.16 1956:334.20 1957:433.08 1960:3.1K 1963:1.3K 2003:735.54
  3 (50)                                    1942:584.09 1951:868.78 1953:374.22 1954:212.24 1957:590.40 1958:1.3K 1959:659.20 1961:1.2K 2010:491.52 2011:1.0K
  3 (75)                                    1949:850.98 1953:2.8K 1954:2.0K 1956:668.36 1961:433.08 1962:1.1K 1964:1.2K 2003:735.54
  3 (80)                                    1940:608.44 1941:1.2K 1948:520.56 1953:596.26 1954:634.27 1955:819.21 1957:833.36 2002:244.86
  5 (100)                                   1944:1.6K 1949:1.1K 1952:671.84 1954:734.94 1960:1.0K 1994:1.0K 2008:496.26 2010:708.64 2019:294.98
  5 (50)                                    1917:842.80 1949:935.34 1955:1.3K 1962:854.04 2001:952.75 2002:972.24
  6 (50)                                    1957:3.7K 1958:719.10 2001:952.75 2010:607.65
  GEN1 (54.2)                               1987:5.9K 1988:1.9K
  GEN2 (54.2)                               1987:3.8K 1988:1.9K

## where

STATE: TX 11.0K, NY 9.3K, FL 7.1K, IL 6.9K, CA 6.7K, PA 6.0K, OH 5.0K, IN 4.7K, NJ 4.2K, NC 4.2K, MI 4.1K, GA 4.0K

## what

YEAR: 2008 9%, 2012 8%, 2009 8%, 2011 8%, 2004 8%, 2010 8%, 2013 8%, 2006 8%, 2005 8%, 2015 8%, 2014 8%, 2003 8%

EPA_REGION: 4 22%, 5 20%, 6 14%, 3 11%, 2 11%, 9 8%, 7 6%, 1 4%, 8 4%, 10 1%

NERC_REGION: SERC 21%, ECAR 15%, WECC 12%, NPCC 10%, SPP 10%, ERCOT 9%, MAPP 7%, MAIN 6%, MAAC 6%, FRCC 4%, ASCC 0%

SOURCE_CATEGORY: Electric Utility 88%, Cogeneration 6%, Industrial Boiler 3%, Petroleum Refinery 1%, Pulp & Paper Mill 1%, Iron & Steel 0%, Small Power Producer 0%, Industrial Turbine 0%, Institutional 0%, Municipal Waste Combustor 0%, Cement Manufacturing 0%, Bulk Industrial Chemical 0%

SO2_PHASE: Phase 2 92%, Table 1 7%, Substitution 1%, Opt-In 0%, Compensating 0%

NOX_PHASE: Early Election 30%, Phase 2 Group 1 28%, Phase 1 Group 1 28%, Phase 2 Group 2 13%

PRIMARY_FUEL_TYPE: Pipeline Natural Gas 59%, Coal 24%, Diesel Oil 8%, Residual Oil 3%, Natural Gas 2%, Process Gas 2%, Other Oil 1%, Other Gas 0%, Wood 0%, Coal Refuse 0%, Petroleum Coke 0%, Natural Gas, Pipeline Natural  0%

_SRC_SHA256: c5940e45aec4fa855b6f76997994b0 9%, e25c07183bcddfc262d0563d77b38c 8%, 8f49fb1b8d02a1f3ff8059e765fb36 8%, ae86981964e289de1282847d947adb 8%, d16ed114e801fce70774c979e55e1c 8%, faaeb320ce22de20a75fb9afddde5d 8%, d7e42f37665df4ef6355751ac28edf 8%, c2688fd99d6355dc0fb326b2fc5fcc 8%, 4effbfeaf711f68f775dd970c669f2 8%, aa23d42cde7e67c5163047b1c20a6f 8%, 7cf5d0bea566353c37e6d1024ff2bb 8%, ce8f9d2ac2851ad8090576bfc6b26d 8%

_SRC_FILE: facility-2008.csv 9%, facility-2012.csv 8%, facility-2009.csv 8%, facility-2011.csv 8%, facility-2004.csv 8%, facility-2010.csv 8%, facility-2013.csv 8%, facility-2006.csv 8%, facility-2005.csv 8%, facility-2015.csv 8%, facility-2014.csv 8%, facility-2003.csv 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATE | state | 52 | 0 | TX 11.0K; NY 9.3K; FL 7.1K; IL 6.9K |
| FACILITY_NAME | who | 1.9K | 0 | Gowanus Generating Statio 909; Astoria Gas Turbine Power 845; Johnsonville 779; Holtsville Facility 683 |
| FACILITY_ID | who | 2.0K | 0 | 2494 909; 55243 845; 3406 779; 8007 683 |
| UNIT_ID | other | 2.0K | 0 | 1 14.7K; 2 12.3K; 3 8.4K; 4 6.0K |
| ASSOCIATED_STACKS | other | 307 | 107.8K | CS0001 1.4K; CS1 1.4K; CP1 1.4K; CP0001 1.3K |
| YEAR | category | 31 | 0 | 2008 5.0K; 2012 4.9K; 2009 4.9K; 2011 4.9K |
| PROGRAM_CODE | other | 129 | 3.9K | ARP 40.0K; ARP, CAIRNOX, CAIROS, CAI 11.5K; ARP, NBP 7.9K; NBP 5.0K |
| PRIMARY_REP_INFO | other | 8.8K | 647 | 1 2.3K; 601740 1.3K; 606322 1.1K; 86 967 |
| EPA_REGION | category | 10 | 0 | 4 28.4K; 5 25.3K; 6 17.9K; 3 14.2K |
| NERC_REGION | category | 11 | 63.8K | SERC 13.4K; ECAR 9.5K; WECC 7.9K; NPCC 6.7K |
| COUNTY | who | 717 | 90 | Queens County 2.0K; Washington County 1.7K; Kings County 1.7K; Los Angeles County 1.7K |
| COUNTY_CODE | other | 917 | 90 | NY081 2.0K; CA037 1.7K; NY047 1.6K; TX201 1.5K |
| FIPS_CODE | other | 165 | 90 | 003 3.8K; 017 3.4K; 013 3.2K; 001 3.0K |
| SOURCE_CATEGORY | category | 12 | 215 | Electric Utility 112.5K; Cogeneration 8.2K; Industrial Boiler 3.9K; Petroleum Refinery 1.2K |
| LATITUDE | amount | 1.9K | 134 | 40.6635 909; 40.7864 845; 36.0278 778; 40.8153 689 |
| LONGITUDE | amount | 1.9K | 134 | -74.0051 909; -73.9133 845; -87.9861 778; -73.0664 683 |
| OWNER_OPERATOR | who | 4.9K | 18.4K | Tennessee Valley Authorit 2.9K; Florida Power & Light Com 1.9K; Virginia Electric & Power 1.3K; Entergy Corporation (Owne 1.3K |
| SO2_PHASE | category | 5 | 30.9K | Phase 2 89.9K; Table 1 6.7K; Substitution 744; Opt-In 280 |
| NOX_PHASE | category | 4 | 106.2K | Early Election 6.8K; Phase 2 Group 1 6.4K; Phase 1 Group 1 6.3K; Phase 2 Group 2 2.9K |
| UNIT_TYPE | who | 1.5K | 906 | Combustion turbine 46.2K; Dry bottom wall-fired boi 25.5K; Combined cycle 24.1K; Tangentially-fired 17.0K |
| PRIMARY_FUEL_TYPE | category | 38 | 4.3K | Pipeline Natural Gas 73.3K; Coal 30.2K; Diesel Oil 9.7K; Residual Oil 3.2K |
| SECONDARY_FUEL_TYPE | who | 97 | 74.6K | Diesel Oil 30.8K; Pipeline Natural Gas 7.7K; Residual Oil 5.4K; Natural Gas 1.5K |
| SO2_CONTROLS | who | 305 | 115.9K | Wet Limestone 4.3K; Wet Lime FGD 2.6K; Dry Lime FGD 2.6K; Fluidized Bed Limestone I 1.2K |
| NOX_CONTROLS | who | 1.7K | 36.5K | Water Injection 14.1K; Dry Low NOx Burners 10.8K; Dry Low NOx Burners/Selec 8.9K; Selective Catalytic Reduc 6.2K |
| PM_CONTROLS | who | 349 | 95.1K | Electrostatic Precipitato 21.8K; Baghouse 6.6K; Electrostatic Precipitato 926; Cyclone 782 |
| HG_CONTROLS | who | 155 | 125.9K | Halogenated PAC Sorbent I 1.2K; Additives to Enhance PAC  366; Untreated PAC Sorbent Inj 235; Additives to Enhance PAC  181 |
| COMMERCIAL_OPERATION_DATE | date | 3.2K | 1.9K | 1971-06-01 1.1K; 1970-06-01 901; 1970-07-01 705; 2001-06-01 693 |
| OPERATING_STATUS | who | 1.9K | 175 | Operating 121.3K; Retired 2.9K; Long-term Cold Storage 337; Future 130 |
| MAX_HOURLY_HI_RATE_MMBTU_HR | other | 2.9K | 18.6K | 500 1.1K; 299 802; 300 791; 1200 688 |
| ASSOCIATED_GENERATORS_NAMEPLATE_CAPACITY_MWE | who | 4.9K | 5.5K | TG2 (5.4), TG1 (5.4) 616; MAG1 (185) 615; MAG2 (185) 615; GEN1 (59.5) 614 |
| _INGESTED_AT | audit date | 1 | 0 | 56662972-04-01 06:28:49.0 128.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 917f552a-b76d-4fc1-ac01-e 128.5K |
| _SRC_SHA256 | category | 31 | 0 | c5940e45aec4fa855b6f76997 5.0K; e25c07183bcddfc262d0563d7 4.9K; 8f49fb1b8d02a1f3ff8059e76 4.9K; ae86981964e289de1282847d9 4.9K |
| _SRC_FILE | category | 31 | 0 | facility-2008.csv 5.0K; facility-2012.csv 4.9K; facility-2009.csv 4.9K; facility-2011.csv 4.9K |
