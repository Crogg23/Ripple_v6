# FED_ICIJ_OFFSHORELEAKS_OTHERS

rows 3.0K  columns 16  scan 4.2s

roles: audit 2, category 6, date 3, id 1, other 1, who 3

## when

INCORPORATION_DATE
  1933         1  #
  1936         1  #
  1939         3  ##
  1942         1  #
  1946         1  #
  1947         1  #
  1948         2  ##
  1949         1  #
  1950         1  #
  1951         1  #
  1953         1  #
  1954         1  #
  1955         2  ##
  1956         2  ##
  1957         1  #
  1958         1  #
  1961         1  #
  1962         2  ##
  1963         4  ###
  1966         1  #
  1967         3  ##
  1968         2  ##
  1970         3  ##
  1971         4  ###
  1972         2  ##
  1973         3  ##
  1974         2  ##
  1975         2  ##
  1976         7  #####
  1977         2  ##
  1978         6  #####
  1979         2  ##
  1980         5  ####
  1981         7  #####
  1982         7  #####
  1983         9  #######
  1984         2  ##
  1985        11  ########
  1986        12  #########
  1987        21  ################
  1988        22  #################
  1989        36  ############################
  1990        30  #######################
  1991        25  ###################
  1992        20  ###############
  1993        29  ######################
  1994        26  ####################
  1995        24  ##################
  1996        39  ##############################
  1997        13  ##########
  1998        31  ########################
  1999        18  ##############
  2000        32  #########################
  2001        26  ####################
  2002        34  ##########################
  2003        29  ######################
  2004        31  ########################
  2005        33  #########################
  2006        25  ###################
  2007        18  ##############
  2008        24  ##################
  2009        25  ###################
  2010        21  ################
  2011        18  ##############
  2012        30  #######################
  2013        24  ##################
  2014        31  ########################
  2015        21  ################
  2016        12  #########

STRUCK_OFF_DATE
  1991         1  ####
  1993         1  ####
  1995         1  ####
  1996         1  ####
  1998         1  ####
  1999         1  ####
  2000         6  ##########################
  2001         7  ##############################
  2002         5  #####################
  2003         6  ##########################
  2004         1  ####
  2005         6  ##########################
  2006         3  #############
  2008         1  ####
  2009         3  #############
  2013         1  ####

CLOSED_DATE
  1994         1  ##
  1995         1  ##
  1996         1  ##
  1997         2  #####
  1998         4  #########
  1999         3  #######
  2000         5  ############
  2001         2  #####
  2002         6  ##############
  2003         8  ##################
  2004         7  ################
  2005         2  #####
  2006         9  #####################
  2007         7  ################
  2008        10  #######################
  2009        12  ############################
  2010        13  ##############################
  2011        11  #########################
  2012         1  ##
  2014         4  #########
  2015         4  #########
  2016         4  #########

## who

NAME by rows
         3  Shampaign Investments Limited
         3  Flipflop International Limited
         2  Renaissance Group
         2  Kayché Limited
         2  Mackie Group
         2  ANTAM ENTERPRISES N.V.
         2  CLASSIQUE DE L'ISLE N.V.
         2  FOX TRADING N.V.
         2  Mivec Limited
         2  Magna Group
         2  Orion Group
         1  SUPERCAR RENTALS N.V.
         1  Crucible Insurance Company Limited
         1  Prime Limited
         1  Argo Group Limited
         1  Castletown and District Over 60's Club
         1  Argon Technologies Limited
         1  SATKAR CENTER N.V.
         1  Group - Maxwell Mellor Group
         1  Group - Pickering Developments Group

COUNTRIES by rows
       105  Isle of Man
        79  Cayman Islands
        26  United Kingdom
        24  United States
        14  Ireland
        13  China
        12  Jersey
        10  Bermuda
         9  British Virgin Islands;Isle of Man
         7  Mauritius
         7  British Virgin Islands
         5  Switzerland
         5  Isle of Man;United Kingdom
         5  Guernsey
         4  Canada
         4  Hong Kong
         3  Greece
         3  Monaco
         3  India
         2  Mexico

