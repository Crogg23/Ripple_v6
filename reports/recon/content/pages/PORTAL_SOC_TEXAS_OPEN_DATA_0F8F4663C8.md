# PORTAL_SOC_TEXAS_OPEN_DATA_0F8F4663C8

rows 1.0K  columns 13  scan 3.4s

roles: audit 2, category 2, date 2, other 4, state 1, who 3

## when

RESPONSIBILITY_BEGIN_DATE
  1963         1  
  1964         1  
  1967         1  
  1968        10  ####
  1969         2  #
  1970         2  #
  1972         3  #
  1973         4  #
  1974         1  
  1977         2  #
  1978         2  #
  1979         4  #
  1980         4  #
  1981         4  #
  1982         3  #
  1983         4  #
  1984         1  
  1985         6  ##
  1986         8  ###
  1987         5  ##
  1988         3  #
  1989         6  ##
  1990         7  ###
  1991         6  ##
  1992         6  ##
  1993        10  ####
  1994        10  ####
  1995         5  ##
  1996        10  ####
  1997         9  ###
  1998        13  #####
  1999        13  #####
  2000        16  ######
  2001        17  ######
  2002        21  ########
  2003        15  ######
  2004        32  ############
  2005        12  ####
  2006        14  #####
  2007        33  ############
  2008        14  #####
  2009        18  #######
  2010        18  #######
  2011        27  ##########
  2012        27  ##########
  2013        30  ###########
  2014        21  ########
  2015        30  ###########
  2016        21  ########
  2017        40  ###############
  2018        38  ##############
  2019        41  ###############
  2020        40  ###############
  2021        31  ###########
  2022        40  ###############
  2023        65  ########################
  2024        61  #######################
  2025        81  ##############################
  2026        40  ###############

INGESTED_AT
  2026      1.0K  ##############################

## who

NAME by rows
         1  OWENS CORNING ROOFING AND ASPHALT, LLC
         1  AVIENT CORPORATION
         1  WESTROCK CP, LLC
         1  ARKEMA INC.
         1  LAVACA PIPE LINE COMPANY
         1  INTERNATIONAL PAPER COMPANY
         1  TICONA POLYMERS, INC.
         1  ENTERGY TEXAS, INC.
         1  CREST PUMPING TECHNOLOGIES, LLC
         1  AMERICAN CHROME & CHEMICALS INC
         1  TARGA RESOURCES LLC
         1  WPX ENERGY PERMIAN, LLC
         1  CLEAN HARBORS DEER PARK, LLC
         1  EVONIK ACTIVE OXYGENS, LLC
         1  WESTERN REFINING COMPANY LLC
         1  AIRCO MECHANICAL, LTD.
         1  WRB REFINING LP
         1  NEW CINGULAR WIRELESS PCS, LLC
         1  AGRIGENETICS, INC.
         1  MANCO STRUCTURES, LTD.

CITY by rows
       256  HOUSTON
        77  DALLAS
        53  SAN ANTONIO
        44  AUSTIN
        32  FORT WORTH
        27  TULSA
        26  THE WOODLANDS
        26  MIDLAND
        22  SPRING
        20  IRVING
        15  DENVER
        13  BARTLESVILLE
        10  SAINT LOUIS
         9  SAN RAMON
         9  PITTSBURGH
         8  LEAGUE CITY
         7  POINT COMFORT
         7  CHICAGO
         7  OKLAHOMA CITY
         7  PLANO

SRC_SHA256 by rows
      1.0K  c06bbdfc5d408be320184ef18da45eef488cedc4949716c51261a6e308efb016

## who x when

