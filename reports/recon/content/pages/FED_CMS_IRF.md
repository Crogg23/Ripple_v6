# FED_CMS_IRF

rows 1.2K  columns 15  scan 3.2s

roles: audit 2, category 2, date 1, id 2, other 3, state 1, who 4

## when

CERTIFICATION_DATE
  1983        18  ######
  1984        96  ##############################
  1985        40  ############
  1986        30  #########
  1987        17  #####
  1988        22  #######
  1989        21  #######
  1990        19  ######
  1991        24  ########
  1992        25  ########
  1993        24  ########
  1994        27  ########
  1995        31  ##########
  1996        21  #######
  1997        27  ########
  1998        24  ########
  1999        15  #####
  2000        20  ######
  2001        17  #####
  2002        27  ########
  2003        32  ##########
  2004        25  ########
  2005        29  #########
  2006        22  #######
  2007        19  ######
  2008        18  ######
  2009        17  #####
  2010        16  #####
  2011        19  ######
  2012        17  #####
  2013        21  #######
  2014        24  ########
  2015        27  ########
  2016        32  ##########
  2017        23  #######
  2018        35  ###########
  2019        34  ###########
  2020        30  #########
  2021        45  ##############
  2022        39  ############
  2023        59  ##################
  2024        47  ###############
  2025        40  ############
  2026         7  ##

## who

PROVIDER_NAME by rows
         3  GOOD SAMARITAN HOSPITAL
         3  BAYLOR SCOTT & WHITE INSTITUTE FOR REHABILITATION
         2  ST MARYS HOSPITAL
         2  LAWRENCE MEMORIAL HOSPITAL
         2  ST LUKES HOSPITAL
         2  ST MARYS MEDICAL CENTER
         2  METHODIST REHABILITATION HOSPITAL
         2  ST. JOSEPH MEDICAL CENTER
         2  DIGNITY HEALTH EAST VALLEY REHABILITATION HOSPITAL
         2  MERCY MEDICAL CENTER
         2  MERCY REGIONAL MEDICAL CENTER
         2  ST VINCENT HOSPITAL
         2  UNION HOSPITAL
         1  REUNION REHABILITATION HOSPITAL DENVER
         1  CASA COLINA HOSP FOR REHAB MEDICINE
         1  JOHNSON REGIONAL REHABILITATION CENTER
         1  ALASKA REGIONAL HOSPITAL
         1  REUNION REHABILITATION HOSPITAL PEORIA LLC
         1  SADDLEBACK MEMORIAL MEDICAL CENTER
         1  QUEEN OF THE VALLEY HOSPITAL

COUNTY_PARISH by rows
        26  Los Angeles
        22  Jefferson
        22  Harris
        19  Cook
        14  Maricopa
        13  Clark
        12  Hamilton
        12  Allegheny
        12  Dallas
        12  Orange
        12  Tarrant
        11  Lake
        11  Montgomery
        10  Wayne
        10  Johnson
         9  Collin
         8  El Paso
         8  Washington
         8  Broward
         8  Erie

ADDRESS_LINE_2 by rows
      1.2K  -
         2  2ND FLOOR
         1  900 HOSPITAL DR
         1  1400 E. BOULDER
         1  3300 OAKDALE AVE N
         1  REHABILITATION MEDICINE-RM 327
         1  200 WEST UNIVERSITY AVE, HAMMOND, LA 70401
         1  140 ACADEMY STREET
         1  PO BOX 350
         1  775 POLE LINE ROAD WEST SUITE
         1  W300
         1  725 NORTH ST
         1  BOX 52
         1  3RD FLOOR TURNER TOWER
         1  4-SOUTH
         1  865 DESHONG DRIVE
         1  BOX 142
         1  624 HOSPITAL DR
         1  9TH FLOOR - INPATIENT REHAB
         1  4300 ALTON ROAD

_SRC_SHA256 by rows
      1.2K  ce2bd8a31f9af2bbe2350c6eaa2ca490f0414d7cac0f7c60a5bd3fa9c13ae374

## who x when

PROVIDER_NAME by CERTIFICATION_DATE
  ALASKA REGIONAL HOSPITAL                  1994:1
  BAYLOR SCOTT & WHITE INSTITUTE FOR REHAB  1989:1 2015:1 2016:1
  CASA COLINA HOSP FOR REHAB MEDICINE       2016:1
  DIGNITY HEALTH EAST VALLEY REHABILITATIO  2016:1 2023:1
  GOOD SAMARITAN HOSPITAL                   1984:1 2001:1 2006:1
  JOHNSON REGIONAL REHABILITATION CENTER    2006:1
  LAWRENCE MEMORIAL HOSPITAL                1983:1 2017:1
  MERCY MEDICAL CENTER                      1985:1 1995:1
  MERCY REGIONAL MEDICAL CENTER             1984:1 2009:1
  METHODIST REHABILITATION HOSPITAL         1991:1 2008:1
  QUEEN OF THE VALLEY HOSPITAL              2008:1
  REUNION REHABILITATION HOSPITAL DENVER    2021:1
  REUNION REHABILITATION HOSPITAL PEORIA L  2023:1
  SADDLEBACK MEMORIAL MEDICAL CENTER        2005:1
  ST LUKES HOSPITAL                         1999:1 2006:1
  ST MARYS HOSPITAL                         1984:1 2008:1
  ST MARYS MEDICAL CENTER                   2000:1 2005:1
  ST VINCENT HOSPITAL                       1984:1 1991:1
  ST. JOSEPH MEDICAL CENTER                 1984:1 1996:1
  UNION HOSPITAL                            1989:1 2009:1