SRC_SHA256 by rows
      3.0K  a47f098b1c7595fa9e4f1554966bb0f9fdbc0d1f1b4b919c61dc9b378c31b68d

## who x when

NAME by INCORPORATION_DATE
  ANTAM ENTERPRISES N.V.                    1983:2
  CLASSIQUE DE L'ISLE N.V.                  1989:2
  FOX TRADING N.V.                          1976:2
  SATKAR CENTER N.V.                        1990:1
  SUPERCAR RENTALS N.V.                     1990:1

COUNTRIES by INCORPORATION_DATE

## what

TYPE: LIMITED LIABILITY COMPANY 99%, SOLE OWNERSHIP 0%, FOREIGN FORMED CORPORATION 0%

JURISDICTION: AW 93%, VGB 6%, BLZ 0%, KNA 0%, PAN 0%, USA 0%

JURISDICTION_DESCRIPTION: Aruba 93%, British Virgin Islands 6%, Belize 0%, Nevis 0%, Panama 0%, South Dakota 0%

SOURCEID: Paradise Papers - Appleby 68%, Paradise Papers - Aruba corpor 30%, Pandora Papers - Trident Trust 2%, Pandora Papers - Overseas Mana 0%, Pandora Papers - Alemán, Corde 0%, Pandora Papers - CILTrust Inte 0%, Pandora Papers - Fidelity Corp 0%

VALID_UNTIL: Appleby data is current throug 68%, Aruba corporate registry data  30%, Provider data is current throu 1%, Provider data is current throu 0%, Provider data is current throu 0%, Provider data is current throu 0%, Provider data is current throu 0%, Provider data is current throu 0%, Provider data is current throu 0%, Provider data is current throu 0%

NOTE: Closed date stands for Cancell 77%, Closed date stands for Liquida 23%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NODE_ID | id | 2.9K | 0 | 240558070 15; 240558069 15; 240558068 15; 240558067 15 |
| NAME | who | 3.0K | 1 | Shampaign Investments Lim 17; Flipflop International Li 17; Mivec Limited 16; Kayché Limited 16 |
| TYPE | category | 4 | 2.1K | LIMITED LIABILITY COMPANY 881; SOLE OWNERSHIP 4; FOREIGN FORMED CORPORATIO 3 |
| INCORPORATION_DATE | date | 835 | 2.1K | 02-JUN-2016 6; 14-NOV-2014 6; 26-SEP-2014 6; 11-JUL-2013 6 |
| STRUCK_OFF_DATE | date | 40 | 2.9K | 31-DEC-2000 3; 31-DEC-2002 2; 10-SEP-2003 2; 24-JUL-2000 2 |
| CLOSED_DATE | date | 114 | 2.9K | 24-SEP-2009 3; 10-APR-2014 2; 03-MAY-2011 2; 08-APR-2011 2 |
| JURISDICTION | category | 7 | 2.0K | AW 888; VGB 62; BLZ 3; KNA 2 |
| JURISDICTION_DESCRIPTION | category | 7 | 2.0K | Aruba 888; British Virgin Islands 62; Belize 3; Nevis 2 |
| COUNTRIES | who | 63 | 2.6K | Isle of Man 105; Cayman Islands 79; United Kingdom 26; United States 24 |
| COUNTRY_CODES | other | 65 | 2.6K | IMN 105; CYM 79; GBR 26; USA 24 |
| SOURCEID | category | 7 | 0 | Paradise Papers - Appleby 2.0K; Paradise Papers - Aruba c 888; Pandora Papers - Trident  49; Pandora Papers - Overseas 11 |
| VALID_UNTIL | category | 10 | 0 | Appleby data is current t 2.0K; Aruba corporate registry  888; Provider data is current  35; Provider data is current  11 |
| NOTE | category | 3 | 2.9K | Closed date stands for Ca 90; Closed date stands for Li 27 |
| INGESTED_AT | audit | 1 | 0 | 1785965368925071 3.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 58fe6553-497a-4e22-a46d-1 3.0K |
| SRC_SHA256 | who | 1 | 0 | a47f098b1c7595fa9e4f15549 3.0K |