NAME by RESPONSIBILITY_BEGIN_DATE
  AGRIGENETICS, INC.                        2001:1
  AIRCO MECHANICAL, LTD.                    2026:1
  AMERICAN CHROME & CHEMICALS INC           2010:1
  ARKEMA INC.                               1992:1
  AVIENT CORPORATION                        2001:1
  CLEAN HARBORS DEER PARK, LLC              2002:1
  CREST PUMPING TECHNOLOGIES, LLC           2024:1
  ENTERGY TEXAS, INC.                       2008:1
  EVONIK ACTIVE OXYGENS, LLC                2014:1
  INTERNATIONAL PAPER COMPANY               1990:1
  LAVACA PIPE LINE COMPANY                  2015:1
  MANCO STRUCTURES, LTD.                    2003:1
  NEW CINGULAR WIRELESS PCS, LLC            2020:1
  OWENS CORNING ROOFING AND ASPHALT, LLC    2020:1
  TARGA RESOURCES LLC                       2004:1
  TICONA POLYMERS, INC.                     1986:1
  WESTERN REFINING COMPANY LLC              2003:1
  WESTROCK CP, LLC                          2011:1
  WPX ENERGY PERMIAN, LLC                   2017:1
  WRB REFINING LP                           2007:1

CITY by RESPONSIBILITY_BEGIN_DATE
  AUSTIN                                    1999:1 2002:1 2012:1 2014:1 2017:1 2018:1 2019:1 2020:1 2021:3 2022:1 2023:6 2024:7 2025:14 2026:5
  BARTLESVILLE                              1968:1 1973:1 1982:1 1994:1 2006:1 2007:1 2012:2 2019:3 2021:1 2022:1
  CHICAGO                                   2001:1 2002:2 2011:1 2017:1 2018:1 2025:1
  DALLAS                                    1986:2 1987:1 1991:2 1993:2 1998:1 2000:2 2001:1 2002:4 2004:3 2005:2 2009:1 2011:3 2012:2 2015:1 2016:2 2017:3 2018:3 2019:4 2020:3 2021:3 2022:4 2023:8 2024:10 2025:8 2026:2
  DENVER                                    2012:1 2015:1 2017:1 2019:3 2020:1 2021:1 2022:2 2024:1 2025:3 2026:1
  FORT WORTH                                1992:1 1993:1 1999:1 2004:1 2010:1 2013:1 2016:1 2019:2 2020:3 2021:3 2022:3 2023:8 2024:3 2025:3
  HOUSTON                                   1968:1 1969:1 1972:1 1973:1 1977:1 1980:1 1981:1 1982:1 1983:2 1985:1 1987:2 1988:2 1989:2 1990:1 1992:2 1993:3 1994:2 1995:1 1996:2 1997:3 1998:5 1999:3 2000:2 2001:2 2002:5 2003:6 2004:14 2005:2 2006:2 2007:10 2008:3 2009:7 2010:6 2011:4 2012:3 2013:12 2014:6 2015:6 2016:4 2017:6 2018:16 2019:10 2020:6 2021:7 2022:13 2023:12 2024:19 2025:18 2026:16
  IRVING                                    1986:1 1989:1 1993:1 1996:1 2002:2 2006:2 2007:1 2010:1 2012:2 2016:2 2017:1 2020:1 2023:3 2025:1
  LEAGUE CITY                               1970:1 1986:1 2004:1 2005:1 2015:2 2021:1 2023:1
  MIDLAND                                   1968:2 1972:1 1979:1 1980:1 1992:1 2001:2 2002:1 2005:1 2006:1 2015:1 2016:1 2017:1 2020:4 2021:1 2022:1 2023:3 2024:1 2025:1 2026:1
  OKLAHOMA CITY                             1997:1 1998:1 2000:1 2009:1 2017:1 2020:1 2024:1
  PITTSBURGH                                1964:1 1995:2 2002:1 2003:1 2004:1 2005:1 2013:1 2019:1
  PLANO                                     2004:1 2006:1 2017:1 2021:1 2022:1 2024:2
  POINT COMFORT                             1990:3 2011:1 2015:3
  SAINT LOUIS                               1991:1 2003:1 2008:1 2012:1 2014:1 2020:5
  SAN ANTONIO                               1979:1 1987:1 1993:1 1994:2 1997:1 1998:1 1999:2 2004:2 2007:1 2011:3 2012:2 2013:3 2014:1 2015:4 2016:3 2017:8 2018:4 2019:5 2020:1 2022:2 2023:1 2024:3 2025:1
  SAN RAMON                                 1968:1 1986:1 2000:1 2006:2 2008:1 2013:1 2023:2
  SPRING                                    1968:2 1969:1 1973:1 1998:1 2002:2 2004:1 2006:1 2007:2 2008:1 2013:1 2014:1 2016:1 2018:1 2019:1 2021:1 2024:1 2025:2 2026:1
  THE WOODLANDS                             1985:1 1997:1 2000:3 2001:1 2005:1 2006:1 2007:1 2008:1 2011:2 2012:1 2013:2 2017:2 2018:1 2019:2 2022:1 2023:4 2024:1
  TULSA                                     1980:2 1985:1 2001:1 2005:1 2007:2 2009:2 2010:1 2011:4 2012:3 2013:1 2014:1 2015:1 2017:1 2018:2 2019:2 2022:1 2024:1

