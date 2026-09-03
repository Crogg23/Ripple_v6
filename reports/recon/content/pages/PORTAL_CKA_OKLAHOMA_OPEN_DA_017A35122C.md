# PORTAL_CKA_OKLAHOMA_OPEN_DA_017A35122C

rows 4.3K  columns 11  scan 4.3s

roles: amount 1, audit 2, category 4, date 2, who 3

## when

DATE_ACQUIRED_OR_INSTALLED
  1905        14  #
  1976         1  
  1977        16  ##
  1978         2  
  1979         4  
  1980         5  
  1981         5  
  1982         6  #
  1983         2  
  1984         3  
  1985         3  
  1986        10  #
  1987         5  
  1988         9  #
  1989        12  #
  1990        12  #
  1991        29  ###
  1992        12  #
  1993        12  #
  1994        22  ##
  1995        30  ###
  1996        26  ###
  1997        68  #######
  1998        42  ####
  1999        58  ######
  2000        84  ########
  2001        75  #######
  2002        72  #######
  2003        68  #######
  2004        99  ##########
  2005       112  ###########
  2006       149  ###############
  2007       138  ##############
  2008       202  ####################
  2009       242  ########################
  2010       164  ################
  2011       172  #################
  2012       165  ################
  2013       196  ###################
  2014       211  #####################
  2015       206  ####################
  2016       145  ##############
  2017       204  ####################
  2018       161  ################
  2019       303  ##############################
  2020       231  #######################
  2021       174  #################
  2022       168  #################
  2023        83  ########
  2024         3  
  2025         3  
  2026         5  

INGESTED_AT
  2026      4.3K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE_OR_COST | 4.3K | 1 | 3.3K | 175.0K | 2.77M | 67.38M |

## who

PROPERTY_NAME by rows
        46  LAPTOP
        22  PRINTER
        21  CPU
        17  SCANNER
        14  DESKTOP
        14  FIRE EQUIP: FIRE FIGHTING EQUI
        14  PROJECTOR
        13  Z-TURN MOWER
        12  SOFTWARE
        12  CATALYST
        12  SERVER
        12  NETWORK SWITCH
        12  GATOR
        12  SWITCH
        10  2019 FORD EXPLORER
         9  BAMBI BUCKET
         9  FIREWALL
         9  LIGHT TRUCKS OR SUVS
         9  TRACTOR
         8  SUV: MID SIZE, 3.7L OR SMALLER

PROPERTY_NAME by dollars
       2.77M        1 rows  VOIP HARDWARE, SOFTWARE, INSTA
       2.13M        1 rows  NTT NETWORK SERVER BC11
       2.05M        1 rows  ACCELA SOFTWARE
       1.77M        1 rows  NTT NETWORK SERVER AN03
       1.76M        1 rows  NTT NETWORK SERVER TXAN02
       1.69M        1 rows  NTT NETWORK SERVER TXAN07
       1.56M        1 rows  NTT NETWORK SERVER TXAN05
       1.44M        6 rows  CABLE, FIBER OPTIC
      929.9K        1 rows  NTT NETWORK SERVER TXAN10
      864.4K        2 rows  CABLE, TELEPHONE (COPPER)
      835.0K        1 rows  COLOR OFFSET PRESS RYOBI 754
      566.6K        1 rows  WORKSTATION, SYSTEMS - S01
      450.0K        1 rows  CABLE FIBER OPTIC CAP TO DPS
      448.8K        9 rows  TRACTOR
      430.8K        1 rows  ROBOTIC MASS COMPARATOR
      424.0K        2 rows  MOTOR GRADER
      398.7K        1 rows  IBM EXTERNAL DRIVE
      382.5K        1 rows  SINGLE MODE FIBER STRANDS
      377.6K        1 rows  IBM POWER 9009 SERVER
      361.3K        3 rows  HPE STORAGE SYSTEMS

PROPERTY_TYPE by rows
      4.3K  PERSONAL PROPERTY

PROPERTY_TYPE by dollars
      67.38M     4.3K rows  PERSONAL PROPERTY

