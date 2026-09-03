# PORTAL_SOC_TEXAS_OPEN_DATA_4D3A5EED0F

rows 2.0K  columns 18  scan 3.9s

roles: audit 2, category 2, date 4, other 6, state 1, who 4

## when

RESP_BEGIN_DATE
  1976         1  
  1990         1  
  1992         1  
  1994         1  
  2001         1  
  2002        20  
  2003        19  
  2004        51  #
  2005        68  #
  2006        18  
  2007        18  
  2008        14  
  2009        12  
  2010        27  #
  2011         6  
  2012        11  
  2013         9  
  2014        23  
  2015        11  
  2016        14  
  2017        10  
  2018        27  #
  2019      1.5K  ##############################
  2020        39  #
  2021        50  #
  2022        24  
  2023        18  
  2024        16  
  2025        12  
  2026         9  

OUT_OF_BUSINESS_DATE
  2021        21  ###
  2022       192  ##############################
  2023        13  ##
  2024        44  #######
  2025        24  ####
  2026         2  

LOC_CITY_ANNEX
  2003         1  ###
  2004         4  ############
  2008         1  ###
  2009         2  ######
  2010         1  ###
  2015         8  ########################
  2016         1  ###
  2017         2  ######
  2018         2  ######
  2019        10  ##############################
  2020         8  ########################
  2021         1  ###
  2022         1  ###
  2023         1  ###
  2024         2  ######
  2025         1  ###
  2026         2  ######

INGESTED_AT
  2026      2.0K  ##############################

## who

LOC_NAME by rows
         6  HOLIDAY INN EXPRESS
         5  LA QUINTA INN & SUITES
         5  SUPER 8 MOTEL
         4  MOTEL 6
         4  RIATA INN
         4  COMFORT SUITES
         3  HOME SUITE STAYS
         3  BUDGET INN
         3  VDF PROPERTIES LLC
         3  HAMPTON INN & SUITES
         2  CITY OF DALLAS
         2  CITY OF ALLEN
         2  QUALITY INN
         2  STITCHIN' HEAVEN INC
         2  PALACE INN
         2  DELUXE INN
         2  STUDIO 6
         2  CITY OF HOUSTON
         2  BEST WESTERN
         2  REEL DEAL

ADDRESS_TEXT by rows
      1.4K  DOMAIN BLVD STE 300
        11  COPANO RIDGE RD
         8  COPANO COVE RD
         6  PADRE BLVD
         5  BAYHOUSE DR
         4  BAY SHORE DR
         4  ELDRIDGE PKWY
         4  NORTH FWY
         4  PINTAIL LN
         4  TEAL RD
         4  N IH 35
         3  FM 1781
         3  MEDICAL DR
         3  FANNIN ST
         3  MCCUE RD
         3  MAIN ST
         3  S WATER ST
         3  SAILHOUSE WAY
         3  W BAY AREA BLVD
         2  N US HIGHWAY 83

LOC_CITY by rows
      1.4K  AUSTIN
       163  ROCKPORT
        91  HOUSTON
        19  SAN ANTONIO
        17  GALVESTON
        15  DALLAS
        12  CORPUS CHRISTI
        12  SOUTH PADRE ISLAND
         8  FORT WORTH
         8  WACO
         8  IRVING
         7  FREDERICKSBURG
         6  FULTON
         5  PORT ARANSAS
         5  COLLEGE STATION
         5  BEAUMONT
         4  NEW BRAUNFELS
         4  ARANSAS PASS
         4  WEBSTER
         4  MIDLAND

SRC_SHA256 by rows
      2.0K  9b5de1d2ccd7a33a79dcfda1a00d82ee048b96dbc42b2da141fd7b71023055e2

## who x when

LOC_NAME by RESP_BEGIN_DATE
  BEST WESTERN                              2004:1 2005:1
  BUDGET INN                                1990:1 2002:1 2008:1
  CITY OF ALLEN                             2019:2
  CITY OF DALLAS                            2019:2
  CITY OF HOUSTON                           2019:1 2024:1
  COMFORT SUITES                            2003:1 2004:1 2006:1 2008:1
  DELUXE INN                                2002:1 2024:1
  HAMPTON INN & SUITES                      2005:1 2006:1 2007:1
  HOLIDAY INN EXPRESS                       2003:1 2004:1 2005:1 2006:1 2008:1 2026:1
  HOME SUITE STAYS                          2023:2 2024:1
  LA QUINTA INN & SUITES                    2003:2 2004:1 2008:1 2020:1
  MOTEL 6                                   2009:1 2018:1 2024:1 2025:1
  PALACE INN                                2005:2
  QUALITY INN                               2007:1 2015:1
  REEL DEAL                                 2017:1 2021:1
  RIATA INN                                 2007:4
  STITCHIN' HEAVEN INC                      2019:1 2021:1
  STUDIO 6                                  2021:1 2025:1
  SUPER 8 MOTEL                             2002:1 2003:1 2004:2 2008:1
  VDF PROPERTIES LLC                        2021:3

