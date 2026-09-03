# FED_CMS_LTCH

rows 311  columns 16  scan 2.1s

roles: audit 2, category 2, date 1, other 8, state 1, who 2

## when

CERTIFICATION_DATE
  1966        11  ##############
  1969         1  #
  1970         1  #
  1974         1  #
  1976         1  #
  1984         3  ####
  1988         3  ####
  1989         2  ###
  1990         1  #
  1991         7  #########
  1992         6  ########
  1993        15  ####################
  1994        18  #######################
  1995        17  ######################
  1996         8  ##########
  1997         6  ########
  1998        13  #################
  1999        15  ####################
  2000        11  ##############
  2001        10  #############
  2002        15  ####################
  2003        21  ###########################
  2004        23  ##############################
  2005        14  ##################
  2006        10  #############
  2007        12  ################
  2008        20  ##########################
  2009        11  ##############
  2010         6  ########
  2011         1  #
  2012         2  ###
  2013         1  #
  2014         3  ####
  2015         4  #####
  2016         5  #######
  2019         1  #
  2020         2  ###
  2022         3  ####
  2023         1  #
  2024         5  #######
  2025         1  #

## who

PROVIDER_NAME by rows
         1  BAPTIST HEALTH EXTENDED CARE HOSPITAL-LR INC
         1  SELECT SPECIALTY HOSPITAL ARIZONA
         1  SELECT SPECIALTY HOSPITAL - SAVANNAH, INC
         1  VIBRA HOSPITAL OF BOISE
         1  BRIDGEPOINT CONT CARE HOSPITAL - NAT HARBORSIDE
         1  WESTERN MARYLAND HOSPITAL CENTER
         1  SELECT SPECIALTY HOSPITAL - BELHAVEN
         1  SELECT SPECIALTY HOSPITAL SPRINGFIELD, INC
         1  OCHSNER SPECIALTY HOSPITAL
         1  MOSIAC LIFE CARE AT ST JOSEPH
         1  SELECT SPECIALTY HOSPITAL-BOARDMAN
         1  KINDRED HOSPITAL - LAS VEGAS (SAHARA CAMPUS)
         1  SELECT SPECIALTY HOSPITAL-GULF COAST, INC
         1  LOUISIANA EXTENDED CARE HOSPITAL OF NATCHITOCHES
         1  BAYCARE ALLIANT HOSPITAL
         1  NOLAND HOSPITAL ANNISTON II, LLC
         1  ACUITY SPECIALTY HOSPITAL OF NEW JERSEY
         1  SELECT SPECIALTY HOSPITAL - THE VILLAGES
         1  SELECT SPECIALTY HOSPITAL-FORT MYERS
         1  SELECT SPECIALTY HOSPITAL-PALM BEACH

_SRC_SHA256 by rows
       311  5a0bccdadc6e9716135f5a2aa897d5bc3919660df817d148ba86ff0bbb87ab44

## who x when