SRC_SHA256 by rows
      4.3K  287a8e6b8afb128cf8abf996bc8a59c34742a31f74bedb708d66d15825de8f2f

SRC_SHA256 by dollars
      67.38M     4.3K rows  287a8e6b8afb128cf8abf996bc8a59c34742a31f74bedb708d66d15825de

## who x when

PROPERTY_NAME by DATE_ACQUIRED_OR_INSTALLED, dollars = VALUE_OR_COST
  2019 FORD EXPLORER                        2019:250.8K
  ACCELA SOFTWARE                           2022:2.05M
  BAMBI BUCKET                              1996:27.6K 2002:73.8K 2007:19.1K 2009:20.3K 2012:31.8K
  CABLE, FIBER OPTIC                        1989:905.3K 1990:87.0K 1992:443.1K
  CABLE, TELEPHONE (COPPER)                 1987:618.2K 1988:246.2K
  CATALYST                                  2007:1.9K 2008:9.1K 2009:3.1K 2010:19.1K 2012:3.0K
  CPU                                       1998:1.2K 1999:639 2000:750 2002:2.9K 2004:750 2005:750 2006:1.3K 2007:1.8K 2008:1.2K 2010:1.3K 2011:2.5K 2012:1.3K 2013:875.12 2014:2.6K
  DESKTOP                                   2005:4.7K 2006:750 2008:2.5K 2009:1.5K 2010:750 2011:800 2013:778.42
  FIRE EQUIP: FIRE FIGHTING EQUI            2020:67.6K 2021:13.4K 2023:2.7K
  FIREWALL                                  2002:4.2K 2003:2.5K 2004:4.2K 2007:679 2008:4.8K 2012:8.1K 2016:4.5K
  GATOR                                     2003:5.9K 2005:13.2K 2010:13.7K 2011:7.5K 2012:26.7K 2013:25.2K 2014:19.9K 2015:16.1K
  LAPTOP                                    1905:13.9K 2000:2.2K 2002:1.5K 2005:3.1K 2006:2.2K 2007:2.7K 2008:3.0K 2009:5.7K 2010:4.7K 2011:1.8K 2012:8.0K 2013:8.2K 2014:3.3K 2015:9.6K 2019:1.3K
  LIGHT TRUCKS OR SUVS                      2021:65.1K 2022:173.2K 2023:34.8K
  NETWORK SWITCH                            2003:44.1K 2006:7.6K 2007:606.85 2008:606.85 2009:5.7K
  NTT NETWORK SERVER AN03                   2021:1.77M
  NTT NETWORK SERVER BC11                   2021:2.13M
  NTT NETWORK SERVER TXAN02                 2021:1.76M
  NTT NETWORK SERVER TXAN05                 2021:1.56M
  NTT NETWORK SERVER TXAN07                 2021:1.69M
  NTT NETWORK SERVER TXAN10                 2021:929.9K
  PRINTER                                   1997:1.1K 1998:1.1K 2000:3.0K 2001:1.6K 2003:2.3K 2004:2.2K 2006:4.7K 2007:1.7K 2008:3.4K 2009:1.1K 2013:1.1K 2016:1.3K
  PROJECTOR                                 2004:1.7K 2006:699 2009:605.83 2010:899 2011:4.5K 2013:800 2014:801 2015:1.8K 2016:1.8K 2022:2.7K
  SCANNER                                   1905:500 2004:742 2008:7.1K 2009:8.3K 2010:6.5K 2011:896.78 2012:1.5K 2016:1.2K 2017:2.1K 2019:872.50 2020:1.8K
  SERVER                                    1999:8.0K 2001:1.9K 2005:11.0K 2006:4.1K 2007:12.0K 2008:8.1K 2010:9.7K 2011:9.7K 2015:4.0K
  SOFTWARE                                  2006:10.2K 2007:4.9K 2010:919.80 2011:31.1K 2012:10.3K
  SUV: MID SIZE, 3.7L OR SMALLER            2019:140.8K 2020:19.3K
  SWITCH                                    1905:1.6K 2001:2.5K 2002:3.2K 2003:1.9K 2007:8.2K 2008:5.3K 2009:930 2010:1.6K 2012:4.8K 2015:2.1K
  TRACTOR                                   2000:46.9K 2001:22.4K 2006:23.2K 2007:8.0K 2013:58.0K 2014:290.3K
  VOIP HARDWARE, SOFTWARE, INSTA            2013:2.77M
  Z-TURN MOWER                              2005:7.7K 2008:7.6K 2009:5.7K 2010:35.3K 2011:9.1K 2013:40.0K 2014:15.1K