ADDRESS_TEXT by RESP_BEGIN_DATE
  BAY SHORE DR                              2005:1 2020:1 2021:2
  BAYHOUSE DR                               2021:3 2022:2
  COPANO COVE RD                            2012:1 2017:1 2018:1 2019:3 2020:1 2022:1
  COPANO RIDGE RD                           2018:3 2019:2 2020:2 2021:4
  DOMAIN BLVD STE 300                       2019:1.4K
  ELDRIDGE PKWY                             2005:2 2006:1 2019:1
  FANNIN ST                                 2004:1 2010:1 2013:1
  FM 1781                                   2012:1 2019:2
  MAIN ST                                   2004:1 2005:1 2008:1
  MCCUE RD                                  2004:1 2005:1 2014:1
  MEDICAL DR                                2008:1 2011:1 2020:1
  N IH 35                                   2002:1 2004:1 2005:2
  N US HIGHWAY 83                           2007:1 2010:1
  NORTH FWY                                 2004:1 2006:1 2010:1 2021:1
  PADRE BLVD                                2004:2 2008:1 2010:1 2019:1 2026:1
  PINTAIL LN                                2017:1 2019:1 2020:1 2021:1
  S WATER ST                                2019:1 2021:1 2022:1
  SAILHOUSE WAY                             2013:1 2016:1 2017:1
  TEAL RD                                   2020:1 2021:2 2022:1
  W BAY AREA BLVD                           2002:1 2005:2

## where

LOC_STATE: TX 2.0K, MA 1, CA 1

## what

NAICS: 531110 80%, 721110 10%, 531311 3%, 721000 3%, 531190 2%, 721191 0%, 721199 0%, 721214 0%, 713120 0%, 561110 0%, 481111 0%, 721310 0%

LOC_JURIS: Y 92%, N 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TP_NUMBER | other | 294 | 0 | 12022080290 1.4K; 12021015925 172; 10106997397 53; 12016274339 42 |
| LOC_NUMBER | other | 1.4K | 0 | 1 223; 2 53; 3 12; 4 11 |
| LOC_NAME | who | 1.9K | 0 | CITY OF RALLS 10; CITY OF QUITMAN 10; CITY OF QUITAQUE 10; CITY OF BELLEVUE 10 |
| ADDRESS_NUMBER | other | 464 | 2 | 11800 1.4K; 1021 50; 2003 9; 111 5 |
| ADDRESS_TEXT | who | 509 | 0 | DOMAIN BLVD STE 300 1.4K; COPANO RIDGE RD 13; COPANO COVE RD 10; PADRE BLVD 7 |
| LOC_STATE | state | 3 | 0 | TX 2.0K; MA 1; CA 1 |
| LOC_CITY | who | 177 | 0 | AUSTIN 1.4K; ROCKPORT 163; HOUSTON 91; SAN ANTONIO 19 |
| LOC_ZIP | other | 283 | 0 | 78758 1.4K; 78382 167; 78597 12; 77056 10 |
| LOC_ZIP4 | other | 392 | 120 | 3418 1.4K; 2325 49; 9522 5; 9518 5 |
| LOC_COUNTY | other | 104 | 0 | 227 1.4K; 4 173; 101 104; 57 30 |
| NAICS | category | 14 | 0 | 531110 1.6K; 721110 207; 531311 66; 721000 65 |
| LOC_JURIS | category | 2 | 0 | Y 1.8K; N 155 |
| RESP_BEGIN_DATE | date | 309 | 0 | 2019-04-01T00:00:00.000 1.4K; 2010-10-08T00:00:00.000 20; 2019-06-01T00:00:00.000 17; 2014-09-30T00:00:00.000 16 |
| OUT_OF_BUSINESS_DATE | date | 63 | 0 | nan 1.7K; 2022-04-30T00:00:00.000 158; 2024-05-01T00:00:00.000 15; 2024-12-31T00:00:00.000 12 |
| LOC_CITY_ANNEX | date | 34 | 0 | nan 2.0K; 2015-10-01T00:00:00.000 7; 2019-04-01T00:00:00.000 6; 2020-12-01T00:00:00.000 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:47:21.84316 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4b4a8dcd-aed5-4472-ae20-c 2.0K |
| SRC_SHA256 | who | 1 | 0 | 9b5de1d2ccd7a33a79dcfda1a 2.0K |