## where

STATE: TX 675, OK 47, CA 24, NJ 22, OH 22, PA 20, MO 18, CO 17, MI 17, NC 14, FL 13, IL 13

## what

COUNTY: HARRIS 47%, DALLAS 17%, BEXAR 9%, TRAVIS 8%, TARRANT 6%, MONTGOMERY 5%, MIDLAND 3%, COLLIN 1%, GALVESTON 1%, CALHOUN 1%, SMITH 1%

BUSINESS_TYPE: FOREIGN LMTD LIAB CO - OOS 44%, FOREIGN PROFIT CORPORATION 22%, TEXAS LIMITED LIABILITY COMPAN 15%, FRGN LIMITED PRTNSHP 7%, TEXAS PROFIT CORPORATION 6%, TX LIMITED PRTNSHP 5%, BUS GENERAL PRTNSHP 0%, TEXAS NON-PROFIT CORPORATION 0%, INDIVIDUAL - SOLE OWNER 0%, IND GENERAL PRTNSHP 0%, FOREIGN INSURANCE CORP - OOS 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 997 | 0 | 32100475113 6; 32099326459 6; 32099128335 6; 32098682886 6 |
| NAME | who | 1.0K | 0 | OUTER LOOP UTILITY, LLC 6; OTSUKA ICU MEDICAL LLC 6; SYSTEMS PROTECTION GROUP  6; DE CENTRAL OPERATING, LLC 6 |
| ADDRESS | other | 671 | 0 | 211 E 7TH ST STE 620 22; 1999 BRYAN ST STE 900 19; 8111 WESTCHESTER DR STE 6 18; 16211 LA CANTERA PKWY STE 16 |
| CITY | who | 226 | 0 | HOUSTON 256; DALLAS 77; SAN ANTONIO 53; AUSTIN 44 |
| STATE | state | 39 | 1 | TX 675; OK 47; CA 24; NJ 22 |
| ZIP | other | 624 | 0 | 78701-3218 21; 75201-3140 18; 75225-6142 18; 78256-2452 16 |
| COUNTY | category | 45 | 334 | HARRIS 284; DALLAS 104; BEXAR 54; TRAVIS 49 |
| BUSINESS_TYPE | category | 11 | 0 | FOREIGN LMTD LIAB CO - OO 441; FOREIGN PROFIT CORPORATIO 227; TEXAS LIMITED LIABILITY C 155; FRGN LIMITED PRTNSHP 66 |
| NAICS_CODE | other | 243 | 108 | 211120 79; 213112 41; 486210 38; 211130 38 |
| RESPONSIBILITY_BEGIN_DATE | date | 665 | 0 | 10/07/2025 18; 06/04/2026 11; 06/03/2026 9; 11/01/2004 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:46:14.20705 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 06857cc0-bca5-43f4-bb2b-2 1.0K |
| SRC_SHA256 | who | 1 | 0 | c06bbdfc5d408be320184ef18 1.0K |