COUNTY_PARISH by CERTIFICATION_DATE
  Allegheny                                 1984:5 1989:1 1991:1 1993:1 2002:1 2003:1 2014:1 2017:1
  Broward                                   1984:1 1985:1 2021:1 2023:2 2024:1 2025:1 2026:1
  Clark                                     1984:1 1993:1 1994:1 1995:1 1997:1 2002:1 2007:1 2012:1 2018:1 2019:1 2020:1 2021:1 2023:1
  Collin                                    1991:1 2007:1 2011:1 2013:1 2015:1 2018:1 2023:2 2024:1
  Cook                                      1983:1 1984:8 1985:1 1988:1 1990:1 1991:1 1993:1 2015:3 2016:1 2024:1
  Dallas                                    1989:1 2008:2 2010:2 2015:1 2016:2 2018:2 2019:1 2022:1
  El Paso                                   1991:1 1994:1 2004:1 2013:1 2017:1 2020:2 2023:1
  Erie                                      1984:1 1986:2 1988:1 1991:1 1992:1 1994:1 2013:1
  Hamilton                                  1984:1 1986:2 1990:1 1994:1 2003:1 2012:1 2014:1 2016:1 2017:1 2021:1 2024:1
  Harris                                    1984:2 1995:2 1996:7 2009:1 2011:2 2012:1 2015:1 2016:1 2019:1 2020:1 2022:1 2024:2
  Jefferson                                 1983:1 1990:1 1991:1 1997:2 1998:3 1999:1 2004:1 2007:1 2008:1 2014:1 2017:2 2018:1 2019:1 2021:1 2022:1 2023:1 2024:2
  Johnson                                   1989:1 1997:1 2006:1 2007:1 2015:2 2018:1 2020:2 2022:1
  Lake                                      1984:1 2001:1 2002:2 2004:1 2019:1 2022:1 2023:3 2026:1
  Los Angeles                               1983:3 1984:6 1985:1 1992:2 1994:4 1996:1 1999:1 2004:1 2008:1 2013:2 2016:2 2017:1 2024:1
  Maricopa                                  1984:1 1985:1 1989:1 1998:1 2009:1 2013:1 2016:2 2020:1 2022:1 2023:3 2024:1
  Montgomery                                1987:1 1993:1 2001:1 2002:1 2009:3 2014:1 2016:1 2023:1 2024:1
  Orange                                    1984:2 1991:2 1992:1 1993:1 1997:1 2005:1 2015:1 2019:1 2024:1 2025:1
  Tarrant                                   1990:2 2009:1 2010:2 2011:1 2015:1 2016:1 2017:1 2021:1 2023:2
  Washington                                1984:1 1988:1 1991:1 1998:1 2000:1 2005:1 2014:1 2017:1
  Wayne                                     1983:1 1984:1 1985:1 1988:2 2003:1 2006:2 2007:1 2010:1

## where

STATE: TX 157, FL 87, CA 83, PA 65, LA 55, OH 53, NY 42, IL 42, MI 41, GA 34, IN 33, TN 32

## what

CMS_REGION: 6 22%, 4 21%, 5 17%, 9 10%, 3 9%, 7 6%, 2 5%, 8 4%, 10 3%, 1 3%

OWNERSHIP_TYPE: Non-profit 47%, For profit 45%, Government 8%, Physician 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CCN | id | 1.2K | 0 | 743035 7; 743032 7; 743031 7; 743030 7 |
| PROVIDER_NAME | who | 1.2K | 0 | REHABILITATION HOSPITAL O 7; CLEARSKY REHABILITATION H 7; HORIZON MEDICAL CENTER OF 7; ENCOMPASS HEALTH REHABILI 7 |
| ADDRESS_LINE_1 | id | 1.2K | 0 | 7950 WALLACE BLVD 7; 25 HOPE DRIVE 7; 6601 W UNIVERSITY DRIVE 7; 3010 YELLOWSTONE BLVD 7 |
| ADDRESS_LINE_2 | who | 68 | 0 | - 1.2K; 2ND FLOOR 2; P.O. BOX 13508 1; BOX 359818 1 |
| CITY_TOWN | other | 837 | 0 | HOUSTON 18; DALLAS 12; CHICAGO 11; SAN ANTONIO 10 |
| STATE | state | 52 | 0 | TX 157; FL 87; CA 83; PA 65 |
| ZIP_CODE | other | 1.1K | 0 | 77030 9; 79902 8; 79124 7; 77304 7 |
| COUNTY_PARISH | who | 538 | 0 | Los Angeles 26; Harris 25; Jefferson 22; Cook 19 |
| TELEPHONE_NUMBER | other | 1.1K | 0 | (502) 596-6346 64; (877) 287-3422 12; (972) 308-8567 7; (757) 388-4261 7 |
| CMS_REGION | category | 10 | 0 | 6 272; 4 257; 5 205; 9 121 |
| OWNERSHIP_TYPE | category | 4 | 0 | Non-profit 570; For profit 545; Government 99; Physician 8 |
| CERTIFICATION_DATE | date | 694 | 0 | 07/01/1984 45; 01/01/1984 31; 01/01/1985 23; 10/01/1983 16 |
| _INGESTED_AT | audit | 1 | 0 | 1782339336878085 1.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 898be91d-d70b-4692-93a0-c 1.2K |
| _SRC_SHA256 | who | 1 | 0 | ce2bd8a31f9af2bbe2350c6ea 1.2K |