PROPERTY_TYPE by DATE_ACQUIRED_OR_INSTALLED, dollars = VALUE_OR_COST
  PERSONAL PROPERTY                         1905:26.0K 1976:9.2K 1977:227.0K 1978:6.9K 1979:19.4K 1980:23.2K 1981:33.5K 1982:45.4K 1983:9.8K 1984:17.9K 1985:5.5K 1986:62.3K 1987:631.9K 1988:290.3K 1989:955.6K 1990:244.6K 1991:233.7K 1992:705.1K 1993:40.4K 1994:132.1K 1995:398.4K 1996:330.7K 1997:345.4K 1998:232.0K 1999:401.1K 2000:353.3K 2001:382.2K 2002:389.4K 2003:238.4K 2004:384.6K 2005:1.04M 2006:1.57M 2007:1.54M 2008:2.05M 2009:3.91M 2010:2.55M 2011:1.12M 2012:1.64M 2013:6.04M 2014:2.77M 2015:2.42M 2016:1.54M 2017:1.90M 2018:2.18M 2019:4.56M 2020:2.40M 2021:14.22M 2022:3.76M 2023:1.35M 2024:3.8K 2025:6.0K 2026:14.8K

## what

AGENCY_CODE: 90 29%, 25 25%, 41 22%, 40 17%, 49 2%, 30 1%, 55 1%, 47 1%, 20 1%, 65 0%, 45 0%, 39 0%

STATE_AGENCY: OMES 29%, MILITARY DEPARTMENT 25%, WESTERN OKLAHOMA STATE COLLEGE 22%, AGRICULTURE, FOOD & FORESTRY 17%, ATTORNEY GENERAL 2%, ABLE COMMISSION 1%, ARTS COUNCIL 1%, INDIGENT DEFENSE SYSTEM 1%, OKLAHOMA ACCOUNTANCY BOARD 1%, STATE BANKING 0%, BOARD OF ARCHITECTS 0%, BOLL WEEVEL ERADICATION 0%

PROPERTY_CLASSIFICATION: OWNED 100%

IT_NON_IT: IT 57%, NON-IT 43%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCY_CODE | category | 14 | 0 | 90 1.3K; 25 1.1K; 41 972; 40 730 |
| STATE_AGENCY | category | 14 | 0 | OMES 1.3K; MILITARY DEPARTMENT 1.1K; WESTERN OKLAHOMA STATE CO 972; AGRICULTURE, FOOD & FORES 730 |
| PROPERTY_TYPE | who | 1 | 0 | PERSONAL PROPERTY 4.3K |
| PROPERTY_CLASSIFICATION | category | 2 | 1.3K | OWNED 3.0K |
| PROPERTY_NAME | who | 3.3K | 0 | LAPTOP 48; DESKTOP 31; NETWORK SWITCH 30; SERVER 25 |
| DATE_ACQUIRED_OR_INSTALLED | date | 2.3K | 91 | 1/1/2021 60; 10/31/2010 32; 6/30/2009 31; 6/30/2010 30 |
| VALUE_OR_COST | amount | 3.3K | 0 | $500.00  38; $750.00  31; $17,664.00  30; $5,000.00  28 |
| IT_NON_IT | category | 2 | 0 | IT 2.5K; NON-IT 1.9K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:59:00.65554 4.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 11349a94-3596-45c9-bba9-2 4.3K |
| SRC_SHA256 | who | 1 | 0 | 287a8e6b8afb128cf8abf996b 4.3K |