PROVIDER_NAME by CERTIFICATION_DATE
  ACUITY SPECIALTY HOSPITAL OF NEW JERSEY   2010:1
  BAPTIST HEALTH EXTENDED CARE HOSPITAL-LR  2008:1
  BAYCARE ALLIANT HOSPITAL                  2008:1
  BRIDGEPOINT CONT CARE HOSPITAL - NAT HAR  2002:1
  KINDRED HOSPITAL - LAS VEGAS (SAHARA CAM  1994:1
  LOUISIANA EXTENDED CARE HOSPITAL OF NATC  2002:1
  MOSIAC LIFE CARE AT ST JOSEPH             2009:1
  NOLAND HOSPITAL ANNISTON II, LLC          2004:1
  OCHSNER SPECIALTY HOSPITAL                1995:1
  SELECT SPECIALTY HOSPITAL - BELHAVEN      1993:1
  SELECT SPECIALTY HOSPITAL - SAVANNAH, IN  2003:1
  SELECT SPECIALTY HOSPITAL - THE VILLAGES  2012:1
  SELECT SPECIALTY HOSPITAL ARIZONA         2000:1
  SELECT SPECIALTY HOSPITAL SPRINGFIELD, I  2008:1
  SELECT SPECIALTY HOSPITAL-BOARDMAN        2000:1
  SELECT SPECIALTY HOSPITAL-FORT MYERS      2015:1
  SELECT SPECIALTY HOSPITAL-GULF COAST, IN  1999:1
  SELECT SPECIALTY HOSPITAL-PALM BEACH      2008:1
  VIBRA HOSPITAL OF BOISE                   2009:1
  WESTERN MARYLAND HOSPITAL CENTER          1966:1

_SRC_SHA256 by CERTIFICATION_DATE
  5a0bccdadc6e9716135f5a2aa897d5bc3919660d  1966:11 1969:1 1970:1 1974:1 1976:1 1984:3 1988:3 1989:2 1990:1 1991:7 1992:6 1993:15 1994:18 1995:17 1996:8 1997:6 1998:13 1999:15 2000:11 2001:10 2002:15 2003:21 2004:23 2005:14 2006:10 2007:12 2008:20 2009:11 2010:6 2011:1 2012:2 2013:1 2014:3 2015:4 2016:5 2019:1 2020:2 2022:3 2023:1 2024:5 2025:1

## where

STATE: TX 39, FL 22, LA 21, CA 20, OH 15, PA 12, MI 11, MA 10, KY 10, GA 10, NJ 9, TN 8

## what

CMS_REGION: 6 25%, 4 24%, 5 14%, 9 10%, 3 9%, 7 5%, 8 4%, 1 4%, 2 3%, 10 2%

OWNERSHIP_TYPE: For profit 70%, Non-profit 26%, Government 4%, Physician 0%, Tribal 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CCN | other | 317 | 0 | 522008 2; 522006 2; 522005 2; 512005 2 |
| PROVIDER_NAME | who | 314 | 0 | SELECT SPECIALTY HOSPITAL 2; SELECT SPECIALTY HOSPITAL 2; LAKEVIEW SPECIALTY HOSPIT 2; SELECT SPECIALTY HOSPITAL 2 |
| ADDRESS_LINE_1 | other | 319 | 0 | 801 BRAXTON PLACE 2; 8901 W LINCOLN AVE 2ND FL 2; 1701 SHARP ROAD 2; 601 COLLIERS WAY 9TH FLOO 2 |
| ADDRESS_LINE_2 | other | 1 | 0 | - 311 |
| CITY_TOWN | other | 263 | 0 | SAN ANTONIO 5; LAS VEGAS 5; HOUSTON 4; MEMPHIS 4 |
| STATE | state | 47 | 0 | TX 39; FL 22; LA 21; CA 20 |
| ZIP_CODE | other | 308 | 0 | 77598 3; 53715 2; 53227 2; 53185 2 |
| COUNTY_PARISH | other | 223 | 0 | Los Angeles 7; Harris 6; Jefferson 6; Clark 5 |
| TELEPHONE_NUMBER | other | 303 | 0 | (608) 260-2700 2; (414) 328-7700 2; (262) 534-7297 2; (740) 283-7497 2 |
| CMS_REGION | category | 10 | 0 | 6 77; 4 76; 5 43; 9 32 |
| OWNERSHIP_TYPE | category | 5 | 0 | For profit 218; Non-profit 80; Government 11; Physician 1 |
| CERTIFICATION_DATE | date | 216 | 0 | 07/01/1966 11; 01/01/2008 5; 01/01/2002 5; 01/01/1994 4 |
| TOTAL_NUMBER_OF_BEDS | other | 117 | 0 | 40 20; 60 14; 30 13; 32 11 |
| _INGESTED_AT | audit | 1 | 0 | 1782339347571874 311 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 0c8ebc3a-50e8-4a5d-b2ff-9 311 |
| _SRC_SHA256 | who | 1 | 0 | 5a0bccdadc6e9716135f5a2aa 311 |
